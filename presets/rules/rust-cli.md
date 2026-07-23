# Domain Rules: Rust CLI Development

Whenever working on a Rust CLI project within this repository, you must adhere to the following absolute constraints:

## 1. Error Handling
- Never use `.unwrap()` or `.expect()` in production code.
- Always return a custom error type (e.g., using `thiserror` or `anyhow`).
- Errors must be descriptive and user-facing.

## 2. Argument Parsing
- Use `clap` with the `derive` feature for all CLI argument parsing.
- Every command and flag must have a `///` docstring so `clap` can generate the `--help` menu.

## 3. Code Organization
- Do not put business logic inside `main.rs` or command handlers.
- `main.rs` should only parse arguments and delegate to modular handler functions in `src/commands/`.

## 4. Performance & Memory
- Avoid unnecessary cloning (`.clone()`). Use references (`&`) and borrowing wherever possible.
- If iterating over large collections, always use iterators instead of allocating new vectors.
