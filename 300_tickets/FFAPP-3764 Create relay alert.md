---
aliases: []
confidence: 
created: 2025-05-20T11:11:58Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FFAPP-3764 Create relay alert
type: project
uid: 
updated: 
version:
---

## Project: FFAPP-3764 Create Relay Alert

---

### 1. Why is This Important? (Purpose & Principles)

We need to stay on top of relay and make sure it is always working. We need to know if it breaks.

### 2. What Does Success Look Like? (Outcome Visioning)

We have several descriptive alerts that are easy to understand and to pinpoint the error.

When something stops working in relay we find out straight away.

It should be part of a comprehensive monitoring of relay.

There is a run book describing what to do with an alert.

### 3. Ideas & Brainstorming (How Could I Achieve this?)

- Initial thoughts on approach:
  - Find the logs related and create a filter
  - our alerting is not very functional at the moment.
  - I've forgot how to use grafana
  - need to review the alerting system.
- Questions I have:
- Resources:
- Random ideas:
  - we need more documentation on monitoring.

### 4. Organised Thoughts & Potential Steps (Organising)

### 5. Next Actions (What's the *very* next thing?)

- [x] Identify relevant logs %%[tid:: [6c4R8xRjXRC64qxM](todoist://task?id=6c4R8xRjXRC64qxM)]%% [completion:: 2025-09-30]
- [x] create filter for logs %%[tid:: [6c4R8xc4qHHGQ7gM](todoist://task?id=6c4R8xc4qHHGQ7gM)]%% [completion:: 2025-09-30]
- [x] Investigate if there is Prometheus for relay %%[tid:: [6c4R8xh39F5mj22v](todoist://task?id=6c4R8xh39F5mj22v)]%%
- [x] find logs from bunny on ff-a %%[tid:: [6c4R8xfpm6Rm4Pgv](todoist://task?id=6c4R8xfpm6Rm4Pgv)]%% [completion:: 2025-09-30]
