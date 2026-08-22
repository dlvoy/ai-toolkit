# Output styles

Claude Code output styles — markdown appended to the system prompt that changes how Claude
responds, not what it knows.

| Style | What it does |
| --- | --- |
| [clear-concise-actionable](clear-concise-actionable/) | Lead with the answer, short reference codes for lists, no flattery or filler. Reconstructed from an IndyDevDan video — see its README for provenance. |

## Installing

Copy the `.md` file — not the folder — into an output styles directory:

```bash
cp <style>/<style>.md ~/.claude/output-styles/      # all projects
cp <style>/<style>.md .claude/output-styles/        # this project
```

Then run `/config`, pick it under **Output style**, and start a new session or `/clear`.

The `README.md` in each folder is documentation for this repo and is not part of the
style. Do not copy it.

See [the output styles note](../howto/claude-output-styles.md) for frontmatter fields, the
built-in styles, and how output styles compare to `CLAUDE.md` and `--append-system-prompt`.
