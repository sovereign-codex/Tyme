#!/usr/bin/env python3
"""Dependency-free semantic validator for SI-ECO-001 synthetic records.

Does not authorize or undertake any real field actions. Includes checks that
JSON Schema alone cannot express, such as identity references and time order.
"""
import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

EXPECTED_TOP = {"schema", "schema_version", "record_id", "classification", "authority", "site", "features", "visits", "observations", "interventions", "limitations"}


def timestamp(value):
    if not isinstance(value, str) or not value:
        raise ValueError("missing timestamp")
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must include timezone")
    return parsed


def finite_number(value, lo=None, hi=None):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and (lo is None or value >= lo)
            and (hi is None or value <= hi))


def validate(record):
    errors = []

    def fail(msg):
        errors.append(msg)

    if not isinstance(record, dict):
        return ["root: expected JSON object"], None
    if set(record) != EXPECTED_TOP:
        fail("root: missing/extra keys: " + ", ".join(sorted(set(record) ^ EXPECTED_TOP)))
    if record.get("schema") != "org.tyme.eco.site-record" or record.get("schema_version") != "0.1.0":
        fail("root: incompatible schema or version")
    if record.get("classification") != "synthetic":
        fail("root: v0.1 only supports synthetic classification")
    if not isinstance(record.get("record_id"), str) or not record.get("record_id"):
        fail("root: record_id required")
    auth = record.get("authority", {})
    if not isinstance(auth, dict) or auth != {"mode": "read-only-experiment", "field_action_enabled": False,
                                             "dispatch_enabled": False, "credentials_loaded": False,
                                             "institutional_effect": "none"}:
        fail("authority: non-authorizing invariant violated")
    site = record.get("site", {})
    frame = site.get("coordinate_frame", {}) if isinstance(site, dict) else {}
    if not isinstance(site, dict) or not isinstance(site.get("site_id"), str) or not site.get("site_id") or not isinstance(site.get("label"), str) or not site.get("label") or site.get("site_kind") != "hypothetical_landscape":
        fail("site: expected labeled hypothetical site")
    if not isinstance(frame, dict) or frame.get("kind") != "local-cartesian-meters" or frame.get("georeferenced") is not False:
        fail("site: coordinates must be explicitly local, not georeferenced")
    width, height = frame.get("width_m"), frame.get("height_m")
    if not finite_number(width, 0) or not finite_number(height, 0) or width == 0 or height == 0:
        fail("site: width_m and height_m must be positive finite numbers")
    if not isinstance(frame.get("origin_description"), str) or not frame.get("origin_description"):
        fail("site: origin_description required")

    features = record.get("features")
    if not isinstance(features, list) or not features:
        fail("features: expected nonempty array")
        features = []
    feature_ids = set()
    for f in features:
        if not isinstance(f, dict):
            fail("features: entry must be object")
            continue
        fid = f.get("feature_id")
        if not isinstance(fid, str) or not fid or fid in feature_ids:
            fail("features: missing or duplicate feature_id")
        else:
            feature_ids.add(fid)
        if f.get("kind") not in {"tree", "plant", "soil_plot", "drainage", "irrigation", "structure"}:
            fail(f"features/{fid}: invalid kind")
        if f.get("identification_status") not in {"unverified", "not_applicable"}:
            fail(f"features/{fid}: unsupported identification claim")
        pos = f.get("position_m")
        if (not isinstance(pos, list) or len(pos) != 2 or not all(finite_number(v) for v in pos)
                or (finite_number(width) and (pos[0] < 0 or pos[0] > width))
                or (finite_number(height) and (pos[1] < 0 or pos[1] > height))):
            fail(f"features/{fid}: position outside local site or malformed")

    visits = record.get("visits")
    if not isinstance(visits, list) or len(visits) < 2:
        fail("visits: expected baseline and synthetic counterfactual follow-up")
        visits = []
    visit_map = {}
    for v in visits:
        if not isinstance(v, dict):
            fail("visits: entry must be object")
            continue
        vid = v.get("visit_id")
        if not isinstance(vid, str) or not vid or vid in visit_map:
            fail("visits: missing or duplicate visit_id")
            continue
        if v.get("role") not in {"synthetic_baseline", "synthetic_counterfactual_followup"}:
            fail(f"visits/{vid}: invalid synthetic role")
        try:
            t = timestamp(v.get("timestamp"))
        except (ValueError, TypeError):
            fail(f"visits/{vid}: invalid timestamp")
            t = None
        visit_map[vid] = (v.get("role"), t)

    observations = record.get("observations")
    if not isinstance(observations, list) or len(observations) < 2:
        fail("observations: expected baseline and follow-up")
        observations = []
    obs_map = {}
    for o in observations:
        if not isinstance(o, dict):
            fail("observations: entry must be object")
            continue
        oid, vid, fid = o.get("observation_id"), o.get("visit_id"), o.get("feature_id")
        if not isinstance(oid, str) or not oid or oid in obs_map:
            fail("observations: missing or duplicate observation_id")
            continue
        obs_map[oid] = o
        if fid not in feature_ids or vid not in visit_map:
            fail(f"observations/{oid}: unknown feature_id or visit_id")
        if o.get("metric") != "soil_moisture_volumetric_pct" or o.get("unit") != "percent":
            fail(f"observations/{oid}: unsupported metric/unit")
        if not finite_number(o.get("value"), 0, 100) or not finite_number(o.get("uncertainty_abs"), 0, 100):
            fail(f"observations/{oid}: invalid finite value or uncertainty")
        if o.get("sampling_role") not in {"baseline", "counterfactual_followup"}:
            fail(f"observations/{oid}: unknown sampling role")
        expected_visit_role = {"baseline": "synthetic_baseline", "counterfactual_followup": "synthetic_counterfactual_followup"}.get(o.get("sampling_role"))
        if vid in visit_map and visit_map[vid][0] != expected_visit_role:
            fail(f"observations/{oid}: sampling role contradicts visit")
        prov = o.get("provenance", {})
        if not isinstance(prov, dict) or prov.get("source_kind") != "synthetic" or prov.get("method") != "fabricated_training_fixture" or not isinstance(prov.get("source_id"), str) or not prov.get("source_id"):
            fail(f"observations/{oid}: missing/false provenance")
        if o.get("review_status") != "unreviewed":
            fail(f"observations/{oid}: fabricated fixture cannot claim review/verification")

    interventions = record.get("interventions")
    if not isinstance(interventions, list) or not interventions:
        fail("interventions: expected at least one simulation")
        interventions = []
    seen_int = set()
    comparisons = []
    for i in interventions:
        if not isinstance(i, dict):
            fail("interventions: entry must be object")
            continue
        iid, fid = i.get("intervention_id"), i.get("feature_id")
        if not isinstance(iid, str) or not iid or iid in seen_int:
            fail("interventions: missing or duplicate intervention_id")
            continue
        seen_int.add(iid)
        if fid not in feature_ids:
            fail(f"interventions/{iid}: unknown feature_id")
        if i.get("status") != "simulated_only" or i.get("outcome_classification") != "synthetic_counterfactual_only":
            fail(f"interventions/{iid}: cannot claim executed or verified outcome")
        if i.get("authorization") != {"approved": False, "actor": None}:
            fail(f"interventions/{iid}: unauthorized field action claim")
        p = i.get("prediction", {})
        if not isinstance(p, dict):
            fail(f"interventions/{iid}: missing prediction")
            continue
        aid, bid = p.get("baseline_observation_id"), p.get("followup_observation_id")
        if p.get("metric") != "soil_moisture_volumetric_pct" or not finite_number(p.get("minimum_delta_points"), 0, 100):
            fail(f"interventions/{iid}: invalid metric or target")
        if aid not in obs_map or bid not in obs_map or aid == bid:
            fail(f"interventions/{iid}: missing/distinct baseline and follow-up references")
            continue
        before, after = obs_map[aid], obs_map[bid]
        if any(o.get("feature_id") != fid or o.get("metric") != p.get("metric") for o in (before, after)):
            fail(f"interventions/{iid}: inconsistent feature/metric across observations")
        if before.get("sampling_role") != "baseline" or after.get("sampling_role") != "counterfactual_followup":
            fail(f"interventions/{iid}: baseline/follow-up role reversal")
        t0 = visit_map.get(before.get("visit_id"), (None, None))[1]
        t1 = visit_map.get(after.get("visit_id"), (None, None))[1]
        if t0 is None or t1 is None or t1 <= t0:
            fail(f"interventions/{iid}: follow-up must occur after baseline")
        if all(finite_number(o.get("value"), 0, 100) and finite_number(o.get("uncertainty_abs"), 0, 100) for o in (before, after)) and finite_number(p.get("minimum_delta_points"), 0, 100):
            delta = round(after["value"] - before["value"], 4)
            lower_delta = round((after["value"] - after["uncertainty_abs"]) - (before["value"] + before["uncertainty_abs"]), 4)
            comparisons.append({"intervention_id": iid, "central_delta_points": delta,
                                "required_delta_points": p["minimum_delta_points"],
                                "central_target_met": delta >= p["minimum_delta_points"],
                                "conservative_lower_delta_points": lower_delta,
                                "real_world_effect_established": False,
                                "status": "SYNTHETIC_ONLY_NOT_FIELD_EVIDENCE"})

    limitations = record.get("limitations")
    if not isinstance(limitations, list) or not limitations or not all(isinstance(x, str) and x for x in limitations):
        fail("limitations: nonempty written caveats required")
    return errors, comparisons


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("record", nargs="?", default=str(Path(__file__).with_name("fixture.json")))
    args = ap.parse_args()
    try:
        with open(args.record, encoding="utf-8") as f:
            record = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print("INVALID: cannot read JSON:", exc)
        return 2
    errors, comparisons = validate(record)
    if errors:
        print("FAIL", len(errors), "invariant(s)")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS: SI-ECO-001 synthetic contract + referential checks")
    print(json.dumps({"comparison": comparisons, "authority": "none", "evidence": "synthetic only"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
