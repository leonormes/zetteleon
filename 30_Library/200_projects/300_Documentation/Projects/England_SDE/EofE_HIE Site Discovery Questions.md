---
aliases: []
confidence: 
created: 2025-01-17T14:09:04Z
epistemic: 
id: EofE_HIE Site Discovery Questions
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: EofE_HIE Site Discovery Questions
type:
uid: 
updated: 
version:
---

## Site Discovery Questions

### 1. Infrastructure

- Number of Installations: How many installations are anticipated for this project?
- Network/Cloud Infrastructure: What network or cloud infrastructure will be used (e.g., AWS via Control Tower with AWS Health)?
- Installation Access: Who will provide installation access? Is it managed via a ticketing system (e.g., Telefonica managing CUH)?
- Platform Access: What method is required for platform access for maintenance (e.g., VDI/VPN/ZTNA to Azure)?
- External Tool Access: How can external FITFILE tools be granted access (e.g., IP range whitelisting)?
- Virtual Machines: Are virtual machines beyond the standard E4 configuration required?

### 2. Kubernetes

- Kubernetes Deployment: Is a landing zone or subscription model operational for Kubernetes deployment?

### 4. Security

- SSL Certificates: Who is responsible for providing SSL certificates?
- DNS Configuration: How will Domain Naming Services (DNS) be configured to provide access to the Node (e.g., Route53 based)?
- Security Behaviours/Tools: What are the current security behaviors and tools in the environment?
- Specific Tooling Requirements: Are there any specific tooling that must be used, or any other security requirements?
- IP Range Requirements: What are the specific IP range requirements?
- Firewall Rules: Who is in charge of the firewall rules for the SDE environment?
- Secrets Management: Is HashiCorp for secrets management compatible with the SDE model?
- Networking: Who is in charge of the networking outside the FITFILE cluster, including security groups and related network security?
- Data Transport Security: What are the rules for data transport between source and master nodes over SSL/Internet?
- Penetration Testing: Which party will commission the pen test and when will it occur?
- CE Plus Certification: When are CE Plus certificates expected to be in place?

### 5. Data

- Data Output Frequency: What is the required frequency of data output (e.g., monthly)?
- Data Sizes: What are the expected data sizes?
- Source Data Access: What are the source data access requirements?
- Failed Data Extracts: How should the system handle and report failed data extracts?
- Data Transport: What are the rules around data transport between the source and master nodes over SSL/Internet?

### 6. Deployment

- Communication Method: What is the preferred method of communication from FITFILE (e.g., email/Teams/Zoom)?
- Deployment Plan: What is the plan, approach, names, and roles to begin the master node deployment, including how to get an AWS tenant and service account?
- Deployment Model: What is the proposed deployment model?
- Service Principles: What service principles are required for deployment into SDE?

### 7. Information Governance (IG)

- IG Requirements: What specific IG requirements must be met?
- Data Controller restrictions: Are there any potential Data Controller restrictions on what can be returned from a query?
- IG Processes: What is an overview of the SDE and the 3 Sites IG processes?
- DPO Approvals: Are approvals attained from relevant Data Protection Officers (DPOs) for SDE and all Sites?
