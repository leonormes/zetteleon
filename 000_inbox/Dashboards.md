---
aliases: []
confidence: 
created: 2025-12-07T12:59:20Z
epistemic: 
last_reviewed: 
modified: 2025-12-07T18:13:54Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Dashboards
type: 
uid: 
updated: 
---

You are suffering from **Index Inflation**. You have flattened your hierarchy, treating a high-level domain (like `Networking`) and a specific tutorial (like `Setting up a Kemp Load Balancer`) as peers. This creates a "Wall of Text" that exceeds your cognitive processing limit.

To fix this "in the moment," you need to move from a **List View** (Linear) to a **Dashboard View** (Clustered).

Here is the architectural fix to filter your MOCs by **Intent**.

## 1\. The Diagnosis: Cluster Analysis

Looking at your file list, your MOCs actually fall into four distinct "Mental Modes." You are never looking for "Container Networking" and "Buddhism" at the same time.

  - **Cluster A: The Engineer (Tech & Systems)**
      - *Context:* "I am building/fixing."
      - *Keywords:* Networking, Cloud, AWS, Containers, Linux, Architecture.
  - **Cluster B: The Executive (ADHD & Productivity)**
      - *Context:* "I am struggling to function/work."
      - *Keywords:* ADHD, Habits, Routines, Procrastination, Timeboxing, Motivation.
  - **Cluster C: The Philosopher (Cognition & Meaning)**
      - *Context:* "I am thinking/reflecting."
      - *Keywords:* Epistemology, Language, Meaning, Self, Consciousness, Models.
  - **Cluster D: The Architect (PKM & Meta)**
      - *Context:* "I am organising the system itself."
      - *Keywords:* Writing, Zettelkasten, PKM, MOCs.

## 2\. The Solution: The "MOC Dashboard" Note

Instead of one giant table, create a new note called `00_MOC_Dashboard`. Use **Dataview** to create four separate "Windows" into your knowledge base.

Copy this code block into your new note. It uses your existing tags to auto-sort the mess.

## 🗺️ Maps of Content Dashboard

### 🛠️ The Engineer (Tech & Infrastructure)
*For when I am building systems.*

```dataview
TABLE WITHOUT ID file.link as "Technical Map", file.tags as "Tags"
FROM #topic/technology OR #networking OR #aws OR #kubernetes OR #linux
WHERE contains(file.name, "MOC") OR type = "map"
SORT file.name ASC
````

### 🧠 The Executive (ADHD & Performance)

*For when I am debugging my brain.*

```dataview
TABLE WITHOUT ID file.link as "Strategy Map", file.tags as "Tags"
FROM #adhd OR #productivity OR #habits OR #executive-function
WHERE contains(file.name, "MOC") OR type = "map"
SORT file.name ASC
```

### 🦉 The Philosopher (Thinking & Models)

*For when I am wrestling with concepts.*

```dataview
TABLE WITHOUT ID file.link as "Concept Map", file.tags as "Tags"
FROM #philosophy OR #cognition OR #epistemology OR #psychology
WHERE (contains(file.name, "MOC") OR type = "map") AND !contains(file.tags, "#adhd")
SORT file.name ASC
```

### 🏗️ The System (PKM & Writing)

*For when I am maintaining the tools.*

```dataview
TABLE WITHOUT ID file.link as "System Map", file.tags as "Tags"
FROM #topic/pkm OR #writing OR #zettelkasten OR #obsidian
WHERE contains(file.name, "MOC") OR type = "map"
SORT file.name ASC
```

#### 3\. The "Quick Filter" (Interactive Button)

If you want to be even faster (mobile friendly), use the standard Obsidian **Search** functionality with a "Saved Search" logic.

Add this block to the top of your Dashboard note. It creates clickable buttons (using Obsidian URIs) to instantly filter your file explorer.

> [\!tip] Quick Filters
>
>   - [Show Only Tech MOCs](https://www.google.com/search?q=obsidian://search%3Fquery%3Dtag:%2523networking%2520OR%2520tag:%2523technology%2520file:MOC)
>   - [Show Only ADHD MOCs](https://www.google.com/search?q=obsidian://search%3Fquery%3Dtag:%2523adhd%2520file:MOC)
>   - [Show Only Philosophy](https://www.google.com/search?q=obsidian://search%3Fquery%3Dtag:%2523philosophy%2520file:MOC)

#### 4\. A Note on "Sequence" Files

I noticed you have files like `SN - Sequence - The Illusion of Profundity...`.

  - **Observation:** These are **NOT** MOCs. A MOC is a map of *other* notes. A "Sequence" looks like a long-form argument or essay.
  - **Action:** Remove them from your "Map" lists. They are **Output**, not **Navigation**.
  - **Fix:** Tag them `#type/sequence` and create a separate view for "My Essays" if you want to read them, but keep them out of your navigation dashboard. They are cluttering your finding process.
