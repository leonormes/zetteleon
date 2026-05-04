# Establishing Your Best Practice AWS Environment - Amazon Web Services

## Why Should I Set up a Multi-account AWS Environment?

AWS enables you to experiment, innovate, and scale more quickly, all while providing the most flexible and secure cloud environment. 

An important means through which AWS ensures security of your applications is the AWS account. An AWS account provides natural security, access and billing boundaries for your AWS resources, and enables you to achieve resource independence and isolation. For example, users outside of your account do not have access to your resources by default. Similarly, the cost of AWS resources that you consume is allocated to your account. While you may begin your AWS journey with a single account, AWS recommends that you set up multiple accounts as your workloads grow in size and complexity. Using a multi-account environment is an AWS best practice that offers several benefits:

- Rapid innovation with various requirements – You can allocate AWS accounts to different teams, projects, or products within your company ensuring that each of them can rapidly innovate while allowing for their own security requirements.

- Simplified billing – Using multiple AWS accounts simplifies how you allocate your AWS cost by helping identify which product or service line is responsible for an AWS charge.

- Flexible security controls – You can use multiple AWS accounts to isolate workloads or applications that have specific security requirements, or need to meet strict guidelines for compliance such as HIPAA or PCI.

- Easily adapts to business processes – You can easily organize multiple AWS accounts in a manner that best reflects the diverse needs of your company's business processes that have different operational, regulatory, and budgetary requirements.

Ultimately, a multi-account AWS environment enables you to use the cloud to move faster and build differentiated products and services, all while ensuring you do so in secure, scalable and resilient manner. But, how should you build your multi-account AWS environment? You may have questions such as what account structure to use, what policies and guardrails should be implemented, or how to set up your environment for auditing.

The rest of this guide will walk you through the elements of building a secure and productive multi-account AWS environment, often referred to as a "landing zone," as recommended by AWS. This represents the best practices that can be used to build an initial framework while still allowing for flexibility as your AWS workloads increase over time.

## Best Practices for Setting up Your Multi-account AWS Environment

The basis of a well-architected multi-account AWS environment is [AWS Organizations](https://aws.amazon.com/organizations/), an AWS service that enables you to centrally manage and govern multiple accounts. Before getting started, let's get familiar with a few terms. An organizational unit (OU) is a logical grouping of accounts in your AWS Organization. OUs enable you to organize your accounts into a hierarchy, and make it easier for you to apply management controls. AWS Organizations [policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies.html) are what you use to apply such controls. [A Service Control Policy](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scp.html) (SCP) is a policy that defines the AWS service actions, such as Amazon EC2 Run Instance, that accounts in your organization can perform.

First, consider what account groupings or OUs you should create. Your OUs should be based on function or common set of controls rather than mirroring your company's reporting structure. AWS recommends that you start with security and infrastructure in mind. Most businesses have centralized teams that serve the entire organization for those needs. As such, we recommend creating a set of foundational OUs for these specific functions:

- Infrastructure: Used for shared infrastructure services such as networking and IT services. Create accounts for each type of infrastructure service you require.

- Security: Used for security services. Create accounts for log archives, security read-only access, security tooling, and break-glass.

Given that most companies have different policy requirements for production workloads, infrastructure and security can have nested OUs for non-production (SDLC) and production (Prod). Accounts in the SDLC OU host non-production workloads and therefore should not have production dependencies from other accounts. If there are variations in OU policies between life cycle stages, SDLC can be split into multiple OU's (e.g. dev and pre-prod). Accounts in the Prod OU host the production workloads.

Apply policies at the OU-level to govern the Prod and SDLC environment per your requirements. In general, applying policies at the OU-level is a better practice than at the individual account-level as it simplifies policy management and any potential troubleshooting.

![](https://d1.awsstatic.com/product-marketing/organizations/Product-Page-Diagram_Foundational.fc99a384c85dc9c5dd7986d92ef48aab527219e9.png)

Once the central services are in place, we recommend creating OUs that directly relate to building or running your products or services. Many AWS customers build these OU's after establishing the foundation.

- Sandbox: Holds AWS accounts that individual developers can use to experiment with AWS Services. Ensure that these accounts can be detached from internal networks and set up a process to cap spend to prevent overuse.

- Workloads: Contains AWS accounts that host your external-facing application services. You should structure OU's under SDLC and Prod environments (similar to the foundational OU's) in order to isolate and tightly control production workloads.

Now that both the foundational and production-oriented OU's are established, we recommend adding additional OU's for maintenance and continued expansion depending on your specific needs. These are some common themes based on practices from existing AWS customers:

- Policy Staging: Holds AWS accounts where you can test proposed policy changes before applying them broadly to the organization. Start by implementing changes at the account level in the intended OU, and slowly work out into other accounts, OUs, and across the rest of the organization.

- Suspended: Contains AWS accounts that have been closed and are waiting to be deleted from the organization. Attach an SCP to this OU that denies all actions. Ensure that the accounts are [tagged](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html) with details for traceability if they need to be restored.

- Individual Business Users: A limited access OU that contains AWS accounts for business users (not developers) who may need to create business productivity-related applications, for example set up an S3 bucket to share reports or files with a partner.

- Exceptions: Holds AWS accounts used for business use-cases that have highly customized security or auditing requirements, different from those defined in the Workloads OU. For example, setting up an AWS account specifically for a confidential new application or feature. Use SCPs at the account level to meet customized needs. Consider setting up a Detect and React system using CloudWatch Events and AWS Config Rules.

- Deployments: Contains AWS accounts meant for CI/CD deployments. You can create this OU if you have a different governance and operational model for CI/CD deployments as compared to accounts in the Workloads OUs (Prod and SDLC). Distribution of CI/CD helps reduce the organizational dependency on a shared CI/CD environment operated by a central team. For each set of SDLC/Prod AWS accounts for an application in the Workloads OU, create an account for CI/CD under Deployments OU.

- Transitional: This is used as a temporary holding area for existing accounts and workloads before moving them to standard areas of your organization. This may be because accounts are part of an acquisition, previously managed by a third party, or legacy accounts from an old organization structure. 

![](https://d1.awsstatic.com/product-marketing/organizations/Product-Page-Diagram_Organizational.66fa1fae2c9602db87a766680b9682c11772ee01.png)

### Conclusion

A well-architected multi-account strategy helps you innovate faster in AWS, while ensuring that you meet your security and scalability needs. The framework described on this page represents AWS best practices that you should use as a starting point for your AWS journey.

![](https://d1.awsstatic.com/product-marketing/organizations/Product-Page-Diagram_Organizational-Foundational-Units.d709f66bf4c45ed1af01360f3d39adecc1a99fb4.png)

To get started, refer to the AWS Organizations [Getting Started Guide](http://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started.html) to build your own multi-account AWS environment. Alternatively, you can use [AWS Control Tower](https://aws.amazon.com/controltower/) to help you quickly set up a secure initial AWS environment in a few clicks.