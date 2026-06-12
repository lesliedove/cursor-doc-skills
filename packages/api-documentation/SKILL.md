---
name: api-documentation
description: >-
  Ansys API, library, and SDK documentation guidelines for the Dev portal.
  Covers writing style, package structure, metadata, compliance, and migration.
  Use when creating, reviewing, or migrating API docs, REST APIs, gRPC APIs,
  library docs, SDK docs, OpenAPI specs, or docfx packages.
---

# Ansys API Documentation Guidelines

## Source of truth

Authoritative requirements flow from Melanie Guyot's team guidelines through publication into DevRelDocs:

1. **Upstream (authoring source):** [ansys-internal/developer-documentation-guidelines](https://github.com/ansys-internal/developer-documentation-guidelines) — Hugo source for `content/docs/` (package types, metadata, migration, compliance checklist). Local clone: `<your-clone>/developer-documentation-guidelines`.
2. **Published site:** `https://doc-guidelines.sandbox.ansysapis.com/docs/` — rendered from that repo; use this URL for **Reference** lines in compliance reports.
3. **Dev portal rubric:** **`.github/AGENTS.md`** in [ansys/DevRelDocs](https://github.com/ansys/DevRelDocs) — agent compliance checklist synced to the published site. When AGENTS.md or the sandbox site disagrees with anything below, **those win**.

Before a real compliance review, fetch the latest AGENTS.md and spot-check the sandbox site for tagged **Must have / Should have / Nice to have** requirements.

Use the sandbox URL (not GitHub repo links) for **Reference** lines in any compliance report — including links to `developer-documentation-guidelines`.

## Compliance reports

When asked for a compliance check, self-review, or pre-PR verification, create or update **`documentation-compliance-report.md`** in the package root (next to `docfx.json`). The report should:

- Classify the package per section 1 below; include only the type(s) that apply (no "N/A" filler).
- List **Issues** as violations only — never tag a passing check with a severity.
- Tag every issue and action item with exactly one severity: **Must fix**, **Should fix**, or **Nice to fix** (mapping below).
- Add a **Reference** link on each issue tied to a tagged guideline rule, using the sandbox URL above.

### Severity mapping (guideline tag → review severity)

| Guideline tag | Review severity when not met |
|---------------|------------------------------|
| **Must have** | **Must fix** |
| **Should have** | **Should fix** |
| **Nice to have** | **Nice to fix** |

Approval line: **Approved** = no open Must fix; **Needs Minor Revisions** = no Must fix; **Needs Major Revisions** = one or more Must fix.

## 1. Classify the package first

Before applying any rules, classify the documentation package by which type(s) apply:

| Type | Authoritative reference | Key indicator |
|------|------------------------|---------------|
| **REST API** | OpenAPI/Swagger spec (JSON or YAML) | `openapi` or `swagger` root object in spec file |
| **API (prose)** | Markdown prose | Wire protocol or message-based API documented in Markdown, not OpenAPI |
| **Library/SDK** | Markdown (possibly generated from Doxygen/Sphinx/proto) | Language-specific interface with classes, methods, functions |

**One primary type per package folder** under `docs/<product>/<doc-package>/versions/<version>/`. **Must not** combine **REST API** (OpenAPI at root) and **Library/SDK** in a single migration package—ship separate folders or PRs. **May** combine **Library/SDK** with **API (prose)** in the same Markdown tree when the wire API has no OpenAPI spec. When multiple surfaces apply, use the union of applicable checklists.

**Package naming:** Never label a package **HTTP API**—use **REST API** (OpenAPI authoritative) or **API (prose)** (wire protocol in Markdown). Do not use **API** and **library** interchangeably (APIs are protocol-based; libraries are language-specific and require install).

## 2. Required files by type

| File | REST API | API (prose) | Library/SDK |
|------|----------|-------------|-------------|
| `docfx.json` | Root | Root | Root |
| OpenAPI spec (`.json`/`.yaml`/`.yml`) | Root | -- | -- |
| `index.md` | `description/index.md` | Root | Root |
| `changelog.md` | `changelog/changelog.md` | Root | Root |
| `toc.yml` | Not required | Root | Root |

REST API packages: only `docfx.json` and the OpenAPI spec at root. Descriptive content goes in `description/`, changelog in `changelog/`.

## 3. Style rules

Follow the [Google developer documentation style guide](https://developers.google.com/style).

- **Must have** — Sentence case for all headings and titles.
- **Must have** — Active voice and present tense.
- **Must have** — Short, clear sentences and consistent technical terminology (no synonym swapping).
- **Must have** — Vale (Google style + Ansys vocab) and Markdownlint pass before PR submission.

## 4. Markdown rules

Format: GitHub Flavored Markdown. Encoding: UTF-8 only (not Windows-1252). Do not rely on unsupported Docfx Markdown extensions.

- **Must have** — One H1 per Markdown file (first heading after frontmatter), except REST `description/index.md` and `changelog/changelog.md` (H2-first, no H1).
- **Must have** — When formulas are used, valid LaTeX (`$$...$$` block, `$...$` inline); invalid or mixed delimiters = **Must fix**.
- File names: lowercase with hyphens (`getting-started.md`, not `Getting_Started.md`). Paths become public URLs—keep them short.
- Image file extensions: always lowercase (`.png`, `.jpg`).
- **Should have** — Informative images have descriptive alt text; empty alt (`![](path)`) only for decorative images.
- Code blocks: always specify language for syntax highlighting.
- Ordered lists with embedded code or images: indent by 4 spaces with a blank line above.
- Links opening in new tabs: use `<a target="_blank" href="...">`.
- Collapsible sections: use `<details>` and `<summary>` tags.
- Tables with merged cells or bulleted lists in cells: use HTML.
- Hidden comments: `<!-- comment -->`.
- When Markdown lacks a construct, inline HTML is permitted (prefer Markdown first).

## 5. Metadata (`docfx.json`)

### Required fields (`build.globalMetadata`)

All metadata keys must be lowercase.

**Markdown and Library/SDK packages:**

```json
{
  "build": {
    "globalMetadata": {
      "title": "Product Name API 2026 R1",
      "summary": "Brief description of the documentation (not the product).",
      "version": "2026 R1",
      "physics": "Product Collection Category"
    }
  }
}
```

**Must have** — `title` is product + version only; omit redundant words like "documentation" or "guide". **Should have** — include valid `product` (see `product.yml`). Validate every taxonomy field in use against `config/portal-metadata/*.yml`.

**REST API packages** (metadata split between `docfx.json` and OpenAPI `info`):

```json
{
  "build": {
    "globalMetadata": {
      "doc_type": "rest_api",
      "product": "Product Name",
      "summary": "Brief description of the documentation.",
      "physics": "Product Collection Category"
    }
  }
}
```

Title and version come from the OpenAPI `info` object for REST API packages.

**Doxygen packages:** add `"doc_type": "doxygen"` and `"product"` to the standard fields.

### Version format

`YYYY R1|R2 [SP01-SP04]` — examples: `2026 R1`, `2026 R1 SP04`, `2026 R2`.

### Optional metadata

- `programming language` (**Nice to have**): use a value from `programming_language.yml` when a single language filter is meaningful. Skip for language-agnostic packages (e.g., many REST APIs). If set, the value must be valid.
- Other optional fields: `product`, `status` (`published`/`unpublished`), `access control`, `author`, `author email`, `description` (file-level only, for SEO), `date` (ISO-8601), `keywords`, `audience`, `context`.

## 6. API reference quality

### REST APIs (descriptive content in `description/index.md`)

**Must have** — H2 sections: Introduction, Resources, Authenticate, Send API requests, Responses. Auth section must state method types (API key, token, or bearer).

**Should have** — Introduction covers testing environment (Dev portal testability, alternatives, production URLs). curl and Postman examples; response table, format, and pagination when applicable.

### REST APIs (OpenAPI reference)

- OpenAPI spec must validate in Swagger Editor without errors.
- `info.description`: one-sentence summary (**Should have**).
- Group endpoints by category using `tags` with tag descriptions (**Should have**).
- **Must have** — `summary` sentence case, no trailing period.
- **Should have** — `description`, parameter descriptions, all responses, concise response-object descriptions, and realistic request/response examples (never generic `"string"` placeholders).

### gRPC APIs

- Generate docs from proto files using `protoc-gen-doc`.
- Follow the [Protocol Buffers Style Guide](https://protobuf.dev/programming-guides/style/).
- **Should have** — file-level description; group related definitions; leading/trailing comments; capitalize comments and end with period.
- Comment every message, service, field, and enum value. Use `@exclude` to omit internal-only comments from generated docs.
- PascalCase for messages/enums/services; `lower_snake_case` for fields.
- Enum zero value: suffix with `UNSPECIFIED`. Enum values end with semicolon.
- Prefix enum values with the enum name to avoid collisions.
- Use Markdown syntax in proto comments. Formulas in comments: valid LaTeX only.

### API (prose)

- **Must have** — Root `index.md` with Introduction; changelog at `changelog.md` or `changelog/changelog.md`.
- **Do not** require Resources, Authenticate, Send API requests, or Responses—that is REST-only.
- **Should have** — Introduction covers capabilities, protocol, and testing environment.

### Other APIs (non-REST, non-gRPC wire protocols)

- **Must have** — Clearly define the specific protocol and data formats.
- Document all messages in Markdown.
- **Should have** — Field descriptions including type and whether each field is mandatory.

## 7. Library/SDK documentation

Descriptive content severity tags:

| Section | Priority |
|---------|----------|
| **Introduction** (`index.md`, H1 must be exactly `# Introduction`) | **Must have** |
| **Changelog** (`changelog.md` or `changelog/changelog.md`) | **Must have** |
| **Getting started** (dependencies, install, dev env, licensing) | **Should have** |
| **User guide** | **Should have** |
| **Usage examples** | **Should have** |
| **Platform overview** (inside Introduction) | **Nice to have** |

Introduction body **Should have** — main features, target audience, language/OS support, library role (client/server/both). Do not flag a missing platform overview as Must fix or Should fix.

Reference documentation requirements:

- Document every function (purpose, parameters, return values, exceptions).
- Document every class (purpose, methods, properties).
- Document all data structures.
- Document class hierarchies and namespaces when applicable.

## 8. Directory structure

### API (prose) and Library/SDK packages

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

Subdirectory `index.md` files (e.g., `getting-started/index.md`) are **Nice to have**, not required. Do not flag missing subsection `index.md` as Must fix or Should fix.

**Image and asset folders** (Should have when figures are used):

- **API (prose) / Library/SDK**: place binary images and diagrams under any `images/` or `assets/` directory in the package tree (not loose beside Markdown or `docfx.json`).
- File extensions are lowercase (`.png`, `.jpg`).
- Informative images have descriptive alt text (Should have).

### REST API-only packages

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

REST API requirements:

- `description/index.md` first heading is **H2** (typically `## Introduction`); section headings (`Introduction`, `Resources`, `Authenticate`, `Send API requests`, `Responses`, optional `Platform overview`) use **H2**. **No H1** in the file.
- `changelog/changelog.md` first heading is **H2** (`## Changelog` or a category like `## Added`, `## Fixed`, `## Changed`, `## Deprecated`, `## Removed`). **No H1** in the file.
- Binary images live under `description/images/` or `description/assets/` only — not at package root.
- `toc.yml` and a root-level `index.md` are **not** required for REST API-only packages.

## 9. TOC configuration (`toc.yml`)

```yaml
- name: Package name
  href: overview.md
  items:
  - name: Get started
    items:
    - name: Prerequisites
      href: get-started/prerequisites.md
```

- `name`: display name (optional—defaults to file title metadata or first H1). Wrap in double quotes if it contains `::`, `~`, `#`, or `{}`.
- `href`: path to the file. Optional for parent-only nodes.
- `items`: child nodes.
- No duplicate `href` values across the TOC.
- Exactly one `toc.yml` per package tree.

## 10. Changelog format

- Latest version at top with release date.
- Categorize: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**.

## 11. Migration overview

Migration to the Dev portal follows 5 steps:

1. **Classify** the package type (one primary type per folder) and confirm required files (see section 2).
2. **Prepare** documentation in Markdown at `docs/<product>/<doc-package>/versions/<YYYY.RX.SPXX>/` (convert from source format if needed).
3. **Submit** a PR to the appropriate GitHub repo (one package per PR when practical):
   - **DevRelDocs** for public documentation
   - **DevRelDocs_internal** for internal documentation
4. **Review** in the sandbox environment — merge to `accept` first, validate, then promote to `main`.
5. **Approve** explicit sign-off for production migration after sandbox validation.

Upload documentation at least 3-4 days (ideally 10 days) before release date. Engage Ansys documentation specialists for pre-migration review when available.

For detailed migration workflows and format conversion instructions, read [migration-reference.md](migration-reference.md).

## 12. Compliance checklist (summary)

Before submitting a PR, verify:

- Markdownlint passes.
- Vale passes (Google style rules).
- All links are functional.
- Images render with lowercase extensions; informative images have alt text.
- Docfx builds clean locally.
- Required metadata fields are populated.
- Taxonomy values validated against YAML sources (`physics.yml`, `product.yml`, `programming_language.yml`) — typically under `config/portal-metadata/` on the active branch.
- Package structure matches the classified type (and any hybrid surfaces).
- For REST API: `description/index.md` and `changelog/changelog.md` use H2-first headings (no H1).

### Compliance reports

When asked for a compliance check, write findings to **`documentation-compliance-report.md`** in the package root for local review only — **do not commit or push** that file to DevRelDocs. Include:

- Title, ISO date, package path relative to repo root.
- **Summary line**: Approved / Needs Minor Revisions / Needs Major Revisions (justified per severity rules below).
- **Classification**: only the type(s) that apply, with evidence. No "N/A" filler for types that don't apply.
- **Issues**: violations only — never tag a passing observation with a severity.
- **Action items**: mirror open Issues only, ordered by severity.
- Each Issue and Action item: tagged with **Must fix**, **Should fix**, or **Nice to fix**, plus an absolute **Reference** link on the sandbox guidelines site (`https://doc-guidelines.sandbox.ansysapis.com/docs/...`) when the finding maps to a tagged guideline rule. **Do not** use `github.com/ansys-internal/developer-documentation-guidelines` URLs in Reference lines.

### Review severity

| Guideline tag | Review severity when not met | Effect |
|---|---|---|
| **Must have** | **Must fix** | Blocks Approved; drives Needs Major Revisions |
| **Should have** | **Should fix** | Drives Needs Minor Revisions (or Major if widespread) |
| **Nice to have** | **Nice to fix** | Optional; does not block Approved |

Approval line:

- **Approved** — no open Must fix; no Should fix the reviewer treats as release-blocking.
- **Needs Minor Revisions** — no Must fix; one or more Should fix or Nice to fix.
- **Needs Major Revisions** — one or more Must fix, or widespread Should-fix issues the reviewer treats as release-blocking.

## 13. PR process

- Submit PRs to **DevRelDocs** (public) or **DevRelDocs_internal** (internal).
- Melanie approves all PRs.
- PR title: clear identification of package and scope.
- PR description: summarize changed docs and target audience.
- Include validation notes (linting results, local rendering, link checks).

## Full references

- For complete writing guidelines, metadata details, and compliance checklist: read [api-guidelines-reference.md](api-guidelines-reference.md).
- For migration workflows and format conversion details: read [migration-reference.md](migration-reference.md).
