#!/usr/bin/env bash
set -euo pipefail

# Start a CarryCtx session and show initial context
# Uses CARRYCTX_AGENT env var or falls back to system username

AGENT="${CARRYCTX_AGENT:-$(whoami)}"
export CARRYCTX_AGENT

echo "Starting session for agent: $AGENT"

# Attempt JSON output first (silences warnings on success), fall back to plain
if ! carryctx session start --json 2>/dev/null; then
	carryctx session start
fi

echo
echo "=== Context ==="
carryctx resume --compact
