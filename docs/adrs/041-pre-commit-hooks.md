---
status: accepted
date: 2026-03-29
deciders: edouard
---

# ADR-041: Pre-commit Hooks for Automated Quality Gates

## Context and Problem Statement

Linting tools are only useful if they run consistently. Relying on developers
to remember `make lint` before committing leads to drift.

## Decision Outcome

Use pre-commit to run all quality checks automatically on `git commit`.

### Hooks

| Hook | Source | What it checks |
|---|---|---|
| trailing-whitespace | pre-commit-hooks | Trailing whitespace |
| end-of-file-fixer | pre-commit-hooks | Missing newline at EOF |
| check-yaml | pre-commit-hooks | Valid YAML |
| check-toml | pre-commit-hooks | Valid TOML |
| check-added-large-files | pre-commit-hooks | Accidentally committed binaries |
| check-merge-conflict | pre-commit-hooks | Unresolved merge markers |
| detect-private-key | pre-commit-hooks | Accidentally committed keys |
| ruff | ruff-pre-commit | Python lint (with --fix) |
| ruff-format | ruff-pre-commit | Python formatting |
| shellcheck | shellcheck-py | Shell script lint |
| bandit | bandit | Security scanning |
| rumdl | local | Markdown lint |
| checkmake | local | Makefile lint |

### Consequences

- Good, because quality is enforced automatically
- Good, because `--fix` hooks auto-correct trivial issues
- Neutral, because `--no-verify` bypass is available when needed
- Bad, because first-time setup requires `uv run pre-commit install`
