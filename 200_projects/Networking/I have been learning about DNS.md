---
aliases: []
confidence:
created: 2025-10-25T17:44:39Z
epistemic:
last_reviewed:
modified: 2025-10-30T14:32:00Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [topic/technology/networking/dns]
title: I have been learning about DNS
type:
uid:
updated:
version:
---

## **Project Initiation Document: The Domain Name System**

This document outlines the plan for a new, scalable system to manage the correspondence between human-memorable computer hostnames and their network addresses.

### **1\. Problem Statement**

The current system of a centrally managed HOSTS.TXT file for mapping hostnames to ARPANET addresses is becoming increasingly unsustainable. The rapid growth in the number of connected hosts presents several critical challenges:

- **Scalability:** The single HOSTS.TXT file is a bottleneck. As the network expands, the file size grows, making its distribution and maintenance cumbersome and slow.  
- **Centralisation:** A single point of control for the entire namespace creates a single point of failure and an administrative burden. Any update requires a centralised process, leading to delays.  
- **Name Collisions:** Without a structured naming system, the likelihood of duplicate hostnames increases, causing confusion and routing errors.  
- **Static Nature:** The HOSTS.TXT file is a static record. It cannot dynamically reflect changes in host addresses without a manual update and redistribution of the file.

This project aims to replace the HOSTS.TXT file with a distributed, hierarchical, and dynamic system for name resolution.

### **2\. User Stories**

To address the shortcomings of the current system, the new Domain Name System (DNS) will cater to the needs of various users:

#### **As A Network User:**

- I want to be able to connect to a remote computer using a simple, memorable name instead of a complex numerical address, so that I can easily access network resources.  
- I expect the name-to-address lookup to be fast and reliable, so that my connection attempts are not delayed or unsuccessful.

#### **As A Network Administrator:**

- I want to be able to manage the names and addresses of the computers within my own organisation's network without needing to consult a central authority for every change, so that I have autonomy and can make updates efficiently.  
- I want a system that can handle a large and growing number of hosts without a degradation in performance, so that our network can scale effectively.  
- I want to be able to create sub-domains within my organisation's domain, so that I can logically structure our network resources.

#### **As An Application Developer:**

- I want a stable and programmatic way to resolve hostnames to network addresses, so that I can build applications that can reliably connect to other services on the network.  
- I want the system to be extensible, so that it can support future types of network information beyond just host-to-address mapping.

### **3\. Requirements**

To fulfil the user stories, the DNS will be built to the following specifications:

#### **Functional Requirements:**

- **Hierarchical Namespace:** The system will implement a hierarchical naming structure, with a root at the top and branching domains and sub-domains, to ensure unique names and logical organisation.  
- **Distributed Database:** The name and address data will be stored in a distributed manner across multiple servers. No single server will hold the entire database.  
- **Delegation of Authority:** The system will allow for the delegation of administrative control over portions of the namespace to different organisations.  
- **Name Resolution Protocol:** A client-server protocol will be defined to allow clients (resolvers) to query servers for name-to-address mappings.  
- **Record Types:** The system will support various record types, starting with 'A' records for address mapping, but with the flexibility to add new types in the future (e.g., for mail exchangers).  
- **Caching:** Resolvers will cache the results of queries for a specified period (Time to Live) to reduce network traffic and improve response times.

#### **Non-Functional Requirements:**

- **High Availability:** The system must be highly available, with no single point of failure. Redundancy will be built in through the use of multiple authoritative name servers for each domain.  
- **Low Latency:** Name resolution queries should be processed with minimal delay to ensure a responsive user experience.  
- **Scalability:** The system must be designed to scale to accommodate a global network of millions of hosts.  
- **Data Integrity:** Mechanisms will be in place to ensure that the data retrieved from a name server is accurate and has not been corrupted in transit.  
- **Interoperability:** The system will be based on open standards to ensure that different implementations can interoperate seamlessly.
