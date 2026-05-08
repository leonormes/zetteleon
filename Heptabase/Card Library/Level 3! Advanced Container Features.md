---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:40+00:00
title: Level 3! Advanced Container Features
---

## Level 3: Advanced Container Features

### Module 1: Security and Capabilities

Theory:

- Linux capabilities
- Seccomp profiles
- AppArmor/SELinux basics

Practical Exercises:

1. Drop capabilities:

```bash
# Start container with limited capabilities
unshare --pid --net --mount-proc cap_drop=all /bin/bash
# Test network operations
ping 8.8.8.8  # Should fail
```

1. Create seccomp profile:

```bash
# Create basic seccomp profile
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {"names": ["read", "write"], "action": "SCMP_ACT_ALLOW"}
  ]
}
```

### Module 2: Container Image Creation

Theory:

- Layer architecture
- Image manifests
- Distribution formats

Practical Projects:

1. Create layered filesystem:

```bash
# Create base layer
mkdir base-layer
# Add application layer
mkdir app-layer
# Create overlay mount
mount -t overlay overlay -o lowerdir=app-layer:base-layer /merged
```
