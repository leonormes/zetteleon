---
aliases: []
author: ["[[Gemini]]"]
confidence: 
created: 2025-12-14T00:00:00Z
description: "Created with Gemini"
epistemic: 
last_reviewed: 
modified: 2025-12-14T18:38:43Z
published:
purpose: 
review_interval: 
see_also: []
source: "https://gemini.google.com/share/e92be7ff3564"
source_of_truth: []
status: 
tags: ["clippings"]
title: Modeling Team Understanding and Bias
type: 
uid: 
updated: 
---

I want to create a mathematical model of team understanding. I have noticed that people have different ideas and understanding about complex topics and sometimes even combined there is no whole picture. But because of cognitive biases and certainty groups think they understand a problem. So each person has a set of knowledge that creates an amount of understanding of a topic. Combining all the sets via communication line talking or documenting creates a bigger understanding. What would a maths model of this look like

This is a concept that can be effectively described using **set theory** and **probability**, with added variables to account for communication and bias.

Here is a formal mathematical model built on your components.

---

## 1\. The Core Elements: Knowledge Sets

First, we define the universe of information and the knowledge of individuals.

- **The "Whole Picture" (Universal Set):** Let be the complete and accurate set of all discrete concepts, facts, and relationships for a given complex topic. The "total" understanding possible is the size (cardinality) of this set, .
- **Individual Knowledge (Subset):** Each person on a team has a knowledge set, , which is a **subset** of (i.e., ).
	- represents the *actual*, correct knowledge that person possesses.
	- **Misinformation** (ideas a person holds that are *not* in ) could be modelled as another set, , but we'll focus on for now.
- **Team's Potential Knowledge (Union):** The total knowledge held by the team *collectively* is the **union** of all their individual sets:
	This represents the maximum possible understanding the team could achieve if communication were perfect.

---

## 2\. Measuring Understanding vs. Overlap

The "amount" of understanding is the size (cardinality) of these sets.

- **Actual Individual Understanding ():** This is a measure of how much of the whole picture person has.
	(This is a value between 0 and 1, or 0% to 100%).
- **Actual Team Understanding ():** This is the measure of the team's *collective* knowledge.

This is where the problem of "combination" you mentioned becomes critical. The size of the union is **not** the simple sum of the individual parts. It's defined by the **Principle of Inclusion-Exclusion**:

- **For 2 people:**
- **The term is the "overlap"** or **shared knowledge**.

High-performing teams often have low overlap (diverse knowledge). Teams where everyone knows the same things have high overlap, and their collective knowledge isn't much bigger than any individual's .

---

## 3\. Modelling Cognitive Bias and Certainty

This is the gap between what a team *thinks* it knows and what it *actually* knows. We must introduce new "perception" variables.

- **Perceived Individual Understanding ():** This is what person *thinks* they know. This is often a function of their bias, .(In Dunning-Kruger, for low , is high and positive, so ).
- **Perceived Team Understanding ():** This is what the group *collectively* assesses its understanding to be. This is not a simple union; it might be:
	- The average of individual perceptions:
	- Dominated by the most confident member:
	- Inflated by groupthink: (where is a group bias term).

This lets us define the two gaps you observed:

1. **The Knowledge Gap (External):** This is the part of the problem the team *cannot* solve, no matter how well they communicate.

	> **Gap (External)** = (The concepts no one on the team knows)

2. **The Certainty Gap (Internal Bias):** This is the "delusion" you mentioned.

	> **Gap (Certainty)** = (When , the team is overconfident. They believe they understand a problem they do not).

---

## 4\. Modelling the "Communication Line"

Your model correctly identifies that (the potential knowledge) is not achieved instantly. Communication is a lossy process.

- **Communication Efficiency ():** We can introduce a factor (where ) that represents the quality of the communication line (documentation, meetings, clarity of language).
- **Realised Team Knowledge ():** The knowledge that is *actually* synthesised and available to the team for a decision is the **Realised Knowledge**, .

If (perfect communication), the team realises 100% of its potential. If (terrible documentation, people talking over each other), they only manage to synthesise 20% of their collective knowledge.

This introduces a third, tragic gap:

1. **The Synthesis Gap (Internal Process):**

> **Gap (Synthesis)** = (Knowledge that *exists* in the team but was *lost* due to poor communication).

---

## A Complete Model Example

Let's put it all together.

**Topic:** Understand a complex software bug.

- **Total Concepts ():** There are 100 concepts needed for a full solution. .

**The Team:**

- **Alice ():** Knows 30 concepts. . But she is overconfident. .
- **Bob ():** Knows 25 concepts. . He is under-confident. .
- **Overlap ():** They share 10 concepts.

**The Model in Action:**

1. **Potential Team Knowledge ():**The team *collectively* holds 45 of the 100 concepts.
2. **Actual Team Understanding ():****45%** (This is their objective, maximum possible understanding).
3. **The Knowledge Gap:** concepts. (There is 55% of the problem that this team *cannot* solve, no matter what).
4. **Perceived Team Understanding ():**Alice is the most confident, so the team defers to her (a model).**60%**
5. **The Certainty Gap (Bias):****15%** (The team is 15% overconfident. They *think* they know 60% of the problem, but they only know 45%).
6. **The Communication Line ():**They have a hasty 10-minute meeting. Communication is poor. .
7. **Realised Team Knowledge ():**Their *actual working knowledge* after the meeting is only 22.5 concepts (or 22.5%).

**The Final State:** The team proceeds to make a decision, *believing* they have 60% understanding, when in reality they only managed to synthesise **22.5%** of the problem, from a potential maximum of **45%**. The remaining **55%** was entirely unknown to them.

This model, based on set theory (), set operations (), and modifiers (), seems to capture the dynamic you described.

---

Would you like to explore how to model the *growth* of these knowledge sets over time (e.g., through research), or how to model the "misinformation" part?

Google Account

Leon Ormes

leonormes@gmail.com
