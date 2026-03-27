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
    import numpy as np
    import galaga_marimo as gm
    from ga import (
        Algebra, exp, log, dual, undual, inverse, reverse,
        complement, uncomplement,
    )
    from ga.notation import Notation, NotationRule


    return Algebra, NotationRule, exp, np, reverse


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(NotationRule, alg):
    alg.notation.set("Reverse", "latex", NotationRule(kind="superscript", symbol=r"\dagger"))
    #alg.notation.set("Reverse", "latex", NotationRule(kind="prefix", symbol=r"~ "))
    return


@app.cell
def _(alg, e1, e2, e3, exp, np, reverse):
    _theta = alg.scalar(np.radians(60)).name(latex=r"\theta")

    _B = (e1 * e2).name("B")
    _v = (3 * e1 + 4 * e2 + e3).name("v")
    _R = exp((-_theta / 2) * _B)

    _rotated = _R * _v * reverse(_R)

    _rotated
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
