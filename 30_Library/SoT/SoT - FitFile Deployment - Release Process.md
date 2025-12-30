---
aliases: ["Release Tagging Procedure", "FitFile Release Checklist", "FitFile Smoke Tests"]
confidence: "5/5"
created: 2025-12-29T10:26:01+00:00
epistemic: "procedure"
last_reviewed: "2025-12-29"
modified: 2025-12-30T14:11:32+00:00
purpose: "To define the standard operating procedure for tagging, promoting, and verifying FitFile platform releases across environments."
review_interval: "3 months"
see_also: ["[[SoT - FITFILE Platform Deployment]]", "[[SoT - FitFile Deployment - Helm Configuration & Operations]]"]
source_of_truth: []
status: "stable"
tags: ["process", "deployment", "release", "qa", "fitfile"]
title: SoT - FitFile Deployment - Release Process
type: "SoT"
uid: 
updated: 
---

## 1. Release Strategy & SemVer

The release process relies on **Semantic Versioning** and **Environment Pointers** within the deployment repository.

- **Repository:** GitLab deployment tags (`https://gitlab.com/fitfile/deployment/-/tags`).
- **SemVer:** Releases must be tagged with a formal version (e.g., `v1.2.3`).
    - **Increment:** Typically a **patch** increment unless specified otherwise.
    - **Metadata:** The tag description must list all included ticket numbers (e.g., `FFAPP-1234`) and descriptions.

### Environment Pointers

Environments track specific "pointer tags" rather than raw version numbers. Promotion involves moving these pointers.

| Environment | Pointer Tag Name | Usage |
|:--- |:--- |:--- |
| **Production** | `latest-release` | Commercial Demos / Live |
| **East of England** | `eoe-latest-release` | Region Specific |
| **CUH** | `cuh-prod-1-latest-release` | Dedicated Customer |

> [!warning] Atomic Promotion
> The staging environment is promoted **atomically** to production. Cherry-picking tickets during release is not supported.

---

## 2. Pre-Release Checklist

Completed prior to any tagging.

### A. Scheduling & Stakeholders

- [ ] **Timing:** Schedule outside customer working hours (unless confirmed idle).
- [ ] **Conflict Check:** Verify no active customer demos (check `FITFILE` calendar and `@danielle.hawley`).
- [ ] **Sync:** Ensure all nodes in a network are promoted in the same window (API compatibility).

### B. Readiness

- [ ] **Validation:** All 'Ready for Test' tickets verified and moved to 'Ready for Release'.
- [ ] **Staging Health:** Confirm `staging-argocd.fitfile.net` shows all apps synced/healthy.

### C. Communication

- [ ] **Notify:** Post to Slack `#dev` channel: "Release starting."
- [ ] **Alerts:** Check `#non-prod-alerts` for active incidents.

---

## 3. Execution: The "Delete and Recreate" Protocol

To promote a commit:

1. **Delete Pointer:** Remove the existing environment tag (e.g., `latest-release`) from the repo.
2. **Reassign Pointer:** Create a **new tag** with the *exact same name* on the target commit.
3. **Trigger:** Do **not** use the "Create release" button. Just create the tag.
4. **Propagate:** Wait **10–15 minutes** for ArgoCD to detect and sync.

---

## 4. Manual Smoke Tests (Happy Path)

Execute on Staging (`ff-test-a`) before production promotion.

### A. Resource Verification

- [ ] **Login:** As `diya.kumar@fitfile.com`.
- [ ] **Project:** "2401 Oncology Cohort Identification".
- [ ] **Queries:** Run plans `int-test-8`, `int-test-26`, `int-test-6`. Verify counts and graphs.

### B. New Customer Workflow

1. **Setup:**
    - [ ] Create new project & add external user.
    - [ ] Tenant Settings: `Small Number Suppression = 0`, `Data Disclosure = Disabled`.
2. **Data Ingestion:**
    - [ ] Create File Upload Datasource (`int_test_dataset_1_100.csv` etc).
    - [ ] Define schemas -> Validate -> Assign to Project.
3. **Query Execution:**
    - [ ] **Identifiable:** Run on `isolated_1000`. Check profile/lineage/export.
    - [ ] **Pseudonymised:** Run and verify.
    - [ ] **Anonymised:** Run and verify.
4. **Security Check:**
    - [ ] Remove identifiable permission. Refresh. Confirm block.
5. **Advanced:**
    - [ ] Enable `Data Disclosure`.
    - [ ] **Merge/Concat:** Run operations between datasets 1 & 2 (Limit 0.1). Verify results.

### C. Teardown

- [ ] Delete Query Plans.
- [ ] Disconnect & Delete Datasource.
- [ ] Delete Project.
