---
aliases: []
confidence: 
created: 2025-09-13T09:59:36Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:12Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Incident Summary Report Intermittent SSLEOFError Investigation
type:
uid: 
updated: 
version:
---

This report provides a detailed, chronological breakdown of the investigation into an intermittent `SSLEOFError` that occurred on 13 September 2025. The issue involved a complex interaction between an Azure Kubernetes (AKS) client and an Amazon EKS server application, touching upon DNS, load balancing, Kubernetes networking, and cloud infrastructure state.

## **1. Executive Summary**

An intermittent `[SSL: UNEXPECTED_EOF_WHILE_READING]` error, reported by a client pod in the Azure `cuh-prod-1` cluster, was traced to a single, persistently faulty worker node (`i-0a3061a5b059d819c`) within the destination AWS EKS cluster. The `relay.codisc-eoe-sde.uk` DNS record resolved to two load balancer IPs, but connections to one (`13.43.164.137`) consistently failed.

The investigation systematically ruled out application code errors, conflicting Kubernetes Ingress and Service resources, AWS Load Balancer configuration, Security Groups, and Network ACLs. A parallel investigation also eliminated a `cert-manager` certificate renewal failure as the cause for this specific symptom.

The root cause was isolated to a faulty runtime state on the specific EC2 instance, which prevented the node's internal networking (`kube-proxy`) from correctly routing traffic from the Application Load Balancer (ALB) to the application pod. The issue was resolved by **terminating the faulty instance**, allowing the EKS Auto Scaling Group to provision a healthy replacement.

---

## **2. Initial Problem Description**

- **Service**: A client pod (`hutch-bunny-78fb4f57dc-xkp4p`) in the Azure `cuh-prod-1` cluster, running behind an explicit HTTP proxy (`http://10.252.142.180:8080/`).
- **Destination**: An API endpoint at `https://relay.codisc-eoe-sde.uk`, served by the `hutch-relay` application in the AWS `hie-prod-34` EKS cluster.
- **Symptom**: The client logged intermittent `SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol'))`. This error signifies that the TLS connection was abruptly closed by the server side without a proper shutdown handshake.
- **Key Clue**: The DNS `A` record for `relay.codisc-eoe-sde.uk` resolved to two public IP addresses. Diagnostic tests using `curl` and `openssl` from the Azure jumpbox quickly revealed that requests to one IP consistently failed, while requests to the other succeeded.

---

## **3. Investigation Chronology and Findings**

The investigation proceeded through several phases as we peeled back the layers of the infrastructure.

### **Phase 1: AWS Load Balancer and Kubernetes Service Conflicts**

The initial hypothesis focused on the AWS load balancing layer.

1. **Identify the Load Balancer**: We confirmed the public IPs belonged to an AWS Load Balancer. By inspecting the Kubernetes Service and Ingress objects in the `hutch` namespace of the EKS cluster, we initially encountered conflicting configurations. A `SyncLoadBalancerFailed...DuplicateListener` error in the AWS Load Balancer Controller logs pointed to a conflict between an `api-gateway-ingress` resource and a `hutch-relay-nlb` service of `type: LoadBalancer`. This was a red herring that was resolved by changing the service type to `ClusterIP`, but the intermittent `SSLEOFError` persisted.
2. **Identify the Correct Traffic Path**: Further investigation of the Terraform configuration in the `central-services` workspace revealed the true architecture: an Application Load Balancer named **`eoe-sde-codisc-relay-alb`** forwards traffic to a target group (`eoe-sde-codisc-relay-tg`). This target group was configured to send traffic to the EKS worker nodes on `NodePort` **32080**.
3. **Check Target Health**: We inspected the target group, which had two registered EC2 instances: **`i-0a3061a5b059d819c`** and **`i-0e32193c309a0eb8b`**. The ALB's health checks, which targeted the `/healthz` path defined in the Terraform [`aws_lb_target_group`](file:///Users/username/path/to/file.extension) resource, reported that **both target nodes were healthy**. This disproved the simple "unhealthy node" theory.

### **Phase 2: Kubernetes Pod Distribution and Application Health**

The hypothesis shifted: perhaps the application pod was faulty on one node, even if the node itself was healthy.

1. **Check Pod Distribution**: Listing pods in the EKS cluster revealed the `hutch-relay` deployment was only running one replica, which was scheduled on node `i-0e32193c309a0eb8b`. The other node (`i-0a3061a5b059d819c`) was receiving traffic from the ALB on port 32080 but had no pod to handle it.
2. **First Remediation Attempt**: The `hutch-relay` deployment was scaled to two replicas, which successfully scheduled a new pod onto the previously empty node.
3. **Error Persists**: Despite the fix, new client logs confirmed the intermittent `SSLEOFError` was still occurring.
4. **Check Application Logs**: We then checked logs for **both** `hutch-relay` pods. They were healthy, responding to health checks, and when successful, returning HTTP `204 No Content` as expected. This proved the application code was not the issue.
5. **Parallel Investigation (Ruled Out)**: During this time, we also diagnosed a critical but separate issue: `cert-manager` was failing to renew the `relay-tls-cert` due to a missing `cloudflare-issuer-api-token` secret in the `hutch` namespace. While this needed fixing, the fact that one IP path worked perfectly proved this was not the cause of this *specific* `SSLEOFError`.

### **Phase 3: Network Firewall Configuration**

With the application cleared, the focus shifted to a potential network block between the ALB and the failing node.

1. **Check Security Groups**: We found that both EKS nodes were using the **exact same security group**. This ruled out a security group misconfiguration, as it would have affected both nodes equally.
2. **Check Network ACLs (NACLs)**: We identified that the two nodes were in different subnets. We inspected the NACLs for both subnets and found they also used the **exact same, permissive NACL**, which allowed all required traffic. This eliminated NACLs as the cause.

### **Phase 4: Node Runtime State**

Having eliminated all logical configuration errors, the final hypothesis was an unrecoverable runtime fault on the failing node.

1. **Understanding the Final Hop**: Traffic from the ALB hits the `NodePort` (32080) on the EC2 instance. The `kube-proxy` service on that node is responsible for managing `iptables` (or `IPVS`) rules that forward this traffic to the pod's internal IP address.
2. **Second Remediation Attempt**: We attempted to reset the Kubernetes network routing on the failing node (`i-0a3061a5b059d819c`) by deleting the `kube-proxy` pod running on it. Kubernetes automatically recreated it, which should have rebuilt the networking rules.
3. **Final Finding**: You confirmed that restarting `kube-proxy` **did not** resolve the issue. This was the definitive evidence that the problem lay beneath Kubernetes's control—at the OS or networking stack level of the EC2 instance itself.
4. **Final Remediation**: The final and successful solution was to **terminate the faulty EC2 instance** (`i-0a3061a5b059d819c`). The EKS Auto Scaling Group automatically provisioned a new, healthy instance to replace it. All subsequent connectivity tests succeeded, fully resolving the error.

---

## **Root Cause**

The root cause was a **persistent, faulty state on a single EKS worker node (`i-0a3061a5b059d819c`)**. This fault specifically corrupted the node's internal network packet forwarding mechanism (managed by `kube-proxy`). As a result, traffic arriving on the `NodePort` was not being correctly translated and forwarded to the pod's IP, causing the connection to be dropped and resulting in the `SSLEOFError` at the client. The issue survived a `kube-proxy` restart, indicating the fault was at a lower level of the instance's OS or virtual networking stack.

Network error occurred: HTTPSConnectionPool(host='', port=443): Max retries exceeded with url: (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol
