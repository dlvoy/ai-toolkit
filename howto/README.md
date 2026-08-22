# How-to notes

Working notes on configuring agentic AI. Short, opinionated, written for me.

| Note | About |
| --- | --- |
| [claude-output-styles.md](claude-output-styles.md) | Selecting a built-in output style, writing your own, and the `keep-coding-instructions` trap. |
| [claude-disabling-attribution.md](claude-disabling-attribution.md) | The `attribution` setting: keeping `Co-Authored-By` trailers and session URLs out of your commits. |
| [copilot-custom-instructions.md](copilot-custom-instructions.md) | Copilot's stand-in for a system prompt: `copilot-instructions.md`, `applyTo` scoping, user-level rules. |
| [copilot-agent-skills.md](copilot-agent-skills.md) | Where Copilot looks for skills, how to install one, and the `SKILL.md` frontmatter. |

## Attribution and provenance

- **copilot-custom-instructions.md** and **copilot-agent-skills.md** started as a single
  [Perplexity](https://www.perplexity.ai/) answer, which I split by hand. Each file kept
  the full shared reference list, so citations no longer matched the text; the footnotes
  have been trimmed to the sources each file actually cites.
- **claude-output-styles.md** and **claude-disabling-attribution.md** started as personal
  scratch notes — a few lines each, partly in Polish, partly hearsay — and were rewritten.

All four were checked against official documentation on **2026-08-22**, against Claude
Code v2.1.240. Corrections applied in that pass:

- `/output-style` and `/output-style:new` no longer exist (deprecated v2.1.73, removed
  v2.1.91). The original note recommended them.
- `includeCoAuthoredBy` is deprecated in favour of the `attribution` object, which the
  original note guessed at without confirming, and which also has a `sessionUrl` key the
  note missed.
- Copilot discovers skills in six paths, not the two the original listed.
- Copilot's instructions UI moved to the Command Palette (**Chat: Open Customizations** /
  **Chat: New Instructions File**); the gear-icon route in the original is stale.

Sources are footnoted in each file. Anything I could not confirm against first-party docs
is marked as unverified inline.

**These go stale.** Both tools ship changes weekly. Trust the linked documentation over
this folder when they disagree.
