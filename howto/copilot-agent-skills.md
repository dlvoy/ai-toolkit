# GitHub Copilot agent skills (VS Code)

**Agent Skills** are folders holding instructions, scripts, and resources that Copilot
loads when they are relevant, or that you invoke as a slash command. The format is an open
standard shared across Copilot in VS Code, the Copilot CLI, the Copilot cloud agent, and
Claude Code — the same `SKILL.md` works in all of them.[^1]

## Where skills live

Six discovery paths, three of each kind:[^1]

| Scope | Paths |
| --- | --- |
| Project | `.github/skills/`, `.claude/skills/`, `.agents/skills/` |
| Personal | `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/` |

Because `.claude/skills/` and `~/.claude/skills/` are on that list, a skill installed for
Claude Code is already visible to Copilot. One install, both tools.

## Option A — the built-in Skills UI

1. Open the Command Palette and run **Chat: Open Customizations**.
2. Go to the **Skills** tab.
3. Choose **New Skill (Workspace)** or **New Skill (User)**.
4. Give the skill a name.
5. VS Code creates a `SKILL.md` with YAML frontmatter and a body. Fill in `name`,
   `description`, and the instructions.
6. Save. The skill is now available in chat — type `/` to see the list.[^1]

## Option B — copy an existing skill

Skills are just folders, so installing someone else's is a copy:

```bash
git clone <skills-repo-url> temp-skills
# then copy the skill folder into one of the paths above, e.g.
cp -r temp-skills/skills/commit .github/skills/
```

Reload VS Code so Copilot picks them up, and read the `SKILL.md` before trusting it — a
skill is instructions an agent will follow.

There are also third-party marketplace extensions that bulk-install skills from a GitHub
repo, such as **Copilot Skills Manager**.[^2] Unverified; the manual copy above does the
same thing with nothing extra installed.

## `SKILL.md` frontmatter

| Field | Purpose |
| --- | --- |
| `name` | Unique id. Lowercase letters, numbers, and hyphens only. **Required.** |
| `description` | What the skill does **and when to use it** — this is what the model matches on. **Required.** |
| `argument-hint` | Hint text shown when invoked as a slash command |
| `user-invocable` | Whether it appears in the `/` menu (default `true`) |
| `disable-model-invocation` | Prevent automatic loading; manual invocation only (default `false`) |
| `context` | Set to `fork` to run in a dedicated subagent context |

Set `disable-model-invocation: true` for anything with side effects you do not want
triggered by relevance — the skills in this repo use it so a commit never happens
because the model thought it was a good idea.[^1]

## See also

- [`skills/`](../skills/) in this repo — two skills using exactly this format.
- [Copilot custom instructions](copilot-custom-instructions.md) — for always-on rules
  rather than invocable workflows.

[^1]: https://code.visualstudio.com/docs/agent-customization/agent-skills

[^2]: https://marketplace.visualstudio.com/items?itemName=DarshanMoradiya.copilot-skills
