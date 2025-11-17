# Orchestration lane

## Purpose
Routes validated payloads to AVOT runners or Codex renderers with rollback safeguards and promotion awareness.

## Inputs → outputs
- **Inputs**: `validated.queue`.
- **Routing**: split by payload type; AVOT-bound artifacts go to `avot.execute`; Codex-bound artifacts go to `codex.integration` with renderer profile hints.
- **Outputs**: `avot.execute`, `codex.integration`, `deadletter.queue` (when routing rules or rollback handles are missing).

## Controls
- **Acceptance gates**: payload must include `rollback_handle` and `provenance.validation_run_id`; readiness must not exceed `soak`.
- **Health**: orchestration dispatch latency, AVOT/Codex queue depth, rollback invocation count.
- **Rollback**: trigger `global.rollback.safe_stop` when AVOT or Codex health dips; reroute Codex-bound payloads to `codex.preview` while issues are investigated.

## Verification steps
- [ ] Confirm routing split between AVOT and Codex is deterministic and logged.
- [ ] Validate rollback handles are present on every outbound message.
- [ ] Exercise safe-stop and ensure Codex payloads are diverted to `codex.preview` with audit trails.
