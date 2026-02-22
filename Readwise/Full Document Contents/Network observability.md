# Network observability

![rw-book-cover](https://docs.aws.amazon.com/assets/images/favicon.ico)

## Metadata
- Author: [[Amazon EKS Document History]]
- Full Title: Network observability
- Category: #articles
- Summary: Amazon EKS now provides enhanced container network observability with performance monitoring and workload traffic visibility.
- URL: https://docs.aws.amazon.com/eks/latest/userguide/network-observability.html

## Full Document
Amazon EKS provides enhanced network observability features that provide deeper insights into your container networking environment. These capabilities help you better understand, monitor, and troubleshoot your Kubernetes network landscape in AWS. With enhanced container network observability, you can leverage granular, network-related metrics for better proactive anomaly detection across cluster traffic, cross-AZ flows, and AWS services. Using these metrics, you can measure system performance and visualize the underlying metrics using your preferred observability stack.

In addition, Amazon EKS now provides network monitoring visualizations in the AWS console that accelerate and enhance precise troubleshooting for faster root cause analysis. You can also leverage these visual capabilities to pinpoint top-talkers and network flows causing retransmissions and retransmission timeouts, eliminating blind spots during incidents.

These capabilities are enabled by [Amazon CloudWatch Network Flow Monitor](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-NetworkFlowMonitor.html).

#### Use Cases

##### Measure network performance to detect anomalies

Several teams standardize on an observability stack that allows them to measure their system’s performance, visualize system metrics and be alarmed in the event that a specific threshold is breached. Container network observability in EKS aligns with this by exposing key system metrics that you can scrape to broaden observability of your system’s network performance at the pod and worker node level.

In the event of an alarm from your monitoring system, you may want to hone in on the cluster and workload where an issue originated from. To support this, you can leverage visualizations in the EKS console that narrow the scope of investigation at a cluster level, and accelerate the disclosure of the network flows responsible for the most retransmissions, retransmission timeouts, and the volume of data transferred.

##### Track top-talkers in your Amazon EKS environment

A lot of teams run EKS as the foundation for their platforms, making it the focal point for an application environment’s network activity. Using the network monitoring capabilities in this feature, you can track which workloads are responsible for the most traffic (measured by data volume) within the cluster, across AZs, as well as traffic to external destinations within AWS (DynamoDB and S3) and beyond the AWS cloud (the internet or on-prem). Additionally, you can monitor the performance of each of these flows based on retransmissions, retransmission timeouts, and data transferred.

#### Features

1. Performance metrics - This feature allows you to scrape network-related system metrics for pods and worker nodes directly from the Network Flow Monitor Agent running in your EKS cluster.
2. Service map - This feature dynamically visualizes intercommunication between workloads in the cluster, allowing you to quickly disclose key metrics (RT, RTO, and DT) associated with network flows between communicating pods.
3. Flow table - With this table, you can monitor the top talkers across the Kubernetes workloads in your cluster from three different angles: AWS service view, cluster view, and external view. For each view, you can see the retransmissions, retransmission timeouts, and data transferred between the source pod and its destination.

	* AWS service view: Shows top talkers to AWS services (DynamoDB and S3)
	* Cluster view: Shows top talkers within the cluster (east ← to → west)
	* External view: Shows top talkers to cluster-external destinations outside AWS

To get started, enable Container Network Observability in the EKS console for a new or existing cluster. This will automate the creation of Network Flow Monitor dependencies ([Scope](https://docs.aws.amazon.com/networkflowmonitor/2.0/APIReference/API_CreateScope.html) and [Monitor](https://docs.aws.amazon.com/networkflowmonitor/2.0/APIReference/API_CreateMonitor.html) resources). In addition, you will have to install the [Network Flow Monitor Agent add-on](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-NetworkFlowMonitor-agents-kubernetes-eks.html). Alternatively, you can install these dependencies using the `AWS CLI`, [EKS APIs](https://docs.aws.amazon.com/eks/latest/APIReference/API_Operations_Amazon_Elastic_Kubernetes_Service.html) (for the add-on), [NFM APIs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-NetworkFlowMonitor-API-operations.html) or Infrastructure as Code (like [Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/networkflowmonitor_monitor)). Once these dependencies are in place, you can configure your preferred monitoring tool to scrape network performance metrics for pods and worker nodes from the NFM agent. To visualize the network activity and performance of your workloads, you can navigate to the EKS console under the “Network” tab of the cluster’s observability dashboard.

When using Network Flow Monitor in EKS, you can maintain your existing observability workflow and technology stack while leveraging a set of additional features which further enable you to understand and optimize the network layer of your EKS environment. You can learn more about the [Network Flow Monitor pricing here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-NetworkFlowMonitor.pricing.html).

#### How does it work?

##### Performance Metrics

If you are running third party (3P) tooling to monitor your EKS environment (such as Prometheus and Grafana), you can scrape the supported system metrics directly from the Network Flow Monitor agent. These metrics can be sent to your monitoring stack to expand measurement of your system’s network performance at the pod and worker node level. The available metrics are listed in the table, under Supported system metrics.

![Illustration of scraping system metrics](https://docs.aws.amazon.com/images/eks/latest/userguide/images/nfm-eks-metrics-workflow.png)Illustration of scraping system metrics
To enable these metrics, override the following environment variables using the configuration variables during the installation process (see: <https://aws.amazon.com/blogs/containers/amazon-eks-add-ons-advanced-configuration/>):

```
OPEN_METRICS:
    Enable or disable open metrics. Disabled if not supplied
    Type: String
    Values: [“on”, “off”]
OPEN_METRICS_ADDRESS:
    Listening IP address for open metrics endpoint. Defaults to 127.0.0.1 if not supplied
    Type: String
OPEN_METRICS_PORT:
    Listening port for open metrics endpoint. Defaults to 80 if not supplied
    Type: Integer
    Range: [0..65535]
```

In addition, Network Flow Monitor captures network flow data along with flow level metrics: retransmissions, retransmission timeouts, and data transferred. This data is processed by Network Flow Monitor and visualized in the EKS console to surface traffic in your cluster’s environment, and how it’s performing based on these flow level metrics.

The diagram below depicts a workflow in which both types of metrics (system and flow level) can be leveraged to gain more operational intelligence.

![Illustration of workflow with different performance metrics](https://docs.aws.amazon.com/images/eks/latest/userguide/images/nfm-eks-metrics-types-workflow.png)Illustration of workflow with different performance metrics
1. The platform team can collect and visualize system metrics in their monitoring stack. With alerting in place, they can detect network anomalies or issues impacting pods or worker nodes using the system metrics from the NFM agent.
2. As a next step, platform teams can leverage the native visualizations in the EKS console to further narrow the scope of investigation and accelerate troubleshooting based on flow representations and their associated metrics.

Important note: The scraping of system metrics from the NFM agent and the process of the NFM agent pushing flow-level metrics to the NFM backend are independent processes.

Important note: system metrics are exported in [OpenMetrics](https://openmetrics.io/) format.

| Metric name | Type | Description |
| --- | --- | --- |
| ingress\_flow\_count | Counter | Numbers of flows to a pod |
| egress\_flow\_count | Counter | Number of flows from a pod to anywhere |
| ingress\_pkt\_count | Counter | Number of TCP packets received by a pod |
| egress\_pkt\_count | Counter | Number of TCP packets sent out by a pod |
| ingress\_bytes\_count | Counter | Number of bytes received by a pod |
| egress\_bytes\_count | Counter | Number of bytes sent out by a pod |
| bw\_in\_allowance\_exceeded | Counter | Number of packets queued or dropped because the inbound aggregate bandwidth exceeded the maximum for the instance |
| bw\_out\_allowance\_exceeded | Counter | Number of packets queued or dropped because the outbound aggregate bandwidth exceeded the maximum for the instance |
| pps\_allowance\_exceeded | Counter | Packets per second limit breached at a pod |
| conntrack\_allowance\_exceeded | Counter | Connection Track limit breached. An event will be generated if 90 to 95% conntrack table limit is reached and logged on the node. |

| Metric name | Type | Description |
| --- | --- | --- |
| TCP retransmissions | Counter | Number of times a sender resends a packet that was lost or corrupted during transmission. |
| TCP retransmission timeouts | Counter | Number of times a sender initiated a waiting period to determine if a packet was lost in transit. |
| Data (bytes) transferred | Counter | Volume of data transferred between a source and destination for a given flow. |

![Illustration of how NFM works with EKS](https://docs.aws.amazon.com/images/eks/latest/userguide/images/nfm-eks-workflow.png)Illustration of how NFM works with EKS
1. When installed, the Network Flow Monitor agent runs as a DaemonSet on every worker node and collects the top 500 network flows (based on volume of data transferred) every 30 seconds.
2. These network flows are sorted into the following categories: Intra AZ, Inter AZ, EC2 → S3, EC2 → DynamoDB (DDB), and Unclassified. Each flow has 3 metrics associated with it: retransmissions, retransmission timeouts, and data transferred (in bytes).

	* Intra AZ - network flows between pods in the same AZ
	* Inter AZ - network flows between pods in different AZs
	* EC2 → S3 - network flows from pods to S3
	* EC2 → DDB - network flows from pods to DDB
	* Unclassified - network flows from pods to the Internet or on-prem
3. Network flows from the Network Flow Monitor Top Contributors API are used to power the following experiences in the EKS console:

	* Service map: Visualization of network flows within the cluster (Intra AZ and Inter AZ).
	* Flow table: Table presentation of network flows within the cluster (Intra AZ and Inter AZ), from pods to AWS services (EC2 → S3 and EC2 → DDB), and from pods to external destinations (Unclassified).

The network flows pulled from the Top Contributors API are scoped to a 1 hour time range, and can include up to 500 flows from each category. For the service map, this means up to 1000 flows can be sourced and presented from the Intra AZ and Inter AZ flow categories over a 1 hour time range. For the flow table, this means that up to 3000 network flows can be sourced and presented from all 6 network flow categories over a 2 hour time range.

*Deployment view*

![Illustration of service map with ecommerce app in deployment view](https://docs.aws.amazon.com/images/eks/latest/userguide/images/ecommerce-deployment.png)Illustration of service map with ecommerce app in deployment view
*Pod view*

![Illustration of service map with ecommerce app in pod view](https://docs.aws.amazon.com/images/eks/latest/userguide/images/ecommerce-pod.png)Illustration of service map with ecommerce app in pod view
*Deployment view*

![Illustration of service map with photo-gallery app in deployment view](https://docs.aws.amazon.com/images/eks/latest/userguide/images/photo-gallery-deployment.png)Illustration of service map with photo-gallery app in deployment view
*Pod view*

![Illustration of service map with photo-gallery app in pod view](https://docs.aws.amazon.com/images/eks/latest/userguide/images/photo-gallery-pod.png)Illustration of service map with photo-gallery app in pod view
###### Example: Flow Table

 *AWS service view*

![Illustration of flow table view](https://docs.aws.amazon.com/images/eks/latest/userguide/images/aws-service-view.png)Illustration of flow table view
*Cluster view*

![Illustration of flow table in cluster view](https://docs.aws.amazon.com/images/eks/latest/userguide/images/cluster-view.png)Illustration of flow table in cluster view
#### Considerations and Limitations

* Container Network Observability in EKS is only available in regions where [Network Flow Monitor is supported](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-NetworkFlowMonitor-Regions.html).
* Supported system metrics are in OpenMetrics format, and can be directly scraped from the Network Flow Monitor (NFM) agent.
* To enable Container Network Observability in EKS using Infrastructure as Code (IaC) like [Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/networkflowmonitor_monitor), you need to have these dependencies defined and created in your configurations: NFM scope, NFM monitor and the NFM agent.
* Network Flow Monitor supports up to approximately 5 million flows per minute. This is approximately 5,000 EC2 instances (EKS worker nodes) with the Network Flow Monitor agent installed. Installing agents on more than 5000 instances may affect monitoring performance until additional capacity is available.
