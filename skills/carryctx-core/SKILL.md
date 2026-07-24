---
name: carryctx-core
description: Core CarryCtx capability. Persistent project context and continuity manager for coding agents. Helps agents manage structured tasks, track progress, save checkpoints, maintain context across sessions and Git worktrees. Use when starting work, tracking task progress, creating checkpoints, switching worktrees, scanning code dependency graphs, running MCP stdio servers, applying presets, or restoring project state.
license: MIT
metadata:
  author: Xuepoo
  version: "0.2.0"
---

# CarryCtx Core Skill

CarryCtx provides first-class project state and context continuity for AI coding agents. It enables agents to manage tasks, track granular progress, create checkpoint snapshots, maintain AST code dependency graphs, run stdio MCP servers, apply workflow presets, and seamlessly preserve context across session restarts and Git worktrees.

## When to Apply

Use CarryCtx commands when:
- **Starting a new task or session**: Register agent identity, start session, and restore context (`carryctx resume`).
- **Managing project tasks**: Create, claim, start, complete, block, or cancel tasks (`carryctx task ...`).
- **Tracking granular progress**: Record structured `todo`, `block`, `risk`, and `note` items.
- **Saving state / Checkpointing**: Capture current work progress, git status, and remaining work before ending sessions or switching focus.
- **Code Graph Exploration**: Scan AST module dependencies (`carryctx graph scan`) and export Mermaid/DOT/ASCII diagrams (`carryctx graph export`).
- **AI Agent Tool Integration (MCP)**: Expose project context to Cursor / Windsurf / AGY via Model Context Protocol stdio server (`carryctx mcp`).
- **Standardizing Workflows (Presets)**: List, inspect, and apply project workflow blueprints, coding rules, and agent personas (`carryctx preset ...`).
- **Parallel task work**: Create and isolate tasks in dedicated Git worktrees (`carryctx worktree ...`).
- **Diagnosing health issues**: Run `carryctx doctor` to surface orphaned tasks, missing hooks, and DB problems.
- **Pruning old data**: Use `carryctx project prune` to clean up completed tasks and keep the DB lightweight.
- **Agent Analytics**: Use `carryctx stats` to audit agent session lengths, task metrics, and export Markdown/CSV reports.

## Prerequisites

1. Install CarryCtx CLI (`cargo install carryctx` or pre-built binary).
2. Initialize CarryCtx in the project repository: `carryctx init`.

## Quick Reference

| Action | Command | Purpose |
|--------|---------|---------| 
| **Agent Setup** | `carryctx agent register --name "$(whoami)" --provider "claude-code"` | Register agent identity |
| **Current Agent** | `carryctx agent current` | Show active agent identity |
| **Start Session** | `carryctx session start` | Begin tracked working session |
| **Resume Context** | `carryctx resume` | Fetch current task, progress & next actions |
| **Create Task** | `carryctx task create --title "..." [--depends-on CTX-0001]` | Define a new task |
| **Claim Task** | `carryctx task claim CTX-0001` | Assign task to current agent |
| **Start Task** | `carryctx task start CTX-0001` | Mark task as in-progress |
| **Track Progress** | `carryctx progress <todo\|block\|risk\|note> "..."` | Record structured progress item |
| **Checkpoint** | `carryctx checkpoint --done "..." --remaining "..."` | Save semantically rich state snapshot |
| **Scan Code Graph** | `carryctx graph scan` | Extract AST dependencies into SQLite graph |
| **Export Graph** | `carryctx graph export --type <mermaid\|dot\|ascii\|json>` | Render dependency graph (PNG/SVG/ASCII) |
| **MCP Stdio Server** | `carryctx mcp` | Launch MCP stdio server with 6 agent tools |
| **Apply Preset** | `carryctx preset apply <preset_name>` | Inject workflow SOPs, rules, or personas |
| **Worktree** | `carryctx worktree create CTX-0001` | Create isolated git worktree for task |
| **End Session** | `carryctx session end` | Safely end session with checkpoint |
| **Doctor** | `carryctx doctor` | Diagnose project health |
| **Install Hooks** | `carryctx hooks install` | Auto-checkpoint on every git commit |
| **Prune Data** | `carryctx project prune --older-than 30` | Clean up old completed tasks |
| **Agent Stats** | `carryctx stats [--markdown] [--output file.csv]` | View metrics and export performance reports |
| **Decision** | `carryctx decision add --title "..." --task CTX-0001` | Record architectural decision |
| **Handoff** | `carryctx handoff create --target <agent> --task CTX-0001` | Transfer work between agents |
| **Session Pause** | `carryctx session pause` | Pause active session timer |
| **Session Resume** | `carryctx session resume` | Resume a paused session |

## Standard Agent Workflow

### 1. Session Initialization & Context Restoration

At the start of any interaction or after an agent restart:

```bash
# Register & set identity if not already configured
carryctx agent current || carryctx agent register --name "claude" --provider "claude-code"

# Start session and load current context
carryctx session start
carryctx resume
```

To pause and resume sessions:

```bash
carryctx session pause    # Pause active session (timer stops)
carryctx session resume   # Resume a paused session
carryctx session end      # End session with optional checkpoint
carryctx session abandon  # End session without checkpoint
```

### 2. Code Dependency Analysis (Graph Subsystem)

Before modifying code or refactoring modules:

```bash
# 1. Scan codebase AST dependencies
carryctx graph scan

# 2. Export sub-graph centered around a specific module
carryctx graph export --type mermaid --focus "src/application/stats.rs" --depth 2

# 3. Export module-level compact ASCII architectural overview
carryctx graph export --type ascii --compact
```

### 3. Workflow Presets & Rule Injection

Inject standard operating procedures or coding guidelines:

```bash
# List available workflow presets
carryctx preset list

# Apply a standard bugfix workflow preset to current project
carryctx preset apply workflows/bugfix
```

### 4. Task Lifecycle

```bash
# List open tasks
carryctx task list --status ready

# Claim & start task
carryctx task claim CTX-0001
carryctx task start CTX-0001

# Mark task finished after verification
carryctx task complete CTX-0001
```

### 5. Granular Progress Tracking

As work progresses, log structured progress items:

```bash
carryctx progress todo "Write unit test for auth middleware"
carryctx progress todo "Implement JWT token validation"
carryctx progress block "Waiting for API endpoint spec confirmation"
carryctx progress risk "Breaking change in upstream dependency"
carryctx progress note "Used LRU cache to optimize token lookups"
# Mark a todo as completed:
carryctx progress complete PX-0001
```

### 6. Creating Checkpoints

Save state before ending a session, switching tasks, or handing off work:

```bash
carryctx checkpoint \
  --done "Finished backend authentication endpoints" \
  --remaining "Frontend login form integration" \
  --blocker "None"
```

### 7. Worktree Parallelism

When working on independent tasks simultaneously:

```bash
carryctx worktree create CTX-0002
# Switches to isolated worktree directory linked to CTX-0002
```


### 7a. Recording Decisions & Handoffs

Capture architectural decisions and hand off work between agents:

```bash
# Record an architectural decision (ADR) linked to a task
carryctx decision add --title "Use SQLite for storage" --task CTX-0001

# List or search decisions
carryctx decision list
carryctx decision search --keyword SQLite

# Mark a decision as superseded by a newer one
carryctx decision supersede DEC-0001 --by DEC-0002

# Create a handoff to transfer work to another agent
carryctx handoff create --target <agent-ulid> --summary "Implement the API" --task CTX-0001

# Accept, reject, or close a handoff
carryctx handoff accept HO-0001
carryctx handoff reject HO-0001 --reason "Not my area"
carryctx handoff close HO-0001
```

### 8. Ending Session & Reporting

```bash
# End working session
carryctx session end

# Export project stats report for PR description or documentation
carryctx stats --markdown --output /tmp/project_stats.md
```

### 9. Model Context Protocol (MCP) Integration

To hook CarryCtx directly into Cursor / Windsurf / AGY:

```json
{
  "mcpServers": {
    "carryctx": {
      "command": "carryctx",
      "args": ["mcp"]
    }
  }
}
```

Exposed MCP Tools:
- `carryctx_graph_explorer`: Query, scan, and export the project Context Graph
- `carryctx_context_manager`: Manage persistent context, checkpoints, and state snapshots
- `carryctx_task_manager`: Manage project tasks, dependencies, and priorities
- `carryctx_progress_tracker`: Manage task progress, notes, and blockers
- `carryctx_decision_logger`: Log and search architectural decision records
- `carryctx_project_admin`: Manage project database, stats, cold storage archiving, and config

### 10. Debugging & Troubleshooting

Enable structured debug logging to diagnose issues:

```bash
# Show debug logs for CarryCtx operations
export RUST_LOG=carryctx=debug
carryctx task list          # See debug output before command results

# Show only errors
export RUST_LOG=error
carryctx status

# Run diagnostics
carryctx doctor             # Check project health
carryctx doctor --json      # Machine-readable diagnostic output
```

## Best Practices for Coding Agents

1. **Always run `carryctx resume` when starting**: Re-orients agent to current task and progress immediately.
2. **Scan code graph before large refactors**: `carryctx graph scan` prevents broken upstream dependencies.
3. **Explicitly claim tasks**: Prevents duplicate execution when multiple agents work on the same repository.
4. **Use structured progress items**: Keep `todo`, `done`, and `block` updated during execution steps.
5. **Checkpoint before stopping**: Always create a checkpoint before yielding control or completing complex multi-step work.
6. **Run `carryctx doctor` on first use or after upgrade**: Surfaces setup gaps before they cause runtime errors.
