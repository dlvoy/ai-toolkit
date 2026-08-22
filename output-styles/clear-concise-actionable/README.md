# Clear, Concise, Actionable

A Claude Code output style that trades pleasantries for signal: put the answer last-line
first, give every list of findings or options a short reference code, drop the flattery.

## Attribution

The instructions in [`clear-concise-actionable.md`](clear-concise-actionable.md) are not
mine. They were AI-extracted from
["FIXING Opus 5: PROOF that Prompt Engineering IS NOT DEAD"](https://www.youtube.com/watch?v=S_QdQ1G4GlU)
by [IndyDevDan](https://www.youtube.com/@indydevdan), who writes the file live on screen
during the video. The file itself was never published — see
[Reconstruction notes](#reconstruction-notes) for how it was recovered and how much of it
is confirmed.

## What it does

- **Purpose** — sets the tone: solve problems, create value, no filler.
- **Positive / negative patterns** — most important information last, plain language,
  each fact stated once. An explicit banned-phrase list ("load-bearing", "worth stating
  plainly", "here's the honest truth"), no analogies, no unearned agreement.
- **Reference points** — three or more findings, decisions, options, risks, questions, or
  actions get short codes (`F1`, `D1`, `O1`, `R1`, `Q1`, `A1`) that stay stable for the
  whole conversation, so you can reply "do A2, drop A3".
- **Hard operational boundaries** — deliver the requested scope only, no speculative
  abstractions, no claiming completion without evidence, never add a commit co-author.
- **Aliases** — `scr`, `eli`, `foc`, `ref` expand to compression/refocus instructions when
  typed on their own.

Useful if you already know the domain and want the answer. Less useful when you want
Claude to explain its reasoning — the Explanatory built-in style is the opposite of this.

## Installing

```bash
cp clear-concise-actionable.md ~/.claude/output-styles/     # all projects
cp clear-concise-actionable.md .claude/output-styles/       # this project
```

Then `/config` → **Output style** → **Clear, Concise, Actionable**. It takes effect after
`/clear` or in a new session. See [the output styles note](../../howto/claude-output-styles.md).

## Changes made in this repo

The body is verbatim from the reconstruction. Two things were added or changed:

1. **YAML frontmatter**, which the original had none of. Without it the style would be
   named after the filename, and — because `keep-coding-instructions` defaults to `false`
   — installing it would have silently dropped Claude Code's built-in software-engineering
   instructions. It is set to `true` here: this style changes how Claude talks, not how it
   engineers.
2. The truncation marker at the end of the file now points at this README, since the
   reconstruction notes moved here.

## Reconstruction notes

*How the file was recovered, and what is and is not trustworthy in it.*

**Source material**: a screen recording (`FIXING Opus 5 PROOF that Prompt Engineering IS
NOT DEAD.webm`, 3840x2160, ~34 min) in which the author hand-types the file live in an
editor, plus a Whisper transcription of the narration with timestamps. Everything in the
file was read off the screen.

**Method**:

1. Parsed the transcript for narration and rough timing of each editing phase.
2. Used `ffprobe`/`ffmpeg` to pull full-resolution frames at targeted timestamps, plus 5x4
   contact-sheet montages (one frame every 15s) to scan long stretches for the moments the
   editor was actually on screen — the recording repeatedly cuts to terminal panes, B-roll,
   and overlay graphics, so most of the runtime shows no file content at all.
3. The editor shows a line-number gutter and a breadcrumb of the current heading, and folds
   finished sections as new ones are typed. That pinned each addition to an exact line
   number, cross-checked against an earlier unfolded shot of the same lines.
4. Ambiguous glyphs (`...` vs `..`, presence or absence of a `D1` bullet, "the" vs "they",
   comma vs period) were resolved with tight pixel crops of single lines rather than
   inferred from context.
5. Where the file was edited after first being typed, the latest on-screen version was
   used — the `eli` alias, for instance, was fixed on screen from `SImplify` to `Simplify`.

**Confidence**:

- Sections 1-4 (Positive/Negative Patterns, Reference Points, Hard Operational Boundaries,
  Aliases) and the Purpose block: **high**. Each line was read from a clean, unfolded
  frame, most more than once at different points in the recording.
- Examples → *Simple Investigation*, *Engineering Recommendation*: **high**, same basis.
- Examples → *Summarizing a blog*, "To do" block: **high**.
- Examples → *Summarizing a blog*, "Not to do" block: **incomplete**. Only the opening two
  lines are confirmed on screen before the recording cuts to a terminal pane, and the
  editor is never scrolled back to that block. Per the narration this block was pasted from
  an actual model response and then trimmed by hand, so the on-screen terminal response is
  not a reliable stand-in for the final text. The block is left truncated with a marker
  rather than guessed at.

**Preserved as-is** — these are on screen in the original, not transcription errors:

- "no-bs, clear concise, actionable relationship" — missing comma between "clear" and
  "concise", inconsistent with the comma used two lines later.
- "Use numbered lists and markdown headings when the improve navigation." — "the" where
  "they" is presumably meant.
- "In addition to clearly communicating. It's important..." — period where a comma is
  presumably meant.
- "the simplest word(s) that satisfies the idea your trying to communicate" — "your" for
  "you're".
- "only repeat if its relevant to subsequent queries" — "its" for "it's".
- "Whats the true signal? Whats the true value?" — missing apostrophes, both instances.
