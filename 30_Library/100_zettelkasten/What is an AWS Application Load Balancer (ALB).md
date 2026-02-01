---
aliases: []
created: 2025-10-24T14:25:58Z
last_reviewed: ""
modified: 2026-02-01T15:08:23+00:00
status: ""
tags: ["aws", "load-balancing", "SoftwareEngineering/Networking", "SoftwareEngineering/networking/cloud-networking"]
title: What is an AWS Application Load Balancer (ALB)
type: ""
updated: 
---

An Application Load Balancer (ALB) is a type of load balancer in Amazon Web Services (AWS) that operates at the application layer (Layer 7) of the OSI model.

Its primary purposes include:

- Balanced Traffic Distribution: Distributes incoming application traffic across multiple targets, such as EC2 instances, containers, and IP addresses.
- Improved Performance: Enhances the performance of web applications by ensuring no single target is overloaded.
- Redundancy and High Availability: By distributing traffic across targets in different Availability Zones, ALBs provide fault tolerance and high availability for applications.
- Advanced Routing: Supports content-based routing, allowing requests to be routed to different target groups based on the content of the request (e.g., URL path, host header).

ALBs are ideal for microservices and container-based applications.

---

Related: Load Balancing Concepts, OSI Model - Layer 7 Application Layer
