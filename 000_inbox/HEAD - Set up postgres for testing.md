---
aliases: []
confidence:
created: 2025-12-08T14:16:00Z
epistemic:
last_reviewed:
modified: 2025-12-09T10:17:25Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status: processing
tags: [state/thinking]
title: HEAD - Set up postgres for testing
type: head
uid:
up: "[[00_Workbench]]"
updated:
---

> [!abstract] The Spark (Contextual Wrapper)
> Ticket: [FFAPP-4635](https://fitfile.atlassian.net/browse/FFAPP-4635) - End-to-end SDE Project Extract (write & test): A0025.
> We need to set up a database to test large datasets in our staging environment to ensure all features and data pipeline steps can work with expected volumes.
>
> **Core Goal:** Verify the SDE Manager can handle the specific "Live Data Volumes" from CUH, particularly the ~508 million measurement records.

> [!info] Data Volume Requirements (Live Data from CUH)
>
> | Table Name | No of records |
> | :--- | :--- |
> | **measurement** | **507,750,094** |
> | **drug_exposure** | **102,268,852** |
> | condition_occurrence | 24,626,962 |
> | visit_occurrence | 21,547,274 |
> | visit_detail | 8,359,106 |
> | concept | 4,802,681 |
> | observation | 2,091,481 |
> | procedure_occurrence | 1,673,318 |
> | person | 1,067,532 |
> | observation_period | 1,057,960 |

How do we manage large data seeds?

We can use the hyve to set up the database with the Schema and stuff.

## 🧠 My Current Model (The Blind Write)

We chose the in cluster model as it was a lot cheaper! The managed Postgres was expensive and we decided we didn't need it.

---

You can absolutely do this with a single PostgreSQL pod, as long as:

-	you're OK with no HA / failover (backup+restore is your only safety net), and
-	you give it enough RAM and decent disk.

Given your row counts, the main questions are: "How big will this be on disk?" and "How much RAM/CPU do I need for smooth-ish analytics with one query at a time?"

⸻

1. Single replica vs more
Given:
-	Only one query at a time
-	OMOP tables, mostly analytical reads
-	Running in k8s via Bitnami PostgreSQL 16 chart

A single primary (1 replica) is technically fine and common:

-	✔ Simpler (no replication, no patroni, etc.)
-	✔ Lower resource cost
-	✖ No automatic failover – if the pod dies or the node goes away, DB is down until k8s reschedules the pod.
-	✖ No read scale-out (you don't need it anyway with 1 query at a time).

If you care about uptime beyond "best-effort dev/stage / analysis box", consider later:

-	Add a replica or
-	Move to a managed service (RDS/Aurora/Cloud SQL) and just connect from the cluster.

But for what you described, 1 replica is fine.

⸻

2. Rough storage sizing
Total rows you gave: ~675 million.

The monster tables are:

-	measurement: ~508M
-	drug_exposure: ~102M
-	condition_occurrence: ~25M
-	visit_occurrence: ~21.5M
-	visit_detail: ~8.3M

Very rough ballpark for OMOP:

-	Data row size (without indexes) often ends up around 100–200 bytes per row depending on how many nullable columns and the actual data.
-	Indexes (primary keys + a few useful secondary indexes on concept_id/date/person_id/etc.) typically add another 1–2x of the table size.

So a broad estimate:

-	Raw data: ~100–150 GB
-	Indexes + bloat + freespace + future growth: can easily push this into the 200–300 GB range.

Recommendation:

-	Start with at least 500 GB of fast SSD storage (ideally provisioned/guaranteed IOPS).
-	If this is long-term / production-ish, I'd go straight to 1 TB so you're not fighting space in 6 months.

In Bitnami values:

```yaml
primary:
persistence:
enabled: true
size: 1000Gi # I'd start here if budget allows
storageClass: fast-ssd-sc # whatever maps to SSD / high-IOPS in your cluster
```

⸻

3. CPU & memory sizing

You don't need crazy CPU for 1 query at a time, but you do want enough RAM so:

-	Working sets and common indexes fit at least partially in memory
-	You're not constantly thrashing the disk cache

RAM

For ~200–300GB-sized dataset:

-	Minimum I'd consider: 16 GiB
-	Comfortable starting point: 32 GiB
-	If budget allows and queries are heavier analytics: 64 GiB is lovely

Given you're infra-savvy and OMOP queries can be gnarly, I'd suggest:

Requests: 16Gi

Limits: 32Gi

Then tune shared_buffers to ~25–30% of RAM available to Postgres (Bitnami allows overrides via postgresqlExtendedConf or postgresqlConfiguration).

CPU

Even with one query at a time, heavy joins/aggregations like OMOP often go parallel.

-	Minimum: 2 vCPU
-	Better starting point: 4 vCPU
-	If queries are big date-range scans or lots of aggregates, 8 vCPU is nice but not mandatory from day one.

I'd start with:

Requests: 2

Limits: 4

So in Bitnami values:

primary:

resources:

requests:

cpu: "2"

memory: "16Gi"

limits:

cpu: "4"

memory: "32Gi"

⸻

4. Postgres config knobs worth setting

You don't have to go crazy, but for this size:

-	max_connections: keep it low (you only expect one query anyway). Something like 50 is plenty.
-	shared_buffers: ~25–30% of RAM (e.g. 8–10GB if you give the pod ~32GB).
-	effective_cache_size: ~50–75% of RAM (helps planner choose index scans).
-	work_mem: be conservative but not tiny. E.g. 32–64MB per connection. Remember it's per sort/hash, per connection.

In Bitnami values:

```sh
postgresqlExtendedConf:
max_connections: "50"
shared_buffers: "8GB"
effective_cache_size: "24GB"
work_mem: "64MB"
```

(Tweak these based on the actual memory limit you end up with.)

⸻

5. Other practical considerations
6.	Disk performance > CPU
For a 500M-row measurement table, disk IOPS and throughput matter more than pure CPU once the dataset is bigger than RAM. Prefer:
-	SSD-backed PVs
-	If you're in cloud: provisioned IOPS type volumes
2.	Backups + PITR
With a single replica, your resilience is:
-	Regular base backups (e.g. nightly)
-	WAL archiving (for point-in-time recovery)
3.	Table/index design & partitioning
For OMOP scale, consider:
-	Partitioning big fact tables (measurement, drug_exposure) by date or person_id ranges if you're doing large time-bounded queries.
-	Creating indexes on the typical OMOP query columns: person_id, visit_occurrence_id, condition_concept_id, measurement_concept_id, drug_concept_id, observation_date/measurement_date, etc.
4.	Connection pooling
Even with one client, wrapping connections with pgBouncer often simplifies future scaling. But you can skip it initially.

⸻

6. TL;DR recommendation

If I had to pick concrete numbers for your k8s Bitnami Postgres 16 with that OMOP dataset and one-query-at-a-time usage:

-	Replicas: primary: 1 (no HA, just backups)
-	Storage PV: size: 1000Gi, SSD storage class
-	Resources (primary):
-	requests: cpu: "2", memory: "16Gi"
-	limits: cpu: "4", memory: "32Gi"
-	Config (rough starting point):
-	max_connections: 50
-	shared_buffers: 8GB
-	effective_cache_size: 24GB
-	work_mem: 64MB

Then:

-	Load some representative data
-	Run your heaviest real-world OMOP queries
-	Watch CPU, memory, disk IO, query times
-	Adjust up/down from there.

If you want, next step I can help you sketch a minimal values.yaml for the Bitnami chart and a simple smoke-test query set to validate the sizing.
