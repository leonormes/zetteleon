---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-26T11:43:55+00:00
title: Build a Container From Scratch! Web Server Project
---

## Build a Container From Scratch: Web Server Project

### Project Overview

We'll create a container that runs a simple Python web server, building everything from scratch using Linux command-line tools. This project will teach you about:

- Process isolation
- Network namespaces
- Filesystem isolation
- Resource limits

### Prerequisites

- Linux system (Ubuntu/Debian recommended)
- Root access
- Basic command line familiarity

### Project Steps

[1. Create Root Filesystem.md](1.%20Create%20Root%20Filesystem.md)

[2. Create Network Namespace.md](2.%20Create%20Network%20Namespace.md)

[3. Create Control Groups.md](3.%20Create%20Control%20Groups.md)

[4. Create Container Launch Script.md](4.%20Create%20Container%20Launch%20Script.md)

[5. Run the Container.md](5.%20Run%20the%20Container.md)

### Learning Exercises

1. Explore Process Isolation

```bash
# Inside container
ps aux
# Compare with host
# On host
ps aux
```

1. Test Memory Limits

```bash
# Create a script to test memory limits
cat > memory_test.py << EOF
x = []
while True:
    x.append(" " * 1000000)
EOF

# Run and observe OOM killer
python3 memory_test.py
```

[Network Exploration.md](Network%20Exploration.md)

[Debugging Tips.md](Debugging%20Tips.md)

### Next Steps

1. Add Features:

   - Implement volume mounting
   - Add port forwarding
   - Create custom network routing
   - Implement resource monitoring

2. Security Improvements:

   - Add capability dropping
   - Implement seccomp profiles
   - Add user namespace mapping
   - Implement resource isolation

3. Advanced Projects:

   - Create multiple connected containers
   - Implement basic orchestration
   - Add logging infrastructure
   - Create container image management

### Troubleshooting Common Issues

1. Permission Denied:

   - Run with sudo
   - Check file permissions
   - Verify user namespace mappings

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
