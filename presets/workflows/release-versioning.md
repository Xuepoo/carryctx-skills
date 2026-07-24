# Release Versioning Standard Operating Procedure (SOP)

This workflow defines the standard step-by-step process for cutting a release: pre-release verification, semver bump with changelog, and tag/publish using CarryCtx.

## Phase 1: Pre-Release Verification

1. **Claim Release Task**: `carryctx task claim <TASK_ID>`
2. **Check for Blockers**: `carryctx status --tasks --all` and confirm no open task depends on or blocks this release.
3. **Run Full Test/Lint Suite**: Run unit tests, integration tests, and lint/format checks; do not proceed on any failure.
4. **Log Verification Result**: `carryctx progress note "Pre-release checks passed: tests, lint, no blocking tasks"`

## Phase 2: Version Bump & Changelog

1. **Determine Bump Type**: Inspect merged changes since the last tag and classify as major/minor/patch per semver.
2. **Bump Version**: Update the version field in the project manifest (`Cargo.toml`, `package.json`, etc.).
3. **Write Changelog Entries**: Group entries under `Added`/`Fixed`/`Changed` headings, one line per notable change.
4. **Checkpoint the State**: `carryctx checkpoint --task <TASK_ID> --done "Bumped version to <X.Y.Z>, updated CHANGELOG" --next "Tag and push"`

## Phase 3: Tag & Publish

1. **Create Git Tag**: `git tag -a v<X.Y.Z> -m "Release v<X.Y.Z>"`
2. **Push Tag**: `git push origin v<X.Y.Z>`
3. **Verify CI/CD Publish**: Confirm the CI/CD publish workflow triggered by the tag completes successfully.
4. **Complete Task**: `carryctx task complete <TASK_ID>`
