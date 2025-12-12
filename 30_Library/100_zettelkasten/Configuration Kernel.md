---
aliases: [Config Kernel, Minimal Config Input]
confidence: 0.8
created: 2025-01-15T10:01:00Z
epistemic: fact
last_reviewed: 2025-01-15
modified: 2025-11-12T14:24:42Z
purpose: Minimal declarative input set for infrastructure deployments
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [configuration, declarative, infrastructure]
title: Configuration Kernel
type: concept
uid: 2025-01-15T10:01:00Z
updated: 2025-01-15T10:01:00Z
---

## Configuration Kernel

**Summary:** The minimal set of variables a human operator should edit for a specific deployment, defining the intent rather than implementation details.

**Details:** A Configuration Kernel contains only essential deployment parameters such as application name, environment identifier, region, base domain, and business metadata. This small surface area makes configuration highly robust by reducing opportunities for typos and errors. The kernel serves as input to a Configuration Generator which derives all other configuration values automatically. Example kernel variables include `app_name`, `environment`, `aws_region`, `base_domain`, and `cost_centre`.
