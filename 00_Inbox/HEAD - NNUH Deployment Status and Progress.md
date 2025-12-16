---
aliases: []
confidence:
created: 2025-12-16T10:25:34Z
epistemic:
last_reviewed:
modified: 2025-12-16T11:57:41Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: []
title: HEAD - NNUH Deployment Status and Progress
type: head
uid:
updated:
---

Okay, let's load the NNUH context and clarify where we stand with the deployment, especially concerning the new outbound traffic route.

**NNUH Deployment Status and Progress:**

1.  **Initial Network & Security Approval**: As of about 4 months ago (2025-08-18), the technical documentation for NNUH was reviewed and approved from a cybersecurity perspective by Mike Brown. NNUH uses a Checkpoint perimeter firewall with an existing IPsec VPN tunnel to Azure for FITFILE connectivity. We noted that NNUH's firewall does not perform web filtering, but this happens at the NHS secure boundary.
2.  **Platform and Application Deployment**:
    -   The core FITFILE platform and initial applications for NNUH were successfully deployed as of 1 December 2025 (Jira task [FFAPP-4510](https://fitfile.atlassian.net/browse/FFAPP-4510) is DONE).
    -   Specific deployments like "NNUH: Hutch Bunny" ([FFAPP-4551](https://fitfile.atlassian.net/browse/FFAPP-4551)) and "NNUH: The Hyve deployment" are also DONE, both targeted for 5 December 2025.
    -   However, "NNUH: Application Configuration Deployment" ([FFAPP-4576](https://fitfile.atlassian.net/browse/FFAPP-4576)) is currently **IN PROGRESS**, with a target date of 5 December 2025. This indicates that while the platform is up, fine-tuning specific application settings is still ongoing.
3.  **Secret Management**: The `nnuh-prod-1` deployment adheres to our "Gold Standard" for secret management, utilizing the Vault Secrets Operator (VSO) to manage secrets such as the `cloudflare-issuer-api-token` and standard application secrets. This was confirmed about an hour ago (2025-12-16 09:25:40) during our secret management audit.
4.  **New Outbound Traffic Routing**: We've just received confirmation today at 10:20 (2025-12-16 10:21:44) from Tom Brooks at NNUH via email that:
    -   The NNUH network team has made the necessary changes on their firewall.
    -   We should now direct all outbound traffic from our services to **5.255.48.222**.
    -   They have offered to set up a meeting for testing.

**What to Do Next:**

The critical next step is to implement and verify this new outbound traffic route. Our standard deployment model emphasizes "Forced Tunnelling with User-Defined Routes (UDR)" to ensure all outbound traffic is inspected by a central firewall (e.g., Azure Firewall) in the hub VNet, with the next hop configured as a Virtual Appliance.

Here's how to get started:

1.  **Update Outbound Route Configuration**:
    -   Identify where the outbound routing for the NNUH FITFILE VNet is configured (e.g., User-Defined Routes applied to subnets, or Azure Firewall egress rules if we manage that component).
    -   Ensure that any default routes (`0.0.0.0/0`) or specific routes for outbound internet traffic are updated to point to the new NNUH egress IP: `5.255.48.222`.
    -   If using an Azure Firewall or similar appliance that we control within our Azure environment for egress, update its routing table or next-hop configuration accordingly.
    -   If any FITFILE services themselves have explicit outbound proxy configurations, ensure these are aligned, although typically forced tunneling handles this at the network level.
2.  **Coordinate Testing with NNUH**: Respond to Tom Brooks' email (received today at 10:20, 2025-12-16 10:21:44) and schedule a joint testing meeting. This testing will involve verifying that FITFILE services can successfully initiate outbound connections to external destinations, and that this traffic is indeed routed via the `5.255.48.222` IP.
3.  **Prepare for Connectivity Troubleshooting**: Refer back to previous connection test procedures, such as the [EOE -> CUH connection test](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2293399554/EOE+-+CUH+connection+test) (3 months, 14 days ago, 2025-09-02), to prepare for potential troubleshooting during the NNUH test. This includes:
    -   Being ready to provide source IP addresses of our AKS nodes/pods for NNUH's firewall log analysis.
    -   Being prepared to use tools like `traceroute`, Azure's "Effective Routes," and "IP Flow Verify" from Network Watcher if issues arise.
4.  **Review Application Configuration Deployment**: While updating the network routes, also review the ongoing "NNUH: Application Configuration Deployment" ([FFAPP-4576](https://fitfile.atlassian.net/browse/FFAPP-4576)) to ensure that any application-specific outbound endpoints or proxy settings are compatible with this new central egress point.

Let me know if you'd like me to help draft a response to Tom Brooks or if you need assistance in identifying the specific configuration files for this change.
