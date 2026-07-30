---
created: 2026-07-29T12:54:12+00:00
modified: 2026-07-30T08:21:38+00:00
permalink: llmeon/00-inbox/aws-access-report
title: aws access report
type: note
---

## Overview

Amazon EKS clusters configured with a private API server endpoint (`endpointPrivateAccess=true`, public access disabled) cannot be reached directly from the internet, mirroring the private-VPC posture already in place for EC2 workloads accessed via AWS Systems Manager (SSM) and the equivalent Azure Bastion pattern on the Azure side. AWS provides several distinct mechanisms for bridging a local machine to that private endpoint, spanning full network-level tunnels, per-request zero-trust access, and simple port-forwarding over existing agent infrastructure. This report ranks six AWS-native options from strongest to weakest security posture, validated against AWS's own documentation and networking best-practices guidance, and corrects two issues identified in a prior draft: a mislabeling of PrivateLink's scope, and an under-justified security ranking between Client VPN and SSM port-forwarding.

## Ranked Options

| Rank | Option | Network exposure | Identity/device granularity | Operational overhead |
|------|--------|-------------------|------------------------------|-----------------------|
| 1 | AWS Verified Access | None—no network-level access granted | Per-request identity + device posture check | Moderate setup, low ongoing |
| 2 | Private cluster endpoint + existing VPC connectivity (VPN/Direct Connect/Transit Gateway/peering) | Scoped to routed private endpoint only | Network-layer only | Low once connectivity exists |
| 2 (tie) | SSM Session Manager port-forwarding to remote host | Single scoped tunnel to one host:port | IAM-gated per session | Low—reuses existing agent |
| 4 | EC2 Instance Connect Endpoint (EICE) tunnel | Single scoped tunnel via VPC endpoint | IAM-gated per session | Low, no agent required |
| 5 | AWS Client VPN | Full VPC network reachability for the client | Authorization rules, not per-request | Moderate—client + cert distribution |
| 6 | Classic bastion host with public IP and SSH | Internet-facing instance, open inbound port | SSH key/credential only | High—patching, key rotation, hardening |

### 1. AWS Verified Access—strongest, Zero-trust

AWS Verified Access evaluates identity and device posture on every single request rather than granting the user broad network reachability. AWS's own networking best-practices guidance explicitly states that Verified Access is "the preferred option" for new application-access use cases, citing per-request policy evaluation, elimination of VPN client management, and stronger audit logging as the deciding factors over VPN-based approaches. Because access decisions happen per request rather than once at connection time, a compromised laptop or leaked credential does not grant broad lateral network reachability—it grants only continuously re-checked access to the specific application endpoint, which for `kubectl` traffic against the EKS API server is a materially smaller blast radius than any VPN-based tunnel. One caveat worth flagging for planning: because the Kubernetes API server is not a browser-based HTTP application, per-request access to it requires installing AWS's "Connectivity Client" on the local machine rather than working through pure browser-based authentication, so it is not entirely client-free for this specific use case.[^1][^2][^3][^4]

### 2 (Tie). Private cLuster eNdpoint rEached via eXisting VPC cOnnectivity

This is distinct from PrivateLink and should not be conflated with it. Amazon EKS supports disabling the public Kubernetes API endpoint entirely and enabling only the private endpoint (`endpointPrivateAccess=true`), which removes any public path to the API server. Reaching that private endpoint from a location outside the cluster's VPC requires standard VPC-network connectivity—VPN, Direct Connect, Transit Gateway, or VPC peering—routed correctly to the private hosted zone. A common setup failure is incorrect DNS configuration: the VPC must have both `enableDnsHostnames` and `enableDnsSupport` set, or the private hosted zone will not resolve, which AWS documentation flags directly as a frequent gotcha. Notably, AWS PrivateLink itself (the `com.amazonaws.region.eks` interface VPC endpoint) is a separate mechanism that provides private connectivity to the EKS control-plane management API—the AWS API used for calls like `DescribeCluster`—and AWS's documentation is explicit that these EKS interface endpoints "do not support access to Kubernetes APIs, as these have a separate private endpoint". For fully air-gapped clusters, `eksctl` also supports building fully private clusters with no outbound internet access, relying on VPC endpoints purely for AWS service calls rather than Kubernetes API traffic.[^5][^6][^7]

### 2 (Tie). SSM Session Manager pOrt-forwarding to rEmote hOst

This option reuses infrastructure already deployed for jumpbox access and applies the same IAM-gated, agent-based tunnel model to the EKS API endpoint instead of RDP or SSH:

```bash
aws ssm start-session \
  --target <instance-id> \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["<PRIVATE_EKS_API_ENDPOINT>"],"portNumber":["443"],"localPortNumber":["6443"]}' \
  --region <region> --profile <profile>
```

`kubectl` is then pointed at `https://localhost:6443` with kubeconfig adjusted for the tunnel. This requires the `AWS-StartPortForwardingSessionToRemoteHost` document specifically—not the plain `AWS-StartPortForwardingSession` used for direct RDP/SSH access to the instance itself—and additionally requires `ssmmessages:CreateControlChannel`, `CreateDataChannel`, `OpenControlChannel`, and `OpenDataChannel` permissions layered on top of `ssm:StartSession`, a commonly missed IAM requirement documented in both AWS's own port-forwarding announcement and repeated community troubleshooting threads. Security-wise, no inbound ports are opened on the instance, the SSM Agent makes only outbound calls to AWS, and the tunnel scope is limited to a single host:port pair, which independent technical comparisons conclude offers "the best balance of high security… and lower operational overhead" compared to both classic bastions and full VPN tunnels for reaching one specific private service. Given this narrow, single-endpoint blast radius, this option is ranked on par with—arguably ahead of—Client VPN rather than beneath it, contrary to a broader-vs-narrower network access logic that should apply consistently across ranked options.[^8][^9][^10][^11][^12][^13]

### 4. EC2 Instance Connect Endpoint (EICE)

EICE is a purpose-built AWS mechanism for eliminating bastion hosts that operates purely through a regional VPC endpoint and security groups, without requiring the SSM Agent or its associated IAM permissions set. The `aws ec2-instance-connect open-tunnel` CLI command establishes an arbitrary port-forwarding tunnel to a private IP address through the endpoint, functionally similar to SSM's remote-host forwarding. This is a legitimate, AWS-native alternative to SSM port-forwarding worth evaluating for the EKS API path, though its tunnel-port restrictions and exact behavior for arbitrary destination ports (versus SSH/RDP-specific tunnels) should be confirmed against current AWS documentation before adopting it for port 443/6443 traffic to the Kubernetes API server.[^14][^15][^16][^17][^18][^19]

### 5. AWS Client VPN—most Direct Match to Azure Bastion's Mental Model

Client VPN tunnels the local machine directly into the VPC at the network layer; once connected, `kubectl` works against the private endpoint exactly as any in-VPC client would. AWS's own comparison guidance states plainly that "Client VPN places the user on the network so they can reach applications by IP," with authorization rules constraining which network destinations are reachable—but this is fundamentally broader network-level access than either Verified Access or a scoped port-forward tunnel. AWS's migration guidance for these two services explicitly frames Verified Access as removing "the need for a client-based VPN" and states Client VPN "is not the long-term answer for application access" for new use cases going forward. This option is the most operationally simple and the closest behavioral equivalent to Azure Bastion, but it carries materially more blast radius than the SSM or EICE tunnel-based approaches if a laptop or credential is compromised.[^20][^1]

### 6. Classic Bastion Host with Public IP—weakest, Legacy Pattern

A public-IP bastion with open SSH remains technically viable for reaching a private EKS endpoint but requires exposing and continuously hardening an internet-facing instance—patching, key rotation, security-group management, and monitoring for open port 22/3389 traffic. AWS's own historical Session Manager announcement confirms this was the prior-generation recommendation before Session Manager port-forwarding existed, explicitly stating that "to reduce the surface of attack, AWS recommends using a bastion host" was the older guidance now superseded. This is the exact pattern the existing SSM jumpbox setup has already moved away from, and it should not be extended to EKS API access.[^21][^22][^10]

## Correction Notes on Prior Draft

Two issues in an earlier version of this analysis are corrected here. First, PrivateLink was previously used as an umbrella label for both the EKS _management_ API and the Kubernetes API server's private endpoint; AWS documentation treats these as separate mechanisms, and only the former is actually "PrivateLink"—the latter is reached via ordinary VPC-network connectivity (VPN/Direct Connect/Transit Gateway/peering) once the private endpoint is enabled. Second, the earlier ranking placed Client VPN above SSM port-forwarding on security grounds; independent technical analysis and the same "narrower access surface is more secure" logic used to rank Verified Access above VPN support placing the single-endpoint SSM tunnel on par with or ahead of the full-network Client VPN tunnel instead.[^7][^9][^5]

## Recommendation Summary

- For the strongest overall security posture: disable the EKS public endpoint entirely, reach the private endpoint via existing VPC connectivity, and gate individual engineer access through AWS Verified Access rather than a network-level VPN tunnel.[^2][^1][^5]
- For reusing infrastructure already trusted and operated (SSM): extend the existing SSM jumpbox pattern with the `AWS-StartPortForwardingSessionToRemoteHost` document targeting the EKS API endpoint, adding the required `ssmmessages` permissions—no new infrastructure, same IAM-gated tunnel model as the current RDP/SSH setup.[^12][^8]
- For the closest behavioral match to Azure Bastion: AWS Client VPN is the nearest equivalent, though it should be considered a transitional step toward Verified Access given AWS's own stated direction for zero-trust application access.[^20][^1]

---

## References

1. [Remote Access - Networking Best Practices](https://aws.github.io/aws-networking-best-practices/connectivity/remote-access/) - AWS Networking Architecture guidance and best practices by the AWS user community, vetted by AWS Net…
2. [AWS Verified Access - AWS Documentation](https://docs.aws.amazon.com/verified-access/latest/ug/what-is-verified-access.html) - Learn about AWS Verified Access, a service that helps you manage secure access to applications witho…
3. [VPN-less Secure Network Access to Corporate Applications](https://aws.amazon.com/blogs/aws/aws-verified-access-preview-vpn-less-secure-network-access-to-corporate-applications/) - AWS Verified Access, a new secure connectivity service that allows enterprises to enable local or re…
4. [Connectivity Client for AWS Verified Access](https://docs.aws.amazon.com/verified-access/latest/ug/connectivity-client.html) - AWS Verified Access provides the Connectivity Client so that you can enable connectivity between use…
5. [Configure network access to cluster API server endpoint](https://docs.aws.amazon.com/eks/latest/userguide/config-cluster-endpoint.html) - Learn how to enable private access and limit public access to the Amazon EKS cluster Kubernetes API …
6. [EKS Fully-Private Cluster - Eksctl User Guide](https://docs.aws.amazon.com/eks/latest/eksctl/eks-private-cluster.html) - eksctl supports creation of fully-private clusters that have no outbound internet access and have on…
7. [Access Amazon EKS using AWS PrivateLink](https://docs.aws.amazon.com/eks/latest/userguide/vpc-interface-endpoints.html) - Learn how to securely access Amazon Elastic Kubernetes Service (Amazon EKS) APIs from within your VP…
8. [Policy for SSM Port Forwarding Session to Remote Host](https://repost.aws/questions/QUMa9_kum3Sk-fg4TL6sPfZg/policy-for-ssm-port-forwarding-session-to-remote-host) - I'm trying to start a port forwarding session to our RDS through a bastion host. I have it working f…
9. [SSH Tunneling vs VPN vs SSM - Sai's Notebook](https://sai-tai.com/aws/networking/private-access-comparison/) - Secure access comparison of SSH tunneling via bastion, VPN connections, and SSM Session Manager port…
10. [Killing the Bastion Host: SSM Session Manager in Practice](https://bipi.in/blog/aws-ssm-session-manager-vs-bastion) - SSM Session Manager replaces bastion hosts with IAM-based access, session logging, and no inbound po…
11. [Securely Access Window Bastion host using System Manager Port Forwarding method](https://dev.to/aws-builders/securely-access-window-bastion-host-using-system-manager-port-forwarding-method-2h2i) - This secure solution I introduced to one of the largest financial institution in US to access their….
12. [Use port forwarding in AWS Systems Manager Session ...](https://aws.amazon.com/blogs/mt/use-port-forwarding-in-aws-systems-manager-session-manager-to-connect-to-remote-hosts/) - We recently announced a new capability within AWS Systems Manager Session Manager that allows forwar…
13. [Secure RDS Access Without Bastion Hosts - Trestle Engineering](https://trestleiq.com/secure-rds-access-without-bastion-hosts-using-aws-ssm-session-manager/) - This blog post introduces a modern, secure alternative that Trestle adopted recently: using AWS Syst…
14. [You can use EC2 Instance Connect Endpoint to connect to an ...](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-using-eice.html) - Open the Amazon EC2 console at <https://console.aws.amazon.com/ec2/>. · In the navigation pane, choos…
15. [Connect to your instances using a private IP address and ...](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-with-ec2-instance-connect-endpoint.html) - The EC2 Instance Connect Endpoint Service establishes a private tunnel from your computer to the end…
16. [EC2 Instance Connect エンドポイント登場！踏み台サーバー不要で ...](https://dev.classmethod.jp/articles/ec2-instance-connect-endpoint-private-access/) - EC2 Instance Connectは死んでいなかった
17. [#aws #awscommunity #awscommunitybuilders #vpc #devops ...](https://www.linkedin.com/posts/roman-siewko_aws-awscommunity-awscommunitybuilders-activity-7075536906003845120-VDkv) - ✴️ Use "EC2 instance Connect" to connect to RDS and other VPC resources—no VPN required, no EC2 Ba…
18. [Simplifying Access to EC2 Instances on Private Subnets with ...](https://www.trevorrobertsjr.com/blog/ec2-instance-connect-automate/) - In this blog post, I shared how you can use the EC2 Instance Connect Endpoint to securely connect to…
19. [Connecting to Private EC2 Instances Using an Amazon ...](https://dev.to/aws-builders/connecting-to-private-ec2-instances-using-an-amazon-ec2-instance-connect-endpoint-chl) - Amazon EC2 Instance Connect (EIC) Endpoints provide a secure and seamless option for connecting to p…
20. [AWS Client VPN and AWS Verified Access migration and ...](https://aws.amazon.com/blogs/networking-and-content-delivery/aws-client-vpn-and-aws-verified-access-migration-and-interoperability-patterns/) - Verified Access validates every application request before granting users access and, crucially, rem…
21. [Port Forwarding Using AWS System Manager Session ...](https://aws.amazon.com/blogs/aws/new-port-forwarding-using-aws-system-manager-sessions-manager/) - To reduce the surface of attack, AWS recommends using a bastion host, also known as a jump host. Thi…
22. [AWS SSM Session Manager: Kill Your Bastion Hosts](https://www.bitslovers.com/aws-ssm-session-manager/) - Every bastion host in your architecture is a maintenance burden and an attack surface. You need to k…
