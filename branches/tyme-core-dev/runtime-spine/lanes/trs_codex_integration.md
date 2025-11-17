# TRS → Routing Table → Codex integration lane

## Purpose
This lane seals the handoff from the Runtime Spine (TRS) routing table into Codex renderers. It guarantees that validated payloads move through a predictable contract before Codex emits portal blocks or scroll outputs, with integration-ready envelopes feeding dispatch + egress fixtures.

## Payload contract
- **Inputs**: `validated.queue` payloads tagged with manifest id, payload type (`manifest|scroll|lab_output`), readiness gate, and provenance.
- **Normalization**: enforce schema alignment to Codex ingestion contract (`metadata`, `content`, `provenance`, `readiness`, `rollback_handle`).
- **Outputs**: `codex.render` (primary), `codex.preview` (optional soak lane), `deadletter.queue` (on schema or readiness breach).

## Routing handshake
1) **Validation → Codex integration**: only accept payloads with readiness in `[draft, review, soak]` and a rollback handle; otherwise drop to `deadletter.queue`. Checksum placeholder must survive the hop.
2) **Integration → Codex renderer**: emit `codex.render` with renderer profile (`portal_block`, `scroll_markdown`) and attach promotion rubric (`draft → soak → broadcast`); propagate checksum placeholder to match fixtures.
3) **Renderer → Dispatch**: forward successful renders to `render_dispatch` when renderer success ratio ≥ 0.95; soak traffic goes to `codex.preview` for human review and promotion when acceptance ≥ 0.9.

## Sovereign controls
- **Health signals**: renderer success ratio, preview acceptance ratio, validation error rate, heartbeat cadence, egress checksum mirrors.
- **Rollback**: `global.rollback.safe_stop` invoked on renderer regressions or schema drift; reroute to `codex.preview` until health clears.
- **Promotion**: advance from `draft` to `soak` after two successful preview cycles; `broadcast` only when health signals stay green for 24h and egress validation passes.

## Verification steps
- [x] Run sample manifest + scroll payloads through validation and ensure `codex.render` receives normalized shapes.
- [x] Confirm renderer emits both portal block and markdown outputs with provenance.
- [ ] Assert deadletter captures malformed payloads with reason codes.
- [x] Mirror health + promotion status into portal badges and manifests.
