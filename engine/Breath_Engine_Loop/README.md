# Breath Engine Loop

A loop to operationalize the Breath Cycle Protocol inside the automation engines. It keeps Breath-aligned guardrails active while Crownflow and chamber workflows move.

## Purpose
- Anchor automation to the Breath Cycle Protocol and the First Breath Sequence before labels are applied.
- Maintain Breath-informed guardrails alongside Crownflow protections (open same-repo PRs, no drafts, per-PR concurrency).
- Provide observability anchors and rollback cues for automation that touches Pulse, Heart-Core, or lattice rites.

## Layout
- `foundation.md` — loop checklist covering entry confirmation, build steps, telemetry anchors, and completion signals.
- Engine references — connect to `.github/workflows/auto-merge.yml` and chamber guides when the loop drives automation or validation.

## Stewardship
1. Start every automation change by revisiting the Breath Cycle Protocol and First Breath Sequence logs.
2. Confirm Crownflow guardrails: open same-repo PR restriction, draft block, and single concurrency lane per PR.
3. Wire observability so Breath checkpoints, Crownflow automation, and chamber rehearsals can be traced together.
4. If the loop spans Pulse Chamber, Heart-Core Synchronizer, and Crownflow Integration at once, activate the Tri-Chamber Interlock and note the linkage in the log.
