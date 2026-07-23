# Session Lifecycle

A CarryCtx session represents a contiguous period of work by a single agent. Sessions track time, associate progress items and checkpoints, and enable context restoration across interruptions.

## States

```
                 ┌──────────┐
                 │  START   │
                 └────┬─────┘
                      │
                      ▼
                ┌──────────┐
         ┌─────►│  ACTIVE  │◄──────┐
         │      └────┬─────┘       │
         │           │             │
      pause       end/abandon    resume
         │           │             │
         ▼           ▼             │
    ┌─────────┐  ┌─────────┐      │
    │ PAUSED  │  │  ENDED  │      │
    └────┬────┘  └─────────┘      │
         │                        │
      resume                  (done)
         │
         └────────────────────────┘
```

Stale detection runs as an additional transition: an **ACTIVE** or **PAUSED** session whose last activity exceeds `session.stale_after` (default: 2h) is automatically marked **STALE** on the next status check.

```
    ┌──────────┐    stale timeout    ┌──────────┐
    │  ACTIVE  │────────────────────►│  STALE   │
    └──────────┘                     └──────────┘
    ┌──────────┐    stale timeout    ┌──────────┐
    │  PAUSED  │────────────────────►│  STALE   │
    └──────────┘                     └──────────┘
```

## Commands

| Command                    | Description                                                                      | Preconditions                    |
| -------------------------- | -------------------------------------------------------------------------------- | -------------------------------- |
| `carryctx session start`   | Start a new session. Ends any active session first (prompts for checkpoint).     | Agent registered.                |
| `carryctx session pause`   | Pause the active session. Timer stops; context preserved.                        | Session must be ACTIVE.          |
| `carryctx session resume`  | Resume a paused or stale session back to ACTIVE.                                 | Session must be PAUSED or STALE. |
| `carryctx session end`     | End the active session. Prompts to create a checkpoint if progress exists.       | Session must be ACTIVE.          |
| `carryctx session abandon` | End the session without creating a checkpoint. Discards uncheckpointed progress. | Session must be ACTIVE.          |

## Behaviour

### Start

- A new session is created with status `ACTIVE` and a start timestamp.
- If another session is currently ACTIVE, the agent is prompted to end it first.
- On start, the current Git HEAD SHA is captured as `start_commit`.

### Pause

- The session's `paused_at` timestamp is set.
- The session transitions to `PAUSED`.
- No new progress items or checkpoints can be added while paused.

### Resume

- The session transitions back to `ACTIVE`.
- `paused_at` is cleared.
- Total elapsed time continues accumulating (pause duration is tracked separately).

### End

- The session's `ended_at` timestamp is set.
- The agent is prompted: _"Create a checkpoint before ending?"_ If yes, the checkpoint wizard runs first.
- The session transitions to `ENDED`.

### Abandon

- Same as end, but no checkpoint is created and no prompt is shown.
- Useful when a session was started by mistake or is being discarded.

### Stale Detection

- A session is stale if its last activity timestamp is older than `session.stale_after`.
- On status checks (`carryctx status`, `carryctx resume`), stale sessions are reported with a warning.
- A stale session can be resumed with `carryctx session resume`, which clears the stale flag.
- Sessions do not auto-end; stale is a warning state, not a terminal state.

## Active Session Guarantee

Only one session may be ACTIVE at a time per repository. Attempting to start a new session while one is active:

1. Warns the agent about the existing active session.
2. Shows the active session's current context (task, checkpoint, elapsed time).
3. Asks: _"End current session and start a new one?"_ If yes, the current session is ended (optionally with a checkpoint) and a new one begins.

## Implementation Notes

- Session state is stored in `<git-common-dir>/carryctx/state.sqlite`.
- Timestamps are UTC ISO-8601.
- Elapsed time excludes paused duration.
- Each session has a UUID identifier and an optional human-readable label.
- Audit events are recorded for every state transition.
