---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/312f4856ad66"
captured: "2026-02-04T09:20:55+00:00 2026-02-04T09:20:55+00:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
help me to understand a semantic clash I see. People talk about software and programming being complex. But to me complex is when outputs are emergent and 'more than the some of its parts', like life emerging from chemistry. Complicated is like a mechanical watch. very difficult but ultimatley understandable and predictable from the parts. surely, by definition, computers are complicated and not complex in this context? The computer processor does exactly what it is instructed to do, bugs and all.

This is a fantastic semantic distinction to make, and you are arguably correct in the strictest sense of the definitions.

The clash you are observing often comes from two different perspectives: the **Micro View** (the code itself) versus the **Macro View** (the system in operation).

To resolve this, we can look at the **Cynefin framework**, which formally distinguishes between these two states exactly as you have:

- **Complicated:** The relationship between cause and effect is discoverable. A mechanical watch is the perfect analogy. You can take it apart, analyse the parts, and predict exactly how it works.
- **Complex:** Cause and effect can only be understood in retrospect. The output is emergent and not predictable merely by analysing the components.

Here is why software engineers insist that modern software has crossed the boundary from **Complicated** to **Complex**.

### 1\. The Illusion of Determinism

You are correct that a processor is deterministic. If `Input A` enters `Function B`, the result should always be `C`. If software remained a single script running on a single machine in a vacuum, it would indeed just be **complicated**.

However, modern software rarely runs in a vacuum. It interacts with:

- **The Network:** Packets get lost, latency spikes, and connections drop randomly.
- **Hardware Faults:** Bits flip, disks fail, and power fluctuates.
- **Asynchronicity:** Millions of instructions happen in parallel. The exact order in which different parts of a system finish a task can change every millisecond.

Because of these environmental variables, a deterministic piece of code can produce non-deterministic behaviour.

### 2\. Emergent Behaviours (The "Retry Storm")

You mentioned that complexity requires the output to be "more than the sum of its parts." In software, this happens through **emergence**.

Consider a "Retry" function.

- **The Part:** A piece of code says, "If the server is busy, wait 1 second and try again." This is simple, predictable logic.
- **The Whole:** Imagine 10,000 users hit a glitch simultaneously. They all fail. They all wait 1 second. They all retry at the exact same moment. The server crashes again under the synchronized load. They all wait 2 seconds...

This is called a "Retry Storm" or "Thundering Herd." The system collapses not because the code was wrong (it did exactly what it was told), but because the *interaction* of correct parts created an unpredictable, emergent disaster. That is complexity.

### 3\. The State Space Explosion

A mechanical watch might have hundreds of parts, but its "state space" (the number of possible configurations it can be in) is finite and manageable.

A modern software system, with its variables, memory states, database entries, and network conditions, has a state space that is effectively infinite. It is mathematically impossible to test every possible combination of states. Therefore, we cannot "know" the system in the same way a watchmaker knows a watch. We can only observe its behaviour, much like a biologist observes an ecosystem.

### Summary

The semantic clash exists because:

- **You are looking at the Instruction:** The code is a list of rules. It is **Complicated**.
- **They are looking at the Execution:** The running system is a chaotic web of interactions. It is **Complex**.

In the industry, we have moved from "fixing machines" (deterministic) to "healing systems" (probabilistic).

---

Would you be interested in hearing about the **Cynefin Framework** in more detail, as it provides a very useful vocabulary for exactly this kind of categorisation?

yes

The Cynefin framework (pronounced *ku-nev-in*) was developed by David Snowden in 1999 whilst at IBM Global Services. It is a Welsh word signifying "habitat" or "place of multiple belongings."

It is widely used in systems theory to do exactly what you are trying to do: distinguish between different types of problems so you know how to solve them.

Here are the five domains of the framework, and where your "watch vs. biology" analogy fits in.

### 1\. Clear (formerly Simple/Obvious)

- **Context:** "Known knowns." The relationship between cause and effect is obvious to everyone.
- **Approach:** Sense → Categorise → Respond.
- **Practice:** Best Practice.
- **Example:** Processing a standard invoice. If happens, do . You do not need an expert; you need a checklist.

### 2\. Complicated (The Domain of Experts)

- **Context:** "Known unknowns." Cause and effect exist, but they are separated by time or space. You cannot just "see" the answer; you have to analyse the data to find it.
- **Approach:** Sense → Analyse → Respond.
- **Practice:** Good Practice.
- **Example:****The Mechanical Watch.** As you correctly identified, this is the realm of the expert. A watchmaker can take the machine apart, analyse the gears, and predict exactly why it stopped. It is difficult, but solvable through reductionism (breaking it down into parts).

### 3\. Complex (The Domain of Emergence)

- **Context:** "Unknown unknowns." Cause and effect can only be perceived in retrospect. You cannot tease apart the variables because they are too intertwined. The output is emergent.
- **Approach:** Probe → Sense → Respond. You must conduct "safe-to-fail" experiments to see how the system reacts.
- **Practice:** Emergent Practice.
- **Example:****A Rainforest (or Modern Software).** You cannot predict exactly what will happen if you introduce a new species (or a new microservice). You have to try it, watch for patterns, and amplify the good results while dampening the bad ones.

### 4\. Chaotic (The Domain of Rapid Response)

- **Context:** No manageable cause-and-effect relationship. The house is on fire.
- **Approach:** Act → Sense → Respond. You do not analyse; you act immediately to stop the bleeding, then try to move the problem into the Complex domain.
- **Practice:** Novel Practice.
- **Example:** A major security breach or a server outage where data is being corrupted live.

### 5\. Confusion (Disorder)

- **Context:** The space in the middle. You do not know which domain you are in.
- **The Danger:** When in disorder, people retreat to their comfort zone. Bureaucrats demand more checklists (Clear), and engineers demand more analysis (Complicated), even if the problem is actually Complex.

---

### Why this validates your Semantic Clash

The frustration you feel often comes from **"The Cliff."**

In the Cynefin diagram, there is a boundary between **Clear** and **Chaotic** that is often represented as a cliff edge. If you treat a Complex system (like software users or a market) as if it were merely Clear or Complicated (rigid rules and predictions), you eventually fall off the cliff into Chaos when reality fails to match your rigid model.

Your intuition was spot on: treating software as merely "Complicated" ignores the emergent "Complex" reality of how it actually behaves in the wild.

Would you like to explore how "Technical Debt" fits into this, or perhaps how management styles differ between these domains?

Google Account

Leon Ormes

leonormes@gmail.com
