---
aliases: []
confidence: 
created: 2025-03-18T12:03:49Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [data-centric, git]
title: undoing changes in git
type: 
uid: 
updated: 
version: 
---

## Understanding the Problem

How to Undo Commits

Here are the main ways to undo commits, and how to choose the right approach:

- `git revert <commit-hash>`
- This creates a new commit that undoes the changes introduced by the specified commit.
- It's the safest option for public repositories because it preserves the commit history.
### How it Works
- Git analyses the changes in the target commit and generates a new commit that applies the inverse changes.
- Example: If you want to undo the changes of commit abcdef123456, you would run git revert abcdef123456. This will create a new commit with the inverse changes.
- When to use: When you intend to undo a commit without rewriting history, especially in shared repositories.
- `git reset --hard <commit-hash>`
- This moves the current branch pointer to the specified commit and discards all subsequent commits.
- It's a destructive operation and should be used with caution, especially in shared repositories.
- Example: git reset --hard 123456abcdef will move your branch to the commit with that hash, and delete all commits that came after it.
- When to use: When you want to completely remove commits from your local history, and you are absolutely sure those commits are not needed by anyone else.
- git reset --soft \<commit-hash\>:
- This moves the current branch pointer to the specified commit, but keeps the changes from the subsequent commits in the staging area.
- This allows you to modify the changes and create a new commit.
- When to use: When you want to undo commits but preserve the changes for further modification or to create a new commit.
- git reset --mixed \<commit-hash\>:
- This moves the current branch pointer to the specified commit, but keeps the changes from the subsequent commits in the working directory.
- This allows you to selectively stage changes and create a new commit.
- When to use: When you want to undo commits and have the changes available to be re-staged.
- git commit --amend:
- This allows you to modify the last commit.
- It creates a new commit with the updated changes and replaces the old commit.
- When to use: When you want to correct mistakes in the last commit, such as typos in the commit message or missing changes.
## Addressing Your Specific Scenario

If you have a commit that adds a new line and you want to undo that change, you should:

- Identify the commit hash: Use git log to find the hash of the commit that added the new line.
- Choose the appropriate method:
- If you want to preserve the history, use git revert \<commit-hash\>.
- If you want to completely remove the commit (and you're working locally), use git reset --hard \<parent-commit-hash\>. Where parent commit hash is the commit before the one that added the line.
Key Point: When undoing a commit, you're not going back to a diff; you're going back to a snapshot. Therefore, to undo a commit, you need to revert to the parent commit of the commit you want to undo, or create a revert commit.
## Visualizing the Process

Imagine your commit history as a timeline:

A -\> B -\> C (new line added) -\> D

- To undo the changes introduced by commit C using git revert, you would create a new commit E that undoes the changes of C:
A -\> B -\> C -\> D -\> E (revert C)

- To undo the changes by removing commit C and D using git reset --hard you would reset to B.
A -\> B

By understanding that commits are snapshots, you can avoid confusion and choose the right method for undoing changes in your Git repository.

You are absolutely right to call me out on that. My phrasing, while common, still subtly reinforces the "commit as diff" misconception.

You've nailed it with your suggestion: "the snapshot (commit) where these changes first appear" is a much more accurate and helpful way to think about it.

Let's refine the language and concepts to be even more precise:

Instead of: "Undo the changes introduced by a specific commit."

Use: "Revert to the state of the repository before the snapshot (commit) where these changes first appeared."

Why this is better:

- Focus on the snapshot: It emphasizes that the commit is a complete snapshot, not just a set of changes.
- Time-based perspective: "Before the snapshot" clearly indicates that we're moving back in time to a previous state.
- Avoids "introduced" ambiguity: "Introduced" can imply that the commit is solely responsible for the changes, whereas it's actually capturing the state of the repo at that point.
## Further Refinements
- When discussing git revert, emphasize that it creates a new snapshot that reverses the effects of the target snapshot. For example: "Git revert creates a new snapshot that reverses the changes made in the target snapshot, effectively returning the repository to its state before those changes first appeared."
- When discussing git reset --hard, stress that it removes snapshots from the history. For example: "Git reset --hard removes the specified snapshot and all subsequent snapshots from the branch's history, irrevocably changing the project's state."
- When discussing git commit --amend emphasize that it creates a new snapshot that replaces the last snapshot.
## Applying the New Phrasing

Let's revisit the previous example:

- Original: "If you have a commit that adds a new line and you want to undo that change, you should..."
- Revised: "If you have a snapshot (commit) where a new line first appears and you want to revert to the state before that change, you should..."
By consistently using this more accurate language, we can reinforce the correct mental model of Git as a snapshot-based version control system.
Thank you for pointing out this important nuance. It's crucial to be precise when discussing Git's data model.

Yes, your assumption is correct. Git does optimize the process of generating diffs, and by default, git diff and related commands (like those used by git log -p) compare a commit to its parent.

Here's a breakdown of the process and the optimizations involved:

1. Basic Diff Generation
- Comparison: When you run git diff \<commit1\> \<commit2\>, Git compares the tree objects associated with those commits.
- Tree Traversal: It recursively traverses the tree structures, comparing blobs (file contents) at each level.
- Line-by-Line Comparison: For each file that has changed (i.e., the blob IDs differ), Git performs a line-by-line comparison to identify the added, removed, and modified lines.
- Output: The output is a diff, a human-readable representation of the differences between the two snapshots.
2. Optimizations
- Object Cache: Git caches the contents of blobs and trees in memory, reducing the need to read from disk.
- Delta Storage (Packfiles): While commits are snapshots, Git optimizes storage by storing only the differences (deltas) between similar objects in packfiles. This reduces the overall size of the repository. When git needs to compare two blobs, and they are stored as deltas, it must reconstruct the full blob to do the comparison.
- Heuristics: Git uses various heuristics to speed up the diffing process. For example, it may skip comparing files that have the same size and modification time.
- Efficient Diff Algorithm: Git uses a highly optimized diff algorithm, typically based on the Myers diff algorithm, to efficiently identify the differences between files.
- Comparing against parent: When you run git diff without specifying commits, it defaults to comparing the working directory against the staging area. When you run git diff --cached it compares the staging area against the last commit. When you use git log -p it compares each commit against its first parent. This is a common operation, and thus is well optimized.
3. Parent Comparison
- As you correctly stated, when you use git log -p or when Git needs to show the changes associated with a commit, it typically compares the commit to its parent.
- This is because the parent commit represents the state of the repository before the changes in the current commit were applied.
- This parent comparison is a very common operation, and as such is very well optimized.
4. Specifying Commits
- You can explicitly specify the commits to compare using git diff \<commit1\> \<commit2\>.
- This allows you to compare any two snapshots in the repository, regardless of their parent-child relationship.
In Summary
- Git generates diffs by comparing the tree objects associated with commits.
- It uses various optimizations to speed up the process, including object caching, delta storage, and efficient diff algorithms.
- By default, Git compares a commit to its parent when displaying changes.
- You can compare any 2 commits that exist within the repository.
Therefore, while the commit itself is a snapshot, the diff is indeed a comparison between two snapshots, most often the current commit and its parent.

Excellent, let's dive into Git's plumbing to demonstrate that commits are snapshots, not diffs, and that diffs are merely a presentation layer.

Scenario:

1. Create a simple repository with a few files.
2. Make a series of commits, each changing a different file.
3. Use Git plumbing commands to inspect the objects and demonstrate the snapshot nature of commits.

Steps:

1. Initialize a Repository and Create Files:

Bash

```sh
mkdir git-snapshot-demo
cd git-snapshot-demo
git init
echo "File 1, initial content" \> file1.txt
echo "File 2, initial content" \> file2.txt
git add file1.txt file2.txt
git commit -m "Initial commit"
```

2. Make a Change and Commit:

Bash

```sh
echo "File 1, modified content" \> file1.txt
git add file1.txt
git commit -m "Modified file1.txt"
```

3. Make Another Change and Commit:

Bash

```sh
echo "File 2, modified content" \> file2.txt
git add file2.txt
git commit -m "Modified file2.txt"
```

4. Inspecting the Objects:

- Find the Commit Hashes:

Bash

```sh
git log --format=%H
```

This will give you the commit hashes in reverse chronological order. Let's assume they are (from latest to oldest):

- `commit3_hash` (Modified file2.txt)
- `commit2_hash` (Modified file1.txt)
- `commit1_hash` (Initial commit)
- Inspect the Commits:

Bash

```sh
git cat-file -p <commit3_hash\>
git cat-file -p <commit2_hash\>
git cat-file -p <commit1_hash\>
```

Observe that each commit object contains:

- A `tree` hash.
- A `parent` hash (except the initial commit).
- Author and committer information.
- The commit message.
- Inspect the Trees:

Bash

```sh
git cat-file -p <tree_hash_from_commit3\>
git cat-file -p <tree_hash_from_commit2\>
git cat-file -p <tree_hash_from_commit1\>
```

Each tree object lists the blobs (files) and their corresponding hashes. Notice that:

- Each tree represents the *entire* state of the directory at that commit.
- Even if only one file changed, the tree reflects the state of *all* files.
- Inspect the Blobs:

Bash

```sh
git cat-file -p <blob_hash_of_file1_from_commit1\>
git cat-file -p <blob_hash_of_file1_from_commit2\>
git cat-file -p <blob_hash_of_file1_from_commit3\> # Will be the same as commit2
git cat-file -p <blob_hash_of_file2_from_commit1\>
git cat-file -p <blob_hash_of_file2_from_commit2\> # Will be the same as commit1
git cat-file -p <blob_hash_of_file2_from_commit3\>
```

Observe that:

- Each blob represents the *entire* content of a file at a specific point in time.
- If a file's content changes, a new blob is created with a different hash.
- If a file's content remains the same, the same blob hash is used across commits.
- Demonstrating Diffs as Presentation:

Bash

```sh
git diff <commit2_hash\> <commit3_hash\>
```

This command *calculates* the diff by comparing the tree objects of `commit2_hash` and `commit3_hash`. It doesn't retrieve a pre-stored diff.

Also notice that if you run

```sh
git log -p <commit3_hash\>
```

Git compares `commit3_hash` to it's parent `commit2_hash` to generate the diff.

Observations:

- Snapshots: Each commit points to a tree that represents the complete state of the repository at that point in time.
- No Diffs Stored: The object database contains blobs (file contents), trees (directory structures), and commits (snapshots), but it does *not* store diffs.
- Diffs Calculated on Demand: The `git diff` command calculates diffs by comparing tree objects, demonstrating that diffs are a presentation of the data, not the underlying storage.

This exercise provides tangible proof that Git stores snapshots, not diffs, and that diffs are generated on the fly.

You've articulated the core of the matter perfectly. Yes, you've hit on the precise way to reconcile the "snapshot" model with the common perception of "changes":

- A "change" is indeed the difference between two snapshots (commits).

Let's break it down:

- Snapshot as the Foundation:
    - A commit is the fundamental unit of storage, representing the complete state of the repository at a given point in time
- Change as the Delta:
    - A "change" is a derived concept, calculated by comparing two snapshots.
    - When you look at a diff, you're seeing the output of a comparison between two tree structures, which ultimately leads to the comparison of the content of blobs.
    - When looking at `git log -p` the diff is the comparison between a commit and its parent commit.
- Multiple Snapshot Comparisons:
    - If you compare snapshots A and C, the diff shows the cumulative changes between those two points in time.
    - If you compare snapshots A and B, and then B and C, you will see the individual changes that together make up the changes between A and C.

Why This Matters

- Clarity:
    - This distinction clarifies that "changes" are a representation of differences, not the primary data stored by Git.
    - It helps to avoid the misconception that commits are inherently about changes.
- Flexibility:
    - Git's ability to compare any two snapshots allows you to analyze changes across any arbitrary period
    - This is useful for debugging, code reviews, and understanding the evolution of your project.
- Accurate Mental Model:
    - It reinforces the idea that Git is a snapshot-based system, with changes being a derived view.

In simpler terms:

- Think of commits as photographs taken at different times.
- A "change" is like pointing out the differences between two photographs.

Therefore, you are completely right. When we look at the diff between multiple snapshots they are changes.

Yes, you absolutely can! You can list all the blobs associated with a file, effectively getting its history. This involves traversing the commit history and extracting the blob IDs for the file at each commit. Here's how you can do it:

**1. Using `git log` and `git ls-tree`**

This is the most straightforward approach:

Bash

```sh
git log --pretty=format:"%H" -- .dockerignore | while read commit_hash; do
  git ls-tree $commit_hash .dockerignore | awk '{print $3}';
done | sort -u
```

**Explanation:**

- `git log --pretty=format:"%H" -- <file_path>`:
    - This lists all the commit hashes that have modified the specified file.
    - `--pretty=format:"%H"` formats the output to show only the commit hashes.
    - `-- <file_path>` limits the log to commits that involve the specified file.
- `while read commit_hash; do ... done`:
    - This loop iterates through each commit hash.
- `git ls-tree $commit_hash <file_path> | awk '{print $3}'`:
    - `git ls-tree` lists the contents of a tree object (in this case, the tree associated with the commit).
    - `$commit_hash` specifies the commit.
    - `<file_path>` specifies the file within the tree.
    - `awk '{print $3}'` extracts the third column, which is the blob ID.
- `sort -u`:
    - This sorts the blob IDs and removes duplicates.

**2. Using `git rev-list` and `git cat-file`**

This approach can be more efficient for large repositories:

```sh
git rev-list --objects -- <file_path> | grep blob | awk '{print $1}' | sort -u
```

**Explanation:**

- `git rev-list --objects -- <file_path>`:
    - This lists all the objects (blobs, trees, commits) that are reachable from the commits that have modified the specified file.
    - `--objects` includes all objects, not just commits.
    - `-- <file_path>` limits the list to objects related to the specified file.
- `grep blob`:
    - This filters the output to show only blob objects.
- `awk '{print $1}'`:
    - This extracts the first column, which is the blob ID.
- `sort -u`:
    - This sorts the blob IDs and removes duplicates.

**Viewing Blob Contents**

Once you have the blob IDs, you can view their contents using `git cat-file`:

Bash

```sh
git cat-file -p <blob_id>
```

**Important Considerations:**

- **File Renames:** If the file has been renamed, these commands may not show the complete history. You may need to use `git log --follow` to track renames.
- **Large Repositories:** For very large repositories, these commands may take some time to execute.
- **Binary Files:** If the file is a binary file, `git cat-file -p` will output the raw binary data, which may not be human-readable.

By using these techniques, you can effectively trace the history of a file's content by listing all the blobs associated with it. This reinforces the concept that the history of a file is the history of the blobs that make up the file, along with the trees that reference those blobs.
