---
author: Claude (investigation with read-only cluster probes)
conformant: false
created: 2026-09-29T11:28:21+01:00
date: 2026-09-29
modified: 2026-09-29T10:30:50+00:00
non_conformance_reason: "agent-drafted work note awaiting Leon's review and edit"
permalink: llmeon/work/ftfl-590-problem-definition-unrestricted-data-source-connections
related_ticket: FTFL-590
status: draft
tags: [app-05, data-sources, fitfile, ftfl-585, ftfl-590, pentest, problem-definition, security, source/llm, ssrf]
title: FTFL-590 Problem Definition — Unrestricted Data Source Connections
type: concept
---

%% Draft written by Claude for Leon to review and edit. Not own words, so no own_words property on purpose. Each gap is tagged Verified or Inferred. Check the Unverified list before this goes on the ticket or Confluence. %%

## FTFL-590 (APP-05)—Problem Definition

Draft, 2026-09-29. Ticket: [FTFL-590](https://fitfile.atlassian.net/browse/FTFL-590), epic [FTFL-585](https://fitfile.atlassian.net/browse/FTFL-585). Source: ProCheckUp report FiL090226JH v1.0, finding APP-05 (page 20). This note defines the problem only. It proposes no solution.

---

### Problem

Users can add data sources by giving the platform a host and port, and the platform then connects to that destination from inside the cluster. This is deliberate: self-service is a core product feature.

The defect is that nothing enforces the boundary between destinations the user is entitled to reach (their own databases and services) and destinations that belong to the platform (cloud metadata, cluster control plane, internal databases, other tenants). The connecting process sits inside the platform's network, so any destination a user types inherits the platform's reach.

ProCheckUp reported this as APP-05 (Medium, CVSS 4.3). It was reproduced on 2026-09-28 on both non-production clusters (TCP connect only, no data retrieved).

---

### Gaps

Each is marked verified or inferred.

1. No destination control in the application.
   - _Verified:_ fitconnect accepts the host and port as entered. I found no validation of where they resolve to.
   - _Inferred, untested:_ the Elasticsearch client may follow redirects, which would bypass any check made only on the entered host.
2. No network restriction on the connecting workloads.
   - _Verified:_ no network policy selects the fitconnect pods or the query task pods, which use the same image. They can reach anything the node can.
3. No separation between user-directed and platform connections.
   - _Verified:_ the same process holds the platform's credentials and opens user-directed connections. A rule that lets the platform reach its own services also lets a user's data source reach them.
4. No control at the layer above.
   - _Verified:_ security groups and NSGs do not filter cloud metadata traffic (AWS documents this; Azure's WireServer is exempt from NSGs). They also cannot tell pods apart.
   - _Verified:_ the AWS cluster security group allows all egress, and the test clusters have no egress firewall. Defence in depth was assumed at that layer, not present.
5. Connection errors leak network information.
   - _Verified:_ raw driver errors go back to the user, so they can tell which hosts and ports answer. The pentest response shows this.
6. Weak defaults on the HTTP connectors.
   - _Verified:_ the S3 connector uses plain HTTP unless SSL is required, and Elasticsearch certificate verification is off by default.
7. No agreed network boundary per node.
   - _Verified:_ the deployment repo records no cluster CIDRs, and customer clusters are private and vary in topology. Nobody has defined which networks a node is meant to reach.
8. The pentest advice conflicts with the product.
   - ProCheckUp's host allowlist would end self-service, which is why the ticket was blocked from 27 April to 10 August.
   - The accreditation question raised in April is still unanswered, and no residual risk has been accepted or documented.

---

### Consequences

- Internal network mapping. _Verified:_ any user who can add data sources can probe internal hosts and ports and read the errors. Which roles can do this is unconfirmed; the report does not say which test account was used.
- Reach into platform internals. _Verified_ at network level: cloud metadata, the Kubernetes API, the kubelet, and databases in other namespaces. On staging, three nodes share one cluster, so this crosses tenants. On AWS the metadata hop limit is 2, so pods can reach it.
- Actual data or credential exposure is unproven. Using those services needs credentials or headers these connectors cannot easily send (general knowledge, untested). The realistic near-term abuse is reconnaissance and reaching unauthenticated internal HTTP services, which fits the Medium rating. It would rise if the redirect bypass is confirmed.
- Customer and regulatory exposure. The platform serves customers holding identifiable and pseudonymised health data, on private networks. A foothold there reachable from a user-facing feature is a material point for their information-governance reviews and for our own accreditations.
- Delivery. The ticket is the last open item in the pentest epic, so the pentest cannot be closed cleanly and there is no retest evidence. Until a risk-acceptance decision or a fix exists, it stays an open finding in customer security reviews.
- Risk in the remedy. Restricting connections crudely would break legitimate private data sources (VPN, privatelink, in-cluster OMOP databases), and a missed dependency would restart-loop the connector.

---

### Constraints

- Self-service must be preserved.
- Customer clusters are private, cannot be tested from here, and vary in topology.
- Security groups cannot express deny rules.

---

### Unverified

- Customer cluster networking.
- Redirect behaviour of the Elasticsearch client.
- Whether metadata credentials can be obtained through these clients.
- Which roles can create data sources.
- What the retest will accept.

---

### Evidence and Sources

Cluster probe, 2026-09-28 (TCP connect from inside the fitconnect pods; connect and close, no bytes sent):

| Target | Staging (ff-test-a) | Testing |
|---|---|---|
| 169.254.169.254:80 (cloud metadata) | open | open |
| Kubernetes API (ClusterIP and public endpoint) | open | open |
| Kubelet:10250 on a node | open | open |
| Postgres in another namespace | open | open |
| 168.63.129.16:80 (Azure WireServer) | timed out | timed out |
| Own Postgres, Mongo, MinIO, workflows-api, DNS | open | open |

The WireServer timeout has no identified cause. NSGs do not apply to that address, so it is something at node level.

Clusters (AKS, `az aks show`): Azure CNI with Calico network policy enforced, `outboundType: loadBalancer`, both in the FITCloud Non-Production subscription.

Code (`Application/InsightFILE/apps/fitconnect`):

- `src/services/dataSources/UseCases/CreateDataSourceConnectionUseCase.ts:51` returns the raw driver error to the caller.
- `src/infra/elasticsearch/client.ts:86-90` sets no redirect limit.
- `src/infra/adapters/S3DatasetRepo.ts:40-44` defaults to `http`.
- `src/config/default.ts:88` sets `sslVerify: false`.

Deployment repo:

- Task pods use the fitconnect-service image: `workflows/src/charts/tasks/templates/load-data-task-template.yaml:56` and `run-sql-task-template.yaml:62`.
- fitconnect liveness probe checks SpiceDB, Mongo, Postgres, MinIO and workflows-api: `charts/components/fitconnect/values.yaml:154`.

AWS module (`terraform-aws-private-infrastructure`):

- `Docs/NETWORKING.md:142`: security groups cannot restrict per pod, and the cluster security group's default egress is not managed.
- `modules/eks/main.tf:462-465`: IMDSv2 required, hop limit 2.

External documentation:

- [AWS: security groups do not filter instance metadata traffic](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [Microsoft: WireServer traffic is not subject to NSGs](https://learn.microsoft.com/en-us/azure/virtual-network/what-is-ip-address-168-63-129-16)

Ticket history:

- Blocked 27 April to 10 August.
- 27 April comment (Robin Mofakham): allowlisting is not feasible, and the accreditation impact of leaving a low-risk item open was raised.
- 10 August comment (Robin Mofakham): the team agreed internally to deny internal services rather than allowlist.
- Sprint 37, assigned to Leon Ormes, In Progress from 2026-09-28.
