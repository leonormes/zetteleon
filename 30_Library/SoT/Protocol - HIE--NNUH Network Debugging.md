---
alias:
- Connectivity Debugging
- Kubernetes Network Debugging Protocol
- Network Troubleshooting Checklist
aliases:
- Protocol - HIE->NNUH Network Debugging
created: 2026-02-04 00:00:00+00:00
modified: 2026-05-26 11:44:21+00:00
tags:
- aws
- azure
- customer/nnuh
- debugging
- kubernetes
- networking
- protocol
title: Protocol - HIE--NNUH Network Debugging
type: protocol
permalink: llmeon/30-library/so-t/protocol-hie-nnuh-network-debugging
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
curl -s ifconfig.me && echo
```

### B. Protocol Specifics (TCP Vs ICMP)

_ICMP is often blocked. TCP is the source of truth._

```bash
# 4. Test TCP Connectivity (Port 443/80)
nc -vz -w 5 ${TARGET_IP} 443

# 5. Test HTTPS Handshake (Detailed verbose output)
curl -v --connect-timeout 5 https://${TARGET_IP}
mtr -T -P 443 --report -c 10 ${TARGET_IP}
# 6. Deep Dive: Why is it failing? (Filtered vs Closed)
# -Pn skips ping discovery. --reason shows why port is marked state.
nmap -Pn -p 80,443 --reason ${TARGET_IP}
```

### Additional Tests to Run

1. Trace where your packets die—find the last hop that responds:

```bash
# TCP-specific traceroute on port 443 (more useful than ICMP traceroute here)
traceroute -T -p 443 -m 30 ${TARGET_IP}

# Also try mtr for a continuous view (run for ~10 seconds)
mtr -T -P 443 --report -c 10 ${TARGET_IP}
```

Why: This shows you exactly which network hop swallows your packets. Useful evidence to hand to whoever manages the firewall.

1. Test with SNI—some firewalls inspect TLS Client Hello and only allow traffic with the correct hostname:

```bash
curl -v --connect-timeout 5 --resolve nnuh-prod-1.fitfile.net:443:195.171.151.154 https://nnuh-prod-1.fitfile.net
```

Why: If the firewall does deep packet inspection, it might care about SNI. (Unlikely to help here since you can't even TCP-connect, but it's worth ruling out once the allowlist is in place.)

1. Check for an alternate port—sometimes gateways listen on non-standard ports:

```bash
nmap -Pn -p 22,80,443,6443,8443,8080 --reason ${TARGET_IP}
```

Why: If any port shows `closed` instead of `filtered`, the host is reachable but not listening there—that's a different problem from a firewall drop.

1. Confirm the egress IP is stable—if the cluster uses multiple NAT gateways:

```bash
for i in $(seq 1 5); do curl -s ifconfig.me; echo; sleep 1; done
```

Why: If the egress IP rotates (e.g. multiple NAT Gateways across AZs), you may need to allowlist a CIDR range, not just one IP.

---

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

---

## 5. Certificate & DNS Validation

### A. Cert-Manager Status (In-Cluster)

```bash
# 1. Check if the certificate is Ready
kubectl get certificate -n <namespace> <cert-name> -o wide

# 2. Inspect if the challenge is stuck (DNS-01 vs HTTP-01)
kubectl get challenges -n <namespace>
kubectl get orders -n <namespace>
```

### B. Remote TLS Verification (From Jumpbox/Netshoot)

```bash
# 3. Quick TLS Health Check (Issuer, SAN, Expiry)
openssl s_client -connect <hostname>:443 -servername <hostname> </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates -ext subjectAltName

# 4. Full Connectivity + Trust Check
curl -vI https://<hostname> 2>&1 | grep -E "Connected to|SSL connection|subject:|issuer:|expire|HTTP/"
```

### C. Split-Horizon Trace

Confirm the resolver path is correct for the environment:

```bash
# 5. Check iterative resolution path
dig +trace <hostname>

# 6. Check upstream resolver on Jumpbox
resolvectl status
```