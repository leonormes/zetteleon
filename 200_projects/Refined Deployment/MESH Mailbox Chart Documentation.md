---
aliases: []
confidence: 
created: 2025-09-19T11:30:30Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [chart, documentation, helm, mailbox, mesh]
title: MESH Mailbox Chart Documentation
type:
uid: 
updated: 
version:
---

## Overview

The **mesh-mailbox** chart deploys a sandbox implementation of NHS MESH (Message Exchange for Social Care and Health) mailbox service. This is a testing/development environment for the UK's national healthcare messaging system.

## What is NHS MESH

**MESH (Message Exchange for Social Care and Health)** is the UK's nationally recognized mechanism for secure data sharing between health and care organizations. It enables:

- **Secure file transfers** up to 50GB between healthcare organizations
- **System-to-system messaging** for automated healthcare workflows
- **Document exchange** in both human-readable (PDFs) and machine-readable formats (FHIR, CSV)
- **Message routing** with Workflow IDs for different message types
- **Reliable delivery** with acknowledgments and non-delivery reports

## What is Deployed

### Main Application

- **Container**: `fitfileregistry.azurecr.io/mesh-mailbox-sandbox:latest`
- **Purpose**: MESH mailbox sandbox for testing healthcare message exchange
- **Architecture**: Single replica deployment with HTTPS endpoint
- **Port**: 443 (HTTPS with SSL enabled by default)

### Service Configuration

- **Service Type**: ClusterIP (internal cluster access)
- **Protocol**: HTTPS/TLS encrypted communication
- **Health Check**: HTTP GET to `/health` endpoint
- **Authentication**: Configurable (default: "none" for sandbox)

## Key Features

### Security & Authentication

- **SSL/TLS**: Enabled by default (`ssl.enabled: true`)
- **Authentication Mode**: Configurable (`authMode: "none"` for sandbox)
- **Shared Key**: Test key for sandbox authentication (`sharedKey: "TestKey"`)
- **HTTPS Only**: All communication over port 443

### Resource Allocation

- **CPU**: 150m (minimal resource requirements)
- **Memory**: 256Mi
- **Replicas**: 1 (single instance for testing)
- **Revision History**: Limited to 1 (space optimization)

### Storage & Data

- **Mailbox Data Directory**: `/tmp/mailboxes` (ephemeral storage)
- **Purpose**: Temporary storage for message exchange testing
- **Persistence**: None (sandbox environment)

## Configuration Options

### Environment Variables

- **AUTH_MODE**: Authentication method (default: "none")
- **SHARED_KEY**: Shared authentication key (default: "TestKey")
- **SSL**: SSL/TLS enablement (default: "yes")
- **MAILBOXES_DATA_DIR**: Directory for mailbox data storage

### Image Configuration

- **Repository**: `fitfileregistry.azurecr.io/mesh-mailbox-sandbox`
- **Tag**: `latest`
- **Pull Policy**: Always (ensures latest sandbox version)
- **ACR Authentication**: Optional via `acrBasicAuth` flag

## Use Cases

### Development & Testing

- **MESH Integration Testing**: Test healthcare message exchange workflows
- **API Development**: Develop applications that integrate with MESH
- **Workflow Validation**: Validate message routing and delivery
- **Security Testing**: Test authentication and encryption mechanisms

### Healthcare Data Exchange

- **GP-to-Hospital**: Test patient data transfers
- **Lab Results**: Test pathology result delivery
- **Referrals**: Test patient referral workflows
- **Discharge Summaries**: Test hospital discharge communications

## Integration Context

### FITFILE Platform Integration

This sandbox enables FITFILE to:

- **Test MESH connectivity** before production deployment
- **Develop healthcare integrations** with NHS systems
- **Validate message formats** (FHIR, HL7, etc.)
- **Test workflow IDs** for different message types

### NHS Digital Ecosystem

- **Sandbox Environment**: Safe testing without affecting live NHS systems
- **Workflow ID Testing**: Test different healthcare message types
- **Directory Services**: Test mailbox lookup and routing
- **Delivery Tracking**: Test message acknowledgment and status reporting

## Important Notes

- **Sandbox Only**: This is NOT connected to live NHS MESH infrastructure
- **Testing Purpose**: For development and integration testing only
- **No Persistence**: Messages are not retained between pod restarts
- **SSL Required**: All communication must be over HTTPS
- **Health Monitoring**: Built-in health check endpoint for Kubernetes probes

This chart provides a safe, isolated environment for developing and testing healthcare message exchange integrations before connecting to the live NHS MESH infrastructure.

[[NeoMesh plans]]
