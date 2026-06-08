---
aliases: []
created: 2025-03-26T13:03:43Z
last_reviewed: ""
modified: 2026-05-26T11:44:24+00:00
see_also: []
status: ""
superseded_by: ""
supersedes: ""
tags: []
title: Integrate Security into the Workflow (Shift Left)
type: ""
updated: 
project_category: development
project_status: archived
project_name: "Core"
---

Make security part of the process, not an afterthought.

## Security in Design/Planning

- Bring up security considerations during design discussions for new features. Ask: "How could this feature be abused? What are the security risks? How can we mitigate them from the start?"
- Use your threat modeling insights here.

## Security Tools in the CI/CD Pipeline

- Automate security checks as much as possible:
  - SAST (Static Application Security Testing): Analyzes source code for vulnerabilities. Many tools integrate with IDEs and CI pipelines.
  - SCA (Software Composition Analysis): Checks third-party dependencies for known vulnerabilities. Crucial, as many breaches exploit vulnerable libraries.
  - Secrets Scanning: Prevents accidental commits of API keys, passwords, etc.
  - IaC (Infrastructure as Code) Scanning: Checks Terraform/CloudFormation/etc. for insecure configurations.
- Configure these tools to provide feedback _early_ and _automatically_. Developers are more likely to fix issues found immediately than those discovered weeks later.

## Security Focus in Code Reviews

- Make security an explicit part of the code review checklist or discussion. Ask reviewers to specifically look for common security flaws (input validation, proper authentication/authorization checks, secure handling of sensitive data).
- As the security-focused person, pay extra attention to this during your reviews and provide constructive feedback.

## Secure Defaults and Templates

- Provide secure base configurations, Docker images, or project templates. Make the secure way the easy way.

[[Make the Threat Real and Relevant]]
