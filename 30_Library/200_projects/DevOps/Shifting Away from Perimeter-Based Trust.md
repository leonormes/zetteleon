---
aliases: []
confidence: 
created: 2025-03-05T12:40:13Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:39Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [IAM]
title: Shifting Away from Perimeter-Based Trust
type: documentation
uid: 
updated: 
version:
---

That's an excellent question, and it gets to the very heart of the zero trust security model. Based on the materials I've provided, identity absolutely forms the foundation of zero trust security for several crucial reasons.

## Shifting Away from Perimeter-Based Trust

Traditional network security often operates on a perimeter-based model. This approach establishes a security boundary, like a firewall, around what is considered the "trusted" internal network. Anything within this perimeter is often implicitly trusted, or at least subject to less stringent security controls. The problem with this model, especially in modern, dynamic environments, is that once an attacker breaches the perimeter, they can often move laterally within the network with relative ease because the assumption of trust persists. This is often described as a "hard shell and soft interior".

Zero trust fundamentally rejects this notion of implicit trust based on network location. Instead, it operates on the principle of "never trust, always verify". In a zero trust framework, every user, device, application, and network flow is considered untrusted by default, regardless of its location – whether inside or outside a traditional network boundary.

## Identity as the New Perimeter

In the absence of trust based on network location, identity becomes the primary factor in determining access. The point of control shifts from physical network controls (like firewalls defining the perimeter) to the trusted identities of users, devices, and applications. This means that before any entity can access a resource, its identity must be rigorously authenticated and authorised.

## Key Principles Stemming from Identity-Centric Security

Several core principles of zero trust are directly enabled and driven by this foundational focus on identity:

- Identity-Driven: Access decisions are primarily based on the identity of the user or service requesting access. This includes verifying who they are through strong authentication mechanisms.
- Mutual Authentication: Not only is the user or device authenticated to the resource, but ideally, the resource should also be authenticated to the user or device. This establishes trust in both directions.
- Least Privilege: Once an identity is authenticated, it should only be authorised to access the specific resources and perform the actions necessary for its intended purpose. This principle limits the potential damage if an account is compromised.
- Explicit Verification: Every access request, regardless of origin, must be explicitly verified based on identity and other contextual factors before access is granted.
- Assume Breach: The zero trust model assumes that attackers may already be present within the network. Therefore, continuous verification and strict access controls based on identity are crucial to limit their movement and impact.
- Microsegmentation: By focusing on the identities of services and applications, zero trust facilitates microsegmentation of the network. Access is granted only between specific, identified services that need to communicate, rather than based on broader network segments. Consul's intentions feature, for example, uses service identity to authorise access between services.
- Secure Remote Access: With identity as the core, secure remote access can be achieved without relying solely on VPNs, which extend the trusted network perimeter. Tools like Boundary, mentioned in the context of HashiCorp's zero trust approach, secure remote access based on user identity and authorised access to specific systems.

## HashiCorp's Perspective

HashiCorp explicitly states that their approach to zero trust "starts with identity" and focuses on securing everything based on trusted identities. They highlight that enterprise-level identity platforms already often use this model, making integration into multi-cloud zero trust security more straightforward. Their suite of tools, Vault, Consul, and Boundary, leverage identity to manage secrets, secure services, and control remote access within a zero trust framework.

In summary, identity is the bedrock of zero trust security because it replaces the flawed assumption of trust based on network location with a model of explicit verification and authorisation for every entity seeking access to resources. This shift to an identity-centric approach is essential for securing the increasingly complex and dynamic environments of today, particularly with the rise of multi-cloud and remote work.

What aspect of identity in zero trust would you like to delve into next? Perhaps the different methods of strong authentication, or how identity is managed across multi-cloud environments? I can also offer a short quiz to check your understanding of this fundamental concept.
