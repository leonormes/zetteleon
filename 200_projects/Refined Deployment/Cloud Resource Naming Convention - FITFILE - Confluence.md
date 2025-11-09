---
aliases: []
author:
confidence: 
created: 2025-09-21T00:00:00Z
description:
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
published:
purpose: 
review_interval: 
see_also: []
source: https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2240217089/Cloud+Resource+Naming+Convention
source_of_truth: []
status: 
tags: [cloud, ff-naming, naming-conventions, resources, standards]
title: Cloud Resource Naming Convention - FITFILE - Confluence
type:
uid: 
updated: 
version:
---

## Resource Groups

Resource Groups (RGs) should follow the naming convention: `Resource Type – Workload – Region – Environment`.

- **Example**: `rg-ff-uks-gp-net`.
  - `rg` stands for Resource Group (Resource Type).
  - `ff` likely stands for FitFile (Workload).
  - `uks` stands for UK South (Region).
  - `gp` stands for General Production (Environment).
  - Other examples include `rg-ff-uks-gp-bkup` for Azure Backup resources and `rg-ff-uks-gp-data` for FITFILE platform and associated services.

### Organizational Standard

This convention is in line with the naming convention used for all resources within the CUH ALZ (Azure Landing Zone). Resource groups are created in the Azure UK South region due to policy enforcement.

### AKS Managed Resource Groups

The Azure-managed resource group for AKS follows the naming convention of the primary resource group but with an `MC_` prefix. For example, `MC_rg-ff-uks-gp-net_aks-ff-uks-gp-01_uksouth` should be amended to `rg-ff-uks-gp-aks` (with `MC_` prefix applied automatically).

**General Rules**:

- A resource group name must be unique within a subscription.
- All Azure resources have a name that must be unique within a scope, which can vary by resource type. For example, a virtual network's name must be unique within a resource group, but duplicate names can exist across subscriptions or regions. Consistent naming conventions are helpful for managing network resources over time.
- Terraform examples for resource group names sometimes use a random suffix for uniqueness, like `myAKSResourceGroup$RANDOM_ID`.

## Virtual Networks (VNets)

The HLD mentions a VNet name example `vnet-ff-uks-gp-01`. This name appears to align with the `Resource Type – Workload – Region – Environment – Instance Number` pattern, similar to Resource Groups.

- **Example**: `vnet-ff-uks-gp-01`.

### General Rules

- A VNet's name must be unique within its resource group.
- Multiple VNets can exist within a single region, but a VNet can exist within only one region.
- Terraform examples show VNet names like `myvnet` or using a random string for uniqueness, such as `vnet-${random_string.name.result}`. Bicep templates might use `resolverVNETName`.
- When Azure automatically creates VNet resources for an AKS cluster, the name is a combination of the resource group name and `-vnet` (e.g., `resource_group_name-vnet`).

## Subnets

Subnets should be renamed following the format: `snet-ff-uks-gp-`.

- **Examples**: `snet-ff-uks-gp-system`, `snet-ff-uks-gp-jumpbox`, `snet-ff-uks-gp-workflows`.

### Specific Subnets for AKS

- For AKS clusters with custom virtual networks, an API server subnet must be created and delegated to `Microsoft.ContainerService/managedClusters`. This subnet is typically named `apiServerSubnet`.
- Another subnet for the cluster nodes is often named `clusterSubnet`.
- The minimum supported API server subnet size is a `/28`.

### Naming Constraints

- A subnet name must be unique within the virtual network.
- For maximum compatibility with other Azure services, the subnet name should begin with a letter (e.g., Azure Application Gateway cannot deploy into a subnet whose name starts with a number).
- The gateway subnet *must* be named `GatewaySubnet` for gateway creation to succeed.
- If you're using your own subnet to deploy an AKS cluster with Azure CNI Overlay, the names of the subnet, VNet, and resource group containing the VNet must be 63 characters or less and are subject to Kubernetes label syntax rules.
- Terraform examples show `subnet1` or `subnet-${random_string.name.result}`.

## Route Tables

Route tables are explicitly mentioned as needing to follow the organizational naming convention. While a direct example of a route table *name* adhering to the `Resource Type – Workload – Region – Environment` format isn't provided, it's inferred that they should conform to similar standards as other network resources within the CUH ALZ.

- **General Rule**: Ensure route tables follow the organizational naming convention.
- **Association**: Route tables are associated with the subnet of a virtual network, not directly with the VNet itself.
- **Rules**: When defining routes, it's recommended to use service tags instead of specific IP addresses to ensure reliability and overcome limits on the number of routes.

## Network Security Groups (NSGs)

NSGs should follow the organizational naming convention if applied to a VNet.

- **Example**: `nsg-ff-uks-gp-net` is an example of an NSG for virtual network resources. This follows the `Resource Type – Workload – Region – Environment` pattern.

### Rule Naming

- An NSG rule name must be unique within the NSG.
- It can be up to 80 characters long.
- It must begin with a letter or number and end with a letter, number, or underscore.
- It can contain only letters, numbers, underscores, periods, or hyphens.
- It's recommended to leave gaps between priority numbers (e.g., 100, 200, 300) when creating rules to easily add rules with higher or lower priority later.

### General Rules

- NSGs can contain as many rules as desired, within Azure subscription limits.
- You can specify `Any`, an individual IP address, a CIDR block, a service tag, or an application security group for source or destination.
- Terraform examples show NSG names like `nsg-${random_string.name.result}`.
- When creating a VM via the Azure portal, an NSG is automatically created and associated with the NIC, often named as a combination of the VM name and `-nsg`.

## AKS Clusters

While explicit formal naming conventions for AKS clusters within the FITFILE HLD are not provided, various sources offer insights into common practices and parameters for naming.

- **Recommended Practice**: The `deployment-key` (e.g., `WM-Prod`) is a short name used consistently across the infrastructure for specific customer deployments. This implies cluster names might incorporate this key.

### Examples

- A class example uses `go-web` as the cluster name.
- Azure CLI commands often use a random ID suffix for uniqueness, e.g., `myAKSCluster$RANDOM_ID`.
- Terraform configurations might use `random_pet.azurerm_kubernetes_cluster_name.id` for the cluster name and `dns_prefix` (e.g., `dns${RANDOM_ID}`).
- `eksctl` defaults to an autogenerated cluster name.
- **Constraints**: If using your own subnet with Azure CNI Overlay, the names of the VNet, Subnet, and Resource Group containing the VNet must be 63 characters or less, as these names are used as labels in AKS worker nodes and are subject to Kubernetes label syntax rules.

## General Naming & Identification Concepts

- **Labels and Annotations**: Labels are key/value pairs used to identify and select groups of related resources (e.g., in a Service's selector) and are critical for Network Policies. Annotations are for non-identifying information, often used by tools or services outside Kubernetes, and can include `owner` metadata.
- Label names are limited to 63 characters and can have an optional 253-character DNS subdomain prefix. They must start with an alphanumeric character and contain only alphanumerics, dashes, underscores, and dots.
- Custom annotations should be prefixed with your company's domain name (e.g., `example.com`) to prevent collisions.
  - It is best practice to set owner annotations on all resources to identify who to contact.
- **Namespaces (Kubernetes)**: Namespaces are a logical partitioning mechanism within a cluster. They allow for the segregation of resources, meaning you can have similarly named services (e.g., `demo`) in different namespaces (e.g., `prod` and `test`) without conflict.
- Best practice is to have one namespace per application or team and avoid using the `default` namespace to prevent mistakes. Kubernetes internal system components run in the `kube-system` namespace.
- To communicate with a Service in another namespace, you can use DNS addresses like `SERVICE.NAMESPACE.svc.cluster.local` or simply `SERVICE.NAMESPACE`.
- Network Policies in Kubernetes are namespaced, making the namespace an ideal trust boundary between teams.
- **Helm Charts**: Helm imposes strict naming conventions for OCI-based charts, where the repository name and tag are automatically determined by the chart's name and semantic version from the `Chart.yaml` file. Helm templates use `.Release.Name` and `.Release.Namespace` to automatically inject the release name and namespace. Named templates often follow the convention `$CHART_NAME.$TEMPLATE_NAME`.
