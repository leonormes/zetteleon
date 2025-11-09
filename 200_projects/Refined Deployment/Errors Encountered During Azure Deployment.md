---
aliases: []
confidence: 
created: 2025-07-02T12:08:36Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aks, azure, errors, project/work/deployment, troubleshooting]
title: Errors Encountered During Azure Deployment
type:
uid: 
updated: 
version:
---

Based on the provided source materials, several specific errors and challenges are highlighted concerning Azure deployments, particularly with Azure Kubernetes Service (AKS):

1. **Initial Access and Permissions Issues**
   - **Problem:** Attempts to log in (`az login`) can "hang," potentially due to a permissions issue or a session conflict. There might also be a lack of upfront clarity on how end-users for testing and other platforms (like the Software Development Environment, SDE) will access the FITFILE application, especially concerning VPNs and DNS records (e.g., `app.privatelink.fitfile.net`). Furthermore, obtaining connection details and security sign-off for on-premise database access can be a pending issue that blocks deployment.
   - **Solutions/Prevention:** To avoid these initial access problems, it's crucial to finalise and confirm all Virtual Network (VNet) and Subnet CIDR blocks (e.g., `10.250.16.0/24`) upfront. Explicitly state the requirement for peering between your VNet and any shared or hub VNets. Define the exact egress path, including whether all traffic (`0.0.0.0/0`) needs to be forced through a specific firewall or virtual appliance IP, and get this IP address confirmed in advance. A comprehensive list of all external endpoints that your cluster and applications need to reach (such as URLs for Grafana, Vault, Microsoft Container Registry (MCR)) should be compiled and provided *before* the project begins. Implementing "pre-flight checks"—small scripts or manual checklists to verify prerequisites like resolving `mcr.microsoft.com` from the jumpbox or connecting to the Azure Container Registry URL—can help identify issues early, providing a "fast failure point" before initiating a long-running deployment.

2. **Azure Resource Quota Limits**
   - **Problem:** During Kubernetes cluster creation, you might encounter an error indicating that you have "reached or exceeded the maximum number of zones in subscription {subscription ID}". This error specifically points to the vCore allowance in your Azure subscription.
   - **Solution:** The resolution is to either increase the vCore allowance in your Azure subscription or reduce the requested Virtual Machine (VM) sizes for your cluster nodes.

3. **`EncryptionAtHost` Not Enabled**
   - **Problem:** An error might occur if `EncryptionAtHost` is not enabled in the subscription.
   - **Solution:** This can be resolved by running a specific command using the Azure CLI.

4. **Azure Container Registry (ACR) Cross-Tenant Access Issues**
   - **Problem:** There's a mentioned error related to ACR cross-tenant access, appearing in the context of the `azurerm_kubernetes_cluster` resource within Terraform configurations.

5. **Missing or Misconfigured Firewall Rules / Outbound Connectivity**
   - **Problem:** Deployment can fail if essential firewall rules are not in place, preventing communication with necessary Azure endpoints. The documentation explicitly lists critical Azure Global Endpoints (e.g., `mcr.microsoft.com`, `*.cdn.mscr.io`, `*.blob.core.windows.net`, `login.microsoftonline.com`, `management.azure.com`) and AKS-Specific Endpoints (e.g., `*.hcp.<region>.azmk8s.io`, `*.tun.<region>.azmk8s.io` on port 9000 or 443, `*.dp.<region>.azmk8s.io` on port 443), as well as Operating System Endpoints (for Ubuntu and Azure Linux nodes, including NTP). Some of these blocked endpoints have explicitly stopped deployments from completing.
   - **Solution:** It is a dependency to provide URLs for whitelisting, especially since FitFile documentation might not provide specific details on all internet-based services it interacts with. When such issues arise, raising expedited changes for firewall rule updates is a necessary step to unblock the deployment.

6. **Transient Faults in Azure**
   - **Problem:** Transient faults are short, intermittent failures in components that are common in distributed cloud environments like Azure. These can occur due to application crashes, pod scaling, node patching, or temporary infrastructure issues like hardware or networking problems. It's impossible to eliminate all transient faults, so clients accessing AKS-hosted applications need to be prepared to retry failed requests.
   - **Mitigation:** Following Kubernetes and Azure best practices in your deployment can minimize the likelihood of transient faults and avoid or mitigate downtime. Applications should handle transient faults, typically by retrying affected requests.

## Common Concepts & Challenges in Cloud-Native Deployments

These specific errors are part of broader challenges in the cloud-native and DevOps landscape:

1. **The Inherent Complexity of Distributed Systems**
   - Cloud-native applications, composed of multiple, cooperating, distributed microservices, are inherently complex and prone to failure in surprising ways. Unlike traditional systems, distributed systems are rarely "up" or "down" but exist in a constant state of partially degraded service. This makes troubleshooting challenging as `nothing is ever completely right aboard a ship`. The technicalities of operating such systems—recovering from failures, handling timeouts, smoothly upgrading versions—are deeply intertwined with their design and implementation.

2. **DevOps: A Human and Organisational Issue**
   - DevOps is fundamentally an organisational and human issue, not just a technical one. It involves development and operations teams learning to work together, designing and building systems collaboratively, and continuously monitoring and improving systems based on feedback. The lines between software engineers and operations engineers are blurring, as "it's all just software now".

3. **Importance of Observability and Monitoring**
   - Cloud-native applications are harder to inspect and debug due to their distributed nature. Therefore, observability (monitoring, logging, tracing, and metrics) is a key requirement.
   - **Logs:** Containers write to standard output and error streams, which are considered logs in Kubernetes. In production, logs from multiple services are aggregated into central databases (e.g., Elasticsearch) for querying and graphing to aid troubleshooting. Kubernetes audit logs are an excellent source of information to understand the complete life cycle of resources.
   - **Metrics:** Key metrics for services include **R**equests, **E**rrors, and **D**uration (RED pattern). For resources, **U**tilisation, **S**aturation, and **E**rrors (USE pattern) are important for performance analysis. Kubernetes-native monitoring is crucial to collect data with proper context (pods, labels, policies, namespaces) rather than just at a low-level IP address basis.
   - **Alerting:** Alerts indicate unexpected deviations, but in distributed systems, over-alerting can lead to "alert fatigue". High-fidelity alerts based on correlated data and machine learning are recommended.
   - **Tools:** `kubectl logs` and `kubectl describe` are essential for troubleshooting containers. Visualisation tools like Hubble UI and CLI can help diagnose DNS, connectivity, and network policy issues by providing real-time traffic flow insights, highlighting dropped packets, and showing interactions between pods.

4. **Security Risks and Misconfigurations**
   - Kubernetes is not secure by default, and securing it requires a holistic understanding of various considerations, including organizational challenges and new best practices.
   - **Shift-Left Security:** Identifying and remediating vulnerabilities early in the CI/CD pipeline (known as "shift-left" security) is much more efficient and cost-effective than finding them after deployment.
   - **Image Scanning:** Regularly scanning container images for known software vulnerabilities (CVEs) in application code and third-party dependencies is essential throughout the lifecycle, from build to registry. Scanners that consider distribution-specific security advisories are more accurate.
   - **Supply Chain Attacks:** The integrity of container images from build to deployment is critical, as attackers could tamper with or replace images in the registry. Access to the registry needs to be controlled.
   - **Misconfigurations:** Badly configured container images (e.g., running as root user with excessive privileges) and badly configured containers (e.g., unnecessary or unplanned privileges, mounting host directories) are significant weaknesses. It's crucial to apply the principle of "least privilege". The Center for Internet Security (CIS) publishes benchmarks for best practices in configuring Docker, Kubernetes, and Linux to enhance security.
   - **Secrets Management:** Application code often needs credentials (secrets). Securely passing these values to containers at runtime is critical, as exposed secrets are a major attack vector. Storing secrets in code or public repositories like GitHub is a significant risk. Centralised solutions like Azure Key Vault are recommended for safeguarding keys and secrets.

5. **Infrastructure as Code (IaC) and Declarative Management**
   - The importance of declarative infrastructure as code is heavily emphasised. This means defining Kubernetes resources using YAML manifests or Helm charts stored in version control to maintain a single source of truth. This approach helps automate and validate deployments, reducing errors.
   - **Avoid Imperative Commands:** While `kubectl run` and `kubectl exec` are useful for quick testing or debugging, using imperative commands for production changes is discouraged. They can lead to the cluster state becoming out of sync with version-controlled manifests, making it difficult to track changes or reproduce environments.

6. **Managed Kubernetes Services (AKS, EKS, GKE)**
   - Managed services like Azure Kubernetes Service (AKS) abstract away much of the operational overhead of managing Kubernetes, including master nodes, security, and scalability, making them ideal for high availability and portability.
   - However, using managed services involves a "shared responsibility model," where the cloud provider handles some security aspects by default, but the user remains responsible for others (e.g., workload security, secure configurations).
   - Self-hosting Kubernetes, while offering more control, requires significant engineering time for initial setup and ongoing maintenance.

7. **Continuous Deployment (CD)**
   - Continuous deployment is the automatic deployment of successful builds to production. A key benefit is ensuring "no surprises in production" by testing the container artifact itself, not just the source code, across various environments. Azure Pipelines is noted as a tool that can be used for CD with Kubernetes.

In summary, successful Azure deployments, especially with Kubernetes, depend on proactive planning, rigorous attention to security from the earliest stages of development, comprehensive observability for rapid issue detection, and a commitment to infrastructure as code for consistent and reproducible environments.

---

### Existing DNS Endpoints (AWS) in the Context of Common Concepts & Challenges

When discussing existing DNS endpoints in an AWS environment, the provided sources highlight a specific challenge related to pre-existing infrastructure and its impact on deployment automation. This fits into the broader common concepts and challenges of managing DNS in complex, distributed cloud-native environments.

**Specific Challenge with Existing AWS DNS Endpoints:** A key observation from the "Notes from EoE" is that existing DNS entries were found in AWS, which subsequently prevented new Terraform deployments from creating them. This indicates a conflict where the desired state defined by Terraform could not be achieved due to pre-existing resources. The specific examples of these existing DNS entries included service names such as `ecr.eu-west-2.api.aws.`, `datasync.eu-west-2.amazonaws.com.`, `ec2.eu-west-2.amazonaws.com.`, `ec2messages.eu-west-2.amazonaws.com.`, and `api.ecr.eu-west-2.amazonaws.com.`. These entries are identified with `HostedZoneId` and `Name` fields, and crucially, an `Owner` field that specifies either an `OwningService` like `vpce.amazonaws.com` or an `OwningAccount` with a specific ID (e.g., `211125702439`). This suggests that these were likely AWS VPC Endpoints, which are managed by AWS services themselves or other accounts, leading to the conflict with independent Terraform-based deployments. The "FITFILE-AWS - Customer Checklist" further supports the existence of VPC endpoints by listing actions such as `ec2:DescribeVpcEndpoints` and `ec2:DescribeVpcEndpointServices`, which are used to inspect these types of resources.

**Broader Context: Common Concepts & Challenges in DNS Management:**

1. **DNS as a Critical Component of Distributed Systems:** DNS (Domain Name System) is fundamental for translating service names to IP addresses. In cloud-native and distributed systems, it's a critical component alongside in-house software, cloud services, network resources, load balancers, monitoring, content distribution networks, and firewalls. Kubernetes, in particular, heavily relies on DNS for service discovery within the cluster, mapping fully qualified domain names (FQDNs) to IP addresses. CoreDNS is the recommended DNS server for Kubernetes clusters. This means any pre-existing or mismanaged DNS entries can have cascading effects on application connectivity.
2. **Service Discovery in Kubernetes:** Kubernetes provides built-in DNS-based service discovery, allowing pods in the same namespace to reach a service by its short name (e.g., `webserver`) and pods in other namespaces to use a qualified name (e.g., `webserver.default`). This eliminates the need for manual IP address tracking, which is crucial given that Pod IPs are ephemeral and change upon restart. While environment variables can also be used for service discovery, DNS is preferred because it doesn't have the drawback of requiring services to be created before the pods that need to discover them.
3. **Network Architecture and IP Address Management:** AWS extensively uses its network services, including VPCs, subnets, Elastic Network Interfaces (ENIs), and Elastic IP addresses (EIPs), to enable the scaling and management of Kubernetes clusters like EKS. EIPs are static public IPv4 addresses that can be remapped to different instances, masking failures. The AWS VPC CNI (Container Network Interface) allows Kubernetes clusters to integrate directly with the AWS network, leveraging native AWS services for network event analysis, traffic management, and network traffic isolation. This deep integration means that existing network configurations, including DNS, can significantly influence new deployments.
4. **Security and Observability Challenges Related to DNS:** DNS is an attractive target for adversaries. Therefore, reviewing DNS activity logs is critical for detecting unexpected activity, such as queries to known malicious domains, unusual DNS response codes (like NXDOMAIN), or suspicious increases in DNS query volumes, which could indicate a denial-of-service (DoS) attack. Observability solutions native to Kubernetes are necessary to correlate DNS activity with other Kubernetes metadata (e.g., namespace, pod name, labels) to facilitate troubleshooting and security analysis. Without proper monitoring, identifying DNS issues that lead to failed service discovery, slow application responses, or communication failures between pods can be challenging.
5. **Importance of Upfront Planning in Complex Deployments:** The issue with existing AWS DNS entries highlights a common challenge in complex cloud deployments: the need for thorough upfront information gathering and coordination. To avoid "firefighting" during deployments, it's recommended to define all required public and private DNS records and confirm which DNS zones they should reside in, along with assigning responsibility for their creation, *before* a project begins. This proactive approach helps to anticipate and mitigate conflicts arising from pre-existing infrastructure or multi-team environments.

In summary, the existence of DNS endpoints in AWS that interfered with Terraform deployments points to a critical "common concept and challenge" in cloud-native operations: the necessity of comprehensive environmental awareness and meticulous planning, especially concerning networking and DNS, to ensure smooth and secure deployments.
