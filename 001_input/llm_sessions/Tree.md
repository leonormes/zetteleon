---
aliases: []
confidence: 
created: 2025-10-25T20:38:54Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:55Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tree
type:
uid: 
updated: 
version:
---

What is a tree

Represents a directory. Trees store a list of blobs and other trees (subdirectories), along with their names and permissions. Think of it as a snapshot of a directory at a specific point in time.

- Definition: A tree represents a *directory*. It maps filenames to blobs (for files) or other trees (for subdirectories).
- Data Structure: A tree can be thought of as a dictionary or a map. The keys are filenames, and the values are pointers (SHA-1 hashes) to blobs or other trees.
- Example: Imagine you have a directory my_project with files my_document.txt and image.png, and a subdirectory src with main.py. The my_project tree would have entries like:
  - my_document.txt -> (SHA-1 hash of “Hello, world!” blob)
  - image.png -> (SHA-1 hash of image data blob)
  - src -> (SHA-1 hash of the src tree)
- Hierarchical Structure: Trees allow Git to represent the entire directory structure of your project.

Git’s Core Data Structures
