# XML Structure Reference — Ansys Documentation (DITA & DocBook)

Full reference for XML structure, tagging, and document organization. Read SKILL.md first for the essentials. Use this file when you need detailed tagging rules, element reference, or document structure guidelines.

---

## 1. Document structure principles

- Provide only information users need. Do not describe UI elements with obvious properties.
- Organize information from known to unknown, general to specific.
- Have a topic sentence in each paragraph; remainder supports that idea.
- Clear referents for pronouns.
- State the organizing principle underlying the manual structure.
- Avoid ending steps with "a dialog box opens." Set context in the next step.

---

## 2. Types of manuals

| Type | Purpose |
|------|---------|
| Command Reference | Complete dictionary of command descriptions, alphabetical |
| Installation Guide / Licensing Guide | Install, configure, license the product |
| Getting Started | Introduce basic features, short tutorial |
| Tutorial Guide | Step-by-step tutorials for realistic tasks |
| User's Guide | Instructions for all standard features |
| Theory Guide | Mathematical equations and modeling theory |
| Release Notes | New features, solution changes, setting changes |
| Known Issues and Limitations | Known problems in current release |
| Best Practices Guide | Guidelines and verified test cases |
| Scripting Guide | Recording and automating actions |

---

## 3. Recommended chapter structure

1. **Introduction** — purpose, scope, overview of the chapter.
2. **Concepts** — background theory or concepts the user needs.
3. **Tasks** — step-by-step procedures.
4. **Reference** — detailed specifications, command descriptions, tables.
5. **Examples** — worked examples demonstrating concepts/tasks.

---

## 4. Screenshots and graphics

- Only include when absolutely necessary for comprehension.
- Do not include screenshots showing obvious or redundant information.
- Ensure screenshots are current (correct version, current defaults, current UI).
- Resolution: 96 DPI for the Help Viewer.
- Use IrfanView to confirm resolution.
- Meaning must be conveyed using methods other than color alone.
- Line drawings: save as .png in Inkscape.

---

## 5. DocBook XML tagging

### Sections

- `<section>` creates a numbered section with a `<title>`.
- A section with child sections must place all block content before the first child section (DTD constraint).
- Use `<bridgehead>` for informal sub-headings that don't create a new section. Always give it an `id`. Do not use `renderas`.

```xml
<bridgehead id="some_unique_id">My Heading</bridgehead>
```

### Content order in sections (DTD constraint)

Block-level content (`<para>`, `<note>`, `<important>`, `<itemizedlist>`, `<informaltable>`, etc.) must come before any child `<section>` elements. This applies to `<section>`, `<chapter>`, and all sectioning elements.

```xml
<!-- CORRECT -->
<section id="parent">
    <title>Parent</title>
    <para>Intro.</para>
    <note><para>Valid here.</para></note>
    <section><title>Sub A</title>...</section>
</section>

<!-- WRONG — note after child section -->
<section id="parent">
    <title>Parent</title>
    <section><title>Sub A</title>...</section>
    <note><para>Invalid here.</para></note>
</section>
```

### Cross-references

| Element | Use |
|---------|-----|
| `<xref>` | Internal links (auto-generates text from target title) |
| `<olink>` | Cross-book links |
| `<ulink>` | External URLs |
| `<link>` | Internal link with manual text (only when target has no title) |

- Prefer auto-generated link text over manual text.
- Never use "click here" as link text.

```xml
<!-- Correct -->
See the <ulink url="https://example.com/install">Installation Guide</ulink>.

<!-- Wrong -->
<ulink url="https://example.com/install">Click here</ulink>
```

### Lists

- `<orderedlist>` when sequence matters.
- `<itemizedlist>` when sequence does not matter.
- `<variablelist>` for term/definition pairs.

### Tables

- Use `<informaltable>` for tables without titles.
- Use `<table>` for formal tables with titles.
- Column widths: use `colwidth` attribute on `<colspec>`.

### Admonitions (special notices)

| Element | Use |
|---------|-----|
| `<note>` | General supplementary information |
| `<tip>` | Helpful hints |
| `<important>` | Key information that must not be missed |
| `<caution>` | Potential for data loss or minor damage |
| `<warning>` | Potential for injury or major damage |

### UI element tags

| UI element | Tag |
|-----------|-----|
| Menu | `<guimenu>` |
| Submenu | `<guisubmenu>` |
| Menu item | `<guimenuitem>` |
| Button | `<guibutton>` |
| Label (check box, option button, field) | `<guilabel>` |
| Key | `<keycap>` |
| Key combination | `<keycombo><keycap>Ctrl</keycap><keycap>S</keycap></keycombo>` |
| User input | `<userinput>` |
| File/path | `<filename>` |
| Command | `<command>` |
| Replaceable variable | `<replaceable>` |
| Literal text | `<literal>` |
| Emphasis | `<emphasis>` |
| Email | `<email>` |

### Menu paths

```xml
<guimenu>File</guimenu> > <guisubmenu>Import</guisubmenu>
 > <guimenuitem>Import surface or line data</guimenuitem>
```

### Images

```xml
<mediaobject>
  <imageobject>
    <imagedata fileref="graphics/mesh_settings.png"/>
  </imageobject>
  <textobject>
    <phrase>Mesh Settings dialog box showing element size and method options</phrase>
  </textobject>
</mediaobject>
```

For inline images, use `<inlinemediaobject>`.

### Emphasis techniques

| Purpose | Tag |
|---------|-----|
| Italic emphasis | `<emphasis>` |
| Bold emphasis | `<emphasis role="bold">` |
| First use of a term | `<firstterm>` |

### Revision flags

Use revision flags to highlight changes for review in QA builds. Apply the `revisionflag` attribute to elements that have changed.

### Footnotes

```xml
<footnote><para>Footnote text here.</para></footnote>
```

### Bibliographies

Use `<bibliography>`, `<biblioentry>`, and related elements for reference lists.

---

## 6. DITA-specific tagging

### Topic types

| Type | Use |
|------|-----|
| `<task>` | Step-by-step procedures |
| `<concept>` | Background information, explanations |
| `<reference>` | Factual information (commands, API, parameters) |
| `<topic>` | Generic (when no specialized type fits) |

### Task topic structure

```xml
<task id="task_id">
  <title>Task Title</title>
  <shortdesc>Brief description.</shortdesc>
  <taskbody>
    <prereq>Prerequisites here.</prereq>
    <context>Context information.</context>
    <steps>
      <step><cmd>Do this first thing.</cmd></step>
      <step><cmd>Do this second thing.</cmd>
        <stepresult>Expected result.</stepresult>
      </step>
    </steps>
    <result>Overall result.</result>
    <postreq>Follow-up actions.</postreq>
  </taskbody>
</task>
```

### Section constraints

- `<section>` elements cannot nest. Use separate `<section>` siblings within `<body>`.
- A `<section>` cannot follow a child `<example>`.
- Check the DITA language spec for element placement constraints.

### Inline elements

| UI element | Tag |
|-----------|-----|
| Menu | `<uicontrol>` |
| Menu cascade | `<menucascade><uicontrol>File</uicontrol><uicontrol>Save</uicontrol></menucascade>` |
| Keyboard shortcut | `<shortcut><keycombo><uicontrol>Ctrl</uicontrol><uicontrol>S</uicontrol></keycombo></shortcut>` |
| User input | `<userinput>` |
| File/path | `<filepath>` |
| Code/command | `<cmdname>` or `<codeblock>` |
| Variable | `<varname>` |
| System output | `<systemoutput>` |
| Wintitle | `<wintitle>` |

### Images in DITA

```xml
<fig>
  <title>Mesh Settings</title>
  <image href="graphics/mesh_settings.png">
    <alt>Mesh Settings dialog box showing element size and method options</alt>
  </image>
</fig>
```

### Lists in DITA

- `<ol>` for ordered lists.
- `<ul>` for unordered lists.
- `<dl>` for definition lists.

### Admonitions in DITA

```xml
<note>General information.</note>
<note type="tip">Helpful hint.</note>
<note type="important">Key information.</note>
<note type="caution">Potential for data loss.</note>
<note type="warning">Potential for injury.</note>
```

### Cross-references in DITA

```xml
<!-- Internal -->
<xref href="topic_id.dita"/>

<!-- External -->
<xref href="https://example.com/install" scope="external" format="html">
  Installation Guide
</xref>
```

### Bookmaps and maps

- **Bookmap:** organizes topics into book structure (chapters, appendixes, glossary).
- **Map:** flat or hierarchical topic collection.
- Use `<topicref>` to reference topics from maps.
- Use `<chapter>`, `<appendix>`, `<glossarylist>` in bookmaps.

### Content reuse

- **Reusable topics:** reference the same topic file from multiple maps.
- **Conref:** reuse elements by reference (`conref="shared/common.dita#topic/element_id"`).
- **Variables:** use `<keyword>` with `keyref` for variable text.

### Conditional processing

Use `@product`, `@platform`, `@audience`, or `@otherprops` attributes to filter content during publication.

---

## 7. Entity references

Product and company names must use XML entity references from `global/terms_global.ent`. Never hardcode.

How to find the right entity:

1. Check `global/terms_global.ent` for the product name.
2. Search existing files in the same guide for usage patterns.
3. Check `<!ENTITY>` declarations in the file's DOCTYPE header for local entities.

Use entities everywhere, including inside `<guilabel>` elements:

```xml
<guilabel>&pn257g; workflow definition file (*.wdf)</guilabel>
<para>Export the current project to an &pn257g; workflow definition file.</para>
```

---

## 8. Commonly used DITA and DocBook tags compared

| Purpose | DITA | DocBook |
|---------|------|---------|
| Paragraph | `<p>` | `<para>` |
| Ordered list | `<ol>` | `<orderedlist>` |
| Unordered list | `<ul>` | `<itemizedlist>` |
| List item | `<li>` | `<listitem>` |
| Definition list | `<dl>` | `<variablelist>` |
| Table | `<table>` | `<table>` or `<informaltable>` |
| Image | `<image>` | `<mediaobject>` / `<imagedata>` |
| Figure | `<fig>` | `<figure>` |
| Note | `<note>` | `<note>` |
| Bold | `<b>` | `<emphasis role="bold">` |
| Italic | `<i>` | `<emphasis>` |
| Code block | `<codeblock>` | `<programlisting>` |
| Inline code | `<codeph>` | `<code>` |
| UI control | `<uicontrol>` | `<guibutton>`, `<guilabel>`, `<guimenu>` |
| File path | `<filepath>` | `<filename>` |
| Cross-reference | `<xref>` | `<xref>`, `<olink>` |
| External link | `<xref scope="external">` | `<ulink>` |
| User input | `<userinput>` | `<userinput>` |
| Section | `<section>` (no nesting) | `<section>` (can nest) |
| Superscript | `<sup>` | `<superscript>` |
| Subscript | `<sub>` | `<subscript>` |
