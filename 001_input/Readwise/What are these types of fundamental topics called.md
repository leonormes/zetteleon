---
aliases: []
confidence: 
created: 2025-10-26T08:56:31Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:41Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: What are these types of fundamental topics called
type:
uid: 
updated: 
version:
---

That's a great observation about how learning works\! When understanding a more basic or general topic helps you grasp a more specific or complex one built upon it, those underlying topics are often called:

1. **Fundamental Concepts (or Fundamentals):** This is perhaps the most common term. Linux namespaces are a fundamental concept underlying containerisation, which Kubernetes utilises for networking (among other things).  
2. **Foundational Knowledge (or Foundations):** Similar to fundamentals, this emphasizes that these concepts form the base upon which more advanced topics are built. Understanding networking principles is foundational to understanding Kubernetes networking implementations.  
3. **Underlying Principles:** This term highlights the core rules, mechanisms, or theories that govern how the higher-level system works. The principles of IP addressing and routing underlie all network communication, including within Kubernetes.  
4. **Prerequisites:** In a more formal learning context, these might be called prerequisites – knowledge you ideally need before tackling the more advanced subject.  
5. **Core Concepts:** These are the essential ideas you need to understand a field. Network namespaces are a core concept in Linux containerisation.  
6. **Enabling Technologies/Concepts:** This term focuses on how the fundamental topic *makes possible* the more specific one. Linux namespaces are an enabling technology for container isolation.

**Why does understanding these "unlock" the current topic?**  
It works exactly as you experienced and described previously:

- **Provides Context:** Knowing the foundation explains *why* the specific topic (like Kubernetes networking) is designed the way it is. It's not arbitrary; it's built upon or constrained by the underlying principles (Linux networking, namespaces).  
- **Demystifies Complexity:** Higher-level systems often abstract away the details of the lower levels. Understanding the lower level (the fundamentals) removes the "magic," showing you the actual mechanisms at play. Kubernetes networking seems less like magic when you understand how routing, iptables/nftables, or network namespaces function.  
- **Builds a Robust Mental Model:** Instead of learning isolated facts about the specific topic, you're building a connected web of knowledge. Understanding the foundation gives you a stronger framework to hang the details of the specific topic on, leading to better retention and deeper comprehension.  
- **Facilitates Problem Solving:** When something breaks in the specific system (Kubernetes networking), understanding the underlying fundamentals (Linux networking) often allows you to diagnose and fix the problem more effectively, as the root cause might lie in that foundational layer.

So, when you dug into Linux namespaces, you were uncovering the **fundamental concepts** and **underlying principles** that **enable** container networking in systems like Kubernetes. This foundational knowledge provided the necessary **context** to truly understand how the higher-level system operates.
