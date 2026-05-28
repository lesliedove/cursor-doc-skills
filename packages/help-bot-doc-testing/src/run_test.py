"""Main test runner -- queries engines, evaluates, generates report."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .question_bank import load_all_questions, TestQuestion
from .engines import OpenAIEngine, AnthropicEngine, PerplexityEngine, GeminiEngine, EngineResult
from .evaluate import evaluate_response, EvalScore
from .report import generate_report

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="bot-doc-test",
        description="Test how AI search engines answer questions about your product docs.",
    )
    parser.add_argument(
        "--product",
        help="Filter to a single product (e.g. ModelCenter, optiSLang)",
    )
    parser.add_argument(
        "--question-id",
        help="Run a single question by ID (e.g. mc-installation-001)",
    )
    parser.add_argument(
        "--engine",
        action="append",
        help="Limit to specific engine(s). Repeatable. (chatgpt, claude, perplexity, gemini)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be tested without making API calls",
    )
    parser.add_argument(
        "--skip-eval",
        action="store_true",
        help="Query engines but skip DeepEval scoring (faster, cheaper)",
    )
    parser.add_argument(
        "--questions-dir",
        type=Path,
        help="Path to questions directory (default: questions/)",
    )
    return parser.parse_args()


def get_active_engines(filter_names: list[str] | None = None) -> list:
    """Return engine instances for which API keys are configured."""
    import os

    all_engines = []
    if os.environ.get("OPENAI_API_KEY"):
        all_engines.append(OpenAIEngine())
    if os.environ.get("ANTHROPIC_API_KEY"):
        all_engines.append(AnthropicEngine())
    if os.environ.get("PERPLEXITY_API_KEY"):
        all_engines.append(PerplexityEngine())
    if os.environ.get("GOOGLE_API_KEY"):
        all_engines.append(GeminiEngine())

    if filter_names:
        filter_set = {n.lower() for n in filter_names}
        all_engines = [e for e in all_engines if e.name in filter_set]

    if not all_engines:
        console.print(
            "[bold red]No matching engines available![/] "
            "Set API keys in .env and check --engine filter.",
        )
        sys.exit(1)
    return all_engines


def filter_questions(
    questions: list[TestQuestion],
    product: str | None = None,
    question_id: str | None = None,
) -> list[TestQuestion]:
    """Apply product and question-id filters."""
    if question_id:
        matched = [q for q in questions if q.id == question_id]
        if not matched:
            console.print(f"[red]Question ID '{question_id}' not found.[/]")
            console.print("Available IDs:")
            for q in questions[:10]:
                console.print(f"  {q.id}")
            if len(questions) > 10:
                console.print(f"  ... and {len(questions) - 10} more")
            sys.exit(1)
        return matched

    if product:
        matched = [q for q in questions if q.product.lower() == product.lower()]
        if not matched:
            products = sorted(set(q.product for q in questions))
            console.print(f"[red]No questions for product '{product}'.[/]")
            console.print(f"Available products: {', '.join(products)}")
            sys.exit(1)
        return matched

    return questions


async def run_queries(
    questions: list[TestQuestion], engines: list
) -> list[EngineResult]:
    """Query all engines for all questions."""
    results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Querying {len(engines)} engines x {len(questions)} questions...",
            total=len(engines) * len(questions),
        )

        for engine in engines:
            for question in questions:
                result = await engine.query(question.question, question.product)
                results.append(result)
                progress.advance(task)

    return results


async def run_evaluations(
    questions: list[TestQuestion], results: list[EngineResult]
) -> list[EvalScore]:
    """Evaluate all results against ground truth."""
    scores = []

    question_map = {q.question: q for q in questions}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Evaluating {len(results)} responses...", total=len(results)
        )

        for result in results:
            question = question_map.get(result.question)
            if question:
                score = await evaluate_response(question, result)
                scores.append(score)
            progress.advance(task)

    return scores


def save_results(
    results: list[EngineResult], scores: list[EvalScore] | None = None
) -> Path:
    """Save raw results and scores to JSONL."""
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    results_path = results_dir / f"run_{timestamp}.jsonl"

    with open(results_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps({"type": "result", **r.to_dict()}) + "\n")
        if scores:
            for s in scores:
                f.write(json.dumps({"type": "score", **s.to_dict()}) + "\n")

    return results_path


def print_summary(scores: list[EvalScore]):
    """Print a quick summary table to the console."""
    table = Table(title="Test Results Summary")
    table.add_column("Engine", style="cyan")
    table.add_column("Pass", style="green")
    table.add_column("Fail", style="red")
    table.add_column("Error", style="yellow")
    table.add_column("Avg Correctness")

    engines = sorted(set(s.engine for s in scores))
    for eng in engines:
        eng_scores = [s for s in scores if s.engine == eng]
        eng_pass = sum(1 for s in eng_scores if s.overall_pass)
        eng_fail = sum(1 for s in eng_scores if not s.overall_pass and not s.errors)
        eng_err = sum(1 for s in eng_scores if s.errors)
        correctness_vals = [s.correctness for s in eng_scores if s.correctness is not None]
        avg = sum(correctness_vals) / len(correctness_vals) if correctness_vals else 0

        table.add_row(eng, str(eng_pass), str(eng_fail), str(eng_err), f"{avg:.2f}")

    console.print(table)


def print_dry_run(questions: list[TestQuestion], engines: list):
    """Show what would be tested without making API calls."""
    console.print("[bold]DRY RUN — no API calls will be made[/bold]")
    console.print()

    table = Table(title="Test Plan")
    table.add_column("#", style="dim")
    table.add_column("ID", style="cyan")
    table.add_column("Product")
    table.add_column("Category")
    table.add_column("Question")
    table.add_column("Ground Truth", style="dim")

    for i, q in enumerate(questions, 1):
        gt_status = f"{len(q.ground_truth_topics)} topics" if q.ground_truth_topics else "[red]NONE[/red]"
        table.add_row(
            str(i), q.id, q.product, q.category,
            q.question[:60] + ("..." if len(q.question) > 60 else ""),
            gt_status,
        )

    console.print(table)
    console.print()
    console.print(f"[bold]Engines:[/bold] {', '.join(e.name for e in engines)}")
    console.print(f"[bold]Total API calls:[/bold] {len(questions)} questions x {len(engines)} engines = {len(questions) * len(engines)}")
    console.print(f"[bold]Estimated eval calls:[/bold] {len(questions) * len(engines) * 3} (3 metrics per response)")
    console.print()

    no_gt = [q for q in questions if not q.ground_truth_topics]
    if no_gt:
        console.print(f"[yellow]Warning:[/yellow] {len(no_gt)} questions have no ground truth topics mapped.")
        console.print("  These will score as errors during evaluation.")
        console.print("  Run: python -m src.map_ground_truth to auto-suggest mappings")


async def main():
    """Main entry point."""
    load_dotenv()
    args = parse_args()

    console.print("[bold]AI Bot Doc Accuracy Testing[/bold]")
    console.print()

    # Load questions
    questions = load_all_questions(args.questions_dir)
    if not questions:
        console.print("[red]No questions found in questions/ directory.[/]")
        console.print("Create a YAML file like questions/myproduct.yaml")
        console.print("Or run: python -m src.discover_questions to seed one")
        sys.exit(1)

    # Apply filters
    questions = filter_questions(questions, args.product, args.question_id)
    console.print(f"Loaded [bold]{len(questions)}[/bold] test questions")

    # Get active engines
    engines = get_active_engines(args.engine)
    console.print(
        f"Active engines: [bold]{', '.join(e.name for e in engines)}[/bold]"
    )
    console.print()

    # Dry run?
    if args.dry_run:
        print_dry_run(questions, engines)
        return

    # Query
    results = await run_queries(questions, engines)
    console.print(f"[green]Collected {len(results)} responses[/green]")

    # Evaluate (unless skipped)
    scores = None
    if not args.skip_eval:
        console.print()
        scores = await run_evaluations(questions, results)

    # Save
    results_path = save_results(results, scores)
    console.print(f"\nRaw results saved to: {results_path}")

    # Report (only if we have scores)
    if scores:
        report_path = generate_report(questions, results, scores)
        console.print(f"Gap report saved to: [bold]{report_path}[/bold]")
        console.print()
        print_summary(scores)
    else:
        console.print()
        console.print("[dim]Evaluation skipped (--skip-eval). No report generated.[/dim]")
        console.print("Results saved — you can score them later with: python -m src.evaluate_results")


def main_sync():
    """Synchronous entry point for console_scripts."""
    asyncio.run(main())


if __name__ == "__main__":
    main_sync()
