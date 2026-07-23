# Checkpoint Policy

Checkpoints are immutable snapshots of project progress at a point in time. They capture semantic progress (what was done, what remains, blockers) alongside the current Git working tree state.

## Immutability

Once created, a checkpoint **cannot be modified or deleted**. This ensures:

- **Audit trail**: Every checkpoint is a permanent record of what the agent reported at that moment.
- **Reproducibility**: A checkpoint's Git SHA always points to the exact state of the repository when the checkpoint was made.
- **Trust**: No retroactive editing of progress history.

### Corrections

If a checkpoint contains incorrect information, do not edit it. Instead:

1. Create a new progress note: `carryctx progress note "Correction to checkpoint CTX-CP-XXXX: <explanation>"`
2. If the error affects an active task, create a new checkpoint with the corrected information.
3. The original checkpoint remains as a record of what was reported — the correction is linked via context.

## Git State Capture

Each checkpoint records:

| Field                     | Description                                 |
| ------------------------- | ------------------------------------------- |
| `checkpoint_id`           | Unique identifier (format: `CTX-CP-XXXX`)   |
| `session_id`              | The session this checkpoint belongs to      |
| `task_id`                 | The task being worked on (optional)         |
| `git_head_sha`            | Full SHA of `HEAD` at checkpoint time       |
| `git_head_message`        | Commit message of `HEAD`                    |
| `has_uncommitted_changes` | Whether the working tree was dirty          |
| `done`                    | What was accomplished since last checkpoint |
| `remaining`               | What still needs to be done                 |
| `blockers`                | External blockers preventing progress       |
| `risks`                   | Identified risks                            |
| `notes`                   | Free-form notes                             |
| `created_at`              | UTC ISO-8601 timestamp                      |

The `git_head_sha` is captured immediately on creation. If the working tree has uncommitted changes, `has_uncommitted_changes` is set to `true` but the checkpoint is still created — agents are not required to commit before checkpointing.

## Relationship to Sessions

- Each checkpoint belongs to exactly one session.
- A session may have zero or more checkpoints.
- Ending a session optionally creates a final checkpoint.
- Checkpoints persist after their session ends.
- The `carryctx resume` command shows the most recent checkpoint from the current or most recent session.

## Lifecycle

```
Session active ──► checkpoint created ──► immutable
                       │
                       ├── correction needed? ──► new progress note + optional new checkpoint
                       │
                       └── used by `carryctx resume` to restore context
```

## Usage Guidelines

1. **Create checkpoints at meaningful boundaries**: after completing a logical unit of work, before switching tasks, or when hitting a blocker.
2. **Be specific in descriptions**: `"Implemented user authentication flow with JWT tokens"` not `"did auth stuff"`.
3. **List all known blockers**: even if a blocker seems temporary, recording it creates accountability.
4. **Don't over-checkpoint**: a checkpoint every few minutes adds noise. One per significant work unit is sufficient.
5. **Use progress items between checkpoints**: todos, done items, risks, and notes provide granular tracking that checkpoints summarize.

## Storage

Checkpoints are stored in `<git-common-dir>/carryctx/state.sqlite` in the `checkpoints` table. They are never pruned or archived — the database grows monotonically.
