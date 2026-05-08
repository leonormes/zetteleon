---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:40+00:00
title: Level 2! Building Basic Containers
---

## Level 2: Building Basic Containers

### Module 1: File System Isolation

Theory:

- Root filesystem concepts
- Mount namespaces
- Overlay filesystems

Practical Exercises:

1. Create container root filesystem:

```bash
# Create minimal root filesystem
mkdir container-root
cd container-root
mkdir bin lib proc sys
# Copy basic binaries
cp /bin/bash bin/
# Copy required libraries
ldd /bin/bash | grep -o '/lib.\.[0-9]' | xargs -I {} cp {} lib/
```

1. Mount proc filesystem:

```bash
# Mount proc in container
mount -t proc none container-root/proc
```

### Module 2: Network Isolation

Theory:

- Network namespaces
- Virtual interfaces
- Container networking models

Practical Exercises:

1. Create network namespace:

```bash
# Create namespace
ip netns add container1
# Create veth pair
ip link add veth0 type veth peer name veth1
# Move one end to namespace
ip link set veth1 netns container1
```

1. Configure networking:

```bash
# Configure IP addresses
ip addr add 172.16.0.1/24 dev veth0
ip netns exec container1 ip addr add 172.16.0.2/24 dev veth1
# Enable interfaces
ip link set veth0 up
ip netns exec container1 ip link set veth1 up
```
