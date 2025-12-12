---
aliases: []
confidence:
created: 2025-11-19T09:07:06Z
epistemic:
last_reviewed:
modified: 2025-11-19T14:33:39Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [nnuh]
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
- Most connectivity is **basic 443 traffic**, which is expected to not be an issue.
- Ben reviewed the Firewall (FW) rules with Tom Brooks.
- Tom Brooks has a couple of questions he will raise on the call today.
- The main question is the **need for more prescriptive IP addresses (IPs)** for some endpoints that require external communications connecting in.
- Sign-off will not be granted for subnet-wide rules, especially for external traffic.

#### Azure Side Update (NNUHFT-SDE)

| **Azure Component**              | **Details**                                                                                                                                              |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **New subscription**             | `NNUHFT-SDE` created                                                                                                                                     |
| *Accounts**                      | Accounts setup for Leon and Oliver                                                                                                                       |
| **Account Rights**               | Granted **Contributor rights** over the subscription (6-month time bound) 20                                                                             |
| **vNet**                         | `NNUHFT-SDE-vnet1` created with an address space of **192.168.200.0/24**                                                                                 |
| **NAT Gateway**                  | Deployed for external internet traffic                                                                                                                   |
| **External IP for NATd traffic** | **20.162.236.86**                                                                                                                                        |
| **Subnet for NAT Gateway**       | A small subnet had to be created: `NAT` with address space **192.168.200.0/29**. This subnet has **3** available IPs. The rest of the vNet space is free |
| **vNet pairing**                 | Enabled back to the NNUH hub to allow for VPN connectivity from on-premise                                                                               |
|                                  |                                                                                                                                                          |

#### Resource Deployment Tags

Ben requests that any resources be deployed with the following tags

- Department: `SDE`
- Environment: `live`

---

### Outstanding Actions List (13 Nov 2025, 19:24)

**From:** Susannah Thomas (FITFILE Project Director) **To:** Mike Shemko, Ben Goss **Cc:** Mark Dines-Allen **Subject:** EoE - NNUH - Actions Register - outstanding items

Susannah provides the following outstanding items from the Actions Register requiring input from Mike Shemko and Ben Goss:

1. Confirm if **`year_of_birth`** will be replaced or expanded into **`date_of_birth`**.
2. **Discuss internally the audit trail requirement** and advise FITFILE which option suits NNUH best.
3. **Provide details on frequency of data updates**37.

**Further Notes:**

- Julia has shared the **White Rabbit guide** via email to assist with providing drug formats to The Hyve.
- Susannah asked Ben Goss if the **subscription request and firewall changes** had been submitted to the CAB committee for approval.
  - This is crucial to install the FITFILE Node and have synthetic data flowing before the Christmas change freeze dates.
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

- **Action:** As Susannah requested, focus on resolving the need for **more prescriptive/specific IP addresses** for external communication endpoints.
- **Context:** NNUH will **not** sign off on subnet-wide Firewall (FW) rules, especially for external traffic10. The team needs to identify the exact source IP addresses required for the endpoints that need external connectivity so the NNUH team (specifically Tom Brooks) can get sign-off.
- **Goal:** Be prepared to discuss and resolve this with **Tom Brooks** on the call today.
- Gitlab repo
  - Some trouble with the GITLAB_TOKEN.
- Create the TFC workspace
- Do we need hutch, hyve

## Deployment Plan: Azure AKS Private Cluster

### Phase 3: Central Services & Tooling
**Reference:** `FITFILE-Azure - Tooling`

Configure the central management plane to accept the new cluster.

#### 1. Vault Configuration

1. Navigate to `Central Services/hcp/vault`.
2. Edit `locals.tf`: Add the deployment block.

    ```hcl
    "<deployment_key>" = {
      secrets = tomap({
        "application" = {},
        "spicedb" = {},
        "cloudflare" = {},
        "monitoring" = {},
        "argo-workflows" = {},
      })
    }
    ```

3. Commit, push, and apply in Terraform Cloud (HCP Terraform).
4. **Populate Secrets:** Go to the Vault UI (`admin/deployments/<key>`) and populate:
    - `application`: DB passwords (generate secure strings), UDE key.
    - `spicedb`: Postgres creds.
    - `cloudflare`: API Token (Edit DNS permissions).
    - `argo-workflows`: SSO Client ID/Secret (if applicable).

#### 2. Auth0 Configuration

1. Navigate to `Central Services/auth0/<env>`.
2. Edit `locals.tf`: Add the new tenant configuration (API Identifier, Tenant Name).
3. Apply via Terraform.
4. **Capture Outputs:** Note `client_id` and `client_secret` from the output.
5. **Update Vault:** Add these Auth0 credentials to the `application` secret in Vault created in step 3.1.

#### 3. Grafana Configuration

1. Navigate to `Central Services/grafana`.
2. Edit `locals.tf`: Add deployment key to `deployments` map.
3. Apply via Terraform.
4. **Update Vault:** Take the output (Prometheus/Loki/Tempo endpoints and users) and update the `monitoring` secret in Vault.

---

### Phase 4: Infrastructure Deployment
**Reference:** `FITFILE-Azure - Infrastructure (private)`

Deploy the actual Azure resources (VNet, AKS, Jumpbox).

#### 1. Terraform Cloud Setup

1. Create a new Workspace in **FITFILE-Platforms** project. Name: `<deployment-key>`.
2. **Configure Variables (Environment, Sensitive):**
    - `ARM_CLIENT_ID` (Service Principal ID)
    - `ARM_CLIENT_SECRET` (SP Secret Value)
    - `ARM_ACCESS_KEY` (SP Secret ID)
    - `ARM_SUBSCRIPTION_ID`
    - `ARM_TENANT_ID`
    - `TF_VAR_admin_password` (Generate a secure password for the Jumpbox).

#### 2. GitLab Repository Setup

1. Create a new Private project in `fitfile/customers`. Name: `<deployment-key>`.
2. Clone locally.
3. Create files: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `providers.tf`.
4. **Versions.tf:** Configure the `cloud` block to point to the Workspace created above.
5. **Main.tf:**

    ```hcl
    module "private-infrastructure" {
      source = "app.terraform.io/FITFILE-Platforms/private-infrastructure/azure"
      version = "<latest>"
      deployment_key = "<deployment-key>"
      admin_password = var.admin_password
    }
    ```

6. **Outputs.tf:** Expose `aks_cluster_outbound_ip_address`.

#### 3. Deploy

1. `terraform login`.
2. `terraform init`.
3. `terraform apply`.
4. **Record the Output:** Note the `aks_cluster_outbound_ip_address` (required for allow-listing if the customer has a firewall).

---

### Phase 5: Platform Configuration
**Reference:** `FITFILE-Azure - Platform (private)`

Configure the software running inside the cluster via the Jumpbox.

#### 1. Generate AppRoles

1. In `Central Services/hcp/vault`, run the `jq` script to extract Role IDs and Secret IDs for the new deployment.
2. Convert the JSON output to HCL format (save this safely, you will need it for the Jumpbox).

#### 2. Connect to Jumpbox

1. Azure Portal -> VM (`FITFILEJumpbox`) -> Serial Console.
2. Login as `azadmin` using the `admin_password` set in Phase 4.
3. Run `az login`.

#### 3. Jumpbox Configuration

1. Run `./vars_setup.sh < /home/azadmin/.kube/config`.
    - *Verify:* `cat vars.tfvars` should show certificate data.
2. **Populate `vars.tfvars`:** Edit the file on the Jumpbox to include:
    - `approles = { ... }` (The HCL object generated in step 5.1).
    - `deployment_key`.
    - `argocd_host` (e.g., `key-argocd.privatelink.fitfile.net`).
    - `ingress_controller_ip_address` (from infra module output).
3. **Terraform Login:** Run `terraform login` on the Jumpbox (create a User Token in TFC settings if needed).

#### 4. Prepare Helm Overrides (Local Machine)

1. Checkout the `Deployment` repository.
2. Create file: `ffnodes/<customer>/<deployment-key>/values.yaml`.
3. Populate using the template (Configure `namespace`, `deploymentkey`, `oauth`, `appConfig`).
4. Commit and push to the `latest-release` branch (or feature branch if testing).

#### 5. Apply Platform (Jumpbox)

1. On the Jumpbox: `terraform init`.
2. `terraform apply -var-file="./vars.tfvars"`.

#### 6. Finalise

1. **State Backup:** Copy the `terraform.tfstate` from the Jumpbox to a subdirectory in the Customer GitLab repository (created in Phase 4). **Do not put it in the root.**
2. **DNS:** Ensure Cloudflare/DNS records are updated with the Ingress IP.
