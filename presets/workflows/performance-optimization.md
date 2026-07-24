# Performance Optimization Standard Operating Procedure (SOP)

This workflow defines the standard step-by-step process for optimizing a hot path with a measured baseline, incremental changes, and documented tradeoffs using CarryCtx.

## Phase 1: Baseline

1. **Claim Task**: `carryctx task claim <TASK_ID>`
2. **Establish Reproducible Benchmark**: Run the profiler/benchmark against the current code at least twice to confirm stable numbers before touching anything.
3. **Log Baseline Numbers**: `carryctx progress note "Baseline: <METRIC> = <VALUE> on <HOT_PATH>"`

## Phase 2: Optimize

1. **Scan Dependency Graph**: `carryctx graph scan`
2. **Map the Hot Path's Surface**: `carryctx graph export --type ascii --focus <HOT_PATH_FILE> --depth 2`
3. **Make One Change at a Time**: Apply a single optimization (e.g. avoid an allocation, cache a computation, batch I/O).
4. **Re-Measure After Each Change**: Re-run the benchmark and discard any change that doesn't move the metric.
5. **Log Each Iteration**: `carryctx progress note "Change: <WHAT>, result: <METRIC> = <NEW_VALUE>"`

## Phase 3: Verify & Document

1. **Run Full Test Suite**: Confirm no correctness regression from any applied optimization.
2. **Record Before/After in Checkpoint**: `carryctx checkpoint --task <TASK_ID> --done "Optimized <HOT_PATH>: <METRIC> <BEFORE> -> <AFTER>" --remaining "PR review"`
3. **Record Tradeoff Decision**: `carryctx decision add --title "Tradeoff in <HOT_PATH> optimization" --context "<CONSTRAINT>" --decision "<WHAT_WAS_TRADED>" --consequences "<MEMORY/COMPLEXITY_COST>" --task <TASK_ID>`
4. **Complete Task**: `carryctx task complete <TASK_ID>`
