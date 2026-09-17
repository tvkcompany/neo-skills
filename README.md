# Neo Skills

Agent skills for working with [Neo](https://neo.tvk.company/), TVK's Flutter framework.

## Install

```sh
npx skills add tvkcompany/neo-skills
```

## Skills

### `create-neo-project`

Creates a Flutter app with Neo wired in, or adds Neo to an existing Flutter project. Detects an empty folder, a projects root, or an existing Flutter app, shows a plan, and waits for confirmation before changing anything.

Use it when you want an agent to scaffold a new Neo app or migrate an existing Flutter app onto Neo.

### `update-neo`

Updates the Neo Flutter package in a project, reads the Neo release notes and docs for every version spanned, applies breaking-change migrations, and proposes optional improvements.

Use it when you want an agent to upgrade a Flutter project from one Neo version to another and handle the migration work guided by the official docs.

## Resources

- Docs: https://neo.tvk.company/
- Install: https://neo.tvk.company/install
- Release notes: https://neo.tvk.company/release-notes
- MCP: https://neo.tvk.company/mcp
