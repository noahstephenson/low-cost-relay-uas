"""Regression checks for the revision's calibration-sensitivity numbers.

Each assertion matches the precision the manuscript (submission/relay_uas_aeroconf.tex)
prints for that value.
"""

from __future__ import annotations

import unittest

from analysis.calibration.sensitivity import build


class SensitivityResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = build()

    def test_dax8_weight_share(self):
        self.assertAlmostEqual(self.results["dax8_weight_share"]["dax8_weight_share"], 0.794, places=3)

    def test_kenv_operating_margin_case(self):
        case = self.results["kenv_operating_margin_case"]
        self.assertAlmostEqual(case["margin_k_w_kg"], 124.7, places=1)
        self.assertAlmostEqual(case["longest_practical_dwell_min"], 35.7, places=1)
        self.assertAlmostEqual(case["energy_slope_one_dwell_min"], 44.5, places=1)

    def test_single_point_refit_band(self):
        band = self.results["single_point_refits"]
        self.assertAlmostEqual(band["practical_dwell_range_min"][0], 33.0, places=1)
        self.assertAlmostEqual(band["practical_dwell_range_min"][1], 49.2, places=1)
        self.assertAlmostEqual(band["energy_slope_dwell_range_min"][0], 41.2, places=1)
        self.assertAlmostEqual(band["energy_slope_dwell_range_min"][1], 61.3, places=1)

    def test_estimator_variant_band(self):
        band = self.results["estimator_variants"]
        self.assertAlmostEqual(band["practical_dwell_range_min"][0], 41.4, places=1)
        self.assertAlmostEqual(band["practical_dwell_range_min"][1], 44.6, places=1)
        self.assertAlmostEqual(band["energy_slope_dwell_range_min"][0], 51.5, places=1)
        self.assertAlmostEqual(band["energy_slope_dwell_range_min"][1], 55.6, places=1)

    def test_coaxial_dax8_refit(self):
        case = self.results["coaxial_dax8_refit"]
        self.assertAlmostEqual(case["implied_dax8_effective_factor"], 0.625, places=3)
        self.assertAlmostEqual(case["longest_practical_dwell_min"], 58.8, places=1)
        self.assertAlmostEqual(case["energy_slope_one_dwell_min"], 73.5, places=1)

    def test_auxiliary_power_sweep(self):
        sweep = self.results["auxiliary_power_sweep"]
        expected = {
            "DJI-M30": {"0": -1.5, "10": -3.7, "40": -9.6},
            "DJI-M4": {"0": 17.2, "10": 8.2, "40": -11.9},
            "DJI-MAVIC3M": {"0": 30.0, "10": 17.8, "40": -8.2},
        }
        for vehicle_id, levels in expected.items():
            for aux_key, error in levels.items():
                with self.subTest(vehicle=vehicle_id, aux=aux_key):
                    self.assertAlmostEqual(sweep[vehicle_id][aux_key]["percent_error"], error, places=1)

    def test_matrice4_specific_energy_case(self):
        case = self.results["matrice4_specific_energy_case"]
        self.assertAlmostEqual(case["specific_energy_wh_kg"], 248.0, delta=0.2)
        self.assertAlmostEqual(case["longest_practical_dwell_min"], 54.4, places=1)
        self.assertAlmostEqual(case["energy_slope_one_dwell_min"], 67.7, places=1)

    def test_check_aircraft_with_payload(self):
        case = self.results["check_aircraft_with_payload"]
        self.assertAlmostEqual(case["usable_fraction"], 0.72, places=2)
        self.assertAlmostEqual(case["DJI-M30"]["gross_mass_kg"], 3.97, places=2)
        self.assertAlmostEqual(case["DJI-M30"]["endurance_min"], 22.0, delta=1.0)
        self.assertAlmostEqual(case["DJI-M4"]["gross_mass_kg"], 1.42, places=2)
        self.assertAlmostEqual(case["DJI-M4"]["endurance_min"], 22.0, delta=1.0)

    def test_relay_position_optimum(self):
        case = self.results["relay_position_optimum"]
        self.assertAlmostEqual(case["relay_position_fraction"], 0.44, places=2)
        self.assertAlmostEqual(case["endpoint_separation_km"], 28.3, places=1)
        self.assertAlmostEqual(case["clearance_threshold_m"], 88.0, delta=0.5)

    def test_fresnel_zone_case(self):
        case = self.results["fresnel_zone_case"]
        self.assertAlmostEqual(case["clearance_threshold_m"], 108.0, delta=1.0)


if __name__ == "__main__":
    unittest.main()
