---
created: 2026-02-02T07:37:39+00:00
modified: 2026-02-02T09:28:18+00:00
tags: [---]
title: "Tesler's Law and Torvalds' Complexity"
---

## The Conservation of Complexity: Validating the Torvalds-Tesler Dialectic in Software Architecture

### Executive Summary

The fundamental struggle of software engineering is not the construction of algorithms but the management of complexity. This research report validates the logical synthesis between Tesler's Law of Conservation of Complexity and Linus Torvalds' dichotomy of Code versus Data Structures. By conceptualizing a software system as a thermodynamic container where complexity is a conserved quantity, we analyze the architectural implications of shifting this mass between two primary vessels: Bucket A (Procedural Code) and Bucket B (Data Structures).

The analysis confirms that while complexity is theoretically conserved—meaning the total logic required to solve a domain problem cannot be eliminated—the _location_ of that complexity determines the system's entropy, maintainability, and performance. We validate the hypothesis that "good programming," as defined by Torvalds and supported by historical figures like Fred Brooks and Rob Pike, is characterized by the deliberate migration of complexity from opaque, temporal control flow (Code) into transparent, spatial representation (Data Structures). However, this report also identifies critical failure modes, specifically the Inner-Platform Effect, where excessive shifts to data structures paradoxically regenerate code complexity in an unmanageable, meta-language form. Through case studies ranging from the Linux Kernel's Virtual File System to Enterprise Tax Calculation Engines, we establish that the optimal architecture is one where the data structure is sufficiently expressive to render the code trivial, thereby validating the Torvalds-Tesler dialectic.

---

1. Introduction: The Physics of Software Complexity

In the theoretical physics of software engineering, complexity behaves like energy: it can be transformed, moved, or hidden, but it can rarely be destroyed. This principle serves as the foundation for examining the interplay between user experience, system architecture, and developer cognition.

#### 1.1 The Theoretical Proposition: Bucket A vs. Bucket B

The user query posits a specific structural relationship within software architecture. It suggests that the total complexity of a system (![][image1]) is a finite quantity derived from the problem domain (Essential Complexity). This mass must be distributed between two primary reservoirs:

- Bucket A (Code): The procedural logic, control flow, algorithms, conditional branching, loops, and temporal steps required to manipulate the system state. This is the domain of _verbs_—actions taken over time.
- Bucket B (Data Structures): The schema, state representation, entity relationships, type definitions, and static organization of information. This is the domain of _nouns_—relationships existing in space (memory).

The core thesis to be validated is that because![][image1] is conserved (Tesler's Law), the hallmark of superior engineering (Torvalds' "Good Programmer") is the strategic displacement of complexity from Bucket A to Bucket B. The hypothesis suggests that complexity housed in data structures is cognitively "cheaper" and architecturally more robust than equivalent complexity housed in code.

#### 1.2 Defining the Axioms

##### 1.2.1 Tesler's Law of Conservation of Complexity

Formulated by Larry Tesler at Xerox PARC in the mid-1980s, the Law of Conservation of Complexity (also known as the Waterbed Theory) asserts that every application has an inherent amount of irreducible complexity.1 Tesler originally framed this in the context of Human-Computer Interaction (HCI): the complexity must be handled by someone—either the engineer writes complex code to make the user's life simple, or the engineer writes simple code that forces the user to handle complex workflows.1

In the context of this report, we extend Tesler's Law inward, past the UI boundary, to the internal architecture. If the complexity is internalized to the system (to spare the user), it must settle somewhere. It effectively becomes a fluid dynamic problem within the codebase: pushing down on the complexity of the data model forces the logic to bulge with exception handling and conditionals.4

##### 1.2.2 Torvalds' Axiom

The second pillar of this dialectic comes from Linus Torvalds, creator of Linux and Git. In a 2006 discussion on the Git mailing list, Torvalds stated:

_"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."_ 5

This perspective aligns with Rob Pike's Rule 5: _"Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming"_.6 It also echoes Fred Brooks in _The Mythical Man-Month_: _"Show me your flowcharts and conceal your tables, and I shall continue to be mystified. Show me your tables, and I won't usually need your flowcharts; they'll be obvious"_.7

#### 1.3 The Synthesis

The synthesis of these two laws suggests a normative claim: Because complexity is conserved (Tesler), we must choose its location. The "Code vs. Data" debate is not about style; it is about choosing the container with the highest structural integrity. Torvalds argues that Data Structures (Bucket B) are that container. This report will rigorously test that claim.

---

1. Theoretical Framework: Entropy and Representation

To validate the statement, we must move beyond aphorisms and establish a theoretical framework for _why_ data structures might handle complexity better than code.

#### 2.1 Essential vs. Accidental Complexity

The distinction between Essential and Accidental complexity, introduced by Fred Brooks in _No Silver Bullet_, is critical for evaluating Bucket allocation.9

| Complexity Type | Definition | Source | Proper Bucket Allocation |
|:---- |:---- |:---- |:---- |
| Essential Complexity | Inherent difficulty of the problem (e.g., US Tax Code, orbital mechanics). | The Domain | Bucket B (Data): Must be modeled explicitly as rules/relationships. |
| Accidental Complexity | Difficulty arising from the solution implementation (e.g., manual memory management, race conditions). | The Tools | Neither: Should be eliminated, but often festers in Bucket A (Code). |

Insight: Torvalds' critique of "bad programmers" largely centers on their tendency to generate Accidental Complexity in Bucket A by failing to properly model Essential Complexity in Bucket B. When the data model (B) fails to capture the nuance of the domain (Essential), the code (A) must become riddled with if-then-else patches to bridge the gap. This confirms Tesler: the complexity didn't disappear; it just manifested as "spaghetti code" instead of a "rich schema".10

#### 2.2 The Cognitive Physics of Code vs. Data

Why is Bucket B superior? The answer lies in human cognitive processing.

1. Temporal vs. Spatial: Code is temporal; it describes a sequence of events over time. To understand a complex function, the programmer must "simulate" the CPU in their head, holding the state of variables as they mutate through loops and branches. This imposes a high Cognitive Load.
2. Static vs. Dynamic: Data structures are spatial and static. A database schema or a struct definition can be visualized as a map. The relationships are explicit and do not depend on "runtime" execution to exist. Humans are evolutionarily adapted to processing spatial maps (visual cortex) more efficiently than abstract temporal sequences (working memory).12

Validation: By shifting complexity to Bucket B, we transform dynamic complexity (which is fragile and hard to test) into static complexity (which is inspectable and distinct). The logic of the statement holds: while the _amount_ of complexity is conserved, its _form_ is transmuted into a state more compatible with human reasoning.

#### 2.3 The Rule of Representation

Rob Pike's "Rule of Representation" provides the mechanism for this shift: _"Fold knowledge into data so program logic can be stupid and robust"_.6

- "Stupid" Code: Code that lacks deep nesting, complex conditionals, or state-dependent side effects. It simply acts as a dumb pipe or a traversal engine.
- "Robust" Data: Data that enforces constraints (e.g., Foreign Keys, Type Systems) such that invalid states are unrepresentable.

If knowledge is folded into data, the code naturally shrinks. For example, a compiler could be written as a massive if-else chain (Bucket A), or as a table of opcodes and patterns (Bucket B). The table approach "conserves" the complexity of the instruction set but removes the accidental complexity of managing control flow.14

---

1. Mechanisms of the Shift: From Imperative to Declarative

To validate the practical application of this logic, we must examine the specific engineering patterns that facilitate the transfer from Bucket A to Bucket B. These mechanisms serve as the "pumps" in our hydraulic complexity model.

#### 3.1 Table-Driven Methods: The Foundational Shift

One of the most direct applications of this philosophy is the Table-Driven Method. This technique explicitly replaces control flow (Bucket A) with memory lookup (Bucket B).

Consider the calculation of insurance premiums based on age and smoking status.

Bucket A Approach (Imperative Logic):

Java

double getRate(int age, boolean isSmoker) {

    if (isSmoker) {

        if (age < 20) return 5.0;

        else if (age < 40) return 7.5;

        else return 10.0;

    } else {

        if (age < 20) return 2.0;

        else if (age < 40) return 3.0;

        else return 4.0;

    }

}

Copy And SaveShareAsk Copilot

- Analysis: The logic is embedded in the control flow. The complexity is measured in Cyclomatic Complexity (the number of independent paths). As the rules grow, the nesting deepens, making the code fragile and hard to test.16

Bucket B Approach (Table-Driven):

The developer creates a data structure (Table) representing the rules.

Java

// Logic becomes "Stupid"

double getRate(int age, boolean isSmoker) {

    return rateTable.get(isSmoker).get(getAgeBracket(age));

}

Copy And SaveShareAsk Copilot

- Analysis: The _logic_ has effectively vanished from the code. The complexity is now housed in rateTable (a CSV, database table, or constant map). The code is robust because adding a new age bracket requires _no code changes_, only data entry. The "complexity" of the insurance rules is conserved (the data table grows), but the _systemic_ complexity is reduced because the Code (A) is decoupled from the Rules (B).14

#### 3.2 Finite State Machines (FSM): Taming the Boolean Salad

A common symptom of "Bad Programmer" syndrome (Bucket A dominance) is the use of extensive boolean flags to track state. This is often pejoratively called "Boolean Salad".19

- The Problem: With 3 boolean flags (isLoading, hasError, isEmpty), there are![][image2] possible states. However, likely only 4 are valid. In Bucket A, the programmer writes complex boolean logic: if (!isLoading && hasError &&!isEmpty). This logic is prone to "impossible state" bugs where the system enters a configuration the programmer didn't anticipate.
- The Solution (Bucket B): Define a Finite State Machine (FSM). The valid states and transitions are defined in a graph structure.
  - Structure: Nodes = States; Edges = Transitions.
  - Code: The code merely executes the transition defined by the graph: currentState = transitions[input].
- Validation: By moving the state logic into a static data structure (the transition table), the code becomes incapable of entering an invalid state (unless the table is wrong). The complexity of managing state transitions is conserved but contained within the strict topology of the graph.20

#### 3.3 Data-Oriented Design (DoD): Performance as Structure

In high-performance domains like game development (Unity DOTS, Unreal Engine), Data-Oriented Design validates Torvalds' axiom by prioritizing memory layout over object abstraction.22

- Bucket A (Object-Oriented): Objects encapsulate data and logic. A Player object contains health, position, and inventory. In memory, an array of Player objects is an "Array of Structures" (AoS).
  - _Complexity:_ Iterating over all players to update positions involves "pointer chasing" and cache misses because position data is interleaved with unrelated data like inventory. The code becomes complex with optimization attempts (prefetching, multi-threading locks).
- Bucket B (Data-Oriented): Data is stripped from objects and organized into contiguous arrays of single types ("Structure of Arrays" - SoA). All positions are in one array; all health in another.
  - _Complexity Shift:_ The complexity moves to the Data Layout. The code becomes a simple loop over a contiguous array: for (i=0; i<count; i++) positions[i] += velocity[i];.
  - _Outcome:_ The algorithm is "self-evident" and blazingly fast because it aligns with the hardware's reality (cache lines). This confirms that "worrying about data structures" (Bucket B) resolves code performance issues (Bucket A).24

---

1. Case Studies: Validating the Theory in the Wild

To move beyond theoretical validation, we must examine real-world software architectures where the allocation of complexity dictated the success or failure of the system.

#### 4.1 The Linux Kernel: A Triumph of Bucket B

Linus Torvalds' own creation, the Linux Kernel, serves as the primary validation of his axiom. The kernel is essentially a massive manager of data structures.

- The Virtual File System (VFS): The VFS does not contain complex if statements checking for filesystem types (e.g., if (type == EXT4)… else if (type == NTFS)…). Instead, it defines a Data Structure: the inode and file_operations struct.
  - The Structure: This struct contains function pointers (read, write, open).
  - The Code: The kernel code is generic: file->f_op->read(…).
  - Analysis: The complexity of supporting 50+ filesystems is completely removed from the core kernel code and pushed into the data structure instances provided by the drivers. If Torvalds had "worried about the code" first, the kernel would contain a monolithic switch statement that would be unmaintainable.5
- Git: Git is famously "content-addressable filesystem" first, and a version control system second. Torvalds designed the Data Structure (the Directed Acyclic Graph of commits, trees, and blobs) before writing the logic.
  - Validation: Because the data structure (DAG) perfectly modeled the problem (history as a graph of snapshots), the code for operations like merge and diff became mathematical consequences of the graph traversal. Complexity was conserved in the SHA-1 hashing and graph/tree objects, leaving the code robust and simple.27

#### 4.2 The Enterprise Tax Engine: A Study in Essential Complexity

Tax calculation represents extreme Essential Complexity. Tax rules change daily, vary by street address, and depend on product categories (e.g., "bagels are tax-free, but sliced bagels are taxable in New York").

- Approach A (Code-Centric):
  - Developers write logic: if (zip == 10001 && item == "sliced_bagel") tax = 0.08875;.
  - _Result:_ A maintenance nightmare. Every legislative change requires a code deployment. The system becomes rigid and opaque. This violates Tesler's Law by trying to hide complexity in code where it cannot be easily managed.28
- Approach B (Data-Centric / Rules Engine):
  - Developers build a Rules Engine. The logic is moved to a database (Bucket B).
  - _Structure:_ Tables for Jurisdictions, TaxRates, ProductCategories, and Rules.
  - _Code:_ The code becomes a generic query builder: SELECT rate FROM Rules WHERE….
  - _Analysis:_ This is the industry standard (e.g., Oracle eBusiness Tax, Vertex). It validates the statement: the complexity of the tax law is conserved, but by moving it to Bucket B, it becomes manageable, updateable without code recompilation, and auditable by non-programmers.30
- The Limit (SaaS): Companies often outsource this to APIs (Avalara). Here, Tesler's complexity is conserved but shifted entirely out of the local system to a vendor, proving the "Waterbed Theory" applies across organizational boundaries too.33

---

1. The Pathologies of Displacement: Refuting the Absolutism

While the logic holds that Bucket B is generally superior, the validation is not absolute. There are scenarios where shifting complexity to data structures creates _more_ problems, refuting a naive application of the principle.

#### 5.1 The Inner-Platform Effect

The most significant counter-argument is the Inner-Platform Effect. This occurs when an architect, zealous about emptying Bucket A, creates a data structure (Bucket B) so complex that it becomes a programming language itself.35

- Scenario: A "Business Rules Engine" allows users to define rules in the database.
- Evolution: Users ask for "AND/OR" logic. Then "Variables". Then "Loops".
- Outcome: The database now contains XML or JSON strings that are effectively code.
- The Refutation: You have not reduced complexity; you have merely moved Code into a container (Database) that lacks compilers, debuggers, version control, and syntax highlighting.
- Verdict: This validates Tesler's Law (complexity is conserved) but violates Torvalds' implied goal of quality. A bad data structure that mimics code is worse than bad code. "Soft Coding" leads to "Configuration Hell" where the system's behavior is undeterminable from the source code.37

#### 5.2 The Anemic Domain Model

In Object-Oriented design, an over-reliance on separating Code and Data can lead to the Anemic Domain Model anti-pattern.

- Bucket B (Data): Classes are just bags of getters/setters (Data Transfer Objects).
- Bucket A (Code): "Service" classes contain all the logic.
- Critique: While this separates A and B, it violates the OOP principle of encapsulation. The logic (Code) is decoupled from the data it validates, leading to potential inconsistencies where data can exist in an invalid state because the validation logic wasn't called. This suggests that a _strict_ separation isn't always the "Good Programmer" trait in OOP contexts; sometimes, the Code must guard the Data tightly.40

#### 5.3 Cognitive Load Transfer

While static data is generally easier to parse, extremely complex data structures can exceed human cognitive limits.

- A SQL query with 15 JOINs and subqueries is technically "declarative data," but it is arguably harder to understand than a well-written imperative loop.
- Refutation: If the "relationships" in Bucket B become a "graph spaghetti" (e.g., cyclic dependencies in a dependency injection container), the system becomes just as unmanageable as "code spaghetti." Complexity conservation means you can drown in data just as easily as you can drown in code.10

---

1. Second-Order Insights: Implications for Modern Architecture

Validating this logic reveals deeper trends in the evolution of software engineering.

#### 6.1 The Rise of "Infrastructure as Code" (IaC)

IaC (Terraform, Kubernetes YAML) is a massive validation of shifting Bucket A to Bucket B.

- Old World (Bucket A): Sysadmins wrote Bash scripts (Imperative Code) to configure servers. apt-get install nginx, service start. Fragile, state-dependent.
- New World (Bucket B): Engineers write YAML files (Declarative Data) describing the _desired state_. replicas: 3, image: nginx.
- Mechanism: The complexity of _how_ to reach that state is pushed into the Kubernetes engine (essential complexity conserved), but the user manages only the structural definition. This confirms that "Good DevOps" worry about the YAML (Data), not the script (Code).43

#### 6.2 Microservices and API Contracts

In distributed systems, Data Structures (API Schemas, Protobufs, JSON) become the primary architectural constraint.

- Insight: Conway's Law implies that the Data Structure is the "contract" between teams. "Good Architects" obsess over these contracts (Bucket B). If the schema is flawed, no amount of clever code (Bucket A) in the microservices can fix the distributed system's problems. This elevates Torvalds' axiom from a single-process insight to a distributed-system imperative.10

#### 6.3 The "No-Code" Movement

The modern "No-Code" movement is essentially the commoditization of the Inner-Platform Effect, but managed by vendors.

- Mechanism: It attempts to turn all of Bucket A (Code) into Bucket B (GUI configuration).
- Tesler's Law Application: The complexity doesn't vanish; it is hidden behind the drag-and-drop interface. When the user hits the limits of the GUI, they hit the "cliff" of Tesler's Law—the irreducible complexity that the GUI cannot express, forcing a return to Code.2

---

1. Synthesis and Final Validation

#### 7.1 The Conservation Validated

The report confirms that Tesler's Law is immutable. Every shift of logic from Code to Data requires a corresponding increase in the sophistication of the Data interpreter.

- Removing if statements requires adding a Rules Engine.
- Removing manual memory management (Code) requires a Garbage Collector (Runtime Complexity).
- Removing imperative UI logic requires a React Virtual DOM (Data Structure Complexity).

#### 7.2 The Allocation Validated

The report confirms that Torvalds' Allocation Strategy is optimal.

- Stability: Data Structures change slower than Code. Basing the architecture on the stable element reduces churn.
- Visibility: Data Structures are inspectable. You can query a database to see the state; you cannot easily "query" a running thread's instruction pointer history.
- Constraints: Data Structures allow for the enforcement of validity (Type safety, Referential integrity). Code can do anything, which means it can do the _wrong_ thing. Data structures restrict the search space of possible bugs.

Table 2: The Validated Matrix of Complexity Allocation

| Strategy | Focus | Resulting Architecture | Tesler's Law Outcome | Verdict |
|:---- |:---- |:---- |:---- |:---- |
| Naive Code | Bucket A | Sprawling if-else logic, hard-coding. | Complexity exposed to developer as maintenance burden. | Refuted (Bad) |
| Smart Data | Bucket B | Table-driven, State Machines, Schemas. | Complexity captured in static models. Code is trivial. | Validated (Good) |
| Over-Data | Bucket B++ | Inner-Platform, Config Hell. | Complexity hidden in untyped/untested data layers. | Refuted (Dangerous) |

#### 7.3 Conclusion

The logic of the statement is VALID, provided one accepts the constraint that Data Structures must be designed, not just populated.

Torvalds does not merely say "use data." He says "worry about data structures and their relationships." This implies that the intellectual effort of the programmer must be spent on Information Architecture. When the topology of the data matches the topology of the problem (Essential Complexity), the Code (Accidental Complexity) evaporates, leaving behind a system that is robust, performant, and understandable.

The "Good Programmer" acts as a physicist of information, using Tesler's Law not as a constraint to be fought, but as a guide to identifying the lowest-energy state for the system's logic—a state that is almost invariably found within the rigid, crystalline lattice of a Data Structure, rather than the fluid, chaotic flux of Procedural Code.
