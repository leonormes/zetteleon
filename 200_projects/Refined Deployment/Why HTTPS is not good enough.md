---
aliases: []
confidence: 
created: 2025-07-23T02:43:05Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [security, topic/technology/networking]
title: Why HTTPS is not good enough
type:
uid: 
updated: 
version:
---

This is a critical and recurring question in security architecture. Your instinct is absolutely correct, especially given the context of protecting patient data. Relying solely on HTTPS over the public internet is not sufficient, and the effort you've put into creating private networks is the foundation of a modern, defense-in-depth security strategy.

Here is a well-structured argument you can use to explain why a private connection is non-negotiable.

## The Core Argument: HTTPS Secures the *Message*, a Private Network Secures the *Address*

The simplest way to frame this is with an analogy:

- **HTTPS over the Public Internet** is like sending an armored car full of cash (your encrypted patient data) through busy public streets. The cash inside is safe, but the car itself is visible to everyone. It can be followed, its routes can be mapped, it can be attacked with overwhelming force (DDoS), and attackers can try to find vulnerabilities in the truck's armor, tires, or engine (the underlying server and its software).
- **A Private Connection (like a Site-to-Site VPN)** is like building a private, underground tunnel directly between two bank vaults. The armored car still drives through this tunnel, but it is completely invisible to the outside world. An attacker wouldn't even know the tunnel exists, let alone be able to attack the car inside it.

While HTTPS is an essential layer, it only protects the data *in transit*. It does nothing to protect the endpoints themselves, which remain exposed.

---

## A Deeper Dive: Four Key Reasons Why HTTPS Alone is Insufficient

Here is a breakdown of the risks you accept when you choose to expose services over the public internet, even with HTTPS.

### 1. You Create a Public Attack Surface

This is the most significant problem. By assigning a public IP address to your service, you are announcing its existence to the entire world. This immediately exposes you to a wide range of threats that a private network is immune to:

- **Reconnaissance and Scanning:** Malicious actors are constantly scanning the entire internet for open ports and known services. Your endpoint will be discovered and cataloged. They will probe it to identify the operating system, the webserver software (e.g., Nginx, Apache), and the TLS/SSL library versions you are using.
- **Zero-Day Vulnerabilities:** If a critical vulnerability is discovered in your public-facing software stack (like Heartbleed in OpenSSL), your service becomes a target for immediate, widespread exploitation by attackers across the globe. In a private network, the endpoint is not reachable, giving you time to patch without being under active attack.
- **Denial-of-Service (DoS/DDoS) Attacks:** A public endpoint can be targeted by DoS attacks, where an attacker floods it with traffic to overwhelm its resources and make it unavailable. This can disrupt critical services. A private connection is not susceptible to these kinds of internet-scale attacks.

**The Problem in Short:** You have built two secure fortresses (your private networks). Exposing a public route is like building a single, publicly-known gate in the wall of each fortress. Even if the gate is strong (HTTPS), it becomes the single point that every attacker will focus on.

### 2. HTTPS Protects Data Confidentiality, Not Endpoint Availability or Integrity

HTTPS does one job very well: it encrypts the conversation between a client and a server. However, it does not guarantee the availability or integrity of the server itself.

- **Encryption is Not a Firewall:** HTTPS will not stop an attacker from exploiting a vulnerability in your application's code, the API gateway, or the underlying operating system. It only protects the data once the connection is established.
- **Authentication is Limited:** Standard HTTPS authenticates the server to the client. It does not inherently authenticate the client to the server. While client-side certificates (mutual TLS) can be used, authentication is often handled by weaker methods like API keys or tokens sent *inside* the encrypted tunnel. If these credentials are leaked, an attacker can establish a perfectly valid HTTPS connection from anywhere in the world.

**The Problem in Short:** Relying on HTTPS alone is like focusing only on the secrecy of a conversation while ignoring the physical security of the people and the building they are in.

### 3. It Undermines the Principle of "Least Privilege" at the Network Level

You have invested in private networks to create a trusted, isolated environment where access is denied by default The core principle is that only explicitly authorized entities within that trusted boundary should be able to communicate.

Exposing a service publicly violates this principle. You are changing the rule from "no one can talk to this service unless they are on our private network" to "anyone in the world can try to talk to this service, and we will rely on application-level controls to reject them." This is a fundamentally weaker security posture.

**The Problem in Short:** It negates the primary security benefit of having a private network in the first place.

### 4. The Compliance and Audit Narrative is Weaker

When dealing with patient data under regulations like HIPAA, you must demonstrate that you have taken all reasonable measures to secure that data.

- **The Strong Narrative (Private Connection):** "We have established a dedicated, encrypted, private tunnel between our two trusted environments. Communication is restricted to this channel, which is not visible to the public internet. Access is controlled at the network layer, and all traffic is encrypted in transit within the tunnel." This is a simple, powerful, and easily auditable story of robust security.
- **The Weaker Narrative (Public Endpoint):** "We have an endpoint exposed to the public internet, but we have secured it. We use HTTPS to encrypt the data, and we have a firewall rule that restricts access to a specific IP address." This immediately invites further questions: How are you protecting against DDoS? How do you manage that IP list? What happens if that IP changes? How do you protect against vulnerabilities in the public-facing software?

---

## Conclusion: A Layered Defense is Best Practice

The best practice is not a choice between one or the other, but to use them together. The gold standard for security is to establish a **Site-to-Site VPN** or a direct private link (**AWS Direct Connect / Azure ExpressRoute**) and then *still* use HTTPS for the traffic that flows within that private tunnel.

This provides a layered, defense-in-depth model:

1. **Network Layer Security:** The private connection (VPN) ensures only the two trusted networks can communicate, completely hiding them from the public internet.
2. **Application Layer Security:** HTTPS ensures that even within that private tunnel, the specific conversation between services is encrypted and the server's identity is verified.

You are right to push back. For data as sensitive as patient records, relying on a single layer of security when a much more robust, private, and defensible architecture is available is an unnecessary and unacceptable risk.

Our knowledge base includes detailed information on:

- **Networking Fundamentals:** OSI and TCP/IP models, layers (physical, link, network, transport, application), protocols (TCP, UDP, IP, HTTP, DNS, BGP, OSPF, SMTP, FTP, TLS/SSL, IPsec, MACsec, ARP, ICMP), network components (hosts, routers, switches, access points), concepts like encapsulation, multiplexing, reliable data transfer, congestion control, latency, throughput, packet loss, and network addressing (IP, MAC, private/public IPs, NAT, subnets, CIDR).
- **Network Security:** Threats (malware, sniffing, DDoS, impersonation), security properties (confidentiality, integrity, authentication), cryptography (symmetric/public-key encryption, keys, hash functions, digital signatures, MACs, nonces), and security protocols/systems (TLS/SSL, PGP, IPsec, VPNs, WEP, 802.11 security, 4G/5G AKA, firewalls, IDS/IPS, anonymity/privacy proxies).
- **Azure/Microsoft ExpressRoute:** Peering types (private, Microsoft), NAT requirements, BGP, AS numbers, security, QoS, VNet connectivity (peering vs. ExpressRoute), Global Reach, disaster recovery with VPN failover, and specific configurations.

---

## Why a Public Route via the Internet with HTTPS is Not Good Enough for Sensitive Private Network Communication (Patient Records)

While HTTPS (HTTP over TLS/SSL) is a foundational element for secure communication over the public Internet, it is often **not sufficient** on its own for critical strategic scenarios involving highly sensitive data like patient records between two private networks. Here's a breakdown of why:

1. **Limited Scope of Protection (Layer 7 vs. Network-Wide):**
   - **HTTPS (TLS) operates at the application layer**. This means it encrypts data between the application process on the sender and the application process on the receiver.
   - However, **metadata, such as source and destination IP addresses, and port numbers, are still visible** in the network and transport layer headers. For patient records, merely obscuring the content may not be enough if the fact of who is communicating with whom (IP addresses) or what service is being accessed (port numbers) could be sensitive information.
   - **Internet Service Providers (ISPs) and intermediate routers can still see this metadata**. Even with SSL, your source IP address is presented to the website in every datagram, and your local ISP can easily sniff the destination address of every packet you send. For highly sensitive data, this level of exposure might be unacceptable for compliance or privacy reasons.
   - **IPsec, in contrast, operates at the network layer (Layer 3) and can provide "blanket coverage"** by encrypting the entire IP datagram payload, which includes transport-layer segments and all application-layer data. This hides the protocol number, original source IP address, and original destination IP address from intermediate sniffers. This offers a more comprehensive security posture for network-to-network communication than application-layer encryption alone.

2. **Performance and Predictability Limitations of the Public Internet:**
   - The **Internet is fundamentally a "best-effort" network**. It does not guarantee timely delivery of packets, nor does it guarantee against packet loss. This unpredictability in latency and throughput is a major concern for real-time applications (e.g., telehealth video consultations) and large file transfers of patient data.
   - **Transport protocols in today's Internet, such as TCP and UDP, do not provide throughput or timing guarantees**. While applications can be designed to cope with this, clever design has limitations when delay is excessive or throughput is limited.
   - **ExpressRoute connections, by contrast, do not traverse the public Internet**. They offer secure connectivity, reliability, higher speeds, and significantly lower and more consistent latencies than typical Internet connections. This dedicated, private connection is critical for ensuring reliable and performant access to sensitive patient data.

3. **Authentication and Trust Model:**
   - The Internet was originally designed based on a model of "mutually trusting users attached to a transparent network". This model is fundamentally inadequate for today's reality where users and networks do not necessarily trust each other.
   - While TLS provides server authentication through certificates, and can be extended for client authentication, the underlying trust in the certificate authority (CA) chain is crucial. DNS itself has vulnerabilities like man-in-the-middle attacks or DNS poisoning, which could redirect traffic to malicious sites even before an HTTPS connection is initiated, unless DNSSEC is employed.

4. **Regulatory and Compliance Requirements (Specific to Patient Records):**
   - Patient records fall under "special category sensitive data," implying stringent regulatory requirements (e.g., GDPR, HIPAA, NHS Digital). These regulations often mandate specific security controls, auditing capabilities, and network isolation that go beyond what a standard public Internet connection with HTTPS can provide.
   - **Forced tunneling** is a specific security measure that may be required for auditing or compliance, redirecting all Internet-bound traffic from a virtual network back through an on-premises proxy. This allows for comprehensive auditing and filtering of all outbound traffic, which is a common requirement for highly regulated data.
   - Some regulations may explicitly require **private connections for cloud-bound traffic**. ExpressRoute directly addresses this by offering a private, dedicated connection to Microsoft's cloud infrastructure.

5. **Operational and Asymmetric Routing Issues:**
   - When an organisation uses both the public Internet and a dedicated connection like ExpressRoute, **asymmetric routing** can occur, particularly with stateful devices like firewalls or NAT. This happens when outbound traffic uses one path (e.g., ExpressRoute) and return traffic uses another (e.g., the Internet). If the firewall on the return path doesn't have a record of the connection, it will drop the packets, leading to connectivity issues. This is a significant operational challenge that requires careful routing and NAT configuration to avoid.

## Best Practices for Making a Secure Connection for Patient Records

Given the sensitive nature of patient records, a multi-layered security approach, leveraging dedicated private connectivity and robust network-layer security, is paramount.

1. **Establish Dedicated Private Connectivity (ExpressRoute):**
   - **Utilise Azure ExpressRoute:** Create private, high-speed, low-latency connections between your on-premises network and Microsoft Azure datacenters. This bypasses the public Internet, inherently improving security, reliability, and performance.
   - **Private Peering for IaaS/PaaS:** Use ExpressRoute's Azure Private peering to connect to your Infrastructure as a Service (IaaS) deployments (e.g., VMs storing patient records) and Platform as a Service (PaaS) services within Azure Virtual Networks (VNets) directly on their private IP addresses. This domain is considered a trusted extension of your core network.
   - **Redundancy for Disaster Recovery:** Set up at least two ExpressRoute circuits in different peering locations and with diverse service providers to eliminate a single point of failure and ensure high availability.
   - **VPN Failover:** Configure a site-to-site VPN as a failover path for ExpressRoute for private peering connections. This ensures business continuity if the ExpressRoute circuit becomes unavailable. For Azure and Microsoft 365 services, the Internet remains the only failover path if ExpressRoute is used.

2. **Implement Robust Encryption:**
   - **IPsec for Network-Layer Confidentiality:** Employ IPsec (Internet Protocol Security) in **tunnel mode** to encrypt traffic end-to-end between your on-premises network and your Azure virtual network over ExpressRoute private peering. Tunnel mode encapsulates the original IP datagram, encrypting its header and payload, effectively hiding source/destination IPs and protocols from intermediate observers. IPsec provides confidentiality, source authentication, data integrity, and replay-attack prevention.
   - **Configure IPsec Transport Mode for Specific Host-to-Host Encryption:** For highly granular security on specific traffic flows (e.g., HTTP traffic on destination port 8080 between Azure VMs and on-premises hosts), implement IPsec transport mode. This encrypts only the payload and ESP trailer, leaving the original IP header unchanged, ideal for end-to-end encryption between hosts.
   - **MACsec for Link-Layer Encryption (ExpressRoute Direct):** If using ExpressRoute Direct, enable MACsec (Media Access Control Security) to encrypt the physical links at Layer 2 between your network devices and Microsoft's. MACsec uses symmetric key encryption (e.g., GCM-AES-256) and protects against sniffing and manipulation at the physical link level. Remember MACsec is disabled by default.
   - **TLS for Application-Specific Security:** Continue to use TLS/HTTPS for application-layer communication, even over IPsec-secured connections. While IPsec provides blanket network-layer security, TLS offers process-to-process encryption, data integrity, and end-point authentication directly at the application level. This multi-layered encryption adds defence-in-depth, addressing security from different perspectives of the OSI model.

3. **Implement Strong Network Segmentation and Firewalling:**
   - **Network Segmentation Boundaries:** Establish clear network segmentation boundaries to isolate sensitive patient record systems from other network segments.
   - **DMZ for Public-Facing Services:** Connect Microsoft peering links to your Demilitarised Zone (DMZ) and private peering directly to your core network. Use firewalls to strictly segregate these zones.
   - **Strict Firewall Rules (ACLs & Stateful Inspection):**
     - Employ packet-filtering firewalls with Access Control Lists (ACLs) to control traffic flow based on IP addresses, port numbers, and protocols.
     - Use **stateful firewalls** that track active connections to prevent asymmetric routing issues and block unsolicited traffic. They record flow information (source/destination IPs and ports) and only permit return traffic for known active connections.
     - **Implement forced tunneling** from Azure VNets back to an on-premises proxy/firewall for all Internet-bound traffic. This enables auditing, logging, and filtering of all outbound Internet access, which is crucial for compliance with sensitive data regulations.
   - **Network Security Groups (NSGs) in Azure:** Utilise NSGs to define granular allowed traffic into and out of subnets and virtual machines within your Azure VNets. Ensure VMs are only accessible via internal IP addresses and do not have public IPs where possible.

4. **Careful Routing and Network Address Translation (NAT) Management:**
   - **Public IP Requirement for Microsoft Peering:** Understand that Microsoft peering *requires* you to use public IPv4 addresses you own for BGP sessions, verified through Internet Registries. Private IP addresses are generally not permitted for Microsoft peering routes, though they are allowed for private peering.
   - **Strict NAT Policies:** Implement Source Network Address Translation (SNAT) for outbound traffic from your private network to public Microsoft services over Microsoft peering. Crucially, **use distinct NAT IP pools for ExpressRoute and Internet connections** to prevent asymmetric routing and connectivity issues.
   - **BGP Routing Policy:** Configure BGP (Border Gateway Protocol) appropriately. Use BGP Local Preference to ensure your on-premises traffic prefers the ExpressRoute path over Site-to-Site VPNs for Azure-destined traffic. Microsoft also uses AS path prepending to influence return traffic paths during maintenance or unplanned events.

5. **Robust Authentication Mechanisms:**
   - **End-Point Authentication:** Implement strong mutual authentication between communicating entities (e.g., servers, applications, users). Protocols like TLS inherently provide server authentication, but for sensitive data, client authentication (e.g., using client certificates) should also be enforced.
   - **Nonces to Prevent Replay Attacks:** Ensure authentication protocols use nonces (numbers used once) to protect against connection replay attacks, where an attacker records and retransmits legitimate session messages.

6. **Quality of Service (QoS) for Real-time Data:**
   - For patient records that include real-time voice or video (e.g., telehealth), implement QoS policies. This involves classifying workloads and marking DSCP (Differentiated Services Code Point) values (e.g., EF for voice) to ensure critical traffic receives preferential treatment and consistent performance across the network. Ensure your network "trusts" and preserves these DSCP markings.

7. **Continuous Monitoring and Auditing:**
   - Beyond initial setup, **regularly monitor network traffic, security logs, and connection states**. Implement Intrusion Detection Systems (IDS) or Intrusion Prevention Systems (IPS) to detect and potentially block suspicious activity.
   - **Periodically validate VPN failover configurations** and conduct disaster recovery tests to ensure passive backup solutions remain dependable. Ensure routing tables and firewall rules remain aligned with security policies.

By adopting these best practices, you can create a highly secure, reliable, and compliant network infrastructure for handling sensitive patient records, moving beyond the limitations of basic HTTPS over the public Internet.

---

## **Regulatory Requirements Overview: GDPR and NHS Digital**

**General Data Protection Regulation (GDPR)** GDPR (Regulation (EU) 2016/679) is a comprehensive data protection law that applies to all organisations processing personal data of individuals in the EU, including the UK post-Brexit via the UK GDPR. Key principles relevant to network security for patient records (a special category of personal data) include:

- **Integrity and Confidentiality (Article 5(1)(f))**: Personal data must be processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction, or damage, using appropriate technical or organisational measures. This is often referred to as "security by design and by default".
- **Security of Processing (Article 32)**: This article mandates that controllers and processors implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, including:
  - The pseudonymisation and encryption of personal data.
  - The ability to ensure the ongoing confidentiality, integrity, availability, and resilience of processing systems and services.
  - The ability to restore the availability and access to personal data in a timely manner in the event of a physical or technical incident.
  - A process for regularly testing, assessing, and evaluating the effectiveness of technical and organisational measures for ensuring the security of the processing.
- **Accountability (Article 5(2))**: The controller is responsible for, and must be able to demonstrate compliance with, the principles. This necessitates robust logging, monitoring, and auditing capabilities.

**NHS Digital Guidelines (General Principles)** While specific NHS Digital guidelines are not detailed in the sources, they generally align with GDPR and typically require:

- **Strong Authentication and Access Control**: Ensuring only authorised individuals and systems can access patient data.
- **Data in Transit and at Rest Encryption**: Protecting patient identifiable data both when it's moving across networks and when it's stored.
- **Network Segmentation**: Isolating sensitive patient data systems from less sensitive systems and the general internet.
- **Audit Trails and Monitoring**: Comprehensive logging of access and changes to patient data to detect and investigate incidents.
- **Resilience and Disaster Recovery**: Ensuring continuous availability of critical patient systems and data.
- **Secure Configuration and Patch Management**: Maintaining systems in a secure state to prevent vulnerabilities.

## **Mapping Security Best Practices to Regulatory Needs**

The following security best practices, drawn from the provided sources, directly contribute to satisfying GDPR and general NHS Digital security requirements for patient records:

1. **Network Segmentation and Isolation**
   - **Technical Practice**: Azure ExpressRoute allows for a private connection between an on-premises network and Azure, bypassing the public internet. This forms a secure network boundary. Within Azure, Virtual Networks (VNets) and subnets can be used to segment the network, isolating different environments (e.g., development, QA, production) and application tiers (web, application, database). Network Security Groups (NSGs) act as firewalls at the NIC or subnet level, controlling inbound and outbound traffic based on rules (e.g., IP addresses, CIDR blocks, protocols, port ranges). Kubernetes NetworkPolicies provide a "pod-level firewall" to specify how groups of pods can communicate, enforcing rules based on labels rather than dynamic IP addresses, suitable for cloud-native environments.
   - **Regulatory Alignment**: This directly supports GDPR's **Integrity and Confidentiality (Article 5(1)(f))** and **Security of Processing (Article 32)**. By segregating networks, organisations minimise the attack surface and limit the scope of a breach. Patient records, being highly sensitive, should reside in the most isolated segments, protected by restrictive NSG and NetworkPolicy rules. This practice helps to ensure that only legitimate resources can access patient data, thereby protecting against unauthorised access or unlawful processing. NHS Digital guidelines would strongly mandate such segmentation to protect patient data from broader network traffic and internet exposure.

2. **Encryption of Data in Transit**
   - **Technical Practice**: Data in transit encryption is a core security service. ExpressRoute itself provides a dedicated private connection, offering inherent security benefits compared to the public internet. For enhanced security, IPsec tunnel-mode policies can be defined for all traffic flowing between on-premises resources and Azure over ExpressRoute, encrypting the original packet including its IP header. TLS (Transport Layer Security) can be implemented on top of TCP to provide confidentiality, data integrity, and end-point authentication for application data.
   - **Regulatory Alignment**: This is a fundamental technical measure for GDPR's **Integrity and Confidentiality (Article 5(1)(f))** and explicitly mentioned under **Security of Processing (Article 32)** for "pseudonymisation and encryption of personal data." Encrypting patient records in transit prevents eavesdropping and tampering by unauthorised parties, even if the underlying network infrastructure is compromised. NHS Digital mandates robust encryption for sensitive data.

3. **Strong Authentication and Access Control**
   - **Technical Practice**: Azure ExpressRoute's security baseline mentions that Azure AD authentication is supported for data plane access. While local administrative accounts are generally not supported for securing ExpressRoute services, the principle of "just enough administration" and "least privilege" (e.g., Azure Role-Based Access Control - Azure RBAC) is emphasized for managing access to service data plane actions. Centralised identity and authentication systems are critical. For BGP peering, only public BGP AS numbers are allowed, and for Microsoft peering, IP address ownership is validated against regional routing registries.
   - **Regulatory Alignment**: This directly addresses GDPR's **Security of Processing (Article 32)** by ensuring that access to patient data and the systems processing it is strictly controlled and granted only to authorised individuals or services. Implementing least privilege ensures that users or systems only have the minimum access necessary to perform their functions, reducing the risk of accidental or malicious data exposure. NHS Digital also places high importance on robust identity and access management for systems handling patient data.

4. **Data Integrity and Non-Repudiation**
   - **Technical Practice**: ExpressRoute circuits can be configured with an MD5 hash on the circuit during private or Microsoft peering setup to secure messages between cross-premises routes and Microsoft edge routers, helping to ensure data hasn't been tampered with in transit. More broadly, hash functions (like SHA-1) and Message Authentication Codes (MACs) or digital signatures are used to provide message integrity and verify the source of a message. Digital signatures can also provide non-repudiation and are used for public key certification in protocols like IPsec and TLS.
   - **Regulatory Alignment**: This directly supports GDPR's **Integrity and Confidentiality (Article 5(1)(f))** and **Security of Processing (Article 32)**. Ensuring data integrity means that patient records cannot be altered or corrupted without detection, whether maliciously or accidentally. For patient records, this is crucial for accuracy and reliability of medical information. NHS Digital requires measures to ensure the integrity of patient data.

5. **Monitoring, Logging, and Audit Trails**
   - **Technical Practice**: ExpressRoute circuits can be monitored for availability, connectivity to VNets, and bandwidth utilization using ExpressRoute Network Insights. Flow logs can be collected and exported to a Security Information and Event Management (SIEM) tool for network forensics analysis, identifying compromised IPs, correlating events, and generating security alerts. Azure Policy definitions are listed in the Regulatory Compliance section of Microsoft Defender for Cloud to help measure compliance with security benchmarks.
   - **Regulatory Alignment**: This directly addresses GDPR's **Accountability (Article 5(2))** and **Security of Processing (Article 32)**. Robust monitoring and logging capabilities are essential for detecting, investigating, and reporting security incidents involving patient data. They provide the necessary audit trails to demonstrate compliance, identify security weaknesses, and respond effectively to breaches, as required by GDPR. NHS Digital mandates comprehensive audit logging for all access to and changes in patient records.

6. **Redundancy and High Availability**
   - **Technical Practice**: ExpressRoute uses a redundant pair of BGP sessions per peering and provisions two redundant ports on two Microsoft edge routers in an active-active configuration for high availability. Microsoft recommends setting up at least two ExpressRoute circuits in different peering locations for disaster recovery. A site-to-site VPN can also be configured as a failover path for ExpressRoute private peering. Redundant network equipment and links are also typical in data center designs for high availability.
   - **Regulatory Alignment**: While primarily a reliability concern, redundancy and high availability directly contribute to GDPR's **Security of Processing (Article 32)**, specifically the "ability to ensure the ongoing confidentiality, integrity, availability, and resilience of processing systems and services" and "the ability to restore the availability and access to personal data in a timely manner in the event of a physical or technical incident." For patient records, continuous availability is critical for patient care, making this an essential compliance measure. NHS Digital strongly emphasises resilience for systems handling patient data.

7. **Managed Prefix Advertisements and Route Filtering**
   - **Technical Practice**: When advertising prefixes over BGP sessions, specifically for Microsoft peering, organisations must ensure only *public* IPv4 address space owned by the customer is accepted, and that only *agreed-to prefixes* are announced to Microsoft via route maps. Organisations must *not* announce their entire internal network routing table. Microsoft provides route filters to select a subset of services to consume through Microsoft peering, reducing the size of route tables.
   - **Regulatory Alignment**: This enhances **Integrity and Confidentiality (Article 5(1)(f))** by limiting the scope of what network information is exposed and processed. By restricting advertised prefixes, the organisation controls which external services can communicate with its network, reducing potential attack vectors and ensuring that patient data is not inadvertently routed or exposed beyond its intended scope. This contributes to a secure processing environment under GDPR Article 32.

In summary, adopting these network security best practices for ExpressRoute and general cloud networking provides a strong foundation for compliance with UK GDPR and the security expectations of NHS Digital for handling sensitive patient records. The focus on encryption, access control, segmentation, integrity, and robust monitoring directly addresses the core requirements for protecting confidentiality, integrity, and availability of personal health data.

---

**Next Step Suggestion:** To further strengthen your compliance argument, consider conducting a detailed Data Protection Impact Assessment (DPIA) for the specific patient record systems utilising ExpressRoute, mapping each technical control to the identified GDPR risks and specifying how they are mitigated. This will provide granular evidence for senior leadership on your compliance posture.
Excellent question. You are right to challenge that assumption, and the official guidance from NHS England and the National Cyber Security Centre (NCSC) provides a strong foundation for your argument.
Here is a structured breakdown of why HTTPS over the public internet is not considered sufficient for protecting patient data between two trusted networks, based on the security frameworks the NHS has adopted.
The Foundation: NHS Security and Compliance Frameworks
Any organisation that has access to NHS patient data and systems is mandated to use the Data Security and Protection Toolkit (DSPT). This is a mandatory self-assessment tool that measures performance against the 10 data security standards set by the National Data Guardian (NDG).[1, 2]
Crucially, for cloud and internet security, NHS England's guidance explicitly adopts the NCSC's 14 Cloud Security Principles as the core standard for all healthcare providers.[3] Your argument should be framed around these official principles.
Argument 1: "Data in Transit Protection" Requires More Than Just Encryption
The idea that "HTTPS is enough" focuses narrowly on encryption. However, the NHS-adopted NCSC guidance is much broader.
NCSC Principle 1: Data in transit protection states that data must be protected against tampering and eavesdropping through a combination of three things:

- Encryption (what HTTPS provides)
- Service Authentication (what the 'S' in HTTPS provides)
- Network-level Protections [4]
  Relying on HTTPS over the public internet only satisfies the first two points. A private connection, such as a Site-to-Site VPN, is the network-level protection that completes the requirement. It creates a trusted, controlled path that denies an attacker the ability to even intercept the data in the first place.
  In short: The official guidance requires a layered approach. HTTPS is one layer, but the network itself must also be protected.
  Argument 2: Private Networks Eliminate the Public Attack Surface, Aligning with "External Interface Protection"
  This is the most powerful part of your argument. The moment you expose an endpoint to the public internet, you create an attack surface.
  NCSC Principle 11: External interface protection mandates that "all external or less trusted interfaces to the service should be identified and defended".[4, 5]
  The guidance explicitly acknowledges that internet-facing interfaces are inherently more susceptible to attack and must be robustly defended against threats like [5]:
- Denial-of-Service (DoS) attacks
- Authentication attacks (e.g., password spraying)
- Application-level attacks (e.g., SQL injection)
  By connecting your two private networks directly, you are adhering to this principle in the most effective way possible: you are eliminating the external interface entirely. There is no public route to attack. This aligns perfectly with the NDG's Data Security Standard 9, which requires a strategy for "protecting IT systems from cyber threats".[6]
  Argument 3: The Concept of a "Secure Data Environment" Presumes Isolation
  NHS strategy is moving towards the use of Secure Data Environments (SDEs) for handling patient data.[7] The security requirements for these environments include:
- Strong network security: Firewalls and intrusion detection systems to block unauthorized access.
- Regular security testing: Penetration testing and vulnerability scanning of the platform and its connections.[7]
  This model is built on the principle of a controlled, isolated setting ("safe settings") where access is prevented by default.[7] Exposing these environments to the public internet fundamentally contradicts the SDE model by creating an uncontrolled entry point that must then be defended, rather than being private by design. Furthermore, NHS guidance on Network Segmentation reinforces this, advocating for the creation of smaller, isolated network segments to limit the "blast radius" of any potential cyber-attack.[8, 9]
  Summary for Your Discussion
  You can structure your final argument as follows:
- Compliance is Non-Negotiable: As handlers of NHS patient data, we are bound by the Data Security and Protection Toolkit (DSPT), which mandates adherence to the NDG and NCSC security standards.[1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
- HTTPS is Only Half the Story: NCSC Principle 1 requires both encryption (HTTPS) and network-level protection. A private connection is the network-level protection.[4]
- Private Networks Eliminate the Attack Surface: NCSC Principle 11 requires defending external interfaces. By not having a public interface, we are implementing the strongest possible defence and negating a whole class of internet-based threats.[4]
- This Aligns with a Defense-in-Depth Strategy: The NHS security model is built on layers. A private network is the foundational layer of control. Placing HTTPS inside that private network provides a second, application-specific layer. Both are necessary to demonstrate due diligence in protecting patient data.
  Of course. This is a critical point to clarify. Relying solely on application-level controls for defense when you have public endpoints is like putting a state-of-the-art lock on a door made of cardboard. The lock itself (HTTPS, application logic) might be strong, but it ignores the fundamental weaknesses of the structure it's attached to.

Based on the architecture we've discussed and official NHS and NCSC security principles, here is a detailed analysis of the risks involved.

### The Fundamental Flaw: Confusing Message Security with Endpoint Security

Application-level controls, including HTTPS, are designed to protect the **application and its data stream** They do an excellent job of ensuring that the *conversation* between a client and your server is private and unaltered.

However, they do nothing to protect the **server, operating system, and network infrastructure** that the application runs on. By creating a public endpoint, you expose this entire underlying stack to the global internet, and application controls are largely blind to the threats that target it.

Here are the specific, tangible risks this creates:

#### 1. You Create a Permanent, Global Attack Surface

A public IP address is an open invitation It allows anyone, anywhere, to connect to your system This immediately exposes you to a constant barrage of automated and targeted attacks that are impossible on a private network.

- **What this means:** Malicious actors and automated scanners are continuously probing the entire internet for vulnerable systems. Your public endpoint will be discovered within minutes and subjected to:
  - **Reconnaissance and Fingerprinting:** Attackers will identify the exact versions of your web server, operating system, and other software components, building a blueprint of your stack to find known weaknesses
  - **Vulnerability Scanning:** Your endpoint will be automatically tested against a vast library of known exploits. If you miss a single patch for any component in the public-facing stack, it can lead to a breach The WannaCry attack that severely impacted the NHS exploited exactly this kind of unpatched, public-facing vulnerability
- **The Risk:** You are forced into a reactive, 24/7 defensive posture. You must patch every component of the public-facing stack perfectly and instantly. A private network, by contrast, is invisible to these scanners. You can't attack what you can't see.

#### 2. You Become Vulnerable to Attacks That Bypass the Application Logic

Many of the most damaging attacks do not target your application's features but the infrastructure that hosts it. Application-level controls have no defense against these.

- **What this means:** As stated in the NCSC's **Principle 11: External interface protection**, which the NHS adopts, internet-facing interfaces must be robustly defended against a specific set of threats that application code is not designed to handle These include:
  - **Denial-of-Service (DoS/DDoS) Attacks:** An attacker can flood your public IP with traffic, overwhelming the server or firewall and making your service unavailable for legitimate users. This can disrupt critical healthcare delivery
  - **Authentication Attacks:** Your login interfaces will be subjected to relentless automated attacks like password spraying and credential stuffing, attempting to break into user accounts.
  - **Protocol-Level Exploits:** Attackers can target vulnerabilities in the underlying TLS/SSL libraries or the TCP/IP stack itself, long before the traffic ever reaches your application code.
- **The Risk:** Your service's **availability** is under constant threat. Even if your application's data remains secure, the service can be knocked offline, which is an unacceptable risk for critical healthcare systems.

#### 3. A Single Breach Creates a Foothold for Lateral Movement

This is perhaps the most critical risk. If an attacker successfully bypasses your application-level controls or exploits a vulnerability in the underlying server, they are now **inside your network perimeter**.

- **What this means:** Once inside, the attacker's goal is to move "laterally" to other, more valuable systems, like the databases holding patient data If the network is not properly segmented, a single breach of a public-facing web server can lead to the compromise of the entire network.
- **The Risk:** This directly contradicts the official NHS England guidance on **Network Segmentation**, which is designed specifically to limit the "blast radius" of an attack and prevent this kind of lateral movement. Relying solely on application controls on a public endpoint creates a single point of failure that, if breached, renders your internal network segmentation ineffective.

#### 4. It Places an Unsustainable Burden on the Application Layer

This strategy forces your application and its immediate security layers (like a Web Application Firewall or WAF) to be responsible for *all* security. This is a fragile and incomplete model.

- **What this means:** Your application developers must be perfect. They must write code that is completely free of common vulnerabilities like SQL injection or cross-site scripting. While this is always the goal, it is an unrealistic expectation. The NHS Secure Boundary service exists precisely because this is so difficult, providing a national standard of next-generation firewalls (NGFW) and WAFs to protect internet traffic.
- **The Risk:** You are concentrating all your risk on a single, thin layer of defense. A true "defense-in-depth" architecture, as required by the NHS "Secure from day zero" principle, uses multiple, independent layers of security. A private network is the foundational layer; application controls are the next. Relying on only one is a violation of this core security principle.

### Summary: A Flawed Architecture

Relying solely on application-level controls with public endpoints is a fundamentally flawed strategy because it mistakes a secure *message* for a secure *system*. It creates a massive and unnecessary attack surface, exposes the service to availability attacks, and undermines the entire principle of a layered, segmented defense that is mandated by NHS and NCSC security standards.

---

### Introduction

The prevailing narrative asserts that while HTTPS (HTTP over TLS/SSL) is foundational for securing Internet communications, it is insufficient on its own for transmitting highly sensitive data—such as patient records—between two private networks. The claim implies that private networking solutions, including VPNs or dedicated communication channels, are a necessary complement, if not a complete substitute, to HTTPS in these scenarios. This report acts as a devil’s advocate to that perspective by challenging the notion that HTTPS is inherently insufficient and that private networking is the indispensable solution for protecting highly sensitive data. A thorough examination of HTTPS’s robust security guarantees, its compliance with regulatory mandates, and the cost-benefit trade-offs of private networks highlights several arguments against the claim.

### Robustness of Modern HTTPS Implementations

Modern HTTPS implementations rely on the latest versions of the Transport Layer Security (TLS) protocol, such as TLS 1.3, which provide strong cryptographic protection. HTTPS ensures confidentiality by encrypting data in transit with advanced cipher suites that achieve perfect forward secrecy. The encryption mechanisms employed ensure that even if communication is intercepted, the underlying sensitive data remains unintelligible without the appropriate session keys.

Furthermore, HTTPS guarantees data integrity through cryptographic hashes or authenticated encryption modes (for example, AES-GCM), making unauthorized modifications detectable. The authentication component—predicated on a robust public key infrastructure (PKI)—verifies the identities of communicating parties. When a client connects to a server, the server presents an X certificate that is authenticated against trusted Certificate Authorities (CAs). Provided the certificate is valid and has not been compromised, the connection is considered secure.

When properly configured, HTTPS has repeatedly demonstrated its capacity to protect sensitive data during transmission. Clinical environments, financial systems, and e-commerce platforms worldwide have relied on HTTPS to secure highly confidential interactions over the public Internet. As long as best practices are followed—such as enforcing HSTS (HTTP Strict Transport Security), using certificate pinning where appropriate, and maintaining regular certificate management—HTTPS alone can be a sufficing solution for secure data transmission.

### Regulatory and Compliance Considerations

Privacy and data protection regulations worldwide have specific requirements for protecting sensitive data during transmission. For instance, in the United States, the Health Insurance Portability and Accountability Act (HIPAA) mandates that protected health information (PHI) must be securely transmitted using encryption. Similarly, the European Union’s General Data Protection Regulation (GDPR) requires data protection measures that mitigate risks during transit.

Industry guidance and regulatory frameworks do not categorically insist on the use of private networks as a prerequisite for compliance. Instead, they emphasize that data in transit must be encrypted and that organizations must implement comprehensive security measures to protect against unauthorized interception. HTTPS, when implemented with strong cryptography and proper configuration, meets these compliance criteria. It has therefore been widely accepted as an adequate mechanism for the secure transmission of sensitive data in various regulated sectors.

Furthermore, reliance on HTTPS aligns with evolving best practices that prioritize multi-layered security strategies. While additional measures such as private networks can provide defense in depth, they are not an exclusive requirement dictated by regulatory bodies. The emphasis remains on ensuring that all transmission channels—public or private—use strong encryption and proper authentication mechanisms.

### Threat Model and Endpoint Considerations

HTTPS addresses a range of threats that are critical to secure data transmission. It is designed to mitigate man-in-the-middle (MITM) attacks, tampering, and eavesdropping. In scenarios where patient records are transmitted, HTTPS secures the data during transit irrespective of whether the underlying network is public or private. This end-to-end security provided by HTTPS ensures that even if communications traverse multiple network segments, the sensitivity of the data remains protected.

It is crucial to recognize that the primary vulnerabilities often lie at the endpoints rather than within the transmission channel itself. Once data reaches the endpoints, it must be decrypted, and at that point, the system’s internal security measures become paramount. Regardless of whether the transmitted data passed through a public or private network, endpoint security—including robust access controls, regular patching, and malware protection—is essential. Relying solely on private networking while neglecting endpoint hardening may foster a false sense of security.

By focusing on strengthening endpoint security and ensuring that HTTPS is implemented according to stringent best practices, organizations can mitigate the risk of exposure. Most vulnerabilities exploited in targeted attacks do not arise during the transit phase, but instead from weak endpoint configurations or inadequate operational security. Thus, while private networking may reduce the exposure of network segments, HTTPS remains the critical mechanism for ensuring that data is secured during transfer.

### Evaluating the Utility of Private Networking

Private networking solutions, such as Virtual Private Networks (VPNs) or dedicated leased lines, are often presented as the necessary complement to HTTPS for highly sensitive communications. These networks create a controlled environment by limiting physical and logical access to authorized users. However, several arguments challenge the notion that private networking is essential when modern HTTPS is properly implemented.

Firstly, private networks add complexity. The design, deployment, and maintenance of private network infrastructures require significant financial and operational resources. In many cases, the cost and administrative overhead associated with establishing and securing a private network may not be justified when an adequately configured HTTPS connection can deliver comparable protection for data in transit.

Secondly, private networks introduce their own vulnerabilities. Although they restrict access through controlled means, misconfigurations or outdated systems within these networks can create exploitable gaps. In an environment where HTTPS encrypts the end-to-end communication channel, the encryption would still prevail even if a private network were compromised. Relying on the isolation provided by a private network could lead to complacency about endpoint security and the overall data protection posture.

Additionally, private networking might reduce the attack surface by limiting exposure; however, encrypted data traversing the public Internet via HTTPS is already shielded by strong cryptographic measures. Therefore, the incremental security gained by adding a private network may be marginal, particularly if robust HTTPS practices are in place. This raises the question of whether the complexity and cost of private networking are justified by the degree of additional protection provided.

Another consideration is scalability and interoperability. Organizations with geographically distributed teams and remote operations often find that relying on private networks can hinder agility and responsiveness. In contrast, HTTPS is universally supported across platforms and devices, simplifying secure access for a broad range of users and environments.

### Comparative Analysis: HTTPS Versus Private Networking

A comparative analysis of HTTPS and private networking reveals several points that challenge the claim implying the necessity of private networks for sensitive data transfer:

1. Modern HTTPS solutions provide strong encryption, integrity checks, and robust authentication. When implemented with current best practices, HTTPS effectively secures data against common threats such as MITM attacks and eavesdropping.
2. Many regulatory standards and frameworks only require encrypted transit of data without mandating the exclusive use of private networks. Organizations have demonstrated compliance with standards like HIPAA and GDPR by using HTTPS with proper security controls.
3. Additional layers of network isolation provided by private networking, while beneficial under certain threat models, can also lead to increased complexity and potential misconfigurations. These complexities might inadvertently create new vulnerabilities rather than offering a straightforward enhancement to security.
4. Private networks often aim to reduce the risk of exposure by ensuring that data never leaves a controlled environment. However, HTTPS inherently provides end-to-end encryption regardless of the underlying network’s nature. In environments where the endpoints are secure and well-managed, the relative security benefits of a private network may be redundant.
5. Cost and scalability considerations favor HTTPS, as it is a mature, widely adopted technology with broad interoperability. For distributed organizations, the agility provided by the widespread availability of HTTPS, paired with rigorous endpoint security, can often outweigh the benefits of private networking.

### Real-World Considerations and Case Studies

There are numerous instances where high-stakes environments successfully rely on HTTPS alone provided that it is configured and managed effectively. Financial institutions and e-commerce platforms routinely secure transactions using HTTPS, despite managing sensitive data over public networks. In many healthcare IT environments, secure web services leveraging HTTPS have met regulatory requirements and maintained robust security postures when combined with strong endpoint and application-level security measures.

An analysis of several documented breaches reveals that many successful attacks occur due to endpoint exploits or mismanagement of certificates rather than a failure of HTTPS protocols themselves. Organizations that invest in continuous monitoring, automated patch management, and certificate lifecycle management often experience fewer vulnerabilities than those that adopt overly complex private networking solutions with lax endpoint controls.

Furthermore, case studies indicate that a layered, defense-in-depth approach does not necessarily require private networking as an isolated solution. Encryption of data in transit via HTTPS, when combined with strong identity and access management (IAM) protocols, session management, and network segmentation at higher layers of the security architecture, offers sufficient protection against most adversarial scenarios targeting sensitive data.

### Weighing Operational Trade-Offs

The operational trade-offs of mandating private networking over a well-configured HTTPS infrastructure deserve careful consideration. Private networks imply dedicated investments in hardware, specialized personnel, and ongoing maintenance. This resource allocation may divert focus from other critical security areas such as hardening endpoints, continuous monitoring, and rapid vulnerability patching.

Moreover, when private network infrastructures evolve to support remote access and cloud-based environments, maintaining consistent security policies across heterogeneous systems becomes increasingly challenging. Modern cloud providers typically enforce HTTPS at scale as their primary secure communication protocol, and many organizations have transitioned to hybrid models that leverage the inherent security of HTTPS without fully isolating data on private networks.

When evaluating cost, benefit, and operational complexity, the benefits of using HTTPS to secure data transmissions remain significant. Its ability to deliver effective end-to-end encryption, combined with the relatively low complexity and broad compatibility, often results in a more pragmatic and resilient security posture compared to the overhead and potential misconfigurations associated with private networking.

### Conclusion

The claim that HTTPS is insufficient on its own for the transmission of highly sensitive data—mandating the use of private networking—takes a narrow view of the overall risk landscape. Modern HTTPS implementations incorporating TLS 1.3, strong cipher suites, and rigorous certificate management protocols provide robust protections for data in transit. In regulated environments, such as those involving patient records, compliance requirements center on the encryption and integrity of data during transmission—a goal well met by HTTPS when configured according to best practices.

While private networking offers the benefits of an isolated, controlled environment, it also introduces increased complexity, additional costs, and potential vulnerabilities that may, in certain cases, offset its theoretical advantages. Endpoint security remains the critical factor regardless of whether data traverses a public or private network, and the extensive experience of industries relying on HTTPS demonstrates that, when implemented correctly, it is a highly effective measure for protecting sensitive data.

In summary, HTTPS alone, when meticulously managed and integrated into a broader, defense-in-depth strategy, is sufficient for secure data transmission—even for highly sensitive patient records. The additional reliance on private networking should be seen as a complementary strategy rather than an indispensable requirement, and its implementation must be carefully weighed against potential operational drawbacks.

You have analyzed this situation perfectly, and your intuition is spot on. The message from your contact reveals significant ambiguity and proposes a solution (whitelisting a public IP) that is fundamentally at odds with the goal of securely connecting two private networks.

## Analysis of the Current Proposal (and Why It's Wrong)

Your contact's message about a "single IP" vs. "multiple IPs + load balancer" and your ticket to "set up a fixed IP for the azure fw to whitelist" are classic signs of a plan to route traffic over the **public internet**.

Here’s why that approach is incorrect for this scenario:

1. **It's Insecure:** It needlessly exposes your internal services to the public internet. Even with firewall whitelisting, you are creating a public endpoint that can be scanned, probed, and potentially attacked. The goal of having private networks is to avoid this entirely.
2. **It's Inefficient:** Traffic would have to exit your Azure VNet, travel across the public internet, and then enter the AWS VPC. This introduces unnecessary latency and multiple points of failure compared to a direct private link.
3. **It's Costly:** Both AWS and Azure charge for data egress to the public internet. You would be paying to send data out of Azure and paying to receive it in AWS, which is far more expensive than using dedicated private connectivity options.
4. **It's Brittle:** Relying on whitelisting static public IPs is a fragile solution. If that IP ever needs to change, the connection breaks until firewall rules are manually updated.

You are absolutely right to challenge this. The "path of least resistance" should not mean the path of least security.

## The Correct Approach: A Secure Private Bridge

The industry-standard and correct way to connect two private cloud networks is to build a secure, encrypted tunnel directly between them. This creates a private bridge, making the two networks behave as if they are one. The key benefit is that all communication happens over **private IP addresses**, never touching the public internet.

The best-practice solution for this is a **Site-to-Site VPN connection**.

### How a Site-to-Site VPN Works

A Site-to-Site VPN establishes a persistent, encrypted tunnel over the internet between a **Virtual Private Gateway** in your AWS VPC and a **Virtual Network Gateway** in your Azure VNet.

Here are the core components:

| In AWS                            | In Azure                          | Its Purpose                                                                                                                                                                            |
| --------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Virtual Private Gateway (VGW)** | **Virtual Network Gateway (VNG)** | This is the VPN concentrator for the entire virtual network. It's the endpoint of the VPN tunnel within its respective cloud. 1                                                        |
| **Customer Gateway (CGW)**        | **Local Network Gateway (LNG)**   | This is a resource that represents the *other* side of the connection. The AWS CGW contains the public IP of the Azure VNG, and the Azure LNG contains the public IP of the AWS VGW. 2 |

Once the tunnel is established, you configure routing (ideally using BGP for dynamic route exchange) to teach each network how to reach the private IP address ranges of the other

## Clarifying the Ambiguity for Your Team

The discussion of "single IP vs. multiple IPs" is still relevant, but it applies to the **VPN Gateways**, not your applications. For high availability, both AWS and Azure gateways can be configured in an active-active mode, providing multiple public IP endpoints for the VPN tunnels themselves, ensuring the connection remains up even if one gateway instance fails This is the proper context for that part of the discussion.

## Recommended Action Plan and Talking Points

For your upcoming call with TT and Gareth, you should steer the conversation away from public IPs and towards establishing a proper private connection.

**Your Position:** "The core requirement is to enable secure, bidirectional communication between our private AWS SDE network and our private Azure FF network. The most secure, reliable, and cost-effective way to achieve this is by establishing a Site-to-Site VPN connection between the two clouds, not by routing traffic over the public internet."

**Key Talking Points:**

1. **Reject the Public IP Whitelisting Model:** Clearly state that this approach is insecure and goes against the principle of having private networks.
2. **Propose the Site-to-Site VPN Architecture:** Frame it as the standard, best-practice solution for multi-cloud private networking.
3. **Focus on Private IP Routing:** Emphasize that with a VPN, services in AWS and Azure will communicate directly using their internal, private IP addresses.
4. **Discuss Authentication:** Mention that the VPN tunnel itself can be authenticated using either pre-shared keys or, for higher security, digital certificates issued by a private CA, which aligns with modern security practices
5. **Plan for High Availability:** Address the "multiple IPs" concern by explaining you'll use active-active VPN gateways on both ends to create redundant tunnels, ensuring the connection is resilient

By reframing the problem and solution this way, you move from a tactical (and flawed) workaround to a strategic and secure architectural decision. You are correct to push for using the specialized tools that AWS and Azure provide for exactly this purpose.
