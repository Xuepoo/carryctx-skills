# State Publication Standard Operating Procedure (SOP)

Publish a redacted, portable snapshot of this project's CarryCtx state after a
merge, so the engineering workflow (tasks, checkpoints, decisions, sessions) is
reviewable alongside the code — and recover a fresh clone from that snapshot
when needed. CarryCtx never touches the network: `carryctx export --publication`
writes a redacted Git commit to a local ref; moving that ref is always a
user-run `git push`.

## Phase 1: Choose the publication target

1. Decide where the redacted snapshot lives before the first publish:
   - **Source repository, its own branch.** Push `refs/heads/carryctx-snapshots`
     to the source repo. Simplest; use it when the source repo is already public.
   - **Dedicated mirror repository.** Push the same ref to a separate
     `*-workflow` repository. Use it when the source repo is private but the
     snapshot must be public, when snapshot history should stay out of ordinary
     `git clone`s, or when publication should use a different credential than
     source push.
2. Prefer one publication target per source repository. Several per-source
   mirrors can be collapsed into one mirror with one branch per source.
3. Record the decision once in the project's docs; do not re-litigate it on
   every merge.

## Phase 2: Publish a redacted snapshot (after merge)

1. From the merged checkout on the default branch, run
   `carryctx export --pack-format dir -o .carryctx/publish --publication`. This
   redacts every table row and `project.json`, stamps `"redacted": true` in
   `manifest.json`, and commits the bundle to `refs/heads/carryctx-snapshots`.
2. Preview first with
   `carryctx export --pack-format dir -o .carryctx/publish --publication --dry-run`
   when you want the target ref and commit without writing anything.
3. Never hand-roll redaction. Do not post-process bundle JSONL with your own
   scripts — the built-in pass is the only one that also stamps the manifest
   flag CarryCtx uses to refuse the artifact as a merge source.
4. Moving the ref is the user's job: `git push <remote> refs/heads/carryctx-snapshots`.
   CarryCtx never pushes or fetches.

## Phase 3: Recover a fresh clone from the snapshot

1. Fetch the published ref into a local remote-tracking ref:
   `git fetch <remote> refs/heads/carryctx-snapshots:refs/remotes/<remote>/snapshots`.
2. Restore the state DB with
   `carryctx import --from-git refs/remotes/<remote>/snapshots --mode replace`.
3. A redacted snapshot is a publication artifact: `carryctx import --from-git refs/remotes/<remote>/snapshots --mode merge`
   refuses it (`UNSUPPORTED_OPERATION`, exit 10). Use fresh import or
   `--mode replace` only — never merge a redacted bundle, because its redacted
   placeholders are not real values.

## Guardrails

- **Never push an unredacted snapshot ref.** `refs/carryctx/local` is local-only;
  publish only the redacted `refs/heads/carryctx-snapshots`.
- **Never merge a published snapshot back.** It is for review and recovery, not
  for merging state between clones.
- **One redaction implementation.** Rely on `carryctx export --publication` for
  the guarantee; do not add a second script that rewrites bundle files.
- **Verify before pushing.** Confirm `"redacted": true` in the bundle's
  `manifest.json`.
