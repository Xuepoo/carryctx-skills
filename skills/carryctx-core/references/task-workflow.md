# CarryCtx Task Workflow

The `carryctx-core` task management system follows a strict state machine defined by the CLI. As an Agent, you must use these commands to transition tasks accurately.

## Task States

- `PLANNED`: The task is created but not ready to be worked on (e.g., waiting on dependencies).
- `READY`: The task is unassigned and ready to be claimed.
- `IN_PROGRESS`: The task is currently being worked on by an owner.
- `BLOCKED`: The task cannot proceed (requires a reason).
- `IN_REVIEW`: The task is completed but pending review.
- `COMPLETED`: The task is successfully finished.
- `CANCELLED`: The task is discarded (requires a reason).

## Task Lifecycle Commands

Always use the CLI commands to move tasks through their lifecycle:

1. **Creating Tasks**
   ```bash
   carryctx task create --title "Fix parser bug" --description "Fails on trailing commas"
   ```

2. **Listing & Viewing Tasks**
   ```bash
   carryctx task list --mine         # See tasks assigned to you
   carryctx task list --status READY # Find tasks you can pick up
   carryctx task show <task_id>      # View full details
   ```

3. **Taking Ownership**
   ```bash
   carryctx task claim <task_id>     # Claim an unassigned task
   carryctx task release <task_id>   # Give up ownership of a task
   ```

4. **Working on a Task**
   ```bash
   carryctx task start <task_id>     # Move from READY to IN_PROGRESS
   carryctx task block <task_id> --reason "Waiting on API response"
   carryctx task unblock <task_id>   # Move back to IN_PROGRESS
   ```

5. **Completing a Task**
   ```bash
   carryctx task review <task_id>    # Mark as ready for review
   carryctx task complete <task_id>  # Mark as fully done
   carryctx task cancel <task_id> --reason "Duplicate of ctx-123"
   ```

6. **Managing Dependencies**
   ```bash
   carryctx task depend <task_id> --on <other_task_id>           # strong (default)
   carryctx task depend <task_id> --on <other_task_id> --kind informational
   carryctx task undepend <task_id> --on <other_task_id>
   ```
   `--kind` accepts only `strong` or `informational` (alias `info`). A
   `strong` dependency blocks claim/start until the prerequisite is completed;
   `informational` is recorded but never gates transitions.

7. **Team & Role Metadata (0.6.0+)**

   ```bash
   carryctx task create --title "..." --team core --required-role backend
   carryctx task team set <task_id> --team core
   carryctx task team set <task_id> --team none    # same as unset
   carryctx task team unset <task_id>
   carryctx task edit <task_id> --required-role backend
   ```

   Both fields are optional additive metadata and default to `null`. Associating,
   changing, or clearing a task's team **never** alters its status, owner,
   dependencies, or scopes — it is bookkeeping, not a lifecycle transition.
   `required_role` is advisory: it records the role the task wants and does not
   restrict who may claim it. Note that `task edit` carries `--required-role` but
   not `--team`; use `task team set` / `task team unset` for association. See
   [team-coordination.md](team-coordination.md).

## Agent Directives

- **Never** attempt to use nonexistent commands like `unclaim`, `approve`, `reject`, or `close`. To give up ownership, use `carryctx task release`.
- **Never** assume a state like `BACKLOG` or `IN_FLIGHT`. Only use the exact states defined above.
- Always check your currently assigned tasks using `carryctx task list --mine` before claiming new ones — to avoid duplicating work, not because a limit exists. Holding several `IN_PROGRESS` tasks at once is supported: `claim`, `start`, and `assign` never fail on a task count, and the legacy `task.single_active_task_per_agent` config key is compatibility-only and non-enforcing. Decide your own capacity, or let a commander decide it.
