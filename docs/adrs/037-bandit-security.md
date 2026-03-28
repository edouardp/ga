---
status: accepted
date: 2026-03-29
deciders: edouard
---

# ADR-037: Bandit for Security Scanning

## Context and Problem Statement

Python code can contain security anti-patterns (hardcoded secrets, unsafe
deserialization, overly broad exception handling) that linters don't catch.

## Decision Outcome

Use Bandit to scan `packages/` for security issues. Tests and examples excluded.

### Configuration

- `.bandit` YAML config excludes tests, examples, .venv
- One intentional `# nosec B110` in `simplify.py` (try/except/pass for
  expression evaluation fallback)
- Runs via pre-commit hook and `make lint`

### Consequences

- Good, because it catches security issues early
- Good, because it's clean on first run (only 1 intentional suppression)
- Neutral, because it only scans Python (shell/markdown covered by other tools)
