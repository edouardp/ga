---
status: accepted
date: 2026-03-29
deciders: edouard
---

# ADR-038: Rumdl for Markdown Linting

## Context and Problem Statement

Documentation quality degrades over time — inconsistent formatting, trailing
whitespace, broken structure. The project has significant markdown in
packages/, CHANGELOG, and docs/.

## Decision Outcome

Use rumdl (Rust markdown linter) scoped to `packages/` and `CHANGELOG.md`.
Scratch docs, planning notes, and ADRs are excluded to avoid noise.

### Configuration

- `.rumdl.toml`: line length 200 (relaxed), allow mixed list markers,
  allow duplicate headings in different sections
- Runs via pre-commit hook and `make lint`

### Consequences

- Good, because it catches structural markdown issues
- Good, because scoping avoids noise from informal docs
- Bad, because ADRs and design docs aren't linted (acceptable trade-off)
