#!/usr/bin/env bash
set -euo pipefail

# Create a CarryCtx checkpoint with structured input
# Prompts for each field if not provided via arguments

usage() {
	cat <<EOF
Usage: $(basename "$0") [options]

Options:
  -d, --done TEXT       What was accomplished since last checkpoint
  -r, --remaining TEXT  What still needs to be done
  -b, --blocker TEXT    External blocker (repeatable)
  -k, --risk TEXT       Identified risk (repeatable)
  -n, --note TEXT       Free-form note (repeatable)
  -t, --task CTX-NNNN   Associated task ID
  -h, --help            Show this help

If --done or --remaining are omitted, you will be prompted interactively.
EOF
	exit 0
}

# Parse arguments
DONE=""
REMAINING=""
BLOCKERS=()
RISKS=()
NOTES=()
TASK=""

while [[ $# -gt 0 ]]; do
	case "$1" in
	-d | --done)
		DONE="$2"
		shift 2
		;;
	-r | --remaining)
		REMAINING="$2"
		shift 2
		;;
	-b | --blocker)
		BLOCKERS+=("$2")
		shift 2
		;;
	-k | --risk)
		RISKS+=("$2")
		shift 2
		;;
	-n | --note)
		NOTES+=("$2")
		shift 2
		;;
	-t | --task)
		TASK="$2"
		shift 2
		;;
	-h | --help) usage ;;
	*)
		echo "Unknown option: $1"
		usage
		;;
	esac
done

# Interactive prompts for required fields
if [[ -z "$DONE" ]]; then
	read -r -p "What was accomplished? " DONE
fi

if [[ -z "$REMAINING" ]]; then
	read -r -p "What remains to be done? " REMAINING
fi

# Build command
CMD=(carryctx checkpoint --done "$DONE" --remaining "$REMAINING")

if [[ -n "$TASK" ]]; then
	CMD+=(--task "$TASK")
fi

for blocker in "${BLOCKERS[@]}"; do
	CMD+=(--blocker "$blocker")
done

for risk in "${RISKS[@]}"; do
	CMD+=(--risk "$risk")
done

for note in "${NOTES[@]}"; do
	CMD+=(--note "$note")
done

echo "Creating checkpoint..."
echo
"${CMD[@]}"
echo
echo "Checkpoint created successfully."
