#!/usr/bin/env python3
"""Read-only manuscript audit of the existing grid; imports no production solver.

Run from any directory. Prints JSON; does not generate or modify scientific files.
The original piecewise mass balance is solved with bracketing/bisection. This checks
numerical consistency with the declared model, not physical prediction accuracy.
"""
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    ci = read_json('analysis/feasibility-inputs.yaml')
    mi = read_json('analysis/mission-connectivity-inputs.yaml')
    payloads = {p['id']: p for p in read_json('analysis/relay-payloads.yaml')['payloads']}
    p = {k: v['nominal'] for k, v in ci['ranges'].items()}
    s = {k: v['value'] for k, v in mi['service_mode'].items()}
    g = ci['constants']['gravity_m_s2']['value']
    rho = ci['constants']['air_density_kg_m3']['value']
    n = ci['constants']['rotor_count']['value']
    q = g / p['disk_loading_n_m2']
    c = g * math.sqrt(p['disk_loading_n_m2'] / (2*rho)) * p['environment_power_margin'] / (p['rotor_figure_of_merit'] * p['motor_controller_efficiency'])
    bounds = ci['analysis_practical_boundaries']
    cache = {}

    def carrier(payload, dwell):
        key = (payload['id'], dwell)
        if key in cache:
            return cache[key]
        b0 = p['auxiliary_power_w'] + payload['dc_power_w'] / p['payload_regulator_efficiency']
        k = p['thrust_margin_ratio'] ** 1.5
        fixed = payload['mass_kg'] + p['avionics_mass_kg'] + p['power_electronics_mass_kg'] + p['mount_base_mass_kg'] + p['mount_payload_fraction'] * payload['mass_kg']
        prop = c*k / p['propulsion_specific_power_w_kg'] + p['rotor_mass_per_disk_area_kg_m2'] * q
        energy_factor = dwell / 60 / (p['battery_depth_of_discharge'] * (1-p['reserve_fraction'])) / p['battery_specific_energy_wh_kg']
        power_factor = p['battery_power_margin_ratio'] / p['battery_specific_power_w_kg']

        def residual(mass):
            energy_mass = (c*mass+b0) * energy_factor
            power_mass = (c*k*mass+b0) * power_factor
            battery = max(energy_mass, power_mass)
            total = (1+p['structure_load_fraction']) * (fixed+battery+prop*mass) + p['structure_base_mass_kg'] + p['structure_area_penalty_kg_m2']*q*mass
            return total-mass, energy_mass, power_mass

        slopes = [(1+p['structure_load_fraction'])*(prop+c*energy_factor)+p['structure_area_penalty_kg_m2']*q,
                  (1+p['structure_load_fraction'])*(prop+c*k*power_factor)+p['structure_area_penalty_kg_m2']*q]
        # Both branches have positive intercepts here. Any branch with slope >=1
        # prevents the max-of-branches residual from reaching zero at positive m.
        require(residual(0)[0] > 0, 'Audit assumes positive mass intercepts')
        if max(slopes) >= 1:
            result = (None, None, None, slopes)
        else:
            low, high = 0., 1.
            while residual(high)[0] > 0:
                high *= 2
                require(high < 1e12, 'Unexpected mass bracket; inspect assumptions')
            for _ in range(100):
                middle = (low+high)/2
                if residual(middle)[0] > 0:
                    low = middle
                else:
                    high = middle
            mass = (low+high)/2
            error, energy_mass, power_mass = residual(mass)
            require(abs(error) < 1e-9*max(1,mass), 'Mass balance failed')
            result = (mass, math.sqrt(4*q*mass/(n*math.pi)), 'energy' if energy_mass >= power_mass else 'power', slopes)
        cache[key] = result
        return result

    with (ROOT/'analysis/results/integrated-tradespace.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    summary = read_json('analysis/results/integrated-tradespace-summary.json')
    seen = set()
    grouped = {}
    worked = []
    for row in rows:
        key = tuple(row[k] for k in ('payload_id','scenario','separation_km','dwell_min','relay_altitude_m'))
        require(key not in seen, f'Duplicate: {key}')
        seen.add(key)
        D = float(row['separation_km'])*1000
        altitude = float(row['relay_altitude_m'])
        dwell = float(row['dwell_min'])
        payload = payloads[row['payload_id']]
        geom = mi['geometry']
        G = (0, geom['ground_altitude_m']['value'])
        R = (D*geom['relay_position_fraction']['value'], altitude)
        U = (D, geom['remote_altitude_m']['value'])

        def clear(a, b):
            if not row['obstruction_height_m']:
                return True
            x = float(row['obstruction_position_fraction'])*D
            if not min(a[0],b[0]) < x < max(a[0],b[0]):
                return True
            return a[1]+(x-a[0])*(b[1]-a[1])/(b[0]-a[0]) > float(row['obstruction_height_m'])

        def margin(a, b, tx, gt, gr):
            distance = math.dist(a,b)/1000
            loss = 32.44+20*math.log10(s['frequency_mhz']*distance)
            return tx+gt+gr-loss-s['miscellaneous_loss_db']-float(row['propagation_excess_loss_db'])-s['receiver_threshold_dbm']

        visibility = [clear(G,U), clear(G,R), clear(R,U)]
        margins = [margin(G,U,s['ground_transmit_power_dbm'],s['endpoint_gain_dbi'],s['endpoint_gain_dbi']),
                   margin(G,R,s['ground_transmit_power_dbm'],s['endpoint_gain_dbi'],s['relay_gain_dbi']),
                   margin(R,U,10*math.log10(payload['rf_output_max_w']*1000),s['relay_gain_dbi'],s['endpoint_gain_dbi'])]
        for column, val in zip(('direct_clear','relay_hop_1_clear','relay_hop_2_clear'), visibility):
            require(val == (row[column]=='True'), f'Visibility: {key} {column}')
        for column, val in zip(('direct_margin_db','relay_hop_1_margin_db','relay_hop_2_margin_db'), margins):
            require(abs(float(row[column])-val) <= .000501, f'Margin: {key} {column}')
        direct = visibility[0] and margins[0] >= 0
        relay = all(visibility[1:]) and min(margins[1:]) >= 0
        require(direct == (row['direct_link_ok']=='True') and relay == (row['relay_link_ok']=='True'), f'Link flags: {key}')
        mass, diameter, branch, slopes = carrier(payload,dwell)
        closed = mass is not None
        practical = closed and mass <= bounds['analysis_max_gross_mass_kg'] and diameter <= bounds['analysis_max_rotor_diameter_m'] and 2*diameter <= bounds['analysis_max_vehicle_span_m']
        require(closed == (row['vehicle_math_closed']=='True') and practical == (row['vehicle_practical_ok']=='True'), f'Carrier flags: {key}')
        if closed:
            require(abs(float(row['gross_mass_kg'])-mass) <= .0000501, f'Mass: {key}')
            require(abs(float(row['rotor_diameter_m'])-diameter) <= .0000501, f'Diameter: {key}')
        else:
            require(row['gross_mass_kg']==row['rotor_diameter_m']=='', f'Nonclosure has physical result: {key}')
        expected = ('DIRECT_SUFFICIENT' if direct else 'RELAY_CONNECTIVITY_INFEASIBLE' if not relay else
                    'RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE' if not closed else
                    'MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE' if not practical else 'RELAY_BENEFICIAL_AND_FEASIBLE')
        require(expected == row['state'], f'Classification: {key}')
        if row['payload_role']=='primary':
            grouped.setdefault(row['scenario'],[]).append(row)
            if row['scenario']=='obstructed_reference' and D==10000 and altitude==120:
                worked.append(dict(dwell_min=dwell,mass_kg=mass,rotor_diameter_m=diameter,branch=branch,branch_slopes=slopes,margins_db=margins))
    # Summary schema is discovered explicitly, never inferred from a narrative.
    primary_summary = summary['scenario_counts']
    counts = {}
    for scenario, group in grouped.items():
        require(len(group)==90, f'Denominator: {scenario}')
        counts[scenario] = dict(Counter(row['state'] for row in group))
        require(counts[scenario] == primary_summary[scenario]['state_counts'], f'Summary: {scenario}')
        carrier_counts = dict(finite_practical_pass=sum(r['vehicle_practical_ok']=='True' for r in group),
                              finite_practical_failure=sum(r['vehicle_math_closed']=='True' and r['vehicle_practical_ok']=='False' for r in group),
                              mathematical_nonclosure=sum(r['vehicle_math_closed']=='False' for r in group))
        require(carrier_counts == primary_summary[scenario]['carrier_counts_before_connectivity_gating'], f'Carrier summary: {scenario}')
        require(list(carrier_counts.values()) == [54,18,18], f'Carrier totals: {scenario}')
    baseline_maps = []
    for payload in payloads:
        baseline_maps.append({(r['separation_km'],r['dwell_min'],r['relay_altitude_m']):r['state'] for r in rows if r['payload_id']==payload and r['scenario']=='obstructed_reference'})
    require(all(m == baseline_maps[0] for m in baseline_maps), 'Secondary payload baseline boundaries differ')
    require(len(rows)==1890, 'Unexpected row count')
    hashes = {str(path.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted((ROOT/'analysis').rglob('*')) if path.is_file() and path.suffix in ('.py','.yaml','.csv','.json','.svg')}
    print(json.dumps(dict(rows_checked=len(rows),propulsion_W_per_kg=c,area_m2_per_kg=q,
                         effective_mass_limit_kg=n*math.pi*.75**2/(4*q),worked_cases=worked,
                         primary_counts=counts,scientific_file_sha256=hashes),indent=2))


if __name__ == '__main__':
    main()
