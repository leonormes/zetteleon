---
aliases: []
author: ["[[Gemini]]"]
confidence: 
created: 2025-12-08T00:00:00Z
description: "Created with Gemini"
epistemic: 
last_reviewed: 
modified: 2025-12-08T13:18:09Z
published:
purpose: 
review_interval: 
see_also: []
source: "https://gemini.google.com/share/ece4e6c0b900"
source_of_truth: []
status: 
tags: ["clippings"]
title: All the Tasks That Need Doing From LCRCA This Email Change
type: 
uid: 
updated: 
---

extract all the tasks that need doing from this email change

## 🛠️ Required Tasks and Actions

Based on the email thread, here is a structured summary of the tasks that need to be actioned, prioritising the necessary steps for deployment and network connection:

### 1. Pre-Deployment Technical Checks (Immediate)

This is the purpose of the scheduled technical call, primarily driven by Jamie Wade (LCRCA Senior Engineer).

- **Review Prerequisites:** Run through the prerequisites to ensure a smooth deployment.
- **Confirm Environment Access:** Confirm that FITFILE has the necessary access to the environment.
- **Complete Deployment Steps:** Get started on the actual deployment during the 2-hour slotted time, assuming readiness.

### 2. Rollout Strategy Clarification (Prerequisite for Full Deployment)

Jamie Wade requires confirmation of the intended deployment pattern to correctly initiate change control.

- **Determine Rollout Pattern:** Clarify the intended rollout pattern (e.g., Phased approach like PoC Production, or a full deployment).
- **Advise on Change Request Timing:** Use the rollout pattern to determine when Jamie needs to raise a Change Request on the LCRCA side.

### 3. Change Request Submission (Required for Full Network Connection)

This is a specific, high-level administrative task for the LCRCA team, contingent on the rollout decision.

- **Submit Change Request (If Required):** If a **full deployment** and **connection to the LCRCA main network** are required, the LCRCA team will need to submit a change request.

### 4. Internal Coordination (FITFILE)

- **Prep Call Discussion:** Susannah Thomas is discussing Jamie's email further on an internal prep call at **3pm today** (08 December 2025) with Robin Mofakham and Leon Ormes.

Would you like me to outline the timeline of the scheduling for the technical call based on the emails?

yes

## 📅 Technical Call Scheduling Timeline

Based on the email exchange, here is the timeline of the scheduling for the technical call between FITFILE and LCRCA (Jamie/Lynn).

| Date (2025)     | Time  | Sender/Action             | Key Information/Outcome                                                                                                                                                                         |
| --------------- | ----- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **03 December** | 15:27 | Lynn Shelbourne (LCRCA)   | Confirmed the design was approved at DAB. Jamie Wade needs time with the tech team, suggesting **1.5-2 hours** might be required.                                                               |
| **03 December** | 17:49 | Susannah Thomas (FITFILE) | Provided availability for the following week, including **Tuesday 9th December: 11am - 3pm**.                                                                                                   |
| **04 December** | 08:13 | Lynn Shelbourne (LCRCA)   | Proposed a time: Jamie is free on **Tuesday 1pm**. Requested to book for **2 hours** for "wiggle room."                                                                                         |
| **04 December** | 18:56 | Susannah Thomas (FITFILE) | Sent an invite for **Tuesday at 1pm** for the tech call.                                                                                                                                        |
| **05 December** | 12:45 | Lynn Shelbourne (LCRCA)   | Confirmed only Jamie and 'J' (J. Davitt) will attend the meeting. Mentioned they would "hopefully send something over on Monday when Jamie is back in."                                         |
| **08 December** | 09:00 | Jamie Wade (LCRCA)        | Confirmed the intention is a quick run through of prerequisites and ensuring FitFile's access. Envisioned **30-60 minutes** but happy to use the **2-hour slot** and get started on deployment. |

---

### Key Confirmed Meeting Details

- **Date:** Tuesday, 09 December 2025
- **Time:** 1:00 pm (13:00)
- **Duration:** 2-hour slot is booked, though the core task may only take 30-60 minutes.
- **Attendees (LCRCA):** Jamie Wade and J. Davitt.

Jamie's email was sent today, **8 December 2025 at 09:00**, indicating the prep call is scheduled for **3pm today**.

Would you like to focus on the key points Jamie wants to cover during the Tuesday 1pm tech call?

do the same for this email chain

## ⚙️ Technical Installation Tasks and Requirements

This email outlines the specific network and infrastructure tasks required from the **Data Provider** site (Milton Keynes University Hospital, based on the recipients) to proceed with the technical installation of the Secure Data Environment (SDE) ahead of the Christmas change freeze.

The tasks are organised around five key technical components:

### 1. Hub-Spoke Connectivity Architecture

The goal is to establish network communication between the new FITFILE SDE environment and the Data Provider's on-premises network.

- **VNet Setup:** The Azure subscription must contain a **VNet** that includes the central firewall and connectivity to the on-premises network (e.g., via **Express Route or VPN**).
- **VNet Peering Configuration:** Configure **VNet peering** between the hub VNet (Data Provider's) and the new FITFILE spoke VNet, ensuring **traffic forwarding is enabled**.

---

### 2. IP Address Allocation

Specific IP ranges and addresses are needed for network configuration.

- **Spoke VNet CIDR Block:** Provide a **non-overlapping /24 CIDR block** for the new spoke VNet.
- **Firewall Private IP:** Provide the private IP address of the central firewall (placeholder: **[Firewall_Private_IP]**).
- **Corporate DNS Server IP:** Provide the IP address of a corporate **DNS server** that is reachable from the new VNet (placeholder: **[Customer_DNS_Server_IP]**).

---

### 3. Firewall Rules Configuration

The central firewall must be configured to allow necessary traffic flow.

- **Outbound Traffic Allowance:** Configure the central firewall to **allow the required outbound traffic** from the spoke VNet's address space.
- **Endpoint List:** Refer to the **detailed list of required endpoints** provided by FITFILE for configuration details.

---

### 4. Service Principal / Deployment Identity

This enables automated, secure, and non-interactive deployment.

- **Service Principal Implementation:** The Service Principal must be implemented in the cloud subscription/account to allow for a **"one-button" deployment** of infrastructure.
- **Conditional Access Mitigation (If Required):** If the Data Provider's Conditional Access or device compliance policies block interactive sign-ins from the jumpbox, one of the following mitigations is required:
	- Add an **exception** for the jumpbox (or its IP range) in the relevant Conditional Access policy.
	- Use a **dedicated, non-interactive deployment identity (service principal)** with scoped permissions for deployment, logging in non-interactively from the jumpbox or a CI/CD runner.

---

### 5. Access and Accounts

Jumpbox access is needed for the FITFILE team.

- **Create Jumpbox User Accounts:** Create an **external user account** using Ollie's and Leon's FITFILE email addresses, granting them access to log into the **Jumpbox**.

---

## 📞 Administrative and Programme Tasks

- **Allocate Programme Manager (PM):** The Data Provider (Chris Wiggins) needs to provide an update on the **allocation of a PM** for the programme.
- **Confirm Call Attendees:** Confirm if **Joao and the PM** can join the call on Tuesday next week, or if the call needs to be rescheduled due to the critical need for IT services support.
- **Provide Feedback:** Chris and Oliver need to provide **feedback** on the above technical requirements and forward them to **Joao** if necessary.

---
