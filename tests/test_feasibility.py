"""Small scientific checks for the conceptual carrier feasibility model."""

from __future__ import annotations

import math
import unittest

from analysis.feasibility import load_inputs, parameters_for_case, solve_point


class FeasibilityModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = load_inputs()
        cls.reference = parameters_for_case(cls.inputs, "reference")

    def point(self, **overrides):
        return solve_point(self.inputs, self.reference, overrides)

    def test_units_and_hand_hover_power_case(self):
        result = self.point(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=20.0)
        self.assertGreater(result["gross_mass_kg"], 0.0)
        self.assertGreater(result["total_disk_area_m2"], 0.0)
        p = dict(self.reference)
        p.update(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=20.0)
        expected = (
            result["gross_mass_kg"] * self.inputs["constants"]["gravity_m_s2"]["value"]
            * math.sqrt(p["disk_loading_n_m2"] / (2.0 * self.inputs["constants"]["air_density_kg_m3"]["value"]))
            / (p["rotor_figure_of_merit"] * p["motor_controller_efficiency"])
            * p["environment_power_margin"]
        )
        self.assertAlmostEqual(result["propulsion_hover_power_w"], expected, places=3)

    def test_monotonic_payload_and_dwell(self):
        light = self.point(payload_mass_kg=0.25, payload_power_w=25.0, endurance_min=20.0)
        heavy = self.point(payload_mass_kg=1.0, payload_power_w=25.0, endurance_min=20.0)
        short = self.point(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=10.0)
        long = self.point(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=30.0)
        self.assertGreaterEqual(heavy["gross_mass_kg"], light["gross_mass_kg"])
        self.assertGreaterEqual(long["required_nominal_battery_energy_wh"], short["required_nominal_battery_energy_wh"])

    def test_worse_figure_of_merit_does_not_improve_power(self):
        good = self.point(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=20.0, rotor_figure_of_merit=0.70)
        poor = self.point(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=20.0, rotor_figure_of_merit=0.55)
        self.assertGreaterEqual(poor["propulsion_hover_power_w"], good["propulsion_hover_power_w"])

    def test_analytical_and_numerical_closure_agree(self):
        result = self.point(payload_mass_kg=1.0, payload_power_w=50.0, endurance_min=20.0)
        self.assertTrue(result["numerical_converged"])
        self.assertTrue(result["mathematical_closed"])
        self.assertLess(result["numerical_analytical_relative_error"], 2e-6)

    def test_energy_and_power_branches_and_transition(self):
        short = self.point(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=10.0)
        long = self.point(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=30.0)
        self.assertEqual(short["battery_sizing_driver"], "power")
        self.assertEqual(long["battery_sizing_driver"], "energy")
        drivers = {self.point(payload_mass_kg=0.5, payload_power_w=25.0, endurance_min=d)["battery_sizing_driver"] for d in (10.0, 20.0, 30.0)}
        self.assertEqual(drivers, {"power", "energy"})

    def test_nonclosure_is_not_a_practical_constraint_failure(self):
        result = self.point(payload_mass_kg=2.0, payload_power_w=100.0, endurance_min=60.0)
        self.assertFalse(result["mathematical_closed"])
        self.assertEqual(result["analytical_branch"], "none")

    def test_practical_constraint_is_distinct_from_mathematical_closure(self):
        result = self.point(payload_mass_kg=1.0, payload_power_w=50.0, endurance_min=30.0)
        self.assertTrue(result["mathematical_closed"])
        self.assertFalse(result["practical_constraint_ok"])
        self.assertTrue(result["practical_constraint_failures"])



    def test_finite_high_mass_case_reports_analytical_physical_state(self):
        result = self.point(payload_mass_kg=0.2, payload_power_w=5.0, endurance_min=45.0)
        self.assertTrue(result["mathematical_closed"])
        self.assertFalse(result["numerical_converged"])
        self.assertAlmostEqual(result["gross_mass_kg"], result["analytical_gross_mass_kg"], places=9)
        self.assertGreater(result["gross_mass_kg"], 15.0)

    def test_nonclosure_has_no_reported_physical_state(self):
        result = self.point(payload_mass_kg=0.2, payload_power_w=5.0, endurance_min=60.0)
        self.assertFalse(result["mathematical_closed"])
        self.assertEqual(result["model_state"], "NONCLOSURE")
        self.assertTrue(result["numerical_guard_exceeded"])
        self.assertIsNotNone(result["numerical_last_gross_mass_kg"])
        for field in (
            "gross_mass_kg", "battery_mass_kg", "battery_mass_fraction",
            "structure_mass_kg", "propulsion_mass_kg", "total_disk_area_m2",
            "equivalent_rotor_diameter_m", "ideal_induced_power_w",
            "propulsion_hover_power_w", "total_hover_power_w",
            "required_nominal_battery_energy_wh", "installed_nominal_battery_energy_wh",
            "peak_battery_power_w", "battery_discharge_margin", "platform_cost_usd",
            "feasibility_burden", "burden_terms", "cost_breakdown",
        ):
            self.assertIsNone(result[field], field)

    def test_finite_closure_dependent_metrics_use_analytical_state(self):
        result = self.point(payload_mass_kg=0.2, payload_power_w=5.0, endurance_min=45.0)
        self.assertTrue(result["mathematical_closed"])
        self.assertEqual(result["model_state"], "FINITE_CLOSURE")
        self.assertAlmostEqual(
            result["battery_mass_fraction"],
            result["battery_mass_kg"] / result["gross_mass_kg"],
            places=12,
        )
        self.assertAlmostEqual(
            result["battery_discharge_margin"],
            result["battery_mass_kg"] * self.reference["battery_specific_power_w_kg"]
            / result["peak_battery_power_w"],
            places=12,
        )
if __name__ == "__main__":
    unittest.main()