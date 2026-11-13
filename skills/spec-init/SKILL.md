---
name: spec-init
description: Set up spec-driven design in the current project. Creates docs/specs (a README explaining the layout, one NN-intent-name folder per feature with intent.md, plan.md and status.md) and adds a Specs section to CLAUDE.md so future sessions plan through the specs. Use for /spec-init, when asked to set up specs, intents or spec-driven design, and whenever the user starts a new project (scaffolding an app, git init, "let's create a new project/repo") — in that case first ask whether the project should follow spec-driven design.
argument-hint: [first intent, e.g. "user login"]
allowed-tools: Bash(git rev-parse *) Bash(git status *) Bash(ls *) Bash(mkdir *) Bash(test *) Bash(date *) AskUserQuestion Read Write Edit Glob
---

# spec-init

Sets up the project root for spec-driven design: every feature or change is an **intent** with
its own folder under `docs/specs`, written down (what and why, then how) before code, and kept
current as the work moves. `CLAUDE.md` gets the rules so every later session follows them.

Templates live next to this file in `templates/`. Read them; do not retype them from memory.

## 1. Decide whether to run

- **Invoked directly** (`/spec-init`, or the user asked for specs / spec-driven design): go on.
- **Triggered by a new project** (the user is scaffolding an app, running `git init`, creating
  a repo): ask once with AskUserQuestion, header `Specs`:
  "Should this project follow spec-driven design (docs/specs with one intent folder per
  feature, wired into CLAUDE.md)?" Options: `Yes, set it up (Recommended)` / `No`.
  On `No`, drop it and carry on with the project; do not ask again in this session.
  Ask after the project folder exists (or together with the other setup questions), so there
  is a root to write into.

## 2. Find the root

1. `git rev-parse --show-toplevel` — the git root is the project root.
2. No repo: use the current working directory if it is clearly the new project's folder;
   otherwise ask which folder. Do not run `git init` yourself unless the user asked for it.

All paths below are relative to that root.

## 3. Check what is already there

- `docs/specs/README.md` exists: the project already uses specs. Do not overwrite it. Report
  that, check that CLAUDE.md has the Specs section (step 5), and stop unless a first intent
  was requested.
- `docs/specs/` exists with other content: list it and ask before adding anything.
- Existing `NN-*` folders: the next intent number is one above the highest, never reusing one.

## 4. Create docs/specs

1. `mkdir -p docs/specs`
2. Write `docs/specs/README.md` from `templates/README.md`. The intents table ends with its
   header and no rows; each intent adds one row (`| 01 | [Name](01-name/intent.md) | planned |`).
3. **First intent** — create one when the argument names one, or when the user already
   described what the project should do (a new project usually has a first feature in the
   conversation). Otherwise skip it; do not invent features.
   - Folder `docs/specs/01-<kebab-name>/` (or the next free number).
   - `intent.md`, `plan.md`, `status.md` from the templates. Fill in what is actually known
     from the conversation; leave a short `TBD` where nothing is known rather than guessing.
     `status.md` starts at `**State:** planned`.
   - Add the row to the table in `docs/specs/README.md`.
4. **Existing codebase** (a project with real code, not a fresh scaffold): offer, in one
   question, to backfill intents for the features already built (state `done`, plan pointing
   at the real files). Only do it on a yes, and read the code first so the plans name real
   files and symbols.

## 5. Wire up CLAUDE.md

Read `templates/claude-section.md` for the section text.

- No `CLAUDE.md`: create one with a `# CLAUDE.md` heading, one line saying what the project is
  (from the conversation or README; `TBD` if unknown), then the Specs section.
- `CLAUDE.md` exists without a `## Specs` section: append the section at the end, separated by
  a blank line. Do not touch the rest of the file.
- It already has a `## Specs` section: leave it, and say whether it matches the template.

If the project has domain rules that must never be broken (safety, money, data loss), mention
them by name in the first bullet ("Their rules, especially the … rules, stay in force"), as
long as they come from the user or the existing code, not your guess.

## 6. Report

A short list: files created, files changed, files left alone, and the first intent if any.
Do not commit; the user commits when they want to.

## Rules for the spec files

- `intent.md` describes the outcome (goal, user-visible behaviour, rules, out of scope), never
  the code. `plan.md` describes the code: files, components, approach, tests. `status.md` says
  where it stands: state, release, done, known gaps, open questions.
- States: `planned`, `in progress`, `done`, `dropped`.
- Intents link to each other with relative links, e.g. `[03](../03-name/intent.md)`.
- Plain, specific prose. Real file paths and symbol names in plans, no placeholders left behind
  once the code exists.
