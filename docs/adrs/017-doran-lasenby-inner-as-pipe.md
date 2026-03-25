---
status: accepted
date: 2026-03-25
deciders: edouard
---

# ADR-017: Doran–Lasenby Inner Product as the | Operator

## Context and Problem Statement

The `|` operator was mapped to `hestenes_inner`, which kills scalars: if either
operand is grade-0, the result is zero. This is surprising — `3 | e1` returning
zero is unintuitive. The Doran–Lasenby inner product uses the same grade
selection rule (|r-s|) but includes scalars, which is more general and matches
the convention in "Geometric Algebra for Physicists" (Doran & Lasenby) and
"Geometric Algebra for Computer Science" (Dorst et al.).

## Decision Drivers

* Hestenes inner kills scalars — `scalar | vector = 0` is surprising
* Doran–Lasenby is strictly more general (superset of Hestenes for non-scalars)
* Doran & Lasenby and Dorst et al. are widely used references
* Both conventions should remain available as named functions

## Considered Options

1. Keep `|` as Hestenes inner
2. Change `|` to Doran–Lasenby inner, keep Hestenes as a named function
3. Change `|` to left contraction

## Decision Outcome

Chosen option: "Change `|` to Doran–Lasenby inner" — the most general
grade-|r-s| inner product that includes scalars.

```python
doran_lasenby_inner(a, b)  # grade-|r-s| part of gp(a,b), including scalars
dorst_inner = doran_lasenby_inner  # alias
hestenes_inner(a, b)       # same but kills scalars (zero if either is grade-0)
```

The `ip()` dispatcher default also changes from `"hestenes"` to `"doran_lasenby"`.

### Consequences

* Good, because `3 | e1` now returns `3*e1` instead of `0`
* Good, because Doran–Lasenby is a superset — no information lost
* Good, because Hestenes inner remains available as `hestenes_inner()`
* Good, because `dorst_inner` alias serves users of that textbook
* Bad, because this is a breaking change for code relying on `|` killing scalars
