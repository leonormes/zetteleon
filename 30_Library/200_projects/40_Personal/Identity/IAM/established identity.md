---
aliases: []
confidence: 
created: 2025-07-05T04:51:55Z
epistemic: 
id: established identity
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: established identity
type:
uid: 
updated: 
version:
---

Identity and Access Management (IAM) is a framework of policies, processes, and technologies that ensures appropriate access to resources within an organization while protecting those resources from unauthorized access. It's essentially about managing "who has access to what" within a company's digital environment. Microsoft Entra ID, formerly known as Azure Active Directory (Azure AD), is Microsoft's cloud-based identity and access management service. It serves as a comprehensive solution for identity, access management, and security, helping to secure access to data in applications both on-site and in the cloud, while simplifying user and group management.

Here’s how IAM systems like Microsoft Entra ID establish and verify an identity:

## 1. Establishing an Identity (Identity Management)

In the digital realm, identity is the foundation for establishing trust and facilitating access to resources. Digital identity encompasses elements like personal identifiers (e.g., usernames, email addresses, employee IDs), biometric data (e.g., fingerprints, facial recognition), and cryptographic credentials (e.g., digital certificates, security tokens).

Identity management involves administering these digital identities throughout their lifecycle. This includes processes such as:

- **Registration/Creation:** This is the initial step where a digital identity is generated and securely linked to a real-world entity, such as a human or a computing device. Microsoft Entra ID can be used to create and manage a single identity for each user across your hybrid enterprise, keeping users, groups, and devices in sync. Identities are assigned from a naming space and associated with an authentication credential. For example, in a local identity model, a host system maintains a registry of users, and external entities wishing to use the system must acquire an identity unique to that registry.
- **Provisioning:** This is the process of creating, modifying, or deleting user accounts and ensuring consistency of digital identities across multiple systems. Microsoft Entra ID supports automated user provisioning to SaaS applications, which includes creating, maintaining, and removing user identities as status or roles change.It can also provision identities from external authoritative systems (like HR systems) to Microsoft Entra ID, from Microsoft Entra ID to applications, and between Microsoft Entra ID and Active Directory Domain Services.
- **Maintenance and Updates:** Identity information must be constantly updated as people join or leave an organization, change roles, or start/finish projects. For instance, a user's role change can dynamically update their access controls. Microsoft Entra ID helps manage the lifecycle of user accounts.

## 2. Verifying an Identity (Authentication)

Authentication is the process of verifying the identity of users or entities attempting to access a system. It is the first layer of defence against unauthorized access. The goal of authentication is to ensure that only authorized users or entities can access a computer system, network, or particular service. Trust in identity authentication is established by computing an assertion that the entity performing authentication is presented with information that only the entity being authenticated can provide; this is referred to as "proof of possession (PoP) of identity".

IAM systems, including Microsoft Entra ID, implement various authentication methods based on the sensitivity of the data and risk level. Common methods include:

- **Credential-based Authentication:** This typically involves providing credentials like a username and password. While simple, traditional passwords are prone to being forgotten, reused, or easily compromised. Microsoft Entra ID provides password policy enforcement, including length and complexity requirements, forced periodic rotation, and account lockout after failed attempts. Smart lockout in Microsoft Entra ID helps protect against brute-force attacks by recognizing valid users from attackers.
- **Biometric Identification:** This is an automated technique that measures and statistically analyzes a person's unique physiological or behavioural traits to verify identity. Biometric authentication is preferred in many industries due to its quick certification procedure and resistance to spoofing and impersonation, enhancing IAM system security. When credentials match a scanned fingerprint, access is granted, providing a strong identification check.
- **Challenge-Handshake Authentication Protocol (CHAP):** CHAP is widely used in network communications for secure verification, particularly in remote access scenarios. It uses cryptographic techniques and exchanges challenge-response messages between users and authentication servers to authenticate user identities and prevent eavesdropping and replay attacks.
- **Multi-Factor Authentication (MFA):** This method requires more than one verification method to safeguard access to data and applications. It adds a critical second layer of security to user sign-ins and transactions. Microsoft Entra MFA delivers strong authentication via various options, including phone calls, text messages, mobile app notifications or verification codes, and third-party OAuth tokens. Organizations can enforce MFA for all users, including Global Administrators.
- **Passwordless Authentication:** Microsoft Entra ID supports various passwordless authentication options, such as Windows Hello for Business, Microsoft Authenticator, Passkeys (FIDO2), and Certificate-based authentication (CBA). These methods align with a Zero Trust model, shifting towards a credential-free approach for user verification. FIDO2 security keys, for example, enable phishing-resistant authentication directly against Microsoft Entra ID.
- **Token-Based Authentication:** IAM solutions integrate with technologies like Security Assertion Markup Language (SAML), OpenID Connect (OIDC), and OAuth to enable secure authentication and authorization at an enterprise scale.
  - **SAML** makes Single Sign-On (SSO) possible by notifying other applications that a user is verified after successful authentication. Microsoft Entra ID signs SAML assertions with a unique certificate and specific standard algorithms, and can also encrypt SAML assertions for enhanced security.
  - **OpenID Connect (OIDC)** adds an identity aspect to OAuth 2.0, sending tokens with user information (like name, email, birthday) between the identity provider and service provider. These tokens are easy for services and apps to use, useful for authenticating mobile games, social media, and app users.
  - Microsoft Entra ID often acts as the Identity Provider (IdP) in these scenarios, verifying user credentials and issuing tokens.

## 3. Role of Attributes in Verification

Digital identity encompasses a broad range of elements, including identifiers and **attributes**. Attributes are specific pieces of information associated with a user or resource, such as a name, role, or security clearance. They are crucial for making informed access and authorization decisions and enforcing access policies. For example, a user's role determines their access to specific files, applications, or systems. Microsoft Entra ID stores user attributes in an identity management database, which can include details like username, email, phone number, job title, and security clearance level.

## 4. Establishing Trust

Trust in a system is predicated on the trust a system or network establishes in an identity. Modern IAM systems form the foundation of Zero Trust security models by enforcing the principle of "never trust, always verify". This means continuous authentication beyond the initial login and contextual authorization based on factors like device, location, and behavior.

Federated Identity Management (FIM) allows the use of a set of identity attributes across multiple systems or organizations, shifting the verification of credentials toward the identity provider. This cross-organizational trust is foundational to federated identity, enabling organizations to acquire necessary information about a foreign entity securely. Technologies like SAML, OpenID, OAuth, and tokenization enable these federated identities. Microsoft Entra ID supports identity federation by integrating with on-premises directories via Active Directory Federation Services (AD FS), synchronization, and replication.

Microsoft Entra ID's capabilities like Conditional Access policies use identity signals to make access decisions and enforce organizational policies. Identity Protection leverages adaptive machine learning algorithms and heuristics to detect anomalies and risk detections that might indicate a compromised identity, generating reports and alerts for investigation and remediation.

Microsoft Entra ID also supports "managed identities" for Azure resources, providing Azure services with an automatically managed identity that can authenticate to any service supporting Microsoft Entra authentication without needing to store credentials in code. These identities are a special type of service principal that eliminates the need for manual credential management.

In essence, Microsoft Entra ID acts as a centralized authority (IdP) for identities, streamlining registration, storing comprehensive identity attributes, and offering a robust suite of authentication methods to verify those identities, all while enabling complex access control decisions and supporting a Zero Trust security posture.

Would you like to explore any of these authentication methods in more detail, or perhaps discuss how authorization works in conjunction with identity verification?
