---
aliases: [MESH Firewall Rules, MESH Integration Guide, NHS MESH Sandbox]
created: 2026-02-01T15:30:00Z
modified: 2026-02-04T07:27:15+00:00
status: evergreen
tags: [ff_deploy, integration, mesh, nhs, sot]
title: SoT - NHS MESH Integration
type: SoT
---

## 1. Overview

The MESH Mailbox chart deploys a sandbox implementation of the NHS Message Exchange for Social Care and Health (MESH) service. This environment allows FITFILE to test secure healthcare data exchange without connecting to live NHS infrastructure.

Purpose:

- Integration testing for `fitconnect`.
- Validating FHIR/HL7 message formats.
- Simulating GP-to-Hospital data flows.

---

## 2. Infrastructure & Deployment

### 2.1 The Sandbox Application

- Image: `fitfileregistry.azurecr.io/mesh-mailbox-sandbox:latest`
- Port: 443 (HTTPS Only).
- Service Type: `ClusterIP` (Internal access only).
- Storage: Ephemeral (`/tmp/mailboxes`). No persistence in sandbox mode.

### 2.2 Configuration (Helm Values)

```yaml
env:
  AUTH_MODE: "none"        # Sandbox mode
  SHARED_KEY: "TestKey"    # Shared secret
  SSL: "yes"               # Mandatory
```

---

## 3. Firewall Requirements (Client-Side)

When connecting to the LIVE or INT NHS MESH infrastructure (not this sandbox), strict firewall rules apply.

### 3.1 Connectivity Options

| Connection Type | Domain | External IPs |
|:---|:---|:---|
| HSCN / N3 | `mesh-sync.national.ncrs.nhs.uk` | `155.231.48.156`, `155.231.48.220` |
| Internet | `mesh-sync.spineservices.nhs.uk` | Dynamic (Allow Hostname) |

### 3.2 Outbound Rules (Private Network -> NHS)

- Protocol: HTTPS (TLS 1.2+).
- Port: 443.
- Destinations:
  - `msg.intspineservices.nhs.uk` (Integration)
  - `msg.spineservices.nhs.uk` (Production)
- Constraint: Do NOT pin to fixed IPs for Internet connections; use DNS resolution.

### 3.3 Verification

```bash
# Test Connectivity
telnet mesh-sync.spineservices.nhs.uk 443
```

---

## 4. Operational Context

### Integration Strategy

This component sits alongside `fitconnect` in the `ffnode` umbrella chart. It simulates the external "NHS Endpoint" that `fitconnect` would normally talk to.

### NHS Digital References

- [MESH Client Installation Guidance](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/client-installation-guidance)
- [MESH API Catalogue](https://digital.nhs.uk/developer/api-catalogue/message-exchange-for-social-care-and-health-api)
