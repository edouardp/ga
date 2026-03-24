"""Tests for the ga library — golden tests and property tests."""

import pytest
import numpy as np
from ga import (
    Algebra, gp, op, left_contraction, right_contraction, hestenes_inner,
    scalar_product, reverse, involute, conjugate, grade, grades, scalar,
    dual, undual, norm2, norm, unit, inverse, commutator, anticommutator,
    is_scalar, is_vector, is_bivector, is_even, wedge, geometric_product, rev,
)


# ---- Fixtures ----

@pytest.fixture
def cl2():
    return Algebra((1, 1))

@pytest.fixture
def cl3():
    return Algebra((1, 1, 1))

@pytest.fixture
def sta():
    return Algebra((1, -1, -1, -1))


# ---- Phase 1: Algebra construction ----

class TestAlgebra:
    def test_cl3_dimensions(self, cl3):
        assert cl3.n == 3
        assert cl3.dim == 8
        assert cl3.signature == (1, 1, 1)

    def test_cl2_dimensions(self, cl2):
        assert cl2.n == 2
        assert cl2.dim == 4

    def test_sta_dimensions(self, sta):
        assert sta.n == 4
        assert sta.dim == 16
        assert sta.signature == (1, -1, -1, -1)

    def test_repr(self, cl3, sta):
        assert repr(cl3) == "Cl(3,0)"
        assert repr(sta) == "Cl(1,3)"

    def test_basis_vectors(self, cl3):
        e1, e2, e3 = cl3.basis_vectors()
        assert e1.data[1] == 1.0
        assert e2.data[2] == 1.0
        assert e3.data[4] == 1.0

    def test_pseudoscalar(self, cl3):
        I = cl3.pseudoscalar()
        assert I.data[7] == 1.0  # e123 = 0b111 = 7

    def test_blade_lookup(self, cl3):
        e12 = cl3.blade("e12")
        assert e12.data[3] == 1.0  # 0b011 = 3

    def test_scalar_constructor(self, cl3):
        s = cl3.scalar(5.0)
        assert s.data[0] == 5.0
        assert np.allclose(s.data[1:], 0)

    def test_vector_constructor(self, cl3):
        v = cl3.vector([1, 2, 3])
        assert v.data[1] == 1.0
        assert v.data[2] == 2.0
        assert v.data[4] == 3.0


# ---- Phase 2: Multivector basics ----

class TestMultivector:
    def test_add(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        r = e1 + e2
        assert r.data[1] == 1.0
        assert r.data[2] == 1.0

    def test_scalar_add(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        r = 3 + e1
        assert r.data[0] == 3.0
        assert r.data[1] == 1.0

    def test_sub(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        r = e1 - e2
        assert r.data[1] == 1.0
        assert r.data[2] == -1.0

    def test_scalar_mul(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        r = 3 * e1
        assert r.data[1] == 3.0

    def test_neg(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        r = -e1
        assert r.data[1] == -1.0

    def test_div(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        r = (2 * e1) / 2
        assert r.data[1] == 1.0

    def test_repr_nonzero(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        r = 3 + 2 * e1 - e2
        s = repr(r)
        assert "3" in s
        assert "e1" in s
        assert "e2" in s

    def test_repr_zero(self, cl3):
        z = cl3.scalar(0)
        assert repr(z) == "0"

    def test_algebra_mismatch(self, cl2, cl3):
        e1_2d = cl2.basis_vectors()[0]
        e1_3d = cl3.basis_vectors()[0]
        with pytest.raises(ValueError, match="different algebras"):
            gp(e1_2d, e1_3d)


# ---- Phase 3: Core operations ----

class TestGeometricProduct:
    def test_basis_vector_squares_cl3(self, cl3):
        """In Cl(3,0), e_i^2 = +1."""
        for e in cl3.basis_vectors():
            r = gp(e, e)
            assert np.isclose(scalar(r), 1.0)

    def test_basis_vector_squares_sta(self, sta):
        """In Cl(1,3), e0^2=+1, e1^2=e2^2=e3^2=-1."""
        vecs = sta.basis_vectors()
        assert np.isclose(scalar(gp(vecs[0], vecs[0])), 1.0)
        for i in range(1, 4):
            assert np.isclose(scalar(gp(vecs[i], vecs[i])), -1.0)

    def test_anticommutativity(self, cl3):
        """e_i * e_j = -e_j * e_i for i != j."""
        e1, e2, e3 = cl3.basis_vectors()
        assert gp(e1, e2) == -gp(e2, e1)
        assert gp(e1, e3) == -gp(e3, e1)
        assert gp(e2, e3) == -gp(e3, e2)

    def test_associativity(self, cl3):
        e1, e2, e3 = cl3.basis_vectors()
        a = 1 + 2 * e1
        b = e2 + 3 * e3
        c = e1 + e2 + e3
        assert gp(gp(a, b), c) == gp(a, gp(b, c))

    def test_distributivity(self, cl3):
        e1, e2, e3 = cl3.basis_vectors()
        a = e1 + e2
        b = e2
        c = e3
        assert gp(a, b + c) == gp(a, b) + gp(a, c)

    def test_pseudoscalar_square_cl3(self, cl3):
        """I^2 = -1 in Cl(3,0)."""
        I = cl3.pseudoscalar()
        assert np.isclose(scalar(gp(I, I)), -1.0)

    def test_operator_star(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        assert e1 * e2 == gp(e1, e2)


class TestOuterProduct:
    def test_basis_wedge(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        e12 = op(e1, e2)
        assert e12.data[3] == 1.0  # e12 = index 3

    def test_wedge_anticommutative(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        assert op(e1, e2) == -op(e2, e1)

    def test_wedge_self_zero(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        r = op(e1, e1)
        assert np.allclose(r.data, 0)

    def test_operator_xor(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        assert (e1 ^ e2) == op(e1, e2)


class TestContractions:
    def test_left_contraction_vector_bivector(self, cl3):
        e1, e2, e3 = cl3.basis_vectors()
        e12 = e1 ^ e2
        # e1 ⌋ e12 = e2
        r = left_contraction(e1, e12)
        assert r == e2

    def test_left_contraction_vector_vector(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        # e1 ⌋ e1 = 1 (dot product)
        r = left_contraction(e1, e1)
        assert np.isclose(scalar(r), 1.0)
        # e1 ⌋ e2 = 0
        r = left_contraction(e1, e2)
        assert np.isclose(scalar(r), 0.0)

    def test_right_contraction(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        e12 = e1 ^ e2
        # e12 ⌊ e2 = e1
        r = right_contraction(e12, e2)
        assert r == e1

    def test_hestenes_inner_vectors(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        assert np.isclose(scalar(hestenes_inner(e1, e1)), 1.0)
        assert np.isclose(scalar(hestenes_inner(e1, e2)), 0.0)

    def test_hestenes_inner_scalar_gives_zero(self, cl3):
        s = cl3.scalar(5.0)
        e1, _, _ = cl3.basis_vectors()
        r = hestenes_inner(s, e1)
        assert np.allclose(r.data, 0)

    def test_scalar_product(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        assert np.isclose(scalar(scalar_product(e1, e1)), 1.0)
        assert np.isclose(scalar(scalar_product(e1, e2)), 0.0)

    def test_operator_pipe(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        e12 = e1 ^ e2
        assert (e1 | e12) == left_contraction(e1, e12)


class TestUnaryOps:
    def test_reverse_vector(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        assert reverse(e1) == e1

    def test_reverse_bivector(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        e12 = e1 ^ e2
        assert reverse(e12) == -e12

    def test_reverse_product_identity(self, cl3):
        """reverse(a*b) == reverse(b) * reverse(a)."""
        e1, e2, e3 = cl3.basis_vectors()
        a = 1 + 2 * e1 + 3 * (e1 ^ e2)
        b = e2 + e3
        assert gp(reverse(b), reverse(a)) == reverse(gp(a, b))

    def test_involute(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        e12 = e1 ^ e2
        mv = 1 + e1 + e12
        inv = involute(mv)
        # scalar unchanged, vector negated, bivector unchanged
        assert np.isclose(inv.data[0], 1.0)
        assert np.isclose(inv.data[1], -1.0)
        assert np.isclose(inv.data[3], 1.0)

    def test_conjugate(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        # conjugate = involute(reverse(x))
        mv = 1 + e1
        assert conjugate(mv) == involute(reverse(mv))

    def test_tilde_operator(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        e12 = e1 ^ e2
        assert ~e12 == reverse(e12)


class TestGradeOps:
    def test_grade_projection(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        mv = 3 + 2 * e1 + (e1 ^ e2)
        assert grade(mv, 0) == cl3.scalar(3)
        assert grade(mv, 1) == 2 * e1
        assert grade(mv, 2) == e1 ^ e2

    def test_grade_idempotent(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        mv = 3 + 2 * e1 + (e1 ^ e2)
        assert grade(grade(mv, 1), 1) == grade(mv, 1)

    def test_grades_multi(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        mv = 3 + 2 * e1 + (e1 ^ e2)
        r = grades(mv, [0, 2])
        assert r == 3 + (e1 ^ e2)

    def test_scalar_extraction(self, cl3):
        mv = cl3.scalar(7.0)
        assert scalar(mv) == 7.0


class TestDualNormInverse:
    def test_dual_undual_roundtrip(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        assert undual(dual(e1)) == e1

    def test_norm_basis_vector(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        assert np.isclose(norm(e1), 1.0)

    def test_norm2_vector(self, cl3):
        v = cl3.vector([3, 4, 0])
        assert np.isclose(norm2(v), 25.0)

    def test_unit(self, cl3):
        v = cl3.vector([3, 4, 0])
        u = unit(v)
        assert np.isclose(norm(u), 1.0)

    def test_inverse_vector(self, cl3):
        e1, _, _ = cl3.basis_vectors()
        v = 2 * e1
        assert gp(v, inverse(v)) == cl3.scalar(1.0)

    def test_inverse_zero_raises(self, cl3):
        with pytest.raises(ValueError, match="not invertible"):
            inverse(cl3.scalar(0))


class TestPredicates:
    def test_is_scalar(self, cl3):
        assert is_scalar(cl3.scalar(5))
        assert not is_scalar(cl3.basis_vectors()[0])

    def test_is_vector(self, cl3):
        assert is_vector(cl3.vector([1, 2, 3]))
        assert not is_vector(cl3.scalar(1))

    def test_is_bivector(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        assert is_bivector(e1 ^ e2)
        assert not is_bivector(e1)

    def test_is_even(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        assert is_even(cl3.scalar(1) + (e1 ^ e2))
        assert not is_even(e1)


class TestAliases:
    def test_aliases(self, cl3):
        e1, e2, _ = cl3.basis_vectors()
        assert geometric_product(e1, e2) == gp(e1, e2)
        assert wedge(e1, e2) == op(e1, e2)
        assert rev(e1) == reverse(e1)


# ---- Golden tests: known identities ----

class TestGoldenCl2:
    """Known results in Cl(2,0)."""

    def test_complex_structure(self):
        alg = Algebra((1, 1))
        e1, e2 = alg.basis_vectors()
        e12 = e1 * e2
        # e12^2 = -1 (acts like imaginary unit)
        assert np.isclose(scalar(e12 * e12), -1.0)


class TestGoldenCl3:
    """Known results in Cl(3,0) — 3D Euclidean."""

    def test_cross_product_via_dual(self, cl3):
        """a × b = dual(a ∧ b) in 3D Euclidean (with our left-contraction dual)."""
        e1, e2, e3 = cl3.basis_vectors()
        # e1 × e2 should be e3
        w = op(e1, e2)
        cross = dual(w)
        assert cross == e3

    def test_rotation(self, cl3):
        """Rotate e1 by 90° in the e1e2 plane → e2."""
        e1, e2, e3 = cl3.basis_vectors()
        theta = np.pi / 2
        B = e1 ^ e2
        R = cl3.scalar(np.cos(theta / 2)) - np.sin(theta / 2) * B
        v_rot = gp(gp(R, e1), reverse(R))
        # Should be approximately e2
        assert np.allclose(v_rot.data, e2.data, atol=1e-12)


class TestGoldenSTA:
    """Known results in Cl(1,3) — Spacetime Algebra."""

    def test_timelike_spacelike(self, sta):
        vecs = sta.basis_vectors()
        # gamma_0^2 = +1
        assert np.isclose(scalar(vecs[0] * vecs[0]), 1.0)
        # gamma_1^2 = -1
        assert np.isclose(scalar(vecs[1] * vecs[1]), -1.0)

    def test_pseudoscalar_square(self, sta):
        """I^2 = -1 in Cl(1,3) with standard blade ordering."""
        I = sta.pseudoscalar()
        assert np.isclose(scalar(I * I), -1.0)
