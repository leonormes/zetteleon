---
aliases: []
confidence: 
created: 2025-10-25T17:39:12Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:54Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Hybrid Cloud Networking Security
type:
uid: 
updated: 
version:
---

## **Azure ExpressRoute Hybrid Networking: Connectivity, Security, and Isolation**

### **1\. Introduction**

Connecting on-premises networks securely and reliably to cloud environments presents significant challenges. Hybrid cloud networking, particularly involving private routing between distinct network domains, involves intricate configurations, specialized terminology, and numerous components that must operate in concert. Ensuring data privacy, maintaining security postures across environments, and providing performant connectivity are paramount concerns for organizations adopting cloud services like Microsoft Azure.1

Azure ExpressRoute is a cornerstone service designed to address these challenges. It provides a mechanism for establishing private, dedicated connections between an organization's on-premises infrastructure, or colocation facilities, and the Microsoft cloud, bypassing the public internet entirely.3 This private pathway offers enhanced reliability, potentially faster speeds, and more consistent latencies compared to typical internet-based connections like Site-to-Site VPNs.1

This report provides a comprehensive technical analysis of Azure ExpressRoute within the context of hybrid networking. It examines how ExpressRoute establishes private connectivity, exploring the resulting network topology, routing behaviors, and crucial address space considerations. It evaluates whether this connection effectively unifies the on-premises and Azure networks or maintains them as distinct entities with private interconnectivity. Furthermore, the report investigates common models and Azure services for implementing secure internet access for Azure resources within this hybrid setup. Different strategies for routing internet-bound traffic and their security implications are analyzed. Crucially, the report details security best practices and technical controls specifically designed to isolate on-premises infrastructure from internet exposure when connected via ExpressRoute. The distinct roles of ExpressRoute peering types (Private Peering and Microsoft Peering) are clarified, along with definitions of key technical concepts. Finally, the findings are synthesized to compare the ExpressRoute-connected model with a single private network and to summarize recommended approaches for secure internet integration and robust on-premises isolation. Understanding these elements is vital for architects and engineers tasked with building secure, scalable, and high-performing hybrid cloud solutions on the Azure platform.

### **2\. Azure ExpressRoute: Establishing Private Connectivity**

Azure ExpressRoute facilitates dedicated, private network connections between an organization's physical infrastructure and Microsoft's global network, forming a critical component of many hybrid cloud strategies.

#### **2.1 Mechanism of ExpressRoute Circuits**

An ExpressRoute circuit represents a logical connection between the customer's network edge and the Microsoft cloud, facilitated through a connectivity provider.7 Unlike internet-based connections, ExpressRoute traffic does not traverse the public internet, offering a private path.3 This connection is identified by a unique Service Key (s-key), a GUID used for coordination between the customer, the provider, and Microsoft.7

Fundamental to ExpressRoute's design is inherent redundancy for high availability. Each circuit physically comprises two independent connections terminating on two separate Microsoft Enterprise Edge (MSEE) routers within the chosen peering location.6 This dual-path architecture is designed to tolerate failures on a single link or MSEE device. However, achieving this high availability requires configuring redundant Border Gateway Protocol (BGP) sessions across both connections.7 While this standard setup provides resilience against failures *within* a single peering location, it does not inherently protect against a complete site outage. For site diversity and protection against location-wide failures, organizations must implement more advanced architectures, such as using ExpressRoute Metro circuits connecting to two distinct peering locations within the same metropolitan area, or deploying geographically diverse circuits connecting to different peering locations altogether.8

#### **2.2 Connectivity Models**

Organizations can establish ExpressRoute connectivity through several distinct models, depending on their existing infrastructure and requirements 11:

1. **CloudExchange Colocation:** If an organization's infrastructure is colocated in a facility hosting a cloud exchange, they can order virtual cross-connections to Azure through the exchange provider. This typically involves Layer 2 or managed Layer 3 connections within the facility.11  
2. **Point-to-Point Ethernet Connection:** Service providers can offer dedicated Layer 2 Ethernet links directly connecting an organization's datacenters or offices to the Microsoft cloud.11  
3. **Any-to-Any (IPVPN) Networks:** Organizations with existing MPLS VPN WANs can integrate Azure into their private network. The IPVPN provider interconnects the customer's WAN with the Microsoft cloud, making Azure appear as another site on the WAN, typically using managed Layer 3 connectivity.11  
4. **ExpressRoute Direct:** This model allows organizations to connect directly to Microsoft's global network at peering locations using high-bandwidth ports (dual 10 Gbps or 100 Gbps).4 It bypasses traditional connectivity providers, offering greater control and scale, suitable for scenarios like massive data ingestion or industries requiring physical isolation.6

The choice of model influences factors like deployment complexity, cost structure, and the degree of routing management undertaken by the customer versus the provider.7 For instance, Layer 2 models (Colocation, Point-to-Point) often necessitate customer management of the BGP routing layer, whereas Layer 3 models (IPVPN) typically involve provider-managed routing. ExpressRoute Direct offers the most control but demands significant infrastructure and expertise from the customer.12

#### **2.3 Resulting Network Topology and Routing (BGP)**

Regardless of the connectivity model, ExpressRoute relies on the Border Gateway Protocol (BGP) to dynamically exchange routing information between the customer's on-premises network and Azure.6 BGP is the standard routing protocol used across the internet and private WANs to determine reachability between different networks (Autonomous Systems).

For each configured peering type (Private and Microsoft, discussed later), separate and redundant BGP sessions must be established over the dual physical links of the ExpressRoute circuit.7 Through these BGP sessions, the on-premises network advertises its reachable IP address prefixes (routes) to Azure, and conversely, Azure (via the ExpressRoute Virtual Network Gateway) advertises the VNet address spaces to the on-premises network.13 This dynamic exchange allows both networks to learn how to reach destinations in the other network over the private ExpressRoute path. If network segments are added or removed on either side, BGP automatically propagates these updates, eliminating the need for manual static route configuration in many cases.13

The resulting topology establishes a private path: On-Premises Edge Routers → Connectivity Provider Network (or Direct Connection) → Microsoft Enterprise Edge Routers (MSEEs) → Azure Backbone → ExpressRoute Virtual Network Gateway → Azure Virtual Network.

BGP is central to ExpressRoute's function, enabling the dynamic routing essential for hybrid connectivity. However, it introduces configuration complexity, requiring careful management of Autonomous System Numbers (ASNs), peering IP addresses, and advertised prefixes. Exceeding advertised prefix limits, for instance, can lead to BGP session drops and connectivity loss.9

#### **2.4 Address Space Considerations**

Proper IP address planning is crucial for successful ExpressRoute deployment. Several distinct address spaces are involved:

1. **BGP Peering Subnets:** Dedicated subnets are required solely for establishing the BGP sessions between the customer/provider edge routers and the MSEEs. For IPv4, this is typically a /29 subnet (split into two /30s) or two separate /30 subnets. For IPv6, it's a /125 (split into two /126s) or two /126 subnets. These subnets can use either private or public IP addresses, but must not overlap with Azure VNet address spaces.9 The first usable IP in each /30 or /126 is typically assigned to the customer/provider router, and the second to the Microsoft router.9  
2. **On-Premises and Azure VNet Address Spaces (Private Peering):** The private IP address ranges used within the on-premises network and the Azure Virtual Networks connected via Private Peering *must not overlap*.7 Overlapping address spaces prevent routing ambiguity and are a common cause of hybrid connectivity failures. Careful planning, potentially involving Network Address Translation (NAT) on the on-premises side, might be required if overlaps exist.18  
3. **Public IP Addresses (Microsoft Peering):** Microsoft Peering requires the use of public IP addresses owned by the customer or their connectivity provider. These public IPs are needed for the BGP peering subnets and also for NAT pools used to translate source IP addresses from the on-premises network when accessing Microsoft public services.7 These public prefixes must be registered in public routing registries, and Microsoft performs validation before activating the peering.9

Failure to plan and allocate non-overlapping private IP spaces and properly registered public IP spaces (for Microsoft Peering) can significantly impede or completely block an ExpressRoute deployment.

### **3\. ExpressRoute-Connected Networks: Unified or Interconnected?**

A common question arises regarding the nature of the network created by connecting on-premises infrastructure to Azure via ExpressRoute: Does it function as a single, unified private network? While ExpressRoute provides seamless private connectivity, understanding the distinction between a truly unified network and an interconnected system of distinct networks is crucial.

#### **3.1 Analysis: Logical Integration vs. Distinct Networks**

ExpressRoute Private Peering undoubtedly creates a high degree of integration. It extends the reachability of the on-premises network into Azure Virtual Networks (VNets) using private IP addressing.7 Resources like Azure Virtual Machines (VMs) within a connected VNet can communicate directly with on-premises servers (and vice versa) using their private IPs, subject to firewall rules and Network Security Groups (NSGs).7 This direct private IP communication often makes the combined environment *feel* like a single, extended network.7

However, despite this seamless connectivity, the on-premises network and the Azure VNet remain fundamentally distinct logical and administrative entities.7 They operate under separate management planes (on-premises network management tools vs. Azure portal/APIs). Security controls are domain-specific; on-premises firewalls manage traffic entering/leaving the physical site, while Azure NSGs and Azure Firewall govern traffic within and into/out of the VNet.1 Furthermore, the requirement for non-overlapping IP address spaces between the connected on-premises ranges and Azure VNets underscores their nature as separate networks being interconnected, rather than a single merged address space.9 DNS resolution might also need specific configuration to work seamlessly across both environments.18

#### **3.2 Practical Implications and Management Differences**

Treating the hybrid environment as a single, unified network can lead to operational challenges and potential security vulnerabilities. Key practical differences include:

- **Security Policy Management:** Security policies must be defined and enforced independently in each environment. An allow rule on an on-premises firewall does not automatically permit traffic through an Azure NSG, and vice versa. Centralized management tools like Azure Firewall Manager can help manage Azure policies, but coordination with on-premises security management is still required.21  
- **Routing Control:** Network traffic flow is not implicitly unified. It is explicitly controlled through BGP route advertisements exchanged over the ExpressRoute peerings and potentially modified within Azure using User Defined Routes (UDRs).13 Understanding BGP attributes (like AS Path, Local Preference) and Azure route precedence (UDR \> BGP \> System Route) is necessary for managing traffic paths.25  
- **Troubleshooting:** Diagnosing connectivity issues requires understanding the boundaries and tools specific to each domain (e.g., on-premises router logs, provider tools, Azure Network Watcher, NSG flow logs).22  
- **Asymmetric Routing:** Particularly with configurations involving both ExpressRoute and internet paths (or multiple ExpressRoute circuits), careful route management is needed to prevent asymmetric routing, where traffic takes one path in one direction and a different path back, which can be problematic for stateful devices like firewalls.9

Assuming implicit policy application or routing behavior based on the "single network" perception can result in unexpected traffic blocking or security gaps. Recognizing the distinct nature of the networks, while leveraging the powerful interconnection provided by ExpressRoute, leads to more robust and secure designs.

#### **3.3 Table: Comparison of Single Private Network vs. ExpressRoute Hybrid Network**

To further clarify the differences, the following table compares key characteristics:

| Feature | Single On-Premises Network | ExpressRoute Hybrid Network |
| :---- | :---- | :---- |
| **Management Plane** | Unified (e.g., local network management tools) | Distributed (On-prem tools \+ Azure portal/API/CLI) |
| **IP Addressing** | Single, potentially overlapping private space | Requires non-overlapping private IP spaces between on-prem and Azure VNets 18 |
| **Routing Control** | Typically internal routing protocols (OSPF, EIGRP) | BGP for inter-network routing; Azure system routes & UDRs within VNets 13 |
| **Security Boundaries & Policy** | Primarily perimeter firewalls, internal segmentation | Separate boundaries: On-prem firewalls, Azure NSGs, Azure Firewall/NVAs 1 |
| **Latency Profile** | Low internal latency | Low VNet latency; ER adds latency based on distance to peering location 28 |
| **Cost Model** | Primarily CapEx (hardware) \+ OpEx (power, cooling) | Azure consumption costs (ER circuit, gateway, data egress) \+ On-prem/Provider costs 4 |
| **Scalability/Flexibility** | Limited by physical infrastructure | Cloud scalability benefits (VNet size, resources) \+ ER bandwidth options 3 |

This comparison highlights that while ExpressRoute enables deep integration, the resulting hybrid environment requires managing two interconnected but distinct network domains with their own specific configurations, controls, and considerations.

### **4\. Implementing Secure Internet Access**

By default, resources within an Azure Virtual Network (VNet) can initiate outbound connections to the internet.3 While convenient for some scenarios, this default behavior is often unacceptable in enterprise environments due to security policies requiring inspection, filtering, and logging of all internet-bound traffic. In a hybrid setup with ExpressRoute, controlling internet egress from Azure resources becomes a critical security consideration to protect both cloud workloads and the connected on-premises network.

#### **4.1 Internet Egress Models: Centralized vs. Distributed vs. Forced Tunneling**

Several architectural patterns exist for managing internet egress from Azure VNets in a hybrid environment:

1. **Centralized Egress from Azure:** This is a common approach, often implemented using a Hub-and-Spoke topology.2 All internet-bound traffic originating from spoke VNets (containing workloads) is routed to a central hub VNet. This hub VNet typically hosts shared security services, such as Azure Firewall or a cluster of Network Virtual Appliances (NVAs), which inspect and filter the traffic before allowing it to the public internet.1  
   - *Advantages:* Centralized policy management, simplified auditing, consistent security posture for all spokes.  
   - *Disadvantages:* The central hub can become a performance bottleneck, potentially introduces a single point of failure (mitigated by HA design of firewall/NVAs), and may add latency for spoke-to-internet traffic compared to direct egress.  
2. **Distributed Egress from Azure:** In this model, individual spoke VNets or logical groups of spokes are provided with their own path to the internet. This can be achieved using resources like Azure NAT Gateway deployed in spoke subnets or dedicated NVAs within spokes.1  
   - *Advantages:* Better scalability, potentially lower latency as traffic doesn't traverse the hub, avoids hub bottleneck issues.  
   - *Disadvantages:* Decentralized security policy management (increases complexity and risk of inconsistency), potentially higher costs due to duplicated resources, more complex auditing.  
3. **Centralized Egress via On-Premises (Forced Tunneling):** This model redirects *all* traffic originating from Azure VNets, including traffic destined for the internet, back to the organization's on-premises network via the ExpressRoute Private Peering connection (or a Site-to-Site VPN).26 Internet access is then controlled and inspected by existing on-premises security infrastructure (firewalls, proxies).  
   - *Advantages:* Leverages existing on-premises security investments and policies, provides maximum control and visibility using familiar tools.  
   - *Disadvantages:* Significantly increases traffic load on the ExpressRoute circuit and on-premises edge infrastructure, introduces latency for internet-bound traffic, can break Azure services that require direct internet access 26, creates reliance on on-premises infrastructure availability for Azure internet connectivity.

The selection between these models involves critical trade-offs. Centralized egress from Azure offers a balance of control and cloud-native integration. Distributed egress prioritizes scalability and performance but sacrifices centralized management. Forced tunneling provides the highest level of control via existing on-prem systems but at the cost of performance, increased dependency, and potential compatibility issues. The choice depends heavily on the organization's security policies, risk tolerance, performance requirements, operational capabilities, and cost constraints.

#### **4.2 Azure Services for Secure Egress**

Azure provides several services to facilitate secure internet egress:

- **Azure Firewall:** A managed, cloud-native, stateful firewall service offered in Basic, Standard, and Premium tiers.22 It provides L3-L7 filtering, threat intelligence feeds (alerting or blocking malicious IPs/domains), FQDN filtering in application rules, and network rule capabilities.23 The Premium tier adds advanced features like TLS inspection and signature-based Intrusion Detection and Prevention System (IDPS).22 Azure Firewall Manager enables centralized policy management across multiple firewalls and hubs.23 It's designed to inspect both north-south (internet/on-prem to VNet) and east-west (VNet-to-VNet) traffic.22 It is a common choice for implementing centralized egress in hub-spoke topologies.26  
- **NAT Gateway:** A fully managed and highly resilient Network Address Translation (NAT) service.30 It allows instances in a private subnet to initiate outbound connections to the internet using one or more static public IP addresses or prefixes assigned to the NAT Gateway resource.30 Its primary benefits are providing scalable outbound connectivity, preventing SNAT port exhaustion issues common with default outbound access or load balancers, and offering a predictable source IP for egress traffic.30 NAT Gateway takes precedence over other outbound methods like load balancer outbound rules or instance-level public IPs when associated with a subnet.30 However, it only supports TCP and UDP protocols (ICMP is not supported) and cannot be deployed in the GatewaySubnet used by VPN or ExpressRoute gateways.30 It's often used in distributed egress models or alongside Azure Firewall for specific outbound NAT requirements.  
- **Network Virtual Appliances (NVAs):** These are virtual machines running networking software, typically from third-party vendors (e.g., firewalls, routers, WAN optimizers), available through the Azure Marketplace.1 NVAs offer feature parity with on-premises appliances, providing familiarity and advanced capabilities not always present in native Azure services.1 They can be deployed in various ways, including via Azure Managed Applications or vendor-specific orchestration tools.34 Azure Route Server can simplify dynamic routing integration with NVAs that support BGP, reducing the need for extensive manual UDR management.35 The main drawback is that the customer is responsible for managing the NVA lifecycle, including deployment, high availability, scaling, patching, and licensing.1

#### **4.3 Internet Traffic Routing Strategies**

Implementing the chosen egress model relies heavily on controlling network routing within Azure:

- **User Defined Routes (UDRs):** UDRs are essential for overriding Azure's default system routes and directing traffic according to the desired architecture.25 In a centralized egress model, UDRs are applied to spoke subnets. A common UDR directs all internet-bound traffic (represented by the 0.0.0.0/0 prefix) to the private IP address of the Azure Firewall or NVA instance located in the hub VNet.26  
- **Border Gateway Protocol (BGP):** BGP plays a crucial role, especially in forced tunneling scenarios. When forced tunneling is configured, the on-premises network advertises the default route (0.0.0.0/0) to Azure via BGP over the ExpressRoute Private Peering (or VPN).13 This BGP route instructs Azure resources to send all traffic not matching a more specific route back to the on-premises network.  
- **Route Precedence:** Understanding how Azure selects a route is critical when multiple routing sources exist. Azure uses the longest prefix match first. If multiple routes have the same prefix match, Azure prioritizes routes in the following order: UDR \> BGP learned route \> System route.25 This means a UDR explicitly defined on a subnet will always take precedence over a BGP route learned from ExpressRoute or a default system route. This precedence is vital for ensuring traffic flows as intended, for example, ensuring a UDR directs traffic to Azure Firewall even if a default route is learned via BGP. A specific consideration arises with Azure Firewall in forced tunneling scenarios: if the Firewall subnet itself learns the default BGP route back to on-premises, the Firewall might lose the direct internet connectivity it needs for updates and threat intelligence feeds. To counteract this, a specific UDR can be applied to the AzureFirewallSubnet or AzureFirewallManagementSubnet with an address prefix of 0.0.0.0/0 and a next hop type of Internet to ensure the firewall maintains its necessary outbound path.26  
- **Azure Firewall Policies:** While UDRs and BGP handle the *path* of the traffic, Azure Firewall Policies define the *rules* applied by the Azure Firewall.33 These policies contain rule collections (Network, Application, DNAT) that specify allowed or denied traffic based on source/destination IP, port, protocol, FQDNs, etc..33  
- **Azure Virtual Network Manager:** For complex environments with numerous VNets and routing requirements, Azure Virtual Network Manager offers capabilities to define routing intent and automate the creation and management of UDRs across network groups, potentially simplifying configuration.36

#### **4.4 Table: Comparison of Internet Egress Models**

| Feature | Centralized Azure Firewall/NVA | Distributed NAT GW/NVA | Forced Tunneling via ER/VPN |
| :---- | :---- | :---- | :---- |
| **Implementation** | Hub VNet with Azure Firewall/NVA cluster, UDRs on spokes | NAT Gateway or NVA per spoke/group, local UDRs if needed | BGP advertisement of 0.0.0.0/0 from on-prem over ER/VPN 31 |
| **Management** | Centralized policy/rule management 29 | Decentralized policy/rule management | Managed by on-premises security infrastructure |
| **Security Control Pt** | Azure Firewall/NVA in Hub VNet 1 | NAT GW (outbound only) or NVA in Spoke VNet | On-premises edge firewalls/proxies |
| **Performance Impact** | Potential hub bottleneck, added latency for spoke-internet | Lower latency (direct path), scalable 30 | Increased ER/VPN load, high latency for internet 31 |
| **Cost Factors** | Firewall/NVA cost, Hub VNet cost, data processing | NAT GW/NVA cost per instance, data processing | Increased ER/VPN bandwidth cost, on-prem infra cost |
| **Typical Use Case** | Enterprises needing strong, centralized cloud-native security | Scenarios prioritizing spoke autonomy, scale, or low latency | Organizations mandated to route all traffic via on-prem security |

#### **4.5 Security Considerations for Egress Traffic**

Regardless of the model chosen, securing egress traffic involves:

- **Inspection:** Implementing L4 and potentially L7 inspection based on organizational policies.22 Azure Firewall Premium offers TLS inspection and IDPS.23  
- **Filtering:** Applying rules based on IP addresses, ports, protocols, FQDNs (for Application rules), and potentially threat intelligence feeds.23  
- **Logging and Monitoring:** Capturing detailed logs (e.g., NSG Flow Logs, Azure Firewall logs) for traffic analysis, threat hunting, and compliance auditing.22

### **5\. Isolating On-Premises Infrastructure**

While ExpressRoute provides a private connection, it also creates a pathway between the Azure environment and the potentially more trusted on-premises network. A critical security objective is to isolate the on-premises infrastructure, preventing security threats, misconfigurations, or unwanted traffic originating from Azure resources (especially those with internet access) from traversing the ExpressRoute circuit and impacting internal systems.

#### **5.1 Rationale for Isolation**

The core principle driving the need for isolation is defense-in-depth and minimizing the potential blast radius of a security incident. If a VM or service in Azure is compromised, or if overly permissive network rules are configured, the ExpressRoute connection could become a vector for attackers to pivot into the on-premises network. Isolating on-premises resources means strictly controlling and inspecting traffic flowing from Azure back to the corporate network over ExpressRoute Private Peering.

#### **5.2 Technical Controls for Isolation**

Achieving effective isolation involves implementing multiple layers of security controls within the Azure environment, governing traffic destined for on-premises networks:

- **Network Security Groups (NSGs):** NSGs act as distributed, stateful L4 firewalls applied at the network interface (NIC) or subnet level within Azure VNets.21 They can be used as a first line of defense. NSG rules can be configured on workload subnets (spokes) to explicitly deny or allow traffic destined for known on-premises IP address ranges based on source/destination IPs, ports, and protocols.21 While NSGs can be applied to the GatewaySubnet where the ExpressRoute gateway resides, this requires extreme caution to avoid blocking essential control plane traffic. A more common practice is to apply restrictive outbound rules on workload subnets to limit what traffic can even attempt to reach the gateway.44 NSGs filter traffic *before* it leaves a subnet towards the gateway or *after* it arrives from the gateway.18  
- **User Defined Routes (UDRs):** Routing plays a vital role in isolation. UDRs can be used to steer traffic destined for on-premises networks away from a direct path to the ExpressRoute gateway and instead force it through a centralized inspection point, such as an Azure Firewall or NVA in the hub VNet.25 By creating UDRs on spoke subnets that match on-premises address prefixes and set the next hop to the firewall's IP address, organizations ensure that traffic is inspected before it reaches the ExpressRoute gateway. To prevent routes learned via BGP from on-premises from bypassing the inspection point, BGP route propagation can be disabled on the spoke subnet's route table, or more specific UDRs can be created to override the learned BGP routes.26  
- **Azure Firewall / Network Virtual Appliances (NVAs):** These centralized security appliances are crucial for inspecting traffic flowing between Azure and on-premises over ExpressRoute.22 Positioned in the hub VNet (typically), they act as a choke point where granular firewall policies can be applied.33 Rules should be configured based on the principle of least privilege, explicitly allowing only the necessary protocols, ports, source Azure IPs/subnets, and destination on-premises IPs required for business functions.33 All other traffic from Azure towards on-premises should be denied by default.  
- **Forced Tunneling:** As discussed previously, forcing all outbound traffic from Azure back to the on-premises network via ExpressRoute provides a strong form of isolation from *Azure-initiated internet threats*.31 Since Azure resources cannot directly reach the internet, the risk of a compromised Azure VM initiating attacks or exfiltrating data directly over the internet is eliminated. All such attempts are routed back through on-premises defenses. However, this does not inherently inspect traffic flowing from Azure *to* on-premises resources *within* the private network; separate controls (like the on-prem firewall inspecting traffic arriving over ER) are still needed for that.  
- **Service Endpoints / Private Link:** While primarily designed to secure connectivity *to* Azure PaaS services, these features contribute indirectly to isolation. By keeping traffic destined for supported PaaS services on the Azure backbone (Service Endpoints) or entirely within private IP space (Private Link/Private Endpoints), they reduce the need for Azure resources to communicate over public endpoints, thereby shrinking the potential attack surface that could pivot towards the on-premises network.46

Effective isolation is rarely achieved with a single tool. It typically requires a layered strategy combining NSG filtering at the source/destination subnet, UDRs to enforce traffic flow through inspection points, and robust firewall policies at the centralized inspection point (Azure Firewall or NVA) governing traffic crossing the hybrid boundary.

#### **5.3 Table: Summary of On-Premises Isolation Controls**

| Control | Mechanism | Primary Function for Isolation | Granularity | Key Consideration/Limitation |
| :---- | :---- | :---- | :---- | :---- |
| **NSG** | L4 Stateful Filtering 21 | Filter traffic at NIC/Subnet level; restrict outbound traffic towards on-prem ranges | IP/Port/Protocol (5-tuple) 21 | Doesn't inspect payload; applied within Azure only 21 |
| **UDR** | Routing Control 25 | Force Azure-to-OnPrem traffic through inspection point (Firewall/NVA) 26 | IP Prefix based routing 25 | Doesn't filter/inspect; relies on correct route configuration & precedence 25 |
| **Azure Firewall / NVA** | L4-L7 Inspection 23 | Central inspection point for all traffic crossing hybrid boundary; enforce allow/deny policies | IP/Port/Protocol/FQDN/Application 33 | Requires UDRs to force traffic; potential bottleneck (needs HA/scaling) 29 |
| **Forced Tunneling** | Routing Control 31 | Redirects ALL Azure outbound traffic (incl. internet) to on-prem; prevents direct internet egress | All outbound traffic (0.0.0.0/0) 31 | Adds latency, load; may break Azure services; relies on on-prem security 26 |
| **Service Endpoints / Private Link** | PaaS Connectivity 47 | Keep traffic to Azure PaaS off public internet, reducing exposure | Per Azure Service/Resource 46 | Indirect isolation benefit; not for general VM-to-onprem traffic |

#### **5.4 Best Practices for Minimizing Exposure**

- **Least Privilege Networking:** Strictly adhere to the principle of least privilege. Only permit network flows between Azure and on-premises that are absolutely necessary for application functionality.45 Deny all other traffic by default.  
- **Azure Segmentation:** Utilize NSGs to enforce segmentation within Azure. Restrict communication between different subnets, especially denying unnecessary traffic from workload subnets towards the GatewaySubnet or the hub VNet where the firewall resides.1  
- **Centralized Inspection:** Mandate that all traffic crossing the Azure-to-on-premises boundary passes through a central Azure Firewall or NVA cluster for inspection and policy enforcement.1  
- **Trust Zones:** If multiple VNets connect via the hub, consider segmenting them based on trust levels (e.g., production, development, DMZ). Apply stricter firewall rules for traffic originating from lower-trust VNets destined for the on-premises network.  
- **Auditing and Monitoring:** Regularly audit NSG rules, UDRs, and firewall policies. Utilize Azure Monitor, NSG Flow Logs, and firewall logs to monitor traffic patterns and detect anomalies or policy violations.8  
- **Policy Enforcement:** Leverage Azure Policy to define and enforce network security standards, such as ensuring NSGs are applied to all subnets or that specific firewall rules are present.38

### **6\. Understanding ExpressRoute Peering Types**

An ExpressRoute circuit can support two primary types of peering, each designed for different connectivity scenarios and having distinct configuration requirements. These peerings are logical BGP connections established over the physical ExpressRoute circuit.7

#### **6.1 Azure Private Peering Deep Dive**

- **Purpose:** To connect Azure Virtual Networks (VNets), containing resources like IaaS VMs or PaaS services injected into VNets (e.g., App Service Environment, Azure Kubernetes Service), directly to the on-premises network using private IP addressing.7 This peering essentially extends the private network reachability between the two environments.  
- **Mechanism:** BGP sessions are established between the ExpressRoute Virtual Network Gateway deployed in the Azure VNet(s) and the on-premises edge routers over the ExpressRoute circuit.7 The gateway advertises the VNet's address space(s) towards on-premises, and the on-premises routers advertise their internal network prefixes towards Azure.16  
- **Address Space:** Uses private IP ranges (RFC1918) or customer-owned public IPs (not advertised to the internet) for the resources within the VNet and on-premises networks being connected.7 Requires dedicated /29 or /30 (IPv4) or /125 or /126 (IPv6) subnets for the BGP peering interfaces themselves.9  
- **AS Number:** Can use either private AS numbers (except 65515-65520) or public AS numbers for the peering ASN. If a public ASN is used, the customer must own it.7  
- **Route Limits:** By default, Azure accepts up to 4,000 IPv4 prefixes advertised from on-premises. This limit can be increased to 10,000 IPv4 prefixes by enabling the ExpressRoute Premium add-on.7 Up to 100 IPv6 prefixes are accepted.7 Exceeding these limits will cause the BGP session to drop.9 Default routes (0.0.0.0/0) are permitted on Private Peering, enabling forced tunneling scenarios.9  
- **Use Case:** The primary use case is extending the corporate network into Azure, enabling seamless private communication between on-premises servers and Azure VMs, accessing internal Azure services privately, and supporting hybrid applications that span both environments.4

#### **6.2 Microsoft Peering Deep Dive**

- **Purpose:** To enable connectivity from the on-premises network to Microsoft's *public* services over the private ExpressRoute connection, instead of traversing the public internet.7 This includes Azure PaaS services with public endpoints (like Azure Storage, Azure SQL Database) and Microsoft 365 services (subject to specific requirements and often needing the Premium add-on).7  
- **Mechanism:** BGP sessions are established between the on-premises edge routers and the Microsoft edge routers (MSEEs).7 Microsoft advertises the public IP prefixes for its services towards the on-premises network. Crucially, customers *must* configure **Route Filters** to select which service prefixes they want to receive; without a route filter, no Microsoft service routes are advertised.7 On-premises networks advertise their public NAT IP prefixes to Microsoft.7  
- **Address Space:** Requires customer-owned, publicly registered IP addresses for both the BGP peering interface subnets (/29 or /30 for IPv4, /125 or /126 for IPv6) and for the NAT pool used to translate on-premises source IPs.7 Private IP addresses (RFC1918) cannot be advertised from on-premises over Microsoft Peering.16 Microsoft validates the ownership of the advertised public prefixes and peering ASN in public routing registries.16  
- **AS Number:** Typically requires a public ASN owned by the customer. A private ASN can be used if the advertised public prefixes are registered to the customer.7  
- **Route Limits:** Azure accepts up to 200 IPv4 prefixes and 200 IPv6 prefixes advertised from on-premises per BGP session.7 Exceeding these limits will cause the BGP session to drop.9 Default routes are not accepted.9  
- **Use Case:** Accessing Azure PaaS public endpoints (Storage, SQL DB, etc.) or Microsoft 365 services over the dedicated ExpressRoute link for potentially better performance, reliability, or compliance reasons, compared to using the public internet.7

#### **6.3 Table: Comparison of ExpressRoute Peering Types**

| Feature | Azure Private Peering | Microsoft Peering |
| :---- | :---- | :---- |
| **Primary Use** | Connect On-Premises Network \<-\> Azure VNets (Private IPs) 7 | Connect On-Premises Network \<-\> Microsoft Public Services (PaaS, M365) 7 |
| **Connected Endpoints** | Azure VMs, Internal Load Balancers, VNet-injected PaaS 7 | Azure PaaS Public Endpoints, Microsoft 365 Services 7 |
| **IP Addressing (Peering)** | Private or Public IPs for /29 or /30 subnets 9 | Customer-owned Public IPs for /29 or /30 subnets 7 |
| **IP Addressing (Source)** | Private IPs (RFC1918) or non-internet advertised Public IPs 7 | On-prem sources must NAT to Customer-owned Public IPs 7 |
| **ASN Requirements** | Private or Public ASN (if public, must own) 7 | Public ASN (owned) or Private ASN (if public IPs registered to customer) 7 |
| **Route Advertisement** | On-prem advertises private prefixes; Azure advertises VNet prefixes 16 | On-prem advertises public NAT prefixes; Microsoft advertises service prefixes 7 |
| **Route Filtering** | Filtering done on-prem; Azure advertises all VNet space 16 | **Required:** Azure Route Filter selects received Microsoft prefixes 7 |
| **Key Config Steps** | Configure peering on ER Circuit, Link VNet via ER Gateway 17 | Configure peering, Provide Public IPs/ASN, Validate ownership, Create/Apply Route Filter 16 |
| **Common Scenarios** | VNet extension, Hybrid Apps, Private access to Azure compute/internal PaaS 4 | Access PaaS/M365 over private link, Compliance requirements 7 |

#### **6.4 Impact on Traffic Flow and Control**

The choice of peering type dictates the traffic flow and control mechanisms:

- **Private Peering:** Directly influences the routing table for private IP communication between the connected networks. Traffic flow is subject to NSGs within Azure and firewalls on-premises.7  
- **Microsoft Peering:** Routes traffic destined for selected Microsoft public service IP ranges over the ExpressRoute circuit instead of the internet.7 It **does not** provide general internet connectivity for Azure VNets; VNet internet egress is still governed by VNet routing tables (system routes or UDRs).3 A common misconception is that Microsoft Peering enables internet access for VNets, which is incorrect and can lead to flawed security designs.  
- **BGP Communities:** For advanced control, BGP communities can be used. Azure can tag routes advertised over Private Peering with custom or regional community values.9 On-premises routers can then use these tags to apply specific routing policies (e.g., set local preference, filter routes) based on the origin or region of the Azure traffic.49 This allows for more sophisticated traffic engineering across the hybrid connection.

Understanding the distinct purpose and behavior of each peering type is fundamental to designing and securing an ExpressRoute hybrid network correctly.

### **7\. Glossary of Key Hybrid Networking Terms**

Understanding the terminology used in Azure hybrid networking is essential for effective design, configuration, and troubleshooting.

- **VNet (Virtual Network):** The fundamental building block for creating private networks within Azure. A VNet provides a logically isolated section of the Azure cloud dedicated to a subscription, allowing Azure resources like VMs to securely communicate with each other, the internet, and on-premises networks. It is analogous to a traditional network operated in a private datacenter but includes Azure infrastructure benefits like scale and availability.3 Each VNet has its own CIDR block, and VNets can be connected to each other or on-premises networks if their address spaces do not overlap.18  
- **Subnet:** A subdivision of a VNet's IP address range. VNets are segmented into one or more subnets. Resources deployed within Azure (like VMs or PaaS services) are placed into specific subnets.50 Subnets allow for logical grouping and the application of specific policies (like NSGs or UDRs) to a subset of resources within the VNet. Azure reserves the first four and the last IP address in each subnet for protocol conformance and Azure service usage.51  
- **BGP (Border Gateway Protocol):** A standardized exterior gateway protocol designed to exchange routing and reachability information between different Autonomous Systems (networks). In the context of Azure hybrid networking, BGP is used over ExpressRoute Private Peering and optionally over Site-to-Site VPN connections to dynamically advertise and learn network prefixes between the on-premises network and Azure VNets.6 This allows routing tables to update automatically as network topology changes.13  
- **VNet Peering:** A mechanism that connects two Azure Virtual Networks within the same region or across different regions (Global VNet Peering).3 Once peered, the VNets appear as one for connectivity purposes, allowing resources in either VNet to communicate directly using their private IP addresses over the Azure backbone network.19 Traffic does not traverse the public internet or require a gateway within the path between peered VNets. VNet peering is non-transitive, meaning if VNet A is peered with VNet B, and VNet B is peered with VNet C, VNet A and VNet C are not automatically peered.19 A key feature is **Gateway Transit**, which allows a peered VNet (spoke) to use the VPN or ExpressRoute gateway located in another peered VNet (hub) to access remote networks (like on-premises).19  
- **ExpressRoute Peering (Private/Microsoft):** Refers to the distinct logical BGP routing configurations established over a single ExpressRoute circuit.7  
  - **Private Peering:** Enables the extension of the on-premises network into Azure VNets using private IP addressing, facilitating direct communication between on-prem resources and Azure VMs/internal services.7  
  - **Microsoft Peering:** Enables connectivity from on-premises networks to Microsoft's public services (Azure PaaS public endpoints, Microsoft 365\) over the private ExpressRoute connection, using public IP addresses and route filters.7  
- **NSG (Network Security Group):** Azure's native, stateful firewall capability that filters network traffic at Layer 4 (TCP/UDP).21 NSGs contain a list of security rules (defined by priority, source/destination IP/port/service tag/ASG, protocol, direction, and action \- Allow/Deny) that control inbound and outbound traffic for network interfaces (NICs) and subnets.21 They are a fundamental tool for implementing micro-segmentation and network access control within Azure VNets.1  
- **UDR (User Defined Route):** A custom route entry created by administrators within a subnet's route table.25 UDRs allow overriding Azure's default system routing behavior to control where network traffic is sent.25 Common uses include forcing traffic through a Network Virtual Appliance (NVA) or Azure Firewall for inspection, directing traffic to a specific gateway, or routing traffic between subnets via an intermediary device.25 Azure selects the most specific route (longest prefix match), and if prefixes match, UDRs take precedence over BGP routes, which take precedence over system routes.25  
- **Firewall Policy (Azure Firewall):** A top-level Azure resource used to define and manage the configuration and rule sets for Azure Firewall instances.33 Policies contain rule collection groups (DNAT, Network, Application) which themselves contain prioritized rule collections, and finally individual rules.33 Firewall Policies support a hierarchical structure (parent/child policies) enabling centralized base policies with delegated application-specific rules.39 They provide a structured way to manage firewall configurations across multiple environments.23

### **8\. Synthesis and Recommendations**

Azure ExpressRoute offers a powerful solution for establishing private, dedicated connectivity between on-premises environments and Azure, forming the backbone of many enterprise hybrid cloud deployments. However, realizing its benefits securely and effectively requires a clear understanding of its architecture, routing mechanisms, and the associated security controls.

#### **8.1 Summary Comparison: ExpressRoute vs. Single Network Model**

Connecting networks via ExpressRoute creates a highly integrated system, but it does not result in a single, unified network. Key distinctions remain:

- **Management:** The on-premises network and Azure VNet retain separate administrative domains and management tools.  
- **Addressing:** Non-overlapping IP address spaces are required, highlighting their distinct nature.  
- **Routing:** Connectivity relies on explicit BGP route exchange and potentially UDRs, not implicit unification.  
- **Security:** Policies are applied independently at different boundaries (on-prem firewalls, Azure NSGs/Firewalls).

While Private Peering allows seamless private IP communication, treating the hybrid environment as anything other than interconnected distinct networks can lead to misconfigurations and security gaps.

#### **8.2 Recommended Approaches for Secure Internet Integration**

Default internet access from Azure VNets should generally be disabled or strictly controlled in enterprise hybrid scenarios. The recommended approaches involve trade-offs:

1. **Centralized Egress (Azure Firewall/NVA):** For most enterprises, routing internet-bound traffic from spoke VNets through a central Azure Firewall (Standard or Premium) or NVA cluster in a hub VNet provides the best balance of security, control, and manageability.1 This requires implementing UDRs on spoke subnets to direct the 0.0.0.0/0 route to the firewall's private IP.26 This model allows for consistent policy application and inspection.  
2. **Distributed Egress (NAT Gateway/NVA):** If scalability or lower latency for specific workloads is paramount, or if full firewall inspection isn't required for certain outbound traffic, using Azure NAT Gateway per subnet/VNet offers a simpler, scalable outbound-only solution.30 Distributed NVAs can also be used but increase management complexity. This might be used alongside a central firewall for specific needs.  
3. **Forced Tunneling (via On-Premises):** This should be considered primarily when organizational policy mandates that all internet traffic, without exception, must egress through existing on-premises security infrastructure.31 Be aware of the significant performance (latency, bandwidth consumption on ER) and potential Azure service compatibility implications.26

#### **8.3 Recommended Approaches for On-Premises Isolation**

Protecting the on-premises network from threats originating in or traversing the Azure environment is critical. A layered security strategy is essential:

1. **Mandatory Inspection:** All traffic flowing from Azure to on-premises over ExpressRoute Private Peering should be forced through a central Azure Firewall or NVA cluster in the hub VNet using UDRs.26 This ensures inspection and policy enforcement at the hybrid boundary.  
2. **Strict Firewall Policies:** Configure explicit allow rules on the central Azure Firewall/NVA for only the necessary protocols, ports, and source/destination IP ranges required for Azure-to-on-premises communication. Deny all other traffic by default.33  
3. **NSG Filtering:** Apply NSGs to workload subnets in Azure to restrict outbound traffic towards known on-premises IP ranges as a first layer of filtering.21 Limit communication paths to only what is required.  
4. **Routing Control:** Use UDRs and potentially disable BGP route propagation on spoke route tables to ensure traffic cannot bypass the central inspection point.25  
5. **Consider Forced Tunneling:** If the primary concern is preventing Azure resources from initiating *any* direct internet connections that could be used to attack on-premises, forced tunneling offers the strongest posture in that specific regard, shifting the internet egress control entirely to on-premises.31

#### **8.4 Concluding Architectural Guidance**

Building a secure and functional hybrid network with Azure ExpressRoute demands meticulous planning and a deep understanding of the interplay between connectivity, routing, and security components.

- Start with a clear definition of security requirements and network traffic flow policies.  
- Adopt a standard topology, like Hub-and-Spoke, to centralize control and shared services.29  
- Carefully plan IP addressing to avoid overlaps.18  
- Understand the distinct roles of Private and Microsoft Peering and configure them appropriately.7  
- Implement layered security controls (NSGs, UDRs, Firewall/NVA) to manage internet egress and isolate the on-premises network.1  
- Leverage BGP for dynamic routing but be mindful of its configuration complexities and limits.9  
- Continuously monitor network traffic, gateway performance, and security logs to ensure the environment operates as expected and to detect potential issues proactively.8

By applying these principles and leveraging the appropriate Azure services and controls, organizations can build robust, secure, and performant hybrid networks using Azure ExpressRoute.

##### **Works cited**

1. Azure best practices for network security \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/security/fundamentals/network-best-practices](https://learn.microsoft.com/en-us/azure/security/fundamentals/network-best-practices)  
2. The virtual datacenter: A network perspective \- Cloud Adoption Framework | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/resources/networking-vdc](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/resources/networking-vdc)  
3. What is Azure Virtual Network? | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)  
4. Azure ExpressRoute | Microsoft Azure, accessed on April 15, 2025, [https://azure.microsoft.com/en-us/products/expressroute](https://azure.microsoft.com/en-us/products/expressroute)  
5. Express Route \- Microsoft Q\&A, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/answers/questions/2121168/express-route](https://learn.microsoft.com/en-us/answers/questions/2121168/express-route)  
6. Azure ExpressRoute Overview: Connect over a private connection \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction)  
7. Azure ExpressRoute: circuits and peering \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-circuit-peerings](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-circuit-peerings)  
8. Design and architect Azure ExpressRoute for resiliency | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/design-architecture-for-resiliency](https://learn.microsoft.com/en-us/azure/expressroute/design-architecture-for-resiliency)  
9. Azure ExpressRoute: Routing requirements \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-routing](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-routing)  
10. About ExpressRoute Metro \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/metro](https://learn.microsoft.com/en-us/azure/expressroute/metro)  
11. Azure ExpressRoute: Connectivity models | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-connectivity-models](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-connectivity-models)  
12. About Azure ExpressRoute Direct | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-erdirect-about](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-erdirect-about)  
13. About BGP with VPN Gateway \- Azure VPN Gateway | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-bgp-overview](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-bgp-overview)  
14. How to configure BGP for Azure VPN Gateway \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/vpn-gateway/bgp-howto](https://learn.microsoft.com/en-us/azure/vpn-gateway/bgp-howto)  
15. About ExpressRoute Virtual Network Gateways | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-about-virtual-network-gateways](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-about-virtual-network-gateways)  
16. FAQ \- Azure ExpressRoute | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-faqs](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-faqs)  
17. Configure peering for ExpressRoute circuit \- Azure portal \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-howto-routing-portal-resource-manager](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-howto-routing-portal-resource-manager)  
18. Azure Virtual Network FAQ | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq)  
19. Virtual network peering | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/windows-server/networking/sdn/vnet-peering/sdn-vnet-peering](https://learn.microsoft.com/en-us/windows-server/networking/sdn/vnet-peering/sdn-vnet-peering)  
20. Azure ExpressRoute: Configure peering: classic \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-howto-routing-classic](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-howto-routing-classic)  
21. Azure network security groups overview \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)  
22. Network security concepts and requirements in Azure | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/security/fundamentals/network-overview](https://learn.microsoft.com/en-us/azure/security/fundamentals/network-overview)  
23. What is Azure Firewall? | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/firewall/overview](https://learn.microsoft.com/en-us/azure/firewall/overview)  
24. Tutorial: Secure your virtual hub using Azure Firewall Manager \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/firewall-manager/secure-cloud-network](https://learn.microsoft.com/en-us/azure/firewall-manager/secure-cloud-network)  
25. Azure virtual network traffic routing | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview)  
26. Azure Firewall & VPN/ExpressRoute UDRs \- Microsoft Q\&A, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/answers/questions/847615/azure-firewall-vpn-expressroute-udrs](https://learn.microsoft.com/en-us/answers/questions/847615/azure-firewall-vpn-expressroute-udrs)  
27. Troubleshoot network link performance: Azure ExpressRoute | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-troubleshooting-network-performance](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-troubleshooting-network-performance)  
28. Connectivity between virtual networks over Azure ExpressRoute \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/virtual-network-connectivity-guidance](https://learn.microsoft.com/en-us/azure/expressroute/virtual-network-connectivity-guidance)  
29. Hub-spoke network topology in Azure \- Azure Architecture Center \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke)  
30. What is Azure NAT Gateway? | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview)  
31. About forced tunneling for site-to-site \- Azure VPN Gateway | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/vpn-gateway/about-site-to-site-tunneling](https://learn.microsoft.com/en-us/azure/vpn-gateway/about-site-to-site-tunneling)  
32. ExpressRoute for Cloud Solution Providers (CSP) \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-for-cloud-solution-providers](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-for-cloud-solution-providers)  
33. Azure Firewall policy rule sets | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/firewall/policy-rule-sets](https://learn.microsoft.com/en-us/azure/firewall/policy-rule-sets)  
34. Azure Virtual WAN: Create a Network Virtual Appliance (NVA) in the hub | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-wan/how-to-nva-hub](https://learn.microsoft.com/en-us/azure/virtual-wan/how-to-nva-hub)  
35. What is Azure Route Server? | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/route-server/overview](https://learn.microsoft.com/en-us/azure/route-server/overview)  
36. Automate management of user-defined routes (UDRs) with Azure Virtual Network Manager, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network-manager/concept-user-defined-route](https://learn.microsoft.com/en-us/azure/virtual-network-manager/concept-user-defined-route)  
37. Diagnose an Azure virtual machine routing problem | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/diagnose-network-routing-problem](https://learn.microsoft.com/en-us/azure/virtual-network/diagnose-network-routing-problem)  
38. Use Azure Policy to help secure your Azure Firewall deployments | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/firewall/firewall-azure-policy](https://learn.microsoft.com/en-us/azure/firewall/firewall-azure-policy)  
39. Use Azure Firewall policy to define a rule hierarchy \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/firewall-manager/rule-hierarchy](https://learn.microsoft.com/en-us/azure/firewall-manager/rule-hierarchy)  
40. How to Use Azure Virtual Network Manager's UDR Management Feature, accessed on April 15, 2025, [https://techcommunity.microsoft.com/blog/azurenetworkingblog/how-to-use-azure-virtual-network-managers-udr-management-feature/4129759](https://techcommunity.microsoft.com/blog/azurenetworkingblog/how-to-use-azure-virtual-network-managers-udr-management-feature/4129759)  
41. Create User-Defined Routes with Azure Virtual Network Manager \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network-manager/how-to-create-user-defined-route](https://learn.microsoft.com/en-us/azure/virtual-network-manager/how-to-create-user-defined-route)  
42. Create, change, or delete an Azure network security group \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/manage-network-security-group](https://learn.microsoft.com/en-us/azure/virtual-network/manage-network-security-group)  
43. Network security group \- how it works | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/network-security-group-how-it-works](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-group-how-it-works)  
44. Azure security baseline for ExpressRoute \- Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/expressroute-security-baseline](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/expressroute-security-baseline)  
45. Azure data security and encryption best practices \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/security/fundamentals/data-encryption-best-practices](https://learn.microsoft.com/en-us/azure/security/fundamentals/data-encryption-best-practices)  
46. Azure virtual network service endpoints | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)  
47. Virtual network integration of Azure services for network isolation | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/vnet-integration-for-azure-services](https://learn.microsoft.com/en-us/azure/virtual-network/vnet-integration-for-azure-services)  
48. Connect a virtual network to an ExpressRoute circuit using the Azure portal \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-howto-linkvnet-portal-resource-manager](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-howto-linkvnet-portal-resource-manager)  
49. Managing complex network architectures with BGP communities \- Azure ExpressRoute, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/expressroute/bgp-communities](https://learn.microsoft.com/en-us/azure/expressroute/bgp-communities)  
50. Understand TCP/IP addressing and subnetting basics \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/tcpip-addressing-and-subnetting](https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/tcpip-addressing-and-subnetting)  
51. Add, change, or delete a virtual network subnet \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-subnet](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-subnet)  
52. Virtual network peering in Azure Stack Hub \- Learn Microsoft, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure-stack/user/virtual-network-peering?view=azs-2501](https://learn.microsoft.com/en-us/azure-stack/user/virtual-network-peering?view=azs-2501)  
53. VNet peering and Azure Bastion architecture | Microsoft Learn, accessed on April 15, 2025, [https://learn.microsoft.com/en-us/azure/bastion/vnet-peering](https://learn.microsoft.com/en-us/azure/bastion/vnet-peering)
