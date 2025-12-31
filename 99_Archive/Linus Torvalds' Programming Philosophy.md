---
aliases: []
tags: []
title: "**The Architecture of Reason: Transcending the Crisis of Software Complexity**"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-31T09:43:47+00:00
modified: 2025-12-31T23:08:31+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# **The Architecture of Reason: Transcending the Crisis of Software Complexity**

## **Executive Summary**

The contemporary software landscape is characterized by a paradox: while tools, languages, and hardware have advanced exponentially, the reliability and maintainability of software systems often appear to be in decline. This report, commissioned to investigate the philosophical underpinnings of exceptional programming, posits that the industry's struggle with a "buggy mess" is not a failure of tooling, but a failure of mental models. The central thesis, anchored in the philosophy of Linus Torvalds, is that the mediocre programmer focuses on code—the transient instructions of execution—while the master programmer focuses on data—the persistent structure of information.

This document provides an exhaustive analysis of the mental models employed by industry luminaries including Linus Torvalds, John Carmack, Joe Armstrong, Rich Hickey, Mike Acton, and Jonathan Blow. By synthesizing their philosophies, we identify a set of "Transcendental Techniques" that oppose the prevailing "Resume-Driven Development" culture. These techniques prioritize data topology over algorithmic complexity, hardware reality over abstract modeling, and fault tolerance over defensive programming. The report details how these paradigms are applied in high-stakes environments—from the Linux kernel and the Git version control system to high-performance game engines and telecommunications infrastructure—demonstrating that the path to software mastery lies in a rigorous, data-centric understanding of the problem space.

---

**Part I: The Torvalds Doctrine and the Primacy of Data**

### **1.1 The Axiom of Data Structure Dominance**

The inquiry begins with a definitive assertion by Linus Torvalds, the creator of Linux and Git, regarding the fundamental distinction between competent and exceptional programming. Torvalds states: *"I will, in fact, claim that the difference between a bad programmer and a good one is whether he considers his code or his data structures more important. Bad programmers worry about the code. Good programmers worry about data structures and their relationships"*.

This statement serves as the foundational axiom for this entire investigation. To understand its depth, one must deconstruct the typical workflow of the "mediocre" programmer. In standard practice, software development often begins with behavioral requirements: "The system must do X when Y happens." The programmer immediately translates this into control flow—writing functions, if statements, and loops. The data is treated merely as the payload that this logic manipulates, often stuffed into generic containers or ill-conceived classes as an afterthought.

Torvalds argues that this approach is backward. Code is secondary; it is merely the mechanism by which data is transformed. Data is the primary reality of the system. If the data structures are designed to reflect the inherent relationships of the problem domain accurately, the code required to manipulate them becomes trivial, robust, and often obvious. Conversely, if the data structure is a poor fit for the problem, the code must become increasingly complex, laden with conditional logic and edge-case handling to bridge the gap between the data's shape and the desired behavior.

The implications of this philosophy extend beyond mere coding style into the realm of system architecture. A data-first mentality forces the architect to confront the "state" of the system immediately. State is the source of complexity in software; by rigorously defining how state is structured, accessed, and mutated, the programmer constrains the entropy of the system. The "bad programmer" who worries about code is essentially trying to manage entropy through sheer force of logic, a battle that inevitably leads to the "buggy mess" of unmaintainable control flow.

### **1.2 Case Study: The "Good Taste" of Linked Lists**

Torvalds provided a granular demonstration of this philosophy during a 2016 TED talk, where he contrasted a "bad taste" implementation of a linked list removal function with a "good taste" version. This example, while seemingly low-level, encapsulates the entire data-centric worldview.

In a standard computer science curriculum, removing an item from a singly linked list is taught as a conditional operation. The programmer must handle two distinct states:

1. **The Head Case:** The item to be removed is the first element in the list. The global "head" pointer must be updated to point to the second element.
2. **The Middle Case:** The item is somewhere else. The "next" pointer of the *previous* element must be updated to skip the removed item.

The resulting code typically looks like this:

```c
// "Bad Taste" - Conditional Logic
void remove_list_entry(node **head, node *entry) {
    node *prev = NULL;
    node *walk = *head;

    while (walk!= entry) {  
        prev = walk;  
        walk = walk->next;  
    }

    if (!prev)  
        *head = entry->next; // Special case: Head removal  
    else  
        prev->next = entry->next; // Standard case  

}
```

Torvalds critiques this not because it is incorrect, but because it lacks "taste." The lack of taste is manifested in the if statement. The conditional exists because the data model (as perceived by the programmer) views the "head" pointer and the "next" pointers inside nodes as fundamentally different entities. One is a global variable; the others are structure members.

The "good taste" approach reframes the data relationship. It recognizes that the *head* is simply a pointer, indistinguishable in function from the *next* pointer of a node. Both are memory addresses that point to a node. By iterating with a pointer-to-a-pointer (an indirect pointer), the programmer can treat the address of the "incoming link" uniformly, regardless of whether that link originates from the global scope or a previous node.

```c
// "Good Taste" - Unified Data Model

void remove_list_entry(node **head, node *entry) {

    node **indirect = head;

    // Iterate while the *pointer itself* does not point to our entry  
    while ((*indirect)!= entry) {  
        indirect = &(*indirect)->next;  
    }

    // Update the pointer (works for head or next)  
    *indirect = entry->next;  

}
```

This transformation eliminates the conditional logic entirely. The code shrinks. The edge case (removing the head) vanishes—not because the algorithm handled it, but because the **mental model of the data** was adjusted to make the edge case topologically identical to the standard case. This is the essence of Torvalds' philosophy: complexity in code is often a symptom of insufficient understanding of the data structure. The "good programmer" seeks a data representation where the "special cases" are mathematically unified with the general case.

### **1.3 Git: The Pinnacle of Data-Oriented Architecture**

The most profound application of Torvalds' data structure philosophy is the Git version control system. Developed in a mere ten days in 2005 after the Linux kernel team lost access to BitKeeper, Git was explicitly designed as "the anti-CVS" (Concurrent Versions System). Its architecture is a direct rejection of the code-centric models that dominated the era.

#### **1.3.1 The Failure of Delta-Based Thinking**

Pre-existing VCS tools like CVS and Subversion were built on a mental model of "changes" or "deltas." They viewed version control as a process of recording the differences between files over time. This is a code-centric view: it focuses on the *operations* (add line, delete line) performed on the data. This model leads to fragility; to reconstruct a file at version X, the system must mathematically apply a chain of deltas to a base file. If any link in that chain is corrupted, the history is lost. Furthermore, branching is expensive because the system must track diverging sets of changes.

#### **1.3.2 The Directed Acyclic Graph (DAG)**

Torvalds approached the problem from a data-centric perspective. He asked: "What is the state of the project?" The answer is a snapshot of the entire filesystem. Git’s core data structure is not a list of changes, but a Directed Acyclic Graph (DAG) of objects.

* **Blobs:** Represent file content.
* **Trees:** Represent directory structures, pointing to blobs or other trees.
* **Commits:** Represent a snapshot of the root tree, pointing to parent commits.

This structure is **Content-Addressable**. Every object is identified by a SHA-1 hash of its contents. This decision, often misunderstood as a security feature, was fundamentally about data integrity and structural simplicity. By hashing the content, Git ensures that identical data is stored exactly once (deduplication) and that any corruption in a file changes its hash, making the corruption immediately detectable.

#### **1.3.3 Implications of the Data Model**

Because Torvalds prioritized the data structure (the DAG), the "code" for complex features became trivial:

1. **Branching:** In a delta-based system, branching is a complex operation of forking change sets. In Git, a branch is simply a 41-byte file containing the hash of a commit. Creating a branch is an O(1) operation—it is just writing a pointer.
2. **Merging:** Merging becomes a graph traversal problem to find a common ancestor, rather than a textual heuristic application.
3. **Distributed Consistency:** Because the data is identified by its hash, two developers on opposite sides of the world who have the same hash are mathematically guaranteed to have the same data. This enabled the distributed workflow that revolutionized software development.

The success of Git is not due to superior algorithms for diffing files; it is due to a superior data structure that made the concept of "distributed version control" a natural property of the graph topology. Torvalds effectively encoded the rules of the system into the data itself, leaving the code "dumb" and robust.

---

**Part II: The Reality of Hardware and Data-Oriented Design**

### **2.1 Mike Acton and the "Three Big Lies"**

While Torvalds focuses on the logical relationships of data, Mike Acton, a prominent figure in high-performance game development, extends this rigor to the *physical* layout of data in hardware. Acton’s philosophy, known as Data-Oriented Design (DOD), arises from a dissatisfaction with the "buggy mess" and slow performance of modern software, which he attributes to the abstraction layers of Object-Oriented Programming (OOP).

Acton identifies "Three Big Lies" that pervade the software industry:

1. **"Software is the platform."** (Reality: Hardware is the platform.)
2. **"Code is designed around the model of the world."** (Reality: Code is designed to transform data.)
3. **"Code is more important than data."** (Reality: Data is paramount.)

The mediocre technique, according to Acton, is to prioritize the "mental model" of the programmer over the reality of the machine. Programmers are taught to model a "Chair" as a class with properties like material, weight, and owner. They then create thousands of Chair objects, scattering them across the system memory (the heap). When the program runs, the CPU must "chase pointers" to find these objects, causing cache misses and stalling the processor.

Acton argues that "If you don't understand the data, you don't understand the problem." The hardware does not care about the concept of a "Chair." It cares about transforming specific subsets of data: geometry data for the renderer, physics data for the collision engine, and audio data for the sound system.

### **2.2 The Transformation Mental Model**

The DOD mental model shifts the programmer's focus from "objects" (nouns) to "transformations" (verbs). A program is viewed as a pipeline that accepts input data and transforms it into output data.

#### **2.2.1 Structure of Arrays (SoA) vs. Array of Structures (AoS)**

To align with this model, DOD advocates for organizing data to maximize **cache coherency**.

* Array of Structures (AoS - Typical OOP): [{pos, vel, hp}, {pos, vel, hp},...]
  When the physics system iterates through this array to update positions, it loads vel and hp into the cache line, even if it only needs pos. This wastes memory bandwidth.
* Structure of Arrays (SoA - DOD): [pos, pos,...], [vel, vel,...], [hp, hp,...]
  The physics system loads a contiguous block of positions, utilizing every byte of the cache line.

The profound insight here is that **context matters**. The data required for one operation (rendering) is often different from the data required for another (AI logic). Bundling them into a single "Object" couples these contexts unnecessarily, leading to inefficiency and complexity. By separating data based on *access patterns* rather than *conceptual identity*, the programmer creates systems that scale linearly and perform predictably.

### **2.3 Jonathan Blow: Friction and the Collapse of Civilization**

Jonathan Blow, creator of the JAI programming language, expands the DOD philosophy into a critique of the entire software ecosystem. He argues that the industry's reliance on "easy" tools (managed languages, garbage collection, heavy frameworks) creates a layer of friction that prevents deep understanding and robust engineering.

#### **2.3.1 The "Collapse" Thesis**

In his talk "Preventing the Collapse of Civilization," Blow posits that software complexity has reached a tipping point where knowledge is being lost rather than gained. As layers of abstraction accumulate (e.g., Electron apps running on top of browsers, running on top of VMs, running on top of OSs), fewer programmers understand the foundations. The "buggy mess" is a symptom of this fragility—developers are gluing together black boxes they do not understand, resulting in software that is bloated, slow, and impossible to debug effectively.

#### **2.3.2 The JAI Philosophy**

Blow’s solution, embodied in JAI, is to remove friction between the programmer and the data.

* **Rejection of RAII/Constructors:** Automatic initialization (common in C++) often hides the cost of data creation. JAI encourages explicit management of data life cycles.
* **Compile-Time Execution:** Allowing the programmer to run arbitrary code during compilation to generate data tables or pre-calculate values, blurring the line between "build script" and "program" to ensure data correctness before runtime.

The mental model here is **Directness**. The master programmer rejects "Resume-Driven" technologies that promise convenience at the cost of opacity. Instead, they seek tools that expose the raw reality of the data and the machine, accepting the responsibility of managing that reality in exchange for total control and understanding.

---

**Part III: The Architecture of Reliability**

### **3.1 Joe Armstrong and the "Error Kernel"**

While Torvalds and Acton focus on structure and performance, Joe Armstrong (creator of Erlang) addressed the problem of reliability in the face of inevitable failure. In the telecommunications industry, where Erlang was born, systems must operate with 99.9999999% reliability. Armstrong’s mental model for achieving this is radically different from the defensive programming techniques taught in universities.

#### **3.1.1 The "Let It Crash" Philosophy**

The "mediocre" technique for handling errors is **Defensive Programming**: wrapping code in try/catch blocks, checking for null at every step, and attempting to recover from every possible anomaly. Armstrong argues that this leads to "zombie" systems—programs that are theoretically running but have entered an inconsistent state due to a handled exception, leading to unpredictable behavior later.

Armstrong’s alternative is **"Let It Crash."** If a process encounters a state it was not designed to handle (e.g., a database connection drops, or input data is malformed), it should immediately terminate. It should not attempt to "fix" the state, because the code that caused the error is likely flawed or the state is already corrupted.

This philosophy relies on two prerequisites:

1. **Isolation:** Processes must share no state. If one crashes, it must not affect the memory of others (The Actor Model).
2. **Supervision:** A separate process (Supervisor) must observe the crash and restart the worker process from a known clean state.

#### **3.1.2 The Error Kernel Pattern**

This leads to the **Error Kernel** architecture, a concept Armstrong formalized but which is applicable beyond Erlang. The Error Kernel is the minimal subset of the system that *must* be correct and *must not* crash for the system to function.

* **The Onion Model:**
  * **Core (Kernel):** Extremely simple, formally verified code that manages the lifecycle of other processes. It has zero external dependencies and almost zero logic.
  * **Inner Layers:** Essential services (routing, supervision).
  * **Outer Layers:** Business logic, request handling, parsing.

Risky operations (parsing user input, network calls) are pushed to the leaves of the onion (the outer layers). If a leaf crashes, the kernel restarts it. The reliability of the system is not defined by the absence of bugs in the business logic, but by the robustness of the supervision hierarchy in the kernel.

### **3.2 The Biological Metaphor**

Armstrong, influenced by Alan Kay, viewed software systems through a biological lens. A multicellular organism is highly reliable despite the constant death of individual cells. The organism does not try to debug a dying cell; the immune system isolates and removes it.

Kay’s definition of Object-Oriented Programming (OOP) aligns with this: "I thought of objects being like biological cells... only able to communicate with messages".32 The "buggy mess" of modern OOP arises because typical languages (Java, C++) allow objects to share memory references, violating the biological principle of isolation. If one object corrupts a memory address, it can kill the whole "organism" (program).

The master programmer models the system not as a monolith, but as a society of independent agents. This model inherently handles concurrency and fault tolerance, as the failure of one agent is a localized event, not a systemic catastrophe.

---

**Part IV: The Discipline of Simplicity and Formalism**

### **4.1 Rich Hickey: Decomplecting Software**

Rich Hickey, creator of Clojure, provides a linguistic and philosophical framework for distinguishing "Simple" from "Easy." His mental model attacks the root cause of the "buggy mess": the conflation of convenience with simplicity.

#### **4.1.1 Simple vs. Easy**

Hickey defines these terms etymologically:

* **Easy (Latin: *adjacent*):** Something is easy if it is familiar or near at hand. Using a popular library is "easy" because it is a quick reach. Typing git pull is easy. Ease is subjective and relative to the programmer's experience.
* **Simple (Latin: *simplex* - one fold):** Something is simple if it is unentangled. A single thread is simple. A pure function is simple. Simplicity is objective.

The industry crisis stems from choosing "Easy" tools (ORMs, massive frameworks) that are "Complected" (braided together). An ORM complects the database schema with the in-memory object graph. If one changes, the other breaks. This braiding creates a combinatorial explosion of state that is impossible to reason about.

#### **4.1.2 Value-Oriented Programming**

Hickey’s solution is to treat data as **Values**. A value (like the number 42) is immutable. It does not change. In contrast, "Objects" in OOP are typically mutable containers of state. Hickey argues that "State is not a value; state is an identity that changes over time."

The master programmer models the system as a succession of immutable values.

* **Process:** `Function(Value T1) -> Value T2`.
* Nothing is overwritten. The past is preserved (conceptually).

This connects back to Torvalds’ Git: Git does not overwrite the previous commit; it creates a new commit that points to the old one. This **Immutability** eliminates the need for locks in concurrency (you can read a value while someone else writes a new one) and makes the system trivially testable.12

### **4.2 Leslie Lamport: Thinking Above the Code**

Leslie Lamport, Turing Award winner, challenges the very act of coding as a primary problem-solving activity. His mental model is that **coding is the last and least important step** of software engineering.

#### **4.2.1 The Specification Mindset**

Lamport argues that the "buggy mess" exists because programmers "think in code." They start writing classes and functions before they understand the logical properties of the system. This "trial and error" coding works for simple scripts but fails for complex distributed systems (e.g., cloud infrastructure).

Lamport advocates for **TLA+ (Temporal Logic of Actions)**, a formal specification language. TLA+ allows the architect to model the system mathematically—defining the "State Space" and the "Next State" relations. The goal is to check for invariants (properties that must always be true) and liveness (properties that must eventually happen).

* **Mediocre Technique:** Write code, run tests, fix bugs. (Cannot find race conditions that happen once in a billion operations).
* **Master Technique (Lamport):** Write a specification, model-check the logic, *then* write code.

Amazon Web Services (AWS) adopted TLA+ to verify their core algorithms (DynamoDB, S3) and found subtle, critical bugs that testing never caught. This proves that "thinking above the code" is not academic ivory-towerism, but a pragmatic necessity for high-reliability engineering.

---

**Part V: Semantic Compression and the Cost of Abstraction**

### **5.1 Casey Muratori and the Critique of "Clean Code"**

Casey Muratori, known for the *Handmade Hero* project, offers a critique of the "Clean Code" movement (Robert C. Martin et al.), which prioritizes readability and heavy fragmentation (many small functions) over structural logic.

Muratori introduces the concept of **Semantic Compression**. He argues that programmers often commit "premature abstraction." They see two lines of code that look similar and immediately create a function or a base class to "DRY" (Don't Repeat Yourself) it out. This often leads to abstractions that do not actually model the domain, but merely hide the code structure.

#### **5.1.1 The Compression Process**

The master programmer writes the "long" version of the code first. They write out the specific logic for the specific problem. They allow duplication to exist temporarily. Only when the *semantics* (the meaning) of the code is fully understood do they "compress" it into a function.

* **Clean Code Approach:** "I need a Shape class because I might have Circles and Squares later." (Speculative Generality).
* **Semantic Compression:** "I have code for drawing a circle. I have code for drawing a square. I see they both share a coordinate transform. I will compress that transform logic into a utility." (Empirical Abstraction).

This ensures that abstractions are born from necessity, not dogma. It keeps the code "honest" and avoids the "spaghetti of indirection" where a developer must jump through ten files to understand one operation.

### **5.2 The "Jungle" of Dependencies**

This philosophy aligns with Joe Armstrong’s "Banana and Gorilla" quote: "You wanted a banana but what you got was a gorilla holding the banana and the entire jungle.".43 Resume-Driven Development encourages pulling in massive libraries (the jungle) to solve simple problems (the banana).

The master programmer seeks to minimize dependencies. They understand that every line of external code is a line they cannot easily debug or optimize. They prefer to write a simple, custom implementation of a linked list (like Torvalds) rather than importing a generic container library if the specific use case demands "good taste" and control.

---

**Part VI: Making Invalid States Unrepresentable**

### **6.1 Scott Wlaschin and Type System Rigor**

A recurring theme among the experts (Wlaschin, the Rust community, Functional Programmers) is the use of the Type System as a verification tool. The "mediocre" technique relies on **Tests** to ensure correctness. The master technique relies on **Types**.

#### **6.1.1 The Principle**

The principle "Make Invalid States Unrepresentable" means designing data structures such that it is mathematically impossible for them to hold nonsensical data.

* **Mediocre Data Model:**

```java
  class User {
      String name;
      String email;
      boolean isEmailVerified;
      // Logic error: email can be null even if isEmailVerified is true
  }

* **Master Data Model (Rust/F# style):**
  Rust
  enum EmailStatus {
      Unverified(String),
      Verified(String)
  }
  struct User {
      name: String,
      email: EmailStatus
  }
```

  In the second model, there is no boolean flag to get out of sync with the data. The structure of the data itself enforces the business rule.

This transcends "defensive programming" because there is no need to check validity at runtime; the compiler guarantees it. This connects back to Torvalds: by worrying about the data structure (the types), the code (validity checks) becomes unnecessary.

---

**Part VII: Cultural Dimensions and the "Buggy Mess"**

### **7.1 Resume-Driven Development (RDD)**

The "buggy mess" user query complains about is often a product of "Resume-Driven Development" (RDD). This is a phenomenon where developers choose technologies not because they solve the problem efficiently, but because they are "trendy" and increase the developer's market value.

* **Symptoms:** Using Microservices for a startup with 10 users; using a Blockchain for a simple database; using a heavy SPA framework for a static blog.
* **Consequence:** Complexity explodes. The team spends more time managing the infrastructure (Kubernetes, build pipelines) than solving the business problem.

The hiring philosophies of successful engineering cultures (as noted in snippets 44) explicitly screen against RDD. They look for "Problem Solving" ability—the capacity to reason about the problem from first principles—rather than familiarity with a specific laundry list of tools.

### **7.2 The Sociology of Mastery**

The master programmers (Torvalds, Carmack, Blow) share a trait: **Intellectual Autonomy**. They do not accept "industry best practices" at face value.

* Torvalds rejected CVS/Subversion to build Git.
* Carmack rejected standard rendering pipelines to invent adaptive tile refresh (and later, VR optimization techniques).
* Blow rejected C++ to build JAI.

They are willing to build their own tools when the "standard" tools are insufficient. This is not "Not Invented Here" syndrome; it is a refusal to compromise on the quality of the data transformation. They understand that the "buggy mess" is the default state of complex systems, and the only way to escape it is through rigorous, often contrarian, simplifiction.

```ts
￼class User {
  String name;
  String email;
  boolean isEmailVerified;
  // Logic error: email can be null even if isEmailVerified is true
}
```

￼* **Master Data Model (Rust/F# style):**

  Rust

```rust
￼enum EmailStatus {
  Unverified(String),
  Verified(String)
}
￼struct User {
  name: String,
  email: EmailStatus
}
```

**Part VIII: Synthesis–A Unified Theory of High-Leverage Programming**

Integrating the insights of Torvalds, Acton, Armstrong, Hickey, Lamport, and Muratori, we can construct a unified mental model for the high-leverage programmer. This model transcends the "mediocre techniques" of the industry.

### **8.1 The Table of Transcendence**

| Domain | Mediocre Mental Model | Transcendental Mental Model (The Masters) | Key Proponent |
|:---- |:---- |:---- |:---- |
| **Foundation** | **Code-Centric:** Focus on algorithms, syntax, and control flow. | **Data-Centric:** Focus on topology, state, and memory layout. | Linus Torvalds |
| **Reality** | **Modeling the World:** "Chair", "Car", "Customer" objects. | **Transformation:** Data streams, cache lines, batch processing. | Mike Acton |
| **Reliability** | **Defensive:** Try/Catch, null checks, hope. | **Isolation:** Error Kernels, Supervisors, "Let it Crash". | Joe Armstrong |
| **Complexity** | **Easy:** Familiar tools, ORMs, magic frameworks. | **Simple:** Unbraided concerns, immutable values. | Rich Hickey |
| **Design** | **Abstraction:** Premature patterns, "Clean Code" dogma. | **Compression:** Semantic compression, removing friction. | Muratori / Blow |
| **Verification** | **Testing:** Unit tests checking happy paths. | **Specification/Typing:** Formal logic, impossible invalid states. | Lamport / Wlaschin |

### **8.2 The Path Forward**

To escape the "buggy mess," the programmer must undergo a shift in perspective:

1. **Stop writing code immediately.** Start defining the data. Draw the graph. Define the invariants.
2. **Reject the "Easy" path.** Do not pull in a library just to save 10 lines of code if it brings in a jungle of complexity.
3. **Respect the Hardware.** understand that every byte implies a cost. Layout matters.
4. **Embrace Failure.** Build systems that can die and resurrect, rather than systems that try to live forever in a corrupted state.
5. **Think in Values.** Immutable data is the only sane way to model a changing world.

The "Good Programmer" that Torvalds speaks of is not a wizard of algorithms. They are an architect of information. They understand that code is ephemeral—it is rewritten, refactored, and deleted. But Data is eternal. It persists in databases, on disks, and across networks. By anchoring the engineering process in the permanence of data structures rather than the transience of code, the master programmer builds systems that stand the test of time, resisting the entropy that consumes the rest of the industry.

#### **Works cited**

1. Who said "data structure(s) is half the code"? [closed] - Stack Overflow, accessed on December 31, 2025, [https://stackoverflow.com/questions/7800839/who-said-data-structures-is-half-the-code](https://stackoverflow.com/questions/7800839/who-said-data-structures-is-half-the-code)
2. Quote by Linus Torvalds: “I will, in fact, claim that the difference betw...” - Goodreads, accessed on December 31, 2025, [https://www.goodreads.com/quotes/6636783-i-will-in-fact-claim-that-the-difference-between-a](https://www.goodreads.com/quotes/6636783-i-will-in-fact-claim-that-the-difference-between-a)
3. Torvalds' quote about good programmer [closed] - Software Engineering Stack Exchange, accessed on December 31, 2025, [https://softwareengineering.stackexchange.com/questions/163185/torvalds-quote-about-good-programmer](https://softwareengineering.stackexchange.com/questions/163185/torvalds-quote-about-good-programmer)
4. There is a quote by Linus Torvalds that is relevant here: "Bad programmers worry... | Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=17580598](https://news.ycombinator.com/item?id=17580598)
5. An illustration of good taste in code - GitHub Pages, accessed on December 31, 2025, [https://felipec.github.io/good-taste/parts/1.html](https://felipec.github.io/good-taste/parts/1.html)
6. What makes good taste? #linux #linus #torvalds - Gist - GitHub, accessed on December 31, 2025, [https://gist.github.com/santisbon/42580049705ba3d8fbef7168e4668e3c](https://gist.github.com/santisbon/42580049705ba3d8fbef7168e4668e3c)
7. mkirchner/linked-list-good-taste: Linus Torvalds' linked list... - GitHub, accessed on December 31, 2025, [https://github.com/mkirchner/linked-list-good-taste](https://github.com/mkirchner/linked-list-good-taste)
8. Applying the Linus Torvalds “Good Taste” Coding Requirement | Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=12793624](https://news.ycombinator.com/item?id=12793624)
9. Git turns 20: A Q&A with Linus Torvalds - The GitHub Blog, accessed on December 31, 2025, [https://github.blog/open-source/git/git-turns-20-a-qa-with-linus-torvalds/](https://github.blog/open-source/git/git-turns-20-a-qa-with-linus-torvalds/)
10. The Architecture of Open Source Applications (Volume 2)Git, accessed on December 31, 2025, [https://aosabook.org/en/v2/git.html](https://aosabook.org/en/v2/git.html)
11. The Architecture and History of Git: A Distributed Version Control System - Medium, accessed on December 31, 2025, [https://medium.com/@rocketmanw/the-architecture-and-history-of-git-a-distributed-version-control-system-62b17dd37742](https://medium.com/@rocketmanw/the-architecture-and-history-of-git-a-distributed-version-control-system-62b17dd37742)
12. Linus Torvalds: Git proved I could be more than a one-hit wonder | Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=21418033](https://news.ycombinator.com/item?id=21418033)
13. DAG (Directed Acyclic Graph): Definition, Examples, and Applications, accessed on December 31, 2025, [https://www.graphapp.ai/engineering-glossary/git/dag-directed-acyclic-graph](https://www.graphapp.ai/engineering-glossary/git/dag-directed-acyclic-graph)
14. How does Linus Torvalds write software without object oriented programming? I've some questions on GIT architecture: r/learnprogramming - Reddit, accessed on December 31, 2025, [https://www.reddit.com/r/learnprogramming/comments/gwlgyl/how_does_linus_torvalds_write_software_without/](https://www.reddit.com/r/learnprogramming/comments/gwlgyl/how_does_linus_torvalds_write_software_without/)
15. Chapter 62: Data-Oriented Design - Graphics Compendium, accessed on December 31, 2025, [https://graphicscompendium.com/software/09-data-oriented-design](https://graphicscompendium.com/software/09-data-oriented-design)
16. Revisiting Data-Oriented Design - ACCU, accessed on December 31, 2025, [https://accu.org/journals/overload/30/167/teodorescu/](https://accu.org/journals/overload/30/167/teodorescu/)
17. Data Oriented Design - An Interpretation | Sebastian Schöner, accessed on December 31, 2025, [https://blog.s-schoener.com/2019-06-09-data-oriented-design/](https://blog.s-schoener.com/2019-06-09-data-oriented-design/)
18. Mike Acton's Data-Oriented Design Workshop (2015) - Dangling Pointers, accessed on December 31, 2025, [https://danglingpointers.com/post/mike-actons-dod-workshop-2015/](https://danglingpointers.com/post/mike-actons-dod-workshop-2015/)
19. JaiPrimer/JaiPrimer.md at master · BSVino/JaiPrimer - GitHub, accessed on December 31, 2025, [https://github.com/BSVino/JaiPrimer/blob/master/JaiPrimer.md](https://github.com/BSVino/JaiPrimer/blob/master/JaiPrimer.md)
20. Jonathan Blow–Preventing the Collapse of Civilization | Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=25788317](https://news.ycombinator.com/item?id=25788317)
21. Transcript of Preventing the collapse of civilization | Código y Fika, accessed on December 31, 2025, [https://codigoyfika.github.io/site/preventing-collapse/](https://codigoyfika.github.io/site/preventing-collapse/)
22. Jai Programming Language: A New Era of High-Performance Computing - Medium, accessed on December 31, 2025, [https://medium.com/@mayurkoshti12/jai-programming-language-a-new-era-of-high-performance-computing-9c676aad1089](https://medium.com/@mayurkoshti12/jai-programming-language-a-new-era-of-high-performance-computing-9c676aad1089)
23. Jonathan Blow on Deep Focus: r/programming - Reddit, accessed on December 31, 2025, [https://www.reddit.com/r/programming/comments/7ahzb4/jonathan_blow_on_deep_focus/](https://www.reddit.com/r/programming/comments/7ahzb4/jonathan_blow_on_deep_focus/)
24. Thoughts on Jai/Jonathan Blow's programming language designed for game dev? - Reddit, accessed on December 31, 2025, [https://www.reddit.com/r/gamedev/comments/if444t/thoughts_on_jaijonathan_blows_programming/](https://www.reddit.com/r/gamedev/comments/if444t/thoughts_on_jaijonathan_blows_programming/)
25. # **A week with Elixir -**     **Joe Armstrong - Erlang and other stuff, accessed on December 31, 2025, [https://joearms.github.io/published/2013-05-31-a-week-with-elixir.html](https://joearms.github.io/published/2013-05-31-a-week-with-elixir.html)**
26. Making reliable distributed systems in the presence of sodware errors - Erlang, accessed on December 31, 2025, [https://erlang.org/download/armstrong_thesis_2003.pdf](https://erlang.org/download/armstrong_thesis_2003.pdf)
27. What are the disadvantages of Erlang over other programming languages? - Quora, accessed on December 31, 2025, [https://www.quora.com/What-are-the-disadvantages-of-Erlang-over-other-programming-languages](https://www.quora.com/What-are-the-disadvantages-of-Erlang-over-other-programming-languages)
28. Erlang's let-it-crash philosophy - applicable elsewhere? [closed] - Stack Overflow, accessed on December 31, 2025, [https://stackoverflow.com/questions/4393197/erlangs-let-it-crash-philosophy-applicable-elsewhere](https://stackoverflow.com/questions/4393197/erlangs-let-it-crash-philosophy-applicable-elsewhere)
29. What's special about Erlang and Elixir? - Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=35966890](https://news.ycombinator.com/item?id=35966890)
30. 208 RR Erlang with Francesco Cesarini - Ruby Rogues - - Top End Devs, accessed on December 31, 2025, [https://topenddevs.com/podcasts/ruby-rogues/episodes/208-rr-erlang-with-francesco-cesarini](https://topenddevs.com/podcasts/ruby-rogues/episodes/208-rr-erlang-with-francesco-cesarini)
31. Building for reliability at HelloSign - Dropbox Tech Blog, accessed on December 31, 2025, [https://dropbox.tech/application/building-for-reliability-at-hellosign](https://dropbox.tech/application/building-for-reliability-at-hellosign)
32. Dr. Alan Kay on the meaning of object-oriented programming, accessed on December 31, 2025, [https://userpage.fu-berlin.de/~ram/pub/pub_jf47ht81Ht/doc_kay_oop_de](https://userpage.fu-berlin.de/~ram/pub/pub_jf47ht81Ht/doc_kay_oop_de)
33. Object-oriented programming - Wikipedia, accessed on December 31, 2025, [https://en.wikipedia.org/wiki/Object-oriented_programming](https://en.wikipedia.org/wiki/Object-oriented_programming)
34. Alan Kay on the Meaning of “Object-Oriented Programming” (2003) | Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=19415983](https://news.ycombinator.com/item?id=19415983)
35. Simple vs Easy - Christopher Frost, accessed on December 31, 2025, [https://chrisfrost.com/developer-tools/simple-vs-easy/](https://chrisfrost.com/developer-tools/simple-vs-easy/)
36. talk-transcripts/Hickey_Rich/SimpleMadeEasy.md at master - GitHub, accessed on December 31, 2025, [https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/SimpleMadeEasy.md](https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/SimpleMadeEasy.md)
37. TLA + in Practice and Theory Part 1: The Principles of TLA +, accessed on December 31, 2025, [https://pron.github.io/posts/tlaplus_part1](https://pron.github.io/posts/tlaplus_part1)
38. Leslie Lamport on Distributed Systems and Precise Thinking | Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=8477259](https://news.ycombinator.com/item?id=8477259)
39. Is Clean Code less Code?: r/coding - Reddit, accessed on December 31, 2025, [https://www.reddit.com/r/coding/comments/32c579/is_clean_code_less_code/](https://www.reddit.com/r/coding/comments/32c579/is_clean_code_less_code/)
40. Goodbye, Clean Code (2020) - Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=29239861](https://news.ycombinator.com/item?id=29239861)
41. Semantic Compression | Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=17090319](https://news.ycombinator.com/item?id=17090319)
42. [P] I accomplished 5000:1 compression by encoding meaning instead of data: r/programming - Reddit, accessed on December 31, 2025, [https://www.reddit.com/r/programming/comments/1mm6t2s/p_i_accomplished_50001_compression_by_encoding/](https://www.reddit.com/r/programming/comments/1mm6t2s/p_i_accomplished_50001_compression_by_encoding/)
43. February | 2020 | Read the Tea Leaves - Nolan Lawson, accessed on December 31, 2025, [https://nolanlawson.com/2020/02/](https://nolanlawson.com/2020/02/)
44. Hiring Philosophy - One2N, accessed on December 31, 2025, [https://one2n.io/playbook/how-we-hire/hiring-philosophy](https://one2n.io/playbook/how-we-hire/hiring-philosophy)
45. 'Make invalid states unrepresentable' considered harmful - Hacker News, accessed on December 31, 2025, [https://news.ycombinator.com/item?id=45164444](https://news.ycombinator.com/item?id=45164444)
46. "Making illegal states unrepresentable", a mini-revelation for me (5 minutes from CppCon 2016 talk by Ben Deane "Using Types Effectively"): r/cpp - Reddit, accessed on December 31, 2025, [https://www.reddit.com/r/cpp/comments/abh0hh/making_illegal_states_unrepresentable_a/](https://www.reddit.com/r/cpp/comments/abh0hh/making_illegal_states_unrepresentable_a/)
47. Enums and Pattern Matching in Rust: A Deep Dive into Type Safety and Control Flow, accessed on December 31, 2025, [https://dev.to/ajtech0001/enums-and-pattern-matching-in-rust-a-deep-dive-into-type-safety-and-control-flow-1gjp](https://dev.to/ajtech0001/enums-and-pattern-matching-in-rust-a-deep-dive-into-type-safety-and-control-flow-1gjp)
48. Platform Engineering Podcast, accessed on December 31, 2025, [https://www.platformengineeringpod.com/](https://www.platformengineeringpod.com/)
49. Unlocking the Power of Engineering Leadership - EngineeringX, accessed on December 31, 2025, [https://engineeringx.org/blog/unlocking-the-power-of-engineering-leadership](https://engineeringx.org/blog/unlocking-the-power-of-engineering-leadership)
