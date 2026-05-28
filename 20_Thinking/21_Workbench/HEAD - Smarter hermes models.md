---
aliases: []
created: 2026-05-28T00:00:23+00:00
modified: 2026-05-28T12:31:13+00:00
tags: [prodos/head, state/thinking]
title: HEAD - Smarter hermes models
---

I need a way to make sure hermes is collecting data using a simple model but then querying complex models to figure things out. Currently I am running claude code and it is grepping and running cli commands using the expensive tokens. This stage is building context and any model could do that.

A problem I see is the lesser models get stuck trying to fix a problem and take ages where claude would do it in one go. How do we get hermes to recognise it is stuck and upgrade until it is solved?
