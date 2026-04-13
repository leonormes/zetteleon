---
type: tmp_atoms
status: tmp
source_title: "Azure Entra Identity Best Practices & Remediation Plan"
source_url: "https://gemini.google.com/app/90721765fb79ed7a"
captured_utc: "2026-04-06T18:12:56+01:00"
signal_to_noise: "90% signal / 10% noise"
---

- Discarded conversational transitions ("Microsoft's guidance focuses heavily on...", "Here are the latest...").
- Discarded high-level summary tables in favour of discrete technical mechanisms.
- Discarded vendor-specific branding (e.g., "YubiKeys") where the underlying technology (FIDO2) is the signal.

### Atom 1: Phishing-Resistant MFA
- Kind: procedure
- Statement: Organisations should transition to phishing-resistant Multi-Factor Authentication (MFA) methods such as FIDO2 security keys, Windows Hello for Business, or certificate-based passkeys.
- Scope & Conditions: Applies to all user accounts, prioritising those with privileged access.
- Evidence: "Microsoft now strongly recommends FIDO2 security keys (like YubiKeys), Windows Hello for Business, or Microsoft Authenticator (certificate-based/Passkeys)."
- Implications:
    - Mitigates credential stuffing and sophisticated phishing attacks.
    - Reduces reliance on easily intercepted SMS and voice-based MFA.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, identity, mfa, phishing-resistance]

### Atom 2: Legacy Authentication Blocking
- Kind: mechanism
- Statement: Blocking legacy authentication protocols such as IMAP, POP3, and SMTP via Conditional Access prevents attackers from bypassing Multi-Factor Authentication.
- Scope & Conditions: Essential for environments where modern authentication is supported.
- Evidence: "Block outdated protocols (IMAP, POP3, SMTP) via Conditional Access. These bypass MFA and are the primary entry point for credential stuffing."
- Implications:
    - Closes a major attack vector for brute-force attacks.
    - Forces clients to use modern, secure authentication flows.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, conditional-access, legacy-auth, microsoft-entra]

### Atom 3: Continuous Access Evaluation (CAE)
- Kind: mechanism
- Statement: Continuous Access Evaluation (CAE) allows Microsoft Entra to revoke user sessions in near real-time when account security posture changes or location shifts significantly.
- Scope & Conditions: Requires compatible clients and services to be effective.
- Evidence: "Ensure CAE is enabled so that if a user's account is disabled or their location changes significantly, their session is revoked in near real-time..."
- Implications:
    - Reduces the window of opportunity for attackers using stolen tokens.
    - Provides immediate enforcement of identity policy changes.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, session-management, cae, zero-trust]

### Atom 4: Just-In-Time (JIT) Admin Access
- Kind: heuristic
- Statement: Administrative rights should be granted as "Just-In-Time" (JIT) eligible roles through Privileged Identity Management (PIM) rather than as permanent assignments.
- Scope & Conditions: Applies to all high-privilege roles like Global Administrator.
- Evidence: "No one should have permanent 'Global Administrator' or 'Security Administrator' rights. Use Microsoft Entra Privileged Identity Management (PIM) to grant 'Just-In-Time' (JIT) access..."
- Implications:
    - Minimises the attack surface of standing privileges.
    - Ensures all administrative actions are logged and time-bound.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, pim, jit, least-privilege]

### Atom 5: Global Administrator Limit
- Kind: constraint
- Statement: Organisations should maintain fewer than five Global Administrator accounts to limit the blast radius of a compromised identity.
- Scope & Conditions: General governance rule for Entra tenants.
- Evidence: "The 'Rule of 5': Microsoft recommends having fewer than five Global Administrators."
- Implications:
    - Simplifies auditing of high-privilege changes.
    - Forces the use of lower-privilege roles for day-to-day tasks.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [governance, blast-radius, identity-management]

### Atom 6: Emergency Access Account Protocol
- Kind: procedure
- Statement: Emergency access "break-glass" accounts must be cloud-only, excluded from standard MFA/Conditional Access, and monitored for any login activity.
- Scope & Conditions: Used only when primary authentication or identity services are unavailable.
- Evidence: "Maintain two 'Emergency Access' accounts that are excluded from MFA and Conditional Access. These should be cloud-only... and be monitored for any login activity."
- Implications:
    - Provides a recovery path during catastrophic identity failures.
    - Represents a high-risk configuration requiring strict monitoring.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [disaster-recovery, security-ops, break-glass]

### Atom 7: Workload Identity Governance
- Kind: heuristic
- Statement: AI agents and workload identities (Service Principals) must be governed with the same rigour as human identities, including the assignment of human sponsors.
- Scope & Conditions: Specifically relevant for 2026 automation-heavy environments.
- Evidence: "New for 2026, you must govern AI agents and Workload Identities (Service Principals) with the same rigour as humans. Assign 'Human Sponsors'..."
- Implications:
    - Prevents orphaned permissions in automated systems.
    - Ensures accountability for actions taken by non-human actors.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [ai-governance, workload-identity, security, 2026-trends]

### Atom 8: Shared Account Interactive Access Restriction
- Kind: failure_mode
- Statement: Interactive sign-in should be disabled for service and shared accounts to prevent unauthorised human access to automated identities.
- Scope & Conditions: Part of security hardening for shared infrastructure.
- Evidence: "Disable interactive sign-in for all service or shared accounts (e.g., fitfile-service, support, appleid)."
- Implications:
    - Forces the use of secure token-based or workload-based authentication.
    - Reduces the risk of credential leakage for shared accounts.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [security, service-accounts, hardening, access-control]

### Atom 9: Directory Creation Restrictions
- Kind: constraint
- Statement: Non-administrative users should be restricted from creating security groups, registering applications, or consenting to third-party applications.
- Scope & Conditions: Hardening of tenant-wide directory settings.
- Evidence: "Restrict the ability for non-admin users to create security groups, register applications, create new tenants, or consent to third-party applications."
- Implications:
    - Limits "shadow IT" and sprawl of unmanaged applications.
    - Prevents lateral movement through user-controlled groups or apps.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [directory-hardening, governance, access-control]

### Atom 10: Trusted Launch for Critical Infrastructure
- Kind: mechanism
- Statement: Enabling Trusted Launch (Secure Boot and vTPM) for critical virtual machines like jumpboxes ensures boot-level integrity and protection against rootkits.
- Scope & Conditions: Infrastructure hardening for sensitive access points.
- Evidence: "Enable Trusted Launch (Secure Boot + vTPM) and Azure Backup for the Jumpbox VM."
- Implications:
    - Increases the difficulty for attackers to persist at the firmware/boot level.
    - Required for high-compliance environments.
- Validation: 
    - [x] Single-Idea
    - [x] Boundary
    - [x] Conjunction
    - [x] Reusability
- Confidence: high
- Tags: [infrastructure-security, azure, trusted-launch, integrity]
