---
aliases: []
confidence: 
created: 2025-10-15T10:49:42Z
epistemic: 
last_reviewed: 
modified: 2025-11-01T15:17:00Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Grafana onCall
type:
uid: 
updated: 
version:
---

## Understanding Incident Response Management (IRM) in Grafana Cloud

Grafana Cloud offers a comprehensive system for monitoring, alerting, and incident response, often referred to as **Incident Response Management (IRM)**. It integrates multiple components to help detect, notify, and manage problems in your infrastructure effectively.

---

### Key Components in Grafana Cloud IRM

1. **Alert Rules**: These define the conditions in your monitored metrics or log data that indicate a problem. For example, an alert rule might be set to fire when CPU usage exceeds 90% for 5 minutes.
2. **Contact Points**: These specify *who* should get notified and *how* (e.g., Slack message, email, PagerDuty).
3. **Notification Policies (Routing)**: These manage how alert instances are routed to contact points, including escalation paths and grouping.
4. **Alert Instances and States**: When an alert rule condition is met, an alert instance is created and goes through states like pending, firing, or recovered.
5. **Alertmanager**: This component handles alert deduplication, grouping, silencing, and routing notifications.
6. **Integrations with OnCall and Messaging Tools**: Grafana’s alerting system integrates with OnCall tools and Slack to facilitate incident management and collaboration.

---

### Typical Workflow Story — From Cluster Issue to Resolved Incident

#### Scenario: A Problematic Cluster Pod Causes a Service Disruption

1. **Problem Occurrence**: A Kubernetes pod in a cluster becomes unresponsive due to resource exhaustion.
2. **Metrics Trigger Alert Rule**: Grafana Cloud’s alert rules monitor CPU and pod health metrics continuously. The alert rule for "High CPU Usage" triggers after the CPU remains above threshold for 5 minutes.
3. **Pending then Firing State**: Once the threshold is breached, the alert instance stays in a "pending" state to avoid flapping from transient issues. If the condition persists, it moves to "firing."
4. **Alertmanager Processes Alert**: The Alertmanager receives the firing alert instance, grouping it with related alerts and checking for silences or escalations.
5. **Notification Delivery via Contact Points**: According to configured notification policies, Alertmanager sends a message to the configured Slack channel and raises an incident in the OnCall system.
6. **Dev OnCall Receives Alert**: A developer on call sees the Slack notification with details and urgency of the issue.
7. **Incident Acknowledgment and Investigation**: The dev acknowledges the alert, checks Grafana dashboards for logs and metrics, and confirms the pod issue.
8. **Mitigation**: The dev may restart the pod, adjust resource limits, or roll back a recent deployment to fix the problem.
9. **Recovery and Alert Resolution**: Once the pod health metrics return to normal, the alert instance recovers. The Alertmanager updates alert states accordingly, and the incident is closed in the OnCall system.
10. **Post-Mortem and Improvements**: Incident details are reviewed for root causes and to improve alert rules or automation.

---

### How Grafana Cloud Tools Fit Together for Robust Incident Response

- **Monitoring & Alert Rules** consistently scan metrics and logs.
- **Alertmanager** manages state, deduplication, and notification routing.
- **Notification Policies and Contact Points** control who gets alerted and how.
- **OnCall Systems and Slack** integrate to provide real-time incident visibility and communication.
- **Dashboards and Logs** offer detailed context for fast diagnosis.

---

Would you like me to walk you through setting up a simple alert rule with Slack notifications in your Grafana Cloud environment? Or, would you prefer a deeper dive into how to use OnCall tools integrated with Grafana alerts?

## Deep Dive: Using OnCall Tools Integrated with Grafana Alerts

Here’s a **structured breakdown** of using Grafana OnCall tools, showing how alerts flow through the system and how a developer responds—optimized for practical, ADHD-friendly workflow:

---

### 1. **How Integration Works**

- **Alerts from Grafana Cloud Alerting**:
  - Alert rules monitor clusters, logs, and metrics.
  - Alerts trigger when thresholds are breached (e.g., CPU, pod failure).[grafana](https://grafana.com/docs/oncall/latest/set-up/get-started/)​
- **OnCall Integration Setup**:
  - In Grafana, go to **Alerts & IRM → OnCall**.
  - Navigate to **Integrations** tab and click **+ New integration**.
  - Choose integration type (Grafana, Prometheus, AWS Incident Manager, etc.), or use a webhook for custom options.grafana+3​
  - Configure routing, escalation chains, and schedules for your teams.

---

### 2. **Alert Workflow Example**

**Incident:** A pod in a cluster crashes due to memory exhaustion.

1. **Alert Rule Fires**
   - Grafana Alerting detects abnormal metric, creates an alert instance.

2. **Alert Routed to OnCall**
   - The alert hits OnCall via API/webhook.grafana+2​
   - OnCall groups the alert, associates it with escalation chain/schedule.

3. **Notification & Routing**
   - OnCall routes to first responder’s Slack, SMS, email, or custom contact point.
   - Alerts appear in the relevant Slack channel, OnCall app, or both.grafana+1​
   - Context-rich notification includes metrics, dashboards, and links.

4. **Escalation if Unacknowledged**
   - If responder does not acknowledge in time, escalation steps trigger (next on-call, manager, SRE team).grafana+1​
   - Automated reminders in Slack (configurable timeout).

5. **Dev OnCall Responds**
   - They acknowledge in Slack or via OnCall interface.
   - Can resolve, add notes, run checks, or reference automated Sift diagnostics directly in Slack/Grafana.[grafana](https://grafana.com/blog/2024/03/29/a-better-grafana-oncall-seamless-workflows-with-the-rest-of-grafana-cloud/)​

6. **Investigation and Resolution**
   - Use linked dashboards/logs for RC, restart pod, fix issue.
   - Resolution notes and actions logged in OnCall.
   - Incident closed upon metric recovery or manual resolution.

---

### 3. **Features That Support Robust Response**

- **Automated Escalation**: Multi-step process, always escalates unacknowledged alerts to next available responder.
- **Custom Schedules**: Calendar-based on-call rotations (centralized for teams).
- **Slack/ChatOps Integration**: Respond to alerts (acknowledge, resolve) without switching context.grafana+1​
- **Runbooks & Context Links**: Alert notifications include direct links to runbooks, dashboards, logs.
- **Sift Automated Diagnostics**: Triggered from OnCall, Sift analyzes logs/metrics to pre-fill diagnostic clues for the on-call dev.[grafana](https://grafana.com/blog/2024/03/29/a-better-grafana-oncall-seamless-workflows-with-the-rest-of-grafana-cloud/)​
- **Incident Management Tools**: Declare, track, and resolve incidents all from Grafana IRM suite.

---

### 4. **Practical Setup Steps**

**For your workflow:**

- Set up OnCall integrations in Grafana Cloud.
- Create escalation chains (who gets called, order).
- Link your Slack workspace via OnCall’s ChatOps tab. Configure reminders/timeouts as needed.[grafana](https://grafana.com/docs/oncall/latest/manage/notify/slack/)​
- Associate alert rules with on-call schedules, escalation policies, and contact points.
- Enable Sift for diagnostics if available.

---

### **Summary Table**

| Step              | Tool/Location              | Key Action                               |
| ----------------- | -------------------------- | ---------------------------------------- |
| Alert Rule Fires  | Grafana Alerting           | Metric breach triggers alert             |
| Routed to OnCall  | Grafana OnCall Integration | Alert grouped, escalation applies        |
| Notification      | Slack/Email/SMS via OnCall | First responder notified, alert visible  |
| Escalation        | OnCall Settings            | Unacknowledged alert triggers escalation |
| Incident Response | Slack/OnCall UI            | Acknowledge, investigate, resolve        |
| Resolution        | OnCall/Grafana             | Notes, runbooks, metrics check           |
| Review            | OnCall/Grafana IRM         | Postmortem, continuous improvement       |

---

**This workflow eliminates guesswork and context switching, giving your DevOps team what they need fast, in the tools you actually use.**
