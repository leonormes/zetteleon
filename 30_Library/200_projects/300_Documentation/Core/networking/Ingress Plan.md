---
aliases: []
confidence: 
created: 2025-03-28T09:57:44Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, ingress, networking]
title: Ingress Plan
type:
uid: 60b2c269-303d-4479-a771-13304f26532d
updated: 
version:
---

Items linked to [[FFAPP-3588] Private EKS: Expose relay APIs](https://fitfile.atlassian.net/browse/FFAPP-3588)[Gateway API](obsidian://adv-uri?vault=1cbfe518c4ad41d8&uid=21f1ae1a-dbbe-47ea-bf28-8645fa3ec6f1&filepath=300_Documentation%2FFITFILE%2FCore%2Fnetworking%2FGateway%20API.md)

[Ingress Plan](obsidian://adv-uri?vault=1cbfe518c4ad41d8&uid=60b2c269-303d-4479-a771-13304f26532d&filepath=000_inbox%2FIngress%20Plan.md)

[Overview | eks-private-sandbox | FITFILE-Platforms | HCP Terraform](https://app.terraform.io/app/FITFILE-Platforms/workspaces/eks-private-sandbox)

[test-sde-v2](hook://file/sRml74sTH?p=RGVwbG95L3NhbmRib3g=&n=test%2Dsde%2Dv2)

[FFAPP-5388](https://fitfile.atlassian.net/browse/FFAPP-3588)

- Get the current terraform off the jumpbox.
- Log in to aws to look at our cluster.
- Talk to cursor about the api gateway in Kubernetes.
- Find the ff-eoe-sde terraform code.
- Create the confluence docs for the plan of making relay accessible
- Find the actual deploy eoe terraform. This should be used to do the ff-dev-sde
- It is still a bit confusing as to what all the different deployments are. I need a consistent naming convention.
- I need centralise the deployment config so that if I make a change it goes to all the deployments.
- We have naming differences. the repo is hie-sde-v2 and the tfc workspace is
  I'll help you research and create a solution for securely exposing your AWS EKS service to Azure AKS using the Kubernetes Gateway API. Let me first examine your repository to understand the current setup.

## Cross-Cluster Service Exposure Using Kubernetes Gateway API

### Overview

This document outlines a solution for securely exposing the `relay` service running on AWS EKS to a remote Azure AKS cluster using the Kubernetes Gateway API. The solution leverages AWS Gateway API Controller to implement secure cross-cluster communication.

### Architecture

#### Components

1. **AWS EKS Cluster (Source)**

   - Existing EKS cluster with the `relay` service
   - AWS Gateway API Controller
   - VPC Lattice Service Network
   - Security groups and IAM roles

2. **Azure AKS Cluster (Target)**

   - Remote AKS cluster
   - Azure Gateway API Controller
   - Network policies
   - Service mesh (optional)

3. **Network Layer**
   - VPC Lattice for AWS side
   - Azure Virtual Network for AKS side
   - Cross-account/Cross-region networking

### Implementation Steps

#### 1. AWS EKS Setup

##### A. Install AWS Gateway API Controller

```hcl
# Add to your EKS module configuration
module "eks" {
  # ... existing configuration ...

  enable_gateway_api = true
  gateway_api_config = {
    service_network_name = "relay-network"
    service_name        = "relay"
    port               = 443
    protocol           = "HTTPS"
    tls_mode           = "TLS"
  }
}
```

##### B. Configure VPC Lattice Service Network

```hcl
resource "aws_vpclattice_service_network" "relay_network" {
  name = "relay-network"
  auth_type = "NONE"  # Can be configured for IAM auth if needed
}

resource "aws_vpclattice_service" "relay" {
  name = "relay"
  auth_type = "NONE"
  custom_domain_name = "relay.internal"
  service_network_identifier = aws_vpclattice_service_network.relay_network.id
}
```

#### 2. Gateway API Resources

##### A. Gateway Configuration

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
  name: relay-gateway
spec:
  gatewayClassName: aws
  listeners:
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
          - kind: Secret
            name: relay-tls
```

##### B. HTTPRoute Configuration

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: relay-route
spec:
  parentRefs:
    - name: relay-gateway
  hostnames: ["relay.internal"]
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: relay
          port: 443
```

#### 3. Security Configuration

##### A. Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: relay-network-policy
spec:
  podSelector:
    matchLabels:
      app: relay
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: azure-aks
      ports:
        - protocol: TCP
          port: 443
```

##### B. TLS Configuration

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: relay-cert
spec:
  secretName: relay-tls
  duration: 2160h
  renewBefore: 360h
  subject:
    organizations:
      - YourOrg
  commonName: relay.internal
  dnsNames:
    - relay.internal
```

### Security Considerations

1. **Network Security**

   - Use VPC Lattice for AWS side network isolation
   - Implement strict network policies
   - Enable TLS encryption for all traffic

2. **Authentication & Authorization**

   - Implement mTLS for service-to-service communication
   - Use IAM roles and service accounts
   - Configure RBAC for service access

3. **Monitoring & Observability**
   - Enable AWS CloudWatch metrics
   - Configure VPC Flow Logs
   - Set up alerting for security events

### Implementation Phases

#### Phase 1: Initial Setup

1. Install AWS Gateway API Controller
2. Configure VPC Lattice Service Network
3. Set up basic Gateway API resources

#### Phase 2: Security Implementation

1. Configure TLS certificates
2. Implement network policies
3. Set up monitoring

#### Phase 3: Azure Integration

1. Configure Azure AKS connectivity
2. Test cross-cluster communication
3. Implement monitoring and alerting

### Testing Strategy

1. **Unit Tests**

   - Test Gateway API configurations
   - Validate security policies
   - Verify TLS configurations

2. **Integration Tests**

   - Test cross-cluster communication
   - Validate security controls
   - Performance testing

3. **Security Tests**
   - Penetration testing
   - Network policy validation
   - TLS verification

### Monitoring & Maintenance

1. **Monitoring**

   - Set up CloudWatch dashboards
   - Configure alerts for:
     - Failed connections
     - TLS certificate expiration
     - Security policy violations

2. **Maintenance**
   - Regular certificate rotation
   - Security policy updates
   - Performance optimization

### Rollback Plan

1. **Quick Rollback**

   - Disable Gateway API resources
   - Revert network policies
   - Restore previous routing

2. **Emergency Procedures**
   - Contact list for security incidents
   - Incident response playbook
   - Backup communication channels

### Next Steps

1. Review and approve architecture
2. Create implementation timeline
3. Set up development environment
4. Begin phased implementation
5. Schedule security review

### References

1. [AWS Gateway API Controller Documentation](https://www.gateway-api-controller.eks.aws.dev/latest/concepts/concepts/)
2. [Kubernetes Gateway API Documentation](https://gateway-api.sigs.k8s.io/)
3. [AWS VPC Lattice Documentation](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html)

Would you like me to elaborate on any specific aspect of this solution or provide more detailed implementation steps for any particular component?
