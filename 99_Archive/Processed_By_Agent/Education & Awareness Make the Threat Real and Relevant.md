---
aliases: []
confidence: ""
created: 2025-03-26T13:03:42Z
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:49:51+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: []
title: Education & Awareness Make the Threat Real and Relevant
type: ""
uid: 
updated: 
version: ""
---

People need to understand _why_ it matters _to them_ and _to this project_.

## Threat Modelling as a Team Exercise

- Don't do this in isolation. Schedule regular, short sessions (maybe once a sprint or month) where the _whole team_ brainstorms potential threats to _your specific system_.
- Use frameworks like STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) but keep it practical. Ask questions like:
  - "What are the most valuable assets in our system?" (e.g., Patient PII, medical records, access keys)
  - "Who might want to attack us and why?" (e.g., Ransomware groups, individuals seeking specific data, disgruntled insiders)
  - "How could they try to get in _given our current architecture/codebase_?" (Focus on APIs, databases, cloud configurations, dependencies)
  - "What would be the impact if they succeeded?"
- This collaborative process makes threats less abstract and fosters shared ownership.

## Real-World Healthcare Breach Case Studies

- Find examples of security breaches in the healthcare sector. Discuss:
  - _How_ the breach occurred (e.g., misconfigured cloud storage, vulnerability in a dependency, phishing, weak authentication).
  - _What_ the consequences were (e.g., massive fines under GDPR/HIPAA, reputational damage, lawsuits, patient harm, mandatory disclosures, operational disruption).
  - _How_ similar vulnerabilities might exist in your own system.
- Hearing about concrete failures and their severe fallout in your specific industry can be a powerful motivator.

## Focused Training Snippets

- Instead of generic security awareness training, focus on relevant topics.
- Dedicate 15-30 minutes in a team meeting to cover:
  - A specific OWASP Top 10 vulnerability (e.g., Injection, Broken Access Control) with code examples _in your language/framework_.
  - Secure coding practices for a feature you are _currently building_.
  - Best practices for the specific cloud services you use (e.g., IAM policies, security group configurations, secret management).
- Keep it short, practical, and immediately applicable.

[[Make the Threat Real and Relevant]]
