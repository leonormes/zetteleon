---
aliases: []
confidence: 
created: 2025-07-03T10:41:22Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: roles
type:
uid: 
updated: 
version:
---

## Subject: Urgent Security Review: Azure Role-Based Access for the FITFILE Project

To: [Relevant Contacts at CUH], [Relevant Contacts at Telefonica]

Cc: [Relevant Internal FITFILE Stakeholders]

Dear All,

I hope this email finds you well.

Following the successful setup of the Azure infrastructure by Telefonica and our initial deployment work, our team at FITFILE has conducted a standard security review of the Identity and Access Management (IAM) roles within our designated subscription.

Our review of the subscription (`709f3d57-b6d7-48c6-8252-6b1c1174a541`) has identified a critical issue that requires your immediate attention. We have found that a significant number of users have been granted highly privileged roles such as `Owner`, `Contributor`, and `User Access Administrator`. Crucially, these permissions are not scoped directly to specific resources but are inherited from broad assignments at the Subscription and Management Group levels.

While we understand the need for administrative access, the current configuration of permanent, standing-access roles presents a significant security risk. It deviates from the industry-standard principle of least privilege, which is fundamental to a robust security posture. With the current setup, FITFILE cannot adequately guarantee the security or integrity of the application environment we are responsible for deploying and managing. This broad access unnecessarily increases the attack surface and the risk of accidental or malicious configuration changes.

To address this, we strongly recommend implementing Azure Privileged Identity Management (PIM).

PIM is the modern standard for securing privileged access. It allows us to convert the current permanent roles into "eligible" assignments. This means administrators do not have standing access but can elevate their privileges on a "just-in-time" basis when a legitimate need arises, providing a justification that is fully audited. This approach drastically reduces risk while maintaining the necessary administrative agility for CUH and Telefonica teams.

To move forward, I would like to propose a meeting between all three parties to:

1. Discuss these findings in detail.
2. Agree on a remediation plan to transition from permanent roles to PIM-based eligible assignments.
3. Define the appropriate roles and groups required for ongoing administration.

We have a detailed report of the current role assignments that we can share and use as a basis for this discussion. Please let me know your availability next week to schedule this urgent meeting.

We look forward to working together to secure this environment to the highest standard.

Best regards,

Leon
