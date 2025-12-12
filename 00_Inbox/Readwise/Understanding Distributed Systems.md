---
aliases: []
confidence: 
created: 2025-12-12T15:49:33Z
epistemic: 
last_reviewed: 
modified: 2025-12-12T16:07:53Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [books]
title: Understanding Distributed Systems
type: 
uid: 
updated: 
---

## Understanding Distributed Systems

![rw-book-cover](https://m.media-amazon.com/images/I/61otEO9SSYL._SY160.jpg)

### Metadata
- Author: [[Roberto Vitillo]]
- Full Title: Understanding Distributed Systems
- Category: #books

### Highlights
- We can generate a skeleton of the HTTP adapter by defining the API of the service with an interface definition language (IDL). An IDL is a language-independent definition of the API that can be used to generate boilerplate code for the server-side adapter and client-side software development kits (SDKs) in your languages of choice. ([Location 502](https://readwise.io/to_kindle?action=open&asin=B09YLRB7QV&location=502))
- Finally, we can also model timing assumptions: The synchronous model assumes that sending a message or executing an operation never takes more than a certain amount of time. This is not very realistic for the type of systems we care about, where we know that sending messages over the network can potentially take a very long time, and processes can be slowed down by, e.g., garbage collection cycles or page faults. The asynchronous model assumes that sending a message or executing an operation on a process can take an unbounded amount of time. Unfortunately, many problems can’t be solved under this assumption; if sending messages can take an infinite amount of time, algorithms can get stuck and not make any progress at all. Nevertheless, this model is useful because it’s simpler than models that make timing assumptions, and therefore algorithms based on it are also easier to implement2. The partially synchronous model assumes that the system behaves synchronously most of the time. This model is typically representative enough of real-world systems. ([Location 699](https://readwise.io/to_kindle?action=open&asin=B09YLRB7QV&location=699))
- In the rest of the book, we will generally assume a system model with fair-loss links, crash-recovery processes, and partial synchrony. If you are curious and want to learn more about other system models, “Introduction to Reliable and Secure Distributed Programming”3 is an excellent theoretical book that explores distributed algorithms for a variety of models not considered in this text. ([Location 707](https://readwise.io/to_kindle?action=open&asin=B09YLRB7QV&location=707))
