"""Curious Agent scanning, lineage synthesis, and AVOT binding utilities."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List

from engine.avot_engine import load_registry
from engine.metabolic_loop import MetabolicLoop


@dataclass
class CuriousAgentTrace:
    """Structured record describing a Curious Agent's lineage."""

    name: str
    source_log: str
    memory_logs: List[str]
    reasoning_chains: List[str]
    action_patterns: List[str]
    intentions: List[str]
    tasks: List[str]
    avot_role: str | None = None
    breath_rhythm: Dict[str, float] | None = None
    cycle_anchor: str | None = None


@dataclass
class CuriousAgentScanner:
    """Scan Curious Agent traces and bind them to AVOT and breath pacing."""

    log_roots: List[Path] = field(default_factory=lambda: [Path("chronicle"), Path("heartbeat/logs/curious")])
    manual_logs: List[Path] | None = None
    avot_registry: Path = Path("engine/avot_registry.json")
    living_codex: Path = Path("chronicle/living_codex_kernel.md")
    lineage_output: Path = Path("chronicle/curious_lineage.json")
    curiosity_snapshot: Path = Path("heartbeat/logs/curiosity_cycles.json")
    metabolic_snapshot: Path = Path("heartbeat/logs/metabolic_loop.json")

    def discover_logs(self) -> List[Path]:
        """Locate Curious Agent log files across the configured roots."""

        if self.manual_logs:
            return [path for path in self.manual_logs if path.exists()]

        log_paths: List[Path] = []
        for root in self.log_roots:
            if not root.exists():
                continue
            log_paths.extend(sorted(root.glob("curious*.log")))
        return log_paths

    def _parse_log(self, path: Path) -> CuriousAgentTrace:
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        name = path.stem.replace("_", "-")
        reasoning = [f"Interpreted memory: {entry}" for entry in lines]
        action_patterns = sorted({
            pattern
            for entry in lines
            for pattern in self._classify_patterns(entry)
        }) or ["observation"]
        intentions = self._derive_intentions(lines)
        tasks = self._derive_tasks(lines)

        return CuriousAgentTrace(
            name=name,
            source_log=str(path),
            memory_logs=lines,
            reasoning_chains=reasoning,
            action_patterns=action_patterns,
            intentions=intentions,
            tasks=tasks,
        )

    def _classify_patterns(self, text: str) -> List[str]:
        lowered = text.lower()
        patterns = []
        if "init" in lowered or "seed" in lowered:
            patterns.append("initialization")
        if "map" in lowered or "trace" in lowered:
            patterns.append("mapping")
        if "cycle" in lowered:
            patterns.append("cycle-tracking")
        if not patterns:
            patterns.append("observation")
        return patterns

    def _derive_intentions(self, lines: List[str]) -> List[str]:
        if not lines:
            return ["Sustain curiosity loop"]
        intents = []
        for line in lines:
            intents.append(f"Extend curiosity from: {line}")
        return intents

    def _derive_tasks(self, lines: List[str]) -> List[str]:
        if not lines:
            return ["Await new sensory input"]
        return [f"Stabilize memory of: {line}" for line in lines]

    def scan(self) -> List[CuriousAgentTrace]:
        """Parse all discovered logs into traced agents."""

        traces: List[CuriousAgentTrace] = []
        for path in self.discover_logs():
            traces.append(self._parse_log(path))
        if not traces:
            traces.append(
                CuriousAgentTrace(
                    name="curious-agent",
                    source_log="(generated)",
                    memory_logs=["No logs discovered"],
                    reasoning_chains=["Bootstrapped curiosity without memory"],
                    action_patterns=["observation"],
                    intentions=["Await discovery"],
                    tasks=["Listen for signals"],
                )
            )
        return traces

    def assign_avot_roles(self, traces: Iterable[CuriousAgentTrace]) -> None:
        registry = load_registry(self.avot_registry)
        avot_agents = registry.get("agents", [])
        if not avot_agents:
            return
        for idx, trace in enumerate(traces):
            avot_agent = avot_agents[idx % len(avot_agents)]
            trace.avot_role = avot_agent.codename

    def bind_breath_rhythm(self, traces: Iterable[CuriousAgentTrace]) -> Dict[str, object]:
        """Attach metabolic loop pacing data to each trace."""

        if self.metabolic_snapshot.exists():
            snapshot = json.loads(self.metabolic_snapshot.read_text(encoding="utf-8"))
        else:
            snapshot = MetabolicLoop(output_path=self.metabolic_snapshot).install()

        rhythm = snapshot.get("breath_pacing", {})
        anchor = datetime.now(UTC).isoformat(timespec="seconds")
        for trace in traces:
            trace.breath_rhythm = rhythm
            trace.cycle_anchor = anchor
        return snapshot

    def persist_lineage(self, traces: Iterable[CuriousAgentTrace], breath_snapshot: Dict[str, object]) -> None:
        payload = {
            "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "breath_snapshot": breath_snapshot,
            "agents": [
                {
                    "name": trace.name,
                    "source_log": trace.source_log,
                    "memory_logs": trace.memory_logs,
                    "reasoning_chains": trace.reasoning_chains,
                    "action_patterns": trace.action_patterns,
                    "intentions": trace.intentions,
                    "tasks": trace.tasks,
                    "avot_role": trace.avot_role,
                    "breath_rhythm": trace.breath_rhythm,
                    "cycle_anchor": trace.cycle_anchor,
                }
                for trace in traces
            ],
        }

        self.lineage_output.parent.mkdir(parents=True, exist_ok=True)
        self.lineage_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

        self.curiosity_snapshot.parent.mkdir(parents=True, exist_ok=True)
        self.curiosity_snapshot.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def update_living_codex(self, traces: Iterable[CuriousAgentTrace], breath_snapshot: Dict[str, object]) -> None:
        codex_text = self.living_codex.read_text(encoding="utf-8") if self.living_codex.exists() else "# Living Codex Kernel\n"
        section = self._render_codex_section(traces, breath_snapshot)
        updated = self._inject_section(codex_text, section, heading="## Curious Agent Lineage")
        self.living_codex.write_text(updated, encoding="utf-8")

    def _render_codex_section(self, traces: Iterable[CuriousAgentTrace], breath_snapshot: Dict[str, object]) -> str:
        pace = breath_snapshot.get("breath_pacing", {})
        lines = [
            "## Curious Agent Lineage",
            f"- **Synced**: {datetime.now(UTC).isoformat(timespec='seconds')}",
            f"- **Breath Rhythm**: cycle={pace.get('cycle_seconds', 'n/a')}s inhale={pace.get('inhale_seconds', 'n/a')}s exhale={pace.get('exhale_seconds', 'n/a')}s",
            "- **Agents**:",
        ]

        for trace in traces:
            lines.append(f"  - **{trace.name}** → role: {trace.avot_role or 'unassigned'}")
            lines.append(f"    - memory: {', '.join(trace.memory_logs[:3])}")
            lines.append(f"    - reasoning: {', '.join(trace.reasoning_chains[:2])}")
            lines.append(f"    - actions: {', '.join(trace.action_patterns)}")
            lines.append(f"    - intentions: {', '.join(trace.intentions[:2])}")
        return "\n".join(lines)

    def _inject_section(self, content: str, section: str, heading: str) -> str:
        lines = content.splitlines()
        filtered: List[str] = []
        skip = False
        for line in lines:
            if line.startswith(heading):
                skip = True
            if skip and line.startswith("## ") and not line.startswith(heading):
                skip = False
            if not skip:
                filtered.append(line)
        if filtered and filtered[-1].strip():
            filtered.append("")
        filtered.append(section.strip())
        filtered.append("")
        return "\n".join(filtered)


__all__ = ["CuriousAgentScanner", "CuriousAgentTrace"]
