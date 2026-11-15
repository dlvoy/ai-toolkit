---
name: figcraft
description: Design systems and UI design in FigCraft, the Figma-like app at C:\Program Files\FigCraft, driven headless through its CLI or MCP server. Use when a project has a .figcraft file or a design system to keep in step with the code (tokens, component sheets, screen layouts, light and dark, preview PNGs), when asked to draw or update UI designs, mockups or a design system, or to turn an SVG into an Android vector drawable. For a single SVG image (logo, icon, illustration) or raster conversion, use the vectorcraft skill instead.
---

# FigCraft

FigCraft (`figcraft.exe`, `figcraft-cli.exe` in `C:\Program Files\FigCraft`) reads and writes
`.figcraft`, Figma `.fig` and REST JSON, Penpot, Sketch, SVG and images. It has variables with
modes, text styles, components, auto layout and a few thousand commands. Everything works without
the window.

## Pick the interface

| Need | Use |
| --- | --- |
| Look at a file | `figcraft-cli info FILE` (pages, top-level frames with ids and sizes, counts) |
| Render for a preview or a check | `figcraft-cli render FILE --page NAME --out x.png [--scale N]`, or `export FILE --node ID --out x.png` |
| Edit the file | `figcraft-cli run --in FILE --out FILE script.json`, or the helper `scripts/fcrun.py` next to this file |
| Interactive work, many small reads | `figcraft-cli mcp` (JSON-RPC over stdio; tools `run_command`, `batch`, `get_node`, `set_properties`, `export`, `save_file`). Attaches to a running app, else headless |
| Find a command or its parameters | `figcraft-cli commands`, grep the output |
| SVG to Android vector drawable | `figcraft-cli export --format xml --out icon.xml icon.svg` |

Pass `--no-system-fonts` to `run`, `render` and `export`. Text then lays out with the built-in
fonts, so renders match on every machine. Built in: Inter, Roboto, Lato, Montserrat, Open Sans,
Poppins, Nunito Sans, Source Sans 3, Merriweather, Playfair Display, Liberation, Noto. Font
downloads may be off, so a webfont like Geist is not there: stand in with Inter and say so.

## Scripts

A script is a JSON array of `{"command": id, "params": {...}}`, run as one undo step. All of it
lands, or none of it does. Results come back one JSON line per step.

- **Steps can't use an earlier step's result.** Work in phases: create or duplicate, save, read
  the new ids from the results, then edit them in the next run. `scripts/fcrun.py` does the
  plumbing (`FigCraft(file).run(steps, save=True)`), and `--tree ID` prints a subtree.
- **Back up the file before a run that saves.** A phase that fails after an earlier phase saved
  leaves half the change in place. Restore the backup and run the phases again rather than
  patching around stray copies.
- Ids are stable across saves, so a dry run (without `--out`) shows what a run will return.

The commands you will use most:

| Command | Notes |
| --- | --- |
| `node.get {id, fields? \| outline?}` | `outline: true` lists children. No depth: walk level by level |
| `node.find {root?, name?, type?, text?, limit?}` | Substring match, case-insensitive; returns `{ids, total}` |
| `node.create {type, parent?, name?, path?, width?, height?, props?}` | `type: vector` takes SVG path data in `path` and scales it to `width`×`height` |
| `text.create {text, x, y, parent?, width?, props?}` | `props`: `fontFamily`, `fontStyle`, `fontSize`, `fill` |
| `node.set {ids, ...}` | Any property: `characters`, `fill`, `cornerRadius`, `layout`, `gap`, `padding`, `sizingH`/`sizingV` (`fixed`, `hug`, `fill`), `mainAlign` (incl. `spaceBetween`), `crossAlign`, `textAutoResize` |
| `edit.duplicate {ids, dx?, dy?, map: true}` | `map` returns every original id → its copy, descendants included |
| `node.reparent {ids, parent, index?}` | No index: last child, so in auto layout it goes to the end. `index: 0` makes it first |
| `edit.delete {ids}` | |
| `variable.create {collection, name, type, value, description?}` | `variable.list` shows collections, modes and ids |
| `variable.setMode {ids, collection, mode}` | Switches a frame and everything in it to a mode, e.g. Light/Dark |

## Working on a design system

1. Read the project's design doc first (often `docs/design/DESIGN.md`). When the file and the
   doc disagree, the doc wins: fix the file.
2. `info` the file. Then `--tree` the frames you will touch, so you edit by id, not by guess.
3. Bind colours to variables (`{"$var": "primary"}`), never raw hex, except a fixed brand colour
   kept as its own primitive variable.
4. Reuse what is there: duplicate an existing row, badge or card and change its texts. That keeps
   the spacing and styles of the system without rebuilding them.
5. **Light and dark.** A common layout keeps a dark copy of each frame beside or below the light
   one, with the `Color` collection set to Dark. After changing a light frame, rebuild its dark
   copy: delete the old one, duplicate the light one to the same place, `variable.setMode` Dark.
   That beats editing both by hand.
6. Auto-layout frames with `sizingV: hug` grow on their own when you add rows. Fixed-size ones
   don't, so check `sizing` before you add.
7. Export every changed frame (`export --node ID`) and look at it before moving on. Text that
   wraps in a control usually needs `textAutoResize: widthAndHeight` plus a wider parent.
8. Render the preview images again when the project keeps them (`render --page NAME`, then
   resize to the old width so the diff stays small).

## Quirks

- `--automation-read-root` / `--automation-write-root` folders must exist, or the server exits
  at once.
- `file.import` of an SVG scales to its `width`/`height`. A shape fills only if the SVG brought
  a fill: setting `fill` afterwards on a stroked import shows nothing. For one path, it is easier
  to pass the path data to `node.create` with `type: vector`.
- `node.get` rejects unknown `fields`. The error lists the valid ones.
- Several thousand commands run in a few seconds. Each `run` reloads and saves the whole file,
  so batch steps into few runs.
