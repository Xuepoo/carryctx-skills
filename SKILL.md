---
name: carryctx
description: Persistent project context and continuity manager for coding agents. Helps agents manage structured tasks, track progress, save checkpoints, and maintain context across sessions and Git worktrees. Use when starting work, tracking task progress, creating checkpoints, switching worktrees, or restoring project state.
license: MIT
metadata:
  author: Xuepoo
  version: "0.1.0"
---

# CarryCtx Agent Skill

CarryCtx provides first-class project state and context continuity for AI coding agents. It enables agents to manage tasks, track granular progress, create checkpoint snapshots, and seamlessly preserve context across session restarts, window changes, and Git worktrees.

## When to Apply

Use CarryCtx commands when:
- **Starting a new task or session**: Register agent identity, start session, and restore context.
- **Managing project tasks**: Create, claim, start, complete, block, or cancel tasks.
- **Tracking granular progress**: Record structured `todo`, `done`, `block`, `risk`, and `note` items.
- **Saving state / Checkpointing**: Capture current work progress, git status, and remaining work before ending sessions or switching focus.
- **Parallel task work**: Create and isolate tasks in dedicated Git worktrees without context collision.
- **Context restoration**: Query relevance-ordered project state (`carryctx resume` or `carryctx status`).

## Prerequisites

1. Install CarryCtx CLI (`cargo install carryctx` or `npm install -g carryctx`).
2. Initialize CarryCtx in the project repository: `carryctx init`.

## Quick Reference

| Action | Command | Purpose |
|--------|---------|---------|
| **Agent Setup** | `carryctx agent register --name "$(whoami)" --provider "claude-code"` | Register agent identity |
| **Current Agent** | `carryctx agent current --name "$(whoami)"` | Set active agent |
| **Start Session** | `carryctx session start` | Begin tracked working session |
| **Resume Context** | `carryctx resume` | Fetch current task, progress & next actions |
| **Create Task** | `carryctx task create --title "..." [--depends-on CTX-0001]` | Define a new task |
| **Claim Task** | `carryctx task claim CTX-0001` | Assign task to current agent |
| **Start Task** | `carryctx task start CTX-0001` | Mark task as in-progress |
| **Track Progress** | `carryctx progress <todo\|done\|block\|risk\|note> "..."` | Record structured progress item |
| **Checkpoint** | `carryctx checkpoint --done "..." --remaining "..."` | Save semantically rich state snapshot |
| **Worktree** | `carryctx worktree create --task CTX-0001` | Create isolated git worktree for task |
| **End Session** | `carryctx session end` | Safely end session with checkpoint |

## Standard Agent Workflow

### 1. Session Initialization & Context Restoration

At the start of any interaction or after an agent restart:

```bash
# Register & set identity if not already configured
carryctx agent current --name "claude" || carryctx agent register --name "claude" --provider "claude-code"

# Start session and load current context
carryctx session start
carryctx resume
```

### 2. Task Lifecycle

```bash
# List open tasks
carryctx task list --status ready

# Claim & start task
carryctx task claim CTX-0001
carryctx task start CTX-0001

# Mark task finished after verification
carryctx task complete CTX-0001
```

### 3. Granular Progress Tracking

As work progresses, log structured progress items instead of keeping implicit memory:

```bash
carryctx progress todo "Write unit test for auth middleware"
carryctx progress done "Implemented JWT token validation"
carryctx progress block "Waiting for API endpoint spec confirmation"
carryctx progress risk "Breaking change in upstream dependency"
carryctx progress note "Used LRU cache to optimize token lookups"
```

### 4. Creating Checkpoints

Save state before ending a session, switching tasks, or handing off work:

```bash
carryctx checkpoint \
  --done "Finished backend authentication endpoints" \
  --remaining "Frontend login form integration" \
  --blocker "None"
```

### 5. Worktree Parallelism

When working on independent tasks simultaneously:

```bash
carryctx worktree create --task CTX-0002
# Switches to isolated worktree directory linked to CTX-0002
```

### 6. Ending Session

```bash
carryctx session end
```

## Best Practices for Coding Agents

1. **Always run `carryctx resume` when starting**: Re-orients agent to current task and progress immediately.
2. **Explicitly claim tasks**: Prevents duplicate execution when multiple agents work on the same repository.
3. **Use structured progress items**: Keep `todo`, `done`, and `block` updated during execution steps.
4. **Checkpoint before stopping**: Always create a checkpoint before yielding control or completing complex multi-step work.
