# Ansys API Documentation Guidelines — Full Reference

This is the detailed reference for Ansys API, library, and SDK documentation. Read SKILL.md first for the essentials. Use this file when you need full details on writing guidelines, metadata configuration, or the compliance checklist.

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

Format: GitHub Flavored Markdown (GFM). Encoding: UTF-8.

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

Do not combine REST API and Library/SDK in a single migration package.

---

## 5. Metadata configuration

### Required metadata (`docfx.json` → `build.globalMetadata`)

All keys must be lowercase.

| Field | Description |
|-------|-------------|
| `title` | Documentation title + version (e.g. "DPF C++ client library 2026 R1") |
| `version` | Format: `YYYY R1\|R2 [SP01-SP04]` |
| `summary` | Brief description of the documentation (not the product) |
| `physics` | Product collection category (see `physics.yml`) |

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
| `product` | Product category (recommended, becoming mandatory) |
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

The primary descriptive file must include:

1. **Introduction**
   - Capabilities and features.
   - Protocol definition.
   - Testing environment info.

2. **Platform overview**
   - Explanatory diagram (API relationships).
   - Application development description.
   - Communication flow explanation.

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

### File naming

- **API (prose)**: landing page = `index.md`; changelog = `changelog.md`.
- **REST API-only**: `description/index.md` + `changelog/changelog.md`.

### API reference: REST

- OpenAPI Specification (JSON or YAML).
- Brief one-sentence description in `info.description`.
- Group endpoints by category using `tags`.
- Each endpoint needs: summary (sentence case, no period), description, parameters, responses, working examples.

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

- Generate from Protocol Buffers using `protoc-gen-doc`.
- Follow the [Protocol Buffers Style Guide](https://protobuf.dev/programming-guides/style/).
- File-level comment at top of each `.proto` file.
- Comment every message, service, field, and enum.
- Use Markdown syntax in proto comments.
- PascalCase for messages/enums/services, `lower_snake_case` for fields.
- Enum zero value suffix: `UNSPECIFIED`.
- Prefix enum values with enum name to avoid collisions.
- Prefer top-level enums with prefixed values over nesting inside a message.
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

- Document all messages in Markdown.
- Define message formats, field types, and whether fields are mandatory.

---

## 7. Writing guidelines: Library/SDK documentation

### Descriptive content

Required sections:

1. **Introduction** (`index.md`): high-level explanation + main features. Platform overview with diagram, context, integration explanation.
2. **Getting started**: dependencies, system requirements, step-by-step installation, dev environment config, licensing.
3. **User guide**: how to use the library/SDK.
4. **Usage examples**: comprehensive code examples, common use cases.
5. **Changelog** (`changelog.md`): latest version at top with release date. Categorize: Added, Changed, Deprecated, Removed, Fixed.

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

- File names: lowercase with hyphens. Use `-` not `_` (URL compatibility).
- Each subdirectory: include its own `index.md`.
- Images: dedicated `images/` directory, lowercase extensions.
- `toc.yml`: exactly one per package tree (no nested TOCs).
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

- `name`: display name. Wrap in double quotes if it contains `::` or `~`.
- `href`: path to the file (optional for parent-only nodes).
- `items`: child nodes.
- No duplicate `href` values across the TOC.

---

## 10. Changelog format

- Latest version at top with release date.
- Categorize changes as: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**.

---

## 11. Documentation compliance checklist

### Style and writing

- Follows Google developer documentation style guide.
- Sentence case headings and titles.
- Active voice, present tense, short clear sentences.

### Quality assurance

- Passes Markdownlint validation.
- Passes Vale linting (Google style).
- All links functional.
- Images display correctly (lowercase extensions).
- Tested locally with Docfx.

### Structure

- Correct package classification applied.
- Required root files present (`index.md`, `changelog.md`, `docfx.json`, `toc.yml` as applicable).
- Logical directory organization.
- REST API packages follow dedicated structure.

### Metadata

- All required metadata fields populated.
- Taxonomy values validated against YAML sources.
- `doc_type` set correctly for REST API and Doxygen packages.

### Review severity labels

- **Must fix**: blocking issues — PR cannot merge.
- **Should fix**: important but not blocking.
- **Nice to fix**: optional improvements.

### Approval criteria

- **Approved**: no open Must fix items.
- **Needs minor revisions**: no Must fix; some Should fix or Nice to fix.
- **Needs major revisions**: one or more Must fix items.

### Pre-submission checks

- Documentation reviewed locally using Docfx.
- All broken link warnings resolved.
- Documentation tested on sandbox environment.
- Peer review completed.
- Documentation uploaded at least 10 days before release date.

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
