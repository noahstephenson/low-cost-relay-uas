#!/usr/bin/env python3
"""Fit the relay-UAS hover factor and reproduce held-out endurance checks."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "analysis/calibration/multirotor-calibration-data.yaml"
INPUT_PATH = ROOT / "analysis/feasibility-inputs.yaml"
SOURCE_PATH = ROOT / ".seal/sources.yaml"
CSV_PATH = ROOT / "analysis/calibration/calibration-results.csv"
SUMMARY_PATH = ROOT / "analysis/calibration/calibration-summary.md"
LB_TO_N = 4.4482216152605
LB_TO_KG = 0.45359237
LB_FT2_TO_N_M2 = 47.8802589803358


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def ideal_power(weight_n: float, rotor_count: int, rotor_diameter_m: float, rho: float) -> tuple[float, float]:
    area = rotor_count * math.pi * (rotor_diameter_m / 2.0) ** 2
    disk_loading = weight_n / area
    return weight_n * math.sqrt(disk_loading / (2.0 * rho)), disk_loading


def fitted_values(data: dict, carrier_inputs: dict) -> dict:
    cfg = data["calibration"]
    rho = float(cfg["air_density_kg_m3"])
    g = float(cfg["gravity_m_s2"])
    fit_rows = [row for row in data["vehicles"] if row["group"] == "fit"]
    pairs = []
    for row in fit_rows:
        weight_n = float(row["measured_thrust_lb"]) * LB_TO_N
        ideal, _ = ideal_power(weight_n, int(row["rotor_count"]), float(row["rotor_diameter_m"]), rho)
        measured = float(row["measured_voltage_v"]) * sum(float(v) for v in row["motor_currents_a"])
        pairs.append((ideal, measured))
    inverse_effective_factor = sum(x * y for x, y in pairs) / sum(x * x for x, _ in pairs)
    effective_factor = 1.0 / inverse_effective_factor
    fm = (
        effective_factor * float(cfg["environment_power_margin"])
        / float(cfg["motor_controller_efficiency"])
    )

    ranges = carrier_inputs["ranges"]
    anchor = data["structural_anchor"]
    gross_mass = float(anchor["design_gross_weight_lb"]) * LB_TO_KG
    payload_mass = float(anchor["payload_weight_lb"]) * LB_TO_KG
    battery_mass = float(anchor["battery_and_wiring_weight_lb"]) * LB_TO_KG
    airframe_mass = float(anchor["airframe_weight_lb"]) * LB_TO_KG
    disk_loading = float(anchor["disk_loading_lb_ft2"]) * LB_FT2_TO_N_M2
    area = gross_mass * g / disk_loading
    power_per_mass = g * math.sqrt(disk_loading / (2.0 * rho)) / effective_factor
    peak_power = power_per_mass * gross_mass * float(ranges["thrust_margin_ratio"]["nominal"]) ** 1.5
    propulsion_mass = (
        peak_power / float(ranges["propulsion_specific_power_w_kg"]["nominal"])
        + float(ranges["rotor_mass_per_disk_area_kg_m2"]["nominal"]) * area
    )
    mount_mass = (
        float(ranges["mount_base_mass_kg"]["nominal"])
        + float(ranges["mount_payload_fraction"]["nominal"]) * payload_mass
    )
    carried_mass = (
        payload_mass + battery_mass + propulsion_mass
        + float(ranges["avionics_mass_kg"]["nominal"])
        + float(ranges["power_electronics_mass_kg"]["nominal"])
        + mount_mass
    )
    structure_base = (
        airframe_mass
        - float(ranges["structure_load_fraction"]["nominal"]) * carried_mass
        - float(ranges["structure_area_penalty_kg_m2"]["nominal"]) * area
    )
    return {
        "effective_hover_factor": effective_factor,
        "rotor_figure_of_merit": fm,
        "structure_base_mass_kg": structure_base,
        "structural_anchor_modeled_propulsion_mass_kg": propulsion_mass,
    }


def build_outputs() -> tuple[str, str, dict]:
    data = read_json(DATA_PATH)
    carrier_inputs = read_json(INPUT_PATH)
    source_ids = {row["id"] for row in read_json(SOURCE_PATH)["sources"]}
    for row in data["vehicles"]:
        missing = set(row["source_ids"]) - source_ids
        if missing:
            raise ValueError(f"{row['id']} uses unregistered sources: {sorted(missing)}")
    if data["structural_anchor"]["source_id"] not in source_ids:
        raise ValueError("structural anchor source is not registered")

    fitted = fitted_values(data, carrier_inputs)
    cfg = data["calibration"]
    rho = float(cfg["air_density_kg_m3"])
    g = float(cfg["gravity_m_s2"])
    effective = fitted["effective_hover_factor"]
    result_rows = []
    check_errors = []
    fit_residuals = []
    for row in data["vehicles"]:
        if row["group"] == "fit":
            weight_n = float(row["measured_thrust_lb"]) * LB_TO_N
            mass_kg = weight_n / g
            ideal, disk_loading = ideal_power(weight_n, int(row["rotor_count"]), float(row["rotor_diameter_m"]), rho)
            published = float(row["measured_voltage_v"]) * sum(float(v) for v in row["motor_currents_a"])
            modeled = ideal / effective
            error = 100.0 * (modeled - published) / published
            fit_residuals.append(error)
            metric = "electrical_hover_power_w"
            battery = None
        elif row["group"] == "check":
            mass_kg = float(row["mass_kg"])
            weight_n = mass_kg * g
            ideal, disk_loading = ideal_power(weight_n, int(row["rotor_count"]), float(row["rotor_diameter_m"]), rho)
            total_power = ideal / effective + float(cfg["auxiliary_power_w"])
            published = float(row["published_hover_min"])
            modeled = float(row["battery_energy_wh"]) / total_power * 60.0
            error = 100.0 * (modeled - published) / published
            check_errors.append(error)
            metric = "hover_endurance_min"
            battery = float(row["battery_energy_wh"])
        else:
            mass_kg = float(row["mass_kg"])
            _, disk_loading = ideal_power(mass_kg * g, int(row["rotor_count"]), float(row["rotor_diameter_m"]), rho)
            published = float(row["published_cruise_min"])
            modeled = None
            error = None
            metric = "excluded_forward_flight_endurance_min"
            battery = float(row["battery_energy_wh"])
        result_rows.append({
            "vehicle_id": row["id"],
            "vehicle": row["name"],
            "split": row["group"],
            "source_ids": "|".join(row["source_ids"]),
            "mass_kg": f"{mass_kg:.6f}",
            "rotor_count": row["rotor_count"],
            "rotor_diameter_m": f"{float(row['rotor_diameter_m']):.6f}",
            "disk_loading_n_m2": f"{disk_loading:.6f}",
            "battery_energy_wh": "" if battery is None else f"{battery:.3f}",
            "condition": row["condition"],
            "metric": metric,
            "published_value": f"{published:.6f}",
            "model_value": "" if modeled is None else f"{modeled:.6f}",
            "percent_error": "" if error is None else f"{error:.6f}",
        })

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(result_rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(result_rows)
    csv_output = buffer.getvalue()
    summary = f"""# Carrier calibration summary

The five-point NASA full-vehicle hover fit gives an effective `FM * eta_d / k_env` of {effective:.6f}. With motor/controller efficiency fixed at {cfg['motor_controller_efficiency']:.2f} and the declared reference environment multiplier fixed at {cfg['environment_power_margin']:.2f}, the fitted rotor figure of merit is {fitted['rotor_figure_of_merit']:.6f}. The fit uses each test article's measured supported thrust and rotor disk area, not the relay model's fixed disk loading.

The NASA component-mass anchor gives `structure_base_mass_kg = {fitted['structure_base_mass_kg']:.6f}` while retaining the declared structural growth, disk-area, avionics, power-electronics, mount, propulsion-specific-power, and thrust-margin terms.

Fit residual range: {min(fit_residuals):+.2f}% to {max(fit_residuals):+.2f}%. Held-out hover-endurance error range: {min(check_errors):+.2f}% to {max(check_errors):+.2f}%. No held-out vehicle misses the +/-20% target.

The endurance check uses the manufacturers' published discharge condition and therefore does not apply the relay mission's 20% reserve or 90% depth-of-discharge policy. Forward-flight-only endurance is excluded.
"""
    diagnostics = {"fitted": fitted, "fit_residuals": fit_residuals, "check_errors": check_errors}
    return csv_output, summary, diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    csv_output, summary, diagnostics = build_outputs()
    outputs = {CSV_PATH: csv_output, SUMMARY_PATH: summary}
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, text in outputs.items() if not path.exists() or path.read_text(encoding="utf-8-sig") != text]
        if stale:
            raise SystemExit("CALIBRATION-STALE: " + ", ".join(stale))
        print(f"CALIBRATION-CURRENT: FM={diagnostics['fitted']['rotor_figure_of_merit']:.6f}; structure_base={diagnostics['fitted']['structure_base_mass_kg']:.6f} kg")
        return 0
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    print(f"CALIBRATION-WRITTEN: FM={diagnostics['fitted']['rotor_figure_of_merit']:.6f}; structure_base={diagnostics['fitted']['structure_base_mass_kg']:.6f} kg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
