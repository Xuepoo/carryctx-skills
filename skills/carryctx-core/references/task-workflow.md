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
   carryctx task depend <task_id> --on <other_task_id> --type blocks
   carryctx task undepend <task_id> --on <other_task_id>
   ```

## Agent Directives

- **Never** attempt to use nonexistent commands like `unclaim`, `approve`, `reject`, or `close`.
- **Never** assume a state like `BACKLOG` or `IN_FLIGHT`. Only use the exact states defined above.
- Always check your currently assigned tasks using `carryctx task list --mine` before claiming new ones.
