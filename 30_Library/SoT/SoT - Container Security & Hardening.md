---
aliases:
- Container Security Best Practices
- Hardening Containers
- K8s Security Hardening
created: 2025-12-25 12:30:00+00:00
modified: 2026-07-04 10:51:03+00:00
permalink: llmeon/30-library/so-t/so-t-container-security-hardening
tags:
- kubernetes
- SoftwareEngineering/Architecture
- SoftwareEngineering/Containers
- SoftwareEngineering/Security
title: SoT - Container Security & Hardening
prodos:
  kind: sot
  lifecycle: stable
  review:
    last_reviewed: '2025-12-25'
---


## 1. The Strategy: Defense in Depth

Container security is not a single setting; it is a multi-layered approach that addresses the image, the supply chain, and the runtime.

---

## 2. Pillar 1: Minimizing the Attack Surface

The primary goal is to ensure the container contains _only_ what is necessary for the application to run.

- Minimal Base Images: Use lightweight distributions (e.g., Alpine, Distroless, Flatcar, Bottlerocket). Fewer binaries = fewer exploits.
- Run as Non-Root: Enforce `runAsNonRoot: true` in Kubernetes security contexts. UID 0 inside a container is too close to UID 0 on the host.
- Read-Only Filesystem: Use `readOnlyRootFilesystem: true`. Prevents attackers from writing malware or configuration overrides to the container VFS.
- Drop Linux Capabilities: By default, containers have too many privileges. Start with `drop: ["ALL"]` and selectively add back only what is required (e.g., `NET_BIND_SERVICE`).
- Disable Privilege Escalation: Set `allowPrivilegeEscalation: false` to prevent child processes from gaining more privileges than their parent.

---

## 3. Pillar 2: Software Supply Chain Integrity

Securing the data before it becomes a running process.

- Trusted Sources: Use official, vetted images from private or authenticated repositories.
- Vulnerability Scanning: Integrate tools (e.g., Clair, Trivy, Aqua) into the CI/CD pipeline. Block deployments if critical vulnerabilities are detected.
- Image Signing (Sigstore/Cosign): Sign images during build and verify the signature at deployment time to prevent tampering.
- Promotion Workflow: Images must pass scanning and testing in Lower Environments before being "promoted" to Production.

---

## 4. Pillar 3: Runtime Security & Observation

Protecting the running process within the cluster.

- Pod Security Admission (PSA): Use Kubernetes-native PSA to enforce `Restricted` or `Baseline` security standards across namespaces.
- Network Policies: Implement Zero-Trust at the network layer. Isolate pods and restrict communication to only explicitly allowed paths (Layer 3/4).
- System Call Filtering (Seccomp): Use seccomp profiles to limit the syscalls a container can make to the host kernel.
- Mandatory Access Control (MAC): Employ AppArmor or SELinux to enforce process-level permission boundaries.

---

## 5. Summary Matrix

| Security Layer | Implementation Mechanism | Target Risk |
|:--- |:--- |:--- |
| Image | Minimal Base / Non-Root / RO FS | Local Exploit / Persistent Malware |
| Supply Chain | Scanning / Signing / Promotion | Tampered Data / Vulnerable Deps |
| Runtime | PSA / NetworkPolicy / Seccomp | Lateral Movement / Kernel Escape |
