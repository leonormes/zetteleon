---
title: <% tp.file.title %>
type: question
own_words: true
tension: ""
candidate_answers: []
related_claims: []
sources: []
tags: [state/thinking, prodos/head]
aliases: []
conformant: true
status: open
prodos:
  kind: head
  lifecycle: active
AoL: <% (await tp.system.suggester(["Personal","Work","System"],["Personal","Work","System"],false,"Area of life")) ?? "Personal" %>
closing_condition: false
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
modified: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
---

## The Question

%% One paragraph. The open thing, stated plainly. Once you can phrase it as a question,
rename this note to "HEAD - <your question>?". If you cannot phrase it as a question,
this is not a HEAD note. See [[SoT - HEAD Note Contract (The Workbench)]] §1. %%

## Why It Matters

%% What decision, belief, or piece of work is downstream of this? If nothing is,
close the note now. %%

## What I Currently Think

%% The current lean. "No idea" is a valid and honest answer. Write it yourself: this note
is marked own_words. If any wording here came from an LLM, delete the own_words property. %%

## What Would Settle It

%% The evidence, experiment, decision, or conversation that closes this thread.
A note that cannot name its own closing condition will still be open in a year.
When you have written it, set closing_condition to true. %%

## Sources

%% Wikilinks to the SoT/claim notes this was harvested from, or the capture that
provoked the question. %%
