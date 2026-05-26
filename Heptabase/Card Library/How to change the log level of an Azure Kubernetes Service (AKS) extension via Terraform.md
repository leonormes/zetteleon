---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-26T11:43:55+00:00
title: How to change the log level of an Azure Kubernetes Service (AKS) extension via Terraform
---

## How to Change the Log Level of an Azure Kubernetes Service (AKS) Extension via Terraform

you need to update the configuration of the extension resource by specifying the appropriate log level setting. However, the exact mechanism depends on the specific extension you're working with.

In general, AKS extensions managed by Terraform can be configured using the `azurerm_kubernetes_cluster_extension` resource. The `logLevel` setting for the extension might be part of the `configuration_protected` or `configuration` blocks, depending on the specific extension you're using.

Here's a general approach you can take to change the log level:

### 1\. Update Terraform for the Extension

If you are already using Terraform to manage the AKS extensions, you should find the Terraform resource corresponding to the extension and look for where the log level is defined. It could be inside the `configuration` or `configuration_protected` block for the `azurerm_kubernetes_cluster_extension` resource.

Here's an example of how the log level can be set:

```hcl
resource "azurerm_kubernetes_cluster_extension" "example" {
  name                = "your-extension-name"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.example.id
  extension_type      = "Microsoft.AzurePolicy"
  auto_upgrade_minor_version = true
  release_train       = "Stable"

  configuration {
    logLevel = "Info" # Change from "Default" to "Info"
  }
}
```

This example assumes you are working with an AKS extension where the `logLevel` is a configurable parameter. You may need to consult the specific extension documentation to confirm the exact key for configuring the log level.

### 2\. Updating via Azure CLI

If you are not managing this via Terraform but prefer to use the Azure CLI instead, you can configure AKS extensions with `az k8s-extension` commands. To update the log level, you'd first retrieve the extension's current configuration and then apply the necessary changes.

Here's how to use the Azure CLI to update an AKS extension log level:

```bash
az k8s-extension update \
    --cluster-name <cluster-name> \
    --resource-group <resource-group-name> \
    --name <extension-name> \
    --config logLevel=Info
```

Make sure to replace `<cluster-name>`, `<resource-group-name>`, and `<extension-name>` with the actual values of your cluster and extension.

### 3\. Apply Changes and Verify

After updating your Terraform or CLI commands, apply the changes:

- For Terraform: Run `terraform apply`.
- For Azure CLI: Simply running the above command will update the extension in real-time.

### Verify the Log Level

You can verify the change by checking the current configuration of the extension:

```bash
az k8s-extension show \
    --cluster-name <cluster-name> \
    --resource-group <resource-group-name> \
    --name <extension-name>
```

This will display the configuration where you can confirm the `logLevel` has been updated to `Info`.

---

If the specific extension you are working with has different configurations, feel free to provide more details, and I can assist with a more tailored solution!
