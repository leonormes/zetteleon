---
aliases: []
confidence: 
created: 2025-03-06T09:39:24Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [IAM]
title: Plan for Security Posture
type: plan
uid: 
updated: 
version:
---

## Plan for Security Posture

[Plan for Security Posture - Confluence](https://fitfile.atlassian.net/wiki/spaces/~633ae2b9fedc6169aed8f601/pages/1593442656/Plan+for+Security+Posture)

Our security posture is our organization's ability to protect from and respond to security threats. The common principles used to define a security posture are **confidentiality**, **integrity**, and **availability**, known collectively as CIA.

- Confidentiality
- Integrity
- Availability

There are 4 layers to cloud native systems security best practices.

- Cloud.
- Cluster.
- Container.
- Code.

This is known as the 4c security model

We can think of it in defence in depth

- **Physical Security**
    - I believe this is not relevant as the system is either on-prem and so the client controls the hardware, or in Azure, who look after the physical security.
- **Identity and Access**
    - At this layer, it's important to:
        - Control access to infrastructure and change control.
        - Use single sign-on (SSO) and multifactor authentication.
        - Audit events and changes.
    - The identity and access layer is all about ensuring that identities are secure, access is granted only to what's needed, and sign-in events and changes are logged.
- **Perimeter**
    - At this layer, it's important to:
        - Use DDoS protection to filter large-scale attacks before they can affect the availability of a system for users.
        - Use perimeter firewalls to identify and alert on malicious attacks against your network.
    - At the network perimeter, it's about protecting from network-based attacks against your resources. Identifying these attacks, eliminating their impact, and alerting you when they happen are important ways to keep your network secure.
- **Network**
    - At this layer, it's important to:
        - Limit communication between resources.
        - Restrict inbound internet access and limit outbound access where appropriate.
        - Implement secure connectivity to on-premises networks.
        - Deny by default.
    - At this layer, the focus is on limiting the network connectivity across all your resources to allow only what's required. By limiting this communication, you reduce the risk of an attack spreading to other systems in your network.
- **Compute**
    - At this layer, it's important to:
        - Secure access to virtual machines.
        - Implement endpoint protection on devices and keep systems patched and current.
        - Malware, unpatched systems, and improperly secured systems open your environment to attacks. The focus in this layer is on making sure that your compute resources are secure and that you have the proper controls in place to minimize security issues.
- **Application**
    - At this layer, it's important to:
        - Ensure that applications are secure and free of vulnerabilities.
        - Store sensitive application secrets in a secure storage medium.
        - Make security a design requirement for all application development.
        - Integrating security into the application development lifecycle helps reduce the number of vulnerabilities introduced in code. Every development team should ensure that its applications are secure by default.
- **Data**
    - In almost all cases, attackers are after data:
        - Stored in a database.
        - Stored on disk inside virtual machines.
        - Stored in software as a service (SaaS) applications, such as Office 365.
        - Managed through cloud storage.
        - Anyone who stores and controls access to data is responsible for ensuring that it's properly secured. Often, regulatory requirements dictate the controls and processes that must be in place to ensure the confidentiality, integrity, and availability of the data.

### List Ideas

- Prevent Access to KubeAPI server
    - The Kubernetes API uses two HTTP ports, designated as localhost and secure port, to communicate. The localhost port does not require TLS, so requests made through this port will avoid the authentication and authorization components. Therefore, you must make sure this port is not enabled outside of the Kubernetes cluster’s test configuration.
- Enforce TLS Between Cluster Components.
- Isolate the Cluster and API with Proper Configurations.
- Use Admission Controllers and Network Policy.
- Use Verified Images with Proper Tags.
- [Apply Pod Security Standards at the Cluster Level](https://kubernetes.io/docs/tutorials/security/)
    - [Apply Pod Security Standards at the Cluster Level](https://kubernetes.io/docs/tutorials/security/cluster-level-pss/)
    - [Apply Pod Security Standards at the Namespace Level](https://kubernetes.io/docs/tutorials/security/ns-level-pss/)
    - [Restrict a Container's Access to Resources with AppArmor](https://kubernetes.io/docs/tutorials/security/apparmor/)
    - [Restrict a Container's Syscalls with seccomp](https://kubernetes.io/docs/tutorials/security/seccomp/)
- Don’t keep secrets in an environment variable.
    - It’s a good practice to have your secret outside an environment variable. The reason for that is that other parts of your system can access environment variables. Use secrets as files or leverage secretKeyRef to minimize threats. You can also leverage Azure Key Vault service to store and access your secrets securely.
- Develop a rolling update strategy
    - To keep your AKS security tight, build a rolling update strategy. Rolling updates allow deployment updates to minimize application downtime by updating pod instances with new ones incrementally.
- Double check unsafe /proc mount
    - Containers with unsafe /proc mount (procMount=Unmasked) let others bypass the default masking behavior of the container runtime. If you set your Kubernetes container with Unmasked /proc mount type, you might expose the host information to that container
- Disable NET_RAW
    - If your containers don’t drop the NET_RAW capability, you might let in various networking exploits from inside the cluster. To boost your AKS security, take advantage of Policy Enforcement solutions such as:
        - Open Policy Agents
        - Kyverno
        - Kubernetes Pod Security admission controller.
- Avoid sharing the host’s IPC or network namespace.
- Avoid using the root file system for container security
    - Are your containers running without a read-only root file system? Expect security issues to arise soon.
- Use Kubernetes Role-Based Access Control (RBAC).
    - Using Kubernetes RBAC and Azure AD-integration, you can secure the API server and provide the minimum permissions required to a scoped resource set, like a single namespace. You can grant different Azure AD users or groups different Kubernetes roles. With granular permissions, you can restrict access to the API server and provide a clear audit trail of actions performed.
- Boost authentication and authorization.
    - Another best practice is integrating Kubernetes with a third-party authentication provider to get an extra layer of security, like multi-factor authentication.
- Upgrade AKS node images
    - I-Upgrade Azure Kubernetes Service (AKS) node images - Azure Kubernetes Service
- AKS: Disable local accounts with Terraform
- Rotate cluster certificates – Rotate encryption keys
- Address Azure best practises
- Configure securityContext correctly. Snyk Article.
- Restrict access to Instance Metadata API
    - Add a network policy in all user namespaces to block pod egress to the metadata endpoint.
- Secure container access to resources
    - Limit access to actions that containers can perform. Provide the least number of permissions, and avoid the use of root access or privileged escalation.
        - For even more granular control of container actions, you can also use built-in Linux security features such as AppArmor and seccomp.
- Define Linux security features at the node level.
- Implement features through a pod manifest.
- Disable local accounts with terraform
    - When deploying an AKS cluster, even if you configure RBAC or AAD integration, local accounts will be enabled by default. This means that, given the right set of permitions, a user will be able to run the az get-credentials command with the --admin flag which will give you a non-audtibale access to the cluster.

### From OWASP Cheat Sheet Kubernetes Security

- Kubernetes Security - OWASP Cheat Sheet Series Securing Kubernetes hosts
- Securing Kubernetes components
- Control network access to sensitive ports¶
- Kubernetes Security Best Practices: Build Phase
- Kubernetes Security Best Practices: Deploy Phase
- Kubernetes Security Best Practices: Runtime Phase
- Separate and Firewall your etcd Cluster
- statically analyse YAML
- Defender for Endpoint
- Ensure that your virtual network deployment aligns to your enterprise segmentation strategy defined in the GS-2 security control. Any workload that could incur higher risk for the organization should be in isolated virtual networks.

Secure cloud services by establishing a private access point for resources. You should also disable or restrict access from public networks when possible.

Deploy private endpoints for all Azure resources that support the Private Linkfeature to establish a private access point for the resources. Using Private Link will keep the private connection from routing through the public network.

Deploy a firewall to perform advanced filtering on network traffic to and from external networks. You can also use firewalls between internal segments to support a segmentation strategy. If required, use custom routes for your subnet to override the system route when you need to force the network traffic to go through a network appliance for security control purposes.

Use Azure Firewall to provide fully stateful application layer traffic restriction (such as URL filtering) and/or central management over a large number of enterprise segments or spokes (in a hub/spoke topology).

Use network intrusion detection and intrusion prevention systems (IDS/IPS) to inspect the network and payload traffic to or from your workload.

Deploy distributed denial of service (DDoS) protection to protect your network and applications from attacks.

Deploy a web application firewall (WAF) and configure the appropriate rules to protect your web applications and APIs from application-specific attacks.

Detect and disable insecure services and protocols at the OS, application, or software package layer. Deploy compensating controls if disabling insecure services and protocols are not possible.

Use Microsoft Sentinel’s built-in Insecure Protocol Workbook to discover the use of insecure services and protocols such as SSL/TLSv1, SSHv1, SMBv1, LM/NTLMv1, wDigest, Unsigned LDAP Binds, and weak ciphers in Kerberos. Disable insecure services and protocols that do not meet the appropriate security standard.

For lightweight connectivity between site-to-site or point-to-site, use Azure virtual private network (VPN) to create a secure connection between your on-premises site or end-user device to the Azure virtual network.

Ensure that Domain Name System (DNS) security configuration protects against known risks

Use Linux Security Features and PodSecurityPolicies.

- capabilities
- SELinux
- AppArmor
- seccomp-bpf

Run Service Mesh

Scan Images and Run IDS (Intrusion Detection System)

Run Containers as a Non-Root User

Use pod security context to limit access to processes and services or privilege escalation

Authenticate with other Azure resources using Azure Active Directory workload identities

Request and retrieve credentials from a digital vault such as Azure Key Vault

Add a network policy in all user namespaces to block pod egress to the metadata endpoint

Limit access to actions that containers can perform. Provide the least number of permissions, and avoid the use of root access or privileged escalation.

Kubernetes may deprecate APIs (like in version 1.16) that your workloads rely on. When bringing new versions into production, consider using multiple node pools on separate versions and upgrade individual pools one at a time to progressively roll the update across a cluster. If running multiple clusters, upgrade one cluster at a time to progressively monitor for impact or changes.

### Security Context Settings

- You Should Understand
    - runAsNonRoot
    - runAsUser / runAsGroup
    - seLinuxOptions
    - seccompProfile
    - privileged / allowPrivilegeEscalation
    - capabilities
    - readonlyRootFilesystem
    - procMount
    - fsGroup / fsGroupChangePolicy
    - sysctls
- Handle Linux Node Reboots With Kured - Azure Kubernetes Service
    - [Kured](https://kured.dev/) is an open-source project by Weaveworks. Please direct issues to the kured GitHub. Additional support can be found in the Slack channel.
    - Some security updates, such as kernel updates, require a node reboot to finalize the process. A Linux node that requires a reboot creates a file named /var/run/reboot-required. This reboot process doesn't happen automatically.
    - You can use your own workflows and processes to handle node reboots, or use kured to orchestrate the process. With kured, a DaemonSet is deployed that runs a pod on each Linux node in the cluster. These pods in the DaemonSet watch for existence of the /var/run/reboot-required file, and then initiate a process to reboot the nodes.
- Security Control Network Security
    - Security principle: Ensure that your virtual network deployment aligns to your enterprise segmentation strategy defined in the GS-2 security control. Any workload that could incur higher risk for the organization should be in isolated virtual networks.
    - Security principle: Secure cloud services by establishing a private access point for resources. You should also disable or restrict access from public networks when possible.
    - Azure guidance: Deploy private endpoints for all Azure resources that support the Private Link feature to establish a private access point for the resources. Using Private Link will keep the private connection from routing through the public network.
    - Security principle: Deploy a firewall to perform advanced filtering on network traffic to and from external networks. You can also use firewalls between internal segments to support a segmentation strategy. If required, use custom routes for your subnet to override the system route when you need to force the network traffic to go through a network appliance for security control purposes.
    - Azure guidance: Use Azure Firewall to provide fully stateful application layer traffic restriction (such as URL filtering) and/or central management over a large number of enterprise segments or spokes (in a hub/spoke topology).
    - Security principle: Use network intrusion detection and intrusion prevention systems (IDS/IPS) to inspect the network and payload traffic to or from your workload. Ensure that IDS/IPS is always tuned to provide high-quality alerts to your SIEM solution.
    - For more in-depth host level detection and prevention capability, use host-based IDS/IPS or a host-based endpoint detection and response (EDR) solution in conjunction with the network IDS/IPS.
    - Security principle: Deploy distributed denial of service (DDoS) protection to protect your network and applications from attacks.
    - Security principle: Deploy a web application firewall (WAF) and configure the appropriate rules to protect your web applications and APIs from application-specific attacks.
    - Security principle: When managing a complex network environment, use tools to simplify, centralize and enhance network security management.
    - Security principle: Detect and disable insecure services and protocols at the OS, application, or software package layer. Deploy compensating controls if disabling insecure services and protocols are not possible.
    - Azure guidance: Use Microsoft Sentinel’s built-in Insecure Protocol Workbook to discover the use of insecure services and protocols such as SSL/TLSv1, SSHv1, SMBv1, LM/NTLMv1, wDigest, Unsigned LDAP Binds, and weak ciphers in Kerberos. Disable insecure services and protocols that do not meet the appropriate security standard.
    - Security principle: Use private connections for secure communication between different networks, such as cloud service provider datacenters and on-premises infrastructure in a colocation environment.
    - Azure guidance: For lightweight connectivity between site-to-site or point-to-site, use Azure virtual private network (VPN) to create a secure connection between your on-premises site or end-user device to the Azure virtual network.
    - For enterprise-level high performance connection, use Azure ExpressRoute (or Virtual WAN) to connect Azure datacenters and on-premises infrastructure in a co-location environment.
    - Security principle: Ensure that Domain Name System (DNS) security configuration protects against known risks

Check Pods for securityContext

**Text Snippet**

```sh
kubectl get pods --all-namespaces -o go-template --template='{{range .items}}{{"pod: "}}{{.metadata.name}}
    {{if .spec.securityContext}}
      PodSecurityContext:
        {{"runAsGroup: "}}{{.spec.securityContext.runAsGroup}}                               
        {{"runAsNonRoot: "}}{{.spec.securityContext.runAsNonRoot}}                           
        {{"runAsUser: "}}{{.spec.securityContext.runAsUser}}                                 {{if .spec.securityContext.seLinuxOptions}}
        {{"seLinuxOptions: "}}{{.spec.securityContext.seLinuxOptions}}                       {{end}}
    {{else}}PodSecurity Context is not set
    {{end}}{{range .spec.containers}}
    {{"container name: "}}{{.name}}
    {{"image: "}}{{.image}}{{if .securityContext}}                                      
        {{"allowPrivilegeEscalation: "}}{{.securityContext.allowPrivilegeEscalation}}   {{if .securityContext.capabilities}}
        {{"capabilities: "}}{{.securityContext.capabilities}}                           {{end}}
        {{"privileged: "}}{{.securityContext.privileged}}                               {{if .securityContext.procMount}}
        {{"procMount: "}}{{.securityContext.procMount}}                                 {{end}}
        {{"readOnlyRootFilesystem: "}}{{.securityContext.readOnlyRootFilesystem}}       
        {{"runAsGroup: "}}{{.securityContext.runAsGroup}}                               
        {{"runAsNonRoot: "}}{{.securityContext.runAsNonRoot}}                           
        {{"runAsUser: "}}{{.securityContext.runAsUser}}                                 {{if .securityContext.seLinuxOptions}}
        {{"seLinuxOptions: "}}{{.securityContext.seLinuxOptions}}                       {{end}}{{if .securityContext.windowsOptions}}
        {{"windowsOptions: "}}{{.securityContext.windowsOptions}}                       {{end}}
    {{else}}
        SecurityContext is not set
    {{end}}
{{end}}{{end}}'
```

**Links:**
- [kubernetes_security](<300_Documentation/TF k8s Deployment Docs/security/kubernetes_security.md>)
- [pod sys_admin](<200_Projects/K8s/pod sys_admin.md>)
- [focus_on_emergence](<focus_on_emergence.md>)

This command will list all currently deployed manifest misconfigurations.

You will need GitHub - zegl/kube-score: Kubernetes object analysis with recommendations for improved reliability and security

```sh
kubectl api-resources --verbs=list --namespaced -o name\
xargs -n1 -I{} bash -c "kubectl get {} --all-namespaces -oyaml && echo ---"
kube-score score -
```
