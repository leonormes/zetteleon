---
created: 2026-02-05T17:20:00Z
modified: 2026-02-05T18:36:27+00:00
status: permanent
tags: [aks, az-cli, azure, cheatsheet, kubectl, networking, troubleshooting]
title: Cheatsheet - Azure AKS Networking
---

This cheatsheet provides parameterized commands for common Azure AKS networking tasks, extracted from investigation logs involving NAT Gateways, DNAT/SNAT, and IP capacity planning.

## 1. Subnet & NAT Gateway Discovery

### Check NAT Gateway Association

```bash
az network vnet subnet show 
  --resource-group <RG> 
  --vnet-name <VNET> 
  --name <SUBNET> 
  --query "natGateway"
```

### Check Route Table Association

```bash
az network vnet subnet show 
  --resource-group <RG> 
  --vnet-name <VNET> 
  --name <SUBNET> 
  --query "routeTable"
```

### List All Subnets with NAT & RouteTable IDs

```bash
az network vnet subnet list 
  --resource-group <RG> 
  --vnet-name <VNET> 
  --query "[].{name:name, natGateway:natGateway.id, routeTable:routeTable.id}" 
  --output table
```

### Associate NAT Gateway to Subnet

```bash
az network vnet subnet update 
  --resource-group <RG> 
  --vnet-name <VNET> 
  --name <SUBNET> 
  --nat-gateway <NAT_GATEWAY_NAME_OR_ID>
```

---

## 2. AKS Outbound Configuration

### Check AKS Outbound Type

```bash
az aks show 
  --resource-group <RG> 
  --name <CLUSTER> 
  --query "networkProfile.outboundType"
```

### Update AKS Outbound Type

```bash
az aks update 
  --resource-group <RG> 
  --name <CLUSTER> 
  --outbound-type userAssignedNATGateway
```

### Discover Pod Subnet (Dynamic IP / Overlay info)

```bash
az aks show 
  --resource-group <RG> 
  --name <CLUSTER> 
  --query "networkProfile.{podCidr:podCidr, podCidrs:podCidrs, networkPlugin:networkPlugin, podSubnetId:podSubnetId}"
```

---

## 3. Connectivity Debugging (Pod Level)

### Run Netshoot Debug Pod

![[cmd-k8s-run-netshoot#⚡ Action]]

### Diagnostic Commands (Inside Pod)

```bash
# Check IP & Routing
ip addr show eth0
ip route show

# Test DNS & External Access
nslookup google.com
curl -v --connect-timeout 5 https://www.google.com
curl -v --connect-timeout 5 https://<TARGET_IP>

# Trace path
traceroute -n <TARGET_IP>
```

---

## 4. Security & Firewall Analysis

### List Outbound NSG Rules

```bash
az network nsg rule list 
  --resource-group <RG> 
  --nsg-name <NSG_NAME> 
  --query "[?direction=='Outbound'].{name:name, priority:priority, access:access, port:destinationPortRange, dest:destinationAddressPrefix}" 
  --output table
```

### Check Effective Routes (NIC Level)

Useful for seeing if a UDR is overriding the NAT Gateway.

```bash
az network nic show-effective-route-table 
  --resource-group <NODE_RESOURCE_GROUP> 
  --name <NIC_NAME> 
  --output table
```

### Create Azure Firewall DNAT Rule (Inbound)

```bash
az network firewall nat-rule create 
  --resource-group <FW_RG> 
  --firewall-name <FW_NAME> 
  --collection-name "InboundTraffic" 
  --name "Allow-HTTPS" 
  --protocols TCP 
  --source-addresses "<SOURCE_PUBLIC_IP>" 
  --destination-addresses "<FW_PUBLIC_IP>" 
  --destination-ports 443 
  --translated-address "<INTERNAL_LB_IP>" 
  --translated-port 443 
  --priority 100
```

---

## 5. IP Usage Auditing

### Count Nodes & Internal LBs

```bash
# Node Count
kubectl get nodes --no-headers | wc -l

# Internal Load Balancers (consuming VNet IPs)
kubectl get svc --all-namespaces -o json | jq '[.items[] | select(.spec.type=="LoadBalancer") | select(.metadata.annotations."service.beta.kubernetes.io/azure-load-balancer-internal"=="true")] | length'
```

### List All Services with Internal LB Annotation

```bash
kubectl get svc --all-namespaces -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,TYPE:.spec.type,INTERNAL:.metadata.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-internal"
```

### IP Masquerade Agent Check

```bash
kubectl get daemonset -n kube-system | grep ip-masq
kubectl get configmap -n kube-system azure-ip-masq-agent-config -o yaml
```

---

## 6. Calico Specifics

### Get Calico Policies

```bash
kubectl get networkpolicies -A
kubectl get globalnetworkpolicies -A
```
