# No title

![rw-book-cover](https://docs.aws.amazon.com/favicon.ico)

## Metadata
- Author: [[amazon.com]]
- Full Title: No title
- Category: #articles
- Summary: AWS provides documentation about its services and features. The content explains how to use AWS tools and best practices. It helps users set up and manage cloud resources.
- URL: https://docs.aws.amazon.com/eks/latest/userguide/doc-history.rss

## Full Document
```
<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
   <channel>
      <title>Amazon EKS Document History</title>
      <link>https://docs.aws.amazon.com/eks/latest/userguide/</link>
      <description>A RSS feed containing the latest updates on https://docs.aws.amazon.com/eks/latest/userguide/.</description>
      <language>en-us</language>
      <atom:link href="https://docs.aws.amazon.com/eks/latest/userguide/doc-history.rss"
                 rel="self"
                 type="application/rss+xml"/>
      <lastBuildDate>Mon, 13 Oct 2025 00:22:00 GMT</lastBuildDate>
      <item>
         <title>Kubernetes version 1.34</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-1-34</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.34&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Thu, 2 Oct 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.34_2025-10-02</guid>
      </item>
      <item>
         <title>Configurable node auto repair</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/node-health.html</link>
         <description>Amazon EKS now provides more granular control over the node auto repair behavior.</description>
         <pubDate>Mon, 22 Sep 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Configurable_node_auto_repair_2025-09-22</guid>
      </item>
      <item>
         <title>Refresh cluster insights</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/view-cluster-insights.html</link>
         <description>You can now manually refresh cluster insights.</description>
         <pubDate>Wed, 27 Aug 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Refresh_cluster_insights_2025-08-27</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added permission to &lt;code class="code"&gt;AmazonEKSServiceRolePolicy&lt;/code&gt;. This role can attach new access policy &lt;code class="code"&gt;AmazonEKSEventPolicy&lt;/code&gt;. Restricted permissions for &lt;code class="code"&gt;ec2:DeleteLaunchTemplate&lt;/code&gt; and &lt;code class="code"&gt;ec2:TerminateInstances&lt;/code&gt;.</description>
         <pubDate>Tue, 26 Aug 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2025-08-26</guid>
      </item>
      <item>
         <title>Cross-service confused deputy prevention</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cross-service-confused-deputy-prevention.html</link>
         <description>Added a topic with an example trust policy that you can apply for Cross-service confused deputy prevention.
Amazon EKS accepts the &lt;code class="code"&gt;aws:SourceArn&lt;/code&gt; and &lt;code class="code"&gt;aws:SourceAccount&lt;/code&gt; conditions in the trust policy of an EKS cluster role.</description>
         <pubDate>Tue, 19 Aug 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Cross-service_confused_deputy_prevention_2025-08-19</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. This includes new patch versions of Kubernetes &lt;code class="code"&gt;1.33.2&lt;/code&gt;, &lt;code class="code"&gt;1.32.6&lt;/code&gt;, &lt;code class="code"&gt;1.31.10&lt;/code&gt;, and &lt;code class="code"&gt;1.30.14&lt;/code&gt;.</description>
         <pubDate>Wed, 30 Jul 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2025-07-30</guid>
      </item>
      <item>
         <title>VPC CNI Multi-NIC feature for multi-homed pods</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/pod-multiple-network-interfaces.html</link>
         <description>Amazon EKS adds multi-homed pods to the VPC CNI. Now you can configure a workload and the VPC CNI assigned IP addresses from every NIC on the EC2 instance to each pod. The application can make concurrent connections to use the bandwidth from each NIC. Every network interface is configured in the same subnet and security groups as the node. Previously, you needed to use Multus CNI to run multiple other CNIs to create multi-homed pods. Documentation and steps to do this have been moved to &lt;a href="https://docs.aws.amazon.com/eks/latest/userguide/pod-multus.html"&gt;eks/latest/userguide/pod-multus.html&lt;/a&gt;.</description>
         <pubDate>Tue, 15 Jul 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#VPC_CNI_Multi-NIC_feature_for_multi-homed_pods_2025-07-15</guid>
      </item>
      <item>
         <title>VPC CNI troubleshooting content update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/network-policies-troubleshooting.html</link>
         <description>Expanded the troubleshooting page for Kubernetes &lt;em&gt;network policy&lt;/em&gt; in the VPC CNI. Added the CRDs and RBAC permissions, and 12 known issues.</description>
         <pubDate>Mon, 30 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#VPC_CNI_troubleshooting_content_update_2025-06-30</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. There arenâ€™t any new patch versions of Kubernetes in these platform version.</description>
         <pubDate>Thu, 26 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2025-06-26</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added &lt;code class="code"&gt;ssmmessages:OpenDataChannel&lt;/code&gt; permission to &lt;code class="code"&gt;AmazonEKSLocalOutpostServiceRolePolicy&lt;/code&gt;.</description>
         <pubDate>Thu, 26 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2025-06-26</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added permissions to &lt;code class="code"&gt;AmazonEKSServiceRolePolicy&lt;/code&gt; and &lt;code class="code"&gt;AmazonEKSComputePolicy&lt;/code&gt; to allow Amazon EKS Auto Mode to launch instances by using the EC2 On-Demand Capacity Reservations in your account. Also, added the permissions to &lt;code class="code"&gt;AmazonEKSComputePolicy&lt;/code&gt; for Amazon EKS to create the EC2 Spot service-linked role on your behalf.</description>
         <pubDate>Fri, 20 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2025-06-20</guid>
      </item>
      <item>
         <title>Managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added &lt;code class="code"&gt;AmazonEKSDashboardConsoleReadOnly&lt;/code&gt; policy.</description>
         <pubDate>Thu, 19 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Managed_policy_updates_2025-06-19</guid>
      </item>
      <item>
         <title>Amazon EKS Auto Mode update to NodeClass</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/create-node-class.html#auto-node-class-spec</link>
         <description>The &lt;code class="code"&gt;NodeClass&lt;/code&gt; template for Auto Mode nodes added configuration for separate pod subnets. This adds the optional keys &lt;code class="code"&gt;podSubnetSelectorTerms&lt;/code&gt; and &lt;code class="code"&gt;podSecurityGroupSelectorTerms&lt;/code&gt; to set the subnets and security groups for the pods.</description>
         <pubDate>Fri, 13 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_Auto_Mode_update_to_NodeClass_2025-06-13</guid>
      </item>
      <item>
         <title>Target secondary and cross-account roles with EKS Pod Identities</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/pod-id-assign-target-role.html</link>
         <description>Amazon EKS adds &lt;em&gt;target IAM roles&lt;/em&gt; to EKS Pod Identities for automated role chaining. You can use this to automatically assume a role in another account and EKS Pod Identity rotates the temporary credentials. Each Pod Identity association must have an IAM role in the same account to assume first, then it uses that role to assume the target role.</description>
         <pubDate>Wed, 11 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Target_secondary_and_cross-account_roles_with_EKS_Pod_Identities_2025-06-11</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. There arenâ€™t any new patch versions of Kubernetes in these platform version.</description>
         <pubDate>Wed, 11 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2025-06-11</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Asia Pacific (Taipei) (&lt;code class="code"&gt;ap-east-2&lt;/code&gt;) AWS Region.</description>
         <pubDate>Fri, 6 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2025-06-06</guid>
      </item>
      <item>
         <title>IPv6 access control for dual-stack public endpoints for new IPv6 clusters</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html</link>
         <description>Amazon EKS adds &lt;code class="code"&gt;IPv6&lt;/code&gt; CIDR blocks to control access to the public cluster endpoint for new &lt;code class="code"&gt;IPv6&lt;/code&gt; clusters. Previously, you could only add &lt;code class="code"&gt;IPv4&lt;/code&gt; CIDR blocks to allow traffic to the public cluster endpoint, even for dual-stack cluster endpoints.</description>
         <pubDate>Thu, 5 Jun 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#IPv6_access_control_for_dual-stack_public_endpoints_for_new_IPv6_clusters_2025-06-05</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. This includes new patch versions of Kubernetes &lt;code class="code"&gt;1.32.5&lt;/code&gt;, &lt;code class="code"&gt;1.31.9&lt;/code&gt;, and &lt;code class="code"&gt;1.30.13&lt;/code&gt;.</description>
         <pubDate>Fri, 30 May 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2025-05-30</guid>
      </item>
      <item>
         <title>New cluster insights for EKS Hybrid Nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-insights.html</link>
         <description>Amazon EKS adds new cluster insights that check the configuration of your hybrid nodes. These insight checks will warn you about issues with on-premises nodes and pods and the remote network configuration of the cluster.</description>
         <pubDate>Thu, 29 May 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_cluster_insights_for_EKS_Hybrid_Nodes_2025-05-29</guid>
      </item>
      <item>
         <title>Kubernetes version 1.33</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions-standard.html#kubernetes-1-33</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.33&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Thu, 29 May 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.33_2025-05-29</guid>
      </item>
      <item>
         <title>Add-on support for Amazon FSx CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fsx-csi.html</link>
         <description>You can now use the AWS Management Console, AWS CLI, and API to manage the Amazon FSx CSI driver.</description>
         <pubDate>Fri, 23 May 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Add-on_support_for_Amazon_FSx_CSI_driver_2025-05-23</guid>
      </item>
      <item>
         <title>Edit Prometheus scrapers in the console</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/prometheus.html#viewing-prometheus-scraper-details</link>
         <description>You can now edit Amazon Managed Service for Prometheus scrapers in the Amazon EKS console.</description>
         <pubDate>Thu, 22 May 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Edit_Prometheus_scrapers_in_the_console_2025-05-22</guid>
      </item>
      <item>
         <title>Managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added &lt;code class="code"&gt;AmazonEKSDashboardServiceRolePolicy&lt;/code&gt; policy.</description>
         <pubDate>Wed, 21 May 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Managed_policy_updates_2025-05-21</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. There arenâ€™t any new patch versions of Kubernetes in these platform versions.</description>
         <pubDate>Fri, 16 May 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2025-05-16</guid>
      </item>
      <item>
         <title>New pages for Amazon FSx for Lustre performance</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fsx-csi.html</link>
         <description>Added new topics with details on optimizing Amazon FSx for Lustre performance.</description>
         <pubDate>Fri, 2 May 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_pages_for_Amazon_FSx_for_Lustre_performance_2025-05-02</guid>
      </item>
      <item>
         <title>Amazon EKS Auto Mode update to NodeClass</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/create-node-class.html#auto-node-class-spec</link>
         <description>The &lt;code class="code"&gt;NodeClass&lt;/code&gt; template for Auto Mode nodes added configuration for forward network proxies. This adds the optional key &lt;code class="code"&gt;advancedNetworking&lt;/code&gt; to set your HTTPS proxy.</description>
         <pubDate>Wed, 30 Apr 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_Auto_Mode_update_to_NodeClass_2025-04-30</guid>
      </item>
      <item>
         <title>Bottlerocket for hybrid nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-bottlerocket.html</link>
         <description>Bottlerocket is now available for EKS Hybrid Nodes.</description>
         <pubDate>Tue, 29 Apr 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Bottlerocket_for_hybrid_nodes_2025-04-29</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. There arenâ€™t any new patch versions of Kubernetes in these platform versions.</description>
         <pubDate>Tue, 29 Apr 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2025-04-29</guid>
      </item>
      <item>
         <title>New concepts pages for hybrid networking</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-concepts.html</link>
         <description>Added pages for concepts of EKS Hybrid Nodes. These cover the on-premises and cloud networking in detail with diagrams.</description>
         <pubDate>Fri, 18 Apr 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_concepts_pages_for_hybrid_networking_2025-04-18</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added permissions to &lt;code class="code"&gt;AmazonEKSClusterPolicy&lt;/code&gt; to allow Amazon EKS to elastic network interfaces created by the VPC CNI. This is required so that EKS can clean up elastic network interfaces that are left behind if the VPC CNI quits unexpectedly.</description>
         <pubDate>Wed, 16 Apr 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2025-04-16</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Added permissions to &lt;code class="code"&gt;AmazonEKSServiceRolePolicy&lt;/code&gt; to allow EKS AI/ML customers to add Egress rules to the default EKS Cluster security group.</description>
         <pubDate>Mon, 14 Apr 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2025-04-14</guid>
      </item>
      <item>
         <title>Node health for EKS Hybrid Nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/node-health.html</link>
         <description>You can use &lt;code class="code"&gt;eks-node-monitoring-agent&lt;/code&gt; on hybrid nodes, starting from version &lt;code class="code"&gt;1.2.0-eksbuild.1&lt;/code&gt;. Run &lt;code class="code"&gt;eks-node-monitoring-agent&lt;/code&gt; as an Amazon EKS add-on to detect and show health issues.</description>
         <pubDate>Mon, 31 Mar 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Node_health_for_EKS_Hybrid_Nodes_2025-03-31</guid>
      </item>
      <item>
         <title>EKS Hybrid Nodes for existing clusters</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-update.html</link>
         <description>You can now add, change, or remove the hybrid nodes configuration of existing clusters. Previously, you could only add the hybrid nodes configuration to new clusters when you created them.
With Amazon EKS Hybrid Nodes, you can use your on-premises and edge infrastructure as nodes in Amazon EKS clusters. AWS manages the AWS-hosted Kubernetes control plane of the Amazon EKS cluster, and you manage the hybrid nodes that run in your on-premises or edge environments.</description>
         <pubDate>Mon, 31 Mar 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#EKS_Hybrid_Nodes_for_existing_clusters_2025-03-31</guid>
      </item>
      <item>
         <title>Rollback: Prevent accidental upgrades with cluster insights</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html#update-cluster-control-plane</link>
         <description>Amazon EKS has temporarily rolled back a feature that would
require you to use a &lt;code class="code"&gt;--force&lt;/code&gt; flag to upgrade your cluster when there were certain cluster insight issues. For more information, see &lt;a href="https://github.com/aws/containers-roadmap/issues/2570" rel="noopener noreferrer" target="_blank"&gt;Temporary rollback of enforcing upgrade insights on update cluster version&lt;/a&gt; on GitHub.</description>
         <pubDate>Fri, 28 Mar 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Rollback:_Prevent_accidental_upgrades_with_cluster_insights_2025-03-28</guid>
      </item>
      <item>
         <title>Bottlerocket FIPS AMIs</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/bottlerocket-fips-amis.html</link>
         <description>Bottlerocket FIPS AMIs are now available in standard managed node groups.</description>
         <pubDate>Thu, 27 Mar 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Bottlerocket_FIPS_AMIs_2025-03-27</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added permissions to &lt;code class="code"&gt;AmazonEKSServiceRolePolicy&lt;/code&gt; to allow Amazon EKS to terminate EC2 instances created by Auto Mode.
Added permissions to &lt;code class="code"&gt;AmazonEKSServiceRolePolicy&lt;/code&gt; to allow Amazon EKS to terminate EC2 instances created by Auto Mode.</description>
         <pubDate>Fri, 28 Feb 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2025-02-28</guid>
      </item>
      <item>
         <title>Update strategies for managed node groups</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/managed-node-update-behavior.html#managed-node-update-upgrade</link>
         <description>You can now use update strategies to configure the version update process for managed node groups. This introduces the &lt;em&gt;minimal&lt;/em&gt; update strategy to terminate nodes before making new ones, which is useful in capacity constrained environments. The &lt;em&gt;default&lt;/em&gt; update strategy continues the existing behavior.</description>
         <pubDate>Mon, 27 Jan 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Update_strategies_for_managed_node_groups_2025-01-27</guid>
      </item>
      <item>
         <title>Kubernetes version 1.32</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-1-32</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.32&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Thu, 23 Jan 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.32_2025-01-23</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Asia Pacific (Thailand) Region (&lt;code class="code"&gt;ap-southeast-7&lt;/code&gt;) and Mexico (Central) (&lt;code class="code"&gt;mx-central-1&lt;/code&gt;) AWS Regions. EKS Auto Mode and VPC Endpoints for the EKS API arenâ€™t available in either Region.</description>
         <pubDate>Tue, 14 Jan 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2025-01-14</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added multiple permissions to &lt;code class="code"&gt;AmazonEBSCSIDriverPolicy&lt;/code&gt; to allow the Amazon EBS CSI Driver restore all snapshots, enable Fast Snapshot Restore (FSR) on EBS volumes, and modify tags on volumes.</description>
         <pubDate>Mon, 13 Jan 2025 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2025-01-13</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added permissions to &lt;code class="code"&gt;AmazonEKSLoadBalancingPolicy&lt;/code&gt;.</description>
         <pubDate>Thu, 26 Dec 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-12-26</guid>
      </item>
      <item>
         <title>Updated cluster insights</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-insights.html</link>
         <description>Amazon EKS upgrade insights will now warn about more cluster health and version compatibility issues. It can detect issues between different Kubernetes and Amazon EKS components such as &lt;code class="code"&gt;kubelet&lt;/code&gt;, &lt;code class="code"&gt;kube-proxy&lt;/code&gt;, and Amazon EKS add-ons.</description>
         <pubDate>Fri, 20 Dec 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Updated_cluster_insights_2024-12-20</guid>
      </item>
      <item>
         <title>Node monitoring agent and auto repair</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/node-health.html</link>
         <description>You can use the new &lt;code class="code"&gt;eks-node-monitoring-agent&lt;/code&gt; as an Amazon EKS add-on to detect and show health issues. You can also enable node auto repair to automatically replace nodes when issues are detected.</description>
         <pubDate>Mon, 16 Dec 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Node_monitoring_agent_and_auto_repair_2024-12-16</guid>
      </item>
      <item>
         <title>Amazon EKS Hybrid Nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-overview.html</link>
         <description>You can now run node on-premises connected to Amazon EKS clusters. With Amazon EKS Hybrid Nodes, you can use your on-premises and edge infrastructure as nodes in Amazon EKS clusters. AWS manages the AWS-hosted Kubernetes control plane of the Amazon EKS cluster, and you manage the hybrid nodes that run in your on-premises or edge environments.</description>
         <pubDate>Sun, 1 Dec 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_Hybrid_Nodes_2024-12-01</guid>
      </item>
      <item>
         <title>Amazon EKS Auto Mode</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/automode.html</link>
         <description>Amazon EKS Auto Mode fully automates Kubernetes cluster infrastructure management for compute, storage, and networking on AWS. It simplifies Kubernetes management by automatically provisioning infrastructure, selecting optimal compute instances, dynamically scaling resources, continuously optimizing costs, patching operating systems, and integrating with AWS security services.</description>
         <pubDate>Sun, 1 Dec 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_Auto_Mode_2024-12-01</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. This includes new patch versions of Kubernetes &lt;code class="code"&gt;1.31.2&lt;/code&gt;, &lt;code class="code"&gt;1.30.6&lt;/code&gt;, &lt;code class="code"&gt;1.29.10&lt;/code&gt;, and &lt;code class="code"&gt;1.28.15&lt;/code&gt;.</description>
         <pubDate>Fri, 22 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2024-11-22</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Updated &lt;code class="code"&gt;AWSServiceRoleForAmazonEKSNodegroup&lt;/code&gt; for compatibility with China regions.</description>
         <pubDate>Fri, 22 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-11-22</guid>
      </item>
      <item>
         <title>Kubernetes version 1.30 is now available for local clusters on AWS Outposts</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-platform-versions.html</link>
         <description>You can now create an Amazon EKS local cluster on an AWS Outposts using Kubernetes version 1.30.</description>
         <pubDate>Thu, 21 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.30_is_now_available_for_local_clusters_on_AWS_Outposts_2024-11-21</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>EKS updated AWS managed policy &lt;code class="code"&gt;AmazonEKSLocalOutpostClusterPolicy&lt;/code&gt;. Added &lt;code class="code"&gt;ec2:DescribeAvailabilityZones&lt;/code&gt; permission so the AWS Cloud Controller Manager on the cluster control plane can identify the Availability Zone that each node is in.</description>
         <pubDate>Thu, 21 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-11-21</guid>
      </item>
      <item>
         <title>Bottlerocket AMIs that use FIPS 140-3</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/retrieve-ami-id-bottlerocket.html</link>
         <description>Bottlerocket AMIs are available that are preconfigured to use FIPS 140-3 validated cryptographic modules. This includes the Amazon Linux 2023 Kernel Crypto API Cryptographic Module and the AWS-LC Cryptographic Module.</description>
         <pubDate>Wed, 20 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Bottlerocket_AMIs_that_use_FIPS_140-3_2024-11-20</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Updated &lt;code class="code"&gt;AWSServiceRoleForAmazonEKSNodegroup&lt;/code&gt; policy to allow &lt;code class="code"&gt;ec2:RebootInstances&lt;/code&gt; for instances created by Amazon EKS managed node groups. Restricted the &lt;code class="code"&gt;ec2:CreateTags&lt;/code&gt; permissions for Amazon EC2 resources.</description>
         <pubDate>Wed, 20 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-11-20</guid>
      </item>
      <item>
         <title>Observability dashboard</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/observability-dashboard.html</link>
         <description>The observability dashboard helps you to quickly detect, troubleshoot, and remediate issues. There are also new &lt;a href="https://docs.aws.amazon.com/eks/latest/userguide/cloudwatch.html"&gt;CloudWatch vended metrics&lt;/a&gt; available in the &lt;code class="code"&gt;AWS/EKS&lt;/code&gt; namespace.</description>
         <pubDate>Mon, 18 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Observability_dashboard_2024-11-18</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>EKS updated AWS managed policy &lt;code class="code"&gt;AmazonEKSServiceRolePolicy&lt;/code&gt;. Added permissions for EKS access policies, load balancer management, and automated cluster resource cleanup.</description>
         <pubDate>Sat, 16 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-11-16</guid>
      </item>
      <item>
         <title>New role creation in console for add-ons that support EKS Pod Identities</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/creating-an-add-on.html#_create_add_on_console</link>
         <description>There are new steps when using the console to create or update add-ons that support EKS Pod Identities where you can automatically generate IAM roles with the appropriate name, role policy, and trust policy for the add-on.</description>
         <pubDate>Fri, 15 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_role_creation_in_console_for_add-ons_that_support_EKS_Pod_Identities_2024-11-15</guid>
      </item>
      <item>
         <title>Managed node groups in AWS Local Zones</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/local-zones.html</link>
         <description>Managed node groups can now be created in AWS Local Zones.</description>
         <pubDate>Fri, 15 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Managed_node_groups_in_AWS_Local_Zones_2024-11-15</guid>
      </item>
      <item>
         <title>New metrics are available</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/view-raw-metrics.html</link>
         <description>There are new metrics available under the API group &lt;code class="code"&gt;metrics.eks.amazonaws.com&lt;/code&gt;.</description>
         <pubDate>Mon, 11 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_metrics_are_available_2024-11-11</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>EKS updated AWS managed policy &lt;code class="code"&gt;AmazonEKSComputePolicy&lt;/code&gt;. Updated resource permissions for the &lt;code class="code"&gt;iam:AddRoleToInstanceProfile&lt;/code&gt; action.</description>
         <pubDate>Thu, 7 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-11-07</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>EKS added a new AWS managed policy: &lt;code class="code"&gt;AmazonEKSComputePolicy&lt;/code&gt;
            </description>
         <pubDate>Fri, 1 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-11-01</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added permissions to &lt;code class="code"&gt;AmazonEKSClusterPolicy&lt;/code&gt;. Added &lt;code class="code"&gt;ec2:DescribeInstanceTopology&lt;/code&gt; permission to allow Amazon EKS to attach topology information to the node as labels.</description>
         <pubDate>Fri, 1 Nov 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-11-01</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>EKS added a new AWS managed policy: &lt;code class="code"&gt;AmazonEKSBlockStoragePolicy&lt;/code&gt;
            </description>
         <pubDate>Wed, 30 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-10-30</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>EKS added a new AWS managed policy: &lt;code class="code"&gt;AmazonEKSLoadBalancingPolicy&lt;/code&gt;
            </description>
         <pubDate>Wed, 30 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-10-30</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added &lt;code class="code"&gt;cloudwatch:PutMetricData&lt;/code&gt; permissions to &lt;code class="code"&gt;AmazonEKSServiceRolePolicy&lt;/code&gt; to allow Amazon EKS to publish metrics to Amazon CloudWatch.</description>
         <pubDate>Tue, 29 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-10-29</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>EKS added a new AWS managed policy: &lt;code class="code"&gt;AmazonEKSNetworkingPolicy&lt;/code&gt;
            </description>
         <pubDate>Mon, 28 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-10-28</guid>
      </item>
      <item>
         <title>Dual-stack endpoints for new IPv6 clusters</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html</link>
         <description>Connect to new &lt;code class="code"&gt;IPv6&lt;/code&gt; clusters with a &lt;code class="code"&gt;eks-cluster.&lt;code class="replaceable"&gt;region&lt;/code&gt;.api.aws&lt;/code&gt; endpoint that is dual-stack. This endpoint is returned when you describe these clusters. &lt;code class="code"&gt;kubectl&lt;/code&gt; and other Kubernetes API clients in &lt;code class="code"&gt;IPv4&lt;/code&gt;, &lt;code class="code"&gt;IPv6&lt;/code&gt;, or dual-stack environments can resolve and connect to these endpoints for public or private clusters.</description>
         <pubDate>Mon, 21 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Dual-stack_endpoints_for_new_IPv6_clusters_2024-10-21</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added &lt;code class="code"&gt;autoscaling:ResumeProcesses&lt;/code&gt;, &lt;code class="code"&gt;autoscaling:SuspendProcesses&lt;/code&gt;, and associated permissions to &lt;code class="code"&gt;AWSServiceRoleForAmazonEKSNodegroup&lt;/code&gt; in China regions to integrate with Amazon Application Recovery Controller for EKS. No changes to other regions.</description>
         <pubDate>Mon, 21 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-10-21</guid>
      </item>
      <item>
         <title>AL2023 accelerated AMIs</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/retrieve-ami-id.html</link>
         <description>You can now use accelerated &lt;code class="code"&gt;NVIDIA&lt;/code&gt; and AWS Neuron instances for AMIs based on AL2023.</description>
         <pubDate>Fri, 11 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AL2023_accelerated_AMIs_2024-10-11</guid>
      </item>
      <item>
         <title>New source format</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>We have switched over to a new source format with some layout changes. There are temporary minor formatting issues that we are addressing.</description>
         <pubDate>Thu, 10 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_source_format_2024-10-10</guid>
      </item>
      <item>
         <title>AWS managed policy updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>Added permissions to &lt;code class="code"&gt;AmazonEKSServicePolicy&lt;/code&gt; and &lt;code class="code"&gt;AmazonEKSServiceRolePolicy&lt;/code&gt;. Added &lt;code class="code"&gt;ec2:GetSecurityGroupsForVpc&lt;/code&gt; and associated tag permissions to allow EKS to read security group information and update related tags.</description>
         <pubDate>Thu, 10 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_2024-10-10</guid>
      </item>
      <item>
         <title>AWS managed policy updates - New policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>EKS added a new AWS managed policy.</description>
         <pubDate>Thu, 3 Oct 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_New_policy_2024-10-03</guid>
      </item>
      <item>
         <title>Kubernetes version 1.31</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-1-31</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.31&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 24 Sep 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.31_2024-09-24</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Wed, 21 Aug 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2024-08-21</guid>
      </item>
      <item>
         <title>Kubernetes version 1.29 is now available for local clusters on AWS Outposts</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-platform-versions.html</link>
         <description>You can now create an Amazon EKS local cluster on an AWS Outposts using Kubernetes version 1.29.</description>
         <pubDate>Tue, 20 Aug 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.29_is_now_available_for_local_clusters_on_AWS_Outposts_2024-08-20</guid>
      </item>
      <item>
         <title>EKS Pod Identity in AWS GovCloud (US)</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/pod-identites.html</link>
         <description>Amazon EKS Pod Identities associate an IAM role with a Kubernetes service account. With this feature, you no longer need to provide extended permissions to the node IAM role. This way, Pods on that node can call AWS APIs. Unlike IAM roles for service accounts, EKS Pod Identities are completely inside EKS; you donâ€™t need an OIDC identity provider.</description>
         <pubDate>Wed, 14 Aug 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#EKS_Pod_Identity_in_AWS_GovCloud_(US)_2024-08-14</guid>
      </item>
      <item>
         <title>Scenario-driven content updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>We renamed and updated topics to be more scenario-driven throughout the entire guide.</description>
         <pubDate>Fri, 9 Aug 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Scenario-driven_content_updates_2024-08-09</guid>
      </item>
      <item>
         <title>Dual-stack VPC interface endpoints for Amazon EKS</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/vpc-interface-endpoints.html</link>
         <description>You can now create dual-stack VPC interface endpoints for Amazon EKS with both &lt;code class="code"&gt;IPv4&lt;/code&gt; and &lt;code class="code"&gt;IPv6&lt;/code&gt; IP addresses and DNS names.</description>
         <pubDate>Wed, 7 Aug 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Dual-stack_VPC_interface_endpoints_for_Amazon_EKS_2024-08-07</guid>
      </item>
      <item>
         <title>New dual-stack endpoints for the Amazon EKS APIs with IPv6 addresses</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html</link>
         <description>The EKS API for creating and managing clusters, and the OIDC issuer URLs for clusters have new dual-stack endpoints. The new DNS name for the Amazon EKS API is &lt;code class="code"&gt;eks.&lt;code class="replaceable"&gt;region&lt;/code&gt;.api.aws&lt;/code&gt; which resolves to &lt;code class="code"&gt;IPv4&lt;/code&gt; addresses and &lt;code class="code"&gt;IPv6&lt;/code&gt; addresses. New clusters have a new dual-stack OIDC issuer URL (&lt;code class="code"&gt;oidc-eks.&lt;code class="replaceable"&gt;region&lt;/code&gt;.api.aws&lt;/code&gt;).</description>
         <pubDate>Thu, 1 Aug 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_dual-stack_endpoints_for_the_Amazon_EKS_APIs_with_IPv6_addresses_2024-08-01</guid>
      </item>
      <item>
         <title>Capacity Blocks for managed node groups</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/capacity-blocks-mng.html</link>
         <description>You can now use Capacity Blocks for managed node groups.</description>
         <pubDate>Mon, 1 Jul 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Capacity_Blocks_for_managed_node_groups_2024-07-01</guid>
      </item>
      <item>
         <title>Auto Scaling Group metrics collection enabled by default</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/enable-asg-metrics.html</link>
         <description>Amazon EKS managed node groups now have Amazon EC2 Auto Scaling group metrics enabled by default with no additional charge. Previously, you had to do several steps to enable this feature.</description>
         <pubDate>Fri, 28 Jun 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Auto_Scaling_Group_metrics_collection_enabled_by_default_2024-06-28</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Thu, 27 Jun 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2024-06-27</guid>
      </item>
      <item>
         <title>Kubernetes version 1.26</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html</link>
         <description>Kubernetes version &lt;code class="code"&gt;1.26&lt;/code&gt; is now in extended support.</description>
         <pubDate>Wed, 12 Jun 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.26_2024-06-12</guid>
      </item>
      <item>
         <title>Improvements to AMI information references</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-amis.html</link>
         <description>We made improvements to the AMI information references, in particular for Bottlerocket.</description>
         <pubDate>Wed, 12 Jun 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Improvements_to_AMI_information_references_2024-06-12</guid>
      </item>
      <item>
         <title>Kubernetes version 1.30</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-1-30</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.30&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Thu, 23 May 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.30_2024-05-23</guid>
      </item>
      <item>
         <title>CoreDNS Autoscaling</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/coredns-autoscaling.html</link>
         <description>CoreDNS autoscaler will dynamically adapt the number of replicas of the CoreDNS deployment in an EKS cluster based on the number of nodes and CPU cores. This feature works for CoreDNS &lt;code class="code"&gt;v1.9&lt;/code&gt; and the latest platform version of EKS release version &lt;code class="code"&gt;1.25&lt;/code&gt; and later.</description>
         <pubDate>Tue, 14 May 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#CoreDNS_Autoscaling_2024-05-14</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. This includes new patch versions of Kubernetes &lt;code class="code"&gt;1.29.4&lt;/code&gt;, &lt;code class="code"&gt;1.28.9&lt;/code&gt;, and &lt;code class="code"&gt;1.27.13&lt;/code&gt;.</description>
         <pubDate>Tue, 14 May 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2024-05-14</guid>
      </item>
      <item>
         <title>CloudWatch Container Insights support for Windows</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cloudwatch.html</link>
         <description>The Amazon CloudWatch Observability Operator add-on now also allows Container Insights on Windows worker nodes in the cluster.</description>
         <pubDate>Wed, 10 Apr 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#CloudWatch_Container_Insights_support_for_Windows_2024-04-10</guid>
      </item>
      <item>
         <title>Kubernetes concepts</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-concepts.html</link>
         <description>Added new Kubernetes concepts topic.</description>
         <pubDate>Fri, 5 Apr 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_concepts_2024-04-05</guid>
      </item>
      <item>
         <title>Restructure Access and IAM Content</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-auth.html</link>
         <description>Move existing pages related to access and IAM topics, such as auth config map, access entries, Pod ID, and IRSA into new section. Revise overview content.</description>
         <pubDate>Tue, 2 Apr 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Restructure_Access_and_IAM_Content_2024-04-02</guid>
      </item>
      <item>
         <title>Bottlerocket OS support for Amazon S3 CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/s3-csi.html</link>
         <description>The Mountpoint for Amazon S3 CSI driver is now compatible with Bottlerocket.</description>
         <pubDate>Wed, 13 Mar 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Bottlerocket_OS_support_for_Amazon_S3_CSI_driver_2024-03-13</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Mon, 4 Mar 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2024-03-04</guid>
      </item>
      <item>
         <title>Amazon Linux 2023</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/al2023.html</link>
         <description>Amazon Linux 2023 (AL2023) is a new Linux-based operating system designed to provide a secure, stable, and high-performance environment for your cloud applications.</description>
         <pubDate>Thu, 29 Feb 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_Linux_2023_2024-02-29</guid>
      </item>
      <item>
         <title>EKS Pod Identity and IRSA support sidecars in Kubernetes 1.29</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-1-29</link>
         <description>In Kubernetes &lt;code class="code"&gt;1.29&lt;/code&gt;, sidecar containers are available in Amazon EKS clusters. Sidecar containers are supported with IAM roles for service accounts or EKS Pod Identity. For more information about sidecars, see &lt;a href="https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/" rel="noopener noreferrer" target="_blank"&gt;Sidecar Containers&lt;/a&gt; in the Kubernetes documentation.</description>
         <pubDate>Mon, 26 Feb 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#EKS_Pod_Identity_and_IRSA_support_sidecars_in_Kubernetes_1.29_2024-02-26</guid>
      </item>
      <item>
         <title>Kubernetes version 1.29</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-1-29</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.29&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 23 Jan 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.29_2024-01-23</guid>
      </item>
      <item>
         <title>Full release: Amazon EKS Extended Support for Kubernetes versions</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html</link>
         <description>Extended Kubernetes version support allows you to stay at a specific Kubernetes version for longer than 14 months.</description>
         <pubDate>Tue, 16 Jan 2024 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Full_release:_Amazon_EKS_Extended_Support_for_Kubernetes_versions_2024-01-16</guid>
      </item>
      <item>
         <title>Amazon EKS cluster health detection in the AWS Cloud</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html#cluster-health-status</link>
         <description>Amazon EKS detects issues with your Amazon EKS clusters and the infrastructure of the cluster prerequisites in &lt;em&gt;cluster health&lt;/em&gt;. You can view the issues with your EKS clusters in the AWS Management Console and in the &lt;code class="code"&gt;health&lt;/code&gt; of the cluster in the EKS API. These issues are in addition to the issues that are detected by and displayed by the console. Previously, cluster health was only available for local clusters on AWS Outposts.</description>
         <pubDate>Thu, 28 Dec 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_cluster_health_detection_in_the_AWS_Cloud_2023-12-28</guid>
      </item>
      <item>
         <title>Cluster insights</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-insights.html</link>
         <description>You can now get recommendations on your cluster based on recurring checks.</description>
         <pubDate>Wed, 20 Dec 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Cluster_insights_2023-12-20</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Canada West (Calgary) (&lt;code class="code"&gt;ca-west-1&lt;/code&gt;) AWS Region.</description>
         <pubDate>Wed, 20 Dec 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2023-12-20</guid>
      </item>
      <item>
         <title>You can now grant IAM roles and users access to your cluster using access entries</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html</link>
         <description>Before the introduction of access entries, you granted IAM roles and users access to your cluster by adding entries to the &lt;code class="code"&gt;aws-auth&lt;/code&gt;
               &lt;code class="code"&gt;ConfigMap&lt;/code&gt;. Now each cluster has an access mode, and you can switch to using access entries on your schedule. After you switch modes, you can add users by adding access entries in the AWS CLI, AWS CloudFormation, and the AWS SDKs.</description>
         <pubDate>Mon, 18 Dec 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#You_can_now_grant_IAM_roles_and_users_access_to_your_cluster_using_access_entries_2023-12-18</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. This includes new patch versions of Kubernetes &lt;code class="code"&gt;1.28.4&lt;/code&gt;, &lt;code class="code"&gt;1.27.8&lt;/code&gt;, &lt;code class="code"&gt;1.26.11&lt;/code&gt;, and &lt;code class="code"&gt;1.25.16&lt;/code&gt;.</description>
         <pubDate>Tue, 12 Dec 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2023-12-12</guid>
      </item>
      <item>
         <title>Mountpoint for Amazon S3 CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/s3-csi.html</link>
         <description>You can now install the Mountpoint for Amazon S3 CSI driver on Amazon EKS clusters.</description>
         <pubDate>Mon, 27 Nov 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Mountpoint_for_Amazon_S3_CSI_driver_2023-11-27</guid>
      </item>
      <item>
         <title>Turn on Prometheus metrics when creating a cluster</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/prometheus.html</link>
         <description>In the AWS Management Console, you can now turn on Prometheus metrics when creating a cluster. You can also view Prometheus scraper details in the &lt;strong&gt;Observability&lt;/strong&gt; tab.</description>
         <pubDate>Sun, 26 Nov 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Turn_on_Prometheus_metrics_when_creating_a_cluster_2023-11-26</guid>
      </item>
      <item>
         <title>Amazon EKS Pod Identities</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/pod-identites.html</link>
         <description>Amazon EKS Pod Identities associate an IAM role with a Kubernetes service account. With this feature, you no longer need to provide extended permissions to the node IAM role. This way, Pods on that node can call AWS APIs. Unlike IAM roles for service accounts, EKS Pod Identities are completely inside EKS; you donâ€™t need an OIDC identity provider.</description>
         <pubDate>Sun, 26 Nov 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_Pod_Identities_2023-11-26</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Sun, 26 Nov 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2023-11-26</guid>
      </item>
      <item>
         <title>CSI snapshot controller</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/csi-snapshot-controller.html</link>
         <description>You can now install the CSI snapshot controller for use with compatible CSI drivers, such as the Amazon EBS CSI driver.</description>
         <pubDate>Fri, 17 Nov 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#CSI_snapshot_controller_2023-11-17</guid>
      </item>
      <item>
         <title>ADOT Operator topic rewrite</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/opentelemetry.html</link>
         <description>The Amazon EKS add-on support for ADOT Operator section was redundant with the AWS Distro for OpenTelemetry documentation. We migrated remaining essential information to that resource to reduce outdated and inconsistent information.</description>
         <pubDate>Tue, 14 Nov 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#ADOT_Operator_topic_rewrite_2023-11-14</guid>
      </item>
      <item>
         <title>CoreDNS EKS add-on support for Prometheus metrics</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/managing-coredns.html</link>
         <description>The &lt;code class="code"&gt;v1.10.1-eksbuild.5&lt;/code&gt;, &lt;code class="code"&gt;v1.9.3-eksbuild.9&lt;/code&gt;, and &lt;code class="code"&gt;v1.8.7-eksbuild.8&lt;/code&gt; versions of the EKS add-on for CoreDNS expose the port that CoreDNS published metrics to, in the &lt;code class="code"&gt;kube-dns&lt;/code&gt; service. This makes it easier to include the CoreDNS metrics in your monitoring systems.</description>
         <pubDate>Fri, 10 Nov 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#CoreDNS_EKS_add-on_support_for_Prometheus_metrics_2023-11-10</guid>
      </item>
      <item>
         <title>Amazon EKS CloudWatch Observability Operator add-on</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cloudwatch.html</link>
         <description>Added Amazon EKS CloudWatch Observability Operator page.</description>
         <pubDate>Mon, 6 Nov 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_CloudWatch_Observability_Operator_add-on_2023-11-06</guid>
      </item>
      <item>
         <title>Capacity Blocks for self-managed P5 instances in US East (Ohio)</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/capacity-blocks.html</link>
         <description>In US East (Ohio), you can now use Capacity Blocks for self-managed P5 instances.</description>
         <pubDate>Tue, 31 Oct 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Capacity_Blocks_for_self-managed_P5_instances_in_US_East_(Ohio)_2023-10-31</guid>
      </item>
      <item>
         <title>Clusters support modifying subnets and security groups</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html</link>
         <description>You can update the cluster to change which subnets and security groups the cluster uses. You can update from the AWS Management Console, the latest version of the AWS CLI, AWS CloudFormation, and &lt;code class="code"&gt;eksctl&lt;/code&gt; version &lt;code class="code"&gt;v0.164.0-rc.0&lt;/code&gt; or later. You might need to do this to provide subnets with more available IP addresses to successfully upgrade a cluster version.</description>
         <pubDate>Tue, 24 Oct 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Clusters_support_modifying_subnets_and_security_groups_2023-10-24</guid>
      </item>
      <item>
         <title>Cluster role and managed node group role supports customer managed AWS Identity and Access Management policies</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-iam-role.html</link>
         <description>You can use a custom IAM policy on the cluster role, instead of the &lt;a href="https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSClusterPolicy.html"&gt;AmazonEKSClusterPolicy&lt;/a&gt;
               AWS managed policy. Also, you can use a custom IAM policy on the node role in a managed node group, instead of the &lt;a href="https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSWorkerNodePolicy.html"&gt;AmazonEKSWorkerNodePolicy&lt;/a&gt;
               AWS managed policy. Do this to create a policy with the least privilege to meet strict compliance requirements.</description>
         <pubDate>Mon, 23 Oct 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Cluster_role_and_managed_node_group_role_supports_customer_managed_AWS_Identity_and_Access_Management_policies_2023-10-23</guid>
      </item>
      <item>
         <title>Fix link to eksctl installation</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Fix install link for eksctl after the page was moved.</description>
         <pubDate>Fri, 6 Oct 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Fix_link_to_eksctl_installation_2023-10-06</guid>
      </item>
      <item>
         <title>Preview release: Amazon EKS Extended Support for Kubernetes versions</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html</link>
         <description>Extended Kubernetes version support allows you to stay at a specific Kubernetes version for longer than 14 months.</description>
         <pubDate>Wed, 4 Oct 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Preview_release:_Amazon_EKS_Extended_Support_for_Kubernetes_versions_2023-10-04</guid>
      </item>
      <item>
         <title>Remove references to AWS App Mesh integration</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS integrations with AWS App Mesh remain for existing customers of App Mesh only.</description>
         <pubDate>Fri, 29 Sep 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Remove_references_to_AWS_App_Mesh_integration_2023-09-29</guid>
      </item>
      <item>
         <title>Kubernetes version 1.28</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-1-28</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.28&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 26 Sep 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.28_2023-09-26</guid>
      </item>
      <item>
         <title>Existing clusters support Kubernetes network policy enforcement in the Amazon VPC CNI plugin for Kubernetes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cni-network-policy.html</link>
         <description>You can use Kubernetes &lt;em&gt;network policy&lt;/em&gt; in existing clusters with the Amazon VPC CNI plugin for Kubernetes, instead of requiring a third party solution.
You can use Kubernetes &lt;em&gt;network policy&lt;/em&gt; in existing clusters with the Amazon VPC CNI plugin for Kubernetes, instead of requiring a third party solution.</description>
         <pubDate>Fri, 15 Sep 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Existing_clusters_support_Kubernetes_network_policy_enforcement_in_the_Amazon_VPC_CNI_plugin_for_Kubernetes_2023-09-15</guid>
      </item>
      <item>
         <title>CoreDNS Amazon EKS add-on supports modifying PDB</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/managing-coredns.html</link>
         <description>You can modify the &lt;code class="code"&gt;PodDisruptionBudget&lt;/code&gt; of the EKS add-on for CoreDNS in versions &lt;code class="code"&gt;v1.9.3-eksbuild.7&lt;/code&gt; and later and &lt;code class="code"&gt;v1.10.1-eksbuild.4&lt;/code&gt; and later.</description>
         <pubDate>Fri, 15 Sep 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#CoreDNS_Amazon_EKS_add-on_supports_modifying_PDB_2023-09-15</guid>
      </item>
      <item>
         <title>Amazon EKS support for shared subnets</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html#network-requirements-shared</link>
         <description>New &lt;a href="https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html#network-requirements-shared"&gt;Shared subnet requirements and considerations&lt;/a&gt; for making Amazon EKS clusters in shared subnets.</description>
         <pubDate>Thu, 7 Sep 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_support_for_shared_subnets_2023-09-07</guid>
      </item>
      <item>
         <title>Updates to What is Amazon EKS?</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html</link>
         <description>Added new &lt;a href="https://docs.aws.amazon.com/eks/latest/userguide/common-use-cases.html"&gt;Common use cases&lt;/a&gt; and &lt;a href="https://docs.aws.amazon.com/eks/latest/userguide/eks-architecture.html"&gt;Architecture&lt;/a&gt; topics. Refreshed other topics.</description>
         <pubDate>Wed, 6 Sep 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Updates_to_What_is_Amazon_EKS?_2023-09-06</guid>
      </item>
      <item>
         <title>Kubernetes network policy enforcement in the Amazon VPC CNI plugin for Kubernetes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cni-network-policy.html</link>
         <description>You can use Kubernetes &lt;em&gt;network policy&lt;/em&gt; with the Amazon VPC CNI plugin for Kubernetes, instead of requiring a third party solution.
You can use Kubernetes &lt;em&gt;network policy&lt;/em&gt; with the Amazon VPC CNI plugin for Kubernetes, instead of requiring a third party solution.</description>
         <pubDate>Tue, 29 Aug 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_network_policy_enforcement_in_the_Amazon_VPC_CNI_plugin_for_Kubernetes_2023-08-29</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Israel (Tel Aviv) (&lt;code class="code"&gt;il-central-1&lt;/code&gt;) AWS Region.</description>
         <pubDate>Tue, 1 Aug 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2023-08-01</guid>
      </item>
      <item>
         <title>Configurable ephemeral storage for Fargate</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fargate-pod-configuration.html#fargate-storage</link>
         <description>You can increase the total amount of ephemeral storage for each Pod running on Amazon EKS Fargate.</description>
         <pubDate>Mon, 31 Jul 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Configurable_ephemeral_storage_for_Fargate_2023-07-31</guid>
      </item>
      <item>
         <title>Add-on support for Amazon EFS CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html#add-ons-aws-efs-csi-driver</link>
         <description>You can now use the AWS Management Console, AWS CLI, and API to manage the Amazon EFS CSI driver.</description>
         <pubDate>Wed, 26 Jul 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Add-on_support_for_Amazon_EFS_CSI_driver_2023-07-26</guid>
      </item>
      <item>
         <title>AWS managed policy updates - New policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS added a new AWS managed policy.</description>
         <pubDate>Wed, 26 Jul 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_New_policy_2023-07-26</guid>
      </item>
      <item>
         <title>Kubernetes version updates for 1.27, 1.26, 1.25, and 1.24 are now available for local clusters on AWS Outposts</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-platform-versions.html</link>
         <description>Kubernetes version updates to 1.27.3, 1.26.6, 1.25.11, and 1.24.15 are now available for local clusters on AWS Outposts</description>
         <pubDate>Thu, 20 Jul 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_updates_for_1.27,_1.26,_1.25,_and_1.24_are_now_available_for_local_clusters_on_AWS_Outposts_2023-07-20</guid>
      </item>
      <item>
         <title>IP prefixes support for Windows nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html</link>
         <description>Assigning IP prefixes to your nodes can enable you to host a significantly higher number of Pods on your nodes than you can when assigning individual secondary IP addresses to your nodes.</description>
         <pubDate>Thu, 6 Jul 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#IP_prefixes_support_for_Windows_nodes_2023-07-06</guid>
      </item>
      <item>
         <title>Amazon FSx for OpenZFS CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fsx-openzfs-csi.html</link>
         <description>You can now install the Amazon FSx for OpenZFS CSI driver on Amazon EKS clusters.</description>
         <pubDate>Fri, 30 Jun 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_FSx_for_OpenZFS_CSI_driver_2023-06-30</guid>
      </item>
      <item>
         <title>Pods on Linux nodes in IPv4 clusters can now communicate with IPv6 endpoints.</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cni-ipv6-egress.html</link>
         <description>After assigning an IPv6 address to your node, your Pods' &lt;code class="code"&gt;IPv4&lt;/code&gt; address is network address translated to the &lt;code class="code"&gt;IPv6&lt;/code&gt; address of the node that itâ€™s running on.</description>
         <pubDate>Mon, 19 Jun 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Pods_on_Linux_nodes_in_IPv4_clusters_can_now_communicate_with_IPv6_endpoints._2023-06-19</guid>
      </item>
      <item>
         <title>Windows managed node groups in AWS GovCloud (US) Regions</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/create-managed-node-group.html</link>
         <description>In the AWS GovCloud (US) Regions, Amazon EKS managed node groups can now run Windows containers.</description>
         <pubDate>Tue, 30 May 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Windows_managed_node_groups_in_AWS_GovCloud_(US)_Regions_2023-05-30</guid>
      </item>
      <item>
         <title>Kubernetes version 1.27</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-1-27</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.27&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Wed, 24 May 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.27_2023-05-24</guid>
      </item>
      <item>
         <title>Kubernetes version 1.26</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.26&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 11 Apr 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.26_2023-04-11</guid>
      </item>
      <item>
         <title>Domainless gMSA</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-windows-ami.html#ad-and-gmsa-support</link>
         <description>You can now use domainless gMSA with Windows Pods.</description>
         <pubDate>Mon, 27 Mar 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Domainless_gMSA_2023-03-27</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Asia Pacific (Melbourne) (&lt;code class="code"&gt;ap-southeast-4&lt;/code&gt;) AWS Region.</description>
         <pubDate>Fri, 10 Mar 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2023-03-10</guid>
      </item>
      <item>
         <title>Amazon File Cache CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/file-cache-csi.html</link>
         <description>You can now install the Amazon File Cache CSI driver on Amazon EKS clusters.</description>
         <pubDate>Fri, 3 Mar 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_File_Cache_CSI_driver_2023-03-03</guid>
      </item>
      <item>
         <title>Kubernetes version 1.25 is now available for local clusters on AWS Outposts</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-local-cluster-create.html</link>
         <description>You can now create an Amazon EKS local cluster on an Outpost using Kubernetes versions &lt;code class="code"&gt;1.22&lt;/code&gt; â€“ &lt;code class="code"&gt;1.25&lt;/code&gt;.</description>
         <pubDate>Wed, 1 Mar 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.25_is_now_available_for_local_clusters_on_AWS_Outposts_2023-03-01</guid>
      </item>
      <item>
         <title>Kubernetes version 1.25</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.25&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Wed, 22 Feb 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.25_2023-02-22</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Tue, 7 Feb 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2023-02-07</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Asia Pacific (Hyderabad) (&lt;code class="code"&gt;ap-south-2&lt;/code&gt;), Europe (Zurich) (&lt;code class="code"&gt;eu-central-2&lt;/code&gt;), and Europe (Spain) (&lt;code class="code"&gt;eu-south-2&lt;/code&gt;) AWS Regions.</description>
         <pubDate>Mon, 6 Feb 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2023-02-06</guid>
      </item>
      <item>
         <title>Kubernetes versions 1.21 â€“ 1.24 are now available for local clusters on AWS Outposts.</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-local-cluster-create.html</link>
         <description>You can now create an Amazon EKS local cluster on an Outpost using Kubernetes versions &lt;code class="code"&gt;1.21&lt;/code&gt; â€“ &lt;code class="code"&gt;1.24&lt;/code&gt;. Previously, only version &lt;code class="code"&gt;1.21&lt;/code&gt; was available.</description>
         <pubDate>Tue, 17 Jan 2023 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_versions_1.21_â€“_1.24_are_now_available_for_local_clusters_on_AWS_Outposts._2023-01-17</guid>
      </item>
      <item>
         <title>Amazon EKS now supports AWS PrivateLink</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/vpc-interface-endpoints.html</link>
         <description>You can use an AWS PrivateLink to create a private connection between your VPC and Amazon EKS.</description>
         <pubDate>Fri, 16 Dec 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_now_supports_AWS_PrivateLink_2022-12-16</guid>
      </item>
      <item>
         <title>Managed node group Windows support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html</link>
         <description>You can now use Windows for Amazon EKS managed node groups.</description>
         <pubDate>Thu, 15 Dec 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Managed_node_group_Windows_support_2022-12-15</guid>
      </item>
      <item>
         <title>Amazon EKS add-ons from independent software vendors are now available in the AWS Marketplace</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html</link>
         <description>You can now browse and subscribe to Amazon EKS add-ons from independent software vendors through the AWS Marketplace.</description>
         <pubDate>Mon, 28 Nov 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_add-ons_from_independent_software_vendors_are_now_available_in_the_AWS_Marketplace_2022-11-28</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Thu, 17 Nov 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2022-11-17</guid>
      </item>
      <item>
         <title>Kubernetes version 1.24</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.24&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 15 Nov 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.24_2022-11-15</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Middle East (UAE) (&lt;code class="code"&gt;me-central-1&lt;/code&gt;) AWS Region.</description>
         <pubDate>Thu, 3 Nov 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2022-11-03</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Mon, 24 Oct 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2022-10-24</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Thu, 20 Oct 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2022-10-20</guid>
      </item>
      <item>
         <title>Local clusters on AWS Outposts are now available</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-local-cluster-create.html</link>
         <description>You can now create an Amazon EKS local cluster on an Outpost.</description>
         <pubDate>Mon, 19 Sep 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Local_clusters_on_AWS_Outposts_are_now_available_2022-09-19</guid>
      </item>
      <item>
         <title>Fargate vCPU based quotas</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/service-quotas.html#service-quotas-eks-fargate</link>
         <description>Fargate is transitioning from Pod based quotas to vCPU based quotas.</description>
         <pubDate>Thu, 8 Sep 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Fargate_vCPU_based_quotas_2022-09-08</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Wed, 31 Aug 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2022-08-31</guid>
      </item>
      <item>
         <title>Cost monitoring</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cost-monitoring</link>
         <description>Amazon EKS now supports Kubecost, which enables you to monitor costs broken down by Kubernetes resources including Pods, nodes, namespaces, and labels.</description>
         <pubDate>Wed, 24 Aug 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Cost_monitoring_2022-08-24</guid>
      </item>
      <item>
         <title>AWS managed policy updates - New policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS added a new AWS managed policy.</description>
         <pubDate>Wed, 24 Aug 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_New_policy_2022-08-24</guid>
      </item>
      <item>
         <title>AWS managed policy updates - New policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS added a new AWS managed policy.</description>
         <pubDate>Tue, 23 Aug 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_New_policy_2022-08-23</guid>
      </item>
      <item>
         <title>Tag resources for billing</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html#tag-resources-for-billing</link>
         <description>Added &lt;code class="code"&gt;aws:eks:cluster-name&lt;/code&gt; generated cost allocation tag support for all clusters.</description>
         <pubDate>Tue, 16 Aug 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Tag_resources_for_billing_2022-08-16</guid>
      </item>
      <item>
         <title>Fargate profile wildcards</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html#fargate-profile-wildcards</link>
         <description>Added support for Fargate profile wildcards in the selector criteria for namespaces, label keys, and label values.</description>
         <pubDate>Tue, 16 Aug 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Fargate_profile_wildcards_2022-08-16</guid>
      </item>
      <item>
         <title>Kubernetes version 1.23</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.23&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Thu, 11 Aug 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.23_2022-08-11</guid>
      </item>
      <item>
         <title>View Kubernetes resources in the AWS Management Console</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/view-kubernetes-resources.html</link>
         <description>You can now view information about the Kubernetes resources deployed to your cluster using the AWS Management Console.</description>
         <pubDate>Tue, 3 May 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#View_Kubernetes_resources_in_the_AWS_Management_Console_2022-05-03</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Asia Pacific (Jakarta) (&lt;code class="code"&gt;ap-southeast-3&lt;/code&gt;) AWS Region.</description>
         <pubDate>Mon, 2 May 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2022-05-02</guid>
      </item>
      <item>
         <title>Observability page and ADOT add-on support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-observe.html</link>
         <description>Added Observability page and AWS Distro for OpenTelemetry (ADOT).</description>
         <pubDate>Thu, 21 Apr 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Observability_page_and_ADOT_add-on_support_2022-04-21</guid>
      </item>
      <item>
         <title>Kubernetes version 1.22</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.22&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Mon, 4 Apr 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.22_2022-04-04</guid>
      </item>
      <item>
         <title>AWS managed policy updates - New policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS added a new AWS managed policy.</description>
         <pubDate>Mon, 4 Apr 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_New_policy_2022-04-04</guid>
      </item>
      <item>
         <title>Added Fargate Pod patching details</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fargate-pod-patching.html</link>
         <description>When upgrading Fargate Pods, Amazon EKS first tries to evict Pods based on your Pod disruption budgets. You can create event rules to react to failed evictions before the Pods are deleted.</description>
         <pubDate>Fri, 1 Apr 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_Fargate_Pod_patching_details_2022-04-01</guid>
      </item>
      <item>
         <title>Full release: Add-on support for Amazon EBS CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html</link>
         <description>You can now use the AWS Management Console, AWS CLI, and API to manage the Amazon EBS CSI driver.</description>
         <pubDate>Thu, 31 Mar 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Full_release:_Add-on_support_for_Amazon_EBS_CSI_driver_2022-03-31</guid>
      </item>
      <item>
         <title>AWS Outposts content update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/outposts.html</link>
         <description>Instructions to deploy an Amazon EKS cluster on AWS Outposts.</description>
         <pubDate>Tue, 22 Mar 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_Outposts_content_update_2022-03-22</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Mon, 21 Mar 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2022-03-21</guid>
      </item>
      <item>
         <title>Windows containerd support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-windows-ami.html.html</link>
         <description>You can now select the &lt;code class="code"&gt;containerd&lt;/code&gt; runtime for Windows nodes.</description>
         <pubDate>Mon, 14 Mar 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Windows_containerd_support_2022-03-14</guid>
      </item>
      <item>
         <title>Added Amazon EKS Connector considerations to security documentation</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/connector-considerations.html</link>
         <description>Describes the shared responsibility model as it relates to connected clusters.</description>
         <pubDate>Fri, 25 Feb 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_Amazon_EKS_Connector_considerations_to_security_documentation_2022-02-25</guid>
      </item>
      <item>
         <title>Assign IPv6 addresses to your Pods and services</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cni-ipv6.html</link>
         <description>You can now create a &lt;code class="code"&gt;1.21&lt;/code&gt; or later cluster that assigns &lt;code class="code"&gt;IPv6&lt;/code&gt; addresses to your Pods and services.</description>
         <pubDate>Thu, 6 Jan 2022 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Assign_IPv6_addresses_to_your_Pods_and_services_2022-01-06</guid>
      </item>
      <item>
         <title>AWS managed policy updates - Update to an existing policy</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html#security-iam-awsmanpol-updates</link>
         <description>Amazon EKS updated an existing AWS managed policy.</description>
         <pubDate>Mon, 13 Dec 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_managed_policy_updates_-_Update_to_an_existing_policy_2021-12-13</guid>
      </item>
      <item>
         <title>Preview release: Add-on support for Amazon EBS CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html</link>
         <description>You can now preview using the AWS Management Console, AWS CLI, and API to manage the Amazon EBS CSI driver.</description>
         <pubDate>Thu, 9 Dec 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Preview_release:_Add-on_support_for_Amazon_EBS_CSI_driver_2021-12-09</guid>
      </item>
      <item>
         <title>Karpenter autoscaler support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html#karpenter</link>
         <description>You can now use the Karpenter open-source project to autoscale your nodes.</description>
         <pubDate>Mon, 29 Nov 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Karpenter_autoscaler_support_2021-11-29</guid>
      </item>
      <item>
         <title>Fluent Bit Kubernetes filter support in Fargate logging</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fargate-logging.html#fargate-logging-kubernetes-filter</link>
         <description>You can now use the Fluent Bit Kubernetes filter with Fargate logging.</description>
         <pubDate>Wed, 10 Nov 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Fluent_Bit_Kubernetes_filter_support_in_Fargate_logging_2021-11-10</guid>
      </item>
      <item>
         <title>Windows support available in the control plane</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/windows-support.html</link>
         <description>Windows support is now available in your control plane. You no longer need to enable it in your data plane.</description>
         <pubDate>Tue, 9 Nov 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Windows_support_available_in_the_control_plane_2021-11-09</guid>
      </item>
      <item>
         <title>Bottlerocket added as an AMI type for managed node groups</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami-bottlerocket.html</link>
         <description>Previously, Bottlerocket was only available as a self-managed node option. Now it can be configured as a managed node group, reducing the effort thatâ€™s required to meet node compliance requirements.</description>
         <pubDate>Thu, 28 Oct 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Bottlerocket_added_as_an_AMI_type_for_managed_node_groups_2021-10-28</guid>
      </item>
      <item>
         <title>DL1 driver support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-ami-build-scripts.html</link>
         <description>Custom Amazon Linux AMIs now support deep learning workloads for Amazon Linux 2. This enablement allows a generic on-premises or cloud baseline configuration.</description>
         <pubDate>Mon, 25 Oct 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#DL1_driver_support_2021-10-25</guid>
      </item>
      <item>
         <title>VT1 video support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-ami-build-scripts.html</link>
         <description>Custom Amazon Linux AMIs now support VT1 for some distributions. This enablement advertises Xilinx U30 devices on your Amazon EKS cluster.</description>
         <pubDate>Mon, 13 Sep 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#VT1_video_support_2021-09-13</guid>
      </item>
      <item>
         <title>Amazon EKS Connector is now available</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-connector.html</link>
         <description>You can use Amazon EKS Connector to register and connect any conformant Kubernetes cluster to AWS and visualize it in the Amazon EKS console.</description>
         <pubDate>Wed, 8 Sep 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_Connector_is_now_available_2021-09-08</guid>
      </item>
      <item>
         <title>Amazon EKS Anywhere is now available</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-deployment-options.html</link>
         <description>Amazon EKS Anywhere is a new deployment option for Amazon EKS that you can use to create and operate Kubernetes clusters on-premises.</description>
         <pubDate>Wed, 8 Sep 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_Anywhere_is_now_available_2021-09-08</guid>
      </item>
      <item>
         <title>Amazon FSx for NetApp ONTAP CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fsx-ontap.html</link>
         <description>Added topic that summarizes the Amazon FSx for NetApp ONTAP CSI driver and gives links to other references.</description>
         <pubDate>Thu, 2 Sep 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_FSx_for_NetApp_ONTAP_CSI_driver_2021-09-02</guid>
      </item>
      <item>
         <title>Managed node groups now auto-calculates the Amazon EKS recommended maximum Pods for nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html</link>
         <description>Managed node groups now auto-calculate the Amazon EKS maximum Pods for nodes that you deploy without a launch template, or with a launch template that you havenâ€™t specified an AMI ID in.</description>
         <pubDate>Mon, 30 Aug 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Managed_node_groups_now_auto-calculates_the_Amazon_EKS_recommended_maximum_Pods_for_nodes_2021-08-30</guid>
      </item>
      <item>
         <title>Remove Amazon EKS management of add-on settings without removing the Amazon EKS add-on software</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html#removing-vpc-cni-eks-add-on</link>
         <description>You can now remove an Amazon EKS add-on without removing the add-on software from your cluster.</description>
         <pubDate>Fri, 20 Aug 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Remove_Amazon_EKS_management_of_add-on_settings_without_removing_the_Amazon_EKS_add-on_software_2021-08-20</guid>
      </item>
      <item>
         <title>Create multi-homed Pods using Multus</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/pod-multiple-network-interfaces.html</link>
         <description>You can now add multiple network interfaces to a Pod using Multus.</description>
         <pubDate>Mon, 2 Aug 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Create_multi-homed_Pods_using_Multus_2021-08-02</guid>
      </item>
      <item>
         <title>Add more IP addresses to your Linux Amazon EC2 nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html</link>
         <description>You can now add significantly more IP addresses to your Linux Amazon EC2 nodes. This means that you can run a higher density of Pods on each node.
You can now add significantly more IP addresses to your Linux Amazon EC2 nodes. This means that you can run a higher density of Pods on each node.</description>
         <pubDate>Tue, 27 Jul 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Add_more_IP_addresses_to_your_Linux_Amazon_EC2_nodes_2021-07-27</guid>
      </item>
      <item>
         <title>containerd runtime bootstrap</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>The Amazon EKS optimized accelerated Amazon Linux Amazon Machine Image (AMI) now contains a bootstrap flag that you can use to enable the &lt;code class="code"&gt;containerd&lt;/code&gt; runtime in Amazon EKS optimized and Bottlerocket AMIs. This flag is available in all supported Kubernetes versions of the AMI.</description>
         <pubDate>Mon, 19 Jul 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#containerd_runtime_bootstrap_2021-07-19</guid>
      </item>
      <item>
         <title>Kubernetes version 1.21</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.21&lt;/code&gt; support.</description>
         <pubDate>Mon, 19 Jul 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.21_2021-07-19</guid>
      </item>
      <item>
         <title>Added managed policies topic</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-iam-awsmanpol.html</link>
         <description>A list of all Amazon EKS IAM managed policies and changes that were made to them since June 17, 2021.</description>
         <pubDate>Thu, 17 Jun 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_managed_policies_topic_2021-06-17</guid>
      </item>
      <item>
         <title>Use security groups for Pods with Fargate</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-groups-for-pods.html</link>
         <description>You can now use security groups for Pods with Fargate, in addition to using them with Amazon EC2 nodes.</description>
         <pubDate>Tue, 1 Jun 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Use_security_groups_for_Pods_with_Fargate_2021-06-01</guid>
      </item>
      <item>
         <title>Added CoreDNS and kube-proxy Amazon EKS add-ons</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html</link>
         <description>Amazon EKS can now help you manage the CoreDNS and &lt;code class="code"&gt;kube-proxy&lt;/code&gt; Amazon EKS add-ons for your cluster.</description>
         <pubDate>Wed, 19 May 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_CoreDNS_and_kube-proxy_Amazon_EKS_add-ons_2021-05-19</guid>
      </item>
      <item>
         <title>Kubernetes version 1.20</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.20&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 18 May 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.20_2021-05-18</guid>
      </item>
      <item>
         <title>AWS Load Balancer Controller 2.2.0 released</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html</link>
         <description>You can now use the AWS Load Balancer Controller to create Elastic Load Balancers using instance or IP targets.</description>
         <pubDate>Fri, 14 May 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_Load_Balancer_Controller_2.2.0_released_2021-05-14</guid>
      </item>
      <item>
         <title>Node taints for managed node groups</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/node-taints-managed-node-groups.html</link>
         <description>Amazon EKS now supports adding note taints to managed node groups.</description>
         <pubDate>Tue, 11 May 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Node_taints_for_managed_node_groups_2021-05-11</guid>
      </item>
      <item>
         <title>Secrets encryption for existing clusters</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html#enable-kms</link>
         <description>Amazon EKS now supports adding &lt;a href="https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/" rel="noopener noreferrer" target="_blank"&gt;secrets encryption&lt;/a&gt; to existing clusters.</description>
         <pubDate>Fri, 26 Feb 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Secrets_encryption_for_existing_clusters_2021-02-26</guid>
      </item>
      <item>
         <title>Kubernetes version 1.19</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.19&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 16 Feb 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.19_2021-02-16</guid>
      </item>
      <item>
         <title>Amazon EKS now supports OpenID Connect (OIDC) identity providers as a method to authenticate users to a version 1.16 or later cluster.</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/authenticate-oidc-identity-provider.html</link>
         <description>OIDC identity providers can be used with, or as an alternative to AWS Identity and Access Management (IAM).</description>
         <pubDate>Fri, 12 Feb 2021 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_now_supports_OpenID_Connect_(OIDC)_identity_providers_as_a_method_to_authenticate_users_to_a_version_1.16_or_later_cluster._2021-02-12</guid>
      </item>
      <item>
         <title>View node and workload resources in the AWS Management Console</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/view-kubernetes-resources.html</link>
         <description>You can now view details about your managed, self-managed, and Fargate nodes and your deployed Kubernetes workloads in the AWS Management Console.</description>
         <pubDate>Tue, 1 Dec 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#View_node_and_workload_resources_in_the_AWS_Management_Console_2020-12-01</guid>
      </item>
      <item>
         <title>Deploy Spot Instance types in a managed node group</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html#managed-node-group-capacity-types</link>
         <description>You can now deploy multiple Spot or On-Demand Instance types to a managed node group.</description>
         <pubDate>Tue, 1 Dec 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Deploy_Spot_Instance_types_in_a_managed_node_group_2020-12-01</guid>
      </item>
      <item>
         <title>Amazon EKS can now manage specific add-ons for your cluster</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html</link>
         <description>You can manage add-ons yourself, or allow Amazon EKS to control the launch and version of an add-on through the Amazon EKS API.</description>
         <pubDate>Tue, 1 Dec 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_can_now_manage_specific_add-ons_for_your_cluster_2020-12-01</guid>
      </item>
      <item>
         <title>Share an ALB across multiple Ingresses</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html</link>
         <description>You can now share an AWS Application Load Balancer (ALB) across multiple Kubernetes Ingresses. In the past, you had to deploy a separate ALB for each Ingress.</description>
         <pubDate>Fri, 23 Oct 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Share_an_ALB_across_multiple_Ingresses_2020-10-23</guid>
      </item>
      <item>
         <title>NLB IP target support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/networkg-load-balancing.html#network-load-balancer</link>
         <description>You can now deploy a Network Load Balancer with IP targets. This means that you can use an NLB to load balance network traffic to Fargate Pods and directly to Pods that are running on Amazon EC2 nodes.</description>
         <pubDate>Fri, 23 Oct 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#NLB_IP_target_support_2020-10-23</guid>
      </item>
      <item>
         <title>Kubernetes version 1.18</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.18&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 13 Oct 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.18_2020-10-13</guid>
      </item>
      <item>
         <title>Specify a custom CIDR block for Kubernetes service IP address assignment.</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html</link>
         <description>You can now specify a custom CIDR block that Kubernetes assigns service IP addresses from.</description>
         <pubDate>Tue, 29 Sep 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Specify_a_custom_CIDR_block_for_Kubernetes_service_IP_address_assignment._2020-09-29</guid>
      </item>
      <item>
         <title>Assign security groups to individual Pods</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/security-groups-for-pods.html</link>
         <description>You can now associate different security groups to some of the individual Pods that are running on many Amazon EC2 instance types.</description>
         <pubDate>Wed, 9 Sep 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Assign_security_groups_to_individual_Pods_2020-09-09</guid>
      </item>
      <item>
         <title>Deploy Bottlerocket on your nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/launch-node-bottlerocket.html</link>
         <description>You can now deploy nodes that are running &lt;a href="https://aws.amazon.com/bottlerocket/" rel="noopener noreferrer" target="_blank"&gt;Bottlerocket&lt;/a&gt;.</description>
         <pubDate>Mon, 31 Aug 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Deploy_Bottlerocket_on_your_nodes_2020-08-31</guid>
      </item>
      <item>
         <title>The ability to launch Arm nodes is generally available</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html#arm-ami</link>
         <description>You can now launch Arm nodes in managed and self-managed node groups.</description>
         <pubDate>Mon, 17 Aug 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#The_ability_to_launch_Arm_nodes_is_generally_available_2020-08-17</guid>
      </item>
      <item>
         <title>Managed node group launch templates and custom AMI</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html</link>
         <description>You can now deploy a managed node group that uses an Amazon EC2 launch template. The launch template can specify a custom AMI, if you choose.</description>
         <pubDate>Mon, 17 Aug 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Managed_node_group_launch_templates_and_custom_AMI_2020-08-17</guid>
      </item>
      <item>
         <title>EFS support for AWS Fargate</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html</link>
         <description>You can now use Amazon EFS with AWS Fargate.</description>
         <pubDate>Mon, 17 Aug 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#EFS_support_for_AWS_Fargate_2020-08-17</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>This is a new platform version with security fixes and enhancements. This includes UDP support for services of type &lt;code class="code"&gt;LoadBalancer&lt;/code&gt; when using Network Load Balancers with Kubernetes version &lt;code class="code"&gt;1.15&lt;/code&gt; or later. For more information, see the &lt;a href="https://github.com/kubernetes/kubernetes/pull/92109" rel="noopener noreferrer" target="_blank"&gt;Allow UDP for AWS Network Load Balancer&lt;/a&gt; issue on GitHub.</description>
         <pubDate>Wed, 12 Aug 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2020-08-12</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Africa (Cape Town) (&lt;code class="code"&gt;af-south-1&lt;/code&gt;) and Europe (Milan) (&lt;code class="code"&gt;eu-south-1&lt;/code&gt;) AWS Regions.</description>
         <pubDate>Thu, 6 Aug 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2020-08-06</guid>
      </item>
      <item>
         <title>Fargate usage metrics</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/monitoring-fargate-usage.html</link>
         <description>
               AWS Fargate provides CloudWatch usage metrics that provide visibility into your accountâ€™s usage of Fargate On-Demand resources.</description>
         <pubDate>Mon, 3 Aug 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Fargate_usage_metrics_2020-08-03</guid>
      </item>
      <item>
         <title>Kubernetes version 1.17</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.17&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Fri, 10 Jul 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.17_2020-07-10</guid>
      </item>
      <item>
         <title>Create and manage App Mesh resources from within Kubernetes with the App Mesh controller for Kubernetes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/mesh-k8s-integration.html</link>
         <description>You can create and manage App Mesh resources from within Kubernetes. The controller also automatically injects the Envoy proxy and init containers into Pods that you deploy.</description>
         <pubDate>Thu, 18 Jun 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Create_and_manage_App_Mesh_resources_from_within_Kubernetes_with_the_App_Mesh_controller_for_Kubernetes_2020-06-18</guid>
      </item>
      <item>
         <title>Amazon EKS now supports Amazon EC2 Inf1 nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/inferentia-support.html</link>
         <description>You can add Amazon EC2 Inf1 nodes to your cluster.</description>
         <pubDate>Thu, 4 Jun 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_now_supports_Amazon_EC2_Inf1_nodes_2020-06-04</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the AWS GovCloud (US-East) (&lt;code class="code"&gt;us-gov-east-1&lt;/code&gt;) and AWS GovCloud (US-West) (&lt;code class="code"&gt;us-gov-west-1&lt;/code&gt;) AWS Regions.</description>
         <pubDate>Wed, 13 May 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2020-05-13</guid>
      </item>
      <item>
         <title>Kubernetes 1.12 is no longer supported on Amazon EKS</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html</link>
         <description>Kubernetes version &lt;code class="code"&gt;1.12&lt;/code&gt; is no longer supported on Amazon EKS. Update any &lt;code class="code"&gt;1.12&lt;/code&gt; clusters to version &lt;code class="code"&gt;1.13&lt;/code&gt; or later to avoid service interruption.</description>
         <pubDate>Tue, 12 May 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_1.12_is_no_longer_supported_on_Amazon_EKS_2020-05-12</guid>
      </item>
      <item>
         <title>Kubernetes version 1.16</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.16&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Thu, 30 Apr 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.16_2020-04-30</guid>
      </item>
      <item>
         <title>Added the AWSServiceRoleForAmazonEKS service-linked role</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/using-service-linked-roles-eks.html</link>
         <description>Added the &lt;strong&gt;AWSServiceRoleForAmazonEKS&lt;/strong&gt; service-linked role.</description>
         <pubDate>Thu, 16 Apr 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_the_AWSServiceRoleForAmazonEKS_service-linked_role_2020-04-16</guid>
      </item>
      <item>
         <title>Kubernetes version 1.15</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.15&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 10 Mar 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.15_2020-03-10</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Beijing (&lt;code class="code"&gt;cn-north-1&lt;/code&gt;) and Ningxia (&lt;code class="code"&gt;cn-northwest-1&lt;/code&gt;) AWS Regions.</description>
         <pubDate>Wed, 26 Feb 2020 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2020-02-26</guid>
      </item>
      <item>
         <title>FSx for Lustre CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fsx-csi.html</link>
         <description>Added topic for installing the FSx for Lustre CSI driver on Kubernetes &lt;code class="code"&gt;1.14&lt;/code&gt; Amazon EKS clusters.</description>
         <pubDate>Mon, 23 Dec 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#FSx_for_Lustre_CSI_driver_2019-12-23</guid>
      </item>
      <item>
         <title>Restrict network access to the public access endpoint of a cluster</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html</link>
         <description>With this update, you can use Amazon EKS to restrict the CIDR ranges that can communicate to the public access endpoint of the Kubernetes API server.</description>
         <pubDate>Fri, 20 Dec 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Restrict_network_access_to_the_public_access_endpoint_of_a_cluster_2019-12-20</guid>
      </item>
      <item>
         <title>Resolve the private access endpoint address for a cluster from outside of a VPC</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html</link>
         <description>With this update, you can use Amazon EKS to resolve the private access endpoint of the Kubernetes API server from outside of a VPC.</description>
         <pubDate>Fri, 13 Dec 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Resolve_the_private_access_endpoint_address_for_a_cluster_from_outside_of_a_VPC_2019-12-13</guid>
      </item>
      <item>
         <title>(Beta) Amazon EC2 A1 Amazon EC2 instance nodes</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/arm-support.html</link>
         <description>Launch &lt;a href="https://aws.amazon.com/ec2/instance-types/a1/" rel="noopener noreferrer" target="_blank"&gt;Amazon EC2 A1&lt;/a&gt; Amazon EC2 instance nodes that register with your Amazon EKS cluster.</description>
         <pubDate>Wed, 4 Dec 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#(Beta)_Amazon_EC2_A1_Amazon_EC2_instance_nodes_2019-12-04</guid>
      </item>
      <item>
         <title>Creating a cluster on AWS Outposts</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-on-outposts.html</link>
         <description>Amazon EKS now supports creating clusters on AWS Outposts.</description>
         <pubDate>Tue, 3 Dec 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Creating_a_cluster_on_AWS_Outposts_2019-12-03</guid>
      </item>
      <item>
         <title>AWS Fargate on Amazon EKS</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/fargate.html</link>
         <description>Amazon EKS Kubernetes clusters now support running Pods on Fargate.</description>
         <pubDate>Tue, 3 Dec 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_Fargate_on_Amazon_EKS_2019-12-03</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Canada (Central) (&lt;code class="code"&gt;ca-central-1&lt;/code&gt;) AWS Region.</description>
         <pubDate>Thu, 21 Nov 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2019-11-21</guid>
      </item>
      <item>
         <title>Managed node groups</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html</link>
         <description>Amazon EKS managed node groups automate the provisioning and lifecycle management of nodes (Amazon EC2 instances) for Amazon EKS Kubernetes clusters.</description>
         <pubDate>Mon, 18 Nov 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Managed_node_groups_2019-11-18</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>New platform versions to address &lt;a href="https://groups.google.com/forum/#!msg/kubernetes-security-announce/jk8polzSUxs/dfq6a-MnCQAJ" rel="noopener noreferrer" target="_blank"&gt;CVE-2019-11253&lt;/a&gt;.</description>
         <pubDate>Wed, 6 Nov 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2019-11-06</guid>
      </item>
      <item>
         <title>Kubernetes 1.11 is no longer supported on Amazon EKS</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html</link>
         <description>Kubernetes version &lt;code class="code"&gt;1.11&lt;/code&gt; is no longer supported on Amazon EKS. Please update any &lt;code class="code"&gt;1.11&lt;/code&gt; clusters to version &lt;code class="code"&gt;1.12&lt;/code&gt; or higher to avoid service interruption.</description>
         <pubDate>Mon, 4 Nov 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_1.11_is_no_longer_supported_on_Amazon_EKS_2019-11-04</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the South America (SÃ£o Paulo) (&lt;code class="code"&gt;sa-east-1&lt;/code&gt;) AWS Region.</description>
         <pubDate>Wed, 16 Oct 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2019-10-16</guid>
      </item>
      <item>
         <title>Windows support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/windows-support.html</link>
         <description>Amazon EKS clusters running Kubernetes version &lt;code class="code"&gt;1.14&lt;/code&gt; now support Windows workloads.</description>
         <pubDate>Mon, 7 Oct 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Windows_support_2019-10-07</guid>
      </item>
      <item>
         <title>Autoscaling</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html</link>
         <description>Added a chapter to cover some of the different types of Kubernetes autoscaling that are supported on Amazon EKS clusters.</description>
         <pubDate>Mon, 30 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Autoscaling_2019-09-30</guid>
      </item>
      <item>
         <title>Kubernetes Dashboard update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/dashboard-tutorial.html</link>
         <description>Updated topic for installing the Kubernetes Dashboard on Amazon EKS clusters to use the beta &lt;code class="code"&gt;2.0&lt;/code&gt; version.</description>
         <pubDate>Sat, 28 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_Dashboard_update_2019-09-28</guid>
      </item>
      <item>
         <title>Amazon EFS CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html</link>
         <description>Added topic for installing the Amazon EFS CSI driver on Kubernetes &lt;code class="code"&gt;1.14&lt;/code&gt; Amazon EKS clusters.</description>
         <pubDate>Thu, 19 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EFS_CSI_driver_2019-09-19</guid>
      </item>
      <item>
         <title>Amazon EC2 Systems Manager parameter for Amazon EKS optimized AMI ID</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/retrieve-ami-id.html</link>
         <description>Added topic for retrieving the Amazon EKS optimized AMI ID using an Amazon EC2 Systems Manager parameter. The parameter eliminates the need for you to look up AMI IDs.</description>
         <pubDate>Wed, 18 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EC2_Systems_Manager_parameter_for_Amazon_EKS_optimized_AMI_ID_2019-09-18</guid>
      </item>
      <item>
         <title>Amazon EKS resource tagging</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html</link>
         <description>You can manage the tagging of your Amazon EKS clusters.</description>
         <pubDate>Mon, 16 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_resource_tagging_2019-09-16</guid>
      </item>
      <item>
         <title>Amazon EBS CSI driver</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html</link>
         <description>Added topic for installing the Amazon EBS CSI driver on Kubernetes &lt;code class="code"&gt;1.14&lt;/code&gt; Amazon EKS clusters.</description>
         <pubDate>Mon, 9 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EBS_CSI_driver_2019-09-09</guid>
      </item>
      <item>
         <title>New Amazon EKS optimized AMI patched for CVE-2019-9512 and CVE-2019-9514</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Amazon EKS has updated the Amazon EKS optimized AMI to address &lt;a href="https://groups.google.com/forum/#!topic/kubernetes-security-announce/wlHLHit1BqA" rel="noopener noreferrer" target="_blank"&gt;CVE-2019-9512 and CVE-2019-9514&lt;/a&gt;.</description>
         <pubDate>Fri, 6 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_Amazon_EKS_optimized_AMI_patched_for_CVE-2019-9512_and_CVE-2019-9514_2019-09-06</guid>
      </item>
      <item>
         <title>Announcing deprecation of Kubernetes 1.11 in Amazon EKS</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html</link>
         <description>Amazon EKS discontinued support for Kubernetes version &lt;code class="code"&gt;1.11&lt;/code&gt; on November 4, 2019.</description>
         <pubDate>Wed, 4 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Announcing_deprecation_of_Kubernetes_1.11_in_Amazon_EKS_2019-09-04</guid>
      </item>
      <item>
         <title>Kubernetes version 1.14</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.14&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 3 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.14_2019-09-03</guid>
      </item>
      <item>
         <title>IAM roles for service accounts</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html</link>
         <description>With IAM roles for service accounts on Amazon EKS clusters, you can associate an IAM role with a Kubernetes service account. With this feature, you no longer need to provide extended permissions to the node IAM role. This way, Pods on that node can call AWS APIs.</description>
         <pubDate>Tue, 3 Sep 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#IAM_roles_for_service_accounts_2019-09-03</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Middle East (Bahrain) (&lt;code class="code"&gt;me-south-1&lt;/code&gt;) AWS Region.</description>
         <pubDate>Thu, 29 Aug 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2019-08-29</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>New platform versions to address &lt;a href="https://groups.google.com/forum/#!topic/kubernetes-security-announce/wlHLHit1BqA" rel="noopener noreferrer" target="_blank"&gt;CVE-2019-9512 and CVE-2019-9514&lt;/a&gt;.</description>
         <pubDate>Wed, 28 Aug 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2019-08-28</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>New platform versions to address &lt;a href="https://groups.google.com/forum/#!topic/kubernetes-security-announce/vUtEcSEY6SM" rel="noopener noreferrer" target="_blank"&gt;CVE-2019-11247 and CVE-2019-11249&lt;/a&gt;.</description>
         <pubDate>Mon, 5 Aug 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2019-08-05</guid>
      </item>
      <item>
         <title>Amazon EKS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Asia Pacific (Hong Kong) (&lt;code class="code"&gt;ap-east-1&lt;/code&gt;) AWS Region.</description>
         <pubDate>Wed, 31 Jul 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_Region_expansion_2019-07-31</guid>
      </item>
      <item>
         <title>Kubernetes 1.10 no longer supported on Amazon EKS</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html</link>
         <description>Kubernetes version &lt;code class="code"&gt;1.10&lt;/code&gt; is no longer supported on Amazon EKS. Update any &lt;code class="code"&gt;1.10&lt;/code&gt; clusters to version &lt;code class="code"&gt;1.11&lt;/code&gt; or higher to avoid service interruption.</description>
         <pubDate>Tue, 30 Jul 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_1.10_no_longer_supported_on_Amazon_EKS_2019-07-30</guid>
      </item>
      <item>
         <title>Added topic on ALB ingress controller</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html</link>
         <description>The AWS ALB Ingress Controller for Kubernetes is a controller that causes an ALB to be created when ingress resources are created.</description>
         <pubDate>Thu, 11 Jul 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_topic_on_ALB_ingress_controller_2019-07-11</guid>
      </item>
      <item>
         <title>New Amazon EKS optimized AMI</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Removing unnecessary &lt;code class="code"&gt;kubectl&lt;/code&gt; binary from AMIs.</description>
         <pubDate>Wed, 3 Jul 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_Amazon_EKS_optimized_AMI_2019-07-03</guid>
      </item>
      <item>
         <title>Kubernetes version 1.13</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.13&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Tue, 18 Jun 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.13_2019-06-18</guid>
      </item>
      <item>
         <title>New Amazon EKS optimized AMI patched for 
                  AWS-2019-005</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Amazon EKS has updated the Amazon EKS optimized AMI to address the vulnerabilities that are described in link:security/security-bulletins/AWS-2019-005/[AWS-2019-005,type="marketing"].</description>
         <pubDate>Mon, 17 Jun 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_Amazon_EKS_optimized_AMI_patched_for_
__________________AWS-2019-005_2019-06-17</guid>
      </item>
      <item>
         <title>Announcing discontinuation of support of Kubernetes 1.10 in Amazon EKS</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html</link>
         <description>Amazon EKS stopped supporting Kubernetes version &lt;code class="code"&gt;1.10&lt;/code&gt; on July 22, 2019.</description>
         <pubDate>Tue, 21 May 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Announcing_discontinuation_of_support_of_Kubernetes_1.10_in_Amazon_EKS_2019-05-21</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>New platform version for Kubernetes &lt;code class="code"&gt;1.11&lt;/code&gt; and &lt;code class="code"&gt;1.10&lt;/code&gt; clusters to support custom DNS names in the &lt;code class="code"&gt;kubelet&lt;/code&gt; certificate and improve &lt;code class="code"&gt;etcd&lt;/code&gt; performance.</description>
         <pubDate>Tue, 21 May 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2019-05-21</guid>
      </item>
      <item>
         <title>Getting started with eksctl</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html</link>
         <description>This getting started guide describes how you can install all of the required resources to get started with Amazon EKS using &lt;code class="code"&gt;eksctl&lt;/code&gt;. This is a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS.</description>
         <pubDate>Fri, 10 May 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Getting_started_with_eksctl_2019-05-10</guid>
      </item>
      <item>
         <title>AWS CLI get-token command</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>The &lt;code class="code"&gt;aws eks get-token&lt;/code&gt; command was added to the AWS CLI. You no longer need to install the AWS IAM Authenticator for Kubernetes to create client security tokens for cluster API server communication. Upgrade your AWS CLI installation to the latest version to use this new functionality. For more information, see &lt;a href="https://docs.aws.amazon.com/cli/latest/userguide/installing.html"&gt;Installing the AWS Command Line Interface&lt;/a&gt; in the &lt;em&gt;
                  AWS Command Line Interface User Guide&lt;/em&gt;.</description>
         <pubDate>Fri, 10 May 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#AWS_CLI_get-token_command_2019-05-10</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>New platform version for Kubernetes &lt;code class="code"&gt;1.12&lt;/code&gt; clusters to support custom DNS names in the &lt;code class="code"&gt;kubelet&lt;/code&gt; certificate and improve &lt;code class="code"&gt;etcd&lt;/code&gt; performance. This fixes a bug that caused node &lt;code class="code"&gt;kubelet&lt;/code&gt; daemons to request a new certificate every few seconds.</description>
         <pubDate>Wed, 8 May 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2019-05-08</guid>
      </item>
      <item>
         <title>Prometheus tutorial</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/prometheus.html</link>
         <description>Added topic for deploying Prometheus to your Amazon EKS cluster.</description>
         <pubDate>Fri, 5 Apr 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Prometheus_tutorial_2019-04-05</guid>
      </item>
      <item>
         <title>Amazon EKS control plane logging</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html</link>
         <description>With this update, you can get audit and diagnostic logs directly from the Amazon EKS control pane. You can use these CloudWatch logs in your account as reference for securing and running clusters.</description>
         <pubDate>Thu, 4 Apr 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_control_plane_logging_2019-04-04</guid>
      </item>
      <item>
         <title>Kubernetes version 1.12</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Added Kubernetes version &lt;code class="code"&gt;1.12&lt;/code&gt; support for new clusters and version upgrades.</description>
         <pubDate>Thu, 28 Mar 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Kubernetes_version_1.12_2019-03-28</guid>
      </item>
      <item>
         <title>Added App Mesh getting started guide</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/mesh-gs-k8s.html</link>
         <description>Added documentation for getting started with App Mesh and Kubernetes.</description>
         <pubDate>Wed, 27 Mar 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_App_Mesh_getting_started_guide_2019-03-27</guid>
      </item>
      <item>
         <title>Amazon EKS API server endpoint private access</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html</link>
         <description>Added documentation for disabling public access for your Amazon EKS clusterâ€™s Kubernetes API server endpoint.</description>
         <pubDate>Tue, 19 Mar 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_API_server_endpoint_private_access_2019-03-19</guid>
      </item>
      <item>
         <title>Added topic for installing the Kubernetes Metrics Server</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html</link>
         <description>The Kubernetes Metrics Server is an aggregator of resource usage data in your cluster.</description>
         <pubDate>Mon, 18 Mar 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_topic_for_installing_the_Kubernetes_Metrics_Server_2019-03-18</guid>
      </item>
      <item>
         <title>Added list of related open source projects</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html</link>
         <description>These open source projects extend the functionality of Kubernetes clusters running on AWS, including clusters that are managed by Amazon EKS.</description>
         <pubDate>Fri, 15 Mar 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_list_of_related_open_source_projects_2019-03-15</guid>
      </item>
      <item>
         <title>Added topic for installing Helm locally</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/helm.html</link>
         <description>The &lt;code class="code"&gt;helm&lt;/code&gt; package manager for Kubernetes helps you install and manage applications on your Kubernetes cluster. This topic shows how to install and run the &lt;code class="code"&gt;helm&lt;/code&gt; and &lt;code class="code"&gt;tiller&lt;/code&gt; binaries locally. That way, you can install and manage charts using the Helm CLI on your local system.</description>
         <pubDate>Mon, 11 Mar 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_topic_for_installing_Helm_locally_2019-03-11</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>New platform version that updates Amazon EKS Kubernetes &lt;code class="code"&gt;1.11&lt;/code&gt; clusters to patch level &lt;code class="code"&gt;1.11.8&lt;/code&gt; to address &lt;a href="https://discuss.kubernetes.io/t/kubernetes-security-announcement-v1-11-8-1-12-6-1-13-4-released-to-address-medium-severity-cve-2019-1002100/5147" rel="noopener noreferrer" target="_blank"&gt;CVE-2019-1002100&lt;/a&gt;.</description>
         <pubDate>Fri, 8 Mar 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2019-03-08</guid>
      </item>
      <item>
         <title>Increased cluster limit</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/service_limits.html</link>
         <description>Amazon EKS has increased the number of clusters that you can create in an AWS Region from 3 to 50.</description>
         <pubDate>Wed, 13 Feb 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Increased_cluster_limit_2019-02-13</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Europe (London) (&lt;code class="code"&gt;eu-west-2&lt;/code&gt;), Europe (Paris) (&lt;code class="code"&gt;eu-west-3&lt;/code&gt;), and Asia Pacific (Mumbai) (&lt;code class="code"&gt;ap-south-1&lt;/code&gt;) AWS Regions.</description>
         <pubDate>Wed, 13 Feb 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2019-02-13</guid>
      </item>
      <item>
         <title>New Amazon EKS optimized AMI patched for ALAS-2019-1156</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Amazon EKS has updated the Amazon EKS optimized AMI to address the vulnerability thatâ€™s described in &lt;a href="https://alas.aws.amazon.com/ALAS-2019-1156.html" rel="noopener noreferrer" target="_blank"&gt;ALAS-2019-1156&lt;/a&gt;.</description>
         <pubDate>Mon, 11 Feb 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_Amazon_EKS_optimized_AMI_patched_for_ALAS-2019-1156_2019-02-11</guid>
      </item>
      <item>
         <title>New Amazon EKS optimized AMI patched for ALAS2-2019-1141</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Amazon EKS has updated the Amazon EKS optimized AMI to address the CVEs that are referenced in &lt;a href="https://alas.aws.amazon.com/AL2/ALAS-2019-1141.html" rel="noopener noreferrer" target="_blank"&gt;ALAS2-2019-1141&lt;/a&gt;.</description>
         <pubDate>Wed, 9 Jan 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_Amazon_EKS_optimized_AMI_patched_for_ALAS2-2019-1141_2019-01-09</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Asia Pacific (Seoul) (&lt;code class="code"&gt;ap-northeast-2&lt;/code&gt;) AWS Region.</description>
         <pubDate>Wed, 9 Jan 2019 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2019-01-09</guid>
      </item>
      <item>
         <title>Amazon EKS region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the following additional AWS Regions: Europe (Frankfurt) (&lt;code class="code"&gt;eu-central-1&lt;/code&gt;), Asia Pacific (Tokyo) (&lt;code class="code"&gt;ap-northeast-1&lt;/code&gt;), Asia Pacific (Singapore) (&lt;code class="code"&gt;ap-southeast-1&lt;/code&gt;), and Asia Pacific (Sydney) (&lt;code class="code"&gt;ap-southeast-2&lt;/code&gt;).</description>
         <pubDate>Wed, 19 Dec 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_region_expansion_2018-12-19</guid>
      </item>
      <item>
         <title>Amazon EKS cluster updates</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html</link>
         <description>Added documentation for Amazon EKS &lt;a href="https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html"&gt;cluster Kubernetes version updates&lt;/a&gt; and &lt;a href="https://docs.aws.amazon.com/eks/latest/userguide/update-workers.html"&gt;node replacement&lt;/a&gt;.</description>
         <pubDate>Wed, 12 Dec 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_cluster_updates_2018-12-12</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Europe (Stockholm) (&lt;code class="code"&gt;eu-north-1&lt;/code&gt;) AWS Region.</description>
         <pubDate>Tue, 11 Dec 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2018-12-11</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>New platform version updating Kubernetes to patch level &lt;code class="code"&gt;1.10.11&lt;/code&gt; to address link:security/security-bulletins/AWS-2018-020/[CVE-2018-1002105,type="marketing"].</description>
         <pubDate>Tue, 4 Dec 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2018-12-04</guid>
      </item>
      <item>
         <title>Added version 1.0.0 support for the ALB ingress controller</title>
         <link>https://github.com/kubernetes-sigs/aws-alb-ingress-controller</link>
         <description>The ALB ingress controller releases version &lt;code class="code"&gt;1.0.0&lt;/code&gt; with formal support from AWS.</description>
         <pubDate>Tue, 20 Nov 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_version_1.0.0_support_for_the_ALB_ingress_controller_2018-11-20</guid>
      </item>
      <item>
         <title>Added support for CNI network configuration</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/cni-custom-network.html</link>
         <description>The Amazon VPC CNI plugin for Kubernetes version &lt;code class="code"&gt;1.2.1&lt;/code&gt; now supports custom network configuration for secondary Pod network interfaces.</description>
         <pubDate>Tue, 16 Oct 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_support_for_CNI_network_configuration_2018-10-16</guid>
      </item>
      <item>
         <title>Added support for MutatingAdmissionWebhook and ValidatingAdmissionWebhook</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>Amazon EKS platform version &lt;code class="code"&gt;1.10-eks.2&lt;/code&gt; now supports &lt;code class="code"&gt;MutatingAdmissionWebhook&lt;/code&gt; and &lt;code class="code"&gt;ValidatingAdmissionWebhook&lt;/code&gt; admission controllers.</description>
         <pubDate>Wed, 10 Oct 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_support_for_MutatingAdmissionWebhook_and_ValidatingAdmissionWebhook_2018-10-10</guid>
      </item>
      <item>
         <title>Added partner AMI information</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-partner-amis.html</link>
         <description>Canonical has partnered with Amazon EKS to create node AMIs that you can use in your clusters.</description>
         <pubDate>Wed, 3 Oct 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_partner_AMI_information_2018-10-03</guid>
      </item>
      <item>
         <title>Added instructions for AWS CLI update-kubeconfig command</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html</link>
         <description>Amazon EKS has added the &lt;code class="code"&gt;update-kubeconfig&lt;/code&gt; to the AWS CLI to simplify the process of creating a &lt;code class="code"&gt;kubeconfig&lt;/code&gt; file for accessing your cluster.</description>
         <pubDate>Fri, 21 Sep 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Added_instructions_for_AWS_CLI_update-kubeconfig_command_2018-09-21</guid>
      </item>
      <item>
         <title>New Amazon EKS optimized AMIs</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Amazon EKS has updated the Amazon EKS optimized AMIs (with and without GPU support) to provide various security fixes and AMI optimizations.</description>
         <pubDate>Thu, 13 Sep 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_Amazon_EKS_optimized_AMIs_2018-09-13</guid>
      </item>
      <item>
         <title>Amazon EKS AWS Region expansion</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Amazon EKS is now available in the Europe (Ireland) (&lt;code class="code"&gt;eu-west-1&lt;/code&gt;) Region.</description>
         <pubDate>Wed, 5 Sep 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_AWS_Region_expansion_2018-09-05</guid>
      </item>
      <item>
         <title>Amazon EKS platform version update</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html</link>
         <description>New platform version with support for Kubernetes &lt;a href="https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/" rel="noopener noreferrer" target="_blank"&gt;aggregation layer&lt;/a&gt; and the &lt;a href="https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/" rel="noopener noreferrer" target="_blank"&gt;Horizontal Pod Autoscaler&lt;/a&gt;(HPA).</description>
         <pubDate>Fri, 31 Aug 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_platform_version_update_2018-08-31</guid>
      </item>
      <item>
         <title>New Amazon EKS optimized AMIs and GPU support</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Amazon EKS has updated the Amazon EKS optimized AMI to use a new AWS CloudFormation node template and &lt;a href="https://github.com/awslabs/amazon-eks-ami/blob/main/templates/al2/runtime/bootstrap.sh" rel="noopener noreferrer" target="_blank"&gt;bootstrap script&lt;/a&gt;. In addition, a new &lt;a href="https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html#gpu-ami"&gt;Amazon EKS optimized AMI with GPU support&lt;/a&gt; is available.</description>
         <pubDate>Wed, 22 Aug 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_Amazon_EKS_optimized_AMIs_and_GPU_support_2018-08-22</guid>
      </item>
      <item>
         <title>New Amazon EKS optimized AMI patched for ALAS2-2018-1058</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Amazon EKS has updated the Amazon EKS optimized AMI to address the CVEs that are referenced in &lt;a href="https://alas.aws.amazon.com/AL2/ALAS-2018-1058.html" rel="noopener noreferrer" target="_blank"&gt;ALAS2-2018-1058&lt;/a&gt;.</description>
         <pubDate>Tue, 14 Aug 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#New_Amazon_EKS_optimized_AMI_patched_for_ALAS2-2018-1058_2018-08-14</guid>
      </item>
      <item>
         <title>Amazon EKS optimized AMI build scripts</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html</link>
         <description>Amazon EKS has open-sourced the build scripts that are used to build the Amazon EKS optimized AMI. These build scripts are now available on GitHub.</description>
         <pubDate>Tue, 10 Jul 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_optimized_AMI_build_scripts_2018-07-10</guid>
      </item>
      <item>
         <title>Amazon EKS initial release</title>
         <link>https://docs.aws.amazon.com/eks/latest/userguide/doc-history.html</link>
         <description>Initial documentation for service launch</description>
         <pubDate>Tue, 5 Jun 2018 19:00:00 GMT</pubDate>
         <guid isPermaLink="false">https://docs.aws.amazon.com/eks/latest/userguide/#Amazon_EKS_initial_release_2018-06-05</guid>
      </item>
   </channel>
</rss>

```
