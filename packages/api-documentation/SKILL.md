---
name: api-documentation
description: >-
  Ansys API, library, and SDK documentation guidelines for the Dev portal.
  Covers writing style, package structure, metadata, compliance, and migration.
  Use when creating, reviewing, or migrating API docs, REST APIs, gRPC APIs,
  library docs, SDK docs, OpenAPI specs, or docfx packages.
---

# Ansys API Documentation Guidelines

## 1. Classify the package first

Before applying any rules, classify the documentation package as exactly one type:

| Type | Authoritative reference | Key indicator |
|------|------------------------|---------------|
| **REST API** | OpenAPI/Swagger spec (JSON or YAML) | `openapi` or `swagger` root object in spec file |
| **API (prose)** | Markdown prose | Wire protocol or message-based API documented in Markdown, not OpenAPI |
| **Library/SDK** | Markdown (possibly generated from Doxygen/Sphinx/proto) | Language-specific interface with classes, methods, functions |

Do not combine REST API and Library/SDK in a single migration package.

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

- Use sentence case for all headings and titles.
- Use active voice and present tense.
- Keep sentences short and clear.
- Use consistent terminology throughout. Do not alternate between synonyms.
- Validate with Vale (Google style rules) and Markdownlint.

## 4. Markdown rules

Format: GitHub Flavored Markdown. Encoding: UTF-8.

- File names: lowercase with hyphens (`getting-started.md`, not `Getting_Started.md`).
- Image file extensions: always lowercase (`.png`, `.jpg`).
- Code blocks: always specify language for syntax highlighting.
- Ordered lists with embedded code or images: indent by 4 spaces with a blank line above.
- Block formulas: `$$...$$`. Inline formulas: `$...$` (LaTeX syntax).
- Links opening in new tabs: use `<a target="_blank" href="...">`.
- Collapsible sections: use `<details>` and `<summary>` tags.
- Tables with merged cells or bulleted lists in cells: use HTML.
- Hidden comments: `<!-- comment -->`.

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

`product`, `status` (`published`/`unpublished`), `access control`, `programming language`, `author`, `author email`, `description` (file-level only, for SEO), `date` (ISO-8601), `keywords`, `audience`, `context`.

## 6. API reference quality

### REST APIs

- OpenAPI spec must validate in Swagger Editor without errors.
- `info.description`: one-sentence summary.
- Group endpoints by category using `tags`.
- Each endpoint needs: `summary` (sentence case, no trailing period), `description`, `parameters`, `responses`, and working examples.
- Request/response examples must use realistic, specific values. Never use generic `"string"` placeholders.

### gRPC APIs

- Generate docs from proto files using `protoc-gen-doc`.
- Follow the [Protocol Buffers Style Guide](https://protobuf.dev/programming-guides/style/).
- Comment every message, service, field, and enum value.
- PascalCase for messages/enums/services; `lower_snake_case` for fields.
- Enum zero value: suffix with `UNSPECIFIED`.
- Prefix enum values with the enum name to avoid collisions.
- Use Markdown syntax in proto comments.

### Other APIs

- Document all messages in Markdown.
- Define message formats, field types, and whether fields are mandatory.

## 7. Library/SDK documentation

Required sections in descriptive content:

1. **Introduction** (`index.md`): purpose, features, platform overview with diagram.
2. **Getting started**: dependencies, installation, dev environment config, licensing.
3. **User guide**: how to use the library/SDK.
4. **Usage examples**: comprehensive code examples, common use cases.
5. **Changelog** (`changelog.md`): latest version at top, categorized as Added/Changed/Deprecated/Removed/Fixed.

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

### REST API-only packages

```
Documentation-package/
├── docfx.json
├── openapi.yaml
├── description/
│   └── index.md
└── changelog/
    └── changelog.md
```

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

- `name`: display name. Wrap in double quotes if it contains `::` or `~`.
- `href`: path to the file. Optional for parent-only nodes.
- `items`: child nodes.
- No duplicate `href` values across the TOC.
- Exactly one `toc.yml` per package tree.

## 10. Changelog format

- Latest version at top with release date.
- Categorize: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**.

## 11. Migration overview

Migration to the Dev portal follows 5 steps:

1. **Classify** the package type and confirm required files (see section 2).
2. **Prepare** documentation in Markdown (convert from source format if needed).
3. **Submit** a PR to the appropriate GitHub repo:
   - **DevRelDocs** for public documentation
   - **DevRelDocs_internal** for internal documentation
4. **Review** in the sandbox environment (preview link provided by the Dev portal team).
5. **Approve** final migration to production.

Upload documentation at least 3-4 days (ideally 10 days) before release date.

For detailed migration workflows and format conversion instructions, read [migration-reference.md](migration-reference.md).

## 12. Compliance checklist (summary)

Before submitting a PR, verify:

- Markdownlint passes.
- Vale passes (Google style rules).
- All links are functional.
- Images render with lowercase extensions.
- Docfx builds clean locally.
- Required metadata fields are populated.
- Taxonomy values validated against YAML sources (`physics.yml`, `product.yml`).
- Package structure matches the classified type.

### Review severity

- **Must fix**: blocking — PR cannot merge.
- **Should fix**: important but not blocking.
- **Nice to fix**: optional improvement.

Approval: no open "Must fix" items = approved.

## 13. PR process

- Submit PRs to **DevRelDocs** (public) or **DevRelDocs_internal** (internal).
- Melanie approves all PRs.
- PR title: clear identification of package and scope.
- PR description: summarize changed docs and target audience.
- Include validation notes (linting results, local rendering, link checks).

## Full references

- For complete writing guidelines, metadata details, and compliance checklist: read [api-guidelines-reference.md](api-guidelines-reference.md).
- For migration workflows and format conversion details: read [migration-reference.md](migration-reference.md).
