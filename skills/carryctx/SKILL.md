---
name: carryctx
description: Persistent project context and continuity manager for coding agents. Helps agents manage structured tasks, track progress, save checkpoints, maintain context across sessions and Git worktrees, generate shell completions, and integrate Git hooks. Use when starting work, tracking task progress, creating checkpoints, switching worktrees, restoring project state, or diagnosing project health.
license: MIT
metadata:
  author: Xuepoo
  version: "0.2.0"
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
- **Diagnosing health issues**: Run `carryctx doctor` to surface orphaned tasks, missing hooks, and DB problems.
- **Setting up shell completions**: Run `carryctx completions <shell>` once per machine for tab-completion.
- **Installing git hooks**: Run `carryctx hooks install` to auto-checkpoint on every commit.
- **Pruning old data**: Use `carryctx project prune` to clean up completed tasks and keep the DB lightweight.
- **Remote Synchronization**: Use `carryctx sync push` or `pull` to sync state across machines or branches.
- **Agent Analytics**: Use `carryctx stats` to audit agent session lengths and task metrics.

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
| **Doctor** | `carryctx doctor` | Diagnose project health |
| **Install Hooks** | `carryctx hooks install` | Auto-checkpoint on every git commit |
| **Shell Completions** | `carryctx completions <shell>` | Enable tab-completion |
| **Prune Data** | `carryctx project prune --older-than 30` | Clean up old completed tasks |
| **Sync State** | `carryctx sync push/pull --remote <path>` | Synchronize DB state with a remote |
| **Agent Stats** | `carryctx stats` | View agent session time and performance metrics |

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
# Clean up the worktree to save disk space if one was created
# git worktree remove .worktrees/CTX-0001
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

### 7. Diagnosing Project Health

Run `carryctx doctor` after upgrades, after switching machines, or when commands behave unexpectedly:

```bash
carryctx doctor           # human-readable diagnostics with fix hints
carryctx doctor --json    # machine-readable output
carryctx doctor --fix     # attempt automatic repairs
```

Doctor checks:
- Global config validity
- Git repository connectivity
- CarryCtx git hook installation
- SQLite database connection and schema version
- Orphaned tasks (tasks whose owner agent no longer exists)
- Active session count

### 8. Git Hooks Integration (optional, recommended)

Install once per repository to auto-checkpoint on every commit and prefix commit messages with the active task ID:

```bash
carryctx hooks install            # installs post-commit + prepare-commit-msg
carryctx hooks install --force    # overwrite existing hooks (backs up originals)
carryctx hooks status             # verify installed hooks
carryctx hooks uninstall          # remove CarryCtx hooks
carryctx hooks uninstall --restore  # restore original hooks from .bak
```

### 9. Project Maintenance, Sync, and Auditing

For long-running projects, you can use advanced commands to maintain a clean database and measure metrics:

```bash
# Prune completed tasks older than 30 days
carryctx project prune --older-than 30

# Sync the SQLite state DB to a remote backend (e.g. /tmp/remote-store)
carryctx sync push --remote /tmp/remote-store
carryctx sync pull --remote /tmp/remote-store

# View analytics and session time for agents
carryctx stats
```

### 10. Shell Tab-Completion (one-time setup per machine)

```bash
# Bash
carryctx completions bash >> ~/.bash_completion.d/carryctx

# Zsh (add to ~/.zshrc)
eval "$(carryctx completions zsh)"

# Fish
carryctx completions fish > ~/.config/fish/completions/carryctx.fish

# PowerShell
carryctx completions powershell | Out-String | Invoke-Expression
```

## Best Practices for Coding Agents

1. **Always run `carryctx resume` when starting**: Re-orients agent to current task and progress immediately.
2. **Explicitly claim tasks**: Prevents duplicate execution when multiple agents work on the same repository.
3. **Use structured progress items**: Keep `todo`, `done`, and `block` updated during execution steps.
4. **Checkpoint before stopping**: Always create a checkpoint before yielding control or completing complex multi-step work.
5. **Run `carryctx doctor` on first use or after upgrade**: Surfaces setup gaps before they cause runtime errors.
6. **Install git hooks on project setup**: `carryctx hooks install` ensures every commit automatically captures a checkpoint without manual intervention.
