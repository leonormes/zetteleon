---
aliases: []
confidence: 
created: 2025-09-26T08:51:51Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:09Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: AWS SDE Audit recommendations
type:
uid: 
updated: 
version:
---

[[2025-09-26]]

## 1. Harden AWS Security Groups (SGs) 🛡️

Your primary line of defence at the infrastructure level can be significantly improved. The current rules are too open.

- **Problem:** The main **Cluster Security Group** (`sg-02dcb1a5bbe8844b8`) allows inbound traffic from the entire internet (`0.0.0.0/0`) on the NodePorts `31139` (HTTP) and `32623` (HTTPS). These ports are used by your `ingress-nginx-controller` service.
- **Risk:** This configuration exposes the TCP ports of the NGINX Ingress controller on **every worker node** directly to the internet. While traffic still needs to pass through the NLB, it bypasses the intended single point of entry and unnecessarily increases the attack surface of each node.
- **Recommendation:** You should restrict the source of these ingress rules. Instead of `0.0.0.0/0`, you should lock them down to the **IP addresses of the AWS Network Load Balancer** (`a09b6c067806443db8a14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com`). This ensures that only the load balancer can send traffic to the nodes on these ports, creating a more controlled and secure ingress path.

---

## 2. Implement Granular Network Policies Segmentation

You are using Calico, which provides the capability for robust network policies, but the current policies are not being used to their full potential.

- **Problem:** The Kubernetes Network Policies currently active in namespaces like `hie-prod-34`, `hutch`, and `spicedb` allow ingress traffic from **any source** (`From: <any>`) within the cluster to critical services like PostgreSQL, MongoDB, and Minio.
- **Risk:** This means that a compromise in *any pod* in *any namespace* could potentially lead to an attack on your databases. For example, a vulnerability in the `reflector` pod could be exploited to connect directly to the `hie-prod-34-postgresql` database, because no network policy prevents it.
- **Recommendation:** Implement **zero-trust networking** by making your policies more granular. Instead of allowing traffic from any pod, use `podSelector` and `namespaceSelector` to define exactly which applications are allowed to communicate.
  - **Example:** The `hie-prod-34-postgresql` Network Policy should be updated to only allow ingress from pods with the label `app=hie-prod-34-ffcloud-service`. This would prevent any other pod in the cluster from even attempting to connect to the database.

---

## 3. Enhance Defense-in-Depth with Network ACLs (NACLs) 🏰

While SGs are your primary firewall, NACLs offer an additional, stateless layer of security.

- **Problem:** The NACL (`acl-0b059cc861528dc9f`) associated with your cluster subnets has a simple "allow all" rule for both inbound and outbound traffic.
- **Risk:** This offers no secondary protection. If a Security Group rule is accidentally misconfigured to be too permissive, the NACL will not prevent unwanted traffic from reaching your nodes.
- **Recommendation:** For a stronger defense-in-depth posture, consider implementing stricter NACL rules. For your **private subnets**, you could restrict ingress to only allow traffic from within your VPC CIDR (`10.65.0.0/20`) and restrict egress to only the NAT Gateway. For the **public subnet**, you could explicitly allow inbound traffic only on ports 80 and 443. This adds a valuable layer of protection against misconfiguration.

---

## 4. Address Pod and Controller Stability 🛠️

Unstable components can sometimes mask or lead to security vulnerabilities.

- **Problem:** The audit log shows that the `compliance-benchmarker` pods in the `tigera-compliance` namespace are restarting constantly (over 700 times) due to failed liveness probes. Additionally, the `reflector` pod has been `OOMKilled` and restarted 27 times.
- **Risk:** While not a direct network configuration issue, constantly crashing pods indicate instability. This can impact reliability and, in some cases, create opportunities for exploitation during a pod's startup or shutdown phases. It also creates noise that could obscure logs from a real security event.
- **Recommendation:** You should investigate the root cause of these restarts. The `compliance-benchmarker` issue is likely a misconfiguration in the Tigera Calico Enterprise components. The `reflector` pod being `OOMKilled` indicates it needs its memory limits and requests adjusted to handle its workload. Stabilising these components is a good operational and security practice.
