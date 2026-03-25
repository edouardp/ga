---
status: accepted
date: 2026-03-25
deciders: edouard
---

# ADR-010: Complement vs Dual — Metric-Independent Duality

## Context and Problem Statement

The standard `dual(x)` operation uses the metric (left-contracts with the
inverse pseudoscalar). In degenerate algebras like PGA (Cl(3,0,1)), the
pseudoscalar is not invertible, so `dual()` fails. How do we provide duality
in all signatures?

## Decision Drivers

* PGA is a key use case — degenerate metrics must work
* `dual()` is well-defined only when the pseudoscalar is invertible
* The complement (index set complement with sign) is purely combinatorial
* Users need both: metric-dependent dual and metric-independent complement

## Decision Outcome

Two separate operations:

- `dual(x)` — left-contracts with the inverse pseudoscalar. Requires invertible
  pseudoscalar. Fails in degenerate algebras.
- `complement(x)` — maps grade-k to grade-(n-k) by index set complement, with
  sign chosen so that `x * complement(x) = pseudoscalar`. Works in all
  signatures including degenerate algebras.

Both have inverses: `undual()` and `uncomplement()`.

### Consequences

* Good, because PGA users get a working duality operation
* Good, because the distinction between metric-dependent and metric-independent is explicit
* Good, because complement signs are precomputed at algebra creation time
