---
name: carryctx-rules
description: Dynamic context-aware rule loader for CarryCtx. Teaches the agent to automatically load and apply domain-specific rules and guidelines from the project's .carryctx/rules/ directory depending on the task at hand. Use to enforce project guidelines and improve accuracy.
license: MIT
metadata:
  author: Xuepoo
  version: "0.2.0"
---

# CarryCtx Rules Skill

This skill teaches the Agent how to interpret and apply dynamic rules defined within the project.

## How it works (Future Implementation)
When this skill is fully implemented, agents will be instructed to:
1. Upon starting a task, check `.carryctx/rules/` for relevant domain instructions (e.g., `frontend.md`, `database.md`).
2. Automatically incorporate those rules into their context to ensure compliance with project standards.
