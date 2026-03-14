---
created: 2026-03-14T09:49:47+00:00
modified: 2026-03-14T11:09:41+00:00
tags: [articles]
title: Type-Level Programming in Scala 3 A Comprehensive Tutorial
---

## Type-Level Programming in Scala 3: A Comprehensive Tutorial

![rw-book-cover](https://substackcdn.com/image/fetch/$s_!INT6!,w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b47ec17-bef3-4aed-95b5-9db998ca6d7b_6000x3851.jpeg)

### Metadata

- Author: [[The Unshielded Mind]]
- Full Title: Type-Level Programming in Scala 3: A Comprehensive Tutorial
- Category: articles
- Summary: Type-level programming runs computations at compile time by encoding values and logic as types. Scala 3 adds match types and given/using to make these encodings clearer and let the compiler act like a proof searcher. The tutorial shows how classic Scala 2 techniques evolve into cleaner, more powerful Scala 3 abstractions.
- URL: <https://drmark.substack.com/p/type-level-programming-in-scala-3>

### Full Document

#### Inception: Writing Programs Inside Your Types Inside Your Programs

Type-level programming allows us to perform computations at compile time using the type system. While the classic Scala 2 resources like [Apocalisp’s blog](https://apocalisp.wordpress.com/) posts pioneered these techniques using implicits and type projections, Scala 3 brings powerful new features that make type-level programming more accessible and expressive.

This tutorial bridges the gap between the foundational concepts from those classic resources and modern Scala 3 features, showing how the same ideas have evolved into cleaner, more powerful abstractions.

[![](https://substackcdn.com/image/fetch/$s_!bqUy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf5ef6a5-e41f-4cb4-a0b8-64b1a797c370_8192x4096.jpeg)](https://substackcdn.com/image/fetch/$s_!bqUy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf5ef6a5-e41f-4cb4-a0b8-64b1a797c370_8192x4096.jpeg)

### Foundations: Types as Values

The core insight of type-level programming is that we can encode values as types and computations as type relationships. This concept, explored extensively in the classic blog posts, remains fundamental in Scala 3. Let's start with the classic Peano encoding of natural numbers at the type level. We represent numbers as nested type constructors where Zero is 0, and each application of Succ adds 1.

```
`// Type-level natural numbers
sealed trait Nat
class Zero extends Nat
class Succ[N <: Nat] extends Nat

// Type aliases for convenience
type _0 = Zero
type _1 = Succ[_0]
type _2 = Succ[_1]
type _3 = Succ[_2]
type _4 = Succ[_3]
type _5 = Succ[_4]`
```

Similarly, we can encode booleans at the type level.

```
`sealed trait Bool
sealed trait True extends Bool
sealed trait False extends Bool`
```

These encodings form the foundation for more complex type-level computations. By representing basic values as types, we can build entire computational systems that execute during compilation.

### Match Types: Pattern Matching at Type Level

Scala 3's match types replace the complex implicit resolution techniques used in Scala 2 for type-level computation. They provide a direct, readable way to express type-level pattern matching. The basic match type syntax resembles regular pattern matching but operates on types rather than values.

```
`type Elem[X] = X match
 case String => Char
 case Array[t] => t
 case Iterable[t] => t
 case Any => X`
```

This match type reduces to Char when X is String, to the element type when X is an Array or Iterable, and to X itself for any other type. The compiler performs this reduction at compile time, giving us type-level computation. Match types can be recursive, enabling complex computations. Consider type-level addition using match types.

```
`type Plus[A <: Nat, B <: Nat] <: Nat = A match
 case Zero => B
 case Succ[a] => Succ[Plus[a, B]]`
```

This is much cleaner than the Scala 2 approach, which required complex implicit resolution chains. The match type clearly expresses the recursive structure of addition, where adding zero to B gives B, and adding a successor to B gives the successor of adding the predecessor to B. We can implement boolean operations with similar clarity.

```
`type Not[B <: Bool] <: Bool = B match
 case True => False
 case False => True

type And[A <: Bool, B <: Bool] <: Bool = A match
 case True => B
 case False => False

type Or[A <: Bool, B <: Bool] <: Bool = A match
 case True => True
 case False => B`
```

### Given/Using: Compiler as Proof Search Engine

Before diving into type classes, it's crucial to understand how Scala 3's given/using mechanism works as a proof search system. This concept, fundamental to type-level programming, treats the compiler as a theorem prover that searches for evidence of type relationships.

[![](https://substackcdn.com/image/fetch/$s_!U02N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddc09a7f-e991-4d9c-bb4b-d696db2e1694_6000x3851.jpeg)](https://substackcdn.com/image/fetch/$s_!U02N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddc09a7f-e991-4d9c-bb4b-d696db2e1694_6000x3851.jpeg)

At its core, the given/using system embodies the Curry-Howard correspondence. Types are propositions that can be true or false, values are proofs that provide evidence for these propositions, and the compiler searches for these proofs automatically. Consider a simple example that demonstrates this principle.

```
`// A proposition: “Type A can be shown as a string”
trait CanShow[A]

// A proof: “Int can be shown as a string”
given CanShow[Int] with {}

// Compiler as proof searcher: “Find me a proof that Int can be shown”
val proof = summon[CanShow[Int]] // Compiler finds the proof`
```

The given keyword declares evidence that certain type relationships hold. The using keyword and its variants ask the compiler to search for such evidence. This creates a powerful system where the compiler acts as an automated theorem prover.
