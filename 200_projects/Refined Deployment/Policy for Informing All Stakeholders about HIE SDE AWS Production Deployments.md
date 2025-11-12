---
aliases: []
confidence: 
created: 2025-11-04T12:40:14Z
epistemic: 
last_reviewed: 
modified: 2025-11-12T14:24:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Policy for Informing All Stakeholders about HIE SDE AWS Production Deployments
type: 
uid: 
updated: 
---

Given that the HIE SDE is now a production deployment and requires ongoing resource updates in AWS, it's crucial to establish a clear policy and process for informing all stakeholders. This will help manage expectations, minimize disruption, and maintain the reliability of the service.

Based on the existing documentation, communication patterns, and team discussions, here is a proposed policy and process:

---

## Policy for Informing All Stakeholders about HIE SDE AWS Production Deployments

### Objective

To ensure all relevant stakeholders are timely informed about planned and unplanned changes to the HIE SDE AWS production environment, minimizing disruption and maintaining confidence in the platform's availability and performance. The HIE SDE is a complex environment involving a private EKS cluster, multi-AZ deployment, layered security, and hybrid connectivity, necessitating a robust communication strategy, as documented in our [HIE SDE v2 Infrastructure Analysis & Resource Mapping](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/Documentation/) notes.

### Scope

This policy applies to all changes (e.g., application updates, infrastructure modifications, security patches, configuration updates, scheduled maintenance, emergency fixes) impacting the HIE SDE AWS production environment.

### Principles
-   **Transparency:** Provide clear, concise, and accurate information.
-   **Timeliness:** Communicate proactively and with sufficient notice where possible, adhering to contractual Service Level Agreements (SLAs) as discussed in the [Slack chat with Susannah Thomas on September 5, 2025](https://slack.com/archives/C01234567/P0123456789).
-   **Relevance:** Tailor communication to the specific needs and technical understanding of different stakeholder groups.
-   **Accountability:** Assign clear responsibility for communication at each stage of the deployment lifecycle.

---

## Process to Follow for HIE SDE AWS Production Deployments

This process integrates our existing guidelines and addresses critical considerations for production environments.

### Phase 1: Planning & Preparation

1.  **Initiate Change Request & Documentation:**
    -   For any planned change (e.g., application update, infrastructure modification like EKS node resizing, security patch), create a detailed Jira ticket (e.g., FFAPP-4458 for node resizing, as seen on [Comet on November 4, 2025](https://app.comet.com/view/FFAPP-4458)).
    -   Refer to and update the general [241007 - AWS Deployment process - FITFILE - Confluence](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1922367492/241007+-+AWS+Deployment+process) and the [AWS - DevOps Checklist](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1922367492/241007+-+AWS+Deployment+process#AWS---DevOps-Checklist) for standardized procedures.
    -   For specific IAM permission requests (e.g., for `tf-deployment` user), create a Jira ticket with detailed actions and resource ARNs, following the template we've used for `eoe-sde-codisc` project (as generated via [Warp on September 29, 2025](<Warp window title: CENTRAL, last accessed 2025-09-29 16:22:42 Monday September 29 2025>)).

2.  **Perform Risk Assessment:**
    -   Evaluate the potential impact of the change. As Ollie Rushton noted in a [Slack chat on September 5, 2025](https://slack.com/archives/C01234567/P0123456789), "Application updates are simpler to deploy, but infrastructure updates are more hands-on (VM version upgrades, kubernetes upgrades, certificate rotation, secret rotation, etc...).".
    -   Assess the risk to service availability and performance, referencing the contractual 99% system uptime and scheduled maintenance downtimes.

3.  **Define Maintenance Window & Downtime:**
    -   If the change requires downtime or significant service degradation, identify a suitable maintenance window that aligns with our SLAs. Susannah Thomas mentioned in a [Slack chat on September 5, 2025](https://slack.com/archives/C01234567/P0123456789) that "System uptime is listed as 99% with scheduled maintenance downtimes listed as above."
    -   **Information Required:** Estimated downtime/impact, purpose of change, and precise start/end times.

4.  **Internal Team Review & Approval:**
    -   Review the change, risk assessment, and planned execution with the DevOps/Infrastructure Team (e.g., Leon, Ollie).
    -   Ensure that manual testing, monitoring strategies, and a clear rollback plan are in place, as Ollie outlined on [Slack on September 5, 2025](https://slack.com/archives/C01234567/P0123456789).
    -   Confirm on-call coverage, especially for deployments outside normal working hours, as the team does not yet have a formal "on-call" role (mentioned by Ollie in [Slack on September 6, 2025](https://slack.com/archives/C01234567/P0123456789)).

5.  **Draft Communication Plan:**
    -   Prepare internal and external communication messages, tailoring content for different audiences.

### Phase 2: Stakeholder Notification (Pre-Deployment)

1.  **Internal Notification (Minimum 24-48 hours notice for planned changes):**
    -   **Slack:** Announce planned changes, maintenance windows, and potential impact in relevant team channels (e.g., `#devops`, `#infrastructure`, `#product`). Always include a link to the corresponding Jira ticket.
    -   **Wednesday Meeting:** For significant roadmap items or cost optimization initiatives (e.g., FFAPP-4315, as documented in [Comet on November 3, 2025](https://app.comet.com/view/FFAPP-4315)), discuss in the weekly Wednesday meeting for prioritization and broader awareness.

2.  **External Notification (As per SLA and Customer Checklist - minimum 3-5 business days for planned service-impacting changes):**
    -   **Customer Communication:** Inform affected customers (e.g., EoE, CUH, MKUH, NNUH) about planned maintenance or changes impacting their service. Refer to the [AWS - Customer Checklist](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1922367492/241007+-+AWS+Deployment+process#AWS---Customer-Checklist) on Confluence for specific guidelines.
    -   **Direct Coordination:** For changes affecting specific integrations or data providers (e.g., S3 access for QA reports), coordinate directly with individuals like Keiran Raine and Easwaran Chandrasekaran (as seen in [Microsoft Teams on November 4, 2025](https://teams.microsoft.com/l/chat/19%3A41b71e0c7a524a8e8f81013a7c64a5c6%40thread.v2/0?groupId=&tenantId=)).
    -   **Channels:** Use agreed-upon external communication channels (e.g., email, dedicated customer portal).

### Phase 3: Execution & Monitoring

1.  **Initiate Deployment:**
    -   Trigger the infrastructure deployment via GitLab CI/CD, which integrates with HCP Terraform. This allows for planned changes to be run as pull request runs (as seen in [Comet on November 4, 2025](https://app.comet.com/view/run-i1gfrutHDUwzAWvz)).
    -   Follow the detailed deployment process specified on Confluence, as mentioned by Ollie Rushton.
    -   Ensure all `terraform plan` outputs are reviewed before proceeding to `terraform apply`.

2.  **Monitor & Observe:**
    -   Actively monitor the deployment through HCP Terraform logs, AWS Console, Grafana, and other relevant monitoring tools.
    -   Manually test key user flows and system capabilities, especially since automated testing may not cover all scenarios (as noted by Ollie in [Slack on September 5, 2025](https://slack.com/archives/C01234567/P0123456789)).

3.  **React & Respond to Issues:**
    -   Be prepared to react swiftly to deployment issues. "Not everything works 1st time, we reduce this risk with practice runs in other environments, but with each customer environment being slightly unique, issues can and will occur." ([Slack on September 5, 2025](https://slack.com/archives/C01234567/P0123456789)).
    -   **Rollback:** If issues cannot be immediately fixed, initiate a rollback using the predefined manual process.

4.  **Real-time Updates (During Critical Events):**
    -   **Internal:** Provide frequent updates in Slack channels regarding progress, issues, or delays.
    -   **External:** If the service is significantly impacted, send timely updates to affected customers via agreed channels.

### Phase 4: Post-Deployment & Review

1.  **Completion Notification:**
    -   **Internal:** Announce successful completion of the deployment in relevant Slack channels.
    -   **External:** Send a completion notice to customers, confirming service restoration and stability.

2.  **Post-Mortem/Lessons Learned:**
    -   For all significant changes or any incidents/failed deployments, conduct a post-mortem review.
    -   Update runbooks (e.g., the Todoist item "create a runbook for one of the errors in alerting" from [Todoist on October 14, 2025](https://todoist.com/app/project/2202685934)) and Confluence documentation ([241007 - AWS Deployment process - FITFILE - Confluence](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1922367492/241007+-+AWS+Deployment+process)) as needed.
    -   Ensure all associated Jira tickets are updated and closed.

---

### Communication Matrix (Summary Example)

| Change Type               | Lead Responsible       | Internal Notification (Slack)                                        | External Notification (Email/Portal)                                | Timing                                              |
| :------------------------ | :--------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------ | :-------------------------------------------------- |
| **Emergency Fix**         | DevOps Engineer        | Immediate alert in `#ops` & `#devops`                                | Immediate to critical stakeholders (as per Customer Checklist)      | As soon as identified, during & after resolution    |
| **Planned Infra Update**  | DevOps Engineer/Lead   | `#devops`, `#infrastructure`, `#product` (24-48h notice)             | Affected customers (3-5 business days notice)                       | Pre-deployment, during (if impact), post-deployment |
| **Application Update**    | DevOps Engineer/Lead   | `#devops`, `#product` (24-48h notice, or as part of sprint update)   | Product/business stakeholders (as agreed, e.g., weekly update)      | Pre-deployment, post-deployment                     |
| **Scheduled Maintenance** | DevOps Engineer/Lead   | `#devops`, `#infrastructure` (Weekly/Bi-weekly reminder)             | All customers (As per SLA/Customer Checklist - significant advance) | Pre-scheduled                                       |
| **IAM Permission Change** | DevOps Engineer/Lead   | `#devops`, `#cloud-security` (Jira link)                             | N/A (unless direct customer impact)                                 | Upon Jira creation & completion                     |
| **Cost Optimization**     | DevOps Engineer/FinOps | `#devops`, `#product`, Wednesday Meeting (for roadmap/prioritization) | N/A (unless affecting service/features)                             | Planning stage, implementation updates              |
