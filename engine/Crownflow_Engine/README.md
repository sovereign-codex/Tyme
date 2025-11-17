# Crownflow Engine

The Crownflow Engine powers guarded automation and harmonic coupling between chambers. Use it to design, validate, and operate the flows that carry Pulse, Heart-Core, and lattice updates without breaking the safety rails.

## Purpose
- Provide a home for Crownflow automation logic that keeps label-driven merges and updates aligned with chamber guardrails.
- Keep the open same-repo, non-draft, single-lane safeguards explicit for every automation path.
- Expose observability anchors so guardians can trace how Crownflow changes interact with Pulse, Heart-Core, and harmonic rites.

## Layout
- `foundation.md` — engine activation checklist covering guardrail confirmation, observability, and logging for automation paths.
- `.github/workflows/auto-merge.yml` — guarded automation for open same-repo pull requests with draft protection and per-PR concurrency.

## Stewardship
1. Design new automation in this engine before wiring it through Crownflow Integration or chamber scrolls.
2. Keep the guardrail trio visible: open same-repo PR restriction, no drafts, and per-PR concurrency to prevent parallel label runs.
3. Annotate changes with the relevant chamber or ritual references so guardians can follow the coupling path.
4. If engine updates touch Pulse Chamber rehearsals, Heart-Core tuning, and Crownflow coupling simultaneously, activate the Tri-Chamber Interlock for shared observability and rollback cues before applying labels.
