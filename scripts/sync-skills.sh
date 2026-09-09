#!/usr/bin/env bash
set -euo pipefail

# Synchronize skills/use-carryctx to local agent skill directories.
#
# Policy: copy-not-symlink. Each destination is a real directory populated
# with `rsync --delete` (no symlink is created; an existing symlink aborts).
# This keeps per-agent installs independent and avoids cross-repo symlink
# surprises on case-sensitive or sandboxed filesystems.
#
# Update policy: expand to sibling `.agents/skills` via this script — the
# workspace sibling `<workspace>/.agents/skills/use-carryctx` is always the
# last target and is resolved relative to this repository, so a single
# `bash scripts/sync-skills.sh` keeps the sibling in sync.
#
# 9 targets (including ~/.codex/skills/use-carryctx):
#   1  ~/.codex/skills/use-carryctx            (Codex)
#   2  ~/.config/opencode/skills/use-carryctx  (Opencode)
#   3  ~/.config/pi/skills/use-carryctx        (Pi)
#   4  ~/.gemini/skills/use-carryctx           (Gemini CLI)
#   5  ~/.gemini/antigravity-cli/skills/use-carryctx (Antigravity)
#   6  ~/.grok/skills/use-carryctx             (Grok)
#   7  ~/.kiro/skills/use-carryctx             (Kiro)
#   8  ~/.claude/skills/use-carryctx           (Claude Code)
#   9  <workspace>/.agents/skills/use-carryctx (workspace sibling)

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
src="$repo_root/skills/use-carryctx"

if [ ! -d "$src" ]; then
	printf 'source not found: %s\n' "$src" >&2
	exit 1
fi

workspace_sibling="$(realpath -m "$repo_root/../.agents/skills/use-carryctx")"

targets=(
	"$HOME/.codex/skills/use-carryctx"
	"$HOME/.config/opencode/skills/use-carryctx"
	"$HOME/.config/pi/skills/use-carryctx"
	"$HOME/.gemini/skills/use-carryctx"
	"$HOME/.gemini/antigravity-cli/skills/use-carryctx"
	"$HOME/.grok/skills/use-carryctx"
	"$HOME/.kiro/skills/use-carryctx"
	"$HOME/.claude/skills/use-carryctx"
	"$workspace_sibling"
)

if ! command -v rsync >/dev/null 2>&1; then
	printf 'rsync not found on PATH\n' >&2
	exit 1
fi

printf 'Syncing %s to %d targets (copy, rsync --delete, no symlinks)…\n' "$src" "${#targets[@]}"

fail=0
for dst in "${targets[@]}"; do
	printf '→ %s\n' "$dst"
	if [ -L "$dst" ]; then
		printf '  ERROR: destination is a symlink (copy-not-symlink violated): %s\n' "$dst" >&2
		fail=1
		continue
	fi
	mkdir -p "$(dirname -- "$dst")"
	if [ -L "$dst" ]; then
		printf '  ERROR: still a symlink after mkdir -p: %s\n' "$dst" >&2
		fail=1
		continue
	fi
	mkdir -p "$dst"
	rsync -a --delete --exclude=".git" "$src"/ "$dst"/
	if [ -L "$dst" ]; then
		printf '  ERROR: dst became symlink after rsync: %s\n' "$dst" >&2
		fail=1
		continue
	fi
	if find "$dst" -type l 2>/dev/null | grep -q .; then
		printf '  WARNING: symlinks found inside %s:\n' "$dst" >&2
		find "$dst" -type l -ls >&2 || true
	fi
done

if [ "$fail" -ne 0 ]; then
	printf 'sync failed\n' >&2
	exit 1
fi

printf 'Verifying no target is a symlink…\n'
for dst in "${targets[@]}"; do
	if [ -L "$dst" ]; then
		printf 'FAIL symlink: %s\n' "$dst" >&2
		exit 1
	fi
	if [ ! -d "$dst" ]; then
		printf 'FAIL missing: %s\n' "$dst" >&2
		exit 1
	fi
done

printf 'All %d targets synced (copy, rsync --delete).\n' "${#targets[@]}"
