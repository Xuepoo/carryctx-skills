---
name: carryctx-workflows
description: Parses workflow blueprints from .carryctx/workflows/ and automatically generates structured task steps. Helps agents translate high-level tasks into detailed standard operating procedures (SOPs).
license: MIT
metadata:
  author: Xuepoo
  version: "0.2.0"
---

# CarryCtx Workflows Skill

This skill allows the Agent to use predefined workflow blueprints to break down complex tasks.

## How it works (Future Implementation)
When fully implemented:
1. If the user asks to "Add a new API endpoint", the Agent looks for `.carryctx/workflows/api-endpoint.toml`.
2. The Agent translates the blueprint steps into granular `carryctx progress todo` commands automatically.
