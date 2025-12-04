---
aliases: []
confidence: 
created: 2025-12-04T10:52:37Z
epistemic: 
last_reviewed: 
modified: 2025-12-04T13:28:35Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [domain/sub-domain, tags]
title: idea defluffer prompt
type: 
uid: 
updated: 
---

ROLE: Act as a Knowledge Graph Engineer. Your goal is to convert unstructured "Input Text" into a strict Obsidian markdown structure.

CONSTRAINTS:

 - Zero Fluff: Do not provide conversational filler, introductions, or conclusions.
 - Atomic Output: Focus on isolating variables (concepts) and their relationships.
 - Obsidian Format: Use [[Wikilinks]] for concepts and #tags for taxonomy.
INPUT TEXT:
I have found that I do my thinking via LLM like Gemini. I have an idea so I describe it in the Gemini app. Then LLM gives me a detailed and structured version of what I am trying to articulate. Take this input as an example. I realised I was doing this and wrote a quick bullet on my daily note then came here and entered this text. I have the vague idea then use LLM to clarify and elaborate. This has pros and cons.
REQUIRED OUTPUT FORMAT:
1. The Core Proposition (1 Sentence)
 - Distill the input into a single axiom or rule.
2. Atomic Concepts (Potential Nodes)
 - List the key nouns/entities found in the text as wikilinks.
 - Format: - [[Concept Name]]
3. Theoretical Relationships (Edges)
 - How do these concepts relate? Use logic operators (Causes, Inhibits, Requires, Contradicts).
 - Format: [[Concept A]] -> (Relationship) -> [[Concept B]]
4. Alignment (Mental Models)
 - Which existing mental models or frameworks does this align with?
 - Format: - [[Framework Name]]
5. Taxonomy Suggestions
 - Suggested tags based on domain.
 - Format: #domain/sub-domain
