# Validation lane

## Purpose
Performs schema + business rule checks on normalized payloads and enriches them with provenance and readiness markers before orchestration.

## Inputs → outputs
- **Inputs**: `ingest.queue`.
- **Validation**: enforce schema drafts for manifests, scrolls, and lab outputs; ensure readiness hint aligns with lifecycle policy; attach `provenance.validation_run_id`, `rollback_handle`, and `handshake.checksum` placeholder for egress validation.
- **Outputs**: `validated.queue` (primary), `deadletter.queue` (schema, readiness, or policy breach).

## Controls
- **Acceptance gates**: payload must carry submitter + timestamp from ingress; readiness limited to `[draft, review, soak]`; checksum placeholder must be initialized for egress validation; rollback handle required for integration readiness.
- **Health**: validation error rate, schema drift alerts, rollback handle population, checksum placeholder coverage.
- **Rollback**: when schema drift detected, pause promotion and hold payloads in `deadletter.queue` until alignment is restored.

## Verification steps
- [ ] Run schema fixtures for manifest + scroll payloads and confirm enrichment fields are attached.
- [ ] Ensure readiness outside the rubric is rejected with explicit reason codes.
- [ ] Capture validation error rates in telemetry snapshots for Chronicle and portal badges.
