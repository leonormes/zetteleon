---
context_files: ["[[SoT - Think Like a Man of Action, Act Like a Man of Thought]]"]
created: 2026-04-07T09:22:33+00:00
enabled_tools: [external_mcp, read_only, skills, vault_ops]
last_active: 2026-04-07T09:24:24.332Z
metadata:
  autoLabeled: true
modified: 2026-04-08T17:58:53+00:00
require_confirmation: [create_files, delete_files, external_calls, modify_files]
session_id: session_1775553753466_w8tvbh7qb
title: AWS HIE Jumpbox Security Protocols Summary
type: agent-session
---

## Agent Session 4-7-2026

### User

> [!metadata]- Message Info
>
> | Property | Value |
> | -------- | ----- |
> | Time | 2026-04-07T09:22:44.232Z |
> | File Version | unknown |

> [!user]+
> Search the ops and SoT folders for protocols regarding AWS HIE Jumpbox Access and summarise the security requirements

---

### Model

> [!metadata]- Message Info
>
> | Property | Value |
> | -------- | ----- |
> | Time | 2026-04-07T09:24:24.331Z |
> | File Version | unknown |

> [!assistant]+
> Based on the Source of Truth (SoT) and Operations (ops) documents in your vault, the protocols for AWS HIE Jumpbox Access are defined primarily in [[Protocol - AWS HIE Jumpbox Access]] and [[ec2-jumpbox-start-stop]].
>
> The security requirements for accessing the HIE Jumpbox are summarised below:
>
> ### 1. Identity & Access Management (IAM)
> -   SSO Authentication: All access requires active authentication via AWS Single Sign-On (SSO) using the `eoe-hie` profile.
> -   Role-Based Access: The target instance (`i-09f84bb55556a2c10`) operates under the specific IAM role `eoe-sde-codisc-jumpbox-ssm-role`.
> -   Specific Profile Enforcement: Users must ensure the `eoe-hie` profile is used for all CLI commands and SSH proxy commands to avoid "Token has expired" errors.
> 
> ### 2. Connectivity & Network Security
> -   SSM-Only Access: The protocol mandates the use of AWS Systems Manager (SSM) Session Manager. This provides a secure tunnel that does not require opening inbound SSH (Port 22) on the instance's security group.
> -   SSH over SSM Document: For standard SSH workflows, the `AWS-StartSSHSession` document is utilised via a `ProxyCommand`.
> -   Instance Identification: Access is established using the Instance ID rather than a public IP address, further obscuring the target from the public internet.
> 
> ### 3. Operational Security Controls
> -   Ephemeral Availability: The jumpbox is not intended to be "always on." It must be manually started before use and stopped immediately after tasks are completed to minimise the attack surface.
> -   Boot-Time Latency: There is a mandatory wait period of 60–120 seconds after starting the instance to allow the SSM agent to initialise before a connection can be established.
> -   Standardised User: Connections are restricted to the `awsadmin` user.
> 
> ### 4. Configuration Requirements
> To maintain security and connectivity, the following `~/.ssh/config` entry is required:
> ```text
> Host jumphost-ssm
>     HostName i-09f84bb55556a2c10
>     User awsadmin
>     ProxyCommand sh -c "aws ssm start-session --target %h --profile eoe-hie --document-name AWS-StartSSHSession --region eu-west-2"
> ```
>
> ### Relevant Files
> -   SoT: [[Protocol - AWS HIE Jumpbox Access]]
> -   Ops: [[ec2-jumpbox-start-stop]]

---
