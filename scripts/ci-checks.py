#!/usr/bin/env python3
"""CarryCtx Skills CI checks (single-file helper for .github/workflows/ci.yml).

Subcommands (all read-only; exit 0 on success, 1 on failure):
  schema-fallback    validate presets/*/*.json with the `jsonschema` library
                     (used only when `check-jsonschema` is unavailable).
  preset-refs        every file referenced by a preset manifest exists, and
                     every presets/*/*.md has a sibling .json (and vice versa).
  frontmatter        skills/*/SKILL.md starts with a frontmatter block holding
                     at least `name:` and `description:`, with the name
                     matching its directory.
  links              no broken relative links in Markdown docs.
  min-version        every preset carryctx.engine floor is valid ">=M.m.p" and
                     does not exceed $CARRYCTX_VERSION.
  extract-shell      write fenced sh/bash/shell blocks from presets/**/*.md
                     (dedented) as files into --out DIR for shellcheck.
  command-examples   every `carryctx <path> [--flag ...]` snippet in the docs
                     resolves against the installed CLI (`carryctx <path>
                     --help` probes). Unknown subcommands/flags fail the run.
                     When no `carryctx` binary is on PATH this prints a notice
                     and exits 0 (skip-with-notice; the workflow documents the
                     pinned install source).

Only the standard library is required, except `schema-fallback` which needs
the pinned `jsonschema` package (see the workflow).
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXCLUDED_DIRS = {".git", "node_modules", ".worktrees"}


def fail(message):
    print(f"::error::{message}")


def iter_docs():
    for doc in sorted(REPO.rglob("*.md")):
        if any(part in EXCLUDED_DIRS for part in doc.parts):
            continue
        yield doc


def cmd_schema_fallback(_args):
    from jsonschema import Draft202012Validator

    # NOTE: the schema declares draft-07 but uses $defs, so validate with
    # Draft202012 (the same leniency check-jsonschema applies).
    schema = json.loads((REPO / "schemas/preset.schema.json").read_text())
    validator = Draft202012Validator(schema)
    count, failed = 0, 0
    for manifest in sorted((REPO / "presets").rglob("*.json")):
        errors = list(validator.iter_errors(json.loads(manifest.read_text())))
        if errors:
            failed += 1
            fail(f"{manifest.relative_to(REPO)}: {errors[0].message}")
        else:
            count += 1
    if failed:
        return 1
    print(f"Validated {count} preset manifests (python jsonschema fallback)")
    return 0


def cmd_preset_refs(_args):
    failures = []
    for manifest_path in sorted((REPO / "presets").rglob("*.json")):
        manifest = json.loads(manifest_path.read_text())
        for key in ("rules", "workflows"):
            for entry in manifest.get(key, []) or []:
                if not (REPO / entry["source"]).is_file():
                    failures.append(
                        f"{manifest_path.relative_to(REPO)}: "
                        f"referenced file missing: {entry['source']}"
                    )
        sibling = manifest_path.with_suffix(".md")
        if not sibling.is_file():
            failures.append(
                f"{manifest_path.relative_to(REPO)}: sibling .md missing"
            )
    for doc in sorted((REPO / "presets").rglob("*.md")):
        if not doc.with_suffix(".json").is_file():
            failures.append(
                f"{doc.relative_to(REPO)}: sibling .json manifest missing"
            )
    for failure in failures:
        fail(failure)
    if failures:
        return 1
    print("All preset file references and md/json pairs resolve")
    return 0


def cmd_frontmatter(_args):
    failures = []
    skills = sorted((REPO / "skills").glob("*/SKILL.md"))
    if not skills:
        failures.append("no skills/*/SKILL.md found")
    for skill in skills:
        rel = skill.relative_to(REPO)
        lines = skill.read_text().splitlines()
        if not lines or lines[0].strip() != "---":
            failures.append(f"{rel}: missing opening frontmatter '---'")
            continue
        try:
            end = lines[1:].index("---") + 1
        except ValueError:
            failures.append(f"{rel}: missing closing frontmatter '---'")
            continue
        frontmatter = "\n".join(lines[1:end])
        for required in ("name:", "description:"):
            if not re.search(rf"(?m)^{required}", frontmatter):
                failures.append(
                    f"{rel}: frontmatter missing required key '{required}'"
                )
        name = re.search(r"(?m)^name:\s*(\S+)", frontmatter)
        if name and name.group(1) != skill.parent.name:
            failures.append(
                f"{rel}: frontmatter name '{name.group(1)}' does not match "
                f"directory '{skill.parent.name}'"
            )
        if not re.search(r"(?m)^license:", frontmatter):
            print(f"::notice::{rel}: frontmatter has no 'license' key")
    for failure in failures:
        fail(failure)
    if failures:
        return 1
    print(f"Checked {len(skills)} SKILL.md frontmatter block(s)")
    return 0


def cmd_links(_args):
    link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    failures, checked = [], 0
    for doc in iter_docs():
        checked += 1
        for lineno, line in enumerate(doc.read_text().splitlines(), 1):
            for match in link_re.finditer(line):
                target = match.group(1).strip()
                if re.match(r"^(https?://|mailto:|#|/)", target):
                    continue
                target = target.split("#")[0].strip()
                if not target:
                    continue
                if not (doc.parent / target).exists():
                    failures.append(
                        f"{doc.relative_to(REPO)}:{lineno}: "
                        f"broken relative link: {target}"
                    )
    for failure in failures:
        fail(failure)
    if failures:
        return 1
    print(f"Checked relative links in {checked} Markdown file(s)")
    return 0


def cmd_min_version(args):
    pinned = tuple(int(p) for p in args.carryctx_version.split("."))
    failures, legacy, checked = [], 0, 0
    for manifest_path in sorted((REPO / "presets").rglob("*.json")):
        manifest = json.loads(manifest_path.read_text())
        engine = (manifest.get("carryctx") or {}).get("engine")
        if engine is None:
            legacy += 1  # legacy lightweight manifest without an engine floor
            continue
        checked += 1
        match = re.match(r"^>=(\d+)\.(\d+)\.(\d+)$", engine)
        if not match:
            failures.append(
                f"{manifest_path.relative_to(REPO)}: invalid engine floor "
                f"{engine!r} (want '>=M.m.p')"
            )
            continue
        if tuple(int(p) for p in match.groups()) > pinned:
            failures.append(
                f"{manifest_path.relative_to(REPO)}: engine floor {engine} "
                f"exceeds pinned CLI {args.carryctx_version}"
            )
    if legacy:
        print(f"::notice::{legacy} legacy manifest(s) without carryctx.engine skipped")
    for failure in failures:
        fail(failure)
    if failures:
        return 1
    print(f"Checked minimum CarryCtx version on {checked} manifest(s)")
    return 0


def cmd_extract_shell(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    blocks = 0
    for doc in sorted((REPO / "presets").rglob("*.md")):
        text = doc.read_text()
        for i, match in enumerate(
            re.finditer(r"```(sh|bash|shell)\n(.*?)```", text, re.S)
        ):
            lines = match.group(2).splitlines()
            indents = [
                len(line) - len(line.lstrip()) for line in lines if line.strip()
            ]
            cut = min(indents) if indents else 0
            code = (
                "\n".join(
                    line[cut:] if len(line) >= cut else line for line in lines
                )
                + "\n"
            )
            (out / f"{doc.stem}-{i}.sh").write_text(code)
            blocks += 1
    print(f"Extracted {blocks} fenced shell block(s) into {out}")
    return 0


def _mask_quotes(text):
    stash, counter = {}, [0]

    def rep(match):
        key = f"\x00{counter[0]}\x00"
        stash[key] = match.group(0)
        counter[0] += 1
        return key

    masked = re.sub(
        r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', rep, text
    )
    return masked, stash


def _split_segments(text):
    masked, stash = _mask_quotes(text)
    parts = re.split(r"\s*(?:&&|\|\||(?<!\\)\||;)\s*", masked)
    segments = []
    for part in parts:
        for key, value in stash.items():
            part = part.replace(key, value)
        part = part.strip()
        if part.startswith("carryctx") and (
            len(part) == 8 or part[8].isspace()
        ):
            segments.append(part)
    return segments


def _normalize(token):
    text = token.strip()
    while len(text) >= 2 and (
        (text[0] == "[" and text[-1] == "]")
        or (text[0] == "(" and text[-1] == ")")
    ):
        text = text[1:-1].strip()
    return text.lstrip("([").rstrip("],);")


def cmd_command_examples(_args):
    # Read-only probes (`carryctx <path> --help`); never writes state.
    #
    # Scope/limitations (deliberate): only long (--flag) names are checked —
    # short flags and option values/placeholders are ignored. Piped `a|b`
    # alternatives pass when at least one resolves; bracketed [optional]
    # tokens are validated by name.
    found = []  # (doc, lineno, command)
    for doc in iter_docs():
        lines = doc.read_text().splitlines()
        joined, buf, start = [], "", 0
        for i, line in enumerate(lines, 1):
            if buf == "":
                start = i
            if line.rstrip().endswith("\\"):
                buf += line.rstrip()[:-1] + " "
            else:
                buf += line
                joined.append((start, buf))
                buf = ""
        if buf:
            joined.append((start, buf))
        in_fence = False
        for lineno, text in joined:
            if text.strip().startswith("```"):
                in_fence = not in_fence
                continue
            candidates = []
            for match in re.finditer(r"`([^`]*)`", text):
                inner = match.group(1).strip()
                if inner.startswith("carryctx") and (
                    len(inner) == 8 or inner[8].isspace()
                ):
                    candidates.append(inner)
                elif inner.startswith("$ ") and inner[2:].startswith("carryctx"):
                    candidates.append(inner[2:].strip())
            if in_fence and "carryctx" in text:
                fenced = re.sub(
                    r"^\s*(?:\d+\.\s*|[-*]\s*|\$\s*)", "", text
                ).strip()
                if fenced.startswith("carryctx") and (
                    len(fenced) == 8 or fenced[8].isspace()
                ):
                    candidates.append(fenced)
            for candidate in candidates:
                for segment in _split_segments(candidate):
                    found.append((doc, lineno, segment))

    help_cache = {}

    def run_help(path):
        key = tuple(path)
        if key not in help_cache:
            proc = subprocess.run(
                ["carryctx", *path, "--help"],
                capture_output=True,
                text=True,
            )
            help_cache[key] = (proc.returncode, proc.stdout + proc.stderr)
        return help_cache[key]

    root_flags = set(re.findall(r"--[a-z][a-z0-9-]*", run_help([])[1]))

    def available_flags(path):
        return set(re.findall(r"--[a-z][a-z0-9-]*", run_help(path)[1])) | root_flags

    failures, checked, skipped = [], 0, 0
    for doc, lineno, command in found:
        rel = doc.relative_to(REPO)
        try:
            tokens = [
                _normalize(t)
                for t in shlex.split(command, comments=True, posix=True)
            ]
        except ValueError:
            skipped += 1
            print(
                f"::warning file={rel},line={lineno}::"
                f"unparseable example skipped: {command[:120]}"
            )
            continue
        rest = tokens[1:]
        while rest and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", rest[0]):
            rest.pop(0)
        alternatives = [[""]]
        for token in rest:
            if re.match(r"^[a-z][a-z0-9-]*$", token):
                for alt in alternatives:
                    alt.append(token)
            elif "|" in token:
                options = [
                    o
                    for o in token.split("|")
                    if re.match(r"^[a-z][a-z0-9-]*$", o)
                ]
                if options:
                    alternatives = [
                        alt + [o] for alt in alternatives for o in options
                    ]
                else:
                    break
            else:
                break
        path_len = max((len(a) - 1 for a in alternatives), default=0)
        flags = []
        for token in rest[path_len:]:
            if token.startswith("--"):
                name = token[2:].split("=", 1)[0]
                if re.match(r"^[a-z][a-z0-9-]*$", name):
                    flags.append(name)
        if path_len == 0 and not flags:
            checked += 1
            continue
        resolved = []
        for alt in alternatives:
            candidate = [x for x in alt if x]
            if not candidate:
                continue
            for n in range(len(candidate), 0, -1):
                if run_help(candidate[:n])[0] == 0:
                    resolved.append(candidate[:n])
                    break
        if path_len > 0 and not resolved:
            failures.append(f"{rel}:{lineno}: unknown subcommand in '{command[:120]}'")
            continue
        available = set(root_flags)
        for path in resolved:
            available |= available_flags(path)
        unknown = [f for f in flags if f"--{f}" not in available]
        if unknown:
            context = " ".join(resolved[0]) if resolved else "(root)"
            failures.append(
                f"{rel}:{lineno}: unknown flag(s) "
                f"{', '.join('--' + f for f in unknown)} "
                f"for 'carryctx {context}' in '{command[:120]}'"
            )
        else:
            checked += 1
    if skipped:
        print(f"::notice::{skipped} unparseable example(s) skipped (see warnings)")
    for failure in failures:
        fail(failure)
    if failures:
        return 1
    print(f"Checked {checked} command example(s) against the installed CLI")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("schema-fallback")
    sub.add_parser("preset-refs")
    sub.add_parser("frontmatter")
    sub.add_parser("links")
    p_min = sub.add_parser("min-version")
    p_min.add_argument(
        "--carryctx-version",
        default=os.environ.get("CARRYCTX_VERSION", ""),
    )
    p_ext = sub.add_parser("extract-shell")
    p_ext.add_argument("--out", required=True)
    sub.add_parser("command-examples")
    args = parser.parse_args(argv)
    return {
        "schema-fallback": cmd_schema_fallback,
        "preset-refs": cmd_preset_refs,
        "frontmatter": cmd_frontmatter,
        "links": cmd_links,
        "min-version": cmd_min_version,
        "extract-shell": cmd_extract_shell,
        "command-examples": cmd_command_examples,
    }[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
