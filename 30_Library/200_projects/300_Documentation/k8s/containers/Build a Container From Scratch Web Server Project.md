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
tags: [containers]
title: Build a Container From Scratch Web Server Project
type: tutorial
uid: 
updated: 
version: 1
---

## Project Overview

We'll create a container that runs a simple Python web server, building everything from scratch using Linux command-line tools. This project will teach you about:

- Process isolation
- Network namespaces
- Filesystem isolation
- Resource limits

## Prerequisites

- Linux system (Ubuntu/Debian recommended)
- Root access
- Basic command line familiarity

## Project Steps

### 1. Create Root Filesystem

```bash
# Create directory structure
mkdir -p container/rootfs
cd container

# Create basic directory structure
mkdir -p rootfs/{bin,lib,lib64,proc,sys}

# Copy basic binaries
cp /bin/bash rootfs/bin/
cp /bin/ls rootfs/bin/
cp /bin/ps rootfs/bin/

# Copy required libraries
# For bash
ldd /bin/bash | grep -o '/lib.\.[0-9]' | xargs -I {} cp --parents {} rootfs/

# Create a simple Python web server
cat > rootfs/server.py << EOF
import http.server
import socketserver

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
EOF

# Copy Python and required libraries
cp $(which python3) rootfs/bin/python3
cp -r /usr/lib/python3 rootfs/usr/lib/
```

### 2. Create Network Namespace

```bash
# Create a new network namespace
ip netns add container_ns

# Create veth pair
ip link add veth0 type veth peer name veth1

# Move veth1 to container namespace
ip link set veth1 netns container_ns

# Configure host side
ip addr add 172.16.0.1/24 dev veth0
ip link set veth0 up

# Configure container side
ip netns exec container_ns ip addr add 172.16.0.2/24 dev veth1
ip netns exec container_ns ip link set veth1 up
ip netns exec container_ns ip link set lo up
```

### 3. Create Control Groups

```bash
# Create memory cgroup
sudo mkdir -p /sys/fs/cgroup/memory/container
echo "50M" | sudo tee /sys/fs/cgroup/memory/container/memory.limit_in_bytes

# Create CPU cgroup
sudo mkdir -p /sys/fs/cgroup/cpu/container
echo "100000" | sudo tee /sys/fs/cgroup/cpu/container/cpu.cfs_quota_us
```

### 4. Create Container Launch Script

```bash
cat > run_container.sh << EOF
#!/bin/bash

# Mount proc and sys
mount -t proc none rootfs/proc
mount -t sysfs none rootfs/sys

# Change root
cd rootfs
exec unshare --pid --net=/var/run/netns/container_ns --mount --uts chroot . /bin/bash
EOF

chmod +x run_container.sh
```

### 5. Run the Container

```bash
# Start the container
sudo ./run_container.sh

# Inside the container, start the web server
python3 server.py &

# From host, test the connection
curl 172.16.0.2:8000
```

## Learning Exercises

1. Explore Process Isolation

```bash
# Inside container
ps aux
# Compare with host
# On host
ps aux
```

2. Test Memory Limits

```python
# Create a script to test memory limits
cat > memory_test.py << EOF
x = []
while True:
    x.append(" "  1000000)
EOF

# Run and observe OOM killer
python3 memory_test.py
```

3. Network Exploration

```bash
# Inside container
ip addr show
ip route show

# On host
ip netns list
ip netns exec container_ns ip addr show
```

## Debugging Tips

### Network Issues

- Check interface status: `ip link show`
- Verify IP addresses: `ip addr show`
- Test connectivity: `ping 172.16.0.1`
- Check routing: `ip route show`

### Resource Limits

- Check memory usage: `cat /sys/fs/cgroup/memory/container/memory.usage_in_bytes`
- Monitor CPU: `cat /sys/fs/cgroup/cpu/container/cpu.stat`

### Process Issues

- Check process tree: `pstree`
- Look for zombie processes: `ps aux | grep Z`
- Check mount points: `mount`

## Next Steps

1. Add Features:
   - Implement volume mounting
   - Add port forwarding
   - Create custom network routing
   - Implement resource monitoring

2. Security Improvements:
   - Add capability dropping
   - Implement seccomp profiles
   - Add [user namespace](User%20Namespace.md) mapping
   - Implement resource isolation

3. Advanced Projects:
   - Create multiple connected containers
   - Implement basic orchestration
   - Add logging infrastructure
   - Create container image management

## Troubleshooting Common Issues

1. Permission Denied:
   - Run with sudo
   - Check file permissions
   - Verify [user namespace](User%20Namespace.md) mappings

2. Network Connectivity:
   - Check interface status
   - Verify IP configuration
   - Check routing tables
   - Verify namespace configuration

3. Resource Limits:
   - Check cgroup mounting
   - Verify limit values
   - Monitor resource usage
   - Check kernel parameters

I've created a hands-on project that will teach you the fundamentals of containers by building one from scratch. This project includes:

1. Creating an isolated root filesystem
2. Setting up network namespaces
3. Implementing resource limits with [cgroups](Cgroups.md)
4. Running a simple Python web server in your container
