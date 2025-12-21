---
aliases: [FitFile Deployment Field Notes]
confidence: 5/5
created: 2025-12-21T12:00:00Z
epistemic: experience
last_reviewed: 2025-12-21
modified: 2025-12-21T12:00:00Z
purpose: To provide a detailed guide of field notes and gotchas for the FitFile deployment process.
review_interval: 3 months
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: true
status: stable
tags: [ff_deploy, field_notes, gotchas]
title: SoT - FitFile Deployment - Field Notes and Gotchas
type: SoT
uid: 
updated: 
version: 1.0
---

## Field Notes & Gotchas (From the Trenches)

This section contains a collection of real-world observations and troubleshooting tips from past deployments.

- **Initial Setup:**
    - When copying an existing deployment (e.g., `hyve-1` to `hyve-2`), meticulously check every reference to the old deployment key and update it. A single forgotten reference (like `vault_namespace`) can cause silent failures.
    - The system may not self-heal if initial settings are wrong. A full destroy and redeploy might be necessary.
- **Terraform Cloud (TFC):**
    - TFC workspaces require environment variables to be set manually. This can be automated as part of the workspace creation process.
    - When adding HCL variables (like `approles`), ensure the formatting is correct. A common mistake is incorrect wrapping of the HCL block.
- **Secrets:**
    - The `Spicedb` pre-shared key must be identical in both the `application` and `spicedb` secret blocks.
    - If you have issues generating a UDE key with `cargo run -- key-gen`, you might need to install a specific nightly version of Rust (e.g., `rustup install nightly-2024-02-04`).
- **Helm/ArgoCD:**
    - A common failure point is the Helm deployment. If it fails, a simple re-run of the apply step might fix it.
    - If you see `no endpoints available for service "ingress-nginx-controller-admission"`, it's an intermittent error. Re-running the apply is the solution.
    - If monitoring tools aren't deployed and Argo shows errors, it's a strong indicator that you've forgotten to add or update the `values.yaml` file for the deployment.
- **AWS Specifics:**
    - When deploying to AWS, you'll need to configure your AWS CLI with `aws configure` and have the necessary IAM permissions.
    - The EKS cluster creation can take a long time.
    - DNS and Auth0 are tightly coupled. The Auth0 configuration depends on the DNS outputs from the EKS Terraform module.
