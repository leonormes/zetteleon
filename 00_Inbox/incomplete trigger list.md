---
created: 2026-01-13T03:49:56+00:00
modified: 2026-01-13T16:47:07+00:00
title: incomplete trigger list
---

SoT - DevOps Trigger List (v1.0)

Protocol:

 - Set Timer: 5 Minutes. (Strict limit to prevent hyper-focus).
 - Scan Mode: Read the prompt. If your brain says "Oh yeah, that thing…"—CAPTURE IT.
 - Do Not Execute: Do not fix the code now. Do not open the console. Just capture the Starter Task.
 - Apply PINCH: If a task feels heavy, tag it with a PINCH driver (e.g., Challenge: Can I script this in under 10 mins?).
1. The Active Scope (Agile & Jira)
 - Fake Progress: Is there a ticket in "In Progress" that hasn't moved in 3 days? (Capture: Check in on Ticket-123).
 - The "Done" Lie: Did I finish a deployment but forget to move the ticket to "Done"?
 - Scope Creep: Am I working on a Terraform refactor that isn't on the board? (Capture: Create ticket for VPC refactor).
 - The Stand-up Debt: Did I promise a link, a doc, or a review during stand-up that I haven't sent yet?
1. Infrastructure as Code (Terraform)
 - The Monolith: Is there a.tf file that is frustratingly long to scroll through? (Capture: Split main.tf into modules).
 - Drift Anxiety: Is there an environment (Dev/Stage) I suspect has drifted from the code?
 - Hardcoded Shame: Did I hardcode an AMI ID or a variable "just for now" that needs to be parameterized?
 - Version Lag: Are we using a Terraform provider version that is spamming us with deprecation warnings?
 - Orphaned State: Are there resources we deleted manually that are still in the state file?
1. Kubernetes & Helm (The Deployment Layer)
 - Values Bloat: Is the values.yaml file for our main app becoming a confusing mess?
 - Image Hygiene: Are we deploying images tagged:latest or old SHAs that need pinning?
 - Chart Rot: Are we using a Helm chart with deprecated API versions (e.g., old Ingress or PDBs)?
 - Secret Sprawl: Do we have Secrets in the cluster that should be in the external Vault/Secret Manager?
 - Namespace Junk: Are there "test" namespaces from last month that need deleting?
1. The Cloud (AWS & Azure)
 - Zombie Resources: Are there EBS volumes, Load Balancers, or Elastic IPs unattached and costing money?
 - Security Doors: Did I leave a Security Group open to 0.0.0.0/0 for "debugging" purposes?
 - IAM Bloat: Does the CI/CD user have AdministratorAccess when it only needs specific permissions?
 - Backup Trust: When was the last time I actually checked if a backup was created successfully?
1. Observability (Grafana & Logging)
 - The "No Data" Graph: Is there a panel in Grafana that is broken/empty that I ignore every day? (Capture: Fix or Delete Panel X).
 - Alert Fatigue: Is there an alert channel that I have muted because it's too noisy? (Capture: Tune threshold for CPU alert).
 - Blind Spots: Is there a specific error I keep seeing in logs that we don't have a metric for?
1. The Human API (Manager & Team)
 - Status Update: Is there a "Win" or a "Blocker" my manager doesn't know about yet?
 - Documentation Debt: Did I figure out a weird fix for a deployment failure that is only in my head? (Capture: Write SoT for Deploy Fix).
 - Continuous Delivery: What is the one manual step I do every deployment that I hate? (Capture: Investigate automating step X).
End of Protocol
Action: Take your captured list.
 - Apply the Two-Minute Rule: If it takes < 2 mins, do it now.
 - For the rest, define the Starter Task (Action 3.1) for each.
 - If you are overwhelmed, use SAVESTATE to dump the list and return to your primary task.
Would you like me to help you define the "Starter Task" for one of the items you just uncovered?
