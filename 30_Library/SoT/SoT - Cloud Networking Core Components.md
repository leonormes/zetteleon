---
aliases: ["Cloud Internet Connectivity", "Cloud Networking SoT", "Internet Gateway vs NAT Gateway", "Load Balancing"]
confidence: "5/5"
created: 2025-12-12T18:25:55Z
epistemic: "theory"
last_reviewed: "2025-12-23"
modified: 2025-12-28T09:56:11+00:00
purpose: "To define the essential networking components, architectural patterns, and load balancing strategies for cloud-native infrastructure."
review_interval: "6 months"
see_also: ["[[SoT - The Data Architecture of DNS]]", "[[SoT - The Data-Centric Theory of Networking]]"]
source_of_truth: []
status: "stable"
tags: ["aws", "azure", "cloud", "infrastructure", "networking"]
title: SoT - Cloud Networking Core Components
type: "SoT"
uid: 
updated: 
---

## 1. Connectivity Layers

Cloud networking requires three distinct layers to function:

1. **Gateway Device:** A bridge between private VNets and the public internet.
2. **Routing:** Explicit rules directing traffic to that gateway.
3. **Addressing:** Public IPs (identity) and NAT (translation).

---

## 2. Gateways (The Edge)

### A. Internet Gateway (Bidirectional)

- **Function:** Enables Ingress and Egress.
- **Use Case:** Public Web Servers, Load Balancers.

### B. NAT Gateway (Egress Only)

- **Function:** Performs Source NAT (SNAT), allowing private resources to initiate outbound connections without accepting inbound connections.
- **Use Case:** Private databases, application worker nodes.

---

## 3. Load Balancing & Abstraction

...

### B. Load Balancer Types

| Type | OSI Layer | Logic | Example |

|:--- |:--- |:--- |:--- |

| **Network (NLB)** | Layer 4 | Fast, packet-level forwarding based on IP/Port. | AWS NLB, Azure LB |

| **Application (ALB)** | Layer 7 | Content-aware; routes based on Headers, Cookies, or Path. | AWS ALB, Azure App Gateway |

| **Global (GSLB)** | DNS | Routes to nearest/healthiest region based on latency. | Route 53, Cloudflare |

| **Gateway (GWLB)** | Layer 3 | Transparently injects security/inspection appliances. | AWS GWLB |

---

## 4. Advanced Abstraction & Security

### A. API Gateway (The Entry Point)

- **Function:** Single entry point for microservices; handles auth, rate limiting, and protocol translation.
- **Key Requirement:** Must authenticate requests *before* routing to backend (e.g., JWT, API Key).

### B. Transit Gateway (The Hub)

- **Function:** Regional network hub connecting thousands of VPCs and on-premises networks.
- **Core Logic:** Uses a central hub-and-spoke model to eliminate complex peering relationships.

### C. Web Application Firewall (WAF)

- **Function:** Inspects Layer 7 traffic for OWASP Top 10 (SQLi, XSS).
- **Difference from Firewall:** Operates on application content, not just IP/Port.

### D. Content Delivery Network (CDN)

- **Function:** Caches static content at edge locations to reduce latency.
- **Logic:** "Cache Miss" triggers origin fetch; "Cache Hit" serves from edge.

---

## 5. Summary Matrix (Cloud Products)

| Concept | AWS Component | Azure Component |

|:--- |:--- |:--- |

| **Virtual Network** | VPC | VNet |

| **Public Gateway** | Internet Gateway (IGW) | Implicit (or Public IP on NIC/LB) |

| **Private Egress** | NAT Gateway | Azure NAT Gateway |

| **Layer 7 LB** | Application Load Balancer | Application Gateway |

| **Global LB / DNS** | Route 53 | Azure DNS / Traffic Manager |

| **API Management** | API Gateway | API Management (APIM) |

| **Network Hub** | Transit Gateway | Virtual WAN |

| **L7 Security** | AWS WAF | Azure WAF |

| **Edge Caching** | CloudFront | Azure CDN / Front Door |

| **DDoS Protection**| AWS Shield | Azure DDoS Protection |
