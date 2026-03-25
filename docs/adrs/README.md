# Architectural Decision Records

This directory contains Architectural Decision Records (ADRs) for the `galaga`
geometric algebra project.

## What are ADRs?

ADRs document significant architectural decisions made during the project. They
capture the context, options considered, decision made, and consequences. This
helps future contributors understand why certain choices were made.

## ADR Index

| ADR | Title | Status |
|-----|-------|--------|
| [001](001-use-architectural-decision-records.md) | Use Architectural Decision Records | Accepted |
| [002](002-named-functions-as-api-contract.md) | Named Functions as the Stable API Contract | Accepted |
| [003](003-explicit-inner-product-variants.md) | Explicit Inner Product Variants | Accepted |
| [004](004-two-layer-architecture.md) | Two-Layer Architecture (Numeric + Symbolic) | Accepted |
| [005](005-separate-marimo-helper-package.md) | Separate Marimo Notebook Helper Package | Accepted |
| [006](006-renderer-supports-repr-latex.md) | Renderer Supports Both .latex() and _repr_latex_() | Accepted |
| [007](007-integer-only-pow.md) | Integer-Only Multivector Exponentiation | Accepted |
| [008](008-commutator-family.md) | Commutator Family — Four Named Functions, No Flags | Accepted |
| [009](009-aliases-are-convenience.md) | Aliases Are Convenience, Not Separate Implementations | Accepted |
| [010](010-complement-vs-dual.md) | Complement vs Dual — Metric-Independent Duality | Accepted |
| [011](011-precomputed-multiplication-tables.md) | Precomputed Multiplication Tables | Accepted |
| [012](012-unicode-repr-opt-in.md) | Unicode Repr with Opt-In Flag | Accepted |
| [013](013-symbolic-drop-in-pattern.md) | Symbolic Drop-In Replacement Pattern | Accepted |
| [014](014-fixed-point-simplification.md) | Fixed-Point Simplification | Accepted |
| [015](015-uv-workspace-monorepo.md) | uv Workspace for Monorepo | Accepted |
| [016](016-t-string-rendering.md) | T-String Rendering in Marimo Notebooks | Accepted |

## Creating New ADRs

1. Copy the frontmatter and structure from any existing ADR
2. Number sequentially (e.g., `017-your-decision.md`)
3. Fill in all sections
4. Update this index

## Format

All ADRs follow the [MADR](https://adr.github.io/madr/) (Markdown Any Decision Records) format.
