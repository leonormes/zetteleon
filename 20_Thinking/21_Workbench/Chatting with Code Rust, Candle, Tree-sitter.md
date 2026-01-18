---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/920e8b8fbc22"
captured: "2026-01-18T08:19:14+00:00 2026-01-18T08:19:14+00:00"
status: "phase-1"
tags:
  - "input"
type: "head"
---
## Phase 1: Ingestion (The Stream)

> [!abstract] Context
> Created with Gemini

### Raw Output / Content
Https://youtube.com/watch?v=1PFiz-X8Bjs&si=Ox1Mr1XvpFEt6RY9

This video, titled **"Chat with your codebase with Candle and Tree-sitter"**, features a presentation by **Pratim Bhosale** at J On The Beach 2025. She explains how to build a custom tool to interact with your codebase using Rust and several machine learning concepts.

### Core Concepts and Workflow

The talk focuses on the "back end" logic of AI coding assistants, moving beyond the user interface to explain how code is indexed and queried.

- **Building Blocks**: The process involves several key stages: indexing, vector search, **HyDE** (Hypothetical Document Embeddings), and reranking \[[06:43](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=403)\].
- **The Workflow**:
	1. The user provides a query in plain English.
	2. The system creates a "hypothetical" piece of code that might answer the query (HyDE).
	3. This is converted into a vector and matched against the actual indexed codebase using **Approximate Nearest Neighbour (ANN)** search \[[23:54](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=1434)\].
	4. The results are reranked for precision before being sent to a Large Language Model (LLM) to generate the final answer \[[16:42](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=1002)\].

### Key Technologies Used

- **Rust and Cargo**: Chosen for performance, portability, and a more reliable package management system compared to Python's pip \[[12:41](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=761)\].
- **Candle**: A minimalist machine learning framework for Rust developed by Hugging Face, used to handle embeddings and model operations locally \[[25:46](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=1546)\].
- **Tree-sitter**: Used for parsing code grammar and building an **Abstract Syntax Tree (AST)**. This allows the tool to "understand" the structure of the code, such as functions and variables, rather than just treating it as plain text \[[19:08](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=1148)\].

### Why Build a Local Tool?

Pratim discusses the "economics" of AI tools, suggesting that while LLM calls are getting cheaper for companies, high-precision vector search on the cloud can be expensive. By building a local tool, developers can:

- Maintain privacy for proprietary code \[[12:20](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=740)\].
- Avoid usage limits and costs associated with cloud-based AI IDEs \[[11:52](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=712)\].
- Customise the tool to provide direct references to specific lines of code \[[29:32](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=1772)\].

### Demo and Limitations

The speaker demonstrates a CLI tool that indexes a Rust project and answers questions like "How does reranking work in this code?" \[[04:46](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=286)\]. Currently, the implementation is limited to parsing Rust files and does not function as a full "agent" with memory of previous questions \[[30:48](http://www.youtube.com/watch?v=1PFiz-X8Bjs&t=1848)\].

**Watch the full video here:**[https://youtube.com/watch?v=1PFiz-X8Bjs](https://youtube.com/watch?v=1PFiz-X8Bjs)

This still leaves us unsure what it means for a LLM to understand a code base. I could understand a code base but have the perspective all wrong and not very utilitarian. I could understand the code in an oop way but be missing the data oriented design benefits. Is I only understood the code from a js perspective and had no grasp of types I would produce poor quality code. What is the most utilitarian way for an llm too understand the code

It is a brilliant observation. "Understanding" for an LLM is not a conscious grasp of intent; it is a statistical mapping of tokens. If you feed an LLM a codebase without a "philosophical anchor," it will likely default to the most common patterns in its training data (usually Java-style OOP or standard React/JS patterns).

To make an LLM's understanding **utilitarian** —meaning it actually helps you build the right thing in the right way—it needs to move beyond raw text.

### The "Utilitarian" Stack: Hybrid Understanding

For an LLM to truly "understand" a codebase in a way that respects your design choices (like Data-Oriented Design vs OOP), it requires a three-layered approach:

#### 1\. Structural Understanding (The "Map")

An LLM needs to know the "geography" of your code. Instead of just reading files as flat text, the most utilitarian systems use **Tree-sitter** or **AST (Abstract Syntax Tree)** parsers.

- **Why it's utilitarian:** It allows the LLM to see "This is a `struct`, this is a `method`, and this `struct` is passed into that `function`."
- **The benefit:** It prevents the LLM from hallucinating relationships. It knows exactly where a variable is defined and where it is used.

#### 2\. Semantic Understanding (The "Vibe")

This is achieved through **Vector Embeddings**. The LLM converts code snippets into high-dimensional vectors.

- **Why it's utilitarian:** If you ask "How does the player take damage?", it doesn't need to find the word "damage." It finds code related to "health reduction," "hit points," or "collision events" because they are semantically similar.

#### 3\. Contextual/Philosophical Understanding (The "Rules")

This is the part you are worried about: the **Lens**. To stop an LLM from applying JS logic to a Rust codebase or OOP logic to a Data-Oriented system, you must provide a **Meta-Context**.

- **Project Rules (`.clinerules` or `CONTRIBUTING.md`):** High-end AI tools now look for specific files that define the "vibe" of the repo.
- **The "Architect" Prompt:** You must explicitly tell the LLM: *"This project follows Data-Oriented Design. Do not encapsulate state within objects; keep data in flat arrays and use systems to process them."*

---

### How to Force "Utilitarian" Understanding

If you want to ensure the LLM doesn't produce "poor quality code" due to a lack of perspective, you should adopt these practices:

| Feature | How to implement |
| --- | --- |
| **Type Safety** | Always include the `tsconfig.json` or `.env` files in the context so the LLM understands the constraints. |
| **Design Patterns** | Create a `DOCS/ARCHITECTURE.md` file. LLMs prioritize files that look like documentation. |
| **Data Layout** | If using DOD, provide a snippet of your most critical data structures and tell the LLM, "Follow this pattern." |

### The "Perspective" Problem

The most utilitarian way for an LLM to understand code is **Contextual Grounding**. Without a high-level summary of *why* the code is written that way (e.g., "We prioritised cache locality over abstraction"), the LLM will default to "clean code" clichés that might actually degrade your performance or architecture.

[Venkat Subramaniam on OOP vs Data Oriented Programming](https://www.youtube.com/watch?v=q-wLJjEbxyg)

This presentation is highly relevant because it explains the fundamental shift in thinking required when moving between OOP and Data-Oriented paradigms—the exact "perspective" shift you are concerned the LLM might miss.

**Would you like me to help you draft a "System Prompt" or an `ARCHITECTURE.md` file that defines your project's design philosophy for your AI tools?**

Extract the key points from the video you just suggested

In the video **"OOP vs Data Oriented Programming: Which One to Choose?"**, Venkat Subramaniam explores the fundamental differences between these two paradigms and provides a framework for deciding when to use each.

### The Role of Object-Oriented Programming (OOP)

- **Polymorphism as the Star**: Venkat identifies polymorphism as the most critical pillar of OOP because it provides extensibility. It allows a system to handle new types of data without modifying existing code, adhering to the **Open-Closed Principle** \[[03:23](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=203)\].
- **Effective Use Cases**: OOP excels when you have full control over a class hierarchy and want to define behaviour within those classes (e.g., an order processor that can handle various payment methods like credit cards or bank transfers) \[[10:10](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=610)\].

### The Pitfalls of Over-Applying OOP

- **The Problem of Parallel Hierarchies**: When adding new functionality (like auditing) to third-party classes you cannot modify, OOP often leads to "parallel hierarchies" where you create an auditor class for every data class \[[34:36](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=2076)\].
- **Increased Cognitive Load**: This approach can lead to overly complex code where the actual business logic is hidden behind multiple layers of design patterns (e.g., Factory or Visitor patterns) \[[36:56](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=2216)\].
- **Runtime Risks**: Using OOP hierarchies for external data can result in runtime errors if a new data type is introduced but the corresponding auditor class hasn't been created yet \[[35:50](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=2150)\].

### The Data-Oriented Programming (DOP) Alternative

- **Simplicity and Conciseness**: DOP prioritises the data itself over the "objects" containing it. It uses modern language features like **Sealed Interfaces** and **Pattern Matching** to handle data types directly in a single location \[[44:05](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=2645)\].
- **Compile-Time Safety**: By using sealed interfaces—which explicitly list all allowed implementations—the compiler can verify that your logic handles every possible case. If a new type is added, the code will fail to compile until you address it, preventing production errors \[[48:51](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=2931)\].
- **Records and Destructuring**: Venkat demonstrates using **Records** to treat data as transparent, immutable containers. This allows for "destructuring," making the code much more concise and easier for a human (or a business analyst) to read \[[53:47](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=3227)\].

### The Verdict: How to Choose

- **No "One-Size-Fits-All"**: Venkat argues that developers shouldn't be dogmatic. The most utilitarian approach is to use both paradigms depending on the context \[[58:41](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=3521)\].
- **Decision Matrix**:
	- **Choose OOP** when you own the hierarchy and want to encapsulate behaviour within objects.
	- **Choose DOP** when you are processing data from a hierarchy you don't control, or when simplicity and compile-time exhaustiveness are more important than absolute extensibility \[[59:19](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=3559)\].
- **Prioritise Low Cognitive Load**: Ultimately, the best choice is the one that reduces complexity and makes the code's intent most obvious to those reading it \[[40:54](http://www.youtube.com/watch?v=q-wLJjEbxyg&t=2454)\].

**Watch the full presentation here:**[https://www.youtube.com/watch?v=q-wLJjEbxyg](https://www.youtube.com/watch?v=q-wLJjEbxyg)

What tools are workflows are sota in LLM research into analysing a code base to produce reusable context for LLM

In the current 2026 landscape, the state-of-the-art (SOTA) has shifted from simple "Vector Retrieval" (finding similar text) to **Structured Contextualisation**.

The goal is no longer just to give the LLM code snippets, but to provide it with a **Mental Model** of the system. Here are the leading tools and workflows used in LLM research and high-end engineering to produce reusable, utilitarian context.

---

### 1\. The "Repository Intelligence Graph" (RIG)

The most recent SOTA research (early 2026) has introduced the **RIG**. Unlike a simple index, a RIG is a deterministic architectural map of your codebase.

- **What it does:** It maps buildable components, aggregators, runners, and external packages, connected by explicit dependency edges.
- **Why it's utilitarian:** Instead of the LLM "guessing" how a file is used, it sees a JSON-serialized graph of exactly how data flows through the build system. This prevents the "JS perspective" errors you mentioned by forcing the LLM to respect the actual dependency boundaries of the project.

### 2\. Hierarchical Summarization Workflow

To handle massive codebases that exceed even the 1M+ token windows of models like Gemini 3, researchers use **Hierarchical Summarization**:

1. **Leaf Level:** Summarise every individual function/method.
2. **Branch Level:** Summarise the purpose of each file based on its functions.
3. **Root Level:** Summarise the module/directory based on the file summaries.
- **The "Reusable" Aspect:** These summaries are cached. When you ask a question, the LLM first looks at the Root summary, "drills down" to the relevant Branch, and only then pulls the raw source code.

### 3\. Symbolic Context Engines

Tools like **CocoIndex** and **Tree-sitter** are now integrated into "Context Engines" rather than just databases.

- **AST-based Chunking:** Instead of cutting code every 500 characters, these tools use Tree-sitter to chunk code by **semantic scope** (e.g., a whole class or a complete data-oriented system).
- **Symbolic Links:** They create a map of every symbol (variable, function, type) so the LLM can "Go to Definition" internally across the entire codebase without needing the files open.

---

### SOTA Tools for 2026

| Tool | Category | Key Utilitarian Feature |
| --- | --- | --- |
| **Cursor / RooCode** | IDE Agents | Uses `.cursorrules` or `.clinerules` to anchor the "perspective" (e.g., "Always use DOD over OOP"). |
| **Claude Code / Gemini CLI** | CLI Agents | These tools now perform **multi-step reasoning**; they run your tests to "verify" their understanding before suggesting code. |
| **Greptile / Sourcegraph Cody** | Repository Indexers | They generate a persistent "Knowledge Graph" of your repo that stays updated with every commit. |
| **RIG-Extractors** | Research Tools | Automate the creation of Repository Intelligence Graphs to feed into agent context windows. |

---

### Solving the "Perspective" Problem: Meta-Context

To ensure an LLM doesn't miss the **Data-Oriented Design (DOD)** benefits or apply a "JS perspective" to Rust, the SOTA workflow involves a **Philosophical Anchor file**.

> **The `.ai-architecture` standard:**Modern workflows involve keeping a file in the root directory (e.g., `ARCH.md` or `.cursorrules`) that explicitly defines the **Constraints** and **Intent**:
> 
> - *"We prioritise cache locality. Avoid pointers where possible."*
> - *"All state must be stored in flat arrays; logic is handled by external systems."*

By providing this "Lens" alongside a **Repository Intelligence Graph**, you ensure the LLM's understanding is not just statistical, but structurally and philosophically aligned with your goals.

**Would you like me to help you generate a "Repository Intelligence" summary or a set of Architectural Rules for your specific codebase?**

Turn my previous prompt into a week structured research prompt for deep research

To get the most out of a "Deep Research" agent (like OpenAI Deep Research or similar iterative models), the prompt needs to be specific about the **problem of perspective** you identified.

Below is a structured research prompt designed to force the AI to look beyond simple RAG (Retrieval-Augmented Generation) and investigate the "Mental Model" of code.

---

## The Deep Research Prompt

**Subject:** State-of-the-Art (SOTA) Methodologies for Multi-Paradigm Codebase Comprehension in LLMs.

**Objective:** Investigate the most "utilitarian" workflows for an LLM to index and understand a large codebase while preserving the **architectural intent** and **design philosophy** (e.g., Data-Oriented Design vs. OOP). The goal is to identify how to prevent "perspective drift" (e.g., an LLM applying Javascript patterns to a Rust project or missing performance benefits of DOD).

**Key Investigative Pillars:**

1. **Structural vs. Semantic Mapping:** \* Compare the effectiveness of **Abstract Syntax Trees (AST)** and **Repository Intelligence Graphs (RIG)** against standard vector embeddings.
	- Research how tools use **Tree-sitter** to maintain scope and relationship awareness during retrieval.
2. **Architectural Grounding (The "Lens" Problem):** \* Explore current research into "Meta-Context" injection.
	- How can we programmatically extract a codebase's "philosophy" (e.g., memory safety priorities, cache locality, or functional purity) to act as a permanent filter for LLM output?
3. **Advanced Retrieval Workflows:** \* Analyse the utility of **HyDE (Hypothetical Document Embeddings)** and **Cross-Encoders/Rerankers** in the context of code.
	- How do these methods handle "utility" for a developer who needs to understand *why* a decision was made, not just *what* the code does?
4. **SOTA Tooling Landscape (2025-2026):** \* Identify the leading frameworks (e.g., **Candle**, **Graph-based Indexers**, **Symbolic Execution Agents**) that move beyond simple "chat with docs" and into "reasoning over architecture."
5. **Reusable Context Standards:** \* Research emerging standards for "Context Files" (like `.ai-context`, `.clinerules`, or automated architectural summaries) that allow an LLM to maintain a consistent "perspective" across different sessions.

**Success Criteria:**The final report must provide a technical roadmap for building a context engine that understands code **not as text**, but as a **structured system of intent**. It should specifically address how to avoid poor-quality code generation resulting from the LLM defaulting to the most common (but potentially incorrect) programming paradigms found in its training data.

---

### Why this prompt works for your needs:

- **ADHD-Friendly Structure:** It breaks the complex "vibe" of your question into five distinct, searchable pillars.
- **Focus on Intent:** It uses the term "Architectural Grounding," which is the technical way of saying "don't let the LLM give me a JS answer for a Rust problem."
- **SOTA Focus:** It specifically asks for 2025–2026 developments, ensuring you don't get outdated advice about basic ChatGPT-4 usage.

**Would you like me to run a simulation of how a Deep Research agent might answer one of these pillars specifically?**

Yes

This is a simulation of how a **SOTA Deep Research Agent** (circa early 2026) would respond to the "Architectural Grounding" pillar of your research prompt.

---

## Research Report: Architectural Grounding and Intent Preservation

**Focus:** Eliminating "Perspective Drift" in LLM Codebase Comprehension **Date:** 18 January 2026

## Executive Summary

The primary failure in current AI-assisted coding is not a lack of *knowledge*, but a lack of *constraints*. When an LLM defaults to a "Javascript perspective" on a Rust project, it is performing a "Statistical Mean Regression"—choosing the most common pattern in its training data rather than the most correct pattern for the specific architecture. SOTA research in 2025–2026 has shifted toward **Deterministic Grounding** to solve this.

---

## 1\. Deterministic Grounding: The Repository Intelligence Graph (RIG)

Recent breakthroughs (e.g., *Cherny-Shahar et al., Jan 2026*) have introduced the **Repository Intelligence Graph**.

- **The Problem:** Traditional RAG (Retrieval-Augmented Generation) treats code like a library of text. The LLM has to "guess" relationships.
- **The SOTA Solution:** A RIG is a deterministic, non-probabilistic map of the build system (using tools like **SPADE** to extract data from CMake or Cargo).
- **Utilitarian Impact:** It provides the LLM with a JSON "Authority Map" before it starts. Instead of guessing how a data-oriented system connects, the LLM consults the RIG to see exactly how components are aggregated.
- **Results:** Research shows a **12.2% increase in accuracy** and a **53.9% reduction in completion time** by shifting the LLM from "understanding structure" to "reasoning over a known structure."

## 2\. Semantic Anchoring via "Contractual Constraints"

To prevent the LLM from missing the benefits of Data-Oriented Design (DOD), researchers are now using **Design-by-Contract (DbC)** as a prompt-injection layer.

- **Preconditions & Postconditions:** By feeding the LLM the "Contracts" of your data structures (e.g., *"This array must remain contiguous for cache efficiency"*), the LLM's pass-rate for complex refactoring tasks increases significantly.
- **Abstraction-Aware Summaries:** Tools like **LocalizeAgent** (2025) now perform "Program Analysis" first, converting raw AST data into "Natural Language Invariants."
	- *Example:* Instead of "Here is a struct," the tool tells the LLM: "This is a DOD-style component. Do not add methods; modify the System processing the array."

## 3\. The "Meta-Context" Layer: Rules vs. Vibe

The industry has settled on a dual-layer approach to maintain "Perspective":

- **Layer A (Global Constraints):** Files like `.cursorrules` or `.clinerules` act as a "Philosophical Firewall." They explicitly forbid paradigms (e.g., "FORBID: Encapsulation in Data Modules").
- **Layer B (Hierarchical Context):** Using **Context-Alignment (CA)**, models are now "aligned" with the specific linguistic style of the repo. If your repo uses "System-Component" nomenclature, the CA layer forces the LLM to use that logic in its reasoning chain.

---

## SOTA Roadmap for your Codebase

To implement the most utilitarian understanding for an LLM today, you should follow this 2026 workflow:

1. **Generate a RIG:** Use an automated tool to output your build dependency graph as a JSON file.
2. **Define Invariants:** Create a `.ai-architecture` file that lists **Forbidden Paradigms** (e.g., "No OOP inheritance in the performance layer").
3. **Active Reranking:** Use a "Cross-Encoder" that ranks retrieved code snippets based on their **Architectural Fit**, not just their text similarity.

---

**Would you like me to draft the specific `.ai-architecture` rules that would force an LLM to respect Data-Oriented Design in your current project?**

What tools or processes are best for analysing the data structures and transformations of that data used in the code whether they are explicit or implicit?

To analyse code from a utilitarian, data-first perspective (ignoring "clean code" dogmas and focusing on what the data actually *does*), you need tools that map **Data Lineage** and **Transformation flows** rather than just syntax.

Most standard tools (like LSPs or basic IDEs) show you the **AST** (Abstract Syntax Tree). They tell you "This is a class." They fail to show the implicit reality: "This data structure is cloned three times unnecessarily before reaching the GPU."

Here are the best tools and workflows to analyse the "physics" of your data.

### 1\. The "Code Property Graph" (CPG)

This is the most powerful utilitarian method. A CPG does not just read code; it overlaps three different graphs to create a complete map of your software's reality.

- **AST (Structure):** What the code looks like.
- **CFG (Control Flow):** The path execution takes (if/else/loops).
- **PDG (Data Dependence):** The path *data* takes. This is the key. It shows that Variable A affects Variable Z, even if they are in different files and never explicitly call each other.

**The Tool: Joern**

- **What it is:** An open-source platform that converts C/C++/Java/JS code into a CPG and lets you query it like a graph database.
- **The Workflow:** You don't read files. You write a query: *"Show me every path where data from `UserEntry` reaches `SQLQuery` without being sanitized."*
- **Why it fixes "Perspective":** It ignores your class hierarchy. It doesn't care if you used a Factory Pattern or a Singleton. It only cares about the raw path of the data bytes.

### 2\. Query-Based Data Flow Analysis

If Joern is for graph exploration, **CodeQL** is for forensic interrogation. It treats your codebase as a relational database.

**The Tool: CodeQL (by GitHub)**

- **Explicit Transformations:** You can write queries to find every instance where a specific `struct` is mutated.
- **Implicit Transformations (Taint Tracking):** CodeQL excels at "Taint Analysis." It can track a piece of data from a source (e.g., a network packet) to a sink (e.g., a memory buffer), revealing implicit transformations that happen via pointers, dependency injection, or callbacks.
- **Utilitarian Benefit:** It allows you to mathematically verify *invariants* (e.g., "Ensure this specific Array is never copied, only referenced").

### 3\. Runtime "Reality Checks"

Static analysis (reading code) is often wrong about performance and cache locality. To understand the "utilitarian" reality of your data layout in memory, you need dynamic observation.

**The Tool: Reversible Debuggers (e.g., RR or Undo)**

- **The Workflow:** Instead of stepping forward, you record the execution. You can then query the timeline: *"When was this memory address last written to?"*
- **Why it matters:** This reveals **False Sharing** and **Cache Thrashing** —implicit data interactions that no static code analysis can see, but which destroy performance in Data-Oriented designs.

### 4\. SOTA LLM Context: The "Graph-of-Flows"

To feed this into an LLM so *it* understands the utilitarian view, you cannot just paste text. You must generate a **Data Intelligence Graph**.

**The Process (2025/2026 Research Standard):**

1. **Extraction:** Use **Tree-sitter** to parse the code into an AST.
2. **Graphing:** Use a tool like **stack-graphs** (Rust-based) to resolve all references (variables/functions) to their definitions.
3. **Projection:** Generate a simplified JSON that lists **"Data Producers"** and **"Data Consumers"**.
4. **Prompting:** Feed this JSON to the LLM.
	- *Result:* The LLM sees `OrderData` -> `transformed_by(ProcessA)` -> `consumed_by(Database)`.

### Summary of Recommendation

| Goal | Best Tool | Why it fits "Utilitarian" View |
| --- | --- | --- |
| **Deep Analysis** | **Joern** | Maps implicit connections between data points across the entire repo. |
| **Enforcing Rules** | **CodeQL** | Mathematically proves that data flows (or doesn't flow) a certain way. |
| **LLM Context** | **Stack-graphs** | Rust-based, incredibly fast; extracts accurate "jump-to-definition" graphs for AI. |
| **Memory Truth** | **RR / Tracy** | Visualises the actual memory layout and cache usage at runtime. |

**Would you like me to generate a specific CodeQL query or Joern script to map the data flow of a critical structure in your project?**

No, research how these techniques work so I can recreate the process for my project of LLM agents analysis full code bases to generate deep context to optimise the context fed to code writing agents

Recreating a state-of-the-art context engine requires moving away from "text search" and toward "program analysis." Your goal is to build a system that treats code as a **computable graph** of data movement, not just a collection of files.

Below is the research-backed blueprint for recreating this process to feed high-utility context into your writing agents.

---

### Phase 1: The Extraction Layer (Deterministic Truth)

To avoid the "JS perspective" on a Rust codebase, you must first extract the objective structure of the code.

- **Tooling:** Use **Tree-sitter** for initial parsing and **Joern** to generate a **Code Property Graph (CPG)**.
- **The Process:** 1. Parse every file into an Abstract Syntax Tree (AST). 2. Resolve all "Symbols" (variable names, function calls) to their definitions. 3. Generate the **Control Flow Graph (CFG)** to see how execution moves through the data.
- **Outcome:** You now have a graph where a node represents a "Transformation" and an edge represents a "Data Dependency."

### Phase 2: Data Flow & Lineage Analysis

This is where you identify the "implicit" transformations you mentioned. You want to know where data comes from (Source), how it changes (Transform), and where it ends up (Sink).

- **Tooling:****CodeQL** or **Joern's Scala API**.
- **The Process:** 1. **Taint Tracking:** Write a query to find all paths from a specific data structure (e.g., a `NetworkPacket` struct) to a specific output (e.g., a `FrameBuffer`). 2. **State-Change Mapping:** Identify every point where a variable is mutated. If you are using Data-Oriented Design, this will reveal exactly which "Systems" are touching which "Components."
- **Outcome:** A structured list of **Data Life-Cycles**. Instead of telling the LLM "Here is `main.rs`," you tell it: *"The `PlayerData` struct is initialized in `loader.rs`, mutated by the `PhysicsSystem`, and finally read by the `Renderer`."*

### Phase 3: The "Lens" & Invariant Generation

Now you must translate that technical graph into a "Philosophical Anchor" for the LLM.

- **Automated Summarisation:** Feed the **Data Life-Cycles** from Phase 2 into a high-reasoning model (like Claude 3.5 or Gemini 1.5 Pro).
- **Prompting for Invariants:** Ask the LLM: *"Based on these data flows, identify the architectural invariants. Is this project using DOD or OOP? Does it prioritize immutability or in-place mutation?"*
- **The Result:** An **Architectural Context File** (`.ai-context`) that contains:
	- **Data Layouts:** Contiguous arrays vs. pointer-heavy objects.
	- **Forbidden Patterns:** (e.g., "Do not use inheritance; data must flow through the `Update` loop").

### Phase 4: The Agent Loop (Model Context Protocol)

Finally, you must give your writing agent "live" access to this graph.

- **Workflow:** Use the **Model Context Protocol (MCP)** to create a bridge between your writing agent and your Joern/CodeQL server.
- **Live Querying:** When the agent needs to write code, it doesn't just look at the file. It sends a tool-call: `get_data_flow("buffer_id")`.
- **The Utility:** The agent receives the *actual* data path, ensuring it writes code that respects the performance benefits of your architecture (like cache locality).

---

### Summary: The "Deep Context" Stack

| Layer | Component | Goal |
| --- | --- | --- |
| **Parsing** | Tree-sitter | Understanding grammar and structure. |
| **Graphing** | Joern / CPG | Understanding execution paths and dependencies. |
| **Tracing** | CodeQL | Understanding data lineage and "taint" (implicit flows). |
| **Distillation** | LLM Invariants | Translating the graph into an "Architectural Perspective." |
| **Delivery** | MCP Server | Providing "live" graph access to the writing agent. |

[Querying the Code Property Graph](https://www.youtube.com/watch?v=KLTn0i3h8Xw)

This video demonstrates how to use a Code Property Graph to interactively query and explore the hidden connections in your code, which is the foundational step for generating the "Deep Context" you need for your agents.

**Would you like me to help you write a sample Joern script or CodeQL query to track a specific data flow in your codebase?**

The video **"Querying the Code Property Graph"** demonstrates how to use the **Ocular** query engine to interrogate a **Code Property Graph (CPG)**. This process moves beyond standard text searching by treating the entire application and its dependencies as a queryable database.

### Key Points & Methodologies

- **Creating the Graph (CPG)**: The process begins with a compiled build artifact (e.g., a `.war` or `.jar` file). A command like `java2cpg` parses this to create a composite graph representing the code, its internal dependencies, and the frameworks it uses in seconds.
- **Dependency Auditing**: Using a fluent API, you can list every open-source dependency and its version. This is used to find vulnerable libraries, such as specific versions of **Jackson** known for deserialisation vulnerabilities.
- **Semantic Type Analysis**: By querying for all types defined in the code, you can deduce the "intent" of the application. For instance, seeing types like `zip4j` or `cipherOutputStream` immediately reveals that the code handles file decompression and encryption.
- **Literal and Secret Detection**: The engine can scan for hard-coded literals. This is particularly useful for finding "design faux pas" like lack of internationalisation or high-risk security flaws such as hard-coded **AWS credentials** embedded directly in methods.
- **Mapping the Attack Surface**: You can programmatically identify all exposed API endpoints (GET/POST requests). This provides a complete map of where an external consumer or attacker can interact with the system.

### Utilitarian Ideas for LLM Agents

- **Fluent API as Agent Interface**: Instead of feeding raw code to an agent, you can provide it with the **Ocular API**. This allows the agent to "ask questions" about the code's structure and only retrieve the relevant nodes, preventing context window bloat.
- **Automated Sensitive Data Discovery**: ShiftLeft uses **NLP and Machine Learning** to classify sensitive data based on variable naming (e.g., identifying a `User` class with a `passport_number` field). An agent could use this to automatically identify "high-priority" data structures for optimisation or security.
- **Contextual Grounding via Methods**: You can trace any specific literal or data flow back to the exact method and file it originated from, providing the LLM with the precise "ground truth" of the code's execution.

For a deeper dive into the mathematical foundations of this technology, you might find this presentation on [Elegant and Scalable Code Querying with Code Property Graphs](https://www.youtube.com/watch?v=TVVo-r0voOk) useful. It explains how multi-layered graphs capture properties across different abstractions like libraries and frameworks, which is essential for building a "Deep Context" engine.

Google Account

Leon Ormes

leonormes@gmail.com

---

## Phase 2: The Gate (4D Filter)
- [ ] **Do:** < 2 mins?
- [ ] **Delegate:** Who?
- [ ] **Defer:** Move to Hangar or SoT?
- [ ] **Delete:** Is this noise?

---

## Phase 5: The Scribe (#SAVESTATE)
- **The Conflict:**
- **The Current State:**
- **The Next Test:**