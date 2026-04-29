---
created: 2026-04-28T12:35:01+00:00
modified: 2026-04-28T12:48:01+00:00
title: Work Required for Deployment NUH
---

---

Based on the technical discovery documents and meeting notes, the following summary outlines the required work and outstanding questions for the Nottingham University Hospitals (NUH) deployment.

---

## Work Required for Deployment

The deployment strategy has evolved from a "Fully On-Premise" model toward a Hybrid approach to balance NUH's security requirements with FITFILE's technical standards.

### 1. Infrastructure Provisioning

- Server Build: NUH is to provision a hardened Ubuntu 24.04 VM using their standard server build form.
- Resource Allocation: The server must be specced to handle memory-intensive Kubernetes orchestration and computational workflows.
- Kubernetes Setup: NUH has proposed setting up a VM with Kubernetes already installed, allowing FITFILE to then install their Node within that environment.

### 2. Networking and Connectivity

- VPN/Direct Link: As of April 2026, the current plan is to use EE-SDE AWS hosting to support the FITFILE platform, connecting back to the NUH on-premises database via VPN.
- Implementation Meeting: A meeting is scheduled for 01/05/2026 to define the specific network permissions and provisioning required on both the SDE and NUH sides.

### 3. Data Integration and Governance

- Initial Data Source: To bypass overstretched digital teams, the initial node will connect to NUH's existing pseudonymised research data (SAT, COSD).
- Cyber Sign-off: The NUH Cyber team (Risk Owner: Andy Callow) must assess and sign off on how the SDE will process data.
- Contractual Status: The draft Combined DCA/DSA (Data Connection/Sharing Agreement) has been sent to the Trust board for final feedback.

---

## Outstanding Questions for NUH

While some technical details are captured in the discovery log, several operational questions remain "Open" or require specific NUH input:

### Change Management and Support

- CAB Process: What is the specific meeting cadence and typical lead time for approving Change Authorisation Board (CAB) requests?
- Escalation: What is the internal NUH escalation process for technical incidents?

### Monitoring and Alerting

- Observability: Does NUH require optional observability into the FITFILE Node? If so, which specific metrics (e.g., Uptime, Response time) are required?
- Alert Routing: Should downtime alerts be routed via a specific service desk or an alternative procedure?

### Backup and Recovery

- RTO/RPO: What are the specific Recovery Time Objective (maximum acceptable downtime) and Recovery Point Objective (maximum acceptable data loss) requirements for this node?
- Retention: What are the required backup frequencies and retention periods for the cluster?

### Maintenance

- Windows: Are there specific maintenance windows FITFILE must adhere to for updates or support?

---

Next Step: The implementation team (RM and Keiran) will meet on 1st May 2026 to finalise these requirements before the all-parties kick-off meeting.

Would you like me to draft a follow-up email to the NUH technical team to prompt for these missing details?

Meeting prep: key confirmations to close on Friday

1. Architecture and scope
- Confirm "Hybrid" split: which components in EE‑SDE (AWS) vs on‑prem NUH
- Data boundaries: source is pseudonymised research data (SAT, COSD); what—if any—PHI touches the node
- Target pilot scope and acceptance criteria

1. Kubernetes/compute environment
- If NUH supplies K8s: supported version, cluster access model (namespace + RBAC), default ingress, network policies, Pod Security level, admission controllers (OPA/Gatekeeper), container runtime
- Storage: available storage classes (RWO/RWX), snapshot support, baseline IOPS
- Image supply: registry allow‑list, image pull secrets, image signing policy (e.g., cosign)
- Recommended VM sizing (if we install K8s): baseline 8 vCPU / 32–64 GB RAM / 500 GB fast SSD (adjust if you have stricter figures)

1. Networking
- VPN type and endpoints (IPsec policy, NAT, CIDRs), tunnel health checks, change window for cutover
- Egress allow‑list: SDE endpoints, container registries, OS repos, time/DNS/CRL/OCSP
- DNS/NTP/proxy settings; firewall ownership and change lead time

1. Security, governance, and change
- CAB cadence and typical lead time; emergency/break‑glass route
- Cyber sign‑off owner (noted: Andy Callow) and expected sign‑off date
- OS hardening baseline (e.g., CIS), endpoint protection, vuln scanning
- Secrets: how we'll manage (K8s secrets vs Sealed Secrets/SOPS or external Vault)
- TLS/PKI: who issues and renews certs; internal vs public CA

1. Observability, backup, and support
- Logs/metrics destination (NUH SIEM?); required SLOs/metrics; who gets alerts
- RPO/RTO, backup frequency/retention; what must be restorable (volumes, config)
- Support and escalation contacts; standard maintenance windows

1. Data and contracts
- Location and access pattern for SAT/COSD; interface details
- DCA/DSA status with Trust board; any outstanding comments and timelines

Pre‑reqs to request before install

- Environment sheet: VM/K8s specs, storage class, ingress, RBAC contacts
- Network diagram and target CIDRs/ports; VPN parameters
- Security baseline doc; CAB template; service desk routing and on‑call contacts
- Dataset access details (SAT, COSD): endpoints, credentials path, data dictionaries (if available)

Draft email to NUH technical team (ready to send)

Subject: NUH × FITFILE—Pre‑reqs and agenda for Hybrid Node deployment (Friday)

Hi <Name/Team>,

Ahead of Friday's session, here's a concise list of confirmations to unblock the Hybrid deployment (EE‑SDE ↔ NUH via VPN) and a proposed agenda.

Please confirm or provide:

- Infrastructure/Kubernetes
  - Will NUH provide a Kubernetes namespace? If so: version, ingress controller, network policies, admission controls, available storage classes (RWO/RWX, snapshots), and container runtime.
  - If VM route: Ubuntu 24.04 hardened build; recommended sizing (we propose 8 vCPU, 32–64 GB RAM, 500 GB SSD); any EDR/AV agents and CIS baseline in use.
  - Container image policy: registry allow‑list, image pull secret format, signing/verification requirements.
- Networking
  - VPN type and parameters (IPsec profile, endpoints, NAT/CIDRs), change window for implementation.
  - Egress allow‑list (SDE endpoints, container registries, Ubuntu repos, DNS/NTP/CRL/OCSP).
  - DNS/NTP/proxy settings and ownership of firewall rules.
- Security & Governance
  - CAB cadence and typical lead time; emergency change route.
  - Cyber sign‑off owner (we have Andy Callow as risk owner) and target date.
  - Secrets and TLS: preferred patterns (K8s secrets/Sealed Secrets/SOPS or external Vault), cert issuance path (internal CA vs public).
  - Vulnerability scanning and endpoint protection expectations.
- Observability, Backup, Support
  - Required metrics/logs and where to route them (e.g., NUH SIEM); alert recipients.
  - RPO/RTO targets; backup frequency and retention; scope of restore (volumes/config).
  - Support contacts and escalation; standard maintenance windows.
- Data Integration & Contracts
  - Initial data sources: SAT/COSD location and access method.
  - Status of the combined DCA/DSA with the Trust board; any pending comments.

Proposed agenda for Friday

1. Confirm architecture boundaries and data flow
2. Network/VPN plan and allow‑lists
3. K8s/VM environment readiness and storage
4. Security, CAB, and secrets/TLS approach
5. Observability, backup/restore, and support model
6. Next steps, owners, and dates

If you can share the above confirmations or docs by EOD Thursday, we can finalize the deployment plan in the meeting and agree timelines.

Thanks very much,

<Your name>

<Title>
<Contact details>

Would you like me to send this as‑is, or tailor it to specific recipients and add any attachments (e.g., a one‑page data‑flow diagram and port list)?
