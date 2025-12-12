---
aliases: []
confidence: 
created: 2025-11-03T13:36:27Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Historical Analysis of CUH to HIE SDE Connectivity
type: 
uid: 
updated: 
---

## Bunny-Relay Networking: Historical Analysis of CUH to HIE SDE Connectivity

This document details the historical work and incident analysis concerning the Bunny-Relay networking between the Cambridge University Hospitals (CUH) and Health Innovation East Secure Data Environment (HIE SDE) environments. It focuses on understanding why the system functioned despite misconfigurations, the impact of incorrect CIDR ranges, and the remediation efforts undertaken.

### I. The Bunny-Relay System Architecture

The Bunny-Relay system was a critical component for the FITFILE platform, facilitating data processing.

- **Bunny Service:** An application hosted within the CUH environment (primarily Azure AKS) responsible for fetching queries from an upstream Task API and resolving them against a local OMOP database. It initiates outbound requests.
- **Relay Service:** Hosted within the HIE SDE environment (AWS EKS), acting as a central hub that exposes an API endpoint to manage tasks. It is fronted by an AWS Application Load Balancer (ALB).
- **Network Path:** Traffic from the Bunny service in CUH egresses through Telefónica's on-premise infrastructure for mandatory inspection and policy enforcement before reaching the Relay service's ALB in HIE SDE. This path involves navigating CUH's on-premise firewalls (FortiGate) and web proxies (McAfee Web Proxy) before heading towards the public internet and finally the AWS EKS environment.

### II. The "Open to the World" Phase and Incorrect CIDR Ranges

The system's initial functionality, despite underlying misconfigurations, was largely due to permissive network rules. The user's query highlights that "The sgs are open to the internet which is why it is working." This points to a period where security group rules were overly broad, masking deeper issues.

#### A. Initial Incorrect CIDR Range in `relay.tf`

- **The Range:** An incorrect CIDR range of `**************/26` was present from the initial creation of the `relay.tf` file around October 28, 2025. This was identified as a foundational misconfiguration.
- **Legacy/Problematic Range:** The CIDR block `194.176.105.64/26` was also present from the initial configuration and persisted in Terraform. This range was intended or legacy CUH egress traffic.

#### B. The `0.0.0.0/0` Ingress Rule

- **Introduction:** Around mid-September 2025, an overly permissive `0.0.0.0/0` ingress rule for HTTPS (port 443) was manually added to the ALB's security group (`sg-06a3ef4dc97a131f1`) in the HIE SDE environment.
- **Rationale:** This manual intervention was likely a response to connectivity issues caused by the incorrect CIDR configurations and other underlying problems. The broad access bypassed intended IP restrictions, temporarily restoring connectivity and masking deeper issues related to misconfigured ALB ports, faulty backend instances, and incorrect routing.
- **State Drift:** This rule represented significant state drift as it was a manual change not reflected in Infrastructure as Code (IaC) and was contrary to the principle of least privilege. It was later removed around November 3, 2025.

#### C. Corrected CUH Egress IP Range

- **The Range:** The latest confirmed egress IP range for CUH traffic, identified on September 10, 2025, is `217.38.237.128/26`.
- **Terraform Update:** This correct range was added to the Terraform configuration around November 3, 2025, to be explicitly included in the SDE Relay ALB security group rules, alongside the legacy `194.176.105.64/26`.

### III. Timeline of Issues, Diagnostics, and Remediation

The Bunny-Relay networking experienced a series of interconnected problems, often exacerbated by state drift and manual interventions.

#### A. Early Configurations & State Drift (Prior to Mid-September 2025)

- **User's Incorrect CIDR Configuration:** The user previously applied incorrect CIDR ranges, which altered security group rules for the ALB. This likely disrupted intended secure connectivity, leading to functional issues.
- **Manual Override:** The `0.0.0.0/0` rule was manually introduced to restore connectivity, creating state drift.

#### B. Mid-September 2025: Intermittent Connectivity Issues and Underlying Problems

- **ALB Target Group Misconfiguration:**
  - **Problem:** The ALB target group (`eoe-sde-codisc-relay-tg`) forwarded traffic to the incorrect port (`80` instead of `32080`/`32082`) and used the wrong health check protocol (`HTTP` instead of `HTTPS`).
  - **Impact:** This prevented successful communication between the Bunny and Relay services, causing `SSLEOFError` and `502 Bad Gateway` errors.
  - **Remediation:** The target group port and health check protocol were corrected.
- **Kubernetes Pod Distribution:**
  - **Problem:** Insufficient replicas of the `hutch-relay` pod were deployed, leading to poor distribution and unavailability of the service on certain nodes.
  - **Remediation:** The deployment was scaled up to two replicas.
- **Faulty AWS Subnet/Instance:**
  - **Problem:** A faulty EC2 instance (`i-0a3061a5b059d819c`) within a specific subnet (`subnet-04b88a21fbe703f1a`) caused one of the ALB's IP addresses to become a "black hole" for traffic, leading to TLS errors.
  - **Remediation:** The faulty instance was terminated, and ALB subnets were reconfigured to provision healthy replacements, restoring stable connectivity.

#### C. October 2, 2025: Outbound Traffic Interruption and Critical Security Findings

A significant incident led to a complete interruption of outbound network traffic from the AWS SDE HIE CODISC environment.

- **Missing Egress Rule in EKS Security Group:**
  - **Problem:** The EKS cluster's security group (`sg-0a3345e3be2761343`) lacked egress rules, blocking all outbound traffic. Pods could not pull images or connect to external services.
  - **Remediation:** A broad egress rule (`--protocol -1 --cidr 0.0.0.0/0`) was manually added to restore outbound connectivity.
- **Misconfigured Route Table:**
  - **Problem:** The route table (`rtb-0c3588944a5ce5db3`) for a private subnet incorrectly directed internet-bound traffic (`0.0.0.0/0`) to the Internet Gateway instead of the NAT Gateway.
  - **Remediation:** The route table was corrected to route traffic through the NAT Gateway.
- **IAM Permission Deficiencies:**
  - **Problem:** The `tf-deployment` user lacked necessary permissions for AWS services, preventing automated remediation by Terraform.
  - **Remediation:** Required IAM permissions were granted.

#### D. November 3, 2025: Terraform Alignment and Configuration Correction

- **Terraform Updates:** Terraform code was updated to align with the intended secure configuration.
  - The ALB security group (`sg-06a3ef4dc97a131f1`) was configured to include only the specific CIDR blocks: `194.176.105.64/26` (legacy CUH), `217.38.237.128/26` (current CUH), and `20.108.119.18/32` (Azure AKS).
  - The insecure `0.0.0.0/0` rule was removed from AWS, and Terraform was applied to enforce the corrected, IP-restricted configuration.
  - EKS security group egress rules were corrected, and the route table was fixed.

### IV. Summary of CIDR States and Security Group Evolution

The security group rules for the HIE SDE Relay Service's ALB (`sg-06a3ef4dc97a131f1`) evolved through several states:

1. **Initial/Intended State:** Allowed HTTPS traffic only from specific CUH egress ranges (`194.176.105.64/26` and later `217.38.237.128/26`) and Azure AKS (`20.108.119.18/32`).
2. **Post-Incorrect CIDR Configuration (Before `0.0.0.0/0`):** Contained erroneous CIDR ranges applied by the user, disrupting intended connectivity.
3. **Problematic State (Mid-September 2025):** An insecure `0.0.0.0/0` ingress rule was manually added, opening the service to the internet and masking underlying issues.
4. **Corrected State (November 3, 2025):** The `0.0.0.0/0` rule was removed, and the security group was restricted to the intended specific CIDR blocks.

The system's functionality during periods of misconfiguration was due to these permissive rules. The resolution involved identifying and correcting specific ALB configurations, backend instance health, routing issues, egress controls, and aligning Infrastructure as Code with the intended secure state.

this recommended action just has the same command twice.

## Remove the 0.0.0.0/0 Rules and Replace with VPC CIDR

```sh
aws ec2 revoke-security-group-ingress \
  --group-id sg-02dcb1a5bbe8844b8 \
  --ip-permissions IpProtocol=tcp,FromPort=31139,ToPort=31139,IpRanges='[{CidrIp=0.0.0.0/0}]'

aws ec2 revoke-security-group-ingress \
  --group-id sg-02dcb1a5bbe8844b8 \
  --ip-permissions IpProtocol=tcp,FromPort=32623,ToPort=32623,IpRanges='[{CidrIp=0.0.0.0/0}]'
```

Is this a mistake?

No, it's not a mistake! The commands are intentionally different - look at the **port numbers**:

1. First command: `FromPort=31139,ToPort=31139` (HTTP port)
2. Second command: `FromPort=32623,ToPort=32623` (HTTPS port)

Both are revoking the `0.0.0.0/0` source, but for **different NodePorts**. They look similar because they're both removing overly permissive rules from the same security group.

If you want to be more efficient, you could combine them:

```bash
# Revoke both NodePort rules in one command
aws ec2 revoke-security-group-ingress \
  --group-id sg-02dcb1a5bbe8844b8 \
  --ip-permissions \
    IpProtocol=tcp,FromPort=31139,ToPort=31139,IpRanges='[{CidrIp=0.0.0.0/0}]' \
    IpProtocol=tcp,FromPort=32623,ToPort=32623,IpRanges='[{CidrIp=0.0.0.0/0}]'
```

And don't forget the ICMP rule too:

```bash
# Also revoke the ICMP rule
aws ec2 revoke-security-group-ingress \
  --group-id sg-02dcb1a5bbe8844b8 \
  --ip-permissions IpProtocol=icmp,FromPort=3,ToPort=4,IpRanges='[{CidrIp=0.0.0.0/0}]'
```

Since the NLB is internal and already has proper rules for subnet access (the `/23` ranges for health checks), these 0.0.0.0/0 rules are unnecessary security risks.
