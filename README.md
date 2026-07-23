# CarryCtx Agent Skills

Agent skills repository for [CarryCtx](https://github.com/Xuepoo/carryctx) — a local-first project state and continuity manager for coding agents.

This repository provides first-class CarryCtx awareness to AI coding agents (such as Antigravity, Claude Code, Cursor, Cline, etc.).

## Installation

Install the CarryCtx skill into your agent environment using the official `skills` CLI tool:

### Via `npx skills` (Recommended)

```bash
# Add to project scope
npx skills add Xuepoo/carryctx-skills -y

# Or specify by full URL
npx skills add https://github.com/Xuepoo/carryctx-skills --skill carryctx

# Add globally (user-level)
npx skills add Xuepoo/carryctx-skills -g -y
```

### Via `skills` CLI (if installed globally)

```bash
skills add Xuepoo/carryctx-skills -y
```

## Available Skills

| Skill | Description | Location |
|-------|-------------|----------|
| **`carryctx`** | Preserves and restores project context, manages tasks, tracks progress, and saves checkpoints across agent sessions. | [`skills/carryctx/`](skills/carryctx/) |

## Skill Structure

```
carryctx-skills/
├── README.md
├── LICENSE
└── skills/
    └── carryctx/
        ├── SKILL.md
        ├── references/
        │   ├── checkpoint-policy.md
        │   ├── session-lifecycle.md
        │   ├── task-workflow.md
        │   └── troubleshooting.md
        └── scripts/
            ├── create-checkpoint.sh
            └── start-session.sh
```

## License

[MIT](LICENSE)
