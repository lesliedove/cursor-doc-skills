"""Discover real user questions from multiple sources.

Sources (in order of preference):
1. Site search analytics (CSV/JSON import from GA4, Adobe, or platform logs)
2. Community forum scraping (discuss.ansys.com)
3. AI engine monitoring (Promptwatch/Peec export)
4. Web search mining (Google autocomplete, People Also Ask)
5. Support ticket keyword export

This script normalizes questions from any source into the standard
question bank YAML format for testing.
"""

from __future__ import annotations

import json
import csv
from pathlib import Path
from dataclasses import dataclass, field

import yaml


@dataclass
class DiscoveredQuestion:
    """A question discovered from a user data source."""

    question: str
    source: str
    product: str = ""
    category: str = "general"
    frequency: int = 0
    url: str = ""


def import_search_analytics(csv_path: str | Path) -> list[DiscoveredQuestion]:
    """Import from site search analytics CSV.

    Expected columns: query, product, count
    (GA4 export, Adobe Analytics export, or platform search logs)
    """
    questions = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = row.get("query", "").strip()
            if not query:
                continue
            questions.append(
                DiscoveredQuestion(
                    question=_normalize_to_question(query),
                    source="search_analytics",
                    product=row.get("product", ""),
                    frequency=int(row.get("count", 0)),
                )
            )
    return questions


def import_forum_questions(json_path: str | Path) -> list[DiscoveredQuestion]:
    """Import forum thread titles/questions from a JSON export.

    Expected format: [{"title": "...", "url": "...", "product": "..."}, ...]
    """
    questions = []
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        title = item.get("title", "").strip()
        if not title:
            continue
        questions.append(
            DiscoveredQuestion(
                question=_normalize_to_question(title),
                source="forum",
                product=item.get("product", ""),
                url=item.get("url", ""),
            )
        )
    return questions


def import_ai_monitoring(json_path: str | Path) -> list[DiscoveredQuestion]:
    """Import from Promptwatch/Peec/Otterly AI monitoring export.

    Expected format: [{"prompt": "...", "product": "...", "engines": [...], "frequency": N}, ...]
    """
    questions = []
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        prompt = item.get("prompt", "").strip()
        if not prompt:
            continue
        questions.append(
            DiscoveredQuestion(
                question=prompt,
                source="ai_monitoring",
                product=item.get("product", ""),
                frequency=item.get("frequency", 0),
            )
        )
    return questions


def _normalize_to_question(text: str) -> str:
    """Turn a search query or forum title into a natural question."""
    text = text.strip()
    if text.endswith("?"):
        return text
    lower = text.lower()
    if lower.startswith(("how", "what", "why", "where", "when", "can", "does", "is")):
        return text + "?"
    return f"How do I {text[0].lower()}{text[1:]}?" if text else text


def _categorize(question: str) -> str:
    """Auto-categorize based on keywords."""
    q = question.lower()
    if any(w in q for w in ("install", "setup", "system req", "prerequisite", "download")):
        return "installation"
    if any(w in q for w in ("license", "licensing", "activation", "seat")):
        return "licensing"
    if any(w in q for w in ("error", "fail", "crash", "not working", "problem", "issue", "bug")):
        return "troubleshooting"
    if any(w in q for w in ("python", "api", "script", "automat", "batch", "command line")):
        return "api_scripting"
    if any(w in q for w in ("optimi", "sensitiv", "doe", "design of experiment", "mop")):
        return "optimization"
    if any(w in q for w in ("workflow", "integrat", "connect", "link", "wrap")):
        return "workflow_integration"
    if any(w in q for w in ("mbse", "requirement", "sam", "sysml")):
        return "mbse"
    if any(w in q for w in ("configur", "setting", "preference", "option")):
        return "configuration"
    return "general"


def deduplicate(questions: list[DiscoveredQuestion]) -> list[DiscoveredQuestion]:
    """Remove near-duplicate questions, keeping highest-frequency version."""
    seen: dict[str, DiscoveredQuestion] = {}
    for q in questions:
        key = q.question.lower().strip("? .")
        if key in seen:
            if q.frequency > seen[key].frequency:
                seen[key] = q
        else:
            seen[key] = q
    return list(seen.values())


def export_to_yaml(
    questions: list[DiscoveredQuestion],
    output_path: str | Path,
    product: str = "",
    prefix: str = "q",
) -> Path:
    """Export discovered questions to the test question bank YAML format.

    Ground truth topics are left blank -- those need to be mapped
    manually or via a separate matching step.
    """
    output_path = Path(output_path)
    items = []
    for i, q in enumerate(questions, 1):
        q.category = _categorize(q.question)
        items.append(
            {
                "id": f"{prefix}-{q.category}-{i:03d}",
                "question": q.question,
                "product": product or q.product,
                "category": q.category,
                "source": q.source,
                "frequency": q.frequency,
                "ground_truth_topics": [],
                "expected_key_facts": [],
                "priority": "high" if q.frequency > 10 else "medium",
            }
        )

    data = {
        "metadata": {
            "product": product,
            "generated_from": list(set(q.source for q in questions)),
            "total_questions": len(items),
            "note": (
                "ground_truth_topics and expected_key_facts need to be filled in "
                "by mapping to llm-docs corpus topics."
            ),
        },
        "questions": items,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return output_path


# --- Convenience: seed from hardcoded real-world questions ---

KNOWN_MC_QUESTIONS = [
    # From forums, web searches, training course descriptions, and common support patterns
    ("How do I install ModelCenter Desktop?", "installation", 25),
    ("What are the system requirements for ModelCenter?", "installation", 20),
    ("How do I install ModelCenter Remote Execution (MCRE)?", "installation", 15),
    ("How do I configure ModelCenter to use a license server?", "licensing", 18),
    ("How do I create a workflow in ModelCenter?", "workflow_integration", 30),
    ("How do I wrap an Excel spreadsheet as a ModelCenter component?", "workflow_integration", 22),
    ("How do I connect ModelCenter to MATLAB?", "workflow_integration", 20),
    ("How do I integrate ModelCenter with Ansys Workbench?", "workflow_integration", 18),
    ("How do I use ModelCenter with Python scripting?", "api_scripting", 25),
    ("How do I run a ModelCenter workflow from the command line?", "api_scripting", 15),
    ("How do I use the ModelCenter API to create components programmatically?", "api_scripting", 12),
    ("How do I set up ModelCenter MBSE with Ansys SAM?", "mbse", 15),
    ("What is ModelCenter MBSE and how does it connect to systems models?", "mbse", 12),
    ("How do I use ModelCenter with Cameo Systems Modeler?", "mbse", 10),
    ("How do I perform a trade study in ModelCenter?", "optimization", 20),
    ("How do I use the Data Explorer in ModelCenter?", "optimization", 15),
    ("How do I use Design of Experiments (DOE) in ModelCenter?", "optimization", 18),
    ("How do I configure remote execution in ModelCenter?", "configuration", 15),
    ("How do I set up distributed computing with ModelCenter?", "configuration", 12),
    ("How do I debug a failing component in a ModelCenter workflow?", "troubleshooting", 15),
    ("ModelCenter workflow fails with connection error - how to fix?", "troubleshooting", 12),
    ("How do I migrate workflows from an older version of ModelCenter?", "troubleshooting", 10),
    ("How do I wrap a custom executable as a ModelCenter component?", "workflow_integration", 18),
    ("How do I link variables between components in ModelCenter?", "workflow_integration", 20),
    ("How do I use ModelCenter plugins for third-party tools?", "workflow_integration", 12),
]

KNOWN_OSL_QUESTIONS = [
    # From forums (discuss.ansys.com), web searches, tutorials, training courses
    ("How do I install optiSLang standalone?", "installation", 20),
    ("What are the system requirements for optiSLang?", "installation", 15),
    ("How do I run optiSLang in batch mode?", "api_scripting", 25),
    ("How do I pass arguments to optiSLang in batch mode?", "api_scripting", 20),
    ("How do I automate optiSLang using PyOptiSLang?", "api_scripting", 22),
    ("PyOptiSLang RuntimeError: Cannot get optiSLang server port - how to fix?", "troubleshooting", 18),
    ("How do I set up a sensitivity analysis in optiSLang?", "optimization", 30),
    ("How do I perform optimization of a damped oscillator in optiSLang?", "optimization", 20),
    ("How do I use the Metamodel of Optimal Prognosis (MOP) in optiSLang?", "optimization", 22),
    ("What is the Coefficient of Prognosis (CoP) in optiSLang?", "optimization", 18),
    ("How do I use AMOP (Adaptive MOP) in optiSLang?", "optimization", 15),
    ("How do I set up a Design of Experiments (DOE) in optiSLang?", "optimization", 25),
    ("How do I integrate optiSLang with Ansys Workbench?", "workflow_integration", 25),
    ("How do I connect optiSLang to Ansys Mechanical?", "workflow_integration", 20),
    ("How do I use optiSLang with Ansys Fluent?", "workflow_integration", 18),
    ("How do I use optiSLang with MATLAB?", "workflow_integration", 15),
    ("How do I use optiSLang with Excel?", "workflow_integration", 15),
    ("How do I perform robust design optimization in optiSLang?", "optimization", 15),
    ("How do I perform reliability analysis in optiSLang?", "optimization", 12),
    ("How do I use Python code objects with optiSLang in Mechanical?", "api_scripting", 18),
    ("Script works in standalone Mechanical but fails in optiSLang - why?", "troubleshooting", 15),
    ("How do I configure optiSLang licensing?", "licensing", 12),
    ("How do I use signal data analysis in optiSLang?", "optimization", 10),
    ("How do I create a parametric study in optiSLang?", "optimization", 20),
    ("How do I use the optiSLang post-processing features?", "optimization", 15),
]


def seed_question_banks(output_dir: str | Path = None):
    """Generate initial question bank YAML files from known real-world questions."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "questions"
    output_dir = Path(output_dir)

    mc_questions = [
        DiscoveredQuestion(
            question=q, source="web_research", product="ModelCenter",
            category=cat, frequency=freq,
        )
        for q, cat, freq in KNOWN_MC_QUESTIONS
    ]
    export_to_yaml(mc_questions, output_dir / "modelcenter.yaml", product="ModelCenter", prefix="mc")

    osl_questions = [
        DiscoveredQuestion(
            question=q, source="web_research", product="optiSLang",
            category=cat, frequency=freq,
        )
        for q, cat, freq in KNOWN_OSL_QUESTIONS
    ]
    export_to_yaml(osl_questions, output_dir / "optislang.yaml", product="optiSLang", prefix="osl")

    print(f"Seeded {len(mc_questions)} ModelCenter questions -> {output_dir / 'modelcenter.yaml'}")
    print(f"Seeded {len(osl_questions)} optiSLang questions -> {output_dir / 'optislang.yaml'}")
    print()
    print("Next steps:")
    print("  1. Get site search analytics (GA4/Adobe CSV) and run: import_search_analytics()")
    print("  2. Get AI monitoring data (Promptwatch/Peec export) and run: import_ai_monitoring()")
    print("  3. Map ground_truth_topics to llm-docs corpus files")
    print("  4. Fill in expected_key_facts for each question")


if __name__ == "__main__":
    seed_question_banks()
