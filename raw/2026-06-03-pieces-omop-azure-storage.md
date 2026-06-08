---
title: OMOP Parquet Data — Azure Storage Resource Names
created: 2026-06-04T08:03:29+00:00
source: pieces-ltm
pieces_ids: ["2abdd8ab-22ec-47c6-9a8b-617482a3ba1a", "82335225-9f79-41e1-bc97-f9109d04c22a", "54216833-0345-4373-a268-a0cae377cb01"]
tags: [raw, pieces]
---

## Asset 1 (Pieces: 2abdd8ab-22ec-47c6-9a8b-617482a3ba1a)
**Captured:** 2026-06-03T12:42:24.278448Z

All pagination chains are now `sufficient`. Here's what your memory clearly confirms:

---

## Resource group and storage names for the OMOP parquet data

### Resource group

**`omop-synthetic-rg`**

This was explicitly created by you on 14 Apr 2026 with:
```bash
az group create --name omop-synthetic-rg --location uksouth
```
Subscription: **FITCloud Non-Production** (`249df46b-f75d-4492-8e78-b33a00473548`), UK South.

### Storage account

**`omopstorage12345`**

Created on 14 Apr 2026 (`Created: 4/14/2026, 8:52:19 AM`), also in `omop-synthetic-rg`, UK South. StorageV2 (general purpose v2), Standard LRS.

The blob containers inside it were:

| Container | Purpose |
|---|---|
| `omop-synthetic-data` | Parquet output files (114 parquet files, ~61.5 GB across 5 nodes) |
| `omop-reference-data` | Golden OMOP vocabulary archive (`omop-vocab-golden.tar.gz`) |
| `omop-code-packages` | Source tarball (`omop_generator-src.tar.gz`) |

The parquet data itself lived at `omop-synthetic-data/omop_generator/synthea23m_parquet/` and the AzCopy upload command you ran uploaded with `--include-pattern "*.parquet"` to `https://omopstorage12345.blob.core.windows.net/omop-synthetic-data`.

For reference, the other OMOP resources in the same `omop-synthetic-rg` were `omopbatch12345` (Azure Batch account) and `omopacr0414172753` (Azure Container Registry).

## Asset 2 (Pieces: 82335225-9f79-41e1-bc97-f9109d04c22a)
**Captured:** 2026-06-03T12:38:45.035679Z

The user is asking about specific resource group and storage names they used for "parquet OMOP data". This is a RECALL scenario. Let me search their memory for this information.

## Asset 3 (Pieces: 54216833-0345-4373-a268-a0cae377cb01)
**Captured:** 2026-06-03T12:38:36.928382Z

what was the resource group and storage names i used for the parque omop data
