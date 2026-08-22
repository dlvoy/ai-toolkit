# Keeping Claude attribution out of git

By default Claude Code adds a trailer to commits it writes, and in web or Remote Control
sessions it appends a link back to the session. Both end up in your public history. The
`attribution` setting controls all of it.[^1]

## The setting

```json
{
  "attribution": {
    "commit": "",
    "pr": "",
    "sessionUrl": false
  }
}
```

| Key | Controls | Default |
| --- | --- | --- |
| `commit` | Text appended to commit messages | `"🤖 Generated with Claude Code"` |
| `pr` | Text appended to pull request descriptions | `""` |
| `sessionUrl` | Link to the claude.ai session, in commits and PRs created from web or Remote Control sessions | `true` |

An empty string removes that line entirely. You can also repoint it rather than blank it:

```json
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

`sessionUrl` is a boolean, not text, and is easy to miss — blanking `commit` and `pr`
alone still leaves session links in commits made from web sessions.[^2]

## Where to put it

Pick the settings file that matches how far you want it to reach. Higher in this list
wins when the same key is set in more than one place:[^3]

| File | Applies to |
| --- | --- |
| `.claude/settings.local.json` | You, this project (gitignored) |
| `.claude/settings.json` | Everyone working on this project |
| `~/.claude/settings.json` | You, every project |

For a personal preference like this, `~/.claude/settings.json` is usually the right home.

## `includeCoAuthoredBy` is the old way

The earlier `includeCoAuthoredBy: false` boolean was deprecated in v2.0.62. It still
works, but `attribution` takes precedence when both are set, and only `attribution` can
customize the text or reach the session URL. Use `attribution` in new configuration.[^1]

## Belt and braces

Settings govern the commits Claude Code composes on its own. Skills that write commit
messages can also forbid attribution at the prompt level — the
[`commit`](../skills/commit/) and [`commit-tag-push`](../skills/commit-tag-push/) skills in
this repo both do, and both re-read the message with `git log -1` afterwards to check.
That works regardless of what `settings.json` says, which is useful on a machine whose
configuration you do not control.

[^1]: https://code.claude.com/docs/en/settings

[^2]: https://github.com/anthropics/claude-code/issues/69614

[^3]: https://code.claude.com/docs/en/settings#settings-precedence
