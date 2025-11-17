# TRS lanes

Use this folder to capture lane-specific specs and stubs for ingress, validation, orchestration, Codex integration, render dispatch, and egress validation. Add one file per lane as definitions mature.

## Lane catalog
- `ingress.md` — envelope intake for manifests, scrolls, and telemetry snapshots.
- `validation.md` — schema + policy checks with provenance enrichment.
- `orchestration.md` — split routes to AVOT runners or Codex renderers with rollback hooks.
- `trs_codex_integration.md` — sealed TRS → Routing Table → Codex lane contract and verification steps.
- `render_dispatch.md` — dispatch renderer outputs to portal + scrolls with promotion gates.
- `egress_validation.md` — verifies render bundles before broadcast to portal, scrolls, and Chronicle badges.
