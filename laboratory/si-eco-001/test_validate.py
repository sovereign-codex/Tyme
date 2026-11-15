#!/usr/bin/env python3
"""SI-ECO-001 positive and adversarial negative checks; Python stdlib only."""
import copy
import json
import unittest
from pathlib import Path
from validate import validate

FIXTURE = json.loads(Path(__file__).with_name("fixture.json").read_text(encoding="utf-8"))


class ContractTests(unittest.TestCase):
    def assertRejected(self, change, marker):
        record = copy.deepcopy(FIXTURE)
        change(record)
        errors, _ = validate(record)
        self.assertTrue(any(marker in error for error in errors), errors)

    def test_synthetic_fixture_passes(self):
        errors, compared = validate(FIXTURE)
        self.assertEqual(errors, [])
        self.assertEqual(len(compared), 1)
        self.assertEqual(compared[0]["central_delta_points"], 3)
        self.assertFalse(compared[0]["central_target_met"])
        self.assertFalse(compared[0]["real_world_effect_established"])

    def test_reject_dispatch_enabled(self):
        self.assertRejected(lambda r: r["authority"].update(dispatch_enabled=True), "authority")

    def test_reject_claim_of_execution(self):
        self.assertRejected(lambda r: r["interventions"][0].update(status="executed"), "executed or verified")

    def test_reject_false_approval(self):
        self.assertRejected(lambda r: r["interventions"][0]["authorization"].update(approved=True), "unauthorized")

    def test_reject_false_verification(self):
        self.assertRejected(lambda r: r["observations"][1].update(review_status="verified"), "cannot claim review")

    def test_reject_missing_provenance(self):
        self.assertRejected(lambda r: r["observations"][0].update(provenance={}), "provenance")

    def test_reject_unknown_feature(self):
        self.assertRejected(lambda r: r["observations"][0].update(feature_id="other-site"), "unknown feature_id")

    def test_reject_duplicate_feature(self):
        self.assertRejected(lambda r: r["features"].append(copy.deepcopy(r["features"][0])), "duplicate feature_id")

    def test_reject_bad_coordinates(self):
        self.assertRejected(lambda r: r["features"][0].update(position_m=[99, 99]), "position")

    def test_reject_georeferenced_local_coords(self):
        self.assertRejected(lambda r: r["site"]["coordinate_frame"].update(georeferenced=True), "coordinates must be explicitly local")

    def test_reject_wrong_time_order(self):
        self.assertRejected(lambda r: r["visits"][1].update(timestamp="2026-04-01T12:00:00Z"), "follow-up must occur after")

    def test_reject_nonfinite_measurement(self):
        self.assertRejected(lambda r: r["observations"][0].update(value=float("nan")), "finite value")

    def test_reject_reversed_baseline(self):
        self.assertRejected(lambda r: r["interventions"][0]["prediction"].update(baseline_observation_id="obs-followup", followup_observation_id="obs-baseline"), "role reversal")

    def test_reject_unmarked_field_data(self):
        self.assertRejected(lambda r: r.update(classification="field-unverified"), "synthetic classification")


if __name__ == "__main__":
    unittest.main(verbosity=2)
