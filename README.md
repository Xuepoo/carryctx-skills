# CarryCtx Agent Skills

Agent skills collection for [CarryCtx](https://github.com/Xuepoo/carryctx) — a local-first project state and continuity manager for coding agents.

[![MIT](https://img.shields.io/badge/license-MIT-6366f1.svg)](./LICENSE)
[![skills.sh](https://skills.sh/b/Xuepoo/carryctx-skills)](https://skills.sh/Xuepoo/carryctx-skills)

This repository is a skills catalog for AI coding agents such as Codex, Claude Code, Cursor, GitHub Copilot, and other agents supported by the [Vercel Labs Skills CLI](https://github.com/vercel-labs/skills).

## Install with `skills`

List available skills:

```bash
npx skills add Xuepoo/carryctx-skills --list
```

Install all skills for all detected agents:

```bash
npx skills add Xuepoo/carryctx-skills --all
```

Install selected skills for specific agents:

```bash
npx skills add Xuepoo/carryctx-skills \
  --skill carryctx-core \
  --skill carryctx-rules \
  --skill carryctx-workflows \
  --skill carryctx-personas \
  --skill carryctx-handoff \
  --agent codex \
  --agent claude-code \
  --agent cursor \
  --agent github-copilot
```

Use one skill without installing it:

```bash
npx skills use Xuepoo/carryctx-skills --skill carryctx-core
```

The Skills CLI supports GitHub shorthand (`owner/repo`), full GitHub URLs, direct skill paths, local paths, and agent-specific installs. See the upstream CLI README for current options and supported agents: <https://github.com/vercel-labs/skills>.

## Available Skills

| Skill                    | Description                                                                                                                                                                                    | Location                                                   | Status    |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------- |
| **`carryctx-core`**      | Preserves and restores project context, manages tasks, tracks progress, and saves checkpoints across agent sessions.                                                                           | [`skills/carryctx-core/`](skills/carryctx-core/)           | Available |
| **`carryctx-rules`**     | Teaches the agent to dynamically load and obey project-specific `.carryctx/rules/`.                                                                                                            | [`skills/carryctx-rules/`](skills/carryctx-rules/)         | Available |
| **`carryctx-workflows`** | Parses `.carryctx/workflows/` blueprints and automatically breaks down tasks into granular todo lists.                                                                                         | [`skills/carryctx-workflows/`](skills/carryctx-workflows/) | Available |
| **`carryctx-personas`**  | Enables agents to adopt `.carryctx/personas/` (e.g., Code Reviewer, Architect) and enforce specific code styles.                                                                               | [`skills/carryctx-personas/`](skills/carryctx-personas/)   | Available |
| **`carryctx-handoff`**   | Produces a handoff-prompt document from CarryCtx state (tasks, checkpoints, decisions, progress) and routes it with `carryctx handoff create` — pairs with the generic `handoff-prompt` skill. | [`skills/carryctx-handoff/`](skills/carryctx-handoff/)     | Available |

## 🎁 Presets Library

Not sure how to write your own Personas, Rules, or Workflows? We've got you covered!

This repository includes a `presets/` folder containing out-of-the-box, battle-tested templates. You can simply copy these into your project's `.carryctx/` directory to instantly upgrade your AI team.

```bash
# Example: Copy the strict Code Reviewer persona into your project
cp -r node_modules/carryctx-skills/presets/personas/reviewer.md .carryctx/personas/
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
