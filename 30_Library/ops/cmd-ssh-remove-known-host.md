---
captured: "2026-02-16T10:51:49+00:00 2026-02-16T10:51:49+00:00"
created: 2026-02-16T10:51:52+00:00
modified: 2026-02-16T10:53:34+00:00
source: "https://gemini.google.com/app/26db32d1ec9ca6e9"
status: "processing"
tags: ["input"]
title: REMOTE HOST IDENTIFICATION HAS CHANGED
type: "head"
---

```sh
Host hie-jmp-test
HostName i-0c1d974fcac60d438
User awsadmin
IdentityFile ~/.ssh/jumpbox\_awsadmin\_key
IdentitiesOnly yes
PreferredAuthentications publickey
PubkeyAuthentication yes
ServerAliveInterval 60
ServerAliveCountMax 3
RequestTTY yes
ForwardX11 no
ForwardAgent no
ProxyCommand sh -c "aws ssm start-session --target %h --region eu-west-2 --profile ${AWS\_PROFILE:-eoe-hie} --document-name AWS-StartSSHSession --parameters 'portNumber=22'"
❯ ssh hie-jmp-test

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:CD5YbenBMWHzutOSRLl6hp2x6MjpE0ZwydeZTVy4mh4.
Please contact your system administrator.
Add correct host key in /Users/leon.ormes/.ssh/known\_hosts to get rid of this message.
Offending ECDSA key in /Users/leon.ormes/.ssh/known\_hosts:40
Host key for i-0c1d974fcac60d438 has changed and you have requested strict checking.
Host key verification failed.
```

---

This error is a common security safeguard. It occurs because your `known_hosts` file contains a specific digital "fingerprint" for that AWS instance ID, but the instance is now presenting a different one.

Since you are connecting via AWS SSM to an EC2 instance, this usually happens if the instance was terminated and recreated with the same ID, or if the SSH host keys on the OS were regenerated.

---

## The Quick Fix

To resolve this, you need to remove the outdated key entry from your local `known_hosts` file. You can do this automatically using the `ssh-keygen` utility:

Bash

```sh
ssh-keygen -R i-0c1d974fcac60d438
```

### What This Command Does

1. It searches your `/Users/leon.ormes/.ssh/known_hosts` file for the hostname `i-0c1d974fcac60d438`.
2. It removes the old, offending key (specifically the one on line 40 mentioned in your error).
3. It creates a backup of your old hosts file (usually named `known_hosts.old`) just in case.

---

## Reconnecting

Once the old key is removed, simply run your SSH command again:

Bash

```sh
ssh hie-jmp-test
```

Note: You will be prompted with a message saying:`The authenticity of host 'i-0c1d974fcac60d438 (<no hostip for proxy>)' can't be established.`

Type yes to accept the new fingerprint and save it to your file.
