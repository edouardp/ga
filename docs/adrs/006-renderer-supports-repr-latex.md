---
status: accepted
date: 2026-03-25
deciders: edouard
---

# ADR-006: Renderer Supports Both .latex() and _repr_latex_()

## Context and Problem Statement

The `galaga-marimo` renderer needs to detect objects that can produce LaTeX.
Our objects use `.latex()` (raw LaTeX), but third-party objects (SymPy, Pandas)
use `_repr_latex_()` (the Jupyter/IPython protocol, `$`-wrapped). Should we
support both?

## Decision Drivers

* Our `.latex()` returns raw LaTeX — the renderer controls wrapping
* `_repr_latex_()` returns `$...$`-wrapped LaTeX — standard Jupyter protocol
* Third-party objects only implement `_repr_latex_()`
* Supporting both makes the renderer more useful

## Considered Options

1. Only support `.latex()`
2. Support both, prefer `.latex()`, strip delimiters from `_repr_latex_()`
3. Switch entirely to `_repr_latex_()`

## Decision Outcome

Chosen option: "Support both, prefer `.latex()`" — the renderer checks for
`.latex()` first (raw content), then falls back to `_repr_latex_()` with
`$...$` / `$$...$$` delimiter stripping.

### Consequences

* Good, because SymPy expressions, Pandas objects, etc. render automatically
* Good, because our objects use `.latex()` with no double-wrapping
* Neutral, because delimiter stripping is slightly hacky but reliable
* Bad, because we depend on the `_repr_latex_()` convention being stable
