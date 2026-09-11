"""Checks for the intentionally stylized architecture visibility experiment."""
from __future__ import annotations
import unittest
from analysis.mission_connectivity import build, classify, load_json
from analysis.feasibility import load_inputs, parameters_for_case, solve_point

class MissionConnectivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.summary, _ = build()

    def test_primary_counts_are_unique_mission_cases(self):
        self.assertEqual(self.summary["primary_unique_mission_cases"], 90)
        self.assertEqual(sum(self.summary["primary_state_counts"].values()), 90)

    def test_full_grid_has_no_duplicate_cases(self):
        keys = {(r["payload_id"], r["scenario"], r["separation_km"], r["dwell_min"], r["relay_altitude_m"]) for r in self.rows}
        self.assertEqual(len(keys), len(self.rows))
        self.assertEqual(len(keys), 1890)

    def test_corrected_primary_headline_counts(self):
        states = ("RELAY_BENEFICIAL_AND_FEASIBLE", "MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE",
                  "RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE", "RELAY_CONNECTIVITY_INFEASIBLE")
        for scenario, expected in (("obstructed_reference", (18, 6, 6, 60)),
                                   ("obstructed_adverse", (6, 2, 2, 80))):
            counts = self.summary["scenario_counts"][scenario]
            self.assertEqual(tuple(counts["state_counts"].get(k, 0) for k in states), expected)
            self.assertEqual(counts["carrier_counts_before_connectivity_gating"],
                             dict(finite_practical_pass=54, finite_practical_failure=18, mathematical_nonclosure=18))

    def test_classification_priority_preserves_connectivity_gate(self):
        link = dict(direct_link_ok=False, relay_link_ok=False, relay_hop_1_clear=False,
                    relay_hop_2_clear=True, direct_clear=False)
        vehicle = dict(mathematical_closed=False, practical_constraint_ok=False)
        self.assertEqual(classify(link, vehicle)[0], "RELAY_CONNECTIVITY_INFEASIBLE")
        link["direct_link_ok"] = True
        self.assertEqual(classify(link, vehicle)[0], "DIRECT_SUFFICIENT")
        link.update(direct_link_ok=False, relay_link_ok=True, relay_hop_1_clear=True)
        self.assertEqual(classify(link, vehicle)[0], "RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE")
        vehicle["mathematical_closed"] = True
        self.assertEqual(classify(link, vehicle)[0], "MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE")
        vehicle["practical_constraint_ok"] = True
        self.assertEqual(classify(link, vehicle)[0], "RELAY_BENEFICIAL_AND_FEASIBLE")

    def test_primary_power_allowance_covers_receive_and_peak(self):
        payload = next(p for p in load_json("analysis/relay-payloads.yaml")["payloads"] if p["id"] == "PAY-MESH-OEM")
        self.assertEqual(payload["dc_power_w"], payload["peak_dc_power_w"])
        self.assertGreater(payload["dc_power_w"], payload["receive_dc_power_w"])
        inputs = load_inputs()
        reference = parameters_for_case(inputs, "reference")
        for dwell in (10, 20, 30, 45, 60):
            old = solve_point(inputs, reference, dict(payload_mass_kg=payload["mass_kg"], payload_power_w=5.0, endurance_min=dwell))
            new = solve_point(inputs, reference, dict(payload_mass_kg=payload["mass_kg"], payload_power_w=payload["dc_power_w"], endurance_min=dwell))
            self.assertEqual(old["mathematical_closed"], new["mathematical_closed"])
            self.assertEqual(old["practical_constraint_ok"], new["practical_constraint_ok"])
            if new["mathematical_closed"]:
                self.assertGreater(new["gross_mass_kg"], old["gross_mass_kg"])
        self.assertEqual({r["payload_dc_power_w"] for r in self.rows if r["payload_role"] == "primary"}, {14.0})

    def test_visibility_screen_makes_altitude_causal(self):
        rows = [r for r in self.rows if r["payload_role"] == "primary" and r["scenario"] == "obstructed_reference" and r["separation_km"] == 10 and r["dwell_min"] == 10]
        by_altitude = {r["relay_altitude_m"]: r for r in rows}
        self.assertFalse(by_altitude[60.0]["relay_hop_1_clear"])
        self.assertTrue(by_altitude[60.0]["relay_hop_2_clear"])
        self.assertTrue(by_altitude[120.0]["relay_hop_1_clear"])
        self.assertEqual(by_altitude[120.0]["state"], "RELAY_BENEFICIAL_AND_FEASIBLE")

if __name__ == "__main__":
    unittest.main()