---
created: 2026-01-24T08:28:03+00:00
modified: 2026-01-29T07:18:10+00:00
tags: [llm-understanding]
title: Code vs. Data Structures_ A Discussion
---

## 1. Introduction: The Ontology of Software Design

In the annals of software engineering, few pronouncements have reverberated with as much persistence and polarizing clarity as the observation made by Linus Torvalds on the Git mailing list in June 2006. In the midst of a technical discussion regarding the implementation of the Git version control system, Torvalds asserted: "Bad programmers worry about the code. Good programmers worry about data structures and their relationships". While frequently deployed as a rhetorical bludgeon in debates regarding developer competence, this aphorism encapsulates a profound architectural philosophy that transcends the specific context of kernel development or version control. It serves as a modern articulation of a fundamental principle regarding the nature of computing: the primacy of state representation over state manipulation.

This report provides an exhaustive analysis of the implications of this quote, dissecting the dichotomy between "code-centric" and "data-centric" design. The "bad programmer," in this framework, is characterized not by malice or lack of intelligence, but by a misplaced focus on the imperative—the transient "how" of execution flows, conditional branches, and loops. Conversely, the "good programmer" focuses on the declarative—the static "what" of the system's ontology, encoded in the topology of data structures. The central thesis presented here is that software complexity obeys a conservation law: it must reside either in the procedural logic (the code) or the structural representation (the data). When complexity is shifted to the data structure, the corresponding code collapses into simplicity, becoming robust, maintainable, and performant.

To fully explore this concept, this report synthesizes historical perspectives from computer science luminaries, conducts a forensic technical analysis of the Git architecture, examines the hardware-level imperatives of Data-Oriented Design (DOD), and evaluates the economic consequences of schema refactoring versus code refactoring.

### 1.1 The Definition of Terms

To proceed with rigor, we must define the terms "code" and "data structures" as they function within this architectural dialectic.

- "Worrying about the code" refers to an obsession with the control flow of the application. It manifests as a reliance on complex algorithms to compensate for inadequate modeling. The code-centric developer views the program as a series of verbs—actions to be performed. They solve ambiguity by adding more instructions: nested if-else blocks, elaborate exception handling, and flags to track state that is not inherently captured by the model. This approach often leads to high cyclomatic complexity, where the number of linearly independent paths through the program source code explodes, making the system fragile and difficult to test.
- "Worrying about data structures" refers to the prioritization of the system's memory layout, schema, and entity relationships. The data-centric developer views the program as a set of nouns—entities that exist in a defined relationship to one another. They invest significant effort up-front to design structures (trees, graphs, hash maps, relational tables) that naturally enforce the constraints of the problem domain. When the data structure is "smart," the code required to manipulate it becomes "dumb"—often reducing to simple traversals, lookups, or iterations.

### 1.2 The Scope of Analysis

This report is structured to guide the reader from the theoretical underpinnings of this philosophy to its concrete application in modern high-performance computing.

1. Theoretical Foundations: We examine the intellectual lineage of the "Data Dominates" principle, tracing it from Fred Brooks to Rob Pike and Eric Raymond.
2. Case Study: Git: We perform a deep architectural review of Git, demonstrating how Torvalds applied his own principle to solve the problem of distributed version control through a Directed Acyclic Graph (DAG).
3. Hardware Reality (DOD): We analyze the physical implications of data structures on modern hardware, focusing on cache locality, SIMD, and the performance costs of Object-Oriented Programming (OOP) abstractions.
4. Algorithmic Simplification: We explore how Table-Driven Methods and Rule Engines replace complex control flow with data lookups, effectively turning logic into data.
5. Economic Implications: We evaluate the long-term maintenance costs of code vs. data, arguing that schema design is the highest-leverage activity in software engineering.

## 2. The Intellectual History of Data Dominance

Torvalds' assertion was not an act of spontaneous generation. It was a crystallization of wisdom that had been accumulating in the computer science community for decades. To understand the depth of the "data vs. code" debate, one must examine the precursors who identified that the essence of software lies in representation, not calculation.

### 2.1 Fred Brooks and the Mythical Man-Month

In 1975, Fred Brooks published _The Mythical Man-Month_, a foundational text on software engineering management. Within it, he offered an observation that serves as the direct ancestor to Torvalds' quote: "Show me your flowcharts and conceal your tables, and I shall continue to be mystified. Show me your tables, and I won't usually need your flowcharts; they'll be obvious".

At the time of Brooks' writing, flowcharts were the dominant method for documenting software logic. They represented the "code"—the decision paths, loops, and jumps. Tables represented the "data"—the memory layout and storage schema. Brooks realized that the flowchart was merely a transient map of a journey through the data. If one understood the destination and the terrain (the tables), the route (the flowchart) became self-evident. Conversely, seeing the route without knowing the terrain provided no insight into the system's purpose.

Implication: Brooks identified that representation is the essence of programming. If a developer can precisely define the data model, the algorithm often reveals itself as a natural consequence. For example, if a data structure is defined as a sorted binary tree, the algorithm to find a value is implicitly defined (binary search). If the data structure is an unsorted array, the algorithm is forced to be a linear search. The structure dictates the code.

### 2.2 Rob Pike's Rule 5

Rob Pike, a key figure in the development of Unix, Plan 9, and the Go programming language, codified this philosophy in his famous "Notes on Programming in C" (1989). His "Rule 5" states: "Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming".

Pike's formulation adds a critical nuance: cognitive load. He argues that the complexity of data structures is easier for the human mind to manage than the complexity of algorithms. A complex algorithm requires the programmer to mentally simulate the CPU's state step-by-step—a process prone to "off-by-one" errors and logic gaps. A complex data structure, however, can often be visualized statically (e.g., drawing a graph on a whiteboard). Because humans are visual creatures, we can reason about static relationships more effectively than dynamic processes.

### 2.3 Eric Raymond and the "Smart Data" Principle

Eric Raymond, in his analysis of the open-source movement (_The Cathedral and the Bazaar_), synthesized these ideas into the "Smart Data Structures and Dumb Code" principle. He argued: "Smart data structures and dumb code works a lot better than the other way around".

Raymond's contribution helps define the "Good Programmer." The good programmer actively seeks to move complexity _out_ of the code and _into_ the data.

- Dumb Data / Smart Code: A system that stores data in a flat text file (dumb data) requires a complex parser and error-checking logic (smart code) to read it.
- Smart Data / Dumb Code: A system that stores data in a structured SQL database or a self-describing format like JSON (smart data) requires only a simple library call to read it (dumb code).

This historical lineage confirms that Torvalds' quote is not merely an opinion on coding style, but a fundamental law of software architecture: The clarity of the code is directly proportional to the fitness of the data structure.

## 3. Case Study: Git and the Architecture of the DAG

The most potent demonstration of the "Data Dominates" principle is the architecture of Git itself. To understand why Torvalds believes "good programmers worry about data structures," we must examine how he applied this belief to build the world's most dominant version control system (VCS) in roughly ten days in 2005.

### 3.1 The Problem Space

Before Git, version control systems like CVS and Subversion (SVN) focused on "deltas"—the differences between files. They conceptualized version control as a series of patches applied to a base file. This is a "code-centric" view: it focuses on the _action_ of changing a file (the delta).

When the Linux kernel team lost their license to use BitKeeper, Torvalds needed a replacement that supported distributed development, massive scale, and data integrity. He did not start by writing the code to "commit" or "merge." He started by designing the data structure.

### 3.2 The Data Structure: A Content-Addressable DAG

Git is, at its core, a content-addressable filesystem. It does not store "changes"; it stores snapshots of the entire project, but it does so using a highly efficient data structure that deduplicates content automatically.

The Git object database consists of four primary immutable object types, defined solely by the SHA-1 hash of their content:

| Object Type | Description | Relationship to Data Structure |
|:---- |:---- |:---- |
| Blob | Binary Large Object. Stores file content. | The leaf node. Contains no metadata (no filename), just data. Identified by hash. |
| Tree | Represents a directory. | The structural node. Contains a list of pointers (hashes) to Blobs or other Trees, along with filenames. |
| Commit | Represents a snapshot in time. | The history node. Points to a root Tree and to parent Commit(s). Contains metadata (author, message). |
| Tag | A named pointer to a commit. | A reference node. Used to mark specific points in history (e.g., v1.0). |

The "Smart" Data Structure: Because every object is named by the hash of its contents, the data structure enforces integrity and deduplication by definition.

- Integrity: If a single bit in a file changes, its hash changes. If the hash changes, the Tree pointing to it must change. If the Tree changes, the Commit pointing to it must change. This forms a Merkle Tree, where the root hash uniquely identifies the entire state of the project history.
- Deduplication: If two files in different directories are identical, they hash to the same Blob. Git stores the Blob only once. Code logic is not required to check for duplicates; the hashing algorithm guarantees it.

### 3.3 How the DAG Solves Merging

The true genius of Git's data structure is how it simplifies the complex problem of merging. In code-centric VCS (like SVN), merging is a heuristic nightmare involving tracking line numbers and file revisions. In Git, merging is a graph traversal problem.

Git's history is a Directed Acyclic Graph (DAG) of commit objects.

- Nodes: Commits.
- Edges: Pointers to parent commits.
- Direction: Child points to Parent (backwards in time).

When a developer wants to merge Branch A and Branch B, Git acts as a "Good Programmer" by relying on the graph:

1. Find the Common Ancestor: Git traverses the DAG back from the tips of A and B to find the best common ancestor (the "merge base"). Because the history is a rigorous graph, this is a deterministic mathematical operation, not a guess.
2. Three-Way Merge: Git performs a three-way merge between the Base, Tip A, and Tip B.
3. Create Merge Commit: A new commit is created with _two_ parents (Tip A and Tip B), creating a diamond shape in the graph.

The "Dumb" Code: Because the DAG structure preserves the exact history of how branches diverged and converged, the merge algorithm does not need to be "smart" about guessing context. The context is encoded in the graph. As noted in the research, "The only thing special about Git's DAG is that you can join branches back together again… Merges in Git reduce confusion… you never have to remember by hand which changes are which".

### 3.4 Performance Implications

The data-centric design also yields massive performance benefits.

- Comparison: To determine if a project has changed between Version A and Version B, Git compares the SHA-1 hash of the root Trees. If they match, the projects are identical. O(1) complexity. If they differ, it recurses only into the sub-trees that differ. A code-centric system would have to walk the entire file system, comparing file by file (O(N)).
- Speed: Mozilla tests showed Git to be orders of magnitude faster than other VCSs because of this structure.

Torvalds explicitly attributed Git's success to this philosophy: "Git actually has a simple design, with stable and reasonably well-documented data structures. In fact, I'm a huge proponent of designing your code around the data… I will, in fact, claim that the difference between a bad programmer and a good one is whether he considers his code or his data structures more important".

## 4. The Hardware Reality: Data-Oriented Design (DOD)

While Torvalds focuses on the logical elegance of data structures, a parallel discipline known as Data-Oriented Design (DOD) arrives at the same conclusion from the opposite direction: hardware physics. In high-performance computing (game engines, simulations, finance), the "bad programmer" is one who designs data structures that ignore how modern CPUs function.

### 4.1 The Lie of Object-Oriented Programming (OOP)

For decades, Object-Oriented Programming (OOP) has been the dominant paradigm. OOP encourages programmers to model the world as "Objects"—self-contained units of data and behavior. This aligns with human intuition but clashes with hardware reality.

The Problem: Cache Misses Modern CPUs are vastly faster than main memory (RAM). To bridge this gap, CPUs use caches (L1, L2, L3). The CPU fetches data in "cache lines" (typically 64 bytes). If the data the CPU needs is in the cache, it is processed instantly. If not (a "cache miss"), the CPU stalls for hundreds of cycles waiting for RAM.

OOP typically organizes data as an Array of Structures (AoS).

- Example: A Ball object contains x, y, z (position) and r, g, b (color) and sprite\_id (texture).
- Memory: \[x,y,z, r,g,b, id\]\[x,y,z, r,g,b, id\]…
- Scenario: A physics loop needs to update the position of 10,000 balls. It does not need the color.
- Inefficiency: When the CPU loads the first ball's position, it also loads the color and texture data into the cache line. This irrelevant data wastes cache space ("cache pollution"). Furthermore, because objects are often allocated individually on the heap (using new), they may be scattered randomly in memory, preventing the CPU's pre-fetcher from predicting the next memory address.

### 4.2 The DOD Solution: Structure of Arrays (SoA)

The "Good Programmer" (in DOD terms) worries about the memory layout. They utilize a Structure of Arrays (SoA) approach.

- Memory:
  - Array 1 (Positions): \[x,y,z\]\[x,y,z\]\[x,y,z\]…
  - Array 2 (Colors): \[r,g,b\]\[r,g,b\]\[r,g,b\]…
- Efficiency: When the physics loop runs, the CPU loads _only_ position data. Every byte in the cache line is used. The CPU pre-fetcher can stream the contiguous array into the cache, maximizing throughput.

### 4.3 Quantifiable Performance Differences

The impact of this "worrying about data structures" is not theoretical; it is measurable.

- Ball Simulation Case Study: A developer compared an OOP implementation of a ball-spawning game against a DOD implementation on an iPhone 16 Pro. The logic (the physics math) was identical. The OOP version supported \~600 balls before dropping below 60 FPS. The DOD version, using contiguous arrays, supported \~6,000 balls—a 10x performance improvement.
- AI Algorithms: Research into AI systems shows that DOD implementations result in significantly lower cache miss rates and fewer system calls, leading to superior execution times for large datasets.
- SIMD: DOD layouts allow the use of Single Instruction, Multiple Data (SIMD) instructions. Because the data is contiguous and homogenous (e.g., 4 floats representing 'x' positions side-by-side), the CPU can update 4 or 8 balls in a single clock cycle. OOP objects usually prevent this optimization.

In this context, the "bad programmer" writes code that looks clean on screen (classes, inheritance) but thrashes the hardware. The "good programmer" designs data structures (arrays, pools, archetype tables) that respect the silicon.

### 4.4 Entity Component Systems (ECS)

The ultimate expression of DOD in game development is the Entity Component System (ECS). In ECS, an "Entity" is not an object; it is merely an ID (an integer). "Components" are pure data (structs) stored in contiguous arrays. "Systems" are the code that iterate over these arrays.

- Separation: Data (Components) is strictly separated from Code (Systems).
- Composition: An entity consists of "Position \+ Velocity \+ Renderable."
- Result: This architecture solves the "fragile base class" problem of OOP (logic entanglement) _and_ the cache locality problem simultaneously.

## 5. Algorithmic Simplification: Table-Driven Methods

Moving up from the hardware level to the application logic level, Torvalds' principle manifests in the technique known as Table-Driven Methods. This approach addresses the complexity of control flow by replacing if-else and switch statements with data lookups.

### 5.1 The Cyclomatic Complexity Trap

A hallmark of the "bad programmer" is the reliance on extensive conditional logic to handle state. Consider a command dispatcher for a chatbot or a game:

The Code-Centric Approach (Giant Switch):

`def handle_command(command):`

    `if command == "SAVE":`

        `save_game()`

    `elif command == "LOAD":`

        `load_game()`

    `elif command == "ATTACK":`

        `perform_attack()`

    `elif command == "DEFEND":`

        `perform_defend()`

    `#… 50 more elifs…`

    `else:`

        `print("Unknown command")`

This structure, often called the "Giant Switch Statement" or "Switch Tower," is an anti-pattern.

1. Readability: It is physically long and hard to scan.
2. Maintainability: Adding a command requires modifying the core function, increasing the risk of introducing syntax errors or breaking existing logic.
3. Performance: In many languages, an if-elif chain is a linear search (O(N)). The CPU must evaluate each condition sequentially.

### 5.2 The Data-Centric Solution (Dictionary Dispatch)

The "good programmer" recognizes that the mapping between a command string and an action is _data_, not logic. They refactor this into a lookup table (Dictionary or Hash Map).

The Data-Centric Approach:

`# The Data Structure defines the relationship`

`command_map = {`

    `"SAVE": save_game,`

    `"LOAD": load_game,`

    `"ATTACK": perform_attack,`

    `"DEFEND": perform_defend`

`}`

`# The Code is generic and "dumb"`

`def handle_command(command):`

    `action = command_map.get(command, default_handler)`

    `action()`

This transformation yields significant benefits:

- Algorithmic Efficiency: Dictionary lookups are typically O(1) (constant time) or O(log N), vastly faster than linear if-else chains for large datasets.
- Dynamic Extensibility: The command\_map can be modified at runtime. New commands can be loaded from a configuration file or a plugin system without recompiling the core execution loop.
- Reduced Complexity: The handle\_command function has a cyclomatic complexity of 1 (a single path). It never needs to change, even if the system grows to support 1,000 commands.

### 5.3 Finite State Machines (FSM)

The distinction is even more critical in state machine design.

- Code-Driven FSM: Implementing a state machine using nested switch statements (Switch on State \-\> Switch on Event) results in "spaghetti code" where transitions are buried in logic blocks. Debugging requires stepping through complex execution paths.
- Table-Driven FSM: The state machine is defined as a transition table (2D array or database).
  - Rows: Current State
  - Columns: Input Event
  - Cell: Next State The "code" is a generic engine: NextState \= TransitionTable\[Input\].
  - Implication: The logic of the system is entirely visible in the table. One can verify the system's behavior by inspecting the data, without reading a single line of code.

### 5.4 Pattern Matching in Modern Languages

Modern languages are evolving to support this data-centric approach natively. Python 3.10 introduced match-case, which provides a structured way to handle pattern matching, effectively blending the readability of a switch statement with the power of data destructuring. However, even with these tools, the underlying principle remains: whenever logic can be represented as a static relationship in a data structure, it should be.

## 6. Enterprise Architecture: Logic as Data

In large-scale enterprise systems, the "data vs. code" problem scales up to the level of business rules. Here, the "bad programmer" hardcodes business policies (e.g., insurance premiums, tax rates, eligibility criteria) into the application code.

### 6.1 The Fragility of Hardcoded Logic

Business rules change faster than software release cycles. If an insurance company changes a premium calculation for drivers under 25, and that logic is embedded in a Java if statement, the company must:

1. Update the code.
2. Recompile the application.
3. Run regression tests.
4. Redeploy the application. This latency is unacceptable in modern business. Furthermore, embedding rules in code makes them opaque to business analysts, who cannot read Java or C\#.

### 6.2 Rule Engines and the Rete Algorithm

The "good programmer" externalizes this logic into a Rule Engine (e.g., Drools, JBoss Rules). In this architecture, business rules are defined as _data_—often in decision tables or domain-specific languages (DSLs) that resemble spreadsheets.

- Data: "IF Age \< 25 AND Car \= 'Sports' THEN Premium \= Premium \ 1.2"
- Code: The Rule Engine generic software that reads these rules and applies them to facts.

The Rete Algorithm: Rule engines use the Rete algorithm, a sophisticated data structure approach to pattern matching. Instead of iterating through every rule for every fact (which would be slow), the Rete algorithm compiles the rules into a discrimination network (a directed acyclic graph).

- Nodes: Conditions (e.g., "Age \> 18").
- Token Passing: When a fact (data) enters the system, it traverses the graph. Partial matches are cached in the nodes.
- Efficiency: This structure allows the engine to evaluate thousands of complex rules against thousands of facts with incredible speed, far outperforming naive procedural code written by a developer.

By treating logic as data, the system achieves Separation of Concerns: the stability of the application infrastructure is decoupled from the volatility of business policy.

\---

## 7. The Economics of Maintenance: Code vs. Schema

Perhaps the most compelling argument for Torvalds' principle is economic. In the lifecycle of a software project, the cost of changing data structures is orders of magnitude higher than the cost of changing code.

### 7.1 The Asymmetry of Refactoring

- Code Refactoring: Changing a function's internal logic, renaming variables, or extracting methods is cheap. Modern IDEs automate these tasks. If code is broken, it can be reverted via Version Control (Git) instantly.
- Data Refactoring (Schema Migration): Changing the database schema is expensive and risky.
  - Data Gravity: Data has mass. You cannot simply "revert" a database schema change if it involved transforming terabytes of live customer data.
  - Coupling: A database schema is often shared by multiple applications (the website, the mobile API, the reporting system). Changing a column name breaks all of them simultaneously.
  - Downtime: Schema migrations often require locking tables, causing system downtime.

### 7.2 The "Ossification" of Data

Data structures tend to "ossify" or harden over time. Once an API is public, its request/response format (its data structure) is frozen. Once a database reaches a certain size, its schema is frozen by the sheer inertia of the data.

The "bad programmer" rushes the data design to get to the coding phase, creating a schema that does not accurately reflect the domain (e.g., assuming a user has only one address). As the system grows, this incorrect assumption becomes a structural rot that no amount of clever code can fix. The code becomes a mess of "hacks" and "workarounds" trying to bridge the gap between the reality of the business and the inadequacy of the data model.

The "good programmer" spends disproportionate time up-front designing the data model (the "bones" of the application). They normalize the database, define strict API contracts, and ensure the relationships (1:1, 1:N, N:M) are correct. They know that if the bones are strong, the flesh (the code) can be healed or replaced. If the bones are broken, the organism dies.

### 7.3 Technical Debt as Schema Debt

Technical debt is often discussed in terms of "messy code." However, the most toxic form of technical debt is Schema Debt. A messy function can be rewritten in an afternoon. A messy database schema can take years to migrate. Torvalds' admonition to "worry about data structures" is essentially a risk management strategy: prioritize the decisions that are hardest to undo.

## 8. Conclusion: The Algorithm is the Shadow

The synthesis of these perspectives—historical, architectural, hardware-level, and economic—reveals that Linus Torvalds' quote is not a mere preference, but a descriptive law of software dynamics.

1. Epistemological Truth: As Brooks and Pike showed, the data structure is the truth of the system; the code is merely a mechanism for translation. To understand a system, one must look at its state, not its transitions.
2. Architectural Validity: Git proves that a superior data structure (DAG) can trivialize complex distributed computing problems (merging), rendering "smart" code unnecessary.
3. Physical Reality: Data-Oriented Design proves that aligning software with hardware memory structures is the primary driver of performance, exposing the inefficiencies of code-centric abstractions like OOP.
4. Economic Prudence: The high cost of schema refactoring dictates that data modeling yields the highest Return on Investment (ROI) of any engineering activity.

In the final analysis, the "bad programmer" sees the data structure as a container for their code—a passive bucket to hold the results of their clever algorithms. The "good programmer" sees the code as a servant of the data structure—a transient, replaceable layer that exists solely to maintain the integrity of the system's relationships.

As we move into an era of AI-generated code, this distinction becomes even more vital. AI can generate "dumb code" with ease—it can write the boilerplate, the loops, and the API calls. But it relies on the human architect to define the schema, the constraints, and the relationships. The role of the human engineer is shifting away from writing the imperative "how" and toward defining the declarative "what." In this future, the programmer who worries about the code will be obsolete; the programmer who worries about data structures will be the architect of the new machine.

The algorithm is merely the shadow cast by the data structure. To change the shadow, one must not shout at the ground; one must move the object.

Citations:.

### Works Cited

1. Quote by Linus Torvalds: "Bad programmers worry about the code. Good prog…" \- Goodreads, <https://www.goodreads.com/quotes/1188397-bad-programmers-worry-about-the-code-good-programmers-worry-about> 2. C++ if statement alternatives \- Stack Overflow, <https://stackoverflow.com/questions/3149422/c-if-statement-alternatives> 3. Table-driven tennis scoring, <https://blog.ploeh.dk/2021/03/29/table-driven-tennis-scoring/> 4. Eric Raymond: Smart data structures \- Quite a Quote\!, <https://quiteaquote.in/2025/01/24/eric-raymond-smart-data-structures/> 5. There is a quote by Linus Torvalds that is relevant here: "Bad programmers worry… | Hacker News, <https://news.ycombinator.com/item?id=17580598> 6. IEEE Software \- The Pragmatic Designer: Principle of Least Expressiveness, <https://www.georgefairbanks.com/ieee-software-v36-n3-may-2019-principle-of-least-expressiveness> 7. Event Modeling Traditional Systems, <https://eventmodeling.org/posts/event-modeling-traditional-systems/> 8. The Road to Hell is Paved with Bioinformatics Formats, <http://omicsomics.blogspot.com/2015/08/the-road-to-hell-is-paved-with.html> 9. Basics of the Unix Philosophy, <https://cscie2x.dce.harvard.edu/hw/ch01s06.html> 10. Rule 5. Data dominates. If you've chosen the right data structures and organiz, <https://news.ycombinator.com/item?id=24136592> 11. Torvalds' quote about good programmer \[closed\] \- Software Engineering Stack Exchange, <https://softwareengineering.stackexchange.com/questions/163185/torvalds-quote-about-good-programmer> 12. Eric S. Raymond Quote: "Smart data structures and dumb code works a lot better than the other way around." \- QuoteFancy, <https://quotefancy.com/quote/1583431/Eric-S-Raymond-Smart-data-structures-and-dumb-code-works-a-lot-better-than-the-other-way> 13. Laws of Programming \- Medium, <https://medium.com/@barisozmen/laws-of-programming-cbec3559f12f> 14. Git \- Wikipedia, <https://en.wikipedia.org/wiki/Git> 15. Git was built in 5 days \- Graphite, <https://graphite.com/blog/understanding-git> 16. 10.2 Git Internals \- Git Objects, <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects> 17. DAG (Directed Acyclic Graph): Definition, Examples, and Applications, <https://www.graphapp.ai/engineering-glossary/git/dag-directed-acyclic-graph> 18. The Git Graph. A Directed Acyclic Graph (DAG) | by Andreas 🎧 Kagoshima \- Medium, <https://medium.com/@a.kago1988/why-the-git-graph-is-a-directed-acyclic-graph-dag-f9052b95f97f> 19. Git's DAG is just a bunch of branches \- apenwarr, <https://apenwarr.ca/log/20090310> 20. Linus Torvalds: Git proved I could be more than a one-hit wonder | Hacker News, <https://news.ycombinator.com/item?id=21418033> 21. When to use objects vs more a data oriented approach: r/cpp\_questions \- Reddit, <https://www.reddit.com/r/cpp>\_questions/comments/1k8ta3o/when\_to\_use\_objects\_vs\_more\_a\_data\_oriented/ 22. Data-Oriented vs Object-Oriented Design | by Jonathan Mines …, <https://medium.com/@jonathanmines/data-oriented-vs-object-oriented-design-50ef35a99056> 23. Impact of Data-Oriented and Object-Oriented Design on Performance and Cache Utilization with Artificial Intelligence Algorithms in Multi-Threaded CPUs † \- † thanks \- arXiv, <https://arxiv.org/html/2512.07841v1> 24. Memory layout in Javascript \- data-oriented vs object-oriented design \- Stack Overflow, <https://stackoverflow.com/questions/25041236/memory-layout-in-javascript-data-oriented-vs-object-oriented-design> 25. The benefit of DOD vs OOP. Actual example with code, in Unity (no ECS). \- Reddit, <https://www.reddit.com/r/gamedev/comments/1ip0v09/the>\_benefit\_of\_dod\_vs\_oop\_actual\_example\_with/ 26. What is Data-Oriented Game Engine Design? | Envato Tuts+ \- Code, <https://code.tutsplus.com/what-is-data-oriented-game-engine-design--cms-21052a> 27. Do GML switch-case statements perform worse than function tables?, <https://softwareengineering.stackexchange.com/questions/460532/do-gml-switch-case-statements-perform-worse-than-function-tables> 28. c\# \- Large Switch statements: Bad OOP? \- Stack Overflow, <https://stackoverflow.com/questions/505454/large-switch-statements-bad-oop> 29. What Is Python Switch Case And Why Should You Master It Before Interviews \- Verve AI, <https://www.vervecopilot.com/hot-blogs/python-switch-case-interviews> 30. 5 Easy Ways to Replace Switch Case in Python \- Analytics Vidhya, <https://www.analyticsvidhya.com/blog/2024/01/replace-switch-case-in-python/> 31. Using a Dictionary to switch—PythonCert 5.0 documentation \- UW PCE: Python Certificate, <https://uwpce-pythoncert.github.io/PythonCertDevel/modules/DictionaryAsSwitch.html> 32. Table-Driven or Event-Driven state machines \[x-post from /r … \- Reddit, <https://www.reddit.com/r/C>\_Programming/comments/1vats8/tabledriven\_or\_eventdriven\_state\_machines\_xpost/ 33. Table-driven approach \- strchr.com, <https://www.strchr.com/table-driven> 34. Replacement of switch statement in Python? \- Spark By {Examples}, <https://sparkbyexamples.com/python/replacement-for-switch-statement-in-python/> 35. Decision Engine vs Rules Engine: Differences, Use Cases, and Benefits | Nected Blogs, <https://www.nected.ai/us/blog-us/decision-engine-vs-rules-engine> 36. Real-World Rule Engines \- InfoQ, <https://www.infoq.com/articles/Rule-Engines/> 37. TDD–Test Driven Development | Pearls of Wisdom \- For Agile Software Methodology, <https://agilepearls.wordpress.com/tag/tdd-test-driven-development/> 38. Architecture Refactoring | Pearls of Wisdom \- For Agile Software Methodology, <https://agilepearls.wordpress.com/tag/architecture-refactoring/>
