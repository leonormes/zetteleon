# HashiCorp’s New Guide Offers Practical Advice on Writing and Rightsizing Terraform Modules

![rw-book-cover](https://res.infoq.com/news/2025/11/advice-rightsizing-terraform/en/headerimage/generatedHeaderImage-1762706293657.jpg)

## Metadata
- Author: [[Craig Risi]]
- Full Title: HashiCorp’s New Guide Offers Practical Advice on Writing and Rightsizing Terraform Modules
- Category: #articles
- Summary: HashiCorp’s new guide helps teams build Terraform modules that are clear, secure, and easy to maintain. It stresses keeping modules focused, versioned, tested, and aligned with user needs. This approach reduces risks and improves infrastructure management in large organizations.
- URL: https://www.infoq.com/news/2025/11/advice-rightsizing-terraform/

## Full Document
In a blog post titled "[How to write and rightsize Terraform modules](https://www.hashicorp.com/en/blog/how-to-write-and-rightsize-terraform-modules)", HashiCorp shares a comprehensive framework for creating maintainable, scalable modules in the [Terraform](https://developer.hashicorp.com/terraform) ecosystem. Author Mitch Pronschinske draws on insights from consultant Rene Schach's HashiDays 2025 session to focus on four key pillars: module scope, code strategy, security, and testing.

According to the post, module design starts with carefully understanding the target users and use cases. Module consumers might include development teams, platform engineers, or security specialists, but each module should have a clear purpose and minimal coupling. HashiCorp recommends separating infrastructure components that change frequently from those that are stable, aligning module lifecycle to resource volatility. For example, compute instances and disks might live in one module while long-lived networking infrastructure resides in another.

On the code structure front, the post advises treating modules like software artifacts: version them semantically, structure files purposefully, provide examples and documentation, and mirror provider schemas rather than diverge needlessly. Good module design, according to the guide, helps simplify upgrades, makes intent clear to new contributors, and reduces drift over time.

Security and testing are also flagged as core concerns. Pronschinske urges teams to validate inputs early using Terraform's variable validation blocks, adopt [policy-as-code](https://blog.gitguardian.com/what-is-policy-as-code-an-introduction-to-open-policy-agent/) frameworks such as [Sentinel](https://www.microsoft.com/en-za/security/business/siem-and-xdr/microsoft-sentinel) or [OPA](https://www.openpolicyagent.org/), and integrate testing into CI/CD pipelines using the native "terraform test" command. Modules that expose fewer inputs, provide sensible defaults, and enforce guardrails are less likely to be misused or introduce risk.

HashiCorp's guide offers a structured set of best practices for Terraform module authors who are working within large organizations or platforms. By focusing on user-centred design, cohesive module boundaries, software-style governance, security checks, and integration with testing pipelines, the blog aims to help teams tailor their infrastructure-as-code practice for greater reusability and maintainability at scale.

In contrast, [common anti-patterns](https://reaverops.medium.com/terraform-anti-patterns-practices-to-steer-clear-of-b7ce2784e85d) include creating monolithic root modules that bundle many resources across unrelated domains, leading to inflated state files, brittle updates, and high coupling. Another [anti-pattern](https://krausen.io/terraform-best-practices-writing-maintainable-infrastructure-code) is modules that assume broad flexibility without guardrails - where every attribute is exposed, every variable is uncontrolled, and which lack versioning, testing, and documentation, making upgrades risky and onboarding slower.

By juxtaposing these, it becomes clear that teams should strive for modules that are cohesive, minimally coupled, version-controlled, and tested, rather than sprawling, untested, and overloaded with variables. This reduces technical debt, improves predictability and maintainability, and aligns Terraform module design with software engineering best practices, as HashiCorp's guidance suggests.

While these best practices are insightful, they are not necessarily unknown. A feature article in [The New Stack](https://thenewstack.io/experts-share-best-practices-for-building-terraform-modules) in 2024 gathered insights from infrastructure engineers on best practices for module development. While not addressing "rightsizing" per se, the article reinforced many of the themes in HashiCorp's blog, notably the importance of modular boundaries and versioning.

Similarly, a series of blog posts by [Spacelift](https://spacelift.io/blog/terraform-best-practices) that pre-dated HashiCorp’s blog discusses common failings in Terraform module design, such as overly broad modules and the absence of testing, effectively serving as criticism of what HashiCorp is trying to remedy.

Together, these sources show that the themes HashiCorp highlights (module scope, software-style discipline, testing) resonate with the broader community's concerns. They also suggest that module design remains a pain point for many teams, and HashiCorp's guidance is arriving amid interest in Terraform module governance and maintainability.

[![](https://cdn.infoq.com/statics_s1_20251106092357u1/images/profiles/4eedfa30bc8c34995c3dbb7fcc18bb8e.jpg)](https://www.infoq.com/profile/Craig-Risi/)
