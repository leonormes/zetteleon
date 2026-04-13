---
created: 2026-04-13T08:56:13+00:00
modified: 2026-04-13T10:30:32+00:00
---
# Implementation Plan: Distributed OMOP Data Generation with Azure Batch

Based on your existing `omop-cli` architecture and the Azure Batch blueprint you've been developing (from your Gemini session around 9:48 AM today), here's the comprehensive implementation plan.

---

## 1. CLI Design: The `omop batch-worker` Sub-command

This command is the **Phase C** entry point, designed to be invoked by Azure Batch task definitions.

### Command Signature

```bash
omop batch-worker \
  --batch-index <INT>           # REQUIRED: Unique worker ID (1-N), determines ID offset
  --population <INT>            # REQUIRED: Number of patients to generate
  --vocab-blob-url <URL>        # REQUIRED: Azure Blob SAS URL for golden vocab archive
  --output-blob-url <URL>       # REQUIRED: Azure Blob SAS URL for uploading results
  --work-dir <PATH>             # OPTIONAL: Local scratch directory (default: /tmp/omop-batch)
  --seed <INT>                  # OPTIONAL: Synthea random seed (default: batch_index)
  --disease-module <NAME>       # OPTIONAL: Synthea disease module for sub-cohort enrichment
  --state <STATE_CODE>          # OPTIONAL: US state for Synthea demographics (default: Massachusetts)
  --skip-upload                 # OPTIONAL: Debug flag to skip blob upload
  --keep-intermediate           # OPTIONAL: Retain intermediate files for debugging
```

### Argument Specification Table

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--batch-index` | `int` | ✅ | — | Worker identifier; determines the `batch_index * 1,000,000,000` offset |
| `--population` | `int` | ✅ | — | Patients per worker (e.g., 100,000) |
| `--vocab-blob-url` | `str` | ✅ | — | SAS URL to `omop-vocab-golden.tar.gz` |
| `--output-blob-url` | `str` | ✅ | — | SAS URL prefix for output upload |
| `--work-dir` | `Path` | ❌ | `/tmp/omop-batch` | Ephemeral scratch space |
| `--seed` | `int` | ❌ | `batch_index` | Ensures reproducibility |
| `--disease-module` | `str` | ❌ | `None` | Optional enrichment (per your existing docs: "best-effort") |
| `--state` | `str` | ❌ | `Massachusetts` | Synthea demographic module |
| `--skip-upload` | `flag` | ❌ | `False` | Debug mode |
| `--keep-intermediate` | `flag` | ❌ | `False` | Retain work-dir contents |

---

## 2. Internal Logic: Step-by-Step Execution Flow

The `batch-worker` command orchestrates 7 discrete stages:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     omop batch-worker Execution Flow                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  │ 1. INIT      │────▶│ 2. DOWNLOAD  │────▶│ 3. SYNTHEA   │            │
│  │ Work Dir     │     │ Golden Vocab │     │ Generate     │            │
│  └──────────────┘     └──────────────┘     └──────────────┘            │
│                                                   │                     │
│                                                   ▼                     │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  │ 6. ARCHIVE   │◀────│ 5. EXPORT    │◀────│ 4. ETL       │            │
│  │ & Upload     │     │ + ID Remap   │     │ (R + MSSQL)  │            │
│  └──────────────┘     └──────────────┘     └──────────────┘            │
│         │                                                               │
│         ▼                                                               │
│  ┌──────────────┐                                                       │
│  │ 7. CLEANUP   │                                                       │
│  │ (optional)   │                                                       │
│  └──────────────┘                                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage Breakdown

#### Stage 1: Initialize Work Directory
```python
def _init_workdir(work_dir: Path, batch_index: int) -> BatchWorkspace:
    """Create isolated workspace with batch-specific subdirectories."""
    workspace = BatchWorkspace(
        root=work_dir / f"batch-{batch_index}",
        vocab_dir=work_dir / f"batch-{batch_index}" / "vocab",
        synthea_out=work_dir / f"batch-{batch_index}" / "synthea-output",
        cdm_export=work_dir / f"batch-{batch_index}" / "cdm-export",
    )
    workspace.root.mkdir(parents=True, exist_ok=True)
    return workspace
```

#### Stage 2: Download Golden Vocabulary
```python
def _download_vocab(vocab_blob_url: str, target_dir: Path) -> None:
    """Stream vocab archive from Azure Blob and extract."""
    # Use azure-storage-blob SDK or azcopy for large files
    # Extract to target_dir preserving CONCEPT.csv, CONCEPT_RELATIONSHIP.csv, etc.
```

#### Stage 3: Synthea Patient Generation
```python
def _run_synthea(population: int, seed: int, state: str, 
                 disease_module: Optional[str], output_dir: Path) -> Path:
    """Invoke Synthea JAR with controlled parameters."""
    # Reuse existing services/synthea.py logic
    # Key: pass --exporter.csv.export=true for FHIR→CSV output
    return output_dir / "csv"
```

#### Stage 4: R-based ETL to MSSQL
```python
def _run_etl(synthea_csv: Path, vocab_dir: Path) -> MssqlConnection:
    """
    Spin up ephemeral MSSQL container, run ETL, return connection handle.
    Reuses services/docker.py and services/etl.py patterns.
    """
    # 1. Start Docker MSSQL container (existing pattern)
    # 2. Load vocabulary into MSSQL
    # 3. Run R ETL script (ETL-Synthea)
    # 4. Return active connection for ID remapping
```

#### Stage 5: ID Remapping + CSV Export (See Section 3)

#### Stage 6: Archive and Upload
```python
def _archive_and_upload(cdm_dir: Path, batch_index: int, 
                        output_blob_url: str) -> str:
    """Create .tar.gz, upload to Blob Storage, return blob path."""
    archive_name = f"omop-batch-{batch_index:05d}.tar.gz"
    # tar + gzip the cdm_dir
    # Upload via azure-storage-blob SDK
    return f"{output_blob_url}/{archive_name}"
```

#### Stage 7: Cleanup
```python
def _cleanup(workspace: BatchWorkspace, keep_intermediate: bool) -> None:
    """Remove scratch files unless debugging."""
    if not keep_intermediate:
        shutil.rmtree(workspace.root)
```

---

## 3. ID Remapping Strategy

### Recommendation: **SQL-based remapping inside MSSQL before export**

This is the most robust approach for three reasons:

| Approach | Pros | Cons |
|----------|------|------|
| **SQL (Recommended)** | FK integrity enforced by DB engine; single atomic operation; all relationships updated consistently | Requires listing all ID columns upfront |
| Python Streaming | No SQL changes; works on any DB export | Must track all FK relationships manually; risk of inconsistency; higher memory for large tables |

### The OMOP CDM ID Columns to Remap

Based on OMOP CDM v5.4, these are the surrogate ID columns requiring offset:

```sql
-- Primary keys (source of truth)
person.person_id
observation_period.observation_period_id
visit_occurrence.visit_occurrence_id
visit_detail.visit_detail_id
condition_occurrence.condition_occurrence_id
drug_exposure.drug_exposure_id
procedure_occurrence.procedure_occurrence_id
device_exposure.device_exposure_id
measurement.measurement_id
observation.observation_id
note.note_id
note_nlp.note_nlp_id
specimen.specimen_id
location.location_id
care_site.care_site_id
provider.provider_id
payer_plan_period.payer_plan_period_id
cost.cost_id
drug_era.drug_era_id
dose_era.dose_era_id
condition_era.condition_era_id
episode.episode_id
episode_event.episode_event_id

-- Foreign keys (must match remapped PKs)
-- Example: condition_occurrence.person_id → person.person_id
-- All *_id columns referencing person, visit, provider, care_site, etc.
```

### Implementation: SQL Remapping Script

Create a stored procedure or Python-generated SQL batch that runs **after ETL completes** but **before CSV export**:

```sql
-- File: services/sql/apply_id_offset.sql
-- Parameter: @offset BIGINT = batch_index * 1000000000

DECLARE @offset BIGINT = %(offset)s;

-- 1. Update primary keys first (disabling FK checks)
ALTER TABLE person NOCHECK CONSTRAINT ALL;
ALTER TABLE visit_occurrence NOCHECK CONSTRAINT ALL;
-- ... repeat for all tables

-- 2. Apply offset to person.person_id and all FKs
UPDATE person SET person_id = person_id + @offset;
UPDATE observation_period SET 
    observation_period_id = observation_period_id + @offset,
    person_id = person_id + @offset;
UPDATE visit_occurrence SET 
    visit_occurrence_id = visit_occurrence_id + @offset,
    person_id = person_id + @offset;
UPDATE condition_occurrence SET 
    condition_occurrence_id = condition_occurrence_id + @offset,
    person_id = person_id + @offset,
    visit_occurrence_id = visit_occurrence_id + @offset;
-- ... continue for all clinical tables

-- 3. Re-enable constraints
ALTER TABLE person CHECK CONSTRAINT ALL;
ALTER TABLE visit_occurrence CHECK CONSTRAINT ALL;
-- ... repeat
```

### Integration Point in Codebase

Add the remapping step to `services/database.py`:

```python
# services/database.py

ID_OFFSET_MULTIPLIER = 1_000_000_000

def apply_batch_id_offset(conn: MssqlConnection, batch_index: int) -> None:
    """
    Apply deterministic ID offset to all OMOP surrogate keys.
    Must run AFTER ETL and BEFORE export.
    """
    offset = batch_index * ID_OFFSET_MULTIPLIER
    
    with open(Path(__file__).parent / "sql" / "apply_id_offset.sql") as f:
        sql_template = f.read()
    
    # Execute with pyodbc or your existing cursor pattern
    conn.execute(sql_template % {"offset": offset})
    conn.commit()
    
    logger.info(f"Applied ID offset {offset} for batch {batch_index}")
```

### Updated Execution Flow with Remapping

```python
# commands/batch_worker.py

def batch_worker(
    batch_index: int,
    population: int,
    vocab_blob_url: str,
    output_blob_url: str,
    work_dir: Path,
    **kwargs
) -> None:
    workspace = _init_workdir(work_dir, batch_index)
    
    # Stage 2
    _download_vocab(vocab_blob_url, workspace.vocab_dir)
    
    # Stage 3
    synthea_csv = _run_synthea(population, batch_index, kwargs.get("state"), 
                               kwargs.get("disease_module"), workspace.synthea_out)
    
    # Stage 4: ETL - keep connection open
    with DockerMssqlContainer() as mssql:
        _load_vocab_to_db(mssql, workspace.vocab_dir)
        _run_r_etl(mssql, synthea_csv)
        
        # Stage 5a: ID REMAPPING (NEW)
        apply_batch_id_offset(mssql.connection, batch_index)
        
        # Stage 5b: Export CSVs
        _export_cdm_tables(mssql.connection, workspace.cdm_export)
    
    # Stage 6
    blob_path = _archive_and_upload(workspace.cdm_export, batch_index, output_blob_url)
    
    # Stage 7
    _cleanup(workspace, kwargs.get("keep_intermediate", False))
    
    logger.info(f"Batch {batch_index} complete: {blob_path}")
```

---

## 4. File Structure Changes

```
services/omop_generator/
├── omop_cli/
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── etl_export.py          # Existing
│   │   └── batch_worker.py        # NEW: Phase C entry point
│   ├── services/
│   │   ├── database.py            # ADD: apply_batch_id_offset()
│   │   ├── docker.py              # Existing
│   │   ├── etl.py                 # Existing
│   │   ├── blob_storage.py        # NEW: Azure Blob upload/download
│   │   └── sql/
│   │       └── apply_id_offset.sql # NEW: ID remapping SQL
│   └── models/
│       └── batch_workspace.py     # NEW: Workspace dataclass
└── Docs/
    └── AZURE_BATCH_ARCHITECTURE.md # NEW: Document this design
```

---

## 5. Orchestration Scripts (Phase B & D)

For completeness, here's the interface the `batch-worker` expects from orchestration:

### Phase B: Fan-Out (Orchestration Script)

```python
# scripts/azure_batch_submit.py

def submit_batch_jobs(
    total_population: int,
    workers: int,
    vocab_blob_url: str,
    output_container_url: str,
    batch_account: str,
    pool_id: str,
) -> None:
    """Submit N tasks to Azure Batch."""
    population_per_worker = total_population // workers
    
    for batch_index in range(1, workers + 1):
        task_command = f"""
        omop batch-worker \
          --batch-index {batch_index} \
          --population {population_per_worker} \
          --vocab-blob-url "{vocab_blob_url}" \
          --output-blob-url "{output_container_url}"
        """
        # Submit via azure.batch SDK
```

### Phase D: Fan-In (Merge Script)

```python
# scripts/merge_batches.py

def merge_cdm_archives(blob_container_url: str, output_dir: Path) -> None:
    """Download all batch archives and concatenate CSVs."""
    # 1. List all omop-batch-*.tar.gz in container
    # 2. Download and extract each
    # 3. For each CDM table:
    #    - Write header once
    #    - Append rows from all batches (skip header on subsequent files)
    # 4. Package final merged dataset
```

---

## 6. Testing Strategy

| Test Type | Scope | Validates |
|-----------|-------|-----------|
| Unit | `apply_batch_id_offset()` | Correct SQL generation; offset math |
| Unit | `_archive_and_upload()` | Blob SDK integration (mock) |
| Integration | Small 2-batch run | IDs don't collide after merge |
| E2E | 10-batch Azure Batch | Full pipeline on real infra |

---

## Summary

1. **CLI Design**: `omop batch-worker` accepts `--batch-index`, `--population`, `--vocab-blob-url`, `--output-blob-url` as required args
2. **Internal Flow**: INIT → DOWNLOAD VOCAB → SYNTHEA → ETL → **ID REMAP (SQL)** → EXPORT → UPLOAD → CLEANUP
3. **ID Remapping**: Apply in SQL inside MSSQL **after ETL, before export** using `effective_id = original_id + (batch_index × 1,000,000,000)` — ensures FK integrity automatically

This aligns with your existing [FTFL-475](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/data-and-analytics/services/omop_generator/Docs/FTFL-475%20Script%20to%20generate%20OMOP%20synthetic%20data.md) requirements and the data-first architecture principles in your planning documents.