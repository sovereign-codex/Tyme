"""Assimilation Engine for the Sovereign Codex repositories.

This script scans repositories in the `sovereign-codex` GitHub organization,
collects lightweight semantic signals (README headings, topics, workflows),
and writes a synthesized "Living Codex Kernel" report.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import textwrap
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable, List, Optional
import urllib.error
import urllib.request

API_BASE = "https://api.github.com"
DEFAULT_ORG = "sovereign-codex"
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
}


def github_request(url: str) -> Optional[dict]:
    """Perform a GitHub API request and return the parsed JSON body.

    Returns ``None`` on an HTTP error to keep the process resilient.
    """

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Tyme-Assimilation-Engine",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            if response.status >= 400:
                return None
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except urllib.error.HTTPError as exc:  # pragma: no cover - network dependent
        print(f"[WARN] GitHub request failed for {url}: {exc}")
        return None
    except urllib.error.URLError as exc:  # pragma: no cover - network dependent
        print(f"[WARN] Network error while reaching {url}: {exc}")
        return None


def fetch_repositories(org: str, limit: Optional[int] = None) -> List[dict]:
    """Fetch repository metadata for the given organization."""

    repositories: List[dict] = []
    page = 1
    while True:
        url = f"{API_BASE}/orgs/{org}/repos?per_page=100&page={page}"
        response = github_request(url)
        if response is None:
            break
        if not response:
            break
        repositories.extend(response)
        if limit and len(repositories) >= limit:
            return repositories[:limit]
        page += 1
    return repositories


def fetch_readme(owner: str, repo: str) -> str:
    """Retrieve and decode the README for a repository if it exists."""

    url = f"{API_BASE}/repos/{owner}/{repo}/readme"
    response = github_request(url)
    if not response:
        return ""

    content = response.get("content", "")
    encoding = response.get("encoding", "base64")
    try:
        if encoding == "base64":
            return base64.b64decode(content).decode("utf-8", errors="ignore")
        return content
    except Exception:  # pragma: no cover - depends on remote payload
        return ""


def fetch_workflows(owner: str, repo: str) -> List[str]:
    """List workflow files for a repository."""

    url = f"{API_BASE}/repos/{owner}/{repo}/contents/.github/workflows"
    response = github_request(url)
    if not response or not isinstance(response, list):
        return []

    workflows: List[str] = []
    for item in response:
        name = item.get("name") or item.get("path")
        if name:
            workflows.append(name)
    return workflows


def extract_headings(markdown: str) -> List[str]:
    """Extract Markdown headings as signals for concepts and architecture."""

    headings = []
    for line in markdown.splitlines():
        if line.lstrip().startswith("#"):
            title = line.lstrip("# ").strip()
            if title:
                headings.append(title)
    return headings


def derive_keywords(text_fragments: Iterable[str], limit: int = 12) -> List[str]:
    """Collect simple keyword signals from text fragments."""

    tokens = []
    for fragment in text_fragments:
        tokens.extend(re.findall(r"[A-Za-z][A-Za-z0-9\-]{3,}", fragment))

    counter = Counter(token.lower() for token in tokens if token.lower() not in STOPWORDS)
    return [word for word, _ in counter.most_common(limit)]


def format_repo_section(repo: dict, readme: str, workflows: List[str]) -> str:
    """Build the Living Codex section for a repository."""

    headings = extract_headings(readme)
    keyword_candidates = [repo.get("description") or "", " ".join(headings), repo.get("language") or ""]
    keyword_candidates.extend(repo.get("topics", []))
    concepts = derive_keywords(keyword_candidates, limit=8)

    architecture_signals = [h for h in headings if any(term in h.lower() for term in ("architecture", "pattern", "design"))]
    workflows_section = "\n".join(f"      - {name}" for name in workflows) if workflows else "      - None detected"

    lineage = f"Origin: {repo.get('created_at', 'unknown')}; Last pulse: {repo.get('pushed_at', 'unknown')}"

    return textwrap.dedent(
        f"""
        ## {repo.get('name', 'Unnamed Repository')}
        - **Description**: {repo.get('description') or 'No description provided.'}
        - **Concepts & Patterns**: {', '.join(concepts) if concepts else 'No dominant signals detected.'}
        - **Architectures & Lineage**: {', '.join(architecture_signals) if architecture_signals else 'Implicit or undocumented.'}
        - **Scrolls (Headings)**:
    {textwrap.indent('- ' + '\n- '.join(headings) if headings else '- None captured', '    ')}
        - **Workflows & Rituals**:
    {textwrap.indent(workflows_section, '    ')}
        - **Design Lineage**: {lineage}
        """
    ).strip()


def build_kernel(org: str, limit: Optional[int], output: Path) -> Path:
    """Execute the assimilation pass and write the Living Codex Kernel."""

    repositories = fetch_repositories(org, limit=limit)
    sections: List[str] = []
    for repo in repositories:
        name = repo.get("name")
        if not name:
            continue
        readme = fetch_readme(org, name)
        workflows = fetch_workflows(org, name)
        sections.append(format_repo_section(repo, readme, workflows))

    timestamp = datetime.now(UTC).isoformat(timespec="seconds")
    header = textwrap.dedent(
        f"""
        # Living Codex Kernel
        *Assimilation Engine pass for `{org}`*

        - **Generated**: {timestamp}
        - **Repositories scanned**: {len(repositories)}
        - **Token**: {'provided' if os.getenv('GITHUB_TOKEN') else 'anonymous (higher rate limits with GITHUB_TOKEN)'}

        The kernel captures surface semantics from Sovereign repositories: descriptions, topics, scroll headings,
        and workflow rituals. Extend this pass with deeper synthesis or recursive refinement as needed.
        """
    ).strip()

    content = header + "\n\n" + "\n\n".join(sections if sections else ["No repositories discovered."])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content + "\n", encoding="utf-8")
    print(f"[OK] Living Codex Kernel written to {output}")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assimilate Sovereign repositories into the Living Codex Kernel.")
    parser.add_argument("--org", default=DEFAULT_ORG, help="GitHub organization to scan (default: sovereign-codex)")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of repositories to scan (useful for quick passes)",
    )
    parser.add_argument(
        "--output",
        default="chronicle/living_codex_kernel.md",
        type=Path,
        help="Output path for the Living Codex Kernel",
    )
    return parser.parse_args()


def main() -> None:  # pragma: no cover - CLI entry point
    args = parse_args()
    build_kernel(org=args.org, limit=args.limit, output=args.output)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
