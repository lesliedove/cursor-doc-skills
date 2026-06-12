# Migration Reference — Ansys Dev Portal

This file covers migration workflows and format conversions for getting documentation onto the Ansys Dev portal. Read SKILL.md first for package classification and required files.

---

## 1. Migration process (5 steps)

### Step 1: Prepare the documentation package

1. Classify the package type (REST API, API prose, or Library/SDK) — one primary type per folder.
2. Place the package at `docs/<product>/<doc-package>/versions/<YYYY.RX.SPXX>/` (e.g. `2026.R1.SP02`). Do not use legacy roots like `2026R1/`.
3. Confirm required files against the requirements matrix in section 2.
4. Organize content in Markdown with required metadata and navigation files.

### Step 2: Set up GitHub access

1. Create a GitHub account if needed.
2. Enable two-factor authentication.
3. Join both Ansys GitHub organizations:
   - [Ansys](https://github.com/ansys)
   - [Ansys Internal](https://github.com/ansys-internal)

### Step 3: Submit a PR

Submit Markdown files (not zipped) via a pull request to the appropriate repository:

- **DevRelDocs** — public documentation.
- **DevRelDocs_internal** — internal documentation.

PR requirements:

- Clear title identifying the package and scope.
- Description summarizing changed docs and target audience.
- Validation notes (linting results, local rendering, link checks).
- Branch naming convention: `release/doc-package-name` (e.g. `2026-r1/mechanical-scripting-interface`).

Melanie approves all PRs.

**Should have** — one documentation package (one version folder) per PR; do not mix unrelated packages.

### DevRelDocs team workflow (post-reorg)

1. Push and merge to the **`accept`** branch first.
2. Wait for automated migration; validate in sandbox.
3. If sandbox passes, promote the same change to **`main`**.
4. Release-safe pattern: land docs unpublished on `main`; on release day, metadata-only PR to set `status: published`.

### Step 4: Review in sandbox

After submission, the Dev portal team deploys to a sandbox and provides a preview link.

1. Open the Synopsys developer sandbox (e.g. `https://developer-a.synopsys.com/`).
2. Sign in with provided credentials when required.
3. When prompted with a second login page, browse as an anonymous user with the preview link instead.
4. Review for: missing content, formatting issues, broken links, TOC/navigation, metadata, images.

### Step 5: Approve final migration

Confirm with the Dev portal team to proceed to the production environment.

### Timeline

Upload documentation at least 3-4 days before release date. Ideal lead time: 10 days.

---

## 2. Package requirements matrix

| Package type | Authoritative reference | Required root files | Descriptive files | Changelog | `toc.yml` | Metadata source | Primary guide |
|---|---|---|---|---|---|---|---|
| **REST API** | OpenAPI/Swagger spec | `docfx.json` + spec file | `description/index.md` | `changelog/changelog.md` | No | Split: `docfx.json` + OpenAPI `info` | REST API (OpenAPI) doc management |
| **API (prose)** | Markdown prose | `index.md`, `docfx.json` | `index.md` | `changelog.md` or `changelog/changelog.md` | Yes | `docfx.json` `build.globalMetadata` | Markdown doc management |
| **Library/SDK** | Markdown (generated or authored) | `index.md`, `docfx.json` | Intro, getting started, user guide, examples | `changelog.md` or `changelog/changelog.md` | Yes | `docfx.json` `build.globalMetadata` | Markdown or Doxygen doc management |

**One primary type per package folder.** **Must not** combine REST API (OpenAPI at root) and Library/SDK in one migration package. **May** combine Library/SDK with API (prose) in the same Markdown tree. Never label a package **HTTP API** — use REST API or API (prose).

---

## 3. Markdown package management

### Required files

**API (prose) and Library/SDK packages:**

- `toc.yml` — navigation definition.
- `docfx.json` — metadata.
- `index.md` — landing page.
- `changelog.md` or `changelog/changelog.md` — release history.

**REST API-only packages:**

- `docfx.json` at root.
- OpenAPI/Swagger spec (`.yml`, `.yaml`, `.json`) at root.
- `description/index.md` for descriptive content.
- `changelog/changelog.md` for release history.
- Do not place `toc.yml`, `index.md`, or `changelog.md` at root.

### File naming rules

- Lowercase with hyphens: `getting-started.md`, not `Getting_Started.md`.
- Use `-` not `_` (URL compatibility).
- Subdirectory `index.md` files are **Nice to have**, not required. Don't flag missing subsection `index.md` as Must fix or Should fix.

### Recommended structure

```
Documentation-package/
├── index.md
├── changelog.md
├── getting-started/
│   ├── index.md
│   ├── prerequisites.md
│   ├── installation.md
│   └── licensing.md
├── user-guide/
│   └── ...
├── examples/
│   └── ...
├── api-reference/
│   └── (generated docs)
├── images/
│   └── (lowercase extensions)
├── toc.yml
└── docfx.json
```

### `toc.yml` format

```yaml
- name: Doc package name
  href: overview.md
  items:
  - name: Get started
    items:
    - name: Prerequisites
      href: get-started/prerequisites.md
```

- `name` is optional (defaults to file title metadata or first H1). Wrap in double quotes if it contains `::`, `~`, `#`, or `{}`.
- No duplicate `href` values.
- Exactly one `toc.yml` per package tree.

---

## 4. REST API package management

### Requirements

- OpenAPI/Swagger spec must validate in [Swagger Editor](https://editor.swagger.io/) without errors.
- Documentation must be in GitHub Flavored Markdown.
- Validate with Vale (Google style).
- `description/index.md`: first heading is **H2** (typically `## Introduction`); section headings (`Introduction`, `Resources`, `Authenticate`, `Send API requests`, `Responses`, optional `Platform overview`) use **H2**. **No H1** in the file.
- `changelog/changelog.md`: first heading is **H2** (`## Changelog` or a category like `## Added` / `## Fixed` / `## Changed` / `## Deprecated` / `## Removed`). **No H1** in the file.
- Binary images live under `description/images/` or `description/assets/` only — not at package root.

### Directory structure

```
Documentation-package/
├── docfx.json
├── openapi.yaml
├── description/
│   ├── index.md
│   └── images/                   (or assets/, if needed)
└── changelog/
    └── changelog.md
```

Only `docfx.json` and the spec file at root. No `toc.yml`, no root-level `index.md`.

---

## 5. Doxygen package management

Doxygen-generated Library/SDK documentation must be converted to Markdown before submission.

### Migration model

1. Generate source docs from code comments.
2. Convert to Markdown (see Doxygen conversion in section 7).
3. Organize as a standard Markdown package.
4. Add `docfx.json` (with `doc_type: "doxygen"`), `toc.yml`, and required metadata.
5. Submit via PR.

### Post-conversion quality checks

- Verify heading hierarchy (one H1 per page, then H2, H3, etc.).
- Verify generated links and image paths.
- Remove conversion artifacts (escaped underscores, unwanted TODO sections, multiple H1 headings).
- Fix relative links that still target source-tool outputs.
- Validate Markdown formatting locally.

---

## 6. Validation before submission

### Tools

- **Markdownlint**: install as VSCode extension. Inline errors and warnings.
- **Vale**: install via `choco install vale`. Configure with Google style. Run `vale .` in the package directory.
- **Docfx**: install via `dotnet tool update -g docfx`. Build with `docfx docfx.json --serve`. View at `http://localhost:8080`.

### Checklist

- Markdownlint passes.
- Vale passes.
- All links functional.
- Images render (lowercase extensions).
- Docfx builds clean.
- Required metadata populated.
- `doc_type` set correctly for REST API and Doxygen packages.

---

## 7. Format conversion index

### DITA to Markdown

**Tool:** Oxygen XML Editor.

1. Open the bookmap in Oxygen XML Editor.
2. Click **Configure Transformation Scenarios**.
3. Select **DITA Map Markdown** and click **Apply Associated**.
4. Output: `out/markdown` directory.
5. Post-process: use the **Process Markdown Files from DITA** GitHub action from [ansys/doc-to-markdown](https://github.com/ansys/doc-to-markdown) to clean files and generate `toc.yml`.
6. Validate with Docfx.

### DocBook to Markdown

**Tool:** Oxygen XML Editor + [ansys/doc-to-markdown](https://github.com/ansys/doc-to-markdown).

Two-step conversion: DocBook XML → HTML → Markdown.

1. Open the XML file in Oxygen XML Editor.
2. Configure transformation: select **DocBook HTML - Chunk**. Create a copy when prompted.
3. Set XSL URL to `your-repo-root/documentation/tools/XSL/custom_docbook/custom_chunk.xsl`.
4. Set `chunk.section.depth` parameter to `3`.
5. Apply. Output: `out/html-chunks`.
6. Convert HTML to Markdown using the **Process Markdown Files from DocBook** action from [ansys/doc-to-markdown](https://github.com/ansys/doc-to-markdown).
7. Validate with Docfx.

### Doxygen to Markdown

**Tool:** Seaborg (`@seaborg/cli`).

**Prerequisites:** Doxygen, Node.js + npm.

1. In Doxyfile, set `GENERATE_XML = YES`. Run Doxygen.
2. Install Seaborg: `npm install @seaborg/cli`.
3. Convert: `npx seaborg <xml-directory> <output-directory>`.
4. Post-process the generated Markdown:
   - Remove private members (Seaborg includes them even when Doxyfile excludes them).
   - Remove backslashes before underscores in headings.
   - Reposition HTML ID tags to row 3 (after H1 heading and blank line).
   - Remove unexpected TODO sections.
   - Fix C language badges if needed (C++ badges appear for C code). Use `replace-language-badge.py`.
5. Generate `toc.yml`: run `python xml-index-to-toc.py` in the XML directory containing `index.xml`.
6. Validate with Docfx.

### Sphinx to Markdown

**Tool:** `sphinx-markdown-builder` extension.

**Prerequisites:** Python, Chocolatey, Sphinx (`choco install sphinx`).

1. Install: `pip3 install sphinx-markdown-builder==0.6.6`.
2. Add `"sphinx_markdown_builder"` to the `extensions` list in `conf.py`.
3. For internal links, add to `conf.py`:
   ```python
   markdown_anchor_sections = True
   markdown_anchor_signatures = True
   ```
4. Build: `sphinx-build -M markdown ./docs ./build`.
5. Post-process using **Process Markdown Files from Sphinx** from [ansys/doc-to-markdown](https://github.com/ansys/doc-to-markdown).
6. For Jupyter notebook examples within Sphinx docs, convert separately (see Jupyter section below).
7. Validate with Docfx.

### Jupyter notebook to Markdown

**Tool:** `nbconvert`.

**Prerequisites:** Python.

1. Install: `pip install nbconvert`.
2. Create an `ansys` template directory with these files:

   **`conf.json`:**
   ```json
   {
     "mimetypes": {
       "text/markdown": true
     }
   }
   ```

   **`index.md.j2`:**
   ```jinja2
   {% extends 'markdown/index.md.j2' %}

   {%- block traceback_line -%}
   *Previous cell output:*
   ```output
   {{ line.rstrip() | strip_ansi }}
   ```

   {%- endblock traceback_line -%}

   {%- block stream -%}
   *Previous cell output:*

   ```output
   {{ output.text.rstrip() }}
   ```

   {%- endblock stream -%}

   {%- block data_text scoped -%}
   *Previous cell output:*

   ```output
   {{ output.data['text/plain'].rstrip() }}
   ```

   {%- endblock data_text -%}
   ```

3. Convert: `jupyter nbconvert --execute notebook.ipynb --to markdown --template=ansys --coalesce-streams`.
4. If the template directory is outside the notebook directory, add `--TemplateExporter.extra_template_basedirs=path/to/template/parent`.

### C# to Markdown

**Tool:** [AnsysVirtualMotion/DotnetDocfxMDGenerationDemo](https://github.com/AnsysVirtualMotion/DotnetDocfxMDGenerationDemo).

Follow the instructions in that repository. It uses Docfx to generate Markdown from C# comments and docstrings.

### Proto files to Markdown

**Tool:** `protoc-gen-doc`.

**Prerequisites:** Go (`choco install golang`), Protocol Buffers.

1. Download `protoc` from [Protocol Buffers releases](https://github.com/protocolbuffers/protobuf/releases).
2. Install: `go install github.com/pseudomuto/protoc-gen-doc/cmd/protoc-gen-doc@latest`.
3. Add `protoc` and `protoc-gen-doc` to your PATH.
4. Optionally create a custom Go template for tailored output.
5. Generate: `protoc --proto_path=<proto-dir> --doc_out=<output-dir> --doc_opt=<template>,<output-filename> <proto-dir>/*.proto`.
6. Verify links using [Markdown Live Preview](https://markdownlivepreview.com/) (VSCode preview may not resolve HTML anchors correctly).
7. Validate with Docfx.

### Word and PDF to Markdown

Three options:

**Docling** (recommended):
```bash
pip install docling
docling path-to-files/ --to md --output path-to-output/
```

**Google Docs extension:**
1. Paste content into a Google Doc.
2. Install the **Docs to Markdown** add-on.
3. Use **Extensions > Convert > Docs to Markdown**.
4. Split the single output file into per-section files.

**Writage:**
1. Install [Writage](https://www.writage.com/).
2. Open `.docx` in Word.
3. Save as Markdown.
4. Split the single output file into per-section files.

After conversion from Word/PDF, create `toc.yml` and `docfx.json` per the Markdown package management rules.

---

## 8. GitHub constraints

- Max 1,000 files per directory.
- Max 1 MB for text files.
- Max 100 MB per image/asset file.
- Files >1 MB: only `raw` or `object` media types.
- Files >100 MB: not supported via GitHub API.
