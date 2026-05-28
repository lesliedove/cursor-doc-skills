# AI Bot Documentation Accuracy Testing

**ADO Ticket:** [1457082](https://tfs.ansys.com:8443/tfs/ANSYS_Development/Portfolio/_workitems/edit/1457082) (child of 1450897)

Test how AI search engines answer questions about Ansys product documentation, score accuracy against ground truth, and identify doc gaps to fix.

## Quick Start

```bash
pip install -e .
cp .env.example .env   # fill in API keys
python -m src.run_test --dry-run          # preview test plan
python -m src.run_test --engine claude    # run with one engine
python -m src.run_test                    # full run (all engines)
```

## What It Does

1. **Questions** — YAML files define test questions with ground-truth answers from the llm-docs corpus
2. **Query** — Each question is sent to AI engines (ChatGPT, Claude, Perplexity, Gemini)
3. **Evaluate** — DeepEval scores each response for correctness, faithfulness, and relevancy
4. **Report** — Gap report identifies where bots give wrong answers and which docs need fixing

## CLI Options

```
python -m src.run_test [OPTIONS]

  --product TEXT       Filter to one product (e.g. ModelCenter, optiSLang)
  --question-id TEXT   Run a single question by ID
  --engine TEXT        Limit to specific engine(s). Repeatable.
                       Values: chatgpt, claude, perplexity, gemini
  --dry-run            Show test plan without making API calls
  --skip-eval          Query engines but skip DeepEval scoring
  --questions-dir PATH Custom path to questions directory
```

## Project Structure

```
bot-doc-testing/
├── questions/           # Test question banks (YAML)
│   ├── modelcenter.yaml
│   └── optislang.yaml
├── src/
│   ├── engines/         # AI engine query adapters
│   │   ├── base.py
│   │   ├── openai_engine.py
│   │   ├── anthropic_engine.py
│   │   ├── perplexity_engine.py
│   │   └── gemini_engine.py
│   ├── evaluate.py      # DeepEval scoring
│   ├── question_bank.py # Load and manage test questions
│   ├── run_test.py      # Main test runner + CLI
│   ├── report.py        # Generate gap reports
│   ├── triage.py        # Root-cause diagnosis
│   ├── discover_questions.py  # Import questions from analytics/forums
│   └── map_ground_truth.py    # Auto-map questions to llm-docs topics
├── samples/             # Example output (see what a run produces)
├── results/             # Raw JSON results per run (gitignored)
├── reports/             # Markdown gap reports (gitignored)
├── ONBOARDING.md        # Adoption guide for other teams
├── pyproject.toml
├── requirements.txt
└── .env.example
```

## Adopting for Your Product

This toolkit is product-agnostic. See **[ONBOARDING.md](ONBOARDING.md)** for the full guide. Summary:

1. Create `questions/<yourproduct>.yaml` with 5-25 test questions
2. Point `LLM_DOCS_PATH` at your product's llm-docs folder
3. Map ground-truth topics (auto or manual)
4. Run `python -m src.run_test --product YourProduct`

## Engines Tested

| Engine | API | Notes |
|--------|-----|-------|
| ChatGPT | OpenAI Responses API + web search | Most popular consumer AI |
| Claude | Anthropic Messages API + web_search tool | Strong at technical content |
| Perplexity | Chat Completions API | Built-in web search, returns citations |
| Gemini | Google Generative Language API + grounding | Powers AI Overviews in Google Search |

## Scoring

| Metric | Measures | Pass Threshold |
|--------|----------|----------------|
| Correctness | Facts match ground truth | >= 0.6 |
| Faithfulness | Response sticks to verifiable info | >= 0.5 |
| Relevancy | Response answers the question asked | >= 0.5 |

A response passes overall if correctness >= 0.6 AND faithfulness >= 0.5.

## Cost

~$0.04–$0.15 per question per engine (query + 3 eval metrics). A 50-question x 4-engine run costs roughly $8–$30 in API calls. Use `--skip-eval` or `--engine` to control cost during development.

## Results So Far

Initial 50-question pilot (25 ModelCenter + 25 optiSLang) tested manually:
- **32% pass, 46% partial, 22% fail** overall
- ModelCenter: 24% pass rate
- optiSLang: 40% pass rate
- Primary failure mode: GUI procedure content invisible to crawlers

See `results/manual_run_2026-05-14.md` for detailed findings.

---

## Credits

Built by **Leslie Poff** (`ldove@synopsys.com`), Staff Engineer, ModelCenter and optiSLang Collaborative Services Team.

Part of the **[`cursor-doc-skills`](https://github.com/lesliedove/cursor-doc-skills)** catalog. Issues, new question banks for other products, or evaluation-engine additions — open an issue on the repo or ping Leslie on Teams.
