---
name: carryctx-workflows
description: Parses workflow blueprints from .carryctx/workflows/ and automatically generates structured task steps. Helps agents translate high-level tasks into detailed standard operating procedures (SOPs).
license: MIT
metadata:
  author: Xuepoo
  version: "0.2.0"
---

# CarryCtx Workflows Skill

This skill teaches you how to break down complex, high-level tasks using predefined blueprints (Standard Operating Procedures) created by the project team.

## Instructions for the Agent

1. **Blueprint Discovery**: When assigned a high-level task (e.g., "Add a new API route", "Create a new database migration"), check if the `.carryctx/workflows/` directory exists in the project.
2. **Parsing Blueprints**: If a blueprint file matches the intent of the task (e.g., `api-route.md`, `new-component.md`), read it to understand the required sequence of steps.
3. **Task Breakdown (Integration with carryctx-core)**: Do not try to hold the entire workflow in your memory. Instead, translate the steps from the blueprint into granular, trackable items using the `carryctx-core` CLI. Run `carryctx progress todo "<step description>"` for each major step defined in the workflow blueprint.
4. **Sequential Execution**: Proceed through the generated `todo` list sequentially. As you finish each step, strictly mark it as complete using `carryctx progress done <id>`. Do not skip any steps outlined in the blueprint unless explicitly instructed by the user.
