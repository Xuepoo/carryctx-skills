# Domain Rules: Go Development

Whenever working on a Go project within this repository, you must adhere to the following absolute constraints:

## 1. Error Handling

- Return errors explicitly as the last return value; never discard them with `_`.
- Wrap errors with context using `fmt.Errorf("doing X: %w", err)` so `errors.Is`/`errors.As` still work.
- Never `panic` in library code; reserve `panic` for truly unrecoverable programmer errors in `main`.
- Check errors immediately after the call that produces them, not several lines later.

## 2. Project Layout

- Put the entrypoint in `cmd/<binary-name>/main.go`; keep `main.go` thin, delegating to packages.
- Put code that must not be imported by other projects in `internal/`.
- Put code intended for external reuse in `pkg/`, and only put it there if it is genuinely reusable.
- One package per directory; package names are short, lowercase, no underscores.

## 3. Concurrency Safety

- Every goroutine you start must have a clear termination condition; never launch a goroutine you cannot cancel or join.
- Propagate `context.Context` as the first parameter through call chains that may need cancellation or deadlines, and check `ctx.Err()` / `ctx.Done()` in loops.
- Never share mutable state across goroutines without a `sync.Mutex`, `sync.RWMutex`, or channel; prefer channels for ownership transfer over shared memory plus locks.
- Run tests with `go test -race` before merging any change that touches goroutines or shared state.

## 4. Tooling

- Run `gofmt -l .` and `goimports -l .` and fix any reported files before committing; never hand-format Go code.
- Run `golangci-lint run` and resolve findings, not suppress them with blanket `//nolint`.
- Run `go vet ./...` as part of the standard check before considering a change complete.
