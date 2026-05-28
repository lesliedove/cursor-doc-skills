# Manual Test Run: AI Bot Doc Accuracy — Full 50-Question Pilot

*Date: 2026-05-14*
*Method: Web search (simulating what AI engines find when users ask these questions)*
*Builds on: manual_run_2026-05-13.md (5 questions tested)*
*Total questions: 50 (25 ModelCenter + 25 optiSLang)*

---

# MODELCENTER (25 questions)

---

## MC-001: "How do I install ModelCenter Desktop?"

*(Tested 2026-05-13 — carried forward)*

- **Cites ansyshelp?** YES
- **Key facts returned:** Prerequisites (Java 64-bit, optional Python), must install as Administrator, install for all users
- **Missing:** No step-by-step procedure, no licensing setup, no reboot mention, no Unified Installer vs standalone choice, no MBSE connector install options
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Help site content findable but bot can't extract complete step-by-step procedure. Install topics too fragmented across pages.

---

## MC-002: "What are the system requirements for ModelCenter?"

- **Cites ansyshelp?** YES — links to corp install prereqs page AND ModelCenter-specific prereqs
- **Key facts returned:**
  - Java 64-bit (8/11/17 LTS), optional Python 3.x 64-bit with thrift+six
  - Intel 64 / AMD64, 8 GB RAM min, 128 GB disk
  - Discrete GPU recommended (NVIDIA Quadro / AMD FirePro, 1 GB VRAM, OpenGL 4.5+)
  - 1024x768 min display (1920x1080 recommended)
  - TCP/IP for license manager, three-button mouse
  - Must install as Administrator
- **Missing:** No ModelCenter-specific version compatibility matrix (which Windows versions supported), no mention of .NET requirements
- **Incorrect:** None — but the hardware requirements pulled from corp/v252 are the *generic Ansys platform* requirements, not ModelCenter-specific. ModelCenter is Java-based and doesn't need a GPU/OpenGL. Bot conflated the two.

### Verdict: PARTIAL

**Gap:** Bot merges generic Ansys platform system requirements with ModelCenter-specific software prerequisites. The corp prereqs page covers all Ansys products; ModelCenter's own prereqs page has the right Java/Python info but doesn't specify hardware. A user following the GPU recommendation would be misled — ModelCenter doesn't use GPU acceleration.

---

## MC-003: "How do I install ModelCenter Remote Execution (MCRE)?"

- **Cites ansyshelp?** YES — links directly to MCRE installation page
- **Key facts returned:**
  - Windows: double-click installer, accept license, click Install
  - Custom install location via Options button
  - Silent install command: `ModelCenterRemoteExecution_vYY.X /passive /norestart SLAACCEPT=yes /log "..."`
  - Linux: `chmod +x`, then `sh` to run installer, accept license
  - Prerequisites: Java 64-bit, Python 3.x (thrift + six)
  - Post-install: licensing settings utility opens
- **Missing:** No mention of Windows service registration option, no mention of configuring the Web Administrator after install, no mention of firewall/port configuration (8080 default)
- **Incorrect:** None

### Verdict: PASS

**Note:** This is a solid answer. The bot finds the actual installation page and extracts clear steps for both platforms plus the silent install command. One of the better results.

---

## MC-004: "How do I configure ModelCenter to use a license server?"

- **Cites ansyshelp?** YES — links to ModelCenter licensing page
- **Key facts returned:**
  - GUI method: Ansys Client Licensing Settings utility > FlexNet Publisher > Enable > enter port (default 1055) + hostname > Test > Save
  - Linux method: create `ansyslmd.ini` with `SERVER=1055@hostname`
  - ANSYSLMD_LICENSE_FILE env var override option
  - MCRE must be installed first
- **Missing:** Nothing significant
- **Incorrect:** None

### Verdict: PASS

**Note:** Excellent answer with clear GUI and CLI steps. ansyshelp content for licensing is well-structured and crawlable.

---

## MC-005: "How do I create a workflow in ModelCenter?"

*(Tested 2026-05-13 — carried forward)*

- **Cites ansyshelp?** YES (index page only)
- **Key facts returned:** Two approaches (GUI and Python), Python example with grpc_modelcenter, two workflow types (DATA and PROCESS)
- **Missing:** No GUI steps at all, no File > New dialog, no Server Browser, no Analysis View, no Link Editor
- **Incorrect:** Describes DATA as "legacy"

### Verdict: FAIL

**Gap:** Bot finds index/TOC page but not actual content pages. Falls back to PyAnsys API docs.

---

## MC-006: "How do I wrap an Excel spreadsheet as a ModelCenter component?"

- **Cites ansyshelp?** NO — links to developer.ansys.com and Ansys Knowledge forum
- **Key facts returned:**
  - Use Component Plug-In SDK from Developer Portal
  - Unified Component Plug-In Framework (v14.5+)
  - Import Files Manually option for Excel
  - Components reusable across Desktop, MCRE, Cloud
- **Missing:** No mention of the built-in Excel Component available in Server Browser, no step-by-step for the Excel Wrapper wizard, no mention of selecting cells/ranges for inputs/outputs, no mention of the legacy QuickWrap Excel approach
- **Incorrect:** None, but the answer steers users to the SDK (developer approach) rather than the built-in drag-and-drop Excel component that most users need

### Verdict: FAIL

**Gap:** The built-in Excel wrapping workflow (Server Browser > Excel Component > select workbook > map cells to variables) doesn't surface at all. Bot finds SDK docs instead of the User Guide content describing the GUI workflow.

---

## MC-007: "How do I connect ModelCenter to MATLAB?"

- **Cites ansyshelp?** YES (User Guide index only)
- **Also cites:** Ansys Innovation Space, ansys.com product page, MathWorks product page
- **Key facts returned:**
  - ModelCenter integrates with MATLAB as part of workflow automation
  - Avoids point-to-point MEX-file programming
  - Links MATLAB with other applications
- **Missing:** No mention of the MATLAB Component in Server Browser, no steps for configuring MATLAB path, no mention of specifying MATLAB script/function, no mention of mapping MATLAB variables to ModelCenter variables, no mention of COM vs batch execution modes
- **Incorrect:** None

### Verdict: FAIL

**Gap:** Only marketing/overview content surfaces. No actionable setup or configuration steps. The bot explicitly says "specific step-by-step instructions for the actual connection process" are not available.

---

## MC-008: "How do I integrate ModelCenter with Ansys Workbench?"

- **Cites ansyshelp?** YES (but only the optiSLang user guide page about ModelCenter node, not ModelCenter's own docs)
- **Key facts returned:**
  - Integration possible through optiSLang's Ansys ModelCenter node
  - Supports .pxcz and .pxc project files
  - Need MCRE running with project directory configured
- **Missing:** No mention of the Workbench Component available in ModelCenter, no steps for dragging Workbench component into workflow, no mention of parameter mapping between Workbench design points and ModelCenter variables
- **Incorrect:** The answer conflates ModelCenter-in-optiSLang with direct ModelCenter-Workbench integration. These are different workflows.

### Verdict: FAIL

**Gap:** Bot finds the optiSLang docs about using ModelCenter projects, not the ModelCenter docs about integrating Workbench simulations. The actual Workbench Component documentation in the MC User Guide doesn't surface.

---

## MC-009: "How do I use ModelCenter with Python scripting?"

- **Cites ansyshelp?** NO — zero ansyshelp links
- **Cites:** modelcenter.docs.pyansys.com exclusively (5 links)
- **Key facts returned:**
  - Install `ansys-modelcenter-workflow` via pip
  - Python 3.9-3.12, Linux/macOS/Windows
  - Engine and Workflow classes from grpc_modelcenter
  - Code example: create workflow, add component, run, save
- **Missing:** No mention of ModelCenter's built-in Script Component for embedded Python, no mention of the COM/Java API for Python scripting, no mention of IronPython support in older versions
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Same pattern as osl-005 yesterday — PyAnsys docs completely dominate. Product docs about built-in Python scripting (Script Component, COM API) don't surface.

---

## MC-010: "How do I run a ModelCenter workflow from the command line?"

- **Cites ansyshelp?** NO — only PyAnsys docs
- **Key facts returned:**
  - Use PyAnsys library: Engine + load_workflow + run
  - Python script approach with grpc_modelcenter
  - MCDProcess class for launching ModelCenter Desktop
- **Missing:** No mention of `ModelCenter.exe /run` command-line option, no mention of runModel.vbs or runModel.bat scripts shipped with the product, no mention of the COM API for scripted execution, no mention of the Job Manager for headless execution
- **Incorrect:** None, but the answer assumes Python/PyAnsys is the only way to run from CLI

### Verdict: PARTIAL

**Gap:** The product ships with direct CLI execution options (command-line flags, batch scripts) that don't surface. Bot only finds the PyAnsys approach.

---

## MC-011: "How do I use the ModelCenter API to create components programmatically?"

- **Cites ansyshelp?** NO — links to developer.ansys.com exclusively
- **Key facts returned:**
  - `createComponent` method with URI, name, parent params
  - VBScript example creating components
  - Supports C#/.NET, C++ (COM), Java, Python
  - Can create links and save model after
- **Missing:** No mention of the PyAnsys `workflow.create_component()` method (from mc-009 results), no mention of the Server Browser path format vs MCRE URI format
- **Incorrect:** None

### Verdict: PASS

**Note:** Developer Portal content is well-structured and the bot extracts a working code example. Good result for an API question.

---

## MC-012: "How do I set up ModelCenter MBSE with Ansys SAM?"

- **Cites ansyshelp?** YES — links directly to "How to Add ModelCenter MBSE to an Ansys SAM Model" page
- **Key facts returned:**
  - Log in to system in browser
  - Open project > File menu > "Open in ModelCenter"
  - Click Open when browser prompts
  - ModelCenter MBSE opens
- **Missing:** No mention of prerequisites (MBSE connector must be installed), no mention of configuring the SysML profile, no mention of mapping execution plans to SAM models
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Bot finds the right page but only extracts the basic "open in ModelCenter" steps. The deeper configuration workflow doesn't surface.

---

## MC-013: "What is ModelCenter MBSE and how does it connect to systems models?"

- **Cites ansyshelp?** NO — only ansys.com marketing pages and developer.ansys.com
- **Key facts returned:**
  - MDAO software for multi-disciplinary analysis
  - Multi-tool integration and workflow automation
  - Requirements-to-engineering connection
  - Digital thread concept
  - APIs in Python, Java, C++, C#/.NET
- **Missing:** No mention of specific MBSE connectors (Cameo, SAM, Teamwork Cloud), no mention of SysML profiles, no mention of execution plans, no mention of design instances, no mention of parametric studies from systems models
- **Incorrect:** None, but answer is entirely marketing-level

### Verdict: PARTIAL

**Gap:** Only product marketing pages surface. The actual MBSE Help documentation explaining connectors, execution plans, and the systems model connection workflow doesn't appear.

---

## MC-014: "How do I use ModelCenter with Cameo Systems Modeler?"

- **Cites ansyshelp?** YES — links to MagicDraw/Cameo Connector release notes
- **Key facts returned:**
  - Need MagicDraw/Cameo Connector installed
  - Cameo Systems Modeler 2024x supported in 2024 R2
  - Java prerequisite
  - Need MagicDraw installation directory during install
  - Version compatibility issues with 2021x Refresh 1 & 2
  - Enables execution plans, design instances, trade studies
- **Missing:** No installation steps for the connector itself, no steps for launching MBSE from within Cameo, no mention of SysML profile configuration, no mention of stereotype mapping
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Release notes page surfaces (good for version compatibility) but not the actual setup/usage procedures. The connector installation and workflow docs don't appear.

---

## MC-015: "How do I perform a trade study in ModelCenter?"

- **Cites ansyshelp?** YES — links to Trade Study Tools page and DOE page
- **Key facts returned:**
  - Lists available tools: Parametric Study, Carpet Plot, DOE, Optimization, Probabilistic Analysis, Darwin Genetic, Data Explorer, RSM Toolkit
  - Basic process: define design variables (drag from Component Tree), specify responses, run, analyze with Data Explorer
  - DOE explores design space with multiple runs
- **Missing:** No mention of how to open the Trade Study pane (View menu), no mention of adding constraints or objectives, no detailed steps for any specific trade study tool
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Bot finds the index-level trade study tools page and extracts the general workflow, but no detailed procedure for any specific tool. Answer is conceptually correct but not actionable.

---

## MC-016: "How do I use the Data Explorer in ModelCenter?"

- **Cites ansyshelp?** YES — links to Data Explorer page, Plot Options, View Controls
- **Key facts returned:**
  - Displays data collected from trade studies
  - Supports Parametric Study, Carpet Plot, DOE, Optimization, Probabilistic tools
  - Progress meter and halt button during collection
  - Plot Options tabs: Dimensions, Constraints, Objectives, Values, Series, Layout, Axes, Legend
  - View Controls: download PNG, zoom, pan, 3D rotation, Pareto front, infeasible designs filter
- **Missing:** No mention of how to add/configure specific plot types (scatter, histogram, parallel coordinates), no mention of data filtering or sorting
- **Incorrect:** None

### Verdict: PASS

**Note:** Good detailed answer about Data Explorer features. The docs pages for plot options and view controls are well-structured and crawlable.

---

## MC-017: "How do I use Design of Experiments (DOE) in ModelCenter?"

- **Cites ansyshelp?** YES — links to DOE Getting Started page
- **Key facts returned:**
  - Drag input variables from Component Tree to Design Variables list
  - Set lower/upper bounds
  - Drag output variables to Responses
  - View Design Table (defaults to Full Factorial)
  - Run DOE — modifies design variables, holds others constant
  - Data Explorer shows results with Variable Importance Summary Plot
- **Missing:** No mention of changing DOE type (Latin Hypercube, Central Composite, etc.), no mention of configuring number of levels
- **Incorrect:** None

### Verdict: PASS

**Note:** This is the Getting Started tutorial content and it surfaces well. Clear, step-by-step, actionable.

---

## MC-018: "How do I configure remote execution in ModelCenter?"

- **Cites ansyshelp?** YES — links to MCRE Configuration page
- **Key facts returned:**
  - Web-based admin tool on port 8080 (localhost or hostname)
  - Launch via Configure button on MCRE interface
  - mcre.conf file for direct config (restart required after changes)
  - Configurable: server port, security, logging, analyses locations
  - SSL and SSH connection options available
- **Missing:** No mention of adding analyses directories through the web admin, no mention of user authentication configuration
- **Incorrect:** None

### Verdict: PASS

**Note:** Solid answer. MCRE docs are well-structured HTML that bots parse easily.

---

## MC-019: "How do I set up distributed computing with ModelCenter?"

- **Cites ansyshelp?** YES — links to MCRE introduction page
- **Also cites:** Ansys Knowledge DCS/DPS guide, corp distributed analysis page
- **Key facts returned:**
  - Use MCRE to publish analysis components on network
  - Start MCRE, click Configure, set Analyses Path
  - Components accessible from any computer on network
  - Gigabit/Infiniband networking recommended
- **Missing:** No mention of load balancing across multiple MCRE instances, no mention of the Scheduler component for parallel execution, no mention of configuring multiple MCRE servers in ModelCenter Desktop, no mention of the Parallel component for concurrent execution
- **Incorrect:** The DCS/DPS reference is for Ansys Workbench distributed solve, not ModelCenter distributed execution — these are different systems. Bot conflated them.

### Verdict: PARTIAL

**Gap:** Bot merges ModelCenter distributed execution (via MCRE) with Ansys Workbench DCS/DPS (different system). The actual ModelCenter docs about Parallel components and multi-server MCRE configuration don't surface.

---

## MC-020: "How do I debug a failing component in a ModelCenter workflow?"

- **Cites ansyshelp?** NO — only PyAnsys docs
- **Key facts returned:**
  - `is_connected` property to check component connection
  - `invalidate()`, `reconnect()`, `download_values()`, `get_source()`, `invoke_method()` methods
  - ComponentReconnectionFailedError and ComponentDownloadValuesFailedError exceptions
- **Missing:** No mention of the component's Run Log pane in the GUI, no mention of the Analysis View error indicators, no mention of checking component properties/status in Properties pane, no mention of the Validation View, no mention of file-level debugging (checking input/output files in the run directory)
- **Incorrect:** None, but the answer is entirely API-level. Most users debug via the GUI.

### Verdict: FAIL

**Gap:** Bot only finds PyAnsys API docs. The ModelCenter Desktop GUI debugging workflow (Run Log, error indicators, Properties pane, Validation View) doesn't surface at all.

---

## MC-021: "ModelCenter workflow fails with connection error — how to fix?"

- **Cites ansyshelp?** YES (Secure Connections page)
- **Also cites:** PyAnsys error classes
- **Key facts returned:**
  - EngineDisconnectedError and ComponentReconnectionFailedError error types
  - Check SSL configuration (not enabled by default)
  - SSH as alternative to persistent MCRE
  - Verify service availability
- **Missing:** No mention of checking MCRE status/logs, no mention of firewall port 8080, no mention of verifying analysis path configuration, no mention of Java version compatibility issues, no mention of checking the MCRE web admin for error logs, no common troubleshooting checklist
- **Incorrect:** None

### Verdict: FAIL

**Gap:** No actual troubleshooting procedure. Bot finds error class names and security config pages but not a diagnostic workflow. There's no troubleshooting guide in our docs that a bot can crawl — this is a content gap.

---

## MC-022: "How do I migrate workflows from an older version of ModelCenter?"

- **Cites ansyshelp?** NO — only Ansys Knowledge forum post
- **Key facts returned:**
  - Legacy plug-ins and wrappers still supported in newer versions
  - "Existing workflows will still run exactly the same"
  - Optional upgrade to Unified Component Plug-In Framework (v14.5+)
  - Contact PHX-Support for migration help
- **Missing:** No mention of the automatic migration dialog when opening old .pxc files, no mention of converting .pxc to .pxcz format, no mention of version-specific breaking changes, no mention of component re-registration after upgrade
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Only a forum tech note surfaces. There's no migration guide in the crawlable docs. The "your workflows still work" message is reassuring but doesn't help users who need to actively migrate.

---

## MC-023: "How do I wrap a custom executable as a ModelCenter component?"

- **Cites ansyshelp?** YES (scriptWrapper generation page from optiSLang docs)
- **Also cites:** developer.ansys.com, Ansys Knowledge
- **Key facts returned:**
  - Unified Component Plug-In Framework approach
  - IComponentConfig interface for executable, command-line args, inputs/outputs
  - ScriptWrapper approach for MCRE
  - "Use Existing Directory" option for files
- **Missing:** No mention of the FileWrapper component (the primary method most users need), no step-by-step for FileWrapper wizard, no mention of QuickWrap, no mention of specifying input/output file templates and parsing rules
- **Incorrect:** None, but answer steers users to SDK/API approaches rather than the built-in FileWrapper component

### Verdict: FAIL

**Gap:** The FileWrapper component (the standard way to wrap executables in ModelCenter) doesn't surface. Bot finds SDK and API docs instead of the User Guide FileWrapper wizard content.

---

## MC-024: "How do I link variables between components in ModelCenter?"

- **Cites ansyshelp?** PARTIALLY — found URLs to the correct help pages but they returned auth-required redirects
- **Also cites:** developer.ansys.com API docs
- **Key facts returned:**
  - IVariableLink interface: LHS (target), RHS (source/expression)
  - suspendLink(), resumeLink(), breakLink() methods
  - Authentication wall blocked the actual help content
- **Missing:** No GUI steps (drag from output to input, or Edit > Link Variables dialog), no mention of automatic linking, no mention of the Link Editor view, no mention of link equations/expressions in the GUI
- **Incorrect:** None

### Verdict: FAIL

**Gap:** The correct ansyshelp pages exist but are behind authentication and the bot can't access them. Only API-level information from the Developer Portal surfaces. The fundamental GUI operation (dragging to link variables) is not described.

---

## MC-025: "How do I use ModelCenter plugins for third-party tools?"

- **Cites ansyshelp?** YES (SolidWorks plug-in page)
- **Also cites:** developer.ansys.com
- **Key facts returned:**
  - Component Plug-In SDK for custom integrations
  - MCRE APIs (Python, Java) for ScriptWrapper components
  - Custom Optimization Algorithm SDK
  - SolidWorks plug-in example: drag from Server Browser, Initialize PACZ dialog, select CAD files, extract design parameters
  - Supports Python, Java, C++, C#/.NET
- **Missing:** No mention of the built-in CATIA, Creo, NX plug-ins by name, no mention of the Excel or MATLAB components as "plug-ins," no overview of all available plug-ins
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Bot finds the SolidWorks plug-in page (good specific example) and SDK docs, but there's no single "available plug-ins" overview page that lists all supported third-party tools. Users can't discover what's available.

---

# OPTISLANG (25 questions)

---

## OSL-001: "How do I install optiSLang standalone?"

- **Cites ansyshelp?** YES — links to Installation and Licensing Guide
- **Key facts returned:**
  - Windows and Linux installation paths available
  - Linux: closely matches Ansys unified installer
  - Silent mode for automated installations
  - Workbench optiSLang Extension installed automatically, needs separate activation
- **Missing:** No Windows-specific install steps (GUI installer wizard pages), no mention of selecting components during install, no mention of setting install directory, no mention of the post-install licensing configuration
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Bot finds the Installation Guide index page but can't extract the actual Windows GUI installer steps. The Linux reference is to sub-pages that don't surface. Generic "refer to the guide" answer.

---

## OSL-002: "What are the system requirements for optiSLang?"

- **Cites ansyshelp?** YES — links to Installation Guide, but explicitly says the actual requirements aren't in the results
- **Key facts returned:**
  - References the System Requirements page exists in the guide
  - That's it — no actual requirements listed
- **Missing:** Everything — OS versions, RAM, disk space, Python version, Java requirements, supported compilers, GPU requirements (or lack thereof)
- **Incorrect:** None (nothing to be wrong about)

### Verdict: FAIL

**Gap:** The System Requirements page exists in the docs but the bot cannot access/extract its content. The page may be behind authentication or rendered in a way crawlers can't parse.

---

## OSL-003: "How do I run optiSLang in batch mode?"

- **Cites ansyshelp?** NO — links to User's Guide PDF (not HTML) and discuss.ansys.com
- **Also cites:** PyOptiSLang docs
- **Key facts returned:**
  - `-b` flag for batch mode
  - `--python` for script, `--script-args` for arguments
  - Full command example with exe path
  - `sys.argv` for accessing args
  - PyOptiSLang programmatic approach with Optislang class
- **Missing:** No mention of `--new` vs opening existing project, no mention of `--script-arg` (singular) option, no mention of logging/output options
- **Incorrect:** None

### Verdict: PASS

**Note:** Forum thread (discuss.ansys.com) provides a great answer, same as the batch args question yesterday. The community forum consistently outperforms the official help site for CLI/scripting questions.

---

## OSL-004: "How do I pass arguments to optiSLang in batch mode?"

*(Tested 2026-05-13 — carried forward)*

### Verdict: PASS

---

## OSL-005: "How do I automate optiSLang using PyOptiSLang?"

*(Tested 2026-05-13 — carried forward)*

### Verdict: PARTIAL — PyAnsys docs only, ignores product docs

---

## OSL-006: "PyOptiSLang RuntimeError: Cannot get optiSLang server port — how to fix?"

- **Cites ansyshelp?** NO — GitHub issue, PyOptiSLang troubleshooting, discuss.ansys.com
- **Key facts returned:**
  - It's a timeout issue, not a port access problem
  - Fix: increase `ini_timeout` parameter (default 20s)
  - Code example: `Optislang(ini_timeout=60)`
  - Debug logging: `Optislang(loglevel="DEBUG")`
- **Missing:** No mention of checking optiSLang installation path, no mention of license availability as a cause, no mention of firewall issues
- **Incorrect:** None

### Verdict: PASS

**Note:** Excellent result. The PyOptiSLang docs site, GitHub issues, and community forum combine to give a complete, actionable answer. This is the kind of troubleshooting content that works well for bots.

---

## OSL-007: "How do I set up a sensitivity analysis in optiSLang?"

*(Tested 2026-05-13 — carried forward)*

### Verdict: PARTIAL — concepts yes, steps no

---

## OSL-008: "How do I perform optimization of a damped oscillator in optiSLang?"

- **Cites ansyshelp?** YES — links to tutorial page
- **Also cites:** PyOptiSLang examples
- **Key facts returned:**
  - Define optimization variables (mass, stiffness)
  - Minimize maximum amplitude with eigen-frequency constraints
  - Sensitivity Wizard first, then Optimization Wizard
  - MOP, AMOP, or EA optimization approaches
  - Tutorial with downloadable files available
- **Missing:** No mention of the specific tutorial project files, no walkthrough of the wizard pages
- **Incorrect:** None

### Verdict: PASS

**Note:** Tutorial content surfaces well. The bot finds the right page and gives a conceptually complete workflow. Good enough for a user to follow along with the tutorial.

---

## OSL-009: "How do I use the Metamodel of Optimal Prognosis (MOP) in optiSLang?"

- **Cites ansyshelp?** YES — links directly to MOP User Guide page
- **Key facts returned:**
  - MOP node: open .omdb file, create approximation models
  - Basic settings: tested metamodels, variable reduction, cross validation
  - Advanced: testing type, approximation type (smoothing vs interpolating)
  - Metamodel types: Polynomial, MLS, Kriging (isotropic/anisotropic)
  - Export FMU option
  - Nominal discrete parameters not supported
- **Missing:** No step-by-step for adding MOP node to Scenery, no mention of connecting MOP to a preceding sensitivity/DOE node
- **Incorrect:** None

### Verdict: PASS

**Note:** Strong result. The MOP docs page is HTML with clear structure that bots parse well. Technical details are accurate and detailed.

---

## OSL-010: "What is the Coefficient of Prognosis (CoP) in optiSLang?"

- **Cites ansyshelp?** YES (MOP page)
- **Also cites:** Wikipedia OptiSLang article, LEAP Australia blog
- **Key facts returned:**
  - Formula: CoP = 1 − (SS_E^pred / SS_T)
  - Uses cross-validation: remove subset, build model, test against removed points
  - Model-independent quality measure
  - Applicable to regression and interpolation
  - Used in MOP for comparing metamodels across variable subspaces
  - Less sensitive to noise than existing tools
- **Missing:** Nothing significant — this is a comprehensive, accurate explanation
- **Incorrect:** None

### Verdict: PASS

**Note:** Excellent result. The Wikipedia article provides the formal definition, and the ansyshelp MOP page confirms the application context. Technical content that is well-defined in external sources gets great bot answers.

---

## OSL-011: "How do I use AMOP (Adaptive MOP) in optiSLang?"

- **Cites ansyshelp?** NO — Ansys Innovation Courses, forum post
- **Key facts returned:**
  - Three-step process: DOE > Metamodels/MOP > Adaptive refinement
  - Use Sensitivity Wizard to set up
  - Automatically runs new simulations to improve metamodel quality
  - Can serve as basis for multi-objective optimization
  - License requirement note (pre-21R2.1 compatibility)
- **Missing:** No mention of AMOP-specific settings (refinement criteria, convergence settings), no mention of how AMOP differs from MOP in the UI (which nodes to use), no step-by-step
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Bot finds course/forum content but not the actual User Guide procedure for configuring AMOP. The answer is conceptually correct but a user couldn't follow it to set up AMOP.

---

## OSL-012: "How do I set up a Design of Experiments (DOE) in optiSLang?"

- **Cites ansyshelp?** PARTIALLY — links to Methods PDF (not HTML)
- **Key facts returned:**
  - Lists DOE schemes: Full factorial, Star points, CCD, Box-Behnken, Koshal, D-optimal, Orthogonal Arrays, Monte Carlo
  - General concept of parametric design studies
  - References workshops and User Guide
- **Missing:** No steps for adding a DOE node to the Scenery pane, no mention of the Sensitivity Wizard DOE configuration, no mention of selecting sampling method and sample count, no mention of Latin Hypercube Sampling (the most commonly used method)
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Bot finds the Methods reference (which lists DOE types) but not the practical "how to set up a DOE" procedure from the User Guide. Tells users what DOE types exist but not how to configure one.

---

## OSL-013: "How do I integrate optiSLang with Ansys Workbench?"

- **Cites ansyshelp?** YES — links directly to Ansys Workbench page in oSL User Guide
- **Key facts returned:**
  - Open .wbpj/.wbpz/.wbjn/.py/.json files in optiSLang dialog
  - Parameters and responses auto-displayed for registration
  - Drag to register or use multi-action buttons
  - Project caching in .optislang folder
  - Batch mode (no GUI) default, Workbench exe auto-detection
  - Configure designs per process, max runtime, Python scripting
- **Missing:** No mention of the optiSLang in Workbench extension vs standalone approaches, no mention of prerequisite: matching Ansys version
- **Incorrect:** None

### Verdict: PASS

**Note:** Strong result. The Workbench integration page in the oSL User Guide is well-structured HTML with clear configuration options.

---

## OSL-014: "How do I connect optiSLang to Ansys Mechanical?"

- **Cites ansyshelp?** NO — only ansys.com webinars and blog posts
- **Key facts returned:**
  - Connection happens within Workbench environment
  - Setup includes FE model, Data Send component, Signal Processing component
  - AI/ML metamodel capabilities
- **Missing:** No actual steps for connecting, no mention of which Workbench nodes to use, no mention of parameterizing the Mechanical model, no mention of the APDL/Mechanical integration node in optiSLang
- **Incorrect:** None, but extremely vague

### Verdict: FAIL

**Gap:** Only webinar/marketing content surfaces. No docs content about the actual Mechanical connection workflow. Bot says "refer to official documentation" — which is exactly the problem.

---

## OSL-015: "How do I use optiSLang with Ansys Fluent?"

- **Cites ansyshelp?** NO — Ansys webinar and Innovation Courses
- **Key facts returned:**
  - Use Solver Wizard to create project
  - Add Ansys Discovery, Fluent-Mesher, Fluent Solver nodes
  - Define input/output parameters
  - Establish connections between nodes
- **Missing:** No mention of Fluent journal file setup, no mention of parameterizing Fluent inputs, no mention of which optiSLang node type to use for Fluent, no mention of Workbench-through integration vs standalone
- **Incorrect:** Mentions "Add an Ansys Discovery node" which is specific to that course's example, not a general requirement for Fluent integration

### Verdict: PARTIAL

**Gap:** Course/webinar content gives a general workflow but not the docs-based procedure. The answer mixes a specific course example with general guidance.

---

## OSL-016: "How do I use optiSLang with MATLAB?"

- **Cites ansyshelp?** YES — links to MATLAB/Octave page in oSL User Guide
- **Also cites:** MathWorks product page
- **Key facts returned:**
  - Native binary interface (no file-based I/O for most interactions)
  - Connect to existing MATLAB instance or create new one
  - MATLAB node: store scripts, configure files/variables
  - Script requirement: existence checks for all parameters
  - Code example for existence checks
  - Connect Mode vs Batch Mode execution
  - MATLAB version selection
  - OSL_ prefix reserved
- **Missing:** No mention of configuring MATLAB path in optiSLang settings, no mention of Octave as a free alternative
- **Incorrect:** None

### Verdict: PASS

**Note:** Excellent result. The oSL User Guide MATLAB page is well-structured and the bot extracts practical code and configuration details. One of the best results in the entire test.

---

## OSL-017: "How do I use optiSLang with Excel?"

- **Cites ansyshelp?** YES — links to Excel Add-in Guide and Introduction page
- **Key facts returned:**
  - Excel Add-in is wizard-based
  - Two functions: Export Data from sheets, Calculate Designs using MOP solver
  - Installation instructions in Add-in Guide
  - References to tutorials
- **Missing:** No mention of the Excel node in optiSLang (different from the add-in), no steps for the add-in installation wizard, no mention of cell/range mapping for parameters
- **Incorrect:** None, but the answer focuses on the Excel Add-in (Excel calling optiSLang) rather than the Excel node (optiSLang calling Excel), which is what most users asking this question likely need

### Verdict: PARTIAL

**Gap:** Bot finds the Excel Add-in docs but not the Excel integration node documentation. These are different products serving different workflows. A user wanting to include an Excel model in their optiSLang workflow wouldn't find their answer here.

---

## OSL-018: "How do I perform robust design optimization in optiSLang?"

- **Cites ansyshelp?** YES — links to Methods for Multi-Disciplinary Optimization
- **Also cites:** PyOptiSLang RDO example, tutorials
- **Key facts returned:**
  - Define uncertainties, set up solver chain, configure parameters
  - AMOP for robust design workflows
  - Multi-objective optimization including Pareto
  - Sensitivity analysis methods available
- **Missing:** No mention of the RDO wizard, no mention of configuring stochastic parameters vs deterministic, no mention of robustness criteria (sigma levels), no mention of the RDO-specific nodes in Scenery
- **Incorrect:** None, but very generic

### Verdict: PARTIAL

**Gap:** Bot finds the high-level methods reference but not the practical RDO setup procedure. The answer lists concepts without actionable steps.

---

## OSL-019: "How do I perform reliability analysis in optiSLang?"

- **Cites ansyshelp?** YES — links to FORM page in User Guide
- **Also cites:** developer.ansys.com Python API
- **Key facts returned:**
  - FORM (First Order Reliability Method) is primary tool
  - Computes design point, beta index, probability of failure
  - First-order Taylor expansion in standard-normal space
  - Add FORM node to Scenery, configure via FORM tab
  - NLPQL algorithm, accuracy/tolerance settings
  - Multiple search runs, Monte Carlo presampling
  - Limitations: requires smooth, convex, differentiable functions
- **Missing:** No mention of Monte Carlo reliability analysis as alternative, no mention of SORM (Second Order), no mention of importance sampling
- **Incorrect:** None

### Verdict: PASS

**Note:** Good technical answer from the User Guide FORM page. Includes both setup steps and important limitations.

---

## OSL-020: "How do I use Python code objects with optiSLang in Mechanical?"

- **Cites ansyshelp?** YES (Mechanical Python Code chapter)
- **Also cites:** PyOptiSLang docs
- **Key facts returned:**
  - Python Code objects execute code in response to Mechanical workflow events
  - Query data model and inject MAPDL commands
  - Must activate "Connect/Run Python Code Objects" preference
  - Auto-completion and syntax highlighting in editor
  - PyOptiSLang scripts and Python API available separately
- **Missing:** No guidance on how to make Python Code objects work with optiSLang design point iterations, no mention of parameterizing Python Code objects for optiSLang, no mention of the specific interaction between optiSLang and Mechanical Python Code objects during batch execution
- **Incorrect:** None, but the answer doesn't actually address the integration question — it describes Mechanical's Python Code objects and optiSLang's Python API separately without explaining how they work together

### Verdict: FAIL

**Gap:** Bot finds docs for each product separately but can't explain the integration. The specific workflow for using Mechanical Python Code objects in an optiSLang loop doesn't surface.

---

## OSL-021: "Script works in standalone Mechanical but fails in optiSLang — why?"

- **Cites ansyshelp?** NO — discuss.ansys.com forum post
- **Key facts returned:**
  - Scripts using `.GetPane()` fail in batch mode (which optiSLang uses)
  - UI pane commands not available in batch/headless execution
  - Solution: use RST reader instead of GUI-based data extraction
  - Check "Connect/Run Python Code Objects" setting
- **Missing:** No mention of other common batch mode incompatibilities, no general guidelines for writing batch-compatible scripts, no mention of checking optiSLang logs for the specific error
- **Incorrect:** None

### Verdict: PASS

**Note:** The forum thread provides exactly the right answer with root cause and solution. Another case where discuss.ansys.com outperforms the official help site for troubleshooting.

---

## OSL-022: "How do I configure optiSLang licensing?"

- **Cites ansyshelp?** YES — links to Installation and Licensing Guide, Configuration page
- **Key facts returned:**
  - Refer to Installation and Licensing Guide sections
  - Configuration via Edit > Settings or optiSLang.ini file
  - Config file locations: Linux `$HOME/.config/Ansys/optiSLang`, Windows `%APPDATA%\Ansys\optiSLang`
  - OSL_CENTRAL_CONFIG_FILE env var override
- **Missing:** No mention of the Ansys License Manager, no mention of specific license features needed (osl_base, osl_premium, etc.), no mention of license server connection settings, no mention of FlexNet Publisher configuration
- **Incorrect:** None, but answer conflates general optiSLang configuration with licensing-specific configuration

### Verdict: PARTIAL

**Gap:** Bot finds the configuration page but not the specific licensing configuration steps. The Installation and Licensing Guide is referenced but its content doesn't surface.

---

## OSL-023: "How do I use signal data analysis in optiSLang?"

- **Cites ansyshelp?** NO — only blog posts, training courses, and User Guide PDF
- **Key facts returned:**
  - Signal Processing component within Workbench project
  - ETK Tab for reference vs simulation signals
  - Files Tab for managing data files
  - Variables Tab for defining variables/responses
  - Material calibration example: force-displacement curves
  - Compare simulation to experimental signals
- **Missing:** No mention of the ETK (Engineer's Toolbox / Extraction, Transformation, Knowledge) system in detail, no mention of signal comparison methods (area, corridor, peak), no mention of the standalone Signal Processing node in optiSLang
- **Incorrect:** None, but answer is based on a specific blog post example rather than general documentation

### Verdict: PARTIAL

**Gap:** Bot finds a blog tutorial about signal processing in a specific workflow but not the general signal data analysis documentation. The ETK system documentation doesn't surface.

---

## OSL-024: "How do I create a parametric study in optiSLang?"

- **Cites ansyshelp?** YES — links to tutorials page and Parametric System page
- **Also cites:** Innovation Courses, PyOptiSLang
- **Key facts returned:**
  - Create project, use Solver Wizard, define inputs/outputs
  - Configure parameter properties: bounds, resolution, types
  - Solver chain template for simulation tool
  - PyOptiSLang template-based approach with ParametricDesignStudyManager
  - Parameter types: Optimization, Stochastic, combined
  - Value types: Real, Integer, Bool, String
- **Missing:** No walkthrough of the Solver Wizard pages, no mention of the Guided Project Wizard (simplest path)
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Bot finds reference documentation about parameter configuration but not the step-by-step workflow for creating a first parametric study using the wizards.

---

## OSL-025: "How do I use the optiSLang post-processing features?"

- **Cites ansyshelp?** YES — links to Visualization page and Viewing Postprocessing Results
- **Also cites:** developer.ansys.com for Python postprocessing scripting
- **Key facts returned:**
  - Web Service: Project Monitoring > node > Visualization
  - Requires postprocessing (premium) license
  - Plot manipulation: hover for tools, click to expand
  - Change axis dimensions from dropdown
  - Design selection: click rows, Shift/Ctrl for multi-select, Best/All/Invert buttons
  - Export as CSV or PNG
  - Python scripting: default generation scripts by result type
  - Python console access via View > Dock Widgets
- **Missing:** No mention of the desktop postprocessing pane (only web service version described), no mention of specific plot types (parallel coordinates, scatter matrix, correlation matrix, anthill plots)
- **Incorrect:** None

### Verdict: PARTIAL

**Gap:** Bot finds the Web Service postprocessing docs but not the desktop application postprocessing (which is what most users use). The specific visualization types aren't enumerated.

---

# SUMMARY TABLE

## ModelCenter Results (25 questions)

| # | ID | Question | Cites AnsysHelp | Verdict |
|---|-----|----------|-----------------|---------|
| 1 | mc-001 | Install ModelCenter Desktop | YES | PARTIAL |
| 2 | mc-002 | System requirements for MC | YES | PARTIAL |
| 3 | mc-003 | Install MCRE | YES | PASS |
| 4 | mc-004 | Configure license server | YES | PASS |
| 5 | mc-005 | Create a workflow | YES (index) | FAIL |
| 6 | mc-006 | Wrap Excel spreadsheet | NO | FAIL |
| 7 | mc-007 | Connect to MATLAB | YES (index) | FAIL |
| 8 | mc-008 | Integrate with Workbench | YES (wrong product) | FAIL |
| 9 | mc-009 | Python scripting | NO | PARTIAL |
| 10 | mc-010 | Run from command line | NO | PARTIAL |
| 11 | mc-011 | API create components | NO | PASS |
| 12 | mc-012 | MBSE with SAM | YES | PARTIAL |
| 13 | mc-013 | What is MBSE | NO | PARTIAL |
| 14 | mc-014 | Use with Cameo | YES | PARTIAL |
| 15 | mc-015 | Perform trade study | YES | PARTIAL |
| 16 | mc-016 | Use Data Explorer | YES | PASS |
| 17 | mc-017 | DOE in ModelCenter | YES | PASS |
| 18 | mc-018 | Configure remote execution | YES | PASS |
| 19 | mc-019 | Distributed computing | YES | PARTIAL |
| 20 | mc-020 | Debug failing component | NO | FAIL |
| 21 | mc-021 | Connection error fix | YES | FAIL |
| 22 | mc-022 | Migrate old workflows | NO | PARTIAL |
| 23 | mc-023 | Wrap custom executable | YES | FAIL |
| 24 | mc-024 | Link variables | PARTIAL (auth wall) | FAIL |
| 25 | mc-025 | Third-party plugins | YES | PARTIAL |

**ModelCenter: 6 PASS / 11 PARTIAL / 8 FAIL (24% pass rate)**

## optiSLang Results (25 questions)

| # | ID | Question | Cites AnsysHelp | Verdict |
|---|-----|----------|-----------------|---------|
| 1 | osl-001 | Install standalone | YES | PARTIAL |
| 2 | osl-002 | System requirements | YES (empty) | FAIL |
| 3 | osl-003 | Run in batch mode | NO | PASS |
| 4 | osl-004 | Batch mode arguments | YES | PASS |
| 5 | osl-005 | Automate with PyOptiSLang | NO | PARTIAL |
| 6 | osl-006 | PyOSL server port error | NO | PASS |
| 7 | osl-007 | Sensitivity analysis | YES | PARTIAL |
| 8 | osl-008 | Damped oscillator opt | YES | PASS |
| 9 | osl-009 | Use MOP | YES | PASS |
| 10 | osl-010 | What is CoP | YES | PASS |
| 11 | osl-011 | Use AMOP | NO | PARTIAL |
| 12 | osl-012 | Set up DOE | PARTIAL | PARTIAL |
| 13 | osl-013 | Integrate with Workbench | YES | PASS |
| 14 | osl-014 | Connect to Mechanical | NO | FAIL |
| 15 | osl-015 | Use with Fluent | NO | PARTIAL |
| 16 | osl-016 | Use with MATLAB | YES | PASS |
| 17 | osl-017 | Use with Excel | YES | PARTIAL |
| 18 | osl-018 | Robust design optimization | YES | PARTIAL |
| 19 | osl-019 | Reliability analysis | YES | PASS |
| 20 | osl-020 | Python code objects + Mech | YES | FAIL |
| 21 | osl-021 | Script fails in oSL | NO | PASS |
| 22 | osl-022 | Configure licensing | YES | PARTIAL |
| 23 | osl-023 | Signal data analysis | NO | PARTIAL |
| 24 | osl-024 | Parametric study | YES | PARTIAL |
| 25 | osl-025 | Post-processing features | YES | PARTIAL |

**optiSLang: 10 PASS / 12 PARTIAL / 3 FAIL (40% pass rate)**

## Combined Results

| Metric | ModelCenter | optiSLang | Combined |
|--------|-------------|-----------|----------|
| PASS | 6 (24%) | 10 (40%) | 16 (32%) |
| PARTIAL | 11 (44%) | 12 (48%) | 23 (46%) |
| FAIL | 8 (32%) | 3 (12%) | 11 (22%) |
| Cites AnsysHelp | 15/25 (60%) | 15/25 (60%) | 30/50 (60%) |

---

# KEY FINDINGS

## What's Working

1. **Installation/licensing docs for MCRE** — MCRE install and license configuration pages are well-structured HTML that bots parse easily. Both get PASS verdicts.

2. **optiSLang technical reference content** — MOP, CoP, FORM, MATLAB integration, and Workbench integration pages are well-structured and deliver strong bot answers. These are the standout pages in the ansyshelp corpus.

3. **Community forum (discuss.ansys.com)** — Consistently outperforms official docs for CLI/scripting questions and troubleshooting. Three questions get PASS verdicts primarily from forum content (osl-003, osl-006, osl-021).

4. **PyAnsys docs sites** — Well-structured Sphinx docs are highly crawlable. They dominate for Python/API questions but create a bias problem (see below).

5. **Developer Portal (developer.ansys.com)** — API reference content surfaces well for programmatic questions. MC-011 gets a PASS from Developer Portal content alone.

6. **Tutorial content** — optiSLang tutorials (damped oscillator, sensitivity analysis) surface well and give users a starting point.

## What's Broken

### 1. GUI procedure content is systematically invisible (12 questions affected)

The most common failure mode. Bot finds overview/index pages but cannot extract step-by-step GUI procedures from ansyshelp.ansys.com. Affected questions: mc-001, mc-005, mc-006, mc-007, mc-008, mc-012, mc-015, mc-023, mc-024, osl-001, osl-011, osl-012.

**Root cause:** ansyshelp.ansys.com serves content through JavaScript-heavy navigation and iframes that AI crawlers cannot parse. Index/TOC pages are visible but the actual task content behind them is not.

### 2. PyAnsys/Developer Portal docs outcompete product docs (7 questions affected)

For any question with a Python/API angle, PyAnsys or Developer Portal docs completely dominate. The product's own documentation about built-in GUI features doesn't surface. Affected: mc-005, mc-009, mc-010, mc-020, osl-005, osl-020, osl-025.

**Impact:** Users get API-first answers when they need GUI-first answers. A user asking "How do I create a workflow?" gets a Python code example instead of File > New.

### 3. ansyshelp authentication wall blocks content (2 questions directly affected, likely more)

MC-024 found the correct help page URLs but got auth-required redirects. Unknown how many other pages are similarly blocked from crawlers.

### 4. No troubleshooting/FAQ content exists for bots to find (3 questions affected)

MC-020, mc-021, and osl-020 have no diagnostic workflow in the docs. When something goes wrong, there's no "check X, then Y, then Z" content for bots to extract.

### 5. Marketing/overview pages outrank product docs (4 questions affected)

For conceptual questions (mc-013, mc-007, osl-014, osl-015), ansys.com product marketing pages dominate over the actual help documentation. Users get sales-level descriptions instead of technical content.

### 6. Cross-product integration docs are weak (3 questions affected)

MC-008, osl-014, osl-020 — questions about how two Ansys products work together get confused or incomplete answers because each product's docs exist in isolation.

## optiSLang vs ModelCenter: Why the Gap?

optiSLang scores significantly better (40% pass vs 24% pass) for identifiable reasons:

1. **optiSLang has more HTML content pages** that are individually crawlable (MOP, FORM, MATLAB, Workbench pages). ModelCenter's content is more heavily locked behind JavaScript navigation.

2. **optiSLang has richer external ecosystem** — MathWorks partner pages, Wikipedia article, Innovation Courses. These provide alternative sources when ansyshelp fails.

3. **ModelCenter's core workflows are more GUI-dependent** — creating workflows, wrapping components, linking variables are inherently visual operations that don't translate to crawlable text as well as optiSLang's more algorithmic/configuration-based workflows.

---

# RECOMMENDED ACTIONS (Updated from 5-question pilot)

## Immediate (validates the llms.txt proposal)

1. **Crawlability audit of ansyshelp.ansys.com** — Test whether individual content pages (not just index pages) are accessible to AI crawlers (Googlebot, GPTBot, ClaudeBot, PerplexityBot). Check robots.txt, JavaScript rendering requirements, and authentication gates.

2. **Propose llms.txt at ansyshelp.ansys.com root** — Provide AI engines a structured map to the most important content pages. Prioritize the 11 FAIL questions' topics.

3. **Identify the 11 FAIL pages specifically** — For each FAIL verdict, locate the exact ansyshelp page(s) that should have answered the question, and test whether they're accessible to crawlers.

## Short-term (doc structure improvements)

4. **Make procedure topics self-contained** — Each task topic should contain the complete step-by-step procedure on a single page, not spread across multiple sub-pages behind JavaScript navigation. Priority targets:
   - ModelCenter: Workflow creation, Excel wrapping, FileWrapper, variable linking, MATLAB setup
   - optiSLang: Installation wizard, DOE setup, AMOP configuration

5. **Add troubleshooting/FAQ sections** — Create crawlable troubleshooting content for common errors and diagnostic workflows. The forum content that bots love proves users need this.

6. **Cross-link product docs and PyAnsys docs** — Every ansyshelp page about a Python-automatable feature should link to the corresponding PyAnsys page, and vice versa. This helps bots discover both sources.

## Medium-term (content strategy)

7. **Create "integration guide" pages** — For each supported Ansys product integration (Workbench, Mechanical, Fluent), create a single comprehensive page covering the complete integration workflow. Current content is fragmented or missing.

8. **Review ModelCenter User Guide structure** — The 32% FAIL rate for ModelCenter (vs 12% for optiSLang) suggests a structural problem with how MC content is organized and served, beyond just crawlability.

9. **Leverage forum content** — The best bot answers come from discuss.ansys.com. Consider promoting proven forum answers into the official docs, or ensuring the forum's crawlability is maintained.
