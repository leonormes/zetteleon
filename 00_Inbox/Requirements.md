---
aliases: []
tags: []
title: User Requirements & Specifications
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-28T09:55:37+00:00
modified: 2025-12-28T18:49:36+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# User Requirements & Specifications

## 1. Functional Requirements

### 1.1. Chart Configuration Management ("The Ledger")

- **FR-01**: The system MUST accept a single declarative configuration file (`config.yaml`) defining all managed charts.
- **FR-02**: The system MUST support multiple deployment types (Terraform, ArgoCD) within the configuration.
- **FR-03**: The system MUST normalize legacy configuration structures into a unified `Chart` model during loading.

### 1.2. Image Internalization (Import)

- **FR-04**: The system MUST support two import modes:
    - **Azure CLI Mode**: Direct ACR-to-ACR import using `az acr import` (Preferred).
    - **Docker Mode**: Fallback using local Docker daemon (`pull` -> `tag` -> `push`).
- **FR-05**: The system MUST automatically detect if a chart is from **Bitnami** and handle specific registry redirection logic (due to Docker Hub rate limits and location changes).
- **FR-06**: The system MUST support "Standalone Images" (images not part of a chart but required by the system) defined in the config.

### 1.3. Chart Modification

- **FR-07**: The system MUST parse local Helm charts to identify image references in `values.yaml`.
- **FR-08**: The system MUST **modify `values.yaml` in-place** to replace upstream registry URLs with the private ACR URL.
- **FR-09**: The system MUST create a backup of `values.yaml` before modification.
- **FR-10**: The system MUST revert changes from the backup if the operation fails (Atomic File Operation).

### 1.4. Architecture Validation

- **FR-11**: The system MUST validate that all images referenced by a chart support a specific CPU architecture (default: `linux/amd64`).
- **FR-12**: The system MUST allow users to specify a strict mode that fails operation if an incompatible image is found.
- **FR-13**: The system MUST be able to discover alternative image tags that support the required architecture if the default one does not.

### 1.5. Analysis & Reporting

- **FR-14**: The system MUST provide an `analyze` command to list all images used by a chart without performing changes.
- **FR-15**: The system MUST support outputting validation results in JSON and Table formats.

## 2. Non-Functional Requirements

### 2.1. Reliability & Safety

- **NFR-01 (Statelessness)**: The application MUST NOT maintain any persistent state database. Restarting the process MUST be safe.
- **NFR-02 (Idempotency)**: Running the import command multiple times on the same configuration MUST result in the same consistent state without side effects (e.g., duplicated tags).
- **NFR-03 (Backup)**: User data (local `values.yaml` files) MUST never be permanently corrupted. Backups are mandatory before writes.

### 2.2. Usability

- **NFR-04 (CLI UX)**: The CLI MUST provide standard flags (`--dry-run`, `--verbose`) for all mutative commands.
- **NFR-05 (Feedback)**: Long-running operations (image uploads) MUST provide visual feedback or logging to indicate liveness.

### 2.3. Performance

- **NFR-06**: Azure CLI mode SHOULD be the default to avoid network bandwidth costs of pulling images to the local machine.

## 3. System Constraints

- **C-01**: The system MUST verify the presence of external dependencies: `helm`, `docker`, and `az` (Azure CLI).
- **C-02**: The system is designed for **Azure Container Registry (ACR)** as the target.
- **C-03**: The system targets **Helm v3** charts.
