# `vectorcraft`

Teaches the agent to make and convert vector images with
[VectorCraft](https://getartcraft.com/apps/vectorcraft), an Illustrator-like app with a headless
CLI and an MCP server: logos, icons and illustrations as SVG, and the rasters made from them.

## Usage

It loads by itself for SVG work, icon sets and format conversion. Or ask for it: `/vectorcraft`.

## What it brings

- `convert` for one-shot conversion and rasterising, `run` for edit-then-export, `mcp` for
  interactive drawing, and how `--scale` maps to pixels.
- Recipes: a favicon set (PNG sizes packed into an `.ico`), apple and PWA icons, Android
  launcher icons (a vector drawable, with FigCraft doing the SVG to XML step).
- Rules: keep the source SVG in the repo, treat downloaded SVGs as untrusted, write plain SVG.

## Prerequisites

VectorCraft installed at `C:\Program Files\VectorCraft`. Pillow, if you pack `.ico` files.
