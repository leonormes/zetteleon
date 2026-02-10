---
captured: "2026-02-10T09:43:19+00:00 2026-02-10T09:43:19+00:00"
created: 2026-02-10T09:43:22+00:00
modified: 2026-02-10T12:47:23+00:00
source: "https://gemini.google.com/share/ca06d57f0edd"
status: "processing"
tags: ["input"]
title: Type Theory An Algebraic Introduction
type: "head"
---

## Raw Output / Content

You said

<https://youtu.be/6hAeJmKXRfo?si=9jcjWnhmxp4F1tBk>

This video from the All Angles channel provides an introduction to type theory and explains how types in computer science can be understood through the lens of algebra.

### What is a Type?

A type is defined mathematically as a set of allowed values combined with a list of functions that can be applied to those values \[[01:12](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=72)\]. Types help programmers manage software development by telling the computer what to expect, how much memory to allocate, and which operations (like addition or subtraction) are valid for a specific variable \[[00:32](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=32)\].

### The Algebra of Types

The video explores how complex types are constructed from simpler ones, noting that the number of possible values in these new types follows algebraic rules:

- Product Types (Cartesian Product): Represented as objects or records, these contain pairs of values from two sets. The total number of values is the product of the sizes of the original types \[[03:05](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=185)\].
- Sum Types (Tagged Union): These represent a value that is either from one type or another. To distinguish between them, a "tag" is used. The size of this type is the sum of the sizes of the original types \[[04:25](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=265)\].
- Exponential Types (Function Types): These consist of all possible functions from one type to another. The number of values is the size of the output type raised to the power of the size of the input type \[[07:15](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=435)\].

### Neutral Elements

Just as in basic arithmetic, certain types act as neutral elements \[[10:44](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=644)\]:

- Empty Type (0): Contains no values and serves as the neutral element for sums () \[[07:44](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=464)\].
- Unit Type (1): Contains a single value and serves as the neutral element for products () \[[08:28](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=508)\].

### Key Concepts and Identities

The video demonstrates how algebraic identities correspond to programming techniques:

- Distributive Law:. This shows that a pair of functions (one for fruits and one for vegetables) is equivalent to a single function that can handle either a fruit or a vegetable \[[10:25](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=625)\].
- Currying:. This identity explains "Currying," a technique where a function taking multiple inputs (a product) is transformed into a series of functions that each take a single input one at a time \[[13:43](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=823)\].

The video concludes by noting that these concepts are foundational for further study in category theory and tensor algebra \[[15:16](http://www.youtube.com/watch?v=6hAeJmKXRfo&t=916)\].
