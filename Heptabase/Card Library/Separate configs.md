# Separate configs

# Separate Config

To separate the Kubernetes-specific configuration from the cloud provider (Azure AKS or AWS EKS), you need to decouple the cloud infrastructure configurations from the Kubernetes configurations.

Here's a step-by-step approach to achieve this separation:

## 1\. Kubernetes-Specific Configuration

The Kubernetes-specific configurations are platform-agnostic and can be applied to any Kubernetes cluster, regardless of whether it's running on Azure AKS, AWS EKS, GCP GKE, or an on-premise solution. These typically include:

- Namespaces

- Deployments

- Services

- Ingress Controllers

- ConfigMaps

- Secrets

- Persistent Volumes & Persistent Volume Claims (if using standard storage classes)

In Kubernetes, these can be managed independently of the cloud provider's configuration.

### To List Kubernetes Configurations in a Deployed AKS Cluster

You can use `kubectl` commands to retrieve the configurations that exist within your AKS cluster, and these configurations can be reused for other cloud providers like AWS EKS.

#### Common `kubectl` Commands to Retrieve Kubernetes-specific Configurations

```bash
# Get all namespaces
kubectl get namespaces

# List all resources within a namespace (replace <namespace> with the actual namespace name)
kubectl get all -n <namespace>

# Get Deployments
kubectl get deployments -A -o yaml  # "-A" for all namespaces

# Get Services
kubectl get services -A -o yaml

# Get Ingresses
kubectl get ingresses -A -o yaml

# Get ConfigMaps
kubectl get configmaps -A -o yaml

# Get Secrets
kubectl get secrets -A -o yaml

# Get Persistent Volume Claims (PVCs)
kubectl get pvc -A -o yaml

# Get Persistent Volumes (PV)
kubectl get pv -A -o yaml

# Get StatefulSets, DaemonSets, Jobs (if applicable)
kubectl get statefulsets -A -o yaml
kubectl get daemonsets -A -o yaml
kubectl get jobs -A -o yaml
```

By running these commands, you can extract the YAML configuration of all your Kubernetes resources (like Deployments, Services, ConfigMaps, Ingresses, etc.) that are specific to the Kubernetes API, and not tied to Azure or AWS.

### 2\. Azure-Specific Configuration (Terraform for AKS)

This part involves the Terraform resources used to provision and configure AKS. These are cloud-specific and tied to Azure. They include:

- AKS Cluster (Azure Resource Manager resource definitions for AKS)

- Azure Load Balancers

- Azure Disk Storage or File Storage classes

- Azure Networking (VNETs, Subnets, etc.)

- Role-based access control (RBAC) for Azure AD integration

- Azure-specific monitoring or logging configurations

In Terraform, you'll typically use `azurerm` provider for Azure-specific configurations like:

```hcl
resource "azurerm_kubernetes_cluster" "aks_cluster" {
  name                = var.cluster_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = var.dns_prefix

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.vm_size
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }
}
```

This is specific to Azure and won't work for AWS EKS, which has its own Terraform resources, like `aws_eks_cluster`.

### 3\. Abstracting Cloud-Specific Configurations

To support both Azure AKS and AWS EKS, you can use different Terraform configurations for the cloud provider (Azure/AWS) while sharing the Kubernetes-specific resources (like Deployments, Services, etc.).

- Provider-Specific Terraform Modules: Write separate modules for provisioning the cloud-specific infrastructure (`azurerm` for AKS, `aws` for EKS).

- Kubernetes Configurations via Terraform: Use the `kubernetes` provider in Terraform to manage Kubernetes resources such as Deployments, Services, ConfigMaps, etc. This can be shared across cloud providers.

   Example Terraform config for Kubernetes resources (platform-agnostic):

   ```hcl
   provider "kubernetes" {
     host                   = azurerm_kubernetes_cluster.aks_cluster.kube_config.host
     client_certificate      = base64decode(azurerm_kubernetes_cluster.aks_cluster.kube_config.client_certificate)
     client_key              = base64decode(azurerm_kubernetes_cluster.aks_cluster.kube_config.client_key)
     cluster_ca_certificate  = base64decode(azurerm_kubernetes_cluster.aks_cluster.kube_config.cluster_ca_certificate)
   }
   
   resource "kubernetes_namespace" "example" {
     metadata {
       name = "example-namespace"
     }
   }
   
   resource "kubernetes_deployment" "nginx" {
     metadata {
       name      = "nginx"
       namespace = kubernetes_namespace.example.metadata.name
     }
   
     spec {
       replicas = 2
   
       selector {
         match_labels = {
           app = "nginx"
         }
       }
   
       template {
         metadata {
           labels = {
             app = "nginx"
           }
         }
   
         spec {
           container {
             name  = "nginx"
             image = "nginx:1.14.2"
   
             ports {
               container_port = 80
             }
           }
         }
       }
     }
   }
   ```

### 4\. Separate Cloud Provider Configurations

For AKS and EKS, you'd have different Terraform files:

- Azure AKS (`aks.tf`):

   ```hcl
   provider "azurerm" {
     features {}
   }
   
   resource "azurerm_kubernetes_cluster" "aks" {
     # Azure-specific config
   }
   ```

- AWS EKS (`eks.tf`):

   ```hcl
   provider "aws" {
     region = var.aws_region
   }
   
   resource "aws_eks_cluster" "eks" {
     # AWS-specific config
   }
   ```

By using this method, you keep the cloud provider-specific configurations separate, while the Kubernetes-specific configurations (like YAML or Kubernetes resources) remain the same across cloud providers.

### 5\. Managing Terraform Workspaces or Modules

To make it more maintainable, consider using Terraform workspaces or modules:

- Workspaces: Use different workspaces to separate Azure and AWS environments while reusing the same Terraform code.

- Modules: Create reusable modules for Kubernetes infrastructure that can be shared across cloud providers.

---

This separation will allow you to switch between AKS and EKS without modifying the Kubernetes-specific parts of your deployment. You can focus on writing Terraform code specific to the cloud provider and ensure the Kubernetes configuration remains consistent across different environments.

Got an error from the subnet saying insufficient IPs in the subnet
The subnet `10.0.0.16/28` has a prefix length of 28, meaning that 28 bits are used for the network portion of the address, leaving 4 bits for the host portion.

To calculate the number of IPs in this range:

1. Subnet mask in binary:
   `/28` corresponds to a subnet mask of `255.255.255.240` or `11111111.11111111.11111111.11110000` in binary.

2. Number of available IPs:
   The number of host IPs is ( 2^{(32 - 28)} = 2^4 = 16 ) IP addresses.

3. Total IPs:
   There are 16 IP addresses in total for this subnet.

### Breakdown of the IP Range

- First IP (Network address): `10.0.0.16` (reserved as the network address)

- Last IP (Broadcast address): `10.0.0.31` (reserved as the broadcast address)

Thus, out of the 16 IPs, 14 are usable for hosts (from `10.0.0.17` to `10.0.0.30`).

### Summary

- Total IPs: 16

- Usable IPs: 14