# `commit-tag-push`

Ship in one step: Conventional Commit, version bump, changelog release section, tag, then
push the commits and the tag.

This is the only skill here that touches the remote. [`commit`](../commit/) never pushes, so
local commits pile up until you run this.

## Usage

```
/commit-tag-push              # auto-detect the bump
/commit-tag-push patch
/commit-tag-push minor closes #42
/commit-tag-push 2.1.0
```

The first token is the version directive; the rest is free-text context.

| Directive | Resolves to |
| --- | --- |
| `X.Y.Z` | Exactly that. A leading `v` is stripped. |
| `patch` / `minor` / `major` | That segment of the current version, incremented, lower segments zeroed. |
| absent, or unrecognized | Auto-detected — and the whole argument is treated as context. |

Under a date-based scheme the directive is ignored, because the version is today's date. The
skill says so in its report rather than pretending the argument did something.

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

## What it pushes

Both the commits and the tag, as two separate commands so a failure on either is visible.

The commit push carries **every unpushed commit on the branch**, not just the one written
here. That is the intended workflow: `/commit` as many times as you like while you work,
then one `/commit-tag-push` to cut the release and send everything. The skill lists the
pending commits in its context before it starts and reports the total it pushed.

## What it does beyond `/commit`

- Always cuts a release. Under SemVer that means folding the **entire** `[Unreleased]`
  section — including entries left by earlier `/commit` runs — into a new release header and
  leaving a fresh empty `[Unreleased]`. Under a date-based scheme there is nothing to fold:
  the day's entries are already sitting under `## <today>`, and that section *is* the release.
- Maintains the reference-style compare-links block at the bottom of `CHANGELOG.md` if one
  exists: repoints `[Unreleased]:` at the new tag and inserts a link comparing the new tag
  against the previous one. The repo URL is read from `git remote get-url origin`, not
  assumed; with no remote, the block is skipped.
- Refuses before touching anything if the target version already exists — as a tag, or as a
  changelog section in a repo with no tags. For bump-keyword and auto-detect modes it
  computes the concrete `X.Y.Z` first, specifically so the collision check happens before any
  file is written.

## Project support

Same detection as [`commit`](../commit/): manifest from `Cargo.toml` / `package.json` /
`pyproject.toml` / none, and the versioning scheme from the latest tag — falling back to the
changelog's existing release headers when the repo has no tags, then to the manifest's `version`
field.

With **no signal anywhere** — no tag, no changelog, no manifest version — it asks instead of
assuming: whether to create a `CHANGELOG.md`, and which scheme to use (SemVer `vX.Y.Z`,
`YYYY-MM-DD`, or `YYYYMMDD`), both in one prompt, before it stages or writes anything. This
skill always tags, so it always needs the scheme answer.

## Initial commit

Works in a repo with no commits: no `HEAD`-based command is run against an unborn branch, the
diff is replaced by a listing of the files that would go in, and the push becomes
`git push -u origin <branch>`.

Because the whole point is pushing, the remote is checked **first**. A fresh repo with no remote
stops the run before anything is staged — with a suggestion to add one, or to use
[`commit`](../commit/) for a local commit and tag — rather than committing and failing at the
push.

Bump keywords and auto-detection have nothing to work from on a first release: the version
resolves to the manifest's version if there is one, `0.1.0` otherwise, or today's date under a
date-based scheme. An explicit `X.Y.Z` still applies exactly, and the report says when a
directive was ignored.

## Adapting it

- **The never-auto-major rule** is the one most people will want to change. It is a single
  bullet in the "Version argument" section.
- **Changelog compare links** assume a GitHub-style `/compare/a...b` URL. Change the
  template for GitLab or others.
- **Pre-release versions** are not supported: `X.Y.Z` only, no `-rc.1` or build metadata.
- **Pushing to a branch other than the current one** is not handled; it pushes what you are
  on.
