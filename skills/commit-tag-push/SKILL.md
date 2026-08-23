---
description: Commit using Conventional Commits, bump the project version (explicit X.Y.Z, a patch|minor|major keyword, or auto-detected from commit types), cut a Keep a Changelog release, tag it, then push every pending commit and the tag. Use only when explicitly invoked.
disable-model-invocation: true
argument-hint: <X.Y.Z|patch|minor|major> [ticket id or note]
allowed-tools: Bash(git add *) Bash(git status *) Bash(git diff *) Bash(git commit *) Bash(git push *) Bash(git branch *) Bash(git rev-parse *) Bash(git rev-list *) Bash(git log *) Bash(git tag *) Bash(git describe *) Bash(git remote *) Bash(npm version *) Bash(node -p *) Bash(cargo update *) Bash(git ls-files *) AskUserQuestion Read Edit Write
---

## Current state

Branch: !`git branch --show-current`

Repo state:

```!
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "GIT UNUSABLE HERE - not a repository, or git refused it. Stop and report the error."
elif git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "HEAD exists - ordinary commit"
else
  echo "NO COMMITS YET - this run writes the INITIAL COMMIT (see the section below)"
fi
```

```!
git status --short
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  git diff HEAD --stat
fi
```

Today: !`date +%Y-%m-%d` (compact: !`date +%Y%m%d`)

Latest tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "none yet"`

Unpushed commits already on this branch:

```!
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "no commits yet - nothing has ever been pushed"
elif git rev-parse --abbrev-ref '@{upstream}' >/dev/null 2>&1; then
  git log --oneline '@{upstream}..HEAD' | grep . || echo "none - branch is level with upstream"
else
  echo "no upstream configured for this branch"
fi
```

Remotes:

```!
git remote -v | grep . || echo "NO REMOTE CONFIGURED - this skill cannot push"
```

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

Commits since latest tag (oldest first):

```!
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "no commits yet - the commit written here is the repo's first"
else
  TAG=$(git describe --tags --abbrev=0 2>/dev/null)
  if [ -n "$TAG" ]; then git log --reverse --pretty='%s' "$TAG"..HEAD; else git log --reverse --pretty='%s'; fi
fi
```

Diff:

```!
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  git diff HEAD
else
  echo "No commits yet, so there is nothing to diff against."
  echo "Files that would go into the initial commit:"
  git ls-files --others --exclude-standard
fi
```

Top of changelog:

!`head -40 CHANGELOG.md 2>/dev/null || echo "NO CHANGELOG.md AT REPO ROOT"`

Existing changelog release headers (the versioning scheme this repo actually uses):

```!
grep -m5 -E '^## ' CHANGELOG.md 2>/dev/null | grep -viE 'unreleased' || echo "none yet"
```

## What this skill ships

The release verb. It writes one more commit, cuts the release, tags it, and then pushes —
**both the commits and the tag**. The push carries every unpushed commit on the branch, not
just the one written here: `/commit` deliberately never pushes, so a run of local commits can
have accumulated behind this one. They all go out together.

## Initial commit — the repo has no commits yet

The "Repo state" block above says whether `HEAD` exists. When it does not, this run writes the
repo's first commit *and* its first release, and several assumptions here do not hold:

- **Never run anything against `HEAD`.** `git diff HEAD`, `git log`, `git describe` and
  `git rev-list @{upstream}..HEAD` all fail on an unborn branch. The context above already
  substituted a file listing for the diff; read the files themselves to decide type and scope.
- **Check the remote before anything else.** This skill exists to push, and a fresh repo often
  has no remote at all — the "Remotes" block above says. With no remote, stop before staging or
  writing a thing: tell the user to add one (`git remote add origin <url>`), or to use `/commit`
  if they only want the local commit and tag. Do not commit first and discover the problem at
  the push step.
- **Type.** A first commit that imports a working project is a `feat:` naming what the project
  is. One that lays down scaffolding only — README, licence, config — is `chore: initial commit`.
  There is no diff to infer a scope from; leave the scope off unless the tree is one component.
- **Staging.** `git add` works normally, but nothing has ever been ignored in this repo before,
  so look at what you are about to stage. If there is no `.gitignore` and the tree contains
  `node_modules/`, `target/`, `dist/`, `.venv/`, `__pycache__/`, `.env` or similar, stop and say
  so before staging anything — offer to write a `.gitignore` first.
- **The branch has no upstream**, so the push in Step 10 is `git push -u origin <branch>`.
- **No version signals.** There are no tags and usually no changelog, so the scheme has to be
  asked for — see "No signal at all" below.
- **Bump keywords and auto-detection are meaningless for a first release.** There is no previous
  version to increment and no commit history to read. Under SemVer the first release is the
  manifest version if the manifest already carries one, otherwise `0.1.0`; under a date-based
  scheme it is today's date. An explicit `X.Y.Z` still applies exactly as given. Say in the
  report that the directive was ignored.

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

Read the signals in this order and stop at the first that answers:

1. **The latest tag**, from the dynamic context above.
2. **The existing changelog release headers**, if there are no tags. A repo can date its
   changelog sections without ever tagging — that is a complete scheme on its own.
3. **The version field in the project manifest**, if there is neither. A `version = "1.4.0"` is
   a SemVer repo whatever else is missing.
4. **Nothing at all** — ask the user. Never default silently.

| Signal looks like | Scheme |
| --- | --- |
| `v1.2.3`, `1.2.3` | [SemVer](https://semver.org/) |
| `2026-08-23` | Date-based, dashed `YYYY-MM-DD` |
| `20260815` | Date-based, compact `YYYYMMDD` |
| manifest `version` only | [SemVer](https://semver.org/) |
| nothing | **ask — see below** |

### No signal at all — ask, don't assume

No tag, no `CHANGELOG.md`, and no `version` field in a manifest — the usual state of a fresh repo
on its initial commit — means the project has not chosen a scheme yet, and neither should you.
This skill always tags, so it always needs the answer. Ask with `AskUserQuestion`, **once, both
questions in a single call**, before staging or writing anything:

| Header | Question | Options |
| --- | --- | --- |
| `Changelog` | No CHANGELOG.md found. Create one? | *Yes, create it (Recommended)* — start a Keep a Changelog file · *No, skip it* — release with no changelog |
| `Versioning` | Which versioning scheme should this repo use? | *SemVer — vX.Y.Z (Recommended)* · *Date-based — YYYY-MM-DD* · *Date-based — YYYYMMDD* |

- Ask only when **every** signal above is absent. A signal that answers is the repo telling you
  what it already does — do not ask the user to confirm it.
- **If the changelog is declined**, skip every changelog step for this run, do not ask again for
  the rest of the session, and say in the final report that no changelog was written. The tag
  still records the scheme, so later runs will not need to ask.
- The scheme answer decides the first version too: `0.1.0` — or the manifest's version, if it
  carries one — under SemVer, today's date under either date-based form.

Under either date-based scheme the whole "Version argument" section below collapses to one
rule: the target version is today's date in the detected form. An explicit `X.Y.Z`, a bump
keyword, and auto-detection all become meaningless — if the user passed one, say so in the
final report rather than silently ignoring it. The collision refusal below still applies, and
is what stops a second release on the same day.

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

`CHANGELOG.md` is at the repo root. If it is missing and the repo has no other version signal,
ask first per "No signal at all" above and create it only on a yes; if it is missing but the repo
does carry a signal — a tag, or a manifest version — create it without asking. Format:

```markdown
## [Unreleased]

## [1.6.2] - 2026-06-19

### Fixed

- ...

[Unreleased]: https://github.com/<owner>/<repo>/compare/v1.6.2...HEAD
[1.6.2]: https://github.com/<owner>/<repo>/compare/v1.6.1...v1.6.2
```

Release headers carry the version and, under SemVer only, the release date:

| Scheme | Header |
| --- | --- |
| SemVer | `## [1.7.0] - 2026-08-23` |
| Date-based, dashed | `## [2026-08-23]` |
| Date-based, compact | `## [20260815]` |

A date-based version already carries its own date, so no separate date is appended. **Match the
existing file** where it differs — notably the brackets, which some repos drop when they keep no
reference-style compare links; use brackets only for a new file.

Groups appear in this order and only when non-empty:

| Group        | Use for                       |
| ------------ | ------------------------------ |
| `Added`      | new features                   |
| `Changed`    | changes in existing behaviour  |
| `Deprecated` | soon-to-be removed features    |
| `Removed`    | now removed features           |
| `Fixed`      | bug fixes                      |
| `Security`   | vulnerabilities                |

Rules for entries:

- Changelogs are for humans, not machines. Describe the noteworthy difference a user would
  notice — never paste the commit subject or a diff summary verbatim.
- One bullet per notable change, sentence case, ending with a period.
- Never leave empty group headings behind.
- Always record deprecations, removals, and breaking changes, even small ones.
- Skip internal-only work: `chore`, `ci`, `style`, `test`, and most `refactor` commits get no
  entry unless behaviour changed. `docs` gets an entry only when user-facing docs changed.
  A `feat` or `fix` always gets one.

**This skill always cuts a release.** How it does that depends on the scheme:

**SemVer** — add this change's own entry to `[Unreleased]`, then fold the *entire*
`[Unreleased]` section — including any entries left there by earlier plain `/commit` runs, not
just this one — into a new release header, leaving a fresh empty `## [Unreleased]` above it.
If there is no `[Unreleased]` section at all, add this change's entry directly under a new
release header.

**Date-based** — there is nothing to fold. Entries already live in a section headed by today's
date, because `/commit` puts them there instead of in `[Unreleased]`. Add this change's entry
to that section — creating `## <today>` at the top if this is the day's first commit — and that
section *is* the release. Do not create an `[Unreleased]` section, before or after. Earlier
entries from today's `/commit` runs are already in place and ship as part of this release.

In both cases, if the reference-style compare links block exists at the bottom of the file
(see format above), update it too: repoint the `[Unreleased]:` link at the new tag, and insert
a new `[<version>]:` link comparing it against the previous tag. Read the repo URL from
`git remote get-url origin` (strip a trailing `.git`) rather than assuming one; if there is no
remote, skip the links block.

## Version argument

Under a date-based scheme, skip this section — the target version is today's date. On an initial
commit, skip it too except for an explicit `X.Y.Z` — see "Initial commit" above for what the
first version is.

`$ARGUMENTS`' first whitespace-separated token is the version directive; everything after it is
free-text context (a ticket id or note), same as plain `/commit`. Resolve the target version
**before** touching anything else, in this order:

1. **Exact version** — the token matches `X.Y.Z` (three non-negative integers, no pre-release
   or build metadata; a leading `v`/`V` is accepted and stripped). Use it exactly — this is a
   direct instruction from the user, not inferred from commit types.
2. **Bump keyword** — the token is `patch`, `minor`, or `major` (case-insensitive). Compute the
   target by incrementing that segment of the *current* version from the manifest — or of the
   latest tag, if there is no manifest — and zeroing the segments below it (`minor` on `1.6.2`
   gives `1.7.0`; `major` on `1.6.2` gives `2.0.0`).
3. **Auto-detect** — the token is absent, or present but matches neither of the above (in which
   case treat the *whole* of `$ARGUMENTS` as free-text context, not a version directive). Decide
   the bump from the Conventional Commit types of every commit since the latest tag (the dynamic
   context block above) **plus** the type you determine for the new commit itself in Step 2
   below:
   - Any of them is `feat` → **minor**.
   - Otherwise (only `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`,
     `revert`, ...) → **patch**.
   - **Never auto-select major**, even if a commit carries a `!` breaking marker or a
     `BREAKING CHANGE:`/`BREAKING-CHANGE:` footer. If you see one, still cap the bump at minor,
     but say so plainly in the final report and suggest the user re-run with an explicit
     `major` argument if that's what they actually want.
   - No commits since the last tag and the new commit is the only change: base the decision on
     that one commit's type using the same rule.
   - No commits at all (initial commit): there is nothing to detect. The first release is
     `0.1.0`, or the manifest's version if it already carries one.

**Refuse early if the resulting tag already exists** (`git rev-parse "<tag>"` resolves) — stop
and tell the user instead of silently doing nothing or overwriting it. Judge this on tags only:
under a date-based scheme a changelog section headed with today's date is expected to be there
already, put there by the day's `/commit` runs, and is not a collision. Do this before
staging or writing anything at all, which means: for bump-keyword and auto-detect modes, you
must compute the concrete `X.Y.Z` (step 2's arithmetic, or step 3's arithmetic after deciding
the bump size) before this check, not defer it to when the version is written.

## Steps

1. Review the diff above. If it contains unrelated changes that would need different commit
   types, stop and propose splitting them into separate commits before continuing. On an initial
   commit there is no diff — read the listed files instead, and split nothing: the first commit
   is allowed to contain everything.
2. Decide the commit's type, scope, and whether it's breaking, from the diff. In auto-detect
   mode this type feeds into the version resolution above.
3. Resolve the target version per "Versioning scheme" and "Version argument" above, including
   the early collision refusal and — if the repo has no version signal at all — the questions in
   "No signal at all", before staging or writing anything. Confirm there is a remote to
   push to while you are still at this point — with none, stop here rather than after committing.
4. Stage the relevant files with `git add`. Never stage `.env`, secrets, or build artifacts. On
   an initial commit, check the tree against the ignore rules first — see "Initial commit" above.
5. Write the version using the command for this project's manifest, per the table above, and
   stage every file it touched. Skip this step entirely when there is no manifest.
6. Update `CHANGELOG.md` per the rules above: add this change's entry under `[Unreleased]`, then
   cut the release (fold `[Unreleased]` into the release header, add a fresh empty `[Unreleased]`
   above it, update the compare-links block if present). Stage it too. Skip this step entirely if
   the user declined a changelog in Step 3.
7. Commit with a heredoc so the body and footers keep their newlines:

```bash
   git commit -m "$(cat <<'EOF'
   feat(auth): refresh access token before expiry

   Tokens were refreshed only after a 401, which dropped in-flight requests.

   Refs: #123
   EOF
   )"
```

   If there is no real code change beyond the version bump (working tree was otherwise clean —
   this was run purely to cut a release), use `chore(release): <tag>` as the message instead of
   inferring a type from an empty diff.
8. Run `git log -1 --pretty=%B` and read the result. If any attribution trailer or generated-by
   line appears, remove it with `git commit --amend` before continuing.
9. Tag the commit: `git tag "<tag>"`.
10. Push the commits: `git push`, or `git push -u origin <branch>` if the branch has no
    upstream — which is always the case on an initial commit. This carries every unpushed commit
    on the branch, including any left behind by earlier `/commit` runs — the dynamic context
    above listed them.
11. Push the tag: `git push origin "<tag>"`. Do this as its own command rather than relying on
    `--follow-tags`, so a failure here is visible instead of silent.
12. Report: the commit hash, the subject line, the changelog changes (entry added and the
    release section cut), the resolved version and how it was resolved (explicit / bump keyword
    / auto-detected — and from which commit types, if auto-detected / date-based), the tag that
    was pushed, and **how many commits went out in total**, naming any that were written by
    earlier `/commit` runs. If a breaking-change marker was seen but capped at minor per the
    rule above, say so here. Say so too if a changelog was skipped because the user declined one,
    or if a version directive was ignored because this was the repo's first release.

Never use `--force` or `--no-verify`. Extra context from the user: $ARGUMENTS
