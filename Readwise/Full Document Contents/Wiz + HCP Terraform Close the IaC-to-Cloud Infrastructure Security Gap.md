# Wiz + HCP Terraform: Close the IaC-to-Cloud Infrastructure Security Gap

![rw-book-cover](https://www.datocms-assets.com/75231/1758586266-wiz_hashicorp_hcp_terraform.gif)

## Metadata
- Author: [[Gilad Berenblut, Nadav Tzuker]]
- Full Title: Wiz + HCP Terraform: Close the IaC-to-Cloud Infrastructure Security Gap
- Category: #articles
- Summary: Wiz integrates with HCP Terraform to scan plans and stop risky infrastructure changes before they deploy. It links live cloud resources to the exact Terraform files and lines that created them. Unified policies run across code, pipelines, and runtime so teams fix issues fast and prevent drift.
- URL: https://share.google/VaVG8UA7joexjHfXF

## Full Document
![](https://www.datocms-assets.com/75231/1758586541-e04lwss17ft-u084jfu35pa-e55943f53779-512.png?fit=crop&fm=jpg&h=100&w=100)
Infrastructure-as-Code (IaC) is a gift to engineers. By centralizing infrastructure definitions in Terraform, teams can standardize, review, and reuse patterns across every environment. HashiCorp has been instrumental in democratizing IaC, and HCP Terraform further enhances this by abstracting away much of the complexity of cloud deployments. One well-crafted module can deploy a compliant VPC baseline a thousand times over with no tickets and no toil.

But this acceleration cuts both ways. A single **risky declaration**, like an overly permissive IAM policy, can silently propagate misconfigurations at the same scale. Without end-to-end context, security tools operate in silos: CSPMs scan runtime and IaC scanners analyze code, creating a disconnect that developers distrust and security teams struggle with.

Wiz and HashiCorp have built an answer that meets teams where they work. Our integration closes the loop between what’s in your code and what’s running in the cloud. This allows you to prevent risky changes before they are deployed and trace any live issue back to its source in the code, delivering complete code-to-cloud visibility. In fact, **HashiCorp leverages this very integration for its own internal engineering teams**.

The first step to securing IaC is catching issues before they reach production. By integrating Wiz as a [**run task**](https://www.wiz.io/blog/wiz-and-hashicorp-integration-cloud-run-tasks) within HCP Terraform and Terraform Enterprise, every infrastructure plan is automatically scanned after the `terraform plan` stage.

Example of a policy applied consistently to both IaC code and live cloud resources
This approach is powered by Wiz's **unified policy engine**, which allows you to codify a rule once, for example, "S3 Bucket should have all 'Block Public Access' settings enabled", and apply it consistently across your code, pipelines, and runtime environments. This consistent enforcement reduces noise and shortens feedback loops, building trust between security and development teams. For business-critical plans, teams can configure policies to block the deployment entirely, providing a critical security gate.

The result is a workflow built for developers. Risks and fix guidance surface directly within Wiz and Terraform runs, allowing engineers to remediate issues in their natural workflow instead of through after-the-fact tickets.

![](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHBwgHBgoICAgLCgoLDhgQDhUWDRENFREaGx8lIh4fFiEmHysjHR0oKS0iJDUlKC0vMj4yGSI4PTcwPCsxMi8BCgsLDg0OHBAQHDsdFhwvOy8vLzsvLy8vLy8vLy8vLy8vLy87Ly8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vL//AABEIAA0AGAMBIgACEQEDEQH/xAAXAAADAQAAAAAAAAAAAAAAAAAABAcD/8QAIRAAAQMDBAMAAAAAAAAAAAAAAgABAxESUQUGQnEEIjH/xAAVAQEBAAAAAAAAAAAAAAAAAAABAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AG9j1j10O1WCG4hfClO0vXWRdsqoSzkEgs3x0huV3FCWbyTea2jUQpP/2Q==)![](https://www.datocms-assets.com/75231/1758587692-test-wiz-io_findings_code-cicd-scans.png?fm=webp)Example of a run task scanning findings report in the Wiz portal 
####  Outcome: Stop Risky Deployments Before They Land

Shifting cloud controls into the Terraform workflow changes the shape of risk.

* **Preventive security:** Critical misconfigurations are caught pre-deployment, not hours later by a CSPM alert.
* **Consistent policy:** Engineers see the same rules behave consistently across code, pipelines, and runtime, which reduces noise, shortens feedback loops, and builds trust.
* **Intact workflows:** Changes are addressed in code, reviewed, and deployed through the same CI/CD pipeline and HCP Terraform, keeping GitOps workflows intact.

Even with the best guardrails, some risks will make it into production. The challenge then becomes tracing a live issue back to its source to fix it once, in the right repository.

Our GA launch of the HCP Terraform connector enables organizations to achieve **complete IaC-to-cloud visibility with zero configuration**.

Stop chasing down code owners and forget about enforcing tagging hygiene. Wiz automatically maps cloud resources back to their Terraform definitions using the state file as the single source of truth. The process starts by scanning your version control system (like GitHub) and resolving Terraform variables and modules. Wiz then uses the Terraform state file as the bridge to automatically connect deployed resources to their declarations in code.

Code-to-cloud pipeline displayed on a Wiz issue
This lineage is visualized directly on the issues and resources' details pages, providing instant clarity. For deeper analysis, the full lineage is explorable in the **Wiz Security Graph**, where IaC resources are first-class citizens alongside runtime and identity context.

Examples of cloud configuration findings mapped to their IaC findings at the source (1:1 match)
When an S3 bucket is misconfigured, Wiz doesn't just name the resource; it points to the exact file, line of code, and module that defined it, along with the author and code owners. Developers can then open a targeted pull request and ship a quick fix.

The security loop becomes tight: Wiz flags an issue, a developer creates a PR to fix it, HCP Terraform redeploys the change, and Wiz confirms the remediation.

#### **Outcome: Accelerate Remediation and Control Drift**

This direct lineage turns hours of detective work into a single click.

* **Faster fixes:** Developers can open a targeted PR and ship a fix through the same pipeline.
* **Developer-first tooling:** With options like AI-assisted remediation and 1-click PRs, fixing issues becomes simple.
* **No more drift:** Eliminate manual console-side hotfixes while preserving IaC integrity as a source of truth for the cloud infrastructure.

> The code-to-cloud integration between Wiz and HCP Terraform/TFE gives us the ability to trace every cloud resource back to the exact lines of code that defined it–taking manual discovery out of the remediation process. Through Wiz scans in run tasks, detective policies can now be used for prevention.
> 
> 

Wiz and HCP Terraform unite prevention and proof, blocking risky deployments and tracing all others back to the source. This is why leading organizations, including HashiCorp, trust this integration to enhance their cloud security posture. This reduces security toil, gives developers precise feedback, and aligns cloud environments with their code definitions.

Ultimately, once the loop between written, deployed, and secure code is closed, there's only more on the horizon.

Upcoming integrations will combine Wiz's deep security insights with new automation frameworks, which will enable organizations to go beyond simply identifying security issues toward actual automated remediation. This new collaboration will give end users a holistic view of their infrastructure, further bridging the gap between security findings and actionable workflows.

If you’re already a Wiz customer, connect your code repositories and set up Wiz [run tasks](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/run-tasks) in your HCP Terraform or Terraform Enterprise organization. You’ll unlock the **unified policy engine** and **code-to-cloud mapping** duo immediately, and your existing cloud data will become far more actionable. Join companies like HashiCorp in leveraging this powerful integration for end-to-end cloud security.

New to Wiz? [Book a demo](https://www.wiz.io/demo). We’ll show you how to unify policy across **code, pipelines, and runtime**, visualize lineage in the **Security Graph**, and help developers fix issues **at the source** with AI-assisted workflows.
