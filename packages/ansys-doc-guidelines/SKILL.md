---
name: ansys-doc-guidelines
description: >-
  Ansys corporate documentation style, structure, and XML formatting rules for
  DITA and DocBook content. Covers writing style, terminology, punctuation,
  capitalization, XML tagging, entity references, cross-references, images,
  lists, procedures, and document structure. Use when writing, editing, or
  reviewing Ansys product documentation in DITA or DocBook format.
---

# Ansys Documentation Guidelines

These are the corporate documentation guidelines for Ansys product documentation authored in DITA and DocBook XML. All rules apply to both formats unless stated otherwise.

## 1. Voice, tense, and person

- Use active voice. Passive voice is wordy and ambiguous.
- Use present tense. Not: "you will be prompted." Use: "Fluent prompts you."
- Address the reader as "you", not "the user."
- Use imperative mood for instructions: "Select the path" not "you should select."

## 2. Brevity and clarity

- Make your point in as few words as possible.
- Use simple terms — many readers speak English as a second language.
- Avoid roundabout constructions: "There are three features in these figures" -> "These figures show three features."
- Avoid jargon and idioms: "rule of thumb" -> "guideline"; "keep in mind" -> "note" or omit; "let's say" -> "for example."
- Use American English spelling.

## 3. Consistency

- Use consistent terminology throughout. Do not alternate between synonyms (e.g. "mesh" vs. "grid").
- Use consistent typography for UI elements: the **Help** menu is always tagged consistently, never "Help Menu" or help Menu.
- Use consistent writing style and tone throughout a document.

## 4. Parallelism

- Headings at the same level: use the same part of speech.
- List items: begin each with the same part of speech (e.g. imperative verbs).
- Series: use parallel structure ("ambitious, self-motivated, and dedicated").

## 5. Terminology — key substitutions

| Instead of | Use |
|-----------|-----|
| abort | stop, end, terminate, close |
| activate | select |
| click on | click |
| crash | terminate abnormally |
| desire | want, require, need |
| e.g. | for example |
| enable (for UI) | select |
| enter (text) | type |
| et cetera / etc. | and so on |
| execute (a program) | run |
| GUI | the product name |
| hit (keyboard) | press |
| i.e. | that is |
| input (verb) | type |
| pane | dialog box |
| please | (omit) |
| pull-down menu | drop-down list |
| radio button | option button |
| text user interface / TUI | command line |
| user interface | the product name |
| utilize | use |
| wish | want, need, require |

## 6. UI element action verbs

| Element | Action verb |
|---------|------------|
| button | click (not "click on") |
| check box | select / clear (not "check/uncheck" or "enable/disable") |
| option button | select (not "toggle") |
| drop-down list | select from |
| tree item | expand / collapse |
| text field | type in |
| keyboard key | press |

## 7. Punctuation

- **Serial comma:** always use. "thermal, structural, and FLOTRAN CFD analyses."
- **Contractions:** avoid in formal docs. Watch "it's" vs. "its."
- **Latin:** do not use e.g., i.e., etc. Write them out.
- **Colons:** only after a complete sentence.
- **Semicolons:** between independent clauses not joined by a conjunction.
- **Em dash:** no spaces around it. Use sparingly for emphasis or abrupt change.
- **En dash:** for ranges (pages 209–225) and negative numbers.
- **Hyphens:** compound adjectives before nouns ("first-level topic") but not after ("the topic is first level"). No hyphen after "ly" adverbs.
- **Ellipses:** when they appear in UI labels, omit them in the documentation text.
- **Periods in lists:** if any item is a complete sentence, end all items with periods. If none are, use no periods.
- **Quotation marks:** use sparingly. Prefer XML formatting tags.
- **Slashes:** avoid. Use hyphens or words. Slashes cause localization problems.

## 8. Capitalization

- **Title caps** for figure/table titles, column headings, book titles, product names, chapter/section titles.
  - Do not capitalize articles, coordinate conjunctions, "to" in infinitives, or prepositions with 5 or fewer letters.
- **Full uppercase** for environment variables, file extensions when referring to file types (e.g. "DB files"), acronyms.
- Never start a sentence with a case-sensitive lowercase word. Rephrase: "printf is..." -> "The printf function is..."

## 9. Abbreviations and acronyms

- First use: spell out with abbreviation in parentheses: "ANSYS Parametric Design Language (APDL)."
- Plurals: add "s" without apostrophe: IDs, CPUs, DOFs.

## 10. Numbers and equations

- Exponential notation in prose: use superscripts (10² not 10^2). In DITA: `10<sup>2</sup>`. In DocBook: `10<superscript>2</superscript>`.
- User input: use the notation the software accepts (e.g. 30E6).
- Never use "billion" — use scientific notation to avoid regional ambiguity.
- Inline equations: use a slash for division (m=E/c²). Formal equations: use stacked fractions.
- Introduce variables with lowercase "where". If more than two variables, use a table.

## 11. XML file headers

- Never modify the XML declaration, DOCTYPE, or root element attributes on existing files.
- New files: copy the full header block from an existing file of the same type in the same directory. Change only the `id` attribute.

## 12. Formatting — match existing files

When adding content to an existing file, match:

- Indentation (tabs vs. spaces, nesting depth)
- Attribute ordering and quoting style
- Whitespace around elements
- Comment style and placement
- Line wrapping conventions

## 13. Entity references for product names

Never hardcode product or company names in prose. Use the XML entity references from `global/terms_global.ent`:

| Entity | Resolves to | Use for |
|--------|-------------|---------|
| `&pn257g;` | optiSLang | optiSLang product name |
| `&ansysCompany;` | Ansys | Company name |
| `&pn239g;` | Sherlock | Sherlock product name |
| `&pn237g;` | Minerva | Minerva product name |

Use entities everywhere, including inside `<guilabel>` elements. Check `global/terms_global.ent` for the full list.

## 14. Deprecated content

Never delete, remove, or omit content marked as deprecated. Deprecated sections, elements, parameters, methods, and notes must be preserved exactly as they are.

## 15. Images and alt text

- Only include screenshots when absolutely necessary for comprehension.
- Images should be 96 DPI for the Help Viewer.
- Every image must have alt text for accessibility.

**DITA:**
```xml
<image href="graphics/mesh_settings.png">
  <alt>Mesh Settings dialog box showing element size and method options</alt>
</image>
```

**DocBook:**
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

Alt text guidelines:

- Describe the content or purpose, not the appearance.
- For UI screenshots: name the dialog box or panel and key visible settings.
- Decorative images: empty alt (`<alt/>` in DITA, `<phrase/>` in DocBook).
- If inside a `<figure>` or `<fig>` with a `<title>`, the alt text must add detail beyond the title.
- Keep under ~150 characters.

## 16. Cross-references and links

- Use `<xref>` (DITA) or `<xref>`/`<olink>` (DocBook) for internal links — auto-generates text from the target's title.
- Use `<ulink>` (DocBook) for external URLs.
- **Never use "click here" or "here" as link text.** Link text must be descriptive.
- Prefer auto-generated link text over manual text (titles change over time).

## 17. Lists and procedures

- Ordered lists: when sequence matters. Unordered: when it does not.
- All items must begin with the same part of speech.
- Avoid single-step procedures. Split into two steps, combine with an adjacent procedure, or make it a sentence.
- Begin each step with the desired state, then give the command.
- State prerequisites before the procedure, not within steps.
- Separate step results from step actions. Do not state obvious results ("A screen appears.").

## 18. DITA-specific rules

- `<section>` elements cannot nest. Use separate `<section>` siblings within `<body>`, or split into separate topics.
- A `<section>` cannot follow a child `<example>` or appear after the body's closing structural elements.
- DITA topic types: task, concept, reference. Use the correct type for the content.
- Task topics: use `<steps>`, `<prereq>`, `<context>`, `<result>`, `<postreq>`.

## 19. DocBook-specific rules

- Use `<bridgehead>` for informal sub-headings that do not create a new `<section>`.
- Do not use the `renderas` attribute on `<bridgehead>`. Give it a unique `id`.
- A `<section>` containing child `<section>` elements must place all block content (`<para>`, `<note>`, `<important>`, `<itemizedlist>`, `<informaltable>`, etc.) before the first child `<section>`. The DTD forbids block elements after child sections.
- The same rule applies to `<chapter>` and any other sectioning element.

```xml
<!-- CORRECT -->
<section id="parent">
    <title>Parent</title>
    <para>Intro text.</para>
    <note><para>This is valid here.</para></note>
    <section><title>Sub A</title>...</section>
    <section><title>Sub B</title>...</section>
</section>
```

## 20. Section headings

- Title caps for all section and chapter titles.
- Task-oriented sections: use verb-based titles ("Configuring the Mesh", not "Mesh Configuration").
- Headings at the same level must use the same part of speech (parallelism).

## Full references

- For the complete terminology table, indexing guidelines, equation/unit formatting, and graphic guidelines: read [writing-style-reference.md](writing-style-reference.md).
- For DocBook XML tagging details, DITA element reference, and document structure guidelines: read [xml-structure-reference.md](xml-structure-reference.md).
