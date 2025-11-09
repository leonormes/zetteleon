---
aliases: []
confidence: 
created: 2025-09-11T08:12:10Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: CALICO_WIKI
type:
uid: 
updated: 
version:
---

## Calico Comprehensive Wiki

### Table of Contents

1. [What is Calico?](#what-is-calico)
2. [Core Components](#core-components)
3. [Architecture Overview](#architecture-overview)
4. [Deployment Options](#deployment-options)
5. [Cloud Provider Integration](#cloud-provider-integration)
6. [Getting Started](#getting-started)
7. [Use Cases and When to Use Calico](#use-cases-and-when-to-use-calico)
8. [Troubleshooting](#troubleshooting)

### What is Calico

Calico is an open-source networking and network security solution for Kubernetes, virtual machines, and bare-metal workloads. Created and maintained by Tigera, it's the most widely adopted solution for container networking and security, powering 8M+ nodes daily across 166 countries.

#### Key Benefits

- **Data Plane Choice**: eBPF, standard Linux, Windows, and VPP
- **Interoperability**: Works across multiple distros, clouds, bare metal, and VMs
- **Optimized Performance**: High speed and low CPU usage
- **Scalable Architecture**: Grows seamlessly with Kubernetes clusters
- **Advanced Security**: Granular access controls and WireGuard encryption
- **Kubernetes Network Policy Support**: Full implementation of Kubernetes Network Policy API
- **Flexible Networking**: BGP, VXLAN, service advertisement, and more

### Core Components

#### 1. Felix

- **Purpose**: The primary Calico agent that runs on each node
- **Responsibilities**:
  - Programs routes and ACLs on the host
  - Provides endpoint information to other Felix instances
  - Validates configuration and writes status information
- **Location**: Runs as a daemon on each Kubernetes node

#### 2. BIRD (BGP Internet Routing Daemon)

- **Purpose**: Distributes routing information between hosts
- **Responsibilities**:
  - Exchanges routing information via BGP protocol
  - Enables pod-to-pod communication across nodes
  - Handles route advertisement to physical network infrastructure
- **When Used**: In BGP networking mode (not needed for overlay modes)

#### 3. Confd

- **Purpose**: Configuration management daemon
- **Responsibilities**:
  - Monitors Calico datastore for BGP configuration changes
  - Generates BIRD configuration files
  - Restarts BIRD when configuration changes
- **Location**: Runs alongside BIRD on each node

#### 4. Typha (Optional but Recommended)

- **Purpose**: Datastore fan-out daemon
- **Responsibilities**:
  - Reduces datastore load by acting as a proxy
  - Caches and fans out datastore updates to Felix instances
  - Improves scalability for large clusters
- **When Required**: Mandatory for clusters with >50 nodes using Kubernetes datastore

#### 5. CNI Plugin

- **Purpose**: Kubernetes Container Network Interface implementation
- **Responsibilities**:
  - Configures network interfaces for pods
  - Assigns IP addresses (IPAM)
  - Sets up routing rules
- **Location**: Installed on each Kubernetes node

#### 6. Calico API Server (Optional)

- **Purpose**: Provides Kubernetes API access to Calico resources
- **Responsibilities**:
  - Enables `kubectl` access to Calico resources
  - Provides validation and defaulting for Calico APIs
  - Supports Calico Enterprise features
- **When Used**: When you need kubectl access to Calico resources

#### 7. Tigera Operator

- **Purpose**: Manages Calico lifecycle in Kubernetes
- **Responsibilities**:
  - Installs and configures Calico components
  - Handles upgrades and configuration changes
  - Manages certificates and secrets
- **Deployment**: Recommended method for production deployments

### Architecture Overview

#### Data Plane Options

##### 1. Standard Linux Networking

- Uses Linux kernel's built-in networking stack
- iptables for policy enforcement
- Standard routing for packet forwarding
- **Best for**: General purpose deployments

##### 2. eBPF Data Plane

- Uses extended Berkeley Packet Filter in the Linux kernel
- Higher performance than iptables
- Lower CPU overhead
- **Best for**: High-performance workloads, large clusters

##### 3. Windows HNS

- Host Network Service integration for Windows nodes
- Supports Windows containers
- **Best for**: Mixed Linux/Windows clusters

##### 4. VPP (Vector Packet Processing)

- High-performance packet processing
- Userspace networking stack
- **Best for**: Specialized high-throughput applications

#### Networking Modes

##### 1. BGP (Border Gateway Protocol)

- **Description**: Native Layer 3 networking without overlays
- **Pros**: High performance, simple troubleshooting, works with existing network infrastructure
- **Cons**: Requires BGP-capable network infrastructure
- **Use Case**: On-premises deployments with BGP-enabled switches/routers

##### 2. VXLAN Overlay

- **Description**: Encapsulates pod traffic in VXLAN tunnels
- **Pros**: Works with any underlying network, no special network requirements
- **Cons**: Slight performance overhead due to encapsulation
- **Use Case**: Cloud deployments, networks without BGP support

##### 3. IPIP Overlay

- **Description**: IP-in-IP encapsulation for cross-subnet traffic
- **Pros**: Lower overhead than VXLAN, works across subnets
- **Cons**: Only encapsulates cross-subnet traffic
- **Use Case**: Hybrid deployments with some BGP capability

### Deployment Options

#### 1. Tigera Operator (Recommended)

The Tigera Operator is the recommended way to install and manage Calico in production environments.

##### Installation Steps

```bash
# Install operator and CRDs
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/operator-crds.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/tigera-operator.yaml

# Configure installation
kubectl create -f - <<EOF
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  # Kubernetes provider (EKS, GKE, AKS, etc.)
  kubernetesProvider: ""
EOF
```

##### Benefits

- Automated lifecycle management
- Handles upgrades and configuration changes
- Certificate management
- Production-ready defaults

#### 2. Helm Chart

Calico provides official Helm charts for deployment.

##### Installation Steps

```bash
# Add Calico Helm repository
helm repo add projectcalico https://docs.tigera.io/calico/charts

# Create namespace
kubectl create namespace tigera-operator

# Install Calico
helm install calico projectcalico/tigera-operator --namespace tigera-operator
```

##### Benefits

- Familiar Helm workflow
- Easy customization through values.yaml
- Version management through Helm

#### 3. Kubernetes Manifests

Direct application of Kubernetes YAML manifests.

##### Available Manifests

- `calico.yaml` - Standard Calico installation
- `calico-vxlan.yaml` - VXLAN overlay networking
- `calico-typha.yaml` - Installation with Typha for large clusters
- `calico-bpf.yaml` - eBPF data plane
- `calico-policy-only.yaml` - Policy enforcement only (use with other CNIs)

##### Installation

```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/calico.yaml
```

##### Benefits

- Direct control over configuration
- No additional tools required
- Good for development and testing

### Cloud Provider Integration

#### Amazon EKS

##### Option 1: AWS VPC CNI + Calico (Policy Only)

**Use Case**: When you want to use AWS VPC networking but need Calico's advanced network policies.

```bash
# Prerequisites: Disable AWS VPC CNI network policy
# Install Calico for policy enforcement only
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/operator-crds.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/tigera-operator.yaml

# Configure for AWS VPC CNI
kubectl create -f - <<EOF
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  kubernetesProvider: EKS
  cni:
    type: AmazonVPC
  calicoNetwork:
    bgp: Disabled
EOF
```

**Benefits**:

- Pods get VPC IP addresses
- Integration with AWS security groups
- Advanced Calico network policies
- AWS Load Balancer integration

##### Option 2: Full Calico Networking

**Use Case**: When you want Calico's full networking stack and don't need VPC integration.

```bash
# Create cluster without nodes
eksctl create cluster --name my-calico-cluster --without-nodegroup

# Remove AWS VPC CNI
kubectl delete daemonset -n kube-system aws-node

# Install Calico
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/operator-crds.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/tigera-operator.yaml

kubectl create -f - <<EOF
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  kubernetesProvider: EKS
  cni:
    type: Calico
  calicoNetwork:
    bgp: Disabled
EOF

# Add nodes
eksctl create nodegroup --cluster my-calico-cluster --node-type t3.medium --max-pods-per-node 100
```

**Benefits**:

- Full Calico feature set
- Flexible IP address management
- Advanced routing capabilities
- No VPC IP address consumption

#### Azure AKS

##### Azure CNI + Calico Network Policy

**Use Case**: Leverage Azure's native networking with Calico's advanced policy engine.

```bash
# Create AKS cluster with Azure CNI and Calico network policy
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --network-plugin azure \
  --network-policy calico \
  --generate-ssh-keys
```

**Benefits**:

- Pods get Azure VNET IP addresses
- Integration with Azure networking features
- Advanced Calico network policies
- Azure Load Balancer integration

**Technical Details**:

- Azure CNI runs in "transparent mode" for Calico compatibility
- Uses kernel routes instead of bridge networking
- Calico enforces policies on individual container interfaces

#### Google GKE

##### GKE with Calico Network Policy

```bash
# Create GKE cluster with Calico network policy
gcloud container clusters create my-cluster \
  --enable-network-policy \
  --zone us-central1-a
```

### Getting Started

#### Quick Start for Self-Managed Kubernetes

1. **Install Calico using the Operator** (Recommended):

```bash
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/operator-crds.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/custom-resources.yaml
```

2. **Verify Installation**:

```bash
kubectl get pods -n calico-system
kubectl get nodes -o wide
```

3. **Install calicoctl** (Optional but recommended):

```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.3/manifests/calicoctl.yaml
```

#### Configuration Examples

##### Basic Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

##### Calico Global Network Policy

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: deny-all-non-system
spec:
  selector: projectcalico.org/namespace != "kube-system"
  types:
    - Ingress
    - Egress
```

### Use Cases and When to Use Calico

#### Choose Calico When You Need

1. **Advanced Network Policies**
   - Fine-grained security controls
   - Global policies across namespaces
   - Application layer policies (with Istio)

2. **High Performance**
   - eBPF data plane for maximum performance
   - Low CPU overhead
   - High throughput requirements

3. **Flexibility**
   - Multiple data plane options
   - Various networking modes (BGP, VXLAN, IPIP)
   - Cross-platform support (Linux, Windows)

4. **Scalability**
   - Large cluster support (1000+ nodes)
   - Efficient resource utilization
   - Typha for datastore scaling

5. **Compliance and Security**
   - Encryption in transit (WireGuard)
   - Audit logging
   - Compliance reporting (with Calico Enterprise)

#### Don't Use Calico When

1. **Simple Requirements**
   - Basic connectivity without policies
   - Small clusters with minimal security needs

2. **Cloud-Native Only**
   - Only using cloud provider features
   - No need for portable networking

3. **Resource Constraints**
   - Very limited CPU/memory
   - IoT or edge devices with minimal resources

### Troubleshooting

#### Common Issues and Solutions

##### 1. Pods Not Getting IP Addresses

**Symptoms**: Pods stuck in `ContainerCreating` state
**Diagnosis**:

```bash
kubectl describe pod <pod-name>
kubectl logs -n calico-system -l k8s-app=calico-node
```

**Common Causes**:

- CNI plugin not installed correctly
- IP pool exhaustion
- Node not ready

##### 2. Network Policy Not Working

**Symptoms**: Traffic allowed when it should be blocked
**Diagnosis**:

```bash
calicoctl get networkpolicy -o yaml
calicoctl get globalnetworkpolicy -o yaml
kubectl logs -n calico-system -l k8s-app=calico-node
```

**Common Causes**:

- Policy selector not matching pods
- Policy order issues
- Missing policy types (Ingress/Egress)

##### 3. BGP Peering Issues

**Symptoms**: Pods on different nodes can't communicate
**Diagnosis**:

```bash
calicoctl node status
calicoctl get bgppeer
sudo birdc show protocols
```

**Common Causes**:

- BGP configuration errors
- Firewall blocking BGP (port 179)
- Network infrastructure not supporting BGP

##### 4. Performance Issues

**Symptoms**: High CPU usage, slow network performance
**Diagnosis**:

```bash
kubectl top nodes
kubectl top pods -n calico-system
```

**Solutions**:

- Enable eBPF data plane
- Tune Felix configuration
- Use Typha for large clusters

#### Useful Commands

```bash
# Check Calico status
kubectl get pods -n calico-system
calicoctl node status

# View network policies
calicoctl get networkpolicy --all-namespaces
calicoctl get globalnetworkpolicy

# Check IP pools
calicoctl get ippool -o wide

# View BGP information
calicoctl get bgpconfig
calicoctl get bgppeer

# Debug connectivity
calicoctl get workloadendpoint
calicoctl get hostendpoint
```

#### Log Locations

- **Felix logs**: `kubectl logs -n calico-system -l k8s-app=calico-node -c calico-node`
- **Typha logs**: `kubectl logs -n calico-system -l k8s-app=calico-typha`
- **Operator logs**: `kubectl logs -n tigera-operator -l k8s-app=tigera-operator`

### Additional Resources

- [Official Calico Documentation](https://docs.tigera.io/calico/latest/)
- [Calico GitHub Repository](https://github.com/projectcalico/calico)
- [Calico Slack Community](https://slack.projectcalico.org/)
- [Tigera Academy Training](https://academy.tigera.io/)
- [Calico Certification](https://www.tigera.io/tigera-products/calico-certification/)

---

*This wiki provides a comprehensive overview of Calico. For the most up-to-date information, always refer to the official Calico documentation.*
