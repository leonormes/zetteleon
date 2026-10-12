---
conformant: false
created: 2026-09-29T13:43:59+00:00
modified: 2026-09-29T13:45:03+00:00
non_conformance_reason: raw LLM paste awaiting triage
permalink: llmeon/00-inbox/llm-2026-09-29-1443
source: LLM conversation 2026-09-29
source_url: null
status: seed
tags: [source/llm]
title: LLM - 2026-09-29 1443
type: concept
---

I'll check what proxy plumbing the deployment repo already has, since that decides how much of a broker exists already.

An egress broker is a small proxy that becomes the only way out for the pods that make user-directed connections. It resolves the destination, checks it against policy, dials the IP it checked, and logs the decision. Stripe's [Smokescreen](https://github.com/stripe/smokescreen) is the reference implementation.

```
fitconnect / task pod ──CONNECT host:port──▶ broker ──▶ destination
(NetworkPolicy: DNS, platform deps, (resolve, classify, check policy,
and the broker only) pin IP, log allow/deny)
```

## What it Adds over the Cheaper Layers

- No bypass route. The connector pods have no direct path out, so a bug in a driver or a missed code path can't skip the check. That is the difference between "deny by default" and "allow except a list", which is the CISA wording we verified.
- One choke point. Every connector and pod goes through the same policy, including the implicit health checks and hourly syncs. It also gives one place for the accepted-and-rejected-flow logging OWASP recommends.
- Public egress can be default-deny too. The NetworkPolicy and guard layers can't do that without a per-node list.

## Where it Stops short

- The policy source matters more than the proxy. If the broker reads fitconnect's registry, a compromised fitconnect can register any destination and the broker will allow it.
    - Per-destination authorisation only adds security if approval is independent of the pod that could be compromised.
    - The realistic tiers are:
        - public destinations: allowed, with the private-range checks;
        - operator-declared private prefixes: allowed;
        - anything else: an operator change.
    - Declared prefixes don't go away; they move into the broker's config. Smokescreen blocks non-public IPs by default, per the research report.
    - I was too generous earlier to call this "per-destination authorisation" without that caveat.
- The broker is a high-value target. It holds the "can reach everything" position, which is the lesson of Capital One and CVE-2020-8555. It needs no credentials, no cloud identity and no token mount.
- It becomes a dependency for every query.
    - It needs at least two replicas and a disruption budget.
    - Keep it out of fitconnect's liveness probe, or an outage becomes a restart loop.

## Fit with Our Stack

- Drivers need an explicit dialer.
    - The drivers ignore `HTTP_PROXY`. The code research found injection points for pg (`stream`), mysql2 (`stream`), tedious (`connector`), axios (agent) and the S3 client (request handler).
    - mysql2 calls `stream` synchronously, so it needs a wrapper socket that queues until the tunnel opens (research finding; I haven't run it).
    - Those are the same five points the in-app guard needs. So building the guard first isn't wasted: the dialer later changes from "connect directly to the checked IP" to "connect through the broker". That is my inference.
- The existing proxy plumbing is the wrong vehicle.
    - The `proxy` block (`values.yaml:84-91`) only feeds Grafana (`charts/ffnode/templates/_grafana.tpl:121`).
    - The mutating webhook injects proxy env vars into every pod at creation and fails closed (`mutating-webhook.yaml:30`).
    - Env-based proxying would also clobber an injected agent, and CUH's `NO_PROXY` bypasses exactly the metadata address and cluster ranges. So the broker must be explicit in code and not switched on by environment.
- MSSQL `host\instance` does a UDP lookup a TCP tunnel can't carry. Either forbid instance-name hosts or resolve them differently.
- Customer proxies (CUH). A customer proxy resolves DNS itself, so IP pinning is impossible on that leg and the customer's proxy is the enforcement point there. I haven't confirmed whether Smokescreen can chain to an upstream proxy.

## Options

|Option|Notes|
|---|---|
|Smokescreen|Proven and small. Mutual-TLS identity per client, enforce and report modes (useful for rollout), per-client ACLs. Its ACL matches hostnames, so IP-literal hosts need handling. Your Zero Trust plan prefers proven technology over custom builds.|
|Istio or Envoy egress gateway|Heavy. TCP matching is by IP and port, one ServiceEntry per destination, and Istio's own docs say sidecar-only control isn't secure.|
|Squid|Works with CONNECT. IP-based ACLs are awkward and it is dated.|
|Custom SOCKS or CONNECT broker|Full control, such as per-data-source identity, but it is a custom security component.|
|Calico egress gateway|Not a filter. It fixes the source IP, so don't confuse it.|

## Size and next step

- Broker chart with certificates: small to medium.
- Application dialer across all connectors: medium to large (research estimate).
- Ongoing: a new component to patch and monitor at every customer node.

I'd run a two-day spike before committing. Run Smokescreen in report mode on ff-test-a, add a small CONNECT dialer for pg and axios, and measure health-check latency and whether TDS and Postgres wire traffic pass cleanly. That would settle the unverified points: non-HTTP driver traffic, IP-literal handling and upstream chaining.

I can't run anything in this side chat. The chart facts above come from the files I just read, and everything about Smokescreen comes from the earlier research reports, not from my own testing.
