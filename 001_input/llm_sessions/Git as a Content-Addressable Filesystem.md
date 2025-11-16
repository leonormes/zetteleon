---
aliases: []
confidence:
created: 2025-10-25T20:34:01Z
epistemic:
last_reviewed:
modified: 2025-10-30T11:06:54Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags:
  - git
title: Git as a Content-Addressable Filesystem
type:
uid:
updated:
version:
---

## Git as a Content-Addressable Filesystem

4. Branch:

   - Definition: A branch is a *movable pointer* to a commit. It represents a line of development.
   - Data Structure: A branch is essentially a file (usually under .git/refs/heads/) that contains the SHA-1 hash of a commit.
   - Example: The main branch might point to the latest commit in your main line of development. When you make a new commit on main, the branch pointer is updated to point to the new commit.
   - Lightweight: Branches are very lightweight because they only store a commit hash.

5. HEAD:

   - Definition: HEAD is a *pointer* to the currently checked-out branch or commit.
   - Data Structure: HEAD is usually a file (under .git/HEAD) that contains either:
     - A reference to a branch (e.g., ref: refs/heads/main).
     - A direct commit hash (in “detached HEAD” state).
   - Example: If you’re working on the main branch, HEAD will point to refs/heads/main.

Concrete Example: Making a Change

1. Initial State: You have a file my_document.txt with “Hello, world!”. Git creates a blob for it and a tree pointing to that blob. You make a commit, creating the initial snapshot.
2. Modify File: You change my_document.txt to “Hello, Git!”.
3. New Blob: Git creates a *new* blob with the content “Hello, Git!”. This new blob has a different SHA-1 hash.
4. Updated Tree: Git creates a *new* tree that’s identical to the old tree except that the entry for my_document.txt now points to the new blob.
5. New Commit: Git creates a *new* commit that points to the updated tree. This commit becomes the new tip of your branch.

Git’s Core Data Structures
