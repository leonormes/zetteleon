---
aliases: []
confidence: 
created: 2025-07-08T20:35:16Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Fitfile deployment fixes
type:
uid: 
updated: 
version:
---

## Detailed Checklist for Updating `fitfile` Deployment Documents

Based on the recent experiences with the `fitfile` deployment, particularly the challenges encountered with networking, access, and configuration, here's a checklist for updating your documentation to ensure smoother future deployments. These updates should aim to turn reactive "firefighting" into a proactive, agreed-upon plan [1, 2].

I. Planning & Pre-Deployment Phase Documentation

This section should focus on capturing the crucial upfront information and coordination required before starting any deployment work.

1. Enhance the "0. Prerequisites" Section (e.g., `240628 - Azure Deployment Process` [3])

- Formalize a Comprehensive Technical Prerequisite Checklist: Document this list with explicit sign-off requirements from the customer (CUH) and managed service provider (Telefonica Tech) [2].
- Naming Conventions: Explicitly detail the required naming conventions for every resource type (e.g., Resource Groups, VNets, Subnets, Route Tables, NSGs, AKS clusters) [2, 4-6]. Ensure this aligns with the HLD and any organizational standards [2, 5].
  - Where to update: `FITFILE-Azure Deployment - Customer Checklist` or a dedicated `Pre-Deployment Checklist` document.
- Network Architecture Finalization:
  - IP Addressing: Clearly define and confirm all VNet and Subnet CIDR blocks (e.g., `10.250.16.0/24`) upfront [4, 7].
  - VNet Peering: Explicitly state requirements for peering between the `fitfile` VNet and shared/hub VNets [7-9].
  - Routing: Define the exact egress path, including if all traffic (`0.0.0.0/0`) needs to be forced through a specific firewall/virtual appliance IP, and obtain this IP address upfront [7, 10, 11]. Document the application of route tables to specific subnets (e.g., system and jumpbox, but not workflows) [11, 12].
  - Where to update: `FITFILE-Azure - Infrastructure (private)` [13] and `TT_CUH_FitFile_HLD_0.1` sections on network design [8, 9, 14].
- Firewall & Outbound Connectivity (Critical List):
  - Compile and document a comprehensive allow-list of all external endpoints that the cluster and applications (`fitfile` app, ArgoCD, Grafana, Vault, MCR, Auth0, GitLab, etc.) need to reach, including URLs, protocols (e.g., HTTPS), and ports (e.g., 443, 8080, 8200) [7, 12, 15]. This list should be provided before project starts [7].
  - Document any inbound allow lists for callback responses (e.g., from Auth0) [16].
  - Where to update: `FITFILE-Azure Deployment - Customer Checklist` [17], `TT_CUH_FitFile_HLD_0.1` [18], and `Telefonica Installation Progress for FitFile` [12, 15, 19].
- Change Management Process (CAB): Document the change management process (e.g., CAB) including standard lead times for firewall rule changes and processes for expedited changes. This helps in building realistic timelines [15, 20].
  - Where to update: A new `Deployment Process` section or within `FITFILE-Azure - Tooling`.
- DNS Setup: Clarify and document the process for setting up Conditional Forwarders on on-prem DNS servers for private DNS zones (e.g., `privatelink.fitfile.net`), including necessary IP addresses and domain names [21, 22]. Document the required DNS records for accessing `fitfile` application and ArgoCD [15].
  - Where to update: `FITFILE-Azure - Infrastructure (private)` [23] and `azure-dns.pdf`.

II. Infrastructure Deployment Documentation

This section pertains to the creation and management of the underlying Azure resources.

1. Terraform/IaC Best Practices:

- Modular IaC Structure: Recommend structuring Terraform code to be more modular (e.g., networking setup in a separate state file from AKS cluster configuration) to reduce the risk of accidental wipes [20].
- Pre-Flight Checks: Implement a small script or manual checklist for pre-flight checks before running main deployments (e.g., verifying `mcr.microsoft.com` resolution, ACR connectivity) [24]. This creates a fast failure point [24].
- Deployment Key Consistency: Emphasize the importance of using the `deployment-key` consistently across all infrastructure components [13, 25, 26].
- Sensitive Variables: Ensure all ARM keys and other sensitive variables are marked as such (e.g., `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` for AWS; client secrets for Azure) and handled securely [13, 27].
- GitLab Integration: Document the steps for creating new customer deployment repositories in GitLab to isolate configuration and manage access [27, 28]. Include steps for cloning template repos (e.g., `terraform-aws-eks-private`) [29].
- Where to update: `FITFILE-AWS - Infrastructure (private)` [27, 29], `FITFILE-Azure - Infrastructure (private)` [28, 30].
- Resource Versioning: Recommend using the current private-infrastructure module version and replacing `<latest_version>` placeholders in Terraform blocks [23].
- Terraform State Management: Document the process for copying `terraform.tfstate` files off the jumpbox and storing them in a subdirectory within the GitLab Customers deployment repo, emphasizing that it should not be in the root to avoid conflicts [31].
- Where to update: `FITFILE-Azure - Infrastructure (private)` [31].
- Compute Quota: Document the need to adjust compute quota for Esv5 Series VMs, as they are not normally in the default for new subscriptions [32].
- Where to update: `FITFILE Azure Deployment - Customer Checklist` [32].

III. Platform Deployment & Configuration Documentation

This covers the setup of GitOps tooling and secret injection.

1. Secrets Management (Vault/Sops):

- Centralized Secrets: Reinforce separating configuration data from application code and deploying it using Kubernetes ConfigMaps and Secrets, noting that this avoids redeploying the app for every password change [33].
- Sops for Helm Charts: Document the use of Sops for managing Helm Chart secrets, encrypting values files, and how it integrates with the deployment process (e.g., temp-staging-secrets file deletion) [34-38].
- Vault Integration: Detail how to populate secrets in HashiCorp Vault (e.g., `application`, `spicedb`, `cloudflare`, `monitoring`, `argo-workflows` secrets), including the process for creating new versions of secrets and populating JSON secrets [26, 39].
- AppRoles: Provide clear instructions on how to obtain and use AppRoles values for Vault access [40-42].
- Avoiding Hardcoding: Emphasize that sensitive information (API keys, passwords) should never be directly added to Kubernetes manifest files or committed to code repositories [43-46]. Recommend using Managed Identity or Azure Key Vault for production workloads [44].
- Where to update: `FITFILE-Azure - Platform (private)` [41, 42], `FITFILE-Azure - Tooling` [26, 39], `Managing Kubernetes Resources Using Helm` [43, 47, 48].

2. GitOps & Helmfile:

- Single Source of Truth: Reiterate that Helmfile should be the single source of truth for cluster deployments, and manual Helm deployments should be avoided if Helmfile is used [49-51].
- Helmfile Configuration: Detail how `helmfile.yaml` specifies everything running in the cluster declaratively, including repositories, releases, chart names, namespaces, and paths to `values.yaml` files [52, 53].
- Automated Sync: Document how `helmfile sync` can be run automatically as part of the continuous deployment pipeline [49].
- Helm Value Overrides: Provide instructions for preparing Helm value overrides in the deployment repo, specifically for the `ffnodes/<customer>/<deployment-key>/values.yaml` path [54, 55].
- Auth0 Integration: Update the `auth0/locals.tf` file with new `ffnode` application blocks and ensure `api_audience` is the DNS record for the ingress controller [56-58].
- Where to update: `FITFILE-AWS - Platform (private)` [40], `FITFILE-Azure - Platform (private)` [41, 54, 55], `FITFILE-Azure - Tooling` [56].

3. Cluster Hardening & Security (General):

- CIS Benchmarks: Document the use of tools like `kube-bench` to audit the Kubernetes cluster against CIS benchmarks for security best practices [37, 59, 60]. Include regular conformance testing using Sonobuoy [61].
- Container Image Security: Detail processes for scanning container images for known vulnerabilities (CVEs) during build and periodically post-deployment (e.g., using Anchore Engine, Trivy, Snyk, Whitesource, Google scanning) [62-74]. Emphasize using minimal base OS components (e.g., distroless/scratch images) to reduce attack surface [70, 71, 73, 75, 76].
- Automated Updates: Document procedures for regularly upgrading Kubernetes clusters and node pools to stay current with security fixes and new features [77-82].
- Deployment Safeguards: Evaluate and document the use of deployment safeguards for validating deployments against best practices at creation/update time [83-85].
- Where to update: `Kubernetes Security and Observability`, `Container Security_ Fundamental Technology`, `azure-aks.pdf`.

IV. Application Deployment Documentation

This section covers the actual deployment of applications using Helm and managing their lifecycle.

1. Helm Chart Best Practices:

- Helm Chart Development: Include guidance on scaffolding new Helm charts, understanding `Chart.yaml` (metadata, API version, type), and managing chart dependencies [86-93].
- Template Best Practices: Document how to dynamically generate Kubernetes YAML using templates, referencing values and built-in objects [94-98].
- Lifecycle Management (Install, Upgrade, Rollback, Uninstall): Detail the commands and processes for managing application lifecycles with Helm [33, 79, 99-107].
- `--values` vs. `--set`: Emphasize `--values` for managing multiple parameters via version-controlled YAML files, and `--set` for sensitive values not stored in source control [43].
- Where to update: `Managing Kubernetes Resources Using Helm`, especially chapters on Helm Chart Development and Installation.

2. Deployment Strategies:

- Database Migrations with Hooks: Document how to handle database migrations using Helm hooks (e.g., `pre-upgrade` for snapshots, `pre-rollback` for restore) [108-114].
- Rolling Updates: Document the default `RollingUpdate` strategy and considerations for `Recreate` [115-118].
- Replica Management: Include best practices for using the minimum number of Pods for a given Deployment to satisfy performance and availability requirements, gradually reducing replicas to meet service level objectives [119, 120].
- Resource Requests and Limits: Emphasize the importance of setting correct resource requests and limits for containers to optimize costs and prevent failures, with regular review against actual usage [47, 48, 120-122].
- Where to update: `Cloud Native DevOps With Kubernetes` [117, 123], `Managing Kubernetes Resources Using Helm` [110, 111, 124].

3. User Access to Application:

- DNS records for UI/API: Clearly document the domain names (e.g., `app.privatelink.fitfile.net`) for accessing the FITFILE application and ArgoCD [15].
- Client Access Methods: Clarify how users (e.g., CUH on-prem) will access the system (web browser, kubectl access, VPN, VDI vs. local VPN agent) and document required tools [11, 125, 126].
- Where to update: `Navigating Complex Cloud Deployments: Lessons Learned` [1], `Telefonica Installation Progress for FitFile` [11, 125, 126].

V. Operational Excellence & Monitoring Documentation

This section covers ongoing operations, observability, and troubleshooting.

1. Monitoring & Observability Strategy:

- Comprehensive Strategy: Document a strategy for collecting logs and metrics to monitor workload health, identify trends, and anticipate failure conditions [127, 128].
- Metrics Introduction: Explain the use of metrics (e.g., requests processed, error rates, response times, CPU/memory usage) for sophisticated monitoring beyond simple working/not working checks [129-135].
- Dashboards: Document the use of dashboards (e.g., Grafana) for graphing metrics, reviewing key dashboards regularly, and using consistent layouts [121, 136, 137].
- Alerting System: Describe how to set up an effective alerting system that can query various log data sources (Kubernetes activity, network, application, DNS logs) and send notifications [138-141].
- Probes: Emphasize setting up liveness and readiness probes to inform Kubernetes about application health and readiness to handle requests [123, 142, 143].
- Auditing: Implement mechanisms for auditing configuration and policy changes for compliance, and Kubernetes-aware network flow logs [144-146].
- Where to update: `Cloud Native DevOps With Kubernetes` [129, 130, 136, 138, 147], `Kubernetes Security and Observability` [148-150], `azure-aks.pdf` [127].

2. Troubleshooting:

- `kubectl` as a Swiss Army Knife: Document the extensive use of `kubectl` for applying configuration, creating/modifying/destroying resources, querying cluster info, viewing logs, and attaching to containers [96, 130, 132, 151-159].
- `kubectl diff`: Reinforce the best practice of using `kubectl diff` before applying any updates to production clusters to see exact changes and warn if live state is out of sync [153, 160, 161].
- Resource Description: Document using `kubectl describe` for detailed information and troubleshooting, especially the `Events` section [152, 162].
- Networking Tools: Include diagnostic tools like `dnsutils` pod, `netshoot` pods, `traceroute`, `ping`, `telnet`, `netcat`, `nmap` for checking connectivity and troubleshooting network issues [163, 164].
- Where to update: `Cloud Native DevOps With Kubernetes` [153, 154, 156-158, 161], `Networking and Kubernetes` [163, 164].

---

For a private AKS cluster, inbound DNS records are crucial for allowing users and other systems to access the deployed services within the cluster, even though the cluster itself does not expose public IP addresses [1-3]. This setup leverages Azure Private DNS zones and an ingress controller.

Here's an elaboration on the details:

1. Private AKS Cluster Fundamentals
   A private AKS cluster is designed for internal use, meaning it's configured to use no public IP addresses and blocks public access, making it available only from within its associated Virtual Network (VNet) [1-3]. To access services deployed within such a cluster, you typically connect from a virtual machine located in the same VNet, or via an ExpressRoute or VPN connection for hybrid scenarios [4].

2. Role of the Ingress Controller
   Even in a private AKS cluster, an Ingress controller is used to manage external HTTP-like traffic access to services within the cluster [5]. It provides advanced capabilities such as load balancing, SSL termination, and name-based virtual hosting by operating at Layer 7 (HTTP) [5]. For a private cluster, this ingress controller is typically exposed through an internal load balancer, which uses a private static IP address [6, 7]. This IP address is the target for your inbound DNS records [8].

3. Inbound DNS Records for Private AKS
   To enable access to services behind the ingress controller in a private AKS cluster, specific DNS records must be defined, typically in an Azure Private DNS Zone [9, 10]. These records resolve to the private IP address of the ingress controller within the VNet.

- Record Types: The most common type of record used for this purpose is an 'A' record, which maps a hostname to an IPv4 address [11-13]. CNAME records can also be used, mapping one domain name to another [11-13].
- Example from Sources: For FITFILE deployments, the `api_audience` must be the DNS record for the ingress controller [9]. Specific examples of private A records include `cuh-poc-1.privatelink.fitfile.net` and `app.privatelink.fitfile.net`, which point to internal IP addresses like `10.0.1.10` or `10.250.16.7` [14-16]. The `ingress_controller_ip_address` variable specifies the IP address from the node pool subnet that the NGINX ingress controller binds to [8]. This `privatelink.fitfile.net` domain is an Azure Private DNS Zone [14, 15].
- Configuration: These records are created within a designated DNS zone [10, 17]. For a private AKS cluster, this would be an Azure Private DNS zone.

3. Azure Private DNS Zones in Detail
   Azure Private DNS is a service designed to manage and resolve domain names within virtual networks without the need for custom DNS solutions [18, 19].

- Linking Virtual Networks: To enable name resolution, you must link the virtual network where your AKS cluster resides to the private DNS zone [11, 20, 21]. Linked virtual networks have full access and can resolve all DNS records published in the private zone [20].
- Auto-registration (for VMs, not direct AKS services): While primarily for Virtual Machines, the auto-registration feature within a virtual network link can automatically manage DNS records for VMs deployed in that VNet, creating 'A' records pointing to their private IP addresses [11, 21-23]. However, for AKS services exposed via an ingress, you would typically manually create the A records pointing to the ingress controller's internal IP.
- DNS Resolution: When using default DNS settings in a VNet, private DNS zones linked to that VNet are queried first for name resolution [21]. Records contained in a private DNS zone are not resolvable from the Internet [21].
- Split-Horizon DNS: Azure Private DNS allows for split-horizon DNS, where the same domain name can resolve to different IP addresses depending on whether the query originates from within the virtual network (private IP) or from the public internet (public IP) [24-26]. This means `app.privatelink.fitfile.net` would only resolve privately within the linked networks.
- Limitations: A virtual network can be linked to only one private DNS zone if automatic registration of VM DNS records is enabled, although a single private zone can be linked to multiple virtual networks [27-29].

4. Connectivity and Access Flow
   Users on a CUH network wishing to access the FitFile system in Azure would visit URLs like `app.privatelink.fitfile.net` or `argocd.privatelink.fitfile.net` [15, 16]. For this to work, a forward lookup for that private DNS zone is part of the high-level design [14]. This private DNS zone ensures that internal traffic (e.g., from an on-premises network connected via ExpressRoute or VPN) is correctly routed to the internal IP of the ingress controller within the private AKS VNet.

- Azure DNS Private Resolver: For more complex hybrid scenarios requiring resolution between Azure and on-premises networks, Azure DNS Private Resolver can be used [30-34]. This service allows on-premises DNS conditional forwarders to send DNS queries to inbound endpoints within Azure, enabling resolution of Azure private DNS zones [35-37].

5. Security Considerations

- Private IP Usage: Leveraging internal load balancers with private IP addresses for ingress controllers limits service access to the internal network, enhancing security [6, 7].
- DNS Protection: Azure RBAC and resource locks are available to protect your private DNS zones and records from unauthorized or accidental changes, which are critical resources as their deletion can lead to service outages [38].
- Dangling DNS Prevention: Alias records can prevent "dangling DNS records" by coupling the lifecycle of a DNS record with an Azure resource. If the underlying resource is deleted, the alias record becomes an empty record set, avoiding security risks [39, 40].
