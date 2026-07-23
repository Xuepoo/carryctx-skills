---
name: carryctx-workflows
description: Parses workflow blueprints from .carryctx/workflows/ and automatically generates structured task steps. Helps agents translate high-level tasks into detailed standard operating procedures (SOPs).
---

# Skill: CarryCtx Workflows

You are equipped with the ability to execute Standard Operating Procedures (SOPs) defined by the project.

## Your Directives

1. **Blueprint Discovery**: When assigned a high-level task (e.g., "Add a new API route", "Create a new database migration"), check if the `.carryctx/workflows/` directory exists in the project.
2. **Parsing Blueprints**: If a blueprint file matches the intent of the task (e.g., `api-route.md`, `new-component.md`), read it to understand the required sequence of steps.
3. **Task Breakdown**: Do not try to hold the entire workflow in your memory. To ensure absolute traceability, do not skip steps. Break down the workflow into Todo items in your current task:

   ```bash
   todo_json="$(carryctx progress todo "Run unit tests" --json)"
   progress_id="$(printf '%s' "$todo_json" | jq -r '.id')"
   ```

4. **Sequential Execution**:
   - Execute the step exactly as described in the workflow blueprint.
   - Wait for it to complete. Check for errors.
   - Mark the step as complete using its ID:
     ```bash
     carryctx progress complete "$progress_id"
     ```
   - Only then move to the next step.
