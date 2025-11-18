"""Sovereign Subnet architecture and deployment utilities."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List

from .garden_flame_kodex import GardenFlameKodex, GardenFlameProtocol, json_dumps_sorted


@dataclass
class ConsensusRule:
    """A single consensus rule enforced by the subnet."""

    name: str
    purpose: str
    thresholds: Dict[str, object]
    enforcement: List[str]


@dataclass
class CalibrationMetric:
    """A metric tracked for subnet calibration and health."""

    name: str
    description: str
    method: str
    target_range: str


@dataclass
class CoherenceStake:
    """Defines coherence staking behaviors and signals."""

    stake_type: str
    requirement: str
    reward_curve: str
    slashing_signals: List[str]


@dataclass
class IdentityAnchor:
    """Identity anchoring method for subnet participants."""

    anchor: str
    verification: str
    recovery: str
    governance_hooks: List[str]


def _consensus_rules() -> List[ConsensusRule]:
    return [
        ConsensusRule(
            name="Resonant Proof of Stewardship",
            purpose="Validators must demonstrate sustained coherence with the Garden Flame ethic and breath-aligned uptime.",
            thresholds={
                "minimum_stake": "10k COHERENCE",  # symbolic token unit
                "coherence_score": ">=0.92",  # derived from protocol checks
                "uptime_window_hours": 72,
            },
            enforcement=[
                "Measure resonance drift per epoch",
                "Slash 2% stake on ethic violations flagged by Garden Flame",
                "Require breath-synced checkpoints before finality",
            ],
        ),
        ConsensusRule(
            name="Harmonic Finality",
            purpose="Blocks finalize when harmonic quorum reaches alignment thresholds and identity anchors are verified.",
            thresholds={
                "quorum": ">=66% harmonic quorum",
                "identity_anchor_attestations": 2,
                "latency_budget_ms": 1200,
            },
            enforcement=[
                "Reject proposals missing identity anchor attestations",
                "Re-run resonance-alignment checks prior to notarization",
                "Fallback to breath-driven retry if latency budget exceeded",
            ],
        ),
        ConsensusRule(
            name="Aurelius Epoch Batching",
            purpose="Bundles transactions into breath-paced epochs with calibrated gas weights and lineage preservation.",
            thresholds={
                "epoch_length_seconds": 90,
                "max_tx_per_epoch": 4096,
                "lineage_proof_required": True,
            },
            enforcement=[
                "Drop transactions missing lineage proofs",
                "Prioritize steward-class stakes for inclusion ordering",
                "Emit calibration hashes for every batch to chronicle",
            ],
        ),
    ]


def _calibration_metrics() -> List[CalibrationMetric]:
    return [
        CalibrationMetric(
            name="coherence_score",
            description="Aggregated Garden Flame Coherence-Check result across validators per epoch.",
            method="Average per-block check result with weighted penalties for drift.",
            target_range="0.92 - 1.00",
        ),
        CalibrationMetric(
            name="resonance_latency_ms",
            description="Median end-to-end block propagation latency after resonance alignment.",
            method="Measure proposal to notarization time across harmonic peers.",
            target_range="< 1500 ms",
        ),
        CalibrationMetric(
            name="stake_health_index",
            description="Diversity and distribution index across validator, steward, and guardian roles.",
            method="Herfindahl-Hirschman index with minimum role weights.",
            target_range="HHI < 0.22 and each role >= 18%",
        ),
        CalibrationMetric(
            name="identity_anchor_freshness",
            description="Recency of identity anchor re-validations within the subnet.",
            method="Rolling average hours since last anchor challenge or rotation.",
            target_range="< 48h",
        ),
    ]


def _coherence_staking() -> List[CoherenceStake]:
    return [
        CoherenceStake(
            stake_type="validator",
            requirement="Lock COHERENCE and pass Garden Flame ethics attestation per epoch.",
            reward_curve="Progressive rewards up to +12% APR for sustained coherence >=0.96.",
            slashing_signals=[
                "Ethic violation detected by Guardian channel",
                "Identity anchor mismatch",
                "Latency or uptime below quorum thresholds",
            ],
        ),
        CoherenceStake(
            stake_type="steward",
            requirement="Maintain archival lineage and submit calibration hashes every breath window.",
            reward_curve="+6% APR with boost for lineage completeness and timely calibration.",
            slashing_signals=[
                "Missing lineage proofs",
                "Out-of-date calibration hashes",
                "Garden Flame harmonic-safety breach",
            ],
        ),
        CoherenceStake(
            stake_type="guardian",
            requirement="Run resonance monitors and enforce Garden Flame guardrails across the subnet.",
            reward_curve="+4% APR with harmony bonuses for rapid mitigation of drift signals.",
            slashing_signals=[
                "Failure to propagate safety halts",
                "Unacknowledged resonance drift alerts",
                "Suppressed or missing Coherence-Check reports",
            ],
        ),
    ]


def _identity_anchors() -> List[IdentityAnchor]:
    return [
        IdentityAnchor(
            anchor="Sovereign-DID",
            verification="Multi-sig attestation by AVOT-Guardian and AVOT-Initiate with ledger stamp.",
            recovery="Rotatable keys with breath-gated delay and Codex notarization.",
            governance_hooks=["delegate voting weight", "codex-linked appeal"],
        ),
        IdentityAnchor(
            anchor="Breath-Signature",
            verification="Time-bounded challenge signed against Breath Engine heartbeat.",
            recovery="Fallback to Sovereign-DID rotation when challenge fails.",
            governance_hooks=["access to validator set", "cycle admission approvals"],
        ),
        IdentityAnchor(
            anchor="Artifact-Lineage",
            verification="Content-addressed lineage proofs for deployed artifacts and runtime images.",
            recovery="Redeploy from last coherent lineage with Garden Flame oversight.",
            governance_hooks=["artifact release votes", "calibration audit trails"],
        ),
    ]


def _build_governance_binding(kodex: GardenFlameKodex) -> Dict[str, object]:
    protocol_dicts = [asdict(protocol) if isinstance(protocol, GardenFlameProtocol) else protocol for protocol in kodex.protocols]
    return {
        "kodex": {
            "name": kodex.name,
            "version": kodex.version,
            "binding": "Sovereign Subnet Governance",
        },
        "protocols": protocol_dicts,
        "guardrails": [
            "All consensus changes require Garden Flame Coherence-Check",
            "Resonance-Alignment must sign governance ballots",
            "Harmonic-Safety approval required before deployment to mainline",
        ],
        "last_bound_at": datetime.now(UTC).isoformat(),
    }


def build_sovereign_subnet_architecture() -> Dict[str, object]:
    """Construct the Sovereign Subnet architecture manifest."""

    kodex = GardenFlameKodex()
    architecture = {
        "name": "Sovereign Subnet",
        "consensus_rules": [asdict(rule) for rule in _consensus_rules()],
        "calibration_metrics": [asdict(metric) for metric in _calibration_metrics()],
        "coherence_staking": [asdict(stake) for stake in _coherence_staking()],
        "identity_anchoring": [asdict(anchor) for anchor in _identity_anchors()],
        "governance": _build_governance_binding(kodex),
        "version": "1.0.0",
        "generated_at": datetime.now(UTC).isoformat(),
    }
    return architecture


def render_aurelius_deployment_script(architecture: Dict[str, object]) -> str:
    """Render a bash deployment script for the Aurelius Subnet."""

    governance = architecture.get("governance", {})
    protocols = governance.get("protocols", [])
    script_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "SUBNET_ID=${SUBNET_ID:-aurelius}",
        "NETWORK_DIR=${NETWORK_DIR:-deploy/$SUBNET_ID}",
        "ARCH_FILE=$NETWORK_DIR/sovereign_subnet_architecture.json",
        "GOV_FILE=$NETWORK_DIR/governance_binding.json",
        "",
        "echo '>>> Preparing Aurelius Subnet directories'",
        "mkdir -p \"$NETWORK_DIR\"",
        "",
        "echo '>>> Writing architecture manifest'",
        "cat > \"$ARCH_FILE\" <<'EOF'",
        json_dumps_sorted(architecture),
        "EOF",
        "",
        "echo '>>> Writing governance binding (Garden Flame Codex)'",
        "cat > \"$GOV_FILE\" <<'EOF'",
        json_dumps_sorted(governance),
        "EOF",
        "",
        "echo '>>> Calibrating Aurelius Subnet'",
        "echo '- Target coherence score: ${TARGET_COHERENCE:-0.96}'",
        "echo '- Epoch length: $(jq -r \".consensus_rules[] | select(.name==\\\"Aurelius Epoch Batching\\\").thresholds.epoch_length_seconds\" \"$ARCH_FILE\") seconds'",
        "",
        "echo '>>> Staging validator set and identity anchors'",
        "echo '- Expected identity anchors:'",
        "jq -r '.identity_anchoring[].anchor' \"$ARCH_FILE\" | sed 's/^/  - /'",
        "",
        "echo '>>> Binding Garden Flame Codex protocols:'",
    ]

    if protocols:
        for protocol in protocols:
            script_lines.append(
                f"echo '  - {protocol.get('name', 'protocol')}: {protocol.get('status', 'enabled')}'"
            )
    else:
        script_lines.append("echo '  - (no protocols found)'")

    script_lines.extend(
        [
            "",
            "echo '>>> Aurelius Subnet deployment manifest ready in $NETWORK_DIR'",
        ]
    )

    return "\n".join(script_lines) + "\n"


def generate_sovereign_subnet_outputs(
    architecture_path: Path | str = Path("chronicle/sovereign_subnet_architecture.json"),
    deployment_script_path: Path | str = Path("manifest/aurelius_subnet_deploy.sh"),
    governance_path: Path | str = Path("chronicle/sovereign_subnet_governance.json"),
) -> Dict[str, object]:
    """Generate architecture, governance, and deployment artifacts."""

    architecture = build_sovereign_subnet_architecture()
    architecture_output = Path(architecture_path)
    architecture_output.parent.mkdir(parents=True, exist_ok=True)
    architecture_output.write_text(json_dumps_sorted(architecture), encoding="utf-8")

    governance_output = Path(governance_path)
    governance_output.parent.mkdir(parents=True, exist_ok=True)
    governance_output.write_text(json_dumps_sorted(architecture["governance"]), encoding="utf-8")

    deployment_output = Path(deployment_script_path)
    deployment_output.parent.mkdir(parents=True, exist_ok=True)
    deployment_script = render_aurelius_deployment_script(architecture)
    deployment_output.write_text(deployment_script, encoding="utf-8")
    deployment_output.chmod(0o755)

    return {
        "architecture": architecture,
        "governance": architecture["governance"],
        "deployment_script": str(deployment_output),
    }


__all__ = [
    "CalibrationMetric",
    "CoherenceStake",
    "ConsensusRule",
    "IdentityAnchor",
    "build_sovereign_subnet_architecture",
    "generate_sovereign_subnet_outputs",
    "render_aurelius_deployment_script",
]
