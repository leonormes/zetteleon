---
aliases: []
created: 2025-10-24T13:14:20Z
last_reviewed: "null"
modified: 2026-02-01T15:08:31+00:00
status: "null"
tags: ["excalidraw", "linking", "obsidian", "topic/pkm/zettelkasten"]
title: Linking Notes and Drawings in Excalidraw
type: "null"
updated: 
---

While Excalidraw allows for rich visual linking, it's important to understand how these links interact with Obsidian's wikilink system.

## Adding Notes to the Canvas

You can add notes to an Excalidraw canvas in several ways:

- Type a wikilink like `[[My Note]]` in a text box. Excalidraw can create the note if it doesn't exist.
- Drag a `.md` file from the file explorer onto the canvas.
- Use the "Insert Link" option.

## Visual vs. Actual Links

Drawing an arrow between two notes on a canvas is a visual-only link. It does not automatically create a `[[wikilink]]` in the underlying markdown files.

To create "real" links that Obsidian recognizes:

1. Manual Wikilinks: When you select an element, you can use the command "Copy Markdown link for selected element to clipboard" to get a link like `[[NoteName#^elementID]]` that you can paste into other notes.
2. ExcaliBrain Plugin: This companion plugin can interpret the visual relationships in your drawings and display them as an interactive, navigable graph, effectively making the visual links "real" within its interface.

---

Source:
