---
created: 2026-04-15T07:26:44+00:00
modified: 2026-04-15T07:26:58+00:00
title: Azure Batch Quota Explained
---

## Azure Batch Quota Explained

Based on your recent work on the OMOP data generation pipeline, you've encountered several quota limits. Let me explain how Azure quotas work and what you'll need for large-scale generation.

---

### How Azure Batch Quotas Work

Azure uses a layered quota system to control resource consumption. For Batch specifically, you're dealing with multiple independent limits:

| Quota Type | Your Current Limit | What It Controls |
|------------|-------------------|------------------|
| Pools per Batch account | 2 (was 0) | Max number of concurrent pools |
| Dedicated core quota | 10 vCPUs | Total vCPUs across all dedicated VMs |
| Spot/low-priority vCPUs | 0 | Total vCPUs for spot VMs |
| VM family quotas | 10 per family | vCPUs per VM series (Dv3, Ev3, etc.) |
| Batch accounts per region | 1-3 | How many Batch accounts in UK South |

---

### Why You're So Limited

From your quota check at [7:58 AM today](https://portal.azure.com/#@fitfile.com/resource/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/omop-synthetic-rg/providers/Microsoft.Batch/batchAccounts/omopbatch12345/accountQuotas), the `AccountQuota: 1` result confirms you're on default/starter quotas:

1. New Batch accounts start with near-zero quotas—This is Azure's anti-abuse policy to prevent accidental billing or resource squatting (as mentioned in the [Azure documentation](https://learn.microsoft.com/en-gb/azure/batch/batch-quota-limit) you referenced yesterday).
2. Non-Production subscription—Your `FITCloud Non-Production` subscription likely has lower default quotas than production subscriptions.
3. Regional constraints—UK South may have tighter limits than US regions due to capacity.

You saw this manifest as:

- `PoolQuotaReached` at 7:45 AM when pool count hit limit
- `AccountCoreQuotaReached` at 7:58 AM when trying to allocate D4 nodes (4 cores × 2 nodes = 8 cores, but you only have 10 total)

---

### Scaling to 12 Million Patients

For 12M patients with full OMOP records, you'll need substantial infrastructure. Here's a rough calculation:

#### Capacity Planning

| Parameter | Estimate |
|-----------|----------|
| Patients per worker | ~10,000 (based on current POPULATION=10 test) |
| Total workers needed | 1,200 concurrent workers (or fewer running longer) |
| vCPUs per worker (D4) | 4 vCPUs |
| Total vCPUs needed | ~4,800 vCPUs (or run in batches) |

#### Realistic Approach: Quota Increase + Wave Execution

Rather than 1,200 concurrent workers, run in waves:

| Strategy | Pool Size | vCPU Quota Needed | Waves to Complete |
|----------|-----------|-------------------|-------------------|
| Conservative | 20 × D4s_v3 | 80 vCPUs | 60 waves |
| Moderate | 50 × D4s_v3 | 200 vCPUs | 24 waves |
| Aggressive | 100 × D4s_v3 | 400 vCPUs | 12 waves |

---

### How to Request Quota Increases

You already submitted ticket `2604140050001941` yesterday at [10:34 AM](https://portal.azure.com/#view/Microsoft_Azure_Support/NewSupportRequestV4Blade) for the pool quota. For scale-up:

#### 1. Check Current Quotas

```bash
# Regional quotas
az batch location quotas show --location uksouth -o table

# Account-level quotas
az batch account show --name omopbatch12345 --resource-group omop-synthetic-rg \
  --query "{poolQuota:poolQuota, dedicatedCoreQuota:dedicatedCoreQuota, lowPriorityCoreQuota:lowPriorityCoreQuota}" \
  -o table
```

#### 2. Request Increases via Portal

Navigate to: [Azure Portal → Batch Account → Quotas → Request Increase](https://portal.azure.com/#@fitfile.com/resource/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/omop-synthetic-rg/providers/Microsoft.Batch/batchAccounts/omopbatch12345/accountQuotas)

Request these specific increases:

| Quota | Current | Request |
|-------|---------|---------|
| Dedicated vCPUs | 10 | 200-400 |
| Spot/low-priority vCPUs | 0 | 200 (optional, cheaper) |
| Pools per account | 2 | 5 |
| standardDv3Family cores | 10 | 200 |
| standardDSv3Family cores | 10 | 200 |

#### 3. Justification Text for Support Ticket

Include this in your quota request:

> We are running a synthetic healthcare data generation pipeline (OMOP CDM) for testing and compliance purposes. Our production workload requires generating 12 million patient records with associated clinical data. We need increased vCPU quotas to run distributed batch processing across multiple worker nodes. This is for the FITCloud Non-Production subscription used for development and testing infrastructure.

---

### Alternative: Use Spot/Low-Priority VMs (70-90% Cheaper)

If cost is a concern, Spot VMs are ideal for batch workloads that can handle interruption:

```bash
# Create pool with low-priority nodes instead
cat > /tmp/pool-spot.json <<'EOF'
{
  "id": "omop-pool-spot",
  "vmSize": "Standard_D4s_v3",
  "targetDedicatedNodes": 0,
  "targetLowPriorityNodes": 20,
  "taskSlotsPerNode": 2,
  "virtualMachineConfiguration": {
    "imageReference": {
      "publisher": "microsoft-azure-batch",
      "offer": "ubuntu-server-container",
      "sku": "20-04-lts"
    },
    "containerConfiguration": { "type": "dockerCompatible" },
    "nodeAgentSKUId": "batch.node.ubuntu 20.04"
  }
}
EOF
```

Note: You'll need to request `lowPriorityCoreQuota` increase first (currently 0).

---

### Summary

| Issue | Root Cause | Fix |
|-------|------------|-----|
| `PoolQuotaReached` | Pool limit was 0, now 2 | ✅ Already fixed via support ticket |
| `AccountCoreQuotaReached` | Only 10 dedicated vCPUs | Request 200-400 vCPU quota |
| Can't scale to 12M patients | Starter quotas too small | Submit quota increase request with business justification |

Immediate next step: Submit a quota increase request for 200+ dedicated vCPUs and 200+ Spot vCPUs via the Azure Portal. Small increases (up to ~100 cores) are often auto-approved within hours; larger requests may take 1-3 business days with manual review.
