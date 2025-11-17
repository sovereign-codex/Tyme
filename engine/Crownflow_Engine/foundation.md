# Crownflow Engine Foundation Checklist

Use this checklist when activating or modifying the Crownflow Engine. It keeps automation guarded, observable, and clearly linked to the chambers it serves.

## Entry Checks
- **Scope Declared:** identify which Pulse, Heart-Core, or lattice rites the engine change will touch.
- **Guardrails Verified:** confirm `.github/workflows/auto-merge.yml` enforces open same-repo PRs, blocks drafts, and runs one concurrency lane per PR.
- **Observability Ready:** specify the dashboards or logs that will capture engine-triggered actions and any rollback cues.

## Build Steps
1. **Design Path:** outline the automation or coupling path and its label usage (`automerge`, `autoresolve`), noting how drafts and open PR checks are enforced.
2. **Wire Signals:** connect observability anchors to the targeted chambers so guardians can trace the engine’s impact.
3. **Align with Integration:** document how the Crownflow Integration chamber will consume or expose the updated engine behavior.
4. **Dry Run:** execute a rehearsal on a safe branch or sandbox; record drift, latency, and rollback notes.

## Logging Template
```
Engine Change: <name>
Scope: <pulse / heart-core / lattice links>
Guardrails: <open same-repo | no drafts | concurrency lane id>
Observability: <dashboards, alerts, traces>
Labels: <automerge/autoresolve/none>
Rehearsal Notes: <latency, drift, rollback>
Outcome: <ready / iterate / rollback>
```

## Completion Signals
- Entry, build, and rehearsal notes stored alongside this checklist with links to observability snapshots.
- Guardians confirm guardrails remain intact (open same-repo restriction, draft block, per-PR concurrency).
- Integration notes shared with Crownflow Integration and affected chamber scrolls before any labels are applied.
