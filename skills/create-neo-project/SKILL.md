---
name: create-neo-project
description: Creates a new Flutter app with Neo wired in, or adds Neo to an existing Flutter project. Detects empty folders, project-root folders, and existing Flutter apps. Confirms the plan before any writes. Use when the user asks to create a Neo project, set up Neo, add Neo to a Flutter app, scaffold a Neo app, or run /create-neo-project.
compatibility: Uses fvm when present, otherwise plain flutter/dart. Optionally uses the Neo Docs MCP; falls back to the baked-in setup recipe and https://neo.tvk.company/install.
---

# Create Neo Project

Create a Flutter app with Neo installed, or add Neo to an existing Flutter app.

Keep output concise. Do not commit, push, create branches, or open PRs. Leave all edits in the working tree for the user to review.

References:

- [Setup recipe](references/setup-recipe.md) - pubspec, fonts, analyzer, app shell, packages, verification.

## When to use

Use this skill when the user asks to:

- Create a new Neo project or Flutter app with Neo.
- Add, install, or wire Neo into an existing Flutter project.
- Run `/create-neo-project`.

Do not use it to upgrade Neo in a project that already depends on it. That is `update-neo`.

## Workflow

### 1. Detect mode

Inspect the **current working directory only**. Do not walk into sibling workspace roots (for example `neo`, `neo-docs`, `playground`) to guess a target.

Find `pubspec.yaml` in the current directory (not a parent).

1. **Existing Flutter** — `pubspec.yaml` exists and declares `sdk: flutter` under `dependencies.flutter`.
   - If `neo` is already in `dependencies` or `dev_dependencies`, stop. Tell the user to run `/update-neo` instead.
   - Otherwise mode is `existing`.
2. **In-place create** — no Flutter `pubspec.yaml`, and the directory is empty aside from ignorable files: `.git`, `.gitignore`, `.DS_Store`, `.cursor`, empty `README` / `README.md`, `LICENSE`. Mode is `in-place`.
3. **Sibling create** — anything else (other projects, files, or a non-empty folder). Mode is `sibling`.

If the cwd is itself a Neo workspace root (`neo`, `neo-docs`, `neo-skills`, `playground`) and the user did not name a new project path, stop and ask where to create the app. Do not scaffold inside those repos.

### 2. Gather inputs

Ask only for values you do not already have:

| Mode | Need |
| --- | --- |
| `in-place` | Organization identifier (reverse domain, e.g. `com.example`). Platforms if the user cares; default `ios,android,web,macos`. Project name from the directory name (must be a valid Dart package name). |
| `sibling` | Project name (snake_case), organization identifier, platforms (same default). |
| `existing` | Nothing required. Optional: whether they want a new auto_route shell or to keep their current router. |

Validate the project name with Flutter's rules: lowercase, numbers, underscores; must start with a letter.

Detect Flutter tooling:

- Use `fvm flutter` and `fvm dart` when `.fvmrc` or `.fvm/` exists at the target root (existing) or will exist after create.
- Otherwise use `flutter` and `dart`.

Verify the chosen Flutter command is available. If not, stop with the missing command.

### 3. Confirm before executing

Print a compact plan, then **stop and wait for explicit confirmation**. Do not create folders, edit files, or run Flutter until the user says to proceed.

```markdown
## Create Neo project

**Mode:** in-place | sibling | existing
**Target:** /absolute/path
**Flutter:** fvm flutter | flutter

### Will run
- `flutter create ...` (omit for existing)

### Will change
- `pubspec.yaml`: neo git dep, packages, fonts
- `analysis_options.yaml`: analyzer + formatter
- `lib/main.dart`: NeoInitializer, ProviderScope, NeoApp
- `lib/router/app_router.dart` and `lib/screens/welcome_screen.dart` (new projects only, or existing only if they asked for a starter)

### Will not
- Commit or push
- Replace existing screens (existing mode)
- Force auto_route over an existing RouterConfig (existing mode)
```

If the user declines, exit cleanly.

### 4. Execute

Follow [Setup recipe](references/setup-recipe.md).

**`in-place`:** `(fvm) flutter create --org {org} --project-name {name} --platforms {platforms} .` then apply the recipe.

**`sibling`:** `(fvm) flutter create --org {org} --project-name {name} --platforms {platforms} {name}` then apply the recipe inside `{name}/`.

**`existing`:** do not run `flutter create`. Apply the recipe onto the current app:

- Add the git dependency, packages, and fonts. Do not remove unrelated dependencies.
- Merge analyzer/formatter settings; do not wipe the rest of `analysis_options.yaml`.
- Show the proposed `main.dart` diff (NeoInitializer + ProviderScope + NeoApp) and apply only after that plan was confirmed.
- Keep existing screens. Do not write `welcome_screen.dart` unless the user asked for a starter screen.
- If the app already has a `RouterConfig` (auto_route, go_router with `.config()`, etc.), wire it into `NeoApp.routerConfig`.
- If the app uses `MaterialApp` / `CupertinoApp` routes that are not a `RouterConfig`, stop and ask before introducing auto_route. `NeoApp` requires `routerConfig`.
- Do not add auto_route (or its generator) when the existing router already satisfies `NeoApp`.

Prefer the published install page via Neo Docs MCP (`/install`) when available. If the MCP is missing, use the recipe file. Do not invent older font filenames or `phosphor_flutter`.

### 5. Verify

From the project root:

```sh
(fvm) flutter pub get
(fvm) dart run build_runner build
(fvm) dart format .
(fvm) flutter analyze
```

Skip `build_runner` when you did not add codegen annotations. If analyze fails because of a change you made, fix it. Do not roll back silently.

### 6. Summarize

```markdown
## Neo project ready

**Mode:** ...
**Path:** ...

### Applied
- short list of files / commands

### Skipped (needs human)
- ...

### Verification
- pub get: ok / failed
- build_runner: ok / failed / skipped
- format: ok / failed
- analyze: clean / N issues
```

Drop empty sections.

## Edge cases

- **Already has Neo:** stop; point to `update-neo`.
- **SSH / GitHub access failure** on `flutter pub get`: explain that Neo is a private git dependency (`git@github.com:tvkcompany/neo.git`) and that SSH must work. Do not switch to HTTPS or a path dependency unless the user asks.
- **Dirty git tree (existing):** warn, include it in the confirmation plan, continue only if they confirm.
- **Invalid project name:** ask for a valid Dart package name.
- **Cwd is a Neo framework/docs/skills/playground checkout:** ask for an explicit target path.
- **User wants a sidebar:** after the app shell works, point them at https://neo.tvk.company/layouts/sidebar. Do not generate a full sidebar starter unless they explicitly ask in a follow-up.
