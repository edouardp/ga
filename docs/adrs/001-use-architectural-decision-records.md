---
status: accepted
date: 2026-03-25
deciders: edouard
---

# ADR-001: Use Architectural Decision Records

## Context and Problem Statement

How do we document and track architectural decisions made in this project so
that future contributors understand why certain choices were made?

## Decision Drivers

* Preserve rationale for API design choices
* Mathematical conventions need explicit justification
* Avoid revisiting decisions without understanding original constraints

## Considered Options

1. MADR (Markdown Any Decision Records)
2. Code comments only
3. No formal documentation

## Decision Outcome

Chosen option: "MADR" because it provides a lightweight, version-controlled
format that lives with the code and follows a consistent structure.

### Consequences

* Good, because decisions are version-controlled alongside code
* Good, because markdown is readable without special tools
* Good, because the template ensures consistent documentation
