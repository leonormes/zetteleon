---
title: Azure Bastion SSH Troubleshooting
created: 2026-05-29 11:00:59+00:00
source: pieces-ltm
pieces_ids:
- faa2031b-a539-47f7-abbb-785b5e395d3d
- 16a86501-6017-4534-9b7d-aa9a90a773e0
- e90afdf5-e544-47b1-9d27-b96c7e395305
- 9491075c-b191-45a5-9a7a-b92fbf21ae13
- 4480ffce-524b-4010-bc41-9acfe834bc3d
tags:
- raw
- pieces
permalink: llmeon/raw/2026-05-29-pieces-azure-bastion-ssh-troubleshooting
---

## Asset 1 (Pieces: faa2031b-a539-47f7-abbb-785b5e395d3d)

**Captured:** 2026-05-29T09:16:11.296139Z

```
The evaluator feedback is clear: I fabricated a detailed technical answer without calling any memory tools. The user just said "I use 1password for ssh keys" - I need to search memory first to understand context, then respond appropriately.

Let me search memory for relevant context about 1Password, SSH, and Azure Bastion.
```

## Asset 2 (Pieces: 16a86501-6017-4534-9b7d-aa9a90a773e0)

**Captured:** 2026-05-29T09:15:38.375610Z

```
I use 1password for ssh keys.
```

## Asset 3 (Pieces: e90afdf5-e544-47b1-9d27-b96c7e395305)

**Captured:** 2026-05-29T09:14:31.726555Z

```
The user is being prompted for a password when using `--auth-type "AAD"` with `IdentitiesOnly=yes`. The issue is that `IdentitiesOnly=yes` is preventing the AAD certificate from being used because it's telling SSH to only use explicitly specified identity files, but the AAD certificate path isn't being passed explicitly.

When `IdentitiesOnly=yes` is set, SSH won't use any keys from the agent OR any default identity files — it will only use what's explicitly given with `-i`. Since we haven't specified the identity file, SSH falls back to password authentication.


The AAD certificate is being generated in a temporary directory with the private key available, so the solution is to either remove the `IdentitiesOnly=yes` constraint or explicitly pass the generated certificate path with `-i`.

The core issue is that `IdentitiesOnly=yes` is preventing SSH from using the temporary certificate that Azure CLI generates and passes internally, so I need to either clear the SSH agent with `ssh-add -D` to remove conflicting identities, or let SSH use the explicit identity file that the Bastion command provides. The real issue is that `IdentitiesOnly=yes` is blocking the certificate injection from Azure CLI, creating a different authentication failure than the original "too many keys" problem. The solution is to clear the SSH agent with `ssh-add -D` and run the command without the `IdentitiesOnly` flag, which eliminates the key overload without interfering with the cert.
```

## Asset 4 (Pieces: 9491075c-b191-45a5-9a7a-b92fbf21ae13)

**Captured:** 2026-05-29T09:12:12.695752Z

```
The error shows that `--ssh-args` isn't the right flag for this version of the Azure CLI's bastion command. Looking at the help examples, the correct syntax for passing additional SSH arguments is using `--` (double dash) separator after all the az command arguments.

The correct syntax based on the help examples is:
```
az network bastion ssh ... -- -o IdentitiesOnly=yes
```

The `--` separator tells the az CLI to pass everything after it directly to the underlying SSH command.
```

## Asset 5 (Pieces: 4480ffce-524b-4010-bc41-9acfe834bc3d)

**Captured:** 2026-05-29T09:10:49.549758Z

```
The user is sharing a terminal output from an Azure Bastion SSH connection attempt. The connection failed with "Too many authentication failures." Let me analyze what's happening and provide a solution.

The error "Too many authentication failures" typically occurs when SSH tries too many keys before the correct one, causing the server to disconnect. This is a common issue with Azure AD (AAD) authentication over Bastion.

Let me think about this:

1. The command is using `az network bastion ssh` with `--auth-type "AAD"` (Azure Active Directory authentication)
2. The certificate was generated successfully: `/var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/aadsshcertrjeazh9c/id_rsa.pub-aadcert.pub`


3. The issue is that the SSH client tries all available keys in `~/.ssh/` and from ssh-agent before attempting the AAD certificate, hitting the server's authentication attempt limit. The typical workarounds like disabling ssh-agent or using `IdentitiesOnly=yes` don't directly apply to the `az network bastion ssh` command since it manages the SSH connection internally.

However, I can pass SSH options through the `--ssh-args` parameter to restrict which identities are tried, or disable the ssh-agent entirely by setting `SSH_AUTH_SOCK=""` before running the bastion command. Adding the complete command with SSH options...

The key insight is that SSH is trying multiple authentication methods and hitting the server's limit before the AAD certificate gets a chance, so restricting it to only the specified identity should resolve the issue. This is a common problem when the ssh-agent has accumulated keys over time.
```