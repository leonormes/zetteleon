---
aliases: []
confidence: 
created: 2025-07-04T08:30:05Z
epistemic: 
id: updated azure customer checklist
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [documentation, ff-central, project/work/deployment]
title: Updated Azure Customer Checklist
type:
uid: 
updated: 
version:
---

## FITFILE Azure Deployment - Customer Checklist (Updated Version)

### Summary of Tasks (Revised)

To successfully deploy in an Azure tenant, the customer and FITFILE need to collaborate and coordinate closely on the following areas:

#### 0. Pre-Deployment Planning & Coordination (Crucial New Emphasis)

This phase is vital for mitigating risks and avoiding delays, as highlighted by the CUH experience.

- **Formal Sign-off of Technical Prerequisites**: Before any deployment work begins, a detailed technical prerequisite checklist must be completed and formally signed off by both the customer and any involved managed service providers.
- **Establish Naming Conventions**:
  - Request and confirm the customer's official naming convention document (e.g., High-Level Design - HLD).
  - Confirm the required names for *every* Azure resource type to be created, including Resource Groups, Virtual Networks (VNets), Subnets, Route Tables, Network Security Groups (NSGs), and Azure Kubernetes Service (AKS) clusters. Consistency is paramount.
- **Define and Document Network Architecture**:
  - Explicitly confirm and document the expected network routes for all traffic, including detailed plans for traffic flow via on-premises proxies or FortiGates, as misconfigurations can lead to bypassing internal firewalls.
  - Ensure clarity on which subnets (e.g., Jumpbox, System, Workflows) require internet access for specific functionalities like sending logs to Grafana or checking secrets with Vault.
- **Agree on Comprehensive Firewall Rules**:
  - Provide and review a detailed, pre-approved list of all required inbound and outbound firewall rules. This must be presented in a formal proforma document for timely implementation.
  - This includes all specific URLs and IP addresses for FITFILE's central services and external dependencies (refer to Section 5 below for a detailed list).
- **Establish User Access Requirements & Identity Management**:
  - Provide a comprehensive, accurate list of email addresses for all users requiring access to the FITFILE platform, clearly specifying their roles (e.g., CUH operators, FITFILE DevOps engineers, platform users for UI access).
  - Plan and coordinate the integration with the Auth0 tenant for user management and authentication. This includes understanding the process and timelines for fixing the Auth0 email engine and adding users via API calls, potentially from the Jumpbox.
- **Clarify Database Connectivity**:
  - Obtain specific MS SQL Server connection settings for applications like 'Bunny' and for the FITFILE system to access OMOP data sources.
  - Crucially, secure formal governance and security sign-off for any on-premise database access.
- **Define Application Access URLs**:
  - Confirm required domain names that CUH will expose for the FITFILE APIs and UI (e.g., `app.privatelink.fitfile.net` for frontend, `argocd.privatelink.fitfile.net` for development monitoring). These need to be resolvable from the CUH network.
- **Confirm Monitoring Requirements**:
  - Agree on the comprehensive monitoring strategy, including specific metrics, logging, and tracing requirements, and how these will integrate with tools like Grafana, Prometheus, and Loki.

##### 1. Azure Tenant & Subscription Setup

These foundational steps ensure the Azure environment is correctly provisioned for FITFILE.

- **Share Customer’s Azure Tenant ID with FITFILE**.
- **Share Azure Subscription ID** of the tenant with FITFILE.
- **Register the use of necessary Resource Providers** in the Azure Subscription. This includes `Microsoft.Compute` and `Microsoft.ContainerService` for AKS.
- **Create a Service Principal with Contributor access** to the Subscription for FITFILE's Terraform deployments. The application ID (ARM_CLIENT_ID) and secret (ARM_ACCESS_KEY) of this service principal are required.
- **Enable Encryption at Host on the Subscription**.
- **Ensure Correct Compute Quota is Registered** in the Azure Subscription. This is especially important for memory-optimized VM series like Esv5, which may not be in the default quota for a new subscription.
- **Add a FITFILE DevOps User to the Customer’s Azure Tenant**. This user should be invited as an external user, changed from 'Guest' to 'Member', and assigned 'Contributor' role on the subscription for FITFILE deployment and access.

##### 2. Network & Security Configuration (Detailed Implementation)

Based on CUH's experience, thorough and accurate network configuration is critical.

- **Implement Outbound Firewall Rules (Allow List)**: Configure the firewall to permit outbound traffic to:
  - **FITFILE Central Services:**
    - Hashicorp Vault: `https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/`.
    - Auth0 tenant: `https://fitfile-prod.eu.auth0.com`.
    - Grafana (Prometheus): `https://prometheus-prod-05-gb-south-0.grafana.net`.
    - Grafana (Loki): `https://logs-prod-008.grafana.net`.
    - Grafana (Tempo): `https://tempo-prod-06-prod-gb-south-0.grafana.net`.
    - GitLab: `https://gitlab.com`.
    - Azure Container Registry: `fitfileregistry.azurecr.io`.
    - Hashicorp releases: `releases.hashicorp.com` (Port 80, 443 HTTP/HTTPS).
    - Terraform registry: `registry.terraform.io` (Port 80, 443 HTTP/HTTPS).
  - **Microsoft Azure Endpoints (Essential for AKS Operations)**:
    - Microsoft Container Registry: `mcr.microsoft.com` (Port 443 - HTTPS).
    - Microsoft Container Registry CDN: `*.cdn.mscr.io` (Port 443 - HTTPS).
    - Azure Storage Blobs: `*.blob.core.windows.net` (Port 443 - HTTPS).
    - Certificate Revocation Lists: `mscrl.microsoft.com` and `crl.microsoft.com` (Port 443 - HTTPS).
    - Azure Active Directory Authentication: `login.microsoftonline.com` (Port 443 - HTTPS).
    - Azure Resource Manager: `management.azure.com` (Port 443 - HTTPS).
  - **AKS-Specific Endpoints**:
    - AKS Managed Control Plane: `*.hcp.<region>.azmk8s.io` and `*.azmk8s.io` (Port 443).
    - AKS Tunnelfront Pod: `*.tun.<region>.azmk8s.io` (Port 9000 or 443).
    - AKS Data Plane: `*.dp.<region>.azmk8s.io` (Port 443).
  - **Operating System Endpoints**:
    - For Ubuntu nodes: `changelogs.ubuntu.com`, `security.ubuntu.com`, `azure.archive.ubuntu.com`.
    - For Azure Linux nodes: `packages.microsoft.com`.
    - Network Time Synchronization: `ntp.ubuntu.com` (Port 123).
  - **Scope:** Ensure these firewall rules apply to all relevant subnets requiring internet access, specifically the Jumpbox, System, and Workflows subnets.
- **Implement Inbound Firewall Rules (Allow List)**: Configure inbound rules to allow callback responses from the Auth0 service. The specific IP addresses provided by Auth0 (e.g., `52.28.184.187`, `52.30.153.34`, etc.) must be added.
- **Configure Private DNS & Forward Lookup**:
  - Confirm that FITFILE will deploy a private DNS zone (e.g., `privatelink.fitfile.net`) within the FITFILE subscription.
  - Ensure a conditional forwarder is set up on the customer's (CUH's) on-premises DNS server. This forwarder should resolve the `privatelink.fitfile.net` domain to the Azure Private DNS Resolver's inbound endpoint IP address (e.g., `10.250.16.52`).
  - Verify that DNS records for the FITFILE application (`app.privatelink.fitfile.net`) and ArgoCD (`argocd.privatelink.fitfile.net`) are created and are resolvable from the CUH network.
- **Establish Network Peering**: Confirm that peering is correctly configured and functional between the FitFile vNet and the CUH ExpressRoute/Shared Services vNet. The CUH deployment experienced issues with peering not being set up initially.
- **Implement Route Tables**: Ensure route tables are configured to correctly force outbound traffic via the on-premises proxy/FortiGate where required, not directly out via Azure Gateway.
- **Configure Internet Proxy Details**: Be aware that it might be necessary to configure internet proxy details *inside* the FITFILE VMs to ensure all egress traffic follows the intended on-premises route. This was a learning from the CUH deployment and requires a change process.

##### 3. Infrastructure & Platform Deployment (FITFILE Team Responsibility, Customer Awareness)

While primarily FITFILE's responsibility, customer teams should be aware of these aspects for collaboration and support.

- **Terraform Cloud Setup**:
  - Customer should be aware of Terraform Cloud for workspace creation and CI/CD setup.
  - This includes the secure handling of sensitive environment variables for Azure Resource Manager (ARM) keys (e.g., `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` for AWS, or client ID/secret for Azure).
- **GitLab Repository Setup**: Customer should be aware of the GitLab repository used to isolate and manage customer-specific deployment configurations.
- **Configure Platform Variables**: Customer should be aware of the configuration of Helm value overrides in the deployment repository (e.g., `ffnodes/<customer>/<deployment-key>/values.yaml`). This includes critical variables like `approles`, `admin_password`, `argocd_host`, and `defaultOrganisationAdminUserId`.
- **Identity & Access Management (Further Details)**:
  - **Auth0 Integration**: Ensure the `user_id` for the default organization administrator is correctly set in the application configuration.
  - **Secrets Management**: Confirm that the correct client IDs and secrets obtained from Auth0 are securely added to Vault for application access.
  - **User Provisioning**: Be aware of the process for adding new users via API calls, potentially from the Jumpbox, as manual processes were a bottleneck in CUH.
  - **Internal Access Control (SpiceDB)**: Set up `project_data_partner` and `project_host` relationships in SpiceDB for proper inter-node communication and project access.
  - **MongoDB Configuration**: Add Tenants and Connections documents directly to the MongoDB configuration of the host node for frontend Query Builder and data retrieval, potentially requiring port-forwarding to the MongoDB pod.
  - **HIE Tenant**: Ensure the HIE tenant is manually added to the project in CUH SpiceDB.
  - **OMOP Data Source**: The OMOP data source needs to be added to the project, possibly via an API call.
  - **HIE Node Configuration**: The `fitConnectHosts` deployment config list of the HIE node needs to be configured with the CUH-exposed domain names for FITFILE APIs.
- **Monitoring & Observability Integration**: Configure Grafana integration for collecting Prometheus metrics, Loki logs, and Tempo traces by securely setting up host and credential values in Vault.
- **Security Best Practices (Ongoing)**:
  - **Azure Backup**: Enable Azure Backup with a policy for daily backups of configurations and query plans. The customer (CUH) needs to understand their ongoing responsibility for managing these backups and conducting regular restore tests (at least monthly) to verify data integrity and procedure correctness. Velero is a recommended tool for backing up cluster state and persistent data.
  - **Microsoft Defender for Cloud**: Enable Microsoft Defender for Cloud (formerly Azure Security Center) for continuous security assessment, benchmarks, and recommendations. The customer (CUH) is responsible for regularly reviewing its status and secure score and addressing any identified issues.
  - **Azure Policy**: Ensure that existing Azure policies within the customer's environment apply correctly to the new FITFILE subscription to maintain consistency and compliance.
  - **Vulnerability Management**: Implement vulnerability scanning in the CI/CD pipeline for container images to detect flaws early. Regularly update base images and application runtimes.
  - **Kubernetes Updates**: Ensure a strategy is in place for frequent upgrades of Kubernetes services to non-vulnerable versions, as new features and security fixes are released regularly.
  - **Declarative Management**: Reinforce the practice of managing Kubernetes resources declaratively using YAML manifests or Helm charts stored in version control, rather than imperative commands, to maintain a single source of truth. Use `kubectl diff` to review changes before applying them to production clusters.
  - **Probes**: Utilize readiness and liveness probes to inform Kubernetes when an application is ready to handle requests or needs to be restarted.
  - **Helm Hooks for Migrations**: For stateful applications, consider implementing Helm lifecycle hooks (e.g., pre-upgrade, pre-rollback) to manage database migrations or backup/restore operations during updates or rollbacks.

##### 4. Application Deployment (FITFILE Team Responsibility, Customer Awareness)

These steps describe the final deployment of FITFILE's applications.

- **Triggering GitOps Flow**: Understand that changes to the application configuration within the designated GitLab repository will automatically trigger the GitOps deployment pipeline.
- **Deployment Strategy Awareness**: Be aware of advanced deployment strategies such as Rolling Updates (default, zero-downtime, but old and new versions coexist), Blue/Green Deployments (separate environments for old/new versions), and Canary Deployments (gradual rollout to a subset of users).
- **Handling Database Migrations**: Explicitly acknowledge the need for specific migration tasks for stateful applications (e.g., `rake db:migrate` for Rails apps) that must run at a particular point in the rollout process, usually before new pods start.
