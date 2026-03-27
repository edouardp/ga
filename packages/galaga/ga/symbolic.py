"""Symbolic expression tree for pretty-printing and algebraic manipulation.

This module provides a lazy expression tree that sits on top of the numeric
core in ``ga.algebra``. It serves two purposes:

1. **Pretty-printing.** Instead of computing ``R * v * ~R`` immediately and
   showing the numeric result, you can wrap the operands as symbols
   (``sym(R, "R")``) and get ``RvR̃`` as output — in Unicode, LaTeX, or
   Jupyter's ``_repr_latex_``.

2. **Algebraic simplification.** The ``simplify()`` function applies rewrite
   rules (double-reverse cancellation, rotor normalisation, grade-aware
   projection, etc.) to expression trees, running to a fixed point.

Architecture
------------
Every GA operation has a corresponding ``Expr`` subclass (``Gp``, ``Op``,
``Grade``, ``Reverse``, etc.) that stores its operands as child nodes.
The tree is built lazily via operator overloads on ``Expr``:

    R * v * ~R  →  Gp(Gp(Sym("R"), Sym("v")), Reverse(Sym("R")))

Each node implements:
- ``eval()``    → recursively evaluates to a concrete ``Multivector``
- ``__str__()`` → Unicode rendering (``RvR̃``)
- ``_latex()``  → LaTeX rendering (``R v \\tilde{R}``)

Drop-in API
-----------
The module re-exports every function from ``ga.algebra`` (``gp``, ``grade``,
``reverse``, etc.) as a wrapper that detects ``Expr`` arguments:

- If any argument is an ``Expr``, it builds a tree node.
- If all arguments are plain ``Multivector``s, it delegates directly to the
  numeric implementation with zero overhead.

This means users can ``from ga.symbolic import gp, grade, reverse`` and use
the same function names for both symbolic and numeric work.

Grade tracking
--------------
``Sym`` nodes auto-detect the homogeneous grade of their wrapped multivector
(e.g., ``sym(e1, "v")`` knows it's grade-1). This enables ``simplify()`` to
resolve ``grade(v, 1) → v`` and ``grade(v, 2) → 0`` without evaluation.

Usage:
    from ga import Algebra
    from ga.symbolic import sym, grade, reverse

    alg = Algebra((1,1,1))
    e1, e2, e3 = alg.basis_vectors()

    R = sym(e1 * e2, "R")
    v = sym(e1 + 2*e2, "v")

    expr = grade(R * v * ~R, 1)
    print(expr)          # ⟨RvR̃⟩₁
    print(expr.eval())   # concrete Multivector result
    print(expr.latex())  # \\langle R v \\tilde{R} \\rangle_{1}
"""

from __future__ import annotations

from typing import Union
import ga.algebra as _alg


# Unicode combining characters for postfix decorations.
# These are appended directly after a character to modify its appearance.
# E.g., "R" + _REVERSE → "R̃" (R with combining tilde above).


def _coerce(x):
    """Coerce a value to Expr if needed. Used by node constructors."""
    if isinstance(x, Expr):
        return x
    if isinstance(x, _alg.Multivector):
        # Deferred to avoid forward reference — _ensure_expr is defined later
        if x._expr is not None:
            return x._expr
        if x._name is not None:
            return Sym(x, x._name_unicode or x._name,
                       name_latex=x._name_latex, name_ascii=x._name)
        return Sym(x, str(x))
    return x


class Expr:
    """Base class for all symbolic GA expression tree nodes.

    Every node in the expression tree inherits from this. The class provides:
    - Operator overloads that build tree nodes (``__mul__`` → ``Gp``, etc.)
    - ``eval()`` to recursively compute the concrete ``Multivector`` result
    - Rendering via ``ga.render`` (unicode and LaTeX)
    - ``_repr_latex_()`` for automatic Jupyter/marimo rendering
    - Convenience properties (``.inv``, ``.dag``, ``.sq``) matching ``Multivector``

    Subclasses must implement ``eval()``.
    """

    def eval(self) -> _alg.Multivector:
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        from ga.render import render
        return render(self)

    def latex(self, wrap: str | None = None) -> str:
        """Return LaTeX representation."""
        from ga.render import render_latex
        raw = render_latex(self)
        if wrap == "$":
            return f"${raw}$"
        if wrap == "$$":
            return f"$$\n{raw}\n$$"
        return raw

    def _repr_latex_(self) -> str:
        """Jupyter notebook integration."""
        return f"${self.latex()}$"

    # --- Operators build expression trees ---

    def __add__(self, other):
        other = _ensure_expr(other)
        return Add(self, other)

    def __radd__(self, other):
        return _ensure_expr(other).__add__(self)

    def __sub__(self, other):
        other = _ensure_expr(other)
        return Sub(self, other)

    def __rsub__(self, other):
        return _ensure_expr(other).__sub__(self)

    def __neg__(self):
        return Neg(self)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return ScalarMul(other, self)
        other = _ensure_expr(other)
        return Gp(self, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return ScalarMul(other, self)
        return _ensure_expr(other).__mul__(self)

    def __xor__(self, other):
        return Op(self, _ensure_expr(other))

    def __or__(self, other):
        return Hi(self, _ensure_expr(other))

    def __invert__(self):
        return Reverse(self)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return ScalarDiv(self, other)
        return NotImplemented

    # Convenience properties matching Multivector
    @property
    def inv(self) -> Expr:
        return Inverse(self)

    @property
    def dag(self) -> Expr:
        return Reverse(self)

    @property
    def sq(self) -> Expr:
        return Squared(self)


class Sym(Expr):
    """A named multivector — leaf node of the expression tree.

    Wraps a concrete ``Multivector`` with a display name. This is the entry
    point for building symbolic expressions: ``sym(e1, "v")`` creates a
    ``Sym`` that prints as "v" but evaluates to ``e1``.

    Grade auto-detection: if the wrapped multivector is homogeneous (all
    nonzero coefficients are the same grade), that grade is recorded in
    ``_grade``. This enables ``simplify()`` to resolve grade projections
    without numeric evaluation — e.g., ``grade(v, 1) → v`` when v is
    known to be grade-1, and ``grade(v, 2) → 0``.
    """

    def __init__(self, mv: _alg.Multivector, name: str, grade: int | None = None,
                 name_latex: str | None = None, name_ascii: str | None = None):
        self._mv = mv
        self._name = name
        self._name_latex = name_latex or name
        self._name_ascii = name_ascii or name
        # Auto-detect grade if not provided
        if grade is not None:
            self._grade = grade
        else:
            self._grade = mv.homogeneous_grade()

    def eval(self) -> _alg.Multivector:
        return self._mv



    def __repr__(self) -> str:
        return self._name_ascii


class Scalar(Expr):
    """A numeric scalar leaf — represents a plain number in the expression tree.

    Created automatically by ``_ensure_expr()`` when a Python int/float
    appears in an expression (e.g., ``3 * sym_v`` creates ``ScalarMul(3, sym_v)``
    but ``sym_v + 3`` creates ``Add(sym_v, Scalar(3))``).

    Note: ``eval()`` raises TypeError because a bare scalar has no algebra
    context. Scalars only make sense combined with ``Sym`` nodes that carry
    an algebra reference.
    """

    def __init__(self, value: Numeric):
        self._value = value

    def eval(self) -> _alg.Multivector:
        raise TypeError("Scalar has no algebra context; use in combination with Sym nodes")




# --- Binary ops ---


































# ============================================================
# Generated Expr subclasses
# ============================================================

# --- Generated Expr subclasses ---
# Most binary/unary Expr nodes are identical: __init__ coerces args,
# eval() delegates to the corresponding ga.algebra function.
# Instead of 22 hand-written classes, we generate them from a table.
# This eliminates ~150 lines of boilerplate and ensures consistency.

def _make_binary_expr(name, alg_func_name):
    """Generate a binary Expr subclass."""
    def __init__(self, a, b):
        self.a, self.b = _coerce(a), _coerce(b)
    def eval(self):
        return getattr(_alg, alg_func_name)(self.a.eval(), self.b.eval())
    return type(name, (Expr,), {'__init__': __init__, 'eval': eval})


def _make_unary_expr(name, alg_func_name):
    """Generate a unary Expr subclass."""
    def __init__(self, x):
        self.x = _coerce(x)
    def eval(self):
        return getattr(_alg, alg_func_name)(self.x.eval())
    return type(name, (Expr,), {'__init__': __init__, 'eval': eval})


# Binary expression nodes
Gp = _make_binary_expr('Gp', 'gp')
Op = _make_binary_expr('Op', 'op')
Lc = _make_binary_expr('Lc', 'left_contraction')
Rc = _make_binary_expr('Rc', 'right_contraction')
Hi = _make_binary_expr('Hi', 'hestenes_inner')
Dli = _make_binary_expr('Dli', 'doran_lasenby_inner')
Sp = _make_binary_expr('Sp', 'scalar_product')
Commutator = _make_binary_expr('Commutator', 'commutator')
Anticommutator = _make_binary_expr('Anticommutator', 'anticommutator')
LieBracket = _make_binary_expr('LieBracket', 'lie_bracket')
JordanProduct = _make_binary_expr('JordanProduct', 'jordan_product')
Regressive = _make_binary_expr('Regressive', 'regressive_product')

# Unary expression nodes
Reverse = _make_unary_expr('Reverse', 'reverse')
Involute = _make_unary_expr('Involute', 'involute')
Conjugate = _make_unary_expr('Conjugate', 'conjugate')
Dual = _make_unary_expr('Dual', 'dual')
Undual = _make_unary_expr('Undual', 'undual')
Complement = _make_unary_expr('Complement', 'complement')
Uncomplement = _make_unary_expr('Uncomplement', 'uncomplement')
Norm = _make_unary_expr('Norm', 'norm')
Unit = _make_unary_expr('Unit', 'unit')
Inverse = _make_unary_expr('Inverse', 'inverse')
Exp = _make_unary_expr('Exp', 'exp')
Log = _make_unary_expr('Log', 'log')
Even = _make_unary_expr('Even', 'even_grades')
Odd = _make_unary_expr('Odd', 'odd_grades')


class Add(Expr):
    def __init__(self, a, b):
        self.a, self.b = _coerce(a), _coerce(b)

    def eval(self):
        return self.a.eval() + self.b.eval()




class Sub(Expr):
    def __init__(self, a, b):
        self.a, self.b = _coerce(a), _coerce(b)

    def eval(self):
        return self.a.eval() - self.b.eval()




class ScalarMul(Expr):
    def __init__(self, k: Numeric, x):
        self.k, self.x = k, _coerce(x)

    def eval(self):
        return self.x.eval() * self.k




class ScalarDiv(Expr):
    """Division by a scalar: x / k."""
    def __init__(self, x, k: Numeric):
        self.x, self.k = _coerce(x), k

    def eval(self):
        return self.x.eval() / self.k




class Div(Expr):
    """Division of two expressions: a / b."""
    def __init__(self, a, b):
        self.a, self.b = _coerce(a), _coerce(b)

    def eval(self):
        return self.a.eval() / self.b.eval()




class Neg(Expr):
    def __init__(self, x):
        self.x = _coerce(x)

    def eval(self):
        return -self.x.eval()




# --- Unary ops ---










class Grade(Expr):
    def __init__(self, x, k: int):
        self.x, self.k = _coerce(x), k

    def eval(self):
        return _alg.grade(self.x.eval(), self.k)



















class Squared(Expr):
    def __init__(self, x):
        self.x = _coerce(x)

    def eval(self):
        return _alg.gp(self.x.eval(), self.x.eval())













# --- Helper ---

def _ensure_expr(x) -> Expr:
    """Coerce a value into an Expr node.

    - ``Expr`` → returned as-is
    - ``int``/``float`` → wrapped in ``Scalar``
    - ``Multivector`` with ``_expr`` → returns the expression tree
    - ``Multivector`` with ``_name`` → wrapped in ``Sym`` with its name
    - ``Multivector`` (anonymous eager) → wrapped in ``Sym`` with its string representation

    This is called by every operator overload to handle mixed-type expressions
    like ``sym_v + 3`` or ``sym_R * e1`` transparently.
    """
    if isinstance(x, Expr):
        return x
    if isinstance(x, (int, float)):
        return Scalar(x)
    if isinstance(x, _alg.Multivector):
        if x._expr is not None:
            return x._expr
        if x._name is not None:
            return Sym(x, x._name_unicode or x._name,
                       name_latex=x._name_latex, name_ascii=x._name)
        return Sym(x, str(x))
    raise TypeError(f"Cannot convert {type(x)} to symbolic expression")


from ga.simplify import simplify, _eq, _known_grade


# ============================================================
# Public API: drop-in replacements for ga.algebra functions
# ============================================================
#
# Each function below checks if any argument is an Expr. If so, it builds
# the corresponding tree node. If all arguments are plain Multivectors,
# it delegates directly to ga.algebra with zero overhead.
#
# This design means users can import from ga.symbolic instead of ga and
# get symbolic behaviour automatically when working with Sym-wrapped values,
# while keeping full numeric performance for unwrapped multivectors.
# ============================================================

def _is_symbolic(x) -> bool:
    """Check if x is an Expr or a lazy Multivector."""
    if isinstance(x, Expr):
        return True
    if isinstance(x, _alg.Multivector) and x._is_lazy:
        return True
    return False


def sym(mv: _alg.Multivector, name: str | None = None, grade: int | None = None) -> _alg.Multivector:
    """Return a lazy copy of a multivector, optionally named.

    Does not mutate the original. Use ``.name()`` on the result to add
    or change the name.

    Args:
        mv: The multivector to copy.
        name: Optional display name.
        grade: If provided, asserts the homogeneous grade for simplification.
               If omitted, auto-detected from the multivector data.
    """
    result = mv._copy_with()  # copy first
    if name is not None:
        result.name(name)
    else:
        result.lazy()
    if grade is not None:
        result._grade = grade
    if result._expr is not None and isinstance(result._expr, Sym):
        result._expr._grade = result._grade
    return result


# ============================================================
# Drop-in replacements for ga.algebra functions
# ============================================================
# These detect lazy Multivector arguments and build Expr trees.
# With plain eager Multivectors, they delegate to ga.algebra.

# --- Generated drop-in replacements ---
# Each drop-in checks if any argument is a lazy MV (via _is_symbolic).
# If so, it builds the corresponding Expr tree node.
# If not, it delegates directly to ga.algebra with zero overhead.
# This is the bridge between the numeric and symbolic layers.
#
# The factories take a string name instead of a direct function reference
# so that ga.algebra doesn't need to be fully loaded when symbolic.py
# is first imported (avoiding circular import issues).

def _make_binary_dropin(node_cls, func_name):
    """Generate a binary drop-in that builds node_cls for symbolic args."""
    def dropin(a, b):
        if _is_symbolic(a) or _is_symbolic(b):
            return node_cls(_ensure_expr(a), _ensure_expr(b))
        return getattr(_alg, func_name)(a, b)
    dropin.__name__ = func_name
    return dropin


def _make_unary_dropin(node_cls, func_name):
    """Generate a unary drop-in that builds node_cls for symbolic args."""
    def dropin(x):
        if _is_symbolic(x):
            return node_cls(_ensure_expr(x))
        return getattr(_alg, func_name)(x)
    dropin.__name__ = func_name
    return dropin


# Binary drop-ins
gp = _make_binary_dropin(Gp, 'gp')
op = _make_binary_dropin(Op, 'op')
left_contraction = _make_binary_dropin(Lc, 'left_contraction')
right_contraction = _make_binary_dropin(Rc, 'right_contraction')
hestenes_inner = _make_binary_dropin(Hi, 'hestenes_inner')
doran_lasenby_inner = _make_binary_dropin(Dli, 'doran_lasenby_inner')
dorst_inner = doran_lasenby_inner
scalar_product = _make_binary_dropin(Sp, 'scalar_product')
commutator = _make_binary_dropin(Commutator, 'commutator')
anticommutator = _make_binary_dropin(Anticommutator, 'anticommutator')
lie_bracket = _make_binary_dropin(LieBracket, 'lie_bracket')
jordan_product = _make_binary_dropin(JordanProduct, 'jordan_product')
regressive_product = _make_binary_dropin(Regressive, 'regressive_product')
meet = regressive_product

# Unary drop-ins
reverse = _make_unary_dropin(Reverse, 'reverse')
involute = _make_unary_dropin(Involute, 'involute')
conjugate = _make_unary_dropin(Conjugate, 'conjugate')
dual = _make_unary_dropin(Dual, 'dual')
undual = _make_unary_dropin(Undual, 'undual')
complement = _make_unary_dropin(Complement, 'complement')
uncomplement = _make_unary_dropin(Uncomplement, 'uncomplement')
norm = _make_unary_dropin(Norm, 'norm')
unit = _make_unary_dropin(Unit, 'unit')
inverse = _make_unary_dropin(Inverse, 'inverse')
squared = _make_unary_dropin(Squared, 'squared')
even_grades = _make_unary_dropin(Even, 'even_grades')
odd_grades = _make_unary_dropin(Odd, 'odd_grades')

normalize = unit
normalise = unit


def grade(x, k):
    if _is_symbolic(x):
        e = _ensure_expr(x)
        if k == "even":
            return Even(e)
        if k == "odd":
            return Odd(e)
        return Grade(e, k)
    return _alg.grade(x, k)


def ip(a, b, mode: str = "doran_lasenby"):
    if _is_symbolic(a) or _is_symbolic(b):
        a, b = _ensure_expr(a), _ensure_expr(b)
        match mode:
            case "doran_lasenby" | "dorst":
                return Dli(a, b)
            case "hestenes":
                return Hi(a, b)
            case "left":
                return Lc(a, b)
            case "right":
                return Rc(a, b)
            case "scalar":
                return Sp(a, b)
            case _:
                raise ValueError(f"Unknown inner product mode: {mode!r}")
    return _alg.ip(a, b, mode=mode)


def sandwich(r, x):
    if _is_symbolic(r) or _is_symbolic(x):
        re = _ensure_expr(r)
        xe = _ensure_expr(x)
        return Gp(Gp(re, xe), Reverse(re))
    return _alg.sandwich(r, x)


sw = sandwich



