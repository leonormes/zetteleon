---
title: "MS SQL deployment options in Azure"
source: "https://claude.ai/chat/a7c38192-a1c7-4311-8403-f3e0f9fc3b32"
captured: "2026-03-16T13:57:54+00:00 2026-03-16T13:57:54+00:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

We want to set up a test ms sql in azure. We have a k8s cluster. We could deploy it as a pod for ease. Or we could use an azure managed ms sql. What are the trade-offs. The customer has the azure managed version.

---

**Claude**

## MS SQL for Testing: K8s Pod vs Azure Managed SQL

## The Core Question

You're really asking: **how closely should your test environment mirror the customer's production environment?** That answer shapes everything.

---

## Trade-off Matrix

| Dimension | K8s Pod (SQL Server container) | Azure Managed SQL |
| --- | --- | --- |
| **Cost** | ✅ Near-zero (just compute) | ❌ ~£130–400+/month depending on tier |
| **Spin-up speed** | ✅ Minutes, declarative YAML | ⚠️ 5–10 mins via Terraform/portal |
| **Teardown** | ✅ `kubectl delete` | ⚠️ Must destroy Azure resource |
| **Parity with customer** | ❌ Low — different engine surface | ✅ High — same managed service |
| **Feature parity** | ❌ Missing managed-only features | ✅ Full feature set |
| **Persistence** | ⚠️ Needs PVC, fragile by default | ✅ Built-in, durable |
| **GitOps-friendly** | ✅ ArgoCD can own it | ⚠️ Terraform-managed, separate lifecycle |
| **Network complexity** | ✅ In-cluster, simple | ⚠️ Private endpoint / VNet peering needed |
| **Auth model** | ⚠️ SQL auth only, typically | ✅ AAD auth, same as customer |
| **Maintenance overhead** | ⚠️ You own patching, backups | ✅ Microsoft manages it |

---

## The Critical Risk with K8s Pod

> **SQL Server in a container is not the same engine as Azure SQL Managed Instance or Azure SQL Database.**

Specifically, the managed offerings run on a **different compatibility surface**:

- **Azure SQL Database** — cloud-native, missing some on-prem T-SQL features (e.g. cross-database queries, SQL Agent, certain CLR features)
- **Azure SQL Managed Instance** — near-full SQL Server compatibility, but still has managed-service constraints
- **SQL Server container** — full on-prem SQL Server engine, which is actually *more permissive* than the managed services

This means **a bug or incompatibility that exists in the customer's environment may not reproduce in your pod, and vice versa.** Your test environment would give you false confidence.

---

## When Each Makes Sense

### ✅ Use K8s Pod if…

- You're testing **your application's SQL connectivity/schema** in isolation
- You need something **ephemeral** — spin up per PR, destroy after test
- You're just validating **driver config, connection strings, Vault secret injection**, etc.
- Cost is a hard constraint right now

### ✅ Use Azure Managed SQL if…

- You're testing **customer-specific behaviour** or reproducing a customer bug
- You need to validate **AAD auth, private endpoint, or managed identity flows**
- You want a **persistent shared dev/test database** the team can use
- You're building Terraform that will eventually deploy to customer environments — test it on the real thing

---

## My Recommendation

**Two-tier approach:**

1. **K8s pod** — for CI/unit-level testing, schema migrations, connection string validation. Cheap, fast, ephemeral.
2. **A single shared Azure SQL instance** (Basic tier, ~£4/month for a test DB) — for integration testing against the real managed surface when you actually need parity.

Don't over-invest in either. The pod is fine for 80% of dev work. The managed instance earns its place when you're debugging something customer-specific.

---

## Immediate Next Action

Before anything else, answer this one question to narrow the decision:

> **What are you actually testing against the database?**
> 
> - Schema/migrations only → pod is fine
> - AAD authentication or managed identity → you need Azure Managed SQL
> - Reproducing a customer issue → you need Azure Managed SQL

Tell me which, and I'll give you the exact YAML for the pod **or** the Terraform snippet for the managed instance — whichever fits.
