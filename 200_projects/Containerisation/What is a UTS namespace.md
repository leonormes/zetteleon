---
aliases: []
confidence: 
created: 2025-10-24T15:28:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, hostname, isolation, linux, namespace, type/fact]
title: What is a UTS namespace
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a PID namespace]], [[What is a mount namespace]], [[What is a network namespace]]

## Summary

A UTS (Unix Time Sharing) namespace isolates system identifiers—specifically the hostname and NIS domain name—allowing each container to have its own hostname independent of the host and other containers.

## Context / Problem

On a standard Linux system:

- There is one global hostname (e.g., `myhost.example.com`)
- All processes see the same hostname via `hostname` command or `/etc/hostname`
- Changing hostname affects the entire system

Containers need isolated hostnames so:

- Each container can identify itself uniquely (e.g., `web-server-1`, `db-replica-2`)
- Application logs show container-specific hostnames
- Network services bind to correct hostname
- Kubernetes sets Pod hostname to Pod name

## Mechanism / Details

### What Is It

A UTS namespace provides:

- **Isolated hostname**: Each namespace can set its own hostname
- **Isolated NIS domain name**: For legacy NIS (Network Information Service)
- **System identity**: Processes see their namespace's hostname, not host's

**UTS = Unix Time Sharing** (historical name from Unix timesharing systems)

### Creating a UTS Namespace

```bash
# Check current hostname
hostname
# Output: host.example.com

# Create new UTS namespace
unshare --uts /bin/bash

# Inside namespace, set new hostname
hostname container-1

# Verify
hostname
# Output: container-1

# Exit namespace
exit

# Back on host:
hostname
# Output: host.example.com (unchanged!)
```

### UTS Namespace Isolation

```sh
Host
  ├─ Hostname: host.example.com
  │
  ├─ Container A (UTS namespace 1)
  │   └─ Hostname: web-server-1
  │
  └─ Container B (UTS namespace 2)
      └─ Hostname: db-replica-2
```

**Each namespace maintains**:

- `struct uts_namespace` in kernel
- Contains `nodename` (hostname) and `domainname` (NIS domain)

### System Calls and Files

**System calls**:

```c
// Set hostname (requires CAP_SYS_ADMIN in namespace)
sethostname("container-1", 11);

// Get hostname
gethostname(buffer, sizeof(buffer));
```

**Files** (modified by namespace):

- `/proc/sys/kernel/hostname` - Shows namespace's hostname
- **NOT** `/etc/hostname` - This is a file, not affected by UTS namespace!

**Important**: `/etc/hostname` file is shared unless you use a **mount namespace**.

### UTS Without Mount Namespace (Security Risk)

From the original note, if you create **UTS namespace WITHOUT mount namespace**:

- Hostname is isolated (`hostname` command works)
- But `/etc/hostname` file is **shared**
- Container can **modify host's `/etc/hostname` file**
- On next boot, host uses container's hostname!

**Example Security Issue**:

```bash
# In container with UTS but no mount namespace:
echo "malicious-hostname" > /etc/hostname
# This affects HOST on next reboot!
```

**Solution**: Always combine UTS with mount namespace, or mount `/etc` read-only.

## Connections / Implications

### What This Enables

- **Container identity**: Each container has a unique hostname for logging
- **Application compatibility**: Apps that depend on hostname work correctly
- **Kubernetes Pod naming**: Pod hostname matches Pod name
- **Service discovery**: Hostname used in network protocols (SMTP, Kerberos)

### What Breaks If This Fails

- **Hostname confusion**: All containers see host hostname
- **Log aggregation issues**: Cannot distinguish log sources by hostname
- **License checks fail**: Software locked to specific hostname
- **Security**: set-UID binaries may behave unexpectedly with crafted hostnames

### Security Consideration from Original Note

**Risk**: Set-user-ID (setuid) applications can be vulnerable:

- Attacker creates UTS namespace with malicious hostname
- Runs setuid application (e.g., `/usr/bin/passwd`)
- Application reads hostname, uses it in file paths
- Attacker can overwrite critical files or bypass restrictions

**Example**:

```bash
# Attacker crafts hostname with path traversal
unshare --uts /bin/bash
hostname "../../etc/shadow"

# Setuid app writes to file based on hostname
# May overwrite /etc/shadow!
```

**Mitigation**: Modern kernels restrict hostname characters, but always validate inputs.

### How It Maps to Kubernetes

**Kubernetes sets Pod hostname to Pod name:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server-1
spec:
  hostname: web-server-1  # Optional: defaults to metadata.name
  subdomain: my-service   # Optional: for FQDN
  containers:
  - name: nginx
    image: nginx
```

**Inside Pod**:

```bash
hostname
# Output: web-server-1

hostname -f
# Output: web-server-1.my-service.default.svc.cluster.local
```

**Behind the scenes**:

```bash
# kubelet creates UTS namespace and sets hostname:
unshare --uts /bin/bash
hostname web-server-1

# Also updates /etc/hostname in container's mount namespace:
echo "web-server-1" > /etc/hostname
```

### Kubernetes Hostname Vs Subdomain

- **hostname**: Short name (e.g., `web-server-1`)
- **subdomain**: Enables FQDN (e.g., `web-server-1.my-service.default.svc.cluster.local`)

**Use case**: StatefulSets use subdomain for stable network identity:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 3
  template:
    spec:
      hostname: web  # Each Pod: web-0, web-1, web-2
```

Pods get hostnames:

- `web-0.nginx.default.svc.cluster.local`
- `web-1.nginx.default.svc.cluster.local`
- `web-2.nginx.default.svc.cluster.local`

### Real-World Inspection

```bash
# List UTS namespaces
ls -l /proc/*/ns/uts

# Compare two processes' UTS namespaces
readlink /proc/1000/ns/uts
readlink /proc/2000/ns/uts
# Same inode = same namespace

# Check hostname in a namespace
nsenter --uts=/proc/2000/ns/uts hostname

# Run command in new UTS namespace
unshare --uts hostname container-temp
```

### Common Use Cases

**1. Multi-tenant environments**:

- Each tenant's container has unique hostname
- Logs clearly show which tenant generated events

**2. Microservices**:

- Service instances have distinct hostnames (`api-server-1`, `api-server-2`)
- Distributed tracing correlates requests by hostname

**3. Testing**:

- Simulate different hosts on single machine
- Test hostname-dependent configuration

## Questions / To Explore

- How does Docker set container hostname?
- What is NIS domain name and is it still used?
- How does Kubernetes generate FQDN for Pods?
- DEBUG - Container hostname conflicts with host
- How do StatefulSets use hostnames for stable identity?
- What are valid characters for Linux hostnames?
- How does /etc/hosts interact with UTS namespace?
