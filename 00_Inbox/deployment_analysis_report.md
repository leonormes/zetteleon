# Deployment Configuration Analysis Report: LCA-DP

## Executive Summary
This report analyzes the ingress, DNS, and hostname configuration for the `LCA-DP` customer deployment. The configuration is distributed across the customer repository (`LCA-DP`), the Helm chart (`ffnode`), and the infrastructure Terraform modules.

**Key Findings:**
- **Hostname:** `lca-prd-2.privatelink.fitfile.net`
- **DNS Zone:** `privatelink.fitfile.net` (Azure Private DNS Zone)
- **Ingress Strategy:** Uses NGINX Ingress Controller with host-based routing.
- **DNS Resolution:** Private DNS A records are created to point the hostname to the Ingress Controller's Private IP.

---

## 1. Hostname & DNS Configuration Strategy (Generic)

The architecture uses a split-responsibility model:
1.  **Infrastructure Layer (Terraform):** Provisons the physical network, private DNS zones, and DNS records.
2.  **Configuration Layer (Customer Repo):** Defines the customer-specific parameters (names, zones, features).
3.  **Application Layer (Helm/ArgoCD):** Configures the Kubernetes Ingress resources to respond to the hostnames.

### Data Flow
1.  **Configuration Source:** `config/customer.yaml` defines the base parameters.
2.  **Terraform Processing:** `locals.tf` logic calculates the `public_fqdn` combining `deployment_key` and `dns_zone`.
3.  **Infrastructure Provisioning:** Terraform creates the Private DNS Zone and A records.
4.  **Values Generation:** Terraform outputs `infra_facts` (including `public_fqdn`).
5.  **Helm Configuration:** CUE templates (`values.cue`) consume `infra_facts` and generate a `values.yaml` for the `ffnode` chart, explicitly setting `ingress.hosts` for each service.

---

## 2. LCA-DP Specific Configuration

### A. Configuration Source
**File:** `LCA-DP/config/customer.yaml`
```yaml
customer_name: lca
env_prefix: prd
instance_id: 2
dns_zone: "privatelink.fitfile.net"
```
**Derived Values:**
- **Deployment Key:** `lca-prd-2` (Calculated in `locals.tf`)
- **Public FQDN:** `lca-prd-2.privatelink.fitfile.net`

### B. Infrastructure (Azure Private DNS)
**Module:** `terraform-azure-private-infrastructure`
**File:** `networking.tf`

The module explicitly supports Private DNS Zones.
- **Enabled:** `private_dns_zone_enabled = true` (passed from `LCA-DP/main.tf`).
- **Zone Name:** Defaults to `privatelink.fitfile.net` in `vars.tf`, which matches the LCA configuration.
- **Records Created:**
    - `lca-prd-2.privatelink.fitfile.net` -> Ingress Controller IP (e.g., `10.0.1.10`)
    - `lca-prd-2-argocd.privatelink.fitfile.net` -> Ingress Controller IP

### C. Application Ingress (Helm/ArgoCD)
**Chart:** `ffnode`
**Template:** `values.cue` (LCA-DP)

The CUE template maps the infrastructure facts to Helm values:
```cue
host: _infra.public_fqdn // Sets global host

frontend: ingress: hosts: [{
    hostname: _infra.public_fqdn // Sets specific ingress host
    path: "/(fitfile)($|/)(.*)"
}]
```
This configuration ensures that the `frontend` service (and others like `fitconnect`, `ffcloud`) create Ingress resources that listen on `lca-prd-2.privatelink.fitfile.net`.

### D. Central Services
**Module:** `terraform-fitfile-central-services-consumer`
Used in `LCA-DP/main.tf` to register authentication callbacks (Auth0) using the same `public_fqdn`, ensuring consistency between the identity provider and the actual ingress.

---

## 3. Configuration Locations Summary

| Component | Configuration File | Parameter | Value (LCA-DP) |
|-----------|--------------------|-----------|----------------|
| **Source of Truth** | `LCA-DP/config/customer.yaml` | `dns_zone` | `privatelink.fitfile.net` |
| **Logic/Calc** | `LCA-DP/locals.tf` | `public_fqdn` | `lca-prd-2.privatelink.fitfile.net` |
| **Infrastructure** | `LCA-DP/main.tf` | `private_dns_zone_enabled` | `true` |
| **DNS Provisioning** | `private-infrastructure/networking.tf` | `azurerm_private_dns_a_record` | Creates A record for `lca-prd-2` |
| **Helm Values** | `LCA-DP/templates/values.cue` | `_infra.public_fqdn` | Mapped to `ingress.hosts` |
| **Ingress Template** | `ffnode/templates/frontend-application.yaml` | `.Values.frontend.ingress.hosts` | Consumes generated values |
