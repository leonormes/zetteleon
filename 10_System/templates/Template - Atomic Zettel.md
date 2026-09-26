---
permalink: llmeon/10-system/templates/template-atomic-zettel
---

%% Claim card. Same as the claim template in SoT - Atomic Note Standard (The Proposition Card). Name the file with the claim itself, as a full declarative sentence of at least four words. Frontmatter values contain no colon-space, apostrophes or double quotes. Delete these comments when done. %%

---
title: <% tp.file.title %>
type: claim
status: seed
tags: []
conformant: true
created: "<% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>+00:00"
modified: "<% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>+00:00"
proposition:
epistemic_status: medium
evidence_links: []
contradicts: []
---

## <% tp.file.title %>

%% Opening statement: one to three sentences, in your own words. The whole idea, readable cold. %%

### Scope & Conditions

%% When it applies, the boundaries, the assumptions. %%

### Evidence

> "Verbatim quote from the source"
> (Author, work, location)

### Implications

-

### Related

- [[Other Note]]—relation: why the connection exists
