# Runtime Spine (TRS) specification draft

## Purpose
The Tyme Runtime Spine (TRS) provides sovereign routing and orchestration for manifests, scroll payloads, and AVOT execution. It keeps ingress, validation, orchestration, and render dispatch lanes aligned so Codex and Crown outputs remain consistent.

**Phase**: Initialization → Spine Integration → Handshake Draft → Integration Readiness → Merge Candidate → **Merge Review (current)** — routing table v0.5 promoted to stable with readiness and rollback gates sealed for finalization.

## Lanes (v0.5)
- **Ingress**: receives manifest drafts, scroll summaries, and telemetry snapshots; normalizes metadata and enforces shape checks. See `runtime-spine/lanes/ingress.md`.
- **Validation**: performs schema + business rule validation; enriches payloads with provenance and readiness gates; routes failures to a deadletter lane. See `runtime-spine/lanes/validation.md`.
- **Orchestration**: dispatches validated payloads to AVOT runners or Codex renderers; records rollback handles and promotion intent. See `runtime-spine/lanes/orchestration.md`.
- **Codex integration (sealed)**: normalization + readiness enforcement before Codex renderers; outputs `codex.render` + `codex.preview`. See `runtime-spine/lanes/trs_codex_integration.md`.
- **Render dispatch lanes**: portal feed + scroll broadcast lanes that apply promotion rubric, renderer health, and preview acceptance checks. See `runtime-spine/lanes/render_dispatch.md`.
- **Egress validation**: validates outbound artifacts (HTML, Markdown, Chronicle badges) for anchors, provenance, and checksum before broadcast. See `runtime-spine/lanes/egress_validation.md`.

## Routing table
See `runtime-spine/routing_table.json` for the authoritative routing table draft (v0.5.0, stable). Each route declares source payload, target lane, and acceptance policy. Promotion rubric (`draft → review → soak → broadcast`) is enforced before Chronicle broadcast. Telemetry snapshots flow through ingress for health mirroring, and egress validation is required before broadcast with Chronicle badge health checks. Routing table stability is required before merge.

## Sovereign controls
- **Rollback**: `global.rollback.safe_stop` applied at orchestration lane when validation or renderer health dips.
- **Health**: heartbeat cadence, ingest queue depth, validation error rate, renderer success ratio, preview acceptance ratio, render latency.
- **Readiness**: promotion gates tracked in manifests; portal badges mirror the current lane health.

## Codex handshake
See `notes/codex_handshake.md` for the ingress → Codex → render dispatch → egress validation handshake, including readiness gates, rollback hooks, fixtures, and telemetry signals mirrored into routing table v0.5.

## Worksteps
- [x] Expand lane stubs in `runtime-spine/lanes/` with specific AVOT and Codex hooks.
- [x] Align validation schemas with Codex contracts and manifest lifecycle rules.
- [ ] Wire routing table emission into the portal for live visibility.
- [x] Mirror stable TRS fields into the root manifest for lattice-wide use.
- [x] Capture preview promotion rules and renderer gates in routing table v0.3.
- [x] Ship egress validation fixtures and promotion badges driven by routing table v0.5.
