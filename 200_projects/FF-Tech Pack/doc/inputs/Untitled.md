---
aliases: []
confidence: 
created: 2025-10-18T10:38:17Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:28Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Untitled
type:
uid: 
updated: 
version:
---

## Technical Overview

Standard template for

FITFILE Node Deployments

Proposed headings (3 levels displayed in table of contents)

Should it be organised by project phases, subjects, or mixed, for example:

- Architecture > Network > Security or
- Security > Network

### Overview

How this document sits in the process

- O
- Outputs / artefacts (design docs, etc)

### Architecture

#### System

- O

#### Networking

#### Application

#### Data

### Security and Compliance

- Vulnerability management
- Secure Development Lifecycle
- Container security and runtime threat management
- Security Incident and Event Management
- Compliance

### Deployment

- Key requirements / Dependencies
- Infrastructure
- Networking

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

1

---

## Technical Overview

- O
- O
- O
- Data
- Considerations / Questions?
- Firewall rules
- Terraform

### Observability and Monitoring

### Operations and Lifecycle Management

- O
- Support service commitments
- Monitoring

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

2

---

## Technical Overview

### Contents

|                                                                                                                                                           |                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| "Overview"                                                                                                                                                | "5"                     |
| "High Level Architecture"                                                                                                                                 | "5"                     |
| "The FITFILE Node..."                                                                                                                                     | "5"                     |
| "FITFILE Node Component Overview"                                                                                                                         | "6"                     |
| "Technology Stack"                                                                                                                                        | "8"                     |
| "Data Data Data Data Using Data Networking. Access Key Components. Privacy - Key Components Linkage Key Components Datasets from Query Plans... Flows..." | "10 10 11 .13 14 15 16" |
| "Network Architecture"                                                                                                                                    | "16"                    |
| "Virtual Network (VNet) Design"                                                                                                                           | "16"                    |
| "Subnet Allocation"                                                                                                                                       | "16"                    |
| "Traffic Routing and Security"                                                                                                                            | ".17"                   |
| "Forced Tunnelling with User-Defined Routes (UDR)"                                                                                                        | "17"                    |
| "HTTP/S Proxy Integration (Optional)"                                                                                                                     | "17"                    |
| "Customer Prerequisites Checklist"                                                                                                                        | "17"                    |
| "Security Posture Summary."                                                                                                                               | "18"                    |
| "Deployment."                                                                                                                                             | "19"                    |
| "Overview."                                                                                                                                               | "19"                    |
| "Key Requirements"                                                                                                                                        | ".20"                   |
| "Firewall Rules & Network."                                                                                                                               | "22"                    |
| "Observability & Monitoring."                                                                                                                             | "22"                    |

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

3

---

## Technical Overview

|                                                                                                                                                                                                                        |                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| "Terraform..."                                                                                                                                                                                                         | ".23"                       |
| "Security and Keeping Data Safe Vulnerability Management Secure Development Container Security & Security Incident & Event Compliance Support and Responsibilities Lifecycle. Runtime Threat Management. Management. " | ".25 26 .26 26 .26 .27 .28" |
| "Support Service Commitments."                                                                                                                                                                                         | ".28"                       |
| "Operating Hours"                                                                                                                                                                                                      | "28"                        |
| "Response Time Objectives"                                                                                                                                                                                             | "28"                        |
| "Critical / High Priority Incident Classification"                                                                                                                                                                     | "28"                        |
| "Availability Target..."                                                                                                                                                                                               | "28"                        |
| "Deployment."                                                                                                                                                                                                          | ".29"                       |
| "User Management"                                                                                                                                                                                                      | ".29"                       |
| "Networking & Change Management."                                                                                                                                                                                      | "29"                        |
| "Dependencies."                                                                                                                                                                                                        | "30"                        |
| "Questions"                                                                                                                                                                                                            | "30"                        |
| "Considerations."                                                                                                                                                                                                      | "30"                        |
| "Project Milestones.."                                                                                                                                                                                                 | "31"                        |
| "Outputs"                                                                                                                                                                                                              | "32"                        |
| "Design documents"                                                                                                                                                                                                     | "32"                        |
| "Operations, and lifecycle management"                                                                                                                                                                                 | "33"                        |
| "Ongoing management"                                                                                                                                                                                                   | "33"                        |
| "Monitoring."                                                                                                                                                                                                          | "33"                        |

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

4

---

## Technical Overview

### Overview

This document provides a technical overview and template for FITFILE Node deployments.

It outlines the architecture, key components, technology stack, data management practices (including data privacy and linkage), deployment procedures, and security considerations.

The document also addresses networking, user management, and change management, emphasizing Terraform and considering dependencies, milestones, and outputs such as design documents.

The document also includes a section on support and responsibilities, including service commitments and incident classification.

### High Level Architecture

The FITFILE Node leverages a modern technology stack including PostgreSQL, Minio, MongoDB, Kubernetes, SpiceDB, Hashicorp Vault, ArgoCD, and Argo Workflow.

Data access is orchestrated by FITConnect, supporting various data sources like static files, MySQL, PostgreSQL, MS SQL, and Elasticsearch.

### The FITFILE Node

The core components of FITFILE's application stack are contained inside a software "Node" deployed into Data Controller perimeters. The key features of the design are:

1. Deploy anywhere any cloud, any infrastructure
2. Centralised control and deployment for easy authentication and update
3. Containerised - each Node has every feature it needs to act independently, including approved third-party services e.g. for harmonisation, and self-heals any issues
4. A Node can act in a secure network of Nodes when controlled exchange of privacy treated data is required
5. Nodes are cost efficient and can be put to sleep when not in use.

Each Node contains components to access, privacy treat, otherwise process (e.g. structure, harmonise or analyse) and link data.

It also contains an interface to view/ download datasets as

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

5

---

## Technical Overview

an outcome of a Query Plan run, to view key data attributes and lineage, and to control projects (FITFILE's core unit of organisation) as well as role-based access to those projects.

To operate, each Node:

1. Is provided with access to its data sources (as shown overleaf)
2. Maintains a connection to FITFILE's Central Services to monitor and provide updates to the Node, and to confirm authorisation and authentication (both user and machine-to-machine)
3. Provides audit traces by logging to a centralised event log (but no customer-specific data is sent to this log).

For projects where multiple Data Controllers' data is needed, access can be granted for a Node to connect to another Node (either directly or via a third Node acting as a co-ordinating station) to run queries on that remote Node's datasets with that access being granted locally through the FITFILE-managed authentication and disclosure system controls.

### FITFILE Node Component Overview

A FITFILE Node consists of several runtime components and data stores.

Note: all data on a FITFILE node is encrypted at rest and transmitted with TLS encryption

#### FITConnect

FITConnect manages the supply of data, the transformation of data including its audit and lineage, as well as data output.

It also orchestrates access to that output for use in other queries.

1. Contains a workflow component that scales up and down its data pipeline when a request for access, privacy treatment or linkage is made
2. Is built to incorporate other data processing when required (e.g. DQ checks, data structuring, data harmonisation, computing statistical attributes of interest)
3. Can store data.

#### InsightFILE/HealthFILE

InsightFILE and HealthFILE represent, respectively, the irreversibly anonymised or reversibly pseudonymised/identifiable Query Plans and the outputs of a privacy-treated (and potentially) linked set of records from one or multiple sources.

Linkage can be deterministic or probabilistic

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

6

---

## Technical Overview

for pseudonymised/identifiable and deterministic (only) for anonymised records. Query Plans contain:

1. The data sources to be used
2. The data elements to be used from that source's schema (for cohort discovery and potentially other data of interest on cohorts of interest)
3. The privacy treatment required
4. The relative weights of each data element with respect to privacy treatment.

InsightFILE and HealthFILE are also the interface for Query Plans on the underlying datasets which can be executed as a scheduled job or within a web interface that is possible to access once relevant IPs to the cluster are whitelisted.

This is the primary user access to data within a FITFILE Node.

### Central Services

Nodes are co-ordinated by several centrally managed, highly scalable and best-in-class internal and externally curated services.

Most importantly amongst the externally curated services are:

1. Grafana aggregates metrics from a FITFILE Node. This includes, but isn't limited to, application data (e.g. requests, audit logs) and runtime data (e.g. CPU usage, memory usage). No source data is recorded to the logs
2. Auth0 manages authentication. Auth0 is best-in-class for RBAC and authentication/authorisation. This is configured at project initiation, and through ongoing support
3. Hashicorp Vault - handles secrets management.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

7

---

## Technical Overview

### Technology Stack

The FITFILE node forms part of a broader set of modern best-of-breed components as described below

- **FITFILE Applications**
  - InsightFILE
  - HealthFILE
  - FITConnect
- **FITFILE APIs**
  - OPENAPI
- **Application & UI Logic**
  - NEXT.js
  - React
  - GraphQL
  - node (application)
  - Rust (cryptography)
- **Data Storage**
  - MINIO (workflow files)
  - PostgreSQL (inbound data)
  - mongoDB (configuration)
- **Data Processing**
  - argo (workflow)
  - python (data)
- **Container Orchestration**
  - kubernetes
- **Current Deployment Options**
  - Azure
  - vmware
  - aws
- **Supporting Services**
  - **User Authentication**
    - Auth0
  - **User Authorisation**
    - spicedb
  - **Node Deployment**
    - ArgoCD
  - **Secrets Management**
    - HashiCorp
  - **Monitoring & Reporting**
    - Grafana
  - **Network Support**
    - CLOUDFLARE

#### Database/Storage Technologies

| **Technology** | **Description**                                                                |
| -------------- | ------------------------------------------------------------------------------ |
| PostgreSQL     | Open-source relational database system known for reliability and extensibility |
| Minio          | High-performance, S3-compatible object storage solution                        |
| MongoDB        | NoSQL database that stores data in flexible, JSON-like documents               |

#### Platform Technologies

| **Technology** | **Description**                                                                    |
| -------------- | ---------------------------------------------------------------------------------- |
| Kubernetes     | Open-source container orchestration platform for managing and scaling applications |
| SpiceDB        | Database for managing fine-grained, relationship-based access control              |

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

8

---

## Technical Overview

| **Technology** | **Description**                                                          |
| -------------- | ------------------------------------------------------------------------ |
| Vault Operator | Tool for managing HashiCorp Vault deployments in Kubernetes environments |
| ArgoCD         | A declarative GitOps continuous delivery tool for Kubernetes             |
| Argo Workflow  | Workflow engine for orchestrating containerised tasks on Kubernetes      |

### Networking Technologies

| **Technology** | **Description**                                                                                                |
| -------------- | -------------------------------------------------------------------------------------------------------------- |
| Calico Cloud   | Cloud-native networking and security platform for Kubernetes and hybrid environments                           |
| Calico CNI     | Container Network Interface plugin providing scalable networking and network policy enforcement for Kubernetes |
| NGINX          | High-performance web server and reverse proxy known for its scalability and load-balancing capabilities        |

### Development Technologies

| **Technology** | **Description**                                                                                    |
| -------------- | -------------------------------------------------------------------------------------------------- |
| Storybook      | A UI component development environment and testing tool for building and showcasing design systems |
| JavaScript     | A versatile programming language primarily used for interactive web applications                   |
| TypeScript     | A superset of JavaScript that adds static typing for improved developer productivity               |
| JSON/YAML      | Data serialisation formats commonly used for configuration files and API communication             |
| Python         | A high-level, interpreted programming language known for its simplicity and versatility            |
| RUST           | A systems programming language focused on safety, speed, and concurrency                           |

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

9

---

## Technical Overview

### Data

#### Data Access - Key Components

Data access is principally orchestrated by FITConnect, which can add, maintain and access

different data sources within its catalogue of data.

A data source is a wrapper of the connection to the data, and a description of that data is known as the data schema.

This schema has a list of data types, whether they identify directly or indirectly, and a user-friendly description of the data (for example, date as a type, and Appointment Date as a description).

Sources can be:

1. Static files uploaded and stored (encrypted) within the Node in a datastore technology
2. Live sources of data in databases these include MySQL, PostgreSQL, MS SQL and Elasticsearch
3. Other data stores - client specific (e.g. data warehouses), connected to as requested.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

10

---

## Technical Overview

In addition to primary sources, other FITConnect nodes can be added as data sources, with appropriate data agreements and access controls.

Thus, a FITConnect can access another Data Providers sources to combine with its own.

In addition, a FITConnect can access the output of other queries (accessed, privacy-treated and linked data) from other sources.

For larger multi-source questions this distributed nature preserves the need for privacy and enables large-scale data analysis across sources and Data Controllers to support federated analytics and the foundations of truly federated learning for non-overlapping as well as overlapping populations while maintaining Data Controller oversight and control of data use.

### Data Privacy - Key Components

FITFILE's data access loads data into a pipeline where it can be transformed, and appropriate pre-agreed privacy treatment can be applied.

The type of privacy treatment and the weights or prioritisation of the maximised data utility are defined via the InsightFILE / HealthFILE interface.

Once the FITConnect receives a data query it initialises a pipeline to load and process the data.

Ther

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

11

---

## Technical Overview

### Privacy Treatment Protocol

Processing can include a privacy treatment protocol, i.e. a series of privacy enhancing/privacy preserving transformations of the data.

FITFILE's privacy treatment protocol can execute reversible pseudonymisation or irreversible anonymisation.

The FITFILE privacy treatment protocol involves a series of techniques applied to a data source's data, as selected/ required by a Query Plan.

Privacy treatment techniques include:

- Aggregation
- Generalisation
- K and $K(m)$ -anonymity
- l-diversity
- t-closeness
- Perturbation
- Rounding
- Suppression
- Sampling
- Differential privacy
- Noise addition
- Permutation

The above list of privacy treatment techniques is constantly evolving.

The privacy treatment techniques are applied to the data generated by a Query Plan iteratively, while the risk of re-identification is constantly monitored.

The protocol creates acceptable results, meaning that the Query Plan-generated data (each acceptable result) is deemed privacy treated, i.e. the re-identification risk assessment threshold is met for each acceptable result.

The protocol then identifies the acceptable result which presents the lowest analytical utility loss and that completes its operation.

### Weighting Factors

The privacy treatment protocol can also select alternate acceptable results if configured to selectively maintain the integrity of any data element or elements.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

12

---

## Technical Overview

This is achieved by assigning data elements included in a Query Plan with coefficients.

These coefficients are weighting factors, commonly referred to as 'weights', and give a data element a higher or lower importance in a group.

In the case of the privacy treatment protocol, after several acceptable results are generated, the selected acceptable result is the one where the highest weighted data element has undergone the least number of transformations.

If more than one data element has been assigned weights, the selected acceptable result will also be additionally defined by the next lower weighted data element or elements, until there are no more data elements with an assigned weight.

This method does not guarantee the selected acceptable result will have the lowest analytical utility loss, but it will guarantee the least number of transformations for those data elements assigned with weights.

### Data Linkage - Key Components

FITFILE's platform allows linkage of record-level data in identifiable, pseudonymised or anonymised format.

#### InsightFILE

Anonymisation = Privacy treatment including a "FITanon"

FITFILE's anonymisation includes the creation of a non-deterministic encrypted cipher that includes one-off random variables (FITanon), based on one or more data elements (direct and/or indirect identifiers).

The FITanon is a mathematical proof generated by FITFILE's patented application of a Zero Knowledge Proof (ZKP), which changes every single time it is generated anywhere by the same data elements.

Using InsightFILE, the linkage is done by sharing these irreversibly anonymised encrypted ciphers with other data sources so that subsequent sources can verify those proofs without being able to reverse or "match".

#### HealthFILE

Pseudonymisation = Privacy Treatment including a FITtoken

FITFILE's pseudonymisation includes the creation of an unchanging deterministic identifier (FITtoken), based on one or more data elements (direct and/or indirect identifiers). The FITtoken

is a static identifier which is always the same if generated by the same data elements.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

13

---

## Technical Overview

In HealthFILE, it is possible to link additional data to a record over time or re-identify a record (or records), as tokens can be recreated to then identify the record or records requested.

Whichever way is used to create links across datasets, the requesting Node will link those datasets based either on FITanons or FITtokens.

### Using Datasets from Query Plans

Data from a Query Plan may be stored in the Node that initiated the Query Plan, along with its lineage and metadata.

There are multiple ways to access that data:

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

14

---

## Technical Overview

1. Users can use the web interface to view and download data as CSV or JSON (preserving structure and metadata)
2. In addition, data can be consumed in an external tool like a Bl or another system.

For data that has multiple runs, for example on a schedule for continuously updating data, the interface provides history of each run to preserve the integrity of analysis at that time.

Web access is available in every Node, with users configured centrally by Auth0.

Security of web access is defined within the perimeter of the installation, so installation-specific whitelisting can be applied.

For example, the application can be made only available to internal users, or web access can be disabled.

### Data Flows

[Description and diagrams]

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

15

---

## Technical Overview

### Networking

#### Networking Requirements for Secure Cloud Deployment

The design is based on a hub-spoke topology, where the FITFILE platform resides in a dedicated "spoke" virtual network (VNet) that integrates with your central "hub" VNet for security, connectivity, and DNS services.

#### Network Architecture

##### Virtual Network (VNet) Design

The platform is deployed into a new, dedicated spoke VNet that will be peered with your existing hub network.

This ensures complete network isolation from other workloads.

- **Address Space:** A dedicated, non-overlapping CIDR block is required for the spoke VNet, typically a $/24$
- **Kubernetes CNI:** FITFILE use the Azure CNI Overlay mode. This conserves IP addresses in your VNet by assigning pod IPs from a separate, dedicated overlay network space (Pod CIDR), which must not overlap with your VNet ranges.
- **Network Policy:** In-cluster traffic is secured using Calico network policies, enabling micro-segmentation to control communication between services.

##### Subnet Allocation

The spoke VNet will be segmented into several smaller subnets, each with a specific purpose to enforce security boundaries.

| **Subnet Purpose**    | **Recommended Size** | **Description**                                                                                                        |
| --------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| System Node Pool      | $/28$ (16 IPs)       | Hosts the core Kubernetes system components.                                                                           |
| Workload Node Pool    | $/28$ (16 IPs)       | Hosts the application workloads and services.                                                                          |
| Management Jumpbox    | $/29$ (8 IPs)        | Hosts a virtual machine for secure administrative access.                                                              |
| DNS Resolver Endpoint | $/28$ (16 IPs)       | (Optional) A delegated subnet for the DNS resolver's outbound endpoint, if there are specific DNS routing requirements |

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

16

---

## Technical Overview

### Traffic Routing and Security

Our security model is based on Zero Trust principles, where all traffic is denied by default and explicitly controlled.

All outbound (egress) traffic is forced through your central firewall for inspection.

### Forced Tunnelling with User-Defined Routes (UDR)

A route table is applied to all relevant subnets to ensure there are no unauthorised paths to the internet.

- **Default Route:** A 0.0.0.0/0 route directs all internet-bound and cross-network traffic to the private IP address of your central firewall (e.g., Azure Firewall) located in the hub VNet.
- Next Hop: The next hop for this route is configured as Virtual Appliance, pointing to [Firewall_Private_IP].

  This configuration guarantees that all outbound traffic from the FITFILE platform is inspected, logged, and controlled by your existing security infrastructure.

### HTTP/S Proxy Integration (Optional)

For environments requiring deep packet inspection of web traffic, the platform can be configured to route all outbound $HTTP/S$ traffic through your corporate proxy.

## Customer Prerequisites Checklist

For a successful deployment, please ensure the following network resources and information are available:

1. Hub-Spoke Connectivity:

   a. An existing hub VNet containing your central firewall and connectivity to your on-premises network (e.g., via Express Route or VPN).

   b. VNet peering must be configured between your hub and the FITFILE new spoke VNet, with traffic forwarding enabled.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

17

---

## Technical Overview

2. IP Address Allocation:

   a. A non-overlapping /24 CIDR block for the new spoke VNet.

   b. The private IP address of your central firewall ([Firewall_Private_IP]).

   c. The IP address of a corporate DNS server reachable from the new VNet ([Customer_DNS_Server_IP]).

3. Firewall Rules:

   a. Your central firewall must be configured to allow the required outbound traffic from the spoke VNet's address space. A detailed list of required endpoints will be provided.

### Security Posture Summary

This architecture provides a robust and secure foundation for the platform.

- **Centralised Egress Inspection:** All outbound traffic is forced through your central firewall, ensuring compliance with corporate security policies.
- **Private API Server:** The Kubernetes API endpoint is private and only accessible from within your network.
- **Micro-segmentation:** Calico network policies provide granular control over in-cluster communication, limiting the lateral movement of any potential threat.
- **Integrated DNS:** Leverages your existing DNS infrastructure, ensuring reliable name resolution and preventing DNS data exfiltration.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

18

---

## Technical Overview

### Deployment

#### Overview

To operate securely, a Node is deployed within the Data Controller's (conceptual) GDPR perimeter and IT estate.

All data is accessed, processed, and privacy treated within that perimeter.

The most common approach, and one FITFILE utilises for its own activities, is to deploy into an Azure or AWS cloud instance, but FITFILE Nodes can be deployed into any Cloud or On Prem environment (the latter is a last course resort where Data Controllers are unable to work with a Cloud-based approach).

Technically, a sub-tenant is created within the infrastructure to allow the deployment of a Node.

Everything within the Node is covered in Terraform, which is code that describes the entire environment. This in turn deploys a Kubernetes cluster containing all the necessary components.

This cluster provides a high degree of security, resilience and scalability.

It also offers simplicity in deployment when updating components, with everything contained within a Node: the software, the networking, and the configuration.

The following diagram shows the cloud deployment model for Azure, which also applies to other cloud vendors (e.g. AWS, Google Cloud).

In all cases FITFILE collaborates closely with Data Controller teams to ensure successful deployment.

The software can be deployed using private or public endpoints for all services.

Private deployments are similarly automated and have extra steps to ensure appropriate configuration of the sub-tenant.

Because endpoints are private, a Jumpbox solution such as Azure Bastion is used to configure the tenant.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

19

---

## Technical Overview

Despite the purpose-built simplicity of its system, FITFILE collaborates with ICT teams to ensure its services and activities are used to correctly and efficiently configure and execute the FITFILE Node deployment and connections.

### Key Requirements

#### AWS Account / Azure Subscription for FITFILE Platform Hosting

The Cloud account/subscription must be capable of deploying the following:

| **AWS**                      | **Azure**                  |
| ---------------------------- | -------------------------- |
| Elastic Kubernetes Service   | Kubernetes Service         |
| Elastic Compute Service      | Virtual Machine Scale Sets |
| Elastic Block Service        | Virtual Machines           |
| Key Management Service       | Spot Virtual Machines      |
| Identity & Access Management | Load balancers             |
| Route53                      | Disk Storage               |
| Elastic Load Balancing       | Azure DNS                  |
| AWS Backup                   | Key Vault                  |

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

20

---

## Technical Overview

| AWS Security Centre | |

### Operational Services

Key services for optimum performance and secure operations:

| **AWS**                  | **Azure**        |
| ------------------------ | ---------------- |
| Security Hub             | Defender         |
| GuardDuty                | Backup Manager   |
| CloudTrail               | Firewall Manager |
| Macie                    | Azure DNS        |
| Web Application Firewall |                  |
| Backup Manager           |                  |

### Deployment Requirements

Service Principal or IAM account implemented in the cloud subscription/ account to allow for "one-button" deployment of infrastructure.

The FITFILE platform operates flexibly within the Data Controller domain naming convention, and the following pattern is suggested:

Clientname.FITFILE.NET (FITFILE hosted)

FITFILE.clientname.co.uk (Data Provider hosted)

### Connectivity Requirements

The FITFILE platform requires the following network configurations:

- Outbound
- HTTPS/443

  Outbound connections are made to key services including Auth0 (Identity Management), Grafana (Observability), FITFILE GitOps services (Platform updates) and HCP Vault (Secrets Management)

- Inbound

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

21

---

## Technical Overview

- VPN/ZTNA based access
- Virtual Desktop Infrastructure

  FITFILE platform operators require elevated permissions for the initial deployment phase and reduced access to least privileged for ongoing operations and where possible "just in time" access when required.

### Firewall Rules & Network

#### Kubernetes / Cloud Networking

- VPC/VNet CIDR range 10.0.0.0/16
  - This range is defined in Terraform on deployment and can be modified should the Data Provider require it
- Pod CIDR Range - 10.244.0.0/16
  - This range is internal to the Kubernetes cluster and will not impact wider CIDR usage

#### Firewall Requirements

- No non-standard port rules required
- TCP443/HTTPS outbound is required at all times
- A Firewall URL List for outbound whitelisting can be provided

## Observability & Monitoring

FITFILE operates a centrally managed observability platform which enables real-time alerting and health monitoring for Data Provider platforms.

Key metrics tracked include:

- Platform Scaling Events
- Sanitised Platform Logs
- Node Operations & Performance
- Container Availability & Operations

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

22

---

## Technical Overview

### Terraform

FITFILE deploys and manages all infrastructure using a GitOps Infrastructure-as-Code model built on Terraform.

This ensures every change is version-controlled, peer-reviewed, and fully auditable, providing a reproducible record of what is deployed and when.

By maintaining the Terraform state centrally and operating the platform as a managed service, FITFILE keeps environments consistently configured, patched, and secure, while allowing rapid and controlled responses to incidents.

This approach removes the operational burden from the customer while maintaining transparency and traceability of all changes.

Typically, the customer will setup and provide an isolated Azure subscription/AWS account for billing separation and access control.

The Azure Contributor role (or AWS equivalent) normally provides adequate access for Terraform to manage infrastructure safely.

here stricter access controls are mandated by Information Governance or IT policies, FITFILE can work with the customer to define a reduced-scope role granting only the necessary permissions.

This is assessed on a per-customer basis, as the precise infrastructure components and configurations differ depending on the deployment solution, and therefore a fixed list of permissions cannot be universally applied.

Once deployed, the provisioned infrastructure can be reviewed by the customer's technical teams, and any significant infrastructure changes would follow the customer's Change Advisory Board (CAB) approval process, ensuring both governance and operational safety.

General overview of permissions needed in Azure:

- "Microsoft.Authorization/roleAssignments/\*",
- "Microsoft.Compute/disks/\*",
- "Microsoft.Compute/virtual Machines/\*",
- "Microsoft.ContainerService/managed Clusters/\*",
- "Microsoft.ManagedIdentity/userAssignedIdentities/\*",
- "Microsoft.Network/networkInterfaces/\*",
- "Microsoft.Network/networkSecurityGroups/\*",
- "Microsoft.Network/private DnsZones/\*",
- "Microsoft.Network/virtual Networks/\*",
- "Microsoft.Resources/subscriptions/providers/read",

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

23

---

## Technical Overview

- "Microsoft.Resources/subscriptions/resourcegroups/\*",

General overview of permissions needed in AWS:

- TODO: Leon to Add

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

24

---

## Technical Overview

### Security and Keeping Data Safe

The FITFILE platform has been designed and developed from inception to be used with personal and sensitive data.

The key security principles are to have security, privacy and compliance by design and by default.

The Node-based federated solution, designed to be installed within a host's cluster, means that it complies and is protected by the Data Controller's own network security.

When data is accessed at source, the following principles apply:

1. Encrypted connections
2. Encrypted at rest
3. Encrypted in transport

All connections operate to HTTPS/1.2 standard at minimum.

All users across the FITFILE service, irrespective of location, use a centralised authorisation service based on the Google Zanzibar project.

This allows the creation of fine-grained access and authentication between machines, between projects and data sources, and the user interactions between all of these.

This centralised service defends against a bad actor data source and it also allows cross-source auditability of usage and transformation of data, and cross-source user access controls.

Hence, projects (an organisational unit within a Node) can use centralised authorisation specific to that project, and the sources a project has access to can also be centrally audited and controlled.

Similarly, a user using a project to access, privacy treat, otherwise process and/or link data can also be given fine grained roles, such as not being able to edit a query, or only being able to execute a query.

Node secrets, like cipher text keys, are stored within the widely trusted Hashicorp Vault and are pulled into the Node using the Vault operator.

FITFILE builds in security at its core by using best in class solutions and tooling as further detailed below.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

25

---

## Technical Overview

### Vulnerability Management

As part of the FITFILE release pipeline, Trivy and COPA are integrated to enhance security and compliance processes.

Trivy is used for automated vulnerability scanning, ensuring that container images and dependencies are free from known security vulnerabilities before they are deployed.

The results of the scans are reviewed in detail to assess risk levels and ensure no critical vulnerabilities are present in the codebase or infrastructure.

COPA is employed to manage and track the software bill of materials (SBOM), providing a transparent view of all components within the release and ensuring they meet compliance standards.

### Secure Development Lifecycle

SonarQube is integrated as a key component of FITFILE's Secure Development Lifecycle, ensuring that security and code quality are embedded throughout the software development process.

By incorporating SonarQube into the CI/CD pipeline, automated static code analysis detects vulnerabilities, security flaws, and maintainability issues early in the development cycle.

### Container Security & Runtime Threat Management

Calico Cloud is used as a key tool in FITFILE's container security and threat management strategy, ensuring that cloud-native applications remain secure and resilient.

Calico Cloud provides robust network security by enabling fine-grained control over container communication, allowing FITFILE to enforce security policies that govern traffic between microservices and containers.

Zero Trust architecture ensures that every communication is verified, reducing the risk of lateral movement in the event of a breach.

### Security Incident & Event Management

FITFILE uses Azure Sentinel as a comprehensive threat detection and response solution to safeguard infrastructure and applications.

Azure Sentinel's cloud-native SIEM platform enables FITFILE to collect, analyse and respond to security data from across environments in real-time.

It leverages advanced machine learning and artificial intelligence to identify potential threats, anomalies, and patterns indicative of malicious activity.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

26

---

## Technical Overview

### Compliance

|                  |                                           | **ISO27001 : 2022** | **ISO27017 : 2015** | **ISO27018 : 2019** | **Cyber Essentials** | **Cyber Essentials Plus** | **NHS DSPT** | **NHSD Cloud Security** | **SOC 2** | **SOC3** | **HIPAA** |
| ---------------- | ----------------------------------------- | ------------------- | ------------------- | ------------------- | -------------------- | ------------------------- | ------------ | ----------------------- | --------- | -------- | --------- |
| FITFILE Platform | Scalable Data Access, Privacy and Linkage | ✓                   |                     |                     | >                    | <                         | <            | >                       |           |          | >         |
| HCP Terraform    | Infrastructure                            | ✓                   | ✓                   |                     | >                    |                           |              |                         |           |          |           |
| HCP Vault        | Secure Secrets Management                 | ✓                   | ✓                   |                     | >                    |                           |              |                         |           |          |           |
| Auth0            | Platform Identity Management              | ✓                   | ✓                   |                     |                      |                           |              |                         |           |          |           |
| Grafana          | Observability & Log Management            |                     |                     |                     |                      |                           |              |                         |           |          |           |
| Azure Sentinel   | SIEM Platform                             |                     | ✓                   | ✓                   |                      |                           |              |                         |           |          | ✓         |

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

27

---

## Technical Overview

### Support and Responsibilities

#### Support Service Commitments

##### Operating Hours

Support personnel are available during standard UK business hours, defined as 9:00amto 5:00pm, Monday to Friday, exclusive of UK bank holidays.

Incidents or questions can be reported within the platform and via <support@fitfile.com>.

##### Response Time Objectives

FITFILE normally undertakes to address support requests within pre-agreed timeframes, measured from the time of receipt during Operating Hours and grouped into "General Priority" and "Critical / High Priority"..

##### Critical / High Priority Incident Classification

Incidents warranting "Critical" or "High Priority" status typically include:

- Issues impacting the confidentiality or integrity of data, or the accuracy of data linkage (Data breach/integrity/linkage).
- Events that risk undermining public confidence in data stewardship or negatively affecting the reputation of involved parties (Public confidence/reputation).
- Circumstances causing significant interruption to service delivery inconsistent with established service level agreements (Service continuity).

##### Availability Target

The service infrastructure is normally managed with a pre-agreed target uptime.

#### Responsibilities

FITFILE operates a shared responsibility model for the operation of the core platform and services with an emphasis on minimising, wherever possible, Data Providers' workload.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

28

---

A Data Provider organisation's primary responsibility is to provide data to the platform as well as the Hosting Provider (Azure/AWS/etc) for the availability of services to operate from.

## Technical Overview

|                                  | **Platform** | **Hosting Provider** | **Data Provider** |
| -------------------------------- | ------------ | -------------------- | ----------------- |
| Data and Updates                 |              |                      | >                 |
| Monitoring                       |              |                      | >                 |
| Security                         | >            |                      |                   |
| Networking and Change Management | >>           |                      |                   |
| User Management                  |              |                      |                   |
| User Onboarding                  | >            |                      |                   |
| Uptime and Availability          |              |                      |                   |
| Deployment                       |              |                      |                   |
|                                  | FITFILE      | Hosting Provider     | Data Provider     |

### Deployment

FITFILE uses Infrastructure as Code capabilities to deploy the FITFILE platform into a Data Provider's infrastructure provider to ensure suitable availability of services and capacity.

### User Management

FITFILE provides a product manager-guided onboarding experience to ensure that platform users can operate within minutes of having been granted access.

The onboarding process is fundamental to secure operations and adherence to the "least privilege access" model.

### Networking & Change Management

FITFILE works with Data Providers to ensure that all processes for change management are adhered to and that the highest levels of compliance and security are maintained.

FITFILE understands from significant experience that Data Providers have a wide range of setups and requirements for their networking.

The FITFILE team seeks to work in close and efficient partnership to achieve the best outcomes as quickly as possible.

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

29

---

## Technical Overview

### Dependencies

What is needed to start a deployment

- Completed discovery document
- Approved design document
- Confirmation of preparation
- Target environment setup and access

### Questions

The following helps as a guide to completing the questionnaire

### Considerations

Key considerations for both FITFILE and Client

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

30

---

## Technical Overview

### Project Milestones

Existing lifecycle:

What are the major technical milestones

- Project setup
- Feasibility
- Governance, Tech and Data Preparation
- Deployment and Configuration
- FITFILE Node deployment in Data Controller(s) & connection to data sources
- Deployment testing and setup of FITFILE Node monitoring & reporting
- Project creation inside FITFILE application and linkage to data sources
- User setup approval with configured project and data access
- User training completion
- Data validation, schema creation and profiling
- Configure reporting API / data export / data visualisation
- Operation and Output

Source: [https://fitfileltd.sharepoint.com/:x:/s/Fitfile](https://fitfileltd.sharepoint.com/:x:/s/Fitfile) Team/EZeAi8-01xRLqliNHbCUjskBTxFTHyP-PNG5003qIA25UA?e=y90SJP

**Reviewed version**

- Technical Discovery (includes tech questions) [project setup]
- Customer Preparation (scheduling, networking, accounts, etc)
- Central Services Configuration (FITFILE)
- Infrastructure deployment (FITFILE + Client)
- Platform and application deployment (FITFILE)
- Configuration
- Networking
- Data provider configuration
- Data Consumer configuration
- Operations / Output

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

31

---

## Technical Overview

### Outputs

What artefacts and comms

#### Design Documents

Specifically what documents

---

FITFILE Group Limited

©2025 All rights reserved Confidential authorised use only

32

---

## Technical Overview

### Operations, and Lifecycle Management

#### Ongoing Management

#### Monitoring

---

­

Confidential authorised use only

**Technical Overview**\
May 2025

This documentation provides a technical overview of the FITFILE system,

how it operates securely, how it accesses source data, privacy treats

it, links datasets together and makes those datasets available to users.

The documentation also shows how a single FITFILE Node is deployed and

updated inside a secure data perimeter, maintains internal connections,

and is configured for use. Where relevant, partner services such as

unstructured data annotation and data harmonisation are included in

appendices.

![Diagram, bubble chart Description automatically generated with medium

confidence](media/image2.png){width="6.935365266841645in"

height="4.65873031496063in"}

##

## Contents

> 2 The FITFILE Node
>
> 3 FITFILE Node Component Overview (including Tech Stack)

7 I. Data Access -- Key Components

8 II. Data Privacy -- Key Components

9 III. Data Linkage -- Key Components

> 11 Deploying and Connecting a FITFILE Node
>
> 15 Using Datasets from Query Plans
>
> 16 Security and Keeping Data Safe
>
> 19 Support and Responsibilities

## The FITFILE Node

> The core components of FITFILE\'s application stack are contained
> inside a software "Node" deployed into Data Controller perimeters. The
> key features of the design are:

1. Deploy anywhere -- any cloud any infrastructure
2. Centralised control and deployment for easy authentication and
   update

3. Containerised -- each Node has every feature it needs to act
   independently, including approved third-party services e.g. for
   harmonisation, and self-heals any issues

4. A Node can act in a secure network of Nodes when controlled exchange
   of privacy treated data is required

5. Nodes are cost efficient and can be put to sleep when not in use.

> Each Node contains components to access, privacy treat, otherwise
> process (e.g. structure, harmonise or analyse) and link data. It also
> contains an interface to view/ download datasets as an outcome of a
> Query Plan run, to view key data attributes and lineage, and to
> control projects (FITFILE's core unit of organisation) as well as
> role-based access to those projects.
>
> To operate, each Node:

1. Is provided with access to its data sources (as shown overleaf)
2. Maintains a connection to FITFILE\'s Central Services to monitor and
   provide updates to the Node, and to confirm authorisation and
   authentication (both user and machine-to-machine)

3. Provides audit traces by logging to a centralised event log (but no
   customer-specific data is sent to this log).

> For projects where multiple Data Controllers' data is needed, access
> can be granted for a Node to connect to another Node (either directly
> or via a third Node acting as a co-ordinating station) to run queries
> on that remote Node's datasets -- with that access being granted
> locally through the FITFILE-managed authentication and disclosure
> system controls.

## FITFILE Node Component Overview

> A FITFILE Node consists of several runtime components and data stores.
> All data is encrypted at rest and transmitted with TLS encryption.

![](media/image4.png){width="6.888100393700787in"

height="2.5568602362204724in"}

*Figure: A FITFILE Node component view*

### FITConnect

> FITConnect manages the supply of data, the transformation of data
> including its audit and lineage, as well as data output. It also
> orchestrates access to that output for use in other queries.
> FITConnect:

1. Contains a workflow component that scales up and down its data
   pipeline when a request for access, privacy treatment or linkage is
   made

2. Is built to incorporate other data processing when required (e.g. DQ
   checks, data structuring, data harmonisation, computing statistical
   attributes of interest)

3. Can store data.

### InsightFILE/ HealthFILE

> InsightFILE and HealthFILE represent, respectively, the irreversibly
> anonymised or reversibly pseudonymised/identifiable Query Plans and
> the outputs of a privacy-treated (and potentially) linked set of
> records from one or multiple sources. Linkage can be deterministic or
> probabilistic for pseudonymised/identifiable and deterministic (only)
> for anonymised records. Query Plans contain:

1. The data sources to be used
2. The data elements to be used from that source's schema (for cohort
   discovery and potentially other data of interest on cohorts of
   interest)

3. The privacy treatment required
4. The relative weights of each data element with respect to privacy
   treatment.

> InsightFILE and HealthFILE are also the interface for Query Plans on
> the underlying datasets which can be executed as a scheduled job or
> within a web interface that is possible to access once relevant IPs to
> the cluster are whitelisted. This is the primary user access to data
> within a FITFILE Node.

### Central Services

> Nodes are co-ordinated by several centrally managed, highly scalable
> and best-in-class internal and externally curated services. Most
> importantly amongst the externally curated services are:

1. Grafana -- aggregates metrics from a FITFILE Node. This includes,
   but isn\'t limited to, application data (e.g. requests, audit logs)
   and runtime data (e.g. CPU usage, memory usage). No source data is
   recorded to the logs

2. Auth0 -- manages authentication. Auth0 is best-in-class for RBAC and
   authentication/authorisation. This is configured at project
   initiation, and through ongoing support

3. Hashicorp Vault -- handles secrets management.

### Tech Stack

> The aforementioned services form part of a broader set of modern
> best-of-breed components summarised below.
>
> ![A screenshot of a computer Description automatically
generated](media/image5.png){width="6.552639982502187in"
> height="3.846503718285214in"}

The tables below describe these components in terms of technology type.

Database/Storage Technologies

---

PostgreSQL Open-source relational database

                                  system known for reliability and

                                  extensibility

---

Minio High-performance, S3-compatible

                                  object storage solution

MongoDB NoSQL database that stores data in

flexible, JSON-like documents

---

> Platform Technologies

---

Kubernetes Open-source container orchestration

                                  platform for managing and scaling

                                  applications

---

SpiceDB Database for managing fine-grained,

                                  relationship-based access control

Vault Operator Tool for managing HashiCorp Vault

                                  deployments in Kubernetes

                                  environments

ArgoCD A declarative GitOps continuous

                                  delivery tool for Kubernetes

Argo Workflow Workflow engine for orchestrating

containerised tasks on Kubernetes

---

> Networking Technologies

---

Calico Cloud Cloud-native networking and

                                  security platform for Kubernetes

                                  and hybrid environments

---

Calico CNI Container Network Interface plugin

                                  providing scalable networking and

                                  network policy enforcement for

                                  Kubernetes

NGINX High-performance web server and

reverse proxy known for its

scalability and load-balancing

capabilities

---

> Development Technologies

---

Storybook A UI component development

                                  environment and testing tool for

                                  building and showcasing design

                                  systems

---

JavaScript A versatile programming language

                                  primarily used for interactive web

                                  applications

TypeScript A superset of JavaScript that adds

                                  static typing for improved

                                  developer productivity

JSON/YAML Data serialisation formats commonly

                                  used for configuration files and

                                  API communication

Python A high-level, interpreted

                                  programming language known for its

                                  simplicity and versatility

RUST A systems programming language

focused on safety, speed, and

concurrency

---

## I. Data Access -- Key Components

> Data access is principally orchestrated by FITConnect, which can add,
> maintain and access different data sources within its catalogue of
> data.
>
> ![](media/image6.png){width="6.851949912510936in"
> height="2.5479166666666666in"}
>
> *Figure: FITFILE Components with Data Access components and connection
> to Data Sources highlighted*
>
> A data source is a wrapper of the connection to the data, and a
> description of that data is known as the data schema. This schema has
> a list of data types, whether they identify directly or indirectly,
> and a user-friendly description of the data (for example, date as a
> type, and Appointment Date as a description).
>
> Sources can be:

1. Static files -- uploaded and stored (encrypted) within the Node in a
   datastore technology

2. Live sources of data in databases -- these include MySQL,
   PostgreSQL, MS SQL and Elasticsearch

3. Other data stores -- client specific (e.g. data warehouses),
   connected to as requested.

> In addition to primary sources, other FITConnects can be added as data
> sources, with appropriate data agreements and access controls. Thus, a
> FITConnect can access another\'s sources to combine with its own.
>
> In addition, a FITConnect can access the output of other queries
> (accessed, privacy-treated and linked data) from other sources. For
> larger multi-source questions this distributed nature preserves the
> need for privacy and enables large-scale data analysis across sources
> and Data Controllers to support federated analytics and the
> foundations of truly federated learning for non-overlapping as well as
> overlapping populations while maintaining Data Controller oversight
> and control of data use.

## II. Data Privacy -- Key Components

> FITFILE's data access loads data into a pipeline where it can be
> transformed, and appropriate pre-agreed privacy treatment can be
> applied. The type of privacy treatment and the weights or
> prioritisation of the maximised data utility are defined via the
> InsightFILE/ HealthFILE interface. Once the FITConnect receives a data
> query it initialises a pipeline to load and process the data.
>
> ![](media/image7.png){width="6.969440069991251in"
> height="2.5836734470691165in"}\
> *Figure: FITFILE Components with Data Privacy components highlighted*

### Privacy Treatment Protocol

> Processing can include a privacy treatment protocol, i.e. a series of
> privacy enhancing/ privacy preserving transformations of the data.
> FITFILE's privacy treatment protocol can execute reversible
> pseudonymisation or irreversible anonymisation.
>
> The FITFILE privacy treatment protocol involves a series of techniques
> applied to a data source's data, as selected/ required by a Query
> Plan. Privacy treatment techniques include:

- Aggregation
- Generalisation
- K and K(m)-anonymity
- l-diversity
- t-closeness
- Perturbation
- Rounding
- Suppression
- Sampling
- Differential privacy
- Noise addition
- Permutation

> The above list of privacy treatment techniques is constantly evolving.
>
> The privacy treatment techniques are applied to the data generated by
> a Query Plan iteratively, while the risk of re-identification is
> constantly monitored. The protocol creates acceptable results, meaning
> that the Query Plan-generated data (each acceptable result) is deemed
> privacy treated, i.e. the re-identification risk assessment threshold
> is met for each acceptable result. The protocol then identifies the
> acceptable result which presents the lowest analytical utility loss
> and that completes its operation.

### Weighting Factors

> The privacy treatment protocol can also select alternate acceptable
> results if configured to selectively maintain the integrity of any
> data element or elements.
>
> This is achieved by assigning data elements included in a Query Plan
> with coefficients. These coefficients are weighting factors, commonly
> referred to as 'weights', and give a data element a higher or lower
> importance in a group. In the case of the privacy treatment protocol,
> after several acceptable results are generated, the selected
> acceptable result is the one where the highest weighted data element
> has undergone the least number of transformations.
>
> If more than one data element has been assigned weights, the selected
> acceptable result will also be additionally defined by the next lower
> weighted data element or elements, until there are no more data
> elements with an assigned weight. This method does not guarantee the
> selected acceptable result will have the lowest analytical utility
> loss, but it will guarantee the least number of transformations for
> those data elements assigned with weights.

## III. Data Linkage -- Key Components

> FITFILE's platform allows linkage of record-level data in
> identifiable, pseudonymised or anonymised format.

### InsightFILE

> Anonymisation = Privacy treatment including a "FITanon"
>
> FITFILE's anonymisation includes the creation of a non-deterministic
> encrypted cipher that includes one-off random variables (FITanon),
> based on one or more data elements (direct and/or indirect
> identifiers). The FITanon is a mathematical proof generated by
> FITFILE's patented application of a Zero Knowledge Proof (ZKP), which
> changes every single time it is generated anywhere by the same data
> elements.
>
> Using InsightFILE, the linkage is done by sharing these irreversibly
> anonymised encrypted ciphers with other data sources so that
> subsequent sources can verify those proofs without being able to
> reverse or "match".

### HealthFILE

> Pseudonymisation = Privacy Treatment including a FITtoken
>
> FITFILE's pseudonymisation includes the creation of an unchanging
> deterministic identifier (FITtoken), based on one or more data
> elements (direct and/or indirect identifiers). The FITtoken is a
> static identifier which is always the same if generated by the same
> data elements.
>
> In HealthFILE, it is possible to link additional data to a record over
> time or re-identify a record (or records), as tokens can be recreated
> to then identify the record or records requested.
>
> Whichever way is used to create links across datasets, the requesting
> Node will link those datasets based either on FITanons or FITtokens.
>
> ![](media/image8.png){width="6.9149901574803145in"
> height="2.564465223097113in"}\
> *Figure: FITFILE Components with Data Linkage components highlighted*
>
> Linked datasets in a FITConnect are themselves data sources and can be
> used in further operations, where they are subject to privacy
> treatment once more before the dataset is viewable or stored in order
> to ensure the linked set complies with the required privacy treatment
> threshold.
>
> ![](media/image9.png){width="7.260415573053368in"
> height="1.7395833333333333in"}
>
> *Figure: Privacy Treatment Protocol applied across single or multiple
> Data Sources*

## Deploying and Connecting a FITFILE Node

> To operate securely, a Node is deployed within the Data Controller\'s
> (conceptual) GDPR perimeter and IT estate. All data is accessed,
> processed, and privacy treated within that perimeter.
>
> The most common approach, and one FITFILE utilises for its own
> activities, is to deploy into an Azure or AWS cloud instance, but
> FITFILE Nodes can be deployed into any Cloud or On Prem environment
> (the latter is a last course resort where Data Controllers are unable
> to work with a Cloud-based approach).
>
> Technically, a sub-tenant is created within the infrastructure to
> allow the deployment of a Node. Everything within the Node is covered
> in Terraform, which is code that describes the entire environment.
> This in turn deploys a Kubernetes cluster containing all the necessary
> components. This cluster provides a high degree of security,
> resilience and scalability. It also offers simplicity in deployment
> when updating components, with everything contained within a Node: the
> software, the networking, and the configuration.
>
> The following diagram shows the cloud deployment model for Azure,
> which also applies to other cloud vendors (e.g. AWS, Google Cloud). In
> all cases FITFILE collaborates closely with Data Controller teams to
> ensure successful deployment. The software can be deployed using
> private or public endpoints for all services. Private deployments are
> similarly automated and have extra steps to ensure appropriate
> configuration of the sub-tenant. Because endpoints are private, a
> jumpbox solution such as Azure Bastion is used to configure the
> tenant.
>
> ![A screenshot of a computer Description automatically
generated](media/image10.png){width="7.263889982502187in"
> height="3.561111111111111in"}
>
> *Figure: FITFILE's build process, and how a Node is deployed and
> updated from the build process*
>
> Despite the purpose-built simplicity of its system, FITFILE
> collaborates with ICT teams to ensure the following services and
> activities are used to correctly and efficiently configure and execute
> the FITFILE Node deployment and connections.

+---------------+-----------------------------------------------------------------+
| Key | Service/ Activity |
| Requirement | |
+===============+=================================================================+
| Account/ | Cloud account/ subscription must be capable of deploying the |
| Subscription | following: |
| for FITFILE | |
| platform | |
| +-----------------------------------------------------------------+
| | AWS |
| | |
| | - Elastic Kubernetes Service |
| | |
| | - Elastic Compute Service |
| | |
| | - Elastic Block Service |
| | |
| | - Key Management Service |
| | |
| | - Identity & Access Management |
| | |
| | - Route53 |
| | |
| | - Elastic Load Balancing |
| | |
| | - AWS Backup |
| | |
| | - AWS Security Centre |
| +-----------------------------------------------------------------+
| | Azure |
| | |
| | - Kubernetes Service |
| | |
| | - Virtual Machine Scale Sets |
| | |
| | - Virtual Machines |
| | |
| | - Spot Virtual Machines |
| | |
| | - Load balancers |
| | |
| | - Disk Storage |
| | |
| | - Azure DNS |
| | |
| | - Key Vault |
+---------------+-----------------------------------------------------------------+
| Operational | Key services for optimum performance and secure operations: |
| Services | |
| +-----------------------------------------------------------------+
| | AWS |
| | |
| | - Security Hub |
| | |
| | - GuardDuty |
| | |
| | - CloudTrail |
| | |
| | - Macie |
| | |
| | - Web Application Firewall |
| | |
| | - Backup Manager |
| +-----------------------------------------------------------------+
| | Azure |
| | |
| | - Defender |
| | |
| | - Backup Manager |
| | |
| | - Firewall Manager |
| | |
| | - Azure DNS |
+---------------+-----------------------------------------------------------------+
| Deployment | Service Principal or IAM account implemented in the cloud |
| Requirements | subscription/ account to allow for "one-button" deployment of |
| | infrastructure. |
| | |
| | The FITFILE platform operates flexibly within the Data |
| | Controller domain naming convention and the following pattern |
| | is suggested |
| | |
| | - Clientname.FITFILE.NET (FITFILE hosted) |
| | |
| | - FITFILE.clientname.co.uk (Data Provider hosted) |
+---------------+-----------------------------------------------------------------+
| Connectivity | The FITFILE platform requires the following network |
| Requirements | configurations: |
| | |
| | - Outbound |
| | |
| | - HTTPS/443 |
| | |
| | Outbound connections are made to key services including Auth0 |
| | (Identity Management), Grafana (Observability), FITFILE GitOps |
| | services (Platform updates) and HCP Vault (Secrets Management) |
| | |
| | - Inbound |
| | |
| | - VPN / ZTNA based access |
| | |
| | - Virtual Desktop Infrastructure |
| | |
| | FITFILE platform operators require elevated permissions for the |
| | initial deployment phase and reduced access to least privileged |
| | for ongoing operations and where possible "just in time" access |
| | when required. |
+---------------+-----------------------------------------------------------------+
| Firewall | # Kubernetes / Cloud Networking |
| Rules & | |
| Network | # VPC/VNet CIDR range -- 10.0.0.0/16 |
| Requirements | |
| | - This range is defined in Terraform on deployment and can be |
| | modified should the Data Provider require it |
| | |
| | - Pod CIDR Range -- 10.244.0.0/16 |
| | |
| | - This range is internal to the Kubernetes cluster and will not |
| | impact wider CIDR usage |
| | |
| | Firewall Requirements |
| | |
| | - No non-standard port rules required |
| | |
| | - TCP443/HTTPS outbound is required at all times |
| | |
| | # A Firewall URL List for outbound whitelisting can be provided |
+---------------+-----------------------------------------------------------------+
| Observability | FITFILE operates a centrally managed observability platform |
| & Monitoring | which enables real-time alerting and health monitoring for Data |
| | Provider platforms. |
| | |
| | Key metrics tracked include: |
| | |
| | - Platform Scaling Events |
| | |
| | - Sanitised Platform Logs |
| | |
| | - Node Operations & Performance |
| | |
| | - Container Availability & Operations |
+---------------+-----------------------------------------------------------------+

##

## Using Datasets from Query Plans

> Data from a Query Plan may be stored in the Node that initiated the
> Query Plan, along with its lineage and metadata. There are multiple
> ways to access that data:

1. Users can use the web interface to view and download data as CSV or
   JSON (preserving structure and metadata)

2. In addition, data can be consumed in an external tool like a BI or
   another system.

> For data that has multiple runs, for example on a schedule for
> continuously updating data, the interface provides history of each run
> to preserve the integrity of analysis at that time.
>
> ![A screenshot of a computer Description automatically
generated](media/image11.png){width="6.9732852143482065in"
> height="2.7826082677165354in"}\
> *Figure: Datasets stored in the FITConnect accessed by a User*
>
> Web access is available in every Node, with users configured centrally
> by Auth0. Security of web access is defined within the perimeter of
> the installation, so installation-specific whitelisting can be
> applied. For example, the application can be made only available to
> internal users, or web access can be disabled.

## Security and Keeping Data Safe

> The FITFILE platform has been designed and developed from inception to
> be used with personal and sensitive data.
>
> The key security principles are to have security, privacy and
> compliance by design and by default. The Node-based federated
> solution, designed to be installed within a host\'s cluster, means
> that it complies and is protected by the Data Controller's own network
> security. When data is accessed at source, the following principles
> apply:

1. Encrypted connections
2. Encrypted at rest
3. Encrypted in transport

All connections operate to HTTPS/1.2 standard at minimum.

> All users across the FITFILE service, irrespective of location, use a
> centralised authorisation service based on the Google Zanzibar
> project. This allows the creation of fine-grained access and
> authentication between machines, between projects and data sources,
> and the user interactions between all of these. This centralised
> service defends against a bad actor data source and it also allows
> cross-source auditability of usage and transformation of data, and
> cross-source user access controls.
>
> Hence, projects (an organisational unit within a Node) can use
> centralised authorisation specific to that project, and the sources a
> project has access to can also be centrally audited and controlled.
>
> Similarly, a user using a project to access, privacy treat, otherwise
> process and/ or link data can also be given fine grained roles, such
> as not being able to edit a query, or only being able to execute a
> query. Node secrets, like cipher text keys, are stored within the
> widely trusted Hashicorp Vault and are pulled into the Node using the
> Vault operator.
>
> FITFILE builds in security at its core by using best in class
> solutions and tooling as further detailed below.

### Vulnerability Management

> As part of the FITFILE release pipeline, Trivy and COPA are integrated
> to enhance security and compliance processes.

- Trivy is used for automated vulnerability scanning, ensuring that
  container images and dependencies are free from known security
  vulnerabilities before they are deployed. The results of the scans are
  reviewed in detail to assess risk levels and ensure no critical
  vulnerabilities are present in the codebase or infrastructure.

- COPA is employed to manage and track the software bill of materials
  (SBOM), providing a transparent view of all components within the
  release and ensuring they meet compliance standards.

### Secure Development Lifecycle

> SonarQube is integrated as a key component of FITFILE's Secure
> Development Lifecycle, ensuring that security and code quality are
> embedded throughout the software development process. By incorporating
> SonarQube into the CI/CD pipeline, automated static code analysis
> detects vulnerabilities, security flaws, and maintainability issues
> early in the development cycle.

### Container Security & Runtime Threat Management

> Calico Cloud is used as a key tool in FITFILE's container security and
> threat management strategy, ensuring that cloud-native applications
> remain secure and resilient. Calico Cloud provides robust network
> security by enabling fine-grained control over container
> communication, allowing FITFILE to enforce security policies that
> govern traffic between microservices and containers. Zero Trust
> architecture ensures that every communication is verified, reducing
> the risk of lateral movement in the event of a breach.

### Security Incident & Event Management

> FITFILE uses Azure Sentinel as a comprehensive threat detection and
> response solution to safeguard infrastructure and applications. Azure
> Sentinel's cloud-native SIEM platform enables FITFILE to collect,
> analyse and respond to security data from across environments in
> real-time. It leverages advanced machine learning and artificial
> intelligence to identify potential threats, anomalies, and patterns
> indicative of malicious activity.

### Compliance Matrix

+-------------------------------+-----------------+------------+------------+--------------+--------------+--------+------------+-------+--------+---------+
| | > ISO27001:2022 | > ISO27017 | > ISO27018 | > Cyber | > Cyber | > NHS | > NHSD | > SOC | > SOC3 | > HIPAA |
| | | > : 2015 | > : 2019 | > Essentials | > Essentials | > DSPT | > Cloud | > 2 | | |
| | | | | | > Plus | | > Security | | | |
+==============+================+:===============:+:==========:+:==========:+:============:+:============:+:======:+:==========:+:=====:+:======:+=========+
| FITFILE | Scalable Data | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ | | | ✓ |
| Platform | Access, | | | | | | | | | | |
| | Privacy and | | | | | | | | | | |
| | Linkage | | | | | | | | | | |
+--------------+----------------+-----------------+------------+------------+--------------+--------------+--------+------------+-------+--------+---------+
| HCP | Infrastructure | ✓ | ✓ | | ✓ | ✓ | | | ✓ | ✓ | |
| Terraform | | | | | | | | | | | |
+--------------+----------------+-----------------+------------+------------+--------------+--------------+--------+------------+-------+--------+---------+
| HCP\ | Secure Secrets | ✓ | ✓ | | ✓ | ✓ | | ✓ | | | ✓ |
| Vault | Management | | | | | | | | | | |
+--------------+----------------+-----------------+------------+------------+--------------+--------------+--------+------------+-------+--------+---------+
| Auth0 | Platform | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ |
| | Identity | | | | | | | | | | |
| | Management | | | | | | | | | | |
+--------------+----------------+-----------------+------------+------------+--------------+--------------+--------+------------+-------+--------+---------+
| Grafana | Observability | ✓ | ✓ | | ✓ | ✓ | | ✓ | ✓ | | |
| | & Log | | | | | | | | | | |
| | Management | | | | | | | | | | |
+--------------+----------------+-----------------+------------+------------+--------------+--------------+--------+------------+-------+--------+---------+
| Azure | SIEM\ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Sentinel | Platform | | | | | | | | | | |
+--------------+----------------+-----------------+------------+------------+--------------+--------------+--------+------------+-------+--------+---------+

## Support & Responsibilities

### Support Service Commitments

> Operating Hours
>
> Support personnel are available during standard UK business hours,
> defined as 9:00 AM to 5:00 PM, Monday to Friday, exclusive of UK bank
> holidays. Incidents or questions can be reported within the platform
> and via <support@fitfile.com>.
>
> Response Time Objectives
>
> FITFILE normally undertakes to address support requests within
> pre-agreed timeframes, measured from the time of receipt during
> Operating Hours and grouped into "General Priority\" and "Critical /
> High Priority".
>
> Critical / High Priority Incident Classification
>
> Incidents warranting \"Critical\" or \"High Priority\" status
> typically include:

- Issues impacting the confidentiality or integrity of data, or the
  accuracy of data linkage (Data breach/integrity/linkage).

- Events that risk undermining public confidence in data stewardship or
  negatively affecting the reputation of involved parties (Public
  confidence/reputation).

- Circumstances causing significant interruption to service delivery
  inconsistent with established service level agreements (Service
  continuity).

> Availability Target
>
> The service infrastructure is normally managed with a pre-agreed
> target uptime.

### Responsibilities

> FITFILE operates a shared responsibility model for the operation of
> the core platform and services with an emphasis on minimising,
> wherever possible, Data Providers' workload.
>
> A Data Provider organisation's primary responsibility is to provide
> data to the platform as well as the Hosting Provider (Azure/AWS/etc)
> for the availability of services to operate from.

+----------------+--------------+----------------+--------------+--------------+--------------+--------------------------+--------------+-----------+
| | > Deployment | > Uptime & | > User | > User | > Networking | > Security | > Monitoring | > Data & |
| | | > Availability | > Onboarding | > Management | > & Change | | | > Updates |
| | | | | | > Management | | | |
+================+:============:+:==============:+:============:+:============:+:============:+:========================:+:============:+:=========:+
| FITFILE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| Platform | | | | | | | | |
+----------------+--------------+----------------+--------------+--------------+--------------+--------------------------+--------------+-----------+
| Data Provider | | | | ✓ | ✓ | # {#section-2 .FITFILE} | | ✓ |
+----------------+--------------+----------------+--------------+--------------+--------------+--------------------------+--------------+-----------+
| Hosting | ✓ | ✓ | | | | | | |
| Provider | | | | | | | | |
+----------------+--------------+----------------+--------------+--------------+--------------+--------------------------+--------------+-----------+

> Deployment
>
> FITFILE uses Infrastructure as Code capabilities to deploy the FITFILE
> platform into a Data Provider's infrastructure provider to ensure
> suitable availability of services and capacity.
>
> User Management
>
> FITFILE provides a product manager-guided onboarding experience to
> ensure that platform users can operate within minutes of having been
> granted access. The onboarding process is fundamental to secure
> operations and adherence to the "least privilege access" model.
>
> Networking & Change Management
>
> FITFILE works with Data Providers to ensure that all processes for
> change management are adhered to and that the highest levels of
> compliance and security are maintained. FITFILE understands from
> significant experience that Data Providers have a wide range of setups
> and requirements for their networking. The FITFILE team seeks to work
> in close and efficient partnership to achieve the best outcomes as
> quickly as possible.

**Safer, faster, better data**
