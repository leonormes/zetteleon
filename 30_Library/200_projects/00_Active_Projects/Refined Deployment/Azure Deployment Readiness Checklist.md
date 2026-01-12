---
aliases: []
confidence: ""
created: 2025-07-01T05:44:33Z
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:49:56+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags:
  - azure
  - ff_deploy
  - documentation
  - prerequisites
  - project/work/deployment
  - setup
title: Prerequisities
type: ""
uid:
updated:
version: ""
---

## 0. Hindsight Notes (Lessons Learned from Past Deployments)

- Network Configuration Complexity: Past deployments have highlighted the critical need for precise IP range definitions, subnet planning, and clear routing configurations. Misconfigurations in these areas have led to connectivity issues and deployment delays. It's essential to gather detailed network architecture information upfront and validate it thoroughly.
- Firewall and Egress/Ingress Rules: Ensuring correct firewall rules for both inbound and outbound traffic is paramount. Delays have occurred due to lengthy approval processes for firewall changes and a lack of clarity on required ports and endpoints. Proactive engagement with the customer's network and security teams is crucial.
- Identity and Access Management (IAM): Inconsistent or incomplete IAM configurations have caused access issues for FITFILE personnel and automated systems. Establishing clear roles, responsibilities, and providing necessary permissions (e.g., Service Principal with least privilege) early in the process is vital.
- Change Management Processes: Navigating customer-specific change management processes (e.g., CAB approvals) can be time-consuming. Understanding these processes early and building them into the project timeline is essential to avoid delays.
- Monitoring and Logging Integration: A critical lesson learned from previous engagements is the impact of incomplete or misconfigured SIEM and logging integrations. When logs are not properly aggregated or alerts are not effectively routed, it critically impairs the ability to monitor threats, audit traffic, and respond to incidents. Ensuring comprehensive log forwarding and alert routing to the customer's existing enterprise SIEM and monitoring platforms is a key requirement for effective incident response and overall system health.

---

## 1. Business Objectives and Scope

- What are the primary business drivers for this Azure deployment?
- What specific business outcomes are expected from this deployment?
- What is the overall scope of the deployment (e.g., specific applications, services, environments)?
- Are there any specific compliance or regulatory requirements (e.g., GDPR, HIPAA, NHS DSPT) that need to be addressed by this deployment?

---

## 2. Network Configuration and Requirements

- IP Addressing:
  - What are the specific IP range requirements for the Azure deployment (e.g., VNet CIDR, subnet CIDR for AKS, Pods, Services)?
  - Are there any existing IP address allocations or restrictions within the customer's environment that need to be considered?
  - Will the customer provide the subnet(s), or will FITFILE be responsible for their creation?
- DNS:
  - What is the customer's existing DNS solution? Is there a specific DNS server or zone that FITFILE should integrate with or utilize for the Azure deployment?
  - Are there specific requirements for internal DNS resolution or split-horizon DNS?
  - Will FITFILE be responsible for managing DNS records (e.g., CNAMEs) or will the customer handle this?
- Connectivity:
  - What is the required method for platform access for maintenance (e.g., VDI/VPN/ZTNA to Hosting Cloud)?
  - Will a bastion host be provided, and how will access be managed (e.g., Windows/Linux jumpbox, Azure Bastion)?
  - Are there any specific requirements for ExpressRoute or VPN gateway configurations for hybrid connectivity?
  - How should pod-to-external-service communication be handled? Are there restrictions on outbound internet access from the cluster?
  - What is the process for allow-listing external services?

---

## 3. Firewall, Egress, and Ingress Rules

- Egress Filtering:
  - Are there specific requirements for egress filtering from the Azure environment?
  - Will all outbound internet traffic from FITFILE's Azure environment be routed through a central firewall and proxy (e.g., on-premises FortiGate and McAfee Proxy), or will direct internet access be permitted?
  - What is the process for requesting new firewall rules, and what is the typical approval timeline (e.g., CAB meeting frequency)?
- Ingress Requirements:
  - Are there specific inbound network requirements for the FITFILE platform or its components (e.g., Auth0 callbacks, WAF integration, on-premises access)?
  - Are there any restrictions on using specific ports or protocols for ingress traffic?
- Firewall Rule Management:
  - Who is responsible for managing the firewall rules outside the FITFILE cluster?
  - How are security groups and network policies managed?

---

## 4. Collaboration and Administrative Access

- Cloud Environment Administration:
  - Who has administrative responsibilities for the cloud environment (team/person)?
  - Would this team be responsible for networking-related changes including DNS/Certificates/Firewalls?
  - What is the process for requesting infrastructure changes?
- User Access and Identity Management:
  - What is the process for user provisioning and de-provisioning?
  - Are there specific authentication requirements for cluster access (e.g., MFA, specific identity providers)?
  - How should FITFILE's central services (e.g., Auth0 for authentication, HashiCorp Vault for secrets) be integrated with the customer's identity management system?
  - What is the process for granting access to FITFILE's central services?
- Service Principal/IAM Roles:
  - What is the process for creating and managing Service Principals (Azure) or IAM roles (AWS) for FITFILE's deployment automation?
  - What level of permissions (e.g., Contributor, custom role) can be granted to the Service Principal/IAM account? Can a reduced-scope role be defined?
  - Are there specific Azure/AWS roles or policies that must be applied or avoided?
- Change Management:
  - What is the customer's formal change management process (e.g., CAB approval)? What is the typical lead time for approvals?
  - How are infrastructure changes communicated and tracked?

---

## 5. Technical Requirements and Dependencies

- Resource Sizing:
  - Discuss node sizing requirements for the Kubernetes cluster (e.g., CPU, memory, storage).
  - Are there specific storage class requirements?
  - Are there specific resource quotas that need to be implemented? How should resource requests and limits be handled for pods?
- Encryption:
  - Is there a specific encryption key that needs to be applied to all storage disks, or will the default subscription encryption key suffice?
- Cloud Security Features:
  - For Azure: Is Azure Defender or Azure Backup active in the subscription?
  - For AWS: Is GuardDuty/Macie/Backup enabled and in use?
  - What container scanning solutions are currently in place?
  - Are there requirements for image signing?
- Infrastructure as Code (IaC):
  - Are there any restrictions on using Terraform Cloud for state management?
  - What are the backup requirements for Terraform state?
  - What are the requirements for reviews and approval of Terraform changes?
- Observability, Logging, and SIEM Integration:
  - Existing Solutions: What enterprise monitoring, logging, and SIEM platforms does the customer currently utilize (e.g., Splunk, Azure Sentinel, ELK Stack, Datadog, Prometheus, Grafana)?
  - Log Management:
    - What are the customer's log retention policies?
    - What log formats are preferred for ingestion into their SIEM/logging platform (e.g., JSON, LEEF, CEF)?
    - What level of detail is required for logs generated by the Azure deployment?
  - Alerting:
    - What are the customer's requirements for alert configuration, thresholds, and notification channels?
    - How should alerts from the Azure deployment be integrated into their existing alerting system?
  - SIEM Integration:
    - What are the required mechanisms (e.g., APIs, log forwarding protocols like Syslog, data formats like JSON/LEEF) for integrating logs and alerts from the new Azure deployment into their existing SIEM systems?
    - Are there specific endpoints or IP ranges that need to be whitelisted for log forwarding?
  - Unified Visibility:
    - What are the customer's expectations for unified visibility across their on-premises and Azure environments?
    - Are there requirements for specific dashboards or reporting that should be integrated with their existing monitoring tools?
  - Incident Response:
    - How should the new Azure deployment contribute to the customer's overall incident response workflows?
    - What are the desired RTO/RPO requirements for the Azure deployment?
  - Responsible Parties: Who will be responsible for infrastructure monitoring and alerts for the new Azure deployment?

---

## 6. Collaboration and Handoff

- Day-to-Day Operations:
  - Who will be responsible for day-to-day cluster operations post-deployment?
- Maintenance and Upgrades:
  - What is the customer's preferred method for managing cluster upgrades?
  - Are there specific maintenance windows or procedures that need to be followed?
- Documentation and Training:
  - What documentation standards are expected for the deployment?
  - What level of training is required for the customer's operations and support teams?
- Handoff Process:
  - What is the defined process for handing over the deployed environment to the customer's operational team?
  - Are there specific handover checklists or validation steps required?

---

## 7. Past Issues and Hindsight

- Previous Deployment Challenges:
  - Have there been any previous Azure or cloud deployment challenges that could have been mitigated with better upfront planning or collaboration? (e.g., network misconfigurations, IAM issues, lengthy change management processes).
  - Were there any specific issues related to monitoring, logging, or SIEM integration in past deployments that could have been avoided with better foresight? (e.g., incomplete log data, alert fatigue, difficulty correlating events).
- Lessons Learned:
  - What are the key lessons learned from previous deployments that FITFILE should be aware of?

---

## 8. Deployment and Project Management

- Deployment Timeline:
  - What is the desired timeline for the deployment? Are there any critical deadlines or upcoming events (e.g., change freezes) that need to be considered?
- Project Team and Contacts:
  - Who are the key technical stakeholders and points of contact on the customer side?
  - What are the roles and responsibilities of the customer's project team?
- Communication Plan:
  - What are the preferred communication channels and frequency for project updates?
  - How will significant changes or incidents be communicated to stakeholders?
- Acceptance Criteria:
  - What are the agreed-upon acceptance criteria for the successful deployment?

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
- You might need to change the script's permissions using `chmod +x./short_name.sh` before running it.
- The generated key needs to be saved in a database. This `deployment-key` will be used consistently across the infrastructure.

## 2. Azure Tenant and Subscription Configuration (Customer Side)

These are crucial prerequisites that often require close liaison between FITFILE and the customer's IT team. Lessons learned from past deployments emphasize the importance of having these details ironed out _before_ starting any Terraform work.

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
- Adhering to Naming Conventions: It's critical to request and follow the official naming convention document (like the HLD) for _every_ resource type created (Resource Groups, VNets, Subnets, Route Tables, NSGs, AKS clusters, etc.). Failure to do so will require time-consuming teardowns and redeployments.
- Finalizing IP Addressing: All VNet and Subnet CIDR blocks must be finalized and confirmed upfront (e.g., `10.250.16.0/24`). Incorrect IP ranges, or insufficient ranges for services like AKS, will necessitate redeployments.

## 3. Network and Connectivity Requirements

Network configuration and firewall rules are often a source of delays and require pre-emptive planning.

- Virtual Network (VNet) Peering: Peering must be configured between the FITFILE vNet and the existing shared/hub vNet (e.g., CUH Shared Service vNet). This allows communication between the vNets and onward to ExpressRoute. If removed by accident during redeployments, it needs to be recreated.
- Defined Egress Path/Routing: All outbound traffic (`0.0.0.0/0`) from the FITFILE vNet needs to be explicitly routed through a specific firewall or virtual appliance IP (e.g., `10.250.1.68` for the Azure FortiGate). This ensures traffic goes via the on-premises proxy as required, rather than directly to the internet.
- Comprehensive Outbound Firewall Rules: A comprehensive list of all external endpoints, their protocols, and ports that the cluster and applications need to reach must be provided _before_ the project starts. This includes:
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

- Formal Pre-Deployment Checklist Sign-off: A detailed technical prerequisite checklist, completed in collaboration with the customer and managed service provider, should be formally signed off _before_ any deployment work begins. This is key to avoiding "firefighting" during deployment.
- Clarify Roles and Responsibilities: Clearly define who is responsible for what. For example, FITFILE for application and AKS infrastructure deployment within the subscription, and the managed service provider (e.g., Telefonica Tech) for core networking, subscription-level permissions, and liaising with internal teams.
- Understand Change Management Process (CAB): Familiarity with the customer's Change Advisory Board (CAB) process, including standard and expedited lead times for changes (e.g., firewall rule changes), is crucial for building realistic timelines and submitting requests well in advance.
- Pre-Flight Checks: Implement small scripts or manual checks before the main deployment to verify that prerequisites (e.g., jumpbox connectivity to external services, ACR URL access) are in place. This provides early failure detection and prevents long, failed deployments.

Understanding and addressing these prerequisites upfront can significantly streamline the Azure deployment process.

Would you like to review any specific part of these prerequisites in more detail, or perhaps we could explore how some of these issues manifested during a deployment, as described in the "Navigating Complex Cloud Deployments: Lessons Learned" document? I can also quiz you on this material if you'd like to test your understanding.
