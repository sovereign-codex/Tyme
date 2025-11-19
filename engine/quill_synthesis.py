"""Synthesis utilities for the Quantum Intelligence Lattice and Quill engine."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List

from .quill_lattice import QuillLatticePrototype, build_quill_lattice_prototype, load_avot_quill


STOPWORDS = {
    "the",
    "and",
    "with",
    "from",
    "that",
    "this",
    "into",
    "for",
    "your",
    "repos",
    "repo",
    "code",
    "data",
    "github",
    "readme",
    "docs",
    "scrolls",
    "workflow",
    "workflows",
    "design",
    "lineage",
    "architecture",
    "patterns",
    "concepts",
    "scroll",
    "living",
    "kernel",
    "tyme",
    "core",
}


@dataclass
class RepositorySignal:
    """Semantic signals harvested from a single repository."""

    name: str
    root: Path
    headings: List[str]
    keywords: List[str]

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "root": str(self.root),
            "headings": self.headings,
            "keywords": self.keywords,
        }


def extract_keywords(text: str, limit: int = 12) -> List[str]:
    """Collect normalized keyword candidates from text blocks."""

    tokens = re.findall(r"[A-Za-z][A-Za-z0-9\-]{3,}", text)
    normalized = []
    for token in tokens:
        lowered = token.lower()
        if lowered in STOPWORDS:
            continue
        normalized.append(lowered)
    seen = []
    for keyword in normalized:
        if keyword not in seen:
            seen.append(keyword)
        if len(seen) >= limit:
            break
    return seen


def read_headings(path: Path) -> List[str]:
    """Extract Markdown headings from a README-like file."""

    headings: List[str] = []
    if not path.exists():
        return headings
    for line in path.read_text().splitlines():
        if line.lstrip().startswith("#"):
            title = line.lstrip("# ").strip()
            if title:
                headings.append(title)
    return headings


def scan_repository(root: Path) -> RepositorySignal:
    """Scan a repository root for headings and lightweight keywords."""

    readme_path = root / "README.md"
    if not readme_path.exists():
        fallback = next(root.glob("README*.md"), None)
        if fallback:
            readme_path = fallback

    headings = read_headings(readme_path)
    keyword_source = readme_path.read_text() if readme_path.exists() else ""
    keywords = extract_keywords(keyword_source)

    return RepositorySignal(name=root.name or str(root), root=root, headings=headings, keywords=keywords)


def cross_reference_signals(signals: Iterable[RepositorySignal]) -> Dict[str, object]:
    """Cross-reference repository signals to surface shared concepts."""

    concept_index: Dict[str, List[str]] = {}
    for signal in signals:
        for keyword in signal.keywords:
            concept_index.setdefault(keyword, []).append(signal.name)

    shared_concepts = {k: v for k, v in concept_index.items() if len(set(v)) > 1}
    pattern_signals = sorted(concept_index.keys(), key=lambda key: len(concept_index[key]), reverse=True)

    harmonic_mappings: List[Dict[str, object]] = []
    for signal in signals:
        harmonic_mappings.append(
            {
                "repository": signal.name,
                "harmonic_headings": signal.headings[:6],
                "dominant_signals": signal.keywords[:8],
                "shared": [kw for kw in signal.keywords if kw in shared_concepts],
            }
        )

    return {
        "pattern_signals": pattern_signals,
        "shared_concepts": shared_concepts,
        "harmonic_mappings": harmonic_mappings,
    }


def expand_quill_engine(lattice: QuillLatticePrototype, cross_refs: Dict[str, object]) -> Dict[str, object]:
    """Expand the lattice definition with synthesis cross-references."""

    lattice_dict = lattice.to_dict()
    pattern_signals: List[str] = cross_refs.get("pattern_signals", [])
    shared_concepts: Dict[str, List[str]] = cross_refs.get("shared_concepts", {})

    quantum_threads = [
        {"concept": concept, "repositories": repos, "channel": "conceptual-thread"}
        for concept, repos in shared_concepts.items()
    ]

    harmonic_overlays = [
        {
            "signal": signal,
            "binds": ["harmonic", "quantum"],
            "resonance": "pattern-recognition",
        }
        for signal in pattern_signals[:10]
    ]

    expansion = {
        "lattice": lattice_dict,
        "quantum_threads": quantum_threads,
        "harmonic_overlays": harmonic_overlays,
        "expansion_summary": {
            "shared_concept_count": len(shared_concepts),
            "pattern_signal_count": len(pattern_signals),
        },
    }

    return expansion


def build_quantum_intelligence_lattice(
    registry_path: Path,
    repository_roots: Iterable[Path],
    lattice_output: Path,
    expansion_output: Path,
) -> Dict[str, object]:
    """Perform the synthesis phase and persist lattice manifests."""

    quill_bundle = load_avot_quill(registry_path)
    activation = quill_bundle["agent"].activate(
        f"{quill_bundle['protocol'].tyme_core_binding}::Quill-Synthesis"
    )
    lattice = build_quill_lattice_prototype()

    signals = [scan_repository(root) for root in repository_roots]
    cross_refs = cross_reference_signals(signals)
    expansion = expand_quill_engine(lattice, cross_refs)

    timestamp = datetime.now(UTC).isoformat()
    quantum_manifest = {
        "phase": "Synthesis",
        "timestamp": timestamp,
        "quill_agent": quill_bundle["agent"].codename,
        "protocol": quill_bundle["protocol"].protocol_name,
        "activation": activation,
        "repositories": [signal.to_dict() for signal in signals],
        "cross_references": cross_refs,
        "lattice": lattice.to_dict(),
    }

    quill_expansion = {
        "engine": "Quill-core",
        "timestamp": timestamp,
        "binding": quill_bundle["protocol"].tyme_core_binding,
        "activation": activation,
        "expansion": expansion,
    }

    lattice_output.parent.mkdir(parents=True, exist_ok=True)
    expansion_output.parent.mkdir(parents=True, exist_ok=True)

    lattice_output.write_text(json.dumps(quantum_manifest, indent=2))
    expansion_output.write_text(json.dumps(quill_expansion, indent=2))

    return {
        "quantum_intelligence_lattice": quantum_manifest,
        "quill_engine_expansion": quill_expansion,
    }


__all__ = [
    "RepositorySignal",
    "build_quantum_intelligence_lattice",
    "cross_reference_signals",
    "expand_quill_engine",
    "extract_keywords",
    "scan_repository",
]
