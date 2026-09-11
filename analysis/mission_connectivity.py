#!/usr/bin/env python3
"""Low-order, auditable relay visibility architecture experiment."""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
from collections import Counter
from pathlib import Path

try:
    from feasibility import load_inputs, parameters_for_case, solve_point
except ModuleNotFoundError:
    from analysis.feasibility import load_inputs, parameters_for_case, solve_point

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "analysis/results"


def load_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8-sig"))


def value(item):
    return item["value"]


def fspl_db(frequency_mhz, distance_km):
    return 32.44 + 20.0 * math.log10(frequency_mhz) + 20.0 * math.log10(distance_km)


def watts_to_dbm(watts):
    return 10.0 * math.log10(watts * 1000.0)


def distance_km(point_a, point_b):
    return math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1]) / 1000.0


def visible(point_a, point_b, screen):
    """Return whether a segment clears a vertical screen that it actually crosses."""
    if screen is None:
        return True
    screen_x = screen["position_fraction_m"]
    if not min(point_a[0], point_b[0]) < screen_x < max(point_a[0], point_b[0]):
        return True
    line_height = point_a[1] + (
        (screen_x - point_a[0]) / (point_b[0] - point_a[0])
    ) * (point_b[1] - point_a[1])
    return line_height > screen["top_m"]


def link_margin_db(tx_dbm, tx_gain_dbi, rx_gain_dbi, path_km, service, excess_loss_db):
    return (
        tx_dbm
        + tx_gain_dbi
        + rx_gain_dbi
        - fspl_db(value(service["frequency_mhz"]), path_km)
        - value(service["miscellaneous_loss_db"])
        - excess_loss_db
        - value(service["receiver_threshold_dbm"])
    )


def screen_from_input(entry):
    return {
        "id": entry["id"],
        "label": entry["label"],
        "position_fraction": value(entry["obstruction_position_fraction"]),
        "top_m": value(entry["obstruction_top_m"]),
    }


def scaled_screen(screen, baseline_length_m):
    if screen is None:
        return None
    return {
        "position_fraction_m": baseline_length_m * screen["position_fraction"],
        "top_m": screen["top_m"],
    }


def predicted_midpoint_clearance_threshold_m(geometry, screen):
    """Solve the first-hop line equation for relay altitude at screen clearance."""
    ground_altitude_m = value(geometry["ground_altitude_m"])
    relay_fraction = value(geometry["relay_position_fraction"])
    return ground_altitude_m + (
        (screen["top_m"] - ground_altitude_m)
        * relay_fraction
        / screen["position_fraction"]
    )


def link_case(separation_km, relay_altitude_m, payload, service, geometry, screen, excess_loss_db):
    baseline_length_m = separation_km * 1000.0
    ground = (0.0, value(geometry["ground_altitude_m"]))
    remote = (baseline_length_m, value(geometry["remote_altitude_m"]))
    relay = (
        baseline_length_m * value(geometry["relay_position_fraction"]),
        relay_altitude_m,
    )
    scaled = scaled_screen(screen, baseline_length_m)
    direct_clear = visible(ground, remote, scaled)
    hop_1_clear = visible(ground, relay, scaled)
    hop_2_clear = visible(relay, remote, scaled)
    direct_distance = distance_km(ground, remote)
    hop_1_distance = distance_km(ground, relay)
    hop_2_distance = distance_km(relay, remote)
    direct_margin = link_margin_db(
        value(service["ground_transmit_power_dbm"]),
        value(service["endpoint_gain_dbi"]),
        value(service["endpoint_gain_dbi"]),
        direct_distance,
        service,
        excess_loss_db,
    )
    hop_1_margin = link_margin_db(
        value(service["ground_transmit_power_dbm"]),
        value(service["endpoint_gain_dbi"]),
        value(service["relay_gain_dbi"]),
        hop_1_distance,
        service,
        excess_loss_db,
    )
    hop_2_margin = link_margin_db(
        watts_to_dbm(payload["rf_output_max_w"]),
        value(service["relay_gain_dbi"]),
        value(service["endpoint_gain_dbi"]),
        hop_2_distance,
        service,
        excess_loss_db,
    )
    return {
        "direct_clear": direct_clear,
        "relay_hop_1_clear": hop_1_clear,
        "relay_hop_2_clear": hop_2_clear,
        "direct_margin_db": direct_margin,
        "relay_hop_1_margin_db": hop_1_margin,
        "relay_hop_2_margin_db": hop_2_margin,
        "direct_link_ok": direct_clear and direct_margin >= 0.0,
        "relay_link_ok": (
            hop_1_clear and hop_2_clear and hop_1_margin >= 0.0 and hop_2_margin >= 0.0
        ),
    }


def classify(link, vehicle):
    """First applicable gate wins; carrier flags retain simultaneous failures.

    FEASIBLE here means relay benefit plus exploratory physical-boundary pass,
    not the standalone carrier cost/battery-fraction class or mission approval.
    """
    if link["direct_link_ok"]:
        return "DIRECT_SUFFICIENT", "direct_link_clear_and_margin_nonnegative"
    if not link["relay_link_ok"]:
        if not link["relay_hop_1_clear"] or not link["relay_hop_2_clear"]:
            return "RELAY_CONNECTIVITY_INFEASIBLE", "relay_visibility_failure"
        mechanism = (
            "relay_visibility_restored_but_relay_link_margin_failure"
            if not link["direct_clear"]
            else "relay_link_margin_failure"
        )
        return "RELAY_CONNECTIVITY_INFEASIBLE", mechanism
    if not vehicle["mathematical_closed"]:
        return "RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE", "endurance_driven_mathematical_nonclosure"
    if not vehicle["practical_constraint_ok"]:
        return "MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE", "finite_closure_exceeds_practical_analysis_boundary"
    mechanism = (
        "direct_visibility_loss_relay_visibility_restoration"
        if not link["direct_clear"]
        else "direct_link_margin_loss_relay_link_margin_extension"
    )
    return "RELAY_BENEFICIAL_AND_FEASIBLE", mechanism


def csv_text(rows):
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def state_counts(rows):
    return dict(sorted(Counter(row["state"] for row in rows).items()))


def architecture_figure(rows, geometry, inputs):
    colors = {
        "DIRECT_SUFFICIENT": "#3973b7",
        "RELAY_BENEFICIAL_AND_FEASIBLE": "#2f9e68",
        "RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE": "#c95757",
        "MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE": "#e6a43a",
        "RELAY_CONNECTIVITY_INFEASIBLE": "#8469a9",
    }
    codes = {"DIRECT_SUFFICIENT": "DIR", "RELAY_BENEFICIAL_AND_FEASIBLE": "PASS",
             "RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE": "NC",
             "MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE": "BOUND",
             "RELAY_CONNECTIVITY_INFEASIBLE": "LINK"}
    altitudes = value(geometry["relay_altitudes_m"])
    separations = value(inputs["sweep"]["separations_km"])
    dwells = value(inputs["sweep"]["dwell_min"])
    elements = [
        '<text x="25" y="35" style="font:bold 22px Arial">Primary architecture map</text>',
        '<text x="25" y="57" style="font:11px Arial">Primary payload, baseline obstructed-reference scenario; one tile is one unique separation × dwell × altitude case.</text>',
    ]
    for panel_index, altitude in enumerate(altitudes):
        panel_x = 80 + panel_index * 330
        elements.append(
            f'<text x="{panel_x + 115}" y="82" text-anchor="middle" style="font:bold 13px Arial">{altitude:.0f} m relay altitude</text>'
        )
        for dwell_index, dwell in enumerate(dwells):
            if panel_index == 0:
                elements.append(
                    f'<text x="73" y="{121 + dwell_index * 58}" text-anchor="end" style="font:11px Arial">{dwell} min</text>'
                )
            for separation_index, separation in enumerate(separations):
                row = next(
                    item
                    for item in rows
                    if item["relay_altitude_m"] == altitude
                    and item["separation_km"] == separation
                    and item["dwell_min"] == dwell
                )
                x = panel_x + separation_index * 38
                y = 94 + dwell_index * 58
                elements.append(
                    f'<rect x="{x}" y="{y}" width="34" height="46" fill="{colors[row["state"]]}"/>'
                    f'<text x="{x + 17}" y="{y + 28}" text-anchor="middle" fill="white" style="font:9px Arial">{codes[row["state"]]}</text>'
                )
        for separation_index, separation in enumerate(separations):
            elements.append(
                f'<text x="{panel_x + separation_index * 38 + 17}" y="400" text-anchor="middle" style="font:10px Arial">{separation}</text>'
            )
    elements.append('<text x="530" y="425" text-anchor="middle" style="font:12px Arial">Endpoint separation (km); rows: on-station dwell (min)</text>')
    elements.append(
        '<text x="25" y="455" style="font:11px Arial">DIR: direct sufficient; PASS: conditional relay/physical pass; BOUND: finite but excluded; NC: mathematical nonclosure; LINK: connectivity failure.</text>'
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="480">'
        '<rect width="100%" height="100%" fill="white"/>'
        + "".join(elements)
        + "</svg>\n"
    )


def architecture_dependencies_figure():
    """Actual implemented dependencies, without an RF-to-payload sizing claim."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="420" viewBox="0 0 1040 420">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#3973b7"/></marker></defs>
<style>text{font-family:Arial;fill:#172033;font-size:14px}.box{fill:#eef3fa;stroke:#9eb4cf}.arrow{stroke:#3973b7;stroke-width:2;fill:none;marker-end:url(#arrow)}</style>
<rect width="100%" height="100%" fill="white"/>
<text x="25" y="35" style="font-size:22px;font-weight:bold">Implemented architecture screening dependencies</text>
<rect class="box" x="25" y="70" width="300" height="60"/><text x="40" y="95">Geometry / visibility / service assumptions</text><text x="40" y="116">and fixed payload RF output</text>
<rect class="box" x="25" y="220" width="300" height="60"/><text x="40" y="245">Fixed payload mass / constant DC demand</text><text x="40" y="266">and dwell / carrier assumptions</text>
<rect class="box" x="390" y="70" width="250" height="60"/><text x="405" y="95">Direct and relay connectivity</text><text x="405" y="116">Visibility gate + link margins</text>
<rect class="box" x="390" y="210" width="250" height="80"/><text x="405" y="234">Carrier mass-power-energy closure</text><text x="405" y="256">Analytical state + exploratory</text><text x="405" y="278">physical-boundary checks</text>
<rect class="box" x="735" y="145" width="280" height="90"/><text x="750" y="170">Hierarchical architecture classification</text><text x="750" y="192">Benefit / connectivity failure /</text><text x="750" y="214">finite exclusion / nonclosure</text>
<path class="arrow" d="M325 100H390"/><path class="arrow" d="M325 250H390"/>
<path class="arrow" d="M640 100H690V168H735"/><path class="arrow" d="M640 250H690V214H735"/>
<text x="25" y="335">Payload inputs are shared assumptions: link margin does not resize equipment or electrical demand.</text>
<text x="25" y="360">Altitude changes connectivity, not constant-density hover power. Numerical convergence is a diagnostic.</text>
<text x="25" y="385">Stationary, one-way screening; no full-mission or validated-aircraft feasibility claim.</text>
</svg>
'''


def build():
    inputs = load_json("analysis/mission-connectivity-inputs.yaml")
    payloads = load_json("analysis/relay-payloads.yaml")["payloads"]
    service = inputs["service_mode"]
    geometry = inputs["geometry"]
    sweep = inputs["sweep"]
    screens = [screen_from_input(entry) for entry in inputs["obstruction_scenarios"]]
    baseline_screen = next(screen for screen in screens if screen["id"] == "baseline_h80_x40")
    carrier_inputs = load_inputs()
    reference_carrier = parameters_for_case(carrier_inputs, "reference")
    runs = [
        ("clear_reference", None, 0.0),
        ("obstructed_reference", baseline_screen, 0.0),
        ("obstructed_adverse", baseline_screen, value(service["adverse_excess_loss_db"])),
    ] + [
        (f"obstruction_sensitivity_{screen['id']}", screen, 0.0)
        for screen in screens
        if screen["id"] != baseline_screen["id"]
    ]
    rows = []
    for payload in payloads:
        role = "primary" if payload["id"] == inputs["primary_payload_id"] else "secondary_sensitivity"
        for run_name, screen, excess_loss_db in runs:
            for altitude in value(geometry["relay_altitudes_m"]):
                for separation in value(sweep["separations_km"]):
                    for dwell in value(sweep["dwell_min"]):
                        link = link_case(
                            separation, altitude, payload, service, geometry, screen, excess_loss_db
                        )
                        vehicle = solve_point(
                            carrier_inputs,
                            reference_carrier,
                            {
                                "payload_mass_kg": payload["mass_kg"],
                                "payload_power_w": payload["dc_power_w"],
                                "endurance_min": dwell,
                            },
                        )
                        state, mechanism = classify(link, vehicle)
                        rows.append({
                            "payload_id": payload["id"],
                            "payload_role": role,
                            "scenario": run_name,
                            "obstruction_scenario_id": screen["id"] if screen else "none",
                            "obstruction_height_m": screen["top_m"] if screen else None,
                            "obstruction_position_fraction": screen["position_fraction"] if screen else None,
                            "propagation_excess_loss_db": excess_loss_db,
                            "separation_km": separation,
                            "dwell_min": dwell,
                            "relay_altitude_m": altitude,
                            "direct_clear": link["direct_clear"],
                            "relay_hop_1_clear": link["relay_hop_1_clear"],
                            "relay_hop_2_clear": link["relay_hop_2_clear"],
                            "direct_margin_db": round(link["direct_margin_db"], 3),
                            "relay_hop_1_margin_db": round(link["relay_hop_1_margin_db"], 3),
                            "relay_hop_2_margin_db": round(link["relay_hop_2_margin_db"], 3),
                            "direct_link_ok": link["direct_link_ok"],
                            "relay_link_ok": link["relay_link_ok"],
                            "payload_mass_kg": payload["mass_kg"],
                            "payload_dc_power_w": payload["dc_power_w"],
                            "vehicle_numerical_converged": vehicle["numerical_converged"],
                            "vehicle_numerical_guard": vehicle["numerical_guard_exceeded"],
                            "vehicle_math_closed": vehicle["mathematical_closed"],
                            "vehicle_practical_ok": vehicle["practical_constraint_ok"],
                            "vehicle_practical_failures": "|".join(vehicle["practical_constraint_failures"]),
                            "gross_mass_kg": round(vehicle["gross_mass_kg"], 4) if vehicle["gross_mass_kg"] is not None else None,
                            "rotor_diameter_m": round(vehicle["equivalent_rotor_diameter_m"], 4) if vehicle["equivalent_rotor_diameter_m"] is not None else None,
                            "state": state,
                            "boundary_mechanism": mechanism,
                        })

    primary_baseline = [
        row for row in rows
        if row["payload_role"] == "primary" and row["scenario"] == "obstructed_reference"
    ]
    primary_run_counts = {
        run_name: {
            "unique_mission_cases": len([
                row for row in rows
                if row["payload_role"] == "primary" and row["scenario"] == run_name
            ]),
            "carrier_counts_before_connectivity_gating": {
                "finite_practical_pass": sum(r["vehicle_practical_ok"] for r in rows if r["payload_role"] == "primary" and r["scenario"] == run_name),
                "finite_practical_failure": sum(r["vehicle_math_closed"] and not r["vehicle_practical_ok"] for r in rows if r["payload_role"] == "primary" and r["scenario"] == run_name),
                "mathematical_nonclosure": sum(not r["vehicle_math_closed"] for r in rows if r["payload_role"] == "primary" and r["scenario"] == run_name),
            },
            "state_counts": state_counts([
                row for row in rows
                if row["payload_role"] == "primary" and row["scenario"] == run_name
            ]),
        }
        for run_name, _, _ in runs
    }
    sensitivity_rows = []
    for screen in screens:
        run_name = "obstructed_reference" if screen["id"] == baseline_screen["id"] else f"obstruction_sensitivity_{screen['id']}"
        run_rows = [
            row for row in rows
            if row["payload_role"] == "primary" and row["scenario"] == run_name
        ]
        visibility = {}
        for altitude in value(geometry["relay_altitudes_m"]):
            altitude_rows = [row for row in run_rows if row["relay_altitude_m"] == altitude]
            visibility[altitude] = all(row["relay_hop_1_clear"] for row in altitude_rows)
        sensitivity_rows.append({
            "obstruction_scenario": screen["id"],
            "obstruction_label": screen["label"],
            "obstruction_height_m": screen["top_m"],
            "obstruction_position_fraction": screen["position_fraction"],
            "predicted_midpoint_clearance_threshold_m": round(
                predicted_midpoint_clearance_threshold_m(geometry, screen), 3
            ),
            "relay_60m_hop_1_visible": visibility[60.0],
            "relay_120m_hop_1_visible": visibility[120.0],
            "relay_240m_hop_1_visible": visibility[240.0],
            "architecture_state_counts": json.dumps(state_counts(run_rows), sort_keys=True),
        })

    summary = {
        "classification_order": ["DIRECT_SUFFICIENT", "RELAY_CONNECTIVITY_INFEASIBLE", "RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE", "MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE", "RELAY_BENEFICIAL_AND_FEASIBLE"],
        "primary_payload_id": inputs["primary_payload_id"],
        "primary_architecture_scenario": "obstructed_reference",
        "primary_unique_mission_cases": len(primary_baseline),
        "primary_state_counts": state_counts(primary_baseline),
        "scenario_counts": primary_run_counts,
        "obstruction_sensitivity": sensitivity_rows,
        "secondary_payload_sensitivity_obstructed_reference": {
            payload["id"]: state_counts([
                row for row in rows
                if row["payload_id"] == payload["id"] and row["scenario"] == "obstructed_reference"
            ])
            for payload in payloads
        },
        "limitations": [
            "Exported margins are hypothetical unobstructed-path values; a blocked path always fails regardless of margin.",
            "Hierarchical state counts assign one label per mission case, not independent failure frequencies or probabilities; carrier flags retain simultaneous failures.",
            "FEASIBLE denotes relay benefit and exploratory physical-boundary pass, not standalone carrier acceptance or operational mission feasibility.",
            "Stationary one-way Ground-to-Relay-to-Remote screening; no transit, recovery, reverse link, control-link assessment, or throughput prediction.",
            "Payload mass and constant DC demand drive carrier sizing; link margin does not resize the payload. Altitude affects links, not constant-density hover sizing.",
            "Payload peak_dc_power_w is source metadata, not an additional solver load. Primary dc_power_w already uses the published peak continuously; secondary DC assumptions remain exploratory.",
            "Screens are stylized visibility scenarios, not terrain prediction.",
            "Payload alternatives are sensitivity cases, not mission counts.",
            "Adverse result is bounded 12 dB sensitivity, not propagation prediction.",
            "The carrier practical mass, rotor-diameter, and footprint boundaries are exploratory analysis boundaries.",
        ],
    }
    outputs = {
        OUTPUTS / "integrated-tradespace.csv": csv_text(rows),
        OUTPUTS / "integrated-tradespace-summary.json": json.dumps(summary, indent=2) + "\n",
        OUTPUTS / "obstruction-sensitivity.csv": csv_text(sensitivity_rows),
        OUTPUTS / "architecture-causal-chain.svg": architecture_dependencies_figure(),
        OUTPUTS / "architecture-tradespace.svg": architecture_figure(primary_baseline, geometry, inputs),
        OUTPUTS / "mission-connectivity-benefit.svg": architecture_figure(primary_baseline, geometry, inputs),
    }
    return rows, summary, outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    rows, summary, outputs = build()
    if arguments.check:
        stale = [
            str(path.relative_to(ROOT))
            for path, text in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8-sig") != text
        ]
        if stale:
            raise SystemExit("MISSION-ANALYSIS-STALE: " + ", ".join(stale))
        print(
            "MISSION-ANALYSIS-CURRENT: "
            f"{summary['primary_unique_mission_cases']} primary unique mission cases; "
            f"{len(rows)} row-level results"
        )
        return
    OUTPUTS.mkdir(exist_ok=True)
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
    print(
        "MISSION-ANALYSIS-WRITTEN: "
        f"{summary['primary_unique_mission_cases']} primary unique mission cases; "
        f"{len(rows)} row-level results"
    )


if __name__ == "__main__":
    main()