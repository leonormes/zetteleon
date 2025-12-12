---
aliases: []
confidence: 
created: 2025-10-24T14:25:58Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, load-balancing, topic/technology/networking, topic/technology/networking/cloud-networking]
title: What is an AWS Application Load Balancer (ALB)
type:
uid: 
updated: 
version:
---

An **Application Load Balancer (ALB)** is a type of load balancer in Amazon Web Services (AWS) that operates at the application layer (Layer 7) of the OSI model.

Its primary purposes include:

- **Balanced Traffic Distribution**: Distributes incoming application traffic across multiple targets, such as EC2 instances, containers, and IP addresses.
- **Improved Performance**: Enhances the performance of web applications by ensuring no single target is overloaded.
- **Redundancy and High Availability**: By distributing traffic across targets in different Availability Zones, ALBs provide fault tolerance and high availability for applications.
- **Advanced Routing**: Supports content-based routing, allowing requests to be routed to different target groups based on the content of the request (e.g., URL path, host header).

ALBs are ideal for microservices and container-based applications.

---

**Related:** Load Balancing Concepts, OSI Model - Layer 7 Application Layer
