---
name: use-carryctx
description: >
  Coordinate multi-step coding work across agents with CarryCtx, the
  local-first durable project lifecycle manager. Load once per main session when planning
  or coordinating engineering work: plan as the commander, assign durable tasks
  with dependencies, teams, and scopes, dispatch implementation to subagents in
  isolated Git worktrees, and accept results by reading state back from
  carryctx instead of trusting subagent self-reports.
license: MIT
metadata:
  author: Xuepoo
  version: "1.3.0"
  min_carryctx: "0.11.0"
---

# Use CarryCtx

CarryCtx is local-first durable project lifecycle management for commander/subagent
teams. It persists tasks, roles, sessions, checkpoints, handoffs, cleanup outbox
requests, and audit state in `<git-common-dir>/carryctx/state.sqlite`, shared by
every agent and linked worktree on the repository. The harness still executes
agents and controls spawning, routing, retries, and concurrency; CarryCtx is the
management and persistence layer, not a generic Automation Engine or Completion
Gates system. This skill is loaded once per main session.

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
- **Merge state deliberately; transport stays the user's job.** Linked worktrees
  share one database, so nothing merges between them. Cross-clone state moves
  through `export` / `import` plus user-run Git transport (`git push`/`fetch`),
  and concurrent work merges three-way via `import --mode merge` — see
  [Cross-Clone Sync & Merge](#cross-clone-sync--merge). Never push an unredacted
  snapshot ref to a public repository.

Bootstrap once, then operate the loop:

```bash
carryctx init                                            # first time only
carryctx agent register --name "$(whoami)" --provider opencode --kind commander
carryctx session start
carryctx resume --compact                                # restore prior context

carryctx task create --title "Backend API" --team core --required-role backend
carryctx task create --title "Login form" --depends-on CTX-0002
carryctx worktree create CTX-0002                          # isolate implementation
```

## Core Commands

Flags below are verified against CarryCtx v0.11.0. Writes require identity: pass
`--agent <name>` (or export `CARRYCTX_AGENT`) — listings never filter by it
implicitly.

```bash
# Plan & track
carryctx task create --title "..." [--priority high] [--team core] \
    [--required-role backend] [--depends-on CTX-0001]
carryctx task show CTX-0002                              # full detail + records
carryctx task claim CTX-0002 && carryctx task start CTX-0002
carryctx task complete CTX-0002                          # after agent/harness verification; transitions task and attempts configured cleanup
carryctx task edit CTX-0002 --title "..." --force         # audited terminal correction

# Read team state back (never trust self-reports)
carryctx team status [core]
carryctx team context [core] [--agent-for sub-1] [--task CTX-0002]

# Durable breadcrumbs written by subagents as they work
carryctx progress note|block|risk "..." --task CTX-0002
carryctx checkpoint --done "..." --remaining "..." --task CTX-0002

# Isolation & continuity
carryctx worktree create CTX-0002        # .worktrees/<task-id>, branch carryctx/<id>
carryctx export --pack-format dir -o ./pack/  # portable state (since 0.8.2; ctxpack v2 since 0.10.0)
carryctx worktree cleanup list           # durable cleanup outbox
carryctx worktree cleanup show <REF>     # request by ID or task reference
carryctx worktree cleanup run            # retry deferred, blocked, or failed cleanup
carryctx handoff create --agent cmd-1 --target sub-1 --task CTX-0002 --summary "..."
```

Everything else — dependency kinds (`strong`/`informational`), file scopes and
conflict detection, task statuses, blockers, decisions, search, event audit,
presets/rules/personas in `.carryctx/`, error recovery — is documented in the
references below. Consult them when operating in that area; do not guess flags.

## Cross-Clone Sync & Merge

State is per clone; linked worktrees share one database. Moving state between
clones or machines is `export` / `import` plus transport the user runs (`git
push`/`fetch`, `scp`, …) — carryctx never touches the network. For concurrent
work, carry the local snapshot DAG on a Git ref and merge three-way:

```bash
# Clone A: export and commit one snapshot to the local-only ref
carryctx export --pack-format dir -o ./pack --snapshot   # refs/carryctx/local

# Clone B: fetch (user transport), then merge the snapshot DAG
git fetch <remote> refs/carryctx/local:refs/remotes/origin/carryctx-local
carryctx import --from-git refs/remotes/origin/carryctx-local --mode merge \
    --snapshot-ref=refs/carryctx/local

# Blocking conflicts stage a session and exit 3 (MERGE_CONFLICTS)
carryctx conflict list
carryctx conflict show <conflict-id>
carryctx conflict resolve <conflict-id> --ours|--theirs [--set field=value]
carryctx conflict apply --snapshot-ref=refs/carryctx/local   # atomic swap
carryctx conflict abort                                       # discard, DB untouched
```

- **Never push an unredacted snapshot ref to a public repository.** The default
  `refs/carryctx/local` is a non-branch local-only ref; carryctx never pushes it,
  and publishing unredacted state requires an explicit user refspec. To share
  state publicly, publish a redacted artifact instead:
  `carryctx export --pack-format dir -o ./pack --publication` redacts every table
  row and `project.json`, stamps `manifest.redacted`, and commits to the fixed
  `refs/heads/carryctx-snapshots` ref; `git push` moves it. For a private source
  repo, host the snapshot in a separate mirror repo — see
  [references/publication-and-mirrors.md](references/publication-and-mirrors.md).
  Otherwise use a private state remote, an encrypted channel, or exchange pack
  directories.
- Merge composes state and takes a verified pre-merge backup, so no `--yes` is
  required (`--yes` stays reserved for `replace`). `--require-base` refuses a
  degraded base-less merge with `VALIDATION_FAILED` (exit 8); `--strict-edits`
  turns row-edit auto-LWW into blocking conflicts.
- Native `git merge` of snapshot commits is **unsupported** — CarryCtx owns the
  semantic merge. A clean merge or `conflict apply` with `--snapshot-ref` writes
  a two-parent merge snapshot commit.

## References

Read the focused guide when operating in that area:

- [references/command-reference.md](references/command-reference.md) — full
  command table for all subcommands and flags (verified against v0.11.0).
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
- [references/publication-and-mirrors.md](references/publication-and-mirrors.md)
  — publishing a redacted state snapshot, choosing a source-branch ref versus a
  mirror repository, and recovering a clone from it.
- [references/troubleshooting.md](references/troubleshooting.md) — error codes,
  recovery, diagnostics.
