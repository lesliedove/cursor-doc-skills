# Manual Test Run: AI Bot Doc Accuracy

*Date: 2026-05-13*
*Method: Web search (simulating what AI engines find when users ask these questions)*
*Engine tested: General web search (represents what ChatGPT/Perplexity/Claude crawl)*

---

## Test 1: "How do I install ModelCenter Desktop?"

### What the bot returns

- **Cites ansyshelp.ansys.com?** YES -- links to Installation Guide and Prerequisites pages
- **Mentions Ansys?** YES
- **Mentions ModelCenter?** YES
- **Key facts returned:**
  - Prerequisites: Java 64-bit (8/11/17 LTS), optional Python 3.x 64-bit
  - Must install as Administrator
  - Install for all users
- **Missing from response:**
  - No actual step-by-step install procedure (says "refer to the guide")
  - No mention of licensing setup (server port + hostname) after install
  - No mention of mandatory reboot
  - No mention of Unified Installer vs standalone installer choice
  - No mention of MBSE connector install options
- **Incorrect info:** None detected

### Our ground truth (from llm-docs)

Key facts the answer SHOULD include:
1. Two installer paths: Ansys Unified Installer (recommended) or standalone ModelCenterSetup.exe
2. Must run as Administrator
3. Product selection: ModelCenter Desktop, optionally MCRE and MBSE connectors
4. Licensing setup opens after install -- enter server port + hostname
5. Reboot required after install
6. Prerequisites: Java 64-bit, optional Python 3.x
7. Download from Ansys Customer Portal

### Verdict: PARTIAL -- Bot finds the right source but gives an incomplete answer

**Gap type:** The public help site content is findable but the bot can't extract a clear step-by-step procedure. The install topics may be too fragmented across pages for crawlers to assemble a complete answer.

---

## Test 2: "How do I pass arguments to optiSLang in batch mode?"

### What the bot returns

- **Cites ansyshelp.ansys.com?** YES (links to API scripting docs and PDF user guide)
- **Also cites:** discuss.ansys.com forum thread, PyOptiSLang docs
- **Mentions Ansys?** YES
- **Mentions optiSLang?** YES
- **Key facts returned:**
  - Use `--script-args` option
  - Full command example: `optislang.exe -b --python script.py --script-args 111 222.2 "333" --new project.opf`
  - `-b` triggers batch mode
  - Access args via `sys.argv` in Python
  - All args are strings, need type conversion
- **Missing:** Nothing significant -- this is a complete, accurate answer
- **Incorrect info:** None detected

### Our ground truth (from llm-docs)

Key facts: `-b` for batch, `--python` for script, `--script-args` for arguments, `sys.argv` access, string type. Also `--script-arg` (singular) for one argument.

### Verdict: PASS -- Bot gives accurate, complete answer

**Note:** The forum thread (discuss.ansys.com) is actually the primary source the bot uses, not the official help docs. The help docs confirm it but the forum answer is more actionable.

---

## Test 3: "How do I create a workflow in ModelCenter?"

### What the bot returns

- **Cites ansyshelp.ansys.com?** YES (User Guide index page)
- **Also cites:** PyAnsys ModelCenter Workflow docs, ansys.com product page
- **Key facts returned:**
  - Two approaches: GUI and Python (PyAnsys)
  - Python example with `grpc_modelcenter` engine
  - Two workflow types: DATA (legacy, dependency-driven) and PROCESS (explicit flow)
- **Missing from response:**
  - No GUI steps at all (says "specific step-by-step GUI instructions are not detailed")
  - No mention of File > New > choose type dialog
  - No mention of Server Browser for adding components
  - No mention of Analysis View for building
  - No mention of Link Editor
  - Heavily biased toward Python/API approach over the GUI which most users need
- **Incorrect info:** 
  - Describes DATA as "legacy" -- our docs don't characterize it that way; both types are current

### Our ground truth (from llm-docs)

Key facts:
1. File > New (Ctrl+N) > choose Process or Data type > save
2. Process = order-driven (Start to Stop flowchart); Data = dependency-driven (scheduler)
3. Build by dragging from Server Browser into Analysis View
4. Link variables between components
5. Process workflows use If/Loop/Sequence/Parallel components
6. Data workflows use schedulers (forward, backward, mixed)

### Verdict: FAIL -- Bot can't find the GUI workflow creation steps

**Gap type:** The ansyshelp.ansys.com User Guide page is an index/TOC that bots can see, but the actual content pages behind it aren't being crawled or assembled into a coherent answer. The bot falls back to PyAnsys API docs (which are on a separate, well-structured docs site) because those are easier to crawl.

---

## Test 4: "How do I set up sensitivity analysis in optiSLang?"

### What the bot returns

- **Cites ansyshelp.ansys.com?** YES (tutorials page, conditional execution page, PDF user guide)
- **Also cites:** Ansys Innovation Space courses
- **Key facts returned:**
  - Create project, define inputs, select outputs
  - Use Sensitivity Wizard
  - AMOP approach with automatic DOE refinement
  - Three steps: DOE generation, Metamodels, MOP with CoP
  - Post-processing with predefined visualizations
- **Missing:**
  - No specifics on which sampling methods are available
  - No mention of dragging wizard onto process chain in Scenery pane
  - Vague on actual UI steps
- **Incorrect info:** None detected

### Our ground truth (from llm-docs)

Key facts:
1. Use Sensitivity wizard from Wizards pane -- drag onto process chain in Scenery pane
2. Wizard pages: Parametrize Inputs, Criteria, Sampling method, Additional options
3. Only parameters with deterministic properties (Optimization or Opt.+Stoch.) apply
4. Create MOP option on Additional options page
5. MOP picks optimal input subspace + optimal meta-model using CoP
6. DOE > Metamodels > MOP pipeline

### Verdict: PARTIAL -- Conceptually correct but missing actionable UI steps

**Gap type:** The bot finds tutorial and course content but not the actual User Guide procedure for the Sensitivity wizard. The detailed wizard page-by-page walkthrough isn't surfacing.

---

## Test 5: "How do I automate optiSLang using PyOptiSLang?"

### What the bot returns

- **Cites ansyshelp.ansys.com?** NO -- zero links to ansyshelp
- **Cites:** optislang.docs.pyansys.com exclusively (5 links)
- **Key facts returned:**
  - Import `from ansys.optislang.core import Optislang`
  - Create instance, access application/project
  - `run_python_script()` and `run_python_file()` methods
  - Each script call creates new Python context
  - Direct server communication via `TcpOslServer`
  - Save/open/new project methods
- **Missing:**
  - No mention of optiSLang Core Headless install option for PyOptiSLang
  - No mention of the embedded Python API (shipped modules, actors)
- **Incorrect info:** None detected

### Our ground truth (from llm-docs)

Key facts:
1. optiSLang ships embedded Python modules (actors, kernel, data types)
2. PyOptiSLang is the PyAnsys package (separate from embedded API)
3. optiSLang Core Headless is the recommended install for PyOptiSLang use
4. Python API reference on developer.ansys.com
5. Example scripts available in examples zip
6. Python console, Python node, and batch mode are execution paths

### Verdict: PARTIAL -- Accurate for PyAnsys but ignores our product docs entirely

**Gap type:** The PyAnsys docs site (optislang.docs.pyansys.com) completely dominates. Our ansyshelp.ansys.com content about the embedded Python API and Core Headless install option doesn't surface at all. Bots don't know about the product-shipped Python modules.

---

## Summary

| # | Question | Cites AnsysHelp | Accuracy | Verdict |
|---|----------|-----------------|----------|---------|
| 1 | Install ModelCenter Desktop | YES | Partial | PARTIAL -- finds source, incomplete answer |
| 2 | optiSLang batch mode args | YES | Complete | PASS |
| 3 | Create workflow in ModelCenter | YES (index only) | Poor | FAIL -- no GUI steps found |
| 4 | Sensitivity analysis in oSL | YES | Partial | PARTIAL -- concepts yes, steps no |
| 5 | Automate oSL with PyOptiSLang | NO | Partial | PARTIAL -- PyAnsys only, ignores product docs |

**Pass rate: 1/5 (20%)**

## Key Findings

### What's working
- optiSLang batch mode question gets a great answer, largely thanks to the forum thread on discuss.ansys.com being well-structured and crawlable.

### What's broken

1. **Fragmented content structure on ansyshelp.ansys.com** -- The help site serves content through iframes and JavaScript-heavy navigation that bots struggle to crawl. Index/TOC pages are visible but actual content pages are often missed.

2. **Procedure steps don't surface** -- Bots find conceptual/overview pages but rarely extract step-by-step procedures. Our install, workflow creation, and wizard setup docs exist but aren't getting through.

3. **PyAnsys docs outcompete product docs** -- For Python/API questions, the pyansys.com docs sites (static, well-structured, Sphinx-generated) completely dominate over ansyshelp.ansys.com content. Bots don't surface the product-shipped Python API at all.

4. **Forum content fills gaps** -- The Ansys community forum (discuss.ansys.com) provides better answers than the help site for specific how-to questions because forum posts are plain HTML that bots can easily parse.

## Recommended Actions

1. **Crawlability audit of ansyshelp.ansys.com** -- Check robots.txt, test if content pages (not just index) are accessible to AI crawlers, verify iframe-embedded content is reachable.
2. **Propose llms.txt** at ansyshelp.ansys.com root to give AI engines a structured map of content.
3. **Prioritize making procedure/task topics self-contained** in the source docs so bots can extract complete answers from a single page.
4. **Cross-link product docs and PyAnsys docs** so bots that find one also discover the other.
