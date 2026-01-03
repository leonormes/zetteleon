---
aliases: []
confidence: "1.0"
created: 2025-11-22T15:00:01Z
epistemic: "definition"
last_reviewed: "2025-11-22"
modified: 2026-01-03T10:19:42+00:00
purpose: "Defines the software endpoint for network communication."
review_interval: "90"
see_also: []
source_of_truth: []
status: "seedling"
tags: ["topic/technology/networking/kernel"]
title: Concept - Network Socket
type: "concept"
uid: 
updated: 
---

## Network Socket

**Summary:** A network socket is a software endpoint that allows a program to send and receive data across a network.

**Details:**
In the Linux kernel, a socket maintains specific state required for communication, such as sequence numbers, congestion windows, and timers for TCP connections. It serves as the interface between the application layer (via system calls like `write()` or `send()`) and the networking stack.
