---
title: "You said I am not a mathematician but love the rig..."
source: "https://gemini.google.com/app/38b685e0d75ab205"
captured: "2026-04-29T09:16:54+01:00 2026-04-29T09:16:54+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

I am not a mathematician but love the rigour of mathematicai thinking. I want to learn about category theory and develop a practical mental model. How do I start to understand the fundamentals and be able to do something with category theory?

---

**Gemini**

Category theory is often described as the "mathematics of mathematics." While traditional maths often focuses on the internal properties of things (like the properties of a number, a geometric shape, or a set of items), category theory zooms out. It provides a rigorous framework for looking at how different things relate to one another.

For a non-mathematician who appreciates structural, logical thinking, category theory offers a profound mental model: it teaches you to define things not by what they *are* inside, but by how they *interact* with everything else.

Here is a practical way to conceptualise the fundamentals.

### 1\. The Core Mental Model: The Network

Imagine you are looking at a map of a railway system. You do not need to know how the engines work, what the stations look like, or the demographics of the cities. You only care about the stations and the tracks connecting them.

**Objects and Morphisms** A "Category" consists of two main things:

- **Objects:** The "dots" or the stations. In mathematics, these could be sets, spaces, or numbers. In practicality, they could be data types, physical states, or logical propositions.
- **Morphisms (Arrows):** The "arrows" or the train tracks between the stations. These represent processes, transformations, or relationships. If an object is a starting state, a morphism is the action that transforms it into another state.

The fundamental shift in thinking is to stop staring at the objects. In category theory, the arrows—the behaviours and relationships—are the primary citizens.

**Composition** A category must obey a strict rule of composition: if there is an arrow from A to B, and an arrow from B to C, there *must* be a valid, direct arrow from A to C.

Think of this as an unbroken chain of logic. If you have a process to turn flour into dough (A → B), and a process to turn dough into bread (B → C), you inherently have a process to turn flour into bread (A → C). If your system does not allow for this smooth combination of steps, it is not a category.

**Functors** Once you have different categories (different networks), you might want to translate between them. A "Functor" is an arrow between *entire categories*. It maps every object in Category X to an object in Category Y, and every arrow in X to an arrow in Y, whilst perfectly preserving the structure and the composition.

### How to "Do Something" With It

Because category theory is the study of pure structure and compositionality, it is incredibly powerful for modelling complex systems where you need to guarantee that small, rigorous parts will combine safely into a larger whole.

**1\. Functional Programming** This is currently the most accessible and practical arena for applied category theory. Functional programming languages (like Haskell, Scala, or F#) use category theory directly.

- **Types** are the objects.
- **Functions** are the morphisms.
- Concepts like **Functors** and **Monads** (infamous in programming circles) are literal category theory structures used to handle things like missing data, errors, or state changes in a strictly mathematical, predictable way.

**2\. Systems Architecture and Modelling** You can use categorical thinking to design software systems, business workflows, or databases. By strictly defining the "states" of your system as objects, and the "allowable actions" as morphisms, you can mathematically prove whether certain end-states are reachable or if your system has logical dead ends.

### Where to Start

To build a practical, rigorous understanding without getting bogged down in traditional mathematical prerequisites, you can start here:

- **Read "Conceptual Mathematics: A First Introduction to Categories" by F. William Lawvere and Stephen H. Schanuel.** This book was specifically written to teach category theory to people who are not mathematicians. It is highly accessible and focuses heavily on building intuition.
- **Read "Category Theory for Programmers" by Bartosz Milewski.** Even if you only dabble in programming, this resource is fantastic. It grounds the abstract diagrams into concrete logic puzzles and code, making the arrows and objects feel incredibly tangible.
- **Learn a bit of Haskell.** You do not need to become a software developer, but spending a weekend learning the basics of a purely functional language will instantly click the concept of "composition" into place in your mind.
