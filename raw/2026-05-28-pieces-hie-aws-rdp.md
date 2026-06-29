---
created: 2026-05-28 22:15:00+00:00
modified: 2026-06-09 08:39:59+00:00
pieces_ids:
- 5f2798af-0061-4829-b92f-b2dc771d67e3
- 789e6885-496c-4185-b319-838496d5715c
- e3ea73a9-7571-4dad-874e-b60d7620eb8e
- f27fbcf0-6fbb-46ef-bd62-6490944b5160
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-05-28-pieces-hie-aws-rdp
permalink: llmeon/raw/2026-05-28-pieces-hie-aws-rdp
---

## Asset 1 (Pieces: e3ea73a9-7571-4dad-874e-b60d7620eb8e)—2026-05-28T09:06:26Z

User request: RDP commands for HIE AWS cluster

> "I need to rdp to the hie aws cluster. I have done it before. I think i need to create a tunnel first then I can use the windows App to rdp. what are the commands"

## Asset 2 (Pieces: f27fbcf0-6fbb-46ef-bd62-6490944b5160)—2026-05-28T09:06:32Z

Agent searched memory for prior HIE jumpbox access commands, found Obsidian note `ec2-jumpbox-start-stop` and SSH config with `hie-jmp-prod` host alias.

## Asset 3 (Pieces: 789e6885-496c-4185-b319-838496d5715c)—2026-05-28T09:08:09Z

Agent pulled specific SSH tunnel / SSM port-forward commands for the RDP tunnel from Obsidian note `Protocol - AWS HIE Jumpbox Access`.

## Asset 4 (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)—2026-05-28T09:08:50Z

Full RDP Runbook delivered to user:

## RDP to HIE AWS Cluster

The pattern is: SSM port-forward tunnel (localhost:3389) → Windows RDP app connects to `localhost`.

### Step 1—Authenticate & Start the Jumpbox

```bash
# Log in to AWS SSO
aws sso login --profile eoe-hie

# Start the EC2 jumpbox (it may be stopped)
aws ec2 start-instances \
  --instance-ids i-09f84bb55556a2c10 \
  --region eu-west-2 \
  --profile eoe-hie

# Wait for it to be running
aws ec2 describe-instance-status \
  --instance-ids i-09f84bb55556a2c10 \
  --include-all-instances \
  --query 'InstanceStatuses[0]' \
  --output text \
  --region eu-west-2 \
  --profile eoe-hie
```

### Step 2—Open the SSM Port-forward Tunnel (RDP)

Forwards `localhost:3389` → the jumpbox's RDP port via SSM. Leave running in a terminal tab:

```bash
aws ssm start-session \
  --target i-09f84bb55556a2c10 \
  --document-name AWS-StartPortForwardingSession \
  --parameters '{"portNumber":["3389"],"localPortNumber":["3389"]}' \
  --region eu-west-2 \
  --profile eoe-hie
```

> Note: `~/.ssh/config` has `hie-jmp-prod` host alias with `ProxyCommand aws ssm start-session --target %h --region eu-west-2 --profile ${AWS_PROFILE:-eoe-hie} --document-name AWS-StartSSHSession` for SSH access.

### Step 3—Connect via Windows RDP App

With the tunnel running:

- Open Windows App (Microsoft Remote Desktop)
- Connect to: `localhost` (port `3389`)
- Username: `awsadmin`
- Password: from 1Password → `hie-test-34 jmpbx` (or `EOE awsadmin` entry)
- Saved RDP connection in app: `AWSSDE` (user: `awsadmin`)

### Step 4—Stop the Jumpbox when Done

```bash
aws ec2 stop-instances \
  --instance-ids i-09f84bb55556a2c10 \
  --region eu-west-2 \
  --profile eoe-hie
```

### Quick Reference

| Detail | Value |
|---|---|
| Instance ID | `i-09f84bb55556a2c10` |
| Region | `eu-west-2` |
| AWS profile | `eoe-hie` |
| RDP user | `awsadmin` |
| RDP target (tunnelled) | `localhost:3389` |
| SSO start URL | `https://d-9c677d0fd8.awsapps.com/start` |

Source note: `30_Library/SoT/Protocol - AWS HIE Jumpbox Access.md` in Obsidian vault.