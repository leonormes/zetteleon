---
aliases: []
confidence: 
created: 2025-09-29T12:31:39Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [cost, FFAPP-4315, ffnode, project/work/fitfile]
title: Your cost is forecasted to exceed its threshold value for your Azure budget, PROD
type:
uid: 
updated: 
version:
---

[[2025-09-29]]

Looking across our entire Azure estate, our biggest costs are in virtual machine usage and backups:

![[image001-1.png]]

We are currently under utilising the VMs we deploy in a few ways:

- We can look into adjusting the resource limits by each application we run inside each node to reduce cpu and memory.
- We can remove applications that we may no longer need:
- Primary care node in production – this is not used at all currently. If we remove it, we will stop syncing STG data, but we can also ask for a full dump from EMIS when the project comes back to life.
- We are running The Hyve application in production constantly, but it only needs to be running when we get updates to synthetic data
- We can turn off Kubernetes clusters outside of operational hours – testing and staging clusters do not need to run over the weekend for instance or at night
- What is in the operational window for Barts?
- We can scale the Workflows Node Pools (where data pipelines run) down to a minimum of 0 nodes – this means queries will be slower to start as a VM will need to be deployed when they run.

As for backups, we can investigate reducing the frequency of the backups and the retention period of the backups. Perhaps we can look at reducing what is actually backed up (we currently backup the whole cluster, but I think we only need the PVs backed up).

The work would need to be refined further and prioritised alongside the current commitments we have, so perhaps I can raise this with Weronika to add to the roadmap, and we can bring this up in our Wednesday meeting.

Kind regards,

Ollie

![[Screenshot 2025-09-29 at 12.32.24.jpg]]
