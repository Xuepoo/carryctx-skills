---
name: use-carryctx
description: Commander doctrine and full command surface for CarryCtx 0.7.x, the local-first project context engine for coding agents. Load once per main session for any multi-step engineering effort — plan as the commander, assign work through durable carryctx tasks with dependencies and teams, dispatch all implementation to subagents (each preferably isolated in its own Git worktree), and accept results by reading state back from carryctx instead of trusting subagent self-reports. Covers tasks, dependencies, teams, sessions, checkpoints, handoffs, presets/rules/personas, search, events, graph, stats, MCP, doctor, and troubleshooting.
license: MIT
metadata:
  author: Xuepoo
  version: "1.0.0"
---

# Use CarryCtx

CarryCtx is a local-first project context engine: durable tasks, sessions,
checkpoints, decisions, teams, and handoffs stored in SQLite under the Git common
dir (`<git-common-dir>/carryctx/state.sqlite`), shared by every agent and linked
worktree on the repository. It is a **management and persistence layer, not an
orchestration runtime** — spawning processes, retries, and concurrency limits
belong to you and your harness. This skill is loaded once per main session.

## When to Apply

Apply at main-session start for any multi-step engineering effort, especially:

> **Prerequisite — run inside the target Git repository.** Every carryctx
> command must execute from within that project's repo clone (state lives at
> `<git-common-dir>/carryctx/state.sqlite`). From a non-repo directory every
> command fails with `GIT_ERROR` exit 4. In multi-repo workspaces, `cd` into
> each product repository first — state is per-repo, never workspace-wide.

- Planning and splitting an effort into tasks with dependencies and owners.
- Dispatching implementation to subagents while keeping your own context lean.
- Running parallel work streams that need isolation (Git worktrees).
- Continuing prior work: restoring context, accepting handoffs, finding past
  decisions and checkpoints by content.

## Commander Doctrine

You (the main-session agent) are the **commander**. Subagents implement; you do
not. The loop:

1. **Plan** — decompose the goal into tasks with explicit dependencies and
   scopes. Small one-line fixes stay inline; batching tightly-coupled tasks to
   one subagent beats fan-out.
2. **Assign** — encode the plan durably in carryctx so nothing depends on your
   conversation surviving: `task create` with `--depends-on`, `--team`,
   `--required-role`, and `task scope add` for conflict detection.
3. **Dispatch** — give each subagent exactly its slice: a task ID plus
   `carryctx team context <team> --agent-for <sub>` output. Prefer running each
   subagent in its own worktree: `carryctx worktree create <TASK_REF>` creates
   `<path>/.worktrees/<task-id>` on a `carryctx/<task-id>` branch.
4. **Accept & verify** — never trust a subagent's self-report. Read state back:
   `team status`, `team context`, `task show`, `search`. Verify the diff and run
   the tests yourself before `task complete`.

Supporting rules:

- **Record durably because subagents die silently.** A process killed before its
  final checkpoint leaves nothing behind. Require subagents to append
  `progress todo/note/block/risk`, `checkpoint`, and `decision add` records as
  they work — `team context` can only rebuild what was written down.
- **Keep your own context lean.** Outline before reading files, prefer compact
  output (`--compact`, `--fields display_id,status,title`), re-read
  `team status` between rounds instead of holding state in conversation.
- **Close what you open.** A task left `in_progress` after its agent stops is
  indistinguishable from active work; end sessions cleanly, checkpoint before
  merging branches away.

Bootstrap once, then operate the loop:

```bash
carryctx init                                            # first time only
carryctx agent register --name "$(whoami)" --provider opencode --kind commander
carryctx session start
carryctx resume --compact                                # restore prior context

carryctx task create --title "Backend API" --team core --required-role backend
carryctx task create --title "Login form" --depends-on CTX-0002
carryctx worktree create CTX-0002                        # isolate implementation
```

## Command Quick Reference

All flags below verified against carryctx 0.7.0. Writes require identity: pass
`--agent <name>` (or export `CARRYCTX_AGENT`) — listings never filter by it
implicitly.

| Action          | Command                                                                                                                | Notes                                                                     |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Initialize      | `carryctx init`                                                                                                        | Config `.carryctx/config.toml`; state in Git common dir                   |
| Register agent  | `carryctx agent register --name sub-1 --provider opencode --kind subagent --role backend`                              | `--kind`: `commander` \| `subagent`                                       |
| Bootstrap       | `carryctx session start` then `carryctx resume --compact`                                                              | One ACTIVE session per agent; `--reuse` keeps the live one                |
| Snapshot        | `carryctx status --compact [--sessions]`                                                                               | Branch, HEAD, active tasks                                                |
| Create task     | `carryctx task create --title "..." [--priority high] [--team core] [--required-role backend] [--depends-on CTX-0001]` | Planned until strong deps complete                                        |
| List tasks      | `carryctx task list [--status ready] [--mine] [--limit N]`                                                             | Statuses: planned ready in_progress blocked in_review completed cancelled |
| Claim / start   | `carryctx task claim CTX-0001` then `carryctx task start CTX-0001`                                                     | Multiple in-progress tasks allowed                                        |
| Dependency      | `carryctx task depend CTX-0002 --on CTX-0001 [--kind informational]`                                                   | `strong` gates claim/start; `informational` records only                  |
| File scope      | `carryctx task scope add CTX-0002 src/api/`; `scope list`; `scope conflicts CTX-0002`                                  | Detect overlapping edits before fan-out                                   |
| Task ↔ team     | `carryctx task team set CTX-0002 --team core` (`unset` to clear)                                                       | Bookkeeping only; never touches lifecycle                                 |
| Block / unblock | `carryctx task block CTX-0002 --reason "..."` / `unblock CTX-0002`                                                     | Visible in `team context`                                                 |
| Complete        | `carryctx task complete CTX-0002`                                                                                      | After you verified the result                                             |
| Progress item   | `carryctx progress todo\|note\|block\|risk "..." --task CTX-0002`                                                      | Durable breadcrumbs                                                       |
| Resolve item    | `carryctx progress complete PX-0001`                                                                                   |                                                                           |
| Checkpoint      | `carryctx checkpoint --done "..." --remaining "..." --task CTX-0002`                                                   | Immutable snapshot; also `--blocker/--risk/--note`                        |
| Decision        | `carryctx decision add --title "..." --rationale "..." --task CTX-0002`                                                | `--rationale` is the searchable why                                       |
| Create team     | `carryctx team create --name core --commander cmd-1`                                                                   | Commander auto-joins as member                                            |
| Membership      | `carryctx team member add core --agent sub-1 --role backend`                                                           | `team commander set core --agent X` / `--clear`                           |
| Team status     | `carryctx team status [core]`                                                                                          | Read-only: members, sessions, active tasks                                |
| Team context    | `carryctx team context [core] [--agent-for sub-1] [--task CTX-0002]`                                                   | Read-only rebuild from durable records                                    |
| Worktree create | `carryctx worktree create CTX-0002`                                                                                    | `.worktrees/<task-id>` on branch `carryctx/<task-id>`                     |
| Worktree remove | `carryctx worktree remove <TASK_REF\|PATH> [--force]`                                                                  | `--force` discards dirty worktrees; `worktree list` for refs              |
| Handoff create  | `carryctx handoff create --target sub-1 --task CTX-0002 --summary "..."`                                               | Target resolves name, ULID, or role                                       |
| Handoff inbox   | `carryctx handoff list` then `accept HO-0001 [--claim-task]`                                                           | Default shows pending only; `--all`/`--status` widen                      |
| Search history  | `carryctx search "<query>" [--type task\|progress\|checkpoint\|decision]`                                              | FTS5 syntax; hits cite owning task                                        |
| Event audit     | `carryctx event list [--cursor <token>] [--since 1h]`                                                                  | Cursor tokens are opaque; `--agent` filters explicitly                    |
| Diagnose        | `carryctx doctor [--fix]`                                                                                              | Warnings-only findings still exit 0                                       |
| Auxiliary       | `carryctx mcp`; `graph scan` / `graph export -t mermaid [--focus src/main.rs]`; `stats --markdown`                     | Stdio MCP server (answers ping); AST dep graph; analytics                 |

## References

Read the focused guide when operating in that area:

- [references/task-lifecycle.md](references/task-lifecycle.md) — states,
  transitions, dependency gating, scopes, team metadata.
- [references/team-coordination.md](references/team-coordination.md) — team
  semantics, read-only projections, dispatch patterns, recording discipline.
- [references/sessions-and-checkpoints.md](references/sessions-and-checkpoints.md)
  — session lifecycle, stale detection, checkpoint policy.
- [references/handoffs.md](references/handoffs.md) — writing and taking over
  handoffs, routing documents, accept/reject/close.
- [references/presets-rules-personas.md](references/presets-rules-personas.md) —
  installing SOPs, domain rules, and personas into `.carryctx/`.
- [references/troubleshooting.md](references/troubleshooting.md) — error codes,
  recovery, diagnostics.
