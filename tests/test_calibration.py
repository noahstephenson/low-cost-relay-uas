"""Regression checks for primary-source carrier calibration and boundaries."""

from __future__ import annotations

import csv
import io
import json
import math
import unittest

from analysis.calibration.boundaries import build as build_boundaries
from analysis.calibration.calibrate_carrier import (
    CSV_PATH,
    DATA_PATH,
    SOURCE_PATH,
    build_outputs,
    ideal_power,
)
from analysis.feasibility import analytical_closure, load_inputs, parameters_for_case, solve_point
from analysis.mission_connectivity import link_case, load_json


class CarrierCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA_PATH.read_text(encoding="utf-8-sig"))

    def test_script_reproduces_committed_csv(self):
        expected, _, _ = build_outputs()
        self.assertEqual(CSV_PATH.read_text(encoding="utf-8-sig"), expected)

    def test_every_calibration_value_has_a_registered_source(self):
        registered = {row["id"] for row in json.loads(SOURCE_PATH.read_text(encoding="utf-8-sig"))["sources"]}
        for row in self.data["vehicles"]:
            with self.subTest(row=row["id"]):
                self.assertTrue(row["source_ids"])
                self.assertLessEqual(set(row["source_ids"]), registered)
                self.assertIn("published_value", row)
                self.assertIn("condition", row)
        self.assertIn(self.data["structural_anchor"]["source_id"], registered)

    def test_held_out_errors_are_independently_recomputed(self):
        csv_text, _, diagnostics = build_outputs()
        rows = {row["vehicle_id"]: row for row in csv.DictReader(io.StringIO(csv_text))}
        effective = diagnostics["fitted"]["effective_hover_factor"]
        cfg = self.data["calibration"]
        for vehicle in (row for row in self.data["vehicles"] if row["group"] == "check"):
            weight = vehicle["mass_kg"] * cfg["gravity_m_s2"]
            ideal, _ = ideal_power(weight, vehicle["rotor_count"], vehicle["rotor_diameter_m"], cfg["air_density_kg_m3"])
            predicted = vehicle["battery_energy_wh"] / (ideal / effective + cfg["auxiliary_power_w"]) * 60.0
            error = 100.0 * (predicted - vehicle["published_hover_min"]) / vehicle["published_hover_min"]
            with self.subTest(vehicle=vehicle["id"]):
                self.assertAlmostEqual(float(rows[vehicle["id"]]["model_value"]), predicted, places=6)
                self.assertAlmostEqual(float(rows[vehicle["id"]]["percent_error"]), error, places=6)
                self.assertLessEqual(abs(error), 20.0)


class BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = build_boundaries()
        cls.mission_inputs = load_json("analysis/mission-connectivity-inputs.yaml")
        cls.payload = next(
            row for row in load_json("analysis/relay-payloads.yaml")["payloads"]
            if row["id"] == cls.mission_inputs["primary_payload_id"]
        )

    def test_link_boundary_matches_direct_margin_calculation(self):
        for name, excess in (("clear", 0.0), ("baseline", 0.0), ("plus_12_db", 12.0)):
            boundary = self.results["link_limited"][name]
            link = link_case(
                boundary["endpoint_separation_km"], 120.0, self.payload,
                self.mission_inputs["service_mode"], self.mission_inputs["geometry"], None, excess,
            )
            with self.subTest(case=name):
                self.assertAlmostEqual(min(link["relay_hop_1_margin_db"], link["relay_hop_2_margin_db"]), 0.0, places=9)

    def test_calibrated_worked_case_masses(self):
        rows = {row["dwell_min"]: row for row in self.results["worked_case"]["rows"]}
        expected = {10.0: 3.583891, 20.0: 3.583891, 30.0: 4.774732, 45.0: 15.145608}
        for dwell, mass in expected.items():
            with self.subTest(dwell=dwell):
                self.assertAlmostEqual(rows[dwell]["gross_mass_kg"], mass, places=6)
        self.assertIsNone(rows[60.0]["gross_mass_kg"])
        self.assertEqual(rows[10.0]["battery_branch"], "power")
        self.assertEqual(rows[20.0]["battery_branch"], "power")
        self.assertEqual(rows[30.0]["battery_branch"], "energy")
        self.assertEqual(rows[45.0]["battery_branch"], "energy")
        self.assertEqual(rows[60.0]["battery_branch"], "none")
    def test_endurance_boundaries_bracket_grid_and_transition(self):
        carrier_inputs = load_inputs()
        for case in ("favorable", "reference", "adverse"):
            p = parameters_for_case(carrier_inputs, case)
            boundary = self.results["endurance"][case]
            common = {"payload_mass_kg": self.payload["mass_kg"], "payload_power_w": self.payload["dc_power_w"]}
            slope_dwell = boundary["energy_slope_one_dwell_min"]
            below = analytical_closure(carrier_inputs, {**p, **common, "endurance_min": slope_dwell - 1e-5})
            above = analytical_closure(carrier_inputs, {**p, **common, "endurance_min": slope_dwell + 1e-5})
            below_slope = next(row["effective_a"] for row in below["candidates"] if row["branch"] == "energy")
            above_slope = next(row["effective_a"] for row in above["candidates"] if row["branch"] == "energy")
            self.assertLess(below_slope, 1.0)
            self.assertGreater(above_slope, 1.0)
            practical_dwell = boundary["longest_practical_dwell_min"]
            if practical_dwell is None:
                self.assertFalse(solve_point(carrier_inputs, p, {**common, "endurance_min": 0.0})["practical_constraint_ok"])
            else:
                self.assertTrue(solve_point(carrier_inputs, p, {**common, "endurance_min": practical_dwell - 1e-5})["practical_constraint_ok"])
                self.assertFalse(solve_point(carrier_inputs, p, {**common, "endurance_min": practical_dwell + 1e-5})["practical_constraint_ok"])
                grid_pass = [d for d in (10.0, 20.0, 30.0, 45.0, 60.0) if solve_point(carrier_inputs, p, {**common, "endurance_min": d})["practical_constraint_ok"]]
                self.assertLessEqual(max(grid_pass), practical_dwell)


if __name__ == "__main__":
    unittest.main()
