---
description: Commit using Conventional Commits and add a Keep a Changelog entry. `as patch|minor|major|X.Y.Z` also bumps the project version and tags the release. Never pushes. Use only when explicitly invoked.
disable-model-invocation: true
argument-hint: [ticket id or note] | as <patch|minor|major|X.Y.Z> [ticket id or note]
allowed-tools: Bash(git add *) Bash(git status *) Bash(git diff *) Bash(git commit *) Bash(git branch *) Bash(git rev-parse *) Bash(git rev-list *) Bash(git log *) Bash(git tag *) Bash(git describe *) Bash(git remote *) Bash(npm version *) Bash(node -p *) Bash(cargo update *) Read Edit Write
---

## Current state

Branch: !`git rev-parse --abbrev-ref HEAD`

```!
git status --short
git diff HEAD --stat
```

Today: !`date +%Y-%m-%d` (compact: !`date +%Y%m%d`)

Latest tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "none yet"`

Project manifest and current version:

```!
if [ -f Cargo.toml ]; then
  echo "manifest: Cargo.toml (Rust)"
  grep -n -E '^[[:space:]]*version[[:space:]]*=' Cargo.toml | head -3
elif [ -f package.json ]; then
  echo "manifest: package.json (Node)"
  node -p "require('./package.json').version"
elif [ -f pyproject.toml ]; then
  echo "manifest: pyproject.toml (Python)"
  grep -n -E '^[[:space:]]*version[[:space:]]*=' pyproject.toml | head -3
else
  echo "manifest: none - the git tag is the version"
fi
```

Diff:

!`git diff HEAD`

Top of changelog:

!`head -40 CHANGELOG.md 2>/dev/null || echo "NO CHANGELOG.md AT REPO ROOT"`

Existing changelog release headers (the versioning scheme this repo actually uses):

```!
grep -m5 -E '^## ' CHANGELOG.md 2>/dev/null | grep -viE 'unreleased' || echo "none yet"
```

## This skill never pushes

It commits, and — with a version argument — tags. It does not run `git push`, ever, not even
for the tag. Leaving the branch local is the point: stack up as many `/commit` runs as you
like, review them, then push when you mean to.

To ship what has accumulated, use `/commit-tag-push`, which cuts a release and pushes every
pending commit along with the tag. To push commits made here without cutting another release,
run `git push --follow-tags` yourself.

## Attribution — hard rule

The commit message contains only what is specified below. Never add:

- `Co-Authored-By: Claude` or any other co-author trailer
- `🤖 Generated with Claude Code`, "written by Claude", or any similar line
- any emoji, tool name, or model name anywhere in the message

The only footers permitted are the ones these instructions define or the user asks for.
This applies to the changelog entry too: it describes the change, never who or what wrote it.

## Commit message format — Conventional Commits 1.0.0

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

- **type** is required: a lowercase noun followed by a colon and a space. `feat` MUST be used
  for a new feature, `fix` MUST be used for a bug fix. Other permitted types: `build`, `chore`,
  `ci`, `docs`, `style`, `refactor`, `perf`, `test`, `revert`.
- **scope** is optional: a noun naming a section of the codebase, in parentheses — `fix(parser):`.
- **description** follows immediately after the colon and space. Imperative mood, no trailing
  period. Keep the whole subject line under 72 characters.
- **body** is optional, begins one blank line after the description, and follows the house
  format in "Body format" below. Explain what changed and why, not how.
- **footers** are optional, begin one blank line after the body, and use the git trailer form
  `Token: value` or `Token #value`. The token uses `-` in place of spaces: `Refs: #123`.
- **Breaking changes** are marked with `!` before the colon, e.g. `feat(api)!:`, or with a
  `BREAKING CHANGE: <description>` footer, or both. `BREAKING CHANGE` MUST be uppercase;
  `BREAKING-CHANGE` is a synonym. With `!`, the footer may be omitted and the description
  then describes the break.
- If the change fits more than one type, split it into several commits rather than picking one.
- Reverts: `revert: <original subject>` with a footer `Refs: <sha>, <sha>`.

Examples:

```
feat(lang): add Polish language
docs: correct spelling of CHANGELOG
feat!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

## Body format

Write the body as a summary followed by a flat list:

1. **One or two sentences** giving the main idea behind the whole change — what it is for.
   Not a restatement of the subject line.
2. **A blank line, then a short bullet list** of what changed. Like a changelog entry but
   flatter: no group headings, fewer items, shorter lines.

```
Rework how both commit skills write messages and changelog entries

- Commit bodies now lead with a summary and a flat list of changes
- Date-based changelogs aggregate into today's section instead of Unreleased
```

Keep the list to changes that matter to someone reading the history later. **Leave trivial
work out** — typo fixes, formatting, comment rewording, dependency bumps — unless that is the
whole point of the commit, in which case it is the whole list. A commit that only fixes typos
says so; a commit that fixes a few typos while adding a feature mentions only the feature.

Three to six bullets is usually right. A longer list is a sign the commit is doing more than
one thing — go back to Step 1 and consider splitting it.

A one-line change with nothing to summarize needs no body at all. The subject line alone is a
complete commit message.

## Versioning scheme — detect, never assume

Only relevant when a version argument is given (see below); plain `/commit` never needs it.

Read the signals in this order and stop at the first that answers:

1. **The latest tag**, from the dynamic context above.
2. **The existing changelog release headers**, if there are no tags. A repo can date its
   changelog sections without ever tagging — that is a complete scheme on its own.
3. **Neither** — default to SemVer.

| Signal looks like | Scheme | Next version |
| --- | --- | --- |
| `v1.2.3`, `1.2.3` | SemVer | Bump per the version argument |
| `2026-08-23` | Date-based, dashed | Today as `YYYY-MM-DD` |
| `20260815` | Date-based, compact | Today as `YYYYMMDD` |
| nothing | SemVer | Bump from the manifest version, or `0.1.0` if there is none |

Under either date-based scheme the version *is* today's date, so `patch`, `minor`, and `major`
carry no meaning. Say so in the final report rather than silently ignoring the keyword, and
refuse if a version for today already exists — as a tag, or as a changelog section header in a
repo that has no tags.

Tags are written `v<version>` when the existing tags carry a `v` prefix, and bare otherwise.
Match what the repo already does; with no tags, use `v` for SemVer and no prefix for a date.

**Writing the version** depends on the manifest reported above:

| Manifest | How to set the version |
| --- | --- |
| `package.json` | `npm version <X.Y.Z> --no-git-tag-version` — rewrites `package.json` and `package-lock.json`, no commit, no tag. Stage both. A date version is not valid SemVer, so under a date-based scheme edit the field directly instead. |
| `Cargo.toml` | Edit the `version` field under `[package]`, or under `[workspace.package]` in a workspace — the dynamic context shows which lines exist. Refresh the lockfile with `cargo update --workspace --offline`. Stage `Cargo.toml` and `Cargo.lock`. |
| `pyproject.toml` | Edit `version` under `[project]`, or under `[tool.poetry]` in a Poetry project. If a `uv.lock` or `poetry.lock` records the project version, refresh it with the corresponding tool. Stage what changed. |
| none | Nothing to write — the tag, or the changelog header, is the only record of the version. |

## Changelog — Keep a Changelog 1.1.0

The file is `CHANGELOG.md` at the repo root. If it does not exist, create it:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
```

Under a date-based scheme, replace that Semantic Versioning line with "and this project uses
date-based version numbers in `YYYY-MM-DD` form." (or `YYYYMMDD`, matching the detected form).

### Where the entry goes

This depends on the detected scheme, and the two cases behave differently:

| Scheme | Section the entry goes in |
| --- | --- |
| SemVer | `## [Unreleased]` |
| Date-based | `## <today>` — never `[Unreleased]` |

**SemVer** — add the entry under `## [Unreleased]`. If there is no such section, because a
previous release cut consumed it or the file was edited by hand, add one above the newest
release section.

**Date-based** — a repo that dates its changelog sections is usually not tagging releases at
all, so there is nothing for an `[Unreleased]` section to be waiting for: the dated section
*is* the release. Therefore:

- If a section headed with today's date already exists, add the entry to it.
- If not, create `## <today>` at the top, above the previous dated section.
- Never add an `[Unreleased]` section to a date-based changelog, and never leave one behind.

Several commits on the same day accumulate into one dated section. That is the point — a
reader wants one list per day, not one per commit. When today's section already has an entry
in the group you need, add a bullet to it rather than starting a second copy of the group.

In both cases, put the entry in the correct group, creating the group heading if it is absent.
Groups appear in this order and only when non-empty:

| Group        | Use for                         |
| ------------ | -------------------------------- |
| `Added`      | new features                    |
| `Changed`    | changes in existing behaviour   |
| `Deprecated` | soon-to-be removed features     |
| `Removed`    | now removed features            |
| `Fixed`      | bug fixes                       |
| `Security`   | vulnerabilities                 |

Rules for entries:

- Changelogs are for humans, not machines. Describe the noteworthy difference a user would
  notice — never paste the commit subject or a diff summary verbatim.
- One bullet per notable change, sentence case, ending with a period.
- Never leave empty group headings behind.
- Always record deprecations, removals, and breaking changes, even small ones.
- Skip internal-only work: `chore`, `ci`, `style`, `test`, and most `refactor` commits get no
  entry unless behaviour changed. `docs` gets an entry only when user-facing docs changed.
  A `feat` or `fix` always gets one. A change to the changelog's own structure gets none —
  that is bookkeeping, not something a reader of the project would notice.
- Released section headers carry the version and, under SemVer only, the release date:

  | Scheme | Header |
  | --- | --- |
  | SemVer | `## [1.7.0] - 2026-08-23` |
  | Date-based, dashed | `## [2026-08-23]` |
  | Date-based, compact | `## [20260815]` |

  A date-based version already carries its own date, so no separate date is appended. Newest
  first. **Match the existing file** where it differs — notably the brackets, which some repos
  drop when they keep no reference-style compare links; use brackets only for a new file.
  A pulled release is marked `[YANKED]` after the header.
- Under SemVer, do not create a released section — this skill writes under `[Unreleased]`,
  **unless** this is a version commit (`as patch|minor|major|X.Y.Z` — see below), which folds
  the release cut into this same commit instead of leaving it as a separate task. Under a
  date-based scheme today's section is where entries go from the start, so there is no
  separate cut to make: `as ...` adds the version bump and the tag, and leaves the changelog
  section exactly where it already is.

## Version argument — `as patch|minor|major|X.Y.Z`

Plain `/commit` (no `as ...`) **never** touches the version, the manifest, or any tag — skip
this whole section entirely and follow Steps below unmodified. This only activates when
`$ARGUMENTS` starts with the literal word `as` (case-insensitive) followed by `patch`, `minor`,
`major`, or an exact `X.Y.Z`. Anything after that token is still free-text context — e.g.
`as minor closes #42` sets a minor version bump with `closes #42` as extra note text.

When detected, this commit also cuts the release locally: it still does everything in Steps
below (real Conventional Commit type and scope from the actual diff, changelog entry,
attribution check), plus:

1. **Resolve the target version** per "Versioning scheme" above. `as X.Y.Z` uses that exact
   version (a leading `v` is accepted and stripped). `as patch|minor|major` increments that
   segment of the current manifest version — or of the latest tag, if there is no manifest —
   and zeroes the segments below it: `minor` on `1.6.2` gives `1.7.0`, `major` gives `2.0.0`.
   This is a direct instruction from the user, not an inference from the commit's own type:
   `as patch` bumps patch even when the change here is a `feat`, and the reverse. Under a
   date-based scheme the argument is moot and today's date is used.
2. **Refuse early if that tag already exists** (`git rev-parse "<tag>"` resolves) — stop and
   tell the user instead of silently doing nothing or overwriting it. Do this *before* Step 1
   of Steps below, before staging or writing anything at all. Judge this on tags only: under a
   date-based scheme a changelog section headed with today's date is expected to be there
   already, and is not a collision.
3. **Set the version** with the command for this project's manifest, per the table above, and
   add every file it touched to what gets staged for this commit.
4. **Cut the changelog release section**, folded into the same edit as the normal changelog
   entry rather than a separate step: after writing this change's entry under `[Unreleased]`
   per the rules above, rename that header to the released form for the detected scheme and add
   a fresh empty `## [Unreleased]` above it.
5. **After the commit succeeds** (Step 4 below), tag it on the commit you just made. If there
   was no real code change to commit — the working tree was otherwise clean, so this was run
   purely to cut a release — the commit message in Step 4 is `chore(release): <tag>` instead of
   a type inferred from an empty diff.
6. **When reporting** (Step 6 below), include the tag name and the resolved version, and say
   the tag has not been pushed.

## Steps

1. Review the diff above. If it contains unrelated changes that would need different commit
   types, stop and propose splitting them into separate commits before continuing.
2. Stage the relevant files with `git add`. Never stage `.env`, secrets, or build artifacts.
3. Decide type, scope, and whether the change is breaking. Update `CHANGELOG.md` per the rules
   above (including the release-cut variant if a version argument is present), then stage it too.
4. Commit with a heredoc so the body and footers keep their newlines:

```bash
   git commit -m "$(cat <<'EOF'
   feat(auth): refresh access token before expiry

   Tokens were refreshed only after a 401, which dropped in-flight requests.

   Refs: #123
   EOF
   )"
```
5. Run `git log -1 --pretty=%B` and read the result. If any attribution trailer or generated-by
   line appears, remove it with `git commit --amend`.
6. If a version argument was given, tag the commit now: `git tag "<tag>"`.
7. Report the commit hash, the subject line, the changelog line you added, and (if applicable)
   the resolved version and the tag that was created. State how many commits the branch is now
   ahead of its upstream (`git rev-list --count @{upstream}..HEAD`, or that there is no
   upstream), and remind the user that nothing was pushed.

**Do not push.** No `git push` for the commit, and none for the tag. Never use `--force` or
`--no-verify`. Extra context from the user: $ARGUMENTS
