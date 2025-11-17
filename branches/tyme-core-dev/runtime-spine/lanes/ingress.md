# Ingress lane

## Purpose
Receives manifest drafts, scroll summaries, and telemetry snapshots and shapes them into a consistent envelope for TRS. The ingress lane applies provenance tagging and de-duplication before forwarding to validation.

## Inputs → outputs
- **Inputs**: `manifest.draft`, `scroll.summary`, `telemetry.snapshot`, `render.egress` health mirrors.
- **Normalization**: attach `metadata.submitter`, `timestamp`, `trace_id`, and `readiness_hint`; enforce size limits, signature checks, and drop duplicate `trace_id`.
- **Outputs**: `ingest.queue` (primary), `deadletter.queue` (on shape, signature, or dedupe failure).

## Controls
- **Acceptance gates**: readiness hints must be present; telemetry payloads must declare originating AVOT; signatures required for render egress mirrors to prevent spoofing.
- **Health**: heartbeat cadence, queue depth, duplicate rejection rate; emit to `telemetry.snapshot` for Chronicle mirrors.
- **Rollback**: divert to `deadletter.queue` when ingress validation fails or queue depth exceeds threshold.

## Verification steps
- [ ] Run manifest + scroll payload samples and confirm envelopes include provenance + readiness hints.
- [ ] Assert duplicates are rejected with reason codes.
- [ ] Verify telemetry snapshots include ingress health signals for downstream monitoring.
