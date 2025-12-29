---
title: ‎Gemini – direct access to Google AI
source: https://gemini.google.com/share/c23a4a54334f
author:
  - "[[Gemini]]"
published:
created: 2025-12-29
description: Created with Gemini
tags:
  - clippings
---
https://youtu.be/0wmcCdoExbM?si=TR4sL2UWNQ5W3P9Z

### Algebraic Data Types (ADTs) in Scala: Framework and Logic

Algebraic Data Types are a method of structuring data based on formal mathematical theory (Haskell and Category Theory influence), prioritising type safety and logic over implementation details \[[00:44](http://www.youtube.com/watch?v=0wmcCdoExbM&t=44)\].

---

### 1\. Core Mental Models

ADTs are categorised based on how they combine types: **Sum** (OR logic) and **Product** (AND logic).

- **Sum Types (OR Logic):** Represents a choice between a fixed set of variants.
	- **Concept:** A type is defined as being either Type A *or* Type B.
	- **Implementation:** Usually defined via a `sealed trait` or `sealed abstract class` to ensure the compiler can check for exhaustive pattern matching \[[03:05](http://www.youtube.com/watch?v=0wmcCdoExbM&t=185)\].
	- **Example:** A `Weather` type that is restricted to exactly `Sunny`, `Windy`, `Rainy`, or `Cloudy` \[[01:59](http://www.youtube.com/watch?v=0wmcCdoExbM&t=119)\].
- **Product Types (AND Logic):** Represents a combination of multiple values.
	- **Concept:** A type is defined as a cartesian product; it requires Value A *and* Value B.
	- **Implementation:** Typically implemented using `case classes` \[[06:04](http://www.youtube.com/watch?v=0wmcCdoExbM&t=364)\].
	- **Example:** A `WeatherForecastRequest` that requires both `latitude` and `longitude` \[[05:43](http://www.youtube.com/watch?v=0wmcCdoExbM&t=343)\].
- **Hybrid Types:** A "Sum of Products" framework, combining both models to represent complex domain states \[[06:44](http://www.youtube.com/watch?v=0wmcCdoExbM&t=404)\].

---

### 2\. Underlying Design Logic

The primary objective of using ADTs is to improve the robustness and reasoning of a system through the following frameworks:

- **Making Illegal States Unrepresentable:** By using sealed hierarchies instead of primitive types (like Strings), you restrict the state space to only valid domain values. This prevents runtime errors by ensuring invalid data cannot be instantiated at the type level \[[08:29](http://www.youtube.com/watch?v=0wmcCdoExbM&t=509)\], \[[11:46](http://www.youtube.com/watch?v=0wmcCdoExbM&t=706)\].
- **Compositionality:** ADTs are highly composable; one ADT can be nested within another to build complex, tree-like data structures without increasing logic overhead \[[08:46](http://www.youtube.com/watch?v=0wmcCdoExbM&t=526)\].
- **Decoupling Data from Functionality:** ADTs act as pure data containers. This separation aligns with functional programming principles, promoting immutability and thread safety for parallel or distributed systems \[[09:00](http://www.youtube.com/watch?v=0wmcCdoExbM&t=540)\].
- **Complexity Reduction:** By limiting the "cardinality" (the number of possible values a type can hold), you reduce the complexity of testing and the surface area for bugs \[[12:08](http://www.youtube.com/watch?v=0wmcCdoExbM&t=728)\].

---

**Source:**[Algebraic Data Types (ADT) in Scala | Rock the JVM](https://www.google.com/search?q=https://youtu.be/0wmcCdoExbM)

https://youtu.be/c-sM\_KjBlEE?si=mGoOB2bYm6w\_YTrH

The provided video outlines the architectural framework of Algebraic Data Types (ADTs) within Rust's type system, mapping type structures to mathematical logic.

### Structural Framework of ADTs in Rust

#### 1\. Atomic Values (Base Units)

- **Zero (Void/Bottom Type):** Represented as an uninhabited `enum Void {}` or the `!` (never) type. This type has no possible values and is typically used for diverging functions that never return \[[00:35](http://www.youtube.com/watch?v=c-sM_KjBlEE&t=35)\].
- **One (Unit):** Represented as `()`. This type has exactly one possible value, which is itself. It serves as a "no-op" in terms of data density \[[00:35](http://www.youtube.com/watch?v=c-sM_KjBlEE&t=35)\].

#### 2\. Core Type Operations

- **Addition (Sum Types):** Implemented via `enum { A, B }`. This represents the logic of **choice** —the resulting instance is *either* A *or* B \[[00:35](http://www.youtube.com/watch?v=c-sM_KjBlEE&t=35)\].
- **Multiplication (Product Types):** Implemented via `tuple (A, B)` or structs. This represents the logic of **combination** —the resulting instance contains *both* A *and* B \[[00:35](http://www.youtube.com/watch?v=c-sM_KjBlEE&t=35)\].

#### 3\. Mathematical Equivalences (Rules of the System)

The type system follows formal algebraic rules \[[00:35](http://www.youtube.com/watch?v=c-sM_KjBlEE&t=35)\]:

- **Commutativity:** Addition (`a + b = b + a`) and Multiplication (`a * b = b * a`) allow for reordering variants or fields without changing the logical capacity of the type.
- **Identity Elements:**
	- Adding Zero: `0 + x = x` (an enum with a 'never' variant is logically equivalent to the other variant).
	- Multiplying by One: `1 * x = x` (a tuple with a unit type `()` is logically equivalent to the other type).
- **Annihilation:**`0 * x = 0`. A product type containing an uninhabited type (`!`) becomes uninhabited itself, as the type cannot be constructed.

### Mental Model: Types as Logic

The system treats types as logical propositions where `A => B` corresponds to the existence of a function `fn(A) -> B`. For maximum type safety, it is recommended to express `Void` as an uninhabited enum to ensure the compiler can enforce that certain states are unreachable \[[01:04](http://www.youtube.com/watch?v=c-sM_KjBlEE&t=64)\].

**Source:**[Understanding Rust's Type System: A Guide to Algebraic Data Types (ADTs)](http://www.youtube.com/watch?v=c-sM_KjBlEE)

https://youtu.be/CUdp1XGwRng?si=FpWP49GiJl602CBj

### Algebraic Data Types (ADTs) in C#: Framework and Automation

The following framework outlines the application of Algebraic Data Types within C#, transitioning from mathematical theory to automated implementation strategies.

---

### 1\. Mathematical Mental Model: Types as Sets

The fundamental logic treats a **Type** as a set of possible values \[[02:02](http://www.youtube.com/watch?v=CUdp1XGwRng&t=122)\]. ADTs are constructed through two primary algebraic operations:

- **Product Types (AND Logic):** Represents a combination where the total cardinality is the multiplicative product of the constituent types (e.g., a struct with an `int` and a `byte`) \[[03:03](http://www.youtube.com/watch?v=CUdp1XGwRng&t=183)\].
- **Sum Types (OR Logic):** Represents a choice where the total cardinality is the sum of the constituent types \[[03:52](http://www.youtube.com/watch?v=CUdp1XGwRng&t=232)\]. Each variant is "tagged" to distinguish it within the set \[[03:42](http://www.youtube.com/watch?v=CUdp1XGwRng&t=222)\].

---

### 2\. Domain Modelling Logic

The primary motivation for ADTs in C# is to shift validation from runtime to compile-time.

- **Making Illegal States Unrepresentable:** Traditional C# modelling often uses large records with nullable fields, requiring complex runtime validation \[[07:11](http://www.youtube.com/watch?v=CUdp1XGwRng&t=431)\]. ADTs ensure that only valid combinations (e.g., a `Payment` that is specifically a `CreditCard` *with* a number) can exist in the type system \[[07:30](http://www.youtube.com/watch?v=CUdp1XGwRng&t=450)\].
- **Closed Hierarchies:** Unlike standard inheritance which is "open," ADTs use a "closed" hierarchy \[[14:05](http://www.youtube.com/watch?v=CUdp1XGwRng&t=845)\]. This enables the compiler to enforce exhaustiveness, ensuring every possible state is handled during pattern matching or dispatch \[[13:49](http://www.youtube.com/watch?v=CUdp1XGwRng&t=829)\].

---

### 3\. Implementation Framework in C#

Since C# lacks native "Sum Type" syntax (like F# or Scala), a structured architectural pattern is required to simulate them:

- **Structural Components:**
	- **Sealed Partial Abstract Class:** Prevents external inheritance and ensures a closed set of variants \[[15:06](http://www.youtube.com/watch?v=CUdp1XGwRng&t=906)\].
	- **Private Constructor:** Prevents direct instantiation of the base type \[[15:18](http://www.youtube.com/watch?v=CUdp1XGwRng&t=918)\].
	- **Nested Variant Classes:** Internal classes representing the specific choices \[[15:39](http://www.youtube.com/watch?v=CUdp1XGwRng&t=939)\].
- **Functional Dispatch (The Match Function):** Instead of `if/else` or `switch` statements on types, a `Match` method is implemented using lambdas for each variant \[[16:04](http://www.youtube.com/watch?v=CUdp1XGwRng&t=964)\]. This provides static safety; adding a new variant forces a compiler error at every call site until the new case is handled \[[17:07](http://www.youtube.com/watch?v=CUdp1XGwRng&t=1027)\].

---

### 4\. Meta-Strategy: DSL-Driven Code Generation

The "How" of implementing ADTs efficiently involves lifting the abstraction level to **Intent**:

- **Abstraction over Boilerplate:** Rather than manually writing hundreds of lines of boilerplate for value semantics (equality, hash codes) and dispatch logic, the developer defines the "intent" in a domain-specific language (DSL) \[[19:00](http://www.youtube.com/watch?v=CUdp1XGwRng&t=1140)\].
- **The Transformation Pipeline:**
	1. **Syntax/Parser:** Text is parsed into an Abstract Syntax Tree (AST) \[[30:59](http://www.youtube.com/watch?v=CUdp1XGwRng&t=1859)\].
	2. **Validation/Rewriting:** The AST is refined or transformed \[[34:46](http://www.youtube.com/watch?v=CUdp1XGwRng&t=2086)\].
	3. **Code Generation (Roslyn):** The custom AST is transformed into a Roslyn AST to generate idiomatic C# code \[[36:55](http://www.youtube.com/watch?v=CUdp1XGwRng&t=2215)\].
- **Visual Studio Integration:** Using "Single File Generators" allows this process to happen automatically upon saving a file, providing a seamless developer experience with "code-behind" files \[[50:32](http://www.youtube.com/watch?v=CUdp1XGwRng&t=3032)\].

**Source:**[Algebraic Data Types for C# - John Azariah](http://www.youtube.com/watch?v=CUdp1XGwRng)

https://youtu.be/Amx7cVz1Qks?si=FCtTr7zm9aAvQUAE

### Category Theory and Algebraic Data Types (ADTs): An Algebraic Framework

The following framework outlines the categorisation of types as algebraic structures, moving beyond implementation syntax to the underlying mathematical logic.

---

### 1\. The Type System as a Semi-ring (Rig)

The fundamental mental model treats the type system as a **Semi-ring** (often termed a **Rig** because it lacks 'n'egative elements) \[[01:11:33](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=4293)\], \[[01:17:33](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=4653)\].

- **Sum Types (Addition):** Represented by `Either` or `sealed traits`. This is the logic of "OR" \[[19:56](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=1196)\].
	- **Additive Identity (0):** The `Void` type (the empty set). . Adding a `Void` variant to a sum type does not change its logical capacity \[[20:14](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=1214)\], \[[01:14:56](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=4496)\].
- **Product Types (Multiplication):** Represented by tuples or records. This is the logic of "AND" \[[00:52](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=52)\].
	- **Multiplicative Identity (1):** The `Unit` type (singleton set). . Including a `Unit` value in a product does not increase information density \[[11:24](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=684)\].

---

### 2\. Structural Isomorphisms and Formal Laws

ADTs follow formal algebraic laws that ensure consistency across complex data structures:

- **Commutativity:** The order of types in a sum or product can be reordered via an isomorphism (e.g., `Swap`) without loss of data \[[11:04](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=664)\], \[[01:14:03](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=4443)\].
- **Associativity:** Nesting of products (e.g., `(A, (B, C))`) is isomorphic to flat structures, enabling the treatment of the category of sets as a **Monoidal Category** \[[10:01](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=601)\], \[[11:39](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=699)\].
- **Distributivity:** Multiplication distributes over addition: . This allows for the decomposition of complex data requests into logical branches \[[01:17:05](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=4625)\].
- **Annihilation:** Multiplying any type by `Void` results in `Void` (). If a product requires an uninhabitable type, the entire product becomes unconstructible \[[01:08:22](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=4102)\], \[[01:16:15](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=4575)\].

---

### 3\. Logical and Practical Implications

- **Curry-Howard Isomorphism:** There is a direct mapping between types and logic propositions (e.g., represents an implication) \[[31:37](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=1897)\].
- **Automated Derivation:** By defining data as a sum or product of known types, the compiler can automatically derive functionality (equality, serialisation, etc.) through structural induction \[[04:20](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=260)\].
- **State Space Reduction:** Using closed sum types (sealed hierarchies) allows the compiler to enforce exhaustive checking, ensuring all logical branches are handled \[[26:56](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=1616)\].

---

**Implementation Reference:**

- **Functional (Haskell/Scala):** High concept density via native sum/product syntax \[[16:56](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=1016)\].
- **Object-Oriented (Java/C++):** Traditionally faked via inheritance or pointers, which introduces "Bottom" types (nulls) that break the formal algebraic rigour \[[21:01](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=1261)\], \[[23:14](http://www.youtube.com/watch?v=Amx7cVz1Qks&t=1394)\].

**Source:**[Category theory - Algebraic Data Types (ADTs) preparing a presentation](http://www.youtube.com/watch?v=Amx7cVz1Qks)

https://youtu.be/z-0-bbc80JM?si=tKf2wTUlZmiX6Ato

### Rust Data Modelling Framework: Eliminating Invalid States

This modelling strategy prioritises type-level constraints over runtime verification, shifting the burden of logic correctness from the developer to the compiler.

---

### 1\. Algebraic Type Systems: Sum vs Product Logic

The framework distinguishes between two fundamental methods of data aggregation:

- **Product Types (AND Logic):** Represented by structs or classes. These are containers for multiple attributes where every field must exist simultaneously.
- **Sum Types (OR Logic):** Implemented via Rust "fat enums" or "tagged unions." Unlike primitive enums in other languages, these variants carry distinct data payloads.
- **Conceptual Logic:** Sum types allow you to model mutually exclusive states directly. For example, a "dead" state variant can omit attributes (like "hunger") that are only relevant to an "alive" state, ensuring the compiler prevents logical errors that would otherwise require runtime checks.

### 2\. Data Normalisation Framework

This approach rejects Object-Oriented (OO) inheritance in favour of relational database principles.

- **Relational Structs:** Data is modelled as tables (structs) in Third Normal Form (3NF) to reduce redundancy and ensure loose coupling between entities.
- **The Newtype Pattern:** Using tuple structs to wrap primitive types (e.g., `Image(String)`) enriches the model with domain-specific meaning, preventing the accidental use of arbitrary primitives where a specific domain type is required.

### 3\. Robust State Machines

States and their valid transitions are formalised using the type system to provide mathematical safety guarantees.

- **Exhaustive Matching:** By matching on a tuple of `(current_state, transition_event)`, the compiler enforces that every possible state-transition combination is explicitly handled.
- **Eliminating Edge Cases:** This architecture removes the need for arbitrary `if/else` statements; unreachable or invalid transitions are rejected at compile-time, ensuring no illegal states can ever be represented.

### Core Mental Model

By enriching the data model with a rigorous type system rather than relying on anonymous strings or integers, you create "zero-cost abstractions" that provide extreme safety with no runtime performance overhead.

**Source:**\[1\] [Rust Data Modelling Without Classes](https://youtu.be/z-0-bbc80JM)

https://youtu.be/ESFxbTTvHek?si=eF6xyqGOGjekY8KM

### Algebraic Data Types (ADTs): A Theoretical Framework

Algebraic Data Types serve as the primary methodology for data modelling in Rust, prioritising type safety and representational correctness through formal logic.

---

### 1\. Core Mental Models: The Algebra of Types

The framework treats types as sets where the "algebra" refers to how the number of possible values (cardinality) is calculated.

- **Product Types (AND Logic):**
	- **Structure:** Represented by `structs`. A product type requires multiple fields to exist simultaneously.
	- **Logic:** The cardinality is the **product** of the possibilities for each field. For instance, an employee struct with two boolean fields has possible states.
- **Sum Types (OR Logic):**
	- **Structure:** Represented by `enums`. A sum type represents a choice between distinct, mutually exclusive variations.
	- **Logic:** The cardinality is the **sum** of the variations. A card suit enum (Hearts, Diamonds, Spades, Clubs) has exactly 4 possible values.

---

### 2\. Architectural Principle: Correctness by Construction

The primary design goal of ADTs is the philosophy of **"Making Impossible States Impossible"**.

- **Constraint vs. Primitive:** By using specific types (like an enum for card ranks) instead of primitives (like integers), you eliminate invalid

You stopped this response

https://youtu.be/sGeQxdHWulo?si=ZhihT9iE550w4OGe

### Domain-Driven Design (DDD) with Algebraic Data Types (ADTs)

The following framework outlines how Algebraic Data Types (ADTs) serve as a mechanism for enforcing business domain constraints at the compiler level, rather than through runtime validation.

---

### 1\. Core Framework: Types as Constraints

The fundamental logic of this approach is to use the type system to ensure that implementation complies strictly with the domain model.

- **Product Types (AND Logic):** Represented as records or tuples. These combine multiple values where every field is mandatory (e.g., a 2D point requiring both X and Y).
- **Sum Types (OR Logic):** Represented as Discriminated Unions. These model mutually exclusive choices (e.g., a book is *either* an Audiobook, an E-book, *or* a Printed book).
- **Compile-Time Verification:** By defining a domain as a sum of specific products, the compiler enforces that only valid combinations of data can be instantiated.

---

### 2\. Paradigm Comparison: Structural Efficiency

The video evaluates three paradigms for data modelling using the example of 2D and 3D points:

| Paradigm | Architectural Logic | Limitations |
| --- | --- | --- |
| **Imperative** | Uses structs and value types for performance. | Lacks polymorphism; requires manual copying for state extension. |
| **Object-Oriented** | Uses inheritance (abstract classes) for code reusability and encapsulation. | Logic is bound to classes; "Downcasting" to specific types is prone to runtime errors. |
| **Functional (ADTs)** | Uses exhaustive pattern matching; logic is decoupled from data structures. | Immutability can lead to higher memory allocation if not managed. |

---

### 3\. Mental Model: Making Illegal States Unrepresentable

The ultimate goal of ADTs in DDD is to create a system where invalid data cannot even be expressed in code.

- **Logic Isolation:** For example, an `Audiobook` type does not contain a `pages` field. In an OO model, one might have a nullable `pages` property, but an ADT model prevents the code from even attempting to access pages on an audio format.
- **Domain Encapsulation:** By hiding private constructors, developers can restrict primitive types (like integers) to valid domain ranges (e.g., a `Rating` type that can *only* represent values from 1 to 5).
- **Exhaustiveness:** The compiler flags any logic that fails to handle a specific domain variant (e.g., forgetting to handle the `3D Point` case), ensuring total coverage of the business logic.

---

### 4\. Design Strategy: Separation of Design and Implementation

- **Code as Documentation:** Domain definitions (ADTs) act as a living repository of business rules that evolve with the application's lifetime.
- **Composition over Inheritance:** Complex domain objects (like travel bookings) are built by composing small "lego-like" blocks of types rather than deep inheritance trees.

**Source:**[Domain Driven Design (DDD) with Algebraic Data Types (ADT)](http://www.youtube.com/watch?v=sGeQxdHWulo)

https://youtu.be/gwlyrj1JtrE?si=JQstkBvmXouOVqeF

### Simple Algebraic Data Types: A Category Theoretic Framework

Algebraic Data Types (ADTs) are characterised by the mapping of type constructions to formal algebraic operations, primarily within the category of sets (**Set**). This framework treats types as objects that can be combined through multiplication (Product) and addition (Sum) \[[01:55](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=115)\].

---

### 1\. Structural Framework: Product and Sum Types

The type system is built upon two dual operations derived from category theory \[[03:45](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=225)\].

- **Product Types (Logical AND):**
	- **Mathematical Basis:** Corresponds to the **Product** in category theory. In the category of sets, this is the cartesian product \[[02:09](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=129)\].
	- **Implementation:** Canonical implementations include pairs, tuples, `structs`, or `classes`. They represent a combination where all constituent types must coexist \[[01:14](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=74)\].
	- **Records:** A specific form of product type that names its elements (fields), facilitating easier data extraction compared to unnamed tuples \[[02:34](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=154)\].
- **Sum Types (Logical OR):**
	- **Mathematical Basis:** Corresponds to the **Co-product**. In the category of sets, this is the disjoint sum \[[03:51](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=231)\].
	- **Implementation:** Implemented as `Either` (Haskell), `enums` (Rust), or `variants`. They represent a choice between mutually exclusive variants \[[03:56](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=236)\].

---

### 2\. The Algebra of Types: The Rig Framework

The "Algebra" in ADTs refers to the isomorphism between types and other mathematical systems, such as natural numbers and logic \[[06:51](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=411)\].

| Mathematical Concept | Logic Proposition | Type Theory Equivalent |
| --- | --- | --- |
| **0** | False | **Void** (Initial Object) \[[07:34](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=454)\] |
| **1** | True | **Unit** (Terminal Object) \[[07:34](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=454)\] |
| **Addition (+)** | OR () | **Sum Type** (`Either`, `Enum`) \[[07:40](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=460)\] |
| **Multiplication ()** | AND () | **Product Type** (`Pair`, `Struct`) \[[07:47](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=467)\] |

This deep relationship forms the basis of the **Curry-Howard Isomorphism**, which formalises the link between logic theory and type theory \[[07:59](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=479)\].

---

### 3\. Functional Applications: Optionality and Isomorphism

- **Handling Optionality:** Instead of using "sentinel values" (e.g., null pointers or -1), ADTs formalise the presence or absence of a value using sum types like `Maybe` or `Option` \[[04:53](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=293)\].
	- `Maybe a = Nothing | Just a`
	- `Option<T> = None | Some(T)`
- **Type Isomorphism:** Two types are considered isomorphic if there is no loss of information between them. This is proven by constructing bi-directional conversion functions \[[08:34](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=514)\]. For example, `Maybe a` is isomorphic to `Either Unit a` \[[08:41](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=521)\].

---

### 4\. Domain Modelling Logic

The framework advocates for **composition** over inheritance. By combining simple product and sum types, developers can build complex, recursive data structures (such as lists) that are logically sound and verified by the compiler \[[06:51](http://www.youtube.com/watch?v=gwlyrj1JtrE&t=411)\].

**Source:**[Category Theory for Programmers: Chapter 6 - Simple Algebraic Data Types](http://www.youtube.com/watch?v=gwlyrj1JtrE)

https://youtu.be/4ifyBOlDvWo?si=s0u2OvyCcaeNS0Vw

### Algebraic Data Types (ADTs) and Trees: A Conceptual Framework

The video establishes a high-level equivalence between Algebraic Data Types and Tree structures, framing them as mechanisms for total data control and representational correctness \[[00:17](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=17)\].

---

### 1\. ADTs: Logic and Control

The core utility of an ADT is to move beyond "loose" primitive types (like Strings) to a controlled state space.

- **Representational Control:** Using a primitive String for a "Gender" field allows for invalid states (e.g., "dad" or arbitrary text). An ADT (Sum Type) restricts the field to a predefined set of valid variants, ensuring "illegal states are unrepresentable" \[[01:20](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=80)\], \[[02:43](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=163)\].
- **Type Identity:** Each variant of an ADT is a unique type. Operations performed on these variants must be defined via specific functions or instances (e.g., defining how two "Gender" types are compared for equality) \[[03:17](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=197)\], \[[06:21](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=381)\].
- **Flexible Instances:** Since variants aren't strings, their logic (equality, string conversion) must be explicitly mapped via pattern matching. This allows for high flexibility, such as defining "wildcard" variants that are considered equal to all others \[[07:34](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=454)\], \[[08:19](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=499)\].

---

### 2\. Trees as ADTs

A Tree is a recursive ADT. In the context of the Clean programming language, it is defined by two fundamental cases:

- **The Node (Product Case):** A structure containing a value and two sub-trees (Left and Right) \[[30:57](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=1857)\].
- **The Leaf (Base Case):** A terminal point representing an empty sub-tree or the end of a branch \[[40:18](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=2418)\].
- **Binary Search Tree (BST) Logic:** A BST adds a formal constraint to the ADT structure: for every node , all values in the left sub-tree are , and all values in the right sub-tree are \[[32:53](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=1973)\].

---

### 3\. Recursion Frameworks for Tree Operations

Operating on a recursive ADT requires a systematic approach to traversal and construction.

- **The Look-Ahead Pattern:** In operations like finding a minimum or inserting a node, one must "look ahead" at the sub-tree before stepping into it. This prevents the algorithm from "stepping into a leaf" (losing the current value) and allows it to stop at the parent of the target position \[[01:14:17](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=4457)\].
- **Recursive Construction:** Because ADTs are immutable, "changing" a tree involves building an entirely new tree. This is done by recursively copying nodes while applying transformations to values as they are re-instantiated into the new structure \[[01:21:22](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=4882)\], \[[01:31:00](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=5460)\].
- **Pattern Matching vs. Utility Functions:**
	- **Pattern Matching:** Objectively more efficient; extracts values (), Left (), and Right () sub-trees directly in the function signature \[[01:17:14](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=4634)\].
	- **Utility Functions:** Using functions like `extractNode`, `goLeft`, and `goRight`. This provides a more readable "utility" layer but can be less efficient \[[01:06:34](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=3994)\], \[[01:16:48](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=4608)\].

---

### 4\. Domain-Specific Logic: Example (Network Router)

ADTs are effectively used to model network protocols where a "Return Status" might be a Sum Type \[[21:36](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=1296)\]:

- **OK Status:** Contains a product of details (Name, IP, Online Status).
- **No Status:** A terminal variant representing an error or offline state. This ensures that the application logic only attempts to process router details when the status is explicitly "OK" \[[27:01](http://www.youtube.com/watch?v=4ifyBOlDvWo&t=1621)\].

**Source:**[Trees and Algebraic Data Types in a Nutshell](http://www.youtube.com/watch?v=4ifyBOlDvWo)

https://youtu.be/r7Qlh9ioX1s?si=FEmmI39F-d9lViGi

### Product and Sum Types: A Data Modelling Framework

Product and Sum types constitute the fundamental building blocks of **Algebraic Data Types (ADTs)**. This framework allows for the precise calculation of a system's state space, ensuring that domain models are logically sound and type-safe \[[00:31](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=31)\].

---

### 1\. Core Mathematical Framework

The names "Product" and "Sum" are derived from how the total number of possible states (cardinality) is calculated for a given type \[[04:18](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=258)\].

- **Product Types (AND Logic):**
	- **Logic:** A type composed of multiple fields that must all exist simultaneously \[[15:53](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=953)\].
	- **Calculation:** The total cardinality is the **product** of the possibilities for each field. For example, two fields with 3 states each result in possible states \[[02:21](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=141), [04:18](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=258)\].
	- **Implementations:** Tuples (e.g., pairs, triples), records, structs, and hash maps \[[06:01](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=361), [19:37](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=1177)\].
- **Sum Types (OR Logic):**
	- **Logic:** A type that represents a choice between mutually exclusive variants (Exclusive OR) \[[15:39](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=939), [21:28](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=1288)\].
	- **Calculation:** The total cardinality is the **sum** of the possible states. Adding a "none" case to a status enum increases the state count by one \[[05:20](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=320), [21:14](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=1274)\].
	- **Implementations:** Enums, `Either`, and `Option` / `Maybe` types \[[05:30](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=330), [06:18](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=378)\].

---

### 2\. Architectural Objective: Eliminating Invalid States

A primary goal in data modelling is to ensure that **"illegal states are unrepresentable."** Using the wrong type structure leads to "combinatorial explosion" of invalid states, requiring excessive runtime conditional logic \[[06:47](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=407), [07:48](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=468)\].

- **The Workflow Problem:** Modelling a two-step approval process with a tuple of two 3-state fields (Unchecked, Approved, Rejected) creates 9 states. However, logic dictates that a second check cannot happen before the first, and a check shouldn't occur after a rejection \[[01:57](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=117), [03:02](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=182)\].
- **Logical Refinement:** By switching from a pure product (tuple) to a more tailored sum type, you can reduce the state space to exactly match the valid business rules (e.g., exactly 5 valid states: 0 Checked, 1 Approved, 2 Approved, 1st Rejected, 2nd Rejected) \[[11:55](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=715), [12:43](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=763)\].

---

### 3\. Advanced Structures: Recursive ADTs

Lists represent a unique hybrid framework where the sum type is recursive \[[15:19](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=919)\].

- **Recursive Logic:** A list is defined as either an **Empty List** OR (**An Element AND the rest of the list**) \[[15:30](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=930), [16:00](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=960)\].
- **Unbounded Complexity:** Because the definition is recursive, the state space becomes infinite and unbounded, allowing for flexible growth (e.g., extending a 2-step approval process to steps) \[[16:16](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=976), [17:33](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=1053)\].

---

### 4\. Paradigmatic Implementation

- **Strict (Haskell):** Provides explicit, compiler-checked Sum and Product types \[[20:43](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=1243)\].
- **Idiomatic (Clojure/JavaScript):** Lacks native sum types but simulates them through "hacks" such as using keywords or strings for enums, and vectors or maps for products \[[19:25](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=1165), [20:12](http://www.youtube.com/watch?v=r7Qlh9ioX1s&t=1212)\].

**Source:**[What are product and sum types?](https://www.google.com/search?q=https://youtu.be/r7Qlh9ioX1s)

https://youtu.be/y9ONOUm62\_A?si=pCIeTIAcOzL5rcd2

This presentation by Tomasz Barański, titled "Functional Programming Guerilla in the Land of Rust," provides an architectural framework for implementing functional paradigms within a systems programming language. It establishes Rust as a platform capable of high-level functional abstraction without compromising low-level performance \[[28:48](http://www.youtube.com/watch?v=y9ONOUm62_A&t=1728)\].

### 1\. Functions as First-Class Entities

Rust treats functions as first-class citizens, a core requirement for functional programming.

- **Definition:** Functions and closures can be created on-demand, stored in variables, passed as arguments, and returned from other functions \[[00:17](http://www.youtube.com/watch?v=y9ONOUm62_A&t=17)\].
- **Memory Management:** Closures are strongly typed and can be allocated on the heap (using `Box`) or stack. The compiler often optimises these allocations away, ensuring that high-level abstractions remain zero-cost \[[02:41](http://www.youtube.com/watch?v=y9ONOUm62_A&t=161)\].
- **Type Inference:** The language employs type inference similar to Haskell, allowing the developer to focus on logic while the compiler handles structural details \[[01:46](http://www.youtube.com/watch?v=y9ONOUm62_A&t=106)\].

### 2\. Framework for Controlled Purity

While not strictly pure like Haskell, Rust enforces "practical purity" through its ownership and mutability model.

- **Immutable by Default:** Functions that do not explicitly declare parameters as `mut` (mutable) are guaranteed not to modify the original object, effectively functioning as pure operations \[[06:42](http://www.youtube.com/watch?v=y9ONOUm62_A&t=402)\].
- **The Unsafe Escape Hatch:** Purity and safety can be explicitly bypassed using the `unsafe` keyword. This acts as a clear marker for developers that a specific block of code requires manual verification for side effects or memory safety \[[08:21](http://www.youtube.com/watch?v=y9ONOUm62_A&t=501)\].
- **System Integrity:** This hybrid model allows low-level hardware interaction while maintaining high-level logical guarantees in the rest of the application \[[08:38](http://www.youtube.com/watch?v=y9ONOUm62_A&t=518)\].

### 3\. Data Modelling: ADTs and Traits

Rust leverages Algebraic Data Types (ADTs) and Traits to model complex domain logic.

- **Algebraic Data Types (ADTs):** Implemented via `enums` that carry data payloads. Unlike C-style enums, Rust enums can represent complex structures like `Option<T>` (equivalent to Haskell's `Maybe`), allowing for exhaustive pattern matching verified by the compiler \[[09:53](http://www.youtube.com/watch?v=y9ONOUm62_A&t=593)\], \[[10:46](http://www.youtube.com/watch?v=y9ONOUm62_A&t=646)\].
- **Traits as Type Classes:** Traits define shared behaviour across types, functioning similarly to Haskell's type classes. They allow for bounded polymorphism, where generic types are restricted to those that provide specific functionality (e.g., the `Display` or `EQ` traits) \[[13:58](http://www.youtube.com/watch?v=y9ONOUm62_A&t=838)\], \[[15:10](http://www.youtube.com/watch?v=y9ONOUm62_A&t=910)\].
- **Automated Derivation:** The compiler can automatically derive standard traits like equality or cloning, reducing boilerplate while maintaining rigorous type safety \[[15:54](http://www.youtube.com/watch?v=y9ONOUm62_A&t=954)\].

### 4\. Metaprogramming and Zero-Cost Composition

The macro system provides a mechanism for extending the language syntax and implementing functional patterns not natively supported.

- **Hygienic Macros:** Macros enable syntax extensions (e.g., `vec!` for list literals) and recursive code generation \[[19:37](http://www.youtube.com/watch?v=y9ONOUm62_A&t=1177)\].
- **Function Composition:** Since Rust does not support point-free function composition out of the box, macros can be used to generate recursive closures that compose arbitrary numbers of functions at compile-time \[[22:48](http://www.youtube.com/watch?v=y9ONOUm62_A&t=1368)\], \[[24:28](http://www.youtube.com/watch?v=y9ONOUm62_A&t=1468)\].
- **Optimization:** Benchmarks indicate that handcrafted imperative code and macro-generated functional compositions result in identical binary performance. The compiler successfully collapses temporary closures into direct machine instructions \[[27:27](http://www.youtube.com/watch?v=y9ONOUm62_A&t=1647)\].

**Source:**[Functional programming guerilla in the land of Rust - Tomasz Barański](http://www.youtube.com/watch?v=y9ONOUm62_A)

https://youtu.be/8fWK2iYgsz8?si=0eeGoCvHea9btBrW

### Practical Application of Algebraic Data Types (ADTs) in TypeScript

This presentation details how Algebraic Data Types solve the "billion-dollar mistake" of null references by shifting error handling and state management from runtime checks to the type system \[[03:00](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=180)\].

---

### 1\. The Core Mental Model: Types as Containers

ADTs in TypeScript (facilitated by libraries like `fp-ts`) act as **containers** for values, where the type explicitly declares the presence, absence, or state of the data \[[10:37](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=637)\]. This moves the developer away from defensive programming (e.g., constant `if (x !== undefined)` checks) toward a declarative flow \[[13:31](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=811)\].

---

### 2\. Essential ADT Frameworks

#### Option (Maybe): Eliminating Null/Undefined

- **Concept:** A container that is either `Some<A>` (contains a value) or `None` (empty) \[[10:16](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=616)\].
- **Logic:** Instead of returning `undefined`, a function returns an `Option`. To access the data, you use `map` (to transform the value if it exists) or `fold` (to define both the "success" and "empty" cases) \[[13:31](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=811)\], \[[15:53](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=953)\].
- **Result:** The compiler ensures you cannot access the value without first accounting for the possibility that it might be missing \[[14:00](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=840)\].

#### Either: Robust Error Handling

- **Concept:** A container that is either `Left<E>` (failure with an error message/object) or `Right<A>` (success with data) \[[19:43](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=1183)\].
- **Logic:** Unlike `Option`, `Either` captures *why* a failure occurred by storing data in the `Left` variant \[[19:27](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=1167)\].
- **Result:** It replaces the need for throwing exceptions, providing an explicit, safe path for errors through the application's domain logic \[[21:56](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=1316)\].

#### RemoteData: State Management without Inconsistency

- **Concept:** A four-state sum type representing the lifecycle of an API request: `Initial`, `Pending`, `Failure`, and `Success` \[[23:53](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=1433)\].
- **Logic:** Traditional state management uses separate boolean flags (e.g., `isLoading`, `hasError`). This leads to "impossible states" (e.g., `isLoading` and `hasError` both being true).
- **Result:**`RemoteData` makes inconsistent states unrepresentable by construction. The UI is forced to handle all four logical states via a single `fold` operation \[[26:33](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=1593)\].

---

### 3\. Operational Logic: Map and Fold

- **Map:** Allows for the transformation of the "success" value inside the container without unwrapping it. If the container is in a "failure" or "none" state, the transformation is ignored \[[13:52](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=832)\].
- **Fold:** The terminal operation that extracts the value. It requires the developer to provide functions for every possible variant of the ADT, ensuring total coverage of the logic \[[15:53](http://www.youtube.com/watch?v=8fWK2iYgsz8&t=953)\].

**Source:**[Practical introduction into ADT in Typescript (ENG)](https://www.google.com/search?q=https://youtu.be/8fWK2iYgsz8)

Google Account

Leon Ormes

leonormes@gmail.com

# **Algebraic Data Types: A First Principles Analysis of Type-Safe Architecture**

## **Abstract**

The history of software engineering is, fundamentally, a history of managing complexity. As systems scale in size and logical intricacy, the combinatorial explosion of possible program states creates a landscape where valid, meaningful states are a vanishingly small island in a vast sea of "illegal" or undefined behaviors. Traditional imperative and object-oriented paradigms, while successful in encapsulating behavior, often fail to structurally restrict the state space of data, relying instead on convention and runtime validation to maintain integrity. This report presents a comprehensive technical analysis of Algebraic Data Types (ADTs) as the foundational mathematical framework for addressing this crisis of state. By treating data types not merely as storage containers but as algebraic entities subject to the laws of Sums (Logical OR) and Products (Logical AND), software architects can construct systems where correctness is enforced by the compiler. This document moves from the set-theoretic roots of type algebra through to the low-level memory mechanics of discriminated unions, comparing native implementations in systems languages like Rust against simulated patterns in the C-family ecosystem. It argues that the adoption of ADTs is not a stylistic preference but a structural necessity for robust, verifiable software architecture.

## ---

**1\. Introduction: The Crisis of State and the Role of Types**

In the design of complex software systems, the primary adversary is the unconstrained state. A "state" is any unique configuration of data that a program can hold in memory at a given moment. As developers add fields, flags, and nullable references to data structures, the number of possible states grows exponentially. A class with three boolean flags has $2^3 \= 8$ states. A class with three 32-bit integers has $(2^{32})^3$ states. In many domain models, the vast majority of these theoretically representable states are nonsensical or "illegal" within the business logic.1

For example, a Payment object might contain a SuccessDate and a FailureReason. In a naive product-type model (like a standard C\# or Java class), it is mechanically possible to construct an object where both fields are populated, or neither. This decoupling of data structure from business invariants forces engineers to write "defensive code"—a proliferation of runtime checks, null guards, and validation routines that obscure the core logic and are prone to human error.3

The solution lies in elevating the type system from a mere label checker to a structural enforcer of logic. Algebraic Data Types (ADTs) provide the mathematical primitives—specifically Sum Types and Product Types—to precisely model the cardinality of data. By aligning the "representable" states (those the type system allows) with the "legal" states (those the domain permits), we achieve the architectural ideal of *correctness by construction*.

This report investigates this paradigm from first principles. It begins with the theoretical foundations of Type Algebra, proving how types form a semiring structure isomorphic to the arithmetic of natural numbers. It then descends into the "physics" of data, analyzing how these abstract concepts map to memory layouts, CPU caches, and compiler optimizations. Finally, it surveys the modern linguistic landscape, contrasting the zero-cost abstractions of Rust with the ergonomic trade-offs in Java, C\#, and TypeScript.

## ---

**2\. The Arithmetic of Type Theory**

To understand the power of ADTs, one must first deconstruct the "algebra" that governs them. The term is not metaphorical; types behave like numbers, and the operations we perform on them—combining them into structs or unions—correspond to arithmetic operations on the cardinality of their underlying sets.4

### **2.1 Set Theoretic Foundations and Cardinality**

At a fundamental level, a type $T$ can be viewed as a set of values (inhabitants). The properties of the type are largely determined by its **cardinality** ($|T|$), which is the number of distinct values that can inhabit that type.

#### **2.1.1 The Primitives: Zero and One**

The algebra of types is built upon two identity elements:

* **The Void Type (0):** This is the type with zero inhabitants. In logic, it corresponds to *False*. In set theory, it is the empty set $\\emptyset$.  
  * *Implementation:* In Rust, this is the \! (Never) type; in Haskell, Void. In TypeScript, never.  
  * *Semantics:* A function accepting Void can never be called. A function returning Void can never return (it must loop forever or terminate the program). It represents "impossibility".6  
* **The Unit Type (1):** This is the type with exactly one inhabitant. In logic, it corresponds to *True*. In set theory, a singleton set $\\{ \\emptyset \\}$.  
  * *Implementation:* In Rust and Haskell, this is (). In C-family languages, it is conceptually void (though void is usually a keyword, not a value; System.Void exists in CLR reflection).  
  * *Semantics:* It carries no information other than its existence. It acts as the multiplicative identity ($T \\times 1 \\cong T$).

#### **2.1.2 Product Types (Logical AND / Multiplication)**

A **Product Type** combines two types $A$ and $B$ such that an instance holds *both* an $A$ *and* a $B$.

* **Cardinality:** $|A \\times B| \= |A| \\cdot |B|$.  
* **Mental Model:** The Cartesian Product of sets.  
* **Examples:** Tuples (A, B), Structs, Records, Classes.

Consider a configuration struct with two boolean flags:

Rust

struct Config {  
    is\_active: bool, // 2 states  
    is\_debug: bool   // 2 states  
}

The cardinality is $2 \\times 2 \= 4$.

1. (True, True)  
2. (True, False)  
3. (False, True)  
4. (False, False)

Product types are the default composite structure in almost all programming languages. They allow state to grow multiplicatively. While necessary for grouping related data, indiscriminate use of products leads to state explosion.5

#### **2.1.3 Sum Types (Logical OR / Addition)**

A **Sum Type** represents a choice between type $A$ *or* type $B$. An instance holds *either* an $A$ *or* a $B$, but never both simultaneously.

* **Cardinality:** $|A \+ B| \= |A| \+ |B|$.  
* **Mental Model:** The Disjoint Union of sets.  
* **Examples:** Enums (Rust/Swift), Discriminated Unions (F\#/TypeScript), Sealed Hierarchies (Java/Scala).

Consider a connection status modeled as a Sum Type:

Rust

enum Connection {  
    Disconnected,      // Unit (1 state)  
    Connected(Session) // Session (N states)  
}

The cardinality is $1 \+ |Session|$. If we modeled this as a Product (a class with a nullable Session), the cardinality would be $1 \\times (1 \+ |Session|)$, which is effectively the same for this trivial case, but the structural guarantees differ.

The distinction becomes critical when multiple choices exist. If we have Status which can be Active (boolean sub-state) or Pending (boolean sub-state):

* **As Product:** struct { isActive: bool, isPending: bool } $\\to 2 \\times 2 \= 4$ states.  
* **As Sum:** enum { Active(bool), Pending(bool) } $\\to 2 \+ 2 \= 4$ states.

While the numeric cardinality matches here, the *semantics* differ. In the Product, isActive and isPending can both be true simultaneously. In the Sum, they are mutually exclusive. Architecture is the art of choosing the algebraic operation that matches the domain constraints.

#### **2.1.4 Exponential Types (Functions)**

A function from type $A$ to type $B$, denoted $A \\to B$, is an exponential type $B^A$.

* **Cardinality:** $|A \\to B| \= |B|^{|A|}$.  
* **Reasoning:** For every one of the $|A|$ input values, the function can result in any of the $|B|$ output values.

This exponential growth explains why testing functions is inherently harder than validating data. A function taking a 32-bit integer and returning a boolean has $2^{(2^{32})}$ possible implementations—a number far exceeding the number of atoms in the observable universe. This underscores the importance of encoding logic in *data types* (which are sums and products) rather than *functions* (exponentials) where possible, a practice often summarized as "Defunctionalization".9

### **2.2 Isomorphisms and Refactoring via Algebra**

Two types $A$ and $B$ are **isomorphic** ($A \\cong B$) if there exist total functions $f: A \\to B$ and $g: B \\to A$ such that $f \\circ g \= id$ and $g \\circ f \= id$. Isomorphic types have identical cardinality and structure, meaning data can be losslessly converted between them. This provides a rigorous mathematical basis for code refactoring.6

The algebraic laws of numbers apply to types, governed by isomorphism.

#### **2.2.1 Commutative Law**

* **Sum:** $A \+ B \\cong B \+ A$  
  * The order of variants in an enum does not matter structurally. Result\<T, E\> is isomorphic to Result\<E, T\>.  
* **Product:** $A \\times B \\cong B \\times A$  
  * A tuple (int, bool) contains the same information as (bool, int).

#### **2.2.2 Associative Law**

* **Sum:** $(A \+ B) \+ C \\cong A \+ (B \+ C)$  
  * A nested Result\<Result\<A, B\>, C\> is isomorphic to a flat enum with three variants A | B | C.  
* **Product:** $(A \\times B) \\times C \\cong A \\times (B \\times C)$  
  * Grouping of fields in structs does not change the information content.

#### **2.2.3 Distributive Law**

$$A \\times (B \+ C) \\cong (A \\times B) \+ (A \\times C)$$  
This is arguably the most architecturally significant law. It relates "Factored" representations to "Expanded" representations.

**Scenario:** Modeling a User who has a mandatory ID and a contact method (either Email or Phone).

LHS (Factored \- Product of Sum):

$$ID \\times (Email \+ Phone)$$

Rust

struct User {  
    id: Uuid,  
    contact: ContactMethod // enum { Email(String), Phone(u64) }  
}

RHS (Expanded \- Sum of Products):

$$(ID \\times Email) \+ (ID \\times Phone)$$

Rust

enum User {  
    EmailUser { id: Uuid, email: String },  
    PhoneUser { id: Uuid, phone: u64 }  
}

These two models are mathematically equivalent (isomorphic).

* **Use LHS** when the application logic frequently accesses id regardless of the contact method (e.g., routing, logging). Access is $O(1)$ without pattern matching.  
* **Use RHS** when the lifecycle or behavior of Email users is entirely distinct from Phone users.

Recognizing this isomorphism prevents "modeling paralysis." Architects can switch between these forms based on access patterns, knowing that no information is lost or created.7

#### **2.2.4 Identity Laws**

* **Sum Identity:** $A \+ 0 \\cong A$.  
  * Adding a Void variant to an enum adds no new states. Either\<T, Void\> is isomorphic to T.  
* **Product Identity:** $A \\times 1 \\cong A$.  
  * A struct struct Wrapper { value: T, meta: () } is isomorphic to T.

#### **2.2.5 Annihilation Law**

* **Product Annihilation:** $A \\times 0 \\cong 0$.  
  * A struct containing a field of type Void (or \!) can never be instantiated. The entire struct becomes uninhabitable. This is useful for "phantom types" or conditionally compiling out features.6

## ---

**3\. Structural Mechanics: The Physics of Data**

While type algebra is abstract, software runs on physical hardware. The implementation of ADTs requires mapping these algebraic structures to bytes in memory. The efficiency of this mapping determines the viability of ADTs in high-performance systems.

### **3.1 The Anatomy of a Sum Type**

To implement a Sum Type $A \+ B$, the runtime must theoretically store two pieces of information:

1. **Discriminant (Tag):** A value indicating whether the memory holds an $A$ or a $B$.  
2. **Payload:** The actual data for $A$ or $B$.

#### **3.1.1 Rust: The Systems Approach**

In Rust, an enum is laid out as a C-style tagged union, but with strict safety guarantees.12

Memory Layout Formula:

$$Size \= SizeOfTag \+ Padding \+ \\max(Size(A), Size(B))$$  
**Example: Detailed Byte Analysis**

Rust

enum Event {  
    Quit,                       // Variant 0 (Unit)  
    KeyPress(u8),               // Variant 1 (u8)  
    Click { x: i64, y: i64 }    // Variant 2 (Two i64s)  
}

1. **Payload Calculation:**  
   * Quit: 0 bytes.  
   * KeyPress: 1 byte.  
   * Click: 16 bytes ($8 \\times 2$).  
   * *Union Size:* Must be 16 bytes (to hold the largest variant, Click).  
2. **Tag:** Typically 1 byte (u8).  
3. **Alignment:** Click contains i64, which requires 8-byte alignment on 64-bit systems.  
4. **Layout:**  
   * \`\`  
   * \[Padding: 7 bytes\] (Required to align the payload to 8 bytes)  
   * \[Payload: 16 bytes\]  
   * **Total Size:** 24 bytes.

This predictable layout allows Rust enums to be stored on the stack, in arrays, and in CPU caches with high efficiency. There is no indirection and no heap allocation unless explicitly requested (e.g., via Box).

#### **3.1.2 Niche Optimization (The "Null Pointer" Trick)**

One of the most profound optimizations in Rust is **Niche Filling**. The compiler analyzes the bit patterns of the types in the variants. If a type has "invalid" bit patterns (niches), the compiler can use those patterns to store the Discriminant, eliminating the need for a separate Tag byte.12

**The Case of Option\<Box\<T\>\>:**

* Algebraically: $1 \+ \\text{Address}$.  
* Box\<T\> is a pointer. Valid pointers are never 0x0 (null).  
* **Optimization:** Rust uses the 0x0 bit pattern to represent the None variant.  
  * None $\\to$ 0x0000...  
  * Some(ptr) $\\to$ ptr (which is non-zero).  
* **Result:** Option\<Box\<T\>\> has the *exact same size* (8 bytes) as Box\<T\>.  
* **Impact:** This makes safety "zero-cost." Architects can use Option references everywhere without incurring the memory penalty of a boolean flag or a wrapper object.

This optimization extends to other types. bool only uses bits 0 and 1\. Option\<bool\> fits in 1 byte (0=None, 1=Some(False), 2=Some(True)). NonZeroU32 is a wrapper that forbids 0, making Option\<NonZeroU32\> the same size as u32.

### **3.2 The Simulated ADT: Class Hierarchies**

In managed languages like Java and C\# (prior to recent updates), Sum Types are simulated using class hierarchies.

**The Simulation:**

Java

interface Event {}  
class Quit implements Event {}  
class Click implements Event { long x; long y; }

Memory Analysis:  
This simulation is physically a "Product of References." A variable Event e is a reference (pointer) to a heap object.

1. **Indirection:** Accessing the data requires a pointer dereference.  
2. **Heap Overhead:** Every instance of Click has an object header. In the JVM/CLR, this includes:  
   * Mark Word / Sync Block (8 bytes).  
   * Class Pointer / Method Table (8 bytes).  
3. **Layout:**  
   * Event e: 8 bytes (Stack reference).  
   * Click Instance (Heap): 16 bytes (Header) \+ 16 bytes (Data) \= 32 bytes.  
4. **Locality:** An array Event is an array of pointers. The actual Click objects are scattered across the heap, causing CPU cache misses during iteration.

**Comparison Table: Array of 1000 Events**

| Metric | Rust Enum (Vec\<Event\>) | Java/C\# Interface (Event) |
| :---- | :---- | :---- |
| **Total Memory** | \~24 KB | \~8 KB (Array) \+ \~32-40 KB (Objects) \= \~40-48 KB |
| **Allocations** | 1 (Contiguous) | 1001 (Array \+ 1000 Objects) |
| **Indirection** | 0 | 1000 Pointer Chases |
| **Cache Efficiency** | High | Low (Pointer Chasing) |

This structural difference explains why systems languages prioritize native Sum Types for performance-critical data.15

### **3.3 The Expression Problem and Dispatch Mechanics**

The choice between ADTs and Class Hierarchies is the physical manifestation of the **Expression Problem**, a fundamental dilemma in language design regarding extensibility.17

**The Grid:** Imagine a matrix where **Rows** are Data Variants (e.g., Circle, Square) and **Columns** are Operations (e.g., Area, Draw).

|  | Area | Draw | Serialize |
| :---- | :---- | :---- | :---- |
| **Circle** | pi\*r^2 | drawCircle() | ... |
| **Square** | s^2 | drawSquare() | ... |

#### **3.3.1 The OOP Approach (Virtual Dispatch)**

OOP organizes code by Rows. The Circle class contains area() and draw().

* **Easy:** Adding a new Row (Triangle). Create class Triangle. No existing code changes.  
* **Hard:** Adding a new Column (Serialize). You must modify the Shape interface and *every* subclass (Circle, Square, Triangle). This violates the Open/Closed Principle for operations.

To mitigate this, OOP uses the **Visitor Pattern** to simulate ADTs.19

* *Mechanism:* Double Dispatch. element.accept(visitor) calls visitor.visit(element).  
* *Trade-off:* It allows adding new operations (Visitors) easily but makes adding new variants (Rows) extremely painful, as every Visitor interface must be updated. It effectively flips the table to match the ADT trade-off, but at the cost of high verbosity and the runtime overhead of two virtual calls per operation.

#### **3.3.2 The Functional Approach (Pattern Matching)**

FP organizes code by Columns. The area function contains a match statement handling Circle and Square.

* **Easy:** Adding a new Column (Serialize). Write a new function serialize(shape: Shape). No existing code changes.  
* **Hard:** Adding a new Row (Triangle). You must update *every* function (area, draw, serialize) to handle the new Triangle case.

Exhaustiveness Checking:  
The key feature of native ADTs is Exhaustiveness. The compiler maintains a checklist of variants. If you add Triangle to the Enum but forget to update the area function, the compiler throws an error. This safety guarantee is absent in standard OOP interfaces (unless Sealed Types are used).21

## ---

**4\. Architectural Application: Correctness by Construction**

The theoretical and structural properties of ADTs enable a powerful design philosophy: **Make Illegal States Unrepresentable**. This mantra, popularized by Yaron Minsky, advocates encoding business constraints directly into the type definitions.1

### **4.1 Domain Modeling Case Study: The Payment State Machine**

Consider a payment processing system. A payment can be pending, authorized, or settled.

**The Anti-Pattern (Product Types / Flags):**

Java

public class Payment {  
    public decimal Amount;  
    public boolean IsAuthorized;  
    public boolean IsSettled;  
    public string AuthCode; // Only valid if IsAuthorized  
    public DateTime SettleDate; // Only valid if IsSettled  
}

**Illegal States:**

1. IsAuthorized \= false but AuthCode is populated.  
2. IsSettled \= true but IsAuthorized \= false (assuming logic requires auth first).  
3. IsSettled \= true but SettleDate is null.

In this model, the validity of the object is defined by values, not structure. Every function consuming Payment must perform "defensive coding":

Java

if (p.IsSettled && p.SettleDate \== null) throw new InvalidStateException();

The ADT Solution (Sum Types):  
We model the state as a Sum Type, representing the lifecycle.

Rust

enum Payment {  
    Pending { amount: Decimal },  
    Authorized { amount: Decimal, auth\_code: String },  
    Settled { amount: Decimal, auth\_code: String, settled\_at: DateTime }  
}

**Analysis:**

* It is structurally impossible to access auth\_code if the payment is Pending. The field simply does not exist in that variant.  
* It is impossible to be Settled without a settled\_at date.  
* The type system acts as the State Machine. Transitions are functions returning the next state:  
  Rust  
  fn authorize(p: Payment::Pending) \-\> Payment::Authorized

  This function cannot even be called with a Settled payment, preventing invalid state transitions at compile time.3

### **4.2 Recursive Architectures and The Calculus of Trees**

Recursive ADTs are the natural representation for hierarchical data, such as Abstract Syntax Trees (ASTs), JSON, or HTML.

Definition:

$$Tree(A) \= Leaf(A) \+ Node(Tree(A) \\times Tree(A))$$  
This equation $T \= A \+ T^2$ mathematically describes a binary tree. The "algebra" allows us to reason about the shape.

#### **4.2.1 Recursion Schemes**

When working with recursive ADTs, a common architectural pattern is to separate the *structure* of the recursion from the *business logic* of the traversal. This is achieved using **Recursion Schemes**, specifically Catamorphisms (folds).22

* **The Base Functor:** We define the shape of one layer of the tree, replacing recursive points with a generic parameter r.  
  Rust  
  enum ExprF\<R\> {  
      Val(i32),  
      Add(R, R),  
      Mul(R, R)  
  }

* **The Fix Point:** We wrap this in a Fix type to tie the knot. type Expr \= Fix\<ExprF\>.  
* **The Algebra:** We define a simple function ExprF\<i32\> \-\> i32 that knows how to reduce *one single layer*.  
  * Val(x) \-\> x  
  * Add(x, y) \-\> x \+ y  
* **The Catamorphism:** A generic cata function applies this algebra bottom-up.

This pattern allows architects to write complex tree transformations (evaluation, optimization, pretty-printing) without ever writing explicit recursion code, eliminating StackOverflow risks and boilerplate.

#### **4.2.2 Zippers: The Derivative of a Type**

What if we need to modify a node deep inside an immutable tree? Rebuilding the entire path is expensive. The **Zipper** is a data structure derived from the calculus of types that represents a "cursor" or "focus".24

Mathematically, the type of a one-hole context for a type $T$ is the derivative $\\frac{\\partial T}{\\partial X}$.  
For a List of elements $X$:

$$L(X) \= 1 \+ X \\cdot L(X)$$Differentiating with respect to $X$:$$\\frac{dL}{dX} \= 0 \+ (1 \\cdot L \+ X \\cdot L') \\implies L'(1 \- X) \= L \\implies L' \= L^2$$

(Using the geometric series identity $L \= 1/(1-X)$).  
The result $L^2$ (or $L \\times L$) tells us that a List Zipper consists of **two lists**:

1. The items before the focus (typically reversed).  
2. The items after the focus.

This mathematical derivation is not just trivia; it provides the exact data structure needed for $O(1)$ navigation in functional architecture.26

## ---

**5\. The Landscape of Implementation**

The theoretical benefits of ADTs are universal, but their adoption varies widely across the programming language landscape.

### **5.1 The Systems Frontier: Rust and Haskell**

**Haskell** is the gold standard for ADTs. Its syntax is terse (data Bool \= True | False), and its runtime (the STG machine) is optimized for graph reduction. However, its lazy evaluation model introduces unpredictability in memory usage (thunks), making it challenging for embedded or real-time systems.27

**Rust** brings ADTs to systems programming. It offers the same expressive power (enum) but with strict evaluation and control over memory layout.

* *Strengths:* Zero-cost abstractions, Niche optimization, explicit memory control.  
* *Weaknesses:* Recursive types are not implicit. Because types must have a known size at compile time, recursive variants must be explicitly wrapped in Box\<T\> or Rc\<T\> to introduce pointer indirection.29

### **5.2 The Managed Simulation: C\# and Java**

Java (Modern):  
Java 21 represents a massive leap forward with Sealed Classes and Pattern Matching for switch.31

* *Sealed Interfaces:* Act as the Sum Type definition. sealed interface Shape permits Circle, Square.  
* *Records:* Act as the Product Type definition. record Circle(double r) implements Shape.  
* *Switch:* Acts as the Match expression. The compiler enforces exhaustiveness for sealed hierarchies.  
* *Trade-off:* It is still physically a class hierarchy (pointers and headers). It lacks the "zero-cost" memory layout of Rust enums but provides the logical safety.32

C\# (Current State):  
C\# is in a transition. While record types provide excellent Product types, Sum types are still second-class.

* *Simulation:* Developers often use libraries like OneOf.33 This library provides a struct-based union OneOf\<T0, T1,...\> with a Match method.  
* *Performance Cost:* While OneOf avoids heap allocation for the union itself, it often incurs boxing costs when accessing values or passing them to generic delegates. Benchmarks show OneOf can be 4-6x slower than native structures due to this overhead.34  
* *Future:* Proposals for "Closed Enums" or "Type Unions" are active, aiming to bring Rust-like memory layout optimizations to the CLR.35

### **5.3 Structural Typing: TypeScript**

TypeScript uses **Discriminated Unions** built on top of JavaScript objects.

TypeScript

type Shape \= 

| { kind: "circle", radius: number }  
| { kind: "square", side: number };

* *Mechanism:* The kind literal string serves as the runtime tag. TypeScript's Control Flow Analysis narrows the type within if or switch blocks.36  
* *Exhaustiveness:* Unlike Rust/Java, TypeScript does not error by default on missing cases. Developers use the assertNever pattern to force a compile-time error:  
  TypeScript  
  function assertNever(x: never): never { throw new Error("Unexpected: " \+ x); }  
  // inside switch default:  
  assertNever(shape);

  If shape has not been narrowed to never (meaning a case was missed), this line fails to compile.37

**Comparison Matrix**

| Feature | Rust | Haskell | Java 21+ | TypeScript | C\# (Current) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Sum Type** | enum | data | sealed interface | Union \` | \` |
| **Memory** | Flat (Tag \+ Union) | Pointer to Thunk | Heap Objects | JS Objects | Heap / Struct |
| **Null Safety** | Option (Niche opt) | Maybe | Optional (Boxed) | null/undefined | Nullable\<T\> |
| **Exhaustiveness** | **Strict** (Error) | **Strict** (Error) | **Strict** (Error) | never check (Manual) | Warning / Library |
| **Pattern Matching** | Native match | Native case | switch pattern | Control flow | switch expr |

## ---

**6\. Conclusion**

Algebraic Data Types represent a convergence of mathematical rigor and software engineering pragmatism. They are not merely a feature of functional languages but a fundamental discovery in the science of data modeling. By treating types as algebraic variables that can be summed and multiplied, architects can design systems that are **correct by construction**.

The shift from class-based hierarchies (Open/Product-heavy) to ADTs (Closed/Sum-heavy) addresses the fundamental asymmetry of the Expression Problem, favoring fixed data shapes with extensible operations—a model often better suited to the predictable business rules of modern applications than the open polymorphism of traditional OOP.

While languages like Rust and Haskell offer the purest implementations with significant performance benefits (memory layout optimizations), the principles are portable. Through features like Java's Sealed Classes, TypeScript's Discriminated Unions, and C\#'s pattern matching, the industry is collectively moving toward a future where the compiler bears the burden of verifying architectural integrity.

**Key Takeaway:** In a robust architecture, the type system is the first line of defense. By making illegal states unrepresentable, we effectively turn unit tests for validity into compile-time proofs of correctness, freeing engineers to focus on the domain logic that matters. The future of robust software is, undeniably, algebraic.

### **Citations**

4 \- Theoretical definitions of Sum and Product types.  
9 \- History of ADTs, Cardinality, and Exponentials.  
6 \- Algebraic Laws and Isomorphisms.  
12 \- Rust Memory Layout and Niche Optimization.  
15 \- Comparison of C\# vs Rust performance.  
17 \- The Expression Problem and Visitor Pattern.  
1 \- Make Illegal States Unrepresentable (DDD).  
22 \- Zippers, Derivatives, and Recursion Schemes.  
31 \- Java 21 Sealed Classes and Pattern Matching.  
36 \- TypeScript Discriminated Unions and Exhaustiveness.  
33 \- C\# OneOf library and trade-offs.  
49 \- Boolean Algebra and Set Theory connections.

#### **Works cited**

1. Make Illegal States Unrepresentable \- Functional Software Architecture, accessed on December 29, 2025, [https://functional-architecture.org/make\_illegal\_states\_unrepresentable/](https://functional-architecture.org/make_illegal_states_unrepresentable/)  
2. Make Invalid States Unrepresentable \- DevIQ, accessed on December 29, 2025, [https://deviq.com/principles/make-invalid-states-unrepresentable](https://deviq.com/principles/make-invalid-states-unrepresentable)  
3. Make invalid states unrepresentable \- GeekLaunch, accessed on December 29, 2025, [https://geeklaunch.io/blog/make-invalid-states-unrepresentable/](https://geeklaunch.io/blog/make-invalid-states-unrepresentable/)  
4. Algebraic data type \- Wikipedia, accessed on December 29, 2025, [https://en.wikipedia.org/wiki/Algebraic\_data\_type](https://en.wikipedia.org/wiki/Algebraic_data_type)  
5. Functional design: Algebraic Data Types \- DEV Community, accessed on December 29, 2025, [https://dev.to/gcanti/functional-design-algebraic-data-types-36kf](https://dev.to/gcanti/functional-design-algebraic-data-types-36kf)  
6. Simple Algebraic Data Types | Bartosz Milewski's Programming Cafe, accessed on December 29, 2025, [https://bartoszmilewski.com/2015/01/13/simple-algebraic-data-types/](https://bartoszmilewski.com/2015/01/13/simple-algebraic-data-types/)  
7. Notas :: 6\. Simple Algebraic Data Types, accessed on December 29, 2025, [https://notas.autophagy.io/en/latest/CTFP/part1/ch6.html](https://notas.autophagy.io/en/latest/CTFP/part1/ch6.html)  
8. The Cardinal Rules of Rust \- Understanding Type Cardinality for ..., accessed on December 29, 2025, [https://leptonic.solutions/blog/algebraic-data-types-in-rust/](https://leptonic.solutions/blog/algebraic-data-types-in-rust/)  
9. What does it mean to have an "algebraic" type system? : r/ProgrammingLanguages \- Reddit, accessed on December 29, 2025, [https://www.reddit.com/r/ProgrammingLanguages/comments/10ewz92/what\_does\_it\_mean\_to\_have\_an\_algebraic\_type\_system/](https://www.reddit.com/r/ProgrammingLanguages/comments/10ewz92/what_does_it_mean_to_have_an_algebraic_type_system/)  
10. Type Isomorphism \- Kwang's Haskell Blog, accessed on December 29, 2025, [https://kseo.github.io/posts/2016-12-25-type-isomorphism.html](https://kseo.github.io/posts/2016-12-25-type-isomorphism.html)  
11. Commutative, Associative and Distributive Laws \- Math is Fun, accessed on December 29, 2025, [https://www.mathsisfun.com/associative-commutative-distributive.html](https://www.mathsisfun.com/associative-commutative-distributive.html)  
12. What is the null pointer optimization in Rust? \- Stack Overflow, accessed on December 29, 2025, [https://stackoverflow.com/questions/46557608/what-is-the-null-pointer-optimization-in-rust](https://stackoverflow.com/questions/46557608/what-is-the-null-pointer-optimization-in-rust)  
13. Unveiling Rust's Memory Layout and the Double-Edged Sword of Unsafe | Leapcell, accessed on December 29, 2025, [https://leapcell.io/blog/unveiling-rust-s-memory-layout-and-the-double-edged-sword-of-unsafe](https://leapcell.io/blog/unveiling-rust-s-memory-layout-and-the-double-edged-sword-of-unsafe)  
14. Rust's Smartest Enum: How NPO Makes Option  
15. Does Rust have an advantage if memory-safety is not an advantage? \- Sander Saares, accessed on December 29, 2025, [https://sander.saares.eu/2024/02/02/does-rust-have-an-advantage-if-memory-safety-is-not-an-advantage/](https://sander.saares.eu/2024/02/02/does-rust-have-an-advantage-if-memory-safety-is-not-an-advantage/)  
16. Why is this Rust code slower than C\#? \- Page 2 \- help \- The Rust Programming Language Forum, accessed on December 29, 2025, [https://users.rust-lang.org/t/why-is-this-rust-code-slower-than-c/49564?page=2](https://users.rust-lang.org/t/why-is-this-rust-code-slower-than-c/49564?page=2)  
17. Sum Types, Visitors, and the Expression Problem, accessed on December 29, 2025, [https://koerbitz.me/posts/Sum-Types-Visitors-and-the-Expression-Problem.html](https://koerbitz.me/posts/Sum-Types-Visitors-and-the-Expression-Problem.html)  
18. The Visitor Pattern and Pattern Matching : r/programming \- Reddit, accessed on December 29, 2025, [https://www.reddit.com/r/programming/comments/1nma2a/the\_visitor\_pattern\_and\_pattern\_matching/](https://www.reddit.com/r/programming/comments/1nma2a/the_visitor_pattern_and_pattern_matching/)  
19. Visitor pattern \- Wikipedia, accessed on December 29, 2025, [https://en.wikipedia.org/wiki/Visitor\_pattern](https://en.wikipedia.org/wiki/Visitor_pattern)  
20. Pattern matching in Java with the Visitor pattern — Engineering Blog \- Wealthfront, accessed on December 29, 2025, [https://eng.wealthfront.com/2015/02/11/pattern-matching-in-java-with-visitor/](https://eng.wealthfront.com/2015/02/11/pattern-matching-in-java-with-visitor/)  
21. F\# discriminated unions versus C\# class hierarchies \- Stack Overflow, accessed on December 29, 2025, [https://stackoverflow.com/questions/7334019/f-discriminated-unions-versus-c-sharp-class-hierarchies](https://stackoverflow.com/questions/7334019/f-discriminated-unions-versus-c-sharp-class-hierarchies)  
22. ASTs with Fix and Free \- Chris Penner, accessed on December 29, 2025, [https://chrispenner.ca/posts/asts-with-fix-and-free](https://chrispenner.ca/posts/asts-with-fix-and-free)  
23. Practical recursion schemes in Rust: traversing and extending trees \- Tweag, accessed on December 29, 2025, [https://tweag.io/blog/2025-04-10-rust-recursion-schemes/](https://tweag.io/blog/2025-04-10-rust-recursion-schemes/)  
24. Zipper (data structure) \- Wikipedia, accessed on December 29, 2025, [https://en.wikipedia.org/wiki/Zipper\_(data\_structure)](https://en.wikipedia.org/wiki/Zipper_\(data_structure\))  
25. Generic Zipper: the context of a traversal \- This FTP site, accessed on December 29, 2025, [https://okmij.org/ftp/continuations/zipper.html](https://okmij.org/ftp/continuations/zipper.html)  
26. Zippers, Part 2: Zippers as Derivatives \- Pavel Panchekha, accessed on December 29, 2025, [https://pavpanchekha.com/blog/zippers/derivative.html](https://pavpanchekha.com/blog/zippers/derivative.html)  
27. Haskell's algebraic data types \- Stack Overflow, accessed on December 29, 2025, [https://stackoverflow.com/questions/16770/haskells-algebraic-data-types](https://stackoverflow.com/questions/16770/haskells-algebraic-data-types)  
28. What is the difference between an Algebraic Data Type and an Abstract Data Type? \- Reddit, accessed on December 29, 2025, [https://www.reddit.com/r/haskell/comments/38grqx/what\_is\_the\_difference\_between\_an\_algebraic\_data/](https://www.reddit.com/r/haskell/comments/38grqx/what_is_the_difference_between_an_algebraic_data/)  
29. Recursive types \- confused on book paragraph \- Rust Users Forum, accessed on December 29, 2025, [https://users.rust-lang.org/t/recursive-types-confused-on-book-paragraph/131713](https://users.rust-lang.org/t/recursive-types-confused-on-book-paragraph/131713)  
30. Using Box  
31. JEP 441: Pattern Matching for switch \- OpenJDK, accessed on December 29, 2025, [https://openjdk.org/jeps/441](https://openjdk.org/jeps/441)  
32. Java 21: Pattern Matching for switch- The Future of Control Flow in Java \- Medium, accessed on December 29, 2025, [https://medium.com/@ucgorai/java-21-pattern-matching-for-switch-the-future-of-control-flow-in-java-8971c80c9d9b](https://medium.com/@ucgorai/java-21-pattern-matching-for-switch-the-future-of-control-flow-in-java-8971c80c9d9b)  
33. OneOf Library in C\# \- DEV Community, accessed on December 29, 2025, [https://dev.to/takatws/oneof-library-in-c-19af](https://dev.to/takatws/oneof-library-in-c-19af)  
34. OneOf (with benchmarks) \- Thoughts and stuff, accessed on December 29, 2025, [https://www.eke.li/2023/04/oneof-with-benchmarks/](https://www.eke.li/2023/04/oneof-with-benchmarks/)  
35. Pattern Matching with Discriminated Unions in .NET \- Thinktecture AG, accessed on December 29, 2025, [https://www.thinktecture.com/net/pattern-matching-with-discriminated-unions-in-net/](https://www.thinktecture.com/net/pattern-matching-with-discriminated-unions-in-net/)  
36. Discriminated Union | TypeScript Guide by Convex, accessed on December 29, 2025, [https://www.convex.dev/typescript/advanced/type-operators-manipulation/typescript-discriminated-union](https://www.convex.dev/typescript/advanced/type-operators-manipulation/typescript-discriminated-union)  
37. aikoven/assert-never: Helper function for exhaustive checks of discriminated unions in TypeScript \- GitHub, accessed on December 29, 2025, [https://github.com/aikoven/assert-never](https://github.com/aikoven/assert-never)  
38. TypeScript's AssertNever: The Guardian Angel of Exhaustive Coding | by Saif eddine hasnaoui | SoftwareCraft Mastery | Medium, accessed on December 29, 2025, [https://medium.com/softwarecraft-mastery/typescripts-assertnever-the-guardian-angel-of-exhaustive-coding-bd4136038820](https://medium.com/softwarecraft-mastery/typescripts-assertnever-the-guardian-angel-of-exhaustive-coding-bd4136038820)  
39. A Very Early History of Algebraic Data Types \- Hillel Wayne, accessed on December 29, 2025, [https://www.hillelwayne.com/post/algdt-history/](https://www.hillelwayne.com/post/algdt-history/)  
40. K-12 – Commutative, Associative, Distributive, Identity and Inverse Laws, accessed on December 29, 2025, [https://mathematicalmysteries.org/k-12-commutative-associative-distributive-identity-and-inverse-laws/](https://mathematicalmysteries.org/k-12-commutative-associative-distributive-identity-and-inverse-laws/)  
41. Properties of Equality: Applying the Commutative, Associative, and Distributive \- Math Learning | Think Academy US, accessed on December 29, 2025, [https://www.thethinkacademy.com/blog/properties-of-equality-applying-the-commutative-associative-and-distributive/](https://www.thethinkacademy.com/blog/properties-of-equality-applying-the-commutative-associative-and-distributive/)  
42. Enums: Rust Objects of Unusual Size \- Angus Morrison, accessed on December 29, 2025, [https://www.angus-morrison.com/blog/enums-rust-objects-unusual-size](https://www.angus-morrison.com/blog/enums-rust-objects-unusual-size)  
43. The Visitor Pattern \- 'Revisited' using Data Oriented Programming techniques. : r/java \- Reddit, accessed on December 29, 2025, [https://www.reddit.com/r/java/comments/1k6lwpu/the\_visitor\_pattern\_revisited\_using\_data\_oriented/](https://www.reddit.com/r/java/comments/1k6lwpu/the_visitor_pattern_revisited_using_data_oriented/)  
44. Making illegal states unrepresentable \- Swiftology, accessed on December 29, 2025, [https://swiftology.io/articles/making-illegal-states-unrepresentable/](https://swiftology.io/articles/making-illegal-states-unrepresentable/)  
45. Easy domain modelling with types, accessed on December 29, 2025, [https://blog.ploeh.dk/2016/11/28/easy-domain-modelling-with-types/](https://blog.ploeh.dk/2016/11/28/easy-domain-modelling-with-types/)  
46. Make Illegal States Unrepresentable\! \- Domain-Driven Design w/ TypeScript, accessed on December 29, 2025, [https://khalilstemmler.com/articles/typescript-domain-driven-design/make-illegal-states-unrepresentable/](https://khalilstemmler.com/articles/typescript-domain-driven-design/make-illegal-states-unrepresentable/)  
47. Java sealed type with pattern switches VS pattern Visitor \- Stack Overflow, accessed on December 29, 2025, [https://stackoverflow.com/questions/70610012/java-sealed-type-with-pattern-switches-vs-pattern-visitor](https://stackoverflow.com/questions/70610012/java-sealed-type-with-pattern-switches-vs-pattern-visitor)  
48. Union Types for Domain Modelling: Disadvantages of using OneOf\<\>? : r/dotnet \- Reddit, accessed on December 29, 2025, [https://www.reddit.com/r/dotnet/comments/1j2btnz/union\_types\_for\_domain\_modelling\_disadvantages\_of/](https://www.reddit.com/r/dotnet/comments/1j2btnz/union_types_for_domain_modelling_disadvantages_of/)  
49. Boolean algebra \- Wikipedia, accessed on December 29, 2025, [https://en.wikipedia.org/wiki/Boolean\_algebra](https://en.wikipedia.org/wiki/Boolean_algebra)  
50. The number of countable isomorphism types of complete extensions of the theory of Boolean algebras \- SciSpace, accessed on December 29, 2025, [https://scispace.com/pdf/the-number-of-countable-isomorphism-types-of-complete-4tl66wfhoe.pdf](https://scispace.com/pdf/the-number-of-countable-isomorphism-types-of-complete-4tl66wfhoe.pdf)