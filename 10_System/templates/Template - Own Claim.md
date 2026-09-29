---
title: <% tp.file.title %>
type: claim
own_words: true
status: seed
tags: []
conformant: true
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
modified: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
proposition: <% tp.file.title %>
epistemic_status: medium
evidence_links: []
contradicts: []
---

%% Hand-written version of Template - Atomic Zettel. Keep the two in step. This one is for notes you write yourself, so it carries own_words: true. If any wording comes from an LLM, delete that property. %%

%% Claim card. Same as the claim template in SoT - Atomic Note Standard (The Proposition Card). Name the file with the claim itself, as a full declarative sentence of at least four words. Frontmatter values contain no colon-space, apostrophes or double quotes. Delete these comments when done. %%

## <% tp.file.title %>

%% Opening statement: one to three sentences, in your own words. The whole idea, readable cold. %%

<% tp.file.cursor(1) %>

### Scope & Conditions

%% When it applies, the boundaries, the assumptions. %%

### Evidence

> "Verbatim quote from the source"
> (Author, work, location)

### Implications

-

### Related

- [[Other Note]]—relation: why the connection exists
