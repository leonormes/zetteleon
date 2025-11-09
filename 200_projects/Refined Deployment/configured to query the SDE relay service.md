---
aliases: []
confidence:
created: 2025-11-03T12:13:28Z
epistemic:
last_reviewed:
modified: 2025-11-03T12:28:32Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [bunny-relay, hie-prod-34, networking, project/work/cuh]
title: configured to query the SDE relay service
type:
uid:
updated:
---

Here’s a detailed summary of how CUH (from the "bunny" agent) was configured to query the SDE relay service, including the latest IP ranges used, based on your infrastructure code and Slack discussions.

---

## 1. **How CUH Traffic Was Allowed to Query the SDE Relay Service**

### **a. AWS ALB Security Group Configuration**

The SDE relay service is exposed via an AWS Application Load Balancer (ALB). To allow traffic from CUH (and specifically from the bunny agent), the ALB’s security group was configured to permit inbound HTTPS (TCP/443) traffic **only** from specific source IP ranges.

This was managed in Terraform as follows:

```hcl
resource "aws_security_group" "relay_alb" {
  name        = "${local.name}-relay-alb-sg"
  description = "Allow HTTPS from Azure AKS only"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["20.108.119.18/32"] # Azure AKS
    description = "Allow HTTPS from Azure"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["194.176.105.64/26"] # CUH
    description = "Allow HTTPS from CUH"
  }
}
```

([See full example in context](file:///your/path/to/terraform/file.tf))

### **b. Additional Testing and Temporary Rules**

During troubleshooting and testing, you sometimes temporarily allowed traffic from everywhere (`0.0.0.0/0`), but this was removed for production security.

---

## 2. **Latest IP Ranges Used**

### **a. CUH Outbound IP Range**

The **latest confirmed egress IP range** for CUH traffic (as provided by Ahmed Aaref on 2025-09-10) is:

- **217.38.237.128/26**

This was explicitly confirmed in Slack:

> Ahmed Aaref (External) 10/09 16:52  
> 217.38.237.128/26

### **b. ALB Security Group Rules**

The security group for the relay ALB was updated to include this range for CUH-originating traffic. In addition, the following ranges were also used for CUH and Azure:

- **194.176.105.64/26** (CUH, as per previous and current Terraform)
- **20.108.119.18/32** (Azure AKS node, for Azure-originated traffic)

**Note:** There are also references to:
- **194.176.185.64/26** and **194.176.185.64/29** in some Terraform snippets, but the main and latest confirmed range is **194.176.105.64/26** and **217.38.237.128/26**.

---

## 3. **Summary Table**

| Source        | CIDR/IP Range         | Purpose/Notes                   |
|---------------|----------------------|---------------------------------|
| CUH (bunny)   | 217.38.237.128/26    | Latest confirmed egress IP      |
| CUH (legacy)  | 194.176.105.64/26    | Still present in SG rules       |
| Azure AKS     | 20.108.119.18/32     | Azure node egress IP            |

---

## 4. **References**

- [Slack Huddle: @Ollie Rushton – FITFILE – Slack](https://slack.com) (2025-09-10, 2025-11-03)
- [Terraform Security Group Example](file:///your/path/to/terraform/file.tf)
- [Terraform Security Group Example with 217.38.237.128/26](file:///your/path/to/terraform/file.tf)

---

## 5. **Final Notes**

- The **current production configuration** only allows inbound HTTPS to the relay ALB from the above CIDR blocks.
- If you need to update the allowed ranges, modify the `cidr_blocks` in the `aws_security_group.relay_alb` resource in your Terraform code and apply the changes.
- Always confirm with the CUH network team if their outbound NAT IPs change.

---

**If you need the exact file or want to see the full Terraform resource, let me know and I can link directly to the relevant [file](file:///your/path/to/terraform/file.tf) in your repo.**
## Network Configuration Analysis: CUH to SDE Relay Service

## CUH Bunny to SDE Relay Network Configuration Analysis

After analyzing the network configuration between CUH-DP and hie-sde-v2, I've identified the critical connection path and the impact of the planned changes.

### Connection Architecture

1. **CUH Bunny Service (Source)**:
   - Located in CUH-DP environment in Azure (Cambridge University Hospitals)
   - IP Range: `194.176.105.64/26` (CUH network range)
   - Service runs in Azure AKS in private network

2. **SDE Relay Service (Destination)**:
   - Located in hie-sde-v2 environment in AWS (EOE SDE)
   - Exposed via public Application Load Balancer (ALB)
   - NodePort: `32082` for production relay service

3. **Connection Path**:
   - CUH Bunny → Internet → SDE Relay ALB → SDE EKS Worker Nodes → Relay Service

### Security Group Configuration

The key security group rules allowing this connection are:

```hcl
# SDE security group rule allowing CUH access
ingress {
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["194.176.105.64/26"]  # CUH network range
  # TEMPORARILY REMOVED: description = "Allow HTTPS from CUH"
}

# Rule allowing the ALB to reach EKS nodes
egress {
  from_port       = 32082
  to_port         = 32082
  protocol        = "tcp"
  security_groups = [module.eks.cluster_security_group_id]
  # TEMPORARILY REMOVED: description = "Allow health checks to EKS nodes"
}

# Rule allowing the traffic to reach the relay service
resource "aws_security_group_rule" "alb_to_eks_health_check" {
  type                     = "ingress"
  from_port                = 32082
  to_port                  = 32082
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.relay_alb.id
  security_group_id        = module.eks.cluster_security_group_id
  description              = "Allow ALB health checks to reach relay service on worker nodes"
}
```

### Issue Analysis

The current Terraform plan changes are **NOT removing any security group rules**, but rather removing rule descriptions to prevent recreation of rules. This is due to state drift between:

1. Manually applied fixes from Oct 2, 2025
2. Terraform managed state

The current change is removing descriptions only:

```hcl
# TEMPORARILY REMOVED: description = "Allow HTTPS from CUH"
```

### Why This Shouldn't Affect Traffic

1. **Rule Content Preserved**: The actual CIDR block (`194.176.105.64/26`) allowing CUH traffic remains unchanged
2. **No Rule Deletion**: The plan shows "update" not "delete" for the security groups
3. **Protocol/Ports Unchanged**: The TCP/443 ingress and TCP/32082 egress rules remain intact

### Recommendation

The planned changes should not impact connectivity between CUH bunny service and the SDE relay service. The changes are only cosmetic (removing descriptions) to prevent Terraform from recreating rules that were manually fixed.

If connectivity issues arise after this change, investigate:

1. Whether other manual changes were made that aren't reflected in this plan
2. Network ACLs that might be impacting traffic
3. Route table configurations in either environment
4. Health of the EKS node ports and relay service

## Relay Service Networking Architecture in Hie-sde-v2

The relay service in the hie-sde-v2 environment provides external connectivity to internal services through a secure, controlled architecture:

### Core Components
1. **Application Load Balancer (ALB)**
2. **Security Group Rules**
3. **Target Groups & Node Attachments**
4. **DNS Configuration**

### Network Flow

```sh
External Clients → Internet → ALB → EKS Worker Nodes → Relay Service
```

### Key Configuration Elements

#### 1. ALB Security Group (aws_security_group.relay_alb)

```hcl
ingress {
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["20.108.119.18/32"]  # Azure AKS
  description = "Allow HTTPS from Azure"
}

ingress {
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["194.176.105.64/26"]  # CUH Network
  description = "Allow HTTPS from CUH"
}
```

#### 2. Target Group Configuration

```hcl
resource "aws_lb_target_group" "relay" {
  port     = 80
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    port    = "32082"  # NodePort for relay service
    path    = "/healthz"
    matcher = "200-399"
  }
}
```

#### 3. EKS Node Attachment

```hcl
resource "aws_lb_target_group_attachment" "relay_nodes" {
  target_group_arn = aws_lb_target_group.relay.arn
  target_id        = data.aws_instances.eks_worker_nodes.ids[count.index]
  port             = 32082  # NodePort where relay service listens
}
```

#### 4. Health Check Access Rule

```hcl
resource "aws_security_group_rule" "alb_to_eks_health_check" {
  type                     = "ingress"
  from_port                = 32082
  to_port                  = 32082
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.relay_alb.id
  security_group_id        = module.eks.cluster_security_group_id
  description = "Allow ALB health checks to reach relay service"
}
```

### Traffic Flow Details
1. **Inbound Traffic**:
   - HTTPS (443) traffic from approved sources (Azure AKS and CUH network)
   - ALB terminates SSL/TLS using ACM certificate

2. **Internal Routing**:
   - ALB forwards requests to EKS worker nodes on NodePort 32082
   - Target group health checks validate service availability via /healthz endpoint

3. **Security**:
   - Least-privilege access: Only specific IP ranges allowed
   - Separate security groups for ALB and EKS nodes
   - Health checks ensure only healthy nodes receive traffic

4. **DNS**:
   - Route53 record (relay.codisc-eoe-sde.uk) points to ALB
   - Provides stable endpoint despite infrastructure changes

### Key Characteristics
- **Public Exposure**: ALB is internet-facing (internal=false)
- **High Availability**: Deployed across multiple AZs
- **Security Isolation**: EKS nodes only exposed via NodePort, not directly
- **Health Monitoring**: Regular health checks ensure service availability
- **Controlled Access**: Explicit IP allow-list for incoming traffic

This architecture provides secure, controlled external access to internal services while maintaining network isolation and monitoring capabilities.

The bunny service traffic originates from the CUH-DP environment in Azure and targets the relay service in hie-sde-v2. Based on the network configuration in CUH-DP:

## Source IP Range for Bunny Traffic

The traffic will originate from **`10.250.16.0/24`** based on the following configuration:

```hcl
vnet_address_space = "10.250.16.0/24"
```

This VNet address space is partitioned into subnets:

1. **AKS Node Pool Subnets**:
   - `default_node_pool_subnet_address_prefix` = `10.250.16.0/28`
   - `additional_node_pool_subnet_address_prefix` = `10.250.16.16/28`

2. **VM Subnet**:
   - `vm_subnet_address_prefix` = `10.250.16.32/29`

3. **Private DNS Subnets**:
   - `private_dns_outbound_subnet_address_prefix` = `10.250.16.48/28`
   - `private_dns_outbound_snet_address_prefix` = `10.250.16.64/28`

## Network Flow

```sh
Bunny Service (10.250.16.0/24) → Firewall (10.250.1.68) → Internet → SDE Relay ALB
```

### Key Configuration Elements
1. **Forced Tunneling**:

   ```hcl
   network_plugin_mode = "overlay"
   firewall_existing_private_ip = "10.250.1.68"
   ```

   - All outbound traffic is forced through the firewall at 10.250.1.68

2. **Proxy Configuration**:

   ```hcl
   http_proxy_config = {
     http_proxy  = "http://10.252.142.180:8080/"
     https_proxy = "http://10.252.142.180:8080/"
     no_proxy = [
       "localhost",
       "127.0.0.1",
       "cuh-prod-1-ffcloud-service",
       "10.2.0.0/24",
       "10.244.0.0/16",
       "10.252.0.0/16"
     ]
   }
   ```

   - Outbound traffic uses a proxy at 10.252.142.180:8080
   - The `no_proxy` list includes internal services that bypass the proxy

3. **Network Security**:

```hcl
default_node_pool_enable_node_public_ip = false
```

   - Nodes have no public IPs, all traffic egresses through firewall

## Why This Range is Expected
1. The bunny service runs in the AKS cluster within the `10.250.16.0/24` VNet
2. All outbound traffic egresses through the firewall at 10.250.1.68
3. The firewall performs Source NAT, making traffic appear from its IP
4. The relay service in SDE is configured to accept traffic from this path

## Verification

To confirm the actual source IP seen by the relay service:

1. Check firewall logs for outbound connections to SDE relay
2. Examine relay service access logs for incoming connections
3. Verify the firewall's public IP matches the allowed CIDR in SDE (`194.176.105.64/26`)

The actual source IP seen by the SDE relay will be the firewall's public IP after NAT, not the private IP range. The firewall performs the final NAT translation before traffic leaves the CUH environment.
