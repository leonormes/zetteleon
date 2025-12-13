---
aliases: []
author:
confidence: 
created: 2024-10-31T10:52:18Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source: "https://nhse-dsic.atlassian.net/wiki/spaces/DCSDCS/pages/1391133887/Messaging+Exchange+for+Social+Care+and+Health+MESH"
source_of_truth: []
status: 
tags: []
title: mesh_capabilities_and_standards_guide
type:
uid: 
updated: 
version:
---

## MESH Capabilities and Standards Guide

- 1
- 2
- 2.1
- 2.2
- 3
- 3.1
- 4
- 5
- 6

### Introduction

The Message Exchange for Social Care and Health (MESH) is a centralised message transfer service provided by The Authority using the Spine Services Core infrastructure. This allows the service to benefit from the large-scale reliability of the Spine Services including its disaster recovery Capabilities and established service support.

The service supports the secure transfer of both clinical and business data flows between NHS Organisations and affiliated organisations. Sending organisations generate messages and “post” them to the central service from where they can then be “collected” by the recipient organisation. The principle of message transfer is “store and retrieve”. MESH is generally provided to end sites as part of Supplier provided Solutions although organisations can manage their interactions with the service directly themselves.

Information and technical documentation on use of the service can be found on The Authority’s website

An on-line message tracking service is provided to enable Suppliers, end-sites and support organisations to trace messages. This Message On-line Enquiry Service (MOLES) supports the tracking of messages as they are transferred across the service in near real-time. Information on MOLES and its use are provided

### Requirements

<table><colgroup><col><col><col></colgroup><tbody><tr><th rowspan="1" colspan="1"><div><h4>ID</h4></div></th><th rowspan="1" colspan="1"><div><h4>Requirement</h4></div></th><th rowspan="1" colspan="1"><div><h4>Level</h4></div></th></tr></tbody></table>

<table><colgroup><col><col><col></colgroup><tbody><tr><th rowspan="1" colspan="1"><div><h4>ID</h4></div></th><th rowspan="1" colspan="1"><div><h4>Requirement</h4></div></th><th rowspan="1" colspan="1"><div><h4>Level</h4></div></th></tr><tr><td rowspan="1" colspan="1"><p>MR2.4.04</p></td><td rowspan="1" colspan="1"><p><strong>MESH Client</strong></p><p>Each new release of the MESH Client&nbsp;<strong>MUST</strong>&nbsp;be installed within 6 months of notification of its release by the MESH Service Team.&nbsp;Any mandatory functional or non-functional changes to any part(s) of the system that are required to be made in order to implement a new release&nbsp;<strong>MUST</strong>&nbsp;also be Deployed along with the new Client.</p></td><td rowspan="1" colspan="1"><p>MUST</p></td></tr></tbody></table>

### Messaging Architecture

MESH supports the transfer of data between organisations using the principle of “store and retrieve”. It utilises a mailbox-based messaging architecture. All registered endpoints have a mailbox. That mailbox can support the transfer and receipt of many different message types. Messages are uploaded and stored on the Central MESH Server from where they are then collected.

The service is agnostic in respect of the types of message payload that it can transfer. This includes the full range of potential data transfers from fully structured, such as FHIR, XML, EDIFACT etc to plain text. Message transfers must however comply with the published

MESH supports the transfer of individual transfers up to 100MB in its standard form. It can support file transfers up to 20GB. To support transfers of this size (up to 20GB) an additional attribute is simply added for the specific transfer which informs the service to adopt a chunking process for that specific transfer.

MESH supports the transfer of data between organisations. It does NOT provide confirmation that end applications within those organisations are able to consume and appropriately process those transfers once they are collected from MESH. The service does record robust recording on transfers as they are transferred across the service, including error logging and non-collected reports. The readiness of end applications to consume message transfers is beyond the scope of MESH and is the responsibility of individual programmes, the standards they adopt and business rules and notifications that they define.

The [Interoperability Toolkit (ITK)](https://nhse-dsic.atlassian.net/wiki/spaces/DCSDCS/pages/1391133906 "https://nhse-dsic.atlassian.net/wiki/spaces/DCSDCS/pages/1391133906") does address the MESH issues in respect of reliable messaging. It is not the only approach but implementations requiring this can develop in accordance with the ITK.

### Connection Methods

Access to MESH can be requested by submission of the appropriate

There are 3 methods for connection to MESH, these are;

1. MESH User Interface (UI)
2. Accessed via Spine Portal (web-enabled)
3. Central configuration by NHS Digital
4. Aimed at Low Tech End-Points (entry level)
5. Smartcards required (2-factor authentication possible as alternative)
6. Administrators in local organisations manage access
7. MESH Client
8. Java-based client provided by NHS Digital (utilises the API)
9. Supports interfacing with end applications
10. Can be run as a service
11. Controlled access to MESH with some level of local config
12. Local Installation/development
13. Aimed at Suppliers and Technical Organisations
14. MESH Application Interface (API)
15. Allows integration to end applications
16. High level of control
17. Assurance Process must be completed
18. Local Installation/development
19. Aimed at Suppliers and Technical Organisations

The majority of the connections to MESH are currently supported by the MESH client. The expectation is that Suppliers and organisations will develop Solutions using the MESH client or the API. The choice of connection method is not prescribed by The Authority. The choice may be made based on the level of control or integration that Suppliers or organisations may prefer in their interaction with the service.

The MESH UI provides entry-level access to the service where there is little local support or Supplier involvement. It allows end users, individually or in teams, rather than end applications to interact with the MESH. This extends the use of MESH from pure application to application only.

If mandated Suppliers must use MESH in accordance to individual interface specifications.

### Compliance, Assurance and Testing

Requirements for compliance and assurance on MESH are dependent on the type of connection to the service. The only use of the MESH API requires the completion of a compliance and assurance process. This is managed directly with The Authority Solutions Assurance Team. The process is relatively “light touch” and includes the completion of a Target Operating Model (TOM).

Technical documentation in respect of the MESH API can be obtained by contacting the MESH Service Team ([mesh@nhs.net](https://nhse-dsic.atlassian.net/ "mailto:mesh@nhs.net")). The documentation is not published on the website to allow engagement, discussion and management of Suppliers or organisations considering the use of the MESH API to connect to the service.

Access to the Solution Assurance team will be gained as part of the

### Environments

MESH is a centralised message transfer service provided by The Authority using the Spine Services Core infrastructure. It therefore is supported on all of the Path to Live (PTL) environments.

### Documentation

Technical documentation and file downloads are hosted at the [MESH download page](https://digital.nhs.uk/message-exchange-social-care-health/downloads "https://digital.nhs.uk/message-exchange-social-care-health/downloads").

### Dependencies

There may be dependencies for implementing this Standard, however, there are no Interoperability Standards within the Capabilities and Standards model that are dependents.

### Roadmap

<table><tbody><tr><th rowspan="1" colspan="1"><div><p><strong>Items on the Roadmap which impact or relate to this Standard</strong></p></div></th></tr></tbody></table>

<table><colgroup><col></colgroup><tbody><tr><th rowspan="1" colspan="1"><div><p><strong>Items on the Roadmap which impact or relate to this Standard</strong></p></div></th></tr><tr><td rowspan="1" colspan="1"><div><table><thead><tr><th>Roadmap Item</th></tr></thead><tbody><tr><td>No content found</td></tr></tbody></table></div></td></tr></tbody></table>
