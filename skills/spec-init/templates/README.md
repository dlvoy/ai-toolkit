# Specs

Each intent (a feature or a change to the project) has its own folder here, named
`NN-intent-name`: a two-digit number followed by a short kebab-case name. Numbers start at `01`
and go up by one; a new intent takes the next free number. Numbers are never reused, even when an
intent is dropped.

Every intent folder holds three files:

| File | What it holds |
| --- | --- |
| `intent.md` | Why the intent exists and what it must do: goal, user-visible behaviour, rules and constraints, what is out of scope. Describes the outcome, not the code. |
| `plan.md` | How it is (or will be) built: the files and components involved, the approach, the steps, and the tests that cover it. |
| `status.md` | Where it stands: state, the release it shipped in, what is done, known gaps and open questions. |

`status.md` starts with a state line, one of `planned`, `in progress`, `done`, `dropped`.

## Workflow

1. **Plan.** A new feature gets a new folder. Write `intent.md` first, then `plan.md`, before
   any code. A change to an existing feature edits that intent's files instead.
2. **Build.** Set `status.md` to `in progress` and keep it current: what is done, what is left,
   what turned out different from the plan (and update `plan.md` to match).
3. **Finish.** Set the state to `done`, note the release it shipped in, and list known gaps.
4. **Drop.** An intent that will not be built is set to `dropped` with the reason; the folder
   and its number stay.

The rules written in an intent stay in force for later work until the intent itself is changed.
Intents refer to each other with relative links, e.g. `[02](../02-name/intent.md)`.

## Intents

| # | Intent | State |
| --- | --- | --- |
