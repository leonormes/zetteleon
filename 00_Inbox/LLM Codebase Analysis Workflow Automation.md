---
created: 2026-01-15T08:11:27+00:00
modified: 2026-01-20T16:17:20+00:00
title: LLM Codebase Analysis Workflow Automation
---

## Architecting AI-Augmented Development: A Comprehensive Framework for LLM-Driven Codebase Analysis and Automation

The integration of Large Language Models (LLMs) into the software development lifecycle represents a fundamental shift in engineering methodology. We are transitioning from a syntax-centric model, where developers manually translate intent into code, to an architecture-centric model, where developers curate context and orchestrate reasoning engines. However, the efficacy of this new paradigm hinges entirely on the quality of "Context Engineering"—the rigorous discipline of preparing, structuring, and managing the information fed into the model. As indicated by recent research into "Context Rot" and attention degradation, simply flooding an LLM with an entire repository is a recipe for hallucination and inefficiency.1

This report details a robust, repeatable workflow for orchestrating LLMs to assist with coding tasks across heterogeneous codebases, ranging from declarative infrastructure in Terraform and Helm to imperative logic in TypeScript and Rust. The proposed framework prioritizes the creation of high-fidelity "Reference Artifacts" over raw code generation, establishing a "Context Topology" that allows an AI agent to reason about a system's architecture before attempting to modify it. By leveraging the specific capabilities of the Gemini CLI for high-reasoning tasks and Ollama for local, privacy-preserving execution, we construct a hybrid, resilient automation pipeline.

---

Part A: Extracted & Categorized Prompts

The conceptual notes provided describe a sophisticated cognitive process—a "Senior Engineer's Mental Model" for onboarding onto a new codebase. To automate this, we must decompose the seamless flow of human thought into discrete, executable "Cognitive Primitives." Each primitive represents a distinct mode of reasoning that requires a specific prompt structure to elicit the optimal response from an LLM.

The analysis of the source text reveals six distinct prompt categories. These are not merely instructions but architectural blueprints that define how the LLM should perceive and process the codebase.

#### 1. The Reconnaissance Prompt (Structural Analysis)

The initial phase of the conceptual workflow demands that the system "get a lay of the land: summarize the directory tree, find the main entry points, and list critical dependencies." This is a discovery task. The cognitive mode required here is High-Level Pattern Recognition. The LLM must ignore the noise of implementation details and focus solely on the structural skeleton of the project.

This prompt serves as the "Surveyor." In large codebases, reading every file to determine the architecture is token-prohibitive. Instead, this prompt operates on metadata: directory trees, file names, and configuration manifests (e.g., package.json, Cargo.toml). By analyzing these artifacts, the LLM can infer the architectural style—whether it is a monolithic Rust application, a microservices-based TypeScript monorepo, or a modular Terraform infrastructure.

Prompt Specification:

The prompt must instruct the model to act as a Systems Architect. It should ingest a raw text representation of the directory structure and the contents of dependency files. The output must not be a summary of what the files contain, but a deduction of how the system is organized. For instance, the presence of a modules/ directory in Terraform implies a modular composition, whereas a flat structure in Go suggests a different pattern. The prompt must explicitly request the identification of "Entry Points"—the files where execution begins—as these are the roots of the dependency graph.

| Prompt Attribute | Specification |
|:---- |:---- |
| Category | Structural Reconnaissance |
| Input Data | Directory Tree (tree output), Dependency Manifests |
| Cognitive Goal | Pattern Inference & Entry Point Identification |
| Output Artifact | 01_Architecture_Overview.md |

#### 2. The Functional Extraction Prompt (Module Deep-Dive)

The second directive is to "go deeper into specific modules" and "explain its purpose, inputs, outputs, and key functions." This represents the core of the analysis workflow: Semantic Compression.

A raw source file contains significant redundancy—syntax noise, imports, and verbose logic—that dilutes the "signal" relevant to an LLM's reasoning. This prompt aims to strip away the implementation details to reveal the "Functional Contract" of the module. This aligns with the concept of "Context Packing" described by expert practitioners, where the goal is to provide the model with a dense "brain dump" of high-level goals and invariants rather than raw code.2

Prompt Specification:

This prompt acts as a "Documentation Specialist." It requires the LLM to read the source code of a single module and produce a "Reference Specification." Crucially, this specification must be structured as data, not prose. It should list every public function, its parameters (Inputs), and its return values (Outputs). This mirrors the "Input/Output" analysis requested in the conceptual notes. By converting code into a functional spec, we create a token-efficient proxy that can be loaded into the context window later, replacing the heavy source code.

#### 3. The Teleological Alignment Prompt (Goal Contextualization)

The user explicitly requests: "Always relate it back to the project's main goal." This introduces the dimension of Teleological Reasoning—understanding parts in relation to the whole.

Code does not exist in a vacuum; it serves a specific business or technical objective. A module named auth.ts has a different significance in a banking application (critical security infrastructure) than in a prototype hobby project (basic utility). This prompt category enforces "Alignment." It ensures that the generated documentation is not dry and descriptive but evaluative.

Prompt Specification:

This prompt functions as a "Product Alignor." It takes the output of the Functional Extraction (the module spec) and the global project goal as inputs. It asks the LLM to synthesize a "Strategic Relevance" statement. This helps future agents understand the criticality of the module. If a future agent is asked to refactor code, knowing that a module is "Critical Path" versus "Auxiliary" will fundamentally change the risk profile of the generated code.

#### 4. The Topology Prompt (Dependency Mapping)

The instruction to "map out how the modules connect" requires Graph Theoretical Reasoning. This moves the analysis from the node level (individual modules) to the edge level (relationships).

In complex systems like Helm charts or distributed Rust services, understanding dependencies is more important than understanding syntax. A change in a variable definition in Terraform can cascade through multiple modules. This prompt is designed to construct the "Connectome" of the codebase.

Prompt Specification:

This prompt acts as a "Systems Integrator." It consumes the summaries of all modules (not the code) and deduces the flow of data and control. The output requirement is strictly defined: a Mermaid.js diagram and a textual description of Upstream (who calls me?) and Downstream (who do I call?) relationships. This visual and textual map allows the LLM to perform impact analysis in later stages, predicting how a change in Module A might break Module B.

#### 5. The Reference Artifact Prompt (Serialization)

The user desires to "create a set of reference docs I can feed back to the LLM." This is a meta-prompt category focused on Context Serialization.

The output of an LLM session is typically ephemeral. To build a repeatable system, we must persist the model's understanding into a format that is optimized for machine reading. As research indicates, providing clear, markdown-formatted context files (GEMINI.md, llms.txt) significantly improves the performance of coding agents.3

Prompt Specification:

This prompt acts as a "Librarian." It takes the fragmented analysis from previous steps (Architecture, Specs, Topology) and formats them into standardized, rigid Markdown files. The instruction here is to prioritize information density and structural clarity over conversational prose. These files are the "Long-Term Memory" of the system.

#### 6. The Refactoring Planner Prompt (Action Planning)

Finally, the user notes: "Sometimes I need to refactor or add a feature, so the context needs to be ready for that." This is the transition from analysis to Agentic Planning.

Best practices in LLM-assisted coding emphasize separating the "Planning" phase from the "Coding" phase.2 Generating code without a plan often leads to "spaghetti code" or hallucinated APIs. This prompt generates a step-by-step roadmap for a proposed change, verifying feasibility against the accumulated context before writing a single line of code.

Prompt Specification:

This prompt acts as the "Lead Engineer." It ingests the User Query and the relevant Reference Artifacts. Its output is not code, but a "Change Manifest"—a list of files to touch, logic to alter, and tests to run.

---

Part B: Ordered Analysis & Context Preparation Checklist

The conversion of a raw codebase into a semantic knowledge base requires a structured, orderly process. This checklist serves as the "Standard Operating Procedure" (SOP) for the automation workflow. It is designed to be universally applicable, handling the specific nuances of diverse technologies through abstraction.

#### Phase 1: Repository Discovery (The Survey)

The objective of this phase is to establish the global context without polluting the LLM's attention window with irrelevant data. "Context Stuffing"—indiscriminately dumping files—leads to degraded reasoning capabilities.1 Therefore, this phase focuses on precise signal extraction.

1. Environment Sanitization & Noise Reduction:
   The first step is to define what not to read. Standard.gitignore files are insufficient for LLM context management, as they often include build artifacts but exclude configuration files that might be relevant for context.
   - Action: Generate a.llmignore file.
   - Heuristic: Exclude high-volume, low-information directories.
     - _TypeScript_: node_modules, dist, coverage, package-lock.json.
     - _Rust_: target, Cargo.lock.
     - _Terraform_:.terraform,.terraform.lock.hcl.
     - _Helm_: charts/ (if they are external dependencies).
   - Rationale: Reducing the token count of the directory tree ensures the LLM focuses on the source code structure rather than dependency trees.
1. Automated Tree Generation:
   A visual representation of the file hierarchy is the most efficient way to convey architectural patterns to an LLM.
   - Action: Execute a tree-generation command respecting the ignore patterns.
   - Command: tree -a -I "$(cat.llmignore | tr 'n' '|')" --prune.
   - Output: Save to _context/raw_tree.txt.
1. Dependency Manifest Extraction:
   The capability of a software project is largely defined by its external dependencies. A Rust project using tokio is fundamentally different from one using std::thread.
   - Action: Identify and aggregate key configuration files.
   - Targets:
     - _Generic_: README.md (High-level intent), Makefile / Justfile (Entry points/Verbs).
     - _TS_: package.json, tsconfig.json.
     - _Rust_: Cargo.toml.
     - _Infra_: versions.tf, Chart.yaml.
   - Constraint: For large lock files, extract only the top-level dependencies, ignoring transitive ones to save tokens.
1. Architectural Synthesis (The First Pass):
   This is the first interaction with the LLM (Gemini/Ollama).
   - Input: raw_tree.txt + manifests.txt.
   - Prompt: The Reconnaissance Prompt.
   - Artifact Generation: Produce 01_Architecture_Overview.md.
   - Key Insight: This document becomes the "System Prompt" for all future interactions. It anchors the model in the reality of the specific project.

#### Phase 2: Context File Generation (The Cartography)

This phase transforms the codebase from a collection of text files into a "Semantic Index." The goal is to create the "Reference Docs" requested by the user.

1. Domain Segmentation Strategy:
   Before analyzing code, we must divide the project into manageable "Context Chunks".6
   - Action: Analyze 01_Architecture_Overview.md to identify "Domains" (logical groupings of functionality).
   - Strategy:
     - _Monoliths_: Segment by top-level directories (e.g., src/api, src/db).
     - _Microservices_: Segment by service root.
     - _Infrastructure_: Segment by Terraform module or Helm chart.
   - Limit: Ensure no single segment exceeds the effective context window of the fallback model (e.g., 4k-8k tokens for standard Ollama models).
1. Iterative Module Summarization (Map-Reduce):
   We apply a "Map-Reduce" pattern to document the codebase. We map the summarization task across all modules and then reduce them into a cohesive system graph.7
   - Action: For each identified domain:
     1. Agglomerate: Concatenate all source files within the domain boundaries.
     2. Prompt: Apply the Functional Extraction Prompt chained with the Teleological Alignment Prompt.
     3. Output: Generate 02_Module_{Name}.md.
   - Language-Specific Nuances:
     - _Rust_: Focus on struct definitions and impl blocks; ignore function bodies if they are verbose.
     - _Terraform_: Focus on resource and module blocks; ignore lengthy locals unless critical.
     - _TypeScript_: Focus on exported interfaces and types.
3. Topology Mapping:
   Once the individual nodes (modules) are documented, we must define the edges (connections).
   - Action: Feed the collection of 02_Module_.md summaries (not the raw code) into the LLM.
   - Prompt: The Topology Prompt.
   - Artifact Generation: Produce 03_System_Topology.md containing the Mermaid diagram and data flow analysis.

#### Phase 3: Context Management Strategy (The Librarian)

Effective context management is about "Just-in-Time" information delivery. We do not want to load the entire library when we only need a single book.

1. The Hierarchical Context Model:
   We adopt the hierarchical loading strategy supported by tools like Gemini CLI 8 and adaptable for Ollama.
   - Global Context: 01_Architecture_Overview.md. This is always loaded. It provides the "Who am I?" and "Where am I?" awareness.
   - Domain Context: 02_Module_{Name}.md. Loaded only when the user query relates to that specific domain.
   - Local Context: The raw source files. Loaded only during the "Planning" and "Coding" phases for the specific files being modified.
1. The GEMINI.md / System Prompt Integration:
   - Gemini CLI: Create a.gemini/GEMINI.md file in the project root. Use @import directives (if supported) or script concatenation to include the Global Context.4
   - Ollama: Construct a dynamic "System Prompt" string in the orchestration layer that prepends the Global Context to every session.
1. The Context Refresh Cycle:
    Codebases are living organisms. Context must be maintained.
    - Trigger: Any successful code generation or refactor.
    - Action: The automation script triggers a re-summarization of _only_ the modified module. This updates the corresponding 02_Module_{Name}.md and potentially the 03_System_Topology.md, ensuring the "Map" never drifts far from the "Territory".3

---

Part C: Modular Automation Plan with Agent Stages

To operationalize this workflow, we require a robust automation system. While shell scripts can chain commands, they lack the sophisticated error handling, string parsing, and state management required for a reliable agentic workflow. Therefore, we propose a Python-based Orchestrator (codegraph.py) that wraps the Gemini and Ollama CLIs.

This orchestrator functions as a "Meta-Agent," managing a team of specialized sub-agents. It leverages Gemini CLI for high-reasoning tasks (Architecture, Topology) due to its superior context window and reasoning capabilities, and falls back to Ollama for local execution or when privacy/cost is a constraint.

#### 1. Automation Architecture: The Agentic Chain

The system is designed as a linear state machine where the output of one agent becomes the immutable context for the next. This minimizes "context drift" and ensures that downstream agents (like the Coder) are constrained by the architectural decisions of upstream agents (like the Architect).

| Agent Name | Role | Input | Prompt Template | Tooling |
|:---- |:---- |:---- |:---- |:---- |
| The Librarian | Discovery | Root Dir | Reconnaissance | tree, File I/O |
| The Analyst | summarization | Source Files | Functional Extraction | LLM (Gemini/Ollama) |
| The Architect | Synthesis | Module Docs | Topology | LLM (Gemini/Ollama) |
| The Engineer | Planning | Query + Context | Refactoring Planner | LLM (Gemini/Ollama) |

#### 2. Implementation Specifics: The Orchestrator

The codegraph.py script serves as the spine of the operation. It abstracts the differences between the two model providers.

##### Model Abstraction Layer

The research highlights distinct usage patterns for the two CLIs. Gemini CLI supports a "headless" mode via the -p flag 9, while Ollama typically reads from stdin via piping.10 The orchestrator must handle these discrepancies transparently.

Python

```py

import subprocess

import os

class LLMProvider:

    def __init__(self, provider="gemini", model="gemini-1.5-pro"):

        self.provider = provider

        self.model = model

    def generate(self, prompt, context_files=, system_instruction=None):  
        """  
        Unified interface for generation.   
        Handles context assembly and CLI invocation.  
        """  
        # Context Assembly: Concatenate files into the prompt  
        full_input = ""  
        for filepath in context_files:  
            with open(filepath, 'r') as f:  
                full_input += f"n--- BEGIN FILE: {filepath} ---n{f.read()}n--- END FILE ---n"  
          
        full_input += f"nnTask:n{prompt}"

        if self.provider == "gemini":  
            return self._run_gemini(full_input, system_instruction)  
        elif self.provider == "ollama":  
            return self._run_ollama(full_input, system_instruction)

    def _run_gemini(self, input_text, system_instruction):  
        # Gemini CLI uses environment variables for system prompts [11]  
        env = os.environ.copy()  
        if system_instruction:  
            # Create a temp file for the system prompt as per best practices  
            with open(".temp_system.md", "w") as f:  
                f.write(system_instruction)  
            env = ".temp_system.md"

        # Use -p for non-interactive (headless) mode   
        cmd = ["gemini", "--model", self.model, "-p", input_text]  
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)  
          
        if result.returncode!= 0:  
            raise Exception(f"Gemini Error: {result.stderr}")  
        return result.stdout

    def _run_ollama(self, input_text, system_instruction):  
        # Ollama requires system prompt to be part of the chat or Modelfile  
        # For ad-hoc CLI usage, we prepend it to the prompt [12]  
        if system_instruction:  
            final_prompt = f"System: {system_instruction}nnUser: {input_text}"  
        else:  
            final_prompt = input_text  
              
        # Pipe input to standard in   
        cmd = ["ollama", "run", self.model]  
        result = subprocess.run(cmd, input=final_prompt, capture_output=True, text=True)  
          
        if result.returncode!= 0:  
            raise Exception(f"Ollama Error: {result.stderr}")  
        return result.stdout  

```

##### Stage 1: The Librarian Agent (Discovery)

This stage executes the repository discovery. It uses Python's native os.walk or the tree command to build the file map.

- Workflow:
  1. Read.llmignore.
  2. Generate file tree string.
  3. Read package.json / Cargo.toml.
  4. Call LLMProvider.generate() with the Reconnaissance Prompt.
  5. Save output to _context/01_Architecture_Overview.md.

##### Stage 2: The Analyst Agent (Context Generation)

This stage iterates over the domains.

- Workflow:
  1. Parse 01_Architecture_Overview.md to identify module paths (heuristic: look for bullet points under "Modules" or directory listings).
  2. For each module path:
     - Collect all source files.
     - Token Check: If the content exceeds the context limit (e.g., 8k for Ollama), apply a "Split-Summarize-Merge" strategy.
     - Call LLMProvider.generate() with Functional Extraction Prompt.
     - Save to _context/02_Module_{Name}.md.

##### Stage 3: The Engineer Agent (Planning & Execution)

This is the interactive stage where the user requests changes.

- Workflow:
  1. User Input: "Refactor the auth logic."
  2. Context Loading:
     - Load 01_Architecture_Overview.md (Global).
     - Load 03_System_Topology.md (Map).
     - Vector Search (Optional) or Keyword Match to find relevant 02_Module_Auth.md.
  3. Planning:
     - Call LLMProvider.generate() with Refactoring Planner Prompt.
     - Display the plan to the user.
  4. Verification: Ask user for confirmation ("Proceed with code generation?").
  5. Execution (If confirmed):
     - Load the _actual_ source files identified in the plan.
     - Prompt the LLM to generate the replacement code.
     - Write the new code to disk (or to a.diff file for safety).

#### 3. Practical Considerations for Local vs. Cloud

The hybrid nature of this plan requires careful handling of model capabilities.

Context Windows & Chunking:

Gemini Pro typically supports extremely large context windows (1M+ tokens), allowing for "whole-module" reasoning. Ollama models, running locally (e.g., Llama 3, Mistral), typically operate with 4k-8k windows.13

- Adaptation: The Orchestrator must detect the active provider. If provider == "ollama", it enforces stricter chunking in Stage 2. It breaks modules down file-by-file rather than folder-by-folder to fit within the memory constraints.

File I/O Safety:

While Gemini CLI has built-in tools for file writing, enabling them can be risky if not sandboxed. The Python Orchestrator mitigates this by handling all file I/O itself. The LLM generates the text, and the Python script writes it. This provides a "Human-in-the-Loop" safety layer, preventing the agent from accidentally deleting or overwriting critical files without permission.

Orchestration Method:

The Python script acts as the "glue." By using argparse, we can expose the stages as CLI commands:

- python codegraph.py init (Runs Librarian)
- python codegraph.py analyze (Runs Analyst)
- python codegraph.py plan "Add a new endpoint" (Runs Engineer)

This modularity allows the developer to run the expensive analysis phases once and then execute multiple lightweight planning queries, optimizing both cost (for Gemini) and time (for Ollama).

#### Conclusion

This framework transforms the chaotic process of "asking AI to fix code" into a rigorous engineering workflow. By formalizing the prompts, structuring the context preparation, and scripting the orchestration, we create a system that is robust enough to handle the complexity of modern, heterogeneous codebases. It moves beyond simple "autocomplete" to provide genuine architectural insight and safe, planned automated refactoring.
