---
name: carryctx
description: Helps coding agents persist and restore project context across sessions, manage tasks, track progress, and coordinate work across Git worktrees.
---

# CarryCtx Agent Skill

Helps coding agents persist and restore project context across sessions, manage tasks, track progress, and coordinate work across Git worktrees.

## Prerequisites

- [CarryCtx CLI](https://github.com/Xuepoo/carryctx) installed (`cargo install carryctx` or `npm install -g carryctx`)
- A Git repository initialized with `carryctx init`

## Quick Start

1. **Register as an agent**: `carryctx agent register --name "$(whoami)" --provider "claude-code"`
2. **Set as current agent**: `carryctx agent current --name "$(whoami)"` or set env `CARRYCTX_AGENT=$(whoami)`
3. **Start a session**: `carryctx session start`
4. **Resume context**: `carryctx resume` — shows current task, checkpoint, progress, and next actions
5. **End session**: `carryctx session end` — optionally creates a checkpoint first

## Workflow

### Starting Work

```
carryctx session start          # or carryctx resume --start-session
carryctx resume                 # get current context
```

### Creating Tasks

```
carryctx task create --title "Implement login page"
carryctx task create --title "Add tests" --depends-on CTX-0001
carryctx task claim CTX-0001    # claim ownership
carryctx task start CTX-0001    # begin work
```

### Tracking Progress

```
carryctx progress todo "Design database schema"
carryctx progress done "Research requirements"
carryctx progress block "Waiting for API review"
carryctx progress risk "Third-party dependency may change"
carryctx progress note "Consider using Redis for caching"
```

### Checkpoints (save state)

```
carryctx checkpoint \
  --done "Implemented login page" \
  --remaining "Add password reset" \
  --blocker "Waiting for API review"
```

### Session Management

```
carryctx session start
carryctx session pause
carryctx session resume
carryctx session end          # prompts for checkpoint
```

### Context & Status

```
carryctx status               # project overview
carryctx status --mine         # my tasks only
carryctx resume                # current task context
carryctx context               # full relevance-ordered context
```

## Best Practices

1. **Start a session** before beginning work — this tracks what you're doing
2. **Create checkpoints** at meaningful boundaries — they capture Git state + semantic progress
3. **Use progress items** liberally — todos, blockers, risks, and notes are structured
4. **Claim tasks** explicitly — prevents duplicate work across agents
5. **Use worktrees** for parallel task work — `carryctx worktree create --task CTX-0001`
6. **End sessions properly** — ending prompts for a checkpoint, ensuring continuity

## Configuration

See `carryctx config list` for current settings. Key settings:

- `agent.default_name` — default agent identity
- `session.stale_after` — how long before a session is marked stale (default: 2h)
- `context.default_mode` — compact or full context output
