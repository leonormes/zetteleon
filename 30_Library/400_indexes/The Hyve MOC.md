---
aliases: []
confidence: 
created: 2025-10-23T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T17:14:02Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [data-harmonization, etl, moc]
title: The Hyve MOC
type: map
uid: 
updated: 
version:
---

## The Hyve Map of Content

This Map of Content (MOC) organizes all information related to **The Hyve**, which provides ETL (Extract, Transform, Load) capabilities for the FITFILE platform, primarily for harmonizing healthcare data into the OMOP Common Data Model using Apache Airflow.

### Core Documentation

- [[TheHyve Chart Documentation|TheHyve Chart Documentation]]: Detailed documentation of the Helm chart for The Hyve integration, which deploys an Apache Airflow container.

### Deployment & Configuration

- [[FFNode hie-prod-34 Configuration Architecture|FFNode hie-prod-34 Configuration Architecture]]: Shows how The Hyve is integrated into the `hie-prod-34` deployment as a separate ArgoCD application.
- [[FITFILE Secret Inventory|FITFILE Secret Inventory]]: Details the secrets required for The Hyve, including Airflow and database credentials.
- [[200_projects/Refined Deployment/ACR-Image-Audit|ACR Image Audit]]: Lists the container images related to The Hyve, such as `thehyve/fitfile_etl_container`.
- [[200_projects/Refined Deployment/ACR-Audit|ACR Audit]]: Provides a comprehensive audit of all container images, including those from The Hyve.

### Projects & Tickets

- [[Re-Container-update Cleaned Email Thread|FFAPP-4402 Email Thread]]: Discussion about updating The Hyve container to upload QA reports to an S3 bucket.
- [[300_tickets/prod-hie/FFAPP-4402/FFAPP-4406 - Prerequisites - HIE SDE Data Go Live|FFAPP-4406 Prerequisites]]: Prerequisites for the HIE SDE Data Go Live, including tasks related to The Hyve container.

### Meeting Notes & Decisions

- [[Critical Discussion Points and Decisions|Critical Discussion Points and Decisions]]: Mentions The Hyve's role in data harmonization and challenges with pharmacy data mapping.
- [[NNUH Deployment Project Summary & Meeting Preparation|NNUH Deployment Project Summary]]: Discusses the delay in pharmacy data integration and The Hyve's role.
- [[NNUH data meeting|NNUH Data Meeting]]: Details the discussion with The Hyve about transitioning from synthetic to live data.

### Visuals

- [[Excalidraw/Hyve golive.excalidraw|Hyve Go-Live Diagram]]: A visual representation of the go-live process for The Hyve.

### Optimization

- [[Azure Production Cost Optimization - FFAPP-4315|Azure Production Cost Optimization]]: Notes on optimizing The Hyve application, which is currently running constantly in production.
