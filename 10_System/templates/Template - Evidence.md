---
permalink: llmeon/10-system/templates/template-evidence
---

%% Evidence card. Name the file "Evidence - Who Says What". source_quote is a direct extraction, not a paraphrase. confidence is a number from 0 to 1 and belongs to evidence notes only. Frontmatter values contain no colon-space, apostrophes or double quotes (reword the book subtitle). Delete these comments when done. %%

---
title: <% tp.file.title %>
type: evidence
status: seed
tags: []
conformant: true
created: "<% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>+00:00"
modified: "<% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>+00:00"
source_quote:
source_reference:
supports_claims: []
confidence: 0.5
---

## <% tp.file.title %>

> "Verbatim quote from the source"

### What It Supports

%% Which claim this bears on, and how. Add a typed edge line below if it grounds the claim: [supports:: [[Claim Note]], confidence=medium] %%

### What It Does Not Show

%% The limits of the evidence. %%
