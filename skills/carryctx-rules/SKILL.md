---
name: carryctx-rules
description: Dynamic context-aware rule loader for CarryCtx. Teaches the agent to automatically load and apply domain-specific rules and guidelines from the project's .carryctx/rules/ directory depending on the task at hand. Use to enforce project guidelines and improve accuracy.
license: MIT
metadata:
  author: Xuepoo
  version: "0.2.0"
---

# CarryCtx Rules Skill

This skill enforces context-aware, domain-specific rules defined by the project team. It ensures you (the Agent) do not guess formatting, architectural conventions, or library choices, but instead read the project's source of truth.

## Instructions for the Agent

1. **Rule Discovery**: At the beginning of any new task, check if the project contains a `.carryctx/rules/` directory. If it exists, list its contents to find rule files that might be relevant to your current assignment.
2. **Context Injection**: If a rule file matches your current task domain (e.g., `frontend.md` for UI work, `database.md` for SQL/schema tasks, `security.md` for authentication), read its contents immediately before making any code changes.
3. **Strict Adherence**: Treat the contents of the read rule files as **absolute constraints**. Do not deviate from the specified conventions.
4. **Handoff**: If you need to delegate sub-tasks to a subagent, explicitly pass the relevant rule file paths to them so they are also bound by the same project rules.
