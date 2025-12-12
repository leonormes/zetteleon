---
aliases: []
assignee: Leon Ormes
budget_target: £750/month
confidence: 
created: 2025-10-03T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
priority: high
project: FFAPP-4315
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: planning
tags: []
title: Azure Production Cost Optimization - FFAPP-4315
type:
uid: 
updated: 
version:
---

## 🎯 Project Overview

**Objective**: Reduce Azure production costs to stay within £750/month budget threshold
**Current Status**: Forecasted to exceed budget - immediate intervention required
**Timeline**: 3 sprints (estimated 6-8 weeks)
**JIRA**: [FFAPP-4315](https://fitfile.atlassian.net/browse/FFAPP-4315)

## 📊 Current State Analysis

### Infrastructure Inventory

- **Subscription**: FITCloud Production (`a448d869-4ec5-4c81-82c5-d6e8fa0ec0df`)
- **Primary AKS Cluster**: `fitfile-cloud-prod-1-aks-cluster`
- **Node Pools**:
  - System: 3 × Standard_E4s_v5 (min: 2, max: 4)
  - Workflows: 1 × Standard_E4s_v5 Spot (min: 1, max: 6)

### Cost Drivers Identified

#### 1. 🖥️ VM Compute (Estimated £400-500/month)

- **Issue**: 4-5 Standard_E4s_v5 VMs running 24/7
- **Optimization Potential**: 40-60% reduction

#### 2. 💾 Snapshot Storage (Estimated £50-100/month)

- **Critical Issue**: 899 total snapshots
  - Production cluster: ~235 snapshots
  - PROD-1 backups: ~664 snapshots
- **Optimization Potential**: 80%+ reduction

#### 3. 🗄️ Storage Accounts (Estimated £30-50/month)

- All backup storage in expensive Hot tier
- No lifecycle management policies

## 🚀 Implementation Roadmap

### Phase 1: Assessment & Analysis (Sprint 1)

**Duration**: 1-2 weeks
**Goals**: Quantify current costs and validate optimization opportunities

#### Tasks

- [ ] **Export Cost Data** (Priority: High)
  - Use Azure Cost Management to export 60-day consumption data
  - Isolate top 10 cost drivers by resource group
  - Create baseline monthly spend analysis
- [ ] **Calculate Savings Potential** (Priority: High)

```bash
# Commands for cost analysis
az consumption budget list --output table
az consumption usage list --start-date 2025-09-01 --end-date 2025-10-01
```

- [ ] **Performance Benchmarking** (Priority: Medium)
  - Collect CPU/Memory utilization from Container Insights
  - Run `kubectl top nodes` and `kubectl top pods` analysis
  - Document current resource usage patterns

#### Deliverables

- Cost breakdown spreadsheet
- Savings opportunity matrix
- Resource utilization baseline

### Phase 2: Infrastructure Optimization (Sprint 2)

**Duration**: 3-4 weeks
**Goals**: Implement major cost reduction measures

#### 2.1 AKS Node Pool Optimization

- [ ] **Right-size System Node Pool** (Priority: High)

```bash
# Test in staging first
az aks nodepool add --name system-test --vm-size Standard_D2s_v5 \
--min-count 2 --max-count 4 --enable-cluster-autoscaler

# If successful, upgrade production
az aks nodepool upgrade --name system --vm-size Standard_D2s_v5
```

- **Expected Savings**: 30-40% on system node costs
- **Risk**: Performance degradation - requires testing

- [ ] **Enable Workflows Auto-scale to Zero** (Priority: High)

```bash
az aks nodepool update \
--resource-group fitfile-cloud-prod-1-rg \
--cluster-name fitfile-cloud-prod-1-aks-cluster \
--name workflows \
--min-count 0
```

- **Expected Savings**: 50%+ on workflows compute during idle periods
- **Risk**: Cold start delays for workflow execution

#### 2.2 Application-level Changes

- [ ] **Remove Primary Care Node** (Priority: Medium)
  - ⚠️ **Stakeholder Sign-off Required**
  - Disable STG data sync (confirm with project team)
  - Clean up associated PVCs and deployments
  - Verify no dependencies remain

- [ ] **Optimize The Hyve Application** (Priority: Medium)
  - Convert from continuous deployment to CronJob
  - Trigger only on synthetic data updates
  - Set default replicas to 0 when idle
  - **Expected Savings**: 20-30% on application-specific compute

#### 2.3 Schedule-based Scaling

- [ ] **Implement Off-hours Shutdown** (Priority: Medium)
  - Create Azure Automation Runbooks
  - Schedule: Stop at 20:00 UTC, Start at 06:00 UTC (weekdays)
  - **⚠️ Critical**: Confirm no overnight batch jobs
  - Test in non-production for 1 week first

```powershell
# Sample runbook logic
$resourceGroup = "fitfile-cloud-prod-1-rg"
$clusterName = "fitfile-cloud-prod-1-aks-cluster"

# Stop cluster
Stop-AzAksCluster -ResourceGroupName $resourceGroup -Name $clusterName

# Start cluster
Start-AzAksCluster -ResourceGroupName $resourceGroup -Name $clusterName
```

#### Deliverables

- Updated node pool configurations
- Automated scaling policies
- Performance validation reports

### Phase 3: Storage & Backup Optimization (Sprint 3)

**Duration**: 2-3 weeks
**Goals**: Eliminate storage waste and optimize backup strategy

#### 3.1 Snapshot Management

- [ ] **Audit Existing Snapshots** (Priority: Critical)

```bash
# List all snapshots with metadata
az snapshot list --query '[].{Name:name, ResourceGroup:resourceGroup, \
Size:diskSizeGb, Created:timeCreated}' --output table

# Count by resource group
az snapshot list --query 'group_by([].resourceGroup, &[0]) | \
map(&{ResourceGroup: [0], Count: length([1])}[])' --output table
```

- [ ] **Implement Retention Policy** (Priority: Critical)
  - **Policy**: Retain last 7 daily + 4 weekly + 6 monthly snapshots
  - **Bulk Delete**: Remove snapshots older than 30 days beyond policy
  - **Expected Reduction**: From 899 to ~50 snapshots (94% reduction)

```bash
# Example cleanup (TEST FIRST!)
az snapshot list --query '[?timeCreated < `2025-09-01`].name' -o tsv | \
xargs -I {} az snapshot delete --name {}
```

- [ ] **Apply Same Policy to Non-Production** (Priority: Medium)
  - Non-prod has 219 additional snapshots
  - Same retention policy applies

#### 3.2 Storage Account Optimization

- [ ] **Implement Storage Tiering** (Priority: High)

```bash
# Move storage accounts to Cool tier
az storage account update --name aksprodbackups --access-tier Cool
az storage account update --name prod1backupsa --access-tier Cool

# Set lifecycle management
az storage account management-policy create \
--account-name aksprodbackups \
--policy @lifecycle-policy.json
```

- [ ] **Revise Backup Strategy** (Priority: Medium)
  - Implement Velero for Kubernetes-native backups
  - Switch from full cluster to PV-only backups
  - Reduce frequency: Daily incremental, weekly full

```yaml
# Velero backup schedule
apiVersion: velero.io/v1
kind: Schedule
metadata:
name: daily-backup
spec:
schedule: "0 1 * * *" # 01:00 UTC daily
template:
  includedResources:
    - persistentvolumes
    - persistentvolumeclaims
```

#### Deliverables

- Cleaned snapshot inventory
- Optimized storage tier configuration
- New backup strategy implementation

## 📈 Expected Outcomes

### Cost Reduction Targets

| Optimization Area | Current Est. | Target Reduction | Monthly Savings |
| ----------------- | ------------ | ---------------- | --------------- |
| VM Compute        | £400-500     | 40-60%           | £160-300        |
| Snapshot Storage  | £50-100      | 80%+             | £40-80          |
| Storage Accounts  | £30-50       | 50%              | £15-25          |
| **Total Savings** |              |                  | **£215-405**    |

### Success Metrics

- [ ] Monthly spend < £750 (with 20% buffer)
- [ ] Snapshot count reduced to < 100 total
- [ ] Node pool utilization > 60% average
- [ ] Zero performance degradation incidents

## ⚠️ Risk Management

### High-Risk Changes

1. **System Node Pool Right-sizing**
   - **Risk**: Performance degradation
   - **Mitigation**: Thorough staging testing, gradual rollout
2. **Schedule-based Shutdown**
   - **Risk**: Disrupting critical overnight processes
   - **Mitigation**: Audit all cron jobs, implement monitoring
3. **Bulk Snapshot Deletion**
   - **Risk**: Accidental data loss
   - **Mitigation**: Test with small batch first, verify backup coverage

### Rollback Procedures

```bash
# Rollback node pool changes
az aks nodepool update --name system --min-count 2 --vm-size Standard_E4s_v5

# Rollback workflows scaling
az aks nodepool update --name workflows --min-count 1

# Emergency cluster restart
az aks start --resource-group fitfile-cloud-prod-1-rg \
--name fitfile-cloud-prod-1-aks-cluster
```

## 📋 Monitoring & Governance

### Budget Alerts

- [ ] Set up 70% threshold alert (£525)
- [ ] Set up 90% threshold alert (£675)
- [ ] Weekly cost review meetings

### Dashboards

- [ ] Create Grafana cost monitoring dashboard
- [ ] Azure Cost Management integration
- [ ] Resource utilization tracking

### Reporting Schedule

- **Daily**: Automated cost alerts
- **Weekly**: Team progress review
- **Monthly**: Executive cost summary

## 👥 Stakeholders & Responsibilities

| Role               | Person/Team         | Responsibilities                            |
| ------------------ | ------------------- | ------------------------------------------- |
| **Project Owner**  | Leon Ormes          | Overall delivery, stakeholder communication |
| **Infrastructure** | Infrastructure Team | Technical implementation                    |
| **Product Owner**  | Weronika            | Roadmap prioritization, resource allocation |
| **Operations**     | DevOps Team         | Monitoring, rollback procedures             |

## 📅 Key Milestones

- [ ] **Week 2**: Cost baseline and savings calculation complete
- [ ] **Week 4**: Node pool optimization deployed to staging
- [ ] **Week 6**: Production infrastructure changes complete
- [ ] **Week 8**: Storage optimization and monitoring in place
- [ ] **Week 10**: Full rollout complete, budget compliance achieved

## 🔗 Related Resources

### Documentation

- [Azure AKS Autoscaling](https://docs.microsoft.com/en-us/azure/aks/cluster-autoscaler)
- [Azure Cost Management](https://docs.microsoft.com/en-us/azure/cost-management-billing/)
- [Velero Documentation](https://velero.io/docs/)
- [Storage Lifecycle Management](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-lifecycle-management-concepts)

### Azure Resources

- [Production Subscription Portal](https://portal.azure.com/#@45e73aa3-1ee9-47c0-ba25-54eda9da021a/resource/subscriptions/a448d869-4ec5-4c81-82c5-d6e8fa0ec0df/overview)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

### Project Files

- Infrastructure Code: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/FITFILE/Production/fitfile-production-infrastructure`
- JIRA Ticket: [FFAPP-4315](https://fitfile.atlassian.net/browse/FFAPP-4315)

---

*Last Updated: 2025-10-03*
*Next Review: Weekly Wednesday meetings*
*Status: Ready for Sprint 1 kickoff*
