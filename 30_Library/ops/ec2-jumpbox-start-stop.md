---
created: 2026-03-05T10:16:02+00:00
modified: 2026-07-13T08:45:29+00:00
permalink: llmeon/30-library/ops/ec2-jumpbox-start-stop
title: ec2-jumpbox-start-stop
---

Stop the jumpbox:

```bash
aws ec2 stop-instances --instance-ids i-09f84bb55556a2c10 --region eu-west-2 --profile eoe-hie
```

Start the jumpbox:

```bash
aws ec2 start-instances --instance-ids i-09f84bb55556a2c10 --region eu-west-2 --profile eoe-hie
```

Check its current state:

```bash
aws ec2 describe-instance-status --instance-ids i-09f84bb55556a2c10 --include-all-instances --query 'InstanceStatuses[0].InstanceState.Name' --output text --region eu-west-2 --profile eoe-hie
```

If you need to wait for it to be fully running before SSHing in (useful in scripts):

```bash
aws ec2 wait instance-running --instance-ids i-09f84bb55556a2c10 --region eu-west-2 --profile eoe-hie
```

These all assume your CLI is configured with the correct profile/region. If you're working across multiple AWS accounts, add `--profile <name>` and/or `--region <region>` as needed.
