---
captured: "2026-04-28T10:18:59+01:00 2026-04-28T10:18:59+01:00"
created: 2026-04-28T09:19:02+00:00
modified: 2026-05-26T11:44:26+00:00
source: "https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2256142353/Connectivity+Patterns+for+CUH+On-Premise+to+AWS+SDE"
status: "processing"
tags: ["input"]
title: HEAD Connectivity Patterns for CUH On-Premise to AWS SDE - FITFILE
type: "head"
---

## Raw Output / Content

## Connectivity Patterns for CUH On-Premise to AWS SDE

## 1\. Objective

This document evaluates the primary architectural patterns for establishing a secure, private, and compliant network connection between the Cambridge University Hospitals (CUH) on-premise network, secured by FortiGate firewalls, and the private AWS Secure Data Environment (SDE).

The evaluation of each option is based on four key criteria:

- Security & Compliance: How well the solution eliminates public attack surfaces and aligns with NHS and NCSC security principles.
- Performance: The expected latency, bandwidth, and reliability of the connection.
- Cost: The estimated monthly operational costs for UK-based infrastructure, broken down by fixed and variable charges.
- Complexity: The operational overhead required to implement and maintain the solution.

---

## 2\. Option 1: AWS Site-to-Site VPN

This is the standard, most common method for securely connecting an on-premise network to an AWS VPC. It creates an encrypted IPsec tunnel over your existing internet connection.

### How it Works

1. An AWS Virtual Private Gateway (VGW) is attached to your SDE's VPC. This acts as the VPN concentrator on the AWS side.
2. In AWS, a Customer Gateway resource is created, which points to the public IP address of your on-premise CUH FortiGate firewall.
3. An AWS Site-to-Site VPN Connection is created, linking the VGW and the Customer Gateway. This establishes two redundant IPsec tunnels for high availability.
4. The CUH FortiGate firewall is configured with the tunnel details provided by AWS (remote gateway IPs, pre-shared keys, etc.) to complete the connection.
5. Routes are added on both sides to direct traffic for the corresponding private networks through the encrypted tunnel.

### Security & Compliance Analysis

- Pros:
	- Eliminates Public Endpoints: Your AWS SDE services do not require public IP addresses. All communication happens over private IPs within the encrypted tunnel.
		- Strong Encryption: Uses industry-standard IPsec to encrypt all data in transit.
		- Meets Compliance: This architecture provides the "network protection" layer required by NCSC Principle 1, and by removing the public interface to the SDE, it fully aligns with NCSC Principle 11.
- Cons:
	- Traffic traverses the public internet, although it is fully encrypted.

### Performance Characteristics

- Bandwidth: Limited by the speed of your on-premise internet connection and the throughput of the FortiGate appliance.
- Latency: Subject to the variability and congestion of the public internet. It is not guaranteed.

### Cost Implications (UK Infrastructure)

This is the most cost-effective private connectivity option.

- Fixed Costs:
	- AWS Site-to-Site VPN Connection (UK): £0.04 per hour (approx. £29.20/month).
- Variable Costs:
	- AWS Data Transfer Out (from London to Internet): The first 100 GB/month are free. After that, it is £0.09 per GB for the next 9.999 TB.
- Example Monthly Cost (1 TB Data Out):
	- Connection Fee: £29.20
		- Data Transfer ((1024 GB - 100 GB) \* £ 0.09): ~ £ 83.16
		- Total Estimated AWS Cost: ~£29.20 + £83.16 per month

---

## 3\. Option 2: AWS Direct Connect

This is the premium, enterprise-grade solution for hybrid connectivity. It establishes a dedicated, private fibre-optic connection between the CUH data centre and AWS, completely bypassing the public internet.

### How it Works

1. A physical, private network circuit is provisioned from a third-party provider between the CUH data centre and an AWS Direct Connect location in the UK.
2. This circuit connects to a port on an AWS router. A Virtual Interface (VIF) is created on this connection.
3. The VIF is attached to the AWS Virtual Private Gateway on your SDE's VPC.
4. The CUH FortiGate is configured to peer with AWS over this private link using BGP (Border Gateway Protocol) to dynamically exchange routes.

### Security & Compliance Analysis

- Pros:
	- Maximum Security: Traffic never traverses the public internet, providing the highest level of isolation and confidentiality. This is the gold standard for meeting NCSC Principle 11.
		- Fully Compliant: Unquestionably meets all requirements for a secure, private connection under the DSPT and NCSC frameworks.
- Cons:
	- It is a point-to-point connection. A network outage on the physical link can cause a service disruption unless a backup is in place.

### Performance Characteristics

- Bandwidth: Dedicated and consistent, with options from 50 Mbps to 100 Gbps.
- Latency: Low and predictable, as it does not traverse the variable public internet.

### Cost Implications (UK Infrastructure)

This is the most expensive option, suitable for high-throughput or latency-sensitive workloads.

- Fixed Costs:
	- Third-Party Provider Circuit: This cost varies significantly based on the provider and location but can be substantial (hundreds to thousands of pounds per month). This is a separate, additional cost.
		- AWS Direct Connect Port Hour Fee (1 Gbps): £0.30 per hour (approx. £219/month).
- Variable Costs:
	- AWS Data Transfer Out (from Europe regions): Significantly cheaper than internet rates at £0.0282 per GB.
- Example Monthly Cost (1 TB Data Out):
	- Port Fee: $219
		- Data Transfer (1024 GB \* £ 0.0282): ~ £ 28.88
		- Total Estimated AWS Cost: ~£247.88/month (This excludes the significant third-party circuit cost).

---

## 4\. Option 3: AWS Direct Connect + VPN Backup (Highly Resilient)

This architecture combines the performance and security of Direct Connect with the redundancy of a Site-to-Site VPN, providing a highly available, fault-tolerant connection.

### How it Works

1. An AWS Direct Connect link is configured as the primary path for all traffic, as described in Option 2.
2. A separate AWS Site-to-Site VPN connection is configured in parallel, as described in Option 1.
3. BGP routing is configured on the CUH FortiGate to prefer the Direct Connect path. If the Direct Connect link fails, BGP will automatically re-route traffic over the backup VPN tunnel.

### Security & Compliance Analysis

- Pros:
	- Combines the maximum security of Direct Connect with the redundancy of a VPN.
		- Provides the highest level of assurance for maintaining connectivity to critical systems.
- Cons:
	- Incurs the costs and management overhead of both solutions.

### Performance Characteristics

- Primary Path (Direct Connect): High bandwidth, low latency.
- Backup Path (VPN): Lower bandwidth, higher latency. Performance will degrade during a failover event but service will remain available.

### Cost Implications (UK Infrastructure)

This is the most expensive option, as it combines the costs of the previous two solutions.

- Fixed Costs:
	- Third-Party Provider Circuit Cost
		- AWS Direct Connect Port Hour Fee (1 Gbps): ~ £ 219/month
		- AWS Site-to-Site VPN Connection Fee (UK): ~£29.20/month
- Variable Costs:
	- Data transfer is charged at the rate of the active path. In normal operation, this would be the cheaper Direct Connect rate (£ 0.0282/GB).
- Example Monthly Cost (1 TB Data Out, Normal Operation):
	- Port Fee: £219
		- VPN Fee: £29.20
		- Data Transfer: ~£28.88
		- Total Estimated AWS Cost: ~£247.88 + ~£29.20 per month (Excluding third-party circuit cost).

---

## 5\. Recommendation

<table><tbody><tr><td rowspan="1" colspan="1"><p>Feature</p></td><td rowspan="1" colspan="1"><p>Option 1: Site-to-Site VPN</p></td><td rowspan="1" colspan="1"><p>Option 2: Direct Connect</p></td><td rowspan="1" colspan="1"><p>Option 3: Direct Connect + VPN</p></td></tr><tr><td rowspan="1" colspan="1"><p><strong>Security Posture</strong></p></td><td rowspan="1" colspan="1"><p>✅ Strong (Private & Encrypted)</p></td><td rowspan="1" colspan="1"><p>✅ Strongest (Fully Private)</p></td><td rowspan="1" colspan="1"><p>✅ Strongest (Fully Private)</p></td></tr><tr><td rowspan="1" colspan="1"><p><strong>Performance</strong></p></td><td rowspan="1" colspan="1"><p>⚠️ Good (Variable Latency)</p></td><td rowspan="1" colspan="1"><p>✅ Best (Low, Predictable Latency)</p></td><td rowspan="1" colspan="1"><p>✅ Best (with Resilient Failover)</p></td></tr><tr><td rowspan="1" colspan="1"><p><strong>Cost (UK)</strong></p></td><td rowspan="1" colspan="1"><p>✅ Lowest (~£29 + $83 for 1TB)</p></td><td rowspan="1" colspan="1"><p>❌ Highest (~$248 for 1TB + Circuit)</p></td><td rowspan="1" colspan="1"><p>❌ Highest (~£29 + $277 for 1TB + Circuit)</p></td></tr><tr><td rowspan="1" colspan="1"><p><strong>Complexity</strong></p></td><td rowspan="1" colspan="1"><p>✅ Low</p></td><td rowspan="1" colspan="1"><p>⚠️ High (Requires Physical Circuit)</p></td><td rowspan="1" colspan="1"><p>❌ Highest</p></td></tr><tr><td rowspan="1" colspan="1"><p><strong>Compliance</strong></p></td><td rowspan="1" colspan="1"><p>✅ Meets NHS/NCSC Standards</p></td><td rowspan="1" colspan="1"><p>✅ Exceeds NHS/NCSC Standards</p></td><td rowspan="1" colspan="1"><p>✅ Exceeds NHS/NCSC Standards</p></td></tr></tbody></table>

- Recommended Starting Point: Option 1 (AWS Site-to-Site VPN). This solution is fully compliant with the required security standards, eliminates the public attack surface, and is the most cost-effective and fastest to implement. It provides the necessary network-level protection for handling patient data.
- Long-Term/Strategic Option: Option 3 (AWS Direct Connect + VPN Backup). If the workloads in the AWS SDE become critical and require guaranteed high-performance and maximum resilience, this is the gold-standard architecture. It should be considered the long-term strategic goal.

Related content
