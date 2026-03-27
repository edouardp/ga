## Plan: Configurable Notation System

### Problem

GA has many competing notations (reverse as ~x, x̃, x†, x^†; dual as x*, x⋆, Ix; etc.). We've chosen good defaults, but users need to override them — especially when following
a specific textbook or convention.

Currently, rendering decisions are scattered across ga/render.py in hardcoded dicts (_POSTFIX_UNICODE, _COMPOUND_FALLBACK, _POSTFIX_LATEX_FMT, _BINARY_UNICODE, etc.). There's
no way to change them without editing the renderer.

### Design

A Notation class that encapsulates all rendering decisions for every expression node type. The renderer queries the Notation object instead of hardcoded tables. The Algebra
holds a Notation instance, and the renderer receives it as a parameter.

### Notation Entry Types

Each operation needs a rendering rule for each of three formats (ascii, unicode, latex). The rule type depends on the operation's visual form:

1. Prefix: ~x, inv(x) — a string prepended, optionally with wrapping
2. Postfix: x†, x⁻¹, x² — a string appended
3. Accent (over/under): x̃ (combining char), \tilde{x} / \widetilde{x} — a decoration above/below, with single-char (combining) and multi-char (prefix fallback) variants
4. Infix: a∧b, a·b — a symbol between two operands
5. Wrap: ⟨x⟩₁, ‖x‖, exp(x) — open/close delimiters around content
6. Juxtaposition: ab — no symbol, smart spacing

python
@dataclass
class NotationRule:
    """How to render one operation in one format."""
    kind: Literal["prefix", "postfix", "accent", "infix", "wrap", "juxtaposition"]
    # For prefix/postfix: the symbol string
    symbol: str = ""
    # For accent: combining char (single-char operand) and fallback prefix (compound)
    combining: str = ""
    fallback_prefix: str = ""
    # For accent latex: \tilde vs \widetilde
    latex_cmd: str = ""
    latex_wide_cmd: str = ""
    # For wrap: open and close delimiters
    open: str = ""
    close: str = ""
    # For infix: the separator
    separator: str = ""


### Notation Class

python
class Notation:
    """Configurable rendering rules for all GA operations."""

    def __init__(self):
        # Populate with defaults
        self._rules: dict[type, dict[str, NotationRule]] = {}
        self._load_defaults()
    
    def rule(self, node_type: type, fmt: str) -> NotationRule:
        """Get the rendering rule for a node type and format ('ascii'/'unicode'/'latex')."""
    
    def set_rule(self, node_type: type, fmt: str, rule: NotationRule):
        """Override a rendering rule."""
    
    def configure(self, node_type: type, **kwargs):
        """Convenience: set rules from keyword args."""
        # e.g. notation.configure(Reverse, unicode_combining="̃", unicode_fallback="~",
        #                         latex_cmd=r"\tilde", latex_wide_cmd=r"\widetilde")


### Presets

python
Notation.default()          # Current rendering
Notation.doran_lasenby()    # Doran & Lasenby textbook conventions
Notation.hestenes()         # Hestenes conventions


### Integration

1. Algebra gets a notation parameter and property:
  python
   alg = Algebra((1,1,1), notation=Notation.default())
   alg.notation.configure(Reverse, unicode_combining="†", latex_cmd=r"\dagger")


2. render() and render_latex() accept an optional Notation:
  python
   def render(node: Expr, notation: Notation | None = None) -> str:


3. Multivector.__str__() and .latex() pass self.algebra.notation to the renderer.

### Task Breakdown

Task 1: NotationRule dataclass and Notation class (standalone, no renderer dependency)

- Define NotationRule with all fields for the 6 rule kinds
- Define Notation with rule(), set_rule(), configure() methods
- Populate defaults matching current hardcoded behavior
- Extensive unit tests: every operation × every format × atom vs compound

Task 2: Unit tests for Notation (write first)

- Test default rules match current rendering for every node type
- Test overriding individual rules
- Test accent rules: combining char for atoms, fallback for compounds
- Test infix rules: symbol, spacing
- Test wrap rules: open/close delimiters
- Test preset configurations

Task 3: Wire Notation into the renderer

- Replace all hardcoded dicts in ga/render.py with Notation lookups
- render(node, notation) and render_latex(node, notation) accept notation
- Verify all existing render tests still pass

Task 4: Wire Notation into Algebra and Multivector

- Add _notation to Algebra.__slots__, default to Notation.default()
- Add notation property on Algebra
- Multivector.__str__() and .latex() pass notation to renderer
- Algebra.__init__ accepts optional notation= parameter

Task 5: Presets and documentation

- Implement 2-3 notation presets
- Add ADR documenting the design
- Update README with notation configuration examples
- Update rendering gallery notebook to show notation switching

### Scope

This is a medium-sized refactor. The Notation class and tests (Tasks 1-2) are self-contained. Wiring it in (Tasks 3-4) touches render.py, algebra.py, and test files. Presets (
Task 5) are additive.

Estimated: ~400 lines of new code, ~200 lines of tests, ~100 lines of docs.