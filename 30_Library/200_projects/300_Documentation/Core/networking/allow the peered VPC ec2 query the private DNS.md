---
aliases: []
confidence: 
created: 2025-02-22T09:02:36Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, ff_deploy, networking, peering, vpc]
title: allow the peered VPC ec2 query the private DNS
type: instruction
uid: 
updated: 
version: 1
---

## 1. VPC Peering Configuration

### Route Tables
- Update the route tables in both VPCs to allow traffic to flow between them.
- Add routes that direct traffic destined for the peer VPC's CIDR block through the peering connection
- Ensure these routes are as restrictive as possible, adhering to the principle of least privilege.
### Non-Overlapping CIDR Blocks
- Confirm that the CIDR blocks of both VPCs do not overlap, as overlapping ranges can cause routing conflicts.

## 2. Security Groups and Network ACLs

Implement strict security controls to regulate traffic between the VPCs:

- Security Groups: Configure security groups to allow inbound traffic on the specific ports required by your web application (e.g., TCP port 443 for HTTPS). Restrict the source to the IP range of the EC2 instance or its security group in the peer VPC.
- Network ACLs: Set up Network Access Control Lists (ACLs) at the subnet level to provide an additional layer of security. Define rules that permit only the necessary inbound and outbound traffic between the subnets hosting the EC2 instance and the EKS cluster.

## 3. DNS Resolution

Ensure that the EC2 instance can resolve the domain name of your web application:

- Private Hosted Zones: If you're using Amazon Route 53 private hosted zones for your web application's domain, associate the hosted zone with both VPCs. This allows resources in the peer VPC to resolve domain names hosted in the private zone.
- Custom DNS Servers: If you're using custom DNS servers, configure the EC2 instance to point to these servers, ensuring they can resolve the web application's domain.

## 4. Encryption and Data Protection

Protect data in transit between the EC2 instance and the web application:

- TLS/SSL: Implement TLS/SSL to encrypt data transmitted between the EC2 instance and the web application. Ensure that your web application is configured to use HTTPS, and install valid certificates.
- Application-Level Encryption: For added security, consider encrypting sensitive data at the application level before transmission.

## 5. Monitoring and Logging

Establish monitoring and logging to detect and respond to potential security incidents:

- VPC Flow Logs: Enable VPC Flow Logs on both VPCs to capture information about the IP traffic flowing between them. Analyze these logs to monitor for unusual or unauthorized access attempts.
- AWS CloudTrail: Use AWS CloudTrail to log API calls and monitor access to resources within your AWS environment.

## 6. Regular Auditing and Compliance

Maintain a robust security posture by regularly reviewing and updating your configurations:

- Security Group and ACL Reviews: Periodically audit security group rules and network ACLs to ensure they adhere to the principle of least privilege and remove any unnecessary permissions.
- Compliance Checks: Utilize AWS Config and AWS Security Hub to assess your environment against security best practices and compliance standards.

In the context of your VPC peering setup, the instruction "Add routes that direct traffic destined for the peer VPC's CIDR block through the peering connection" means configuring your route tables to ensure that any network traffic intended for the other VPC is correctly routed via the established peering connection. Here's a detailed explanation with examples:

Understanding the Concept

When two VPCs are peered, they can communicate with each other as if they are part of the same network. However, this communication doesn't happen automatically; you must explicitly define routes in each VPC's route tables to direct traffic to the peer VPC through the peering connection.

Example Scenario

Assume you have two VPCs:

- VPC A:
    - CIDR Block: `10.0.0.0/16`
    - Route Table ID: `rtb-aaa111`
    - Peering Connection ID: `pcx-aaa111`
- VPC B:
    - CIDR Block: `192.168.0.0/16`
    - Route Table ID: `rtb-bbb222`
    - Peering Connection ID: `pcx-bbb222`

Steps to Configure Routing

1. Identify the Route Tables:

    - Determine which route tables are associated with the subnets that need to communicate across the VPCs.
2. Modify Route Tables in VPC A:

    - Navigate to the Amazon VPC console.
    - Select "Route Tables" from the navigation pane.
    - Choose the route table `rtb-aaa111` associated with VPC A.
    - Click on "Edit routes" and add a new route:
        - Destination: `192.168.0.0/16` (CIDR block of VPC B)
        - Target: `pcx-aaa111` (Peering connection ID)

This route was directs any traffic from VPC A destined for the `192.168.0.0/16` network to the peering connection.

3. Modify Route Tables in VPC B:

    - Repeat the process in VPC B:
        - Destination: `10.0.0.0/16` (CIDR block of VPC A)
        - Target: `pcx-bbb222` (Peering connection ID)

This route ensures that traffic from VPC B destined for the `10.0.0.0/16` network is routed through the peering connection.

Practical Example

Suppose an EC2 instance in VPC A with the private IP address `10.0.1.10` needs to communicate with an EC2 instance in VPC B at `192.168.1.20`.

- When the instance in VPC A sends a request to `192.168.1.20`, the route table in VPC A directs this traffic to the peering connection `pcx-aaa111` because the destination IP falls within the `192.168.0.0/16` range.
- Upon reaching VPC B, the route table there recognizes that the source IP `10.0.1.10` is within the `10.0.0.0/16` range and allows the traffic to reach the target instance.

By configuring these routes, both VPCs can securely and efficiently communicate over the peering connection.

Important Considerations

- Bidirectional Routing: Ensure that both VPCs have routes configured to direct traffic to each other's CIDR blocks. Without reciprocal routes, communication will be unidirectional.
- Security Groups and Network ACLs: In addition to route tables, verify that security groups and network ACLs are configured to allow the desired traffic between the VPCs.
- Non-Overlapping CIDR Blocks: VPCs must have non-overlapping CIDR blocks to establish a peering connection successfully.

It seems that the other vpc has 2 cidr ranges:10.64.11.0/24 10.64.8.64/26. But the route table has these 2 destinations 10.64.11.128/25, 10.64.11.0/25 pointing the peering connection pcx-06524c8e180979086. does this work or make sense?

In your current setup, the route table entries are configured as follows:

- Route Table Entries:
	- `10.64.11.128/25` → `pcx-06524c8e180979086`
	- `10.64.11.0/25` → `pcx-06524c8e180979086`

These entries cover the IP address range `10.64.11.0` to `10.64.11.255`, effectively splitting the `10.64.11.0/24` CIDR block into two equal halves:

- `10.64.11.0/25` spans `10.64.11.0` to `10.64.11.127`
- `10.64.11.128/25` spans `10.64.11.128` to `10.64.11.255`

However, the second CIDR block of the peer VPC, `10.64.8.64/26`, which covers the range `10.64.8.64` to `10.64.8.127`, is not addressed by the current route table entries.

Recommendation:

To ensure complete and accurate routing to all subnets in the peer VPC, it's advisable to add a route that specifically targets the `10.64.8.64/26` CIDR block. This can be achieved by adding the following route to your route table:

- Destination: `10.64.8.64/26`
- Target: `pcx-06524c8e180979086`

By implementing this route, you ensure that traffic destined for the `10.64.8.64/26` subnet is correctly routed through the VPC peering connection, facilitating proper communication between your VPC and all subnets of the peer VPC.

To allow access from the second VPC to your web app running in an Amazon EKS cluster, you and the other person need to set up network connectivity between the two VPCs and configure security settings properly. Here’s what each side needs to do:

---

### 1. Choose a VPC Peering or Transit Gateway (TGW) Approach

Since you are working with two separate VPCs, you have two main options for connectivity:

- VPC Peering (Simpler, but doesn't support transitive routing)
- AWS Transit Gateway (TGW) (Better for multiple VPCs but more complex)

If you expect only a few VPCs, VPC Peering is fine. If there will be more in the future, Transit Gateway is better.

---

### 2. Networking Setup

Your VPC (EKS Cluster VPC):

- Accept the VPC peering connection (if using peering)
- Update route tables to allow traffic from the second VPC
- Ensure the correct subnets are accessible

Second VPC:

- Request a VPC peering connection (if using peering)
- Update route tables to send traffic to your VPC
- Ensure instances in this VPC can route traffic correctly

---

### 3. Security Group & NACL Configuration

On Your Side (EKS Cluster Security Group):

- Allow inbound traffic from the second VPC's CIDR to your EKS service
- Example:

    ```sh
    Source: <2nd VPC CIDR>
    Protocol: TCP
    Port: <Your WebApp Port>
    ```

On the Other Side (Security Group of Source VPC):

- Allow outbound traffic to your EKS cluster on the correct port

---

### 4. DNS Resolution (If Needed)

If your web app is exposed via an internal Load Balancer or Private DNS:

- Enable DNS resolution over VPC peering
- Use AWS Route 53 Private Hosted Zones (if required)

---

### 5. Verify with Connectivity Tests

- Use `curl` or `nc` (netcat) from the second VPC to check if it can reach the EKS service
- Check VPC Flow Logs if traffic is being blocked

Would you like specific commands for setting up the routes or security groups?

No, your VPC’s routing does not need to allow traffic to the second VPC's CIDR ranges—only from the second VPC to your web app.

Here’s why:

- The second VPC is the one initiating requests to your web app.
- Your EKS cluster (or its Load Balancer) is only responding to those requests.
- AWS handles return traffic automatically through the connection (VPC Peering or Transit Gateway), as long as the source request was allowed in the first place.

### Routing Requirements

✅ Your VPC (EKS Cluster VPC):

- Route does not need to explicitly point to the second VPC.
- Security groups must allow inbound traffic from the second VPC’s CIDR range.

✅ Second VPC (EC2 Subnet):

- Must have a route to your EKS cluster's VPC CIDR (or just the Load Balancer’s subnet).

---

### Example Route Table Configurations

#### Your VPC (EKS VPC Route Table)

|Destination|Target|
|---|---|
|0.0.0.0/0|Internet Gateway (if public)|
|10.0.0.0/16 (EKS VPC)|local|

(No need to add the second VPC CIDR here.)

#### Second VPC (EC2 Subnet Route Table)

|Destination|Target|
|---|---|
|10.1.0.0/16 (EKS VPC CIDR)|VPC Peering / TGW|
|0.0.0.0/0|Internet Gateway / NAT (if needed)|

---

### Security Considerations

- Your EKS Load Balancer or Ingress Controller’s security group must allow inbound traffic from the second VPC’s CIDR.
- Your EC2 instances in the second VPC must allow outbound traffic to the EKS service.

Let me know if you want help with specific AWS CLI or Terraform commands!
