---
session_id: session_1770385335152_1zf8sz6to
type: agent-session
title: SSH SSM HIE Jumpbox Note Search
context_files: []
enabled_tools:
  - read_only
  - vault_ops
require_confirmation:
  - modify_files
  - create_files
  - delete_files
created: 2026-02-06T13:42:15.152Z
last_active: 2026-02-06T13:44:02.334Z
metadata:
  autoLabeled: true
---

# Agent Session 2-6-2026


## User

> [!metadata]- Message Info
> | Property | Value |
> | -------- | ----- |
> | Time | 2026-02-06T13:43:53.911Z |
> | File Version | unknown |

> [!user]+
> find my note on ssh ssm on the hie jumpbox

--- 
## Model

> [!metadata]- Message Info
> | Property | Value |
> | -------- | ----- |
> | Time | 2026-02-06T13:44:02.325Z |
> | File Version | unknown |

> [!assistant]+
> I found your note on the HIE Jumpbox access protocol: **[[Protocol - AWS HIE Jumpbox Access]]**.
> 
> ### Quick Reference for SSH via SSM:
> *   **Target Instance:** &#x60;i-09f84bb55556a2c10&#x60;
> *   **AWS Profile:** &#x60;eoe-hie&#x60;
> *   **Region:** &#x60;eu-west-2&#x60;
> 
> **Recommended Connection Command:**
> &#x60;&#x60;&#x60;bash
> AWS_PROFILE&#x3D;eoe-hie ssh jumphost-ssm
> &#x60;&#x60;&#x60;
> 
> **SSH Config Snippet:**
> If you need to update your &#x60;~/.ssh/config&#x60;, the note specifies:
> &#x60;&#x60;&#x60;text
> Host jumphost-ssm
>     HostName i-09f84bb55556a2c10
>     User awsadmin
>     ProxyCommand sh -c &quot;aws ssm start-session --target %h --profile eoe-hie --document-name AWS-StartSSHSession --region eu-west-2&quot;
> &#x60;&#x60;&#x60;
> 
> The full note is located at &#x60;30_Library/SoT/Protocol - AWS HIE Jumpbox Access.md&#x60;.

--- 