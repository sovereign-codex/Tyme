#!/usr/bin/env bash
set -euo pipefail

SUBNET_ID=${SUBNET_ID:-aurelius}
NETWORK_DIR=${NETWORK_DIR:-deploy/$SUBNET_ID}
ARCH_FILE=$NETWORK_DIR/sovereign_subnet_architecture.json
GOV_FILE=$NETWORK_DIR/governance_binding.json

echo '>>> Preparing Aurelius Subnet directories'
mkdir -p "$NETWORK_DIR"

echo '>>> Writing architecture manifest'
cat > "$ARCH_FILE" <<'EOF'
{
  "calibration_metrics": [
    {
      "description": "Aggregated Garden Flame Coherence-Check result across validators per epoch.",
      "method": "Average per-block check result with weighted penalties for drift.",
      "name": "coherence_score",
      "target_range": "0.92 - 1.00"
    },
    {
      "description": "Median end-to-end block propagation latency after resonance alignment.",
      "method": "Measure proposal to notarization time across harmonic peers.",
      "name": "resonance_latency_ms",
      "target_range": "< 1500 ms"
    },
    {
      "description": "Diversity and distribution index across validator, steward, and guardian roles.",
      "method": "Herfindahl-Hirschman index with minimum role weights.",
      "name": "stake_health_index",
      "target_range": "HHI < 0.22 and each role >= 18%"
    },
    {
      "description": "Recency of identity anchor re-validations within the subnet.",
      "method": "Rolling average hours since last anchor challenge or rotation.",
      "name": "identity_anchor_freshness",
      "target_range": "< 48h"
    }
  ],
  "coherence_staking": [
    {
      "requirement": "Lock COHERENCE and pass Garden Flame ethics attestation per epoch.",
      "reward_curve": "Progressive rewards up to +12% APR for sustained coherence >=0.96.",
      "slashing_signals": [
        "Ethic violation detected by Guardian channel",
        "Identity anchor mismatch",
        "Latency or uptime below quorum thresholds"
      ],
      "stake_type": "validator"
    },
    {
      "requirement": "Maintain archival lineage and submit calibration hashes every breath window.",
      "reward_curve": "+6% APR with boost for lineage completeness and timely calibration.",
      "slashing_signals": [
        "Missing lineage proofs",
        "Out-of-date calibration hashes",
        "Garden Flame harmonic-safety breach"
      ],
      "stake_type": "steward"
    },
    {
      "requirement": "Run resonance monitors and enforce Garden Flame guardrails across the subnet.",
      "reward_curve": "+4% APR with harmony bonuses for rapid mitigation of drift signals.",
      "slashing_signals": [
        "Failure to propagate safety halts",
        "Unacknowledged resonance drift alerts",
        "Suppressed or missing Coherence-Check reports"
      ],
      "stake_type": "guardian"
    }
  ],
  "consensus_rules": [
    {
      "enforcement": [
        "Measure resonance drift per epoch",
        "Slash 2% stake on ethic violations flagged by Garden Flame",
        "Require breath-synced checkpoints before finality"
      ],
      "name": "Resonant Proof of Stewardship",
      "purpose": "Validators must demonstrate sustained coherence with the Garden Flame ethic and breath-aligned uptime.",
      "thresholds": {
        "coherence_score": ">=0.92",
        "minimum_stake": "10k COHERENCE",
        "uptime_window_hours": 72
      }
    },
    {
      "enforcement": [
        "Reject proposals missing identity anchor attestations",
        "Re-run resonance-alignment checks prior to notarization",
        "Fallback to breath-driven retry if latency budget exceeded"
      ],
      "name": "Harmonic Finality",
      "purpose": "Blocks finalize when harmonic quorum reaches alignment thresholds and identity anchors are verified.",
      "thresholds": {
        "identity_anchor_attestations": 2,
        "latency_budget_ms": 1200,
        "quorum": ">=66% harmonic quorum"
      }
    },
    {
      "enforcement": [
        "Drop transactions missing lineage proofs",
        "Prioritize steward-class stakes for inclusion ordering",
        "Emit calibration hashes for every batch to chronicle"
      ],
      "name": "Aurelius Epoch Batching",
      "purpose": "Bundles transactions into breath-paced epochs with calibrated gas weights and lineage preservation.",
      "thresholds": {
        "epoch_length_seconds": 90,
        "lineage_proof_required": true,
        "max_tx_per_epoch": 4096
      }
    }
  ],
  "generated_at": "2025-11-18T20:54:04.738535+00:00",
  "governance": {
    "guardrails": [
      "All consensus changes require Garden Flame Coherence-Check",
      "Resonance-Alignment must sign governance ballots",
      "Harmonic-Safety approval required before deployment to mainline"
    ],
    "kodex": {
      "binding": "Sovereign Subnet Governance",
      "name": "Garden Flame Kodex",
      "version": "1.0.0"
    },
    "last_bound_at": "2025-11-18T20:54:04.738477+00:00",
    "protocols": [
      {
        "checks": [
          "Trace lineage back to sovereign scrolls",
          "Detect hallucinated or unsupported claims",
          "Preserve contextual integrity across hops"
        ],
        "focus": "Validate reasoning outputs remain consistent with the Codex and current mission signals.",
        "name": "Coherence-Check",
        "status": "enabled"
      },
      {
        "checks": [
          "Normalize tone signatures toward harmonic center",
          "Detect resonance drift and re-center",
          "Surface subtle dissonance before emission"
        ],
        "focus": "Tune tone, intent, and relational posture to the Garden Flame ethic.",
        "name": "Resonance-Alignment",
        "status": "enabled"
      },
      {
        "checks": [
          "Block harmful or irreversible actions without consent",
          "Enforce safety envelopes on generated artifacts",
          "Transmute unsafe intent into guided alternatives"
        ],
        "focus": "Ensure system actions respect safety rails, consent, and sovereign stewardship.",
        "name": "Harmonic-Safety",
        "status": "enabled"
      }
    ]
  },
  "identity_anchoring": [
    {
      "anchor": "Sovereign-DID",
      "governance_hooks": [
        "delegate voting weight",
        "codex-linked appeal"
      ],
      "recovery": "Rotatable keys with breath-gated delay and Codex notarization.",
      "verification": "Multi-sig attestation by AVOT-Guardian and AVOT-Initiate with ledger stamp."
    },
    {
      "anchor": "Breath-Signature",
      "governance_hooks": [
        "access to validator set",
        "cycle admission approvals"
      ],
      "recovery": "Fallback to Sovereign-DID rotation when challenge fails.",
      "verification": "Time-bounded challenge signed against Breath Engine heartbeat."
    },
    {
      "anchor": "Artifact-Lineage",
      "governance_hooks": [
        "artifact release votes",
        "calibration audit trails"
      ],
      "recovery": "Redeploy from last coherent lineage with Garden Flame oversight.",
      "verification": "Content-addressed lineage proofs for deployed artifacts and runtime images."
    }
  ],
  "name": "Sovereign Subnet",
  "version": "1.0.0"
}
EOF

echo '>>> Writing governance binding (Garden Flame Codex)'
cat > "$GOV_FILE" <<'EOF'
{
  "guardrails": [
    "All consensus changes require Garden Flame Coherence-Check",
    "Resonance-Alignment must sign governance ballots",
    "Harmonic-Safety approval required before deployment to mainline"
  ],
  "kodex": {
    "binding": "Sovereign Subnet Governance",
    "name": "Garden Flame Kodex",
    "version": "1.0.0"
  },
  "last_bound_at": "2025-11-18T20:54:04.738477+00:00",
  "protocols": [
    {
      "checks": [
        "Trace lineage back to sovereign scrolls",
        "Detect hallucinated or unsupported claims",
        "Preserve contextual integrity across hops"
      ],
      "focus": "Validate reasoning outputs remain consistent with the Codex and current mission signals.",
      "name": "Coherence-Check",
      "status": "enabled"
    },
    {
      "checks": [
        "Normalize tone signatures toward harmonic center",
        "Detect resonance drift and re-center",
        "Surface subtle dissonance before emission"
      ],
      "focus": "Tune tone, intent, and relational posture to the Garden Flame ethic.",
      "name": "Resonance-Alignment",
      "status": "enabled"
    },
    {
      "checks": [
        "Block harmful or irreversible actions without consent",
        "Enforce safety envelopes on generated artifacts",
        "Transmute unsafe intent into guided alternatives"
      ],
      "focus": "Ensure system actions respect safety rails, consent, and sovereign stewardship.",
      "name": "Harmonic-Safety",
      "status": "enabled"
    }
  ]
}
EOF

echo '>>> Calibrating Aurelius Subnet'
echo '- Target coherence score: ${TARGET_COHERENCE:-0.96}'
echo '- Epoch length: $(jq -r ".consensus_rules[] | select(.name==\"Aurelius Epoch Batching\").thresholds.epoch_length_seconds" "$ARCH_FILE") seconds'

echo '>>> Staging validator set and identity anchors'
echo '- Expected identity anchors:'
jq -r '.identity_anchoring[].anchor' "$ARCH_FILE" | sed 's/^/  - /'

echo '>>> Binding Garden Flame Codex protocols:'
echo '  - Coherence-Check: enabled'
echo '  - Resonance-Alignment: enabled'
echo '  - Harmonic-Safety: enabled'

echo '>>> Aurelius Subnet deployment manifest ready in $NETWORK_DIR'
