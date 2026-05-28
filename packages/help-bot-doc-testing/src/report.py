"""Generate markdown gap reports from test results."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .evaluate import EvalScore
from .engines.base import EngineResult
from .question_bank import TestQuestion


def generate_report(
    questions: list[TestQuestion],
    results: list[EngineResult],
    scores: list[EvalScore],
    output_dir: str | Path = None,
) -> Path:
    """Generate a markdown gap report from evaluation results."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "reports"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    report_path = output_dir / f"gap_report_{timestamp}.md"

    question_map = {q.id: q for q in questions}
    result_map: dict[tuple[str, str], EngineResult] = {}
    for r in results:
        for q in questions:
            if r.question == q.question:
                result_map[(q.id, r.engine)] = r

    engines = sorted(set(s.engine for s in scores))
    passing = [s for s in scores if s.overall_pass]
    failing = [s for s in scores if not s.overall_pass and not s.errors]
    errored = [s for s in scores if s.errors]

    lines = [
        f"# AI Bot Doc Accuracy Report",
        f"",
        f"*Generated: {datetime.now(timezone.utc).isoformat()}*",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Questions tested | {len(questions)} |",
        f"| Engines tested | {', '.join(engines)} |",
        f"| Total evaluations | {len(scores)} |",
        f"| Passing | {len(passing)} ({_pct(len(passing), len(scores))}) |",
        f"| Failing | {len(failing)} ({_pct(len(failing), len(scores))}) |",
        f"| Errors | {len(errored)} |",
        f"",
    ]

    # Per-engine summary
    lines.append("## Per-Engine Results")
    lines.append("")
    lines.append("| Engine | Pass | Fail | Error | Avg Correctness | Cites AnsysHelp |")
    lines.append("|--------|------|------|-------|-----------------|-----------------|")
    for eng in engines:
        eng_scores = [s for s in scores if s.engine == eng]
        eng_pass = sum(1 for s in eng_scores if s.overall_pass)
        eng_fail = sum(1 for s in eng_scores if not s.overall_pass and not s.errors)
        eng_err = sum(1 for s in eng_scores if s.errors)
        avg_correct = _avg([s.correctness for s in eng_scores if s.correctness is not None])
        cites_pct = _pct(
            sum(1 for s in eng_scores if s.cites_ansys_help), len(eng_scores)
        )
        lines.append(
            f"| {eng} | {eng_pass} | {eng_fail} | {eng_err} | {avg_correct:.2f} | {cites_pct} |"
        )
    lines.append("")

    # Failing questions (the gaps)
    if failing:
        lines.append("## Documentation Gaps (Failing Questions)")
        lines.append("")
        lines.append("These questions got incorrect or incomplete answers from AI engines.")
        lines.append("")

        failing_by_question: dict[str, list[EvalScore]] = {}
        for s in failing:
            failing_by_question.setdefault(s.question_id, []).append(s)

        for qid, qscores in sorted(failing_by_question.items()):
            q = question_map.get(qid)
            if not q:
                continue
            lines.append(f"### {qid}: {q.question}")
            lines.append(f"")
            lines.append(f"- **Product:** {q.product}")
            lines.append(f"- **Category:** {q.category}")
            lines.append(f"- **Priority:** {q.priority}")
            lines.append(f"- **Ground truth topics:** {', '.join(q.ground_truth_topics)}")
            lines.append(f"- **Expected key facts:** {', '.join(q.expected_key_facts)}")
            lines.append(f"")
            lines.append(f"| Engine | Correctness | Faithfulness | Cites Help |")
            lines.append(f"|--------|-------------|--------------|------------|")
            for s in qscores:
                lines.append(
                    f"| {s.engine} | {_fmt_score(s.correctness)} | "
                    f"{_fmt_score(s.faithfulness)} | {'Yes' if s.cites_ansys_help else 'No'} |"
                )
            lines.append("")

    # Source attribution analysis
    lines.append("## Source Attribution")
    lines.append("")
    lines.append("How often do engines cite ansyshelp.ansys.com as a source?")
    lines.append("")
    for eng in engines:
        eng_scores = [s for s in scores if s.engine == eng]
        cite_count = sum(1 for s in eng_scores if s.cites_ansys_help)
        lines.append(f"- **{eng}:** {cite_count}/{len(eng_scores)} ({_pct(cite_count, len(eng_scores))})")
    lines.append("")

    # Recommendations
    lines.append("## Recommended Actions")
    lines.append("")
    if failing:
        lines.append("1. Review failing questions above and update source documentation")
        lines.append("2. Regenerate llm-docs corpus after fixes")
        lines.append("3. Wait for crawler cycle (1-4 weeks depending on engine)")
        lines.append("4. Rerun this test to verify improvement")
    else:
        lines.append("All questions passing! Consider expanding the question bank.")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def _pct(num: int, total: int) -> str:
    if total == 0:
        return "0%"
    return f"{num * 100 // total}%"


def _avg(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _fmt_score(score: float | None) -> str:
    if score is None:
        return "—"
    return f"{score:.2f}"
