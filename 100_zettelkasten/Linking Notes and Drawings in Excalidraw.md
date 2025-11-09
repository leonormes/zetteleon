---
aliases: []
confidence: 
created: 2025-10-24T13:14:20Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [excalidraw, linking, obsidian, topic/pkm/zettelkasten]
title: Linking Notes and Drawings in Excalidraw
type:
uid: 
updated: 
version:
---

While Excalidraw allows for rich visual linking, it's important to understand how these links interact with Obsidian's wikilink system.

## Adding Notes to the Canvas

You can add notes to an Excalidraw canvas in several ways:

- Type a wikilink like `[[My Note]]` in a text box. Excalidraw can create the note if it doesn't exist.
- Drag a `.md` file from the file explorer onto the canvas.
- Use the "Insert Link" option.

## Visual vs. Actual Links

Drawing an arrow between two notes on a canvas is a **visual-only link**. It does not automatically create a `[[wikilink]]` in the underlying markdown files.

To create "real" links that Obsidian recognizes:

1. **Manual Wikilinks**: When you select an element, you can use the command "Copy Markdown link for selected element to clipboard" to get a link like `[[NoteName#^elementID]]` that you can paste into other notes.
2. **ExcaliBrain Plugin**: This companion plugin can interpret the visual relationships in your drawings and display them as an interactive, navigable graph, effectively making the visual links "real" within its interface.

---

**Source:**
