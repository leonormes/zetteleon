---
aliases: []
confidence: 
created: 2025-09-03T04:36:15Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/kubernetes, topic/technology/networking]
title: MESH service firewall allowlist requirements
type:
uid: 
updated: 
version:
---

Here’s what you need for your firewall configuration depending on whether you’re connecting via **HSCN** or **Internet**:

## ✅ For HSCN / N3 Connection

- **Domain name**: `mesh-sync.national.ncrs.nhs.uk`
- **Port**: TCP 443
- **Protocol**: HTTPS (TLS)
- **External IPs**:
  - `155.231.48.156`
  - `155.231.48.220`
- **Purpose**: Used by the MESH client to send and receive messages

## ✅ For Internet Connection

- **Domain name**: `mesh-sync.spineservices.nhs.uk`
- **Port**: TCP 443
- **Protocol**: HTTPS (TLS)
- **Purpose**: Used by the MESH client to send and receive messages

You can verify access by running (on Windows Command Prompt or Linux terminal):

```sh
telnet mesh-sync.spineservices.nhs.uk 443
```

or for HSCN:

```sh
telnet mesh-sync.national.ncrs.nhs.uk 443
telnet 155.231.48.156 443
telnet 155.231.48.220 443
```

Full guidance here: [NHS Digital – MESH client installation firewall details](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/client-installation-guidance)

---

URLs / hostnames to allowlist

- MESH API catalogue pages (docs):
  - National Data Opt-out via MESH: [https://digital.nhs.uk/developer/api-catalogue/national-data-opt-out-service-mesh](https://digital.nhs.uk/developer/api-catalogue/national-data-opt-out-service-mesh)
  - MESH API: [https://digital.nhs.uk/developer/api-catalogue/message-exchange-for-social-care-and-health-api](https://digital.nhs.uk/developer/api-catalogue/message-exchange-for-social-care-and-health-api)
- MESH service endpoints (by environment):
  - Integration (INT): msg.intspineservices.nhs.uk
  - Production (LIVE): msg.spineservices.nhs.uk
  - Note: Your exact mailbox routes and any additional subdomains are confirmed during onboarding in the NHS England developer portal.

Firewall rules (outbound, from your private network)

- Protocols: HTTPS (TLS)
- Ports: 443
- Destination hostnames:
  - msg.intspineservices.nhs.uk (if you’re integrating/testing)
  - msg.spineservices.nhs.uk (if you’re live)
  - digital.nhs.uk (for documentation, not the runtime API)
- DNS: Allow normal DNS resolution for the above hostnames. Do not pin to fixed IPs; NHS guidance is to allowlist by hostname, not IP, as IPs may change [NHSmail firewall guidance](https://support.nhs.net/knowledge-base/nhsmail-firewall-and-proxy-server-access/).
- TLS: Permit outbound TLS 1.2+ to those hosts. You’ll be presenting an NHS-issued client cert for MESH API calls (per the MESH API onboarding).
