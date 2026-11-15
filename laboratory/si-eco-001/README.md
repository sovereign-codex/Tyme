# SI-ECO-001 - Ecological Intelligence / Embodied Stewardship

> Foundational direction: "A day the world has never seen."
>
> Status: experimental, synthetic, review-only. **Not** a deployed ecological digital twin.

## Why this exists

TYME can preserve and review intelligence-related evidence. SI-ECO-001 explores a
bounded *physical-world evidence record* for a single site without creating a
second governance system or asserting new institutional authority.

The first cycle is deliberately synthetic: persistent objects -> time-stamped
readings -> hypothetical ecological intervention -> counterfactual follow-up ->
uncertainty-aware comparison. The fixture demonstrates **data-contract behavior**,
not ecological effectiveness.

## Contents

| File | Purpose |
| --- | --- |
| `index.html` | Standalone mobile-readable offline inspection console with embedded synthetic sample |
| `fixture.json` | Canonical fabricated record with three site features, two synthetic observations, one simulated intervention |
| `schema.json` | JSON Schema Draft 2020-12 structural contract (synthetic-only v0.1) |
| `validate.py` | Dependency-free referential, temporal, numeric, and non-authority checks |
| `test_validate.py` | Positive fixture test and 13 adversarial negative tests |
| `mobile-preview.png` (portable ZIP only) | Screenshot from a headless Chromium rendering of the offline console |

The HTML is portable as a **single file**, no build, CDN, token, tracking, or network
required. It can inspect another record only if its essential synthetic-only
invariants pass. The browser check is for preview, not full schema validation.
Always run `validate.py` before treating an imported JSON as a valid fixture.

## Run locally

1. Open `index.html` in a browser. The synthetic record is already embedded.
2. Tap a feature on the site schematic to inspect its stable identifier and local position.
3. Inspect the baseline, target, simulated follow-up, and evidence limitation.
4. Optionally export or inspect a different synthetic JSON record.

Run contract and negative tests using Python 3.10+:

```sh
python3 validate.py fixture.json
python3 -m unittest -v test_validate.py
```

Optional extra structural check when the `jsonschema` package is available:

```sh
python3 -c 'import json,jsonschema; s=json.load(open("schema.json")); f=json.load(open("fixture.json")); jsonschema.Draft202012Validator(s,format_checker=jsonschema.FormatChecker()).validate(f); print("Schema PASS")'
```

## Synthetic result (expected)

- Baseline: 11% volumetric soil moisture, **+/-2 percentage points** (fabricated).
- Hypothetical target: at least +4 percentage points.
- Synthetic counterfactual follow-up: 14% +/-2 points (fabricated).
- Central difference: +3 points, below target.
- Conservative lower difference: -1 point; intervals overlap.
- Correct conclusion: **no real-world efficacy established**. This is neither
  an actual installation nor an independent ecological verification.

## Invariants and custodial boundaries

1. No real property address, identifiable customer photo, accurate map, or live GPS coordinate.
2. Local coordinates are in **meters** with an explicitly arbitrary origin; they
   are **not GeoJSON** longitude/latitude. Do not label the data georeferenced.
3. Site, feature, visit, observation, and intervention identifiers are stable
   and their references must resolve.
4. Each synthetic observation identifies source, method, visit, metric, units,
   value, and uncertainty. No fixture can claim independent verification.
5. No field intervention may be marked executed or approved; all authority
   fields enforce **no dispatch, no credentials, no institutional effect**.
6. Baseline and counterfactual follow-up are separate time-ordered records.
7. Contradictions, unexpected results, and unverified taxonomy must not be
   silently rewritten to imply success.
8. The offline page has no automatic persistence. Explicit JSON export is the
   only save path, and no private data is transmitted anywhere.

## What v0.1 does not do

No real site capture, photogrammetry, species identification, external models,
sensors, geospatial registration, verified environmental outcomes, AVOT dispatch,
Notion writes, GitHub Actions, Cloudflare deployments, or autonomous physical control.

## One-site field successor (not implemented)

After the synthetic pilot passes review, a separate **field schema** could be
specified for one site with owner consent. Its minimum data elements would be:

- Site permission, field operator, coarse location/privacy policy, and survey
  confidence, not raw geolocation by default.
- Georeferenced features only where survey controls exist; otherwise preserve
  the local coordinate frame and its uncertainty.
- Field observation timestamps, units, method, instrument calibration,
  observation source, uncertainty, and a stable feature identifier.
- Human-approved intervention planning separate from actual execution.
- Follow-up observations and independent checks, preserving negative results.

A real site is a **different evidence class** and must never be created merely
by toggling the `classification` in the synthetic record.

## Standards mapping (future, not implemented)

- [GeoJSON RFC 7946](https://www.rfc-editor.org/rfc/rfc7946): geographic coordinates
  in longitude/latitude WGS84; **not** used for synthetic local meters.
- [STAC](https://www.ogc.org/standards/stac/): catalog imagery or timestamped
  raster and other geospatial assets once a real location and provenance exist.
- [OGC SensorThings](https://www.ogc.org/standards/sensorthings/): a potential
  model for later field sensors, observation streams, and features of interest.

## Integration gate

Repository home: `sovereign-codex/Tyme/laboratory/si-eco-001/` is a proposed
research location, not a new canonical kernel.

Before connecting to TYME, Codex-net-index, Aetherwell, or public Hall runtime,
require: reviewed field schema; consent controls; valid provenance; independent
negative-case tests; a human authorization boundary; and an explicit adapter
contract that preserves existing custody and evidence identities.

Do not merge or deploy this fixture as an operational ecological capability.
