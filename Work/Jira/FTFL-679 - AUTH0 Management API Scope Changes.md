---
assignee: Leon Ormes
created: 2026-05-28T00:00:00+00:00
issuetype: Task
jira_id: '31912'
jira_key: FTFL-679
jira_url: https://fitfile.atlassian.net/browse/FTFL-679
labels: [auth0, infrastructure, security]
modified: 2026-07-20T16:33:31+00:00
permalink: llmeon/jira/ftfl-679-auth0-management-api-scope-changes
priority: High
reporter: Leon Ormes
status: To Do
tags: [auth0, fitfile, infrastructure, jira, security, task]
title: FTFL-679 - AUTH0 Management API Scope Changes
updated: 2026-05-28
---

## FTFL-679—[AUTH0] Management API Scope Changes - Connection Options

| Field | Value |
|---|---|
| Jira ID | [31912](https://fitfile.atlassian.net/browse/FTFL-679) |
| Status | To Do |
| Priority | High |
| Issue Type | Task |
| Assignee | Leon Ormes |
| Reporter | Leon Ormes |
| Labels | auth0, security, infrastructure |
| Created | 2026-05-28 |
| Updated | 2026-05-28 |

### Summary

Auth0 notice requiring Management API scope updates for connection options. Action required by July 27, 2026 to prevent production disruptions.

### Affected Tenant

- Fitfile-prod (Europe)

### Problem

From April 1 to May 24, the Fitfile-prod tenant received Management API requests to a connections endpoint with an access token missing the required connection options scopes.

Starting July 27, 2026:

- The `options` field will no longer be returned in responses
- Attempts to update connections will fail if the respective scopes are missing
- This is particularly impactful to CI/CD pipelines that automate tenant configuration

### Required Actions

1. Review Auth0 integrations for potential impacts (focus on CI/CD pipelines)
2. Audit tokens to identify required scope updates
3. Update scopes as needed
4. Switch tenants to the new behavior

### Background

At the end of 2024, Auth0 introduced new scopes for connection options and announced an end-of-life date of April 2025 for access without these scopes.

- Free tenants and dev/staging tenants were transitioned May–July 2025
- Remaining tenants (including Fitfile-prod) are now being transitioned in the final phase

### Useful Resources

- [Announcement: New Management API scopes required for connection options](https://community.auth.com/p/scope-changes)
- [Timelines: End-of-life Rollout](https://community.auth.com/p/scope-timelines)
- [Migration steps: Migrate to Management API Connection Options Scopes](https://community.auth.com/p/scope-migration)
