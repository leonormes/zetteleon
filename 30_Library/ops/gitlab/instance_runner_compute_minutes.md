---
created: 2026-05-16T10:16:41+00:00
description: Compute minutes, purchasing, usage tracking, quota management for instance runners on GitLab.com and GitLab Self-Managed.
group: Pipeline Execution
info: To determine the technical writer assigned to the Stage/Group associated with this page, see <https://handbook.gitlab.com/handbook/product/ux/technical-writing/#assignments>
modified: 2026-05-26T11:44:06+00:00
stage: Verify
title: instance_runner_compute_minutes
---

{{< details >}}

- Tier: Free, Premium, Ultimate
- Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated

{{< /details >}}

The amount of compute minute usage that projects can consume to run jobs on admin-managed [instance runners](../runners/runners_scope.md#instance-runners)

is limited. This limit is tracked with an instance runner compute quota on the GitLab server. When a namespace exceeds quota, the [quota is enforced](#enforcement).

Admin-managed instance runners are those [managed by the GitLab instance administrator](../../administration/cicd/compute_minutes.md).

> [!note]
> On GitLab.com instance runners are both admin-managed and GitLab-hosted because the instance is managed by GitLab.

## Compute Quota Enforcement

### Monthly Reset

Compute minutes usage is reset to `0` monthly.

The compute quota is [reset to the monthly allocation](https://about.gitlab.com/pricing/).

For example, if you have a monthly quota of 10,000 compute minutes:

1. On April 1 you have 10,000 compute minutes available.
2. During April, you use 6,000 of the 10,000 compute minutes available in the quota.
3. On May 1, the accumulated compute usage resets to 0, and you have 10,000
   compute minutes available for May.

Usage data for the previous month is kept to show a historical view of the consumption over time.

### Notifications

An in-app banner is displayed and an email notification sent to the

namespace owners when the remaining compute minutes is:

- Less than 25% of the quota.
- Less than 5% of the quota.
- Completely used (zero minutes remaining).

### Enforcement

When the compute quota is used for the current month, instance runners stop processing new jobs.

In pipelines that have already started:

- Any pending job (not yet started) or retried job that must be processed by instance runners is dropped.
- Jobs running on instance runners can continue to run until the overall namespace usage goes over-quota
  by 1,000 compute minutes. After the 1,000 compute minute grace period, any remaining running jobs
  are also dropped.

Project and group runners are not affected by the compute quota and continue processing jobs.

## View Usage

You can view the compute usage (including [additional minutes](../../subscriptions/gitlab_com/compute_minutes.md)) for a group or personal namespace to understand

compute usage trends and how many compute minutes remain.

In some cases, the quota limit is replaced by one of the following labels:

- Unlimited: For namespaces with unlimited compute quota.
- Not supported: For namespaces where instance runners are not enabled.

### View Usage for a Group

Prerequisites:

- You must have the Owner role for the group.

To view compute usage for your group:

1. In the top bar, select Search or go to and find your group. The group must not be a subgroup.
2. Select Settings > Usage quotas.
3. Select the Pipelines tab.

The projects list shows projects with compute usage or instance runners usage

in the current month only. The list includes all projects in the namespace and its

subgroups, sorted in descending order of compute usage.

### View Usage for a Personal Namespace

You can view the compute usage for your personal namespace:

1. In the upper-right corner, select your avatar.
2. Select Edit profile.
3. In the left sidebar, select Usage quotas.

The projects list shows [personal projects](../../user/project/working_with_projects.md)

with compute usage or instance runners usage in the current month only.
