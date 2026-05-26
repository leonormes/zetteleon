---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-26T11:43:54+00:00
title: Level 1! Container Building Blocks
---

## Level 1: Container Building Blocks

### Module 1: Process Isolation with Namespaces

Theory:

- Understanding Linux namespaces (pid, net, mnt, uts, ipc, user)
- Process isolation principles
- Resource containment basics

Practical Exercises:

1. Create an isolated process:

```bash
# Create a new UTS namespace
unshare --uts /bin/bash
# Verify isolation by changing hostname
hostname container1
# Verify change doesn't affect host
```

1. Explore PID namespace:

```bash
# Create new PID namespace
unshare --pid --fork /bin/bash
# List processes and observe isolation
ps aux
```

### Module 2: Resource Control with Cgroups

Theory:

- Understanding cgroup hierarchy
- Resource limiting mechanisms
- CPU, memory, and I/O control

Practical Exercises:

1. Create and manage cgroups:

```bash
# Create a new cgroup
sudo mkdir /sys/fs/cgroup/memory/mycontainer
# Set memory limit (100MB)
echo 100000000 > /sys/fs/cgroup/memory/mycontainer/memory.limit_in_bytes
# Run process in cgroup
echo $$ > /sys/fs/cgroup/memory/mycontainer/cgroup.procs
```

1. Monitor resource usage:

```bash
# Watch memory usage
cat /sys/fs/cgroup/memory/mycontainer/memory.usage_in_bytes
```
