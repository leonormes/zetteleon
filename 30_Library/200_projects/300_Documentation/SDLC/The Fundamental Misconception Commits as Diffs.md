---
aliases: []
confidence: 
created: 2025-03-18T09:03:35Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:44Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [data-centric, git]
title: The Fundamental Misconception Commits as Diffs
type: 
uid: 
updated: 
version: 
---

The common visualization of commits as a series of diffs is misleading. When we see `git log -p`, it shows the changes between commits, reinforcing this diff-centric view. However, this is just a *presentation* of the data, not the underlying storage.

**The Reality: Commits as Snapshots**

In reality, each commit in Git is a complete snapshot of your project's entire working directory at a specific point in time. Here's a breakdown of how Git stores this data:

1. **Blobs:**
    - These are the fundamental data units in Git. A blob represents the content of a file.
    - Git stores the content of each version of every file as a blob.
    - Blobs are identified by their SHA-1 hash, which is calculated based on their content. This means if two files have the same content, they will have the same blob ID.
    - Blobs are content addressable. If the content changes, a new blob is created.
2. **Trees:**
    - A tree object represents a directory.
    - It contains a list of blobs (files) and other trees (subdirectories), along with their names and permissions.
    - Like blobs, trees are also identified by their SHA-1 hash, which is calculated based on their content (the list of blobs and subtrees it contains).
    - Trees allow git to store the directory structure of your repo.
3. **Commits:**
    - A commit object is the top-level object in Git.
    - It contains:
        - A reference to a single tree object (the root directory of the snapshot).
        - Metadata:
            - Author and committer information (name, email, timestamp).
            - Commit message.
            - References to parent commit(s). This is what creates the commit history.
    - Commits, like trees and blobs, are also identified by their SHA-1 hash.
4. **Tags and Branches:**
    - Tags are simply named pointers to specific commits.
    - Branches are also named pointers to specific commits. The difference is that a branch pointer usually moves as new commits are added.

**Visualizing the Data Model**

Imagine a file system where each file version and directory structure is stored as a unique object identified by its content.

- **Initial Commit:**
    - Git takes a snapshot of your working directory.
    - It creates blobs for each file.
    - It creates trees to represent the directory structure, pointing to the blobs.
    - It creates a commit object pointing to the root tree, with metadata.
- **Subsequent Commits:**
    - If a file is modified, a new blob is created for the updated content.
    - If a file is added or deleted, the corresponding tree is updated (creating a new tree object).
    - A new commit object is created, pointing to the new root tree and referencing the previous commit as its parent.

**Key Takeaways**

- **Snapshots, Not Diffs:** Git stores the complete state of your project at each commit, not just the changes.
- **Content-Addressable Storage:** Git uses SHA-1 hashes to identify objects, ensuring data integrity and efficient storage.
- **Object Relationships:** Commits, trees, and blobs form a directed acyclic graph (DAG), which represents the commit history and project structure.

**Why Git Shows Diffs**

If Git stores snapshots, why does it show diffs?

- **Efficiency:** Displaying diffs is more efficient for humans to understand changes. It's easier to see what has changed than to compare two complete snapshots.
- **`git diff` and `git log -p`:** These commands calculate the differences between snapshots on the fly. They don't store diffs.
- **Storage Optimization:** While Git stores snapshots, it uses a technique called delta storage to optimize space. If a file is only slightly modified, Git can store the new blob and a reference to the previous blob, along with the changes (a delta). However, this is an internal optimization and doesn't change the fundamental data model.

**Building a Better Mental Model**

1. **Think in terms of objects:** Visualize your repository as a collection of blobs, trees, and commits, each identified by its SHA-1 hash.
2. **Focus on the commit graph:** Understand how commits are connected through parent references, forming a directed acyclic graph.
3. **Separate storage from presentation:** Remember that Git stores snapshots, but displays diffs for human convenience.
4. **Use `git cat-file`:** This command allows you to inspect the raw Git objects directly. For example:
    - `git cat-file -t <object-hash>` (shows the object type)
    - `git cat-file -p <object-hash>` (shows the object content)
5. **Visualize with `gitk` or `git log --graph --oneline --decorate --all`:** These tools help you visualize the commit graph and understand the relationships between commits.

**Example**

```sh
$ git cat-file -t <commit-hash>
commit

$ git cat-file -p <commit-hash>
tree <tree-hash>
parent <parent-commit-hash>
author ...
committer ...
...

$ git cat-file -t <tree-hash>
tree

$ git cat-file -p <tree-hash>
100644 blob <blob-hash>    file1.txt
040000 tree <subtree-hash> subdirectory

$ git cat-file -t <blob-hash>
blob

$ git cat-file -p <blob-hash>
Contents of file1.txt
```

By working through these examples, you can start to see how Git's data model works in practice.

By consistently visualizing the repository as a network of objects, you'll develop a more accurate and powerful understanding of Git.
