---
name: carryctx-personas
description: Allows the agent to adopt specific personas and roles (e.g., Code Reviewer, Architect) defined in .carryctx/personas/. Modifies agent behavior, strictness, and code style output based on the active role.
license: MIT
metadata:
  author: Xuepoo
  version: "0.2.0"
---

# CarryCtx Personas Skill

This skill allows you to dynamically adopt different roles, strictness levels, or "personas" based on the project's configurations.

## Instructions for the Agent

1. **Persona Discovery**: Be aware that the project may define specific AI personas in the `.carryctx/personas/` directory (e.g., `reviewer.md`, `architect.md`, `qa-engineer.md`).
2. **Role Adoption**: When explicitly asked by the user to adopt a persona (e.g., "Act as the Architect"), or when your current task strongly aligns with a specific persona (e.g., you are asked to rigorously review a Pull Request), immediately read the corresponding persona file.
3. **Behavior Modification**: Adjust your communication style, reasoning process, strictness, and output format to exactly match the persona's definition. 
   - *Example*: If acting as a strict Security Reviewer, prioritize pointing out vulnerabilities over code style, and refuse to approve code that lacks input validation.
4. **Persistence**: Maintain this persona for the duration of the task or until the user instructs you to revert to your default behavior.
