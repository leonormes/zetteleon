---
alias: [AWS SSM SSH Protocol, HIE Jumpbox Access]
conformant: false
created: 2026-02-05T00:00:00+00:00
modified: 2026-07-20T16:33:56+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/protocol-aws-hie-jumpbox-access
status: stable
tags: [aws, customer/hie, jumpbox, protocol, ssh, ssm]
title: Protocol - AWS HIE Jumpbox Access
type: protocol
---

## Logic Map

- Target Instance: `i-09f84bb55556a2c10`
- IAM Role: `eoe-sde-codisc-jumpbox-ssm-role`
- Profile: `eoe-hie`
- Region: `eu-west-2`

---

## 1. Authentication & Power On

```bash
# 1. Login to SSO
aws sso login --profile eoe-hie

# 2. Start the Instance
aws ec2 start-instances --instance-ids i-09f84bb55556a2c10 --region eu-west-2 --profile eoe-hie
```

## 2. Establishing Connection

_Note: If using `ssh`, you must export the profile for the ProxyCommand to see it._

```bash
# Option A: One-liner (Recommended)
AWS_PROFILE=eoe-hie ssh jumphost-ssm

# Option B: Manual SSM Session (No SSH)
aws ssm start-session --target i-09f84bb55556a2c10 --profile eoe-hie
```

## 3. Permanent SSH Config Fix

_Edit `~/.ssh/config` to ensure the correct profile is always used for this host._

```text
Host jumphost-ssm
    HostName i-09f84bb55556a2c10
    User awsadmin
    ProxyCommand sh -c "aws ssm start-session --target %h --profile eoe-hie --document-name AWS-StartSSHSession --region eu-west-2"
```

---

## Troubleshooting

| Error | Cause | Resolution |
|:--- |:--- |:--- |
| `Token has expired` | SSH ProxyCommand using `default` profile | Use `AWS_PROFILE=eoe-hie ssh …` |
| `TargetNotConnected` | Instance still booting | Wait 60-120 seconds for SSM agent to start |

---

## Related Sessions

- [[AWS HIE Jumpbox Security Protocols Summary]] (2026-04-07): Summary of identity, connectivity, and operational security requirements.
