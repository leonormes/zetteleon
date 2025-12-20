---
aliases: []
confidence: 
created: 2025-02-19T10:00:44Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [debug, ff_deploy, networking, vpc]
title: from the linux jumpbox inside the vpc how do I deb
type: documentation
uid: 
updated: 
version:
---

## Debugging Internet Connectivity Issues from a Linux Jumpbox in AWS VPC

---

### Key Findings Summary

When a Linux jumpbox within an AWS VPC cannot reach the internet, the root cause typically involves misconfigured network routing, security group/NACL restrictions, or instance-level configuration errors. This report synthesizes diagnostic methodologies from AWS documentation[^3][^6][^15], Linux network debugging tools[^2][^7][^13], and VPC architectural best practices[^1][^4][^12] to isolate and resolve such issues.

---

### Network Configuration Validation

#### 1. Verify Internet Gateway and Route Table Configuration

The jumpbox must reside in a **public subnet** with a route table directing `0.0.0.0/0` traffic to an internet gateway (IGW)[^3][^15].

**Steps:**

1. Navigate to the **VPC Console** > **Route Tables** > Select the subnet’s associated route table.
2. Confirm a route exists with:
    - **Destination**: `0.0.0.0/0`
    - **Target**: `igw-xxxxxxxx` (IGW ID)[^15].
3. Validate the IGW is attached to the VPC under **Internet Gateways**[^6].

**Failure Indicators**:

- Missing `0.0.0.0/0` route → Add route via IGW[^15].
- IGW not attached → Attach IGW to VPC[^6].

---

#### 2. Check Security Group and NACL Rules

##### Security Groups

- **Outbound Rules**: Ensure the jumpbox’s security group allows all outbound traffic (`0.0.0.0/0` on ports 80/443)[^11][^15].
- **Inbound Rules**: SSH (port 22) should be restricted to trusted IPs[^1][^4].

**Command**:

```bash  
aws ec2 describe-security-groups --group-ids sg-085b7a3273a7eff91 --query 'SecurityGroups[^0].IpPermissionsEgress'  
```

##### Network ACLs

- **Inbound**: Allow ephemeral ports (1024-65535) from `0.0.0.0/0`[^1][^11].
- **Outbound**: Allow HTTP/HTTPS (80/443) to `0.0.0.0/0`[^3][^11].

**Command**:

```bash  
aws ec2 describe-network-acls --filters Name=association.subnet-id,Values=<subnet-id>  
```

**Failure Scenarios**:

- Overly restrictive NACL outbound rules → Allow `0.0.0.0/0` on 80/443.
- Ephemeral port blocking → Permit 1024-65535[^1].

---

### Instance-Level Diagnostics

#### 3. Validate Public IP Assignment

A jumpbox in a public subnet requires a public IPv4 address or Elastic IP[^3][^15].

**Check via CLI**:

```bash  
curl http://169.254.169.254/latest/meta-data/public-ipv4  
```

**No Public IP?** → Assign Elastic IP or enable auto-assign in subnet settings[^15].

---

#### 4. Test Outbound Connectivity

**Basic Tests**:

1. **Ping Public IP**:

```bash  
ping -c 4 8.8.8.8  # Test IPv4 connectivity[^5][^7][^13]  
```

    - **No reply** → Network path blocked (NACL/Security Group)[^3].
    - **Reply received** → DNS may be failing (proceed to Step 5).
2. **HTTP Access**:

```bash  
curl -Iv https://google.com  # Test HTTPS via IP/domain[^5][^13]  
```

**Advanced Tools**:

- **`mtr` for Path Analysis**:

```bash  
mtr -4 8.8.8.8  # Identify packet loss points[^9][^13]  
```

- **`tcpdump` for Packet Capture**:

```bash  
sudo tcpdump -i eth0 'port 80 or port 443'  # Inspect HTTP/S traffic[^9]  
```

---

#### 5. DNS Resolution Checks

**Commands**:

```bash  
dig google.com  # Test DNS resolution[^5][^13]  
nslookup google.com  
```

**Failure Modes**:

- **No resolution** → Check VPC DNS settings (`enableDnsSupport`/`enableDnsHostnames`)[^15].
- **Slow resolution** → Validate VPC DNS server (e.g., `169.254.169.253`)[^15].

**Override DNS**:

```bash  
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf  # Use Google DNS temporarily  
```

---

#### 6. Inspect Local Firewall and Routing

**Firewall Rules (iptables/ufw)**:

```bash  
sudo iptables -L -v  # List active rules[^9][^16]  
sudo ufw status  
```

**Fix**: Allow outbound traffic:

```bash  
sudo iptables -A OUTPUT -j ACCEPT  # Caution: Overly permissive for testing  
```

**Routing Table**:

```bash  
ip route show  # Verify default route via IGW[^13][^17]  
```

- **Missing default route** → Reconfigure DHCP or static routing.

---

#### 7. Validate Instance Metadata Service (IMDS) Access

AWS metadata service (`169.254.169.254`) should be reachable:

```bash  
curl http://169.254.169.254/latest/meta-data/  # IMDSv1 test[^18]  
```

**Blocked?** → Check hop limit or HTTP metadata service restrictions[^18].

---

### Advanced AWS-Specific Debugging

#### 8. Use VPC Reachability Analyzer

AWS’s built-in tool diagnoses connectivity paths[^14]:

1. **Navigate to VPC Console** > **Reachability Analyzer**.
2. Create analysis path:
    - **Source**: Jumpbox instance ID.
    - **Destination**: External IP (e.g., 8.8.8.8).
    - **Port**: 80 (HTTP).

**Output**: Identifies blocked hops (e.g., NACL, security group)[^14].

---

#### 9. Enable VPC Flow Logs

Flow logs capture traffic at the ENI level[^14][^18]:

1. **Create Flow Log**:

```bash  
aws ec2 create-flow-logs --resource-type Subnet --resource-ids <subnet-id> \  
    --traffic-type ALL --log-destination-type cloud-watch-logs  
```

2. Analyze logs for `REJECT` entries indicating NACL/security group blocks[^14].

**Key Fields**:

- `srcaddr`: Jumpbox IP.
- `action`: `ACCEPT`/`REJECT`.
- `dstport`: Destination port (e.g., 80, 443)[^18].

---

#### 10. Check SSM Agent and IAM Roles

If using AWS Systems Manager (SSM) for management:

1. **Agent Status**:

```bash  
sudo systemctl status amazon-ssm-agent  # Ensure running[^1][^15]  
```

2. **IAM Role**: Verify `AmazonSSMManagedInstanceCore` policy is attached[^15].

**Debugging**:

```bash  
sudo tail -f /var/log/amazon/ssm/amazon-ssm-agent.log  # Agent connectivity issues  
```

---

### Conclusion and Recommendations

#### Identified Issue Workflow

1. **Missing IGW Route**: Most common public subnet failure[^3][^15].
2. **Overly Restrictive NACLs**: Blocking ephemeral ports[^1][^11].
3. **Misconfigured Security Groups**: Denying outbound HTTP/S[^11].
4. **Local Firewall Rules**: iptables/ufw blocking traffic[^9][^16].

#### Proactive Measures

- **Implement VPC Flow Logs**: Continuously monitor traffic patterns[^18].
- **Use Reachability Analyzer**: Pre-deployment connectivity validation[^14].
- **Automate NACL/SG Audits**: AWS Config rules for compliance[^11].

#### Final Validation Steps

1. **Route Table Audit**: Confirm `0.0.0.0/0` → IGW[^15].
2. **NACL Ephemeral Ports**: Allow 1024-65535 outbound[^1].
3. **Security Group Outbound**: Permit 80/443 to `0.0.0.0/0`[^11].
4. **Public IP Assignment**: Ensure auto-assign enabled[^15].

By systematically addressing routing, security policies, and instance configurations, administrators can resolve internet connectivity issues in Linux jumpboxes while adhering to AWS best practices[^1][^3][^15].
