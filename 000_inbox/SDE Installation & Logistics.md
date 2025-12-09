---
aliases: []
author: ["[[Gemini]]"]
confidence:
created: 2025-12-08T00:00:00Z
description: Created with Gemini
epistemic:
last_reviewed:
modified: 2025-12-09T11:54:05Z
published:
purpose:
review_interval:
see_also: []
source: https://gemini.google.com/share/7b44e14a51fb
source_of_truth: []
status:
tags: []
title: SDE Installation & Logistics
type:
uid:
updated:
---

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

That document outlines several technical tasks and logistical actions required to move the Secure Data Environment (SDE) installation forward, particularly ahead of the Christmas change freeze.

Drawing on your preference for abstract-conceptual structure, I have grouped the tasks into **Logistical** and **Technical Installation** categories, focusing on the *what* and *why* for efficient understanding.

## 🗂️ Required Tasks: SDE Installation & Logistics

### 1\. ⚙️ Technical Installation Requirements (Data Provider Site)

These tasks must be completed at the Data Provider site to enable a successful SDE deployment:

| Category | Task | Details/Why |
| --- | --- | --- |
| **Connectivity** (Hub-Spoke) | **VNet Configuration** | Ensure the Azure subscription has a VNet containing a central firewall and connectivity to the on-premises network (e.g., via Express Route or VPN). |
|  | **VNet Peering** | VNet peering must be configured between the existing hub VNet and the new FITFILE spoke VNet, with traffic forwarding enabled. |
| **IP Allocation** | **Allocate CIDR Block** | Provide a non-overlapping /24 CIDR block for the new spoke VNet. |
|  | **Provide Firewall IP** | Provide the private IP address of the central firewall (`[Firewall_Private_IP]`). |
|  | **Provide DNS IP** | Provide the IP address of a corporate DNS server reachable from the new VNet (`[Customer_DNS_Server_IP]`). |
| **Firewall Rules** | **Configure Outbound Traffic** | The central firewall must be configured to allow the required outbound traffic from the spoke VNet's address space. (A detailed list of required endpoints is provided by FITFILE ). |
| **Service Principal** | **Implement Service Principal** | Implement a Service Principal in the cloud subscription/account to allow for "one-button" deployment of infrastructure. |
| **Jumpbox Access** | **Create User Account** | Create an external user account with access to log into the Jumpbox, using Ollie's and Leon's FITFILE email addresses. |
| **Conditional Access** | **Mitigate CA Issues** | If Conditional Access or device compliance policies block interactive sign-ins from the jumpbox, either: |
|  |  | \* Add an **exception** for the jumpbox (or its IP range) in the relevant Conditional Access policy , **OR** |
|  |  | \* Use a dedicated, non-interactive deployment identity (service principal) with **scoped permissions** and log in non-interactively from the jumpbox or a CI/CD runner. |

---

### 2\. 🗓️ Logistical & Confirmation Tasks

These involve programme management, scheduling, and information provision:

- **Logistical Confirmation:** Confirm the allocation of a Programme Manager (PM) for the programme.
- **Meeting Confirmation:** Confirm if **Joao** and the new **PM** can join the call on Tuesday next week. If the IT services team support is not confirmed, advise if the call needs to be rescheduled.
- **Feedback & Forwarding:** Provide feedback on the technical requirements list and forward the information to Joao if required.

---

**Next step:** Would you like a concise summary of the *next actions* required by Christopher Wiggins and Oliver Chandler?

yes

Certainly. Given the email is directed to Christopher Wiggins and Oliver Chandler, the immediate next actions they need to take, or ensure are actioned, are:

## 🎯 Next Actions for Christopher Wiggins and Oliver Chandler

### 1\. 🤝 Programme Management & Scheduling

- **Confirm PM Allocation:** Provide an update on the allocation of a Programme Manager (PM) for the programme.
- **Confirm Meeting Attendance:** Confirm if Joao and the allocated PM can join the call on Tuesday next week.
- **Advise on Rescheduling:** If support from the IT services team (including Joao and the PM) cannot be confirmed for Tuesday, advise if the call needs to be re-scheduled.

### 2\. ⚙️ Technical Action (Data Provider Site)

- **Feedback/Forward:** Provide feedback on the five-point list of network resources and information and forward the list to Joao if required.
- **Resource Provisioning:** Ensure the following necessary technical resources and information are provisioned or available ahead of the Christmas change freeze for successful deployment:
	- The Azure VNet configuration, peering, and traffic forwarding (Hub-Spoke Connectivity).
	- The /24 CIDR block allocation , Central Firewall Private IP (`[Firewall_Private_IP]`) , and Corporate DNS Server IP (`[Customer_DNS_Server_IP]`).
	- The Firewall rules configured to allow required outbound traffic (using the detailed endpoints list from FITFILE).
	- The Service Principal is implemented.
	- A user account for Ollie and Leon (using their FITFILE email addresses) is created for Jumpbox access.
	- Conditional Access mitigations for the Jumpbox are implemented, if necessary (either an exception or a non-interactive deployment identity).

---

**Next step:** The email confirms that the Data Sharing Agreement has been signed and the first payment of £25k is being processed. Would you like to check for any other dependencies or risks mentioned in the document?

yes

Yes, the document mentions several key dependencies and mitigates a potential risk related to access.

## ⚠️ Dependencies and Risk Management

---

### 1\. 🔗 Critical Dependencies (The "Why")

The entire list of technical installation requirements represents **critical dependencies** that must be fulfilled by the Data Provider (MKUH) to enable FITFILE to proceed with deployment.

- **Pre-Christmas Change Freeze:** The required network resources and information need to be available *ahead* of the Christmas change freeze to ensure a successful deployment.
- **Live Data Transition:** The ability to transition to **Live data** is dependent on two prior actions:
	1. **Data Sharing Agreement:** This is confirmed as signed by John Bradley. (Risk mitigated/Dependency met).
	2. **Synthetic Data Flow & Testing:** Live data transition can only occur *once* synthetic data is flowing and tested.

---

### 2\. 💰 Financial & Agreement Confirmation

While not a future risk or dependency, the email confirms two prerequisites are being met:

- **Data Sharing Agreement:** Confirmed as **signed** by John Bradley.
- **First Payment:** The first payment of **£25k** is confirmed as being processed in line with the Data Centre Agreement.

---

### 3\. 🛡️ Risk & Mitigation (Conditional Access)

The primary risk mentioned relates to **Jumpbox access** and Conditional Access policies:

- **Risk:** The Data Provider’s Conditional Access or device compliance policies could **block interactive sign-ins** from the Jumpbox.
- **Mitigations:** Two options are provided to mitigate this risk and ensure the application deployment can be initiated:
	1. **Add an Exception:** Add an exception for the jumpbox (or its IP range) in the relevant Conditional Access policy.
	2. **Use Dedicated Identity:** Use a dedicated, non-interactive deployment identity (service principal) with scoped permissions for deployment, and log in non-interactively from the jumpbox or a CI/CD runner.

---

**Next step:** Would you like a breakdown of the roles (e.g., Mark Dines-Allen, Christopher Wiggins, Joao) and their implied responsibilities based on the email context?

yes

Certainly. Here is a breakdown of the roles and their implied responsibilities based on the context of the email, structured around the action required.

## 👥 Implied Role Responsibilities

The email establishes a communication and accountability framework for the SDE installation.

### 1\. 📢 Sender (Mark Dines-Allen - Dines-Allen Ltd Supporting Health Innovation East)

- **Role:** Project coordinator, key communicator between FITFILE and the Data Provider (MKUH), and requirements driver.
- **Responsibility:**
	- Initiate and track the progression of the technical installation.
	- Confirm completion of major contractual prerequisites (DSA signed, payment processed).
	- Provide the definitive list of technical resources and information required from the Data Provider.
	- Request updates and scheduling confirmations (PM allocation, meeting attendees).

---

### 2\. 🏥 Primary Recipients (Christopher Wiggins and Oliver Chandler - MKUH NHS)

- **Role:** Key contacts and operational leads for the Data Provider (MKUH), responsible for overseeing the fulfillment of technical and logistical requirements.
- **Responsibility:**
	- Progress the initial change requests (Subscription, IP Addresses, Service Principles).
	- Provide feedback on the technical requirements and forward them to Joao if necessary.
	- Confirm the allocation of a Programme Manager (PM).
	- Confirm attendance of the PM and Joao for the critical call next week, or advise if the meeting needs to be rescheduled.
	- Ensure all necessary network resources and information (VNet configuration, IP addresses, Firewall rules, Service Principal, Jumpbox access/mitigations) are made available within the Data Provider site before the Christmas change freeze.

---

### 3\. 🖥️ Key Technical Personnel (Joao & PM)

- **Role (Joao):** Implied IT Services/Technical Lead for the Data Provider (MKUH), critical for the technical installation and support.
- **Role (PM):** Programme Manager, responsible for project oversight and logistics planning.
- **Responsibility:**
	- **Joao:** Address and action the technical requirements list (likely regarding the configuration of Azure, VNets, Firewall, etc.). His attendance at the call is considered **critical** for support from the IT services team.
	- **PM:** Join the call on Tuesday next week and take over the programmatic oversight from the Data Provider side.

---

### 4\. 💻 FITFILE Team (Susannah Thomas, Robin Mofakham, Oliver Rushton, Leon Ormes, Weronika Jastrzebska, Helena Ahlfors)

- **Role:** Technical implementation and support team for the SDE deployment.
- **Responsibility:**
	- Provide the detailed list of required endpoints for firewall configuration.
	- **Ollie and Leon:** Require external user accounts to be created to access the Jumpbox for application deployment.

---

**Next step:** Would you like to focus on any of the specific technical requirements, such as the **Hub-Spoke Connectivity** model?

Google Account

Leon Ormes

leonormes@gmail.com
