# Skills

Agent Skills for git hygiene: Conventional Commits in, Keep a Changelog out, no AI
attribution anywhere in the history.

| Skill | Use it when |
| --- | --- |
| [`commit`](commit/) | Everyday commits. Writes the commit and a `[Unreleased]` changelog entry. Cuts a release too, if you ask with `as patch\|minor\|major\|X.Y.Z`. **Never pushes.** |
| [`commit-tag-push`](commit-tag-push/) | You are shipping. Always bumps the version, folds `[Unreleased]` into a release section, tags, and pushes the tag along with every commit waiting on the branch — and can work out the bump size from the commit types since the last tag. |

The split is about the remote, not the release. `commit` stays local however you invoke it,
so you can stack up work and review it before any of it leaves the machine.
`commit-tag-push` is the one verb that touches `origin`.

```
/commit            /commit            /commit-tag-push minor
   |                  |                       |
   +-- local ---------+-- local --------------+--> origin: 3 commits + tag
```

To push commits made by `commit` without cutting another release, do it yourself with
`git push --follow-tags`.

## Prerequisites

- **A git repo with a remote**, for `commit-tag-push`. `commit` works fine without one. The
  compare links come from `git remote get-url origin`; without a remote that step is skipped.
- **`CHANGELOG.md` at the repo root.** Created for you if missing — though in a repo with no
  version signal at all, you are asked first rather than having one appear uninvited.
- **Conventional Commits already in use**, ideally. `commit-tag-push`'s auto-detection reads
  the types of commits since the last tag; unparseable history falls back to a patch bump.
- **A version manifest, or none.** Cargo, npm, and pyproject are detected and written to;
  a repo with no manifest works fine — the tag, or the changelog header, becomes the only
  record of the version.
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

Then invoke as `/commit` or `/commit-tag-push`. Both set
`disable-model-invocation: true`, so they never fire on their own — a commit only ever
happens because you asked for one.

The `README.md` in each skill folder is documentation for this repo, not part of the
skill. Copying it along is harmless.

## Elsewhere

Skills I rely on but do not host here — install them from the source.

### [`unslop`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md)

Strips the tells that make agent output read as machine-written. Thirty-one categories of
them: puffery, "delve" and "landscape" vocabulary, fancy synonyms for "is", forced
rule-of-three lists, em dash and colon overuse, title case headings, decorative emoji,
chatbot sign-offs, hedging, sycophancy, abstract metaphors like "substrate" and "paradigm".
The second half is the harder part — vary the sentence rhythm, use specifics, have an
opinion.

Worth having on any agent that writes prose you will show to someone else. Its description
is `Cut AI tells from any writing. Must always apply.`, so unlike the two skills here it is
meant to load on relevance and stay loaded, not wait for a slash command.

It ships as part of [`cursor/plugins`](https://github.com/cursor/plugins); copy the
`pstack/skills/unslop/` folder into any of the skill paths listed above.

## Design notes

**Versioning is detected, not assumed.** The scheme comes from the shape of the latest tag —
`v1.2.3` for SemVer, `2026-08-23` or `20260815` for date-based. With no tags it falls back to
the shape of the existing changelog release headers, so a repo that dates its changelog and
never tags still works; with neither, to the manifest's `version` field. The project type comes
from which manifest exists. Earlier versions of these skills hard-coded one project and one
scheme each, which made them useless outside the repo they came from.

**With no signal at all, they ask.** A repo with no tag, no changelog, and no manifest version
has not chosen a scheme, and guessing one on its behalf is how a project ends up with a
convention nobody picked. Both skills stop and ask two questions in a single prompt — create a
`CHANGELOG.md`? and SemVer `vX.Y.Z`, `YYYY-MM-DD`, or `YYYYMMDD`? — before staging or writing
anything. The answer is self-recording: it lands in the changelog preamble and the tag, which
are the same signals the detection above reads, so the question is asked once per repo.

**They work on an empty repo.** An unborn branch has no `HEAD`, which makes `git diff HEAD`,
`git log`, and `git describe` all fail, so every context block is guarded and the diff is
replaced by a listing of the files that would go into the first commit. `commit-tag-push` also
checks for a remote up front, since a fresh repo often has none and discovering that after the
commit and tag are already written is the worst time to find out.

**Only one of them can reach the remote.** `commit` has no `Bash(git push *)` in its
`allowed-tools` at all, so the restriction is enforced by the harness rather than by the
model remembering a rule. Pushing is a decision worth making on purpose.

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
