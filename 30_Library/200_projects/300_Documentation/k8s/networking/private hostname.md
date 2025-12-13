---
aliases: []
confidence: 
created: 2025-02-25T21:47:46Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: private hostname
type:
uid: 
updated: 
version:
---

In a private VPC with an EKS cluster, you have considerable flexibility in naming hostnames for your web applications that are not accessed via the public internet. Here's a breakdown of the rules and considerations:

General Rules and Flexibility

 - Private Networks, Private Names: Since your web applications are within a private network and not exposed to the public internet, you are not bound by public DNS naming conventions or restrictions. You can choose any hostname that is valid within your private DNS zone.
 - Internal DNS Resolution: As long as your private VPC has DNS resolution enabled, and your EKS cluster is configured to use this DNS, your applications within the cluster will be able to resolve hostnames to internal IP addresses.
 - No Public Registration Needed: You do not need to register these hostnames with any public DNS registrars, as they are for internal use only.
Recommended Practices and Considerations
 - DNS Hostnames and Resolution: Ensure that both DNS Hostnames and DNS Resolution are enabled for your VPC. This is a fundamental requirement for EKS clusters to function correctly in a private VPC. You can check and enable these settings in the AWS Management Console under your VPC settings.
- Private Hosted Zones in Route 53: For better management and control over your internal DNS, it's highly recommended to set up a private hosted zone in Route 53.
- Domain Name: Choose a domain name for your internal zone (e.g., eks.internal, private.company.com). This domain will be used as the suffix for your internal hostnames.
- VPC Association: Associate this private hosted zone with your VPC. This ensures that DNS queries within your VPC for your chosen domain are directed to Route 53 Private DNS.
- CoreDNS Configuration: EKS clusters use CoreDNS for internal DNS resolution. You may need to modify the CoreDNS ConfigMap to forward queries for your private hosted zone domain to the VPC's DNS resolver. This typically involves adding a forward zone in the CoreDNS configuration that points to 169.254.169.253, which is the VPC's DNS resolver.
- Hostname Conventions: While you have flexibility, it's still good practice to follow some conventions for clarity and organization:
   - Use descriptive names that reflect the application or service (e.g., webapp-backend.eks.internal, internal-api.private.company.com).
   - Consider using subdomains to further organize your services (e.g., backend.webapp.eks.internal, api.internal.private.company.com).
 - Security: Implement appropriate security measures to control access to your private DNS server and ensure only authorized resources can resolve internal hostnames. Use IAM roles and security groups to restrict access.
In summary, for web applications within a private EKS cluster, you can use virtually any hostname as long as it adheres to basic DNS syntax and is resolvable within your private network. Using a private hosted zone in Route 53 and configuring CoreDNS is the recommended approach for managing these internal hostnames effectively. This setup allows you to define custom domain names and ensure reliable internal DNS resolution within your private EKS environment.

Hostnames in networks serve several critical purposes, and while they are definitely helpful for humans, their function goes far beyond just being easily identifiable names. Here's a breakdown:

Key Uses of Hostnames in Networks:

 - Human-Friendly Identification: You are right that one of the primary reasons for hostnames is to make it easier for humans to interact with and identify devices on a network. Instead of remembering and typing complex numerical IP addresses (like 192.168.1.10 or 2001:db8::c0ca:babe), humans can use memorable and meaningful names (like web-server-01 or printer-office). This greatly simplifies tasks like:
   - Accessing servers: Instead of typing an IP address in a web browser, you can type a hostname like company-intranet.local.
   - Connecting to remote machines: Using SSH or other remote access tools, you can connect using ssh user@hostname.example.com instead of ssh user@192.168.1.10.
   - Referring to devices in documentation and scripts: Hostnames make configurations and instructions much clearer and easier to understand.
 - Abstraction of IP Addresses: Hostnames provide a layer of abstraction over IP addresses. IP addresses can change (especially in dynamic environments using DHCP), but hostnames can remain relatively constant. This means:
   - Services remain accessible even if IP addresses change: If a server's IP address is reassigned, as long as the hostname is still correctly associated with the new IP address in the DNS system, users can continue to access the service using the same hostname.
   - Simplified network management: Network administrators can manage services and devices using consistent hostnames, without needing to constantly update configurations due to IP address changes.
 - DNS (Domain Name System) Resolution: Hostnames are fundamental to the Domain Name System (DNS). DNS is the phonebook of the internet (and private networks). It translates human-readable hostnames into the IP addresses that computers need to communicate with each other. This translation process is essential for:
   - Web Browse: When you type a website address (e.g., <www.example.com>) into your browser, DNS resolves this hostname to the IP address of the web server hosting that website.
   - Email delivery: Email systems use DNS to find the mail servers associated with a domain name to deliver emails.
   - All network communication: Many network protocols and applications rely on DNS to resolve hostnames to IP addresses before establishing connections.
 - Service Discovery: In modern networks, especially in cloud environments and microservices architectures, hostnames play a role in service discovery. Services can register themselves with a service registry (often integrated with DNS), allowing other services to find and communicate with them using their hostnames.
 - Configuration and Automation: Hostnames are used extensively in configuration files, scripts, and automation tools to refer to specific devices or services. This makes configurations more portable and easier to manage.
In essence, hostnames are not just for human convenience. They are a crucial component of network infrastructure that enables:
 - Simplified human interaction.
 - Robust and flexible network communication.
 - Abstraction from underlying IP addressing.
 - Scalable and manageable network services.
While humans benefit from the ease of use hostnames provide, the underlying network infrastructure and machines rely on hostnames and the DNS system to function effectively. They are a fundamental building block of modern networks, enabling both human and machine communication.

While the terms "hostname" and "DNS name" are often used interchangeably, they are not strictly exactly the same thing, although they are very closely related and often refer to the same string of characters. Here's a breakdown of the nuances:

Hostname:

 - Definition: A hostname is the label assigned to a device (like a computer, server, printer, etc.) on a network. It's essentially a name given to identify that specific device.
 - Scope: Hostnames are primarily used within a local network or a specific administrative domain.
 - Examples: my-laptop, web-server-01, printer-office.
 - Configuration: Hostnames are typically configured directly on the device itself within its operating system settings.
 - Resolution (Local): Within a local network, hostnames can sometimes be resolved to IP addresses through local mechanisms like:
   - hosts file: A static file on each machine that maps hostnames to IP addresses.
   - NetBIOS/mDNS: Protocols for hostname resolution within a local network segment, often used for simpler networks without a dedicated DNS server.
DNS Name (Domain Name System Name):
 - Definition: A DNS name is a hostname that is part of the Domain Name System (DNS) hierarchy. It's a fully qualified domain name (FQDN) that is globally unique within the DNS system.
 - Scope: DNS names are used for devices and services that need to be accessible across the internet or within larger, more complex networks.
 - Examples: <www.example.com>, mail.google.com, webapp-backend.company.internal.
 - Configuration: DNS names are registered and managed within the DNS system, typically through DNS servers and registrars.
 - Resolution (Global and Hierarchical): DNS names are resolved to IP addresses through the hierarchical DNS system, starting from root servers and working down through domain name servers to find the authoritative server for the domain.
Key Differences and Relationship:
 - Scope and Uniqueness: The primary difference is scope and uniqueness. Hostnames are generally locally significant, while DNS names are designed to be globally unique within the DNS system.
 - DNS Integration: A DNS name is always a hostname, but a hostname is not always a DNS name. To be a DNS name, the hostname must be registered and resolvable within the DNS system.
 - FQDN (Fully Qualified Domain Name): DNS names are often referred to as FQDNs. An FQDN includes the hostname and all the domain levels up to the root. For example, in web-server-01.example.com, web-server-01 could be considered the hostname in a local context, but web-server-01.example.com is the DNS name or FQDN.
 - Resolution Mechanism: Hostnames can be resolved locally (using hosts files, etc.), while DNS names are resolved through the DNS system.
Analogy:
Think of it like names for people:
 - Hostname: Like a nickname you use with your close friends and family. It's locally understood within your immediate circle.
 - DNS Name: Like your full legal name. It's globally recognized and registered in official records (like the DNS system is for internet names).
In Practice - Interchangeability:
In many everyday situations, especially when discussing internet-facing services, people often use "hostname" and "DNS name" interchangeably, and it's usually understood to mean the fully qualified DNS name.
Example to illustrate:
Let's say you have a web server:
 - Hostname (Local): You might configure the server itself to have the hostname webserver.
 - DNS Name (Global): You might register a DNS record in your domain example.com to point <www.example.com> to the IP address of webserver. In this case, <www.example.com> is the DNS name or FQDN, and webserver is the local hostname of the machine.
In summary:
While "hostname" and "DNS name" are closely related and often used loosely to mean the same thing, DNS name specifically refers to a hostname that is part of the global Domain Name System and is used for internet-wide or large network resolution. Hostname is a broader term that can refer to any name assigned to a device, including those used only within local networks. When precision is needed, especially in networking contexts, it's best to be clear whether you are referring to a local hostname or a fully qualified DNS name (FQDN).

Yes, that's a very accurate and concise way to put it! A Fully Qualified Domain Name (FQDN) is indeed a hostname, but specifically formatted for inclusion and resolution within the Domain Name System (DNS).

Here's why that's a good way to think about it and some further clarification:

Accurate because:

 - It starts as a hostname: An FQDN begins with a hostname, which is the basic name you'd give to a device on a network.
 - Formatted for DNS: The "formatted" part is crucial. It highlights that to become a DNS name, the hostname needs to be extended with domain information to fit into the hierarchical structure of DNS.
Further Clarification - What "formatted for DNS" means:
 - Domain Suffix: "Formatted for DNS" primarily means appending a domain suffix to the hostname. This suffix indicates which domain the hostname belongs to within the DNS hierarchy. Examples of domain suffixes are .com, .org, .net, .co.uk, .internal, etc.
 - Fully Qualified: The "fully qualified" part means that the name is complete and unambiguous within the DNS system. It includes all parts of the domain hierarchy, all the way up to the root (though the root is often implied and not explicitly written).
 - Example Breakdown:
   - Let's say your hostname is webserver.
   - To make it a DNS name, you add a domain suffix, like example.com.
   - The FQDN becomes webserver.example.com. This is now formatted for DNS. DNS can resolve example.com to a nameserver, and then that nameserver can tell you about webserver within that domain.
In essence:
Think of a hostname as the first name of a device. To make it globally addressable in the DNS "phonebook," you need to add a "last name" (the domain) to create a full name (the FQDN) that DNS can understand and use to find the device's IP address.
So, your statement is a very accurate and helpful way to understand the relationship between hostnames and FQDNs in the context of DNS.
