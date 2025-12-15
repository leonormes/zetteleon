---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, namespace]
title: PID Namespace
type: instruction
uid: 
updated: 
version: 1
---

## 1. Create a New PID Namespace

```bash
# Create isolated PID namespace with mounted /proc (critical for accurate process view)
sudo unshare --pid --fork --mount-proc /bin/bash
```

Key flags:

- `--pid`: Creates new PID namespace
- `--fork`: Required to properly detach from parent process
- `--mount-proc`: Creates private /proc view (prevents host process leakage)

---

## 2. Verify Process Isolation

Inside namespace:

```bash
# View processes visible in the namespace
ps aux

# Check current shell's PID (should show 1)
echo $$

# Check namespace ID (compare with host)
ls -l /proc/$$/ns/pid
```

Expected output:

```sh
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   7236  2868 pts/0    S    12:34   0:00 /bin/bash
root         5  0.0  0.0   9088  3264 pts/0    R+   12:34   0:00 ps aux
```

---

## 3. Compare with Host System

In new terminal on host:

```bash
# Find actual PID of namespace process
ps aux | grep 'unshare.pid'

# Check namespace ID from host's perspective
sudo ls -l /proc/<PID>/ns/pid
```

---

## 4. Advanced Verification

Create a process inside the namespace:

```bash
# In namespace terminal
sleep 3600 &
echo $!  # Shows namespace PID (e.g., 2)
```

Check from host:

```bash
# Find real PID using namespace PID
sudo nsenter --target <HOST_PID> --pid ls -l /proc/2
```

---

## 5. Cleanup

```bash
# Exit namespace shell
exit

# Verify all child processes terminated
pstree -p | grep unshare
```

---

## Key Observations

1. PID Translation:
   - Inside namespace: PID 1 (your shell)
   - Host system: Actual PID (e.g., 45982)

2. Isolation Proof:

   ```bash
   # Inside namespace
   $ echo $$
   1

   # On host
   $ ps -p 45982 -o pid,cmd
   PID CMD
   45982 /bin/bash
   ```

3. Namespace ID Comparison:

   ```bash
   # Inside namespace
   $ readlink /proc/$$/ns/pid
   pid:[4026531836]

   # On host
   $ sudo readlink /proc/45982/ns/pid
   pid:[4026532207]
   ```

---

## Common Pitfalls

1. Missing `--mount-proc`:
   - `ps` shows host processes without it
2. Forgetting `--fork`:
   - New process tree won't detach properly
3. Root Privileges:
   - Namespace operations require `sudo`

To truly eliminate IoED, try:

1. Break the namespace and debug why `ps` shows host processes
2. Create nested PID namespaces
3. Write a script that automates namespace creation and verification

Docker and other production-grade container runtimes follow the same fundamental principles as homemade containers but add critical layers of security, standardization, and optimization. Let's break down the similarities and key differences:

---

## Core Similarities to Homemade Containers

All container systems ultimately use Linux kernel primitives:

1. Namespaces (Same Foundation):

```bash
# Docker equivalent of our earlier unshare command
docker run --pid=host --uts=host [...]  # Explicit namespace controls
```

   - PID, Mount, Network, UTS, IPC, User namespaces
   - Same kernel APIs (`unshare`, `setns`)

2. Control Groups (cgroups):

```bash
# Direct cgroup manipulation vs Docker's abstraction
echo "100000" > /sys/fs/cgroup/cpu/docker/<ID>/cpu.cfs_quota_us
```

   - Memory/CPU/IO limits enforced through cgroups v2

3. Filesystem Isolation:
   - Uses `overlay2` driver (layered FS) instead of basic `chroot`

---

## Key Differences in Production Runtimes

Here's what Docker/containerd do beyond basic primitives:

### 1. Security Hardening

| Primitive             | Homemade Container          | Docker Default               |
|-----------------------|-----------------------------|------------------------------|
| Capabilities          | Retains all                 | Drops 14+ capabilities       |
| Seccomp               | None                        | Default syscall filter       |
| AppArmor/SELinux      | Disabled                    | Custom profiles              |
| User Namespaces       | Often root-mapped           | Rootless mode support        |
| Device Control        | Full access                 | Whitelisted devices          |

Example security context:

```bash
docker run --security-opt seccomp=/path/profile.json \
           --cap-drop NET_RAW \
           --user 1000:1000 \
           [...]
```

### 2. Standardization & Ecosystem

- OCI Specifications: Docker implements Open Container Initiative standards for:
  - Image format (OCI Image Spec)
  - Runtime (OCI Runtime Spec)
  - Distribution (OCI Distribution Spec)
- Container Lifecycle Management:

```bash
# Compare to our basic namespace creation
docker run → containerd → runc → namespaces+cgroups
```

### 3. Advanced Features

| Feature               | Homemade          | Docker                  |
|-----------------------|-------------------|-------------------------|
| Networking            | Manual veth pairs | CNI plugins, DNS, SDN   |
| Storage               | Basic mounts      | Volume drivers, CSI     |
| Orchestration         | None              | Swarm/Kubernetes integration |
| Image Management      | Tarballs          | Layered images, registries |

---

## Docker's Container Creation Process

Here's the detailed flow when you run `docker run`:

1. Image Preparation:

```bash
# Uses containerd to pull and manage images
ctr images pull docker.io/library/nginx:latest
```

2. Runtime Setup:
   - Creates namespaces via `runc` (Docker's OCI runtime)
   - Applies cgroups via `systemd` or cgroupfs driver

3. Isolation Layers:

```bash
# View namespaces for a running container
ls -l /proc/$(docker inspect --format '{{.State.Pid}}' <ID>)/ns
```

4. Security Context:

```bash
# View applied security profile
docker inspect --format '{{.HostConfig.SecurityOpt}}' <ID>
```

5. Orchestration:

```bash
# Docker's control plane communication
dockerd → containerd → containerd-shim → runc
```

---

## Why Homemade Containers Are Insecure

1. Default Privileges:
   - Your basic `unshare` example runs as root with full capabilities
   - Docker drops privileges by default

2. Attack Surface:

```bash
# Compare syscall access
docker-secure: ~60 allowed syscalls
homemade:      ~300+ syscalls available
```

3. Resource Leakage:
   - Homemade containers often leak mounts, cgroups
   - Docker manages garbage collection

---

## Modern Container Runtimes Landscape

All major runtimes build on the same primitives but differ in implementation:

| Runtime      | Used By         | Key Differentiator          |
|--------------|-----------------|------------------------------|
| runc         | Docker, Podman  | Reference OCI implementation |
| crun         | Podman, CRI-O   | Written in C for performance |
| gVisor       | GCP, Cloud Run  | Kernel syscall interposition |
| Kata          | Confidential Compute | VM-like isolation       |
| Firecracker  | AWS Lambda      | MicroVM-based isolation     |

---

## Deep Dive Exercise

To truly overcome IoED, try this:

1. Inspect a Docker Container's Namespaces:

```bash
sudo ls -l /proc/$(docker inspect -f '{{.State.Pid}}' <ID>)/ns
```

2. Compare with Homemade:

```bash
# Create basic namespace
sudo unshare --pid --fork --mount-proc sleep 300 &
# Inspect its namespaces
ls -l /proc/$!/ns
```

3. Security Comparison:

```bash
# Docker's default seccomp profile
curl -O https://raw.githubusercontent.com/moby/moby/master/profiles/seccomp/default.json
# Compare to unconfined homemade container
```

---

## Key Takeaways

1. Same Foundation: All containers use namespaces/cgroups
2. Critical Additions:
   - Security profiles (seccomp, capabilities, LSMs)
   - Standardized image format and runtime
   - Ecosystem tooling (networking, storage, orchestration)
3. Production Requirements:
   - Defense-in-depth security
   - Resource guarantees
   - Cluster-aware operations

To truly master containers, I recommend:

1. Read the [runc source code](https://github.com/opencontainers/runc)
2. Experiment with [libcontainer](https://pkg.go.dev/github.com/opencontainers/runc/libcontainer) directly
3. Use [sysdig](https://sysdig.com/) to inspect container syscalls in real-time

This approach bridges the gap between "I can make a namespace" and "I understand real container security".

Okay, let's break down the technical details from the video about PID namespaces in Docker and the steps the presenter took for the demonstration.

Technical Details about PID Namespaces in Docker

1. PID Namespaces Isolate Process IDs:

    - The core concept is that PID namespaces provide isolation for process IDs. When you create a new PID namespace, the processes within it have their own set of PIDs, starting from 1 (typically the init process within that namespace).
    - This isolation means that a process inside the container cannot see or directly interact with processes outside of its own PID namespace (on the host or in other containers) using PIDs.
2. Hierarchy of PID Namespaces:

    - PID namespaces are hierarchical. The initial PID namespace on the system is the "root" namespace.
    - When you create a new PID namespace, it becomes a child of the namespace where it was created.
    - A parent namespace can see the processes in its child namespaces (it will see them with their PIDs relative to the parent namespace). However, a child namespace cannot see the processes in its parent or sibling namespaces.
3. Docker's Use of PID Namespaces:

    - By default, when you run a Docker container, it gets its own PID namespace.
    - This isolation is one of the reasons why processes inside a container typically start with PID 1.
    - It's also why running `ps` inside a container only shows you the processes within that container.
4. PID 1 in Containers (The Init Process):

    - The process with PID 1 inside a container's PID namespace is a special process – it's the init process.
    - The init process has responsibilities like reaping orphaned processes (processes whose parent has died) to prevent them from becoming zombies.
    - If the process with PID 1 dies, the entire container will typically be terminated.
5. Sharing PID Namespaces (Advanced):

    - Docker provides options to share PID namespaces.
    - `docker run --pid=host ...`: This allows a container to share the host's PID namespace. In this scenario, the container will see all the processes on the host system, and its processes will be visible on the host as well.
    - `docker run --pid=container:<name|id> ...`: This allows a container to join the PID namespace of another running container. It allows both containers to see and manage each others' processes.

Demonstration Steps in the Video

Here's a breakdown of what the presenter did to demonstrate PID namespacing, based on the provided link:

1. Run a Basic Container:

    - He started by running a simple Ubuntu container in detached mode:Bash

```sh
docker run -d ubuntu sleep infinity 
``` 

        - `docker run -d`: Runs a container in detached mode (in the background).
        - `ubuntu`: Specifies the Ubuntu image.
        - `sleep infinity`: This is the command that will be executed inside the container. It tells the container to sleep indefinitely, keeping it alive without doing anything resource-intensive.
2. Inspect the Container's Process:

    - He used `docker top <container_id>` to show the processes running inside the container:
        - `docker top`: Lists the processes running in a container.
        - `<container_id>`: The ID or name of the container.
    - The output showed that `sleep infinity` was running as PID 1 inside the container, demonstrating that the container has its own isolated process ID space.
3. Run a Container in the Host's PID Namespace:

    - He then ran another Ubuntu container, but this time shared the host's PID namespace:Bash

```sh
docker run -it --pid=host ubuntu bash
```

- `docker run -it`: Runs a container in interactive mode with a pseudo-TTY.
- `--pid=host`: Crucially, this option tells Docker to use the host's PID namespace for this container.
- `ubuntu`: Specifies the Ubuntu image.
- `bash`: Starts a bash shell inside the container.
1. Observe Processes from Within the Host-PID Container:

    - Inside this new container (which is sharing the host's PID namespace), he ran `ps aux`.
    - The output showed *all* the processes running on the host system, including processes from other containers and the host itself. This clearly demonstrated that when a container shares the host's PID namespace, it loses the PID isolation.
2. Run a Container Sharing Another Container's PID Namespace:

    - Finally, he launched a third container, this time sharing the PID namespace of the first container:Bash

```sh
docker run -it --pid=container:<container_id_of_first_container> ubuntu bash 
``` 

- `--pid=container:<container_id_or_name>`: This instructs the new container to use the same PID namespace as another running container.
1. See Processes from the Shared Container:

- Within the third container, when he executed `ps aux`, the output displayed only the `sleep infinity` process from the initial container and the processes of the current (third) container. The processes of the host are hidden. This demonstrated that both containers are now part of the same, isolated PID namespace.

In essence, the video uses a series of Docker commands to demonstrate how PID namespaces provide isolation, how that isolation can be bypassed by sharing the host's PID namespace, and how containers can be made to share the same PID namespace for inter-container process visibility. Let me know if you would like more detail on any specific part.
