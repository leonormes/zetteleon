---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-29T09:36:05+00:00
permalink: llmeon/30-library/100-zettelkasten/root-llm-dispatches-generative-subtasks-to-sub-llms-via-code-mediated-function-calls
proposition: In a Recursive Language Model, a Root LLM acts as orchestrator — it writes
  "Python code, manages the environment's variables, and defines prompts — but does"
  not itself perform the generative work on task data. When a specific piece of generative
  or classification work is needed, the Root LLM invokes a special `llm_query` function
  from within its own Python code, which dispatches that specific chunk of work to
  a Sub-LLM. Delegation happens through a code-level function call, not through a
  fixed agent-role handoff or a graph transition.
tags: [domain/llm, topic/agent-architecture, topic/multi-agent, topic/rlm]
title: Root LLM Dispatches Generative Subtasks to Sub-LLMs via Code-Mediated Function Calls
  Calls
type: claim
---

## Root LLM Dispatches Generative Subtasks to Sub-LLMs via Code-Mediated Function Calls

The Root LLM's job is orchestration, not generation: it decides what needs to happen, writes the Python that makes it happen, and holds the state of the overall task in environment variables. Whenever a step actually requires an LLM's judgment or generative ability—classifying a batch of questions, for instance—the Root LLM writes a call to an `llm_query`-style function, exactly as it would call any other function in its code. That function call is what dispatches the work to a Sub-LLM.

The distinguishing feature is _how_ the dispatch happens: it's a function call inside code the Root LLM itself wrote, at a moment the Root LLM itself chose, with a scope it itself defined—not a pre-wired role handoff (fixed sub-agents each responsible for a fixed slice of the task) and not a graph transition (a predefined edge in an orchestration graph). The Root LLM has full discretion over when to delegate, what to delegate, and how many times to do it.

### Scope & Conditions

Applies specifically to RLM-style architectures where the orchestrating LLM has code-execution access and calls sub-LLMs as functions from within that code. Distinct from architectures where sub-agent delegation is structurally fixed in advance (role-based sub-agent division) or mediated by an external orchestration graph (LangGraph-style agent loops).

### Evidence

Source: "From RLMs to Agent Harnesses" (Still Broken AI). "The Root LLM acts as the orchestrator. Its primary job is to write the Python code, manage variables, and define prompts" [29:18]. "When a specific AI task is needed (e.g., classifying a batch of questions), the Root LLM executes a special `llm_query` function in the Python environment, which calls a Sub-LLM to do the heavy lifting" [29:49].

### Implications

- This is a distinct delegation mechanism from existing sub-agent patterns in this vault: [[Specialized Sub-Agent Roles Divide Research, Context Retrieval, and Code Editing]] divides work by fixed role assigned in advance; [[Deep Agents for Long Horizon Planning]] delegates via a graph/tool-call loop with tailored prompts per sub-agent. This note's mechanism is dispatch-by-code, decided dynamically at runtime by the orchestrator itself, with no predefined role boundaries.
- It depends on the environment-variable architecture: this dispatch pattern only makes sense once [[Recursive Language Models Load Context as Environment Variables, Not Prompt Tokens]] is already true—the Root LLM needs somewhere to hold state between dispatches, and that's the REPL environment, not its own context.
- It's the mechanism that makes dynamic runtime chunking possible: [[RLMs Dynamically Chunk Data at Runtime, Unlike RAG's Static Pre-Defined Chunking]] depends on the Root LLM being able to decide, on the fly, how many Sub-LLM calls to make and over what slices—which is exactly what this dispatch mechanism provides.

### Related

- [[Specialized Sub-Agent Roles Divide Research, Context Retrieval, and Code Editing]]—contrast: fixed-role division vs. this note's dynamic, code-mediated, runtime-decided dispatch.
- [[Deep Agents for Long Horizon Planning]]—contrast: graph/tool-call-mediated delegation vs. this note's literal function-call-from-code dispatch.
- [[Recursive Language Models Load Context as Environment Variables, Not Prompt Tokens]]—depends_on: the environment is the substrate that makes this dispatch pattern coherent.
- [[Software Factory Pattern - Specialized Sandboxed Agents Autonomously Own Feature, Bugfix, and Incident Lifecycles]]—related: both describe multi-LLM division of labor, at different granularities (org-scale agent fleet vs. single-task orchestrator/sub-LLM dispatch).

### See Also

- [[RLMs Avoid Context Bloat by Storing Intermediate State as Symbolic Variables, Not Context Tokens]]

%%[depends_on:: [[Recursive Language Models Load Context as Environment Variables, Not Prompt Tokens]], strength=4, confidence=medium]%%
