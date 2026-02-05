---
created: 2026-02-05T10:25:38+00:00
modified: 2026-02-05T11:25:22+00:00
title: AWS - HIE - Jumpbox
---

Instance ID: `i-09f84bb55556a2c10`

IAM Role: `eoe-sde-codisc-jumpbox-ssm-role`

`aws ssm start-session --target i-09f84bb55556a2c10`

```sh
aws sso login --profile eoe-hie
aws ec2 start-instances --instance-ids i-09f84bb55556a2c10 --region eu-west-2 --profile eoe-hie
ssh jumphost-ssm
```

It looks like you successfully authenticated the `eoe-hie` profile and started the jump host instance, but the SSH command failed because it doesn\'t know which AWS profile to use.

The `ssh jumphost-ssm` command typically triggers a background AWS command (via `ProxyCommand` in your SSH config). By default, this background command tries to use your `default` AWS profile, not the `eoe-hie` profile you just refreshed.

Here is the quick fix and the explanation.

## 1. The Immediate Fix

You need to tell your current shell (and the SSH command running inside it) to use the `eoe-hie` profile explicitly.

Run this command in your terminal:

```bash
export AWS_PROFILE=eoe-hie
```

Then try your SSH connection again:

```bash
ssh jumphost-ssm
```

## 2. Why This Happened

Your `aws ec2 start-instances` command worked because you manually added `--profile eoe-hie`.

However, when you run `ssh jumphost-ssm`, your SSH client looks at your `~/.ssh/config` file. It likely contains a line similar to this:

```sh
Host jumphost-ssm
    ProxyCommand sh -c "aws ssm start-session --target i-09f84bb55556a2c10 ..."

```

Because that `ProxyCommand` doesn't explicitly specify `--profile eoe-hie`, it falls back to looking for a `default` profile. Since you haven't logged into `default` (only `eoe-hie`), it throws the "Token has expired" error.

## 3. Alternative: Fix it Permanently

If you want to avoid exporting the variable every time, you can edit your SSH config file (`~/.ssh/config`) to force that specific host to always use the correct profile.

Update the `ProxyCommand` line to include the profile flag:

```sh
ProxyCommand sh -c "aws ssm start-session --target i-09f84bb55556a2c10 --profile eoe-hie ..."
```

---

Note on Instance Status:

In your output, the instance `i-09f84bb55556a2c10` was in the `pending` state. It usually takes 1-2 minutes for the instance to reach `running` status and for the SSM Agent to come online.

If you fix the profile issue above and get a new error like `TargetNotConnected`, simply wait a minute for the jump host to finish booting.

Next Step:Once you are SSH'd into the jump host, you can proceed with the DNS Firewall interrogation we discussed. Would you like the specific AWS CLI commands to run _from the jump host_ to find those VPC and Firewall Rule Group IDs?
