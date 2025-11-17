# ⚡ First Pulse Preparation

A readiness ritual to prime the lattice for its initial synchronized pulse. Use this when the Breath has been honored and the grid needs to hum as one.

## Purpose
- Confirm the Breath rites are complete and logged.
- Stage observability so early pulses are captured without loss.
- Align collaborators on timing, scope, and safety signals.

## Prerequisites
- **Breath aligned:** `First_Breath_Sequence` completed and logged under `heartbeat/logs/`.
- **Manifest validated:** `python scripts/validate_manifest.py` passing with no missing paths.
- **Access confirmed:** credentials or tokens for any dependent services are available in your session.

## Preparation Steps
1. **Anchor intent**
   - Revisit the [Breath Cycle Protocol](./Breath_Cycle_Protocol.md) and ensure the current work item is clearly written in your heartbeat log.
   - Declare the intended pulse window (start/end) in the log entry.

2. **Stabilize the lattice**
   - Run a dry-run of the target module or workflow to surface obvious failures before pulsing.
   - If dry-run produces warnings, note them in the log and resolve or explicitly defer with owner sign-off.

3. **Prime observability**
   - Enable or verify runtime logging is pointed to `heartbeat/logs/pulse-<date>.log`.
   - Start a lightweight watcher (e.g., `tail -f heartbeat/logs/pulse-<date>.log`) in a separate pane to confirm events land as expected.
   - For external services, ensure webhooks or callbacks point to reachable endpoints in your environment.

4. **Set safety rails**
   - Define rollback steps for the pulse (e.g., revert commit, disable feature flag, stop service) and capture them in the log.
   - Identify on-call or reviewer roles for the pulse window and document contact handles.

5. **Countdown and initiate**
   - Announce T-minus checkpoints (T-10, T-5, T-1) in the relevant channel, referencing the log entry.
   - Execute the pulse action (deploy, job start, sync) and monitor the watcher for the first 3–5 minutes.

6. **Exhale and record**
   - Append observed signals, anomalies, and resolutions to the same heartbeat log entry.
   - If rollback was used, document timing and outcome; if not, note stable state confirmation.

## Completion Signals
- Pulse completed within the declared window with logs captured under `heartbeat/logs/`.
- Watcher confirmed event flow with no missing intervals during the pulse window.
- Rollback path documented and either executed or validated as unnecessary.
