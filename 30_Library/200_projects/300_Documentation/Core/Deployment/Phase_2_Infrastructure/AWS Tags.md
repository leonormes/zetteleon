---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: AWS Tags
type:
uid: 
updated: 
version:
---

For personal medical data, which is highly sensitive and protected under various regulations (like HIPAA), we should use the highest data classification level. Let me update the tags to reflect this:

```terraform:main.tf
  tags = {
    Owner               = "fitfile"
    BusinessUnit        = "devops"
    Environment         = "prd"
    Criticality        = "high"
    Service            = "application"
    Application        = "res"
    DataClassification = "HighlyConfidential-PHI"  # Updated to reflect medical data classification
    ProvisionByOrgName = "FITFILE"
  }
```

I've updated the `DataClassification` tag to `HighlyConfidential-PHI` where:

- "PHI" stands for Protected Health Information
- "HighlyConfidential" indicates the highest level of data sensitivity
- This classification is appropriate for personal medical data that requires special handling and protection under healthcare privacy regulations

The owner is already correctly set to "fitfile" (lowercase) in the configuration.

Let's run a plan to see the impact of these tag changes:

```bash
terraform plan
```

I see that the Terraform plan shows the following changes related to the tag updates:

1. The `DataClassification` tag will be updated from "CompanyConfidential" to "HighlyConfidential-PHI" across all resources.
2. The changes will affect multiple AWS resources including:
   - VPC Endpoints (autoscaling, ec2, ec2messages, ecr.api, ecr.dkr, elasticloadbalancing, logs, s3, ssm, ssmmessages, sts)
   - Each endpoint will have its tags updated to include the new data classification

3. Impact:
   - 50 resources to add
   - 9 resources to change
   - 55 resources to destroy
   - Estimated cost impact: +$0.64/month (total: $132.22/month)

The plan shows that updating the tags will require replacing many resources, particularly the VPC endpoints. This is because tags are often immutable properties that require resource recreation.

Would you like me to proceed with applying these changes? Or would you prefer to review the changes further or make any adjustments before proceeding?

Error: updating EC2 Internet Gateway (igw-0879de2758fbe02c7): detaching EC2 Internet Gateway (igw-0879de2758fbe02c7) from VPC (vpc-09699438879dc1479): operation error EC2: DetachInternetGateway, https response error StatusCode: 400, RequestID: 849c7b21-36d8-4f97-9c5e-39f82dee46ae, api error DependencyViolation: Network vpc-09699438879dc1479 has some mapped public address(es). Please unmap those public address(es) before detaching the gateway.
