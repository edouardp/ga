---
status: accepted
date: 2026-03-29
deciders: edouard
---

# ADR-035: Ruff for Python Linting and Formatting

## Context and Problem Statement

The project had no automated code quality enforcement. Inconsistent formatting,
unused imports, and unsorted imports accumulated across 30+ Python files.

## Decision Outcome

Use Ruff as the single Python lint and format tool. It replaces flake8, isort,
pyupgrade, and black in one fast Rust-based tool.

### Configuration

- Target: Python 3.11 (galaga's minimum)
- Line length: 120
- Rules: E, W, F, I, B, UP
- Suppressed: E501 (line length via setting), E741/E743 (GA uses `I`, `l`),
  E402 (circular imports), E701 (compact dispatch tables)
- Examples excluded (marimo notebooks have non-standard structure)

### Consequences

- Good, because one tool handles lint + format + import sorting
- Good, because it's fast (~100ms for the whole project)
- Good, because auto-fix resolves most issues
- Neutral, because formatting changes make git blame noisy for one commit
