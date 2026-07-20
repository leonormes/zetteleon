---
captured: 2026-07-20T13:50:47+01:00 2026-07-20T13:50:47+01:00
created: 2026-07-20T12:50:49+00:00
modified: 2026-07-20T16:34:34+00:00
permalink: llmeon/20-thinking/21-workbench/head-new-chat-1
source: https://gemini.google.com/app/e56d7e0ebf91cea9
status: processing
tags: [input]
title: HEAD In Azure What Exactly Is a Bastion
type: head
---

## Raw Output / Content

You

In Azure what exactly is a bastion? I know what it is for and often use one. But what is it actually? A specialized VM?

---

Gemini

In its simplest terms, an Azure Bastion is a PaaS (Platform as a Service) resource that acts as a managed gateway. While it behaves like a "jump box" or a "bastion host" you might have manually configured in the past, its underlying architecture is more sophisticated than a standard virtual machine.

### The Underlying Infrastructure

To answer your question directly: Yes, it is essentially a cluster of specialised, hardened virtual machines. However, unlike a standard VM that you manage, Azure Bastion is abstracted. When you deploy it, Microsoft provisions a set of scalable VM instances into a dedicated subnet called `AzureBastionSubnet`.

- Managed Scale: You don't see these VMs in your "Virtual Machines" list. Azure manages the patching, scaling, and maintenance of these instances automatically.
- Protocol Translation: The "magic" of Bastion is that it acts as a proxy. It sits between the public internet and your private VNet. It receives traffic over HTTPS (port 443) and then translates that into RDP or SSH to communicate with your target VMs over their private IP addresses.

### How the Connection Flows

Instead of using a client like PuTTY or Remote Desktop Connection directly from your desktop, the connection happens through your web browser using HTML5.

| Step | Component | Action |
| --- | --- | --- |
| 1 | User Browser | Connects to the Azure Portal via HTTPS (443). |
| 2 | Azure Bastion | Authenticates the session and initiates a private RDP/SSH connection. |
| 3 | Target VM | Receives the connection on its Private IP; no Public IP is required on the VM. |

### Key Technical Characteristics

- Non-Exposed Ports: Because the Bastion handles the "jump," you can close port 3389 (RDP) and port 22 (SSH) on your Network Security Groups (NSGs) to all external traffic. You only need to allow traffic coming from the `AzureBastionSubnet`.
- Hardened by Default: Because you cannot log into the Bastion instances themselves or install software on them, the attack surface is significantly smaller than a DIY jump server.
- Tiered Features: \* Basic: Core RDP/SSH functionality.
	- Standard: Supports "IP-based connection" (connecting to VMs in peered VNets) and manual scaling (up to 50 instances).

### Is it just a "Jump Box"?

Conceptually, yes. But technically, it is a highly available, scale-set-based proxy service. It removes the "management overhead" of a jump box—you no longer have to worry about patching the OS of the jump box itself or managing its public IP address and disk space.

> Note: If you are using the Standard SKU, you can even use a local client (like the native RDP client on your laptop) to connect _through_ the Bastion, though it still tunnels the traffic over port 443 to keep things secure.

---

You

We only have 1 actual VM jumpbox. Is using a bastion worth it or should we just ssh to the box instead? My manager keeps trying to get rid of the bastion

---

Gemini

Deciding between a managed Azure Bastion and a DIY Jumpbox usually comes down to whether you want to manage _security_ or _infrastructure_. If you only have one VM, your manager might see Bastion as an unnecessary monthly cost, but there are several "hidden" risks with the jumpbox approach.

Here is a breakdown of how they compare to help you weigh the decision:

### Comparison: Managed Bastion vs. DIY Jumpbox

| Feature | Azure Bastion (PaaS) | DIY Jumpbox (VM) |
| --- | --- | --- |
| Exposure | No Public IP. Communication is via Port 443 (HTTPS). | Public IP required. SSH (22) or RDP (3389) must be open to the internet. |
| Maintenance | Zero. Microsoft handles OS patching and hardening. | Manual. You must patch, update, and secure the jumpbox OS. |
| Cost | Fixed hourly rate. Can be pricey for small environments (~£140+/month). | Low. Only the cost of a small B-series VM (~£10-20/month). |
| Access Control | Integrated with Entra ID (Azure AD) and RBAC. | Managed via SSH keys or local accounts. |
| Auditability | Full session logging and monitoring integrated with Azure. | Requires manual setup of syslog or screen logging. |

### When to Keep the Jumpbox

If your primary concern is cost and you have a very small environment, the jumpbox is hard to beat. To make it "safe," you should ideally:

- Use Just-In-Time (JIT) VM Access (requires Microsoft Defender for Cloud) to keep ports closed except when needed.
- Restrict the Source IP in your Network Security Group (NSG) to only your office or home IP.
- Use SSH Keys only—never passwords.

### When to Fight for the Bastion

The Bastion is the "modern" way to do this for a few specific reasons:

1. Eliminating the "Pivot Point": If a jumpbox is compromised, the attacker has a full Linux/Windows environment to run tools, scan your network, and escalate. A Bastion is a locked-down proxy; there is no "shell" for an attacker to sit in.
2. Ease of Access: You can access your VMs directly through the Azure Portal in a browser. This is helpful if you are on a locked-down machine where you can't use an SSH client.
3. No Public IPs: With Bastion, your entire VNet can stay completely private. You don't need a single Public IP address in your environment, which significantly simplifies your security audit.

### The "Starter Task" Approach

If your manager is worried about the cost, one compromise is the Developer SKU (if available in your region). It is much cheaper but lacks some features like VNet peering support.

Alternatively, if you find that managing the jumpbox is becoming a "chore" that distracts you from your actual engineering work, that is your strongest argument. A Bastion is "set and forget," whereas a jumpbox is another pet that needs feeding.

Is your manager primarily concerned about the monthly cost, or is it more about the complexity of the setup?
