# GitHub Copilot custom instructions (VS Code)

Copilot does not expose a raw "system prompt" field, but **custom instructions** do the
same job: persistent rules that apply to your chats and code generation.

## A. Repository / workspace instructions

The always-on file is `.github/copilot-instructions.md` in the root of your repo — create
`.github` if it does not exist.[^1][^2]

```md
# Copilot custom instructions

## Output style
- Always answer in English.
- Use concise, bullet-point lists for steps.
- For code, prefer:
  - TypeScript over JavaScript when possible.
  - Functional style, no classes unless necessary.
  - Explicit types, no `any`.
- Explain non-trivial code in 1-3 short sentences before the snippet.
- Do not include long preambles like "Sure, here is..."; go straight to the answer.
```

VS Code also reads, from the workspace root, `AGENTS.md` and `CLAUDE.md` (the latter from
the root or `.claude/`). If you already keep one of those for another agent, Copilot picks
it up — no duplication needed.[^1]

### Scoping rules to specific files

Instead of one big file, put `*.instructions.md` files under `.github/instructions/` (for
example `frontend.instructions.md`, `backend.instructions.md`) and give each an `applyTo`
glob in frontmatter:[^1]

```md
---
applyTo: "src/**/*.tsx"
---

- Use function components and hooks, never class components.
```

Without `applyTo`, an instructions file is not applied automatically.[^1]

### Settings

Relevant setting ids:[^1]

| Setting | Purpose |
| --- | --- |
| `chat.includeApplyingInstructions` | Enable pattern-based (`applyTo`) instructions |
| `chat.instructionsFilesLocations` | Extra folders to look for instructions files in |
| `chat.useAgentsMdFile` | Read `AGENTS.md` |
| `chat.useNestedAgentsMdFiles` | Read nested `AGENTS.md` files |
| `chat.useClaudeMdFile` | Read `CLAUDE.md` |

Older guides tell you to enable
`github.copilot.chat.codeGeneration.useInstructionFiles`.[^3] That setting predates the
current layout; check the settings above first if instructions are not being applied.

## B. User-level instructions (all projects)

Personal instructions live in `~/.copilot/instructions/` (VS Code also reads
`~/.claude/rules/`).[^1] To create one from the UI, run **Chat: New Instructions File**
from the Command Palette and choose the user-level location. **Chat: Open Customizations**
opens the Agent Customizations editor, where instructions, skills, and prompts are managed
together.[^1]

Repository instructions override user-level ones.

From chat you can also run:[^1]

- `/instructions` — opens the Configure Instructions menu.
- `/init` — generates workspace-wide instructions for the current repo.
- `/create-instruction` — generates a targeted instructions file from a description.

## Example: strict output-style instructions

```md
# Output style for Copilot

- Language: English only.
- Structure:
  - Start with a 1-2 sentence direct answer.
  - Then use sections with `##` headers if the answer is long.
  - Use bullet lists for steps/options.
- Code:
  - Show minimal, focused snippets.
  - Prefer modern syntax and explicit types.
  - Add brief comments only where logic is non-obvious.
- Tone:
  - Technical, concise, no filler phrases.
  - No "Sure", "Certainly", or long intros.
- When unsure:
  - State assumptions explicitly.
  - Ask at most one clarifying question at the end.
```

This effectively becomes your system prompt for style.[^2][^4]

## See also

- [Copilot agent skills](copilot-agent-skills.md) — for reusable *workflows* rather than
  always-on rules.
- [Claude Code output styles](claude-output-styles.md) — the equivalent mechanism on the
  Claude side.

[^1]: https://code.visualstudio.com/docs/copilot/customization/custom-instructions

[^2]: https://docs.github.com/en/copilot/concepts/prompting/response-customization

[^3]: https://github.blog/changelog/2025-03-06-github-copilot-updates-in-visual-studio-code-february-release-v0-25-including-improvements-to-agent-mode-and-next-exit-suggestions-ga-of-custom-instructions-and-more/

[^4]: https://docs.github.com/en/copilot/reference/custom-instructions-support
