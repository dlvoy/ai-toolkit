# `commit-and-tag`

Ship a release in one step: Conventional Commit, version bump, changelog release section,
tag, push.

## Usage

```
/commit-and-tag              # auto-detect the bump
/commit-and-tag patch
/commit-and-tag minor closes #42
/commit-and-tag 2.1.0
```

The first token is the version directive; the rest is free-text context.

| Directive | Resolves to |
| --- | --- |
| `X.Y.Z` | Exactly that. A leading `v` is stripped. |
| `patch` / `minor` / `major` | That segment of the current version, incremented, lower segments zeroed. |
| absent, or unrecognized | Auto-detected — and the whole argument is treated as context. |

### Auto-detection

Reads the Conventional Commit types of every commit since the latest tag, plus the type of
the commit it is about to write:

- any `feat` → **minor**
- otherwise → **patch**
- **never major**, even for a `!` marker or a `BREAKING CHANGE:` footer

That last rule is deliberate. A major bump is a decision about your users, not something to
infer from a commit message. When a breaking marker is seen the bump is still capped at
minor and the report says so, so you can re-run with an explicit `major` if that is what
you meant.

## What it does beyond `/commit`

- Always cuts a release, folding the **entire** `[Unreleased]` section — including entries
  left by earlier plain `/commit` runs — into a new release header, then leaving a fresh
  empty `[Unreleased]`.
- Maintains the reference-style compare-links block at the bottom of `CHANGELOG.md` if one
  exists: repoints `[Unreleased]:` at the new tag and inserts a link comparing the new tag
  against the previous one. The repo URL is read from `git remote get-url origin`, not
  assumed; with no remote, the block is skipped.
- Refuses before touching anything if the target tag already exists. For bump-keyword and
  auto-detect modes it computes the concrete `X.Y.Z` first, specifically so the collision
  check happens before any file is written.

## Project support

Same detection as [`commit`](../commit/): manifest from `Cargo.toml` / `package.json` /
`pyproject.toml` / none, scheme from the latest tag's shape. Under the date-based scheme
the target version is today's `YYYYMMDD` and the version argument is meaningless — the
skill says so instead of ignoring it silently, and the tag-collision refusal is what
prevents a second release on the same day.

## Adapting it

- **The never-auto-major rule** is the one most people will want to change. It is a single
  bullet in the "Version argument" section.
- **Changelog compare links** assume a GitHub-style `/compare/a...b` URL. Change the
  template for GitLab or others.
- **Pre-release versions** are not supported: `X.Y.Z` only, no `-rc.1` or build metadata.
