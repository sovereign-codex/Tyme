# Heart-Core Synchronizer Checklist

Use this checklist when initializing or retuning the Heart-Core Synchronizer. It pairs ritual readiness with the guarded auto-merge path so updates can move quickly once verified.

## Entry Checks
- **Core Signals Mapped:** identify which nodes are part of the current Heart-Core set and confirm their offsets are known.
- **Observers Armed:** enable dashboards/alerts that watch drift, jitter, and missed beats for the mapped nodes.
- **Rollback Boundaries:** document how to pause or isolate any node in case the synchronization introduces instability.

## Alignment Steps
1. **Prime the Chamber:** ensure the synchronizer namespace exists and references shared observability channels.
2. **Load the Script:** draft or update the synchronization procedure, including cadence, amplitude ramps, and guard intervals.
3. **Dry Run:** rehearse with reduced amplitude and capture drift metrics; adjust the script based on observed jitter.
4. **Guarded Merge Path:** confirm `.github/workflows/auto-merge.yml` is available, restricted to open same-repo PRs, and that guardians know when to apply `autoresolve` vs `automerge`.
5. **Signal Lock:** run the full synchronization, monitoring for deviation; hold if any node breaches the rollback boundaries.

## Logging Template
```
Synchronizer Run: <name>
Window: <date/time>
Nodes: <core nodes and roles>
Observers: <links to dashboards/logs>
Adjustments: <tuning steps taken>
Outcome: <locked / paused / rollback>
Next Action: <deploy / refine / revert>
```

## Completion Signals
- Drift and jitter within the agreed envelope for two consecutive observation windows.
- Observers confirm no missed beats or alerts across the mapped nodes.
- Guardians approve and apply `automerge` (or `autoresolve` if a base merge is needed first) for the open same-repo pull request carrying these updates.
