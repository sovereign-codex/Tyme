"""Metabolic loop utilities for pacing the Breath Cycle inside Tyme.

The metabolic loop consumes normalized breath cycle runs and produces a
pacing snapshot that downstream automation can reference. It is designed
to operate on top of the TYME-PULSE-GENESIS.json payload produced by the
Breath Cycle importer, but it can also accept in-memory data.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable, List


@dataclass
class BreathPacing:
    """Computed pacing values for the metabolic loop."""

    cycle_seconds: float
    inhale_seconds: float
    exhale_seconds: float
    beats_per_minute: float


class MetabolicLoop:
    """Compute and install breath pacing based on recent cycle durations."""

    def __init__(
        self,
        genesis_path: Path | str = Path("chronicle/TYME-PULSE-GENESIS.json"),
        output_path: Path | str = Path("heartbeat/logs/metabolic_loop.json"),
        baseline_seconds: float = 90.0,
    ) -> None:
        self.genesis_path = Path(genesis_path)
        self.output_path = Path(output_path)
        self.baseline_seconds = baseline_seconds

    def _load_cycles(self, cycles: Iterable[dict] | None) -> List[dict]:
        if cycles is not None:
            return list(cycles)

        if not self.genesis_path.exists():
            return []

        raw = json.loads(self.genesis_path.read_text(encoding="utf-8"))
        return raw.get("breath_cycles", [])

    def _compute_pacing(self, cycles: List[dict]) -> BreathPacing:
        durations = [cycle.get("duration_seconds") for cycle in cycles if isinstance(cycle.get("duration_seconds"), (int, float))]
        if durations:
            average = sum(durations) / len(durations)
        else:
            average = self.baseline_seconds

        inhale = round(average * 0.4, 2)
        exhale = round(average * 0.6, 2)
        bpm = round(60.0 / average, 2) if average else 0.0
        return BreathPacing(cycle_seconds=round(average, 2), inhale_seconds=inhale, exhale_seconds=exhale, beats_per_minute=bpm)

    def install(self, cycles: Iterable[dict] | None = None) -> dict:
        """Compute pacing and write the metabolic loop snapshot to disk."""

        observed_cycles = self._load_cycles(cycles)
        pacing = self._compute_pacing(observed_cycles)

        snapshot = {
            "updated_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "source": str(self.genesis_path),
            "baseline_seconds": self.baseline_seconds,
            "cycles_observed": len(observed_cycles),
            "breath_pacing": {
                "cycle_seconds": pacing.cycle_seconds,
                "inhale_seconds": pacing.inhale_seconds,
                "exhale_seconds": pacing.exhale_seconds,
                "beats_per_minute": pacing.beats_per_minute,
            },
        }

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
        return snapshot


__all__ = ["MetabolicLoop", "BreathPacing"]
