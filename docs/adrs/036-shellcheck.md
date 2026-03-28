---
status: accepted
date: 2026-03-29
deciders: edouard
---

# ADR-036: Shellcheck for Shell Script Linting

## Context and Problem Statement

The project has shell scripts in `scripts/` (publish, release, lint). Shell
scripts are easy to get subtly wrong (quoting, word splitting, portability).

## Decision Outcome

Use shellcheck to lint all `.sh` files in `scripts/`.

### Configuration

- Suppressed: SC2016 (expressions in single quotes — intentional), SC1091
  (can't follow sourced files — shellcheck limitation with dynamic paths)
- Runs via pre-commit hook and `make lint`

### Consequences

- Good, because it catches real shell bugs (unquoted variables, etc.)
- Good, because it's zero-config for our scripts
- Neutral, because SC1091 means sourced files aren't checked transitively
