---
aliases: []
confidence: 
created: 2025-12-09T11:21:13Z
epistemic: 
last_reviewed: 
modified: 2025-12-09T11:24:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Azure Jumpbox Preflight Check – Customer One‑Pager
type: 
uid: 
updated: 
---

## Azure Jumpbox Preflight Check – Customer One‑Pager

**Goal:**  
Before FITFILE deploys into your Azure subscription, we want to confirm that:

- The jumpbox / bastion host can reach Azure over HTTPS  
- The deployment user can log in with the Azure CLI  
- The user has the right permissions on the target subscription  
- Azure Resource Manager (ARM) is reachable from your network  

This avoids “last‑minute surprises” (e.g. Conditional Access blocking `az login`) during the deployment window.

---

## 1. Who Does What

**Your Azure / Entra Admin(s)**

- Ensure Conditional Access allows Azure CLI from the jumpbox
- Confirm the deployment user has the right role(s) on the target subscription

**Your Infrastructure / Jumpbox Operator**

- Runs FITFILE’s preflight script `run_me_first.sh` on the jumpbox  
- Shares the script output with FITFILE

FITFILE will provide the script and support you in interpreting the results.

---

## 2. When to Run These Checks

Please complete these steps:

1. **After**:
   - The Azure subscription for the deployment exists
   - The FITFILE deployment user account has been created
2. **Before**:
   - Any formal change freeze
   - The planned FITFILE deployment window

If you later change Conditional Access, firewall rules, or user roles, we recommend re‑running the script.

---

## 3. Portal-Side Checks (Entra / Azure Admin)

### 3.1 Conditional Access: Test Azure CLI from the Jumpbox

Use the **Conditional Access “What If”** tool to make sure Azure CLI logins from the *Azure environment* (where the jumpbox will run) are not blocked.

**Inputs for the What‑If test:**

- **User:** the FITFILE deployment user (e.g. `leon.ormes@…`)
- **Cloud app:**  
  - *Microsoft Azure CLI* (App ID: `04b07795-8ddb-461a-bbee-02f9e1bf7b46`)
- **Location:**  
  - The **egress IP or IP range that outbound traffic from the Azure spoke/jumpbox will use**  
    (for example, your central firewall / NAT gateway egress range).  
  - If this is not yet known, you can initially run the What‑If with **Any location**, and re‑run it later once the egress range is defined.
- **Device state:**  
  - Treat the jumpbox as **Unregistered / Non‑compliant**
- **Client type:**  
  - Modern client / mobile & desktop apps (Azure CLI uses this path)

**What you’re looking for:**

- No Conditional Access policy should **block** this scenario.  
- It’s fine to **require MFA** or similar controls.  
- If a policy blocks access, please adjust it (e.g. exception for the *Azure spoke egress* named location, or a dedicated “deployment” policy that allows Azure CLI for this user and IP range).

### 3.2 RBAC: Confirm the Deployment User’s Role

On the **target subscription**:

- Go to **Subscriptions → [Your Subscription] → Access control (IAM) → Check access**
- Look up the FITFILE deployment user
- Ensure they have at least one of:
  - **Contributor**
  - **Owner**
  - Or an agreed **custom “deployment” role** with equivalent permissions

If you use **PIM (Privileged Identity Management)**:

- Confirm the user has an **eligible** role on this subscription  
- Confirm they know how to **activate** it (and that approvers will be available) before the deployment window

---

## 4. Jumpbox-Side Check (run_me_first.sh)

Your jumpbox / bastion operator should run the script FITFILE provides:

1. **Copy the script to the jumpbox** (e.g. `run_me_first.sh`)
2. **Make it executable:**

   ```bash
   chmod +x run_me_first.sh
   ```

3. **Run it as the deployment user:**

   ```bash
   ./run_me_first.sh
   ```

4. **When prompted, enter:**
   - Your **Tenant ID** (GUID)
   - Your **Subscription ID** (GUID)
5. **Complete the Azure device code login:**
   - The script shows a code and a URL (e.g. `https://microsoft.com/devicelogin`)
   - Open the URL in a browser, enter the code, and sign in **as the same user** you’re using on the jumpbox

### What the Script Checks

The script will:

- Confirm **Azure CLI** is installed
- Verify HTTPS connectivity to:
  - `login.microsoftonline.com`
  - `management.azure.com`
- Log in using **device code** and detect common Conditional Access errors (e.g. `53003`)
- Confirm:
  - The specified **subscription is visible** and can be selected
  - The user has a suitable **role** (Owner/Contributor or agreed custom role)
- Perform a simple **ARM API** “smoke test”

At the end it will print either:

- **“Preflight checks PASSED”** – you are ready for FITFILE deployment  
- Or a clear **error message** indicating what failed (network, login, role, etc.)

---

## 5. What to Send to FITFILE

When the script finishes, please:

1. Copy the **full terminal output** (including any warnings)  
2. Send it to your **FITFILE contact**

This gives us everything we need to confirm readiness or help you resolve any remaining issues **before** the deployment window.

---
