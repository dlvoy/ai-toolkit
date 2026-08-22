# Skills

Agent Skills for git hygiene: Conventional Commits in, Keep a Changelog out, no AI
attribution anywhere in the history.

| Skill | Use it when |
| --- | --- |
| [`commit`](commit/) | Everyday commits. Writes the commit and a `[Unreleased]` changelog entry, then pushes. Cuts a release too, but only if you ask with `as patch\|minor\|major\|X.Y.Z`. |
| [`commit-and-tag`](commit-and-tag/) | You are shipping. Always bumps the version, folds `[Unreleased]` into a release section, tags, and pushes — and can work out the bump size from the commit types since the last tag. |

If you only install one, install `commit` — it does the release path as an argument.
`commit-and-tag` exists because "release now" deserves its own verb, and because it can
auto-detect the bump.

## Prerequisites

- **A git repo with a remote.** The compare links in `commit-and-tag` come from
  `git remote get-url origin`; without a remote that step is skipped.
- **`CHANGELOG.md` at the repo root.** Created for you if missing.
- **Conventional Commits already in use**, ideally. `commit-and-tag`'s auto-detection reads
  the types of commits since the last tag; unparseable history falls back to a patch bump.
- **A version manifest, or none.** Cargo, npm, and pyproject are detected and written to;
  a repo with no manifest works fine — the tag becomes the only record of the version.
- **Node** must be on `PATH` for npm projects, **cargo** for Rust projects. Only the branch
  matching your project runs.

## Installing

The Agent Skills format is shared, so the same folder works in both tools:

```bash
cp -r commit ~/.claude/skills/        # Claude Code, all projects
cp -r commit ~/.copilot/skills/       # Copilot in VS Code, all projects
cp -r commit .claude/skills/          # this project (Copilot reads this path too)
cp -r commit .github/skills/          # this project, Copilot's own path
```

Then invoke as `/commit` or `/commit-and-tag`. Both set
`disable-model-invocation: true`, so they never fire on their own — a commit only ever
happens because you asked for one.

The `README.md` in each skill folder is documentation for this repo, not part of the
skill. Copying it along is harmless.

## Design notes

**Versioning is detected, not assumed.** The scheme comes from the shape of the latest tag:
`v1.2.3` means SemVer, an 8-digit `20260815` means date-based, no tags means SemVer. The
project type comes from which manifest exists. Earlier versions of these skills hard-coded
one project and one scheme each, which made them useless outside the repo they came from.

**Attribution is stripped at the prompt level.** Both skills forbid `Co-Authored-By`
trailers, generated-by lines, and tool or model names in commit messages, then re-read the
message with `git log -1` afterwards and amend if one slipped through. This is deliberately
redundant with the `attribution` setting — see
[the note on that](../howto/claude-disabling-attribution.md) — because the setting is
per-machine and the skill travels with the repo.

**`--force` and `--no-verify` are refused**, always.

## Attribution

Mine, written for my own projects. They implement three third-party specifications:

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)

The rule text in each `SKILL.md` paraphrases those specs so the agent has them in context.
Read the specs themselves if you want the authoritative wording.
