---
name: update-neo
description: Updates the Neo Flutter package in a project to the latest version, reads Neo release notes and docs for every version spanned, applies breaking-change migrations, and proposes optional improvements. Use when the user asks to update Neo, upgrade the Neo package, bump Neo to the latest version, migrate after a Neo release, or run /update-neo.
compatibility: Requires a Flutter project with neo as a dependency. Uses fvm when present, otherwise plain flutter. Optionally uses the Neo Docs MCP; falls back to HTTPS fetches from https://neo.tvk.company/.
---

# Update Neo

Update a Flutter project's Neo dependency, migrate required breaking changes from the release notes, and propose optional improvements the project can benefit from.

Keep output concise. Do not commit, push, create branches, or open PRs. Leave all edits in the working tree for the user to review.

References:

- [Release notes fetching](references/release-notes-fetching.md) - Neo Docs MCP commands and HTTPS fallback.
- [Migration checklist](references/migration-checklist.md) - how to translate release notes into focused code edits.

## When to use

Use this skill when the user asks to:

- Update, upgrade, or bump the `neo` Flutter package.
- Migrate a Flutter app after a Neo release.
- Fix breaking changes from Neo release notes.
- Run `/update-neo`.

Do not use it for releasing Neo itself, updating Neo documentation, or upgrading unrelated Flutter packages.

## Workflow

### 1. Preflight

1. Find the project root by locating `pubspec.yaml` in the current directory or nearest parent. Stop if none exists.
2. Confirm `neo` appears under `dependencies:` or `dev_dependencies:`. Stop if it is not a dependency.
3. Check git status if the project is a git repo. If files outside `pubspec.yaml` and `pubspec.lock` are dirty, warn the user and ask before continuing.
4. Detect Flutter tooling:
   - Use `fvm flutter` and `fvm dart` when `.fvmrc` or `.fvm/` exists at the project root.
   - Otherwise use `flutter` and `dart`.
5. Verify the chosen Flutter command is available. If not, stop with the exact missing command.

### 2. Determine Versions

1. Read `pubspec.lock` and record `OLD_VERSION` from `packages.neo.version`.
2. If `pubspec.lock` is missing or does not include Neo, read the Neo constraint from `pubspec.yaml` and treat the resolved current version as unknown.
3. Record the raw Neo constraint from `pubspec.yaml`.
4. Run `(fvm) flutter pub outdated --json` and parse Neo's latest version.
5. If `pub outdated` cannot determine the latest version, fall back to GitHub releases if available.
6. If Neo is already at the latest version, stop with `Neo is already up to date at {version}.`

### 3. Check the Constraint

If the `pubspec.yaml` constraint does not allow the latest Neo version, stop and ask the user before editing it. Include:

- Current constraint.
- Latest Neo version.
- Proposed replacement constraint.

Proceed only after explicit approval. If the user declines, exit cleanly and say a manual constraint bump is required.

### 4. Upgrade Neo

Run:

```sh
(fvm) flutter pub upgrade neo
```

Then re-read `pubspec.lock` and record `NEW_VERSION`. If the resolved version did not change, stop and explain whether the constraint, dependency overrides, or a path/git dependency blocked the upgrade.

### 5. Read Release Notes and Docs

Read [Release notes fetching](references/release-notes-fetching.md), then fetch the release notes through the Neo Docs MCP when available. Fall back to the public docs URLs only when the MCP is unavailable.

Extract every `<Update label="x.y.z" ...>` block where `x.y.z` is greater than `OLD_VERSION` and less than or equal to `NEW_VERSION`.

Classify release note sections:

- `BREAKING CHANGES` - must apply.
- `Removed` - must apply.
- `Deprecated` - must apply when a replacement is available; otherwise report.
- `New` - optional.
- `Improvements` - optional only when the project uses the affected API.
- `Fixes` - informational unless they point to a required code change.

For each must-apply item, fetch the relevant docs page when the release note does not provide enough information to make a type-safe edit.

### 6. Scan the Project

Search `lib/`, `test/`, `integration_test/`, and example app folders when they exist. Focus on `.dart` files and project-owned code.

Create two groups:

- **Must apply**: concrete edits needed for breaking changes, removals, and actionable deprecations.
- **Optional**: project usages that could benefit from new parameters, new widgets, or improved behaviour.

Do not guess. If a required migration is ambiguous, add it to `Skipped (needs human)` with the file and reason.

### 7. Ask What to Apply

Before editing project code, print a compact preview:

```markdown
## Must apply
- `path/to/file.dart`: short migration description

## Optional
- `path/to/file.dart`: short improvement proposal
```

Ask whether to apply only must-apply migrations or must-apply plus optional improvements. Stop cleanly if the user declines both.

### 8. Apply and Verify

Follow [Migration checklist](references/migration-checklist.md). Edit one file at a time using the IDE edit tooling so failed matches are visible.

After edits, run:

```sh
(fvm) flutter pub get
(fvm) dart format .
(fvm) flutter analyze
(fvm) flutter test
```

Skip `flutter test` when no `test/` directory exists. If analyze or tests fail, do not roll back. Fix clear issues caused by the migration; otherwise report the remaining failures.

### 9. Summarize

Finish with:

```markdown
## Neo updated {OLD_VERSION} -> {NEW_VERSION}

### Applied
- `path/to/file.dart`: change summary

### Skipped (needs human)
- `path/to/file.dart`: reason

### Optional improvements available
- Widget or API: short proposal with docs link

### Verification
- pub get: ok / failed
- format: ok / failed
- analyze: clean / N issues
- tests: passed / failed / not present
```

Drop empty sections. Keep it short and do not mention implementation details the user does not need.

## Edge Cases

- **Same version**: stop after version detection.
- **Downgrade requested**: refuse; Neo migrations are one-way. Suggest manually pinning the dependency if they truly need a downgrade.
- **`git:` or `path:` Neo dependency**: skip `pub upgrade neo`; report the resolved version and perform release-note analysis only when a version range can be determined.
- **MCP unavailable**: fall back to `https://neo.tvk.company/release-notes` and relevant docs pages.
- **No `test/` directory**: skip tests and report `not present`.
- **Major version jump**: warn that the migration may require extra manual review before editing.
- **Ambiguous migration**: do not guess. Report it in `Skipped (needs human)`.

## References

- [Release notes fetching](references/release-notes-fetching.md)
- [Migration checklist](references/migration-checklist.md)
