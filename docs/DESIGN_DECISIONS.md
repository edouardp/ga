# Design Decisions

High-level principles that guide the `galaga` geometric algebra library.

## 1. Named functions are the contract

Every operation has a stable, named function: `gp`, `op`, `grade`, `reverse`, `dual`, `inverse`, etc. These names never change meaning.

Operators (`*`, `^`, `|`, `~`) are sugar — convenient, but not the API you depend on. If there's ever ambiguity about what an operator does, the named function resolves it.

## 2. No ambiguity

Where mathematics has competing conventions, we expose each one explicitly rather than picking a default.

- Inner products: `left_contraction`, `right_contraction`, `hestenes_inner`, `scalar_product` — all available, all named.
- Commutator family: `commutator` (ab − ba), `lie_bracket` (½(ab − ba)), `anticommutator` (ab + ba), `jordan_product` (½(ab + ba)) — four functions, no boolean flags.
- The `|` operator maps to Hestenes inner, but that's documented sugar, not a hidden choice.

## 3. Explicit over implicit

Two named functions beat one function with a mode flag. `lie_bracket(a, b)` is self-documenting; `commutator(a, b, half=True)` is not.

The ½ in `lie_bracket` vs `commutator` is not a formatting choice — it changes the algebraic convention. That distinction deserves its own name.

## 4. Aliases exist for convenience, not as separate implementations

`wedge` is literally `op`. `rev` is literally `reverse`. `normalize` is literally `unit`. They share the same function object — no divergence, no maintenance burden.

## 5. Two-layer architecture

- **`ga.algebra`** — The numeric core. `Algebra` (factory), `Multivector` (value type), and every named operation. Computation happens here via precomputed multiplication tables and dense NumPy arrays.
- **`ga.symbolic`** — An opt-in expression-tree layer for pretty-printing and symbolic manipulation. Every symbolic function is a drop-in replacement: it detects `Expr` arguments and builds trees, but passes plain `Multivector` arguments straight through to the numeric core.

The symbolic layer is imported separately (`from ga import symbolic as sym`) because most users only need it for notebooks and display.

## 6. Operators build expression trees transparently

In the symbolic layer, `R * v * ~R` builds a `Gp(Gp(R, v), Reverse(R))` tree — no special syntax needed. The same code that does numeric computation also builds symbolic expressions when the inputs are wrapped.

## 7. Rendering protocol

Objects that can render as LaTeX expose `.latex()` (raw LaTeX content) and `_repr_latex_()` (Jupyter/IPython protocol with `$...$` wrapping). The `galaga_marimo` helper detects both, preferring `.latex()` for embedding in larger expressions.

## 8. Stable public surface

The `__init__.py` re-exports the numeric API so `from ga import *` gives you everything for computation. The `__all__` list is the contract. New operations are added; existing ones don't change meaning.

## 9. Separate notebook helper

The marimo integration (`galaga_marimo` / `gamo`) is a separate package, not part of the core. It depends on marimo and uses Python 3.14 t-strings for automatic LaTeX rendering. This keeps the core library dependency-free (only NumPy) and framework-agnostic.

## 10. ADRs for specific decisions

Individual architectural decisions are recorded in [`docs/adrs/`](adrs/). Each ADR captures the context, decision, and consequences for a specific choice.
