#!/usr/bin/env python3
"""Reproducibility sweep for the revision's calibration-sensitivity numbers.

Every value here is produced by calling the existing solver functions in
analysis/calibration/calibrate_carrier.py, analysis/calibration/boundaries.py,
analysis/feasibility.py, and analysis/mission_connectivity.py with overridden
parameters. No hover-power, closure, or link-margin physics is reimplemented.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

try:
    from analysis.calibration.calibrate_carrier import (
        DATA_PATH,
        INPUT_PATH,
        compute_pairs,
        fit_effective_factor,
        fitted_values,
        fitted_values_from_effective_factor,
        ideal_power,
        read_json,
    )
    from analysis.calibration.boundaries import (
        endurance_boundaries_for_parameters,
        link_limited_separation_km,
    )
    from analysis.feasibility import load_inputs, parameters_for_case
    from analysis.mission_connectivity import (
        load_json,
        predicted_midpoint_clearance_threshold_m,
        value,
    )
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from analysis.calibration.calibrate_carrier import (
        DATA_PATH,
        INPUT_PATH,
        compute_pairs,
        fit_effective_factor,
        fitted_values,
        fitted_values_from_effective_factor,
        ideal_power,
        read_json,
    )
    from analysis.calibration.boundaries import (
        endurance_boundaries_for_parameters,
        link_limited_separation_km,
    )
    from analysis.feasibility import load_inputs, parameters_for_case
    from analysis.mission_connectivity import (
        load_json,
        predicted_midpoint_clearance_threshold_m,
        value,
    )

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "analysis/calibration/sensitivity-results.json"
PRIMARY_PAYLOAD_ID = "PAY-MESH-OEM"


def _reference_context() -> tuple[dict, dict, dict, dict, float, float]:
    data = read_json(DATA_PATH)
    carrier_inputs = read_json(INPUT_PATH)
    cfg = data["calibration"]
    rho = float(cfg["air_density_kg_m3"])
    g = float(cfg["gravity_m_s2"])
    inputs = load_inputs()
    return data, carrier_inputs, cfg, inputs, rho, g


def dax8_weight_share() -> dict:
    """DAx8's share of the unweighted least-squares fit (through the origin)."""
    data, _, cfg, _, rho, _ = _reference_context()
    pairs = compute_pairs(data, rho)
    total_sq = sum(x * x for x, _, _ in pairs)
    shares = {vid: (x * x) / total_sq for x, _, vid in pairs}
    return {
        "dax8_weight_share": shares["NASA-DAX8"],
        "all_vehicle_shares": shares,
    }


def kenv_margin_case() -> dict:
    """Applying a further 15% operating margin on top of the fitted relation."""
    _, _, _, inputs, _, g = _reference_context()
    p = parameters_for_case(inputs, "reference")
    reference_k = (
        g * p["environment_power_margin"] / (p["rotor_figure_of_merit"] * p["motor_controller_efficiency"])
        * math.sqrt(p["disk_loading_n_m2"] / (2.0 * float(inputs["constants"]["air_density_kg_m3"]["value"])))
    )
    p_margin = dict(p)
    p_margin["environment_power_margin"] = p["environment_power_margin"] * 1.15
    margin_k = (
        g * p_margin["environment_power_margin"] / (p_margin["rotor_figure_of_merit"] * p_margin["motor_controller_efficiency"])
        * math.sqrt(p_margin["disk_loading_n_m2"] / (2.0 * float(inputs["constants"]["air_density_kg_m3"]["value"])))
    )
    boundary = endurance_boundaries_for_parameters(inputs, p_margin, "kenv_operating_margin")
    return {
        "reference_k_w_kg": reference_k,
        "margin_k_w_kg": margin_k,
        "longest_practical_dwell_min": boundary["longest_practical_dwell_min"],
        "energy_slope_one_dwell_min": boundary["energy_slope_one_dwell_min"],
    }


def _boundary_with_fm_override(inputs: dict, rotor_figure_of_merit: float, label: str) -> dict:
    """Boundaries with only the hover figure-of-merit overridden.

    The structural intercept (Table components) is calibrated separately against the
    NASA 2018 conceptual-design breakdown and is held at its reference value while the
    hover-power fit itself is varied, matching how Section 3.4 separates the two
    calibrations.
    """
    p = parameters_for_case(inputs, "reference")
    p["rotor_figure_of_merit"] = rotor_figure_of_merit
    return endurance_boundaries_for_parameters(inputs, p, label)


def single_point_refits() -> dict:
    data, carrier_inputs, cfg, inputs, rho, _ = _reference_context()
    pairs = compute_pairs(data, rho)
    rows = {}
    for x, y, vehicle_id in pairs:
        effective_factor = fit_effective_factor([(x, y, vehicle_id)])
        fitted = fitted_values_from_effective_factor(effective_factor, data, carrier_inputs, cfg)
        boundary = _boundary_with_fm_override(inputs, fitted["rotor_figure_of_merit"], vehicle_id)
        rows[vehicle_id] = {
            "effective_hover_factor": effective_factor,
            "rotor_figure_of_merit": fitted["rotor_figure_of_merit"],
            "longest_practical_dwell_min": boundary["longest_practical_dwell_min"],
            "energy_slope_one_dwell_min": boundary["energy_slope_one_dwell_min"],
        }
    practical = [row["longest_practical_dwell_min"] for row in rows.values()]
    slope = [row["energy_slope_one_dwell_min"] for row in rows.values()]
    return {
        "per_vehicle": rows,
        "practical_dwell_range_min": [min(practical), max(practical)],
        "energy_slope_dwell_range_min": [min(slope), max(slope)],
    }


def estimator_variants() -> dict:
    data, carrier_inputs, cfg, inputs, rho, _ = _reference_context()
    pairs = compute_pairs(data, rho)
    per_point_factor = [x / y for x, y, _ in pairs]
    mean_ratio_factor = sum(per_point_factor) / len(per_point_factor)
    geometric_mean_factor = math.exp(sum(math.log(v) for v in per_point_factor) / len(per_point_factor))
    quads_only_pairs = [row for row in pairs if row[2] != "NASA-DAX8"]
    quads_only_factor = fit_effective_factor(quads_only_pairs)

    rows = {}
    for name, effective_factor in (
        ("mean_ratio", mean_ratio_factor),
        ("geometric_mean", geometric_mean_factor),
        ("quads_only_lsq", quads_only_factor),
    ):
        fitted = fitted_values_from_effective_factor(effective_factor, data, carrier_inputs, cfg)
        boundary = _boundary_with_fm_override(inputs, fitted["rotor_figure_of_merit"], name)
        rows[name] = {
            "effective_hover_factor": effective_factor,
            "rotor_figure_of_merit": fitted["rotor_figure_of_merit"],
            "longest_practical_dwell_min": boundary["longest_practical_dwell_min"],
            "energy_slope_one_dwell_min": boundary["energy_slope_one_dwell_min"],
        }
    practical = [row["longest_practical_dwell_min"] for row in rows.values()]
    slope = [row["energy_slope_one_dwell_min"] for row in rows.values()]
    return {
        "per_estimator": rows,
        "practical_dwell_range_min": [min(practical), max(practical)],
        "energy_slope_dwell_range_min": [min(slope), max(slope)],
    }


def coaxial_dax8_refit() -> dict:
    data, carrier_inputs, cfg, inputs, rho, _ = _reference_context()
    pairs_8_disk = compute_pairs(data, rho)
    pairs_4_disk = compute_pairs(data, rho, rotor_count_overrides={"NASA-DAX8": 4})
    dax8_ideal_4disk, dax8_measured, _ = next(row for row in pairs_4_disk if row[2] == "NASA-DAX8")
    implied_effective_factor = dax8_ideal_4disk / dax8_measured

    effective_factor = fit_effective_factor(pairs_4_disk)
    fitted = fitted_values_from_effective_factor(effective_factor, data, carrier_inputs, cfg)
    boundary = _boundary_with_fm_override(inputs, fitted["rotor_figure_of_merit"], "dax8_coaxial_4_disk")
    return {
        "implied_dax8_effective_factor": implied_effective_factor,
        "five_point_effective_factor": effective_factor,
        "rotor_figure_of_merit": fitted["rotor_figure_of_merit"],
        "longest_practical_dwell_min": boundary["longest_practical_dwell_min"],
        "energy_slope_one_dwell_min": boundary["energy_slope_one_dwell_min"],
    }


def auxiliary_power_sweep() -> dict:
    data, _, cfg, _, rho, g = _reference_context()
    pairs = compute_pairs(data, rho)
    effective_factor = fit_effective_factor(pairs)
    check_rows = [row for row in data["vehicles"] if row["group"] == "check"]
    result = {}
    for row in check_rows:
        weight_n = float(row["mass_kg"]) * g
        ideal, _ = ideal_power(weight_n, int(row["rotor_count"]), float(row["rotor_diameter_m"]), rho)
        hover_power = ideal / effective_factor
        published = float(row["published_hover_min"])
        by_aux = {}
        for aux_power_w in (0.0, 10.0, 25.0, 40.0):
            total_power = hover_power + aux_power_w
            modeled = float(row["battery_energy_wh"]) / total_power * 60.0
            error = 100.0 * (modeled - published) / published
            by_aux[str(int(aux_power_w))] = {"modeled_hover_min": modeled, "percent_error": error}
        result[row["id"]] = by_aux
    return result


def matrice4_specific_energy_case() -> dict:
    _, _, _, inputs, _, _ = _reference_context()
    m4 = next(row for row in read_json(DATA_PATH)["vehicles"] if row["id"] == "DJI-M4")
    specific_energy_wh_kg = m4["battery_energy_wh"] / m4["battery_mass_kg"]
    p = parameters_for_case(inputs, "reference")
    p["battery_specific_energy_wh_kg"] = specific_energy_wh_kg
    boundary = endurance_boundaries_for_parameters(inputs, p, "m4_specific_energy")
    return {
        "battery_energy_wh": m4["battery_energy_wh"],
        "battery_mass_kg": m4["battery_mass_kg"],
        "specific_energy_wh_kg": specific_energy_wh_kg,
        "longest_practical_dwell_min": boundary["longest_practical_dwell_min"],
        "energy_slope_one_dwell_min": boundary["energy_slope_one_dwell_min"],
    }


def check_aircraft_with_payload() -> dict:
    """Held-out check aircraft carrying the declared payload, under the reference P0 and usable fraction."""
    data, _, cfg, inputs, rho, g = _reference_context()
    pairs = compute_pairs(data, rho)
    effective_factor = fit_effective_factor(pairs)
    p = parameters_for_case(inputs, "reference")
    payload = next(
        row for row in load_json("analysis/relay-payloads.yaml")["payloads"] if row["id"] == PRIMARY_PAYLOAD_ID
    )
    p0_w = p["auxiliary_power_w"] + payload["dc_power_w"] / p["payload_regulator_efficiency"]
    usable_fraction = p["battery_depth_of_discharge"] * (1.0 - p["reserve_fraction"])
    result = {"fixed_power_w": p0_w, "usable_fraction": usable_fraction}
    for vehicle_id in ("DJI-M30", "DJI-M4"):
        row = next(item for item in data["vehicles"] if item["id"] == vehicle_id)
        gross_mass_kg = row["mass_kg"] + payload["mass_kg"]
        weight_n = gross_mass_kg * g
        ideal, _ = ideal_power(weight_n, int(row["rotor_count"]), float(row["rotor_diameter_m"]), rho)
        hover_power = ideal / effective_factor
        total_power = hover_power + p0_w
        endurance_min = usable_fraction * row["battery_energy_wh"] / total_power * 60.0
        result[vehicle_id] = {"gross_mass_kg": gross_mass_kg, "endurance_min": endurance_min}
    return result


def relay_position_optimum() -> dict:
    """Relay position fraction that maximizes the baseline link range, and its clearance threshold."""
    best_fraction, best_range_km = 0.5, link_limited_separation_km(0.0, 120.0, relay_position_fraction=0.5)[
        "endpoint_separation_km"
    ]
    fraction = 0.01
    while fraction < 1.0:
        result = link_limited_separation_km(0.0, 120.0, relay_position_fraction=fraction)
        if result["endpoint_separation_km"] > best_range_km:
            best_range_km = result["endpoint_separation_km"]
            best_fraction = fraction
        fraction = round(fraction + 0.001, 3)

    inputs = load_json("analysis/mission-connectivity-inputs.yaml")
    geometry = inputs["geometry"]
    screen = next(s for s in inputs["obstruction_scenarios"] if s["id"] == "baseline_h80_x40")
    screen_dict = {
        "top_m": value(screen["obstruction_top_m"]),
        "position_fraction": value(screen["obstruction_position_fraction"]),
    }
    optimum_geometry = {**geometry, "relay_position_fraction": {"value": best_fraction}}
    threshold_m = predicted_midpoint_clearance_threshold_m(optimum_geometry, screen_dict)
    return {
        "relay_position_fraction": best_fraction,
        "endpoint_separation_km": best_range_km,
        "clearance_threshold_m": threshold_m,
    }


def fresnel_zone_case() -> dict:
    """0.6 first-Fresnel-zone clearance threshold for the baseline 10 km, midpoint-relay case."""
    inputs = load_json("analysis/mission-connectivity-inputs.yaml")
    geometry = inputs["geometry"]
    service = inputs["service_mode"]
    screen = next(s for s in inputs["obstruction_scenarios"] if s["id"] == "baseline_h80_x40")
    relay_fraction = value(geometry["relay_position_fraction"])
    screen_fraction = value(screen["obstruction_position_fraction"])
    screen_top_m = value(screen["obstruction_top_m"])
    frequency_ghz = value(service["frequency_mhz"]) / 1000.0
    separation_km = 10.0

    hop_1_length_km = relay_fraction * separation_km
    screen_offset_km = screen_fraction * separation_km
    remaining_km = hop_1_length_km - screen_offset_km
    fresnel_radius_m = 17.3 * math.sqrt(
        screen_offset_km * remaining_km / (frequency_ghz * hop_1_length_km)
    )
    clearance_fraction = 0.6
    adjusted_top_m = screen_top_m + clearance_fraction * fresnel_radius_m

    geometry_dict = {**geometry, "relay_position_fraction": {"value": relay_fraction}}
    screen_dict = {"top_m": adjusted_top_m, "position_fraction": screen_fraction}
    threshold_m = predicted_midpoint_clearance_threshold_m(geometry_dict, screen_dict)
    return {
        "separation_km": separation_km,
        "first_fresnel_zone_radius_m": fresnel_radius_m,
        "clearance_fraction": clearance_fraction,
        "adjusted_screen_top_m": adjusted_top_m,
        "clearance_threshold_m": threshold_m,
    }


def build() -> dict:
    return {
        "dax8_weight_share": dax8_weight_share(),
        "kenv_operating_margin_case": kenv_margin_case(),
        "single_point_refits": single_point_refits(),
        "estimator_variants": estimator_variants(),
        "coaxial_dax8_refit": coaxial_dax8_refit(),
        "auxiliary_power_sweep": auxiliary_power_sweep(),
        "matrice4_specific_energy_case": matrice4_specific_energy_case(),
        "check_aircraft_with_payload": check_aircraft_with_payload(),
        "relay_position_optimum": relay_position_optimum(),
        "fresnel_zone_case": fresnel_zone_case(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text = json.dumps(build(), indent=2) + "\n"
    if args.check:
        if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text(encoding="utf-8-sig") != text:
            raise SystemExit("SENSITIVITY-RESULTS-STALE")
        print("SENSITIVITY-RESULTS-CURRENT")
        return 0
    OUTPUT_PATH.write_text(text, encoding="utf-8", newline="\n")
    print("SENSITIVITY-RESULTS-WRITTEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
