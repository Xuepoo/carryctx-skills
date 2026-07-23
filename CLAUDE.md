# CarryCtx — Claude Code Integration Guide

This project uses **CarryCtx** (`carryctx`) for persistent project context and continuity management across coding-agent sessions.

## Mandatory Session Protocol

Every time you start working in this repository, execute the following sequence:

```bash
# 1. Register/confirm agent identity
carryctx agent current --name "claude" \
  || carryctx agent register --name "claude" --provider "claude-code"

# 2. Start a tracked session
carryctx session start

# 3. Load current context
carryctx resume
```

`carryctx resume` will tell you:
- The active task (title, description, status, owner)
- Recent progress items (todos, blockers, done items)
- The last checkpoint (what was done, what remains)
- Related worktrees and dependent tasks

## Task Tracking

Before beginning any new piece of work, ensure a task exists and is claimed:

```bash
carryctx task list --status ready        # see what is unstarted
carryctx task claim CTX-NNNN            # assign to yourself
carryctx task start CTX-NNNN            # mark in-progress
```

## Logging Progress

Log significant steps continuously — do not accumulate changes in implicit memory:

```bash
carryctx progress todo "Step to do next"
carryctx progress done "Step just completed"
carryctx progress block "Blocker encountered: <description>"
carryctx progress risk "Potential risk: <description>"
carryctx progress note "Architectural note worth recording"
```

## Checkpointing

Create a checkpoint:
- Before ending any session
- Before switching tasks or worktrees
- After completing a meaningful sub-goal
- When handing off to another agent

```bash
carryctx checkpoint \
  --done "What was just completed" \
  --remaining "What still needs to be done" \
  --blocker "Any current blockers (or 'None')"
```

## Ending a Session

```bash
# Create final checkpoint first, then end session
carryctx session end
```

## Diagnosing Problems

If commands fail unexpectedly or context is missing, run:

```bash
carryctx doctor
```

This checks git connectivity, database health, orphaned tasks, active sessions, and hook installation.

## Git Hooks (if not already installed)

```bash
carryctx hooks install   # auto-checkpoint on commit, auto-prefix commit msgs with task ID
```

## Shell Completions (one-time setup)

```bash
eval "$(carryctx completions bash)"   # or zsh/fish/powershell
```

## Key Commands Reference

| Situation | Command |
|-----------|---------|
| Start of session | `carryctx session start && carryctx resume` |
| What's my task? | `carryctx status` |
| Mark step done | `carryctx progress done "..."` |
| Save progress | `carryctx checkpoint --done "..." --remaining "..."` |
| End of session | `carryctx session end` |
| Project unhealthy | `carryctx doctor` |
| New task | `carryctx task create --title "..."` |
| Parallel work | `carryctx worktree create --task CTX-NNNN` |
