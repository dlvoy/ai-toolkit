# Claude Code output styles

An output style is markdown that Claude Code appends to its **system prompt**. It changes
how Claude responds — role, tone, default format — not what it knows about your codebase.
Reach for one when you find yourself re-prompting for the same voice every turn.

It is the persistent alternative to the per-invocation flags:

| Approach | Scope |
| --- | --- |
| `claude --append-system-prompt "<text>"` | One invocation. Also `--append-system-prompt-file`, `--system-prompt`, `--system-prompt-file`. |
| Output style | Every session, until you switch it |
| `CLAUDE.md` | Every session, but added as a user message after the system prompt |

## Selecting a style

Run `/config` and pick one under **Output style**. The choice is saved to
`.claude/settings.local.json` in the current project.[^1]

> **The `/output-style` command is gone.** It was deprecated in v2.1.73 and removed in
> v2.1.91. Older notes and blog posts still tell you to run `/output-style` or
> `/output-style:new` — they do nothing now.[^1]

To set it without the menu — or in the desktop app, where `/config` opens the settings
pane instead of a picker — write the field directly into any settings file:

```json
{
  "outputStyle": "Explanatory"
}
```

Output style is part of the system prompt, which is read once at session start. **Changes
take effect after `/clear` or in a new session**, not immediately.[^1]

## Built-in styles

| Style | Behaviour |
| --- | --- |
| **Default** | The standard software-engineering system prompt. |
| **Proactive** | Executes immediately, assumes rather than pausing on routine decisions, prefers action over planning. Independent of permission mode. |
| **Concise** | Leads with the result, skips preamble, keeps answers short — while doing the same depth of work. Requires v2.1.237+. |
| **Explanatory** | Adds educational "Insights" about implementation choices and codebase patterns. |
| **Learning** | Like Explanatory, plus it leaves `TODO(human)` markers for you to implement. |

## Writing your own

A custom style is a markdown file with YAML frontmatter. The filename becomes the style
name unless you set `name`. Save it at one of:

- **User** (all projects): `~/.claude/output-styles/`
- **Project**: `.claude/output-styles/`

```markdown
---
name: Diagrams first
description: Lead every explanation with a diagram
keep-coding-instructions: true
---

When explaining code, architecture, or data flow, start with a Mermaid diagram showing
the structure, then explain in prose.
```

### Frontmatter

| Field | Purpose | Default |
| --- | --- | --- |
| `name` | Style name | The filename |
| `description` | Shown in the `/config` picker | None |
| `keep-coding-instructions` | Keep Claude Code's built-in software-engineering instructions | `false` |
| `force-for-plugin` | Plugin styles only: apply automatically whenever the plugin is enabled | `false` |

> **Watch `keep-coding-instructions`.** It defaults to `false`, which means a custom style
> *replaces* Claude Code's built-in instructions on scoping changes, writing comments, and
> verifying work. That is right for a writing assistant or data analyst. It is wrong for a
> style that only changes how Claude talks while it keeps on coding — set it `true` there.[^1]

Project styles load from every `.claude/output-styles/` between the working directory and
the repo root; the one closest to the working directory wins on a name collision.[^1]

## Scope

Output styles apply to the **main conversation only**. A subagent runs its own system
prompt and is unaffected. A fork is the exception — it inherits the parent's full system
prompt.[^1]

[^1]: https://code.claude.com/docs/en/output-styles
