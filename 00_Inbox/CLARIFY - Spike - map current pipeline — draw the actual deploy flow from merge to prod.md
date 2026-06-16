---
created: 2026-06-11T14:48:39+00:00
title: "CLARIFY - Spike: map current pipeline — draw the actual deploy flow from merge to prod"
tags: [clarify, todoist-inbox]
type: clarify
---

Imported from Todoist inbox on 2026-06-11 15:48.

## Description

Before fixing anything, get the current state on paper (or in Excalidraw/Mermaid). This is the forcing function for all the other tasks.

First physical action: open a scratch file and draw the pipeline as a sequence:
  1. Code merged to main
  2. What triggers the staging deploy?
  3. What gate exists between staging and prod?
  4. What happens when staging breaks — where exactly does the pipeline halt?

This will make the problem concrete and the solution obvious.

## Next Action

Review and clarify what this means, then take action.

