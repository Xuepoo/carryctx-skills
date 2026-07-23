# CarryCtx Agent Skills

Agent skills collection for [CarryCtx](https://github.com/Xuepoo/carryctx) — a local-first project state and continuity manager for coding agents.

This repository provides modular, first-class CarryCtx awareness to AI coding agents (such as Antigravity, Claude Code, Cursor, Cline, etc.). Install only the skills you need.

## Installation

Install CarryCtx skills into your agent environment using the official `skills` CLI tool:

### 1. Interactive Installation (Select Multiple / All)

If you want to install all skills at once, simply run the command without specifying a skill. An interactive menu will appear allowing you to select all of them:

```bash
npx skills add https://github.com/Xuepoo/carryctx-skills
# (Press 'a' to select all, then 'Enter' to install)
```

### 2. Install Specific Skills (Headless)

If you only want specific modules, you can install them directly via the `--skill` flag:

```bash
# Add the Core CLI capability
npx skills add https://github.com/Xuepoo/carryctx-skills --skill carryctx-core -y

# Add other capabilities as needed:
npx skills add https://github.com/Xuepoo/carryctx-skills --skill carryctx-rules -y
npx skills add https://github.com/Xuepoo/carryctx-skills --skill carryctx-workflows -y
npx skills add https://github.com/Xuepoo/carryctx-skills --skill carryctx-personas -y
```

## Available Skills

| Skill | Description | Location | Status |
|-------|-------------|----------|--------|
| **`carryctx-core`** | Preserves and restores project context, manages tasks, tracks progress, and saves checkpoints across agent sessions. | [`skills/carryctx-core/`](skills/carryctx-core/) | Available |
| **`carryctx-rules`** | Teaches the agent to dynamically load and obey project-specific `.carryctx/rules/`. | [`skills/carryctx-rules/`](skills/carryctx-rules/) | *Planned* |
| **`carryctx-workflows`** | Parses `.carryctx/workflows/` blueprints and automatically breaks down tasks into granular todo lists. | [`skills/carryctx-workflows/`](skills/carryctx-workflows/) | *Planned* |
| **`carryctx-personas`** | Enables agents to adopt `.carryctx/personas/` (e.g., Code Reviewer, Architect) and enforce specific code styles. | [`skills/carryctx-personas/`](skills/carryctx-personas/) | *Planned* |

## Skill Structure

```text
carryctx-skills/
├── README.md
├── LICENSE
└── skills/
    ├── carryctx-core/        # Basic CLI wrapping
    │   ├── SKILL.md
    │   ├── references/
    │   └── scripts/
    ├── carryctx-personas/    # Agent role adoption
    │   └── SKILL.md
    ├── carryctx-rules/       # Context-aware rule loading
    │   └── SKILL.md
    └── carryctx-workflows/   # Blueprint parsing
        └── SKILL.md
```

## License

[MIT](LICENSE)
