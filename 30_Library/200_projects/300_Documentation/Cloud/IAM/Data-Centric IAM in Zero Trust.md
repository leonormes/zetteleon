---
aliases: []
confidence: 
created: 2025-03-15T10:12:06Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [data-centric, IAM]
title: Data-Centric IAM in Zero Trust
type: 
uid: 
updated: 
version: 
---

From a data perspective, IAM in zero trust is about controlling access to data assets based on:

## Identity Data

Verifying the identity of users and devices attempting to access data. This involves managing data about users (employees, customers, partners), devices (laptops, servers, IoT devices), and services (applications, APIs).

## Contextual Data

Analysing the context of each access request. This includes data about:

### User Attributes

Role, department, security clearance, location, device posture.

### Resource Attributes

Data sensitivity, classification, compliance requirements, location.

### Environmental Attributes

Time of day, network conditions, threat intelligence feeds, anomaly detection signals.

## Policy Data

Enforcing access policies defined based on identity and context. Policies are essentially rules that dictate who can access what data under which conditions. Policy data includes:

## Authorization Rules

Defining allowed actions (read, write, execute, delete) on specific data assets.

## Authentication Requirements

Specifying the strength and type of authentication needed (multi-factor authentication, passwordless).

Auditing and logging configurations: Defining what access events to record for monitoring and compliance.

In essence, data is at the heart of zero trust IAM. It's not just about who is accessing what, but under what circumstances and with what level of assurance based on a rich dataset.

[[IAM from a Data Perspective in Zero Trust Networking and Security]]
