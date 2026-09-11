# State Publication & Mirrors

CarryCtx can publish a **redacted** snapshot of project state as a portable,
reviewable Git artifact. Unlike the local-only snapshot ref used for cross-clone
merging, a publication is safe to push to a public remote: every secret-shaped
value is replaced before the bundle is written and `manifest.redacted` is set.

The binary never touches the network. It writes the redacted commit to a local
ref; moving it anywhere is a user-run `git push`.

## When to publish, and where

| Situation                                                             | Target                                                             |
| --------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Source repo is already public; snapshots can share its history        | Source repo's own `refs/heads/carryctx-snapshots` branch           |
| Source repo is private but the workflow snapshot must be public       | A separate mirror repository (`*-workflow`)                        |
| Snapshot history should not enter ordinary `git clone`s of the source | A separate mirror repository                                       |
| Publication needs a different credential than source push             | A separate mirror repository                                       |
| Several sources each want a public snapshot                           | One mirror repo, one branch per source (collapse N mirrors into 1) |

A mirror repository is **publish-only**: it holds snapshots for review and
recovery. It is not a merge source and it is never consumed back into the state
database as authoritative state.

## Publishing

```bash
# Preview the target ref and commit without writing anything
carryctx export --pack-format dir -o .carryctx/publish --publication --dry-run

# Publish: redact all tables + project.json, stamp manifest.redacted, commit the ref
carryctx export --pack-format dir -o .carryctx/publish --publication
```

- `--publication` always targets the fixed public ref
  `refs/heads/carryctx-snapshots`; a non-default `--snapshot-ref` alongside it is
  refused (`INVALID_ARGUMENTS`, exit 2) so the redacted/public ref separation
  cannot be redirected.
- The local-only, unredacted ref is `refs/carryctx/local` (`--snapshot`); it must
  never be pushed to a public remote.
- Redaction is the built-in `carryctx_pack::redact` pass. Do **not** post-process
  the bundle with your own script: a hand-rolled pass will not stamp
  `manifest.redacted`, and CarryCtx keys its safety decision on that flag alone.

## Transport

Moving the ref is ordinary user transport:

```bash
git push <remote> refs/heads/carryctx-snapshots
```

Push it to the source repo's own branch, or to a mirror repository's branch
(one branch per source). The snapshot commit carries `CarryCtx-Export-Id`,
`CarryCtx-Parents`, and `CarryCtx-Source` trailers, so its provenance travels
with it.

## Recovering a clone

```bash
git fetch <remote> refs/heads/carryctx-snapshots:refs/remotes/<remote>/snapshots
carryctx import --from-git refs/remotes/<remote>/snapshots --mode replace
```

`import --from-git <ref>` materializes the ref's tree and runs the normal import
path. A redacted bundle is accepted by fresh/replace import but **refused as a
merge source** (`UNSUPPORTED_OPERATION`, exit 10) — its redacted placeholders are
not real values, so it can never be merged into live state.

## Guardrails

- Never push an unredacted ref to a public remote. Publish only
  `refs/heads/carryctx-snapshots`.
- Never partially redact or hand-edit bundle JSONL; rely on `--publication`.
- Never merge a redacted bundle back into state; recovery uses replace mode.
- Prefer one publication target per source; collapse many per-source mirrors
  into one mirror with one branch per source.
- Verify `"redacted": true` in `manifest.json` before pushing.

## See also

- [command-reference.md](command-reference.md) — the full flag surface,
  including `export --publication` and `import --from-git`.
- [sessions-and-checkpoints.md](sessions-and-checkpoints.md) — what a checkpoint
  record contains and why snapshots are reviewable.
