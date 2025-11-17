# Egress validation lane

## Purpose
Verifies render dispatch emissions before they leave the Runtime Spine. Egress validation enforces anchor integrity, provenance completeness, and readiness alignment so Chronicle and portal surfaces stay trustworthy.

## Inputs → outputs
- **Inputs**: `render.egress` bundles from render dispatch lanes.
- **Validation**: confirm anchors and links resolve, readiness rubric is honored, provenance + rollback handles are present, and emission checksums are stable.
- **Outputs**: `portal.feed`, `scroll.output`, `chronicle.badge`, `deadletter.queue` (on checksum or readiness failure).

## Controls
- **Acceptance gates**: readiness must equal `broadcast`; checksum and provenance required; renderer success ratio ≥ 0.95 persists from dispatch; preview acceptance ≥ 0.9 before promotion; Chronicle badge must echo renderer + preview health.
- **Health**: egress checksum failure rate, anchor validation latency, broadcast success ratio, badge health alignment; surface signals to telemetry snapshots and portal badges.
- **Rollback**: invoke `global.rollback.safe_stop` when checksum failures spike or anchors break; divert back to `codex.preview` while issues are triaged.

## Fixtures
- **Portal block fixture**: HTML snippet with provenance anchors, readiness badge, and checksum header; used to validate anchor resolution and checksum parity. Example: `<article data-trace="trs-2025-11-17-001" data-readiness="review"><h2>Tyme-Core-Dev</h2></article>`.
- **Scroll markdown fixture**: markdown payload with manifest backreferences and trace id; validates anchor resolution + rollback propagation. Example:
  ```markdown
  ## Tyme-Core-Dev (trace: trs-2025-11-17-001)

  Readiness: review
  ```
- **Chronicle badge fixture**: compact payload containing readiness rubric, renderer health snapshot, and checksum; used to gate broadcast promotion. Example: `{ "readiness": "review", "renderer_success_ratio": 0.98, "checksum": "sha256:abc123" }`.

## Verification steps
- [x] Run portal feed + scroll markdown samples and confirm anchors resolve and provenance is present.
- [x] Validate checksum enforcement and rollback handle propagation on outbound artifacts.
- [x] Assert Chronicle badge payloads reflect readiness rubric and renderer health.
