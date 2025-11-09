---
aliases: []
confidence: 
created: 2025-10-22T08:45:09Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FITFILE Technical Overview
type:
uid: 
updated: 
version:
---

## FITFILE Technical Overview

### October 2025 — Version 2.1

---

### Contents

- Architecture
- Platform
- The FITFILE Node
- FITFILE Node Component Overview
- FITConnect
- InsightFILE / HealthFILE
- Central Services
- Technology Stack
- Networking
- Data
- Deployment
- Key Requirements
- Firewall Rules / Network
- Observability / Monitoring
- Terraform
- Security & Data Safety
- Access Control
- Authentication
- Vulnerability Management
- Secure Development Lifecycle
- Container Security Runtime Threat Management
- Security Incident Event Management
- Compliance
- Support & Responsibilities

---

### Architecture

#### Platform

FITFILE offers a **decentralised platform** designed for safe, efficient access, processing, and linkage of sensitive records across data perimeters. FITFILE Nodes are placed at each Data Controller or site.

- Each FITFILE Node is a self-contained, Kubernetes-based platform (Azure/AWS) managed by GitOps (Terraform/ArgoCD).
- Storage: PostgreSQL, MinIO, MongoDB.  
  *(Comment: RM6 — I thought we didn't do MongoDB. Which NoSQL do we support?)*
- Auth0 for authentication, SpiceDB for authorisation, HashiCorp Vault for secrets.
- FITConnect: Orchestrates ingestion, workflows from files/DBs/APIs, privacy treatment using InsightFILE / HealthFILE.
- Networking: Hub-and-spoke, Zero Trust, Calico microsegmentation, private endpoints, outbound HTTPS/firewall/proxy, corporate DNS, Grafana observability.
- All traffic TLS encrypted. No raw source data leaves perimeter unless explicitly approved by Data Controller.

**Comment: RM2 — We should create a network/system-level diagram here, maybe improve an existing project diagram like NNUH with sensitive references removed?**  
**PR3R2 — Very much agreed.**  
**PR4 — Platform or cluster?**  
**RM5R4 — It's a Kubernetes cluster, serving as a platform regardless of cloud tech.**

---

#### The FITFILE Node

- Core components run inside the Node, deployed in the Data Controller environment.
- **Features:**
  1. Deploy anywhere (any cloud/infrastructure).
  2. Centralised control/deploy for auth/update.
  3. Containerised for independent function and self-healing.
  4. Secure network of Nodes for privacy-treated data exchange as needed.
  5. Cost-efficient, able to sleep when not in use.
- Data access, privacy treatment, processing (structure/harmonise/analyse/link), and an interface for project/data management.
- **Operation:**
  1. Access to its own data sources.
  2. Connection to Central Services (monitoring, auth, updates).
  3. Centralised audit log, but no customer-specific data sent.

*(Comment: RM6 — Which NoSQL do we support?)*

- Multi-controller: Node can connect to others directly or via a coordinator for distributed queries (with local auth/disclosure system controls).
- **All data at rest is encrypted; transmission uses TLS.**

---

#### FITFILE Node Component Overview

FITFILE Node = runtime components and multiple data stores.

---

##### FITConnect

Manages:

- Data supply
- Transformation (audit, lineage)
- Data output (orchestrates access for other queries)

Functions:

1. Workflow scaling (on access/privacy/linkage request).
2. Incorporates/links other processing (DQ checks, stats, structuring, harmonisation, tokenisation, opt-outs).
3. Can store data.

---

##### InsightFILE / HealthFILE

- InsightFILE = irreversibly anonymised
- HealthFILE = reversibly pseudonymised/identifiable Query Plans
- Outputs = privacy-treated, linked records from single/multiple sources
- **Linkage:** Deterministic or probabilistic (for pseudonymised/identifiable), deterministic only for anonymised

A Query Plan contains:

1. Data sources to use
2. Data elements from schema (for cohort discovery/etc.)
3. Required privacy treatment
4. Weighting of data elements

*(Comment: PR7 — Harder to follow without diagram. Upfront network diagram including FITConnect and InsightFILE/HealthFILE needed.)*  
*(Comment: OR8 — Mention data catalogue here. FITConnect = source connection, schema definition, privacy influence, data catalogue/lineage, gateway to Workflows API/data pipeline.)*

*(PR9R8 — Fully agreed. OR10 — “Coordinator” instead? RM11R10 — Worth discussing UI language. OR12 — Query Plans should have a section? RM13R12 — Move section, separate topic? OR14 — Projects should be mentioned as organisational unit for user access.)*

- Query Plans interface for scheduled jobs/web access after cluster whitelisting. Primary user interface for Node data.

---

##### Central Services

Nodes operated by several internal/externally curated services:

- Grafana (metrics)
- Auth0 (authentication, RBAC, authZ)
- HashiCorp Vault (secrets)

*(Comment: OR15 — VMWARE not supported in diagram. RM16R15 — White box covers it, also SpiceDB isn't central service. PR17R15 — VMware was for initial on-prem; Lucid chart updated to remove. Decide: leave SpicedDB or restructure. RM18R15 — Update for v3. LO19 — Box on right called Supporting Services but referenced elsewhere as “Central Services”.)*

---

### Technology Stack

#### Database/Storage

- **PostgreSQL:** Reliable, extensible open-source database
- **MinIO:** S3-compatible object storage
- **MongoDB:** NoSQL document DB

#### Platform Technologies

- **Kubernetes:** Container orchestration
- **SpiceDB:** Relationship-based access control

#### Other (Operators, GitOps, Workflow)

- **Vault Operator:** HashiCorp Vault deployment in K8s
- **ArgoCD:** GitOps CD for K8s
- **Argo Workflow:** Container orchestration

#### Networking

- **Calico Cloud/CNI:** Kubernetes/hybrid network policy
- **NGINX:** Web server/reverse proxy

#### Development

- **Storybook:** UI design/test
- **JavaScript:** Web application dev
- **NodeJS:** JavaScript runtime  
  *(Comment: LO20 — Should just be NodeJS, that's what's actually used. RM21R20 — NodeJS important for ecosystem. RM22R20 — Added both.)*
- **TypeScript:** Typed JavaScript superset
- **JSON/YAML:** Data/config files
- **Python/Rust:** Programming languages

---

### Networking

- **Topology:** Hub-and-spoke, FITFILE in dedicated spoke VNet, integrated with hub for security/connectivity/DNS
- **Isolation:** Spoke VNet peered with hub, dedicated CIDR
- **Azure CNI Overlay:** Conserves IP addresses (pod IPs from separate overlay network)
- **Calico policies:** Secure in-cluster traffic, microsegmentation

#### Subnet Allocation

| Subnet                | Recommended Size | Description                                   |
| --------------------- | ---------------- | --------------------------------------------- |
| System Node Pool      | /28 (16 IPs)     | Core K8s system components                    |
| Workload Node Pool    | /28 (16 IPs)     | Application workloads/services                |
| Management Jumpbox    | /29 (8 IPs)      | VM for secure admin access                    |
| DNS Resolver Endpoint | /28 (16 IPs)     | Optional; delegated for DNS outbound endpoint |

#### Traffic Routing and Security

**Zero Trust:**  
Outbound egress forced through central firewall.

- **Forced Tunnelling/UDR:** Route table applied to prevent unauthorised internet paths; default route via firewall.
- **HTTPS Proxy Integration (optional):** For deep inspection, route outbound HTTPS through corporate proxy.

#### Customer Prerequisites Checklist

**Network resources needed:**

1. Hub-Spoke connectivity (hub VNet w/firewall, on-prem network connectivity, VNet peering).
2. Non-overlapping CIDR block for spoke VNet, private IP for firewall.
3. IP for corporate DNS (reachable from spoke VNet).
4. Central firewall rules must allow required outbound traffic.

---

### Security Posture Summary

- All outbound traffic inspected centrally
- Kubernetes API endpoint private to site network
- In-cluster microsegmentation limits lateral movement
- Integrated DNS prevents exfiltration and ensures reliable name resolution

---

### Data

#### Data Access Key Components

- **FITConnect** orchestrates access to multiple data sources
- Data source: connection + schema (physical/semantic types, IDs, relationships)
- Supported sources:
  1. Static files (uploaded, encrypted in datastore)
  2. Live DBs (MySQL, PostgreSQL, MSSQL, Elasticsearch)
  3. Other stores (custom/client, data warehouse, additional Node sources)
- FITConnect can combine data across providers with appropriate access controls.

---

#### Data Privacy Key Components

- Data loaded into a pipeline to apply privacy treatment set via InsightFILE/HealthFILE.
- Pipeline initialised after data query request.

---

##### Privacy Treatment Protocol

Techniques include:

- Aggregation
- Generalisation
- k/Km-anonymity
- l-diversity
- t-closeness
- Perturbation
- Rounding
- Suppression
- Sampling
- Differential privacy
- Noise addition
- Permutation

*Protocol is iterative—monitors reid risk, ensures privacy threshold met before producing result with lowest analytic utility loss.*

---

##### Weighting Factors

- Alternate results selectively maintain integrity for key elements using assigned weights/coefficient.
- The chosen result minimises transformations for highest-weighted elements.

---

#### Data Linkage Key Components

- Linkage in identifiable, pseudonymised, anonymised format.
- **InsightFILE/HealthFILE** labels *not visible in platform*, used only for describing linkage capabilities.

*(Comment: OR23 — Separating by these names is silly as RBAC grants access by query plan, not product label. RM24R23 — If undiscernible, don't reference. PR25R23 — Option to re-incorporate into product or clarify. OR26 — Just “non-deterministic”; RM27R26/PR28R26 — Previous wording used for clarity. OR29 — Confirm “straight match” for proof. RM30R29 — Added. OR31 — FITtokens use HMAC-SHA256 w/shared secret, deployed to all Nodes. RM32R31 — Added.)*

**InsightFILE (Anonymisation):**

- Creates non-deterministic encrypted cipher (FITanon) with one-off random variables, using Zero Knowledge Proof (ZKP).
- Each generation differs, even with same data.

**HealthFILE (Pseudonymisation):**

- Creates deterministic identifier (FITtoken) with HMAC-SHA256 and shared secret.
- Enables linking/re-identification by regenerating token.
- Linked datasets become usable as sources again, subject to further privacy thresholds.

---

### Querying Data

- Query Plan data stored with lineage/metadata.
- Access options:
  1. Web UI: view/download as CSV/JSON (preserve structure/metadata)
  2. RESTful API, BI tools, other systems  
     *(Comment: OR33 — Consumed via RESTful API. RM34R33 — Added.)*

- Multiple runs = history available for integrity

---

### Deployment

- Node deployed in Data Controller’s GDPR perimeter/IT estate. All access, processing, privacy treatment within perimeter.
- Usual cloud hosts: Azure/AWS (On-premises is fallback for non-cloud-ready sites).
- Member tenant setup for Node deployment.
- Terraform scripts describe full environment, spinning up K8s cluster with all components.
- High security, resilience, scalability, and ease of update.
- K8s API always private, requiring Jumpbox/Bastion for config.

*(Comment: RM35 — Needs tidying/rethink. OR36R35 — Diagram for deployment/GitOps model? RM37R35 — Can't see diagram, should be added. PR38R35 — End-of-section diagram outdated, Lucid chart intro. OR39 — Language around "sub-tenant" is confusing; suggest Subscription/Resource Group/AWS Account, etc. RM40R39 — Member tenant as child to owner tenant. RM41R39 — Section is Azure-focused, not AWS. OR42 — Private K8s API = always requires Jumpbox/Bastion for deployment. RM43R42 — Added.)*

---

#### Key Requirements

**Cloud hosting subscription must provide:**

- Kubernetes Service (AKS/EKS)
- Compute (VM/scale sets)
- Block Storage/Disks
- Key Management
- Spot VMs
- IAM
- Load balancers (Route53/Azure DNS, Elastic Load/Azure DNS)
- Backup
- Security Centre

*Move section to purely focus on GitOps tooling update/patch model within cluster, not internal pipeline.*  
*(OR44/R44 — Needs discussion.)*  
*Headers made index page look bad (RM46). PR47 — Font style inconsistent; use here for sub-headings.*

##### AWS/Azure Operational Services, Security Hub, Defender, GuardDuty, CloudTrail, Firewall, Macie, DNS, Web App Firewall, Backup Manager

---

#### Deployment Requirements

- Service Principal/IAM account in subscription for 1-button infra deployment.
- Domain naming conventions:
  - Clientname.FITFILE.NET (hosted by FITFILE)
  - FITFILE.clientname.co.uk (hosted by Data Provider)
- Connectivity: Outbound HTTPS (Auth0, Grafana, GitOps, Vault, platform updates). Inbound VPN (ZTNA).
  - Virtual Desktop: Elevate perms for deployment, revert to least-privileged for ops.

---

#### Firewall Rules / Network

**Kubernetes Cloud Networking:**

- VPC/VNet CIDR: `10.0.0.0/16` (defined by Terraform; modifiable)
- Pod CIDR: `10.244.0.0/16` (internal K8s)
- Firewall: Require TCP443/HTTPS outbound; no non-standard ports.
- FITFILE can provide whitelisting URL list for outbound firewall.

#### Observability / Monitoring

- Central management, real-time alerting, health tracking:
  - Platform Scaling Events
  - Sanitised Logs
  - Node Operations
  - Container Availability

---

#### Terraform

- **GitOps IaC model with Terraform:**
  - All changes are version-controlled, peer-reviewed, auditable.
  - Centralised state: managed service = consistent config, fast incident response.
  - Removes Data Controller’s operational burden while maintaining transparency/traceability.
- Site sets up isolated Azure subscription/AWS account for billing/access control.
- Azure Contributor/AWS equivalent recommended.
- For stricter governance, roles can be scoped more tightly.

Infrastructure can be reviewed, changes go through CAB.

##### Terraform Cloud Service Principal Custom Role

- Requires permissions to provision/manage resources.
- Must be able to assign roles to managed identities.
- Least-privilege principle: only necessary permissions for predefined roles.

*(Comment: RM48 — Remove base implementation talk, focus on the consideration.)*

---

### Security and Keeping Data Safe

- **Principle:** Security, privacy, compliance by design and default.
- **Federated solution:** Hosts cluster, compliance with Controller/site network security.

**Data accessed at source:**

1. Encrypted connections
2. Encrypted at rest
3. Encrypted in transport (min HTTPS 1.2)

- Auth0: central IDP, adaptive security
- Authorisation: local per Node (SpiceDB, Google Zanzibar), RBAC/attribute-based controls
- User roles set by project, fine-grained perms for query execution/editing
- Secrets/keys: stored in HashiCorp Vault, per-customer namespaces to isolate

*(Comment: OR49 — Secrets are stored per customer namespace to isolate.)*

*(Comment: OR50 — Robin requested to replace the Authentication/AuthZ sections above.)*

---

#### Access Control

- **Goals:**
  1. Strong, centralised authentication
  2. Fine-grained, contextual authorisation (local enforcement)
  3. Auditable, least-privilege access

**Implemented by:**

- Auth0 (central IdP)
- SpiceDB (fine-grained authZ via Google Zanzibar model)

#### Authentication

- Central Auth0 tenant holds users/services for FITFILE mesh.
- Each deployment: UI application client & API audience created in Auth0.
- Trust boundaries (aud claim in tokens); explicit cross-deployment API access; user = OIDC Auth Code PKCE, services = OAuth2 Client Credentials.
- JWT tokens (short lived), verified on each API call.

#### Authorisation

- Each deployment: dedicated SpiceDB instance.
- Permission model: RBAC+PBAC for Tenant/Project; caveats/policies for resource-level access.
- Data Disclosure = policy: access only after approval.
- Real-time perms eval; immediate effect across network (including Project access removal).

---

#### Vulnerability Management

- Trivy and COPA in release pipeline
  - Trivy: container/image vulnerability scanning
  - COPA: manage software bill of materials (SBOM)
    *(Comment: OR51 — Not widely deployed, could remove. LO52R51 — Used w/Trivy, not active now but could patch CVEs. PR53R51 — Keep in text, decide on more use.)*
- Results reviewed, ensure no critical vulnerabilities

#### Secure Development Lifecycle

- SonarQube in CI/CD pipeline
  - Automated code/static analysis for vulnerability and quality

#### Container Security Runtime Threat Management

- **Calico Cloud:** microservice/container comms security, Zero Trust architecture

#### Security Incident Event Management

- Azure Sentinel for threat detection, response: SIEM, ML/AI for real-time anomaly/threat reporting

---

#### Compliance

- ISO27001:2022, ISO27017:2015, ISO27018:2019
- Cyber Essentials / Plus
- NHS DSPT / NHSD Cloud Security
- SOC2, SOC3, HIPAA

FITFILE Platform: Scalable Data Access, Privacy, Linkage

HCP Terraform Infrastructure

HCP Vault Secure Secrets Management

Auth0 Platform Identity Management

Grafana Observability Log Management

Azure Sentinel SIEM Platform

---

### Support & Responsibilities

#### Support Service Commitments

- **Operating Hours:** UK business hours (9am–5pm Mon-Fri, excl. UK bank holidays)
- **Incident/Question Reporting:** Via platform or support email.
- **Response Time Objectives:** By priority (General/Critical High); timeframes agreed.

#### Critical/High Priority Incidents

- Issues impacting data confidentiality/integrity/linkage
- Breaches, public confidence/reputation, major interruptions

#### Availability Target

- Managed with target uptime agreed beforehand.

#### Responsibilities

- Shared responsibility model: FITFILE reduces Data Controller workload.
- Data Controller: provide data to platform, ensure host provider availability.

*(Comment: PR56 — Changed “Data Provider” for consistency; generalised for Consumers like EoE SDE.)*

---

#### Deployment Uptime & Availability

- User Onboarding
- User Management
- Networking & Change Management
- Security Monitoring
- Data & Updates

FITFILE provides PM-guided onboarding; ready to use within minutes of access.  
Change management in partnership with Controllers/sites for best outcomes.
