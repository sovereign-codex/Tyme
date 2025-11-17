# Catalytic initialization plan

## Objectives
- Stand up a catalytic lane that accelerates AVOT + Codex handoff (ingest → transform → render) without manual glue code.
- Establish guardrails for runtime readiness (health signals, rollback switches, validation checks) before promotion.
- Provide repeatable bootstrap steps so downstream nodes can mirror the catalytic setup.

## Interfaces (draft)
- **Inputs**: manifest payloads, scroll summaries, AVOT telemetry snapshots, and renderer configuration flags.
- **Transformations**: normalize inputs, enrich with provenance + readiness signals, then fan out to Codex emitters.
- **Outputs**: HTML/Markdown snippets for the portal, JSON snapshots for automation, and status pings for Chronicle.

## Worksteps
- [ ] Define catalytic queue + routing rules (ingest, validate, dispatch to renderers).
- [ ] Specify health + rollback switches (circuit breaker thresholds, retry policy, safe-stop command).
- [ ] Draft readiness rubric for catalytic promotion (draft → soak → broadcast) and mirror in manifests.
- [ ] Produce sample catalytic payloads and validate against Codex/Crown schemas.
- [ ] Wire a portal panel that tracks catalytic lanes and exposes live status badges.

## Dependencies
- AVOT telemetry fields to feed health + provenance.
- Codex renderer contracts for payload shape + expected outputs.
- Manifest lifecycle rules for promotion and rollback alignment.

## Health + observability (draft)
- Heartbeat cadence, ingest queue depth, validation error rate, renderer success ratio, and last safe rollback point.
- Capture a minimal status JSON that can be surfaced in the portal and Chronicle.
