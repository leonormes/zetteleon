---
aliases: []
confidence: 
created: 2025-12-09T09:30:44Z
epistemic: 
last_reviewed: 
modified: 2025-12-09T09:35:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Azure Deployment Readiness Checklist
type: 
uid: 
updated: 
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
