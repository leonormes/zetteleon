---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/c23a4a54334f"
author:
  - "[[Gemini]]"
published:
created: 2025-12-29
description: "Created with Gemini"
tags:
  - "clippings"
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