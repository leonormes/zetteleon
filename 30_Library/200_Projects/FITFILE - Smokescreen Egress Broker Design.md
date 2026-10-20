---
conformant: true
created: 2026-10-20 10:57:54+01:00
modified: 2026-10-20 10:57:54+01:00
project_category: devops
project_name: Egress Security
status: draft
tags:
- fitfile
- infra
- security
- egress
- kubernetes
- smokescreen
- sde
- design
title: FITFILE - Smokescreen Egress Broker Design
type: project
permalink: llmeon/30-library/200-projects/fitfile-smokescreen-egress-broker-design
---

## FITFILE—Smokescreen Egress Broker for Secure Clusters

Status: draft design note, 2026-10-20. No decision taken.

> Provenance. Agent-drafted from a read-only review of the `Deployment` repo and [[LLM - Egress Broker]] (29 Sep research paste). Nothing here was checked against a live cluster. Statements about Smokescreen come from earlier research reports, not from testing. Review before relying on it.

---

### 1. Decision Sought

Whether to put Stripe's [Smokescreen](https://github.com/stripe/smokescreen) in front of the fitconnect and task pods as their only route out in FITFILE secure data environment (SDE) clusters.

Recommendation: run the two-day spike (§8). Adopt only if the open points in §7 settle.

### 2. Problem

fitconnect opens connections to destinations a user supplies: datasource hosts, object stores, peer nodes. A compromised or misused connector could be pointed at the cloud metadata endpoint, cluster ranges, other namespaces or the open internet. The controls that should stop this are weaker than they look (§3).

### 3. Current State

|Layer|What it does|Gap|Where|
|---|---|---|---|
|AWS Network Firewall (EoE prod, `hie-sde-v2`)|Default action `drop_strict`, strict rule order.|`tcp_outbound_allow` (priority 100) passes any TCP from the VPC CIDR to any destination and port. It sits above the HTTPS allow-list (priority 200), so the five IP rules for quay.io, auth.docker.io, Calico Cloud and two AWS ranges never decide a TCP flow. Outbound TCP is effectively open. The same priority-100 rule is in `hie-test-34` and `test-sde-v2`. It may be deliberate (for example on-prem database access); confirm with the owner.|`Clusters/eoe/Production/hie-sde-v2/modules/gateway/main.tf:199` and `:263`. `firewall_enabled` defaults to true and is not overridden.|
|fitconnect egress NetworkPolicy|Allows DNS, same-namespace pods, `allowNamespaces` (spicedb), `/32` allow-CIDRs, then `0.0.0.0/0` except link-local, Azure WireServer and `denyCidrs`.|A deny-list, not an allow-list. Private ranges stay open unless added to `denyCidrs`. `enabled: false` by default.|`deployment/charts/components/fitconnect/templates/fitconnect-networkpolicy.yaml:47`, `values.yaml:126`|
|Calico on-prem CIDR policy|Scopes egress to an on-prem SQL range to pods labelled `egress-onprem-db`.|Per-CIDR only, and the policy is a commented-out example in this file.|`Clusters/eoe/Production/eenuh-prod-1/application/values.yaml:153`|
|CUH customer proxy|AKS `http_proxy_config` routes outbound traffic through the customer's proxy, with a long `no_proxy` list.|The customer proxy is the enforcement point and resolves DNS itself.|`Clusters/eoe/Production/CUH-DP/main.tf:52`|
|Mutating proxy webhook|Injects proxy environment variables into pods at creation.|Environment-based. The connector drivers ignore `HTTP_PROXY`, so this is the wrong vehicle (per [[LLM - Egress Broker]]).|`deployment/charts/components/mutating-proxy-webhook`|

### 4. Proposal

```
fitconnect / task pod ──CONNECT host:port──▶ Smokescreen ──▶ destination
(NetworkPolicy: DNS, platform deps,          (resolve, classify,
 and the broker only)                         check policy, pin IP, log)
```

- **Broker.** A Smokescreen Deployment with at least two replicas and a disruption budget. No credentials, no cloud identity, no service account token. Mutual-TLS identity per client.
- **Pods.** The fitconnect and task pods get a NetworkPolicy allowing DNS, platform dependencies and the broker only.
- **Dialers.** Each connector gets an explicit dialer through the broker. Injection points: pg (`stream`), mysql2 (`stream`), tedious (`connector`), axios (agent), S3 client (request handler).
- **Policy tiers.**
    - Public destinations: allowed, with the private-range checks.
    - Operator-declared private prefixes (for example on-prem SQL): allowed, held in broker config.
    - Anything else: an operator change.
- **Policy source.** Independent of fitconnect's registry. If the broker trusts the registry, a compromised fitconnect can approve its own destinations.
- **Rollout.** Report mode first, then enforce.

### 5. What It Adds in Secure Clusters

- Default-deny for connector pods, with no bypass route.
- Non-public IPs blocked by default: metadata endpoint, node and cluster ranges, other namespaces.
- Hostname-level policy and per-client identity. The AWS firewall rules match IPs only.
- One log of allowed and denied connections, usable as SDE audit evidence.
- The same control on AWS and Azure, instead of cloud-specific firewall rules per customer.

### 6. What It Does Not Fix

- Nodes, system pods and other workloads. The AWS firewall rule in §3 still needs its own fix: remove or reorder the allow-all TCP group, or move to domain-based rules. That is independent of the broker.
- The broker is a high-value target and a dependency for every query. Keep it out of fitconnect's liveness probe, or an outage becomes a restart loop.
- The customer-proxy leg at CUH. IP pinning is impossible where the customer proxy resolves DNS.

### 7. Open Points (Unverified)

1. Whether non-HTTP wire traffic (TDS, Postgres) passes cleanly through a CONNECT tunnel.
2. How Smokescreen handles IP-literal hosts, since its ACLs match hostnames.
3. Whether Smokescreen can chain to an upstream proxy, which CUH needs.
4. mysql2 calls `stream` synchronously, so it needs a wrapper socket that queues until the tunnel opens (research finding, not run).
5. MSSQL `host\instance` does a UDP lookup a TCP tunnel can't carry. Forbid instance-name hosts or resolve them differently.

### 8. Spike

Two days.

1. Run Smokescreen in report mode on `ff-test-a`.
2. Add a small CONNECT dialer for pg and axios.
3. Measure health-check latency and whether TDS and Postgres traffic pass cleanly.
4. Repeat on `hie-test-34`, the EoE test SDE, which carries the same firewall rule as prod.

Exit: points 1–3 in §7 answered and a decision recorded.

### 9. Effort

- Broker chart with certificates: small to medium.
- Application dialers across all connectors: medium to large (research estimate).
- Ongoing: a new component to patch and monitor at every customer node.

### 10. Related

[[LLM - Egress Broker]] · [[SoT - Network Security Architecture]] · [[SoT - Azure Hybrid Networking (ExpressRoute)]]