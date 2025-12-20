---
aliases: []
confidence: 
created: 2025-03-03T10:02:17Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [calico, cni, k8s, networking]
title: we have Kubernetes running in Aws. we have install
type: documentation
uid: 
updated: 
version: 1
---

## We Have Kubernetes Running in Aws. We Have Installed the Calico CNI. Know the Cni is there what Can I Do First to Start Using the Features

Once Calico CNI is installed on your Kubernetes cluster in AWS, you can start leveraging its features by following these steps:

### 1. Verify Installation

- Ensure Calico is running correctly by checking the status of pods in the `tigera-operator` namespace:

```bash
kubectl get pods -n tigera-operator
```

- Confirm nodes are in the `Ready` state:

```bash
kubectl get nodes
```

### 2. Set Up Network Policies

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

Apply it using `kubectl apply -f <policy-file>`[^4][^6].

### 3. Configure IP Address Management (IPAM)

- Calico uses IPAM to allocate IPs to pods. You can configure IP pools for your cluster or inspect IP blocks using:

```bash
calicoctl ipam show --show-blocks
```

### 4. Enable Encryption

- Secure data in transit by enabling IPsec or WireGuard encryption for pod-to-pod communication[^2][^4].

### 5. Leverage Routing Features

- Utilize Calico's BGP routing to create a highly scalable and efficient network for large clusters[^2][^10].

### 6. Monitor And Troubleshoot

- Use `calicoctl` or Kubernetes tools like `kubectl logs` to monitor the performance and troubleshoot issues with Calico components.

These steps will help you start utilizing Calico's networking and security features effectively.
