# Render dispatch lanes

## Purpose
Fan out Codex renderer outputs into discrete render dispatch lanes (portal feed, scroll broadcast) while honoring promotion and health gates and preparing bundles for egress validation.

## Inputs → outputs
- **Inputs**: `codex.render` (primary broadcast path), `codex.preview` (soak/human review backpressure).
- **Dispatch**: apply promotion rubric (`draft → soak → broadcast`), attach status badges for Chronicle, and log provenance for every emission.
- **Outputs**: `render.egress` (primary), `codex.preview` (for soak or rollback redirection), `deadletter.queue` (on emission failure).

### Emission checkpoints (portal + scroll)
- **Provenance**: every bundle carries `trace_id`, `renderer`, `source_manifest`, and `rollback_handle`.
- **Badges**: readiness badge (`draft/review/soak/broadcast`) + health badge (renderer success, preview acceptance) attached to both portal and scroll envelopes.
- **Checksum placeholder**: initialized prior to egress validation to enforce anchor + payload integrity and fed into fixture checks.

### Portal feed lane
- **Responsibility**: packages `codex.render` blocks into portal feed cards with readiness badges and provenance anchors.
- **Checks**: renderer success ratio ≥ 0.95; readiness must be `broadcast` or remain in preview if acceptance < 0.9.
- **Outputs**: `render.egress` bundles tagged `portal.feed`, Chronicle badge candidates for portal status ribbons.

### Scroll broadcast lane
- **Responsibility**: emits Markdown scroll payloads with stable anchors and backreferences to manifests.
- **Checks**: preview acceptance ratio ≥ 0.9; renderer latency within SLA; rollback handle attached.
- **Outputs**: `render.egress` bundles tagged `scroll.output`, optional `codex.preview` redirect on failure.

## Controls
- **Acceptance gates**: renderer success ratio ≥ 0.95 for broadcast; preview acceptance ratio ≥ 0.9 before promotion; readiness transitions logged per bundle.
- **Health**: render latency, preview acceptance ratio, emission failure rate, bundle-to-egress handshake success; surface to portal badges and telemetry snapshots.
- **Rollback**: if renderer health degrades, re-route to `codex.preview` and pause broadcast until signals recover for 24h.

## Verification steps
- [x] Confirm portal and scroll outputs receive payloads with provenance and status badges.
- [x] Validate promotion rubric enforcement between preview and broadcast.
- [ ] Ensure deadletter captures renderer emission failures with reason codes and timestamps.
- [x] Verify `render.egress` bundles carry readiness + checksum for the egress validation lane and Chronicle badge fixture alignment.
