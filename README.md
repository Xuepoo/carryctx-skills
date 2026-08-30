# CarryCtx Agent Skills

Agent skills collection for [CarryCtx](https://github.com/Xuepoo/carryctx) — a local-first project state and continuity manager for coding agents.

[![MIT](https://img.shields.io/badge/license-MIT-6366f1.svg)](./LICENSE)
[![skills.sh](https://skills.sh/b/Xuepoo/carryctx-skills)](https://skills.sh/Xuepoo/carryctx-skills)

This repository is a skills catalog for AI coding agents such as Codex, Claude Code, Cursor, GitHub Copilot, and other agents supported by the [Vercel Labs Skills CLI](https://github.com/vercel-labs/skills). CarryCtx provides local-first, durable project lifecycle management for commander/subagent teams: the harness still executes agents, while CarryCtx persists tasks, roles, sessions, checkpoints, handoffs, cleanup requests, and audit state.

## Install with `skills`

List available skills:

```bash
npx skills add Xuepoo/carryctx-skills --list
```

Install for all detected agents:

```bash
npx skills add Xuepoo/carryctx-skills --all
```

Install the skill for specific agents:

```bash
npx skills add Xuepoo/carryctx-skills \
  --skill use-carryctx \
  --agent codex \
  --agent claude-code \
  --agent cursor \
  --agent github-copilot
```

Use it without installing:

```bash
npx skills use Xuepoo/carryctx-skills --skill use-carryctx
```

The Skills CLI supports GitHub shorthand (`owner/repo`), full GitHub URLs, direct skill paths, local paths, and agent-specific installs. See the upstream CLI README for current options and supported agents: <https://github.com/vercel-labs/skills>.

## Available Skills

One skill, loaded once per main session, covering the shipped CarryCtx v0.8.0 surface:

| Skill              | Description                                                                                                                                                                                                                          | Location                                       | Status    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- | --------- |
| **`use-carryctx`** | Commander doctrine and command surface: plan as the commander, assign durable tasks with dependencies and teams, dispatch implementation to subagents in per-task Git worktrees, accept results by reading state back from CarryCtx. | [`skills/use-carryctx/`](skills/use-carryctx/) | Available |

## 🎁 Presets Library

Not sure how to write your own Personas, Rules, or Workflows? We've got you covered!

This repository includes a `presets/` folder containing out-of-the-box, battle-tested templates. You can simply copy these into your project's `.carryctx/` directory to instantly upgrade your AI team — or install them through the CLI:

```bash
carryctx preset install /path/to/presets/workflows/bugfix.json
carryctx preset apply workflows/bugfix
```

## Skill Structure

```text
carryctx-skills/
├── README.md
├── LICENSE
├── presets/                  # 🎁 Library of ready-to-use templates
│   ├── personas/
│   ├── rules/
│   └── workflows/
└── skills/
    └── use-carryctx/         # Commander doctrine + full CLI reference
        ├── SKILL.md          # Thin router: doctrine + quick reference
        └── references/       # Focused operational guides
            ├── task-lifecycle.md
            ├── team-coordination.md
            ├── sessions-and-checkpoints.md
            ├── handoffs.md
            ├── presets-rules-personas.md
            └── troubleshooting.md
```

## License

[MIT](LICENSE)
