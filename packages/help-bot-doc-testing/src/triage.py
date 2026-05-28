"""Generate a triage-ready markdown from test results.

For each failing or partial question, diagnoses the root cause and
proposes a specific doc fix with source topics to update.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class TriageItem:
    """A single doc improvement recommendation."""

    question_id: str
    question: str
    product: str
    category: str
    verdict: str  # FAIL, PARTIAL, PASS
    root_cause: str  # crawlability, content_gap, fragmentation, overshadowed
    diagnosis: str
    source_topics: list[str]
    proposed_fix: str
    priority: str  # P1, P2, P3
    effort: str  # small, medium, large


def diagnose_result(
    question: str,
    verdict: str,
    cites_ansys_help: bool,
    response_complete: bool,
    response_has_steps: bool,
    competing_source: str = "",
) -> tuple[str, str]:
    """Determine root cause and diagnosis from test observations."""

    if not cites_ansys_help and competing_source:
        return (
            "overshadowed",
            f"Bots don't find ansyshelp.ansys.com at all. "
            f"{competing_source} dominates search results. "
            f"Our product docs are either not crawlable or not indexed.",
        )

    if cites_ansys_help and not response_complete and not response_has_steps:
        return (
            "fragmentation",
            "Bots find our help site but can only reach index/TOC pages. "
            "The actual content is behind iframes or JS navigation that "
            "crawlers can't follow. Answer is assembled from page titles "
            "and summaries, not real content.",
        )

    if cites_ansys_help and not response_has_steps:
        return (
            "crawlability",
            "Bots find and cite our help pages but can't extract "
            "procedure steps. Content pages may be reachable but structured "
            "in a way that loses step-by-step detail during crawling.",
        )

    if not cites_ansys_help:
        return (
            "content_gap",
            "No relevant content found on ansyshelp.ansys.com for this question. "
            "Either the topic doesn't exist in our docs or it's not indexed.",
        )

    return ("unknown", "Needs manual investigation.")


def generate_triage(items: list[TriageItem], output_dir: str | Path = None) -> Path:
    """Generate the triage markdown from a list of items."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "results"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = output_dir / f"triage_{timestamp}.md"

    failing = [i for i in items if i.verdict in ("FAIL", "PARTIAL")]
    passing = [i for i in items if i.verdict == "PASS"]

    by_cause: dict[str, list[TriageItem]] = {}
    for item in failing:
        by_cause.setdefault(item.root_cause, []).append(item)

    cause_labels = {
        "crawlability": "Crawlability -- content exists but bots can't extract it",
        "fragmentation": "Fragmentation -- answer spread across too many pages / behind iframes",
        "content_gap": "Content Gap -- topic missing or not indexed",
        "overshadowed": "Overshadowed -- competing docs outrank our help site",
        "unknown": "Unknown -- needs manual investigation",
    }

    lines = [
        "# Doc Improvement Triage",
        "",
        f"*Generated: {datetime.now(timezone.utc).isoformat()}*",
        f"*Source: Manual test run against AI search engines*",
        f"*ADO parent: #1457082*",
        "",
        "## Summary",
        "",
        f"- **Tested:** {len(items)} questions",
        f"- **Passing:** {len(passing)}",
        f"- **Needing action:** {len(failing)}",
        "",
        "### By Root Cause",
        "",
        "| Root Cause | Count | Items |",
        "|------------|-------|-------|",
    ]

    for cause, cause_items in sorted(by_cause.items()):
        ids = ", ".join(i.question_id for i in cause_items)
        lines.append(f"| {cause_labels.get(cause, cause)} | {len(cause_items)} | {ids} |")

    lines.extend([
        "",
        "### By Priority",
        "",
        "| Priority | Count |",
        "|----------|-------|",
        f"| P1 (high-traffic, wrong answer) | {sum(1 for i in failing if i.priority == 'P1')} |",
        f"| P2 (incomplete answer) | {sum(1 for i in failing if i.priority == 'P2')} |",
        f"| P3 (minor gap) | {sum(1 for i in failing if i.priority == 'P3')} |",
        "",
        "---",
        "",
    ])

    for item in sorted(failing, key=lambda x: ("P1", "P2", "P3").index(x.priority) if x.priority in ("P1", "P2", "P3") else 9):
        lines.extend([
            f"## {item.question_id}: {item.question}",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Product | {item.product} |",
            f"| Category | {item.category} |",
            f"| Verdict | **{item.verdict}** |",
            f"| Priority | **{item.priority}** |",
            f"| Effort | {item.effort} |",
            f"| Root Cause | {item.root_cause} |",
            "",
            f"### Diagnosis",
            "",
            item.diagnosis,
            "",
            f"### Source Topics to Update",
            "",
        ])
        for topic in item.source_topics:
            lines.append(f"- `{topic}`")
        lines.extend([
            "",
            f"### Proposed Fix",
            "",
            item.proposed_fix,
            "",
            "---",
            "",
        ])

    if passing:
        lines.extend([
            "## Passing Questions (No Action Needed)",
            "",
        ])
        for item in passing:
            lines.append(f"- **{item.question_id}:** {item.question}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
