---
aliases: []
confidence: 
created: 2025-03-10T11:29:51Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:50Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [IAM]
title: We have a small team of developers in a small comp
type: plan
uid: 
updated: 
version: 1
---

---

We Have a Small Team of Developers in a Small Company. There Are 6 Devs Who Make Changes to Code. I Am Trying to Create a Policy for Access to the Azure Tenant. We Currently Have Many Elevated Privileges. I Am Imagining Having a Root Identity That Is Essentially the Company and Not Tied to a Person as Such, Though the Company Owner Should Ultimately Control This One. I Want to Manage Everything via GitOps

Research a good plan for having the least privileged access for all with a break glass root id that is not used unless in an emergency. Then a terraform cloud, GitLab GitOps route for making any changes to any resources in our Azure tenant. Currently, 1 person has all the access and all the keys, and I don't like it. I want to move responsibility to a shared model where multiple people are involved in any changes to critical aspects of our tenant and deployments. Suggest a plan. Remove as much hierarchy as possible but make it safe and auditable via GitOps processes. I need a good well-supported access model for a small team, but that has to conform to lots of governance in the UK due to accessing NHS Patient data

Implementing a secure, auditable access model for Azure tenant management with NHS data compliance requires a layered approach combining identity governance, GitOps automation, and emergency protocols. Here's a consolidated plan based on Microsoft/Azure best practices and NHS data protection requirements:

![[Break-Glass Identity Architecture]]

![[Least Privilege Access Model]]

![[GitOps Automation Pipeline]]

![[NHS Data Compliance Controls]]

![[Team Access Protocol]]
