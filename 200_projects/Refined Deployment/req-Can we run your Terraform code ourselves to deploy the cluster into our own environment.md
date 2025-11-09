---
aliases: []
confidence: 
created: 2025-06-20T05:43:32Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: req-Can we run your Terraform code ourselves to deploy the cluster into our own environment
type:
uid: 
updated: 
version:
---

## 1. FAQ Page

| FAQ ID & The Question                                                                             |
| ------------------------------------------------------------------------------------------------- |
| FAQ-201: Can we run your Terraform code ourselves to deploy the cluster into our own environment? |

Category: Security & Deployment

Standard Answer:

We appreciate the desire for control over your environment; however, to ensure the highest levels of security and operational integrity, we do not permit clients to run our Terraform code directly. Our deployment process is managed exclusively through our secure, automated GitOps pipeline.

This approach ensures that every change to the infrastructure is version-controlled, peer-reviewed, and subjected to a suite of automated security and compliance checks before being deployed. This centralised management guarantees that your environment is provisioned correctly, remains secure against misconfigurations, and maintains a complete, auditable history of all changes, which is crucial for handling sensitive data. Handing over the Terraform code would bypass these critical safety measures, and we would no longer be able to guarantee the security or stability of the deployment.

Key Links:

Related Features: [[3.1.1 Managed IaC Deployment]], [[3.1.2 GitOps Change Management]], [[3.2.1 Automated Security Scanning]]

Underlying Requirements: [[REQ-101 Secure Deployment Process]], [[REQ-102 Auditable Infrastructure Changes]], [[REQ-103 Prevention of Configuration Drift]]

## 2. Requirements Page

### Summary of Requirements

| Requirement ID | Title                                 | Type           | Source                |
| :------------- | :------------------------------------ | :------------- | :-------------------- |
| REQ-101        | Secure Deployment Process             | Security       | Internal Policy       |
| REQ-102        | Auditable Infrastructure Changes      | Non-Functional | Security Constraint   |
| REQ-103        | Prevention of Configuration Drift     | Non-Functional | Operational Stability |
| REQ-104        | Centralised Infrastructure Management | Functional     | Client Request        |

---

### Requirement Details

Requirement ID & Title: REQ-101 Secure Deployment Process

Source: Internal Policy

Type: Security

Description: The process for deploying and managing client environments must be fundamentally secure, protecting against unauthorised changes, vulnerabilities, and misconfigurations. All deployments must pass through automated security validation before being applied.

Key Links:

Satisfied by Feature(s): [[3.1.1 Managed IaC Deployment]], [[3.2.1 Automated Security Scanning]]

Requirement ID & Title: REQ-102 Auditable Infrastructure Changes

Source: Security Constraint

Type: Non-Functional

Description: Every modification to the production infrastructure must be tracked and logged in an immutable manner. There must be a clear record of who proposed a change, who approved it, and precisely what was altered. This is essential for compliance and forensic analysis.

Key Links:

Satisfied by Feature(s): [[3.1.2 GitOps Change Management]]

Requirement ID & Title: REQ-103 Prevention of Configuration Drift

Source: Operational Stability

Type: Non-Functional

Description: The system must ensure that the deployed infrastructure configuration continuously matches the authorised configuration defined in the source code repository. Any manual or unauthorised changes (drift) should be prevented or automatically remediated.

Key Links:

     Satisfied by Feature(s): [[3.1.1 Managed IaC Deployment]], [[3.1.2 GitOps Change Management]]

Requirement ID & Title: REQ-104 Centralised Infrastructure Management

Source: Client Request (Interpreted from FAQ-201)

Type: Functional

Description: To maintain security and quality guarantees, all infrastructure provisioning and updates must be managed from a central, controlled system rather than being executed from individual or client-side machines.

Key Links:

     Satisfied by Feature(s): [[3.1.1 Managed IaC Deployment]]

## 3. Feature Page

### 3.1.1 Managed IaC Deployment

| Property      | Value        |
| :------------ | :----------- |
| ID            | 3.1.1        |
| Status        | Live         |
| Owner         | DevOps Team  |
| Last Reviewed | 18 June 2025 |

Brief Description:

A managed service that uses Terraform Cloud to deploy and maintain client cluster environments via a secure, automated pipeline.

Purpose & User Value:

This feature ensures that client environments are provisioned consistently, reliably, and securely without requiring manual intervention from the client. It provides peace of mind that the infrastructure is built according to our validated best practices and that its state is actively managed.

Functional Details:

All infrastructure is defined as code (IaC) using Terraform.

Deployment is executed from a centralised, secure platform (Terraform Cloud).

Client-specific variables and secrets are managed securely within the platform's environment controls.

The system maintains the state of the infrastructure, preventing drift and ensuring consistency across updates.

Privacy & Security Considerations:

Access to the deployment environment is strictly controlled via role-based access control (RBAC).

Credentials for client environments are vaulted and only accessible by the automated pipeline at runtime.

The state file, which may contain sensitive information, is encrypted at rest and in transit.

Links to Collateral:

Addresses Requirements: [[REQ-101 Secure Deployment Process]], [[REQ-103 Prevention of Configuration Drift]], [[REQ-104 Centralised Infrastructure Management]]

Relevant FAQs: [[FAQ-201 Can we run your Terraform code ourselves?]]

Jira Tasks: DEVOPS-411, SEC-209

---

### 3.1.2 GitOps Change Management

| Property      | Value        |
| :------------ | :----------- |
| ID            | 3.1.2        |
| Status        | Live         |
| Owner         | DevOps Team  |
| Last Reviewed | 18 June 2025 |

Brief Description:

An operational framework where the Git repository is the single source of truth for all infrastructure changes, which are applied automatically following a defined approval workflow.

Purpose & User Value:

This feature provides a transparent and fully auditable trail for every change made to the infrastructure. By enforcing a peer-review process (via Pull Requests), it enhances quality and collaboration while reducing the risk of erroneous or malicious changes reaching the production environment.

Functional Details:

Any proposed change to the infrastructure must be submitted as a Pull Request (PR) in the designated Git repository.

PRs require at least one approval from a designated code owner.

Upon merging the PR, an automated pipeline is triggered, which plans and applies the Terraform changes.

The Git history serves as a complete, immutable log of all infrastructure modifications.

Privacy & Security Considerations:

Branch protection rules are enforced to prevent direct commits to the main branch.

The PR approval process ensures that changes are scrutinised for security implications before they are merged.

Links to Collateral:

Addresses Requirements: [[REQ-102 Auditable Infrastructure Changes]], [[REQ-103 Prevention of Configuration Drift]]

Relevant FAQs: [[FAQ-201 Can we run your Terraform code ourselves?]]

Jira Tasks: DEVOPS-415

---

### 3.2.1 Automated Security Scanning

| Property      | Value         |
| :------------ | :------------ |
| ID            | 3.2.1         |
| Status        | Live          |
| Owner         | Security Team |
| Last Reviewed | 18 June 2025  |

Brief Description:

Automated security pipelines that scan Infrastructure as Code (IaC) for vulnerabilities, compliance issues, and misconfigurations.

Purpose & User Value:

This feature acts as a preventative control, catching potential security issues before they are deployed. This proactively hardens the client's environment and reduces the risk of security breaches caused by infrastructure misconfigurations.

Functional Details:

As part of the PR workflow, automated tools (e.g., Checkov, tfsec) scan the Terraform code.

The pipeline will fail if any critical or high-severity vulnerabilities are detected, blocking the PR from being merged.

Checks are performed against industry benchmarks (e.g., CIS Benchmarks) and our internal security policies.

Privacy & Security Considerations:

Scans are configured to detect insecure configurations such as public S3 buckets, overly permissive firewall rules, or a lack of encryption.

The scan results are posted directly in the PR for review by the developer and approvers.

Links to Collateral:

Addresses Requirements: [[REQ-101 Secure Deployment Process]]

Relevant FAQs: [[FAQ-201 Can we run your Terraform code ourselves?]]

Jira Tasks: SEC-188, DEVOPS-420
