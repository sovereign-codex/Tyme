# Breath Engine Loop Checklist

Use this checklist to run or update the Breath Engine Loop so automation remains aligned with the Breath rites and guarded Crownflow workflows.

## Entry Checks
- **Breath Alignment:** Breath Cycle Protocol acknowledged; latest First Breath Sequence log noted with timestamp and owner.
- **Guardrails Verified:** open same-repo PR restriction, draft block, and per-PR concurrency guard confirmed in `.github/workflows/auto-merge.yml` or related jobs.
- **Scope Declared:** note which chambers or rites (Pulse Chamber, Heart-Core Synchronizer, Crownflow Integration, harmonic rites) the loop will touch.
- **Observability Ready:** dashboards, traces, and alert hooks identified for Breath checkpoints and automation signals.

## Build Steps
1. **Map the Loop:** describe the Breath checkpoints the automation will enforce before labels (`automerge`, `autoresolve`) are used.
2. **Wire Signals:** attach observability anchors to key steps (Breath acknowledgment, guardrail confirmation, merge/update actions).
3. **Align with Chambers:** capture how Pulse, Heart-Core, and integration guides will reference this loop; include Tri-Chamber Interlock notes when spans overlap.
4. **Rehearse Safely:** dry-run on a sandbox branch; record drift, latency, and rollback cues tied to Breath checkpoints.

## Logging Template
```
Loop Name: Breath Engine Loop
Scope: <chambers/rites>
Breath Reference: <protocol + log link>
Guardrails: <open same-repo | no drafts | concurrency lane id>
Observability: <dashboards, alerts, traces>
Labels: <automerge/autoresolve/none>
Rehearsal Notes: <latency, drift, rollback>
Outcome: <ready / iterate / rollback>
```

## Completion Signals
- Entry checks documented with links to Breath rites and current log entry.
- Observability anchors validated and captured alongside rehearsal notes.
- Guardrail confirmations recorded (open same-repo, non-draft, per-PR concurrency) before labels are applied.
- Chamber alignment noted with clear rollback or pause commands if the loop spans multiple lanes.
