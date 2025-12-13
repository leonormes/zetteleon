---
aliases: []
confidence: 
created: 2025-02-26T12:58:48Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [k8s, networking]
title: Use Calico
type: documentation
uid: 
updated: 
version: 1
---

we have Kubernetes running in Aws. we have installed the Calico CNI. know the cni is there what can I do first to start using the features

Once Calico CNI is installed on your Kubernetes cluster in AWS, you can start leveraging its features by following these steps:

## 1. **Verify Installation**
   - Ensure Calico is running correctly by checking the status of pods in the `tigera-operator` namespace:

```bash
kubectl get pods -n tigera-operator
```

   - Confirm nodes are in the `Ready` state:

```bash
kubectl get nodes 
```

## 2. **Set Up Network Policies**
   - Use Calico's advanced network policies to secure pod communication. Calico supports both Kubernetes-native and its own policies for fine-grained control.
   - Example: Create a policy to deny all traffic by default and allow specific ingress:

```yaml
apiVersion: projectcalico.org/v3
     kind: NetworkPolicy
     metadata:
       name: allow-ingress
       namespace: default
     spec:
       selector: all()
       ingress:
         - action: Allow
           source:
             nets:
               - "192.168.1.0/24"
     ```
   Apply it using `kubectl apply -f \<policy-file\>`[4][6].

### 3. **Configure IP Address Management (IPAM)**
   - Calico uses IPAM to allocate IPs to pods. You can configure IP pools for your cluster or inspect IP blocks using:
```bash
calicoctl ipam show --show-blocks
```

## 4. **Enable Encryption**
   - Secure data in transit by enabling IPsec or WireGuard encryption for pod-to-pod communication.

## 5. **Leverage Routing Features**
   - Utilize Calico's BGP routing to create a highly scalable and efficient network for large clusters.

## 6. **Monitor And Troubleshoot**
   - Use `calicoctl` or Kubernetes tools like `kubectl logs` to monitor the performance and troubleshoot issues with Calico components.

These steps will help you start utilizing Calico's networking and security features effectively.

After installing Calico CNI in your Kubernetes cluster on AWS, you can immediately start leveraging its features to enhance your cluster's networking and security. Here's a breakdown of initial steps and features you can explore:

Verify Calico Installation

 - Check Pod Status: Ensure all Calico pods are running correctly in the calico-system namespace. This confirms that Calico is properly deployed and functioning.
   kubectl get pods -n calico-system

   You should see pods like calico-typha, calico-node, and calico-kube-controllers in a Running state.

 - CNI Configuration: Verify that Kubernetes nodes are using Calico as their CNI. You can check the node annotations for CNI information.
   kubectl get node \\<node-name\\> -o yaml | grep "node.alpha.kubernetes.io/network-unavailable"

This command should return false if the node is correctly configured with a CNI like Calico.

Explore Network Policies

 - Default Deny Policies: Calico network policies allow you to control traffic flow at the pod level. By default, Kubernetes allows all traffic between pods. Calico lets you implement a "default deny" policy to enhance security. This means you explicitly allow only necessary traffic, and all other traffic is blocked.
   - Create a Default Deny Policy: Apply a NetworkPolicy that denies all ingress and egress traffic in a namespace.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

Save this as default-deny-policy.yaml and apply it:

`kubectl apply -f default-deny-policy.yaml -n \<your-namespace\>`

   - Allow Specific Traffic: After implementing default deny, you can create policies to allow specific traffic based on your application needs. For example, to allow ingress traffic to pods with label app: my-app on port 80:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-myapp
spec:
  podSelector:
    matchLabels:
      app: my-app
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector: {} # Allow from all pods in the same namespace
    ports:
    - protocol: TCP
      port: 80
```

Save this as allow-ingress-myapp-policy.yaml and apply it:

`kubectl apply -f allow-ingress-myapp-policy.yaml -n \<your-namespace\>`

 - Test Network Policies: Deploy example applications and use kubectl exec or calicoctl (Calico's command-line tool) to test connectivity and verify that your network policies are working as expected.
Utilize Calico IP Address Management (IPAM)
 - IP Address Pools: Calico manages IP addresses for pods. You can examine the default IP pools and customize them if needed.
   calicoctl get ippool default-ipv4-ippool -o yaml

   This command will show you the configuration of the default IPv4 IP pool, including CIDR, NAT outgoing settings, and more.

 - Customize IP Pools (Optional): If you have specific IP addressing requirements, you can modify the default IP pool or create new ones. For example, you might want to create separate IP pools for different namespaces or node groups. Refer to the official Calico documentation for details on customizing IP pools if needed.
Explore Calico Command-Line Tool (calicoctl)
 - Install calicoctl: Download and install calicoctl to interact directly with Calico's data store and manage Calico resources. Instructions are available in the official Calico documentation.
 - Basic calicoctl Commands: Use calicoctl to get information about Calico resources and status.

```sh
calicoctl get nodes
calicoctl get profiles
calicoctl get networkpolicies --all-namespaces
```

These commands help you understand the current state of your Calico deployment and the policies in place.

Further Exploration

Once you have verified the installation and explored basic network policies and IPAM, you can delve deeper into Calico's advanced features:

 - Global Network Policies: Implement cluster-wide network policies that apply across namespaces.
 - Tiered Network Policies: Organize network policies into tiers for more complex security models.
 - Calico DNS Policy: Control DNS access for pods.
 - Host Endpoints: Secure the Kubernetes nodes themselves.
 - BGP Peering: Integrate Calico with your existing network infrastructure using BGP.
 - Calico Enterprise Features (If Applicable): If you are using Calico Enterprise, explore features like intrusion detection and prevention (IDS/IPS), Web Application Firewall (WAF), and security dashboards.
