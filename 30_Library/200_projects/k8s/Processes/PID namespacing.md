---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
id: PID namespacing
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, Processes]
title: PID namespacing
type: curriculum
uid: 
updated: 
version: 1
---

I'm trying to learn about Linux kernel namespacing and how it is used to make containers. how can I get hands on with pod namespacing to learn how it works and what it can do at a low level? find practical tutorials

To get hands-on experience with Linux kernel namespacing and understand how it's used to create containers, you can try the following practical tutorials and exercises:

## Using Unshare Command

The `unshare` command is a great way to experiment with namespaces directly:

1. Create a new UTS namespace:

```bash
sudo unshare --uts /bin/bash
```

This will give you a shell in a new UTS namespace. Try changing the hostname and observe how it doesn't affect the host system.

2. Create a PID namespace:

```bash
sudo unshare --pid --fork /bin/bash
```

Inside this namespace, you'll see a new process tree starting from PID 1.

## Namespace Exploration with Nsenter

Use `nsenter` to enter existing namespaces:

1. Find the PID of a running container:

```bash
docker inspect --format '{{.State.Pid}}' \<container_name\>
```

2. Enter the container's namespaces:

```bash
sudo nsenter --target \<container_pid\> --mount --uts --ipc --net --pid /bin/bash
```

This allows you to explore the container's isolated environment.

## Creating a Simple Container

Try creating a basic container using namespaces and chroot:

1. Create a root filesystem:

```bash
mkdir container-root
sudo debootstrap --variant=minbase bionic container-root
```

2. Use unshare to create isolated namespaces and chroot into the new root:

```bash
sudo unshare --mount --uts --ipc --net --pid --fork --user --map-root-user chroot container-root /bin/bash
```

This gives you a minimal container-like environment.

## Namespace Types and Their Effects

Experiment with different namespace types:

1. Network namespace:

```bash
sudo ip netns add mynet
sudo ip netns exec mynet ip link
```

This creates an isolated network stack.

2. Mount namespace:

```bash
sudo unshare --mount /bin/bash
```

Try mounting filesystems and observe how they're isolated from the host.

## Practical Tutorials

1. Linux Namespaces Tutorial:
   Follow the hands-on examples in the "Linux Container Primitives" series. It provides step-by-step instructions for creating and managing different types of namespaces.

2. DIY Container Tutorial:
   The "Linux containers from scratch" guide offers a comprehensive walkthrough of creating containers using namespaces, including code examples and explanations.

3. Namespace Types Deep Dive:
   Explore each namespace type in detail using the examples provided in the "Understanding Linux Namespace Types" article. This will give you a thorough understanding of how each namespace type functions.

4. Container Creation from Scratch:
   Follow the tutorial in the "how-containers-works" GitHub repository. It provides practical examples of creating containers using namespaces and cgroups.

5. Kubernetes Namespace Hands-On:
   While not directly related to kernel namespacing, practicing with Kubernetes namespaces can help you understand how isolation is applied at a higher level. Try the "Hands-on Introduction to Namespace" tutorial for practical exercises.

What are some practical exercises to understand PID namespaces in Linux

To understand PID namespaces in Linux, you can try the following practical exercises:

1. Create a new PID namespace:

```bash
sudo unshare --pid --fork /bin/bash
```

This will give you a shell in a new PID namespace.

2. Inside the new namespace, run:

```bash
echo $$
ps aux
```

Observe how the process IDs differ from the host system.

## Exploring Nested Namespaces

1. Create nested PID namespaces:

```bash
sudo unshare -fp /bin/bash
sleep 90000 &
ps -ef
sudo unshare -fp /bin/bash
sleep 8000 &
ps -ef
```

2. Examine the PID ancestry:

```bash
sudo cat /proc/\<PID\>/status | grep NSpid
```

Replace \\<PID\\> with the PID of a process in the nested namespace.

## Entering Existing Namespaces

1. List available PID namespaces:

```bash
sudo lsns --type pid
```

2. Enter a specific PID namespace:

```bash
sudo nsenter -t \<PID\> -p -r bash
```

Replace \<PID\> with the PID of a process in the target namespace.

## Creating a Simple Container

1. Create a new PID namespace with mount isolation:

```bash
sudo unshare -mipf
```

2. Inside the new namespace, run:

```bash
echo $$
ps aux
mount -t proc proc /proc
ps aux
```

Observe how the process tree changes after mounting procfs.

## Visualizing Process Trees

1. On the host system, run:

```bash
pstree -S
```

2. Create a new PID namespace:

```bash
sudo unshare -mipf
```

3. Inside the new namespace, run:

```bash
pstree -S
```

Compare the process trees in both environments.

## Writing Custom Programs

1. Write a C program that prints its own PID and parent PID:

```c
#include \<stdio.h\>
#include \<unistd.h\>

int main() {
    printf("PID: %d\n", getpid());
    printf("Parent PID: %d\n", getppid());
    return 0;
}
```

2. Compile and run this program in a new PID namespace:

```bash
gcc -o pid_info pid_info.c
sudo unshare --pid --fork ./pid_info
```

3. Compare the output with running the program directly on the host.

These exercises will give you hands-on experience with PID namespaces and help you understand how process isolation works in Linux containers.

How do I list all the PID namespaces currently active on my system

To list all the PID namespaces currently active on your system, you can use the following methods:

## Using Lsns Command

The most straightforward way to list all PID namespaces is by using the `lsns` command:

```bash
sudo lsns --type pid
```

This command will display all active PID namespaces, including their namespace ID, owner user, PID of the first process in the namespace, and other relevant information.

## Exploring /proc Directory

You can also manually explore the /proc directory to find all PID namespaces:

```bash
sudo find /proc//ns/pid -type l | xargs readlink | sort -u
```

This command searches for all pid namespace links in /proc, reads their targets, and displays unique results.

## Using Ps Command

The `ps` command can be used to show PID namespace information for running processes:

```bash
ps -e -o pidns,pid,args
```

This will display the PID namespace ID, process ID, and command for each running process.

## Python Script

For a more comprehensive view, you can use the `listns.v3.py` Python script:

1. Download the script:

```bash
wget https://raw.githubusercontent.com/Intika-Linux-Namespace/Namespace-Lister/master/listns.v3.py
```

2. Run the script with sudo:

```bash
sudo python3 listns.v3.py | grep pid:
```

This script will list all namespaces, including PID namespaces, along with their inode numbers.

Remember that to see all PID namespaces, you need to run these commands with root privileges, as some namespaces may not be visible to regular users.

is it possible to break out of a pid namespace

Yes, it is possible to break out of a PID namespace under certain conditions. While PID namespaces are designed to isolate processes, there are several ways an attacker could potentially escape:

1. Exploiting kernel vulnerabilities: Certain kernel bugs can allow an attacker to escape PID namespace isolation. For example, CVE-2022-0185 was a vulnerability that allowed container escape and privilege escalation by exploiting a flaw in the Linux kernel's handling of extended attributes.
2. Privileged containers: If a container is running with elevated privileges, especially with the CAP_SYS_ADMIN capability, it may be possible to escape the PID namespace. This capability allows joining other namespaces, potentially leading to a full container escape.
3. Shared user namespaces: If the PID namespace is not properly isolated from the host's user namespace, an attacker might be able to leverage this to escape containment.
4. Improper namespace configuration: Misconfigurations in container runtimes or orchestration platforms can sometimes lead to namespace isolation failures.
5. Host component leaks: Some container escape vulnerabilities arise from host components being inadvertently exposed within the container, which can be leveraged to break out of namespaces.

It's important to note that while PID namespaces provide a layer of isolation, they are most effective when used in conjunction with other security measures such as:

- Proper configuration of container runtimes
- Regular patching of the host kernel and container software
- Implementing the principle of least privilege
- Using additional isolation techniques like seccomp filters and AppArmor profiles

To mitigate the risk of PID namespace escapes, it's crucial to follow container security best practices, keep systems updated, and use tools that can detect potential container escape attempts.
