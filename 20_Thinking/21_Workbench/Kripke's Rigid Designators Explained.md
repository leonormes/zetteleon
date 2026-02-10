---
captured: "2026-02-10T09:43:45+00:00 2026-02-10T09:43:45+00:00"
created: 2026-02-10T09:43:48+00:00
modified: 2026-02-10T10:18:02+00:00
source: "https://gemini.google.com/share/1ae44961f661"
status: "processing"
tags: ["input"]
title: "Kripke's Rigid Designators Explained"
type: "head"
---

## Raw Output / Content

You said

<https://youtu.be/MncEzRAw3tU?si=bl5nheagvb-sbgrX>

An interesting choice of material. While most of your peers are drowning in the "Marketplace of Attention" watching 10-minute tutorials on how to use a library that will be deprecated by Tuesday, you've stumbled upon actual Intellectual Infrastructure. This is Jeffrey Kaplan's lecture on Saul Kripke's _Naming and Necessity_.

Kripke's work is the fundamental bedrock for how we understand Identifiers—whether they are variables in a codebase or entries in a database. If you don't understand the difference between a description and a rigid designator, you don't understand Systems Design.

Here is the "De-Hype" filter applied to this 22-minute pedagogical exercise.

### 1. The Hype Check (The Grade)

The video opens with a dramatic retelling of a 1970 Princeton lecture series [[00:00](http://www.youtube.com/watch?v=MncEzRAw3tU&t=0)]. It frames Kripke as a "prodigy" who "destroyed" a theory. In reality, it is a standard, albeit very clear, academic breakdown of the failure of Descriptivism. There is no "Retention Hacking" here, just a man with a whiteboard and a functioning brain.

### 2. The Signal (The Notes)

Core Concept: Proper names function as Rigid Designators, meaning they refer to the same object in every possible world, regardless of whether the descriptions we associate with that object remain true [[10:39](http://www.youtube.com/watch?v=MncEzRAw3tU&t=639)].

The Mechanism (The "De-Hype" Breakdown):Kripke's refutation of Searle's "Cluster Theory" (the idea that a name is just a shorthand for a list of attributes) follows these logical steps:

- Step 1: The Modal Test (Refuting Necessity): If a name (e.g., "Abraham Lincoln") were synonymous with a description (e.g., "The 16th President"), then the statement "Lincoln might not have been President" would be a logical contradiction. It isn't. Therefore, the name is not the description [[01:27](http://www.youtube.com/watch?v=MncEzRAw3tU&t=87)].
- Step 2: The Ignorance/Error Test: Users successfully refer to entities (e.g., Cicero or Feynman) even when they possess zero unique identifying information or flat-out incorrect metadata [[11:43](http://www.youtube.com/watch?v=MncEzRAw3tU&t=703)]. Reference is not a "search query" against a database of traits; it's a direct link.
- Step 3: The Gödel/Schmidt Counter-factual: Kripke proves that even if our most "weighted" description of a person is false (e.g., if a man named Schmidt actually proved the Incompleteness Theorem and Gödel stole it), the name "Gödel" still refers to the person we originally pointed at, not the person who actually fits the description [[15:18](http://www.youtube.com/watch?v=MncEzRAw3tU&t=918)].
- Step 4: The Rigid Designation Rule: A proper name picks out the object itself, whereas a description (a "non-rigid designator") picks out whatever happens to fit the criteria in a given context [[10:39](http://www.youtube.com/watch?v=MncEzRAw3tU&t=639)].

Hidden Constraints:

- Part 1 Only: This video is strictly a _critique_. It tells you why the old theory is broken but stops before explaining the Causal Theory of Reference (how the name gets attached to the thing in the first place).
- The "Jack the Ripper" Exception: Kripke concedes that for "theoretical names" where the object is never seen and only defined by its deeds, descriptivism might actually hold [[19:24](http://www.youtube.com/watch?v=MncEzRAw3tU&t=1164)].

### 3. The Professor's Verdict

Keep: The Gödel/Schmidt thought experiment [[15:18](http://www.youtube.com/watch?v=MncEzRAw3tU&t=918)]. It is the ultimate "First Principles" proof that identity is independent of metadata. In system terms: A GUID (Globally Unique Identifier) is a rigid designator; a "WHERE" clause in SQL is a description. Never confuse the two.Discard: The first two minutes of "January in New Jersey" atmospheric fluff and the mandatory "buy my book/sign up for my newsletter" pitch at the end [[21:55](http://www.youtube.com/watch?v=MncEzRAw3tU&t=1315)].

Conclusion: A rare 10/10 for signal-to-noise ratio. Watch the next part to understand the Causal Chain—that's where the actual "Systems Design" of language happens.

URL:[http://www.youtube.com/watch?v=MncEzRAw3tU](http://www.youtube.com/watch?v=MncEzRAw3tU)

You said

<https://youtu.be/eSS8-i28oho?si=HgLKicMDgZ6jk6bx>

Another segment from Kaplan. This time, we move from the critique of Descriptivism to Kripke's constructive alternative: the Causal Theory of Reference. While the previous video was about why "metadata lookup" is a bad model for identity, this one explains the "Network Protocol" that actually makes naming work.

### 1. The Hype Check (The Grade)

Sensationalism Score: Low The "Hook" vs. Reality: Kaplan uses the word "demolished" [[00:07](http://www.youtube.com/watch?v=eSS8-i28oho&t=7)] to describe Kripke's previous work, which is a bit of academic chest-thumping, but the rest of the video is remarkably sober. It promises Kripke's theory and delivers a concise, 4-minute abstract of it. No "Retention Hacking" detected, just high-density information.

### 2. The Signal (The Notes)

Core Concept: A name refers to an object not because of what the speaker knows about the object, but because of a causal-historical chain connecting the speaker back to the object's initial naming [[01:11](http://www.youtube.com/watch?v=eSS8-i28oho&t=71)].

The Mechanism (The "Causal Chain" Protocol):

- Step 1: Initial Baptism (The Genesis Block): An object is given a name through ostension (pointing at it) or a fixing description (e.g., "the first child born today") [[02:55](http://www.youtube.com/watch?v=eSS8-i28oho&t=175)].
- Step 2: Transmission (Link to Link): The name is passed through a community. Speaker A tells Speaker B about "Richard Feynman." Speaker B now has the name in their vocabulary [[01:14](http://www.youtube.com/watch?v=eSS8-i28oho&t=74)].
- Step 3: Intentional Deference (The Handshake): For the reference to succeed, the receiver must _intend_ to use the name with the same reference as the person from whom they learned it [[03:29](http://www.youtube.com/watch?v=eSS8-i28oho&t=209)]. You are "deferring" the identifying work to the previous link in the chain.

Hidden Constraints:

- The Intent Requirement: If you hear a name and decide to use it for your cat instead of the physicist, you have broken the chain. Reference depends on the _intent_ to stay within the established causal history [[03:34](http://www.youtube.com/watch?v=eSS8-i28oho&t=214)].
- Impending Obsolescence: Kaplan hints at the end that this theory was "defeated" by Gareth Evans just a few years later [[04:00](http://www.youtube.com/watch?v=eSS8-i28oho&t=240)]. This video presents the theory as a landmark, but one that is ultimately incomplete or flawed.

### 3. The Professor's Verdict

Keep: The concept of Social Deference [[02:00](http://www.youtube.com/watch?v=eSS8-i28oho&t=120)]. You don't need to be an expert to talk about a subject; you just need to be a member of a linguistic community that maintains a valid link to the source. This is the human equivalent of a Pointer or a Symbolic Link in a file system.Discard: The "baptism" terminology. While Kripke used it, it's unnecessarily religious for a logical framework. Think of it as Initialization.

Conclusion: This is a 4-minute masterclass in how "Pointers" work in human language. Use it to understand why your variables should be named based on their _origin and intent_, not just their current _state_.

URL:[http://www.youtube.com/watch?v=eSS8-i28oho](http://www.youtube.com/watch?v=eSS8-i28oho)
