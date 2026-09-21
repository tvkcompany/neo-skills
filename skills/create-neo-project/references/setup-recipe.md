# Setup recipe

Canonical Neo install recipe. Prefer the published page at `https://neo.tvk.company/install` when Neo Docs MCP or HTTPS is available. Use this file when docs cannot be fetched.

Do not use `phosphor_flutter` or static `.otf` font files.

## Toolchain

Use `fvm flutter` / `fvm dart` when `.fvmrc` or `.fvm/` exists at the project root. Otherwise `flutter` / `dart`.

## Flutter create (new projects only)

```sh
(fvm) flutter create --org {org} --project-name {name} --platforms {platforms} {target}
```

`{target}` is `.` for in-place create, or the project folder name for sibling create.

## pubspec.yaml

### Neo git dependency

`{VERSION}` is the latest Neo release tag from [Latest version](latest-version.md). If that cannot be determined, use `main`. Do not use `production` or `development`.

```yaml
neo:
  git:
    url: git@github.com:tvkcompany/neo.git
    ref: {VERSION}
```

Do not add Neo with `flutter pub add neo` from pub.dev.

### Packages (new projects)

Runtime: `auto_route`, `flutter_hooks`, `gap`, `hooks_riverpod`, `phosphoricons_flutter`, `riverpod_annotation`

Dev: `auto_route_generator`, `build_runner`, `riverpod_generator`

Install with `(fvm) flutter pub add ...` and `(fvm) flutter pub add --dev ...` after the git dependency is in `pubspec.yaml`, then `(fvm) flutter pub get`.

Existing projects: add only packages that are missing. Skip auto_route and its generator when the app already has a `RouterConfig`.

### Fonts

```yaml
flutter:
  fonts:
    - family: Inter
      fonts:
        - asset: packages/neo/assets/fonts/inter_variable.ttf
        - asset: packages/neo/assets/fonts/inter_variable_italic.ttf
          style: italic
    - family: Geist Mono
      fonts:
        - asset: packages/neo/assets/fonts/geist_mono_variable.ttf
        - asset: packages/neo/assets/fonts/geist_mono_italic_variable.ttf
          style: italic
```

Merge into existing `flutter:` keys. Do not delete unrelated `assets:` entries.

## analysis_options.yaml

Merge; do not replace the whole file:

```yaml
analyzer:
  errors:
    invalid_annotation_target: ignore

formatter:
  trailing_commas: preserve
```

## App shell (new projects)

`lib/main.dart`:

```dart
import 'package:flutter/widgets.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:neo/neo.dart';

import 'router/app_router.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  NeoInitializer.initialize().then((_) {
    runApp(
      ProviderScope(
        child: MyApp(),
      ),
    );
  });
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final appRouter = ref.watch(routerProvider);

    return NeoApp(
      title: "My App",
      defaultThemeMode: .system,
      routerConfig: appRouter.config(),
    );
  }
}
```

Use the real project display name for `title`.

`lib/router/app_router.dart`:

```dart
import 'package:auto_route/auto_route.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import 'app_router.gr.dart';

part 'app_router.g.dart';

@Riverpod(keepAlive: true)
AppRouter router(Ref ref) {
  return AppRouter(ref);
}

@AutoRouterConfig(replaceInRouteName: 'Screen,Route')
class AppRouter extends RootStackRouter {
  final Ref ref;

  AppRouter(this.ref);

  @override
  List<AutoRoute> get routes => [
    CustomRoute(
      path: "/",
      page: WelcomeRoute.page,
      initial: true,
    ),
    RedirectRoute(
      path: "*",
      redirectTo: "/",
    ),
  ];
}
```

`lib/screens/welcome_screen.dart`:

```dart
import 'package:auto_route/auto_route.dart';
import 'package:flutter/widgets.dart';
import 'package:gap/gap.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:neo/neo.dart';

@RoutePage()
class WelcomeScreen extends ConsumerWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = ref.watch(neoCurrentThemeProvider);

    return Container(
      color: theme.colors.bgPrimary,
      child: NeoSafeArea(
        child: Center(
          child: Column(
            mainAxisSize: .min,
            children: [
              Text(
                "Welcome to Neo",
                style: theme.textStyles.header1.copyWith(color: theme.colors.fgPrimary),
              ),
              Gap(theme.spacings.medium),
              NeoButton(
                variant: .filled,
                label: "Get started",
                onPressed: () {},
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

Delete Flutter's default `lib/main.dart` counter app when replacing it.

## Existing projects

- Add Neo, fonts, missing packages, analyzer keys.
- Replace `MaterialApp` / `CupertinoApp` with `NeoApp` only as confirmed.
- Call `WidgetsFlutterBinding.ensureInitialized()` then `NeoInitializer.initialize()` before `runApp`.
- Wrap with `ProviderScope` if missing.
- Keep existing screens.
- `NeoApp.routerConfig` is required. Reuse an existing `RouterConfig`. Introduce auto_route only if the user agrees.

## Code generation

When auto_route or riverpod_annotation files were added or changed:

```sh
(fvm) dart run build_runner build
```

## Style

- `package:flutter/widgets.dart` for custom widgets; add cupertino/material only if needed.
- Dart dot shorthands where the type is known (`.filled`, `.system`, `.min`).
- `Gap(theme.spacings.*)` instead of arbitrary `SizedBox` for Neo UI.
- `phosphoricons_flutter` icons (`PhosphorIconsRegular`, `PhosphorIconsDuotone`), not `phosphor_flutter`.
- No `StatefulWidget`.
- Do not import `package:neo/neo.dart` from inside the `neo` package itself; apps should import `package:neo/neo.dart`.
