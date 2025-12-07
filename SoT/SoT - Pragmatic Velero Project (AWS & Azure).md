---
aliases: []
confidence:
created: 2025-11-13T20:10:22Z
decay-signals: []
epistemic:
last-resonance: 2025-11-13
last-synthesis: 2025-11-13
last_reviewed:
llm-responses: 1
modified: 2025-12-07T18:13:20Z
purpose:
quality-markers: []
resonance-score: 1
review_interval:
see_also: []
source_of_truth: true
status:
supersedes: []
synthesis-count: 1
tags: []
title: SoT - Pragmatic Velero Project (AWS & Azure)
trust-level: developing
type: SoT
uid:
updated:
---

## 1. Working Knowledge (Stable Foundation)

- **Pragmatism First:** Achieve a concrete, simple success on *one* platform first (e.C., AWS). Use defaults (default storage class, provider-supplied IAM policies) to get a functional baseline. This builds momentum and provides a "known good" state.
- **Learning Second:** Use the *second* platform (e.g., Azure) to abstract and deepen knowledge. The act of translating the "known good" AWS setup to Azure forces an understanding of *why* it works, revealing the core concepts (auth, storage, snapshot APIs) versus implementation details.
- **Document Contrast:** The most valuable learning output is documenting the *differences* between the two implementations (e.g., "AWS uses IRSA for auth; Azure uses a Service Principal").

## 2. Current Understanding (Coherent Narrative)

This note outlines a pragmatic project plan for learning Velero for Kubernetes (k8s) backups, specifically targeting both AWS and Azure. The primary challenge is balancing the immediate, practical need ("make backups work") with the long-term learning goal ("understand *how* they work deeply").

The proposed approach is a phased, iterative loop:

1. **Phase 1 (Pragmatism):** Implement the simplest possible use case on Azure.
2. **Phase 2 (Learning):** Implement the *same* use case on AWS, forcing a deep dive into the provider-specific differences in authentication and storage.
3. **Phase 3 (Scaling):** Abstract the common patterns and test more advanced, realistic scenarios (e.g., cross-cluster migration, least-privilege permissions).

## 3. Integration Queue (Structured Input)

### 📤 Integration Source 2025-11-13 (Agent Synthesis)

- **Raw Excerpt/Key Insight:** Need to find the specific Velero plugin documentation for Azure Blob Storage vs. AWS S3.
- **Value Proposition:** The core implementation details for storage backends are currently missing from Layer 3.
- **Conflict Analysis:** None.
- **Suggested Action:** Find documentation links and add to Understanding Layer 3.

### 📤 Integration Source 2025-11-13 (Agent Synthesis)

- **Raw Excerpt/Key Insight:** Need to map out the exact IAM (AWS) and Service Principal (Azure) permissions for least-privilege access.
- **Value Proposition:** The MVU uses overly permissive roles for speed. A production-ready solution (Layer 3) requires a documented, least-privilege alternative.
- **Conflict Analysis:** None.
- **Suggested Action:** Research and add to Understanding Layer 3 as a 'production' alternative.

## 4. Understanding Layers (Progressive Abstraction)

- **Layer 1: Basic Mental Model — The simplest, most durable truth.**
  - Velero backs up k8s cluster resources (the YAML definitions) to a cloud object storage bucket (like S3 or Blob).
  - It can *also* (optionally) trigger snapshots of Persistent Volumes (like EBS or Azure Disks) to back up stateful data.
- **Layer 2: Mechanistic Explanation — How/why Layer 1 works (the process).**
  - Velero runs as a deployment inside the k8s cluster.
  - It uses cloud-provider-specific plugins (e.g., `velero-plugin-for-aws`, `velero-plugin-for-azure`) to communicate with the cloud's native APIs.
  - This communication requires explicit permissions (Auth) to access the object storage and snapshot APIs. This auth mechanism is the most critical and complex part of the setup.
- **Layer 3: Protocol/Detail Level — Lower-level specifics/implementation.**
  - **AWS:** Requires an S3 bucket (for k8s objects) and IAM permissions (to read/write to S3 and create/read EBS snapshots). Authentication is best handled via **IRSA** (IAM Roles for Service Accounts).
  - **Azure:** Requires an Azure Storage Account + Blob Container (for k8s objects) and an Azure **Service Principal (SP)** with permissions (e.g., `Contributor` or a custom role) over the cluster's resource groups to manage snapshots.

## 5. Minimum Viable Understanding (MVU)

- **Established:** 2025-11-13
- **Status:** **DRAFT**
- **Last Confirmed Working:** n/a
- **Bullet list of the absolute minimum required to operate effectively today:**
  - **Goal:** Successfully back up and restore a single 'hello-world' application (e.g., NGINX with a 1Gi PVC) on *one* cloud provider.
  - **Pragmatic Entrypoint (Phase 1: AWS):**
        1. **Cluster:** Have a working EKS cluster.
        2. **Plugin:** Install the `velero-plugin-for-aws`.
        3. **Storage:** Create one S3 bucket.
        4. **Auth (Pragmatic):** Create an IAM Role for Service Accounts (IRSA) using the **AWS-provided default IAM policy** from the Velero documentation (this will be overly permissive, which is acceptable for this *initial* test).
        5. **Install:** Use the `velero install` CLI command, pointing to your bucket and IRSA role.
        6. **Action:** Deploy `hello-world` app. Run `velero backup create aws-test --include-namespaces hello-world`.
        7. **Test:** Delete the `hello-world` namespace. Run `velero restore create --from-backup aws-test`.
        8. **Verify:** Confirm the app and its PVC data are restored.
  - **Learning Loop (Phase 2: Azure):**
        1. Once the AWS test passes, document the *IAM policy* and *IRSA binding*.
        2. Attempt the *exact same test* on an AKS cluster.
        3. Document every difference in the Auth (Service Principal vs. IRSA) and Storage (Blob Container vs. S3 Bucket) setup. **This comparison document is the primary learning objective.**

## 6. Battle Testing and Decay Signals

- **Core Claim(s):**
    1. A "pragmatic-first" (AWS simple case) followed by a "learning-second" (Azure compare/contrast) approach is the optimal balance for this project.
    2. Provider-specific authentication (IAM/SP) is the most complex part of a Velero implementation.
- **Challenges Survived:**
  - *None yet.*
- **Current Status:** **REINFORCED** (This is the initial hypothesis)
- **Decay/Obsolescence Markers:**
  - *None yet.*

## 7. Tensions, Gaps, and Cross-SoT Coherence

- **Tensions:**
  - *Pragmatism vs. Security:* The MVU intentionally uses overly-permissive, default IAM/SP roles for speed. This is a direct tension with a production-ready setup, which demands least-privilege.
  - *Cost vs. Recovery Point:* Snapshotting all PVCs is easy but can be expensive. Learning Velero's label/annotation filtering to selectively back up volumes is a key tension to manage.
- **Confidence Gaps:**
  - *Cost:* Real-world cost implications of frequent snapshots on EBS vs. Azure Disk.
  - *Auth Nuance:* Specific differences between Azure's multiple auth methods (Service Principal vs. Managed Identity) for Velero.
- **Cross-SoT Conflicts:**
  - **Flagged:** [[Kubernetes SoT]] may advocate for GitOps-based recovery (e.g., ArgoCD) over state-based backup (Velero). Need to synthesise *when* to use Velero (for stateful data) vs. *when* to just re-apply GitOps manifests (for stateless apps).

## 8. Sources and Links

- **Related SoTs:**
