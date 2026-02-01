---
aliases: ["Accelerate", "DORA Research", "Software Delivery Performance"]
created: 2026-01-08T16:30:00Z
last_reviewed: ""
modified: 2026-02-01T15:08:02+00:00
status: "stable"
tags: ["architecture", "culture", "devops", "dora", "leadership"]
title: SoT - Accelerate & DORA
type: "SoT"
---

## SoT - Accelerate: The Science of Software Delivery

### 1. The Core Engine: Software Delivery Performance

High-performing organizations excel in _both_ speed and stability. There is no trade-off; stability-enabling practices are the same ones that foster high tempo.

#### The Four Key Metrics

1. Lead Time for Changes: The time from code commit to code successfully running in production.
2. Deployment Frequency: How often the organization deploys code (a proxy for batch size).
3. Mean Time to Restore (MTTR): How long it takes to restore service after an incident.
4. Change Failure Rate: The percentage of production changes resulting in degraded service or requiring remediation.

| Metric | High Performers (2017) | Low Performers (2017) |
|:--- |:--- |:--- |
| Deployment Frequency | On demand (multiple per day) | Between once per week and once per month |
| Lead Time for Changes | < 1 Hour | Between one week and one month |
| MTTR | < 1 Hour | Between one day and one week |
| Change Failure Rate | 0-15% | 31-45% |

### 2. The Capability Model

The research identifies 24 key capabilities across five domains. Unlike maturity models, which assume a static "destination," the capability model focuses on continuous, contextual improvement.

#### A. Continuous Delivery (Technical)

- Version Control: Comprehensive use for application code, system configuration, and scripts.
- Trunk-Based Development: Integrating into master/trunk daily; avoiding long-lived branches or "code freezes."
- Continuous Integration (CI): Automated builds and tests triggered by every check-in.
- Deployment & Test Automation: Reliable, automated pipelines that provide fast feedback.
- Shift Left on Security: Integrating InfoSec into the entire lifecycle rather than as a downstream phase.

#### B. Architecture

- Loosely Coupled Architecture: Systems designed so teams can test and deploy applications on demand without high-bandwidth coordination with other teams.
- Empowered Teams: Practitioners are empowered to choose their own tools and technologies.

#### C. Lean Management & Product Development

- WIP Limits: Using Work-in-Process limits to expose bottlenecks.
- Visual Management: Using dashboards and kanban boards to visualize work status and quality metrics.
- Small Batches: Decomposing work into features completed in less than one week.
- Customer Feedback: Regularly incorporating customer input into product design.

### 3. Organizational Culture & Leadership

#### Westrum Typology of Culture

Culture is the primary predictor of performance and can be measured by how information flows.

| Generative (Performance-Oriented) | Bureaucratic (Rule-Oriented) | Pathological (Power-Oriented) |
|:--- |:--- |:--- |
| High cooperation | Modest cooperation | Low cooperation |
| Messengers are trained/welcomed | Messengers are neglected | Messengers are "shot" (punished) |
| Risks are shared | Narrowly defined responsibility | Responsibility is avoided |
| Bridging is encouraged | Bridging is tolerated | Bridging is discouraged |
| Failure leads to inquiry/learning | Failure leads to "justice" | Failure leads to scapegoating |

#### Transformational Leadership

Leadership does not directly cause high performance but enables the adoption of technical and process practices.

- Five Factors: Vision, Intellectual Stimulation, Inspirational Communication, Supportive Leadership, and Personal Recognition.

### 4. The Human Element

- "Act Your Way to a New Culture": You do not change how people think to change culture; you change their _behaviors_. Implementing CD and Lean practices directly improves organizational culture.
- Burnout: Predicted by pathological culture, lack of control, and high "deployment pain" (anxiety surrounding releases).
- Identity: Strong software delivery performance correlates with higher employee job satisfaction and eNPS (Net Promoter Score).

---

### Sources & References

- _Accelerate: The Science of Lean Software and DevOps_ (Forsgren, Humble, Kim).
- DORA (DevOps Research and Assessment) annual reports (2014-2017).
- [[SoT - DevOps & Infrastructure Architecture Strategy]]
