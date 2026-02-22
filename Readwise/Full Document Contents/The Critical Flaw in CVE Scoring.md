# The Critical Flaw in CVE Scoring

![rw-book-cover](https://eu-images.contentstack.com/v3/assets/blt6d90778a997de1cd/blt1c6763c3f72205a3/6894a9f83fe247f1f805fa1b/CVE_(1800)_Borka_Kiss_Alamy.jpg?disable=upscale&width=1200&height=630&fit=crop)

## Metadata
- Author: [[Ofri Ouzan]]
- Full Title: The Critical Flaw in CVE Scoring
- Category: #articles
- Summary: Many reported software vulnerabilities are rated "critical" but are not truly urgent in real-world use. This causes security teams to waste time on low-risk issues and leads to burnout. Organizations need to consider context when prioritizing threats to focus on what really matters.
- URL: https://share.google/Y400wvM8eLboCatGp

## Full Document
![The letters CVE in white on a black band over a purple background that kind of looks like a circuit board](https://eu-images.contentstack.com/v3/assets/blt6d90778a997de1cd/blt1c6763c3f72205a3/6894a9f83fe247f1f805fa1b/CVE_(1800)_Borka_Kiss_Alamy.jpg?width=1280&auto=webp&quality=80&format=jpg&disable=upscale)Source: Borka Kiss via Alamy Stock Photo
COMMENTARY

Today's software supply chain is under relentless pressure, as new vulnerabilities emerge at a record pace. [In 2024 alone](https://www.businesswire.com/news/home/20250401200753/en/JFrog-Enables-Trusted-AI---Uncovers-Critical-Security-Threats-Emerging-from-AIs-Expansion-in-the-Software-Supply-Chain), more than 33,000 new Common Vulnerabilities and Exposures (CVEs) were reported. This sheer [volume of threats has left security teams and developers stretched thin](https://www.darkreading.com/threat-intelligence/cve-disruption-threatens-foundations-defensive-security) as they're forced to triage which threats require immediate action, all while juggling their core responsibilities.

While many of these vulnerabilities may seem critical on paper, taking a closer look often reveals a different story. In fact, recent research found that only [12%](https://www.businesswire.com/news/home/20250401200753/en/JFrog-Enables-Trusted-AI---Uncovers-Critical-Security-Threats-Emerging-from-AIs-Expansion-in-the-Software-Supply-Chain) of these CVEs deemed "critical" by government organizations truly warranted such a severity rating.

This disconnect highlights a growing challenge for the cybersecurity industry: Although established CVE scoring systems like [MITRE](https://jfrog.com/blog/mitres-close-call-in-cve-management/) offer a useful baseline, they often fail to account for the unique context of each organization's environment. As a result, teams risk focusing on theoretical risks while genuine threats may be overlooked.

Take, for example, CVE-2024-45490 — a vulnerability in a widely used software tool that received a [9.8 CVSS score](https://nvd.nist.gov/vuln/detail/cve-2024-45490). Although it received a "Critical" rating, further analysis and context revealed it is only applicable in 10% of real-world applications. Exploiting this flaw would require a very specific and unlikely set of conditions for developers, making real-world exploitation extremely improbable.

To bring greater clarity to teams evaluating CVEs, security leaders should establish a checks and balances system of evaluating these threats with the necessary contextual analysis. This approach can help teams cut through the noise of low-risk vulnerabilities and ensure resources are directed toward their most pressing security problems.

#### Not All CVE Ratings Are What They Seem

A [recent analysis](https://s201.q4cdn.com/814780939/files/doc_presentations/2025/Apr/01/JFrog-Software-Supply-Chain-Report-2025.pdf) of 140 high-profile CVEs that were published in 2024, revealed that 88% of "Critical" and 57% of "High" CVE scores were not as severe as the CVSS scoring would have you believe. In fact, only 27 CVEs (15%) were found to be truly highly exploitable.

This highlights the importance of assessing the real-world context of CVEs. Without this information, misclassification can lead to alert fatigue, drain productivity and morale, and increase the risk of human error, which can cause more harm than the vulnerabilities themselves.

By factoring in aspects of the CVE like exploitability in their specific environment, exposure levels, and business impact, teams can make more informed decisions about which vulnerabilities demand immediate attention.

#### The Impact on Developers and Security Teams

The constant flood of security warnings and CVE disclosures makes it increasingly difficult to [distinguish real threats from less urgent issues](https://www.darkreading.com/vulnerabilities-threats/why-cves-are-an-incentives-problem). Over time, this overwhelming volume of alerts can erode focus, leading to burnout, slower response times, and a greater likelihood of dangerous mistakes. As threat actors grow more sophisticated, the risk of critical issues slipping through the cracks only intensifies.

A major contributor to this fatigue is the prevalence of false positives. When security tools flag safe code as vulnerable, analysts are still required to investigate these alerts to rule out real threats. Instead of focusing on building new features or improving existing products, developers are also often pulled away to respond to a barrage of other security notifications, many of which turn out to be inconsequential.

Ultimately, vulnerability fatigue not only hampers the effectiveness of security teams and developers alike but also puts organizations at greater risk of serious security incidents. To break this cycle, organizations need smarter, context-driven prioritization that empowers teams to focus on what truly matters.

#### Why Our Approach to CVEs Must Change

As the number of CVEs and other pertinent threats to the software supply chain continues to grow, it's essential for organizations to move beyond surface-level assessments and analyze the context of each vulnerability before rushing to remediate. Context can dramatically reshape the perceived threat of a vulnerability because what appears urgent in isolation may turn out to be low-risk in real-world scenarios.

Embracing a more nuanced, context-driven approach empowers security teams to focus on vulnerabilities that truly matter, rather than being pulled in every direction to address each new disclosure.

Additionally, a context-aware strategy supports better communication between technical and business stakeholders, aligning security priorities with organizational goals. By creating the opportunity for more informed decision-making, organizations can strengthen their overall resilience and maintain the agility needed to adapt to emerging threats, without sacrificing innovation or productivity.

#### About the Author
