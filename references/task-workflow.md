# Task Workflow

CarryCtx tasks track discrete units of work through a defined lifecycle. Tasks are identified by `CTX-NNNN` IDs and support dependencies, ownership, and structured progress.

## State Machine

```
                    ┌──────────┐
                    │  BACKLOG │
                    └────┬─────┘
                         │
                      create
                         │
                         ▼
                    ┌──────────┐
          ┌────────►│  OPEN    │◄────────┐
          │         └────┬─────┘         │
          │              │               │
       unclaim        claim           reopen
          │              │               │
          │              ▼               │
          │         ┌──────────┐         │
          │         │ CLAIMED  │         │
          │         └────┬─────┘         │
          │              │               │
          │            start             │
          │              │               │
          │              ▼               │
          │         ┌──────────┐         │
          │         │ IN_FLIGHT│         │
          │         └────┬─────┘         │
          │              │               │
          │          complete            │
          │              │               │
          │              ▼               │
          │         ┌──────────┐         │
          │         │  REVIEW  │         │
          │         └────┬─────┘         │
          │              │               │
          │         approve  │  reject   │
          │              │   │           │
          │              ▼   ▼           │
          │         ┌──────────┐         │
          │         │COMPLETED│         │
          │         └──────────┘         │
          │              │               │
          │           close              │
          │              │               │
          │              ▼               │
          │         ┌──────────┐         │
          └─────────┤  CLOSED  │         │
                    └──────────┘         │
                         │               │
                         └───────────────┘
```

## Transitions

### BACKLOG → OPEN

`carryctx task create --title "..." [--depends-on CTX-NNNN]`

A task enters the backlog when created. It is automatically moved to OPEN if no dependencies are specified, or if all dependencies are already COMPLETED or CLOSED. Otherwise it remains in BACKLOG until its dependencies are resolved.

### OPEN → CLAIMED

`carryctx task claim CTX-NNNN [--assigned-to <agent>]`

Claims ownership of a task. If `--assigned-to` is omitted, the current agent is assigned. A task can only transition from OPEN to CLAIMED. The previous assignee (if any) is cleared.

### CLAIMED → IN_FLIGHT

`carryctx task start CTX-NNNN`

Marks the task as actively being worked on. This is the working state where progress items, checkpoints, and commits are associated.

### IN_FLIGHT → REVIEW

`carryctx task complete CTX-NNNN`

Marks the implementation as done and moves the task to review. This should only be done when the agent believes the task is functionally complete and tests pass.

### REVIEW → COMPLETED

`carryctx task approve CTX-NNNN`

Confirms the task meets its acceptance criteria. This is typically done after verification. Once completed, the task's completion timestamp is recorded.

### REVIEW → IN_FLIGHT (reject)

`carryctx task reject CTX-NNNN --reason "..."`

Returns the task to IN_FLIGHT when review reveals issues. A reason should always be provided.

### COMPLETED → CLOSED

`carryctx task close CTX-NNNN`

Final state. A closed task is fully done. The difference between COMPLETED and CLOSED is that COMPLETED signals the work passed review, while CLOSED is administrative — it means no further action is expected. In practice, most tasks go directly from COMPLETED to archival, but CLOSED exists for cases where a task is resolved without completion (e.g. superseded, wontfix).

### CLAIMED → OPEN (unclaim)

`carryctx task unclaim CTX-NNNN`

Releases ownership. The task goes back to OPEN for another agent to claim.

## Progress Tracking

Within any state, agents can record progress items:

| Item    | Command                                         | Description                             |
| ------- | ----------------------------------------------- | --------------------------------------- |
| Todo    | `carryctx progress todo "..."`                  | Work that still needs doing             |
| Done    | `carryctx progress done "..."`                  | Completed work item                     |
| Blocked | `carryctx progress block "..." --context "..."` | External dependency preventing progress |
| Risk    | `carryctx progress risk "..." [--impact high]`  | Something that may cause issues         |
| Note    | `carryctx progress note "..."`                  | General observation or decision         |

Progress items are timestamped and associated with the active session. They are visible in `carryctx resume` and `carryctx context` output.

## Dependencies

Tasks can depend on other tasks:

```
carryctx task create --title "Add login" --depends-on CTX-0001,CTX-0002
```

A task whose dependencies are not all COMPLETED or CLOSED stays in BACKLOG. Dependencies are checked on creation and when a task transitions to COMPLETED or CLOSED — dependent tasks are re-evaluated and moved to OPEN if their dependencies are now satisfied.

## Checkpoints

Checkpoints capture task progress at a point in time:

```
carryctx checkpoint --task CTX-NNNN \
  --done "Implemented the login form" \
  --remaining "Need to add validation" \
  --blocker "API not yet deployed"
```

Checkpoints are immutable once created (see [checkpoint-policy.md](checkpoint-policy.md)). They associate progress with both the task and the current Git HEAD.

## Listing Tasks

```
carryctx task list                    # all tasks
carryctx task list --state OPEN       # filter by state
carryctx task list --assigned-to "$(whoami)"  # my tasks
carryctx task show CTX-NNNN           # full details
```

## Output

All task commands support `--json` for machine-readable output. The JSON envelope follows the CLI specification:

```json
{
  "status": "success",
  "data": {
    "id": "CTX-0001",
    "title": "Implement login page",
    "state": "IN_FLIGHT",
    "assigned_to": "agent-name",
    "dependencies": ["CTX-0000"]
  }
}
```
