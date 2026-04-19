---
created: 2026-04-16T14:48:52+00:00
modified: 2026-04-19T18:30:38+00:00
tags: [2604140050001941]
title: pieces_copilot_message_export_april_16_2026_3_48pm
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Thursday Apr 16, 2026 - 3:48 PM_
---

## Node Limits Analysis: swpc_synthea vs. Azure Infrastructure

Based on your recent troubleshooting and the meeting discussions, the blocker isn't swpc_synthea itself—it's your Azure Batch account quotas.

---

### What You're Actually Hitting

#### Azure Batch Quotas (The Real Blocker)

From your debugging session on April 15 at 7:58 AM:

| Quota Type | Your Current Limit | What You Need for 12M |
|------------|-------------------|----------------------|
| Pools per account | 2 (was 0 before support ticket) | 5+ |
| Dedicated vCPUs | 10 cores | 200-400+ cores |
| Pool allocation errors | PoolQuotaReached, AccountCoreQuotaReached | N/A |

You documented in your [Azure Batch Quota Explained note](file:///Users/Leon.ormes/.config/obsidian/vaults/LLMeon/Azure%20Batch%20Quota%20Explained.md) that even with D4 nodes (4 cores each), you're maxing out at 2-3 concurrent workers before hitting the vCPU ceiling.

---

### swpc_synthea Itself: No Hard Node Limits

The [swpc_synthea repository](https://github.com/nhsengland/swpc_synthea) you reviewed on April 15 at 5:04 PM shows:

- ✅ Accepts variable population sizes via `./run_synthea -p populationSize`
- ✅ Java-based generator with configurable cohort sizes
- ✅ No documented internal node/scale limits
- ✅ UK-adapted with NICE guidelines, dm+d codes, SNOMED CT

The tool can generate 12M patients—it just needs sufficient compute resources to do so.

---

### Your Capacity Planning (from Miro, 10:06 AM today)

From your infrastructure planning session:

Realistic Scale Approach:

- Moderate wave execution: 50 x D4s_v3 nodes = 200 vCPUs → 24 waves to complete 12M patients
- Aggressive execution: 100 x D4s_v3 nodes = 400 vCPUs → 12 waves

Current Reality:

- 10 vCPUs = you can barely run 2 parallel workers
- At this rate, you'd need 600+ sequential waves—completely impractical

---

### The Meeting Consensus (2:00-3:00 PM Today)

From your NHS Synthetic Data & OMOP Pipeline meeting, the team discussed:

- Storage target: ~60 TiB for 12M patients
- Compute reality: "A single server would take ~12 days; distributed Spark or AWS EC2 clusters are mandatory"
- Quality vs. scale trade-off: You advocated strongly for realistic data quality (not "crappy data"), which means using swpc_synthea's full clinical logic

Your position at 2:42-2:52 PM: Use swpc_synthea for authentic OMOP data, but scale it properly via distributed infrastructure.

---

### Next Steps (You've Already Started)

1. ✅ Support Ticket Filed (Ticket 2604140050001941, April 14 at 10:34 AM)
   - Pool quota raised from 0 → 2
   
2. 🔄 Quota Increase Request Needed:
   - Request 200-400 dedicated vCPUs via Azure Portal
   - Justification text is ready in your [quota documentation](file:///Users/Leon.ormes/.config/obsidian/vaults/LLMeon/Azure%20Batch%20Quota%20Explained.md)
   
3. 📧 Expert Guidance Pending:
   - Your email to Julia Kurps at The Hyve (sent April 16 at 2:09 PM)
   - She confirmed forwarding to their team for advice on large-scale OMOP generation

---

### Bottom Line

No, swpc_synthea doesn't have internal node limits blocking your 12M target. The constraint is purely infrastructure—Azure Batch quotas are choking you at 10 vCPUs. Once you get approval for 200-400 vCPUs (or use Spot VMs for 70-90% cost savings), swpc_synthea will happily generate the data in distributed waves.

The tool is fine. Your Azure subscription needs upgrading.
