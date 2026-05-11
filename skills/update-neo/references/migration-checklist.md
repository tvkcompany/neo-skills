# Migration Checklist

Use this checklist after release notes have been reduced to concrete must-apply and optional items.

## Build a Migration Map

For each relevant release note item, capture:

- Affected public API (`NeoButton`, `NeoTableColumn.label`, `theme.colors.brand`, etc.).
- Change type: rename, removal, replacement, new required shape, deprecation, or optional improvement.
- Old pattern to search for.
- New pattern to apply.
- Docs page URL or MCP path used as evidence.

Do not include `Neo*Primitive` APIs unless the user's app imports them directly; they are internal implementation details.

## Search Strategy

Search project-owned Dart code first:

- `lib/`
- `test/`
- `integration_test/`
- `example/` or `examples/`

Also inspect `analysis_options.yaml`, `pubspec.yaml`, and generated localization/router entry points only when release notes mention configuration-level changes.

Prefer exact symbols before broad searches:

```text
NeoButtonVariant.filled
bgHoverColor:
NeoTableColumn(
theme.colors.fgBrand
```

Then search the affected class or widget name to catch less obvious usages.

## Edit Rules

- Edit one file at a time.
- Preserve user comments, especially `// TODO:` and `// FIX:`.
- Keep migrations minimal and local to the breaking change unless the user opted into optional improvements.
- Use type-safe Dart, existing project style, and the project's formatting.
- When replacing enum values, prefer Dart dot shorthands only if the surrounding code already has enough type context.
- When a replacement requires a behavioural choice, do not invent it. Mark the item as `Skipped (needs human)`.

## Common Migration Patterns

### Rename a named parameter

Before:

```dart
NeoTableColumn(
  name: 'Name',
)
```

After:

```dart
NeoTableColumn(
  label: 'Name',
)
```

### Replace split interaction colors

Before:

```dart
NeoButton(
  bgHoverColor: hoverColor,
  bgPressedColor: pressedColor,
)
```

After:

```dart
NeoButton(
  bgInteractionColor: hoverColor,
)
```

If hover and pressed colors differ, choose the more semantically appropriate existing token only when obvious. Otherwise report it as needing human review.

### Convert ordered cells to keyed cells

Before:

```dart
NeoTableRow(
  cells: [
    Text(user.name),
    Text(user.email),
  ],
)
```

After:

```dart
NeoTableRow(
  cells: {
    'name': Text(user.name),
    'email': Text(user.email),
  },
)
```

Only do this when column IDs are available in the same file or an obvious nearby declaration. Otherwise report the file as needing human review.

## Optional Improvements

Only propose optional changes when the project already uses the affected widget/API. Examples:

- A release adds `emptyStateBuilder` to `NeoDropdownField` and the project has custom empty-state code nearby.
- A release adds `activeRowId` to `NeoTable` and the project has selected-row state.
- A release improves a widget's default behaviour and the project has workaround code that can be removed.

Do not apply optional changes unless the user chose the optional scope.

## Verification

After edits, run the project's Flutter commands through the detected toolchain:

```sh
(fvm) flutter pub get
(fvm) dart format .
(fvm) flutter analyze
(fvm) flutter test
```

Skip `flutter test` when no `test/` directory exists. If failures appear:

1. Fix clear migration-caused errors.
2. Re-run the smallest useful command.
3. Report remaining failures with file paths and the likely owner/action.

Do not hide or roll back failures silently.

## Summary Data to Track

Track enough information while editing to produce the final summary:

- Old and new Neo versions.
- Files changed.
- Must-apply changes applied.
- Optional changes applied or left available.
- Items skipped because they need human judgement.
- Verification command results.
