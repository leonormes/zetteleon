---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/700e18422ad6"
author:
  - "[[Gemini]]"
published:
created: 2025-12-29
description: "Created with Gemini"
tags:
  - "clippings"
---
extract the tagging part of the release process as a md wiki

## Release Tagging Procedure

The tagging process is a critical phase of the FITFILE release cycle, ensuring that specific commits are promoted to the correct environments using semantic versioning and environment-specific pointers.

---

### 1\. Semantic Versioning

Before environment promotion, a formal version tag must be created in the deployment repository.

- **Repository Location**: GitLab deployment tags (`https://gitlab.com/fitfile/deployment/-/tags`).
- **Version Format**: Follow **Semantic Versioning 2.0.0**.
- **Version Increment**: Usually a **patch version** increment; consult the team for confirmation.
- **Documentation**: The tag must include a description and a list of all ticket numbers (e.g., `FFAPP-1234`) being released with their respective descriptions.

### 2\. Environment Tagging Strategy

Each customer environment tracks a specific release tag. Because ArgoCD agents monitor these tags, promoting a release requires reassigning the environment tag to a new commit.

| Environment/Customer | Tag Name |
| --- | --- |
| FITFILE Production (Commercial Demos) | `latest-release` |
| East of England | `eoe-latest-release` |
| Cambridge University Hospitals | `cuh-prod-1-latest-release` |

### 3\. Execution Steps

To promote a specific commit to an environment, follow this "delete and recreate" logic:

1. **Delete Existing Pointer**: Navigate to the deployment repository tags and delete the current environment tag (e.g., `latest-release`) for the target environment.
2. **Reassign Tag**: Create a new tag using that **exact same environment tag name** on the commit you wish to release.
3. **Deployment Trigger**: Do **not** click the "Create release" button in GitLab for environment tags.
4. **Propagation**: Wait approximately **10–15 minutes** for ArgoCD agents to detect the tag change and update production deployments.

---

### Critical Constraints

- **Network Synchronization**: All nodes within a network must be promoted within the same non-working hours to maintain **API compatibility**.
- **Atomic Promotion**: Everything currently in the **staging environment** is promoted to production; there is no current mechanism to cherry-pick specific tickets during the release.

Would you like me to extract the Manual Smoke Test "Happy Path" into a checklist format as well?

yes

### Manual Smoke Tests (Happy Path)

The following tests must be executed on the staging environment (`ff-test-a.fitfile.net`) prior to production release.

---

### 1\. Resource Verification

- **Authentication**: Login to the application as `diya.kumar@fitfile.com`.
- **Navigation**: Access project **"2401 Oncology Cohort Identification"**.
- **Query Consistency**: Run the following query plans and verify results (count and result graph) match expected outputs:
	- `int-test-8`
	- `int-test-26`
	- `int-test-6`

### 2\. New Customer Workflow

- **Account Integrity**: Confirm user roles and project access remain unchanged after login.
- **Tenant Configuration**: In Tenant Settings, ensure **Small Number Suppression** is set to 0 and **Data Disclosure** is disabled.
- **Project Setup**: Create a new project, assign user roles, and add an external user.
- **Data Ingestion**:
	- Create a file upload datasource using: `int_test_dataset_1_100.csv`, `int_test_dataset_2_100.csv`, `int_test_dataset_3_100.csv`, and `int_test_dataset_isolated_1000.json`.
	- Define schemas and wait for validation.
	- Assign the datasource to the new project.
- **Query Execution**:
	- **Identifiable**: Run an Identifiable Query plan on `int_test_dataset_isolated_1000`; verify results, data profile, lineage, and export functionality.
	- **Pseudonymised**: Create and run a pseudonymised query plan; verify results.
	- **Anonymised**: Create and run an anonymised query plan; verify results.
- **Permission Logic**: Remove identifiable data access from project permissions; refresh and confirm the identifiable dataset is blocked.
- **Advanced Operations**:
	- Enable **Data Disclosure** in the tenant.
	- **Merge**: Run a merge pseudonymised query between datasets 1 and 2 (, suppression limit 0.1, weighted columns); approve request in **Data Operations** and verify results.
	- **Concat**: Run a concat pseudonymised query between datasets 1 and 2 (, suppression limit 0.1, weighted columns); verify results.

### 3\. Teardown & Cleanup

- **Query Plans**: Delete plans and confirm they are removed from the project.
- **Datasource**: Disconnect the datasource; verify it no longer appears in project metadata or the project view after refresh.
- **Project**: Delete the project and confirm it is removed from the dashboard.
- **Final Cleanup**: Delete the datasource and verify removal from the data sources list.

---

Would you like me to create a summary of the **Pre-Release Checklist** to ensure all environmental and administrative dependencies are met?

Yes

### Pre-Release Checklist

The pre-release phase focuses on environment stability and customer impact mitigation. This must be completed before any tagging or testing begins.

---

#### 1\. Scheduling & Stakeholders

- **Customer Timing**: Ensure the release occurs outside of customer working hours.
- **Exception Rule**: If it is confirmed that no customers are currently using the environments, you are free to release.
- **Demo Protection**: Verify that no customer demonstrations are scheduled in the production environment (`app.fitfile.net`).
- **Coordination**: Check with @danielle.hawley if demos are not already listed in the FITFILE calendar.

#### 2\. Ticket & Code Readiness

- **Verification**: Ensure all tickets in 'Ready for Test' have been verified against acceptance criteria.
- **Validation**: Confirm all tickets are validated with the product owner.
- **Status Update**: Move validated tickets to 'Ready for Release'.
- **Environment Sync**: Visit `staging-argocd.fitfile.net` to verify all applications are synced and healthy.
- **Infrastructure Note**: Be aware that everything in staging is promoted to production; cherry-picking is currently impossible.

#### 3\. Communication & Monitoring

- **Slack Notification**: Send a message to the `#dev` channel stating that the release is starting.
- **Incident Review**: Check the `#non-prod-alerts` channel and review any active incidents.

---

### Release Process Framework

| Stage | Focus | Key Action |
| --- | --- | --- |
| **I. Pre-Release** | Risk Mitigation | Check calendars, Slack alerts, and ticket statuses. |
| **II. Smoke Tests** | Functional Validation | Execute the "Happy Path" on staging (`ff-test-a`). |
| **III. Tagging** | Version Control | Increment SemVer and reassign environment tags in GitLab. |
| **IV. Post-Release** | Deployment Audit | Monitor ArgoCD and Grafana for 10–15 minutes. |

Would you like me to compile all these sections into a single, downloadable technical SOP document?

Google Account

Leon Ormes

leonormes@gmail.com