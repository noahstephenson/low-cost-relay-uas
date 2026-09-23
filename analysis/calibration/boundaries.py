#!/usr/bin/env python3
"""Continuous link and endurance boundaries for the calibrated carrier model."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

try:
    from analysis.feasibility import analytical_closure, load_inputs, parameters_for_case, solve_point
    from analysis.mission_connectivity import load_json, value, watts_to_dbm
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from analysis.feasibility import analytical_closure, load_inputs, parameters_for_case, solve_point
    from analysis.mission_connectivity import load_json, value, watts_to_dbm

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "analysis/calibration/boundary-results.json"


def maximum_path_km(tx_dbm: float, tx_gain_dbi: float, rx_gain_dbi: float, service: dict, excess_loss_db: float) -> float:
    allowable_fspl = (
        tx_dbm + tx_gain_dbi + rx_gain_dbi
        - value(service["miscellaneous_loss_db"])
        - excess_loss_db
        - value(service["receiver_threshold_dbm"])
    )
    return 10.0 ** (
        (allowable_fspl - 32.44 - 20.0 * math.log10(value(service["frequency_mhz"]))) / 20.0
    )


def link_limited_separation_km(
    excess_loss_db: float, relay_altitude_m: float = 120.0, relay_position_fraction: float | None = None
) -> dict:
    inputs = load_json("analysis/mission-connectivity-inputs.yaml")
    payloads = load_json("analysis/relay-payloads.yaml")["payloads"]
    payload = next(row for row in payloads if row["id"] == inputs["primary_payload_id"])
    service = inputs["service_mode"]
    geometry = inputs["geometry"]
    fraction = value(geometry["relay_position_fraction"]) if relay_position_fraction is None else relay_position_fraction
    ground_altitude_km = value(geometry["ground_altitude_m"]) / 1000.0
    remote_altitude_km = value(geometry["remote_altitude_m"]) / 1000.0
    relay_altitude_km = relay_altitude_m / 1000.0
    hop_1_limit = maximum_path_km(
        value(service["ground_transmit_power_dbm"]), value(service["endpoint_gain_dbi"]),
        value(service["relay_gain_dbi"]), service, excess_loss_db,
    )
    hop_2_limit = maximum_path_km(
        watts_to_dbm(payload["rf_output_max_w"]), value(service["relay_gain_dbi"]),
        value(service["endpoint_gain_dbi"]), service, excess_loss_db,
    )

    def endpoint_limit(path_limit: float, vertical_km: float, horizontal_fraction: float) -> float:
        if path_limit <= abs(vertical_km):
            return 0.0
        return math.sqrt(path_limit ** 2 - vertical_km ** 2) / horizontal_fraction

    hop_1_endpoint = endpoint_limit(hop_1_limit, relay_altitude_km - ground_altitude_km, fraction)
    hop_2_endpoint = endpoint_limit(hop_2_limit, relay_altitude_km - remote_altitude_km, 1.0 - fraction)
    return {
        "endpoint_separation_km": min(hop_1_endpoint, hop_2_endpoint),
        "limiting_hop": "ground_to_relay" if hop_1_endpoint <= hop_2_endpoint else "relay_to_remote",
        "hop_1_path_limit_km": hop_1_limit,
        "hop_2_path_limit_km": hop_2_limit,
        "relay_altitude_m": relay_altitude_m,
        "excess_loss_db": excess_loss_db,
    }


def _bisect_transition(predicate, low: float, high: float, iterations: int = 80) -> float:
    if not predicate(low) or predicate(high):
        raise ValueError("boundary is not bracketed")
    for _ in range(iterations):
        middle = (low + high) / 2.0
        if predicate(middle):
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def endurance_boundaries_for_parameters(inputs: dict, p: dict, label: str) -> dict:
    """Practical rotor-limit and energy-slope-one dwell boundaries for arbitrary parameters.

    Shared by the named-case boundaries below and by sensitivity.py's calibration
    variants (k_env margin, single-point refits, estimator variants, coaxial DAx8,
    Matrice 4 specific-energy substitution), so every boundary in this repository is
    produced by the same bisection against the same solver functions.
    """
    payload = next(row for row in load_json("analysis/relay-payloads.yaml")["payloads"] if row["id"] == "PAY-MESH-OEM")
    overrides = {"payload_mass_kg": payload["mass_kg"], "payload_power_w": payload["dc_power_w"]}

    def practical(dwell: float) -> bool:
        return solve_point(inputs, p, {**overrides, "endurance_min": dwell})["practical_constraint_ok"]

    def energy_slope_below_one(dwell: float) -> bool:
        closure = analytical_closure(inputs, {**p, **overrides, "endurance_min": dwell})
        energy = next(row for row in closure["candidates"] if row["branch"] == "energy")
        return energy["effective_a"] < 1.0

    practical_at_zero = practical(0.0)
    practical_boundary = _bisect_transition(practical, 0.0, 240.0) if practical_at_zero else None
    nonclosure_boundary = _bisect_transition(energy_slope_below_one, 0.0, 240.0)
    return {
        "case": label,
        "longest_practical_dwell_min": practical_boundary,
        "practical_boundary_status": "bounded" if practical_at_zero else "no_practical_solution_at_zero_dwell",
        "energy_slope_one_dwell_min": nonclosure_boundary,
        "payload_mass_kg": payload["mass_kg"],
        "payload_power_w": payload["dc_power_w"],
    }


def endurance_boundaries(case: str) -> dict:
    inputs = load_inputs()
    p = parameters_for_case(inputs, case)
    return endurance_boundaries_for_parameters(inputs, p, case)


def build() -> dict:
    inputs = load_inputs()
    reference = parameters_for_case(inputs, "reference")
    payload = next(row for row in load_json("analysis/relay-payloads.yaml")["payloads"] if row["id"] == "PAY-MESH-OEM")
    worked = []
    for dwell in (10.0, 20.0, 30.0, 45.0, 60.0):
        result = solve_point(inputs, reference, {
            "payload_mass_kg": payload["mass_kg"], "payload_power_w": payload["dc_power_w"], "endurance_min": dwell,
        })
        energy_candidate = next(row for row in result["analytical_candidates"] if row["branch"] == "energy")
        worked.append({
            "dwell_min": dwell,
            "gross_mass_kg": result["gross_mass_kg"],
            "rotor_diameter_m": result["equivalent_rotor_diameter_m"],
            "battery_branch": result["analytical_branch"],
            "energy_branch_slope": energy_candidate["effective_a"],
            "mathematical_closed": result["mathematical_closed"],
            "practical_constraint_ok": result["practical_constraint_ok"],
        })
    return {
        "link_limited": {
            "clear": link_limited_separation_km(0.0),
            "baseline": link_limited_separation_km(0.0),
            "plus_12_db": link_limited_separation_km(12.0),
        },
        "endurance": {case: endurance_boundaries(case) for case in ("favorable", "reference", "adverse")},
        "worked_case": {
            "separation_km": 10.0, "relay_altitude_m": 120.0,
            "scenario": "obstructed_reference", "payload_id": payload["id"], "rows": worked,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text = json.dumps(build(), indent=2) + "\n"
    if args.check:
        if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text(encoding="utf-8-sig") != text:
            raise SystemExit("BOUNDARY-RESULTS-STALE")
        print("BOUNDARY-RESULTS-CURRENT")
        return 0
    OUTPUT_PATH.write_text(text, encoding="utf-8", newline="\n")
    print("BOUNDARY-RESULTS-WRITTEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
