# Dependency Upgrade Standard Operating Procedure (SOP)

This workflow defines the standard step-by-step process for upgrading a dependency, fixing resulting breakage, and verifying the result using CarryCtx.

## Phase 1: Scope the Upgrade

1. **Claim Task**: `carryctx task claim <TASK_ID>`
2. **Read Changelog/Breaking Changes**: Review the dependency's changelog or migration guide between the current and target version.
3. **Isolate Worktree**: `carryctx worktree create <TASK_ID>`
4. **Log Scope**: `carryctx progress note "Upgrading <DEP> from <OLD_VERSION> to <NEW_VERSION>, breaking changes: <SUMMARY>"`

## Phase 2: Upgrade & Fix Breakage

1. **Bump Version**: Update the dependency version in the manifest (`Cargo.toml`, `package.json`, `requirements.txt`, etc.).
2. **Run Full Test Suite**: Run the complete test suite to surface compile/type errors and failing tests.
3. **Fix Compile/Type Errors**: Resolve breakage introduced by API changes, one file at a time.
4. **Resolve Deprecation Warnings**: Address new deprecation warnings so the next upgrade is cheaper.
5. **Log Each Fix**: `carryctx progress note "Fixed <FILE>: <WHAT_CHANGED_AND_WHY>"`

## Phase 3: Verify & Record

1. **Run Security Audit**: `cargo audit` / `npm audit` / equivalent for the ecosystem, and resolve any new advisories.
2. **Record Non-Obvious Workarounds**: `carryctx decision add --title "Workaround for <DEP> v<NEW_VERSION>" --context "<WHY_NEEDED>" --decision "<WORKAROUND>" --consequences "<TECH_DEBT_OR_FOLLOWUP>" --task <TASK_ID>`
3. **Checkpoint the State**: `carryctx checkpoint --task <TASK_ID> --done "Upgraded <DEP> to <NEW_VERSION>, fixed breakage, audit clean" --remaining "PR review"`
4. **Complete Task**: `carryctx task complete <TASK_ID>`
