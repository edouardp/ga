import marimo

app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("# Geometric Algebra — Symbolic Expressions\nThis notebook demonstrates the symbolic layer of the `ga` library.")
    return


@app.cell
def _():
    import numpy as np
    from ga import Algebra
    from ga.symbolic import (
        sym, gp, op, grade, grades, reverse, involute, conjugate,
        dual, undual, norm, unit, inverse, squared,
        left_contraction, right_contraction, hestenes_inner, scalar_product,
        even_grades, odd_grades,
    )
    return (
        Algebra, np,
        sym, gp, op, grade, grades, reverse, involute, conjugate,
        dual, undual, norm, unit, inverse, squared,
        left_contraction, right_contraction, hestenes_inner, scalar_product,
        even_grades, odd_grades,
    )


@app.cell
def _(mo):
    mo.md("## Setup — 3D Euclidean Algebra")
    return


@app.cell
def _(Algebra, sym):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors()

    # Wrap numeric multivectors as named symbols
    R = sym(e1 * e2, "R")
    v = sym(e1 + 2 * e2, "v")
    a = sym(e1, "a")
    b = sym(e2, "b")
    A = sym(e1 * e2, "A")
    B = sym(e2 * e3, "B")
    return alg, e1, e2, e3, R, v, a, b, A, B


@app.cell
def _(mo):
    mo.md("## Products")
    return


@app.cell
def _(R, v, a, b, A, B, gp, op, left_contraction, right_contraction, hestenes_inner, scalar_product):
    # Each expression renders as LaTeX automatically in marimo
    gp(a, b)
    return


@app.cell
def _(a, b, op):
    op(a, b)
    return


@app.cell
def _(a, b, left_contraction):
    left_contraction(a, b)
    return


@app.cell
def _(a, b, right_contraction):
    right_contraction(a, b)
    return


@app.cell
def _(A, B, hestenes_inner):
    hestenes_inner(A, B)
    return


@app.cell
def _(A, B, scalar_product):
    scalar_product(A, B)
    return


@app.cell
def _(mo):
    mo.md("## Sandwich Product & Grade Projection")
    return


@app.cell
def _(R, v, grade):
    # The classic rotor sandwich: grade-1 projection of R v R̃
    expr = grade(R * v * ~R, 1)
    expr
    return (expr,)


@app.cell
def _(expr, mo):
    mo.md(f"Evaluating: {expr.latex(wrap='$')} = `{expr.eval()}`")
    return


@app.cell
def _(mo):
    mo.md("## Unary Operations")
    return


@app.cell
def _(R, reverse):
    reverse(R)
    return


@app.cell
def _(v, involute):
    involute(v)
    return


@app.cell
def _(v, conjugate):
    conjugate(v)
    return


@app.cell
def _(mo):
    mo.md("## Dual, Norm, Unit, Inverse")
    return


@app.cell
def _(v, dual):
    dual(v)
    return


@app.cell
def _(v, undual):
    undual(v)
    return


@app.cell
def _(v, norm):
    norm(v)
    return


@app.cell
def _(v, unit):
    unit(v)
    return


@app.cell
def _(v, inverse):
    inverse(v)
    return


@app.cell
def _(mo):
    mo.md("## Even / Odd Grades, Squared")
    return


@app.cell
def _(A, even_grades):
    even_grades(A)
    return


@app.cell
def _(v, odd_grades):
    odd_grades(v)
    return


@app.cell
def _(R, squared):
    squared(R)
    return


@app.cell
def _(mo):
    mo.md("## Arithmetic & Operator Sugar")
    return


@app.cell
def _(a, b):
    a + b
    return


@app.cell
def _(a, b):
    a - b
    return


@app.cell
def _(a):
    3 * a
    return


@app.cell
def _(a, b, R):
    # Parenthesization is automatic
    (a + b) * R
    return


@app.cell
def _(mo):
    mo.md("## Evaluating Expressions")
    return


@app.cell
def _(mo, a, b, op, norm, inverse, grade, R, v):
    exprs = [
        ("Wedge", op(a, b)),
        ("Norm", norm(v)),
        ("Inverse", inverse(a)),
        ("Sandwich", grade(R * v * ~R, 1)),
    ]
    mo.vstack([
        mo.md(f"**{name}:** {e.latex(wrap='$')} = `{e.eval()}`")
        for name, e in exprs
    ])
    return


@app.cell
def _(mo):
    mo.md("## Rotation Demo")
    return


@app.cell
def _(alg, e1, e2, np, sym, grade, mo):
    theta = np.pi / 2
    Bplane = e1 ^ e2
    Rot = alg.rotor_from_plane_angle(Bplane, theta)

    R_sym = sym(Rot, "R")
    v_sym = sym(e1, "v")
    rotated = grade(R_sym * v_sym * ~R_sym, 1)

    mo.vstack([
        mo.md(f"Rotate $v = e_1$ by $90°$ in the $e_1 e_2$ plane:"),
        rotated,
        mo.md(f"Result: `{rotated.eval()}`"),
    ])
    return


@app.cell
def _(mo):
    mo.md("## LaTeX Output\nEvery expression has `.latex()` for raw LaTeX and `.latex(wrap='$')` for inline math.")
    return


@app.cell
def _(R, v, grade, mo):
    sandwich = grade(R * v * ~R, 1)
    mo.vstack([
        mo.md(f"`.latex()` → `{sandwich.latex()}`"),
        mo.md(f"`.latex(wrap='$')` → {sandwich.latex(wrap='$')}"),
    ])
    return


if __name__ == "__main__":
    app.run()
