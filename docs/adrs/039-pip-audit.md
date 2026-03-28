---
status: accepted
date: 2026-03-29
deciders: edouard
---

# ADR-039: Pip-audit for Dependency Vulnerability Scanning

## Context and Problem Statement

Dependencies can have known security vulnerabilities (CVEs). Without scanning,
these go unnoticed until a downstream user or audit flags them.

## Decision Outcome

Use pip-audit to check installed packages against the PyPI advisory database.
Runs as a non-blocking warning in `make lint` because fixes depend on upstream.

### Current Status

One CVE in pygments (transitive dependency via marimo). No fix available yet.

### Consequences

- Good, because it surfaces known vulnerabilities
- Good, because it's non-blocking — doesn't prevent development when upstream
  hasn't released a fix
- Neutral, because it only checks PyPI advisories (not GitHub advisories)
