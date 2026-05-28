"""Map test questions to ground-truth topics in the llm-docs corpus.

Reads YAML front matter from each llm-docs topic file and uses keyword
matching to suggest the best ground-truth topics for each question.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import yaml


def _load_topic_metadata(docs_path: Path) -> list[dict]:
    """Load YAML front matter from all topic files."""
    topics = []
    for md_file in sorted(docs_path.glob("*.md")):
        if md_file.name in ("llms.txt", "skipped-pages.md"):
            continue
        text = md_file.read_text(encoding="utf-8", errors="replace")
        match = re.match(r"^---\n(.+?)\n---", text, re.DOTALL)
        if not match:
            continue
        try:
            meta = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue

        if not isinstance(meta, dict):
            continue

        topics.append(
            {
                "file": md_file.name,
                "title": meta.get("title", ""),
                "keywords": meta.get("keywords", []),
                "summary": meta.get("summary", ""),
                "doc_type": meta.get("doc_type", ""),
                "source_book": meta.get("source_book", ""),
            }
        )
    return topics


def _score_topic(question: str, topic: dict) -> float:
    """Score how well a topic matches a question (0.0 - 1.0)."""
    q_words = set(re.findall(r"\w+", question.lower()))
    score = 0.0

    title_words = set(re.findall(r"\w+", topic["title"].lower()))
    title_overlap = len(q_words & title_words) / max(len(q_words), 1)
    score += title_overlap * 0.4

    kw_set = set()
    for kw in topic.get("keywords", []) or []:
        kw_set.update(re.findall(r"\w+", str(kw).lower()))
    kw_overlap = len(q_words & kw_set) / max(len(q_words), 1)
    score += kw_overlap * 0.3

    summary_words = set(re.findall(r"\w+", topic.get("summary", "").lower()))
    summary_overlap = len(q_words & summary_words) / max(len(q_words), 1)
    score += summary_overlap * 0.3

    return min(score, 1.0)


def suggest_ground_truth(
    question: str,
    product: str,
    llm_docs_path: str | Path = None,
    top_n: int = 3,
) -> list[dict]:
    """Suggest top-N ground truth topics for a question.

    Returns list of {"file": "...", "title": "...", "score": 0.X}
    """
    if llm_docs_path is None:
        llm_docs_path = Path(os.environ.get("LLM_DOCS_PATH", r"C:\GitRepos\llm-docs"))
    else:
        llm_docs_path = Path(llm_docs_path)

    product_dir = llm_docs_path / product.lower().replace(" ", "")
    if product.lower() == "modelcenter":
        product_dir = llm_docs_path / "modelcenter"
    elif product.lower() == "optislang":
        product_dir = llm_docs_path / "optislang"

    if not product_dir.exists():
        return []

    topics = _load_topic_metadata(product_dir)
    scored = []
    for topic in topics:
        s = _score_topic(question, topic)
        if s > 0.05:
            scored.append({"file": topic["file"], "title": topic["title"], "score": round(s, 3)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


def auto_map_question_bank(yaml_path: str | Path, llm_docs_path: str | Path = None):
    """Update a question bank YAML with suggested ground truth mappings."""
    path = Path(yaml_path)
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    product = data.get("metadata", {}).get("product", "")

    for q in data.get("questions", []):
        if q.get("ground_truth_topics"):
            continue
        suggestions = suggest_ground_truth(q["question"], product or q.get("product", ""), llm_docs_path)
        if suggestions:
            product_folder = "modelcenter" if "modelcenter" in product.lower() else "optislang"
            q["ground_truth_topics"] = [f"{product_folder}/{s['file']}" for s in suggestions]
            q["_suggested_titles"] = [f"{s['title']} (score: {s['score']})" for s in suggestions]

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Updated {path} with ground truth suggestions")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        auto_map_question_bank(sys.argv[1])
    else:
        questions_dir = Path(__file__).parent.parent / "questions"
        for yaml_file in questions_dir.glob("*.yaml"):
            auto_map_question_bank(yaml_file)
