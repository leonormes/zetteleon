# New Infrastructure-as-Code Tool "formae" Takes Aim at Terraform

![rw-book-cover](https://res.infoq.com/news/2025/10/iac-formae/en/card_header_image/generatedCard-1761678829222.jpg)

## Metadata
- Author: [[Matt Saunders]]
- Full Title: New Infrastructure-as-Code Tool "formae" Takes Aim at Terraform
- Category: #articles
- Summary: Platform Engineering Labs released formae, a new open-source tool for managing cloud infrastructure that automatically discovers and updates existing resources. It aims to solve common problems like state drift and complex workflows by treating the real environment as the source of truth. Formae uses a unique language and design to reduce complexity and improve reliability compared to older tools like Terraform.
- URL: https://www.infoq.com/news/2025/10/iac-formae/

## Full Document
Infrastructure tool company [Platform Engineering Labs](https://platform.engineering/) has released [formae](https://platform.engineering/formae), an open-source infrastructure-as-code platform. It is trying to address what they describe as fundamental limitations in existing infrastructure-as-code tools. In a [press release](https://www.prweb.com/releases/platform-engineering-labs-unveils-formae-a-groundbreaking-open-source-infrastructure-as-code-platform-built-for-the-future-302590945.html), the New York-based company announced the launch on 22 October 2025, positioning formae as the first major innovation in infrastructure-as-code in nearly a decade.

The platform tackles problems familiar to many platform engineering teams: sprawling cloud estates, drift between code and live environments, and fragile toolchains. According to Pavlo Baron, co-founder and CEO of Platform Engineering Labs, the tool emerged from direct experience with these challenges:

>  We built formae out of our own pain. It is the first platform that starts from reality, not from an idealised plan. It accepts even the messiest truth of any cloud environment and provides a safe, reliable way to evolve it.
> 
>  

![formae preview, courtesy of Platform Engineering Labs](https://res.infoq.com/news/2025/10/iac-formae/en/resources/11_jyLnLam-uUC98Gv-DXtBvw-1761678828326.webp)formae preview, courtesy of Platform Engineering Labs
There are two modes of operation for formae. Firstly there is a 'reconcile' mode which aligns the desired environment state with what actually exists in production, and secondly 'patch' mode which allows operators to apply incremental changes. The platform eliminates explicit state file management by treating reality itself as the state, versioned in code. Changes are managed through an agent-based architecture that decouples state management from clients.

formae differentiates itself through automatic discovery and codification of existing infrastructure. The platform maps every running resource across cloud estates regardless of how those resources were originally created, whether through Terraform, OpenTofu, Pulumi, manual cloud console operations, or legacy scripts. This approach contrasts with traditional infrastructure-as-code tools, which need engineers to start with a plan and maintain separate state data depending on which tool created the resources.

The platform uses PKL, a configuration-as-code language originally developed by Apple, rather than the HashiCorp Configuration Language used by Terraform and OpenTofu. This choice has drawn mixed reactions. [Writing on LinkedIn](https://www.linkedin.com/posts/adamjacob_quick-start-activity-7386778249323933696-alg8), Adam Jacob, CEO and co-founder of [System Initiative](https://www.infoq.com/news/2025/09/system-initiative-ai-platform/), noted that the PKL decision "maybe is good, or maybe is bad, depending on how you feel about external DSLs."

Jacob also offered measured praise for formae's technical approach. He commended its separation of inventory from resource declaration as "smart," because it allows teams to query inventory and produce declarations when needed. He also praised the quality of the documentation and its clear design for building developer abstractions.

In the press release, [Marc Schnitzius, Platform Engineering Lead at codecentric](https://de.linkedin.com/in/marc-schnitzius), highlighted the platform's design philosophy:

>  formae doesn't just move complexity from dev to ops — it truly helps achieve reduced cognitive load for both developers and operations teams by abstracting the complexity on both sides in modern cloud-native environments.
> 
>  

formae is entering a busy space, with Terraform and OpenTofu having mature ecosystems and broad multi-cloud support, and other tools, such as [Spacelift](https://spacelift.io/), providing additional workflow automation. It attempts to address Terraform workflow risks by utilising automated discovery and ensuring that infrastructure updates are kept to a minimum. Sentiment suggests that the platform's success will probably hinge on whether its approach to automatic discovery and codification proves more valuable than the familiarity and community support surrounding existing tools.

The tool is published under a Functional Source License from Platform Engineering Labs. The intention of this is to make formae accessible and safe for users, while also creating a business model that sustains the company. The open-source release enables early adopters to experiment and adopt regardless of their budget, and allows community members to contribute to the project.

Also in the press release, Harry Brumleve, founder of Thoughtful Software and early-stage advisor, described formae as "a significant evolutionary leap forward in both DevOps and software development" with potential impact extending beyond engineering teams to create value for businesses and customers.

The platform is [available on GitHub](https://github.com/platform-engineering-labs/formae) with community discussions hosted on Discord. Platform Engineering Labs states its mission as eliminating unnecessary toil, reducing human error, and enabling confident engineer contributions within platform engineering. An [introductory blog post](https://blog.platform.engineering/we-have-launched-formae-iac-how-it-it-should-be-6b3ea0d801dd) also provides further details.
