# Bugfix Standard Operating Procedure (SOP)

This workflow defines the standard step-by-step process for investigating, reproducing, fixing, and verifying bugs using CarryCtx.

## Phase 1: Bug Reproduction & Isolation
1. **Fetch & Read Traceback**: Never diagnose without reading full un-truncated logs.
2. **Claim Task**: `carryctx task claim <TASK_ID>`
3. **Isolate Worktree**: `carryctx worktree create --task <TASK_ID>`
4. **Log Initial Findings**: `carryctx progress block "Investigating issue: <ERROR_SUMMARY>"`

## Phase 2: Dependency Analysis & Fix
1. **Scan Code Graph**: `carryctx graph scan`
2. **Explore Affected Modules**: `carryctx graph export --type ascii --focus <AFFECTED_FILE> --depth 2`
3. **Write Regression Test**: Add a reproducing test before modifying implementation code.
4. **Implement Fix**: Fix root cause without masking symptoms.
5. **Log Completed Fix**: `carryctx progress done "Implemented fix in <FILE>"`

## Phase 3: Verification & Submission
1. **Run Full Test Suite**: Verify linting, formatting, unit tests, and integration tests pass.
2. **Complete Task**: `carryctx task complete <TASK_ID>`
3. **Create Checkpoint**: `carryctx checkpoint --done "Fixed <BUG_TITLE>" --remaining "PR Merge"`
4. **Push Branch & PR**: Push branch, open PR, and verify CI checks pass.
