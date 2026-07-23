---
name: carryctx-personas
description: Allows the agent to adopt specific personas and roles (e.g., Code Reviewer, Architect) defined in .carryctx/personas/. Modifies agent behavior, strictness, and code style output based on the active role.
license: MIT
metadata:
  author: Xuepoo
  version: "0.2.0"
---

# CarryCtx Personas Skill

This skill teaches the Agent how to adopt highly specific roles/personas defined by the project team.

## How it works (Future Implementation)
When fully implemented:
1. Projects can define personas in `.carryctx/personas/reviewer.toml` or `architect.toml`.
2. The Agent can be instructed to "Act as the Architect" or "Review this code using the Reviewer persona", instantly applying the project's custom system prompt modifiers.
