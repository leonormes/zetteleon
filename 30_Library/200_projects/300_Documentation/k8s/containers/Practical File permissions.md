---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, linux]
title: Practical File permissions
type: 
uid: 
updated: 
version: 
---

```sh
-rw-r--r-- 1 bitnami bitnami       4188 Nov  9  2023 .bashrc
```

Let's break down the Linux file permissions and metadata for the `.bashrc` file:

```sh
-rw-r--r-- 1 bitnami bitnami 4188 Nov  9  2023 .bashrc
```

## 1. File Type & Permissions (`-rw-r--r--`)
   - First Character: `-` indicates this is a regular file
     (Common types: `d`=directory, `l`=symlink, `c`/`b`=device)

   - Permissions Triplet (3 groups of 3 characters):
     1. Owner (User): `rw-`
        - Read (✔️)
        - Write (✔️)
        - Execute (❌)
     2. Group: `r--`
        - Read (✔️)
        - Write (❌)
        - Execute (❌)
     3. Others/World: `r--`
        - Read (✔️)
        - Write (❌)
        - Execute (❌)

## 2. Hard Link Count (`1`)
   - This file has 1 hard link (typical for regular files; directories usually have more).

## 3. Ownership
   - Owner: `bitnami` (user who owns the file)
   - Group: `bitnami` (group that owns the file)

## 4. File Size (`4188`)
   - Size: 4188 bytes (~4.1 KB).

## 5. Last Modified (`Nov  9  2023`)
   - Last modified on November 9, 2023.

## 6. File Name (`.bashrc`)
   - A hidden file (starts with `.`) used for user-specific Bash shell configurations.

---

## Permission Summary Table

| Permission Class | Read | Write | Execute |
|-------------------|------|-------|---------|
| Owner (`bitnami`) | ✔️   | ✔️    | ❌      |
| Group (`bitnami`) | ✔️   | ❌    | ❌      |
| Others            | ✔️   | ❌    | ❌      |

## Octal Representation
- `-rw-r--r--` translates to 644 in octal:
  - Owner: `6` (4+2+0 = read + write)
  - Group: `4` (read)
  - Others: `4` (read)

Let's clarify the breakdown of the 10-character permission string (e.g., `-rw-r--r--`):

## The 10 Characters Explained
1. 1st Character: File type (not a permission).
   - Indicates the type of file (e.g., regular file, directory, symlink).
- Examples:

  | Character | File Type |
  |-----------|-----------|
  | `-` | Regular file |
  | `d` | Directory |
  | `l` | Symbolic link |
  | `b` | Block device |
  | `c` | Character device |
  | `s` | Socket |
  | `p` | Named pipe (FIFO) |

2. Next 9 Characters: Permissions split into 3 groups of 3 (owner, group, others):
   - Characters 2–4: Owner permissions (`rw-` in your example).
   - Characters 5–7: Group permissions (`r--`).
   - Characters 8–10: Others/World permissions (`r--`).

---

## Example Breakdown (`-rw-r--r--`)

```sh
- r w - r - - r - -
│ │ │ │ │ │ │ │ │ │
1 2 3 4 5 6 7 8 9 10
```

1. 1st Character (`-`): Regular file.
2. 2–4 (`rw-`): Owner has read + write, no execute.
3. 5–7 (`r--`): Group has read only.
4. 8–10 (`r--`): Others have read only.

---

## Why 10 Characters Total
- 1 character for file type.
- 9 characters for permissions (3 groups × 3 permissions).
- Total = 10 characters.

To list groups on a Linux system via the command line, use one of the following methods:

---

### 1. List All Groups on the System

```bash
cat /etc/group
```

   - Displays all groups stored in the `/etc/group` file.
   - Each line follows the format: `group_name:password:GID:members`.

   Example Output:

```sh
root:x:0:
sudo:x:27:ubuntu
bitnami:x:1000:
```

---

### 2. List Groups Using `getent` (for Systems with LDAP/NIS)

```bash
getent group
```

   - Works like `cat /etc/group` but also includes groups from external databases (e.g., LDAP).

---

### 3. List Groups the Current User Belongs To

```bash
groups
```

   - Shows a space-separated list of groups for the current user.

   Example Output:

```sh
bitnami sudo docker
```

---

### 4. List Groups for a Specific User

```bash
groups username
```

   - Replace `username` with the target user (e.g., `groups bitnami`).

---

### 5. Detailed Group Info with `id`

```bash
id -Gn  # Group names for the current user
id -Gn username  # Group names for a specific user
id -G   # Group IDs (GIDs) for the current user
```

   - `-Gn`: Lists group names.
   - `-G`: Lists group IDs.

   Example:

```bash
$ id -Gn bitnami
bitnami sudo docker
```

---

### Key Notes
- Use `sudo` if you need elevated privileges to view restricted group data.
- `/etc/group` and `getent group` show all system groups.
- `groups` and `id` focus on the current user or a specified user.
