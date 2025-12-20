---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
dependencies:
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
name: troubleshooting_guide
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: troubleshooting_guide
type: operational_guide
uid: 
updated: 
version:
---

## Private Deployment Troubleshooting Guide

### Common Issues and Resolution Steps

#### 1. Private Network Connectivity Issues

##### Symptom: Clusters Unable to Communicate Across Clouds

```bash
# Test connectivity between clusters
kubectl exec -it <pod-name> -- curl -v <service-endpoint>
# Connection times out or returns connection refused
```

Troubleshooting Steps:

1. Verify Express Route/Direct Connect status

```bash
# Azure
az network express-route show --name <circuit-name> --resource-group <rg>

# AWS
aws directconnect describe-connections
```

2. Check DNS resolution

```bash
# From Azure pod
kubectl exec -it <pod-name> -- nslookup <aws-endpoint>

# From AWS pod
kubectl exec -it <pod-name> -- nslookup <azure-endpoint>
```

3. Verify network security groups/security groups
   - Check Azure NSG rules
   - Verify AWS security group configurations
   - Ensure required ports are open

4. Validate route tables
   - Check UDRs in Azure
   - Verify AWS route tables
   - Confirm BGP propagation

#### 2. Container Registry Access Issues

##### Symptom: Unable to Pull Images from Central ACR

```bash
# Error in pod events
kubectl describe pod <pod-name>
# Shows ImagePullBackOff or ErrImagePull
```

Troubleshooting Steps:

1. Verify private endpoint connectivity

```bash
# Test DNS resolution
kubectl exec -it <pod-name> -- nslookup <acr-name>.azurecr.io

# Test network connectivity
kubectl exec -it <pod-name> -- curl -v <acr-name>.azurecr.io
```

2. Check authentication configuration
   - For AKS: Verify managed identity assignment
   - For EKS: Check IAM role configuration

```bash
# AKS
az aks show -n <cluster-name> -g <resource-group> --query "identityProfile"

# EKS
aws iam get-role --role-name <role-name>
```

3. Validate ACR access policies

```bash
# List ACR roles
az role assignment list --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ContainerRegistry/registries/<acr-name>
```

#### 3. Identity Federation Issues

##### Symptom: Authentication Failures Across Clouds

```bash
# Error in logs showing authentication failures
kubectl logs <pod-name>
# Shows unauthorized or authentication failed
```

Troubleshooting Steps:

1. Verify OIDC configuration

```bash
# EKS OIDC provider
aws eks describe-cluster --name <cluster-name> --query "cluster.identity"

# Azure AD app registration
az ad app show --id <app-id>
```

2. Check service account configuration

```bash
# Verify service account
kubectl describe serviceaccount <sa-name>

# Check pod identity binding
kubectl describe AzureIdentityBinding <binding-name>  # For AKS
kubectl describe ServiceAccount <sa-name>             # For EKS
```

3. Validate role assignments

```bash
# Azure RBAC
az role assignment list --assignee <principal-id>

# AWS IAM
aws iam list-attached-role-policies --role-name <role-name>
```

#### 4. Cross-Cloud DNS Resolution Problems

##### Symptom: DNS Resolution Failures

```bash
# Failed DNS lookup
kubectl exec -it <pod-name> -- nslookup <service-name>
# Shows NXDOMAIN or timeout
```

Troubleshooting Steps:

1. Check private DNS zone configuration

```bash
# Azure private DNS zones
az network private-dns zone list

# AWS Route53 private hosted zones
aws route53 list-hosted-zones
```

2. Verify DNS forwarder setup

```bash
# Check Azure DNS forwarder
az network private-dns link vnet list --zone-name <zone-name>

# Check Route53 resolver endpoints
aws route53resolver list-resolver-endpoints
```

3. Test DNS resolution path

```bash
# From pod
kubectl exec -it <pod-name> -- dig +trace <service-name>
```

### Common Resolution Patterns

#### Network Connectivity

1. Always start with DNS resolution tests
2. Then verify network path (traceroute where possible)
3. Check security group configurations
4. Validate routing tables

#### Authentication

1. Verify identity configuration
2. Check role/permission assignments
3. Validate service account setup
4. Test with minimal permissions

#### Container Registry

1. Test network connectivity
2. Verify DNS resolution
3. Check authentication configuration
4. Validate image path and tags

### Preventive Measures

1. Regular Health Checks

```bash
# Create monitoring pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
 name: network-test
spec:
 containers:
 - name: network-test
   image: busybox
   command:
EOF
```

2. Monitoring Setup
   - Configure alerts for network latency
   - Monitor DNS resolution times
   - Track authentication failures
   - Set up registry pull metrics

3. Documentation
   - Keep network diagrams updated
   - Document all security group changes
   - Maintain service dependency maps
   - Update DNS configuration changes

### Escalation Procedures

1. L1 Support
   - Basic connectivity testing
   - Log collection
   - Initial triage

2. L2 Support
   - Network path analysis
   - Security configuration review
   - Identity troubleshooting

3. L3 Support
   - Cross-cloud networking issues
   - Complex authentication problems
   - Performance optimization
