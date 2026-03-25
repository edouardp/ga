"""Tests for the symbolic redesign: naming and evaluation semantics."""

import pytest
import numpy as np
from ga import Algebra
from ga.symbolic import sym, simplify, Expr, Sym


@pytest.fixture
def cl3():
    return Algebra((1, 1, 1))


class TestNameMethod:
    def test_name_sets_all_variants(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = (e1).name("v")
        assert v._name == "v"
        assert v._name_unicode == "v"
        assert v._name_latex == "v"

    def test_name_with_overrides(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.name("v", latex=r"\mathbf{v}", unicode="𝐯")
        assert v._name == "v"
        assert v._name_latex == r"\mathbf{v}"
        assert v._name_unicode == "𝐯"

    def test_name_makes_lazy(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.name("v")
        assert v._is_lazy is True

    def test_name_preserves_value(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.name("v")
        assert v == e1

    def test_name_ascii_kwarg(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.name("v", ascii="v_ascii")
        assert v._name == "v_ascii"


class TestAnonMethod:
    def test_anon_clears_name(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.name("v").anon()
        assert v._name is None
        assert v._name_unicode is None
        assert v._name_latex is None

    def test_anon_preserves_lazy(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.name("v").anon()
        assert v._is_lazy is True

    def test_anon_on_anonymous_is_noop(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = (e1 + cl3.basis_vectors()[1])
        v2 = v.anon()
        assert v2._name is None


class TestLazyEagerMethods:
    def test_lazy_on_eager(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = (e1).lazy()
        assert v._is_lazy is True

    def test_eager_on_lazy(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        Be = B.eager()
        assert Be._is_lazy is False
        assert Be._name == "B"  # name preserved

    def test_eval_is_eager(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        Be = B.eval()
        assert Be._is_lazy is False
        assert Be._name == "B"

    def test_chaining_name_eager(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B").eager()
        assert B._name == "B"
        assert B._is_lazy is False

    def test_idempotence_lazy(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.lazy().lazy()
        assert v._is_lazy is True

    def test_idempotence_eager(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.eager().eager()
        assert v._is_lazy is False

    def test_idempotence_anon(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.anon().anon()
        assert v._name is None


class TestDisplayRules:
    def test_named_prints_name(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        assert str(B) == "B"

    def test_named_eager_prints_name(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.name("v").eager()
        assert str(v) == "v"

    def test_anon_lazy_prints_expr(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        anon = B.anon()
        # Should show the expression tree, not the name
        assert str(anon) != "B"

    def test_anon_eager_prints_format(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        x = e1 + e2
        # Eager anonymous — existing behavior
        s = str(x)
        assert "e" in s or "+" in s

    def test_latex_named(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = e1.name("v", latex=r"\mathbf{v}")
        assert v.latex() == r"\mathbf{v}"

    def test_latex_anon_eager(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        # Anonymous eager — coefficient rendering
        x = e1.anon()
        latex = x.latex()
        assert "e" in latex


class TestLazyPropagation:
    def test_lazy_plus_eager(self, cl3):
        e1, e2, e3 = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        x = B + e3
        assert x._is_lazy is True
        assert "B" in str(x)
        assert "e₃" in str(x)

    def test_eager_plus_eager_stays_eager(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        x = e1 + e2
        assert x._is_lazy is False

    def test_lazy_mul(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        x = B * e1
        assert x._is_lazy is True

    def test_scalar_mul_lazy(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        x = 2 * B
        assert x._is_lazy is True
        assert "2" in str(x)
        assert "B" in str(x)

    def test_names_dont_propagate(self, cl3):
        e1, e2, e3 = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        x = B + e3
        assert x._name is None

    def test_eager_result_concrete(self, cl3):
        e1, e2, e3 = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        x = (B + e3).eager()
        assert x._is_lazy is False
        # Should have concrete data
        assert np.any(x.data != 0)


class TestBasisBlades:
    def test_basis_named_eager(self, cl3):
        e1, e2, e3 = cl3.basis_vectors()
        assert e1._name is not None
        assert e1._is_lazy is False

    def test_basis_str(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        assert str(e1) == "e₁"

    def test_basis_anon(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        a = e1.anon()
        # Should print concrete blade form
        assert a._name is None

    def test_basis_rename(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        x = e1.name("x")
        assert str(x) == "x"

    def test_pseudoscalar_named(self, cl3):
        I = cl3.pseudoscalar()
        assert I._name == "I"
        assert str(I) == "𝑰"

    def test_blade_lookup_named(self, cl3):
        b = cl3.blade("e12")
        assert b._name == "e12"

    def test_custom_names(self):
        sta = Algebra((1, -1, -1, -1), names="gamma")
        g0, g1, g2, g3 = sta.basis_vectors()
        assert g0._name is not None
        assert "γ" in str(g0)


class TestSymAlias:
    def test_sym_returns_multivector(self, cl3):
        from ga.algebra import Multivector
        e1, _, _ = cl3.basis_vectors()
        v = sym(e1, "v")
        assert isinstance(v, Multivector)
        assert str(v) == "v"

    def test_sym_grade_detection(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        v = sym(e1, "v")
        assert v._grade == 1
        B = sym(e1 ^ e2, "B")
        assert B._grade == 2

    def test_sym_explicit_grade(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        v = sym(e1 + e2, "v", grade=1)
        assert v._grade == 1

    def test_sym_eval(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        R = sym(e1 * e2, "R")
        Re = R.eval()
        assert str(Re) == "R"
        assert Re._is_lazy is False


# ============================================================
# Spec use cases (verbatim from symbolic-redesign.md)
# ============================================================

class TestSpecUseCases:
    """Test all 10 use cases from the spec."""

    def test_use_case_1_plain_numeric(self, cl3):
        """Plain numeric / algebraic use."""
        e1, e2, e3 = cl3.basis_vectors()
        x = 2 * e1 + 3 * e2
        # Basis blades are named + eager, result is eager
        assert x._is_lazy is False

    def test_use_case_2_named_symbolic_bivector(self, cl3):
        """Define a named symbolic bivector."""
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        assert str(B) == "B"
        assert B._is_lazy is True

    def test_use_case_3_reveal_structure(self, cl3):
        """Reveal the symbolic structure again."""
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        assert str(B.anon()) != "B"

    def test_use_case_4_evaluate_keep_name(self, cl3):
        """Evaluate but keep the name."""
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        Be = B.eager()
        assert str(Be) == "B"
        # anon reveals concrete form
        s = str(Be.anon())
        assert s != "B"

    def test_use_case_5_rename(self, cl3):
        """Rename an existing named object."""
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).name("B")
        B2 = B.name("plane")
        assert str(B2) == "plane"

    def test_use_case_6_lazy_unnamed(self, cl3):
        """Lazy unnamed expressions."""
        e1, e2, e3 = cl3.basis_vectors()
        expr = ((e1 + e2) ^ e3).lazy()
        s = str(expr)
        # Should show symbolic structure, not just a name
        assert expr._is_lazy is True

    def test_use_case_7_rotor_workflow(self, cl3):
        """Rotor workflow."""
        from ga import exp
        e1, e2, _ = cl3.basis_vectors()
        theta = 0.5
        B = (e1 ^ e2).name("B")
        R = (-B * theta / 2).name("R")
        v = e1
        v_rot = R * v * ~R
        # v_rot is lazy because R is lazy
        assert v_rot._is_lazy is True
        # Can get concrete result
        concrete = v_rot.eager()
        assert concrete._is_lazy is False
        assert np.any(concrete.data != 0)

    def test_use_case_8_basis_blade_rename(self, cl3):
        """Basis blades stay eager but can become lazy/named differently."""
        e1, _, _ = cl3.basis_vectors()
        E = e1.name("E")
        assert str(E) == "E"
        assert str(E.anon()) != "E"

    def test_use_case_9_symbolic_shorthand(self, cl3):
        """Symbolic shorthand over symbolic structure."""
        e1, e2, _ = cl3.basis_vectors()
        B = (e1 ^ e2).lazy()
        assert B._is_lazy is True

        B = B.name("B")
        assert str(B) == "B"

        assert str(B.anon()) != "B"

    def test_use_case_10_evaluate_without_losing_labels(self, cl3):
        """Evaluate without losing developer labels."""
        e1, e2, _ = cl3.basis_vectors()
        psi = (3 * e1 + 4 * e2).name("psi")
        psi_eval = psi.eager()
        assert str(psi_eval) == "psi"
        s = str(psi_eval.anon())
        assert s != "psi"
