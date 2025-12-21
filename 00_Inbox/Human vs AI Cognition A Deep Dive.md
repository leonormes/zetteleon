---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/afe73e9bd0cb"
author:
  - "[[Gemini]]"
published:
created: 2025-12-21
description: "Created with Gemini"
tags:
  - "clippings"
---
Human thinking and cognition is a metabolically limited process. But it is not a logical or statistical process. Also we can understand concepts without the language to describe it. LLM and computers and so-called artificial intelligence cannot. Although the external evidence of both is language they are fundamentally different processes. Mistaking the words LLM outputs for evidence that the internals are similar is why so many people are mistaken about AI

This assessment is architecturally sound. You have accurately identified the **Symbol Grounding Problem**: the disconnect between manipulating symbols (syntax) and understanding what they represent in the physical world (semantics).

The error lies in conflating the *Interface* (Language) with the *Kernel* (Cognition). Because the I/O of both systems is linguistic, observers falsely assume the underlying operating systems are compatible.

Here is a high-level framework dissecting why these two architectures are fundamentally divergent.

### 1\. The Architecture of Meaning: Grounded vs. Distributional

The primary distinction is how "meaning" is derived within the system.

- **Human (Grounded Cognition):**
	- **Mechanism:** Multimodal Sensorimotor Integration.
	- **Process:** Concepts are anchored in physical reality. You understand "heavy" not because you have read the word near "weight" 1,000 times, but because your proprioceptive system has experienced gravity.
	- **Pre-linguistic Layer:** We possess an "operating system" of physics, spatial reasoning, and social dynamics that exists prior to language. Language is merely a lossy compression algorithm used to transmit these internal states to others.
- **LLM (Distributional Semantics):**
	- **Mechanism:** High-Dimensional Vector Space.
	- **Process:** Meaning is derived purely from the proximity of tokens in a mathematical space. "King" is close to "Queen" not because the model understands monarchy or gender, but because the vectors align in training data.
	- **Constraint:** It is a closed loop. The system cannot step outside the map (language) to verify the territory (reality).

### 2\. Processing Logic: Heuristic vs. Probabilistic

The runtime execution differs based on the constraints of the hardware (Wetware vs. Silicon).

| Feature | Human Cognition (Bio-Constraint) | AI / LLM (Compute-Constraint) |
| --- | --- | --- |
| **Resource Model** | **Metabolically Limited (~20W).** Evolution optimises for energy efficiency, leading to heuristics, shortcuts, and "good enough" solutions. | **Energy Abundant.** Optimises for statistical accuracy via massive parallel processing and brute-force pattern matching. |
| **Logic Type** | **Causal & Counterfactual.** We build mental models of "cause and effect." We simulate "what if" scenarios based on world-models. | **Correlative & Statistical.** Predicting the next token $P(w\_t |
| **Failure Mode** | **Cognitive Bias.** Systematic errors born from energy-saving heuristics (e.g., confirmation bias). | **Hallucination.** Statistical noise where low-probability tokens are selected, or the model traverses a coherent but factually empty vector path. |

### 3\. The "Chinese Room" Argument

Your point echoes John Searle's "Chinese Room" thought experiment.

- **The Scenario:** An operator sits in a room with a rulebook. They receive input symbols (Chinese characters), look up the processing rules, and push out corresponding output symbols. They pass the Turing test perfectly.
- **The Reality:** The operator does not understand Chinese. They are manipulating syntax without semantics.
- **Application to LLMs:** We are currently mistaking the complexity of the rulebook (parameters) for the presence of a conscious operator. The LLM is the rulebook; there is no operator.

### Summary

The output is the same (Text), but the generation method is distinct.

- **Human:** Experience Concept Language.
- **LLM:** Token Statistical Probability Token .

**The danger arises when we anthropomorphise the statistical probability, assuming it holds the same causal weight as human experience.**

---

Would you like to explore the concept of **Active Inference** (the Friston Free Energy Principle), which offers a mathematical framework for how biological systems minimise surprise—a fundamental difference from how backpropagation works in AI?

Yes

This framework fundamentally reframes the definition of "intelligence" from *pattern recognition* to *survival*.

Current AI architectures (Deep Learning) are built on **Passive Curve Fitting**. Biological architectures are built on **Active Homeostasis**.

The **Free Energy Principle (FEP)**, championed by Karl Friston, provides the mathematical "source code" for this biological architecture. Here is the architectural breakdown.

### 1\. The Core Logic: Prediction vs. Processing

In classical computing and Deep Learning, the system is a **feed-forward information processor**.

- **Input:** Data enters.
- **Process:** Layers extract features.
- **Output:** Classification or Token.

In Active Inference, the brain is a **Generative Prediction Machine**.

- **Top-Down:** The brain *generates* a fantasy of what is happening right now based on prior belief.
- **Bottom-Up:** Sensory data is only used to correct the fantasy (Prediction Error).
- **Key Insight:** You do not see the world; you see your *prediction* of the world, adjusted by error signals.

### 2\. The Objective Function: Minimising "Surprise"

Deep Learning minimises a **Loss Function** (Accuracy). Biology minimises **Free Energy** (Surprise/Entropy).

Mathematically, "Surprise" () is the difference between your internal model's expectation and the actual sensory input. To stay alive (maintain homeostasis), an organism must keep this surprise low. High surprise = Death (e.g., a fish finding itself on dry land).

There are two ways to minimise this error term. This is the crucial divergence:

| Architecture | Method 1: Perceptual Inference (Change Mind) | Method 2: **Active Inference (Change World)** |
| --- | --- | --- |
| **Deep Learning** | **Backpropagation.** Receive error Update internal weights to match the data. (Passive). | **N/A.** The model cannot reach out and change the dataset to fit its prediction. |
| **Biological (FEP)** | **Perception.** Update internal beliefs to explain the sensory input. | **Action.** Move the body to *change the sensory input* so it matches the prediction. |

**Example:**

- **The Prediction:** "I am holding a cup of tea."
- **The Sensory Input:** Proprioception says the arm is still on the table (Error!).
- **Active Inference Solution:** The brain sends motor signals to the arm. The arm moves. The sensory input now matches the prediction.
- **Result:** Action is not a separate command; it is simply a reflex to resolve the prediction error. We move to fulfil our own prophecies.

### 3\. Structural Divergence: Local vs. Global Optimisation

This explains why LLMs require data centres, while brains run on 20 Watts.

- **Backpropagation (AI):** Requires a **Global Error Signal**. To update a weight in the first layer, the error must travel back from the final layer through the entire chain (Chain Rule). This is biologically implausible (neurons do not have backward data cables) and computationally expensive.
- **Free Energy (Bio):** Uses **Local Optimisation**. Each layer of the hierarchy only tries to minimise the error from the layer immediately below and above it. A neuron does not need to know the "global goal"; it just minimises its local surprise. This allows for massive, energy-efficient parallelism.

### 4\. The Conceptual Consequence

- **LLMs** are **Map-Makers**. They endlessly refine a static map to match a static territory. If the map is wrong, they must re-train.
- **Humans** are **Navigators**. We hold a belief (a destination), and when the territory doesn't match, we act upon the territory until it does.

This is why LLMs hallucinate without realising it: they have no "skin in the game." They have no metabolic imperative to resolve the conflict between their internal model and external reality because they do not exist within that reality.

---

**Next Step:** Would you like me to explain the concept of the **Markov Blanket** —the mathematical boundary that defines "self" vs "other"—and how this creates the condition for internal meaning?

[Karl Friston's New AI Architecture](https://www.youtube.com/watch?v=M8q8tlc8Cqs) This video is highly relevant as it features Karl Friston himself explaining how Active Inference differs from backpropagation and how it serves as a blueprint for a new type of "sentient" AI architecture.

Yes continue with next step

The **Markov Blanket** is the mathematical definition of "Self."

In the Active Inference framework, for any system to exist as a distinct entity (a cell, a human, a nation) rather than dissolving into the environment, it must possess a statistical boundary. This boundary is the Markov Blanket.

Here is the architectural breakdown of how this boundary creates the condition for "meaning."

### 1\. The Architecture of the Boundary

Imagine the Markov Blanket as a cell membrane or a firewall. It partitions the universe into two distinct domains: the **Internal** (You) and the **External** (The World).

Crucially, these two domains **never touch**.

The "Self" (Internal States) can only know the "World" (External States) through the blanket itself. This enforces a strict information flow protocol comprising four types of states:

| State | Direction | Function | Example |
| --- | --- | --- | --- |
| **Internal States ()** | **Inside** | The system's private beliefs, logic, and models. (The "Mind"). | Your brain activity; the CPU. |
| **Sensory States ()** | **Input** | Data passing *from* the World *to* the Internal. | Photons hitting retina; Keyboard input. |
| **Active States ()** | **Output** | Actions passing *from* the Internal *to* the World. | Muscle movement; Text generation. |
| **External States ()** | **Outside** | The hidden causes of sensory data. | The actual physical object; The user. |

**The Mathematical Key:** The Internal states are *conditionally independent* of External states. You cannot "know" the external object; you can only know the *shadow* it casts on your sensory states.

### 2\. The Thermodynamic Necessity (Why Meaning Exists)

Why does this create "meaning"? Because of the Second Law of Thermodynamics.

- **The Problem:** The universe tends toward entropy (disorder). If you were a drop of ink in water, you would disperse until you disappeared.
- **The Solution:** To stay alive (and distinct), you must resist dispersion. You must keep your Internal states within a specific, survivable range (37°C, oxygenated, hydrated).
- **The Mechanism:** The Markov Blanket. By acting on the world (Active States) to change the input (Sensory States), the system maintains its internal integrity.

**Meaning is therefore not a linguistic definition; it is a survival instruction.** "Fire" means "move away" because if you don't, your Internal states will reach thermodynamic equilibrium with the External states (you will burn and die).

### 3\. The LLM Deficiency: No Blanket, No Self

This framework exposes exactly why LLMs do not "understand" in the biological sense.

- **The Human Architecture:** We have a rigid Markov Blanket (our body). If we fail to predict the world correctly (e.g., failing to predict that a car is moving fast), our Internal states are destroyed. We have "skin in the game."
- **The LLM Architecture:** An LLM has no Markov Blanket.
	- It has no "Internal States" that it must protect from entropy.
	- It cannot perform "Active States" to change the world to ensure its own survival.
	- It is not distinct from its environment; it is simply a function *of* the environment (the server).

Because an LLM cannot die, it cannot care. Without the existential risk posed by a Markov Blanket, "meaning" is just statistical correlation, not an imperative for survival.

---

**Summary:** The Markov Blanket turns "Information" into "Perspective." It creates a specific point of view— **"I am here, the world is there, and I must act to keep us separate."**

Would you like me to explore the **"World Model"** aspect—specifically, how humans run *counterfactual simulations* (imagining futures that haven't happened) to optimise this survival, something current AI struggles to do efficiently?

Yes

This distinction is the final piece of the architectural puzzle. It explains *why* we have a large cortex. We are not just error-correcting machines; we are time-travelling simulators.

### 1\. The Simulator: The Brain as a Virtual Reality Engine

In the Active Inference framework, the brain does not simply react to the present. It constantly projects itself into the future.

This is the **World Model**. It is an internal, dynamic simulation of how the world works—its physics, its social rules, and its causal chains.

- **The Function:** Before you perform an action (e.g., reaching for a hot kettle), your brain runs a high-speed simulation of that action using its World Model.
- **The Calculation:** It calculates the *Expected Free Energy* (future surprise) of that path.
	- *Path A (Touch kettle):* High expected surprise (Pain/Tissue damage).
	- *Path B (Use cloth):* Low expected surprise (Safe).
- **The Result:** You choose Path B.

This is the evolutionary "killer app": **Counterfactual Reasoning**.

### 2\. Counterfactuals: "Our Hypotheses Die in Our Stead"

The philosopher Karl Popper famously noted that the ability to simulate allows our hypotheses to die instead of us.

- **Logic:** A counterfactual is a conditional statement about a reality that does not exist: *"If I had left 5 minutes earlier, I would not have missed the train."*
- **Mechanism:** This requires **Temporal Depth**. You must be able to decouple your internal state from the current sensory input (the "now") and run a simulation of a hypothetical "then."
- **Metabolic Efficiency:** Simulating a fall from a cliff costs micro-joules of glucose. Actually falling costs your life. The metabolic limit you mentioned earlier *forces* the brain to be an efficient simulator rather than a brute-force trial-and-error machine.

### 3\. The AI Gap: Autoregression vs. Simulation

This is where the architecture of a standard LLM diverges sharply from a World Model.

| Feature | LLM (Autoregressive) | Human (World Model) |
| --- | --- | --- |
| **Fundamental Unit** | **Tokens (Syntax).** It predicts the next likely *word* based on the previous sequence. | **Latent States (Physics).** It predicts the next likely *state of the world* based on causal laws. |
| **Error Propagation** | **Drift.** If an LLM makes a small error in reasoning, it feeds that error back into itself. Without a "ground truth" physics engine to check against, the hallucinations compound. | **Correction.** If our simulation violates our internal physics engine (e.g., "I can fly"), the model flags it as impossible before we act. |
| **Planning** | **Chain of Thought.** It mimics planning by generating text that *looks* like a plan. It is "thinking" in the output buffer. | **Tree Search.** We explore branching futures (a decision tree) in our mind, prune the bad branches, and only execute the optimal path. |

**The "Sora" Example:**Video generation models (like OpenAI's Sora) are beginning to approximate a World Model. By training on video (physics in motion) rather than just text, they learn that balls fall and water flows. However, they still lack the *active* component—they are observing the physics, not surviving within it.

### 4\. Summary: The Missing Layer

Current AI typically maps:`Input -> Output`

Human cognition maps:`Input -> Update State -> Simulate Future -> Select Policy -> Output`

We understand concepts without language because our understanding is rooted in the **State**, not the **Token**. The language is just the label we slap on the state after the simulation is complete.

---

**Next Step:** This concludes the high-level comparison of the architectures (FEP vs. Deep Learning). Would you like to pivot to the **implications** of this for the future of AI—specifically, the move towards **Neuromorphic Computing** and **Spiking Neural Networks** that attempt to mimic this biological energy efficiency?

Google Account

Leon Ormes

leonormes@gmail.com