---
type: tmp_atoms
status: tmp
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
captured_utc: '2026-09-19T00:00:00+00:00'
signal_to_noise: 70% signal / 30% noise
permalink: llmeon/00-inbox/tmp-atoms-data-structures-vs-control-flow
---

## Noise Removed

- The 47-entry numbered "Works cited" bibliography — link-list noise, not atomic content.
- A verbatim second copy of the full essay appended after the critique (lines ~243–376 of the source) — exact duplicate of content already extracted, discarded as redundant.
- Motivational/rhetorical framing ("the pinnacle of system design", "a relentless struggle against complexity") — underlying claims kept, framing discarded.

## Atoms

### Atom 001: Tesler's Law of Conservation of Complexity (Scoped)
- Kind: claim
- Statement: Software has an inherent amount of complexity dictated by its problem domain that can be relocated between a system's layers (interface, code, data) but not eliminated by any single layer absorbing it.
- Scope & Conditions: Applies specifically to essential/irreducible complexity per Tesler's original postulate, not to total system complexity — Tesler's own wording concedes that reducible complexity exists and can genuinely be destroyed.
- Evidence: "Tesler...observed that this inherent complexity behaves much like mass or energy in physics; it cannot be legislated out of existence." / "Tesler postulated that every application has an inherent amount of irreducible complexity, and the only question is who has to deal with it. That wording concedes that reducible complexity exists."
- Implications:
    - Simplifying one layer (e.g. UI) forces another layer (code) to absorb the corresponding complexity.
    - The Law only constrains the portion of complexity that is genuinely irreducible.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: medium
- Tags: [complexity, tesler-law, software-architecture, conservation]

### Atom 002: Essential vs Accidental Complexity (Brooks)
- Kind: definition
- Statement: Software difficulty splits into essential complexity (inherent to the problem domain itself) and accidental complexity (self-inflicted by the tools, languages, and implementation choices used to solve it).
- Scope & Conditions: From Fred Brooks's 1986 "No Silver Bullet"; essential complexity is argued to be constant across representations.
- Evidence: "Essential complexity is defined as the inherent, unavoidable difficulty of the problem itself... Accidental complexity, conversely, is the self-inflicted friction introduced by the tools, programming languages, and implementation paradigms chosen by the developers."
- Implications:
    - A framework or paradigm can only ever reduce accidental complexity, never essential complexity.
    - Representation choice governs where accidental complexity accumulates, not whether essential complexity exists.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [complexity, fred-brooks, software-architecture, definitions]

### Atom 003: Mutable State Causes Combinatorial State-Space Explosion and Contaminates Pure Logic
- Kind: mechanism
- Statement: Introducing mutable state into a system multiplies the number of configurations that must be reasoned about combinatorially, and once a pure function calls a stateful procedure it becomes "contaminated" — no longer understandable in isolation.
- Scope & Conditions: Applies wherever state can change over time; effect compounds with the number of independent stateful variables (n booleans → 2^n states).
- Evidence: "If a system possesses a mere ten independent boolean flags, the developer has inadvertently created 1,024 potential states to account for... If a pure, stateless function is forced to call a stateful procedure, the original function becomes contaminated, meaning a developer can no longer reason about it without simultaneously simulating the entire global state of the application in their head."
- Implications:
    - Testing effort scales combinatorially with independent mutable state, not linearly.
    - Isolating state at system boundaries preserves the ability to reason about the rest of the system in isolation.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [state, mutable-state, out-of-the-tar-pit, complexity]

### Atom 004: Smart Data Structures Yield Trivial Code (Torvalds' Maxim, Corrected Sourcing)
- Kind: claim
- Statement: Linus Torvalds argued that the difference between a bad and a good programmer is whether they prioritise their code or their data structures, and that well-chosen data structures make the algorithms operating on them self-evident.
- Scope & Conditions: Originates as a footnote in a 2006 git mailing-list reply about licensing and interoperability, not a general software essay or the 2016 TED talk (which supplies the separate linked-list example — see Atom 005). Torvalds' actual point there is that a stable, well-documented data format is a durable interface while code built on it is disposable.
- Evidence: "'Bad programmers worry about the code. Good programmers worry about data structures and their relationships.'" — footnote to Torvalds, "Re: Licensing and the library version of git", git mailing list, 27 Jul 2006.
- Implications:
    - The quote is frequently mis-cited as a standalone philosophical essay; its original context is a narrow point about interoperability via a stable data format.
    - Citing this quote for a general "structure over control flow" thesis borrows context it wasn't made in.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [linus-torvalds, data-structures, quote-provenance, git]

### Atom 005: The Linked-List "Good Taste" Example Eliminates Complexity Rather Than Relocating It
- Kind: mechanism
- Statement: Torvalds' preferred implementation of singly-linked-list node removal — using a pointer-to-a-pointer instead of tracking a "previous node" — removes the special-case `if` branch for the list head entirely rather than moving that complexity somewhere else.
- Scope & Conditions: A 2016 TED-talk example of "good taste" in code; demonstrated for singly-linked-list deletion specifically.
- Evidence: "Because the data structure has been conceptually generalized through indirection, the edge case completely vanishes. The if statement is entirely eliminated... The if didn't move anywhere. It stopped existing."
- Implications:
    - This is the source report's own headline "conservation" example, yet it is structurally a counterexample: total complexity went down, not sideways.
    - Elimination (this case) and relocation (see Atoms 007, 011) are mechanistically different outcomes and should not be conflated.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [linus-torvalds, linked-list, good-taste, elimination-vs-relocation, epistemics]

### Atom 006: Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure
- Kind: mechanism
- Statement: Git represents every file, tree, and commit as an object named by the SHA-1 hash of its own content, so identity, tamper-detection, and history verification become direct consequences of the data structure rather than results computed by separate algorithms.
- Scope & Conditions: Applies to Git's object model specifically (2005 design for Linux kernel-scale distributed version control).
- Evidence: "Because the data structure perfectly modeled a tamper-evident, directed acyclic graph, the algorithms required to distribute code, verify integrity, and merge histories became trivial consequences of the structure itself."
- Implications:
    - Content-addressing turns "is this the same version?" and "was this tampered with?" into structural comparisons instead of bespoke diff/verification algorithms.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: medium
- Tags: [git, content-addressing, data-structures, distributed-systems]

### Atom 007: Rob Pike's Rule 5 — Data Dominates
- Kind: claim
- Statement: Rob Pike's fifth rule of programming holds that once the right data structures are chosen and organised well, the algorithms needed to manipulate them are almost always self-evident, so data structures — not algorithms — should be the central design concern.
- Scope & Conditions: From Pike's 1989 "Notes on C Programming"; rules 3–5 address algorithm/data trade-offs.
- Evidence: "Rule 5: Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming."
- Implications:
    - Design effort should be front-loaded onto modelling the data correctly rather than onto algorithmic cleverness.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [rob-pike, data-structures, programming-rules]

### Atom 008: Corrected Quote Lineage — Brooks → Pike → Raymond → Torvalds ("Fold Knowledge Into Data")
- Kind: distinction
- Statement: The "smart data structures, dumb code" phrasing commonly attributed to Torvalds is actually Eric Raymond's, coined while restructuring fetchmail's protocol machines and credited by Raymond himself to Brooks's "Show me your tables" line in The Mythical Man-Month, chapter 9; Raymond later formalised it as the Rule of Representation: "Fold knowledge into data, so program logic can be stupid and robust."
- Scope & Conditions: A provenance correction establishing the actual attribution chain (Brooks 1975 → Pike 1989 → Raymond 1997/2003 → Torvalds 2006), not a new technical claim.
- Evidence: "The 'smart structures / dumb code' phrasing is Raymond's. He drew it from reorganising fetchmail's protocol machines into a generic driver plus three method tables, and credited Brooks's Mythical Man-Month, chapter 9, as the same point."
- Implications:
    - Citations of this maxim should point to Raymond's Rule of Representation (or Brooks directly), not to Torvalds, unless specifically discussing Torvalds' independent restatement.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: medium
- Tags: [quote-provenance, eric-raymond, fred-brooks, epistemics]

### Atom 009: Cyclomatic Complexity Is a Lagging Symptom of Poor Data Modelling, Not the Root Cause
- Kind: distinction
- Statement: McCabe's cyclomatic complexity metric counts independent paths through a program's control-flow graph and so measures excessive branching as a symptom, while Chapin's data complexity metric measures the complexity of the data being manipulated, which sits closer to the underlying cause.
- Scope & Conditions: A measurement-theory distinction between two 1970s-era software metrics.
- Evidence: "While a high cyclomatic complexity indicates that a function is difficult to test and prone to defects, it is ultimately a lagging indicator. It measures the symptom (excessive branching) rather than the disease (poor data modeling)."
- Implications:
    - Driving cyclomatic complexity down without addressing the underlying data model risks treating the symptom, not the disease.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: medium
- Tags: [cyclomatic-complexity, mccabe, chapin, metrics]

### Atom 010: Shotgun Parsing Scatters Validation Logic Through Execution Logic
- Kind: definition
- Statement: "Shotgun parsing" (Alexis King's term) is the anti-pattern where input-validation checks are interleaved with execution logic and repeated at scattered points across a codebase instead of being performed once at a system boundary.
- Scope & Conditions: Applies to systems that accept loosely-typed input (e.g. generic dictionaries) and validate it ad hoc wherever it is consumed.
- Evidence: "Alexis King refers to this anti-pattern as 'shotgun parsing,' a state where input-validating logic is mixed directly with the execution logic and scattered randomly across the codebase... late-stage validation failures can occur after partial processing has already mutated the system state, leading to data corruption."
- Implications:
    - Because validation isn't bound to the data's type, downstream code must either blindly trust it or redundantly re-check it.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [alexis-king, shotgun-parsing, validation, anti-pattern]

### Atom 011: Parse, Don't Validate — Validation Is Lossy, Parsing Is Constructive
- Kind: mechanism
- Statement: A validation function discards the proof of correctness it computed (returning only true/false while the data stays in its raw type), whereas a parser is constructive — it transforms raw input into a more structured type that carries the proof of validity with it for the rest of its lifetime.
- Scope & Conditions: Alexis King's "Parse, Don't Validate" principle; assumes a type system expressive enough to encode the refined type as distinct from the raw type.
- Evidence: "Validation is an inherently lossy process... If the function returns True, the calling code knows the data is safe, but the data itself remains in its raw, unconstrained format... Parsing, by contrast, is a constructive transformation... the output type is a distinct refinement of the input type."
- Implications:
    - Once parsed, downstream functions that require the refined type get their validity guarantee for free from the type system, with zero repeated control flow.
    - A validation-only approach forces every downstream function to choose between blind trust and redundant re-checking.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [parse-dont-validate, alexis-king, type-driven-design, validation]

### Atom 012: Making Illegal States Unrepresentable via Types (NonEmpty List Example)
- Kind: heuristic
- Statement: Instead of validating that a list is non-empty before taking its head, a NonEmpty list type — structurally a tuple of one guaranteed element plus a possibly-empty remainder — makes emptiness impossible to represent, so no control flow is needed to guard against it.
- Scope & Conditions: Requires parsing/converting a generic list into the NonEmpty type at the boundary where the non-emptiness guarantee is first required.
- Evidence: "The structural solution is to abandon the generic list and define a NonEmpty list data type... A function designed to retrieve the head of a NonEmpty list requires zero control flow, zero Option wrappers, and zero validation checks, because it is structurally impossible for the type to be empty."
- Implications:
    - If the underlying business rule changes (e.g. empty becomes valid), the type signature itself must change, forcing the compiler to flag every affected call site.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [type-driven-design, illegal-states-unrepresentable, alexis-king]

### Atom 013: Jackson Structured Programming — Control Flow Should Be Isomorphic to Data Structure
- Kind: claim
- Statement: Michael Jackson's 1975 Jackson Structured Programming (JSP) method derives a program's control structure directly and exclusively from Data Structure Diagrams of its input and output, so sequences, iterations, and selections in the data are mirrored one-for-one by sequential blocks, loops, and conditionals in the code.
- Scope & Conditions: Developed for COBOL batch-file processing; rejects top-down procedural decomposition as the starting point for program design.
- Evidence: "JSP dictated that the control structure of a program must be derived directly and exclusively from the data structures of the input and output files it processes... The code becomes a direct, isomorphic reflection of the data structure."
- Implications:
    - Because requirement changes over a product's life are usually small tweaks to data structure rather than radical algorithmic shifts, a JSP-derived program changes predictably and locally when its input schema changes.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: medium
- Tags: [jackson-structured-programming, data-structures, control-flow, historical]

### Atom 014: Data-Oriented Design — Structure-of-Arrays Eliminates the Cache-Miss Stalls Array-of-Structures Causes
- Kind: mechanism
- Statement: Because CPUs fetch memory in fixed-size cache lines, storing per-entity properties as an Array of Structures (one heap object per entity, each bundling unrelated fields) pollutes every cache-line fetch with irrelevant data, whereas a Structure of Arrays (one flat, contiguous array per property) lets every fetched cache line contain only the data the current loop actually needs.
- Scope & Conditions: A hardware-grounded consequence of CPU cache-line fetching and hardware prefetching; most relevant to hot loops processing many homogeneous entities (e.g. game-engine particle systems).
- Evidence: "Because the Particle object contains extra, unrelated data (color, lifetime), the 64-byte cache line pulled into the CPU is severely polluted with irrelevant information... a single 64-byte cache line fetch pulls in the specific data for multiple particles simultaneously. The hardware prefetcher recognizes the predictable linear access pattern."
- Implications:
    - SoA layout also removes virtual-function/vtable dispatch overhead common in AoS+OOP designs, and enables SIMD vectorisation of the resulting tight loops.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [data-oriented-design, cache-lines, structure-of-arrays, performance, mike-acton]

### Atom 015: Primitive Obsession Forces Validation Into Control Flow; Value Objects Absorb It Into Structure
- Kind: claim
- Statement: Representing a heavily-constrained domain concept with a bare primitive type (e.g. a generic string for a Social Security Number, or a plain int for an account balance) discards all structural constraints, forcing every consuming function to re-validate it, whereas a Value Object with a smart constructor enforces the constraint once, at construction, and is thereafter treated as immutable proof of validity.
- Scope & Conditions: A Domain-Driven Design pattern for eliminating "primitive obsession."
- Evidence: "When primitives are utilized, they carry no structural constraints... developers must sprinkle validation logic and control flow loops throughout the entire application... An AccountBalance type is created with a smart constructor that strictly enforces the rule that the value must be non-negative at the time of creation."
- Implications:
    - Passing structured Value Objects instead of raw primitives also prevents accidental parameter-order swaps between same-typed primitives.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [domain-driven-design, primitive-obsession, value-objects]

### Atom 016: Poor Data Structure Exhausts an AI Coding Agent's Context Window Before It Can Trace Execution Logic
- Kind: claim
- Statement: When a codebase relies heavily on control flow, shared mutable state, and deep inheritance, its logic is diffuse across many files, so an LLM coding agent must read across dozens of files to reconstruct the implicit state and branching before it can safely modify the code — and often exhausts its context window before doing so, producing plausible but incorrect edits; smart data structures, small modules, and explicit interfaces keep the same reasoning within budget.
- Scope & Conditions: Applies specifically to LLM-based code-generation/editing agents operating under a fixed context-window budget.
- Evidence: "An AI model attempting to understand a deeply nested, procedural architecture must read across dozens of files and thousands of lines of code to track the implicit state and scattered conditional branching. Because the structural representation is poor, the AI exhausts its context window before it can grasp the full execution path, resulting in plausible but dangerously incorrect code generation."
- Implications:
    - Gives "data dominates" a new, LLM-era justification distinct from the original human-cognition and CPU-cache arguments: it is also what keeps a system inside an agent's context budget.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: medium
- Tags: [llm-agents, context-window, software-architecture, ai-code-generation]

### Atom 017: Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as "Conservation"
- Kind: distinction
- Statement: Reducing procedural complexity by restructuring data can happen through at least two mechanistically different routes — elimination, where a special case is redefined out of existence (e.g. the linked-list pointer-to-pointer trick), and relocation, where the same amount of complexity is genuinely moved into a table, parser, or type constraint (e.g. Pike's data tables, or parse-don't-validate) — and only the second route is actual evidence for a "conservation" claim.
- Scope & Conditions: A methodological distinction drawn from contrasting Torvalds' linked-list example against Pike's table-driven parsing and King's parse-don't-validate.
- Evidence: "Only mechanisms 2 and 3 look like conservation. Mechanism 1, the headline Torvalds example, is a counterexample to it."
- Implications:
    - Citing an elimination example (complexity destroyed) as proof of a conservation law (complexity only relocated) is a category error, even though both examples feel like "the data structure did the work."
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [epistemics, conservation-of-complexity, elimination-vs-relocation, falsifiability]

### Atom 018: A Conservation Claim Becomes Unfalsifiable If "Essential Complexity" Is Defined Post-Hoc
- Kind: failure_mode
- Statement: If "essential complexity" is defined merely as "whatever complexity survived a simplification attempt," then any observed reduction can always be redescribed as accidental complexity being removed while essential complexity was conserved — making the conservation claim true by definition and untestable; it only becomes falsifiable if essential complexity is estimated independently, before the representation is chosen (e.g. by counting domain states or business rules).
- Scope & Conditions: A general falsifiability critique applicable to any "conservation of X" claim defined circularly around what remains after optimisation.
- Evidence: "If 'essential' just means 'whatever survived simplification', conservation is true by definition and can't be falsified. It only becomes testable if you estimate essential complexity independently before choosing a representation, for example by counting domain states or business rules."
- Implications:
    - Any future defence of "complexity is conserved" needs an independent, ex-ante measure of essential complexity, not a post-hoc one.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [falsifiability, epistemics, unfalsifiable-claims, conservation-of-complexity]

### Atom 019: Moving a Constraint Into a Type Is Cost Amortisation, Not a Zero-Sum Transfer
- Kind: claim
- Statement: Even where the same information is preserved whether a constraint lives in a type or in a runtime check, the enforcement cost is not conserved: a constraint expressed as a type is written once and checked by the compiler at every call site for free, whereas the same constraint expressed as a null check must be repeated at every call site and is enforced by nobody if a site forgets it — so moving a constraint into structure is a cost reduction, not a like-for-like relocation.
- Scope & Conditions: The best-supported alternative to strict "conservation": enforcement cost, not information, is what actually changes when constraints move from control flow into types.
- Evidence: "A constraint in a type is written once, checked by the compiler, and inherited by every call site. The same constraint as a null check is repeated N times and checked by nobody. Moving it into structure is amortisation, not a zero-sum transfer."
- Implications:
    - Reframes the defensible thesis as "structure is a cheaper home for essential complexity than control flow", not "total complexity is constant."
    - Testable with before/after refactor metrics (conditional count, cyclomatic complexity, defect rate), unlike strict conservation.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [cost-amortisation, type-systems, epistemics, conservation-of-complexity]

### Atom 020: The Right Data Structure, Not a "Smart" One, Is Pike's Actual Rule
- Kind: constraint
- Statement: Rob Pike's Rule 4 ("use simple algorithms as well as simple data structures") asks for the structure that correctly fits the domain, not a maximally clever or elaborate one; over-engineered types and deep class hierarchies are themselves a form of accidental complexity, so "push complexity into structure" is not unconditionally good advice.
- Scope & Conditions: A falsifier/boundary condition on the whole "smart structures" thesis — names its own failure mode.
- Evidence: "Pike warns against 'smart'. His Rule 4 says to use simple algorithms as well as simple data structures. He asks for the right structure, not a smart one. Over-engineered types and deep class hierarchies are structural complexity that is itself accidental."
- Implications:
    - Any "push complexity into data structures" guideline needs a matching falsifier: has the resulting type/schema become elaborate enough to be its own source of accidental complexity?
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: medium
- Tags: [rob-pike, over-engineering, falsifier, accidental-complexity]

### Atom 021: Empirical Support for "Types Prevent Bugs" Is Thin and Indirect
- Kind: constraint
- Statement: The strongest available empirical evidence for structure-first design is adjacent rather than direct: a 2017 study (Gao, Bird & Barr) found that static typing via Flow or TypeScript would conservatively have caught only about 15% of a sample of 400 fixed public JavaScript bugs, and a 2019 reproduction (Berger et al.) of an earlier cross-language study found only four programming languages with a statistically significant, and very small, association with defect rates — neither study isolates domain-faithful data modelling as the variable being tested.
- Scope & Conditions: Concerns the empirical (not mechanistic) case for structure-first design; the mechanism itself is separately well-supported by worked examples, not by controlled studies.
- Evidence: "Gao, Bird and Barr (ICSE 2017) sampled 400 fixed public JavaScript bugs and found Flow or TypeScript would conservatively have caught about 15%... Berger et al.'s 2019 reproduction of Ray et al. found only four languages with a statistically significant association with defects, and the effect sizes were exceedingly small."
- Implications:
    - The overall claim should be tagged "corroborated by mechanism and worked examples, but not measured" rather than empirically proven.
- Validation:
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: medium
- Tags: [empirical-evidence, type-systems, epistemics, evidence-quality]