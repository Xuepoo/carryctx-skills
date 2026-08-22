# Team Coordination

A **Team** is durable, project-scoped membership stored in the same
`<git-common-dir>/carryctx/state.sqlite` as tasks and sessions. Because it lives
in Git-common state rather than in a session, a team survives session ends,
closed terminals, new windows, and linked worktrees. Any agent that can reach the
repository sees the same team.

Available since **0.6.0**.

## What CarryCtx Owns, and What It Does Not

CarryCtx is a **management and persistence layer, not an orchestration
framework**. It owns the durable answer to three questions:

- Who is on this team?
- What is each member working on?
- What does each member need to know to continue?

The **external harness** — the thing actually running the agents, whether that is
OpenCode, Claude Code, or a shell script — owns everything about execution:
spawning processes, routing work, retries, concurrency limits, worktree creation,
heartbeats, and model selection.

0.6.0 ships **no scheduler, no worker runtime, no lease or heartbeat machinery,
no prompt cache, and no token optimizer**. Do not wait for CarryCtx to dispatch
work; it will not. Read state, decide, act, and record the outcome.

## Write Commands

Every command below mutates state, appends an audit event in the same
transaction, and supports `--json` and `--dry-run`. Under `--dry-run` the
envelope reports `"operation": {"applied": false}` and nothing is persisted.

`<TEAM_REF>` accepts a team name or its ULID. `<AGENT_REF>` accepts an agent name
or ULID.

```bash
# Create a team. --commander also adds that agent as a member.
carryctx team create --name core
carryctx team create --name core --commander cmd-1

# Membership
carryctx team member add core --agent sub-1 --role backend
carryctx team member remove core --agent sub-1

# Commander
carryctx team commander set core --agent cmd-1
carryctx team commander set core --clear

# Task association
carryctx task team set CTX-0001 --team core
carryctx task team set CTX-0001 --team none    # same as unset
carryctx task team unset CTX-0001

# Agent identity with an execution kind
carryctx agent register --name cmd-1 --provider opencode --kind commander
carryctx agent register --name sub-1 --provider opencode --kind subagent --role backend

# Tasks carrying team and role metadata
carryctx task create --title "Backend API" --team core --required-role backend
carryctx task edit CTX-0001 --required-role backend
```

`--kind` accepts only `commander` or `subagent`. Note that `agent register --role`
(the agent's own default role) and `team member add --role` (the role that agent
plays on that specific team) are separate fields; an agent may hold different
roles on different teams.

`task edit` carries `--required-role` but **not** `--team`. Change association
with `task team set` / `task team unset`.

## Semantic Rules

- **A commander must be a member of its own team.** Setting a non-member as
  commander is rejected with `STATE_CONFLICT: Commander must be a member of this team.`
- **The current commander cannot be removed from the team.** Removal is rejected
  with `STATE_CONFLICT: Cannot remove the current team commander.` until the
  commander is replaced with `commander set --agent <other>` or explicitly cleared
  with `commander set --clear`. After clearing, removal succeeds.
- **Team association never touches task lifecycle.** Setting, changing, or
  clearing a task's team leaves `status`, `owner_agent_id`, dependencies, and
  scopes exactly as they were. `--team none` is equivalent to `task team unset`.
- **`agents.kind` and `tasks.required_role` are nullable additive metadata.**
  Agents registered before 0.6.0 report `"kind": null`; tasks report
  `"required_role": null`. Nothing about their behavior changes.
- **`required_role` is advisory.** It records the role a task wants. It does not
  restrict who may claim the task.
- **Team names are unique per project.** Reusing one currently surfaces a raw
  `DATABASE_ERROR` about a UNIQUE constraint rather than a friendly conflict.
- **Adding an existing member is an error**, not an upsert:
  `STATE_CONFLICT: Agent is already a member of this team.`

## Multiple Active Tasks Are Supported

An agent may hold **many** tasks in `in_progress` at once. `claim`, `start`, and
`assign` never fail because of a task count.

The legacy config key `task.single_active_task_per_agent` is
**compatibility-only and non-enforcing**. It is still accepted in
`.carryctx/config.toml` and still written by `carryctx init`, but setting it to
`true` does not prevent a second or third concurrent task.

Capacity policy belongs to the commander or the harness, not to CarryCtx. If you
want one task per subagent at a time, enforce that in your own dispatch logic and
verify it by reading `active_task_count` from `team status`.

## Read-Only Projections

```bash
carryctx team status [<TEAM_REF>]
carryctx team context [<TEAM_REF>] [--agent-for <AGENT_REF>] [--task <TASK_REF>]
```

Both commands **open the database read-only, run no migrations, and write
nothing** — no audit events, no claims, no sessions, no `last_active_at` touch.
They are safe to call as often as you like, from any number of agents, at any
point in a task. Neither requires `--agent`.

### `team status`

With a team ref, the envelope's `data` is `{team, members, counts}`:

```json
{
  "team": {
    "id": "01M0KJZW4W922Q1WA3J1YMH32P",
    "name": "core",
    "project_id": "01M0KJZW0CAAW1GGW8CCAKFSP6",
    "commander_agent_id": "01M0KJZW1XW6WG7X8TBD2TCBXG",
    "created_at": "...",
    "updated_at": "..."
  },
  "members": [
    {
      "agent_id": "01M0KJZW2EF3Y3HHM0VWA5TSBH",
      "name": "sub-1",
      "kind": "subagent",
      "role": "backend",
      "active_session_id": "01M0KK1MR6027S8W0ZBM245DFE",
      "active_task_count": 3,
      "tasks": [
        {
          "display_id": "CTX-0001",
          "status": "in_progress",
          "team_id": "01M0K..."
        }
      ]
    }
  ],
  "counts": { "total": 3, "commanders": 1, "subagents": 2, "unassigned": 0 }
}
```

Each member carries its team role, its agent kind, its active session id (`null`
when the agent has no live session), and its **non-terminal** tasks.

Read `counts` precisely:

| Field        | Actually means                                                                                      |
| ------------ | --------------------------------------------------------------------------------------------------- |
| `total`      | number of members on the team                                                                       |
| `commanders` | `1` if the team has a commander set, else `0` — **not** a count of members with `kind: "commander"` |
| `subagents`  | members whose agent `kind` is `subagent`                                                            |
| `unassigned` | non-terminal tasks on this team with **no owner** — a task count, not a member count                |

With **no** team ref, `data` is `{teams: [...]}` for the whole project, where each
element has that same `{team, members, counts}` shape.

### `team context`

`data` carries these keys, all `snake_case`:

`team`, `view`, `members`, `tasks`, `dependencies`, `scopes`, `progress`,
`scope_conflicts`, `blockers`, `conflicts`, `latest_checkpoints`, `decisions`,
`handoffs`, `recent_events`, `rebuild`.

- `team` is trimmed to `{id, name}`.
- `members` here is trimmed to `{agent_id, name, kind, role}` — no session or task
  counts. Use `team status` when you need those.
- `rebuild` is `{"source": "durable_records", "session_id": <id-or-null>}`,
  stating that the projection was assembled from persisted records rather than
  from live session memory.
- `view` reports the projection's scope: `"commander"` for the whole team,
  `"member"` under `--agent-for`, `"task"` under `--task`.

`--agent-for` and `--task` narrow **every** collection consistently. Under
`--agent-for sub-1`, `members` contains only `sub-1` and `tasks` contains only
that agent's tasks. Under `--task CTX-0002`, `tasks` contains only `CTX-0002`.

**Dependency edges are closed over the returned task set**: no edge in
`dependencies` ever references a task absent from `tasks`. A `CTX-0002 → CTX-0001`
edge that appears in the full team view correctly disappears under
`--task CTX-0002`, because `CTX-0001` is not in that narrowed set. Do not treat a
narrowed view's empty `dependencies` as evidence that a task has no prerequisites.

### Output Format Caveat

Both projections currently emit **JSON regardless of `--format`**. Asking for
`--format text` or `--format markdown` still returns the JSON envelope. Parse
accordingly, and do not paste the result into a report expecting prose.

## Durable Recording Discipline

`team context` can only rebuild what was actually written down. Its `progress`,
`blockers`, `latest_checkpoints`, `decisions`, and `handoffs` collections come
from durable records, so **an agent that works silently and then dies leaves
nothing behind** — no partial results, no reason for its choices, no indication of
how far it got. Its replacement starts from zero.

Record as you go, not at the end:

```bash
carryctx progress todo  "Add integration test for token refresh"
carryctx progress note  "Chose LRU over TTL: src/cache.rs:88 shows hot-key skew"
carryctx progress block "Waiting on CTX-0007 schema decision"
carryctx checkpoint --done "Refresh endpoint green" --remaining "Rate limit path"
carryctx decision add --title "LRU over TTL" --task CTX-0001 --rationale "..."
```

Guidance for team members:

1. **Checkpoint at boundaries, not at exit.** A checkpoint written only at
   shutdown is the one you lose when the process is killed.
2. **Write the "why" into a decision or note** the moment you make a non-obvious
   choice. A diff shows what changed; only the record shows why.
3. **Block explicitly.** `progress block` and `task block --reason` make a stall
   visible in `team context`; going quiet does not.
4. **Reference IDs across agents.** Cite `CTX-NNNN`, `DEC-NNNN`, or a checkpoint
   ULID rather than restating another agent's findings.
5. **Close out tasks you started.** A task left `in_progress` after you stop is
   indistinguishable from one being actively worked, which makes both
   `team status` and `task list --status in_progress` unreliable as signals.

## Commander Working Pattern

A commander decides work grouping **situationally**. CarryCtx enforces no
grouping algorithm and no fan-out policy.

```bash
# Read the durable picture before deciding anything.
carryctx team status core
carryctx team context core

# Give a subagent exactly its slice.
carryctx team context core --agent-for sub-1
```

Reasonable judgment, not a fixed rule:

- **Do small work inline.** Dispatching a one-line fix costs more than fixing it.
- **Batch tightly-related tasks to one subagent.** Tasks touching the same module
  or sharing a prerequisite are usually cheaper in one place, and they avoid
  conflicting edits.
- **Fan out only genuinely independent work.** Check `dependencies` and
  `scope_conflicts` before splitting; two tasks that both rewrite the same file
  are not independent, whatever their dependency edges say.
- **Re-read `team status` between rounds.** It is the only reliable statement of
  who is live and what they hold, and it costs nothing.

Because CarryCtx does not spawn or supervise processes, the commander (or the
harness) is responsible for noticing that a subagent stopped reporting. Compare
`active_session_id` and `active_task_count` across successive `team status` calls
rather than expecting a timeout event.

## Storage

- Teams, members, and task association live in
  `<git-common-dir>/carryctx/state.sqlite`, shared by all linked worktrees.
- Every write appends an audit event: `team.created`, `team.member_added`,
  `team.member_removed`, `team.commander_changed`, `task.team_changed`.
- Inspect them with `carryctx event list` or via `carryctx stats`.
