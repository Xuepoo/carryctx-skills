# Git-Backed Sync Standard Operating Procedure (SOP)

This workflow moves CarryCtx project state across machines through Git instead of
a sync server: `export` serializes state into a portable directory, Git carries
the bytes, and `import` restores them. CarryCtx never touches the network; the
binary ships no network stack. Requires CarryCtx 0.8.2+.

## Phase 1: One-Time Setup

1. **Upgrade and back up**: `carryctx --version` must be 0.8.2+, then
   `carryctx project backup --format json`.
2. **Commit the declarative config**: `.carryctx/config.toml` is designed for
   version control. Commit it if it is not tracked yet.
3. **Slim the database (optional)**: `carryctx project prune --older-than-days 90`
   archives old completed tasks so the first snapshot stays small.
4. **Create the snapshot branch**: an orphan branch keeps snapshots out of the
   main history, so no `.gitignore` change is needed on `main`:
   `git checkout --orphan carryctx-snapshots`, `git rm -rf .` (clears the index
   only), `carryctx export --pack-format dir -o . --format json`,
   `git add -A`, commit, `git push -u origin carryctx-snapshots`,
   then `git checkout main`.

## Phase 2: Pre-Push Hook Automation

1. **Check for existing hooks first**: `cat .git/hooks/pre-push`. Chain to any
   existing content instead of overwriting it. (CarryCtx's own `hooks install`
   manages `post-commit`, so `pre-push` is the collision-free slot.)
2. **Install the hook** at `.git/hooks/pre-push` (executable). It operates on
   the snapshot branch through a linked worktree, never `checkout`, so a dirty
   working tree cannot break it:

   ```sh
   #!/bin/sh
   [ -n "$CARRYCTX_SNAP_INNER" ] && exit 0
   case "$(git rev-parse --abbrev-ref HEAD)" in carryctx-snapshots) exit 0;; esac
   WT="${XDG_CACHE_HOME:-$HOME/.cache}/carryctx-snapshots/$(basename "$(git rev-parse --show-toplevel)")"
   git worktree list | grep -q "$WT" || git worktree add -q "$WT" carryctx-snapshots 2>/dev/null || exit 0
   [ -d "$WT" ] || exit 0
   export CARRYCTX_AGENT="${CARRYCTX_AGENT:-$(whoami)}"
   carryctx export --project "$(git rev-parse --show-toplevel)" --pack-format dir -o "$WT" --format json >/dev/null \
     || { echo "carryctx export failed; push aborted"; exit 1; }
   git -C "$WT" add -A
   git -C "$WT" diff --cached --quiet || CARRYCTX_SNAP_INNER=1 git -C "$WT" commit -qm "chore(ctx): snapshot $(date -u +%FT%TZ)" --no-verify
   git -C "$WT" push -q origin HEAD:carryctx-snapshots || { echo "snapshot push failed; push aborted"; exit 1; }
   ```

   `--no-verify` on the machine-generated snapshot commit skips the heavy
   language hooks; the message format is controlled. An export failure aborts
   the code push so history never silently gaps.

3. **Tag milestones by hand**: `git tag ctx-snap-v<X.Y.Z> carryctx-snapshots`
   at releases so code tags and state snapshots correspond one to one.

## Phase 3: Daily Push / Pull and Onboarding

1. **Push (serial, one writer at a time)**: a normal `git push` now carries a
   snapshot with it. Before pushing, `git fetch` and compare `created_at` /
   `counts` in the remote `manifest.json`; if the remote is newer than your
   local state, stop and reconcile first.
2. **Inspect before importing**: `git log -p carryctx-snapshots -- manifest.json`
   shows task-count evolution; `jq .counts` confirms the bundle matches
   expectations.
3. **Take over on a new machine**:
   `git worktree add /tmp/ctx-snap origin/carryctx-snapshots`,
   `carryctx import /tmp/ctx-snap --mode replace --yes --format json`,
   `carryctx doctor`, then
   `carryctx doctor --prune-stale-worktrees --yes` to drop the other machine's
   absolute worktree paths. `--mode replace` keeps an automatic `pre_import_*`
   backup, recoverable with `project restore`.
4. **Read history without importing**: `git log --oneline carryctx-snapshots`
   is enough to review what happened; importing is only needed to continue work.

## Red Lines

1. **Never auto-import in hooks** (e.g. `post-merge`): silently replacing local
   state is a surprise. Hooks push; humans pull.
2. **Never merge the snapshot branch into `main`**: it is a parallel timeline,
   merging it pollutes code history.
3. **Private repositories only**, unless the bundle is scrubbed or encrypted:
   snapshots contain hostnames, absolute paths, agent names, and raw task text
   that may include pasted secrets.
4. **Re-import without `--mode` is refused** (`STATE_CONFLICT`); `--mode merge`
   is not implemented yet and reports `UNSUPPORTED_OPERATION`. Concurrent edits
   resolve last-writer-wins until merge lands, so keep one writer at a time.
