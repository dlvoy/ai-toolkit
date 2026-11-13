# `spec-init`

Sets a project up for spec-driven design: every feature is an **intent** with its own folder
under `docs/specs`, written down before any code, and `CLAUDE.md` tells every later session to
plan through those folders.

## Usage

```
/spec-init
/spec-init user login
```

It also fires on its own when you start a new project (scaffolding an app, `git init`, "let's
create a new repo"). In that case it asks first whether the project should follow spec-driven
design, and does nothing on a no.

## What it creates

```
docs/specs/
  README.md              how the specs work, plus the table of intents
  01-user-login/         only if a first intent is named or already described
    intent.md            what and why: goal, behaviour, rules, out of scope
    plan.md              how: approach, files and symbols, steps, tests
    status.md            planned | in progress | done | dropped, done, gaps
CLAUDE.md                gains a "## Specs" section (created if missing)
```

The project root is the git root, or the current folder when there is no repo. It never runs
`git init` and never commits.

## Behaviour on an existing project

- `docs/specs/README.md` already there: nothing is overwritten; only the CLAUDE.md section is
  checked.
- `CLAUDE.md` already has a `## Specs` section: left alone.
- A codebase with real features: it offers to backfill intents for them (state `done`), and
  reads the code first so the plans name real files.

## Files

| File | Role |
| --- | --- |
| `SKILL.md` | The skill. |
| `templates/README.md` | Becomes `docs/specs/README.md`. |
| `templates/intent.md`, `plan.md`, `status.md` | Skeletons for an intent folder. |
| `templates/claude-section.md` | The section appended to `CLAUDE.md`. |

## Attribution

Mine. The layout is lifted from one of my own Android projects, generalised.
