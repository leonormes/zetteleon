---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [naming_things]
title: Naming and organisation
type:
uid: 
updated: 
version:
---

## Organising Resource

Azure and AWS both offer robust approaches to organizing resources and managing permissions, but they use different terminologies and structures. Let's compare and contrast their approaches to help you align your deployment management across both platforms.

## Azure Approach

Azure uses a hierarchical structure to organize resources and manage permissions:

### Management Groups

- Top-level container for organizing subscriptions
- Can nest up to six levels deep
- Used to apply policies and access controls across multiple subscriptions[1]

### Subscriptions

- Container for resources
- Used for billing and access management
- Can be organized under management groups[2]

### Resource Groups

- Containers for resources within a subscription
- Used for logical grouping of related resources
- Helpful for applying policies and access controls at a more granular level[2]

### Azure Landing Zones

- Conceptual architecture for organizing resources
- Consists of platform landing zones and application landing zones
- Provides a scalable and modular approach to resource organization[8]

## AWS Approach

AWS uses a different structure for organizing resources and managing permissions:

### AWS Organizations

- Top-level service for managing multiple AWS accounts
- Provides centralized management of accounts
- Enables the use of Service Control Policies (SCPs) for permissions management[3]

### Organizational Units (OUs)

- Groupings of AWS accounts within an organization
- Can be nested for hierarchical organization
- Used for applying SCPs and managing permissions across groups of accounts[3]

### AWS Accounts

- Container for AWS resources
- Used for billing and access management
- Can be organized into OUs within AWS Organizations[7]

### Resource Groups and Tagging

- Used for logical grouping of resources across or within accounts
- Tagging allows for custom organization and management of resources[7]

## Comparison and Contrast

1. Hierarchy Structure
   - Azure: Management Groups > Subscriptions > Resource Groups > Resources
   - AWS: Organizations > OUs > Accounts > Resources

2. Policy Application
   - Azure: Uses Azure Policy at various levels of the hierarchy
   - AWS: Uses Service Control Policies (SCPs) at the organization and OU levels[3]

3. Resource Grouping
   - Azure: Uses Resource Groups within subscriptions
   - AWS: Uses tagging and Resource Groups across accounts

4. Billing Separation
   - Azure: Primarily at the subscription level
   - AWS: At the account level, with consolidated billing options[7]

5. Cross-Account Access
   - Azure: Managed through Azure Active Directory
   - AWS: Managed through IAM roles and policies[6]

6. Landing Zone Concept
   - Azure: Explicit Landing Zone architecture with platform and application zones[8]
   - AWS: Similar concepts implemented through account structure and AWS Control Tower

## Alignment Strategies

1. Consistent Naming Convention: Implement a consistent naming strategy across both platforms for easy identification of resources.
2. Hierarchical Structure: Map Azure Management Groups to AWS Organizations and OUs for consistent policy application.
3. Resource Tagging: Use consistent tagging strategies in both Azure and AWS for better resource organization and management.
4. Access Management: Align IAM policies in AWS with Azure RBAC for consistent access control across platforms.
5. Policy Alignment: Create equivalent policies in Azure Policy and AWS SCPs to maintain consistent governance.
6. Landing Zone Approach: Implement AWS Control Tower or custom landing zone architecture to mirror Azure Landing Zone concepts.
7. Centralized Monitoring: Use Azure Monitor and AWS CloudWatch with centralized logging to maintain visibility across both platforms.

By understanding and aligning these approaches, you can create a more consistent and manageable multi-cloud environment for your deployments[1][3][8].

To pull down all your management groups and their settings from the top-level tenant using Azure CLI, you can use the following command:

```bash
az account management-group list --expand -r
```

This command will:

1. List all management groups in your Azure tenant
2. Expand the details of each management group (--expand)
3. Recursively retrieve all child management groups (-r)

The output will include information such as:

- Management group IDs
- Display names
- Parent relationships
- Child management groups
- Associated subscriptions

If you want to format the output for better readability, you can add the `--output` parameter. For example:

```bash
az account management-group list --expand -r --output table
```

This will present the information in a more readable table format[1][3].

To get more detailed information about the hierarchy settings, you can use:

```bash
az account management-group hierarchy-settings list
```

This command will retrieve the hierarchy settings defined at the management group level, including default management group for new subscriptions and authorization requirements for group creation[5].

When organizing resources in GitLab repositories and Terraform Cloud projects and workspaces, the choice between structuring by customer or by environment depends on your specific needs and workflow. Here are some considerations for each approach:

### Customer/Dev, Test, Prod

Pros:

- Customer-Centric: This structure is intuitive if your primary focus is on individual customers. It allows you to easily see all environments for a specific customer.
- Isolation: Each customer's environments are isolated, which can simplify access control and management.

Cons:

- Redundancy: You may end up duplicating environment-specific configurations across customers.
- Scalability: As the number of customers grows, managing multiple environments for each can become complex.

### Dev/Customer, Test/Customer, Prod/Customer

Pros:

- Environment-Centric: This structure is beneficial if your focus is on managing environments consistently across customers. It allows for easier comparison and management of environments.
- Consistency: Promotes consistent environment configurations across all customers, reducing duplication.

Cons:

- Complexity: It may be more complex to manage customer-specific configurations within shared environments.
- Access Control: Requires careful management of access controls to ensure customers only see their own data.

### Recommendation

- Hybrid Approach: Consider a hybrid approach where you have a base structure by environment (Dev, Test, Prod) and use naming conventions or subdirectories to differentiate customers within each environment. This can provide a balance between customer-centric and environment-centric organization.
- Use Tags and Labels: In Terraform Cloud, use tags and labels to further categorize and filter projects and workspaces by customer and environment.
- Automation and Templates: Use automation tools and templates to ensure consistency across environments and customers, regardless of the structure you choose.

Ultimately, the best structure depends on your team's workflow, the number of customers, and the complexity of your deployments. Consider the pros and cons of each approach and choose the one that aligns best with your operational needs.

Aligning your resources around deployment stages like Tooling, Infrastructure, and Platform can offer several benefits, but it also comes with potential challenges. Here's a breakdown of the pros and cons:

### Benefits of Aligning Resources by Deployment Stages

1. Clarity and Focus:
   - Each stage has a clear purpose, making it easier to manage and understand the deployment process.
   - Teams can specialize in specific stages, improving efficiency and expertise.

2. Modularity:
   - Changes in one stage (e.g., Tooling) can be made independently of others, reducing the risk of unintended impacts.
   - Easier to update or replace components within a stage without affecting the entire system.

3. Scalability:
   - As your organization grows, you can scale each stage independently based on demand and resource needs.

4. Consistency:
   - Promotes consistent practices and configurations across different projects and environments.

### Challenges and Considerations

1. Complexity:
   - Managing separate stages can introduce complexity, especially if there are dependencies between them.
   - Requires careful coordination and communication between teams responsible for different stages.

2. Resource Management:
   - May require additional resources to manage and maintain separate stages, potentially increasing overhead.

3. Integration:
   - Ensuring seamless integration and communication between stages can be challenging, especially in complex environments.

4. Initial Setup:
   - Transitioning to a stage-based approach may require significant initial effort to reorganize existing resources and processes.

### Recommendation

- Evaluate Current Needs: Consider your current deployment process, team structure, and resource availability. If your current setup is working well, a major reorganization might not be necessary.
- Pilot Program: If you're interested in exploring this approach, consider running a pilot program with a small project to assess the benefits and challenges.
- Incremental Changes: Instead of a complete overhaul, make incremental changes to align resources with deployment stages where it makes sense and adds value.
- Feedback and Iteration: Gather feedback from your team and stakeholders to continuously improve the process.

Ultimately, the decision should be based on whether the benefits of aligning resources by deployment stages outweigh the potential complexity and resource requirements for your specific context.

Organizing Infrastructure as Code (IaC) and customer deployments across GitLab and Terraform Cloud requires careful consideration of your organization's needs, workflows, and best practices. HashiCorp and industry experts recommend several approaches to effectively manage your infrastructure. Here are some additional ideas and recommendations:

## Terraform Cloud Organization

HashiCorp recommends using Terraform Cloud's organizational features to structure your resources effectively[4]:

### Projects

Terraform Cloud introduced "Projects" as a new organizational layer between organizations and workspaces. This feature allows you to:

- Group related workspaces together
- Apply team-based permissions at the project level
- Isolate subsets of workspaces within a single organization

Benefits of using Projects include:

- Increased agility with workspace organization
- Reduced risk through centralized control
- Better efficiency with self-service capabilities

### Workspaces

Within projects, organize your workspaces based on:

- Environment (e.g., dev, staging, production)
- Application or service
- Team or business unit

Use consistent naming conventions for workspaces to improve clarity and management.

## GitLab Repository Structure

When organizing your IaC in GitLab, consider the following structure[3]:

### Separate Repositories

Create distinct repositories for:

- Infrastructure code (e.g., Terraform configurations)
- Application code

This separation allows for better version control and management of infrastructure changes.

### Infrastructure Repository Structure

Within your infrastructure repository:

1. Create separate directories for each cloud provider (e.g., AWS, Azure, GCP)
2. Use a "templates" directory for reusable Terraform modules
3. Include a `gitlab-ci.yml` file for CI/CD pipeline configuration

### Modularization

Leverage Terraform modules to encapsulate and reuse common infrastructure patterns[2]. This approach:

- Promotes code reuse
- Improves maintainability
- Allows for consistent implementation of best practices

## GitOps Workflow

Implement a GitOps workflow for managing your infrastructure[3]:

1. Use GitLab as the single source of truth for all infrastructure and application deployment code
2. Leverage merge requests (MRs) for collaboration and review of infrastructure changes
3. Automate the deployment process using GitLab CI/CD pipelines

## Terraform State Management

HashiCorp recommends using Terraform Cloud for state management[1]:

- Store state files remotely in Terraform Cloud
- Utilize workspace-specific state files
- Enable state locking to prevent concurrent modifications

## Tagging and Labeling

Implement a consistent tagging and labeling strategy[7]:

- Use tags to categorize resources by customer, environment, or application
- Apply labels in Terraform Cloud to organize workspaces and projects

## Security and Compliance

Incorporate security best practices[7]:

- Use HashiCorp Vault or similar tools to manage sensitive data securely
- Implement policy as code using tools like HashiCorp Sentinel or Open Policy Agent (OPA)
- Enable audit logging for tracking changes to infrastructure

## Continuous Integration and Deployment

Integrate Terraform with your CI/CD pipeline[7]:

- Automate Terraform plan and apply stages in your GitLab CI/CD pipeline
- Implement automated testing for your infrastructure code

## Hybrid Approach

Consider a hybrid approach that combines customer-centric and environment-centric organization:

- Use top-level projects in Terraform Cloud for environments (e.g., Dev, Test, Prod)
- Within each project, create workspaces for individual customers or applications
- Utilize tags and labels to further categorize resources

By implementing these practices and organizational structures, you can create a scalable, maintainable, and secure infrastructure management system that aligns with HashiCorp's recommendations and industry best practices. Remember to regularly review and adjust your approach based on your team's feedback and evolving needs[6].
