---
aliases: []
confidence: 
created: 2025-03-21T10:46:29Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:50Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [git]
title: Git Command to Clone only the git Folder
type: 
uid: 
updated: 
version: 
---

Yes, there is a Git command that allows you to clone a repository without checking out the working tree (i.e., without unpacking the files and folders). This is achieved using the `--no-checkout` option in conjunction with the `--bare` option, or the `--sparse` option.

## Using `--bare`

The `--bare` option creates a bare repository. A bare repository stores the repository's history but does not have a working tree. This is ideal for server-side repositories.

```bash
git clone --bare <repository_url> <destination_directory>.git
```

Explanation:

 - git clone: The base command for cloning a repository.
 - --bare: Creates a bare repository, which means:
   - No working tree.
   - All Git metadata is stored directly in the repository directory (i.e., the .git directory is the repository directory itself).
   - Typically used for remote repositories.
 - <repository_url>: The URL of the Git repository you want to clone.
 - <destination_directory>.git: The directory where the bare repository will be created. The .git suffix is a common convention for bare repositories.
Example:
git clone --bare [https://github.com/example/my-repo.git](https://github.com/example/my-repo.git) my-repo.git

This will create a directory named my-repo.git containing only the Git metadata.

Using --no-checkout and --sparse

For a non-bare clone where you want to retrieve the git history, but not checkout the working directory, you can also use --no-checkout in combination with --sparse. This is useful if you want to inspect the history, but don't need the files immediately.

git clone --no-checkout --sparse <repository_url> <destination_directory>

Explanation:

 - git clone: The base command for cloning a repository.
 - --no-checkout: After the clone, no file is checked out.
 - --sparse: Enables sparse checkout, which, when combined with --no-checkout prevents any file from being checked out.
 - <repository_url>: The URL of the Git repository you want to clone.
 - <destination_directory>: The directory where the repository will be created.
Example:
git clone --no-checkout --sparse [https://github.com/example/my-repo](https://www.google.com/search?q=https://github.com/example/my-repo) my-repo

This will create a directory named my-repo containing the .git directory and an empty working tree.

Choosing between --bare and --no-checkout --sparse

 - If you need a server-side repository or only the Git history without any working tree, use --bare.
 - If you need to inspect the history, such as logs, branches, or tags, but do not need the files immediately, or want to perform a sparse checkout later, use --no-checkout --sparse.
In either case, the result will be that the cloned repository will not contain the files and folders of the working tree, only the git history within the .git folder.
