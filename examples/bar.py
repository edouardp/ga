import marimo

__generated_with = "0.21.1"
app = marimo.App()


@app.cell
def _():
    import sys
    from pathlib import Path

    _root = str(Path(__file__).resolve().parent.parent)
    _gamo = str(Path(__file__).resolve().parent.parent / "packages" / "gamo")
    for p in [_root, _gamo]:
        if p not in sys.path:
            sys.path.insert(0, p)
    return


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import numpy as np
    from ga import (
        Algebra, gp, op, grade, reverse, involute, conjugate,
        dual, norm, unit, inverse, exp, log, sandwich, scalar,
        left_contraction, hestenes_inner, even_grades, odd_grades,
        squared
    )
    from ga.symbolic import (
        sym, simplify, grade as sgrade, reverse as srev,
        norm as snorm, unit as sunit, inverse as sinverse,
    )
    import galaga_marimo as gm

    return Algebra, grade


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return e1, e2, e3


@app.cell
def _(e1, e2, e3):
    A = e1 ^ e2
    B = e2 ^ e3

    A + 2*B 
    return


@app.cell
def _(e1, e2, e3):
    e1 ^ e2 + (2*e2) ^ e3
    return


@app.cell
def _(C, grade):
    grade(C, 2).eval()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
