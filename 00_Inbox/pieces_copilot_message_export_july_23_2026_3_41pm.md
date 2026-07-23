---
title: pieces_copilot_message_export_july_23_2026_3_41pm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-23-2026-3-41pm
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Thursday Jul 23, 2026 - 3:41 PM*
---
## Validation of the FITFILE Stress Testing Report Draft

I cross-checked your draft against your Pieces memory (Grafana, Jira/GitLab, Teams chats, Confluence design docs) from the last ~4 months of FITFILE stress-testing work. Here's what's grounded, what needs adjustment, and what's still a gap.

### Infrastructure

**Confirmed:**
- **Regions split (ST1 UK South vs others UK West)** — partially corroborated: the Vault cluster backing the platform runs in `Azure (uksouth)` and a backup vault (`sbox-aks-backup-vault`, subscription "Testing") is located in **UK South**. Separately, a `kubectx` session against `aks-ffsts2-ukw-gp-1` shows sandbox-testing-2 using a **UK West** cluster naming convention (`ukw`), consistent with your ST2-5 claim.
- **Private K8s networking** — the AKS cluster `aks-ff-uks-gp-1` overview shows `Networking: Azure CNI Overlay, Private cluster enabled`, with Calico as the network policy engine.
- **NodePool for workflows exists** — an Azure AKS "workflows" node pool is visible in your portal history (`aks-ff-uks-gp-01`), consistent with the "Workflows NodePool" metric category in your draft, though I could not confirm the full 4-way split (`system, fitfile, omopdb, workflows`) as an explicit re-architected set in one place.
- **K8s version / VM sizes** — one cluster snapshot (`aks-ff-uks-gp-1`) shows `Kubernetes version: 1.33.2`, node sizes `Standard_E4as_v7` and `Standard_E4ads_v7`.

**Gaps / suggestions:**
- I could not find a tool-grounded confirmation of the exact **"5 FITFILE environments / 5 AKS clusters / 5 OMOP PostgreSQL databases"** count. Only `sandbox-testing-1` and `sandbox-testing-2` appear explicitly named in the [Database Metrics Grafana dashboard](https://fitfiletest.grafana.net/d/aklmtf/database-metrics-cpu-memory-storage?orgId=1&from=now-6h&to=now&timezone=browser&var-cluster=sandbox-testing-2). Suggest pulling the full ST1–ST5 cluster list from Azure Resource Manager or Terraform state before finalizing the diagram, since your memory only surfaces 2 of the 5 by name.
- The "database on a bigger box, pgconfig optimised for read" claim for ST1 is **not yet directly evidenced** in what I retrieved — worth attaching the actual Postgres `postgresql.conf` diff or VM SKU comparison as an appendix so the claim is auditable.

### Test Design — Test data

- **synthea_27m** and the OMOP synthetic data generation pipeline are well attested: Sprint 13 (8–15 Apr) tickets `FTFL-475` (script to generate OMOP synthetic data), `FTFL-479` (script to install OMOP data into target database), `FTFL-488` (synthetic OMOP data storage), and `FTFL-494` (de-duplication using entity resolution) — from the [FITFILE Sprint 13 Scrum Board](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281).
- **Achilles reports reference** — this item is legitimate and already under discussion, not just a placeholder: a Teams chat titled "Sprint Demo & Release Planning: OHDSI Integration" covers **Achilles reports integration into OHDSI Atlas** and a "Distributed Achilles Reports integration" design (Coordinating Node vs Data Provider Node push/pull options), and Sprint 21's board lists `FTFL-658 Investigate the Achilles Reports`. Good — this closes the "for later" note with a concrete ticket you can cite.
- **Cohort definitions** — I found fragmentary audio evidence of "Atlas cohort definitions" being iterated on ("we'll use supply the three Atlas cohort definitions...") and a Slack mention from Ollie Rushton about "re-running your cohort definition" post-migration, but I did **not** find a clean, readable JSON cohort definition file or a canonical list of cohort names/sizes. This is a genuine gap — the "Reference the JSON cohort definitions" and "List each of the cohort sizes and data extract volume" sections need source documents pulled directly from your repo/Atlas export, since memory only has garbled audio on this topic.
- **Patient expected overlap / missing tables in synthetic data** — no clear tool evidence surfaced for either. Flag these as unconfirmed; you'll need to source them from wherever the overlap analysis and missing-table audit actually live (likely a notebook or doc not indexed in LTM).

### Metrics

**Confirmed:** Grafana is your observability backbone — `fitfiletest.grafana.net`, subscribed to **Grafana Cloud Pro**, with dashboards specifically for:
- [Database Metrics (CPU / Memory / Storage)](https://fitfiletest.grafana.net/d/aklmtf/database-metrics-cpu-memory-storage?orgId=1&from=now-6h&to=now&timezone=browser&var-cluster=sandbox-testing-1) — covering minio, mongodb, postgresql, spicedb-postgresql, thehyve-postgresql pods per cluster, plus a **Slow Query Log** panel (`log_min_duration_statement` + `auto_explain`) on sandbox-testing-1.
- [Kubernetes Overview](https://fitfiletest.grafana.net/dashboards/f/dfs2pe0fy5ptse/stress-testing) — availability/stability/infrastructure panels (OOMKilled containers, evicted pods, node pressure, etc.).

**Gap:** I found no direct evidence of **"Total Query Time," "cost of total query," or "cost breakdown per data provider per query"** as existing dashboard panels. These may be aspirational/planned metrics rather than already-built ones — worth clarifying in the report whether these are *delivered* or *planned* observability additions, since your Observations section separately calls out "New dashboards for cost analysis of queries" as something new/recent, which suggests the cost dashboards are newer work not yet fully reflected in what I could retrieve.

### Fixes

- **OMOP Reindexer optimization — largely confirmed, but check the specific numbers.** A Teams chat with Oliver Rushton states: *"Claude is working on a plan to optimise the OMOP reindexer task - first starting with single threaded improvements... then adding multi threaded improvements (as this will require argo workflow changes). One of the fixes improved performance by >10x. Phases 1 and 2 are complete - a ~19x speedup (32.18s → 1.66s) on the benchmark."* Your draft says "~x20 faster" — the actual quoted figure is **~19x** (32.18s → 1.66s), not 20x. Recommend correcting to "~19x" or explicitly rounding with the source numbers shown.
- **Vectorized transforms confirmed at commit level** — GitLab MR `FTFL-999` ("Add regression and benchmark coverage for the OMOP reindexer before optimising it," merged by Ollie Rushton) shows commits: `Vectorise retype_numeric validation in the shared io_manager` and `Vectorise person_id equivalence matching instead of using iterrows` — directly supporting your "vectorized column transforms" and "optimised person_id remapping" bullets. I did not see a commit explicitly labeled "increasing chunk sizes," so that specific claim is unconfirmed — worth double-checking against the full MR diff at [gitlab.com/fitfile/data-and-analytics MR !613](https://gitlab.com/fitfile/ude-cli/-/merge_requests/new).
- **OOMKilled — confirmed, but not the "Finalize task."** Grafana's Kubernetes Overview dashboard repeatedly shows OOMKilled containers, but the containers named are **`reflector`** and **`minio`** (specifically `dev-minio`), not a "Finalize" task/pod. Your draft's "Finalize task OOMKilled" line isn't matched by what I found — either the Finalize-specific OOMKilled event isn't in memory, or the bullet should be corrected to reference the reflector/minio OOMKill events actually logged. Worth verifying which pod the "Finalize" fix actually targeted before publishing.
- **NodePool re-architecture / reduced pod sizing** — only partially evidenced (the "workflows" pool exists in Azure); I could not confirm the full system/fitfile/omopdb/workflows 4-pool split or the specific "reduced running size of cluster pods" change from memory. Recommend sourcing the Terraform/Helm diff for the NodePool config directly.

### Observations

- **Nginx Ingress burst traffic** — partially evidenced: `ingress-nginx-controller` (LoadBalancer) exists on your clusters, and GitLab MR `ftfl-573 adding enable service port 80` was merged into the `terraform-helm-fitfile-platform` module. However, I found no explicit discussion of burst-traffic replica scaling — this observation may be forward-looking rather than something already tested; consider phrasing it as a recommendation rather than a finding unless you have load-test evidence to attach.
- **Read-optimised DB config impact on query times** — no direct tool evidence found linking ST1's read-optimised config to measured query time deltas. This ties back to the Infrastructure gap above — you'll want the actual before/after query time comparison as supporting data.
- **New dashboards (workflow end-to-end, cost analysis)** — the Grafana Cloud Pro subscription and dashboard infrastructure are confirmed as existing, but I didn't find the specific new dashboards named. Likely genuine recent additions not yet reflected in indexed memory — fine to keep as a forward-looking observation.

### Results table

No workflow IDs, test names, or a results table were found in memory — this section will need to be populated fresh from wherever your test run outputs/Argo Workflow IDs are actually stored (Argo UI, Grafana Explore, or a spreadsheet), since none of my searches surfaced a structured results table.

---

### Summary of suggested edits before you finalize

1. Correct the reindexer speedup figure from "~x20" to **"~19x (32.18s → 1.66s)"** per Oliver Rushton's chat.
2. Verify whether "Finalize task OOMKilled" is the right fix description — memory shows OOMKilled events on **reflector** and **minio**, not a "Finalize" pod.
3. Source the missing cohort JSON definitions, patient overlap analysis, and missing-tables audit directly from your repo/Atlas exports — these weren't retrievable from LTM.
4. Confirm the full 5-cluster/5-database topology and the 4-way NodePool split from Terraform/Azure directly, since memory only surfaced 2 of 5 clusters and a partial NodePool picture.
5. Populate the Results table and the query-cost/total-query-time metrics from your actual test run outputs — these appear to be either not yet built or not indexed in memory.