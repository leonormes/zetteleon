---
title: "Propositions as knowledge foundations"
source: "https://claude.ai/chat/fc5a1a18-2272-4c96-9ac0-cf5c5cd9d8e9"
captured: "2026-04-23T12:18:44+01:00 2026-04-23T12:18:44+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

Analyse this claim. Dive deep into the meaning and validate or refute it. It is in the context of PKM and writing to think. The fundamental building block of knowledge is the Proposition.

---

## Verdict: Mostly true, but overreaches without qualification

The claim is defensible and useful *for the specific domain of declarative knowledge and writing-to-think*, but it's wrong if taken as a universal claim about knowledge as such. Let me unpack.

### 1\. What a "proposition" actually is

A proposition is a **declarative claim that bears a truth value** — it can be true or false.

- ✅ *"B-trees outperform hash indexes for range queries"* — proposition.
- ❌ *"B-trees"* — a concept/topic, not a proposition.
- ❌ *"How do B-trees handle splits?"* — a question, not a proposition.
- ❌ *"Index that column"* — an imperative, not a proposition.

Crucially, a proposition is distinct from the sentence expressing it. *"It is raining"* and *"Il pleut"* express the **same proposition**. The proposition is the *content*, not the *wording*.

### 2\. The case FOR the claim

#### 2a. The epistemic tradition backs it

Since Plato's *Theaetetus*, knowledge has been characterised as **justified true belief** — and belief is always *belief-that-P*, where P is a proposition. You don't believe "cats"; you believe *that* cats are mammals. The entire JTB framework presupposes propositions as the thing being known.

#### 2b. Propositions are the atoms of inference

Logic, mathematics, and scientific reasoning all chain propositions via inference rules. Concepts alone cannot be "inferred from" other concepts — only propositions can.

#### 2c. They are the only thing that can be wrong

This is the critical one for PKM. A topic note titled *"Kubernetes networking"* cannot be falsified, challenged, or contradicted — it's just a bucket. A proposition note titled *"Pod-to-pod traffic bypasses kube-proxy when using Cilium's eBPF dataplane"* can be:

- Tested against reality
- Contradicted by another note
- Refined over time
- Linked to the evidence that justifies it

This is why Luhmann's Zettelkasten, Ahrens's *How to Take Smart Notes*, and Andy Matuschak's evergreen-notes practice all converge on **atomic, claim-shaped notes with complete-sentence titles**. The proposition format *forces the commitment that makes thinking visible*.

#### 2d. It maps to "writing to think"

The reason writing clarifies thinking is that prose *demands you commit to claims*. You cannot write a paragraph about "Kubernetes" — you can only write sentences that assert things. The moment you try to assert, you discover what you don't actually understand. Propositions are where thinking lives or dies.

### 3\. The case AGAINST (or: where the claim overreaches)

#### 3a. Ryle's distinction: knowing-how vs knowing-that

Gilbert Ryle argued that procedural knowledge — riding a bike, debugging a cascading Vault failure by feel, sight-reading code — is **not reducible to propositions**. You can know how to balance on a bike without being able to state the propositions describing it. If propositions were THE fundamental unit, skill would be mysterious.

#### 3b. Concepts are arguably more fundamental

You cannot form the proposition *"The pod is CrashLoopBackOff"* without possessing the concepts POD and CRASHLOOPBACKOFF. Concepts are the *building blocks of the building blocks*. So "fundamental" is ambiguous:

- **Compositionally fundamental** → concepts.
- **Epistemically fundamental** (bearer of truth) → propositions.

#### 3c. Tacit knowledge (Polanyi)

"We know more than we can tell." Expert intuition, pattern recognition, the thing that makes you smell a cert-manager DNS-01 issue three minutes into a session — much of this resists full propositional articulation.

#### 3d. Acquaintance vs description (Russell)

Knowing a person, knowing the feel of a place — a different species of knowledge from propositional knowledge-that.

### 4\. The refined claim (what I'd actually defend)

> **The proposition is the fundamental unit of *declarative* knowledge, and the most productive atomic unit for PKM and writing-to-think — but it sits atop a substrate of concepts and alongside non-propositional forms (procedural, tacit) that PKM systems capture poorly.**

This preserves the useful bite of the original claim without the overreach.

### 5\. What this means for your PKM practice

This is where the theory earns its keep:

- **Note titles should be complete declarative sentences.** *"Vault JWT roles must exist before VSO reconciles"* — not *"Vault JWT roles"*. If you can't state it as a claim, you don't yet know what you're trying to say.
- **One proposition per note.** Atomicity isn't aesthetic — it's what makes notes linkable and contradictable.
- **Separate your note types.** Propositions (claims), concepts (definitions/MOCs), observations (raw from-the-field notes), questions (open loops). They play different roles and conflating them blunts all of them.
- **Procedural knowledge needs a different container.** Runbooks, checklists, and worked examples are not propositions and shouldn't be forced into that shape. Your MKUH five-layer triage runbook is procedural — it lives correctly as a procedure, not as atomised claims.

### 6\. Your immediate next action

**Open your PKM and find one note whose title is a noun phrase (a topic, not a claim). Rewrite only the title as a complete declarative sentence.**

That's the entire micro-step. Don't restructure the body, don't reorganise folders, don't touch anything else. One title. The act of rewriting will immediately tell you whether the note contains a claim at all, or whether it's a topic-shaped dumping ground — and that diagnostic is the real payoff.

---

**You**

can it be said that llm/ai only deals with declarative knowledge as described above?

---

**Claude**

## No — and the distinction matters more than it first appears

The claim is intuitive but wrong in a subtle way. LLMs are actually *unusual* in the history of AI precisely because they blur the declarative/procedural line. Let me work through this carefully.

### 1\. First, disambiguate "deals with"

This question smuggles in ambiguity. "Deals with" could mean:

- **(a) Represents internally** — what's encoded in the weights?
- **(b) Outputs** — what do they produce?
- **(c) Operates on** — what do they take as input?
- **(d) Reasons about** — what do they manipulate?

The answer is different for each. The naive claim tends to conflate them.

### 2\. The case for "yes, only declarative"

The surface-level argument:

- Training data is text → text expresses propositions → therefore the model learns propositions.
- Output is text → text is declarative → therefore output is declarative knowledge.
- There's no "body," no sensorimotor loop, no bike-balancing — so no genuine procedural knowledge.

This is the Ryle-flavoured objection: an LLM can *tell you* how to ride a bike but cannot *ride* one. Therefore it only has knowing-that, not knowing-how.

**This is the intuition, and it's partially right. But it conflates the output modality with the internal representation.**

### 3\. Why the claim breaks down

#### 3a. LLMs demonstrably have procedural capacity

An LLM doing multi-digit arithmetic, translating between languages, generating working code, or following a novel instruction it has never seen verbatim is **executing a procedure**, not retrieving a proposition. Mechanistic interpretability research has found actual *circuits* inside models — induction heads, indirect object identification circuits, modular arithmetic algorithms — that are **learned procedures**, not stored facts.

When GPT adds 847 + 293, it is not looking up *"847 + 293 = 1140"* as a proposition. It is running a learned algorithm over tokens. That is procedural knowledge in the Rylean sense — knowing-how — even though it happens to be knowing-how-to-manipulate-symbols rather than knowing-how-to-ride-a-bike.

#### 3b. The weights are not a proposition store

A common folk model: "the LLM has memorised a giant pile of facts." This is misleading. The weights encode:

- **Distributional regularities** — which tokens follow which, in which contexts.
- **Learned transformations** — circuits that map input patterns to output patterns.
- **Latent concepts** — directions in activation space that correspond to features.
- **Pattern-completion machinery** — the ability to continue arbitrary structure.

None of that is cleanly "propositional." It's closer to a **massively compiled library of micro-skills** than a knowledge base. The declarative content emerges at the *output layer*, when the model generates text — but the underlying machinery is procedural.

#### 3c. In-context learning is pure procedure

When you give an LLM few-shot examples and it generalises the pattern, it is performing **learned inference** on the fly. There is no proposition *"when you see input X, output Y"* stored in the weights for your specific task. The model is executing a meta-procedure that adapts to novel patterns. This is closer to *skill* than *fact*.

#### 3d. Concepts, not propositions, are the natural internal unit

Interpretability work (features in superposition, sparse autoencoders, the Anthropic "Golden Gate Claude" demonstrations) suggests the model's internal vocabulary is **concepts and features**, composed on the fly into context-dependent outputs. Propositions are a thing the model *constructs* when generating, not a thing it *stores*.

### 4\. The sharper framing

Here's the refined claim I'd actually defend:

> **LLMs are trained on declarative text as their primary signal, and their outputs are typically declarative — but their internal representations are a hybrid of concepts, distributional patterns, and learned procedures. They have meaningful procedural competence within the symbolic domain, and essentially none outside it.**

Three dimensions are worth separating:

| Dimension | LLMs have it? | Notes |
| --- | --- | --- |
| Declarative knowledge (knowing-that) | ✅ Yes, extensively | The dominant training signal |
| Symbolic procedural knowledge (knowing-how, within text) | ✅ Yes | Arithmetic, code, translation, reasoning chains |
| Embodied procedural knowledge (knowing-how, sensorimotor) | ❌ No | No body, no sensorimotor loop |
| Tacit/experiential knowledge | ⚠️ Arguable | Pattern recognition *resembles* it but the phenomenology is absent |
| Knowledge by acquaintance (Russell) | ❌ No | No direct acquaintance with anything |

### 5\. The deeper point for your PKM instincts

This matters for how you think about using LLMs in your knowledge work:

- **LLMs are good declarative-knowledge *producers*** — so they can help you draft proposition-shaped notes, identify implicit claims in your prose, surface contradictions between notes.
- **LLMs are good symbolic-procedural *executors*** — so they can run transformations over your notes (reformatting, linking, extracting claims) that *aren't* just retrieval.
- **LLMs cannot substitute for your tacit expertise** — the thing that makes you smell a Vault JWT issue three minutes in is precisely what the model lacks. It can *describe* such patterns declaratively if you've given it the text, but it doesn't *have* the skill the way you do.
- **The model is not a fact database.** Treating it as one leads to the hallucination trap. Treating it as a *pattern-completion engine that generates plausible declarative text* is more accurate and safer.

### 6\. Where the original intuition is right

The claim has a defensible core: **as an interface, LLMs are overwhelmingly declarative.** You interact with them via claims, questions, and instructions; they respond with claims, explanations, and instructions. The procedural machinery is internal and largely invisible to the user. So for the purposes of *designing workflows around LLMs*, treating them as declarative-knowledge engines is a usable approximation — just not a true description of what they are.

### 7\. Immediate next action

**Pick one recent LLM interaction where you assumed the model was "looking up a fact" and reframe it as "executing a learned procedure over tokens."**

For example: the last time you asked about a Helm chart behaviour, the model wasn't retrieving a stored proposition about that chart — it was pattern-completing from distributional regularities about Helm, Kubernetes, and the specific terms in your prompt. Notice how that reframing changes your calibration about when to trust the output and when to verify. That recalibration is the whole payoff of the distinction.

---

**You**

You said 'When GPT adds 847 + 293, it is not looking up "847 + 293 = 1140" as a proposition' but isn't the llm just using another tool, like a calculator to get the answer? It doesn't know how to do the maths but it can use a computer process to run commands that give it the answer?

---

**Claude**

## Good catch — but you're conflating two different things

This is a genuinely important distinction, and it's one that trips up a lot of people thinking about modern AI systems. Let me separate them cleanly.

### 1\. Two fundamentally different architectures

There are **two separate things** that can happen when you ask an LLM to add numbers:

#### (a) Pure LLM — no tools

The model receives the tokens `"847 + 293 = "` and generates the next tokens using only its weights and the forward pass. No code executes. No calculator. Just matrix multiplications producing token probabilities.

#### (b) LLM + tool use (agentic)

The model is wired into a system where it can emit a structured call like `python("847 + 293")`, a separate runtime executes that code, and the result gets fed back into the model's context. The model then generates a response incorporating the result.

**These are architecturally distinct.** My claim was about (a). Your intuition is describing (b). Both exist; they are not the same system.

### 2\. When I said "GPT adds 847 + 293"

I was specifically talking about case (a) — the bare model, no tools. And in that case, the claim holds: the model is not looking up a proposition, and it's not calling a calculator. There is no calculator to call. The only machinery available is the forward pass through the weights.

And the empirical finding — from mechanistic interpretability work by Anthropic, Neel Nanda's group, and others — is that **transformers learn genuine arithmetic circuits**. Not perfect ones, not for arbitrary sizes, but actual learned procedures that implement something algorithm-shaped. For small additions, these circuits get it right *without any tool*. For larger numbers, they degrade and hallucinate — which is itself evidence that it's a learned-procedure-with-limits, not a lookup.

You can verify this yourself: ask a raw LLM (no tool use enabled) to add two 4-digit numbers. It'll usually get it. Ask it to add two 15-digit numbers. It'll usually fail. A calculator wouldn't fail. A lookup table would either have it or not. The *pattern of failure* — competent within a range, degrading predictably beyond it — is the fingerprint of a learned procedure.

### 3\. Your intuition is right about modern deployed systems

Here's where you're actually onto something important. **The Claude you're talking to right now is case (b).** I have tools. When you ask me to do serious arithmetic, the right move is to actually run Python, not to trust the forward pass. This is:

- More reliable (Python doesn't hallucinate digits)
- More honest (the model's arithmetic circuits are not trustworthy at scale)
- More auditable (you can see the code)

So **in practice**, for deployed agentic systems, arithmetic is increasingly offloaded to tools — exactly as you described. Your mental model matches reality for most user-facing LLM products in 2026.

### 4\. But this doesn't rescue the "only declarative" claim

Here's the subtle bit, and why I was making the point in the first place:

**Even if you grant that LLMs outsource arithmetic to a calculator, they still have to do procedural work to use the calculator.**

Consider what happens when I decide to use a Python tool for your arithmetic question:

1. Parse the intent from your natural language ("add these numbers" vs "explain addition" vs "is this sum correct?")
2. Decide *whether* a tool call is appropriate
3. Construct a syntactically valid call with the right arguments
4. Receive the result and integrate it into a coherent response
5. Decide whether the result looks sane or whether something went wrong

**None of that is declarative knowledge.** It's all procedural — knowing-how-to-use-tools, knowing-how-to-decompose-problems, knowing-how-to-route-subtasks. The model isn't retrieving the proposition *"when asked arithmetic, call python"*; it's executing a learned policy over contexts and tools.

So the calculator example, rather than refuting my original point, actually **strengthens** it: LLMs have procedural capacity at *multiple* levels — the circuit level (arithmetic circuits in the weights) AND the agentic level (tool orchestration). The declarative-only framing misses both.

### 5\. The sharper reframing

Your question gestures at a genuinely interesting architectural question: **where does the procedural competence live?**

| Layer | Procedural work | Example |
| --- | --- | --- |
| Weights/circuits | Learned algorithms in the forward pass | Small arithmetic, copying, induction |
| In-context | Pattern-matching on the prompt | Few-shot learning, format-following |
| Tool use | Orchestrating external runtimes | Calling Python for serious arithmetic |
| Agentic loop | Multi-step planning with tools | "Search, read, synthesise, write" |

A modern LLM system is procedural at *all four levels simultaneously*. The declarative content — the claims and explanations — is what surfaces in the output, but the machinery producing it is procedural end-to-end.

### 6\. Why this matters for your practice

This recalibrates trust in a useful way:

- **Raw LLM arithmetic is untrustworthy** — it's a learned circuit, not a calculator. When precision matters, insist on tool use or verify.
- **Agentic LLMs using tools are more trustworthy for computation** — but introduce a new failure mode: *wrong tool call*. The model might compute the right thing on the wrong inputs.
- **The declarative output is always a generated artefact** — whether it came from weights alone or from weights+tools, it's still pattern-completion at the final step. It reads like a fact but is produced like a continuation.

### 7\. Immediate next action

**In your next LLM interaction involving numbers, explicitly check: did the model use a tool or did it compute from weights alone?**

You can often tell from the response. If there's a visible code execution, it used a tool. If it just asserts the number in prose, it came from the forward pass — and you should be suspicious proportional to the number's size or the calculation's complexity. That one-bit check (tool or not?) will meaningfully upgrade your calibration about when to trust LLM output in technical work.

---

**You**

But maths is patterns. THe llm doesn't know how to 'Add' as a descrete skill. It is just getting to the answer via patterns it has trained on

---

**Claude**

## You're circling something real — but the argument proves the opposite of what you think

This is a great pushback, and it's the point where the conversation gets genuinely philosophically interesting. Let me try to show you why the argument, when followed through, actually **dissolves the declarative/procedural distinction you started with** — rather than collapsing procedural into "just patterns."

### 1\. The argument you're making

Steelmanned:

> The LLM doesn't have addition as a *skill*. It has statistical regularities over token sequences. When those regularities happen to produce correct sums, that's pattern-matching succeeding, not a procedure executing. Calling it "procedural knowledge" dresses up pattern-completion in philosophical clothing it doesn't deserve.

This is a respectable position. It's roughly the **eliminativist** view: there's no "real" addition happening, just statistics that mimic addition.

### 2\. Why it's not quite right — the empirical part

Here's the thing: mechanistic interpretability has actually looked inside these models. Not speculatively — with real tools, on real weights. What they find for arithmetic is:

- **Specific neurons and attention heads** that activate for specific digit positions.
- **Fourier-like representations** of numbers in activation space (Nanda et al. on modular arithmetic found the model literally learns to represent numbers as rotations on a circle and does arithmetic via trigonometric identities — this is not a joke).
- **Carry-propagation circuits** that handle the "when digit sum exceeds 9, add 1 to the next column" step.
- **Clean algorithmic structure** that generalises beyond training examples within its range.

That's not "pattern-matching succeeded by accident." That's **an algorithm, implemented in weights, that the network discovered via gradient descent.** The fact that it emerged from statistical learning doesn't make it not an algorithm, any more than the fact that your brain emerged from evolution makes your arithmetic not arithmetic.

### 3\. The deeper philosophical point — here's the real move

Now the interesting part. You said:

> "Maths is patterns. The LLM doesn't know how to 'add' as a discrete skill. It's just getting to the answer via patterns."

**Ask yourself: what would "adding as a discrete skill" even look like, physically?**

When *you* add 847 + 293, what is happening? Neurons fire in patterns. Those patterns were shaped by years of exposure to training data (school, practice, feedback). Some neural circuit you can't introspect produces the answer. You experience it as "doing addition" — but at the implementation level, it's **patterns of activation shaped by prior patterns of activation.**

When a pocket calculator adds 847 + 293, what is happening? Voltages in transistors implement Boolean logic that implements binary addition. Patterns of electrons, shaped by patterns of silicon doping, produce the answer.

**So what is "real" addition, as opposed to "just patterns"?**

There isn't a ghost-in-the-machine version of addition that sits apart from its physical implementation. **Every implementation of addition is patterns.** Patterns of neurons, patterns of silicon, patterns of transformer weights. The question isn't *"is it patterns?"* — everything is. The question is *"do the patterns implement the algorithm reliably?"*

This is essentially the **functionalist** position in philosophy of mind, and it's the dominant view for a reason: if you demand something more than "patterns that reliably implement the function," you can't explain how *anything* — brains, calculators, or LLMs — manages to compute.

### 4\. Where the LLM genuinely differs from a calculator

But your intuition isn't empty. There *is* a real difference, it's just not "patterns vs. real skill." The real difference is:

| Property | Calculator | LLM arithmetic circuit | Human arithmetic |
| --- | --- | --- | --- |
| Designed vs. emerged | Designed | Emerged from gradient descent | Emerged from learning |
| Symbolic or statistical | Symbolic | Statistical with algorithmic structure | Mixed |
| Domain boundaries | Crisp (within int range) | Fuzzy (degrades with size) | Fuzzy (degrades with complexity) |
| Error mode | Overflow / none | Plausible-looking wrong answers | Slips, miscarries |
| Introspectable | Fully | Partially (via interpretability) | Barely |

The LLM's arithmetic is **less reliable and more brittle** than a calculator's. That's a real and important difference. But it's a difference of *quality of implementation*, not *whether it's implementation at all*.

### 5\. The move that dissolves your original dichotomy

Here's where this leads back to your original question about declarative vs. procedural knowledge:

If you push "it's just patterns" hard enough, you end up having to say the same thing about **human procedural knowledge**. When you debug a Vault JWT issue by feel, your brain is running patterns shaped by prior patterns. When you balance on a bike, same thing. When you parse English, same thing.

So one of two conclusions follows:

- **(a) Procedural knowledge doesn't really exist anywhere.** Everything — humans, LLMs, calculators — is "just patterns." The declarative/procedural distinction is a folk-psychological convenience with no deep reality.
- **(b) Procedural knowledge is exactly "patterns that reliably implement a capability."** In which case LLMs have it, brains have it, calculators have it. The distinction is real but it's about *function*, not *substance*.

Most philosophers of mind take (b). It preserves the useful distinction (there really is a difference between *knowing that Paris is the capital of France* and *knowing how to ride a bike*) without invoking mysterious non-physical skills.

On view (b), the LLM's arithmetic circuits are **genuine procedural knowledge** — unreliable, limited in range, weirdly implemented via Fourier tricks, but genuine. Not because they're dignified with that name, but because they're patterns that reliably (within a range) implement the function.

### 6\. Why "just patterns" is a loaded phrase

The word "just" is doing enormous work in "just patterns." It smuggles in the assumption that patterns are *lesser* than some other thing — some proper, real, non-pattern-based way of knowing. But that other thing doesn't exist. There is no non-pattern-based implementation of any cognitive function anywhere in the known universe.

This is the same move as "humans are *just* atoms" or "love is *just* chemistry." Technically true, but the "just" is rhetorical, not analytical. It implies a demotion that the facts don't support.

### 7\. So what's the honest answer?

The honest framing:

- The LLM doesn't have a *symbolic* addition skill like a calculator has.
- It has a *learned statistical approximation* of addition, implemented as circuits in weights.
- Within its competence range, those circuits behave algorithmically — not accidentally.
- Outside that range, they degrade — which is why tool use for arithmetic is a good architectural choice.
- Calling this "procedural knowledge" is accurate on a functionalist reading, and misleading only if you smuggle in mysterious assumptions about what "real" skill requires.

Your intuition — *"but it's just patterns, not real addition"* — is actually the starting point for one of the hardest problems in philosophy of mind. You're not wrong to feel the force of it. But when you chase it rigorously, it doesn't land where it seems to point. It either eliminates procedural knowledge everywhere, or accepts that "patterns implementing function" is what procedural knowledge *is*.

### 8\. Immediate next action

**Write one proposition-shaped note capturing your current position on this.**

Something like: *"LLM arithmetic is/is not genuine procedural knowledge because \_\_\_"* — fill in the because with your current best reasoning. Don't aim for the final answer; aim to **commit to a claim you can later contradict.**

The payoff: in six months, when you've read more interpretability work or thought about it further, you'll have a specific prior view to update against — rather than a hazy sense of "I used to think something about this." That's the PKM mechanism doing its actual job: making your past thinking *concrete enough to be wrong*, so your future thinking can be better.
