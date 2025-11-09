---
aliases: []
confidence: 
created: 2025-07-01T05:44:33Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [azure, documentation, prerequisites, project/work/deployment, setup]
title: Prerequisities
type:
uid: 
updated: 
version:
---

The source materials provide a comprehensive overview of the prerequisites required for an Azure deployment, highlighting both the technical steps and the critical coordination needed between FITFILE and the customer (e.g., CUH, Telefonica Tech).

Here's a detailed breakdown of the prerequisites:

## 1. Workstation and Local Setup Prerequisites

Before beginning the deployment, the individual performing the deployment needs to ensure their local workstation is properly configured.

- Software Installation: You must have specific software installed on your workstation:
- `tfenv` and `terraform` with the correct version.
- `azure-cli`.
- `last-pass` for password management.
- Directory Setup: You need to create a directory for the deployment.
- Repository Cloning: Several key repositories must be cloned to your local machine:
- FITFILE development (or `fitfile-production` for a production deployment).
- UDE CLI.
- Central Services.
- Deployment Key Generation: A unique identifier for the deployment, called a `deployment-key`, must be generated.
- This is done by running a script named `short_name.sh` located in the `Central Services` repository.
- The script will ask for the full name of the customer and the deployment environment (e.g., Dev, Prod) to return a shortname.
- You might need to change the script's permissions using `chmod +x ./short_name.sh` before running it.
- The generated key needs to be saved in a database. This `deployment-key` will be used consistently across the infrastructure.

## 2. Azure Tenant and Subscription Configuration (Customer Side)

These are crucial prerequisites that often require close liaison between FITFILE and the customer's IT team. Lessons learned from past deployments emphasize the importance of having these details ironed out *before* starting any Terraform work.

- Azure Tenant and Subscription IDs: The customer needs to share their Azure Tenant ID and Azure Subscription ID with FITFILE.
- Resource Provider Registration: The Azure Subscription must have specific Resource Providers registered. These are necessary for deploying various Azure services. The required providers include:
- `Microsoft.ContainerService` (for Kubernetes Service).
- `Microsoft.ManagedIdentity` (for Kubernetes managed identities).
- `Microsoft.Network` (for networking infrastructure).
- `Microsoft.Storage` (for storage accounts).
- `Microsoft.Compute` (for virtual machines).
- If a resource provider is not registered, `terraform apply` will fail with an error like "The Resource Provider was not registered". The solution involves running `az provider register --namespace "Some.ResourceProvider"`.
- Service Principal Creation and Permissions: A service principal must be created in the Azure tenant for FITFILE's Terraform Cloud Provisioner.
- It should be named something like "FITFILE Terraform Cloud Provisioner".
- The `secret id`, `value` of the secret, and the `Application (client) ID` need to be copied. These become the `ARM_ACCESS_KEY`, `ARM_CLIENT_SECRET`, and `ARM_CLIENT_ID` environment variables in Terraform Cloud.
- This service principal requires `Contributor` access to the subscription.
- Additionally, it needs the `User Access Administrator` role with a condition to assign the `Network Contributor` role, specifically to allow the AKS cluster identity to assign roles.
- Enable Encryption at Host: The subscription needs to have `EncryptionAtHost` enabled. This can take up to 20 minutes to register. The command to enable it via Azure CLI is `az feature register --namespace microsoft.compute --name EncryptionAtHost`.
- Compute Quota Adjustment: By default, FITFILE's Terraform attempts to use the Esv5 Series of virtual CPUs, which are memory-optimized. New subscriptions may have a limited default compute quota, which can lead to `QuotaExceeded` errors during deployment.
- The customer needs to ensure sufficient vCore allowance (e.g., requesting a limit of 10 for Standard ESv5 Family vCPUs).
- Alternatively, VM sizes can be reduced.
- Adding FITFILE DevOps User: A designated FITFILE DevOps user needs to be invited to the customer's Azure Tenant as an external user.
- The user type should be changed from Guest to Member.
- This user should then be assigned the `Contributor` role on the subscription. This is necessary for day-to-day management access (e.g., via a Jumpbox or VPN).
- Adhering to Naming Conventions: It's critical to request and follow the official naming convention document (like the HLD) for *every* resource type created (Resource Groups, VNets, Subnets, Route Tables, NSGs, AKS clusters, etc.). Failure to do so will require time-consuming teardowns and redeployments.
- Finalizing IP Addressing: All VNet and Subnet CIDR blocks must be finalized and confirmed upfront (e.g., `10.250.16.0/24`). Incorrect IP ranges, or insufficient ranges for services like AKS, will necessitate redeployments.

## 3. Network and Connectivity Requirements

Network configuration and firewall rules are often a source of delays and require pre-emptive planning.

- Virtual Network (VNet) Peering: Peering must be configured between the FITFILE vNet and the existing shared/hub vNet (e.g., CUH Shared Service vNet). This allows communication between the vNets and onward to ExpressRoute. If removed by accident during redeployments, it needs to be recreated.
- Defined Egress Path/Routing: All outbound traffic (`0.0.0.0/0`) from the FITFILE vNet needs to be explicitly routed through a specific firewall or virtual appliance IP (e.g., `10.250.1.68` for the Azure FortiGate). This ensures traffic goes via the on-premises proxy as required, rather than directly to the internet.
- Comprehensive Outbound Firewall Rules: A comprehensive list of all external endpoints, their protocols, and ports that the cluster and applications need to reach must be provided *before* the project starts. This includes:
- Hashicorp Vault (HTTPS/443, 8200).
- Auth0 authentication and UI components (HTTPS/443).
- FITFILE main domain (HTTPS/443).
- Grafana logging, tracing, and Prometheus metrics ingestion (HTTPS/443).
- GitLab (TCP/22, HTTPS/443).
- Microsoft package repositories (HTTP/80, HTTPS/443).
- FITFILE Private and Public Azure Container Registry (HTTPS/443).
- Microsoft Container Registry and CDN (HTTPS/443).
- Azure AD authentication (HTTPS/443).
- Azure API operations (HTTPS/443).
- Azure Monitor (metrics, data collection, Log Analytics) (HTTPS/443).
- Container Agent Telemetry (HTTPS/443).
- Azure CNI / kubenet (HTTPS/443).
- Azure CDN (HTTPS/443).
- Azure Blob Storage (HTTPS/443).
- Azure CLI installation (HTTPS/443).
- Kubernetes policy sync and Gatekeeper policy artifacts (HTTPS/443).
- Ubuntu/Canonical package and security updates (HTTP/80, HTTPS/443).
- Time sync (UDP/123).
- OpenSUSE packages (HTTP/80, HTTPS/443).
- Core Kubernetes system container images (HTTPS/443).
- VM extensions and components storage (HTTPS/443).
- Missing these rules can block deployment and application functionality, leading to significant delays due to change management processes.
- Inbound Firewall Rules: Rules to allow inbound traffic from specific prescribed IP addresses, such as Auth0 OAuth callback responses, are also required.
- DNS Configuration:
- Define required public/private DNS records (e.g., `app.privatelink.fitfile.net`, `argocd.privatelink.fitfile.net`).
- A private DNS zone will be deployed by FITFILE engineers as part of their Terraform scripts.
- Telefonica Tech will then configure a DNS forwarder in the CUH on-premises DNS to resolve the IP address of the FITFILE service (e.g., `privatelink.fitfile.net`).

## 4. External System Dependencies

Connecting to external systems requires upfront definition of access methods and credentials.

- Auth0 Configuration: As FITFILE uses Auth0 for identity tokens, Auth0 needs to be configured for the new deployment. This involves adding a new `ffnode` application in Auth0 by modifying and applying Terraform changes in the `central-services` repository. The resulting `client_id` and `client_secret` from Auth0 are needed later for Terraform variables and Vault secrets.
- Database Connectivity: If connecting to an on-premises SQL database, the server FQDN/IP, port, and authentication method (e.g., CUH AD username and password rather than a local SQL account) must be defined and signed off by governance and security teams. This can be a significant blocker.
- ACR Cross-Tenant Access: Issues with Azure Container Registry (ACR) cross-tenant access can occur. Solutions include creating a private link between tenants or manually injecting a Docker pull secret into the Kubernetes cluster.

## 5. Process and Coordination Prerequisites

Beyond technical steps, clear communication and a structured approach are vital.

- Formal Pre-Deployment Checklist Sign-off: A detailed technical prerequisite checklist, completed in collaboration with the customer and managed service provider, should be formally signed off *before* any deployment work begins. This is key to avoiding "firefighting" during deployment.
- Clarify Roles and Responsibilities: Clearly define who is responsible for what. For example, FITFILE for application and AKS infrastructure deployment within the subscription, and the managed service provider (e.g., Telefonica Tech) for core networking, subscription-level permissions, and liaising with internal teams.
- Understand Change Management Process (CAB): Familiarity with the customer's Change Advisory Board (CAB) process, including standard and expedited lead times for changes (e.g., firewall rule changes), is crucial for building realistic timelines and submitting requests well in advance.
- Pre-Flight Checks: Implement small scripts or manual checks before the main deployment to verify that prerequisites (e.g., jumpbox connectivity to external services, ACR URL access) are in place. This provides early failure detection and prevents long, failed deployments.

Understanding and addressing these prerequisites upfront can significantly streamline the Azure deployment process.

Would you like to review any specific part of these prerequisites in more detail, or perhaps we could explore how some of these issues manifested during a deployment, as described in the "Navigating Complex Cloud Deployments: Lessons Learned" document? I can also quiz you on this material if you'd like to test your understanding.
