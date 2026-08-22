# `commit`

Stage, write a Conventional Commit, add a Keep a Changelog entry under `[Unreleased]`,
verify no AI attribution crept into the message, and push.

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

| Invocation | Version | Tag | Changelog |
| --- | --- | --- | --- |
| `/commit` | untouched | none | entry under `[Unreleased]` |
| `/commit as <version>` | bumped in the manifest | created and pushed | `[Unreleased]` folded into a release section |

Plain `/commit` never touches the version, the manifest, or a tag. That separation is the
point of the skill: most commits are not releases.

## What it does

1. Reads branch, status, diff, latest tag, project manifest, and the top of the changelog
   into context before deciding anything.
2. Refuses up front if the target tag already exists — before staging or writing a thing.
3. Stages the relevant files, never `.env`, secrets, or build artifacts.
4. Picks a type and scope from the actual diff, and stops to propose a split if the diff
   contains unrelated changes needing different types.
5. Writes the changelog entry as something a human would want to read, not a restated
   commit subject.
6. Commits via heredoc so bodies and footers keep their newlines.
7. Re-reads the message with `git log -1` and amends if an attribution trailer appears.
8. Tags and pushes when a version argument was given.

## Project support

The manifest is detected, in this order: `Cargo.toml`, `package.json`, `pyproject.toml`,
then none. The versioning scheme is detected from the latest tag — `v1.2.3` for SemVer,
`20260815` for date-based, SemVer when there are no tags. Under the date-based scheme
`patch`/`minor`/`major` have no meaning and today's date is used instead; the skill reports
that rather than pretending the keyword did something.

## Adapting it

Likely edits when you install this somewhere new:

- **Changelog groups** — the six Keep a Changelog groups are listed in a table; add or
  rename to taste.
- **What skips a changelog entry** — currently `chore`, `ci`, `style`, `test`, and most
  `refactor`.
- **Tag prefix** — the skill matches your existing tags and defaults to `v`.
- **Push behaviour** — it pushes on every run. Delete Step 7 if you would rather review
  before pushing.
