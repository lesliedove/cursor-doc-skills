"""Load and manage test question banks from YAML files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class TestQuestion:
    """A single test question with ground-truth context."""

    id: str
    question: str
    product: str
    category: str
    ground_truth_topics: list[str] = field(default_factory=list)
    expected_key_facts: list[str] = field(default_factory=list)
    priority: str = "medium"

    @property
    def ground_truth_text(self) -> str:
        """Load and concatenate ground truth topic content from llm-docs."""
        import os

        docs_path = Path(os.environ.get("LLM_DOCS_PATH", r"C:\GitRepos\llm-docs"))
        texts = []
        for topic_path in self.ground_truth_topics:
            full_path = docs_path / topic_path
            if full_path.exists():
                texts.append(full_path.read_text(encoding="utf-8"))
        return "\n\n---\n\n".join(texts)


def load_question_bank(yaml_path: str | Path) -> list[TestQuestion]:
    """Load questions from a YAML file."""
    path = Path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Question bank not found: {path}")

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    questions = []
    for item in data.get("questions", []):
        questions.append(
            TestQuestion(
                id=item["id"],
                question=item["question"],
                product=item.get("product", ""),
                category=item.get("category", "general"),
                ground_truth_topics=item.get("ground_truth_topics", []),
                expected_key_facts=item.get("expected_key_facts", []),
                priority=item.get("priority", "medium"),
            )
        )
    return questions


def load_all_questions(questions_dir: str | Path = None) -> list[TestQuestion]:
    """Load all question bank YAML files from the questions directory."""
    if questions_dir is None:
        questions_dir = Path(__file__).parent.parent / "questions"
    else:
        questions_dir = Path(questions_dir)

    all_questions = []
    for yaml_file in sorted(questions_dir.glob("*.yaml")):
        all_questions.extend(load_question_bank(yaml_file))
    return all_questions
