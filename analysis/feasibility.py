#!/usr/bin/env python3
"""Deterministic architecture-level Relay-UAS feasibility sweep.

The model intentionally stops at component classes. It selects no hardware and
contains no RF implementation, build, integration, or test instructions. Inputs are
JSON-compatible YAML so the standard library is sufficient.

Core equations (SI units)
-------------------------
Weight:
    W = m_gross * g

Disk area for a swept disk loading DL:
    A_total = W / DL

Ideal induced hover power from momentum theory:
    P_ideal = W^(3/2) / sqrt(2 * rho * A_total)

Estimated electrical propulsion power:
    P_prop = P_ideal / (FM * eta_drive) * k_environment

Required nominal battery energy:
    E_nominal = (P_prop + P_aux + P_payload / eta_reg) * t
                / (DoD * (1 - reserve_fraction))

Battery mass is the larger of the energy- and power-limited values:
    m_battery = max(E_nominal / specific_energy,
                    P_peak * battery_power_margin / specific_power)

The propulsion-group and structure masses depend on installed peak power, battery
mass, payload mass, and disk area. The resulting gross mass is relaxed back into the
equations until the relative mass change is below the configured tolerance. For a
fixed battery-sizing branch, constant disk loading makes this mapping affine:
``m_new = a*m + b``. The independently calculated fixed point is a verification of
this conceptual representation, not a proof of real-aircraft stability.

``reserve_fraction`` is the fraction withheld from the energy remaining after the
permitted depth-of-discharge limit. Thus usable nominal energy is
``DoD * (1 - reserve_fraction)``.
This is an architecture sensitivity model, not a certification or component-sizing
method.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "analysis" / "feasibility-inputs.yaml"
OUTPUT_DIR = ROOT / "analysis" / "results"

RESULT_FILES = {
    "summary": OUTPUT_DIR / "feasibility-summary.json",
    "grid": OUTPUT_DIR / "feasibility-grid.csv",
    "sensitivity": OUTPUT_DIR / "sensitivity-ranking.csv",
    "convergence": OUTPUT_DIR / "convergence-traces.csv",
    "region_plot": OUTPUT_DIR / "feasible-region.svg",
    "trade_plot": OUTPUT_DIR / "endurance-mass-cost.svg",
    "sensitivity_plot": OUTPUT_DIR / "sensitivity-ranking.svg",
}


def load_inputs() -> dict[str, Any]:
    return json.loads(INPUT_PATH.read_text(encoding="utf-8-sig"))


def range_value(ranges: dict[str, Any], name: str, case: str) -> float:
    item = ranges[name]
    if case == "reference":
        return float(item["nominal"])
    beneficial_high = {
        "battery_specific_energy_wh_kg",
        "battery_specific_power_w_kg",
        "battery_depth_of_discharge",
        "rotor_figure_of_merit",
        "motor_controller_efficiency",
        "propulsion_specific_power_w_kg",
        "payload_regulator_efficiency",
    }
    adverse_high = {
        "disk_loading_n_m2",
        "environment_power_margin",
        "thrust_margin_ratio",
        "rotor_mass_per_disk_area_kg_m2",
        "structure_base_mass_kg",
        "structure_load_fraction",
        "structure_area_penalty_kg_m2",
        "avionics_mass_kg",
        "power_electronics_mass_kg",
        "mount_base_mass_kg",
        "mount_payload_fraction",
        "auxiliary_power_w",
        "battery_cost_usd_per_wh",
        "propulsion_cost_usd_per_kw",
        "structure_cost_usd_per_kg",
        "avionics_cost_usd",
        "power_electronics_cost_usd",
        "mount_cost_usd",
        "other_platform_cost_usd",
        "reserve_fraction",
    }
    if name in beneficial_high:
        key = "high" if case == "favorable" else "low"
    elif name in adverse_high:
        key = "low" if case == "favorable" else "high"
    else:
        key = "nominal"
    return float(item[key])


def parameters_for_case(inputs: dict[str, Any], case: str) -> dict[str, float]:
    return {name: range_value(inputs["ranges"], name, case) for name in inputs["ranges"]}


def stable_float_tree(value: Any, significant_digits: int = 12) -> Any:
    """Normalize reported floats so generated JSON is stable across OS math libraries."""
    if isinstance(value, float):
        normalized = float(f"{value:.{significant_digits}g}")
        return 0.0 if normalized == 0.0 else normalized
    if isinstance(value, list):
        return [stable_float_tree(item, significant_digits) for item in value]
    if isinstance(value, dict):
        return {key: stable_float_tree(item, significant_digits) for key, item in value.items()}
    return value


def analytical_closure(inputs: dict[str, Any], p: dict[str, float]) -> dict[str, Any]:
    """Return the branch-consistent affine closure for the conceptual model.

    With constant disk loading, propulsion power and rotor area are linear in gross
    mass. Each battery branch is therefore affine, which permits an independent
    fixed-point check against the relaxed numerical iteration.
    """
    constants = inputs["constants"]
    g = float(constants["gravity_m_s2"]["value"])
    rho = float(constants["air_density_kg_m3"]["value"])
    area_per_mass = g / p["disk_loading_n_m2"]
    propulsion_power_per_mass = (
        g * math.sqrt(p["disk_loading_n_m2"] / (2.0 * rho))
        / (p["rotor_figure_of_merit"] * p["motor_controller_efficiency"])
        * p["environment_power_margin"]
    )
    payload_bus_power = p["payload_power_w"] / p["payload_regulator_efficiency"]
    peak_per_mass = propulsion_power_per_mass * p["thrust_margin_ratio"] ** 1.5
    peak_fixed = p["auxiliary_power_w"] + payload_bus_power
    propulsion_mass_per_mass = (
        peak_per_mass / p["propulsion_specific_power_w_kg"]
        + p["rotor_mass_per_disk_area_kg_m2"] * area_per_mass
    )
    mount_mass = p["mount_base_mass_kg"] + p["mount_payload_fraction"] * p["payload_mass_kg"]
    carried_fixed_mass = (
        p["payload_mass_kg"] + p["avionics_mass_kg"]
        + p["power_electronics_mass_kg"] + mount_mass
    )
    usable_fraction = p["battery_depth_of_discharge"] * (1.0 - p["reserve_fraction"])
    energy_per_mass = (
        propulsion_power_per_mass * p["endurance_min"] / 60.0
        / usable_fraction / p["battery_specific_energy_wh_kg"]
    )
    energy_fixed = (
        (p["auxiliary_power_w"] + payload_bus_power) * p["endurance_min"] / 60.0
        / usable_fraction / p["battery_specific_energy_wh_kg"]
    )
    power_per_mass = peak_per_mass * p["battery_power_margin_ratio"] / p["battery_specific_power_w_kg"]
    power_fixed = peak_fixed * p["battery_power_margin_ratio"] / p["battery_specific_power_w_kg"]
    candidates = []
    for branch, battery_per_mass, battery_fixed in (
        ("energy", energy_per_mass, energy_fixed),
        ("power", power_per_mass, power_fixed),
    ):
        slope = (
            (1.0 + p["structure_load_fraction"])
            * (battery_per_mass + propulsion_mass_per_mass)
            + p["structure_area_penalty_kg_m2"] * area_per_mass
        )
        intercept = (
            (1.0 + p["structure_load_fraction"]) * (carried_fixed_mass + battery_fixed)
            + p["structure_base_mass_kg"]
        )
        finite = slope < 1.0
        mass = intercept / (1.0 - slope) if finite else None
        valid = False
        if mass is not None and mass > 0.0:
            energy_mass = energy_per_mass * mass + energy_fixed
            power_mass = power_per_mass * mass + power_fixed
            valid = energy_mass >= power_mass if branch == "energy" else power_mass >= energy_mass
        candidates.append({
            "branch": branch, "effective_a": slope, "effective_b_kg": intercept,
            "analytical_gross_mass_kg": mass, "finite_closure": finite,
            "branch_consistent": valid,
        })
    selected = next((item for item in candidates if item["finite_closure"] and item["branch_consistent"]), None)
    return {
        "candidates": candidates,
        "selected": selected,
        "propulsion_power_per_mass_w_kg": propulsion_power_per_mass,
        "area_per_mass_m2_kg": area_per_mass,
    }

def solve_point(
    inputs: dict[str, Any],
    parameters: dict[str, float],
    overrides: dict[str, float] | None = None,
    capture_trace: bool = False,
) -> dict[str, Any]:
    p = dict(parameters)
    p.update(overrides or {})
    analytical = analytical_closure(inputs, p)
    constants = inputs["constants"]
    solver = inputs["solver"]
    g = float(constants["gravity_m_s2"]["value"])
    rho = float(constants["air_density_kg_m3"]["value"])
    rotor_count = int(constants["rotor_count"]["value"])
    gross = float(solver["initial_gross_mass_kg"])
    relaxation = float(solver["relaxation_factor"])
    tolerance = float(solver["relative_mass_tolerance"])
    max_iterations = int(solver["max_iterations"])
    divergence_mass = float(solver["divergence_gross_mass_kg"])
    trace: list[dict[str, float]] = []
    converged = False
    numerical_guard_exceeded = False
    reason = "maximum_iterations"

    state: dict[str, float] = {}
    for iteration in range(1, max_iterations + 1):
        weight = gross * g
        disk_area = weight / p["disk_loading_n_m2"]
        ideal_power = weight ** 1.5 / math.sqrt(2.0 * rho * disk_area)
        propulsion_hover_power = (
            ideal_power
            / (p["rotor_figure_of_merit"] * p["motor_controller_efficiency"])
            * p["environment_power_margin"]
        )
        payload_bus_power = p["payload_power_w"] / p["payload_regulator_efficiency"]
        total_hover_power = propulsion_hover_power + p["auxiliary_power_w"] + payload_bus_power
        mission_energy = total_hover_power * p["endurance_min"] / 60.0
        usable_fraction = p["battery_depth_of_discharge"] * (1.0 - p["reserve_fraction"])
        peak_propulsion_power = propulsion_hover_power * p["thrust_margin_ratio"] ** 1.5
        peak_battery_power = peak_propulsion_power + p["auxiliary_power_w"] + payload_bus_power
        required_nominal_energy = mission_energy / usable_fraction
        energy_limited_battery_mass = required_nominal_energy / p["battery_specific_energy_wh_kg"]
        power_limited_battery_mass = (
            peak_battery_power * p["battery_power_margin_ratio"]
            / p["battery_specific_power_w_kg"]
        )
        battery_mass = max(energy_limited_battery_mass, power_limited_battery_mass)
        installed_nominal_energy = battery_mass * p["battery_specific_energy_wh_kg"]
        propulsion_mass = (
            peak_propulsion_power / p["propulsion_specific_power_w_kg"]
            + p["rotor_mass_per_disk_area_kg_m2"] * disk_area
        )
        mount_mass = p["mount_base_mass_kg"] + p["mount_payload_fraction"] * p["payload_mass_kg"]
        structure_mass = (
            p["structure_base_mass_kg"]
            + p["structure_load_fraction"]
            * (p["payload_mass_kg"] + battery_mass + propulsion_mass
               + p["avionics_mass_kg"] + p["power_electronics_mass_kg"] + mount_mass)
            + p["structure_area_penalty_kg_m2"] * disk_area
        )
        calculated_gross = (
            p["payload_mass_kg"]
            + battery_mass
            + propulsion_mass
            + p["avionics_mass_kg"]
            + p["power_electronics_mass_kg"]
            + mount_mass
            + structure_mass
        )
        next_gross = relaxation * calculated_gross + (1.0 - relaxation) * gross
        relative_change = abs(next_gross - gross) / max(next_gross, 1e-9)
        state = {
            "iteration": float(iteration),
            "gross_mass_kg": next_gross,
            "battery_mass_kg": battery_mass,
            "structure_mass_kg": structure_mass,
            "propulsion_mass_kg": propulsion_mass,
            "total_disk_area_m2": disk_area,
            "ideal_induced_power_w": ideal_power,
            "propulsion_hover_power_w": propulsion_hover_power,
            "total_hover_power_w": total_hover_power,
            "required_nominal_battery_energy_wh": required_nominal_energy,
            "installed_nominal_battery_energy_wh": installed_nominal_energy,
            "energy_limited_battery_mass_kg": energy_limited_battery_mass,
            "power_limited_battery_mass_kg": power_limited_battery_mass,
            "relative_mass_change": relative_change,
        }
        if capture_trace:
            trace.append(dict(state))
        if not math.isfinite(next_gross):
            gross = next_gross
            reason = "numerical_nonfinite"
            break
        if next_gross > divergence_mass:
            numerical_guard_exceeded = True
        gross = next_gross
        if relative_change <= tolerance:
            converged = True
            reason = "converged"
            break

    if not state:
        raise RuntimeError("solver produced no state")

    peak_battery_power = (
        state["propulsion_hover_power_w"] * p["thrust_margin_ratio"] ** 1.5
        + p["auxiliary_power_w"]
        + p["payload_power_w"] / p["payload_regulator_efficiency"]
    )
    available_battery_power = state["battery_mass_kg"] * p["battery_specific_power_w_kg"]
    discharge_margin = available_battery_power / max(peak_battery_power, 1e-9)
    battery_fraction = state["battery_mass_kg"] / max(gross, 1e-9)
    rotor_diameter = math.sqrt(4.0 * state["total_disk_area_m2"] / (rotor_count * math.pi))
    vehicle_span = 2.0 * rotor_diameter
    selected_closure = analytical["selected"]
    mathematical_closed = selected_closure is not None
    analytical_mass = selected_closure["analytical_gross_mass_kg"] if selected_closure else None
    numerical_last_gross_mass = gross
    closure_relative_error = (
        abs(gross - analytical_mass) / max(analytical_mass, 1e-9)
        if converged and analytical_mass is not None else None
    )
    # A valid affine fixed point is the authoritative analytical model state. The
    # relaxed iteration remains only a verification diagnostic; a nonclosing
    # iteration is never reported as a finite carrier result.
    if mathematical_closed:
        gross = analytical_mass
        disk_area = gross * g / p["disk_loading_n_m2"]
        ideal_power = (gross * g) ** 1.5 / math.sqrt(2.0 * rho * disk_area)
        propulsion_hover_power = ideal_power / (p["rotor_figure_of_merit"] * p["motor_controller_efficiency"]) * p["environment_power_margin"]
        payload_bus_power = p["payload_power_w"] / p["payload_regulator_efficiency"]
        total_hover_power = propulsion_hover_power + p["auxiliary_power_w"] + payload_bus_power
        required_nominal_energy = total_hover_power * p["endurance_min"] / 60.0 / usable_fraction
        energy_limited_battery_mass = required_nominal_energy / p["battery_specific_energy_wh_kg"]
        peak_propulsion_power = propulsion_hover_power * p["thrust_margin_ratio"] ** 1.5
        peak_battery_power = peak_propulsion_power + p["auxiliary_power_w"] + payload_bus_power
        power_limited_battery_mass = peak_battery_power * p["battery_power_margin_ratio"] / p["battery_specific_power_w_kg"]
        battery_mass = max(energy_limited_battery_mass, power_limited_battery_mass)
        propulsion_mass = peak_propulsion_power / p["propulsion_specific_power_w_kg"] + p["rotor_mass_per_disk_area_kg_m2"] * disk_area
        structure_mass = p["structure_base_mass_kg"] + p["structure_load_fraction"] * (p["payload_mass_kg"] + battery_mass + propulsion_mass + p["avionics_mass_kg"] + p["power_electronics_mass_kg"] + mount_mass) + p["structure_area_penalty_kg_m2"] * disk_area
        state.update({"gross_mass_kg": gross, "battery_mass_kg": battery_mass, "structure_mass_kg": structure_mass, "propulsion_mass_kg": propulsion_mass, "total_disk_area_m2": disk_area, "ideal_induced_power_w": ideal_power, "propulsion_hover_power_w": propulsion_hover_power, "total_hover_power_w": total_hover_power, "required_nominal_battery_energy_wh": required_nominal_energy, "installed_nominal_battery_energy_wh": battery_mass * p["battery_specific_energy_wh_kg"], "energy_limited_battery_mass_kg": energy_limited_battery_mass, "power_limited_battery_mass_kg": power_limited_battery_mass})
        available_battery_power = battery_mass * p["battery_specific_power_w_kg"]
        discharge_margin = available_battery_power / max(peak_battery_power, 1e-9)
        battery_fraction = battery_mass / gross
        rotor_diameter = math.sqrt(4.0 * disk_area / (rotor_count * math.pi))
        vehicle_span = 2.0 * rotor_diameter
    practical = inputs.get("analysis_practical_boundaries", {})
    practical_failures = []
    if mathematical_closed and practical:
        rotor_diameter = math.sqrt(4.0 * state["total_disk_area_m2"] / (rotor_count * math.pi))
        vehicle_span = 2.0 * rotor_diameter
        if gross > float(practical["analysis_max_gross_mass_kg"]):
            practical_failures.append("gross_mass")
        if rotor_diameter > float(practical["analysis_max_rotor_diameter_m"]):
            practical_failures.append("rotor_diameter")
        if vehicle_span > float(practical["analysis_max_vehicle_span_m"]):
            practical_failures.append("vehicle_span")
    practical_ok = mathematical_closed and not practical_failures

    if mathematical_closed:
        structure_cost = 50.0 + state["structure_mass_kg"] * p["structure_cost_usd_per_kg"]
        propulsion_cost = (
            state["propulsion_hover_power_w"] * p["thrust_margin_ratio"] ** 1.5 / 1000.0
            * p["propulsion_cost_usd_per_kw"]
        )
        battery_cost = state["installed_nominal_battery_energy_wh"] * p["battery_cost_usd_per_wh"]
        cost_breakdown = {
            "structure_usd": structure_cost,
            "propulsion_usd": propulsion_cost,
            "avionics_usd": p["avionics_cost_usd"],
            "battery_usd": battery_cost,
            "power_electronics_usd": p["power_electronics_cost_usd"],
            "mount_usd": p["mount_cost_usd"],
            "other_platform_usd": p["other_platform_cost_usd"],
        }
        platform_cost = sum(cost_breakdown.values())
    else:
        cost_breakdown = None
        platform_cost = None
    boundaries = inputs["analysis_acceptance_boundaries"]
    if mathematical_closed:
        burden_terms = {
            "portability": gross / p["analysis_portability_mass_kg"],
            "cost": platform_cost / p["analysis_cost_boundary_usd"],
            "battery_fraction": battery_fraction / float(boundaries["reference_battery_mass_fraction"]),
            "discharge": float(boundaries["minimum_reference_discharge_margin"]) / discharge_margin,
        }
        feasibility_burden = max(burden_terms.values()) if converged else 10.0
        technically_closes = converged and discharge_margin >= float(
            boundaries["minimum_marginal_discharge_margin"]
        ) and battery_fraction <= float(boundaries["marginal_battery_mass_fraction"])
        if converged and all(value <= 1.0 for value in burden_terms.values()):
            conditional_class = "FEASIBLE"
        elif technically_closes and gross <= 1.5 * p["analysis_portability_mass_kg"] and platform_cost <= 2.0 * p[
            "analysis_cost_boundary_usd"
        ]:
            conditional_class = "MARGINAL"
        else:
            conditional_class = "INFEASIBLE"
    else:
        burden_terms = None
        feasibility_burden = None
        conditional_class = "INFEASIBLE"

    return {
        "converged": converged,
        "numerical_converged": converged,
        "numerical_guard_exceeded": numerical_guard_exceeded,
        "convergence_reason": reason,
        "mathematical_closed": mathematical_closed,
        "model_state": "FINITE_CLOSURE" if mathematical_closed else "NONCLOSURE",
        "analytical_branch": selected_closure["branch"] if selected_closure else "none",
        "effective_a": selected_closure["effective_a"] if selected_closure else None,
        "effective_b_kg": selected_closure["effective_b_kg"] if selected_closure else None,
        "analytical_gross_mass_kg": analytical_mass,
        "numerical_analytical_relative_error": closure_relative_error,
        "analytical_candidates": analytical["candidates"],
        "iterations": int(state["iteration"]),
        "conditional_class": conditional_class,
        "owner_requirement_class": "UNDETERMINED",
        "feasibility_burden": feasibility_burden,
        "burden_terms": burden_terms,
        "payload_mass_kg": p["payload_mass_kg"],
        "payload_power_w": p["payload_power_w"],
        "endurance_min": p["endurance_min"],
        "gross_mass_kg": gross if mathematical_closed else None,
        "numerical_last_gross_mass_kg": numerical_last_gross_mass,
        "battery_mass_kg": state["battery_mass_kg"] if mathematical_closed else None,
        "battery_mass_fraction": battery_fraction if mathematical_closed else None,
        "structure_mass_kg": state["structure_mass_kg"] if mathematical_closed else None,
        "propulsion_mass_kg": state["propulsion_mass_kg"] if mathematical_closed else None,
        "total_disk_area_m2": state["total_disk_area_m2"] if mathematical_closed else None,
        "equivalent_rotor_diameter_m": rotor_diameter if mathematical_closed else None,
        "approximate_vehicle_span_m": vehicle_span if mathematical_closed else None,
        "practical_constraint_ok": practical_ok,
        "practical_constraint_failures": practical_failures,
        "ideal_induced_power_w": state["ideal_induced_power_w"] if mathematical_closed else None,
        "propulsion_hover_power_w": state["propulsion_hover_power_w"] if mathematical_closed else None,
        "total_hover_power_w": state["total_hover_power_w"] if mathematical_closed else None,
        "required_nominal_battery_energy_wh": state["required_nominal_battery_energy_wh"] if mathematical_closed else None,
        "installed_nominal_battery_energy_wh": state["installed_nominal_battery_energy_wh"] if mathematical_closed else None,
        "battery_sizing_driver": (
            "energy"
            if state["energy_limited_battery_mass_kg"] >= state["power_limited_battery_mass_kg"]
            else "power"
        ) if mathematical_closed else "none",
        "achievable_endurance_min": (
            state["installed_nominal_battery_energy_wh"]
            * p["battery_depth_of_discharge"]
            * (1.0 - p["reserve_fraction"])
            / state["total_hover_power_w"]
            * 60.0
        ) if mathematical_closed else None,
        "peak_battery_power_w": peak_battery_power if mathematical_closed else None,
        "battery_discharge_margin": discharge_margin if mathematical_closed else None,
        "platform_cost_usd": platform_cost,
        "cost_breakdown": cost_breakdown,
        "trace": trace,
    }


def halton(index: int, base: int) -> float:
    result = 0.0
    fraction = 1.0
    while index > 0:
        fraction /= base
        index, remainder = divmod(index, base)
        result += remainder * fraction
    return result


def scale_range(item: dict[str, Any], unit_value: float) -> float:
    return float(item["low"]) + unit_value * (float(item["high"]) - float(item["low"]))


def ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    result = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        average_rank = (start + end - 1) / 2.0 + 1.0
        for position in range(start, end):
            result[order[position]] = average_rank
        start = end
    return result


def pearson(x: list[float], y: list[float]) -> float:
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    numerator = sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y))
    denominator = math.sqrt(
        sum((a - x_mean) ** 2 for a in x) * sum((b - y_mean) ** 2 for b in y)
    )
    return numerator / denominator if denominator else 0.0


def spearman(x: list[float], y: list[float]) -> float:
    return pearson(ranks(x), ranks(y))


def csv_text(rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row.get(key, "") for key in fieldnames})
    return buffer.getvalue()


def svg_document(width: int, height: int, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{title}</title>\n'
        '<desc id="desc">Generated deterministically by analysis/feasibility.py.</desc>\n'
        '<style>text{font-family:Arial,sans-serif;fill:#172033}.axis{stroke:#607089;stroke-width:1}.grid{stroke:#d9e0ea;stroke-width:1}.label{font-size:12px}.small{font-size:10px}.title{font-size:18px;font-weight:700}</style>\n'
        f'{body}\n</svg>\n'
    )


def region_svg(rows: list[dict[str, Any]], payload_power: float = 50.0) -> str:
    subset = [row for row in rows if row["case"] == "reference" and row["payload_power_w"] == payload_power]
    payloads = sorted({float(row["payload_mass_kg"]) for row in subset})
    endurances = sorted({float(row["endurance_min"]) for row in subset})
    lookup = {(float(row["payload_mass_kg"]), float(row["endurance_min"])): row for row in subset}
    colors = {"FEASIBLE": "#2f9e68", "MARGINAL": "#e6a43a", "INFEASIBLE": "#c95757"}
    text_colors = {"FEASIBLE": "#ffffff", "MARGINAL": "#172033", "INFEASIBLE": "#ffffff"}
    borders = {
        "FEASIBLE": 'stroke="#247a52" stroke-width="2"',
        "MARGINAL": 'stroke="#8a5b00" stroke-width="2" stroke-dasharray="7 4"',
        "INFEASIBLE": 'stroke="#9f2d2d" stroke-width="3"',
    }

    feasible_dwell = [
        endurance for endurance in endurances
        if any(lookup[(payload, endurance)]["conditional_class"] == "FEASIBLE" for payload in payloads)
    ]
    infeasible_dwell = [
        endurance for endurance in endurances
        if all(lookup[(payload, endurance)]["conditional_class"] == "INFEASIBLE" for payload in payloads)
    ]

    def dwell_span(values: list[float]) -> str:
        if not values:
            return "No tested dwell"
        if len(values) == 1:
            return f"{values[0]:g} min"
        return f"{min(values):g}–{max(values):g} min"

    finding = (
        f"{dwell_span(feasible_dwell)} includes feasible cases; "
        f"{dwell_span(infeasible_dwell)} is infeasible across the tested payload range."
    )
    left, top, cell_w, cell_h = 150, 175, 132, 64
    width = left + cell_w * len(endurances) + 40
    height = top + cell_h * len(payloads) + 115
    parts = [f'<rect width="{width}" height="{height}" fill="#ffffff"/>']
    parts.append('<text x="25" y="38" style="font-size:28px;font-weight:700">Exploratory Feasibility: Dwell vs Payload</text>')
    parts.append(f'<text x="25" y="74" style="font-size:17px;font-weight:700">{finding}</text>')
    parts.append('<text x="25" y="102" style="font-size:14px;fill:#536174">50 W payload demand · exploratory 10 kg / $2,500 boundaries · no hardware selected</text>')
    parts.append(f'<text x="{left + cell_w * len(endurances) / 2}" y="138" text-anchor="middle" style="font-size:16px;font-weight:700">Required on-station dwell</text>')
    parts.append(f'<text x="{left - 14}" y="160" text-anchor="end" style="font-size:14px;font-weight:700">Payload mass</text>')
    for column, endurance in enumerate(endurances):
        x = left + column * cell_w
        parts.append(f'<text x="{x + cell_w/2}" y="160" text-anchor="middle" style="font-size:14px;font-weight:700">{endurance:g} min</text>')
    for row_index, payload in enumerate(payloads):
        y = top + row_index * cell_h
        parts.append(f'<text x="{left - 14}" y="{y + cell_h/2 + 5}" text-anchor="end" style="font-size:14px">{payload:g} kg</text>')
        for column, endurance in enumerate(endurances):
            x = left + column * cell_w
            item = lookup[(payload, endurance)]
            category = item["conditional_class"]
            parts.append(f'<rect x="{x}" y="{y}" width="{cell_w-3}" height="{cell_h-3}" rx="5" fill="{colors[category]}" {borders[category]}/>')
            parts.append(f'<text x="{x + cell_w/2}" y="{y + 27}" text-anchor="middle" style="font-size:12px;font-weight:700;fill:{text_colors[category]}">{category}</text>')
            label = f'{float(item["gross_mass_kg"]):.1f} kg gross' if item["gross_mass_kg"] is not None else "NONCLOSURE"
            parts.append(f'<text x="{x + cell_w/2}" y="{y + 48}" text-anchor="middle" style="font-size:12px;fill:{text_colors[category]}">{label}</text>')
    parts.append(f'<text x="25" y="{height-64}" style="font-size:13px;font-weight:700">Cells show conditional class and finite analytical gross mass; nonclosures have no finite model state.</text>')
    parts.append(f'<text x="25" y="{height-40}" style="font-size:13px">Solid = feasible · dashed = marginal · heavy border = infeasible.</text>')
    parts.append(f'<text x="25" y="{height-18}" style="font-size:13px;fill:#536174">Owner requirements remain undecided; this is an exploratory design-space result.</text>')
    return svg_document(width, height, "\n".join(parts), "Conditional payload-endurance feasibility region")


def line_plot_svg(series: list[tuple[str, list[tuple[float, float, float]]]]) -> str:
    width, height = 820, 470
    left, right, top, bottom = 70, 760, 55, 385
    x_values = [point[0] for _, points in series for point in points]
    mass_values = [point[1] for _, points in series for point in points]
    cost_values = [point[2] for _, points in series for point in points]
    x_min, x_max = min(x_values), max(x_values)
    mass_max = max(mass_values) * 1.08
    cost_max = max(cost_values) * 1.08
    colors = ["#2266aa", "#d9822b", "#7b4ab5"]
    parts = ['<rect width="820" height="470" fill="#ffffff"/>']
    parts.append('<text x="20" y="28" class="title">Finite-closure endurance growth in mass and platform cost</text>')
    for step in range(6):
        y = bottom - (bottom - top) * step / 5
        mass_label = mass_max * step / 5
        cost_label = cost_max * step / 5
        parts.append(f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" class="grid"/>')
        parts.append(f'<text x="{left-8}" y="{y+4}" text-anchor="end" class="small">{mass_label:.1f} kg</text>')
        parts.append(f'<text x="{right+8}" y="{y+4}" class="small">${cost_label:,.0f}</text>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="axis"/>')
    parts.append(f'<line x1="{right}" y1="{top}" x2="{right}" y2="{bottom}" class="axis"/>')
    parts.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="axis"/>')
    for endurance in sorted(set(x_values)):
        x = left + (endurance - x_min) / (x_max - x_min) * (right - left)
        parts.append(f'<text x="{x}" y="{bottom+20}" text-anchor="middle" class="small">{endurance:g}</text>')
    parts.append(f'<text x="{(left+right)/2}" y="{bottom+42}" text-anchor="middle" class="label">On-station dwell (min); nonclosures omitted</text>')
    for index, (label, points) in enumerate(series):
        color = colors[index % len(colors)]
        mass_coords = []
        cost_coords = []
        for endurance, mass, cost in points:
            x = left + (endurance - x_min) / (x_max - x_min) * (right - left)
            y_mass = bottom - mass / mass_max * (bottom - top)
            y_cost = bottom - cost / cost_max * (bottom - top)
            mass_coords.append(f"{x:.1f},{y_mass:.1f}")
            cost_coords.append(f"{x:.1f},{y_cost:.1f}")
        parts.append(f'<polyline points="{" ".join(mass_coords)}" fill="none" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<polyline points="{" ".join(cost_coords)}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="7 5" opacity="0.7"/>')
        y_legend = 57 + index * 20
        parts.append(f'<line x1="490" y1="{y_legend}" x2="520" y2="{y_legend}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="528" y="{y_legend+4}" class="small">{label}: mass solid, cost dashed</text>')
    return svg_document(width, height, "\n".join(parts), "Endurance versus gross mass and platform cost")


def sensitivity_svg(rows: list[dict[str, Any]]) -> str:
    top_rows = rows[:10]
    width, height = 760, 390
    left, right, top = 230, 710, 50
    bar_h = 26
    max_score = max(float(row["overall_score"]) for row in top_rows)
    parts = ['<rect width="760" height="390" fill="#ffffff"/>']
    parts.append('<text x="20" y="28" class="title">Sensitivity ranking for conditional feasibility burden</text>')
    for index, row in enumerate(top_rows):
        y = top + index * (bar_h + 6)
        value = float(row["overall_score"])
        width_bar = (right - left) * value / max_score
        parts.append(f'<text x="{left-10}" y="{y+18}" text-anchor="end" class="small">{row["variable"]}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{width_bar:.1f}" height="{bar_h}" rx="3" fill="#3973b7"/>')
        parts.append(f'<text x="{left+width_bar+6:.1f}" y="{y+18}" class="small">{value:.3f}</text>')
    return svg_document(width, height, "\n".join(parts), "Ranked sensitivity of feasibility burden")


def nullable_round(value: float | None, digits: int) -> float | None:
    return round(value, digits) if value is not None else None

def build_outputs(inputs: dict[str, Any]) -> dict[Path, str]:
    cases = {case: parameters_for_case(inputs, case) for case in ("favorable", "reference", "adverse")}
    grid_rows: list[dict[str, Any]] = []
    for case, parameters in cases.items():
        for payload_mass in inputs["sweep"]["payload_mass_grid_kg"]:
            for payload_power in inputs["sweep"]["payload_power_grid_w"]:
                for endurance in inputs["sweep"]["endurance_grid_min"]:
                    result = solve_point(inputs, parameters, {
                        "payload_mass_kg": float(payload_mass),
                        "payload_power_w": float(payload_power),
                        "endurance_min": float(endurance),
                    })
                    grid_rows.append({
                        "case": case,
                        "payload_mass_kg": payload_mass,
                        "payload_power_w": payload_power,
                        "endurance_min": endurance,
                        "conditional_class": result["conditional_class"],
                        "model_state": result["model_state"],
                        "owner_requirement_class": result["owner_requirement_class"],
                        "converged": result["converged"],
                        "iterations": result["iterations"],
                        "gross_mass_kg": nullable_round(result["gross_mass_kg"], 6),
                        "battery_mass_kg": nullable_round(result["battery_mass_kg"], 6),
                        "battery_mass_fraction": nullable_round(result["battery_mass_fraction"], 6),
                        "total_hover_power_w": nullable_round(result["total_hover_power_w"], 6),
                        "required_nominal_battery_energy_wh": nullable_round(result["required_nominal_battery_energy_wh"], 6),
                        "installed_nominal_battery_energy_wh": nullable_round(result["installed_nominal_battery_energy_wh"], 6),
                        "battery_sizing_driver": result["battery_sizing_driver"],
                        "achievable_endurance_min": nullable_round(result["achievable_endurance_min"], 6),
                        "equivalent_rotor_diameter_m": nullable_round(result["equivalent_rotor_diameter_m"], 6),
                        "battery_discharge_margin": nullable_round(result["battery_discharge_margin"], 6),
                        "platform_cost_usd": nullable_round(result["platform_cost_usd"], 2),
                        "feasibility_burden": nullable_round(result["feasibility_burden"], 6),
                    })

    sensitivity_variables = [
        "payload_mass_kg", "payload_power_w", "endurance_min",
        "battery_specific_energy_wh_kg", "disk_loading_n_m2",
        "rotor_figure_of_merit", "motor_controller_efficiency",
        "structure_base_mass_kg", "reserve_fraction", "environment_power_margin",
        "propulsion_specific_power_w_kg", "battery_specific_power_w_kg",
        "battery_cost_usd_per_wh", "structure_load_fraction",
        "battery_power_margin_ratio", "analysis_portability_mass_kg",
        "analysis_cost_boundary_usd",
    ]
    bases = inputs["sweep"]["halton_bases"]
    sample_count = int(inputs["sweep"]["sensitivity_samples"])
    sample_inputs = {name: [] for name in sensitivity_variables}
    sample_outputs = {name: [] for name in ("gross_mass_kg", "platform_cost_usd", "feasibility_burden")}
    reference = parameters_for_case(inputs, "reference")
    for sample_index in range(1, sample_count + 1):
        overrides = {}
        for variable, base in zip(sensitivity_variables, bases):
            value = scale_range(inputs["ranges"][variable], halton(sample_index, int(base)))
            overrides[variable] = value
        result = solve_point(inputs, reference, overrides)
        if not result["mathematical_closed"]:
            continue
        for variable in sensitivity_variables:
            sample_inputs[variable].append(overrides[variable])
        for output in sample_outputs:
            sample_outputs[output].append(float(result[output]))

    sensitivity_rows = []
    for variable in sensitivity_variables:
        correlations = {
            output: spearman(sample_inputs[variable], values)
            for output, values in sample_outputs.items()
        }
        overall = math.sqrt(sum(value * value for value in correlations.values()) / len(correlations))
        sensitivity_rows.append({
            "variable": variable,
            "overall_score": round(overall, 6),
            "rho_gross_mass": round(correlations["gross_mass_kg"], 6),
            "rho_platform_cost": round(correlations["platform_cost_usd"], 6),
            "rho_feasibility_burden": round(correlations["feasibility_burden"], 6),
        })
    sensitivity_rows.sort(key=lambda row: float(row["overall_score"]), reverse=True)

    representative_points = [
        ("light_short", {"payload_mass_kg": 0.5, "payload_power_w": 25.0, "endurance_min": 20.0}),
        ("middle", {"payload_mass_kg": 1.0, "payload_power_w": 50.0, "endurance_min": 30.0}),
        ("demanding", {"payload_mass_kg": 1.5, "payload_power_w": 100.0, "endurance_min": 45.0}),
    ]
    convergence_rows = []
    representative_results = {}
    for label, overrides in representative_points:
        result = solve_point(inputs, reference, overrides, capture_trace=True)
        representative_results[label] = {key: value for key, value in result.items() if key != "trace"}
        for state in result["trace"]:
            convergence_rows.append({"point": label, **{f"numerical_{key}": round(value, 8) for key, value in state.items()}})

    class_counts: dict[str, dict[str, int]] = {}
    for case in cases:
        counts = {category: 0 for category in ("FEASIBLE", "MARGINAL", "INFEASIBLE")}
        for row in grid_rows:
            if row["case"] == case:
                counts[row["conditional_class"]] += 1
        class_counts[case] = counts

    reference_slice = [row for row in grid_rows if row["case"] == "reference" and row["payload_power_w"] == 50.0]
    endurance_series = []
    for payload in (0.5, 1.0, 1.5):
        points = []
        for endurance in inputs["sweep"]["endurance_grid_min"]:
            item = next(row for row in reference_slice if row["payload_mass_kg"] == payload and row["endurance_min"] == endurance)
            if item["gross_mass_kg"] is not None: points.append((float(endurance), float(item["gross_mass_kg"]), float(item["platform_cost_usd"])))
        endurance_series.append((f"{payload:g} kg payload", points))

    nominal_cost = representative_results["middle"]["cost_breakdown"]
    cost_ranking = sorted(nominal_cost.items(), key=lambda item: item[1], reverse=True)
    summary = {
        "analysis_id": inputs["analysis_id"],
        "model_version": inputs["model_version"],
        "parent_commit": inputs["parent_commit"],
        "approval_state": inputs["approval_state"],
        "grid_points": len(grid_rows),
        "sensitivity_samples": sample_count,
        "physical_sensitivity_samples": len(sample_outputs["gross_mass_kg"]),
        "sensitivity_nonclosures_excluded": sample_count - len(sample_outputs["gross_mass_kg"]),
        "conditional_class_counts": class_counts,
        "all_owner_requirement_dispositions": "UNDETERMINED",
        "representative_points": stable_float_tree(representative_results),
        "sensitivity_ranking": sensitivity_rows,
        "middle_point_cost_ranking": [
            {"category": category, "cost_usd": round(value, 2)} for category, value in cost_ranking
        ],
        "limitations": [
            "No owner-approved numeric target exists; FEASIBLE/MARGINAL/INFEASIBLE labels are conditional on analysis-only boundaries.",
            "NONCLOSURE means no finite analytical model state; numerical iteration diagnostics are excluded from physical result reporting and mass/cost sensitivity calculations.",
            "Payload volume, station tolerance, command-link geometry/conformance, detailed environment, and CFG-DOM sourcing are UNDETERMINED.",
            "Momentum-theory power is corrected by broad efficiency ranges but is not a substitute for rotor or vehicle test data.",
            "Structural growth and cost are parametric class-level approximations, not a stress model, supplier quote, BOM, or lifecycle-cost estimate.",
            "Platform cost excludes the black-box relay payload, external systems, labor, integration, and verification.",
            "No component, RF implementation, build, integration, or flight-test decision is made.",
        ],
    }

    grid_fields = [
        "case", "payload_mass_kg", "payload_power_w", "endurance_min",
        "conditional_class", "model_state", "owner_requirement_class", "converged", "iterations",
        "gross_mass_kg", "battery_mass_kg", "battery_mass_fraction",
        "total_hover_power_w", "required_nominal_battery_energy_wh",
        "installed_nominal_battery_energy_wh", "battery_sizing_driver",
        "achievable_endurance_min",
        "equivalent_rotor_diameter_m", "battery_discharge_margin",
        "platform_cost_usd", "feasibility_burden",
    ]
    sensitivity_fields = [
        "variable", "overall_score", "rho_gross_mass", "rho_platform_cost",
        "rho_feasibility_burden",
    ]
    convergence_fields = [
        "point", "numerical_iteration", "numerical_gross_mass_kg", "numerical_battery_mass_kg",
        "numerical_structure_mass_kg", "numerical_propulsion_mass_kg", "numerical_total_disk_area_m2",
        "numerical_ideal_induced_power_w", "numerical_propulsion_hover_power_w", "numerical_total_hover_power_w",
        "numerical_required_nominal_battery_energy_wh", "numerical_installed_nominal_battery_energy_wh",
        "numerical_energy_limited_battery_mass_kg", "numerical_power_limited_battery_mass_kg",
        "numerical_relative_mass_change",
    ]
    return {
        RESULT_FILES["summary"]: json.dumps(summary, indent=2, sort_keys=False) + "\n",
        RESULT_FILES["grid"]: csv_text(grid_rows, grid_fields),
        RESULT_FILES["sensitivity"]: csv_text(sensitivity_rows, sensitivity_fields),
        RESULT_FILES["convergence"]: csv_text(convergence_rows, convergence_fields),
        RESULT_FILES["region_plot"]: region_svg(grid_rows),
        RESULT_FILES["trade_plot"]: line_plot_svg(endurance_series),
        RESULT_FILES["sensitivity_plot"]: sensitivity_svg(sensitivity_rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if committed outputs differ from deterministic regeneration")
    args = parser.parse_args()
    inputs = load_inputs()
    outputs = build_outputs(inputs)
    if args.check:
        stale = []
        for path, expected in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8-sig") != expected:
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            print("FEASIBILITY-OUTPUTS-STALE: " + ", ".join(stale))
            return 1
        print(f"FEASIBILITY-OUTPUTS-CURRENT: {len(outputs)} deterministic artifacts")
        return 0
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"FEASIBILITY-ANALYSIS-WRITTEN: {len(outputs)} artifacts from {inputs['sweep']['sensitivity_samples']} sensitivity samples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
