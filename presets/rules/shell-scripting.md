# Domain Rules: Shell Scripting

Whenever writing or editing a shell script within this repository, you must adhere to the following absolute constraints:

## 1. Safety Flags

- Every script starts with an explicit shebang (`#!/usr/bin/env bash`, not bare `#!/bin/sh` unless POSIX compatibility is required).
- Immediately follow the shebang with `set -euo pipefail`: `-e` stops on error, `-u` catches unset variables, `-o pipefail` surfaces failures inside pipelines.
- If a command is expected to fail (e.g. probing for existence), handle it explicitly with `|| true` or an `if` check, never by disabling `-e` globally.

## 2. Quoting Discipline

- Always quote variable expansions: `"$var"`, `"${arr[@]}"`, `"$(cmd)"`. Unquoted expansions are subject to word-splitting and globbing.
- Quote command substitutions the same way: `result="$(some_command "$arg")"`.
- Use `printf '%s\n' "$var"` instead of `echo $var` when the value's contents aren't guaranteed safe.

## 3. Avoid Parsing `ls`

- Never parse `ls` output to enumerate files; filenames with spaces, newlines, or glob characters break it.
- Use globs directly (`for f in ./*.log; do ...; done`) or `find ... -print0 | while IFS= read -r -d '' f; do ...; done` for recursive or filtered cases.

## 4. Test Syntax

- Use `[[ ]]` over `[ ]` in bash scripts: it avoids word-splitting on unquoted variables, supports `&&`/`||` inline, and gives regex/glob matching (`=~`, `==`).
- Reserve `[ ]` only for scripts that must run under POSIX `sh`.

## 5. Lint Discipline

- Every script must be `shellcheck -S warning` clean before it's considered done; fix the underlying issue rather than suppressing with `# shellcheck disable`.
- Run `shfmt -w` for consistent formatting before committing.
- Never silence a shellcheck warning without a comment explaining why it's a false positive in this specific case.
