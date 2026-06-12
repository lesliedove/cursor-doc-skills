# Ansys API Documentation Guidelines — Full Reference

This is the detailed reference for Ansys API, library, and SDK documentation. Read SKILL.md first for the essentials. Use this file when you need full details on writing guidelines, metadata configuration, or the compliance checklist.

> **Source of truth.** Requirements originate in [ansys-internal/developer-documentation-guidelines](https://github.com/ansys-internal/developer-documentation-guidelines) (Melanie Guyot's team; local clone `<your-clone>/developer-documentation-guidelines`), publish to `https://doc-guidelines.sandbox.ansysapis.com/docs/`, and sync into `.github/AGENTS.md` in [ansys/DevRelDocs](https://github.com/ansys/DevRelDocs). When this file disagrees with AGENTS.md or the sandbox site, those win. Use the sandbox URL (not GitHub repo links) for **Reference** lines in any compliance report.

---

## 1. Terminology

### APIs

Interfaces that facilitate communication between software regardless of programming language. They define a communication protocol and message definitions.

- **REST APIs**: HTTP protocol + JSON/YAML data format.
- **gRPC APIs**: HTTP protocol + Protocol Buffers data format.
- **Other APIs**: Other protocols (e.g. OSC) + specific message definitions.

### Libraries

Language-specific interfaces offering efficient performance for specialized tasks. Consist of compiled code using functions, classes, and methods. Must be installed.

### SDK

A collection of libraries for a client plus ready-to-run code samples providing a framework for building against interfaces.

### Framework

Extends SDK concept to include pre-built modules for almost every interaction possible.

### Key distinction

- **API docs** describe language-agnostic, protocol-based interfaces (no installation required).
- **Library docs** describe language-specific interfaces (installation required). Must mention supported languages, operating systems, and the library's role (server, client, or both).
- Do **not** use **API** and **library** interchangeably — that deviates from industry norms and confuses readers.
- **Framework** is an industry term only; Ansys does not ship framework packages on the Dev portal today.

### Package type vs protocol labels

- **REST API** package = OpenAPI/Swagger at root is authoritative.
- **API (prose)** package = wire protocol and messages in Markdown (no OpenAPI as reference).
- **Library/SDK** package = language-specific surface (classes, functions, samples).
- Never label a migration package **HTTP API** — use **REST API** or **API (prose)**.
- **Must not** combine **REST API** (OpenAPI) and **Library/SDK** in one migration folder. **May** combine Library/SDK with **API (prose)** in the same Markdown tree.

---

## 2. Style rules

Follow the [Google developer documentation style guide](https://developers.google.com/style).

- Sentence case for headings and titles.
- Active voice. Present tense.
- Short, clear sentences.
- Use Vale with Google style guide rules to enforce these.
- Use Markdownlint for structural compliance.

---

## 3. Markdown rules

Format: GitHub Flavored Markdown (GFM). Encoding: UTF-8 only (not Windows-1252). Do not rely on unsupported Docfx Markdown extensions. MathML only where the package already supports it; prefer LaTeX `$`/`$$`.

- Block formulas: `$$...$$`. Inline formulas: `$...$` (LaTeX syntax).
- Subscript/superscript: use LaTeX (`$H_{2}O$`, `$E=mc^{2}$`).
- Image extensions: always lowercase (`.png`, `.jpg`).
- Ordered lists with code or images: indent by 4 spaces, blank line above each element.
- Links in new tabs: `<a target="_blank" href="...">`.
- Anchor links: `[text](#heading-slug)` for same page, `[text](file.md#heading-slug)` for other pages.
- Custom anchors: `<p id="eq-1">` then `[text](#eq-1)`.
- Image alt text + title: `![alt text](path "title text")`.
- Tables with merged cells, bulleted lists in cells, or headerless tables: use HTML.
- Hidden comments: `<!-- comment -->`.
- Collapsible sections: `<details>` and `<summary>` tags.

---

## 4. Package classification

Classify before applying any guidelines:

| Type | Authoritative reference | Required root files |
|------|------------------------|---------------------|
| **REST API** | OpenAPI/Swagger file | `docfx.json` + spec file at root; `description/index.md`; `changelog/changelog.md` |
| **API (prose)** | Markdown prose | `index.md`, `changelog.md`, `toc.yml`, `docfx.json` at root |
| **Library/SDK** | Markdown (possibly generated) | `index.md`, `changelog.md`, `toc.yml`, `docfx.json` at root |

Submit **one primary type per** `docs/<product>/<doc-package>/versions/<version>/` folder. **Must not** bundle OpenAPI REST API and Library/SDK in one package. Library/SDK **may** include **API (prose)** in the same Markdown tree. Apply every checklist that matches a delivered surface.

---

## 5. Metadata configuration

### Required metadata (`docfx.json` → `build.globalMetadata`)

All keys must be lowercase.

| Field | Description |
|-------|-------------|
| `title` | Documentation title + version (e.g. "DPF C++ client library 2026 R1"). **Must have** — omit redundant "documentation" or "guide" |
| `version` | Format: `YYYY R1\|R2 [SP01-SP04]` |
| `summary` | Brief description of the documentation (not the product) |
| `physics` | Product collection category (see `physics.yml` under `config/portal-metadata/` on the active branch) |

### REST API metadata split

- `docfx.json`: `doc_type: "rest_api"`, `product`, `summary`, `physics`.
- OpenAPI `info`: `title`, `version`, `description`.

### Doxygen packages

- Add `doc_type: "doxygen"` plus `product`.

### Markdown documentation example

```json
{
  "build": {
    "globalMetadata": {
      "title": "AVxcelerate Asset Preparation API 2026 R1",
      "summary": "Prepare AVxcelerate assets and tracks by augmenting existing 3D content with physics-based properties.",
      "version": "2026 R1",
      "physics": "Autonomous Vehicle Simulation"
    }
  }
}
```

### REST API documentation example

```json
{
  "build": {
    "globalMetadata": {
      "doc_type": "rest_api",
      "product": "AVxcelerate Sensors",
      "summary": "The Sensors REST API allows you to manage your Sensors Library.",
      "physics": "Autonomous Vehicle Simulation"
    }
  }
}
```

### Doxygen documentation example

```json
{
  "build": {
    "globalMetadata": {
      "title": "Common Fluids Format 2026 R1",
      "summary": "The Ansys Common Fluids Format SDK is a collection of APIs and data models for accessing or writing data to Ansys Common Fluids Format files.",
      "version": "2026 R1",
      "doc_type": "doxygen",
      "physics": "Fluids"
    }
  }
}
```

### Optional metadata

| Field | Description |
|-------|-------------|
| `product` | **Must have** for REST API `docfx.json`; **Should have** for all Markdown packages (see `product.yml`) |
| `status` | `published` or `unpublished` |
| `access control` | Access level (default: public) |
| `programming language` | Language terms |
| `author` / `author email` | Content author info |
| `description` | SEO description (file-level only) |
| `date` | ISO-8601 creation date |
| `keywords` | AI/SEO discovery keywords |
| `audience` | Target audience |
| `context` | Usage context |

File-level metadata uses YAML frontmatter. File-level values add to (not replace) global values.

---

## 6. Writing guidelines: API documentation

### Descriptive content (Markdown)

#### REST API (`description/index.md`)

**Must have** — H2 sections: Introduction, Resources, Authenticate, Send API requests, Responses. Auth must state method types (API key, token, bearer).

**Should have** per section:
- Introduction — capabilities, protocol, **testing environment** (Dev portal testability, alternatives, production URLs).
- Authenticate — key/token retrieval instructions.
- Send API requests — curl and Postman examples.
- Responses — response table, format (e.g. JSON), pagination when applicable.

#### API (prose) (`index.md`)

**Must have** — Introduction section. **Do not** require Resources, Authenticate, Send API requests, or Responses (REST-only).

**Should have** — Introduction covers capabilities, protocol, and testing environment.

#### Shared introduction topics

1. **Introduction**
   - Capabilities and features *(Should have)*.
   - Protocol definition *(Should have)*.
   - Testing environment info *(Should have)*.

2. **Platform overview** *(Nice to have)*
   - Explanatory diagram (API relationships).
   - Application development description.
   - Communication flow explanation.
   - Note: a missing Platform overview is **Nice to fix** at most, never Must fix or Should fix.

3. **Resources** (REST APIs) — define handled resources.

4. **Authenticate**
   - Authentication methods (API key, token, bearer token).
   - Key/token retrieval instructions.

5. **Send API requests**
   - curl examples.
   - Postman examples.

6. **Responses**
   - Response table (types, values, descriptions).
   - Response format (e.g. JSON).
   - Pagination info (if applicable).

For **REST API** descriptive files, the section headings (`## Introduction`, `## Resources`, `## Authenticate`, `## Send API requests`, `## Responses`) use **H2**. The file must contain **no H1** — Docfx supplies the page title from `info.title` in the OpenAPI spec.

### File naming

- **API (prose)**: landing page = `index.md`; changelog = `changelog.md` or `changelog/changelog.md`.
- **Library/SDK**: landing page = `index.md` with H1 exactly `# Introduction`; changelog = `changelog.md` or `changelog/changelog.md`.
- **REST API-only**: `description/index.md` + `changelog/changelog.md`.

### API reference: REST

- OpenAPI Specification (JSON or YAML) — **Must have** — validates for migration.
- **Should have** — one-sentence `info.description`; endpoints grouped with `tags` (+ tag descriptions).
- **Must have** — `summary` sentence case, no trailing period.
- **Should have** — `description`, parameter descriptions, all responses, concise response-object descriptions, realistic examples.

### Request/response examples

Use realistic, specific samples — not generic `"string"` placeholders:

```json
{
  "sensorsInformation": {
    "totalSensorCount": 1,
    "validSensors": [
      {
        "id": {"id": "f52b570d-be6f-4fa8-92c4-9146047904da"},
        "type": {"type": "Radar"},
        "name": "Radar"
      }
    ]
  }
}
```

Do not use:

```json
{
  "sensorsInformation": {
    "totalSensorCount": 1,
    "validSensors": [
      {
        "id": {"id": "string"},
        "type": {"type": "string"},
        "name": "string"
      }
    ]
  }
}
```

### API reference: gRPC

- **Must have** — Generate from Protocol Buffers using `protoc-gen-doc`.
- Follow the [Protocol Buffers Style Guide](https://protobuf.dev/programming-guides/style/).
- **Should have** — file-level comment at top of each `.proto` file; group related messages/enums/services; leading comments for context, trailing for brief field notes.
- Comment every message, service, field, and enum. Capitalize first letter; end with period.
- Use Markdown syntax in proto comments. Formulas in comments: valid LaTeX (`$`/`$$`) — invalid = **Must fix**.
- PascalCase for messages/enums/services, `lower_snake_case` for fields.
- Enum zero value suffix: `UNSPECIFIED`. Enum values end with semicolon.
- Prefix enum values with enum name to avoid collisions.
- Prefer top-level enums with prefixed values over nesting inside a message.
- **Should have** — document message purpose, field constraints, enum usage, service workflow, and each RPC's request/response.
- Use `@exclude` in comments to hide them from generated docs.

Proto comment example:

```protobuf
/**
 * Defines the user API for managing accounts and profiles.
 */

// Represents the user's account status.
enum AccountStatus {
    ACCOUNT_STATUS_UNSPECIFIED = 0; // Default value.
    ACCOUNT_STATUS_ACTIVE = 1;     // Account is active.
    ACCOUNT_STATUS_SUSPENDED = 2;  // Account is suspended.
}

// A message that represents a user's profile.
message UserProfile {
   // The unique identifier for the user.
   int32 id = 1;
   // The user's full name.
   string name = 2;
   // The user's email address.
   string email = 3;
}

// Provides operations for managing user accounts.
service UserService {
    // Creates a new user account.
    rpc CreateUser (CreateUserRequest) returns (CreateUserResponse);
    // Retrieves user information by ID.
    rpc GetUser (GetUserRequest) returns (GetUserResponse);
}
```

### API reference: Other APIs

- **Must have** — Clearly define the specific protocol and data formats.
- Document all messages in Markdown.
- **Should have** — Field descriptions including type and whether each field is mandatory.

---

## 7. Writing guidelines: Library/SDK documentation

### Descriptive content

| Section | Priority |
|---------|----------|
| **Introduction** (`index.md`, H1 exactly `# Introduction`) | **Must have** |
| **Changelog** (`changelog.md` or `changelog/changelog.md`) | **Must have** |
| **Getting started** (dependencies, install, dev env, licensing) | **Should have** |
| **User guide** | **Should have** |
| **Usage examples** | **Should have** |
| **Platform overview** (inside Introduction) | **Nice to have** |

Introduction body **Should have** — main features, target audience, language/OS support, library role (client/server/both). Treat a missing platform overview as Nice to fix at most.

### Reference documentation

- Document every function: purpose, parameters, return values, exceptions.
- Document every class: purpose, methods, properties.
- Document all data structures.
- Document class hierarchies and namespaces when applicable.
- Use consistent naming conventions throughout.

### Folder structure

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
│   ├── index.md
│   ├── basic-usage.md
│   ├── advanced-features.md
│   └── troubleshooting.md
├── examples/
│   ├── index.md
│   └── example-N.md
├── api-reference/
│   └── (generated documentation)
├── images/
│   └── (lowercase extensions)
├── toc.yml
└── docfx.json
```

---

## 8. File structure and naming

- **Must have** — One H1 per file (first heading after frontmatter), except REST `description/index.md` and `changelog/changelog.md` (H2-first, no H1).
- File names: lowercase with hyphens. Use `-` not `_` (URL compatibility). Paths become public URLs—keep them short.
- Subdirectory `index.md` files (e.g. `getting-started/index.md`) are **Nice to have**, not required. Do not flag missing subsection `index.md` as Must fix or Should fix.
- **Image and asset folders** (Should have when figures are used):
  - **REST API**: place binary images and diagrams under **`description/images/`** or **`description/assets/`** only — not at package root.
  - **API (prose) / Library/SDK**: place binary images and diagrams under any `images/` or `assets/` directory in the package tree (not loose beside Markdown or `docfx.json`).
  - Image extensions are lowercase. **Should have** — informative images have descriptive alt text; empty alt only for decorative images. **Nice to have** — optional title in quotes after URL.
- When Markdown lacks a construct, inline HTML is permitted.
- `toc.yml`: exactly one per package tree (no nested TOCs). Not required for **REST API-only** packages.
- Code blocks: always specify language for syntax highlighting.
- Encoding: UTF-8 (mandatory).

---

## 9. TOC configuration (`toc.yml`)

```yaml
- name: Doc package name
  href: overview.md
  items:
  - name: Get started
    items:
    - name: Prerequisites
      href: get-started/prerequisites.md
    - name: Install library
      href: get-started/install-library.md
  - name: User guide
    items:
    - name: Overview
      href: user-guide/overview.md
```

- `name`: display name (optional—defaults to file title metadata or first H1). Wrap in double quotes if it contains `::`, `~`, `#`, or `{}`.
- `href`: path to the file (optional for parent-only nodes).
- `items`: child nodes.
- No duplicate `href` values across the TOC.

---

## 10. Changelog format

- Latest version at top with release date.
- Categorize changes as: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**.

---

## 11. Documentation compliance checklist

### Compliance reports

When asked for a compliance check, self-review, or pre-PR verification, write findings to **`documentation-compliance-report.md`** in the package root (next to `docfx.json`) for local review only — **do not commit or push** that file to DevRelDocs:

- Title, ISO date, package path relative to the repo root.
- Summary line: Approved / Needs Minor Revisions / Needs Major Revisions (justified per severity rules below).
- Classification: only the type(s) that apply, with evidence. No "N/A" filler.
- **Issues**: violations only — never tag a passing observation with a severity.
- **Action items**: mirror open Issues only, ordered by severity.
- Each Issue and Action item: tagged with **Must fix**, **Should fix**, or **Nice to fix**, plus an absolute **Reference** link on the sandbox guidelines site (`https://doc-guidelines.sandbox.ansysapis.com/docs/...`) when the finding maps to a tagged guideline rule. **Do not** use `github.com/ansys-internal/developer-documentation-guidelines` URLs in Reference lines.

### Style and writing

- Follows Google developer documentation style guide.
- Sentence case headings and titles.
- Active voice, present tense, short clear sentences.

### Quality assurance

- Passes Markdownlint validation.
- Passes Vale linting (Google style).
- All links functional.
- Images display correctly (lowercase extensions); informative images have alt text (Should have).
- Tested locally with Docfx.
- **Must have** — Each Markdown file starts with an H1 as the first heading and contains exactly one H1, **except** REST API `description/index.md` and `changelog/changelog.md`, which must start with **H2** and contain **no H1**.
- **Must have** — When formulas are used, valid LaTeX per the Markdown rules; invalid delimiters = **Must fix**.

### Structure

- Correct package classification applied (including hybrid surfaces).
- Required root files present per classification (`index.md`, `changelog.md`, `docfx.json`, `toc.yml` for API/Library/SDK; `docfx.json` + spec, `description/index.md`, `changelog/changelog.md` for REST API).
- Logical directory organization.
- REST API packages follow dedicated structure (no root `toc.yml` or `index.md`).

### Metadata

- All required metadata fields populated.
- Taxonomy values validated against YAML sources (typically under `config/portal-metadata/` on the active branch).
- `doc_type` set correctly for REST API and Doxygen packages.
- `programming language` validated when set; omitting it is acceptable for language-agnostic packages.

### Severity tagging (mandatory)

| Guideline tag | Review severity when not met |
|---------------|------------------------------|
| **Must have** | **Must fix** |
| **Should have** | **Should fix** |
| **Nice to have** | **Nice to fix** |

- **Must fix**: blocking issue — PR cannot merge.
- **Should fix**: important but not blocking.
- **Nice to fix**: optional improvement.

### Approval criteria

- **Approved**: no open Must fix items.
- **Needs minor revisions**: no Must fix; some Should fix or Nice to fix.
- **Needs major revisions**: one or more Must fix, or widespread Should-fix issues the reviewer treats as release-blocking.

### Pre-submission checks

- Documentation reviewed locally using Docfx.
- All broken link warnings resolved.
- Documentation tested on sandbox environment.
- Peer review completed.
- Documentation uploaded at least 10 days before release date.
- **Must have** — Package hosted in DevRelDocs (public) or DevRelDocs_internal (internal).
- **Must have** — Explicit sign-off for production migration after sandbox validation.
- **Nice to have** — Issue category labels (Policy, Correctness, Quality) alongside severity in compliance reports.

### Post-migration verification

- Documentation displays correctly in sandbox.
- Navigation works as expected.
- Search functionality works.
- All links work.
- Images render properly.
- Code examples display with correct syntax highlighting.
- Metadata displays correctly in Search result page filters.

---

## 12. Linters

### Markdownlint

Install the Markdownlint extension in VSCode. Errors and warnings appear inline.

### Vale

Install Vale:

```bash
choco install vale
```

Configure Vale:

1. Generate a `.vale.ini` using [Vale's Config Generator](https://vale.sh/generator). Select **Google Developer Documentation Style Guide** as the base style.
2. Run `vale sync` in the directory containing `.vale.ini`.
3. Create vocabulary files at `styles/config/vocabularies/ansys/accept.txt` and `reject.txt` for project-specific terms.
4. Add `Vocab = ansys` to `.vale.ini`.

Run Vale:

```bash
vale .                              # All files in current directory
vale --config=doc/.vale.ini .       # From repo root
vale path/to/directory              # Specific directory
```

### Vale VSCode

Install the Vale VSCode extension for inline feedback.

---

## 13. Docfx

Install:

```bash
dotnet tool update -g docfx
```

Prerequisites: .NET SDK 8.0+. Optional: Node.js v20+ (for PDF generation).

Build and preview:

```bash
docfx docfx.json --serve
```

Open `http://localhost:8080` to view. Resolve all broken link warnings before publishing.

---

## 14. GitHub constraints

- Max 1,000 files per directory.
- Max 1 MB for text files.
- Max 100 MB per image/asset file.
- Files >1 MB: only `raw` or `object` media types.
- Files >100 MB: not supported via API.
