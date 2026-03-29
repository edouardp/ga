from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_polarisation_notebook_does_not_embed_gm_calls_inside_markdown_cells():
    """Ensure gm.md() calls are not nested inside mo.md() markdown cells."""
    source = (ROOT / "examples" / "physics" / "polarisation.py").read_text()

    assert 'mo.md(r"""\n    gm.md(' not in source
    assert 'gm.md(t"\\"\\"' not in source


def test_polarisation_notebook_uses_explicit_latex_naming_over_raw_positional_strings():
    """Verify latex labels use the latex= keyword arg, not positional .name() calls."""
    source = (ROOT / "examples" / "physics" / "polarisation.py").read_text()

    assert 'latex=r"R_{45^\\circ}"' in source
    assert 'latex=r"e_{12}"' in source
    assert '.name(r"R_{45\\degree}")' not in source
    assert ".name(r'e_{12}')" not in source


def test_polarisation_notebook_uses_private_temporaries_in_repeated_marimo_cells():
    """Check that repeated cell-local variables use underscore-prefixed names to avoid redeclaration."""
    source = (ROOT / "examples" / "physics" / "polarisation.py").read_text()

    assert "    N = n_slider.value" not in source
    assert "    step_deg = 90.0 / N" not in source
    assert "    E = e1.eval()" not in source
    assert "    for i in range(1, N + 1):" not in source
    assert "    I_out = norm(E) ** 2" not in source
    assert "    theory = np.cos(np.radians(step_deg)) ** (2 * N)" not in source


def test_polarisation_notebook_avoids_mathtext_in_matplotlib_plot_labels():
    """Ensure matplotlib labels don't use raw LaTeX mathtext strings."""
    source = (ROOT / "examples" / "physics" / "polarisation.py").read_text()

    assert "label=r'$\\frac{1}{4}\\sin^2(2\\theta)$'" not in source
    assert "label=r'$\\cos^{2N}(90°/N)$'" not in source


def test_rotations_from_bivectors_notebook_uses_principle_driven_sections():
    """Verify the notebook keeps the teaching structure and includes a failure-mode control."""
    source = (ROOT / "examples" / "algebra" / "rotations_from_bivectors.py").read_text()

    assert "# Rotations from Bivectors" in source
    assert "## Domain Grounding" in source
    assert "## GA Formulation" in source
    assert "## Minimal Math" in source
    assert "## Code Layer" in source
    assert "## Validation" in source
    assert 'options=["unit bivector", "raw wedge"]' in source
    assert 'label="generator"' in source


def test_rotations_from_bivectors_notebook_uses_gm_md_only_for_interpolated_markdown():
    """Static explanatory sections should use marimo markdown rather than gm.md()."""
    source = (ROOT / "examples" / "algebra" / "rotations_from_bivectors.py").read_text()

    assert source.count('gm.md(t"""') == 2
    assert 'mo.md(r"""' in source
    assert "# Rotations from Bivectors" in source
    assert "## Domain Grounding" in source
    assert "## GA Formulation" in source
    assert "## Minimal Math" in source
    assert "## Domain Check" in source
