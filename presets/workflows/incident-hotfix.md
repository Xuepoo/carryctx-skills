# Incident Hotfix Standard Operating Procedure (SOP)

This workflow defines the standard step-by-step process for responding to a production incident with a minimal, fast-tracked fix using CarryCtx.

## Phase 1: Triage

1. **Create Incident Task**: `carryctx task create --title "Incident: <SUMMARY>" --priority urgent`
2. **Claim Immediately**: `carryctx task claim <TASK_ID>`
3. **Isolate Off Production**: `carryctx worktree create <TASK_ID> --base <PROD_BRANCH_OR_TAG>`
4. **Log Incident Summary**: `carryctx progress block "Production incident: <ROOT_SYMPTOM>, affected: <SERVICE/ENDPOINT>"`

## Phase 2: Minimal Fix

1. **Scope the Fix Tightly**: Change only what is required to stop the incident; defer refactors and unrelated cleanup.
2. **Write Regression Test**: Add a test that reproduces the failure before applying the fix.
3. **Implement Smallest Fix**: Patch the root cause with the narrowest possible diff.
4. **Checkpoint Progress**: `carryctx checkpoint --task <TASK_ID> --done "Applied minimal fix + regression test" --remaining "Fast-track verification, deploy"`

## Phase 3: Fast-Track Verification & Deploy

1. **Run Critical Subset**: If the full suite is too slow, run only the tests covering the affected module/path.
2. **Deploy**: Ship the hotfix through the emergency deploy path and confirm the incident symptom clears.
3. **Complete Task**: `carryctx task complete <TASK_ID>`
4. **Schedule Full-Suite Follow-Up**: `carryctx task create --title "Full-suite verification for hotfix <TASK_ID>" --depends-on <TASK_ID>`
5. **Record Root Cause Decision**: `carryctx decision add --title "Root cause of <INCIDENT>" --context "<WHAT_TRIGGERED_IT>" --decision "<FIX_APPLIED>" --consequences "<FOLLOW_UP_NEEDED>" --task <TASK_ID>`
