# Release Notes Fetching

Use the Neo Docs MCP first. Fall back to the public docs URLs only when the MCP is unavailable or cannot return the needed page.

## Preferred: Neo Docs MCP

Before calling any Neo Docs MCP tool, discover the available tools and read the relevant tool descriptor/schema. Do not assume specific tool names, argument names, filesystem paths, or response shapes; the MCP tool descriptions are the source of truth and may change over time.

Use the MCP for two jobs:

- Find the release notes page and read its full content.
- Search or fetch specific docs pages mentioned by the release notes when more migration detail is needed.

When the MCP exposes both search and page-fetch/read capabilities, prefer reading the full release notes page first, then use search only to locate follow-up pages whose paths are not obvious from links in the release notes. Always pass parameters exactly as described by the current tool schema.

## Fallback: Public URLs

If the MCP is not installed or a tool call fails because the server is unavailable, fetch public docs pages:

- Release notes: `https://neo.tvk.company/release-notes`
- Docs home: `https://neo.tvk.company/`
- Widget pages: `https://neo.tvk.company/widgets/{category}/{slug}`
- Layout pages: `https://neo.tvk.company/layouts/{slug}`
- Utility pages: `https://neo.tvk.company/utilities/{slug}`
- Theming pages: `https://neo.tvk.company/theming/{slug}`

Use the fetched page content as source material. Do not scrape unrelated pages unless release notes or search results point there.

## Version Range

Given `OLD_VERSION` and `NEW_VERSION`, extract only release note blocks where:

```text
OLD_VERSION < label <= NEW_VERSION
```

Release note blocks use this shape:

```mdx
<Update label="1.9.0" ...>
  # 1.9.0
  ...
</Update>
```

Process matching releases oldest to newest so later entries can supersede earlier migration guidance.

## Section Mapping

Treat section titles case-insensitively and ignore emoji when matching:

- `BREAKING CHANGES` -> must apply.
- `Removed` -> must apply.
- `Deprecated` -> must apply when a replacement is documented; otherwise report.
- `New` -> optional.
- `Improvements` -> optional only when the project uses the affected API.
- `Fixes` -> informational unless a code change is clearly required.

Ignore internal implementation details unless the user's app directly imports the affected public API.

## Page Lookup Hints

Release notes usually link public APIs like:

```mdx
[`NeoButton`](/widgets/buttons/button)
```

Use the link or page path in the format required by the currently available MCP tool. Do not assume a `.mdx` suffix unless the tool description explicitly says to use one.

If a release note mentions a symbol without a link, search first, then read the best matching page. Prefer official docs pages over inferred source-code assumptions.

## Failure Handling

If neither MCP nor HTTPS docs are available, stop before editing project files. Report that release notes could not be read, because migration guidance is the source of truth for this skill.
