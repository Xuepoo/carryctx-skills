#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
schema="$repo_root/schemas/preset.schema.json"

mapfile -t manifests < <(printf '%s\n' "$repo_root"/presets/*/*.json | sort)
if ((${#manifests[@]} == 0)); then
	printf 'No preset manifests found\n' >&2
	exit 1
fi

check-jsonschema --schemafile "$schema" "${manifests[@]}"
printf 'Validated %d preset manifests\n' "${#manifests[@]}"
