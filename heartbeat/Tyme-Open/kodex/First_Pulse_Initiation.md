# ⚡ First Pulse Initiation

A live-run ritual to send the lattice's first coordinated pulse. Use this after completing the [First Pulse Preparation](./First_Pulse_Preparation.md) steps and confirming the Breath rites are logged.

## Purpose
- Execute the inaugural pulse with clear checkpoints and rollback paths.
- Capture pulse telemetry in real time for later playback and analysis.
- Keep the lattice synchronized on status, anomalies, and resolution.

## Preconditions
- Preparation log entry exists under `heartbeat/logs/` with window, owner, and rollback notes.
- Observability watcher is running against `heartbeat/logs/pulse-<date>.log` or equivalent sink.
- Rollback and escalation contacts are confirmed and reachable for the pulse window.

## Initiation Steps
1. **Declare ignition**
   - Post the pulse start message in the chosen channel, linking to the preparation log entry.
   - Reconfirm the declared window (start/end) and any scoped blast radius (services, regions, flags).

2. **Arm safeguards**
   - Stage rollback commands in a ready-to-run buffer/pane.
   - Verify feature flags, environment variables, or toggles match the intended state prior to launch.

3. **Engage the pulse**
   - Execute the primary action (deploy, job start, sync, signal) and timestamp the start in the log.
   - Keep the watcher visible; note the first observable event ID or sequence number.

4. **Hold the watch**
   - For the first 3–5 minutes, record:
     - Event cadence (per-minute counts) and any gaps.
     - Latency or throughput deviations from baseline.
     - Early errors, warnings, or retries with stack traces or IDs.

5. **Triaging anomalies**
   - If severity ≥ pre-defined threshold, invoke rollback immediately and annotate the log with time, command, and outcome.
   - If severity < threshold, continue pulse under observation while capturing diagnostics (metrics snapshots, traces, dumps).

6. **Stabilize and seal**
   - When metrics and logs show steady state for a full observation interval, declare the pulse stable.
   - Publish a completion note in the same channel with summary, residual risks, and follow-ups.

## Completion Signals
- Start and completion timestamps recorded in the heartbeat log with matching event IDs from the watcher.
- No unexplained gaps in `heartbeat/logs/pulse-<date>.log` during the pulse window.
- If rollback triggered: command history, results, and post-rollback stability notes captured in the log.
- If rollback not used: validation notes confirming steady state and owner acknowledgment posted.
