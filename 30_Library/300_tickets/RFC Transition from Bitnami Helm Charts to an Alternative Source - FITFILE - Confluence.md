---
aliases: []
author:
confidence: 
created: 2025-10-07T00:00:00Z
description:
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
published:
purpose: 
review_interval: 
see_also: []
source: https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2296381442/RFC+Transition+from+Bitnami+Helm+Charts+to+an+Alternative+Source
source_of_truth: []
status: 
tags: []
title: RFC Transition from Bitnami Helm Charts to an Alternative Source - FITFILE - Confluence
type:
uid: 
updated: 
version:
---

## Summary

This document proposes a plan to migrate away from using Bitnami-provided Helm charts. Bitnami has recently introduced a new enterprise pricing model that will result in significant licensing costs (£1000s) for our organization. This RFC outlines our current usage, defines our requirements for a new chart source, evaluates potential alternatives, and recommends a path forward.

## 1. The Problem

We heavily rely on Helm charts for deploying applications and infrastructure components to our Kubernetes clusters. A significant portion of these charts, particularly for critical database and infrastructure services like MongoDB, PostgreSQL, and MinIO, are sourced from the Bitnami repository.

Due to their recent pricing changes, continued use of these charts will incur substantial and unsustainable costs. We must identify and transition to a new, cost-effective, and secure source for these components to avoid service disruption and financial burden.

## 2. Why We Use Bitnami

Our reliance on Bitnami has been based on several key factors:

- **Wide Selection & Quality:** Bitnami offers a comprehensive catalog of pre-packaged charts for popular open-source software. These charts are generally well-maintained, reliable, and follow community best practices.
- **Ease of Use:** Their charts have historically provided a straightforward way to deploy complex applications, integrating well with our automation.
- **Security Reputation:** Bitnami has a reputation for providing frequently updated images and charts, which aligns with our security-conscious approach.
- **Historical Cost:** The charts were previously free, making them an excellent community resource.

## 3. Our Core Requirements for Helm Charts

Based on our established GitOps workflows and security posture, any new source of Helm charts must satisfy the following requirements.

- **Security First:**
  - Charts must come from a reputable and trusted source.
  - Container images must be scannable by our internal tooling, primarily **Trivy**, as seen in the vulnerability scanning steps of our `chart-manager` tool.
  - Images should be patchable using our `copa` integration where possible.
  - Charts must not contain hardcoded secrets and should integrate with our Vault-based secret management.
- **Automation Compatibility:**
  - The charts must be compatible with our `chart-manager` scripts for automated import, analysis, and ingestion into our private Azure Container Registries (`fitfilepublic` and `fitfileregistry`).
  - The structure of the chart must allow for image references to be rewritten to point to our private ACRs during the import process.
- **GitOps & Terraform Integration:**
  - The charts must deploy reliably via our **ArgoCD GitOps** workflow.
  - Versioning must be centrally manageable through our `fitfile-version-manager` Terraform Cloud workspace, which acts as our single source of truth for component versions.
- **Maintainability & Reliability:**
  - Charts must be actively maintained, with a clear history of updates and security patches.
  - They should be well-documented and follow Helm best practices to ensure predictability and ease of maintenance.

## 4. Proposed Alternatives & Evaluation

Here are several potential alternatives to Bitnami, evaluated against our requirements.

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>Option</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Description</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Pros</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Cons</p><figure></figure></div></th></tr></tbody></table>

<table><tbody><tr><th rowspan="1" colspan="1"><div><p>Option</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Description</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Pros</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Cons</p><figure></figure></div></th></tr><tr><td rowspan="1" colspan="1"><p><strong>A: Curated Community Repos</strong></p></td><td rowspan="1" colspan="1"><p>Sourcing charts from official projects or reputable community repositories listed on platforms like <a href="https://artifacthub.io/packages/helm/argo/argocd-apps">Artifact Hub</a>.</p></td><td rowspan="1" colspan="1"><ul><li><p>Cost-effective (usually free).&lt;br&gt;- Wide selection of charts.</p></li></ul></td><td rowspan="1" colspan="1"><ul><li><p>Quality and maintenance can be inconsistent.&lt;br&gt;- Requires thorough vetting for each chart.&lt;br&gt;- Security practices vary by maintainer.</p></li></ul></td></tr><tr><td rowspan="1" colspan="1"><p><strong>B: Official Vendor Charts</strong></p></td><td rowspan="1" colspan="1"><p>Using charts published and maintained directly by the software's creators (e.g., HashiCorp, Jetstack).</p></td><td rowspan="1" colspan="1"><ul><li><p>Highest level of trust and authenticity.&lt;br&gt;- Maintained by the experts on that software.&lt;br&gt;- Timely security updates.</p></li></ul></td><td rowspan="1" colspan="1"><ul><li><p>Not all software we use has an official chart.&lt;br&gt;- Requires managing multiple repository sources.</p></li></ul></td></tr><tr><td rowspan="1" colspan="1"><p><strong>C: Fork and Maintain</strong></p></td><td rowspan="1" colspan="1"><p>Forking the existing Bitnami charts and taking over their maintenance internally.</p></td><td rowspan="1" colspan="1"><ul><li><p>Guaranteed compatibility with our current setup.&lt;br&gt;- Full control over the chart's contents and update cycle.</p></li></ul></td><td rowspan="1" colspan="1"><ul><li><p><strong>High maintenance overhead.</strong> We become responsible for all future updates, dependency changes, and security patches.&lt;br&gt;- Diverts developer time from core product work.</p></li></ul></td></tr><tr><td rowspan="1" colspan="1"><p><strong>D: Build from Scratch</strong></p></td><td rowspan="1" colspan="1"><p>Creating our own Helm charts for these components.</p></td><td rowspan="1" colspan="1"><ul><li><p>Perfectly tailored to our specific needs.&lt;br&gt;- Maximum control.</p></li></ul></td><td rowspan="1" colspan="1"><ul><li><p><strong>Highest maintenance overhead.</strong> Requires deep expertise for complex applications like databases.&lt;br&gt;- Prohibitively time-consuming.</p></li></ul></td></tr></tbody></table>

A "one-size-fits-all" approach is not ideal. I recommend a **hybrid strategy** that prioritizes security and maintainability:

1. **Prioritize Official Vendor Charts (Option B):** For any component that has an official, well-maintained Helm chart (like HashiCorp's charts), we should use it as the default choice.
2. **Vet Community Charts (Option A):** For software without an official chart, we will use [Artifact Hub](https://artifacthub.io/packages/helm/argo/argocd-apps "https://artifacthub.io/packages/helm/argo/argocd-apps") to find the most reputable community-maintained alternative. Each selection must be vetted for maintenance activity, security, and compatibility with our tooling.
3. **Fork as a Last Resort (Option C):** Forking should only be considered if a critical component has no viable official or community alternative. This would require assigning a clear owner responsible for its lifecycle management.

To move forward, I propose the following action plan:

1. **Inventory:** Create a definitive list of all Bitnami charts currently managed by our system. This can be derived from our configuration file located at `helm_chart_deployment/scripts/chart-manager/config/helm_chart_list.yaml`.
2. **Research:** For each chart in the inventory, research and identify a suitable replacement according to the hybrid strategy recommended above.
3. **Update Configuration:** Update the `helm_chart_list.yaml` file with the new repository URLs and chart names.
4. **Test:** Use the `chart-manager` tool to import and test the new charts in a staging environment. Verify that they deploy correctly via ArgoCD and integrate with our existing infrastructure.
5. **Rollout:** Plan a phased rollout to update the production environment once testing is complete.

<table><colgroup><col> <col> <col> <col> <col></colgroup><tbody><tr><th rowspan="1" colspan="1"><div><p><mark>Service</mark></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Alternative Chart/Operator</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Repository URL</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Key Benefits/Features</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Recommendation</p><figure></figure></div></th></tr></tbody></table>

<table><colgroup><col> <col> <col> <col> <col></colgroup><tbody><tr><th rowspan="1" colspan="1"><div><p><mark>Service</mark></p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Alternative Chart/Operator</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Repository URL</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Key Benefits/Features</p><figure></figure></div></th><th rowspan="1" colspan="1"><div><p>Recommendation</p><figure></figure></div></th></tr><tr><td rowspan="1" colspan="1"><p>MongoDB</p></td><td rowspan="1" colspan="1"><p>Percona Operator for MongoDB</p></td><td rowspan="1" colspan="1"><p><a href="https://github.com/percona/percona-server-mongodb-operator">https://github.com/percona/percona-server-mongodb-operator</a></p></td><td rowspan="1" colspan="1"><p>Enterprise-grade features, automated deployments, replica sets &amp; sharding, integrated backups, PMM monitoring, Apache 2.0 license</p></td><td rowspan="1" colspan="1"><p><strong>Recommended</strong></p></td></tr><tr><td rowspan="1" colspan="1"><p>MongoDB</p></td><td rowspan="1" colspan="1"><p>MongoDB Community Operator</p></td><td rowspan="1" colspan="1"><p><a href="https://github.com/mongodb/mongodb-kubernetes-operator">https://github.com/mongodb/mongodb-kubernetes-operator</a></p></td><td rowspan="1" colspan="1"><p>Official MongoDB backing, supports v4.2-7.0, TLS encryption, Prometheus metrics</p></td><td rowspan="1" colspan="1"><p>Alternative (Deprecated - support ends Nov 2025)</p></td></tr><tr><td rowspan="1" colspan="1"><p>MongoDB</p></td><td rowspan="1" colspan="1"><p>KubeDB Operator</p></td><td rowspan="1" colspan="1"><p><a href="https://github.com/kubedb/operator">https://github.com/kubedb/operator</a></p></td><td rowspan="1" colspan="1"><p>Simplified Kubernetes-native deployment, multi-database support</p></td><td rowspan="1" colspan="1"><p>Alternative (Limited free features)</p></td></tr><tr><td rowspan="1" colspan="1"><p>PostgreSQL</p></td><td rowspan="1" colspan="1"><p>CloudNativePG (CNPG)</p></td><td rowspan="1" colspan="1"><p><a href="https://github.com/cloudnative-pg/cloudnative-pg">https://github.com/cloudnative-pg/cloudnative-pg</a></p></td><td rowspan="1" colspan="1"><p>CNCF Sandbox project, pure K8s-native, automated failover, PITR, rolling updates, no external dependencies</p></td><td rowspan="1" colspan="1"><p><strong>Recommended</strong></p></td></tr><tr><td rowspan="1" colspan="1"><p>PostgreSQL</p></td><td rowspan="1" colspan="1"><p>Crunchy Data Postgres Operator (PGO)</p></td><td rowspan="1" colspan="1"><p><a href="https://github.com/CrunchyData/postgres-operator">https://github.com/CrunchyData/postgres-operator</a></p></td><td rowspan="1" colspan="1"><p>Enterprise-grade features, pgBackRest integration, pgBouncer connection pooling, comprehensive monitoring, Apache 2.0 license</p></td><td rowspan="1" colspan="1"><p><strong>Recommended</strong></p></td></tr><tr><td rowspan="1" colspan="1"><p>PostgreSQL</p></td><td rowspan="1" colspan="1"><p>Zalando Postgres Operator</p></td><td rowspan="1" colspan="1"><p><a href="https://github.com/zalando/postgres-operator">https://github.com/zalando/postgres-operator</a></p></td><td rowspan="1" colspan="1"><p>Battle-tested (5+ years production), Patroni-based HA, live volume resizing, in-place major upgrades, MIT license</p></td><td rowspan="1" colspan="1"><p><strong>Recommended</strong></p></td></tr><tr><td rowspan="1" colspan="1"><p>MinIO</p></td><td rowspan="1" colspan="1"><p>Official MinIO Operator + Helm Chart</p></td><td rowspan="1" colspan="1"><p><a href="https://github.com/minio/operator,">https://github.com/minio/operator,</a></p><p><a href="https://charts.min.io/">https://charts.min.io</a></p></td><td rowspan="1" colspan="1"><p>Direct MinIO team maintenance, perfect feature parity, tenant management, official ArgoCD guides</p></td><td rowspan="1" colspan="1"><p><strong>Recommended</strong></p></td></tr><tr><td rowspan="1" colspan="1"><p>MinIO</p></td><td rowspan="1" colspan="1"><p>SeaweedFS</p></td><td rowspan="1" colspan="1"><p><a href="https://github.com/seaweedfs/seaweedfs">https://github.com/seaweedfs/seaweedfs</a></p></td><td rowspan="1" colspan="1"><p>S3-compatible alternative, performance-focused, features removed from free MinIO</p></td><td rowspan="1" colspan="1"><p>Alternative (Requires full migration)</p></td></tr></tbody></table>
