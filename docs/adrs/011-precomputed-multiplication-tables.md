---
status: accepted
date: 2026-03-25
deciders: edouard
---

# ADR-011: Precomputed Multiplication Tables

## Context and Problem Statement

How should the geometric product be computed? The product of two basis blades
depends on the algebra's signature and can involve sign changes from
anticommuting basis vectors.

## Decision Drivers

* Performance matters — GA products are called frequently
* The sign rules are determined entirely by the signature at algebra creation time
* Dense NumPy arrays enable vectorized computation

## Decision Outcome

Precompute the full multiplication table at `Algebra` creation time using
bitmask representations of basis blades. Each blade is an integer bitmask
(e.g., `e1^e2 = 0b011`). The product of two blades is computed by XOR
(for the result blade) and counting swaps (for the sign).

The multiplication table is stored as a dense array. The geometric product
of two multivectors is then a double loop over nonzero coefficients,
indexing into the precomputed table.

### Consequences

* Good, because product computation is a simple table lookup
* Good, because the table is computed once and reused for all products
* Good, because all other products (outer, inner, etc.) are derived by grade filtering
* Bad, because memory scales as O(2^n × 2^n) — impractical for n > ~12
