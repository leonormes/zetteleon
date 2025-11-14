---
aliases: []
confidence: 
created: 2025-11-14T11:02:52Z
epistemic: 
last_reviewed: 
modified: 2025-11-14T11:11:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: NNUH
type: 
uid: 
updated: 
---

## 📧 Email Thread: EoE - NNUH - Actions Register Outstanding Items

### Latest Update (14 Nov 2025, 09:11)

**From:** Susannah Thomas (FITFILE Project Director) 1111**To:** Oliver Rushton, Leon Ormes, Robin Mofakham 2**Cc:** Weronika Jastrzebska, Helena Ahlfors, Enric Serra 3**Subject:** FW: EoE - NNUH - Actions Register outstanding items 4

- Susannah notes that there is **progress on NNUH**5.
- She hopes the team can make more progress this afternoon on the call with Tom Brooks and Harj Uppal
- She asks the recipients to note Ben Goss's comments about the **IPs** and asks if this can be resolved with Tom Brooks today.

---

### NNUH Progress and Azure Update (14 Nov 2025, 08:27)

**From:** Ben Goss (NNUHFT Technical Authority - Digital Health) 8888**To:** Susannah Thomas, Mike Shemko, Tom Brooks 9**Cc:** Mark Dines-Allen, Harj Uppal 10**Subject:** RE: EoE - NNUH - Actions Register - outstanding items 11

#### Firewall Rules & Connectivity Questions

- The **Azure side was configured** earlier in the week.
- Most connectivity is **basic 443 traffic**, which is expected to not be an issue13.
- Ben reviewed the Firewall (FW) rules with Tom Brooks14.
- Tom Brooks has a couple of questions he will raise on the call today15.
- The main question is the **need for more prescriptive IP addresses (IPs)** for some endpoints that require external communications connecting in16.
- Sign-off will not be granted for subnet-wide rules, especially for external traffic17.

#### Azure Side Update (NNUHFT-SDE)

| **Azure Component**              | **Details**                                                                                                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **New subscription**             | `NNUHFT-SDE` created                                                                                                                                             |
| *Accounts**                      | Accounts setup for Leon and Oliver                                                                                                                               |
| **Account Rights**               | Granted **Contributor rights** over the subscription (6-month time bound) 20                                                                                     |
| **vNet**                         | `NNUHFT-SDE-vnet1` created with an address space of **192.168.200.0/24** 21                                                                                      |
| **NAT Gateway**                  | Deployed for external internet traffic                                                                                                                           |
| **External IP for NATd traffic** | **20.162.236.86**                                                                                                                                                |
| **Subnet for NAT Gateway**       | A small subnet had to be created: `NAT` with address space **192.168.200.0/29**242424. This subnet has **3** available IPs25. The rest of the vNet space is free |
| **vNet pairing**                 | Enabled back to the NNUH hub to allow for VPN connectivity from on-premise                                                                                       |
|                                  |                                                                                                                                                                  |

#### Resource Deployment Tags

Ben requests that any resources be deployed with the following tags28:

- Department: `SDE` 29
- Environment: `live` 30

---

### Outstanding Actions List (13 Nov 2025, 19:24)

**From:** Susannah Thomas (FITFILE Project Director) 31313131**To:** Mike Shemko, Ben Goss 32**Cc:** Mark Dines-Allen 33**Subject:** EoE - NNUH - Actions Register - outstanding items 34

Susannah provides the following outstanding items from the Actions Register requiring input from Mike Shemko and Ben Goss:

1. Confirm if **`year_of_birth`** will be replaced or expanded into **`date_of_birth`**35.
2. **Discuss internally the audit trail requirement** and advise FITFILE which option suits NNUH best36.
3. **Provide details on frequency of data updates**37.

**Further Notes:**

- Julia has shared the **White Rabbit guide** via email to assist with providing drug formats to The Hyve38.
- Susannah asked Ben Goss if the **subscription request and firewall changes** had been submitted to the CAB committee for approval39.
    - This is crucial to install the FITFILE Node and have synthetic data flowing before the Christmas change freeze dates40.
- Susannah confirms she will send the notes from the day's call to Mike Shemko the following morning41.

---

## 🚀 Next Steps for Leon Ormes & Oliver Rushton

Leon and Oliver are the primary recipients of the Azure configuration update and have been granted access. Their focus should be on preparing for the deployment and addressing the critical IP address issue before the call.

### 1. Azure Access and Configuration Confirmation

- **Action:** Confirm access to the new Azure subscription: `NNUHFT-SDE`
- **Action:** Verify that their accounts have been set up and granted **Contributor rights** over the subscription (6-month time bound).
- **Information to Note:**
    - The Virtual Network is `NNUHFT-SDE-vnet1` with an address space of **192.168.200.0/24**
    - The external IP address for NATd traffic (internet egress) is **20.162.236.86**

### 2. Preparation for Node Deployment

- **Action:** Ensure all resources deployed for the FITFILE Node use the required tags5:
    - Department: `SDE` 
    - Environment: `live` 
- **Context:** The vNet pairing is enabled back to the NNUH hub for VPN connectivity from on-premise, which supports the overall deployment architecture8.

### 3. Critical IP Address Issue

- **Action:** As Susannah requested, focus on resolving the need for **more prescriptive/specific IP addresses** for external communication endpoints999.
- **Context:** NNUH will **not** sign off on subnet-wide Firewall (FW) rules, especially for external traffic10. The team needs to identify the exact source IP addresses required for the endpoints that need external connectivity so the NNUH team (specifically Tom Brooks) can get sign-off.
- **Goal:** Be prepared to discuss and resolve this with **Tom Brooks** on the call today12121212.
