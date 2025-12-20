---
aliases: []
confidence: 
created: 2025-10-24T15:25:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [filesystem, kernel, linux, type/fact, vfs]
title: What is the Linux VFS (Virtual File System)
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a network namespace]], [[What is a mount namespace]]

## Summary

The Virtual File System (VFS) is a kernel abstraction layer that provides a uniform interface for different file systems to interact with the Linux kernel, enabling support for diverse file systems (disk-based, network, pseudo like /proc) through four primary object types: superblock, inode, dentry, and file.

## Context / Problem

Linux supports hundreds of file system types—ext4, NFS, tmpfs, proc, sysfs, and more. Without an abstraction layer, the kernel would need file-system-specific code throughout its codebase. VFS solves this by providing a common interface that all file systems implement, allowing the kernel to treat them uniformly while each file system handles its own internal details.

## Mechanism / Details

### The Four VFS Object Types

#### 1. Superblock
**Represents**: An entire mounted file system  
**Contains**:

- File system type (ext4, tmpfs, NFS, etc.)
- Block size
- Mount flags (read-only, noexec, etc.)
- Pointers to other critical structures
- Root inode reference

**Operations**: Reading/writing superblock metadata, allocating inodes, syncing file system

#### 2. Inode
**Represents**: A file or directory  
**Contains**:

- File size
- Ownership (UID, GID)
- Permissions (rwxrwxrwx)
- Timestamps (atime, mtime, ctime)
- Location of data blocks on disk
- File type (regular file, directory, symlink, device)

**Operations**: Creating, deleting, reading, writing files; changing permissions; creating links

**Note**: Inode does NOT contain the filename—that's stored in directory entries (dentries)

#### 3. Dentry (Directory Entry)
**Represents**: A mapping from filename to inode  
**Contains**:

- Filename string
- Pointer to corresponding inode
- Pointer to parent dentry
- Pointers to child dentries (if directory)

**Purpose**: **Caching** to speed up path lookups  
**Example**: Path `/home/user/file.txt` creates dentries:

- `/` → inode 2
- `home` → inode 1024
- `user` → inode 2048
- `file.txt` → inode 4096

**Operations**: Lookup, validation, cache management

#### 4. File
**Represents**: An open file (from a process perspective)  
**Contains**:

- File descriptor (fd)
- Current offset (read/write position)
- Access mode (read, write, append)
- Pointer to dentry (and thus inode)
- Reference count

**Operations**: Read, write, seek, close, mmap

### VFS in Action: Opening a File

```bash
# Process executes:
open("/home/user/file.txt", O_RDONLY)

# Kernel VFS workflow:
1. Start at root dentry (/)
2. Lookup "home" → find inode 1024
3. Lookup "user" in inode 1024 → find inode 2048
4. Lookup "file.txt" in inode 2048 → find inode 4096
5. Check permissions on inode 4096 (can this process read?)
6. Allocate file object, link to inode 4096
7. Assign file descriptor (fd 3)
8. Return fd 3 to process
```

All steps use VFS abstractions—the actual file system (ext4, NFS) handles disk I/O.

### The Vfsmount Structure

**Represents**: A mounted file system instance  
**Contains**:

- Mount point path (e.g., `/home`)
- Pointer to superblock
- Mount flags (bind, remount, etc.)
- Parent and child mount relationships

**Purpose**: Represents a subtree in the overall file system hierarchy

**Example**:

```bash
mount /dev/sdb1 /mnt/data
# Creates vfsmount:
#   mount_point: /mnt/data
#   superblock: /dev/sdb1's ext4 superblock
#   parent: root filesystem's vfsmount
```

### VFS and Mount Namespaces

Each **mount namespace** has its own set of **vfsmount** structures, creating an isolated view of the file system hierarchy. Processes in different mount namespaces see different mount points even though they share the same underlying VFS.

**Example**:

- Container A mounts `/dev/sdc` at `/data`
- Container B does not see this mount
- Both use the same VFS layer, but different vfsmount trees

## Connections / Implications

### What This Enables

- **File system diversity**: Support ext4, btrfs, NFS, tmpfs with common kernel interface
- **Container file system isolation**: Mount namespaces leverage VFS to provide isolated views
- **Efficient caching**: Dentry cache speeds up repeated path lookups
- **Unified tools**: `ls`, `cat`, `cp` work on any file system via VFS

### What Breaks If This Fails

- **Dentry cache corruption**: File lookups become extremely slow or fail
- **Inode exhaustion**: Cannot create new files even with free disk space
- **Superblock corruption**: Entire file system becomes unmountable
- **File object leaks**: Process cannot open new files (too many open files)

### How It Maps to Containers

**Network namespaces** isolate network stack, but **mount namespaces** isolate file system views using VFS:

- Each container can have different `/etc/hosts` files
- Container A can mount `/tmp` as tmpfs, Container B as disk
- Kubernetes volumes use mount namespaces to present volumes to Pods

**Without mount namespace**:

- All containers share the same vfsmount tree
- Mounting in one container affects all containers
- **Security risk**: Container can modify host `/etc/passwd`

See: What is a mount namespace, How mount namespaces isolate file systems

## Questions / To Explore

- What is the difference between hard links and symbolic links in VFS?
- How does the dentry cache improve file system performance?
- What is the relationship between file descriptors and file objects?
- How do overlay file systems (OverlayFS) work with VFS?
- DEBUG - Process cannot open files (too many open files)
- How does Kubernetes use mount namespaces for volume management?
