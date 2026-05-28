# Writing Style Reference — Ansys Documentation

Full reference for writing style, terminology, and punctuation. Read SKILL.md first for the essentials. Use this file when you need the complete terminology table, detailed punctuation rules, indexing guidelines, or equation/unit formatting.

---

## 1. Complete terminology table

| Term | Rule | Notes |
|------|------|-------|
| & (ampersand) | Only in proper names/abbreviations | Use "and" instead |
| 1D, 2D, 3D | No hyphen | |
| abort | Do not use | Use stop, end, terminate, close |
| activate | Do not use for UI switching | Use "select" |
| argument | A modifier for a command | |
| back up (verb) | Two words | |
| backup (noun/adj) | One word | |
| BC | Do not abbreviate | Write "boundary condition" in full |
| biaxial, bilinear | One word, no hyphen | |
| billion | Do not use | Use scientific notation |
| (blank) | Use parentheses around "blank" | Not `<blank>` |
| Boolean | Capitalize | |
| button | Use "click" (not "click on") | Tag with `<guibutton>` |
| cannot | One word | Not "can not" |
| Cartesian | Capitalize | |
| check box | Two words | Use "select" / "clear" |
| click | Not "click on" | |
| comprises | Consider using "has" instead | "Is comprised of" is historically incorrect |
| crash | Do not use | Use "terminate abnormally" |
| cross-section | Hyphenated | |
| data | Singular and plural | |
| database | One word | |
| defect | Do not use | Use "bug" |
| delete | Use for permanent removal | Not "remove" |
| deselect | Use as verb/adj | Not "unselect" as verb |
| desire | Do not use | Use want, require, need |
| dialog box | Temporary separate window | Refer by name in top bar |
| DOF | Acceptable, but consider writing out | |
| double-click | Hyphenated | |
| download | One word | |
| drop-down list | Use instead of "pull-down menu" | |
| e.g. | Do not use | Use "for example" |
| electromagnetic | One word | |
| email | One word | Use `<email>` tag |
| enable | Do not use for UI items | Use "select" |
| enter | Do not use for typing | Use "type" |
| et al. | Only in literary references | Use "and others" elsewhere |
| etc. | Do not use | Use "and so on" |
| execute | Not for running programs | "Run the program. Execute the command." |
| exit | Only as command name | Use "quit" as verb |
| expand / collapse | For tree items | |
| field | Area where user can type | |
| filename, filepath | One word each | Use `<filename>` tag |
| GUI | Do not use | Use product name |
| hard copy | Two words | |
| hit | Do not use for keyboard | Use "press" |
| i.e. | Do not use | Use "that is" |
| in-phase, in-plane | Hyphenated | |
| input | Do not use as verb | Use "type" |
| isosurface | One word | |
| k-epsilon | Hyphenated, no caps | |
| left-click | Generally just say "click" | |
| load step | Two words as noun | |
| menu bar | Do not capitalize | |
| middle-click | Hyphenated | |
| modeled, modeler, modeling | One "l" | |
| non-adiabatic | Hyphenated | |
| nonlinear, nonzero | One word | |
| online | One word | |
| option button | Use instead of "radio button" | |
| out-of-phase, out-of-plane | Hyphenated | |
| pane | Do not use | Use "dialog box" |
| panel | Section within a dialog box | Not the entire dialog |
| parameter | Do not use for command positions | Use "argument" |
| pathname | One word | |
| please | Do not use | |
| postprocessing, preprocessing | One word | |
| press | Only for keyboard keys | |
| principal / principle | Principal = chief/amount; principle = truth | |
| printout | One word | |
| pull-down menu | Do not use | Use "drop-down list" |
| quit | Use as verb | |
| radio button | Do not use | Use "option button" |
| remove | Not for permanent deletion | Use "delete" for permanent |
| Reynolds stress model | Capitalize "Reynolds", no apostrophe, no RSM abbreviation | |
| right-click | Hyphenated | |
| run time | Two words as noun | |
| select | For choosing options | Opposite: "cleared" |
| set up (verb) | Two words | |
| setup (noun/adj) | One word | |
| shared-memory | Hyphenated | |
| stand-alone | Hyphenated | |
| steady-state | Hyphenated | |
| submenu | Use menu item names instead | `File > Import > Import surface or line data` |
| submodeling, superelement | One word | |
| surface-to-surface | Do not use S2S | |
| tab | UI element, not a verb | User works "in a tab" |
| temperature-dependent | Hyphenated | |
| terminate | Use "terminate abnormally" for crashes | |
| text user interface / TUI | Do not use | Use "command line" |
| that vs. which | "that" = essential clause; "which" = nonessential (after comma) | |
| third-party | Hyphenated as adjective | |
| time-step (adj), timestep (noun) | Follow UI usage | |
| toggle button | Do not use | Use "option button" |
| toolbar, toolbox | One word | |
| type | Use as verb instead of "enter" or "input" | |
| under-relaxation | Hyphenated | |
| unselect | Only as adjective ("unselected") | Use "deselect" as verb |
| user-defined function | Hyphenated | UDF after first definition |
| user interface | Do not use | Use product name |
| utilize | Do not use | Use "use" |
| von Mises | Lowercase "von", capitalize "Mises" | |
| want | For user choices | |
| wavefront | One word | |
| wish | Do not use | Use want, need, require |
| workspace | Obsolete Workbench term | Use "tab" since R15.0 |
| X/Y/Z direction, X/Y/Z axis | No hyphen | Capitalize letter only for global coordinate system |
| zero-thickness | Hyphenated | |

---

## 2. Punctuation — detailed rules

### Apostrophes

- Add only the apostrophe (no "s") when the resultant form would be hard to pronounce.
- Joint ownership: add 's only to the last noun ("Production and Product Packaging's database").
- Do not use apostrophes with personal pronouns or to form plurals of figures, letters, or acronyms.

### Brackets

- Square brackets for commands mentioned parenthetically: "Select the nodes [NSEL]."
- Square brackets for optional command-line entries.
- Do not use square brackets as substitute for parentheses.
- Avoid angle brackets for variables in text. Use the `<replaceable>` tag.

### Commas — detailed

- Serial comma: always before the last item in a series of three or more.
- Before final conjunction joining independent clauses.
- To set off parenthetical elements.
- "However", "moreover", "furthermore" within a clause: set off by commas.
- "However", "moreover", "furthermore" beginning a new clause: semicolon before, comma after.
- Do not use comma after an introductory phrase that immediately precedes the verb it modifies.
- Enclose nonrestrictive modifiers by commas.

### Dashes — detailed

- **Em dash (—):** no spaces. Use for emphasis, abrupt change, or setting off explanatory material. Informal mark — use sparingly.
- **En dash (–):** for ranges (pages 209–225) and negative numbers (–30°C). No spaces.
- **Hyphens:** compound adjectives before nouns ("first-level topic"). Do not hyphenate after "ly" adverbs. Do not hyphenate most prefixes (ante, anti, bi, co, de, inter, non, pre, re, semi, sub, un, etc.) unless the combined word has a different meaning (re-solve vs. resolve).

### Spaces

- One space after punctuation and at end of sentences.
- No trailing spaces in titles (they persist in cross-references).

---

## 3. Writing for translation

- Simple, short sentences. Define special terms in a glossary.
- Use lists and tables instead of dense paragraphs.
- Always include articles (a, an, the). Do not omit for conciseness.
- Verify that documentation text matches UI strings exactly.
- Watch for words that can be multiple parts of speech. Clarify with rephrasing.

---

## 4. Exceptions to Microsoft Manual of Style

| Microsoft says | Ansys says |
|---------------|------------|
| Do not use "chapter" | Use "chapter" when the containing element is a chapter |
| Use "shortcut menu" | Use "context menu" |
| Do not use "cut" as verb | Cut, copy, delete are acceptable |
| Use "root directory" | Use "home directory" for UNIX home dirs |
| Sentence-case headings | Use title-case capitalization |
| Mark single-step procedures with bullet | Avoid single-step procedures entirely |
| "Billion" is acceptable | Do not use "billion" — use scientific notation |

---

## 5. Indexing guidelines

- Use `<indexterm>` with `<primary>`, `<secondary>`, `<tertiary>`.
- When an entry would have more than three locators, subdivide.
- Lowercase for index entries unless proper name.
- Generally use plural form for initial noun in `<primary>`.
- Index only nouns (plus common operations like "printing").
- Do not place index tags in title tags.
- Do not punctuate index entries (no quotation marks).
- Structure: noun as primary, verb as secondary.

```xml
<!-- Correct -->
<indexterm>
  <primary>loads</primary>
  <secondary>applying</secondary>
</indexterm>
```

---

## 6. Equations and units

### Spacing

- Space between a number and its unit. Use non-breaking space (`&nbsp;`) in DocBook/DITA.
- No space between a letter and subscript/superscript.
- No space between temperature value, degree symbol, and scale: 22°C coded as `22&deg;C`.

### Symbols

- Scientific notation: use cross symbol for multiplication (5×10⁶).
- Product of units: raised dot (N·m).
- Division: solidus (m/s) or exponent (m s⁻¹).
- Non-breaking space between units: `m&nbsp;s⁻¹`.

### Font conventions

- Unit symbols: upright font.
- Variables: italics (except when variable is an English word).
- Vectors: bold upright.
- Common functions (sin, cos): lowercase upright.
- Gradient/divergence/curl/laplacian: uppercase delta, not italicized.

### Equation formatting

- Multiple equality signs can be on one line if they don't break over a line in PDF.
- Long equations: break before the equal sign or operating symbol.
- Introduce variables with lowercase "where". One variable: no colon. Multiple: use a table with colon.
- Inline equations: use slash for division. Formal equations: stacked fractions.

---

## 7. Capitalization of SI units

- Unit symbols in lowercase unless derived from a person's name (W for watt, V for volt, N for newton).
- When spelled out, always lowercase except at start of sentence or "degrees Celsius."
- Exceptions: L (litre), M (mega), G (giga).
- Unit symbols unaltered in plural, no period after.
