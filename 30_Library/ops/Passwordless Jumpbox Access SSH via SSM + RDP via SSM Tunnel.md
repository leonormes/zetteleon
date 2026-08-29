---
created: 2026-07-28T09:21:54+00:00
modified: 2026-08-29T09:36:47+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-28-2026-10-21am
title: Passwordless Jumpbox Access SSH via SSM + RDP via SSM Tunnel
type: note
---

## Passwordless Jumpbox Access: SSH via SSM + RDP via SSM Tunnel

The core idea: stop authenticating to the jumpbox with a username/password at all. AWS Systems Manager (SSM) Session Manager replaces that step with IAM-based authorization—your AWS credentials (SSO/IAM role) are what grant access, not a local OS password. This works for both SSH and RDP through the same mechanism, just with a different SSM document.

### How the Auth Model Changes

Per AWS's Session Manager documentation (docs.aws.amazon.com, confirmed via web search, though the search tool did not return individual clickable citation URLs this time—only a domain-scoped answer):

- Access is gated by `ssm:StartSession` IAM permission, scoped to the target instance ARN and to the specific SSM document (`AWS-StartPortForwardingSession` or `AWS-StartSSHSession`).
- For SSH specifically, the managed node needs SSH running and SSM Agent ≥ 2.3.672.0; AWS's own guidance says you can then allow/deny access purely with IAM policy, no OS password required.
- For RDP, there is no equivalent "SSM RDP session"—RDP still needs its own transport, so the pattern is a local port-forward tunnel (`AWS-StartPortForwardingSession`, local port → remote `3389`), with your native RDP client pointed at `localhost:<local-port>`. The Windows-side login inside that tunnel is a separate, still-necessary authentication step (see caveat below).
- If you forward to a _remote host_ behind the managed instance (`AWS-StartPortForwardingSessionToRemoteHost`), you additionally need the `ssmmessages:CreateControlChannel` / `CreateDataChannel` / `OpenControlChannel` / `OpenDataChannel` permissions—a commonly missed requirement.

### SSH: Key-based, no Password

```bash
# One-liner using an SSH config alias with ProxyCommand
AWS_PROFILE=<your-profile> ssh jumphost-ssm
```

`~/.ssh/config` entry that makes this work (auth is your SSH key against `authorized_keys`—never a password):

```text
Host jumphost-ssm
  HostName <instance-id>
  User <os-user>
  ProxyCommand sh -c "aws ssm start-session --target %h --profile <your-profile> --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
```

Or manually forward the SSH port and connect separately:

```bash
aws ssm start-session \
  --target <instance-id> \
  --document-name AWS-StartPortForwardingSession \
  --parameters '{"portNumber":["22"],"localPortNumber":["2222"]}' \
  --region <region> --profile <your-profile>

ssh -p 2222 <os-user>@localhost   # public key auth, no password prompt
```

### RDP: SSM Tunnel + RDP Client, no Interactive AWS Password

```bash
aws ssm start-session \
  --target <instance-id> \
  --document-name AWS-StartPortForwardingSession \
  --parameters '{"portNumber":["3389"],"localPortNumber":["3389"]}' \
  --region <region> --profile <your-profile>
```

Then point your Windows RDP client at `localhost:3389`. Caveat confirmed by the AWS-documentation search: this tunnel only removes the _AWS-side_ password requirement (SSM auth = your IAM identity). The actual Windows logon inside the RDP session is a separate credential. AWS's own two supported options here are:

- Windows username/password (still a password, just not an AWS one), or
- EC2 key pair (`.pem`) to decrypt the initial admin password, or
- IAM Identity Center session—if you're signed in via IAM Identity Center in the console, AWS's Fleet Manager RDP path can skip re-entering Windows credentials.

So: full end-to-end no password anywhere for RDP realistically means routing through Fleet Manager + IAM Identity Center, or accepting that the Windows OS login itself still needs _some_ credential (password or cert-based Windows auth)—Fleet Manager does not auto-generate a temporary Windows password for you.

### Linux Passwordless RDP Alternative (Xrdp)

If your RDP target is Linux (xrdp) rather than Windows, true SSH-key-based RDP auth is not a native xrdp feature. It's achievable only via a PAM workaround: configure `pam_ssh_agent_auth` in the PAM stack xrdp invokes, with `SSH_AUTH_SOCK` forwarded from an agent—this is a custom integration, not an out-of-box xrdp setting.

### IAM Policy Scoping (Least pRivilege)

```json
{
  "Effect": "Allow",
  "Action": "ssm:StartSession",
  "Resource": [
    "arn:aws:ec2:<region>:<account-id>:instance/<instance-id>",
    "arn:aws:ssm:<region>::document/AWS-StartPortForwardingSession",
    "arn:aws:ssm:<region>::document/AWS-StartSSHSession"
  ]
}
```

Add `ssm:TerminateSession` scoped to the caller's own session ARN pattern, and `ec2:DescribeInstances` / `ssm:Describe*` as read-only helpers.

### Note on the Jumpbox Identifiers in Your Notes

Your existing runbook (surfaced from `search_memory`, e.g. `event 96e7e8ce-0296-4374-99cf-bc1daa0b68a0`—"Protocol - AWS HIE Jumpbox Access") already documents this exact instance using:

- Target instance `i-09f84bb55556a2c10`
- IAM role `eoe-sde-codisc-jumpbox-ssm-role`
- Profile `eoe-hie`, region `eu-west-2`

and an `~/.ssh/config` `jumphost-ssm` host alias with `ProxyCommand aws ssm start-session --target %h … --document-name AWS-StartSSHSession`, plus a separate `AWS-StartPortForwardingSession` tunnel on `3389` for RDP—i.e., you already have this exact SSH-via-SSM pattern working for your HIE jumpbox. The remaining gap based on your question is that some other jumpbox in your fleet is still using username/password auth rather than this pattern; if you tell me which instance/profile that is, I can check memory for its current config and adapt the policy above to it specifically.
