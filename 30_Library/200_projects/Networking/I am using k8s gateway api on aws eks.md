---
aliases: []
confidence: 
created: 2025-04-04T09:13:36Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [gateway, networking]
title: I am using k8s gateway api on aws eks
type: 
uid: 
updated: 
version: 
---

## I Am Using k8s Gateway Api on Aws Eks. <https://www.gateway-api-controller.eks.aws.dev/latest/>

I want to do the same thing on Azure AKS. It seems to use an application gateway which adds £250 a month to the cost. AWS doesn't seem to add this much. Why is this? Am I looking at the wrong option? How can I use Gateway API on Azure AKS without the extra cost?

The cost difference stems from Azure's Application Gateway pricing model compared to AWS's approach with the VPC Lattice controller. Here's a detailed breakdown and alternative solutions:

---

### Cost Analysis: AWS Vs Azure

**AWS EKS Gateway API Setup**

- Uses free open-source controller ([AWS Gateway API Controller](https://www.gateway-api-controller.eks.aws.dev/latest/))[^1]
- Only pays for EKS cluster (\$0.10/hr) + compute/storage[^2]
- No additional gateway service fees

**Azure AKS Gateway API Setup**

- Default implementation uses **Azure Application Gateway** (V2 SKU)
- Fixed cost: ~\$0.246/hr (\$179.58/month) regardless of traffic[^3]
- Variable costs for capacity units (~\$0.008/hr per unit)[^3]
- Total ≈ £250/month due to mandatory fixed fees

---

### Why the Price Difference

1. **Managed Service vs Open Source**
Azure Application Gateway is a fully managed L7 load balancer with WAF, while AWS's solution uses an open-source controller with VPC Lattice (no extra managed service).
2. **High Availability Requirements**
Azure charges fixed fees even with 0 instances to guarantee HA, whereas AWS offloads HA to Kubernetes.

---

### Cost-Effective Alternatives for AKS

#### Option 1: Open-Source Ingress Controllers

| Solution | Cost Impact | Implementation Steps |
| :-- | :-- | :-- |
| **NGINX Ingress** | Only node compute costs | 1. Deploy [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/) <br> 2. Use with Azure Basic Load Balancer (free) |
| **HAProxy** | Node compute costs | 1. Install via Helm <br> 2. Configure with Kubernetes Gateway API CRDs |

#### Option 2: Service Mesh Ingress

- **Linkerd** or **Istio**: Free/open-source, but requires compute resources
- Example cost for 3 nodes: ~\$150/month (vs £250 for App Gateway)

#### Option 3: Azure Front Door + API Management

- **Front Door**: Global CDN with DDoS protection (~\$0.075/GB)
- **API Management**: Pay-per-use tier (~\$0.019/request)[^4]
- Combined cost typically < £100/month for moderate traffic

---

### Steps to Implement Gateway API on AKS Without Application Gateway

1. **Install Gateway API CRDs**:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
```

2. **Deploy NGINX Controller**:

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-sku"=basic
```

3. **Configure Gateway Resource**:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: aks-gateway
spec:
  gatewayClassName: nginx
  listeners:
  - protocol: HTTP
    port: 80
```

---

### Key Recommendations

- Use **NGINX/HAProxy** with Azure Basic LB for lowest cost
- Avoid Application Gateway V2 unless required for WAF features
- Monitor capacity units if using autoscaling[^3]
- Compare with AWS: Azure's solution adds ~£250/month for managed L7 features, while AWS offloads this to cluster resources

This approach aligns with Netflix's multi-cloud strategy of using platform-native solutions where cost-effective[^4], while maintaining Kubernetes API consistency.
