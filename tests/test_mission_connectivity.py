"""Checks for the intentionally stylized architecture visibility experiment."""
from __future__ import annotations
import unittest
from analysis.mission_connectivity import build

class MissionConnectivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.summary, _ = build()

    def test_primary_counts_are_unique_mission_cases(self):
        self.assertEqual(self.summary["primary_unique_mission_cases"], 90)
        self.assertEqual(sum(self.summary["primary_state_counts"].values()), 90)

    def test_visibility_screen_makes_altitude_causal(self):
        rows = [r for r in self.rows if r["payload_role"] == "primary" and r["scenario"] == "obstructed_reference" and r["separation_km"] == 10 and r["dwell_min"] == 10]
        by_altitude = {r["relay_altitude_m"]: r for r in rows}
        self.assertFalse(by_altitude[60.0]["relay_hop_1_clear"])
        self.assertTrue(by_altitude[60.0]["relay_hop_2_clear"])
        self.assertTrue(by_altitude[120.0]["relay_hop_1_clear"])
        self.assertEqual(by_altitude[120.0]["state"], "RELAY_BENEFICIAL_AND_FEASIBLE")

if __name__ == "__main__":
    unittest.main()