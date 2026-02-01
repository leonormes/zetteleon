---
created: 2026-01-30T22:17:26+00:00
modified: 2026-02-01T15:09:20+00:00
title: Order Theory
---

In standard programming (Python, Terraform, Jinja2), the word "Order" usually refers to Execution Order (Time). Line 1 happens before Line 2.

In CUE and formal mathematics, "Order" refers to specificity (Information Content). It defines a hierarchy of values from "vague" to "exact."

Here is the breakdown of what Order Theory means in this specific context:

1. The "Order" is Specificity, Not Time
In Order Theory, we arrange values based on how strict they are. This arrangement is often visualized as a vertical line (a Lattice).
 - Bottom (\bot): The most general state. "I know nothing; this could be anything."
 - Middle: Partial knowledge. "I know this is an integer," or "I know this is a struct with a field called port."
 - Top (Leaf): Concrete knowledge. "This is exactly the number 8080."
When we say CUE is "based on Order Theory," we mean that computation only moves in one direction: from General to Specific.
1. Assignment vs. Refinement (The Crucial Difference)
The "Assignment" Model (Imperative)
In languages like Python or Helm templates, variables are containers. You can empty the container and put something else in.
 - Step 1: replicas = 2
 - Step 2: replicas = 4
 - Result: replicas is 4. The history is lost. This is destructive.
The "Refinement" Model (Order Theory)
In CUE, variables are not containers; they are definitions of truth. You cannot change the truth; you can only add more detail to it.
 - Constraint A: replicas: int (It must be an integer)
 - Constraint B: replicas: >1 (It must be greater than 1)
 - Constraint C: replicas: 4 (It is exactly 4)
Because 4 is an int AND >1, this is valid.
If you tried to add Constraint D: replicas: 5, CUE would fail. You cannot say "It is exactly 4" and "It is exactly 5" at the same time.
1. Why is this called a "Partial Order"?
It is "partial" because not every value can be compared or unified.
 - You can compare int and 5 (because 5 is a type of int).
 - You cannot compare 5 and "cat" (they are incomparable branches of the lattice).
In a Helm chart, if you mix a string and an int, it might crash at runtime. In CUE, because string and int have no ordering relationship (one is not a subset of the other), the system rejects the configuration instantly.
Summary for the Architect
When the quote says "discard assignment," it means:
Stop thinking: "First I set the default, then I override it with the production value."
Start thinking: "First I define the shape of the data (schema), and then I fill in the details (values). If the details don't fit the shape, the config is invalid."
