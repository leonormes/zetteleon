---
title: <% tp.file.title %>
type: evidence
own_words: true
status: seed
tags: []
conformant: true
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
modified: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
source_quote:
source_reference:
supports_claims: []
confidence: 0.5
---

%% Hand-written version of Template - Evidence. Keep the two in step. This one is for notes you write yourself, so it carries own_words: true. If any wording comes from an LLM, delete that property. %%

%% Evidence card. Name the file "Evidence - Who Says What". source_quote is a direct extraction, not a paraphrase. confidence is a number from 0 to 1 and belongs to evidence notes only. Frontmatter values contain no colon-space, apostrophes or double quotes (reword the book subtitle). Delete these comments when done. %%

## <% tp.file.title %>

> <% tp.file.cursor(1) %>

### What It Supports

%% Which claim this bears on, and how. If it grounds the claim, add a typed edge line below in the form open-bracket supports two-colons wikilink-to-the-claim close-bracket. %%

### What It Does Not Show

%% The limits of the evidence. %%
