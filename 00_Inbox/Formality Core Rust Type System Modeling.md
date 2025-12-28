---
aliases: []
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-28T21:47:54+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
title: Formality Core Rust Type System Modeling
source: "https://gemini.google.com/share/2ca00ab7abd7"
author:
  - "[[Gemini]]"
published:
created: 2025-12-28T21:45:03+00:00
description: "Created with Gemini"
tags:
  - "clippings"
---

https://youtu.be/9qLACD9Bfbk?si=yDXiIrgo\_8A5vOgj

In this presentation at RustNL 2024, Niko Matsakis introduces **Formality Core**, a lightweight framework built in Rust for modeling and experimenting with type systems.

### Core Framework: Formality Core

The project addresses the increasing difficulty of maintaining a mental model of the Rust type system as it grows in complexity \[[01:08](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=68)\]. It prioritises **concept density** and clear logic over performance, aiming to provide an executable, formalised way to understand how the type checker works \[[02:10](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=130)\].

- **Grammar Definition**: Uses Rust structs and enums with a `#[term]` macro to autogenerate parsers and debug implementations \[[07:43](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=463)\].
- **Judgment Functions**: Encapsulates type-checking rules as Rust functions. Unlike standard deterministic code, these rules can represent non-deterministic logic (trying all possible rules to see which applies) \[[22:25](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=1345)\].
- **Inference Rule Notation**: Matsakis leverages the mathematical "Turnstyle" notation () inside Rust macros to make formal logic readable as "Given environment, expression has type " \[[19:01](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=1141)\].

### Theoretical vs. Practical Logic

The system is designed to bridge the gap between academic type theory and engineering practice:

- **The "Why"**: Traditional academic papers are often inaccessible \[[03:23](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=203)\]. Formality Core allows engineers to use notation from papers but execute it directly in Rust.
- **Soundness through Fuzzing**: The framework supports generating random programs to test if the type checker correctly prevents runtime errors in the interpreter \[[35:19](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=2119)\].
- **Tooling**: It integrates with `rust-analyzer` for "expect tests," allowing developers to iterate on type rules and automatically update expected outputs \[[34:07](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=2047)\].

### Strategic Objective for Rust

The long-term goal is to create a formal model of Rust that can be used during the RFC process to test new features before they are stabilised \[[44:38](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=2678)\]. It serves as an executable specification that can be fuzzed against the actual `rustc` compiler to find discrepancies and bugs \[[37:05](http://www.youtube.com/watch?v=9qLACD9Bfbk&t=2225)\].

**Key Links:**

- **Video:**[Type Theory for Busy Engineers - Niko Matsakis](http://www.youtube.com/watch?v=9qLACD9Bfbk)

https://youtu.be/1iPWt1gvT\_w?si=6B7m\_vOj-pW0rCzg

The video **"Rust and the price of ignoring theory"** by James Faure provides a critical analysis of the Rust programming language from the perspective of formal type theory and functional programming principles.

### Core Argument: The Theoretical Debt

Faure argues that Rust was developed "orthogonally to theory," leading to an "unbound and incomplete" type system \[[15:55](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=955)\]. He posits that by ignoring established research in functional programming and type theory, Rust has inherited fundamental flaws that are now difficult to rectify due to backwards compatibility pressures.

### 1\. Memory Management & Regions

- **Borrowing vs. Linearity**: Rust's ownership model is viewed as a "separate pass" that generates constraints, which Faure considers a "cop-out" compared to type-directed solutions \[[01:21](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=81)\]. He suggests that **linearity** (and graded modal types) is a more principled way to handle resources \[[18:58](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=1138)\].
- **Oxide & Regions**: He cites **Oxide** as a more successful formalisation of Rust using region-based aliasing \[[01:36](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=96)\]. Regions decouple data lifetimes from function lifetimes, effectively extending stack memory without the rigidity of the call stack \[[02:08](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=128)\].
- **The Adjunction**: Borrowing and linearity form an **adjunction**; Rust focuses on borrowing but misses the "more useful half" (linearity) which allows for better quantification of resource usage \[[18:58](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=1138)\].

### 2\. Type System Limitations

- **Unsoundness**: Faure points to a long-standing issue (unfixed since 2015) where Rust's subtyping allows casting a local lifetime to `'static` because constraints aren't properly tracked in function types \[[15:49](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=949)\].
- **GATs & Higher-Rank Types**: He describes Rust's Generalized Algebraic Data Types (GATs) as "second-class" and criticises the lack of true higher-kinded types \[[14:32](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=872), [36:03](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=2163)\].
- **Dependent Types**: He advocates for **dependent types** (as seen in Idris) to ensure correctness by construction, such as guaranteed in-bounds array access, which Rust handles via runtime panics \[[17:15](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=1035)\].

### 3\. Engineering & ABI Critiques

- **The ABI Mistake**: Rust repeats "mistakes of C via LLVM," failing to improve the Application Binary Interface (ABI) \[[04:39](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=279)\]. Faure suggests that small objects should be passed in registers rather than being forced to memory by outdated ABI rules \[[04:12](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=252)\].
- **Dynamic Linking**: He strongly criticises Rust's culture of static linking and bundling, calling it "obscene" for security \[[32:10](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=1930)\]. Static linking delays security patches and "trashes the cache" by duplicating code like `print f` across every executable \[[27:44](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=1664)\].

### 4\. Alternative Frameworks

- **Granule**: A research language mentioned for its use of **graded modal types**, which allows fine-grained control over how many times a resource is used (e.g., exactly twice) \[[20:16](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=1216)\].
- **Swift's Resilient Layout**: Swift is praised for its "resilient layout" and witness tables, which allow for a stable ABI and better dynamic linking compared to Rust's monomorphisation \[[28:40](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=1720)\].

### Conclusion

The video characterises Rust as a "stop-gap" language—better than C++ but inferior to principled functional languages like Haskell or OCaml \[[51:35](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=3095)\]. Faure's "Top-Down" view is that programming should be about **equations and transformations**, not "manually fiddling with mutable registers" \[[11:54](http://www.youtube.com/watch?v=1iPWt1gvT_w&t=714)\].

**Video Link:**[Rust and the price of ignoring theory](http://www.youtube.com/watch?v=1iPWt1gvT_w)

https://youtu.be/9vgBnSxEpUw?si=eJxzewDDBEz2RWOs

This presentation by Sagnik Bhattacharya explores the deep connection between computer science and mathematical logic through the **Curry-Howard Isomorphism**, demonstrating how type systems can be used to prove theorems and ensure program correctness.

### 1\. The Curry-Howard Isomorphism (CHI)

The core thesis is that **propositions are types** and **proofs are programs** \[[06:26](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=386)\]. If a type can be "inhabited" (i.e., you can create an instance of it), the corresponding logical proposition is proven true.

| Logical Concept | Programming Equivalent |
| --- | --- |
| **Proposition** | Type \[[06:36](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=396)\] |
| **Proof** | Program / Function \[[06:46](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=406)\] |
| **True** | Unit Type (e.g., `None` in Python, `()` in Rust) \[[09:42](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=582)\] |
| **False** | Bottom / Never Type (e.g., `NoReturn`, `!`) \[[10:42](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=642)\] |
| **Conjunction (A ∧ B)** | Tuple or Struct `(A, B)` \[[12:13](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=733)\] |
| **Disjunction (A ∨ B)** | Union Type or Enum `Either<A, B>` \[[12:51](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=771)\] |
| **Implication (A → B)** | Function definition `fn(A) -> B` \[[13:30](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=810)\] |
| **Universal Quantifier (∀)** | Generics \[[14:38](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=878)\] |

### 2\. Type-Level Programming & Formal Proofs

The speaker demonstrates how to use types to represent **Peano Axioms** for natural numbers \[[42:15](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=2535)\]:

- **Zero and Successor**: Numbers are defined as types: `Zero`, `Succ<Zero>` (1), `Succ<Succ<Zero>>` (2) \[[42:51](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=2571)\].
- **Recursive Logic**: Equality and addition are implemented as traits. The compiler "proves" addition at compile time by unrolling recursive type definitions \[[48:16](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=2896)\].
- **Logic Constraints**: He shows that while we can prove, intuitionistic logic (and thus most programs) cannot prove without specific language extensions, as you cannot extract evidence of from a function that returns the "Never" type \[[23:32](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=1412)\].

### 3\. Practical Engineering Application: Rust

The "Top-Down" value of this theory is its application in systems like Rust to eliminate runtime errors:

- **Memory Safety**: Rust uses its type system to track **Ownership and Borrowing** \[[29:57](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=1797)\]. The compiler acts as a logic engine to prove that no two pointers can mutably alias the same memory, preventing data races and dangling pointers at compile time \[[31:33](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=1893)\].
- **Static Analysis of Shapes**: Using "Type-level numbers," one can encode matrix dimensions into types. This allows the compiler to prove that a matrix multiplication is valid () before the code even runs, throwing a compilation error if the dimensions mismatch \[[35:14](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=2114), [37:50](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=2270)\].
- **Length-Indexed Lists**: Demonstrates a `Zip` function that only compiles if two lists have the exact same length, effectively moving a common runtime "IndexOutOfBounds" error to a compile-time logical proof \[[52:02](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=3122), [54:17](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=3257)\].

### Conclusion: "The Chef Analogy"

Bhattacharya compares a programmer to a chef writing a recipe \[[26:27](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=1587)\]. A weak type system lets you "add rat poison" to the spaghetti and only realize the mistake when someone eats it (runtime). A strong type system acts as an expert chef who rejects the recipe immediately if it doesn't make logical sense \[[27:44](http://www.youtube.com/watch?v=9vgBnSxEpUw&t=1664)\].

**Video Link:**[Types are Awesome | Curry-Howard Isomorphism](http://www.youtube.com/watch?v=9vgBnSxEpUw)

https://youtu.be/g7dcbdqGL78?si=eD2sWxi-Yw5D\_Igw

In this livestream, "Barry" works through **Chapter 1 of "Thinking with Types"** by Sandy Maguire, focusing on the fundamental algebraic properties of type systems.

### 1\. Cardinality and Inhabitants

The "cardinality" of a type is the number of distinct values (inhabitants) it can have \[[06:40](http://www.youtube.com/watch?v=g7dcbdqGL78&t=400)\].

- **Void**: 0 inhabitants (represents logical `False`).
- **Unit (`()`)**: 1 inhabitant (represents logical `True`).
- **Bool**: 2 inhabitants (`True`, `False`).
- **Numeric Types**: e.g., `Word8` has 256 inhabitants (0-255) \[[54:34](http://www.youtube.com/watch?v=g7dcbdqGL78&t=3274)\].

### 2\. Isomorphisms

Two types are **isomorphic** if they have the same cardinality \[[08:48](http://www.youtube.com/watch?v=g7dcbdqGL78&t=528)\]. This means you can define two functions, `to` and `from`, such that:

- `to. from == id`
- `from. to == id` \[[10:42](http://www.youtube.com/watch?v=g7dcbdqGL78&t=642)\] The presenter demonstrates this by showing that a custom `Spin` type (with `Up` and `Down`) is isomorphic to `Bool` \[[14:33](http://www.youtube.com/watch?v=g7dcbdqGL78&t=873)\]. He uses **QuickCheck** to automate the proof of these properties \[[36:34](http://www.youtube.com/watch?v=g7dcbdqGL78&t=2194)\].

### 3\. The Algebra of Types

The video maps standard algebraic operations to type constructors:

- **Sum Types (Addition)**: `Either a b` has a cardinality of \[[43:54](http://www.youtube.com/watch?v=g7dcbdqGL78&t=2634)\].
- **Product Types (Multiplication)**: Tuples `(a, b)` have a cardinality of \[[49:25](http://www.youtube.com/watch?v=g7dcbdqGL78&t=2965)\].
- **Exponential Types (Functions)**: A function `a -> b` has a cardinality of (result types raised to the power of input types) \[[01:03:42](http://www.youtube.com/watch?v=g7dcbdqGL78&t=3822)\].
	- *Example Exercise*: The cardinality of `Either Bool (Bool, Maybe Bool) -> Bool` is calculated as \[[01:08:16](http://www.youtube.com/watch?v=g7dcbdqGL78&t=4096)\].

### 4\. Curry-Howard Isomorphism

This is the bridge between logic and programming: **propositions are types** and **proofs are programs** \[[01:23:03](http://www.youtube.com/watch?v=g7dcbdqGL78&t=4983)\].

- A logical theorem like is equivalent to the programming isomorphism between `() -> a` and `a` \[[01:25:50](http://www.youtube.com/watch?v=g7dcbdqGL78&t=5150)\].
- The speaker proves by implementing the `curry` and `uncurry` functions \[[01:32:12](http://www.youtube.com/watch?v=g7dcbdqGL78&t=5532)\].
- He also proves the distributive law, showing that a function taking an `Either` is isomorphic to a tuple of two functions \[[01:59:38](http://www.youtube.com/watch?v=g7dcbdqGL78&t=7178)\].

### Summary of Isomorphic Proofs

The session concludes by successfully testing these isomorphisms in Haskell, reinforcing that boring mathematical identities (like) represent powerful architectural tools in software design \[[02:49:34](http://www.youtube.com/watch?v=g7dcbdqGL78&t=10174)\].

**Video Link:**[Thinking with Types, Chapter 1](http://www.youtube.com/watch?v=g7dcbdqGL78)

Google Account

Leon Ormes

leonormes@gmail.com
