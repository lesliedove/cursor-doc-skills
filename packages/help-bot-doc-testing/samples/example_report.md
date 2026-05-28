# AI Bot Doc Accuracy Report

*Generated: 2026-05-14T18:30:00+00:00*

## Summary

| Metric | Value |
|--------|-------|
| Questions tested | 5 |
| Engines tested | chatgpt, claude, perplexity |
| Total evaluations | 15 |
| Passing | 6 (40%) |
| Failing | 7 (46%) |
| Errors | 2 |

## Per-Engine Results

| Engine | Pass | Fail | Error | Avg Correctness | Cites AnsysHelp |
|--------|------|------|-------|-----------------|-----------------|
| chatgpt | 2 | 2 | 1 | 0.58 | 60% |
| claude | 3 | 2 | 0 | 0.65 | 80% |
| perplexity | 1 | 3 | 1 | 0.45 | 40% |

## Documentation Gaps (Failing Questions)

These questions got incorrect or incomplete answers from AI engines.

### mc-workflow_integration-005: How do I create a workflow in ModelCenter?

- **Product:** ModelCenter
- **Category:** workflow_integration
- **Priority:** high
- **Ground truth topics:** modelcenter/mc-how-to-add-a-model-to-the-modelcenter-workflow.md, modelcenter/mc-how-to-create-an-executable-workflow-from-a-block-1.md
- **Expected key facts:** File > New, Analysis View, Server Browser, DATA vs PROCESS type

| Engine | Correctness | Faithfulness | Cites Help |
|--------|-------------|--------------|------------|
| chatgpt | 0.35 | 0.42 | Yes |
| perplexity | 0.28 | 0.38 | No |

### mc-workflow_integration-006: How do I wrap an Excel spreadsheet as a ModelCenter component?

- **Product:** ModelCenter
- **Category:** workflow_integration
- **Priority:** high
- **Ground truth topics:** modelcenter/mc-how-to-wrap-an-excel-workbook-legacy.md
- **Expected key facts:** Server Browser, Excel Component, cell mapping, input/output ranges

| Engine | Correctness | Faithfulness | Cites Help |
|--------|-------------|--------------|------------|
| chatgpt | 0.22 | 0.30 | No |
| claude | 0.31 | 0.45 | No |
| perplexity | 0.18 | 0.25 | No |

## Source Attribution

How often do engines cite ansyshelp.ansys.com as a source?

- **chatgpt:** 3/5 (60%)
- **claude:** 4/5 (80%)
- **perplexity:** 2/5 (40%)

## Recommended Actions

1. Review failing questions above and update source documentation
2. Regenerate llm-docs corpus after fixes
3. Wait for crawler cycle (1-4 weeks depending on engine)
4. Rerun this test to verify improvement
