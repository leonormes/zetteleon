# Cracking the Vault: how we found zero-day flaws in authentication, identity, and authorization in HashiCorp Vault

![rw-book-cover](https://cyata.ai/wp-content/uploads/2025/08/cracking-the-vault.webp)

## Metadata
- Author: [[Admin]]
- Full Title: Cracking the Vault: how we found zero-day flaws in authentication, identity, and authorization in HashiCorp Vault
- Category: #articles
- Summary: Researchers found serious logic flaws in HashiCorp Vault’s authentication and policy systems that let attackers bypass security measures like lockouts and multi-factor authentication. These bugs allow attackers to impersonate users, escalate privileges to root, and run code on Vault servers without detection. The findings show how small errors in Vault’s core can lead to total system compromise and highlight risks in real-world deployments.
- URL: https://share.google/jZDcD13hWejZJB8Gj

## Full Document
Secrets vaults are the backbone of digital infrastructure. They store the credentials, tokens, and certificates that govern access to systems, services, APIs, and data. They’re not just a part of the trust model, they *are* the trust model. In other words, if your vault is compromised, your infrastructure is already lost.

Driven by the understanding that vaults are high-value targets for attackers, our research team at Cyata set out to conduct a comprehensive assessment of HashiCorp Vault (“Vault”), one of the most widely used tools in this space.

Over several weeks of deep investigation, we identified **nine previously unknown zero-day vulnerabilities**, **each assigned a CVE** through responsible disclosure. We worked closely with HashiCorp to ensure all issues were patched prior to public release.

The flaws we uncovered bypass lockouts, evade policy checks, and enable impersonation. One vulnerability even allows root-level privilege escalation, and another – perhaps most concerning – leads to the first public **remote code execution (RCE)** reported in Vault, enabling an attacker to execute a full-blown system takeover.

We found a pattern of logic failures that, individually and in combination, create dangerous attack paths – especially in real-world Vault deployments where misconfigurations or excessive permissions are common.

These vulnerabilities weren’t memory corruption or race condition issues, but subtle logic flaws buried in Vault’s authentication, identity, and policy enforcement layers. Some had existed for nearly a decade, quietly embedded and easy to miss, yet straightforward to exploit once understood.

Previous public research on Vault risks, most notably Google Project Zero’s [Enter the Vault](https://googleprojectzero.blogspot.com/2020/10/enter-the-vault-auth-issues-hashicorp-vault.html) (2020), focused on bypasses in cloud-provider-specific IAM backends like AWS and GCP. Our work targets Vault’s **core authentication flows**, surfacing issues that impact both Open Source and Enterprise versions, across multiple solution providers.

In this post, we share what we found, how we found it, and what it means for the infrastructure Vault is meant to protect.

In parallel, we conducted a similar assessment of **CyberArk Conjur**, uncovering several high-severity vulnerabilities – composing a pre-auth remote code authentication chain. Those findings are detailed [in a separate post on Conjur](https://cyata.ai/blog/exploiting-a-full-chain-of-trust-flaws-how-we-went-from-unauthenticated-to-arbitrary-remote-code-execution-rce-in-cyberark-conjur/).

HashiCorp Vault is an open-source tool designed to secure, store, and control access to secrets, including API keys, database passwords, certificates, and encryption keys.

Used across organizations of all sizes, Vault centralizes secret management and enforces fine-grained access policies across distributed systems.

At its core, it acts as a security boundary: authenticating users and machines and brokering access to sensitive data.

Vault plays a critical role in modern DevSecOps pipelines, helping teams reduce the risks of hardcoded credentials, secret sprawl, and unauthorized access.

Users frequently highlight its integration flexibility, detailed policy enforcement, and suitability for complex, distributed environments.

In many environments, it’s trusted as the final gatekeeper of secrets and, depending on its configuration, a breach of Vault can mean a breach of **everything**.

![](https://cyata.ai/wp-content/uploads/2025/08/Group-2147203144.webp)
Vault highlights

* Secrets management and cryptographic engine designed for dynamic, multi-cloud and hybrid environments
* Centralized secrets storage with access via API
* Dynamic credential provisioning with automatic expiration
* Identity-based access controls supporting human and machine authentication
* Encryption as a service for data at rest and in transit
* Certificate management for generating, rotating, and revoking certificates
* Distribution, enabling, disabling, and rotating encryption keys

This research was the result of a deliberate, weeks-long effort by our research team to uncover logic-level vulnerabilities in Vault – the kind that don’t show up in memory scanners or crash logs, but that can quietly undermine a system’s trust model.

We didn’t stumble into these issues. We sought them out, starting with a clear hypothesis – if Vault plays the role of trust anchor for organizations, then even minor inconsistencies in how it enforces identity, authentication, or policy could have outsized consequences.

We focused on Vault’s core request flow, especially the `request_handling.go` file which functions as the “brain” of Vault. This is where requests are routed, identities resolved, and policy decisions made. We spent weeks reviewing the logic across functions and modules, looking for edge cases where trust boundaries might blur.

We didn’t rely on fuzzers or automated probes. Instead, we conducted a deep manual review of the source code – looking not just at what each function did, but how different components interpreted identity and input. Where we saw inconsistencies in casing, aliasing, or formatting, we dug deeper.

These weren’t random guesses, each test input was a precision-guided hypothesis shaped by the code itself. We also approached the system like an attacker: starting with minimal access and asking, *“How far can we push from here?”*

We repeated that process again and again.

This recurring loop – spotting subtle inconsistencies, reasoning through their downstream impact, and validating them with controlled testing – led us to each of the nine vulnerabilities disclosed in this report.

Ultimately, we didn’t just look for vulnerabilities. We looked at how trust itself could break and followed the logic wherever it led.

HashiCorp Vault supports a wide range of authentication methods, 14 by default. To kick off our research, we began with the simplest and most widely used – `userpass`, Vault’s native username-and-password login mechanism.

To enable `userpass`, users configure it through the Vault UI or API as one of the available authentication methods.

![](https://cyata.ai/wp-content/uploads/2025/08/hashicorp-1.webp)
In a typical `userpass` setup, each user is assigned a hashed password and one or more Vault policies. On login, Vault verifies the credentials and applies the appropriate policy upon success.

Given how foundational `userpass` is to Vault and how widely it’s deployed across production environments, we were surprised to discover logic flaws in this core component. Even here, at the default entry point to the system, the trust model could be broken.

![](https://cyata.ai/wp-content/uploads/2025/08/userpass-login.webp)
**What we looked for**

We began by reviewing how Vault enforces lockout protections under `userpass` – specifically, how failed login attempts are tracked, throttled, and attributed to individual users.

**What we found**

Our first stop was Vault’s userpass backend. We wanted to understand not only how it works – but also how it could be manipulated into misbehaving.

Our investigation focused on Vault’s **lockout protection** logic, the mechanism that’s supposed to throttle brute-force attempts. We discovered three vulnerabilities, all related to how Vault tracks and handles failed login attempts:

* **CVE-2025-6010 – Redacted (Pending Fix)**This CVE has been temporarily withheld from publication at the request of the vendor. No technical details will be shared at this time.
* **CVE-2025-6004 – Lockout bypass via case permutation**
* **CVE-2025-6011 – Timing-based enumeration**  
When Vault authenticates a real user, it performs a bcrypt hash comparison. For nonexistent users, that step is unintentionally skipped due to an early return. This leads to a detectable timing difference, allowing attackers to infer which usernames are valid.

**Why it matters**

These flaws allow an attacker to:

In short, Vault’s simplest authentication path – the first line of defense – contained logic bugs that could be exploited to undermine access controls before any policies were ever enforced.

Step 2 – LDAP logic flaws and MFA enforcement bypass

After uncovering multiple vulnerabilities in `userpass`, we turned our attention to another backend that shares the same lockout mechanism: `ldap`. It’s one of Vault’s most widely used authentication methods in production environments, often integrated with directory services like Active Directory or OpenLDAP. And like `userpass`, it enforces a lockout threshold by default, which made it a compelling next target for investigation.

To enable the `ldap` backend, it must be configured through the Vault UI or API:

![](https://cyata.ai/wp-content/uploads/2025/08/hashicorp-2.webp)
Unlike `userpass`, where Vault verifies credentials internally, the `ldap` method delegates authentication to an external server. Vault simply forwards the provided credentials, and the LDAP server performs the verification.

The full authentication flow looks like this:

![](https://cyata.ai/wp-content/uploads/2025/08/ldap-login-flow-new.webp)
**What we looked for**

After discovering username enumeration issues in `userpass`, we turned our attention to the `ldap` backend – specifically, how it handles lockout behavior for unknown users.

Unlike `userpass`, `ldap` applies lockout uniformly to all failed login attempts, regardless of whether the username exists. This consistent treatment prevents the kind of enumeration attacks seen in `userpass`.

But despite this uniformity, we uncovered **two high-impact logic flaws**.

**What we found**

We found two critical flaws that weakened lockout enforcement and bypassed MFA controls under specific configuration conditions.

**CVE-2025-6004 – Lockout bypass via input normalization mismatch**

This vulnerability stems from how Vault and the LDAP server handle input formatting differently. Vault tracks lockouts by the exact input string, but most LDAP servers normalize input, ignoring case and trimming spaces.

So, these inputs:

These are all interpreted by LDAP as the same user, but treated by Vault as different aliases.

That discrepancy results in an astronomical number of login attempts that bypass the intended lockout limits. For example:

**Impact:**

An attacker can make **billions of password guesses** against the same account in a single lockout window – completely defeating the brute-force protection mechanism

**CVE-2025-6003 – MFA enforcement bypass via** `username_as_alias` **and** `EntityID`  

The second flaw was even more subtle and potentially more dangerous.

Vault allows admins to set `username_as_alias=true` in the `ldap` configuration. This means the username itself is used as the basis for identity resolution.

But when MFA enforcement is applied at the `EntityID` or `IdentityGroup` level, a mismatch occurs between how Vault resolves the user and how it enforces MFA.

Even though the user logs in successfully, Vault may fail to associate the correct `EntityID` and therefore, MFA never gets triggered.

For this bypass to occur, two conditions must be met:

1. `username_as_alias=true` in the LDAP auth configuration
2. MFA enforcement is applied at the `EntityID`or `IdentityGroup` level
3. This issue only became apparent after a deep analysis of how Vault handles `EntityID`resolution in tandem with authentication workflows, but the result is easily exploitable in practice, including via the UI.

**Impact:**

When MFA is enforced at the `EntityID` level, Vault may fail to associate the correct `EntityID`, allowing the login to proceed without triggering MFA.

CVE-2025-6003 MFA enforcement bypass:

**Why it matters**

These two vulnerabilities allow an attacker to:

* **Bypass Vault’s lockout mechanism**, enabling a high volume of password guesses per account
* **Silently bypass MFA enforcement** in specific configurations where MFA is applied at the `EntityID` or `IdentityGroup` level and `username_as_alias=true` is set

Both flaws directly undermine core security protections in enterprise Vault deployments and highlight how subtle logic mismatches can erode trust at the identity layer.

`userpass` and `ldap` are widely used authentication backends in Vault, but they’re rarely deployed on their own. In most real-world setups, multi-factor authentication (MFA) is also configured. That’s why it was clear to us that any analysis of the authentication surface would be incomplete without examining it.

The MFA method we investigated is TOTP (Time-based One-Time Password), the most common MFA method overall, and especially common alongside `userpass` and `ldap`.

This approach adds a rotating numeric code on top of static credentials, aiming to stop brute-force and replay attacks with minimal overhead.

**TOTP in Vault**

Vault’s built-in TOTP MFA relies on a per-entity shared secret. During authentication, it generates a 6-digit code (valid for a 30-second window by default) and compares it to the user’s input.

By taking a look under the hood, we saw that:

**Vault’s TOTP flow**

1. Login begins

2. Vault checks for TOTP MFA

3. A passcode is extracted:

4. Vault checks if the passcode was already used (replay detection):

5. Rate-limiting is enforced per `EntityID`:

```
rateLimitID := fmt.Sprintf("%s_%s", configID, entityID)

numAttempts, _ := usedCodes.Get(rateLimitID)
if numAttempts == nil {
    usedCodes.Set(rateLimitID, uint32(1), passcodeTTL)
} else {
    num, ok := numAttempts.(uint32)
    if !ok {
        return fmt.Errorf("invalid counter type returned in TOTP usedCode cache")
    }
    if num == maximumValidationAttempts {
        return fmt.Errorf("maximum TOTP validation attempts %d exceeded the allowed attempts %d.", num, maximumValidationAttempts)
    }
    err := usedCodes.Increment(rateLimitID, 1)
    if err != nil {
        return fmt.Errorf("failed to increment the TOTP code counter")
    }
}
```

6. Code validation occurs using the `ValidateCustom()` function:

```
key, err := c.fetchTOTPKey(ctx, configID, entityID)
if err != nil {
    return errwrap.Wrapf("error fetching TOTP key: {{err}}", err)
}

if key == "" {
    return fmt.Errorf("empty key for entity's TOTP secret")
}

valid, err := totplib.ValidateCustom(passcode, key, time.Now(), validateOpts)
```

7. If the code is valid, it is marked as used:

8. Authentication completes

![](https://cyata.ai/wp-content/uploads/2025/08/totop-image.webp)
**What we looked for**

We dug into Vault’s TOTP implementation, looking for logic flaws that could significantly weaken this layer of protection, whether individually or when combined.

**What we found**

We uncovered **three major logic flaws**, plus a CVE that captures their combined impact:

**Bug 1 – Used passcode enumeration**

Vault checks for code reuse before applying rate-limiting. This opens a subtle but powerful attack surface.

If an attacker submits a passcode that was recently used, Vault responds with a specific error:

This behavior reveals information. Even if a code is expired, Vault confirms it was valid at some point, enabling enumeration of previously used passcodes.

**Bug 2 – One-time-use bypass via space padding**

This issue originates deep inside Vault’s TOTP validation stack. Specifically:

So `"123456"` and `" 123456"` are treated as equivalent by the validator.

But Vault’s internal `usedCodes` cache does not normalize the input. This means:

**Impact:**

An attacker can **bypass the one-time-use restriction** simply by adding spaces.

**Bug 3.1 – Rate-limiting evasion via time skew**

Even if an attacker has a valid TOTP code using Bug 1, Vault may still reject it because the enumeration attempts required to discover that code may have already triggered per-entity rate-limiting within the TOTP validity window. But this protection can be bypassed if the attacker understands how Vault sets its TTL threshold:

This default is **30 seconds**, matching the default TOTP period. But due to skew, passcodes may remain valid for **up to 60 seconds**, spanning two time windows.

**Bug 3.2 – Rate-limiting bypass via entity switching**

Vault enforces rate limits **per** `EntityID`, but the `usedCodes` cache is **global**. This creates a loophole:

Even worse, **CVE-2025-6013**, which we discovered and described above, allows LDAP users to generate multiple `EntityIDs` for the same identity. So even if Vault enforced rate limits per `EntityID` (which it doesn’t), attackers could still rotate `EntityIDs` to keep attacking.

All these flaws combine into a dangerous scenario.

Despite TOTP being configured as a second factor, Vault’s logic flaws allowed attackers to **brute-force MFA codes** within a small time window.

**Why it matters**

These flaws significantly reduced the effectiveness of MFA in Vault, enabling attackers to bypass protections like rate-limiting and one-time-use enforcement, and in some configurations, guess valid TOTP codes without triggering MFA challenges as expected.

In Vault, TLS certificate authentication is commonly used for machine-to-machine scenarios, allowing automated services, infrastructure components, or nodes to securely identify themselves.

To enable cert-based authentication, users configure it through the Vault UI or API:

![](https://cyata.ai/wp-content/uploads/2025/08/hashicorp-3.webp)
Once enabled, Vault’s `cert` method supports two modes:

In both cases, Vault maps the TLS client certificate to an `EntityID` using the authentication mount path and the Common Name (CN) from the certificate.

(auth mount path, alias.Name)

The value of `alias.Name` is taken from the Common Name (CN) field of the client certificate presented during the TLS handshake, not from the certificate configured in Vault:

In CA mode, this behavior makes sense – CNs vary and can’t be predicted in advance. But in non-CA mode, this introduces a dangerous blind spot.

**What we looked for**

We examined how Vault maps identities in cert-based authentication, particularly in non-CA mode, to identify potential mismatches between trust and identity resolution.

**What we found**

We discovered a logic flaw in Vault’s non-CA certificate authentication: Vault verifies only that the TLS client certificate’s public key matches the pinned certificate, but does not verify that the CN matches as well.

**CVE-2025-6037 – Certificate entity impersonation**

* Present a certificate with the correct public key
* Modify the CN in the client certificate to any arbitrary value
* Cause Vault to assign the resulting `alias.Name` to that CN

Because Vault maps this alias to an `EntityID`, the attacker is now authenticated as any identity whose alias matches the forged CN.

This allows impersonation of other machine identities, inheriting:

Even though policies directly tied to a specific certificate remain inaccessible, in many deployments, `EntityID` – linked policies may be sufficient to escalate access or retrieve secrets.

**Why it matters**

Vault’s trust model depends on accurate identity mapping. This vulnerability breaks that assumption by allowing any private-key holder of a pinned cert to impersonate other machine identities, a severe breach of trust.

In environments where certificates govern automated secret retrieval, service orchestration, or backend access control, this opens the door to full lateral compromise.

So far, we’ve focused on breaking Vault’s authentication surface, through `userpass`, `LDAP`, `MFA`, and `cert`.

Now we turn to what happens after authentication: what can a legitimate user do? In this section, we show how an admin-level user can escalate privileges and obtain a root token, despite the boundaries the Vault trust model is designed to enforce.

The Vault trust model is one that relies on strict role separation. Even users with admin-level tokens are restricted from performing certain privileged actions. But that boundary can break.

**How it works**

Vault uses a policy-based authorization system. Each identity or token is granted permissions through attached policies.

Two built-in policies define access boundaries:

To prevent misuse, Vault includes a hardcoded restriction to block assignment of the `root` policy. This protection applies at all expected enforcement points, including:

To assign policies to an identity, Vault provides the following endpoint:

`POST /v1/identity/entity/id/{entity_id}`

This endpoint allows modification of the attached policy set for a given `EntityID`. It’s powerful and typically reserved for high-privilege users.

This hardcoded check explicitly blocks requests that attempt to assign the `root` policy, or so it seems.

**What we looked for**

With initial access achieved, we turned our attention to potential escalation paths, particularly whether admin users could gain root.

We uncovered a **logic flaw** in how Vault normalizes policy names, one that lets an attacker escalate from **admin to root** by bypassing its most explicitly protected gate.

**What we found**

**CVE-2025-5999 – Root privilege escalation via policy normalization**

Inside `SanitizePolicies`, this logic appears:

This introduces a subtle but powerful mismatch:

Because these variations aren’t blocked by the validation check, they pass through and are then normalized to ‘root’ during enforcement.

So, if an attacker submits a request assigning `" root"` as a policy, it silently passes the block and becomes `root` in practice.

Vault will now treat the token as having full administrative privileges.

**Why it matters**

This logic flaw allows an attacker with admin-level access to:

This bypass targets one of the **most tightly protected controls in Vault** and succeeds without crashing the service, triggering alarms, or touching memory. It’s a clean, silent privilege escalation.

In the previous step, we demonstrated how an admin-level user can escalate to root token privileges.

From there, the next logical step was to investigate whether that level of access could be used to achieve code execution, specifically, to abuse Vault’s internal interfaces in order to run arbitrary commands on the server.

**What we looked for**

**What we found**

Vault supports loading custom plugins – binaries that provide secret engines, auth methods, or other extensible functionality. These plugins are stored in a predefined `plugin_directory`, which is configured during setup and cannot be modified at runtime.

During our testing, we discovered a method for creating and loading an attacker-controlled plugin.

**CVE-2025-6000 – RCE via plugin catalog abuse**

**Step 1 – Writing a payload to disk**

Even when storing data through the API, the resulting file is encoded and wrapped in structured formats.

There’s no way to get raw bytes written directly to disk . . . except in one place:

**Audit logs.**

Audit logs are written in plaintext, not encrypted. And while each entry is a structured JSON object, we discovered something surprising:

**Vault’s audit log system supports a “prefix” – a string prepended to every log entry.**

We set the prefix to a payload like `#!/bin/bash\n...` and let Vault write the rest. The JSON body that follows is ignored by Bash. All that matters is that the script starts with a valid shebang and executable code.

**Step 2 – Locating the** `plugin_directory`

The `plugin_directory` configuration is used only for loading plugins. So, to locate it, our best bet was to examine the plugin loading endpoint:

`POST /v1/sys/plugins/catalog/:type/:name.`

We experimented with it to understand how plugin loading works and what the code flow looks like. During testing, we found that when attempting to load a non-existent binary, the endpoint returns an error message, and that message includes the full path to the `plugin_directory`.

For example, when we tried to load the binary `invalid91cad96-b8e6-4f5b-9359-ad20fe5815c4`, we got:

**Step 3 – Writing to the plugin directory**

Now that we had the `plugin_directory` we wanted to write our audit file to there.

Fortunately, Vault allows configuring the audit backend to write logs to any absolute file path.

**Step 4 – Getting execute permissions**

Vault doesn’t load just any file as a binary. The file must have execute permissions in order to be loaded as a plugin.

This turned out to be the most unexpected and critical part. When configuring the audit log file, there is an option to set the file’s mode. and this includes support for executable modes.

So we set:

**Note:** Using the audit logs, we can create a file with arbitrary contents matching a regex, write it to any absolute `file_path`, and assign it executable permissions.

**Step 5 – Capturing the hash**

In the registration phase, a SHA256 of the binary must be provided. This might sound simple, but for our audit log approach, it presents a challenge: audit logs include timestamps and other unpredictable values, making it impossible to precompute the hash.

To solve this, we configured multiple audit backends simultaneously.

We added a second backend that streamed logs to a TCP socket we controlled. This gave us a real-time copy of the exact file content, allowing us to compute the correct SHA256 after the file was written.

**Full exploit flow**

Default -> RCE (CVE-2025-6037, CVE-2025-5999, CVE-2025-6000):

**Why it matters**

This vulnerability chains together multiple trusted Vault components – audit logging, file permissions, plugin registration, to break critical security boundaries.

translates into a full remote code execution with no memory corruption or native code injection.

CVE-2025-6000 is **the first public RCE reported in Vault**, even though the underlying risk had been present for nearly a decade.

**Post-exploitation scenarios**

With RCE in Vault, an attacker gains complete control, but what they do next depends on their intent. We highlight two realistic post-exploitation strategies observed during testing.

**Vault ransomware**

Vault stores all critical state – including secrets, tokens, and policies, encrypted on disk. One of the key components required for decryption is the file:

If this file is deleted, Vault permanently loses access to its encryption key, rendering the remaining data unreadable – even to administrators.

By removing a single file, an attacker can flip Vault’s encryption model on its head, turning it from a security mechanism into a ransomware vector.

**Stealthy path: audit-free persistence**

In Vault Enterprise, the **Control Group** feature is designed to enforce multi-approver workflows for sensitive operations. But with RCE, this mechanism can be subverted for stealth.

By writing custom control group files directly to disk, an attacker can abuse the system to send HTTP requests and receive responses without being audited. This results in persistent, low-visibility access that bypasses oversight.

This abuse was discovered through black-box testing, as Control Group is exclusive to Vault Enterprise and not openly documented.

This research exposes critical weak points in Vault’s trust and identity model – flaws that, under real-world conditions, form exploitable attack paths and can drive devastating results.

Below are three realistic attack paths, based on common authentication methods:

1. `userpass` attack path (high-effort, persistent attacker)

* Enumerate valid usernames via error message mismatch
* Bypass lockout using case variation
* Bypass TOTP MFA rate limits and one-time-use protection
* *(If the compromised user has admin privileges)* → escalate to `root` via policy normalization
* Achieve RCE via audit log and plugin abuse

2. `ldap` attack path (config-dependent)

This scenario depends on specific but common configuration choices

3. `cert` attack path (targeted impersonation)

* Impersonate an admin-level user by modifying CN in a certificate with a trusted public key
* *(If the impersonated identity has entity-based policies)* → gain admin access
* Escalate to `root`
* Trigger RCE through audit logging chain

This path requires access to the private key of a pinned certificate and benefits from permissive policy binding.

Each of these paths leverages distinct logic flaws in Vault, but all converge at the same critical outcome: **root access and full code execution inside the Vault server**.

**Why this matters**

This research shows how authentication, policy enforcement, and plugin execution can all be subverted through logic bugs, without touching memory, triggering crashes, or breaking cryptography.

**These logic vulnerabilities – one of which would qualify as CVSS ‘critical’ – could be weaponized to exfiltrate secrets, disable access controls, or sabotage infrastructure from within.**

**It’s a reminder that even without memory safety bugs, logic flaws can open the door to complete compromise.**

As part of our research, we analyzed the history of key vulnerabilities in Vault to understand how long they had existed before our discovery. Two cases stood out:

*CVE-2025-6037 – Certificate impersonation*

This vulnerability existed in Vault for over **eight years**. For the first seven years, it was effectively a **full authentication bypass via certificate**, not just impersonation, making it far more severe.

This vulnerability has existed in Vault for **nine years**, dating back to the project’s early releases.

This is also the **first public RCE ever reported in Vault**. While there have been issues in adjacent areas before, none previously enabled full command execution on the Vault server.

At Cyata, we followed a strict responsible disclosure process throughout this research. Every vulnerability was privately reported to HashiCorp with clear documentation, technical detail, and proof-of-concept support.

We worked in close coordination with HashiCorp’s security team to ensure that all issues were understood, addressed, and resolved before any public disclosure – minimizing risk to users and ensuring timely protection.

HashiCorp responded professionally at every stage of the process, engaging constructively and collaborating with us until all findings were fully resolved.

* **May 18, 2025** – Cyata submitted the initial disclosure to the HashiCorp security team, covering the majority of the findings. Some issues were still under active investigation.
* **May 23, 2025** – We followed up with the complete list of confirmed vulnerabilities.
* **May 24, 2025** – HashiCorp responded with additional questions, primarily focused on the certificate impersonation issue.
* **May 24 (Evening)** – Cyata sent a detailed technical explanation clarifying the impersonation path.
* **May 25, 2025** – We shared a full proof-of-concept video demonstrating the certificate impersonation attack in action.
* **June 12, 2025** – HashiCorp acknowledged and accepted all findings, assigning **nine CVEs** across the reported issues.

*Coordinated patching and resolution*

HashiCorp moved quickly to develop and release patches for both the Open Source and Enterprise versions of Vault. These fixes were made available to users ahead of public disclosure, ensuring organizations could protect their environments immediately.

Further information from the vendor is available in [this HashiCorp advisory](https://discuss.hashicorp.com/t/hcsec-2025-22-multiple-vulnerabilities-impacting-hashicorp-vault-and-vault-enterprise/76096).

At Cyata, we believe meaningful research doesn’t stop at discovery. It must include responsible coordination, resolution, and ultimately, protection for the infrastructure the world depends on.

This research reinforces a critical truth – even memory-safe software can fail at the logic level – and when it does, the consequences can be just as severe.

Vault is designed to be the ultimate protector of secrets and infrastructure access. But this work shows how subtle logic bugs in authentication flows, identity resolution, and policy enforcement, can quietly break trust.

And when trust in the vault is broken, the impact is immediate and devastating: attackers can impersonate users, bypass MFA, extract credentials, seize root tokens, and even execute arbitrary commands. With control over Vault, they can hijack internal services, pivot across environments, and hold entire systems hostage, all without triggering conventional alarms.

One of our key takeaways is that vaults must be tested not only against brute-force and interface abuse, but against deep behavioral inconsistencies – edge cases that only emerge when you understand how the system is wired together internally.

Cyata’s research team uncovered these vulnerabilities through manual review, attacker-style reasoning, and persistence. This wasn’t automation. It was a methodical, step-by-step process, reasoning through Vault’s design and asking: where can things go wrong?

The issues uncovered in this research are exceptionally severe, capable of quietly compromising the core layer that organizations rely on to protect everything else.

We believe that research like this is essential – not only to harden individual products, but to help the security community stay one step ahead of attackers.
