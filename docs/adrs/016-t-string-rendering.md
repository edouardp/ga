---
status: accepted
date: 2026-03-25
deciders: edouard
---

# ADR-016: T-String Rendering in Marimo Notebooks

## Context and Problem Statement

How should GA objects be rendered in marimo notebooks? The standard approach
(`mo.md(f"...")`) stringifies objects before the renderer sees them, losing
type information needed for LaTeX rendering.

## Decision Drivers

* Python 3.14 t-strings expose interpolated values as typed objects
* GA objects have `.latex()` methods for LaTeX rendering
* Plain Python values (strings, ints, floats) should render as text
* Format specs (`:latex`, `:block`, `:text`, `:.3f`) should control rendering

## Decision Outcome

Use Python 3.14 t-strings with a custom renderer. `gm.md(t"...")` walks the
template's interpolations, classifies each value by type, and assembles
markdown with automatic LaTeX wrapping:

- Objects with `.latex()` or `_repr_latex_()` → inline LaTeX (`$...$`)
- Plain values → escaped text
- Format specs override auto-detection

### Consequences

* Good, because `gm.md(t"Vector: {v}")` just works — no manual `.latex()` calls
* Good, because format specs give fine-grained control
* Good, because conversion flags (`!s`, `!r`) force text mode for debugging
* Bad, because requires Python 3.14+ (t-strings are new)
* Bad, because LaTeX backslashes need `\\` in t-strings (no raw t-strings yet)
