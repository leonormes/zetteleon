---
title: <% tp.file.title %>
type: source
own_words: true
status: seed
tags: [source/book]
conformant: true
source_reference: "{{VALUE:citation}}"
authors: "{{VALUE:authors}}"
year: "{{VALUE:year}}"
calibre_id: "{{VALUE:calibre_id}}"
calibre_link: "{{VALUE:calibre_link}}"
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
modified: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
---

%% One note per book or article. The citation lives here once, so every Evidence or point note
can link back to this note instead of retyping it. Paraphrase in your own words and quote
rarely. Created by the Source choice in QuickAdd, which fills the citation from Calibre. %%

## What this source is about

<% tp.file.cursor(1) %>

## Ideas worth a note of their own

%% One line per idea you will turn into an Evidence or point note. Link each one here as you write it. %%

-

## What it does not show

%% The limits of this source: what it does not cover, what it assumes, who would disagree. %%
