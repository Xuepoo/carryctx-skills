# Troubleshooting

Common issues encountered when using CarryCtx and how to resolve them.

## Stale Lock

**Error message**: `error: lock file exists at <path>. If you are sure no other process is running, run 'carryctx lock remove'.`

**Cause**: A previous CarryCtx process crashed or was killed without releasing a file lock. CarryCtx uses file-based locking to prevent concurrent database access.

**Resolution**:

```
carryctx lock remove
```

This removes the lock file and allows the next operation to proceed. Only do this if you are certain no other CarryCtx process is running. Verify with:

```
ps aux | grep carryctx
```

## Database Migration Required

**Error message**: `error: database schema version X does not match expected version Y. Run 'carryctx migrate'.`

**Cause**: The installed CLI version is newer than the database schema. This happens after upgrading CarryCtx.

**Resolution**:

```
carryctx migrate
```

This applies any pending schema migrations. The database is backed up before migration. Migration is idempotent — running it multiple times is safe. The `state.sqlite` file is located at `<git-common-dir>/carryctx/state.sqlite`.

## Session Already Active

**Error message**: `warning: a session is already active (ID: <uuid>, started at <timestamp>). End it first with 'carryctx session end'.`

**Cause**: Attempting to start a new session while one is already ACTIVE. CarryCtx enforces a single active session per repository.

**Resolution**:

- **End the existing session**: `carryctx session end` (prompts for checkpoint).
- **Abandon the existing session**: `carryctx session abandon` (no checkpoint, discards progress).
- **Resume work**: if you want to continue the existing session, use `carryctx session resume` if paused, or just `carryctx resume` to see context.

## Task Already Claimed

**Error message**: `error: task CTX-NNNN is already claimed by <agent>. Use '--force' to override or contact <agent>.`

**Cause**: Attempting to claim a task that is already assigned to another agent. This prevents duplicate work.

**Resolution**:

- **Contact the claiming agent**: coordinate via your team's communication channel.
- **Force reassignment** (use with caution): `carryctx task claim CTX-NNNN --force`. This silently reassigns the task. Only do this if the other agent is confirmed to not be working on it.
- **Unclaim first**: ask the other agent to run `carryctx task unclaim CTX-NNNN` to release ownership.

## No Active Session

**Error message**: `error: no active session. Start one with 'carryctx session start'.`

**Cause**: Running a command that requires an active session (e.g. checkpoint, progress add) without one.

**Resolution**: `carryctx session start`

## Agent Not Registered

**Error message**: `error: agent '<name>' is not registered. Register with 'carryctx agent register --name <name>'.`

**Cause**: The agent identity used for `CARRYCTX_AGENT` or `--name` has not been registered.

**Resolution**: `carryctx agent register --name "$(whoami)" --provider "<provider>"`

## Worktree Already Exists

**Error message**: `error: a worktree for task CTX-NNNN already exists at <path>.`

**Cause**: Creating a worktree for a task that already has one.

**Resolution**:

- **Use the existing worktree**: `cd <path> && carryctx resume`
- **Force recreate**: `carryctx worktree create --task CTX-NNNN --force` (removes and recreates the worktree, then checks out the task branch)

## Command Not Found

**Error message**: `command not found: carryctx`

**Cause**: CarryCtx CLI is not installed or not on PATH.

**Resolution**:

- **Via Cargo**: `cargo install carryctx`
- **Via npm**: `npm install -g carryctx`
- **Verify**: `carryctx --version`

## Database Corruption

**Error message**: `error: database disk image is malformed` or `SQL logic error`.

**Cause**: The SQLite database was corrupted by a crash, concurrent write, or filesystem issue.

**Resolution**:

```
carryctx db repair
```

This runs SQLite recovery (`PRAGMA integrity_check`, `.recover`). If recovery fails, restore from the latest backup in `<git-common-dir>/carryctx/backups/`. CarryCtx automatically creates pre-migration backups.

## Unknown Worktree (Broken Symlink)

**Cause**: A worktree was deleted manually but CarryCtx still tracks it.

**Resolution**:

```
carryctx worktree prune
```

This scans all tracked worktrees, verifies they still exist, and removes missing ones from the database.

## Doctor Diagnostics

When you are unsure what is wrong, run the full diagnostic suite:

```bash
carryctx doctor
```

Output icons:
- `✓` — check passed
- `·` — informational (no action required)
- `⚠` — warning — something may need attention
- `✗` — error — action required

Common doctor findings:

| Finding | Meaning | Fix |
|---------|---------|-----|
| `No CarryCtx git hooks installed` | Hooks not set up | `carryctx hooks install` |
| `N task(s) have deleted owners` | Agent was removed but still owns tasks | `carryctx task unclaim <id>` |
| `Cannot open project` | DB missing or git not initialised | `carryctx init` |
| `No active session` | No session running | `carryctx session start` |

For machine-readable output (e.g. in CI): `carryctx doctor --json`

## Git Hooks Not Working

**Symptom**: Commits do not create checkpoints or prepend task IDs to commit messages.

**Cause**: CarryCtx hooks are not installed, or were overwritten by another tool.

**Resolution**:

```bash
carryctx hooks status   # check which hooks exist and whether CarryCtx manages them
carryctx hooks install --force  # reinstall (backs up existing hooks to .bak)
```

To verify a hook is managed by CarryCtx: `grep "CarryCtx" .git/hooks/post-commit`

## Completions Not Working

**Symptom**: Tab-completion for `carryctx` does not work in the shell.

**Resolution**: Re-run the one-time setup for your shell:

```bash
# Bash
carryctx completions bash >> ~/.bash_completion.d/carryctx
source ~/.bash_completion.d/carryctx

# Zsh
echo 'eval "$(carryctx completions zsh)"' >> ~/.zshrc && source ~/.zshrc

# Fish
carryctx completions fish > ~/.config/fish/completions/carryctx.fish
```
