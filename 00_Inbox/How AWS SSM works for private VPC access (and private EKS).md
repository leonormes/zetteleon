---
created: 2026-07-30T20:24:53+00:00
modified: 2026-07-31T09:14:04+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-30-2026-9-24pm
title: How AWS SSM works for private VPC access (and private EKS)
type: note
---

## How AWS SSM Works for Private VPC Access (And pRivate EKS)

### 1. General: Session Manager into a Private VPC

SSM Session Manager is reverse-connect, not inbound SSH.

1. An SSM Agent runs on a managed EC2 instance (Amazon Linux, Ubuntu, Windows, etc.).
2. The agent makes outbound HTTPS connections to AWS Systems Manager.
3. Your laptop (AWS CLI + Session Manager plugin) asks SSM to start a session.
4. SSM pairs your session request with the agent's existing outbound channel.
5. Traffic never needs an inbound security-group rule, public IP, bastion SSH, or internet gateway on the instance.

That is why it works cleanly in private subnets.

#### Control Plane Vs Data Plane

| Path | VPC interface endpoint | Role |
|---|---|---|
| Systems Manager API | `com.amazonaws.<region>.ssm` | Start/list/terminate sessions, SendCommand, etc. |
| Agent ↔ service control messages | `com.amazonaws.<region>.ec2messages` | Agent registration, status, heartbeats |
| Interactive session / port-forward data | `com.amazonaws.<region>.ssmmessages` | Encrypted session / stream data |

Those three Interface VPC Endpoints (PrivateLink) are the minimum for private-only Session Manager. Extra endpoints (`logs`, `s3`, `kms`, `ec2`) are only for features like session logging, S3 log delivery, or KMS encryption—not basic access.

Security model: IAM controls who can start sessions and on which nodes (`ssm:StartSession`, document restrictions, tag conditions). There is no open SSH port to attack. Sessions can be logged to CloudWatch/S3.

Docs:

- [Use AWS PrivateLink to set up a VPC endpoint for Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-create-vpc.html)
- [Session Manager prerequisites](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-prerequisites.html)

---

### 2. Port-forwarding Mechanics

Two session documents matter:

A. Port on the managed instance itself
`AWS-StartPortForwardingSession`

```bash
aws ssm start-session \
  --target i-0123456789abcdef0 \
  --document-name AWS-StartPortForwardingSession \
  --parameters '{"portNumber":["80"],"localPortNumber":["56789"]}'
```

Flow: `localhost:56789` → SSM tunnel → that EC2's port 80.

B. Port on another host the instance can reach (jump / proxy)
`AWS-StartPortForwardingSessionToRemoteHost`

```bash
aws ssm start-session \
  --target i-0123456789abcdef0 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{
    "host":["internal.example.local"],
    "portNumber":["443"],
    "localPortNumber":["8443"]
  }'
```

Flow: `localhost:8443` → SSM tunnel → managed EC2 → TCP to remote host:port inside the VPC.

This second mode is what you use for RDS, internal ALBs, private EKS API endpoints, etc.—anything the hop instance can route to, that is not listening on the hop itself.

Requirements:

- Recent enough SSM Agent + Session Manager plugin
- IAM permission to start the specific document
- Network path from hop → target (SG, NACL, routing)
- Hop reaches the three SSM VPC endpoints (or internet via NAT)

---

### 3. Private EKS API Server via SSM

#### How Private EKS Endpoints Work

With private-only (or private+public disabled) EKS:

- The API server hostname resolves to private ENIs in your VPC (or a linked VPC via PrivateLink-style cluster networking).
- Clients must reach that private IP:443 from inside the network path—no public `eks.amazonaws.com` path for cluster API traffic.
- `kubectl` talks HTTPS to `https://<cluster-id>.gr7.<region>.eks.amazonaws.com` (exact DNS from `aws eks describe-cluster`).

You cannot "SSM directly into the EKS control plane." The control plane is AWS-managed. You SSM into something in (or attached to) the VPC, then port-forward to the API server DNS/IP.

#### Typical Pattern: SSM Jump Instance + Remote-host forward

```text
Laptop (kubectl)
    │  localhost:6443
    ▼
SSM Session Manager tunnel  (ssmmessages)
    │
    ▼
Private EC2 “ops” hop  (SSM Agent, private subnet)
    │  TCP 443 inside VPC
    ▼
EKS private API endpoint ENI :443
```

Example:

```bash
# 1) Get private API endpoint
ENDPOINT=$(aws eks describe-cluster --name my-cluster \
  --query 'cluster.endpoint' --output text)
# https://ABCDEF123.gr7.eu-west-1.eks.amazonaws.com

HOST=${ENDPOINT#https://}

# 2) Port-forward through hop instance
aws ssm start-session \
  --target i-0abcopsjump \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters "{\"host\":[\"$HOST\"],\"portNumber\":[\"443\"],\"localPortNumber\":[\"6443\"]}"

# 3) Point kubeconfig at localhost (TLS name must still match cert)
kubectl --server=https://127.0.0.1:6443 \
  --insecure-skip-tls-verify=false \
  get nodes
```

TLS gotcha: The API server cert is issued for the EKS endpoint hostname, not `127.0.0.1`. Common fixes:

- Put the real hostname in kubeconfig `server:` and map it in `/etc/hosts` → `127.0.0.1`, or
- Use `kubectl` with a custom CA and SNI-aware local proxy, or
- Temporarily use a wrapper that sets `server: https://<real-host>:6443` while traffic hits the forwarded local port via hosts override.

Most teams do:

```text
# /etc/hosts
127.0.0.1  ABCDEF123.gr7.eu-west-1.eks.amazonaws.com
```

and keep `server: https://ABCDEF123.gr7….eks.amazonaws.com:6443` in kubeconfig while SSM forwards local `6443` → remote `443`.

#### What the Hop Needs

- SSM Agent + instance profile (`AmazonSSMManagedInstanceCore` or tighter custom policy)
- SG egress to:
  - SSM interface endpoints (443)
  - EKS API SG / control-plane ENIs (443)
- Same VPC (or routed VPC/peering/TGW) as the cluster
- Optional: no public IP, private subnets only

EKS cluster security group / additional SGs must allow 443 from the hop's SG (or hop subnet CIDR).

---

### 4. Alternatives and Tradeoffs

| Approach | Pros | Cons |
|---|---|---|
| SSM port-forward via hop | No inbound bastion ports; IAM + audit; works in fully private VPC; low cost | Per-user sessions; TLS/hosts dance; not great for many concurrent CI agents without pooling |
| Classic SSH bastion | Familiar | Inbound 22, key sprawl, patch burden |
| VPN / Client VPN / Direct Connect | Full network membership; native DNS/TLS | Heavier ops; always-on connectivity |
| EKS public endpoint + restricted CIDRs | Simple kubectl | Broadens attack surface; not "private only" |
| PrivateLink to EKS (cross-account/VPC patterns) | Clean service exposure | More networking design; still need a path from the client network |
| Systems Manager + EC2 Instance Connect / bastion apps | Still SSM-backed | Same hop model, different bootstrap |

Practical recommendation:

- Day-to-day human `kubectl` / `helm` from a laptop → SSM remote-host port-forward through a small hardened ops instance (or ASG of them) is standard and solid.
- CI/CD / fleet of agents → prefer runners inside the VPC (CodeBuild VPC, self-hosted Actions runners, GitLab runners on private subnets) so they hit the private endpoint natively without tunnels.
- Strong production baseline → private EKS endpoint + SSM for break-glass humans + in-VPC automation; avoid long-lived public API access.

---

### 5. End-to-end Checklist (Private EKS + SSM)

1. EKS endpoint config: private `true`, public as required by policy.
2. Three SSM interface endpoints (`ssm`, `ssmmessages`, `ec2messages`) in the hop's subnets; private DNS enabled.
3. Hop EC2: SSM Agent healthy in Fleet Manager; correct instance profile.
4. SGs: hop → endpoints 443; hop → EKS API 443.
5. IAM: user/role may `ssm:StartSession` on hop + allowed documents.
6. Local: AWS CLI v2 + Session Manager plugin.
7. Session: `AWS-StartPortForwardingSessionToRemoteHost` to EKS API host:443.
8. kubeconfig/hosts aligned so TLS hostname matches.
9. Auth: still normal EKS auth (`aws eks get-token` / IAM authenticator)—SSM only carries TCP; it does not replace IAM/Kubernetes RBAC.

---

Bottom line: SSM does not open the VPC. The agent dials out to AWS; you attach a managed, encrypted tunnel to that channel. For private EKS, that tunnel terminates on a managed hop in the VPC, which then makes a normal VPC-local TCP connection to the private API server ENI on 443. Identity for Kubernetes remains IAM + RBAC; SSM is only the network path.
