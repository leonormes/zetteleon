---
aliases: []
confidence: ""
created: 2026-01-07T18:09:12+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:50:02+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: active
tags:
  - containers
  - k8s
  - learning
title: 2026-01-07-1808-HEAD - Learning Kubernetes
type: ""
---

## Learning Project: Kubernetes & Containers

### 4. Operational Checklist

- [ ] **Phase I: Hangar**
    - [x] **Context:** Created HEAD Note.
    - [ ] **Ingest:** Uploaded sources to NotebookLM (or equivalent).
    - [ ] **Charter:** Defined Capstone Project: **Build a Zero-Trust Enterprise Container Platform**.
    - [x] **Syllabus:** Extracted Concepts, Facts, Procedures.
- [ ] **Phase II: Cockpit (Repeat per Session)**
    - [ ] **Hard Start:** Attempted Unit Test first (5m).
    - [ ] **Retreat:** Switched to Drill if stuck (20m).
    - [ ] **Return:** Re-engaged and verified with Hostile Compiler (20m).
    - [ ] **Feynman:** Explained concept aloud (5m).
- [ ] **Phase III: Cryosleep**
    - [ ] **Bridge:** Wrote Save State log.
    - [ ] **Merge:** (Final) Created SoT Note and Archived HEAD.

---

### Phase I: The Hangar

#### 1.1 The Capstone (Boss Fight)

**Goal:** Build a Zero-Trust Enterprise Container Platform.
**Success Criteria:**
1. Demonstrate deep understanding of Linux primitives (Namespaces, Cgroups).
2. Build containers from scratch without Docker.
3. Deploy a secured Kubernetes cluster with Zero-Trust Networking (Calico).
4. Implement enterprise-grade observability and policy enforcement.

#### 1.2 The Syllabus

##### Module A: Linux Containers: From Scratch to Production

**Level 1: Container Building Blocks**
- **Concepts:** Process Isolation, Linux Namespaces (pid, net, mnt, uts, ipc, user), Resource Control (Cgroups).
- **Procedures:**
    - Create isolated process: `unshare --uts /bin/bash`
    - Create new PID namespace: `unshare --pid --fork /bin/bash`
    - Limit memory: `echo 100000000 > /sys/fs/cgroup/memory/mycontainer/memory.limit_in_bytes`

**Level 2: Building Basic Containers**
- **Concepts:** Root filesystem, Mount namespaces, Overlay filesystems, Network namespaces, veth pairs.
- **Procedures:**
    - Create container root fs (bin, lib, proc, sys).
    - Mount proc: `mount -t proc none container-root/proc`
    - Create network namespace: `ip netns add container1`
    - Configure veth pairs: `ip link add veth0 type veth peer name veth1`

**Level 3: Advanced Container Features**
- **Concepts:** Linux capabilities, Seccomp profiles, AppArmor/SELinux, Image Layer architecture.
- **Procedures:**
    - Drop capabilities: `unshare... cap_drop=all`
    - Create seccomp profile.
    - Create layered filesystem with overlay mounts.

**Level 4: Integration Projects**
- **Project 1:** Basic Container Runtime (Namespace isolation + Cgroups + Networking).
- **Project 2:** Container Image Builder (OCI-compatible images).

##### Module B: Kubernetes Mastery

**Level 1: Foundation Builder**
- **Focus:** Basic Concepts (Pods, Deployments, Services).
- **Projects:** Stateless web app, Multi-pod app with services, Health checks.

**Level 2: Service Architect**
- **Focus:** Service Networking, Ingress, Storage, ConfigMaps.
- **Projects:** DB with persistent storage, Ingress controller, Microservices app.

**Level 3: Platform Engineer**
- **Focus:** Scaling, Quotas, StatefulSets, CRDs.
- **Projects:** Distributed database, Custom controllers, Cluster monitoring.

**Level 4: Security Specialist**
- **Focus:** RBAC, Network Policies, Security Contexts.
- **Projects:** Zero-trust networking, Custom admission controllers, Vulnerability scanning.

**Level 5 & 6: System & Enterprise Architect**
- **Focus:** Multi-cluster, Service Mesh, GitOps, Multi-tenancy, Cost optimization.
- **Projects:** Multi-cluster mesh, GitOps pipelines, Multi-tenant platform.

##### Module C: Networking Deep Dive (Calico & Zero Trust)

**Level 1: Linux Networking Fundamentals**
- **Concepts:** Network Namespaces, Veth pairs, Bridges.
- **Project:** "Connect Two Network Namespaces" script.

**Level 2: CNI & Kubernetes Networking Model**
- **Concepts:** CNI Specification, Pod-to-Pod communication, Kube-proxy.
- **Project:** Write basic CNI plugin, Trace packet flows.

**Level 3: Calico Architecture & Basics**
- **Concepts:** Felix, BIRD, IPAM, BGP.
- **Project:** Set up local cluster with Calico, Monitor BIRD/Felix.

**Level 4: Policy Implementation (Zero Trust)**
- **Concepts:** Default Deny, Label-based selectors, Policy precedence.
- **Lab:** "Understanding Calico Policy Basics" (Default Deny, Allow DNS, Allow Web).

---

### Phase II: The Cockpit (Bridge)

#### Current State

- **Status:** Initial Syllabus created.
- **Next Physical Action:** Execute the "Connect Two Network Namespaces" script (Module C, Level 1).

#### Bridge Log

- [] Run `ip netns add ns1` exercise.
