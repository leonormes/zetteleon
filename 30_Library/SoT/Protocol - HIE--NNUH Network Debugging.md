---
alias:
  - Connectivity Debugging
  - Kubernetes Network Debugging Protocol
  - Network Troubleshooting Checklist
aliases:
  - Protocol - HIE->NNUH Network Debugging
created: 2026-02-04T00:00:00+00:00
modified: 2026-02-06T19:31:21+00:00
tags:
  - aws
  - azure
  - debugging
  - kubernetes
  - networking
  - protocol
  - customer/nnuh
title: Protocol - HIE--NNUH Network Debugging
type: protocol
---

## Logic Map

- Objective: Systematically diagnose connectivity issues between clusters (e.g., EKS $\to$ AKS) or from public internet to ingress.
- Strategy: Divide and Conquer. Test from the _Source_ (Egress), then the _Destination Infrastructure_ (Cloud Network), then the _Destination Cluster_ (Kubernetes/Ingress).
- Prerequisites:
    - `kubectl` access to both clusters.
    - A `netshoot` pod running in the source cluster.
    - SSH access to a Jumpbox in the destination network (optional but recommended).
    - Reference: [[SoT - Network Debugging Tools & Patterns]]

---

## 1. Source Side: Verify Egress (From Netshoot)

_Run these inside a debug pod in the source cluster._

`kubectl run netshoot-test -i --tty --rm --image nicolaka/netshoot -- /bin/bash`

### A. Basic Connectivity

```bash
export TARGET_IP=195.171.151.154
# 1. Is ping actually sending? (Short timeout to detect hang vs packet loss)
ping -c 4 -W 1 ${TARGET_IP}

# 2. Do we have internet access? (Check NAT/Egress)
ping -c 4 8.8.8.8

# 3. What is my public egress IP? (For allowlisting)
curl -s ifconfig.me
```

### B. Protocol Specifics (TCP Vs ICMP)

_ICMP is often blocked. TCP is the source of truth._

```bash
# 4. Test TCP Connectivity (Port 443/80)
nc -vz -w 5 ${TARGET_IP} 443

# 5. Test HTTPS Handshake (Detailed verbose output)
curl -v --connect-timeout 5 https://${TARGET_IP}

# 6. Deep Dive: Why is it failing? (Filtered vs Closed)
# -Pn skips ping discovery. --reason shows why port is marked state.
nmap -Pn -p 80,443 --reason ${TARGET_IP}
```

### C. Packet Inspection (The "Truth Serum")

_Run this while executing the curl/nc command in another terminal._

```bash
# 7. Check if packets are actually leaving the pod
tcpdump -n -i any host ${TARGET_IP}
# Look for: Flags [S] (SYN sent). 
# No Reply = Dropped downstream. 
# Reply [R.] = Rejected (Closed port).
```

---

## 2. Destination Infrastructure: Azure/Cloud (From Jumpbox)

_Run these from a VM inside the destination VNet._

### A. Identify the Target

```bash
# 1. Who owns this Public IP? (Is it even ours?)
az network public-ip list --query "[?ipAddress=='${TARGET_IP}']"

# 2. List Load Balancers
az network lb list --output table
```

### B. Cloud Firewall/NSG Checks

```bash
# 3. Check Effective NSG Rules (Requires VM name)
az network nsg rule list --nsg-name ${AZ_NSG_NAME} --resource-group ${AZ_RESOURCE_GROUP} --output table

# 4. Check Azure Firewall Rules (If applicable)
az network firewall network-rule list --firewall-name ${AZ_FIREWALL_NAME} --resource-group ${AZ_RESOURCE_GROUP} --collection-name ${AZ_FW_RULE_COLLECTION}
```

---

## 3. Destination Cluster: Kubernetes Ingress (From Jumpbox/Local)

### A. Bypass Public Path (Test Internal Ingress)

_Confirm the app is healthy inside the VNet, ignoring public firewalls._

```bash
# 1. Hit the Internal Ingress Controller IP directly
# (Get IP from: kubectl get svc -n ${K8S_INGRESS_NAMESPACE})
nc -vz ${K8S_INTERNAL_INGRESS_IP} 443

# 2. Test TLS Handshake (Ignore cert errors)
curl -v -k https://${K8S_INTERNAL_INGRESS_IP}

# 3. Spoof the Host Header (The "Gold Standard" Test)
# Simulates real traffic without DNS/Public IP issues.
curl -v -k --resolve ${TARGET_HOSTNAME}:443:${K8S_INTERNAL_INGRESS_IP} https://${TARGET_HOSTNAME}
```

### B. Kubernetes Configuration (kubectl)

```bash
# 4. List all LoadBalancer services (Is it Public or Internal?)
kubectl get svc -A -o wide | grep -i loadbalancer

# 5. Check Service Annotations (Look for "service.beta.kubernetes.io/azure-load-balancer-internal")
kubectl get svc -n ${K8S_NAMESPACE} ${K8S_SERVICE_NAME} -o yaml

# 6. Map Ingress Rules to Backends (Machine Readable)
kubectl get ingress -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{":\n"}{range .spec.rules[*]}{"  "}{.host}{"\n"}{range .http.paths[*]}{"    "}{.path}{" -> "}{.backend.service.name}{":"}{.backend.service.port.number}{"\n"}{end}{end}{"\n"}{end}'

# 7. Check Backend Pods (Are they actually running?)
kubectl get endpoints -n ${K8S_NAMESPACE} ${K8S_SERVICE_NAME}
```

---

## 4. Decision Matrix (Interpretation)

| Test Result | Diagnosis | Next Action |
|:--- |:--- |:--- |
| `ping` fails, `nc` works | ICMP Blocked (Normal) | Ignore ping. Focus on TCP. |
| `nc` fails (Timeout) | Traffic Blackholed | Check NSGs, Firewalls, and Route Tables. |
| `nc` fails (Connection Refused) | Port Closed | Check Pod Health, Service Port mapping. |
| `curl --resolve` works, Public IP fails | Public Edge Issue | Check WAF, Public LB, or NAT rules. |
| `kubectl get endpoints` is empty | Service has no Pods | Check Pod Labels and Deployment status. |
