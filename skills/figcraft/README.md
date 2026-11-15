# `figcraft`

Teaches the agent to work on design systems in FigCraft, a Figma-like app with a full headless CLI and an MCP server: tokens, component sheets, screen
layouts in light and dark, and preview renders, all kept in step with the code.

## Usage

It loads by itself when a project has a `.figcraft` file or the task is UI design or a design
system. Or ask for it: `/figcraft`.

## What it brings

- Which interface to use for what: `info`, `render`/`export`, `run` scripts, `mcp`.
- How scripts behave (all or nothing, no references between steps), and the phase pattern that
  follows from it.
- The commands that matter, with the parameters that are easy to get wrong.
- A workflow for design systems: doc first, variables over hex, duplicate rather than rebuild,
  dark copies made from light ones, an export after every change.
- Known quirks (fonts, SVG import fills, automation roots).
- `scripts/fcrun.py`, a small Python runner (`FigCraft(file).run(steps, save=True)`, and
  `--tree ID` to print a subtree).

## Prerequisites

FigCraft installed at `C:\Program Files\FigCraft`, or `FIGCRAFT_CLI` pointing at
`figcraft-cli`. Python 3 for the helper.
