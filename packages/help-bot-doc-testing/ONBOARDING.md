# Adopting This Toolkit for Your Product

This guide walks you through setting up bot-doc-testing for a new Ansys product in about 30 minutes.

## Prerequisites

- Python 3.10+
- At least one API key: OpenAI, Anthropic, Perplexity, or Google Gemini
- Your product's llm-docs corpus (the Markdown files from the llm-docs conversion pipeline)

## Step 1: Install

```bash
cd bot-doc-testing
pip install -e .
cp .env.example .env
# Edit .env — add your API keys and set LLM_DOCS_PATH
```

## Step 2: Create Your Question Bank

Create a YAML file at `questions/<yourproduct>.yaml`:

```yaml
metadata:
  product: YourProduct
  generated_from:
  - manual
  total_questions: 5
  note: Start small. 5-10 high-traffic questions is enough for a first run.

questions:
- id: yp-installation-001
  question: "How do I install YourProduct?"
  product: YourProduct
  category: installation
  source: manual
  frequency: 30
  ground_truth_topics:
  - yourproduct/yp-installation-guide.md
  expected_key_facts:
  - "Windows and Linux supported"
  - "Requires Java 11+"
  - "Run installer as administrator"
  priority: high
```

### Question Bank Schema

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique ID. Convention: `prefix-category-NNN` |
| `question` | Yes | The exact question to send to AI engines |
| `product` | Yes | Product name (used for filtering and ground truth lookup) |
| `category` | Yes | One of: installation, licensing, workflow_integration, api_scripting, optimization, mbse, configuration, troubleshooting, general |
| `source` | No | Where the question came from (manual, web_research, search_analytics, forum, ai_monitoring) |
| `frequency` | No | Relative frequency/importance (higher = more users ask this) |
| `ground_truth_topics` | Yes | Paths to llm-docs files that should answer this question |
| `expected_key_facts` | No | Specific facts a correct answer must include |
| `priority` | No | high or medium (high = frequency > 10) |

### Where to Find Questions

Best sources for real user questions, in order of quality:

1. **Site search analytics** — What do users search for on your help site? (Adobe Analytics Internal Search report)
2. **Community forums** — discuss.ansys.com threads tagged with your product
3. **Support tickets** — Common question patterns from customer support
4. **AI monitoring** — Tools like Otterly.ai or Peec that track what users ask AI engines about your product
5. **Google autocomplete** — Type "how to [product name]" and see suggestions
6. **Web research** — What shows up when you Google your product + common tasks

The `discover_questions.py` module can import from CSV (search analytics) and JSON (forum, AI monitoring) exports.

## Step 3: Map Ground Truth

Ground truth topics are the llm-docs files that contain the correct answer. The toolkit scores AI engine responses against this content.

**Option A: Auto-suggest (fast, imprecise)**

```bash
python -m src.map_ground_truth questions/yourproduct.yaml
```

This uses keyword matching to suggest topics. Review the `_suggested_titles` field it adds — scores below 0.4 are likely wrong and need manual correction.

**Option B: Manual mapping (slower, accurate)**

Browse your `llm-docs/<yourproduct>/` folder and find the file(s) that best answer each question. Put the relative path in `ground_truth_topics`.

**Tip:** A question can have multiple ground truth topics. If the answer spans multiple pages, list all of them — the evaluator concatenates their content.

## Step 4: First Run

Start with a dry run to verify your setup:

```bash
python -m src.run_test --product YourProduct --dry-run
```

This shows the test plan without making any API calls. Check that:
- All your questions loaded
- Ground truth topics show "N topics" (not "NONE")
- Expected engines are listed

Then run for real (start with one engine to save cost):

```bash
python -m src.run_test --product YourProduct --engine claude
```

Or run a single question to verify the pipeline works:

```bash
python -m src.run_test --question-id yp-installation-001
```

## Step 5: Read Your Report

After a run, you'll find:
- `results/run_YYYY-MM-DD_HHMM.jsonl` — Raw results + scores (machine-readable)
- `reports/gap_report_YYYY-MM-DD_HHMM.md` — Human-readable gap report

See `samples/` for example output.

## Understanding Scores

### Metrics

| Metric | What It Measures | Threshold |
|--------|-----------------|-----------|
| **Correctness** | Are the facts in the response accurate vs. ground truth? | >= 0.6 to pass |
| **Faithfulness** | Does the response stick to verifiable information? | >= 0.5 to pass |
| **Answer Relevancy** | Does the response actually answer the question asked? | >= 0.5 (informational) |

A response **passes** if correctness >= 0.6 AND faithfulness >= 0.5.

### Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| **PASS** | Engine gives a correct, faithful answer | None needed |
| **PARTIAL** | Some correct info, but missing key details | Improve doc structure or add missing content |
| **FAIL** | Wrong answer, or right topic but no useful content extracted | Investigate crawlability or content gap |

### Common Root Causes

| Root Cause | Symptom | Fix |
|------------|---------|-----|
| **Crawlability** | Engine cites your help page but answer lacks detail | Check if page content is behind JS/iframes |
| **Fragmentation** | Answer uses page titles/summaries, not actual content | Consolidate procedure into a single page |
| **Content gap** | Engine doesn't cite your docs at all | Topic may not exist or isn't indexed |
| **Overshadowed** | Third-party or marketing pages outrank product docs | Improve page SEO, add llms.txt |

## Step 6: Iterate

The testing loop:

1. Run test → identify gaps
2. Fix docs (restructure, add content, improve crawlability)
3. Regenerate llm-docs corpus
4. Wait for crawler cycle (1-4 weeks for most engines)
5. Rerun test → measure improvement

## Cost Estimates

Each full run costs approximately:

| Component | Per Question Per Engine | 50 Questions x 4 Engines |
|-----------|----------------------|--------------------------|
| Engine query | $0.01 - $0.05 | $2 - $10 |
| DeepEval scoring (3 metrics) | $0.03 - $0.10 | $6 - $20 |
| **Total** | $0.04 - $0.15 | **$8 - $30** |

Use `--skip-eval` to query engines without scoring (useful for manual review). Use `--engine` to limit to one engine during development.

## CLI Reference

```
python -m src.run_test [OPTIONS]

Options:
  --product TEXT       Filter to one product (e.g. Fluent, Mechanical)
  --question-id TEXT   Run a single question by its ID
  --engine TEXT        Limit to specific engine(s). Repeatable.
                       Values: chatgpt, claude, perplexity, gemini
  --dry-run            Show test plan without making API calls
  --skip-eval          Query engines but skip DeepEval scoring
  --questions-dir PATH Path to questions directory
```

## File Layout After Adoption

```
bot-doc-testing/
├── questions/
│   ├── modelcenter.yaml    # (included as example)
│   ├── optislang.yaml      # (included as example)
│   └── yourproduct.yaml    # ← you add this
├── src/                    # Test framework (don't modify)
├── results/                # Generated per run (gitignored)
├── reports/                # Generated per run (gitignored)
├── samples/                # Example output for reference
├── .env                    # Your API keys (gitignored)
├── pyproject.toml
└── ONBOARDING.md           # This file
```

## Troubleshooting

**"No API keys configured"** — Check your `.env` file exists and has at least one key set.

**"No ground truth content available" errors** — Your `LLM_DOCS_PATH` doesn't point to the right directory, or the topic file paths in your YAML are wrong. Check that the files exist at `$LLM_DOCS_PATH/<product>/<filename>.md`.

**All questions score as errors** — Most likely a DeepEval configuration issue. DeepEval uses OpenAI for its judge model by default, so you need `OPENAI_API_KEY` set even if you're only testing Perplexity or Gemini.

**Scores seem too low** — Check your ground truth topics. If the mapped files don't actually answer the question, correctness will be low even when the AI engine gives a good answer.

## Contact

Questions about this toolkit: Leslie Poff (Team Charlie, Documentation)
ADO work item: [#1457082](https://tfs.ansys.com:8443/tfs/ANSYS_Development/Portfolio/_workitems/edit/1457082)
