---
created: 2026-08-12T14:07:36+00:00
modified: 2026-08-12T15:05:01+00:00
permalink: llmeon/00-inbox/cve-management-best-practices
title: CVE Management Best Practices
type: note
---

## Strategic Management of Non-Exploitable Vulnerabilities: Integrating Trivy, Rego, VEX, and Renovate

### 1\. The Architectural Challenge of Software Supply Chain Security

The rapid adoption of DevSecOps practices has formalized the requirement for continuous, automated security assessments throughout the software development lifecycle. At the center of this transformation are tools like Trivy, a comprehensive Software Composition Analysis (SCA) scanner, and Renovate, a sophisticated dependency update orchestrator. Together, these systems establish a foundational defense against software supply chain attacks. However, as the velocity of software delivery accelerates, engineering and security teams increasingly encounter a systemic friction point: the sheer volume of Common Vulnerabilities and Exposures (CVEs) reported by static analysis tools often vastly exceeds the organization's capacity for remediation.

This friction is exacerbated by the fundamental limitations of standard vulnerability scanning. Third-party components typically constitute between seventy and ninety percent of modern application codebases1. Scanners match the versions of these components against advisory databases like the National Vulnerability Database (NVD) or the GitHub Advisory Database to flag known vulnerabilities. Yet, a scanner merely identifies the presence of a vulnerable package; it cannot inherently determine if the vulnerable function is actually executed by the application at runtime1.

This absence of reachability analysis means that raw CVE counts are not accurate reflections of practical risk1. A critical vulnerability in a cryptography library that is never instantiated by the application presents a negligible threat, but it will still trigger pipeline failures and compliance audits. The resulting phenomenon, often termed "CVE fatigue," forces teams to spend countless hours manually triaging findings that pose no material danger, eroding trust in automated security tooling and masking genuinely critical threats.

The core architectural challenge is establishing a highly automated, machine-readable pipeline that tracks and documents vulnerabilities that will not be fixed, either because no upstream patch is available, or because the vulnerability cannot be exploited in the specific deployment context. Organizations face mounting pressure to solve this problem formally, driven in part by impending regulatory frameworks such as the European Union's Cyber Resilience Act (CRA). The CRA mandates that organizations shipping software must document their components via Software Bills of Materials (SBOMs) and handle vulnerabilities through coordinated disclosure3. To comply without halting development, teams require standardized, auditable mechanisms for defining which vulnerabilities are accepted risks, which are architecturally mitigated, and which are actively being patched.

This report provides an exhaustive analysis of the mechanisms available to manage, suppress, and track vulnerabilities over time. It details the evolution of suppression in Trivy from basic ignore files to advanced Policy-as-Code using Open Policy Agent (OPA) and Rego. It thoroughly examines the Vulnerability Exploitability eXchange (VEX) standard as the definitive solution for cross-platform vulnerability tracking. Finally, it explores advanced Renovate configurations required to orchestrate security updates, manage breaking changes, and automate the remediation lifecycle without destabilizing the codebase.

### 2\. Contextual Vulnerability Suppression in Trivy

Trivy, maintained by Aqua Security, is an industry-standard scanner capable of analyzing container images, filesystems, code repositories, and SBOMs4. While Trivy defaults to a strict version-matching paradigm, its architecture includes multiple tiers of suppression mechanisms designed to handle false positives and accepted risks.

#### 2.1. Baseline Exclusions via the Plaintext Ignore File

The most primitive method for tracking and suppressing unfixed vulnerabilities in Trivy is the.trivyignore file. This is a simple plaintext file placed at the root of a repository that declares a list of finding identifiers, such as CVE IDs, misconfiguration codes, secret rule IDs, or license identifiers, which the scanner must exclude from its final output5.

While highly accessible, this format introduces severe architectural limitations for long-term vulnerability tracking. Primarily, the suppression scope is entirely global. If a team adds a CVE to the.trivyignore file because the vulnerable library is only used in a local test fixture, that CVE is simultaneously suppressed if the same library is inadvertently introduced into the production application code. Furthermore, the file lacks structural metadata; while teams can use standard hash symbols for inline comments to provide human-readable justifications, this context is not parsed by Trivy and cannot be extracted into audit reports6.

To prevent ignored vulnerabilities from becoming permanent blind spots, the plaintext format supports temporal expirations. By appending an expiration date to the identifier (e.g., CVE-2019-14697 exp:2023-01-01), teams can instruct Trivy to automatically re-flag the vulnerability after the specified date6. This feature is a critical best practice for enforcing the periodic reassessment of accepted risks, ensuring that suppressions are continuously audited as threat landscapes evolve.

#### 2.2. Granular Filtering with the YAML Specification

To address the limitations of global suppression, Trivy introduced an experimental, structured YAML format:.trivyignore.yaml. This specification transitions vulnerability tracking from a flat list to a context-aware ruleset, allowing organizations to define the precise conditions under which a CVE should be ignored5.

The YAML format categorizes suppressions into dedicated blocks for vulnerabilities, misconfigurations, secrets, and licenses, applying conditional filters to each rule.

Table\_title: Core Evaluation Fields in the.trivyignore.yaml Specification

| Field | Type | Operational Function |
|:---- |:---- |:---- |
| id | String | The specific identifier of the finding (e.g., a CVE ID). Historically required, but now optional if contextual filters are provided. |
| paths | String Array | Restricts the suppression to specific file paths within the target, enabling environmental isolation. |
| purls | String Array | Restricts the suppression to specific Package URLs (PURLs). This field is exclusively available for vulnerability filtering. |
| statement | String | A documented justification for the suppression, improving auditability for compliance teams. |
| expired\_at | Date | Enforces an expiration timeline for the suppression rule using standard date formatting. |

The integration of the paths and purls fields fundamentally alters how teams can track unexploitable vulnerabilities. For instance, a high-severity path traversal vulnerability in a Python package utilized exclusively by a developer utility script can be suppressed by strictly defining its path within the repository9. If another engineer later imports that exact package version into the main application, the path condition will fail to match, and Trivy will correctly flag the vulnerability9.

Recent architectural enhancements to the.trivyignore.yaml parser have further refined this capability by allowing the id field to be omitted entirely11. In earlier versions, a strict equality match required teams to enumerate every single CVE ID associated with a package. For heavily vulnerable legacy packages like operating system kernel headers that are present in an image but not exercised at runtime, teams were forced to manually maintain lists of hundreds of CVEs11. By permitting the omission of the id field, teams can now create blanket suppressions based solely on a purl or path, drastically reducing maintenance overhead for structurally unexploitable components11.

### 3\. Dynamic Evaluation via Policy-as-Code

While the YAML specification excels at static suppression, it cannot evaluate vulnerabilities dynamically based on their technical attributes. For complex environments where exploitability is determined by architectural constraints, Trivy integrates with the Open Policy Agent (OPA) and its declarative policy language, Rego12.

When executed with the \--ignore-policy flag, Trivy generates its standard JSON output internally and passes this data payload to the Rego engine. Security engineers can write custom logic that traverses this JSON structure, evaluating metadata such as the Common Vulnerability Scoring System (CVSS) vectors, Common Weakness Enumeration (CWE) classifications, or specific vendor severity ratings to dictate whether a finding should be suppressed or escalated5.

#### 3.1. Evaluating CVSS Vectors for Architectural Mitigation

The most robust application of Rego in vulnerability management is the automated filtering of CVEs based on CVSS attack vectors. The CVSS framework categorizes vulnerabilities based on the exact contextual prerequisites required for successful exploitation, such as network access, user interaction, or specific privilege levels15.

Consider a bioinformatics platform executing containerized workloads on a Kubernetes cluster. These containers are deployed strictly to process batch data sets, such as genomic sequencing files. Architecturally, these containers are entirely non-interactive: they expose no inbound network listeners, they do not run in privileged mode, and they do not host user interfaces15.

Under these rigid architectural constraints, any vulnerability that requires both Local Access and User Interaction is structurally impossible to exploit15. For example, a vulnerability requiring an attacker to have local shell access and trick a human user into clicking a malicious link within the container environment cannot materialize15.

A Rego policy can mathematically identify and suppress these specific classes of CVEs across the entire fleet. The CVSS specification evolved from version 3.1 to 4.0, splitting the singular User Interaction metric into Passive and Active interactions, requiring the Rego logic to account for both string formats15. A comprehensive Rego policy for this environment iterates over every vulnerability in Trivy's input structure, verifying the presence of specific CVSS string components. If a vulnerability's CVSS vector contains the string for Local Access alongside the string for User Interaction, the policy evaluates to true, instructing Trivy to ignore the finding15.

By deploying these policies organization-wide, platform engineering teams can massively reduce the volume of unactionable alerts without requiring developers to manually justify each new advisory7.

#### 3.2. Strategic Cautions with Dynamic Filtering

While dynamic filtering via Rego is exceptionally powerful, it carries inherent risks related to the quality of upstream vulnerability data. Filtering broadly by subjective classifications, such as suppressing all vulnerabilities tagged with a specific CWE, is widely considered an anti-pattern.

The National Vulnerability Database (NVD) relies on human analysts to classify vulnerabilities, and misclassifications are frequent15. If a security team writes a Rego policy to suppress all Cross-Site Scripting (CWE-79) vulnerabilities in a non-web container, a critical remote code execution vulnerability erroneously tagged as CWE-79 by the NVD would bypass the scanner entirely5. Therefore, dynamic policies should strictly target highly deterministic architectural mitigations, such as CVSS environmental vectors or explicit severity thresholds, rather than relying on subjective taxonomies14.

### 4\. The Vulnerability Exploitability eXchange (VEX) Standard

The primary deficiency of both.trivyignore.yaml files and Rego policies is their tight coupling to the local Trivy execution environment. If a container image is scanned in a local CI/CD pipeline, the suppressions are applied successfully. However, if that same image is pushed to a registry and subsequently scanned by a different tool—such as Docker Scout, Grype, or Dependency-Track—the local suppressions are absent, and the non-exploitable CVEs immediately reappear16.

To solve this fragmented communication of exploitability, the cybersecurity industry, led by the Cybersecurity and Infrastructure Security Agency (CISA) and the National Telecommunications and Information Administration (NTIA), developed the Vulnerability Exploitability eXchange (VEX) specification20.

#### 4.1. Defining the VEX Specification and OpenVEX

VEX is designed as a machine-readable companion to the SBOM. While an SBOM provides a comprehensive inventory of the components within an application, a VEX document explicitly declares whether the vulnerabilities associated with those components are actually exploitable in the context of the shipped product20.

OpenVEX is a lightweight, JSON-LD implementation of the CISA VEX minimum requirements. It is designed to be highly embeddable and integration-friendly20. An OpenVEX document maps a specific software product, typically identified by a Package URL (PURL), to a specific vulnerability identifier, such as a CVE, and assigns a standardized impact status20.

Table\_title: VEX Impact Status Designations

| Status | Operational Definition | Requirement |
|:---- |:---- |:---- |
| not\_affected | The vulnerability cannot be exploited in this context, and no remediation is required. | Must be accompanied by a formal, machine-readable justification. |
| affected | The vulnerability is exploitable, presenting a material risk to the application. | Often accompanied by an action statement recommending remediation steps. |
| fixed | The vulnerability has been resolved in the declared version of the product. | Serves as an explicit assertion of a patch. |
| under\_investigation | The maintainers are actively assessing the impact; exploitability is currently unknown. | Signals that downstream users should monitor for updates. |

Crucially, when a product is marked as not\_affected, the OpenVEX specification mandates a justification. These justifications are standardized strings, such as inline\_mitigations\_already\_exist, vulnerable\_code\_not\_present, or vulnerable\_code\_not\_in\_execute\_path21. This enforces a rigorous standard for vulnerability suppression, moving organizations away from arbitrary ignores and toward cryptographically verifiable assertions of safety17.

#### 4.2. Integrating VEX with Trivy Scans

Trivy functions as a native consumer of VEX documents, automatically filtering its scan results based on the assertions contained within the VEX payload21. If a VEX document asserts that a specific PURL is not\_affected by a specific CVE, Trivy entirely suppresses that finding from its vulnerability report17.

Trivy supports the consumption of VEX data through three distinct architectural patterns:

First, teams can explicitly pass local VEX files to the scanner using the \--vex flag, instructing Trivy to overlay the VEX assertions onto the current scan target21.

Second, Trivy can dynamically retrieve VEX documents from centralized repositories compliant with the VEX Hub specification. By executing a scan with the \--vex repo flag, Trivy automatically queries remote registries for relevant VEX documents18. This capability allows large enterprises to maintain a single, authoritative VEX repository where security teams publish exploitability assessments, ensuring that all distributed CI/CD pipelines automatically inherit the correct suppressions without duplicating configuration files18.

Third, and most significantly for containerized environments, VEX documents can be cryptographically signed and attached directly to an Open Container Initiative (OCI) image manifest as an attestation17. By scanning with the \--vex oci flag, Trivy automatically discovers the attached VEX document in the remote registry, verifies the cryptographic signature, and applies the suppressions before generating the final report17. This mechanism ensures that the exploitability context travels inextricably with the image itself, allowing any third-party auditor using a compliant scanner, such as Docker Scout, to instantly recognize the suppressions17.

#### 4.3. Creating and Managing VEX Documents

To generate these assertions, organizations utilize specialized command-line utilities such as vexctl, developed by the OpenVEX project22. Security engineers can rapidly generate VEX documents by declaring the product, the vulnerability, the status, and the justification. For example, issuing a vexctl create command with a not\_affected status and an inline\_mitigations\_already\_exist justification immediately produces a valid OpenVEX JSON-LD structure22.

In complex environments, multiple stakeholders may issue VEX assertions regarding the same product over time. An initial assessment may mark a CVE as under\_investigation, while a subsequent assessment marks it as not\_affected. The vexctl merge command is designed to chronologically evaluate these disparate documents, intelligently replaying the status updates in sequence to calculate the final, authoritative impact status22. Finally, the vexctl attest \--attach \--sign command facilitates the secure binding of the VEX document to the OCI image registry, completing the lifecycle from investigation to cryptographic attestation22.

### 5\. Automating Dependency Remediation with Renovate

While Trivy and VEX provide sophisticated mechanisms for tracking and suppressing non-exploitable vulnerabilities, these practices represent reactive mitigation. A proactive security posture dictates that dependencies should be continuously updated to eliminate vulnerabilities at the source, thereby shrinking the overall attack surface regardless of apparent exploitability29.

Renovate, an open-source dependency automation tool maintained by Mend.io, continuously monitors code repositories and package registries, automatically generating Pull Requests (PRs) or Merge Requests (MRs) to update outdated components29. Managing security updates effectively via Renovate requires intricate configuration to balance the necessity of rapid patching against the risk of destabilizing the codebase.

#### 5.1. The Dual Engines of Vulnerability Alerting

Renovate orchestrates security-driven updates through two distinct, and sometimes overlapping, configuration subsystems: vulnerabilityAlerts and osvVulnerabilityAlerts. Understanding the architectural difference between these engines is vital for accurate implementation.

The vulnerabilityAlerts subsystem relies natively on platform-specific infrastructure, most notably the GitHub Dependency Graph and Dependabot alerts31. When a repository is hosted on GitHub, Renovate queries the platform's API to retrieve open security advisories. Upon detecting an active alert, Renovate prioritizes the creation of a targeted PR that updates the specific vulnerable package to the minimum version required to resolve the CVE2.

Conversely, the osvVulnerabilityAlerts subsystem operates independently of the hosting platform. When this feature is enabled, Renovate downloads comprehensive vulnerability data directly from the Open Source Vulnerability (OSV) database31. It then performs offline cross-referencing against the dependencies extracted from the repository33. This subsystem is an absolute necessity for organizations self-hosting Renovate on platforms such as GitLab, Bitbucket, or Azure DevOps, where native Dependabot alerting is either unavailable or entirely unsupported2.

#### 5.2. Resolving Configuration Conflicts in Package Rules

A pervasive challenge in automated dependency management is managing breaking changes introduced by major version updates. Standard engineering practice dictates that minor and patch updates, which generally maintain backward compatibility, should be aggressively auto-merged. Major version updates, which typically contain breaking API changes, require manual testing and intervention35.

Consequently, teams frequently configure Renovate to disable major updates entirely using the packageRules array:

```JSON
{
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "enabled": false
    }
  ]
}
```

However, a structural conflict arises when a severe vulnerability is discovered, and the upstream maintainer only backports the security patch to a new major release branch34. By design, if vulnerability alerting is active, Renovate treats security remediation as paramount. Renovate's internal architecture utilizes a force object for vulnerability alerts, which fundamentally overrides global packageRules configurations34.

As a result, even if major updates are explicitly disabled at the root level, Renovate will aggressively generate a PR for a major version bump if it is deemed the only viable path to resolve a CVE34. This override behavior frequently blindsides engineering teams, causing automated pipeline failures when highly incompatible major versions are unexpectedly proposed for integration34.

To regain control and explicitly block major security updates, organizations must alter their configuration syntax. The suppression rule must be explicitly nested within the vulnerabilityAlerts block to counter the forced override:

```JSON
{
  "vulnerabilityAlerts": {
    "enabled": true,
    "packageRules": [
      {
        "matchUpdateTypes": ["major"],
        "enabled": false
      }
    ]
  }
}
```

Alternatively, rather than blocking major security updates entirely, teams can leverage the additionalBranchPrefix property within the nested packageRules. This technique isolates major security PRs onto distinctly named branches, ensuring they are grouped separately for manual review and do not disrupt the automated integration of minor security patches37.

#### 5.3. Managing Unfixable Dependencies

In scenarios where a dependency is deeply entangled in legacy code and cannot be updated without a total system rewrite, generating continuous security PRs is futile and contributes directly to CVE fatigue. Disabling updates for a specific package requires carefully targeted configuration to overcome the vulnerability alerting engine.

To silence Renovate for a highly vulnerable, unpatchable legacy dependency, the rule must explicitly disable both standard version bumps and security-driven alerts simultaneously:

```JSON
{
  "packageRules": [
    {
      "matchPackageNames": ["legacy-core-lib"],
      "enabled": false,
      "vulnerabilityAlerts": {
        "enabled": false
      }
    }
  ]
}
```

This configuration entirely removes the specified package from Renovate's evaluation loop, permanently silencing the alerts39. Because Renovate is no longer tracking this component, the accepted risk must be documented out-of-band, ideally by generating a VEX document consumed by Trivy to ensure the broader organization remains aware of the suppression context.

### 6\. Mitigating Automation Noise and Supply Chain Risks

Operating Renovate effectively at an enterprise scale requires advanced tuning to mitigate supply chain poisoning and prevent architectural performance bottlenecks.

#### 6.1. Implementing Release Age Cooldowns

The software supply chain has experienced a drastic increase in dependency confusion attacks and malicious package publications31. Attackers routinely publish malicious updates mimicking popular libraries, explicitly targeting automated systems like Renovate for immediate, unverified ingestion. To counter this threat vector, Renovate provides the minimumReleaseAge configuration2.

Setting this value acts as a mandatory cooldown period. For instance, requiring an update to survive in the public registry for a specified duration before Renovate proposes a PR gives the open-source community time to identify and revoke malicious releases39. However, explicitly applying minimumReleaseAge to security updates requires careful risk calculation. Delaying a genuine security patch intentionally leaves the application exposed to known exploits. Organizations must balance the risk of zero-day exploits against the risk of supply chain poisoning. Specialized security presets allow fine-tuning of this behavior, exempting specific types of urgent updates from the delay period40.

#### 6.2. Performance Optimization in Large Monorepos

In massive enterprise monorepos containing thousands of dependency manifest files and potentially thousands of historical, unactionable security alerts, enabling global vulnerability alerting can induce catastrophic performance degradation within the Renovate execution environment41.

Renovate's internal evaluation engine executes deep-cloning operations using the klona library to merge the forced vulnerabilityAlerts rules against every matched package dependency instance41. In repositories with immense dependency graphs, this synchronous cloning sequence starves the Node.js event loop41. This starvation results in cascading failures: network sockets close unexpectedly, GraphQL fetch operations against the hosting platform timeout, and the entire repository run aborts with an ExternalHostError before any PRs can be generated41.

To mitigate this critical bottleneck, platform teams must adopt aggressive noise reduction strategies. This involves rapidly closing non-actionable alerts on the hosting platform to shrink the payload evaluated by Renovate, and heavily utilizing ignorePaths41. By excluding directories that do not deploy to production, such as test/fixtures/\*\* or docs/\*\*, teams drastically reduce the volume of dependency instances Renovate must process, restoring stability to the automation pipeline41.

### 7\. Synthesizing a Unified DevSecOps Workflow

Achieving sustainable vulnerability management requires synthesizing the capabilities of Trivy and Renovate into a cohesive lifecycle. The operational delta between a vulnerable package and an exploitable vulnerability is where organizational security policy is executed.

A mature, unified workflow adheres to the following sequence:

First, Renovate continuously monitors the dependency graph. When a vulnerability is declared in an upstream database, the alerting engine ensures a high-priority PR is opened to resolve it31. If the update passes all continuous integration tests, it is auto-merged, the vulnerability is eliminated, and no manual tracking is required.

Second, if the vulnerability cannot be patched—either because no upstream fix exists, or because the fix requires a breaking architectural change—the security team initiates a reachability analysis. They investigate whether the application invokes the vulnerable function. If the vulnerable module is isolated, or if CVSS vectors indicate exploitation is impossible in the deployed environment, the CVE is categorized as non-exploitable1.

Third, rather than ignoring the alert in Renovate indefinitely or relying on a fragile local.trivyignore file, the security team generates an OpenVEX document using vexctl. The document formally asserts a not\_affected status with a cryptographic justification, and is then signed and attached directly to the OCI image registry18.

Finally, downstream pipeline enforcement is executed by Trivy. During the deployment phase, Trivy scans the image, automatically fetching the VEX attestation via \--vex oci and applying the suppressions18. The remaining vulnerabilities are evaluated against dynamic Rego policies to eliminate any residual architecturally mitigated risks14. If any remaining vulnerability exceeds the organization's maximum risk tolerance, Trivy blocks the deployment9.

By layering these advanced capabilities—utilizing Renovate for relentless automated remediation, deploying Rego policies in Trivy to dynamically eliminate mitigated risks, and adopting the OpenVEX standard to cryptographically suppress non-exploitable findings—organizations transform Software Composition Analysis from a source of overwhelming noise into a highly tuned security perimeter. This strategic synthesis ensures engineering teams focus exclusively on genuine threats, safeguarding the software supply chain without sacrificing delivery velocity.

_This is for informational purposes only. For medical advice or diagnosis, consult a professional._

#### Works Cited

> 1. SCA Tools Comparison 2026: Snyk vs Dependabot vs Renovate \- Rafter, [https://rafter.so/blog/sca-tools-comparison](https://rafter.so/blog/sca-tools-comparison)
> 2. Dependabot vs Renovate (2026): Zero Config vs Full Control | Konvu, [https://konvu.com/compare/dependabot-vs-renovate](https://konvu.com/compare/dependabot-vs-renovate)
> 3. The Fragmented World of Dependency Policy | Andrew Nesbitt, [https://nesbitt.io/2026/03/19/the-fragmented-world-of-dependency-policy.html](https://nesbitt.io/2026/03/19/the-fragmented-world-of-dependency-policy.html)
> 4. How Does My Scanner See HeroDevs? Trivy Edition, [https://www.herodevs.com/blog-posts/how-does-my-scanner-see-herodevs-trivy-edition](https://www.herodevs.com/blog-posts/how-does-my-scanner-see-herodevs-trivy-edition)
> 5. Filtering \- Trivy, [https://trivy.dev/docs/latest/configuration/filtering/](https://trivy.dev/docs/latest/configuration/filtering/)
> 6. Filtering \- Trivy, [https://trivy.dev/docs/latest/guide/configuration/filtering/](https://trivy.dev/docs/latest/guide/configuration/filtering/)
> 7. Ignoring Vulnerabilities for a Period of Time · aquasecurity trivy · Discussion \#2991 \- GitHub, [https://github.com/aquasecurity/trivy/discussions/2991](https://github.com/aquasecurity/trivy/discussions/2991)
> 8. Configuration \- Trivy, [https://trivy.dev/docs/latest/scanner/misconfiguration/config/config/](https://trivy.dev/docs/latest/scanner/misconfiguration/config/config/)
> 9. How to Configure Trivy Severity Filtering \- OneUptime, [https://oneuptime.com/blog/post/2026-01-28-trivy-severity-filtering/view](https://oneuptime.com/blog/post/2026-01-28-trivy-severity-filtering/view)
> 10. trivyignore.yaml not allow to ignore multiple vulnerabilities ids in the same path · aquasecurity trivy · Discussion \#7974 \- GitHub, [https://github.com/aquasecurity/trivy/discussions/7974](https://github.com/aquasecurity/trivy/discussions/7974)
> 11. make id optional in.trivyignore.yaml to ignore all findings for a PURL/path · Issue \#10583 · aquasecurity/trivy \- GitHub, [https://github.com/aquasecurity/trivy/issues/10583](https://github.com/aquasecurity/trivy/issues/10583)
> 12. How to Implement Trivy Rego Policies \- OneUptime, [https://oneuptime.com/blog/post/2026-01-30-trivy-rego-policies/view](https://oneuptime.com/blog/post/2026-01-30-trivy-rego-policies/view)
> 13. How to write custom policies for Trivy \- \_CLOUD, [https://blog.ediri.io/how-to-write-custom-policies-for-trivy](https://blog.ediri.io/how-to-write-custom-policies-for-trivy)
> 14. Enforcing Artifact Security with Trivy and OPA | CNCF, [https://www.cncf.io/blog/2025/05/01/enforcing-artifact-security-with-trivy-and-opa/](https://www.cncf.io/blog/2025/05/01/enforcing-artifact-security-with-trivy-and-opa/)
> 15. viral-ngs/.trivy-ignore-policy.rego at main \- GitHub, [https://github.com/broadinstitute/viral-ngs/blob/main/.trivy-ignore-policy.rego](https://github.com/broadinstitute/viral-ngs/blob/main/.trivy-ignore-policy.rego)
> 16. Container Security 101—Jon Zeolla documentation, [https://jonzeolla.com/labs/container-security-101.html](https://jonzeolla.com/labs/container-security-101.html)
> 17. Docker Scout vs Trivy on DHI \- MrCloudBook, [https://mrcloudbook.com/docker-scout-vs-trivy-on-dhi/](https://mrcloudbook.com/docker-scout-vs-trivy-on-dhi/)
> 18. Scan Docker Hardened Images, [https://docs.docker.com/dhi/how-to/scan/](https://docs.docker.com/dhi/how-to/scan/)
> 19. VEX documents (including OpenVEX) and.trivyignore are ignored during SBOM ingestion and re-analysis · Issue \#4862 · DependencyTrack/dependency-track \- GitHub, [https://github.com/DependencyTrack/dependency-track/issues/4862](https://github.com/DependencyTrack/dependency-track/issues/4862)
> 20. What is OpenVex? \- Chainguard Academy, [https://edu.chainguard.dev/open-source/sbom/what-is-openvex/](https://edu.chainguard.dev/open-source/sbom/what-is-openvex/)
> 21. Reduce CVE noise with OpenVEX assessments in Datadog, [https://www.datadoghq.com/blog/datadog-public-artifact-vulnerabilities-openvex/](https://www.datadoghq.com/blog/datadog-public-artifact-vulnerabilities-openvex/)
> 22. Getting Started with OpenVEX and vexctl \- Chainguard Academy, [https://edu.chainguard.dev/open-source/sbom/getting-started-openvex-vexctl/](https://edu.chainguard.dev/open-source/sbom/getting-started-openvex-vexctl/)
> 23. How to Create Trivy VEX Documents \- OneUptime, [https://oneuptime.com/blog/post/2026-01-30-trivy-vex-documents/view](https://oneuptime.com/blog/post/2026-01-30-trivy-vex-documents/view)
> 24. Trivy ignores my VEX file · aquasecurity trivy · Discussion \#10022 \- GitHub, [https://github.com/aquasecurity/trivy/discussions/10022](https://github.com/aquasecurity/trivy/discussions/10022)
> 25. Local VEX Files \- Trivy, [https://trivy.dev/docs/latest/guide/supply-chain/vex/file/](https://trivy.dev/docs/latest/guide/supply-chain/vex/file/)
> 26. VEX Repository \- Trivy, [https://trivy.dev/docs/latest/supply-chain/vex/repo/](https://trivy.dev/docs/latest/supply-chain/vex/repo/)
> 27. trivy/docs/guide/supply-chain/vex/oci.md at main · aquasecurity/trivy \- GitHub, [https://github.com/aquasecurity/trivy/blob/main/docs/guide/supply-chain/vex/oci.md](https://github.com/aquasecurity/trivy/blob/main/docs/guide/supply-chain/vex/oci.md)
> 28. openvex/vexctl: A tool to create, transform and attest VEX metadata \- GitHub, [https://github.com/openvex/vexctl](https://github.com/openvex/vexctl)
> 29. Renovate–Keeping Your Updates Secure?, [https://blog.compass-security.com/2025/05/renovate-keeping-your-updates-secure/](https://blog.compass-security.com/2025/05/renovate-keeping-your-updates-secure/)
> 30. How do you resolve CVEs in containers efficiently?: r/kubernetes \- Reddit, [https://www.reddit.com/r/kubernetes/comments/1qz172q/how\_do\_you\_resolve\_cves\_in\_containers\_efficiently/](https://www.reddit.com/r/kubernetes/comments/1qz172q/how_do_you_resolve_cves_in_containers_efficiently/)
> 31. Configuration Options \- Renovate Docs, [https://docs.renovatebot.com/configuration-options/](https://docs.renovatebot.com/configuration-options/)
> 32. 12 Tips to Self-host Renovate Bot \- Jerry Ng, [https://jerrynsh.com/12-tips-to-self-host-renovate-bot/](https://jerrynsh.com/12-tips-to-self-host-renovate-bot/)
> 33. Give your feedback about the \`osvVulnerabilityAlerts\` experimental feature · renovatebot renovate · Discussion \#20542 \- GitHub, [https://github.com/renovatebot/renovate/discussions/20542](https://github.com/renovatebot/renovate/discussions/20542)
> 34. false\` and \`packageRules\` cannot block major updates for OSV vulnerability fixes · renovatebot renovate · Discussion \#42760 \- GitHub, [https://github.com/renovatebot/renovate/discussions/42760](https://github.com/renovatebot/renovate/discussions/42760)
> 35. Upgrade best practices \- Renovate Docs, [https://docs.renovatebot.com/upgrade-best-practices/](https://docs.renovatebot.com/upgrade-best-practices/)
> 36. Security vulnerability updates creating major version PRs despite matchUpdateTypes: \["major"\] with enabled: false · renovatebot renovate · Discussion \#40134 \- GitHub, [https://github.com/renovatebot/renovate/discussions/40134](https://github.com/renovatebot/renovate/discussions/40134)
> 37. Config to include Security / Vulnerability in grouping. · renovatebot renovate · Discussion \#15107 \- GitHub, [https://github.com/renovatebot/renovate/discussions/15107](https://github.com/renovatebot/renovate/discussions/15107)
> 38. Major updates being pushed in cases where we are not expecting them · renovatebot renovate · Discussion \#34919 \- GitHub, [https://github.com/renovatebot/renovate/discussions/34919](https://github.com/renovatebot/renovate/discussions/34919)
> 39. osvVulnerabilityAlerts not respecting "enabled": false within a packageRule · renovatebot renovate · Discussion \#40800 \- GitHub, [https://github.com/renovatebot/renovate/discussions/40800](https://github.com/renovatebot/renovate/discussions/40800)
> 40. Security Presets \- Renovate Docs, [https://docs.renovatebot.com/presets-security/](https://docs.renovatebot.com/presets-security/)
> 41. perf(package-rules): avoid re-cloning invariant packageRules array on every rule match in applyPackageRules · Issue \#44459 · renovatebot/renovate \- GitHub, [https://github.com/renovatebot/renovate/issues/44459](https://github.com/renovatebot/renovate/issues/44459)
> 42. renovate.json · main \- shepard \- GitLab, [https://gitlab.com/dlr-shepard/shepard/-/blob/main/renovate.json?ref\_type=heads](https://gitlab.com/dlr-shepard/shepard/-/blob/main/renovate.json?ref_type=heads)
