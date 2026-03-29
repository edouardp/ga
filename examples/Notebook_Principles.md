# 📘 Geometric Algebra Example Notebook Principles

## 🎯 Purpose

Each notebook must simultaneously teach:

1. The **real-world/domain concept**
2. The **GA formulation**
3. The **library usage**

The notebook is not an API demo — it is a **conceptual learning tool**.

------

# 🧠 Core Principles

## 1. Concept-first, not API-first

- Start from the **real-world phenomenon**
- Introduce GA as the **natural model**
- Introduce code as **notation for the model**

------

## 2. One idea per notebook

- Each notebook teaches **one core concept**
- No mixing multiple abstraction levels
- Keep scope tight and focused

------

## 3. Use the 3-layer model

Every notebook must include:

- **Domain layer** — what is happening in reality
- **GA layer** — how GA models it
- **Code layer** — how to implement it

And must loop:

```
Domain → GA → Code → Domain (validation)
```

------

## 4. Progressive reveal

Structure concepts in order:

1. Intuition (no symbols)
2. Minimal math
3. Code
4. Exploration

Avoid dumping full algebra up front.

------

## 5. Minimal necessary math

- Use only the math required to understand the concept
- Avoid long derivations unless essential
- Prefer clarity over completeness

------

## 6. Multiple representations

Show the same idea in multiple forms:

- Geometry (visual)
- Algebra (GA expression)
- Code (library usage)

Optional:

- Matrix / traditional equivalent

------

## 7. Make invariants explicit

Always show what is preserved:

- magnitude
- angle
- structure

Users should see what “correct” means.

------

## 8. Validate back to reality

Always confirm:

- results match expected physical/domain behaviour
- outputs are interpretable in real-world terms

------

## 9. Prefer construction over definition

- Build concepts from simpler operations
- Name them after they are understood

Example:

- two reflections → rotation → “rotor”

------

## 10. Distinguish clearly

Always separate:

- object (bivector)
- generator (Lie algebra element)
- operator (rotor)
- action (sandwich product)

------

## 11. Avoid abstraction jumps

Do not jump directly to:

- Lie theory
- Spin groups
- STA

Unless the notebook is explicitly about them.

------

# 🎛️ Interactivity Principles (marimo)

## 12. Interactivity must be meaningful

Every control must map to:

- a geometric parameter
- a physical quantity

No arbitrary sliders.

------

## 13. Use four interaction types

- **Sliders** → continuous parameters (angles, magnitudes)
- **Toggles** → structural changes (normalisation, metric)
- **Dropdowns** → object selection (vectors, planes)
- **Failure controls** → break assumptions

------

## 14. Maintain the interaction loop

Every interactive notebook must support:

```
User input
→ geometry updates
→ algebra updates
→ invariants visible
→ intuition improves
```

------

## 15. Synchronise views

When interactive, update together:

- visual output (plot)
- symbolic expression
- numeric values

------

## 16. Include failure modes

Deliberately allow:

- incorrect inputs
- broken assumptions

Show:

- what fails
- why it fails

------

## 17. Do not overuse interactivity

Avoid it when:

- it adds no intuition
- concept is purely structural
- it distracts from clarity

------

# 🧩 Notebook Structure (required)

Each notebook should follow this structure:

## 1. Title + claim

- Clear statement of what is being demonstrated

------

## 2. Domain grounding

- Describe the real-world behaviour
- What should happen and why

------

## 3. Traditional approach (optional)

- Show non-GA method briefly
- Highlight complexity or limitations

------

## 4. GA formulation

- Map domain → GA objects
- Explain roles (vector, bivector, rotor, etc.)

------

## 5. Minimal math

- Present only key equations

------

## 6. Code implementation

- Show equivalent library usage
- Map code to concepts

------

## 7. Interactive exploration (if applicable)

- Add meaningful controls
- Visualise results

------

## 8. Validation

- Confirm behaviour matches expectations
- Show invariants

------

## 9. Failure cases

- Show incorrect usage and consequences where appropriate

------

## 10. Extension

- Suggest next step or generalisation

------

# ⚠️ Anti-Patterns (must avoid)

- API-first explanations
- Symbol-heavy “math dumps”
- Multiple concepts in one notebook
- Interactivity without meaning
- No connection back to real-world behaviour
- No validation or invariants
- Static notebooks where interaction would help

------

# 🧭 Final Guiding Principle

Each notebook must answer:

> **Why is GA the natural way to understand this problem?**

Not:

> “How do I use this GA library?”
