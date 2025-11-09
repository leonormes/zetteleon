---
aliases: []
confidence: 
created: 2025-09-19T11:16:26Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [hyve]
title: TheHyve Chart Documentation
type:
uid: 
updated: 
version:
---

## Overview

The **thehyve** chart is a FITFILE integration that deploys an ETL (Extract, Transform, Load) container running **Apache Airflow** for healthcare data processing workflows. It's designed to work with **OMOP Common Data Model** databases for standardized healthcare data.

## What is Deployed

### Main Application

- **Container**: `fitfileregistry.azurecr.io/thehyve/fitfile_etl_container:0.3.2`
- **Framework**: Apache Airflow (LocalExecutor mode)
- **Components**:
  - **Airflow Webserver**: Web UI for workflow management (port 8080)
  - **Airflow Scheduler**: Background task scheduler
  - **Init Container**: Database initialization and admin user setup

### Architecture

- **Deployment Strategy**: Recreate (to avoid MultiAttachVolume errors)
- **Replica Count**: 1 (single instance)
- **Security Context**: Runs as user/group 50000:50000 (non-root)
- **Resource Allocation**:
  - Scheduler: 1-2 CPU, 16-24Gi memory
  - Webserver: 500m CPU, 512Mi memory

## Database Configuration - **YES, We Control PostgreSQL** ✅

### PostgreSQL Dependency

- **Chart Version**: postgresql 15.5.15 (from FITFILE ACR)
- **Controlled by FITFILE**: ✅ **YES** - We fully control the PostgreSQL deployment
- **Deployment**: Conditional via `postgresql.enabled: true` in values.yaml
- **Source**: `oci://fitfileregistry.azurecr.io/helm`
- **Management**: Deployed as a Helm dependency, managed by our infrastructure

### Database Connections

The application connects to **two separate databases**:

#### 1. OMOP Target Database

- **Purpose**: Healthcare data in OMOP Common Data Model format
- **Default Config**:
  - Username: `postgres`
  - Port: `5432`
  - Database: `ohdsi`
- **Connection**: Via `OMOP_TARGET_DB` environment variable
- **Secret Management**: Uses Kubernetes secrets for credentials

#### 2. Airflow Metadata Database

- **Purpose**: Airflow's internal metadata and workflow state
- **Default Config**:
  - Username: `airflow`
  - Port: `5432`
  - Database: `airflow`
- **Connection**: Via `AIRFLOW__CORE__SQL_ALCHEMY_CONN` environment variable
- **Secret Management**: Uses Kubernetes secrets for credentials

## Storage & Persistence

### Reports Volume

- **PVC Name**: `{release-name}-reports`
- **Mount Path**: `/tmp/reports` (both webserver and scheduler)
- **Default Size**: 1Gi
- **Access Mode**: ReadWriteOnce
- **Purpose**: Shared storage for ETL reports and outputs

### Log Volume

- **Type**: EmptyDir (ephemeral)
- **Mount Path**: `/opt/airflow/logs`
- **Size Limit**: 500Mi
- **Purpose**: Airflow task logs

## Key Features

### Airflow Configuration

- **Executor**: LocalExecutor (single-node processing)
- **RBAC**: Disabled (`AIRFLOW__WEBSERVER__RBAC: False`)
- **Examples**: Disabled (clean installation)
- **DAG Storage**: Serialized DAGs enabled
- **Config Exposure**: Enabled for debugging

### Security & Access

- **Service Account**: Auto-created with API credentials
- **Image Pull Secrets**: Configurable for private registries
- **Admin User**: Optional initialization with configurable credentials
- **Network Policy**: ClusterIP service (internal access)

### Ingress & Networking

- **Service Type**: ClusterIP
- **Port**: 8080
- **Ingress**: Optional (disabled by default)
- **Health Checks**: HTTP probes on root path (`/`)

## Use Case

This chart is designed for **healthcare data ETL workflows** using:

- **OMOP CDM**: Standardized healthcare data model
- **Apache Airflow**: Workflow orchestration and scheduling
- **FITFILE Platform**: Integration with FITFILE's healthcare data platform

The deployment enables data scientists and engineers to build, schedule, and monitor ETL pipelines that transform healthcare data into the OMOP Common Data Model format for analytics and research purposes.

**Answer to your question**: **Yes, we do control the PostgreSQL database** - it's deployed as a Helm chart dependency (postgresql 15.5.15) from our own ACR registry and is fully managed by our infrastructure.
