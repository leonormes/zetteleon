---
aliases: []
confidence: 
created: 2025-07-12T11:08:55Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: The Handshake Puzzle
type:
uid: 
updated: 
version:
---

Here is a practical activity that demonstrates the generative side of maths for a Year 8 pupil.

## The Handshake Puzzle: Discovering a Pattern

This activity lets Bessie act like a mathematician by collecting data, spotting a pattern, and **generating** her own rule (an equation) to describe it.

### You Will Need

- A few willing participants (or you can use small objects like Lego figures to represent people).
- A piece of paper and a pencil.

---

## The Activity

### Step 1: Collect the Data

Start by posing the question: "If everyone in a room shakes hands with everyone else exactly once, how many handshakes are there in total?"

Now, collect the data for small groups:

- **2 People:** Person A shakes hands with Person B. That's **1** handshake.
- **3 People:** A shakes with B and C (2). B shakes with C (1). That's 2 + 1 = **3** handshakes.
- **4 People:** A shakes with B, C, D (3). B with C, D (2). C with D (1). That's 3 + 2 + 1 = **6** handshakes.

Record your findings in a simple table:

| Number of People (p) | Total Handshakes (H) |
| :------------------- | :------------------- |
| 2                    | 1                    |
| 3                    | 3                    |
| 4                    | 6                    |
| 5                    | ?                    |

Ask Bessie to work out the handshakes for **5 people** and add it to the table. (It will be $4 + 3 + 2 + 1 = 10$

### Step 2: Spot the Pattern

Now, look at the table together. The numbers of handshakes are `1, 3, 6, 10...` These are the **triangle numbers**. Ask Bessie what she notices about how the numbers are growing.

### Step 3: Generate the Rule

This is the creative, generative part. Say, "Instead of counting every time, can we create a formula to predict the number of handshakes for *any* number of people?"

Guide her thinking with these questions:

- "If you have $p$ people in a room, how many people does each person shake hands with?" (Answer: $p - 1$ because you don't shake your own hand).
- "So, if we multiply the number of people ($p$) by the number of handshakes each person makes ($p - 1$), what do we get?" (Answer: $p × (p - 1)$).
- "Let's test that for 4 people: $4 × (4 - 1) = 4 × 3 = 12$ . But we only counted 6 handshakes. What do you notice about our answer?" (Answer: It's exactly double!).
- "Why is it double?" (Answer: Because when we calculated it that way, we counted A shaking B's hand and B shaking A's hand as two separate handshakes, but they are the same one).
- "So how can we correct our formula?" (Answer: Divide it by 2).

You have just **generated** the equation for the handshake problem:

$$H = \frac{p \times (p - 1)}{2}$$

---

## The Maths Behind It

This activity perfectly demonstrates the difference between the two types of knowledge:

- **Applicative Knowledge:** Would be if you gave Bessie the formula at the start and just asked her to calculate the handshakes for 20 people. You are asking her to *apply* a known rule.
- **Generative Knowledge:** Is what you just did. You started with a real-world situation, collected data, found a pattern, and used logic to *generate* a brand-new formula that describes the pattern. This is thinking like a true mathematician.
