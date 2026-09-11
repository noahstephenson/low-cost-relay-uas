#!/usr/bin/env python3
from __future__ import annotations
import csv,json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT / "analysis"))
from feasibility import load_inputs,parameters_for_case,solve_point
ROOT=Path(__file__).resolve().parents[2]; data=json.loads((ROOT/'analysis/validation/vehicle-validation-data.yaml').read_text()); inputs=load_inputs(); p=parameters_for_case(inputs,'reference'); rows=[]
for v in data['vehicles']:
 r=solve_point(inputs,p,{'payload_mass_kg':0.5,'payload_power_w':10.0,'endurance_min':20.0}); rows.append({**v,'model_reference_gross_mass_kg':round(r['gross_mass_kg'],3),'model_reference_battery_energy_wh':round(r['installed_nominal_battery_energy_wh'],1),'model_reference_rotor_diameter_m':round(r['equivalent_rotor_diameter_m'],3),'comparison_status':'scale-only; not a calibrated prediction'})
fields=list(rows[0]); out=ROOT/'analysis/validation/vehicle-validation-results.csv';
with out.open('w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(ROOT/'analysis/validation/vehicle-validation-summary.md').write_text('# Vehicle-scale sanity check\n\nThis is an order-of-magnitude vehicle-scale sanity check, not validation of endurance or exact performance. Published vehicles differ in payload, mission profile, battery topology, propellers, and environmental conditions. The reference conceptual point is intentionally repeated only to locate the model scale relative to public multirotors.\n\n| Published vehicle | Published gross mass | Published energy | Published rotor diameter | Reference conceptual point |\n|---|---:|---:|---:|---:|\n'+''.join(f'| {r["name"]} | {r["gross_mass_kg"]} kg | {r["battery_energy_wh"]} Wh | {r["rotor_diameter_m"]} m | {r["model_reference_gross_mass_kg"]} kg |\n' for r in rows)+'\nThe comparison shows that the model produces a small-to-medium multirotor scale for its short-dwell reference case. It does **not** establish prediction accuracy, compatibility, or airworthiness.\n',encoding='utf-8')
print(f'VEHICLE-VALIDATION-WRITTEN: {len(rows)} rows')