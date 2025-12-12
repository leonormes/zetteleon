---
aliases: []
confidence: 
created: 2025-10-07T09:40:06Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FFAPP-4153-Context
type:
uid: 
updated: 
version:
---

## FFAPP-4153: Discovery and Analysis of Bitnami Chart Replacements - Complete LLM Context

### Executive Summary

This document provides comprehensive context for Jira ticket FFAPP-4153, which involves identifying and researching replacements for all Bitnami Helm charts currently in use within the FITFILE platform infrastructure. This is a critical platform engineering initiative to improve security and automation capabilities.

### Ticket Details

#### Basic Information

- **Jira Key**: FFAPP-4153
- **Internal ID**: 20780
- **Project**: FITFILE Application (FFAPP)
- **Type**: Story
- **Status**: 🔵 In Progress
- **Priority**: ⚠️ Medium
- **Assignee**: Leon Ormes
- **Reporter**: Leon Ormes

#### Dates

- **Created**: September 4, 2025, 07:09:03 UTC
- **Last Updated**: October 7, 2025, 09:26:13 UTC
- **Time in Progress**: ~33 days

#### User Story

As a Platform Engineer, I want to identify all Bitnami charts currently in use and research suitable, vetted replacements, so that we can create a clear migration plan that meets our security and automation requirements.

### Key Stakeholder Feedback

#### Ollie Rushton's Comments (September 29, 2025)

Two critical discussion points were raised:

1. **ACR Import Strategy**: "To discuss whether we can just import `latest` as a specific version in our ACR."
   - This suggests exploring Azure Container Registry (ACR) as a solution for chart management
   - Question about versioning strategy for imported charts

2. **Dependency Scope**: "Also to discuss whether we need to review all dependencies on Bitnami which are not within our ACR."
   - Indicates there may be Bitnami dependencies outside the current ACR scope
   - Need to define the boundary of what needs to be migrated

### Related Work Context

#### Active Related Tickets

##### FFAPP-4166: Roll Out Validated Helm Chart Sources to Production

- **Status**: Ready
- **Purpose**: Production rollout of validated chart sources
- **Relationship**: This appears to be the next phase after discovery (4153)

##### FFAPP-4160: Implement and Test New Helm Charts in Staging

- **Status**: Ready
- **Purpose**: Testing new charts in staging environment
- **Relationship**: Testing phase for charts identified in discovery work

#### Completed Related Work

##### FFAPP-4175: EKS AMI Migration

- **Status**: Done
- **Context**: Migration of EKS nodes from Amazon Linux 2 to Bottlerocket/Amazon Linux 2023
- **Relevance**: Shows team's experience with infrastructure migrations

##### FFAPP-4181: TLS Configuration for Helm Charts

- **Status**: Done
- **Assignee**: Ollie Rushton
- **Context**: Modified ffcloud and fitconnect Helm charts for TLS support
- **Relevance**: Recent experience with chart modifications

### Technical Context

#### Platform Architecture

Based on related tickets and comments, the FITFILE platform includes:

- **Azure Container Registry (ACR)** for container/chart storage
- **Kubernetes/EKS** infrastructure
- **Helm Charts** for application deployment
- **Multiple environments**: Staging and Production
- **Core Applications**: ffcloud, fitconnect, The Hyve components

#### Security & Compliance Requirements

- Need for "vetted replacements" suggests security compliance requirements
- Automation requirements indicate DevOps/CI/CD integration needs
- Discussion of specific versions vs "latest" indicates version control compliance

### Business Impact

#### Risk Assessment

- **Security Risk**: Continued use of unvetted Bitnami charts
- **Operational Risk**: Dependency on external chart sources
- **Compliance Risk**: Potential audit/security review findings

#### Success Criteria

- Complete inventory of current Bitnami chart usage
- Identified vetted alternatives for each chart
- Clear migration plan with timelines
- Security and automation requirements met

### Action Items & Decisions Needed

#### Immediate Tasks (Based on Discovery Phase)

1. **Complete Inventory**: Catalog all Bitnami charts currently in use
2. **Dependency Mapping**: Identify charts inside vs outside ACR
3. **Research Alternatives**: Find vetted replacements for each chart
4. **Security Evaluation**: Assess security posture of alternatives

#### Strategic Decisions Required

1. **ACR Strategy**: Decide on importing `latest` as specific versions
2. **Scope Definition**: Determine boundary of migration effort
3. **Timeline**: Set migration deadlines
4. **Resource Allocation**: Assign team members to migration phases

#### Follow-up Tickets

- FFAPP-4160 (Testing) - Depends on discovery completion
- FFAPP-4166 (Production Rollout) - Final phase implementation

### Team Context

#### Key Personnel

- **Leon Ormes**: Platform Engineer, Primary assignee
- **Ollie Rushton**: Active contributor, raised key technical questions
- **Team Expertise**: Recent experience with EKS migrations and Helm chart modifications

#### Skills & Experience

- Kubernetes/EKS platform management
- Helm chart development and modification
- Azure Container Registry operations
- Infrastructure migrations
- Security compliance

### Current Status Assessment

#### Progress Indicators

- Ticket created September 4, 2025
- In Progress status for 33+ days
- Active stakeholder engagement (Ollie's comments)
- Related testing/rollout tickets in Ready status

#### Potential Blockers

- Scope clarification needed (ACR vs non-ACR dependencies)
- Technical decisions on versioning strategy
- Resource availability for comprehensive chart research

### CRITICAL DISCOVERY: Complete Bitnami Chart Inventory

#### Current Bitnami Usage Analysis (October 7, 2025)

Based on comprehensive analysis of the helm chart deployment directory:

##### **Primary Bitnami Charts (ArgoCD Managed)**

| Chart          | Version  | Source                                     | ACR             | Purpose                                               | Status |
| -------------- | -------- | ------------------------------------------ | --------------- | ----------------------------------------------------- | ------ |
| **MongoDB**    | 16.5.0   | <oci://registry-1.docker.io/bitnamicharts> | fitfileregistry | Primary NoSQL database for ffnode applications        | Locked |
| **PostgreSQL** | 12.12.10 | <oci://registry-1.docker.io/bitnamicharts> | fitfileregistry | Primary relational database                           | Locked |
| **MinIO**      | 12.13.2  | <oci://registry-1.docker.io/bitnamicharts> | fitfileregistry | Object storage for integration tests and applications | Locked |

##### **Secondary Bitnami Dependencies**

| Chart          | Usage Context            | Status  | Purpose                                   |
| -------------- | ------------------------ | ------- | ----------------------------------------- |
| **RabbitMQ**   | charts/hutch/values.yaml | Enabled | Message queue for hutch application       |
| **PostgreSQL** | charts/hutch/values.yaml | Enabled | Additional instance for hutch application |

##### **Technical Architecture Context**

**ACR Strategy Analysis:**

- **fitfileregistry**: Houses all Bitnami charts (mongodb, postgresql, minio)
- **fitfilepublic**: Houses non-Bitnami charts (argo-cd, ingress-nginx, vault-secrets-operator)
- All charts use locked versions via Chart.lock files
- OCI registry format: `oci://registry-1.docker.io/bitnamicharts`

**Chart Management Infrastructure:**

- **Existing Tool**: chart-manager utility already available
- **Config Location**: `scripts/chart-manager/config/helm_chart_list.yaml`
- **Capabilities**: Version checking, chart analysis, ACR import, security scanning (Trivy)
- **TFC Integration**: Connected to FITFILE-Platforms/global-version-manager workspace

#### Answer to Ollie's Key Questions

##### 1. "Import 'latest' as Specific Version in ACR"

**Current State**: All Bitnami charts use locked specific versions:

- MongoDB: 16.5.0 (locked April 8, 2025)
- PostgreSQL: 12.12.10 (locked April 8, 2025)
- MinIO: 12.13.2 (locked April 8, 2025)

**Strategy Decision Needed**:

- ✅ **Current Approach**: Specific versions provide stability and predictability
- 🤔 **Alternative**: Import 'latest' with specific version tagging could provide update flexibility
- 📋 **Recommendation**: Keep current approach until replacements are vetted

##### 2. "Review Dependencies not within ACR"

**Analysis Result**:

- ✅ All identified Bitnami charts ARE within ACR scope (fitfileregistry)
- ✅ Dependencies are properly managed via umbrella charts (databases, hutch)
- ✅ Scope is well-defined and contained within current infrastructure

#### Migration Readiness Assessment

##### **Infrastructure Ready**

- ✅ Chart management tooling exists
- ✅ ACR strategy defined
- ✅ Version locking in place
- ✅ Related tickets prepared (FFAPP-4160 staging, FFAPP-4166 production)

##### **Research Targets Identified**

1. **MongoDB Alternatives**: Azure Cosmos DB, MongoDB Atlas, Community MongoDB Operator
2. **PostgreSQL Alternatives**: Azure PostgreSQL Flexible Server, CrunchyData Postgres Operator, CloudNativePG
3. **MinIO Alternatives**: Azure Blob Storage with S3 compatibility, Rook/Ceph, SeaweedFS
4. **RabbitMQ Alternatives**: Azure Service Bus, Apache Kafka (Strimzi), NATS

### Recommended Next Steps

1. **✅ COMPLETED**: Comprehensive inventory of current Bitnami usage
2. **Strategy Meeting**: Address Ollie's questions with concrete data (answers provided above)
3. **Research Phase**: Begin systematic evaluation of replacement options for the 5 identified charts
4. **Migration Planning**: Develop detailed timeline leveraging existing FFAPP-4160/4166 tickets

---

**Document Generated**: October 7, 2025, 09:39 UTC
**Source**: Jira ticket FFAPP-4153 and related project context
**Last Ticket Update**: October 7, 2025, 09:26:13 UTC

**Jira Link**: [https://fitfile.atlassian.net/browse/FFAPP-4153](https://fitfile.atlassian.net/browse/FFAPP-4153)
