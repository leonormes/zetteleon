---
created: 2026-04-15T07:05:09+00:00
modified: 2026-04-19T18:30:38+00:00
title: Azure Batch OMOP Worker - Clean-State Runbook
---

## 1. Complete Cleanup & Setup Flow

### Step 1: Login and Clean Existing Resources

```bash
# Set context
cd /Volumes/DAL/Fitfile/gitlab/FITFILE/Application/data-and-analytics/services
export SUBSCRIPTION="FITCloud Non-Production"
export BATCH_ACCOUNT="omopbatch12345"
export RESOURCE_GROUP="omop-synthetic-rg"

# Login
az account set --subscription "$SUBSCRIPTION"
az batch account login --name "$BATCH_ACCOUNT" --resource-group "$RESOURCE_GROUP"

# Delete all jobs
for JOB in $(az batch job list --query "[].id" -o tsv); do
  echo "Deleting job: $JOB"
  az batch job delete --job-id "$JOB" --yes
done

# Delete all pools
for POOL in $(az batch pool list --query "[].id" -o tsv); do
  echo "Deleting pool: $POOL"
  az batch pool delete --pool-id "$POOL" --yes
done

# Clean local logs
rm -f ./*worker-*-stdout.txt ./*worker-*-stderr.txt
```

---

## 2. Quota-Safe Strategy

Check current quota:

```bash
az batch location quotas show --location uksouth -o table
```

Recommended approach (choose based on quota):

### Option A: Single D4 Node with 2 Task Slots (RECOMMENDED)

- VM Size: Standard_D4s_v3 (4 cores, 16GB RAM)
- Nodes: 1 dedicated node
- Task slots per node: 2
- Total capacity: 2 concurrent workers
- Core usage: 4 cores (fits most quotas)

### Option B: Two D2 Nodes (fallback if D4 unavailable)

- VM Size: Standard_D2s_v3 (2 cores, 8GB RAM)
- Nodes: 2 dedicated nodes
- Task slots per node: 1
- Total capacity: 2 concurrent workers
- Core usage: 4 cores
- Risk: May hit OOM on vocab load (observed before on D2)

### Option C: Single D2 Node Sequential (minimal quota)

- VM Size: Standard_D2s_v3
- Nodes: 1
- Task slots: 1
- Run workers sequentially (not concurrent)

---

## 3. Create Pool (Option A - Single D4 with 2 slots)

```bash
# Create pool JSON
cat > /tmp/pool-omop-final.json <<'EOF'
{
  "id": "omop-pool-final",
  "vmSize": "Standard_D4s_v3",
  "targetDedicatedNodes": 1,
  "targetLowPriorityNodes": 0,
  "taskSlotsPerNode": 2,
  "taskSchedulingPolicy": {
    "nodeFillType": "Pack"
  },
  "virtualMachineConfiguration": {
    "imageReference": {
      "publisher": "microsoft-azure-batch",
      "offer": "ubuntu-server-container",
      "sku": "20-04-lts",
      "version": "latest"
    },
    "containerConfiguration": {
      "type": "dockerCompatible"
    },
    "nodeAgentSkuId": "batch.node.ubuntu 20.04"
  }
}
EOF

# Create pool
az batch pool create --json-file /tmp/pool-omop-final.json

# Wait for pool to be ready
echo "Waiting for pool allocation (this may take 3-5 minutes)..."
while true; do
  STATE=$(az batch pool show --pool-id omop-pool-final --query "allocationState" -o tsv)
  NODES=$(az batch pool show --pool-id omop-pool-final --query "currentDedicatedNodes" -o tsv)
  echo "Pool state: $STATE, Nodes: $NODES"
  
  if [ "$STATE" = "steady" ] && [ "$NODES" -ge 1 ]; then
    echo "Pool ready!"
    break
  fi
  
  # Check for errors
  RESIZE_ERRORS=$(az batch pool show --pool-id omop-pool-final --query "resizeErrors" -o json)
  if [ "$RESIZE_ERRORS" != "[]" ] && [ "$RESIZE_ERRORS" != "null" ]; then
    echo "Pool allocation failed:"
    echo "$RESIZE_ERRORS"
    exit 1
  fi
  
  sleep 15
done

# Verify nodes are idle and ready
az batch node list --pool-id omop-pool-final --query "[].{id:id,state:state}" -o table
```

---

## 4. Task JSON Templates

### task-worker-0.json (minimal Correct schema)

```json
{
  "id": "worker-0",
  "commandLine": "/bin/bash -c 'cd /mnt/batch/tasks/workitems && curl -L \"$CODE_SAS_URL\" -o code.tar.gz && tar -xzf code.tar.gz && cd data-and-analytics/services/omop_generator && ./scripts/azure_batch/launch_worker.sh'",
  "environmentSettings": [
    {
      "name": "BATCH_INDEX",
      "value": "0"
    },
    {
      "name": "CODE_SAS_URL",
      "value": "<YOUR_CODE_TARBALL_SAS_URL>"
    },
    {
      "name": "VOCAB_BLOB_URL",
      "value": "<YOUR_VOCAB_SAS_URL>"
    },
    {
      "name": "OUTPUT_BLOB_URL",
      "value": "<YOUR_OUTPUT_SAS_URL>"
    },
    {
      "name": "POPULATION",
      "value": "10"
    },
    {
      "name": "OMOP_VOCAB_CHUNK_ROWS",
      "value": "50000"
    }
  ],
  "containerSettings": {
    "imageName": "fitfileregistry.azurecr.io/omop/worker-prebaked:20260414-162811",
    "containerRunOptions": "--privileged -v /var/run/docker.sock:/var/run/docker.sock"
  }
}
```

### task-worker-1.json

```json
{
  "id": "worker-1",
  "commandLine": "/bin/bash -c 'cd /mnt/batch/tasks/workitems && curl -L \"$CODE_SAS_URL\" -o code.tar.gz && tar -xzf code.tar.gz && cd data-and-analytics/services/omop_generator && ./scripts/azure_batch/launch_worker.sh'",
  "environmentSettings": [
    {
      "name": "BATCH_INDEX",
      "value": "1"
    },
    {
      "name": "CODE_SAS_URL",
      "value": "<YOUR_CODE_TARBALL_SAS_URL>"
    },
    {
      "name": "VOCAB_BLOB_URL",
      "value": "<YOUR_VOCAB_SAS_URL>"
    },
    {
      "name": "OUTPUT_BLOB_URL",
      "value": "<YOUR_OUTPUT_SAS_URL>"
    },
    {
      "name": "POPULATION",
      "value": "10"
    },
    {
      "name": "OMOP_VOCAB_CHUNK_ROWS",
      "value": "50000"
    }
  ],
  "containerSettings": {
    "imageName": "fitfileregistry.azurecr.io/omop/worker-prebaked:20260414-162811",
    "containerRunOptions": "--privileged -v /var/run/docker.sock:/var/run/docker.sock"
  }
}
```

Update your actual task files:

```bash
# Make sure your task JSON files in services/ have the correct schema above
# No 'userName' or 'password' fields - pool uses managed identity for ACR pull
```

---

## 5. Submit Job and Tasks

```bash
# Create job
JOB_ID="omop-run-$(date +%Y%m%d-%H%M%S)"
az batch job create --id "$JOB_ID" --pool-id omop-pool-final

# Submit tasks
az batch task create --job-id "$JOB_ID" --json-file ./task-worker-0.json
az batch task create --job-id "$JOB_ID" --json-file ./task-worker-1.json

echo "Job ID: $JOB_ID"
echo "Tasks submitted."
```

---

## 6. Monitor Tasks (macOS-friendly)

```bash
# Live monitor loop
while true; do
  clear
  date
  echo "Job: $JOB_ID"
  echo "---"
  az batch task list --job-id "$JOB_ID" \
    --query "[].{id:id, state:state, node:nodeInfo.nodeId, exitCode:executionInfo.exitCode, result:executionInfo.result}" \
    -o table
  
  # Check if all tasks completed
  ACTIVE=$(az batch task list --job-id "$JOB_ID" --query "[?state=='active' || state=='running'].id" -o tsv | wc -l)
  if [ "$ACTIVE" -eq 0 ]; then
    echo ""
    echo "All tasks finished. Downloading logs..."
    break
  fi
  
  sleep 15
done
```

---

## 7. Download Logs

```bash
# Download stdout/stderr for both workers
for TASK in worker-0 worker-1; do
  echo "Downloading logs for $TASK..."
  az batch task file download \
    --job-id "$JOB_ID" \
    --task-id "$TASK" \
    --file-path stdout.txt \
    --destination ./${TASK}-stdout.txt 2>/dev/null || echo "No stdout for $TASK"
  
  az batch task file download \
    --job-id "$JOB_ID" \
    --task-id "$TASK" \
    --file-path stderr.txt \
    --destination ./${TASK}-stderr.txt 2>/dev/null || echo "No stderr for $TASK"
done

# Quick review
echo "=== worker-0 stderr tail ==="
tail -50 ./worker-0-stderr.txt

echo "=== worker-1 stderr tail ==="
tail -50 ./worker-1-stderr.txt
```

---

## 8. Diagnose Common Failures

```bash
# Check task failure reasons
az batch task list --job-id "$JOB_ID" \
  --query "[?executionInfo.result=='failure'].{id:id, exitCode:executionInfo.exitCode, failureInfo:executionInfo.failureInfo}" \
  -o json

# Check node states
az batch node list --pool-id omop-pool-final \
  --query "[].{id:id, state:state, recentTasks:recentTasks[0].taskId, errors:errors}" \
  -o json

# If tasks never started (active + no node assignment):
az batch task list --job-id "$JOB_ID" \
  --query "[?state=='active' && nodeInfo.nodeId==null].{id:id, state:state}" \
  -o table
# This usually means: pool quota issue, or pool not container-capable
```

---

## 9. Prevention Checklist

Before each run, verify:

- [ ] Pool is container-capable

  ```bash
  az batch pool show --pool-id omop-pool-final \
    --query "virtualMachineConfiguration.containerConfiguration.type" -o tsv
  # Must output: dockerCompatible
  ```

- [ ] ACR pull identity configured

  ```bash
  # Verify Batch managed identity
  az batch account show --name "$BATCH_ACCOUNT" --resource-group "$RESOURCE_GROUP" \
    --query "identity.principalId" -o tsv
  # Should output: 9bac3d8e-691c-4200-9a86-880864bb2840
  
  # Verify AcrPull role assignment
  az role assignment list --assignee 9bac3d8e-691c-4200-9a86-880864bb2840 \
    --query "[?roleDefinitionName=='AcrPull'].{scope:scope}" -o table
  # Should show fitfileregistry scope
  ```

- [ ] Docker socket mounted in task JSON

  ```bash
  # Verify containerRunOptions includes socket mount
  grep "containerRunOptions" task-worker-0.json
  # Must contain: --privileged -v /var/run/docker.sock:/var/run/docker.sock
  ```

- [ ] No disk pressure on pool

  ```bash
  az batch node list --pool-id omop-pool-final \
    --query "[].{id:id, state:state, errors:errors}" -o json
  # Check for DiskFull errors
  ```

- [ ] Quota headroom available

  ```bash
  az batch location quotas show --location uksouth \
    --query "{dedicatedCoreQuota:dedicatedCoreQuota, poolQuota:poolQuota, activeJobAndScheduleQuota:activeJobAndScheduleQuota}" -o table
  ```

---

## 10. Quick Reference Commands

```bash
# Set these once per session
export SUBSCRIPTION="FITCloud Non-Production"
export BATCH_ACCOUNT="omopbatch12345"
export RESOURCE_GROUP="omop-synthetic-rg"

# Login shortcut
alias batch-login='az account set --subscription "$SUBSCRIPTION" && az batch account login --name "$BATCH_ACCOUNT" --resource-group "$RESOURCE_GROUP"'

# Pool status
alias pool-status='az batch pool show --pool-id omop-pool-final --query "{id:id,state:allocationState,nodes:currentDedicatedNodes,nodeState:allocationStateTransitionTime}" -o table'

# Node health
alias node-health='az batch node list --pool-id omop-pool-final --query "[].{id:id,state:state,slots:runningTasksCount}" -o table'

# Task status
alias task-status='az batch task list --job-id "$JOB_ID" --query "[].{id:id,state:state,exit:executionInfo.exitCode}" -o table'
```

---

## 11. If D4 Quota Fails - Fallback to Sequential Run

```bash
# Create single D2 pool (1 node, 1 task slot)
cat > /tmp/pool-omop-d2-sequential.json <<'EOF'
{
  "id": "omop-pool-d2-seq",
  "vmSize": "Standard_D2s_v3",
  "targetDedicatedNodes": 1,
  "taskSlotsPerNode": 1,
  "virtualMachineConfiguration": {
    "imageReference": {
      "publisher": "microsoft-azure-batch",
      "offer": "ubuntu-server-container",
      "sku": "20-04-lts",
      "version": "latest"
    },
    "containerConfiguration": {
      "type": "dockerCompatible"
    },
    "nodeAgentSkuId": "batch.node.ubuntu 20.04"
  }
}
EOF

az batch pool create --json-file /tmp/pool-omop-d2-sequential.json

# Submit job with both tasks (they'll run sequentially on 1 slot)
JOB_ID="omop-run-sequential-$(date +%Y%m%d-%H%M%S)"
az batch job create --id "$JOB_ID" --pool-id omop-pool-d2-seq
az batch task create --job-id "$JOB_ID" --json-file ./task-worker-0.json
az batch task create --job-id "$JOB_ID" --json-file ./task-worker-1.json
```

---

## Summary

Recommended flow:

1. Run cleanup (Step 1)
2. Create D4 single-node pool with 2 slots (Step 3)
3. Update task JSONs with your SAS URLs
4. Submit job + tasks (Step 5)
5. Monitor with live loop (Step 6)
6. Download logs when complete (Step 7)

If you hit quota issues: Use the sequential D2 fallback (Step 11), though be aware this may OOM on large vocab loads.

Key success factors:

- Pool must have `containerConfiguration.type = dockerCompatible`
- Task JSON must have `containerRunOptions` with Docker socket mount
- No static ACR credentials in task JSON (identity-based pull only)
- Monitor node disk usage to avoid `DiskFull` errors

All commands tested for macOS compatibility. Let me know if you hit any blockers and paste the exact error output.
