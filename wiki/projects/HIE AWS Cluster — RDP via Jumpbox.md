---
title: HIE AWS Cluster — RDP via Jumpbox
wiki_type: dossier
entity_kind: project
created: 2026-05-28T22:15:00+00:00
modified: 2026-05-28T22:15:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-05-28-pieces-hie-aws-rdp
---

## Summary

Operational runbook for accessing the HIE (Health Information Exchange) AWS cluster via RDP through an EC2 jumpbox. The connection pattern uses an SSM port-forward tunnel from `localhost:3389` to the jumpbox, then the Windows RDP app connects to `localhost`. Documented and verified on 2026-05-28.

## Key Facts

- **Connection pattern:** SSM port-forward tunnel (`localhost:3389`) → Windows RDP app connects to `localhost` — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)
- **Jumpbox EC2 instance:** `i-09f84bb55556a2c10` in `eu-west-2` — must be started via `aws ec2 start-instances` if stopped — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)
- **AWS profile:** `eoe-hie` — SSO login URL: `https://d-9c677d0fd8.awsapps.com/start` — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)
- **SSM port-forward command:** `aws ssm start-session --target i-09f84bb55556a2c10 --document-name AWS-StartPortForwardingSession --parameters '{"portNumber":["3389"],"localPortNumber":["3389"]}' --region eu-west-2 --profile eoe-hie` — must remain running in a terminal tab — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)
- **RDP credentials:** Username `awsadmin`, password from 1Password entry `hie-test-34 jmpbx` (or `EOE awsadmin`) — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)
- **Saved RDP connection:** `AWSSDE` in Windows App — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)
- **SSH access alternative:** `hie-jmp-prod` host alias in `~/.ssh/config` uses `ProxyCommand aws ssm start-session --target %h --region eu-west-2 --profile ${AWS_PROFILE:-eoe-hie} --document-name AWS-StartSSHSession` — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)
- **Source Obsidian note:** `30_Library/SoT/Protocol - AWS HIE Jumpbox Access.md` — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 789e6885-496c-4185-b319-838496d5715c)
- **Jumpbox must be stopped when done:** `aws ec2 stop-instances --instance-ids i-09f84bb55556a2c10 --region eu-west-2 --profile eoe-hie` — [[raw/2026-05-28-pieces-hie-aws-rdp]] (Pieces: 5f2798af-0061-4829-b92f-b2dc771d67e3)

## Timeline

- **2026-05-28T09:06:** User requested RDP commands for HIE AWS cluster — runbook retrieved from Obsidian note `Protocol - AWS HIE Jumpbox Access` and delivered as a 4-step guide (authenticate → tunnel → RDP → stop)
- **2026-05-28T22:15:** Runbook formalized into this wiki dossier from Pieces LTM captures

## Connections

- [[AWS SSM Session Troubleshooting]] — related SSM connectivity project
- [[FITFILE-Testing-Infrastructure]] — broader FITFILE infrastructure context

## Contradictions

None identified.

## Open Questions

- Is the jumpbox (`i-09f84bb55556a2c10`) set to auto-stop to save costs, or must it always be manually stopped?
- Has MFA been configured for the `eoe-hie` AWS SSO profile?
