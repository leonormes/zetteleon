---
created: 2026-07-28T09:33:47+00:00
modified: 2026-07-28T09:36:49+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-28-2026-10-33am
title: AWS options for accessing the private EKS cluster API from your local machine — ranked by security
type: note
---

## AWS Options for Accessing the Private EKS Cluster API from Your Local machine—ranked by Security

You currently use SSM to reach a jumpbox in the private VPC on AWS, and Azure Bastion on the Azure side. For the EKS Kubernetes API specifically, AWS gives you four distinct mechanisms, and they solve different layers of the problem—network-level tunnel, zero-trust per-request access, and private service connectivity. No LTM notes on this exact pattern were found in your workstream (`search_memory` returned only tangential EKS/kubectl troubleshooting events, e.g. `1f4f798f-b64d-4533-936b-2c5336e8f93a` "Kubectl Debugging & Fixes" and `030a03cb-a114-4446-b6cf-e4448c1172e8` "Kubernetes, Certs, and Vault Updates"), so this is a fresh advisory grounded in AWS documentation via web search.

### The Options, in order of Security Posture

1. AWS Verified Access—strongest, zero-trust
2. AWS PrivateLink (for the EKS management API surface)—strong, no internet exposure
3. AWS Client VPN / Direct Connect—strong, but places the user on the network
4. SSM Session Manager port-forwarding to a bastion-less instance—good, avoids inbound SSH/RDP exposure, closest to what you already do
5. Classic bastion host with public IP—weakest of the standard patterns (what you're moving away from)

### 1. AWS Verified Access—closest Equivalent to "Bastion, but zEro-trust"

Verified Access evaluates identity and device posture on every request rather than putting the user on the VPC network at all. AWS's own networking guidance states Client VPN puts the user _on_ the network while Verified Access puts the _application_ behind a zero-trust policy engine, and explicitly recommends Verified Access as the preferred option for new application-access use cases. For `kubectl` access specifically this is a stronger posture than VPN because a compromised laptop or leaked credential doesn't grant broad network reachability—only scoped, continuously-checked access to the specific endpoint.

### 2. AWS PrivateLink—private Connectivity to the EKS Management API Surface

AWS documents PrivateLink as a private connection between your VPC and Amazon EKS management APIs, avoiding the public internet entirely. Per AWS's EKS cluster endpoint documentation, confirmed in this pass:

- With private endpoint access only (`endpointPrivateAccess=true`, public access disabled), there is no public path to the API server at all.
- Reaching that private endpoint from outside the cluster VPC requires VPN, Direct Connect, Transit Gateway, or VPC peering—PrivateLink itself is the mechanism that lets those connected networks resolve and route to the EKS API privately.
- Your VPC needs correct DNS support (`enableDnsHostnames` / `enableDnsSupport`) for the private hosted zone to resolve—a common setup gotcha AWS flags directly.
- Note: PrivateLink is not itself a "log in as a human" tool—it's the private-networking primitive that VPN/Direct Connect/Transit Gateway ride on top of to reach the private endpoint without traversing the internet.

### 3. AWS Client VPN—most Direct Like-for-like with Azure Bastion

Client VPN tunnels your laptop directly into the VPC at the network level, then `kubectl` just works against the private endpoint like any in-VPC client. This is the most operationally simple option and matches the mental model you already have from Azure Bastion, but it does put the user's laptop on the network—broader blast radius than Verified Access if the laptop or credential is compromised.

### 4. SSM Session Manager port-forwarding—what You Already Do, Applied to the K8s API

Same pattern as your existing RDP/SSH jumpbox tunnel, just forwarding to port 443 on the EKS API endpoint instead of 3389/22:

```bash
aws ssm start-session \
  --target <instance-id> \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["<PRIVATE_EKS_API_ENDPOINT>"],"portNumber":["443"],"localPortNumber":["6443"]}' \
  --region <region> --profile <profile>
```

Then point `kubectl` at `https://localhost:6443` (with the cluster's CA cert / kubeconfig adjusted accordingly). This requires the `AWS-StartPortForwardingSessionToRemoteHost` document specifically (not the plain `AWS-StartPortForwardingSession` you use for RDP), and needs the extra `ssmmessages:CreateControlChannel` / `CreateDataChannel` / `OpenControlChannel` / `OpenDataChannel` permissions on top of `ssm:StartSession`—a commonly-missed requirement per AWS community guidance. Security-wise this is solid: no inbound ports on the jumpbox, IAM gates the tunnel, and the instance still needs to be reachable inside the VPC (SSM Agent makes only outbound calls to AWS)—it's a good middle ground and reuses infrastructure you already trust.

### 5. Classic Bastion with Public IP—least Secure

Still technically an AWS-documented option for reaching a private EKS endpoint, but it requires exposing and hardening an internet-facing instance with SSH access—the pattern you're explicitly trying to move away from for the jumpbox itself.

### Recommendation

Given you're already running SSM cleanly for the jumpbox and want the equivalent of Azure Bastion's zero-trust feel:

- If you want a direct behavioral match to Azure Bastion: AWS Client VPN is the closest, but consider layering Verified Access on top for the API-server access path specifically, since AWS positions it as the stronger zero-trust successor for exactly this kind of "reach a private control-plane API" use case.
- If you want to reuse what you already operate (SSM): extend your existing SSM jumpbox pattern with `AWS-StartPortForwardingSessionToRemoteHost` targeting the EKS API endpoint—zero new infrastructure, same IAM-gated tunnel model as your RDP/SSH setup, no inbound ports anywhere.
- For the most security-hardened setup overall: disable EKS public endpoint access entirely (`endpointPrivateAccess=true`, public disabled), reach it exclusively via PrivateLink-backed private connectivity, and gate individual engineer access through Verified Access rather than a broad network-level VPN tunnel.

Citation caveat: the AWS-domain-restricted web search returned a synthesized answer citing AWS's EKS cluster endpoint docs and PrivateLink docs by content, but did not surface individual clickable source URLs in the tool output for me to link here—the underlying pages are `docs.aws.amazon.com`'s Amazon EKS cluster endpoint access control page and the AWS PrivateLink/EKS blog, but I don't have the exact URL strings to cite without fabricating them. If you want, I can re-run a search asking explicitly for the URL of "Amazon EKS cluster endpoint access control" and the EKS PrivateLink announcement so you have direct links for your runbook.
