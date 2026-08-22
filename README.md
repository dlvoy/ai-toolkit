# ai-toolkit

My personal toolkit for agentic AI: skills, output styles, and how-to notes for
[Claude Code](https://code.claude.com/docs/) and
[GitHub Copilot](https://code.visualstudio.com/docs/copilot/overview) in VS Code.

## Status: personal, shared as-is

This is a place for me to keep and reinstall my own tools, published because sharing a
link is easier than sharing a zip. You are welcome to it, with the obvious caveats:

- **Not maintained.** Things get updated when I need them updated, and not otherwise.
- **No support, no guarantees.** Issues and pull requests are not being watched.
- **Expect to customize.** These encode my conventions and my projects. Fork it, cut what
  you do not want, and change the rest.

Everything here is MIT licensed — see [LICENSE](LICENSE) — but read
[Attribution](#attribution) below, because parts are derived from other people's work.

## What's here

### [`skills/`](skills/) — Agent Skills

| Skill | What it does |
| --- | --- |
| [`commit`](skills/commit/) | Conventional Commit + Keep a Changelog entry + push. Optionally cuts a release with `as patch\|minor\|major\|X.Y.Z`. |
| [`commit-and-tag`](skills/commit-and-tag/) | Same, but always cuts a release: bumps the version, folds `[Unreleased]` into a release section, tags, pushes. |

Both detect the project type (Cargo / npm / pyproject / none) and the versioning scheme
(SemVer or date-based) instead of assuming one, and both refuse to put AI attribution in
your commit messages.

### [`output-styles/`](output-styles/) — Claude Code output styles

| Style | What it does |
| --- | --- |
| [`clear-concise-actionable`](output-styles/clear-concise-actionable/) | Lead with the answer, short codes for lists of findings/options/risks, no flattery or filler. |

### [`howto/`](howto/) — notes

| Note | About |
| --- | --- |
| [Claude Code output styles](howto/claude-output-styles.md) | Selecting, writing, and installing output styles. |
| [Disabling Claude attribution](howto/claude-disabling-attribution.md) | Keeping `Co-Authored-By` and session URLs out of your git history. |
| [Copilot custom instructions](howto/copilot-custom-instructions.md) | The closest thing Copilot has to a system prompt. |
| [Copilot agent skills](howto/copilot-agent-skills.md) | Installing and writing skills for Copilot in VS Code. |

## Installing

**Skills** — copy the skill folder into one of the discovery paths. The Agent Skills
format is shared between tools, so the same `SKILL.md` works in both:

```bash
# Just you, every project
cp -r skills/commit ~/.claude/skills/        # Claude Code
cp -r skills/commit ~/.copilot/skills/       # Copilot in VS Code

# This project, committed to the repo
cp -r skills/commit .claude/skills/          # Claude Code
cp -r skills/commit .github/skills/          # Copilot in VS Code
```

Copilot also reads `.claude/skills/` and `.agents/skills/` (project) and
`~/.claude/skills/`, `~/.agents/skills/` (personal) — see
[the Copilot note](howto/copilot-agent-skills.md) — so a single install often covers both.

**Output styles** — copy the `.md` file (not the folder) into `~/.claude/output-styles/`
for every project, or `.claude/output-styles/` for one project, then pick it in `/config`
under **Output style**:

```bash
cp output-styles/clear-concise-actionable/clear-concise-actionable.md ~/.claude/output-styles/
```

Skills and output styles both take effect in a new session, or after `/clear`.

## Attribution

Attribution lives in the `README.md` next to each item rather than inside the artifact
itself, so installed files stay clean:

- [`output-styles/clear-concise-actionable/`](output-styles/clear-concise-actionable/README.md)
  — reconstructed from a video by IndyDevDan; full provenance and confidence notes there.
- [`howto/`](howto/README.md) — two notes started as Perplexity output; all four were
  fact-checked against official documentation.
- [`skills/`](skills/README.md) — mine, implementing the Conventional Commits, Keep a
  Changelog, and SemVer specifications.
