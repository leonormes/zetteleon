---
aliases: []
author:
confidence: 
created: 2024-10-31T10:55:36Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source: "https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh"
source_of_truth: []
status: 
tags: []
title: mesh_data_sharing_guide
type:
uid: 
updated: 
version:
---

## MESH Data Sharing Guide

Message Exchange for Social Care and Health (MESH) provides the ability to share data directly between health and care organisations and is the nationally recognised mechanism for this method of data sharing.

---

### About This Service

Message Exchange for Social Care and Health (MESH) provides the ability to share data directly between health and care organisations and is the nationally recognised mechanism for this method of data sharing.

MESH can be used to:

- transfer large files (up to 50GB) securely from one organisation to another
- send a file to someone's GP, using their NHS number and other details
- send documents, in human-readable formats such as PDFs, or machine-readable structured messages, such as FHIR messages, CSV files or binary files

---

### Who the Service is for

MESH enables any health and social care organisations, including both frontline and backend services, to send and receive messages.

MESH provides two modes of data transfer:

System to system – MESH can be directly integrated into point-of-care applications, using either a client or an [Application Programming Interface (API)](https://digital.nhs.uk/developer/guides-and-documentation/introduction-to-healthcare-technology/integration-and-apis#apis).

User interface – a web-based service for ad hoc transfers of smaller messages.

MESH is used across the UK and is also available for non-UK cases to transfer data across Health and Care organisations.

---

### National Usage Policy

MESH provides the ability to share data directly with other organisations and we recommend its use in this context.

---

### Examples of Use

You can use MESH to send messages of any type, for many reasons.

#### Support For Direct Care

- send and receive vaccination data to NHS and supplier systems
- send machine readable pathology reports securely and reliably to GP Systems
- receive reliable data that ensure patients record are updated correctly

#### Large Data Transfers

- send datasets to NHS England
- receive a list of NHS numbers from the national data opt-out programme

For a full list of nationally-defined messages, visit our API catalogue, filtered to show [MESH integrations](https://digital.nhs.uk/developer/api-catalogue?filter=mesh).

---

### How This Service Works

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" content="<mxfile host=&quot;nhsd-confluence.digital.nhs.uk&quot; modified=&quot;2023-07-19T12:31:29.175Z&quot; agent=&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36&quot; etag=&quot;EEmk-zYYXy-CfdwyxaAV&quot; version=&quot;21.2.1&quot; type=&quot;atlas&quot;><diagram id=&quot;bu3Qk-5sr2d5vccLCwXj&quot; name=&quot;Page-1&quot;>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</diagram></mxfile>" height="347" version="1.1" viewBox="-0.5 -0.5 602 347" width="602"><defs></defs><g><path d="M 232.76 195.01 C 232.76 186.72 258.82 180.01 290.96 180.01 C 306.39 180.01 321.19 181.59 332.11 184.4 C 343.02 187.21 349.15 191.03 349.15 195.01 L 349.15 279.14 C 349.15 287.43 323.1 294.14 290.96 294.14 C 258.82 294.14 232.76 287.43 232.76 279.14 Z" fill="#f0f6fa" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="4"></path><path d="M 349.15 195.01 C 349.15 203.29 323.1 210.01 290.96 210.01 C 258.82 210.01 232.76 203.29 232.76 195.01" fill="none" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="4"></path><g transform="translate(-0.5 -0.5)"><switch><foreignObject height="100%" pointer-events="none" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;" width="100%"></foreignObject><text fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="20px" font-weight="bold" text-anchor="middle" x="291" y="256">MESH</text> </switch></g><rect fill="#0072ce" height="100" pointer-events="none" stroke="#0072ce" stroke-width="3" width="117.89" x="7.75" y="190.17"></rect><g transform="translate(-0.5 -0.5)"><switch><foreignObject height="100%" pointer-events="none" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;" width="100%"></foreignObject><text fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="14px" text-anchor="middle" x="67" y="244"></text></switch></g><g transform="translate(-0.5 -0.5)"><switch><foreignObject height="100%" pointer-events="none" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;" width="100%"></foreignObject><text fill="#FFFFFF" font-family="Helvetica" font-size="12px" text-anchor="middle" x="71" y="212">Supplier systems</text></switch></g><path d="M 39.19 278.99 L 39.19 234.15 C 39.19 232.41 41.17 231.01 43.61 231.01 L 70.35 231.01 C 72.44 231.31 73.93 232.63 73.89 234.15 L 74.03 252.46 L 74.03 258.43 L 63.72 258.43 C 61.11 258.63 59.01 260.04 58.56 261.88 L 58.56 265.33 L 46.04 265.33 L 46.04 267.32 L 58.56 267.32 L 58.56 271.41 L 46.04 271.41 L 46.04 273.5 L 58.56 273.5 L 58.56 278.99 Z M 67.4 239.27 L 67.4 237.08 L 46.12 237.08 L 46.12 239.27 Z M 61.66 262.56 C 61.66 261.43 62.93 260.5 64.53 260.47 L 104.09 260.47 L 104.09 283.13 L 61.66 283.13 Z M 84.49 259.21 L 89.87 255.71 L 101.66 255.71 C 102.86 255.84 103.83 256.48 104.09 257.33 L 104.09 259.21 Z" fill="#fcfcfc" pointer-events="none" stroke="none"></path><path d="M 149.23 230.94 Q 149.23 230.94 206.61 230.94" fill="none" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><path d="M 142.48 230.94 L 151.48 226.44 L 149.23 230.94 L 151.48 235.44 Z" fill="#0072ce" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><path d="M 213.36 230.94 L 204.36 235.44 L 206.61 230.94 L 204.36 226.44 Z" fill="#0072ce" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><rect fill="#0072ce" height="90" pointer-events="none" stroke="#0072ce" stroke-width="3" width="220.53" x="178.39" y="5.03"></rect><g transform="translate(-0.5 -0.5)"><switch><foreignObject height="100%" pointer-events="none" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;" width="100%"></foreignObject><text fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="14px" text-anchor="middle" x="289" y="54"></text></switch></g><g transform="translate(-0.5 -0.5)"><switch><foreignObject height="100%" pointer-events="none" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;" width="100%"><div data-drawio-colors="color: #FFFFFF; " style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 212px; height: 1px; padding-top: 15px; margin-left: 181px;" xmlns="http://www.w3.org/1999/xhtml"><p><b style=""><span style="font-size: 12px;">Point-of-care applications</b></p></div></foreignObject><text fill="#FFFFFF" font-family="Helvetica" font-size="12px" text-anchor="middle" x="286" y="18">Point-of-care applications</text> </switch></g><path d="M 352.06 30.71 C 352.71 30.71 353.28 30.29 353.28 29.75 C 353.28 29.01 352.58 28.73 352.14 28.73 C 351.4 28.73 350.89 29.2 350.89 29.74 C 350.89 30.3 351.52 30.71 352.06 30.71 Z M 374.63 79.93 L 374.63 33.65 L 329.56 33.65 L 329.56 79.93 Z M 352.08 85.85 C 353.58 85.85 354.46 84.79 354.46 83.92 C 354.46 82.78 353.42 81.92 352.04 81.92 C 350.7 81.92 349.72 82.9 349.72 83.83 C 349.72 85.03 350.86 85.85 352.08 85.85 Z M 330.55 87.82 C 328.32 87.82 326 86.12 326 83.94 L 326 29.71 C 326 27.68 328.02 25.78 330.69 25.78 L 373.51 25.78 C 376.12 25.78 378.19 27.68 378.19 29.62 L 378.19 83.86 C 378.19 86 376.13 87.82 373.43 87.82 Z" fill="#ffffff" pointer-events="none" stroke="none"></path><rect fill="#0072ce" height="33.94" pointer-events="none" stroke="none" width="21.85" x="187.57" y="41.71"></rect><path d="M 244.87 66.6 L 244.87 35.35 C 245.31 34.32 246.26 33.59 247.38 33.43 L 301.33 33.43 C 302.7 33.58 303.82 34.58 304.12 35.92 L 304.12 66.6 L 309.83 72.78 C 310.08 73.55 309.84 74.35 309.16 75 C 308.49 75.64 307.44 76.07 306.26 76.19 L 242.73 76.19 C 241.54 76.09 240.47 75.66 239.78 75.01 C 239.09 74.36 238.84 73.55 239.09 72.78 Z M 247.23 66.6 L 301.97 66.67 L 301.97 36.56 C 301.71 35.8 301.05 35.26 300.26 35.14 L 248.66 35.14 C 247.88 35.41 247.32 36.1 247.23 36.91 Z M 268.96 70.79 L 267.03 73.56 L 280.46 73.56 L 278.96 70.79 Z" fill="#ffffff" pointer-events="none" stroke="none"></path><path d="M 212.83 42.53 C 213.03 42.53 213.12 42.45 213.12 42.27 C 213.12 42.11 213.01 42.01 212.83 42.01 L 208.19 42.01 C 207.99 42.01 207.93 42.17 207.93 42.27 C 207.93 42.38 208.04 42.53 208.19 42.53 Z M 218.7 67.5 L 218.7 45.18 L 202.34 45.18 L 202.34 67.5 Z M 210.54 71.8 C 211.11 71.8 211.97 71.4 211.97 70.47 C 211.97 69.82 211.33 69.22 210.54 69.22 C 209.66 69.22 209.08 69.88 209.08 70.47 C 209.08 71.39 209.93 71.8 210.54 71.8 Z M 202.29 73.5 C 200.83 73.5 199.46 72.5 199.46 70.94 L 199.46 42.61 C 199.46 41.18 200.7 40.03 202.31 40.03 L 218.55 40.03 C 220.28 40.03 221.49 41.28 221.49 42.57 L 221.49 70.92 C 221.49 72.6 219.97 73.5 218.7 73.5 Z" fill="#ffffff" pointer-events="none" stroke="none"></path><path d="M 290.29 159.97 L 290.63 149.07 L 290.13 117.19" fill="none" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><path d="M 290.08 166.71 L 285.86 157.58 L 290.29 159.97 L 294.86 157.86 Z" fill="#0072ce" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><path d="M 290.03 110.44 L 294.67 119.37 L 290.13 117.19 L 285.67 119.51 Z" fill="#0072ce" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><rect fill="#0072ce" height="101.11" pointer-events="none" stroke="#0072ce" stroke-width="3" width="122.84" x="456.47" y="188.05"></rect><g transform="translate(-0.5 -0.5)"><switch><foreignObject height="100%" pointer-events="none" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;" width="100%"></foreignObject><text fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="14px" text-anchor="middle" x="518" y="243"></text></switch></g><g transform="translate(-0.5 -0.5)"><switch><foreignObject height="100%" pointer-events="none" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;" width="100%"></foreignObject><text fill="#FFFFFF" font-family="Helvetica" font-size="12px" text-anchor="middle" x="518" y="215">Health and care worke...</text> </switch></g><path d="M 491.62 267.2 C 490.06 267.2 488.79 266.15 488.79 264.85 L 488.79 239.04 C 488.79 237.74 490.06 236.68 491.62 236.68 L 542.42 236.68 C 543.16 236.68 543.88 236.93 544.41 237.37 C 544.94 237.81 545.24 238.41 545.24 239.04 L 545.24 248.91 C 544.06 248.66 542.85 248.58 541.64 248.68 L 541.64 239.62 L 492.32 239.62 L 492.32 264.14 L 532.82 264.14 C 530.73 264.81 528.97 265.87 527.74 267.2 L 523.37 267.2 C 522.93 268.26 522.74 269.37 522.8 270.49 C 523.17 271.61 524.37 272.4 525.76 272.43 C 525.52 273.56 525.35 274.7 525.27 275.84 L 501.92 275.84 C 501.09 275.65 500.53 275.03 500.53 274.31 C 500.53 273.6 501.09 272.98 501.92 272.78 C 503.82 272.85 505.74 272.8 507.63 272.61 C 508.66 272.5 509.64 272.15 510.45 271.61 C 511.07 271.08 511.36 270.34 511.23 269.61 C 511.15 268.79 510.94 267.97 510.59 267.2 Z M 542.56 264.79 C 538.35 264.68 535.01 261.47 535.01 257.56 C 535.07 253.68 538.4 250.55 542.56 250.44 C 544.64 250.37 546.67 251.09 548.18 252.42 C 549.7 253.76 550.57 255.61 550.6 257.56 C 550.6 259.52 549.74 261.4 548.23 262.77 C 546.71 264.13 544.66 264.86 542.56 264.79 Z M 527.25 279.08 C 527.53 276.33 527.98 273.61 528.59 270.9 C 528.88 269.21 530.04 267.71 531.76 266.79 L 535.01 265.14 C 535.6 265.03 536.21 265.14 536.7 265.44 C 538.27 266.79 540.57 267.58 543 267.61 C 545.43 267.65 547.76 266.92 549.4 265.61 C 550.06 265.3 550.86 265.3 551.52 265.61 L 555.26 267.49 C 556.12 268.15 556.78 268.98 557.16 269.9 C 557.98 272.93 558.59 275.99 559 279.08 Z" fill="#ffffff" pointer-events="none" stroke="none"></path><path d="M 372.17 232.48 Q 372.17 232.48 429.55 232.48" fill="none" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><path d="M 365.42 232.48 L 374.42 227.98 L 372.17 232.48 L 374.42 236.98 Z" fill="#0072ce" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><path d="M 436.3 232.48 L 427.3 236.98 L 429.55 232.48 L 427.3 227.98 Z" fill="#0072ce" pointer-events="none" stroke="#0072ce" stroke-miterlimit="10" stroke-width="3"></path><g transform="translate(-0.5 -0.5)"><switch><foreignObject height="100%" pointer-events="none" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;" width="100%"></foreignObject><text fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="14px" font-weight="bold" text-anchor="middle" x="293" y="325">send and receive...</text> </switch></g></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"></g><a target="_blank" transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems"><text font-size="10px" text-anchor="middle" x="50%" y="100%">Text is not SVG - cannot display</text> </a></switch><title>A diagram showing MESH in the centre, with double sided arrows pointing to and from supplier systems, point-of-care applications and health and care workers as these all use MESH to send large messages</title></svg>

MESH enables senders and recipients to exchange messages securely and reliably. 

1. Sender uploads a message to MESH via their outbox
2. The MESH service holds the message until the recipient is able to retrieve it
3. The recipient retrieves the message and acknowledges the successful download of it
4. Sender is able to track the delivery status of sent messages
5. A non-delivery report will be sent to the sender if the recipient doesn't retrieve the message within 5 days

The service also provides message routing controls and directory services. Messages can be given a Workflow ID, which helps recipients understand the type of message they are receiving. For more information, visit [MESH: Workflow Groups and Workflow IDs](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/workflow-groups-and-workflow-ids).

---

### Status, Service Level and Current Usage

This service has been live since 2015. It is an evolution of an earlier service called Data Transfer Service (DTS). In terms of usage:

- there are over 400 different message types in use per month
- there are around 22,000 active mailboxes in a given month
- it handles around 30-60 million messages per month

It is a platinum service, meaning it is available and supported 24 hours a day, 365 days a year.

---

### Roadmap

---

### How to Access This Service

You can access MESH in a number of ways. All options are free to use, but you need to show you have a valid use case to use MESH.

You can also use a combination of these options, which you’ll need to set up each one separately.

MESH is available over the internet and over the Health and Social Care Network (HSCN).

---

### 1\. API

Use the MESH API to integrate MESH into your own software products.

There is a digital onboarding process to access the service. Expect it to take a minimum of 1 month.

Once integrated and onboarded, you can send files up to 50 GB.

[Get started with MESH API (external link, opens in a new tab)](https://digital.nhs.uk/developer/api-catalogue/message-exchange-for-social-care-and-health-api#api-description__end-to-end-process-to-integrate-with-mesh-api)

---

### 2\. Client

The MESH Client is a software package that enables basic integration to MESH without the need for in depth assurance. It is best suited to system-to-system messaging.

You'll need system administrator rights to install and configure the MESH Client. This can take 1 to 3 weeks.

Once installed, ideally on a server, you can drop one file for the payload and another file for details about the message type, including the specific folders they should be sent to within your file system. MESH will automatically check these folders (on a configurable interval) and send the messages. Incoming messages will appear in the folders, to be retrieved when convenient.

Once you’ve set up MESH Client, you can send files up to 50 GB.

[Get started with MESH Client (external link, opens in a new tab)](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/client-installation-guidance#installation-pre-requisites)

---

### 3\. User Interface (UI)

MESH UI is a web application that enables the manual sending or receiving of small files, in low volumes. It’s ideal for sending things like datasets to NHS England.

There is no need to install any software. This means it's ideal for health or care workers that are not able to automate or integrate systems. To access MESH UI, workers must be authenticated via [NHS Care Identity Service 2 (NHS CIS2)](https://digital.nhs.uk/services/care-identity-service/applications-and-services/cis2-authentication).

Expect it take 2 to 3 weeks to apply and get set up.

Once it’s set up, you can send files up to 50 MB, or 100 MB if you access the website through [the Health and Social Care Network](https://digital.nhs.uk/services/health-and-social-care-network).

[Get started with MESH UI](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-user-interface-ui)

---

---

---

### Further Information

[MESH guidance hub](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub)

View our selection of MESH and MOLES technical documentation. These guides will help you install and use your MESH client, manage your advanced settings and identify recipient mailboxes using the endpoint lookup service.

Last edited: 15 August 2024 4:07 pm
