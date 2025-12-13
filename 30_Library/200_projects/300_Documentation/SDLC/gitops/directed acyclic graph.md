---
aliases: []
confidence: 
created: 2025-03-21T04:21:01Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:50Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [git]
title: directed acyclic graph
type: 
uid: 
updated: 
version: 
---

No, the data in Git is not stored as a linked list. It's stored as a directed acyclic graph (DAG).

Here's why this distinction is important:

Linked List vs. Directed Acyclic Graph (DAG)

- Linked List:
    - A linked list is a linear data structure where each element (node) points to the next element
    - It has a single starting point (head) and a single ending point (tail)
    - Traversal is strictly sequential
    - There are no branches or merges.
- Directed Acyclic Graph (DAG):
    - A DAG is a collection of nodes (commits) connected by directed edges (parent-child relationships)
    - It allows for branching and merging, meaning a node can have multiple parents or children
    - It has a direction (the edges point from parent to child), but it's acyclic (there are no loops)
    - Traversal can be non-linear.

Git's Data Structure

- Git's commit history is a DAG because:
    - Commits are nodes.
    - Parent-child relationships between commits are edges
    - Branches and merges create non-linear relationships.
    - Git's history is directed (commits point to their parents)
    - Git's history is acyclic (you can't have a commit that's its own ancestor)

Why a DAG Is Essential for Git

- Branching and Merging:
    - A linked list couldn't represent branching and merging, which are fundamental Git operations.
    - A DAG allows Git to track the complex relationships between commits in different branches.
- Efficient History Traversal:
    - While you can traverse Git's history linearly (e.g., `git log`), you can also traverse it non-linearly to explore specific branches or merge histories.
    - A DAG supports this flexibility.
- Accurate Representation of History:
    - A DAG accurately represents the true nature of version control, where changes can diverge and converge.
