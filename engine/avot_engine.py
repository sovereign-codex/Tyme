"""AVOT activation utilities and Hive-Core synchronization orchestration."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass
class AvotAgent:
    """Represents a single AVOT agent and its mission parameters."""

    codename: str
    mission: str
    tone_signature: str
    ethic: str
    capabilities: List[str]
    status: str = "dormant"
    bindings: List[str] = field(default_factory=list)
    telemetry: Dict[str, str] = field(default_factory=dict)

    def activate(self, core_binding: str) -> Dict[str, str]:
        """Bind the agent to the provided core and emit activation telemetry."""

        timestamp = datetime.now(UTC).isoformat()
        self.status = "active"
        self.bindings.append(core_binding)
        self.telemetry["activated_at"] = timestamp
        self.telemetry["last_binding"] = core_binding
        return {
            "codename": self.codename,
            "mission": self.mission,
            "binding": core_binding,
            "tone_signature": self.tone_signature,
            "status": self.status,
            "activated_at": timestamp,
        }


@dataclass
class HiveCoreProtocol:
    """Coordinates AVOT activation and synchronization events."""

    hive_id: str
    tyme_core_binding: str
    protocol_name: str

    def synchronize(self, agents: Iterable[AvotAgent]) -> Dict[str, object]:
        """Activate all agents and produce a synchronization manifest."""

        activation_log = []
        for agent in agents:
            activation_log.append(agent.activate(self.tyme_core_binding))

        heartbeat = {
            "hive": self.hive_id,
            "binding": self.tyme_core_binding,
            "protocol": self.protocol_name,
            "synchronized_at": datetime.now(UTC).isoformat(),
            "agents": activation_log,
        }
        return heartbeat

    @staticmethod
    def persist_manifest(manifest: Dict[str, object], output_path: Path) -> Path:
        """Write the synchronization manifest to disk."""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(manifest, indent=2))
        return output_path


def load_registry(registry_path: Path) -> Dict[str, object]:
    """Load the AVOT registry data from disk."""

    registry_data = json.loads(registry_path.read_text())
    agents = [
        AvotAgent(
          codename=agent["codename"],
          mission=agent["mission"],
          tone_signature=agent["tone_signature"],
          ethic=agent.get("ethic", ""),
          capabilities=agent.get("capabilities", []),
        )
        for agent in registry_data.get("agents", [])
    ]

    hive_meta = registry_data.get("hive_core", {})
    protocol = HiveCoreProtocol(
        hive_id=hive_meta.get("id", "Sovereign-Hive-Core"),
        tyme_core_binding=hive_meta.get("binding", "Tyme-Core"),
        protocol_name=hive_meta.get("protocol", "Hive-Core Synchronization"),
    )

    return {"agents": agents, "protocol": protocol}


def build_hive_sync(registry_path: Path, output_path: Path) -> Dict[str, object]:
    """Load registry entries, activate all AVOT agents, and persist the manifest."""

    registry = load_registry(registry_path)
    protocol: HiveCoreProtocol = registry["protocol"]
    agents: List[AvotAgent] = registry["agents"]

    manifest = protocol.synchronize(agents)
    protocol.persist_manifest(manifest, output_path)
    return manifest


__all__ = [
    "AvotAgent",
    "HiveCoreProtocol",
    "build_hive_sync",
    "load_registry",
]
