---
captured: "2026-04-28T13:28:10+01:00 2026-04-28T13:28:10+01:00"
created: 2026-04-28T12:28:11+00:00
modified: 2026-05-26T11:44:30+00:00
source: "https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2632253441/2026-02-12+HIE+NUH+FITFILE+-+FITFILE+Tech+and+Data+Questions+meeting"
status: "processing"
tags: ["input"]
title: HEAD 2026-02-12 HIENUHFITFILE - FITFILE Tech and Data Questions meeting - EOE SDE project
type: "head"
---

## Raw Output / Content

## 2026-02-12: HIE/NUH/FITFILE - FITFILE Tech and Data Questions Meeting

## Participants

- FITFILE:,,,,
- HIE EoE: Mark Dines-Allen
- HIE East Mids: Nada Mostafa
- NUH: Phil Quinlan, Andy Rae, Irene Juurlink, Alex Waldren-Glenn
- Apologies: John Baines (NUH)

## Agenda

- Discuss tech and data requirements

## Meeting Recording

Link to recording of the meeting: [FITFILE / NUH Tech and Data Discovery Session](https://fathom.video/share/fVywGmKXBZyM7aZcCShFz5JiHyhQcsKJ)

## Meeting Summary

### Clarifying Deployment Model

- The group discussed the deployment model for the FITFILE software - there was a slight misunderstanding as to how the deployment would work. NUH advised they require a fully on-premise solution, whereas FITFILE's proposed solution is a hybrid Cloud/on-premises approach. The discussion focused on understanding the technical requirements, NUH's existing infrastructure and capabilities, and the pros and cons of the different deployment options.

### Exploring On-premises Feasibility

- Helena from FITFILE suggested exploring the on-premises option in more detail, to understand the NUH's existing server infrastructure, Kubernetes clusters, and technical capabilities. This would help determine if an on-premises deployment is feasible and identify any constraints or requirements that need to be addressed.
- FITFILE will discuss the options in detail internally, and proposed a call with John Baines and Chris Turner from NUH's Infrastructure team to dive deeper into the technical details and feasibility of an on-premises deployment.
- FITFILE will also provide additional documentation and guidance on their hybrid deployment model used with CUH. The goal is to find the simplest solution to get the initial deployment up and running, while also considering the longer-term options.
- Phil suggested an option where NUH set up a VM, put the Kubernetes cluster on the VM, and then FITFILE install their Node there - this is more achievable and something that NUH has done before and fits with the approvals already in place. This needs further discussion with John Baines and FITFILE.

### Identifying Key Stakeholders and Approval Process

- The group discussed the internal NHS approval process that would be required if for a Cloud deployment within the Trust - this would involve other key stakeholders and the process would take significantly longer than the current solution proposed by Phil and his team.
- Phil asked for clarity on what the SDE roles are regarding the usage of the data, i.e. who has access within the SDE and locally. Mark will set up a call with the SDE Data Managers to discuss further.
- Phil advised that NUH's Cyber team will need to assess how the SDE will process the data and sign-off on this (Andy Callow as risk owner) ahead of the SDE accessing any live data. The installation of the Node can proceed whilst this in being assessed.
- Helena confirmed that FITFILE have User Guides for the Data Provider and Data Controller which can be shared with NUH.
