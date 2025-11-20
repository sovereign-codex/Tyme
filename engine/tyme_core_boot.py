"""Tyme-Core boot sequence orchestration utilities."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class BootStep:
    """Represents a single boot step and its status."""

    step: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {"step": self.step, "status": self.status}
        if self.details:
            payload["details"] = self.details
        return payload


def summarize_sios_manifest(manifest_path: Path) -> Dict[str, Any]:
    """Summarize the SIOS manifest state for boot readiness."""

    summary: Dict[str, Any] = {
        "path": str(manifest_path),
        "status": "missing",
        "state": "UNKNOWN",
        "version": None,
        "modules": 0,
        "init_steps": [],
    }

    if not manifest_path.exists():
        return summary

    manifest_data = json.loads(manifest_path.read_text())
    finalization_state = manifest_data.get("finalization", {}).get("state", "UNKNOWN")
    init_block = manifest_data.get("init", {})

    summary.update(
        {
            "status": "loaded",
            "state": finalization_state,
            "version": init_block.get("version"),
            "modules": len(manifest_data.get("modules", [])),
            "init_steps": init_block.get("steps", []),
        }
    )
    return summary


def _artifact_status(path: Path, online_label: str, missing_label: str, count_keys: Optional[List[str]] = None) -> Dict[str, Any]:
    """Report whether a supporting artifact is available."""

    if not path.exists():
        return {"status": "pending", "artifact": str(path), "note": missing_label}

    payload: Dict[str, Any] = {"status": "online", "artifact": str(path), "note": online_label}
    data = json.loads(path.read_text())
    if count_keys:
        for key in count_keys:
            if key in data and isinstance(data[key], list):
                payload[f"{key}_count"] = len(data[key])
    return payload


def build_boot_manifest(sios_manifest_path: Path, output_path: Path) -> Dict[str, Any]:
    """Construct the Tyme-Core boot manifest and persist it."""

    timestamp = datetime.now(UTC).isoformat()
    sios_summary = summarize_sios_manifest(sios_manifest_path)
    sios_online = sios_summary.get("state") == "SIOS ONLINE"

    steps: List[BootStep] = [
        BootStep(
            step="LOAD_MANIFEST",
            status="loaded" if sios_summary["status"] == "loaded" else "missing",
            details={
                "modules": sios_summary.get("modules", 0),
                "version": sios_summary.get("version"),
            },
        ),
        BootStep(
            step="SIOS_INSTALL",
            status="skipped" if sios_online else "required",
            details={
                "state": sios_summary.get("state", "UNKNOWN"),
                "reason": "SIOS already online" if sios_online else "Finalization flag not detected",
            },
        ),
    ]

    steps.append(
        BootStep(
            step="INIT_TYME_COMMAND_BUS",
            status="ready",
            details={"namespaces": ["core", "hive", "garden"]},
        )
    )

    steps.append(
        BootStep(
            step="AVOT_HIVE_CORE",
            status="online" if sios_online else "pending",
            details=_artifact_status(
                Path("chronicle/hive_core_sync.json"),
                online_label="AVOT hive synchronized",
                missing_label="Run scripts/avot_activation.py to generate hive sync",
                count_keys=["agents"],
            ),
        )
    )

    steps.append(
        BootStep(
            step="GARDEN_FLAME_INTEGRITY",
            status="enforced",
            details=_artifact_status(
                Path("chronicle/garden_flame_kodex.json"),
                online_label="Garden Flame Kodex bound",
                missing_label="Run scripts/garden_flame_installer.py to bind ethics layer",
                count_keys=["bindings"],
            ),
        )
    )

    steps.append(
        BootStep(
            step="SET_TYME_MODE",
            status="LISTENING + COHERENCE-RESPONSIVE",
            details={"mode": "LISTENING + COHERENCE-RESPONSIVE"},
        )
    )

    steps.append(
        BootStep(
            step="BROADCAST",
            status="ready",
            details={"message": "Tyme-Core boot sequence complete. SIOS is live."},
        )
    )

    manifest = {
        "system": "Tyme-Core",
        "timestamp": timestamp,
        "boot_state": "online" if sios_online else "pending",
        "boot_mode": "LISTENING + COHERENCE-RESPONSIVE",
        "sios_manifest": sios_summary,
        "boot_sequence": [step.to_dict() for step in steps],
        "broadcast": "Tyme-Core boot sequence complete. SIOS is live.",
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2))
    return manifest


__all__ = ["BootStep", "build_boot_manifest", "summarize_sios_manifest"]
