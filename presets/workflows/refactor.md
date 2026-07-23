# Refactor Standard Operating Procedure (SOP)

This workflow guides large-scale code refactoring while preserving existing API contracts and test coverage.

## Phase 1: Baseline Analysis
1. **Scan Code Graph**: `carryctx graph scan`
2. **Export Architectural Map**: `carryctx graph export --type mermaid --compact`
3. **Verify Baseline Tests**: Run full test suite before touching any code.
4. **Log Plan**: `carryctx progress todo "Refactor <MODULE_NAME> into decoupled layers"`

## Phase 2: Incremental Refactoring
1. **Preserve Public API**: Do not break external callers or function signatures.
2. **Decouple Dependencies**: Extract single-responsibility sub-modules.
3. **Log Incremental Progress**: Log `done` items as each sub-module passes unit tests.

## Phase 3: Validation & Auditing
1. **Re-scan Code Graph**: `carryctx graph scan` to confirm clean module boundaries.
2. **Quality Gate Check**: Run lint, format, typecheck, and unit test suites.
3. **Generate Stats Report**: `carryctx stats --markdown --output /tmp/refactor_stats.md`
4. **Create Checkpoint**: `carryctx checkpoint --done "Completed refactoring of <MODULE>"`
