# Latest Neo version

Resolve the latest **released** Neo version (`X.Y.Z`) and use it as the git `ref`. Prefer a version tag over a branch.

Discover Neo Docs MCP tools and read their schemas before calling them. Do not assume tool names.

## Preferred: Neo Docs MCP

Read the release notes page (URL path `/release-notes` → `/release-notes.mdx` on the docs filesystem).

The latest release is the first `<Update>` whose `tags` include `"Latest"`:

```mdx
<Update label="1.12.1" tags={["Latest"]} description="26-08-2026">
```

`{VERSION}` is that `label`. If no `Latest` tag exists, use the first `<Update label="X.Y.Z">` on the page (newest is at the top).

`label` must match `^\d+\.\d+\.\d+$`. Ignore prerelease labels.

## Fallback: docs website

If the MCP is missing or fails, fetch `https://neo.tvk.company/release-notes.md` (Mintlify markdown, not the HTML page). Parse the same `<Update label="..." tags={["Latest"]}>` shape as the MCP source.

If `.md` is unavailable, fetch `https://neo.tvk.company/release-notes` and take the first `data-component-part="update-label"` whose nearby `update-tag` is `Latest`, else the first `update-label` matching `^\d+\.\d+\.\d+$`.

Do not scrape unrelated pages. Do not use GitHub as the first fallback.

## If version cannot be determined

Set `{VERSION}` to `main` and say so in the confirmation plan. Do not use `production` or `development`.
