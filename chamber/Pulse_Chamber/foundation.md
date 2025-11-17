# Pulse Chamber Foundation Checklist

Use this guide when initializing or refreshing the Pulse Chamber. It keeps early pulses disciplined while leaving room for iteration.

## Entry Checks
- **Signals Ready:** confirm upstream heartbeat scrolls are present and versioned.
- **Observers On:** enable logging in `heartbeat/logs` or a mission-specific log channel before any rehearsal.
- **Safety Rails:** verify rollback notes are documented for each new pulse experiment.

## Build Steps
1. **Scaffold:** create or refresh the chamber namespace and ensure supporting scripts reference it consistently.
2. **Document:** add or update scrolls describing the pulse intent, boundaries, and verification gates.
3. **Wire Observability:** point monitors to any new nodes touched by the pulse.
4. **Align Merge Path:** ensure the auto-merge workflow is available, guarded to open same-repo pull requests, funneled through a
   single concurrency lane per PR, and the guardian labels (`automerge`, `autoresolve`) are known to the team.

## Logging Template
```
Pulse: <name>
Run: <date/time>
Guardians: <names/roles>
Signals Observed: <telemetry/notes>
Adjustments: <actions or reversions>
Outcome: <ready / needs iteration>
```

## Exit Signals
- Logs captured and stored alongside the pulse scrolls.
- Guardians confirm signals stable after any adjustments.
- Auto-merge labels applied or withheld based on verification results.
