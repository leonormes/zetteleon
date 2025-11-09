---
aliases: []
confidence: 
created: 2025-08-19T23:32:29Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Prime Numbers Create a Mathematical Trapdoor
type:
uid: 
updated: 
version:
---

The security of modern public-key cryptography (like RSA) is built on a trapdoor function: an operation that is easy to do in one direction but extremely difficult to reverse without a secret piece of information.

The use of prime numbers provides this.

- Easy Direction: Multiplying two enormous prime numbers (p and q) to get a modulus (n) is computationally trivial.
- Hard Direction: Factoring the modulus n to find the original p and q is practically impossible for large numbers.
  The secret knowledge of p and q is the "trapdoor" that allows the owner to easily perform otherwise impossible calculations, such as creating the private key.
  Links to: [[Prime Numbers Are the Atomic Elements of All Numbers]], [[Public and Private Keys Are Mathematically Asymmetric]]

[[prime atoms]]
