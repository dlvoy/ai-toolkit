# `commit`

Stage, write a Conventional Commit, add a Keep a Changelog entry under `[Unreleased]`, and
verify no AI attribution crept into the message.

**It never pushes.** Not the commit, and not the tag when you ask for one. Commits stack up
locally until you push them yourself or run [`commit-tag-push`](../commit-tag-push/).

## Usage

```
/commit
/commit closes #42
/commit as patch
/commit as minor closes #42
/commit as 2.1.0
```

The first token decides the mode. `as` followed by `patch`, `minor`, `major`, or an exact
`X.Y.Z` turns this into a release commit; anything else is free-text context that the model
may use in the commit body or a `Refs:` footer.

| Invocation | Version | Tag | Changelog | Pushed |
| --- | --- | --- | --- | --- |
| `/commit` | untouched | none | entry under `[Unreleased]` | no |
| `/commit as <version>` | bumped in the manifest | created locally | `[Unreleased]` folded into a release section | no |

Plain `/commit` never touches the version, the manifest, or a tag. That separation is the
point of the skill: most commits are not releases.

To send a locally tagged release without cutting another one, push it yourself:

```bash
git push --follow-tags
```

## What it does

1. Reads branch, status, diff, latest tag, project manifest, and the top of the changelog
   into context before deciding anything.
2. Refuses up front if the target version already exists — before staging or writing a thing.
3. Stages the relevant files, never `.env`, secrets, or build artifacts.
4. Picks a type and scope from the actual diff, and stops to propose a split if the diff
   contains unrelated changes needing different types.
5. Writes the changelog entry as something a human would want to read, not a restated
   commit subject.
6. Commits via heredoc so bodies and footers keep their newlines.
7. Re-reads the message with `git log -1` and amends if an attribution trailer appears.
8. Tags when a version argument was given, and reports how far ahead of upstream the branch
   now sits.

## Commit message body

Bodies follow a fixed shape: one or two sentences giving the main idea, then a flat bullet
list of what changed — no group headings, fewer and shorter items than a changelog entry.

```
Rework how both commit skills write messages and changelog entries

- Commit bodies now lead with a summary and a flat list of changes
- Date-based changelogs aggregate into today's section instead of Unreleased
```

Trivial work stays out of the list — typo fixes, formatting, dependency bumps — unless it is
the point of the commit. A list longer than about six bullets is treated as a signal that the
commit should be split. A one-line change gets no body at all.

## Where the changelog entry goes

Under **SemVer**, into `## [Unreleased]`, as usual.

Under a **date-based** scheme, into `## <today>` — and never into `[Unreleased]`, which does
not appear in these changelogs at all. A repo that dates its sections is usually not tagging,
so the dated section is the release. Several commits on the same day accumulate into one
section rather than each starting their own, which is what you want to read back later.

## Project support

The manifest is detected, in this order: `Cargo.toml`, `package.json`, `pyproject.toml`,
then none.

The versioning scheme is detected from the latest tag — `v1.2.3` for SemVer, `2026-08-23` or
`20260815` for date-based. With no tags, it falls back to the shape of the existing changelog
release headers, which is what makes a repo that dates its changelog but never tags work
correctly. With neither signal, SemVer.

Under a date-based scheme `patch`/`minor`/`major` have no meaning and today's date is used
instead; the skill reports that rather than pretending the keyword did something.

## Adapting it

Likely edits when you install this somewhere new:

- **Changelog groups** — the six Keep a Changelog groups are listed in a table; add or
  rename to taste.
- **What skips a changelog entry** — currently `chore`, `ci`, `style`, `test`, most
  `refactor`, and any change to the changelog's own structure.
- **Tag prefix** — the skill matches your existing tags, defaulting to `v` for SemVer and no
  prefix for a date.
- **The no-push rule** — if you want the old behaviour back, add a push step at the end and
  put `Bash(git push *)` back in `allowed-tools`.
