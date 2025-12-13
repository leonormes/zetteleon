---
aliases: []
confidence: 
created: 2025-02-20T21:40:46Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking]
title: networking debugging tools
type: 
uid: 
updated: 
version: 
---

Here are some especially useful tools on a Linux Ubuntu AWS EC2 instance for debugging network connection issues:

General Network Connectivity Tools (Often Pre-installed):

 - ping:
   - Use Case: The most basic tool to check if a host is reachable. Sends ICMP Echo Request packets and listens for replies.
   - Helpful For:
     - Verifying basic IP connectivity to a destination (IP address or hostname).
     - Measuring round-trip time (latency) to a host.
     - Detecting packet loss.
   - Example: ping google.com or ping <IP_address>
 - traceroute / tracepath:
   - Use Case: Shows the network path (routers/hops) that packets take to reach a destination. traceroute uses UDP or ICMP, while tracepath uses UDP and is often preferred as it doesn't require root privileges.
   - Helpful For:
     - Identifying where network connectivity breaks down along the path to a destination.
     - Pinpointing slow or problematic hops.
     - Understanding the route traffic is taking.
   - Example: traceroute google.com or tracepath google.com
   - Note: Intermediate routers might not always respond to traceroute requests, so results might not always be complete.
 - dig / nslookup:
   - Use Case: DNS (Domain Name System) lookup tools. dig is generally more powerful and feature-rich than nslookup.
   - Helpful For:
     - Verifying DNS resolution: checking if a hostname resolves to an IP address.
     - Diagnosing DNS problems if hostnames are not resolving correctly.
     - Querying specific DNS servers and record types (A, AAAA, MX, etc.).
   - Example: dig google.com or dig AAAA google.com (for IPv6 address) or nslookup google.com
 - ip (or ifconfig - older, but often available):
   - Use Case: For displaying and manipulating network interfaces, addresses, routes, and links. ip is the modern replacement for ifconfig.
   - Helpful For:
     - Checking the EC2 instance's IP address (ip a or ip addr).
     - Viewing network interface configuration (ip link show <interface_name>, e.g., ip link show eth0).
     - Examining routing tables (ip route show or ip r).
     - Checking network statistics (ip -s link).
   - Example: ip a or ifconfig
 - netstat / ss:
   - Use Case: Display network connections, routing tables, interface statistics, masquerade connections, and multicast memberships. ss (socket statistics) is the modern replacement for netstat and is generally faster and more powerful.
   - Helpful For:
     - Listing listening ports and established connections (ss -tulnp or netstat -tulnp).
     - Identifying which processes are using which ports and connections.
     - Checking connection states (ESTABLISHED, LISTEN, etc.).
     - Viewing routing table information (netstat -r or ss -route).
   - Example: ss -tulnp (shows listening TCP and UDP ports with process information) or netstat -an | grep LISTEN (shows all listening ports).
Tools to Install (Using apt install <tool_name>):
 - tcpdump:
   - Use Case: A powerful packet capture and network protocol analyzer. Captures network traffic passing through an interface.
   - Helpful For:
     - Deeply inspecting network traffic to see exactly what packets are being sent and received.
     - Diagnosing protocol-level issues.
     - Analyzing TCP handshakes, DNS queries, HTTP requests, etc.
     - Filtering traffic based on host, port, protocol, etc.
   - Example: sudo tcpdump -i eth0 -n -s 0 port 80 (captures HTTP traffic on interface eth0) or sudo tcpdump -i eth0 icmp (captures ICMP traffic).
   - Note: Requires sudo to run as it needs privileged access to network interfaces. Captured data can be complex to analyze; consider using Wireshark (see below) for GUI analysis of tcpdump output.
 - mtr (My Traceroute):
   - Use Case: Combines the functionality of ping and traceroute. Provides a continuously updated view of the route and latency to a destination, hop by hop.
   - Helpful For:
     - More dynamically and visually identifying network path issues and latency over time.
     - Better for diagnosing intermittent network problems.
     - Showing packet loss at each hop along the route.
   - Example: mtr google.com (interactive display) or mtr -r -c 10 google.com (report mode, 10 pings per hop).
 - nmap (Network Mapper):
   - Use Case: A versatile network scanner and port scanner.
   - Helpful For:
     - Port scanning: discovering open ports on a target host.
     - Identifying services running on open ports.
     - Operating system detection (sometimes).
     - Network discovery.
   - Example: nmap <IP_address> (basic port scan) or nmap -sV <IP_address> (service version detection).
   - Caution: Port scanning might be considered intrusive on networks you don't own or have permission to scan. Use responsibly and ethically, especially when scanning external endpoints.
 - ethtool:
   - Use Case: For displaying and changing Ethernet interface settings.
   - Helpful For:
     - Checking link speed and duplex settings of the network interface (ethtool eth0).
     - Verifying if the network interface is up and running.
     - Checking for interface errors and statistics.
   - Example: ethtool eth0
 - wireshark (GUI-based, may be less common on server, but useful for analysis of tcpdump captures):
   - Use Case: A powerful GUI-based network protocol analyzer. While you might not run the full GUI on a server, you can capture packets with tcpdump on the EC2 instance and then analyze the capture file in Wireshark on your local machine.
   - Helpful For:
     - In-depth analysis of captured network traffic.
     - Decoding protocols and understanding packet contents.
     - Filtering and searching through captures.
     - Visualizing network conversations and flows.
   - Workflow Example:
     - sudo tcpdump -i eth0 -w capture.pcap (capture traffic to a file on EC2)
     - Download capture.pcap to your local machine (using scp or similar).
     - Open capture.pcap in Wireshark on your local machine for analysis.
AWS Specific Tools & Considerations:
 - AWS VPC Reachability Analyzer: (AWS Console or AWS CLI)
   - Use Case: A built-in AWS tool to analyze network reachability between two points in your VPC. It simulates traffic paths and identifies potential issues with security groups, NACLs, route tables, etc.
   - Helpful For:
     - Troubleshooting connectivity within your VPC.
     - Verifying if traffic is allowed by security groups and NACLs along a specific path.
     - Diagnosing routing problems within the VPC.
   - Access: AWS Management Console -> VPC -> Reachability Analyzer. Or use AWS CLI commands.
 - AWS VPC Flow Logs: (AWS Service)
   - Use Case: Captures information about IP traffic going to and from network interfaces in your VPC. Logs are sent to CloudWatch Logs or S3.
   - Helpful For:
     - Auditing network traffic.
     - Security monitoring.
     - Diagnosing connectivity issues by examining traffic flow patterns and rejections.
     - Understanding traffic patterns in your VPC.
   - Configuration: Needs to be enabled for your VPC, subnet, or network interface. Logs can be analyzed in CloudWatch Logs or queried in S3.
 - AWS Network Manager: (AWS Service)
   - Use Case: For centralized monitoring and management of your AWS networks (VPCs, Transit Gateways, Direct Connect, VPNs).
   - Helpful For:
     - Visualizing your network topology.
     - Monitoring network health and performance.
     - Troubleshooting network issues across your AWS environment.
   - Access: AWS Management Console -> Network Manager.
 - EC2 Instance Console Output/System Logs:
   - Use Case: Check the EC2 instance's system logs (e.g., /var/log/syslog, /var/log/messages, /var/log/cloud-init.log) and console output for boot errors, network configuration issues, or application errors that might be related to network connectivity.
   - Helpful For:
     - Identifying problems during instance startup related to networking.
     - Looking for error messages from network services.
     - Checking cloud-init logs for instance initialization issues.
   - Access: EC2 Instance -> Actions -> Monitor and troubleshoot -> Get system log or Connect to instance via SSH/EC2 Instance Connect and check log files.
Debugging Workflow Suggestions:
 - Start with the Basics:
   - Use ping to check basic reachability to the destination IP or hostname.
   - Use dig to verify DNS resolution if using hostnames.
   - Use ip a to confirm the EC2 instance has an IP address and the interface is up.
   - Use ip route show to check the routing table.
 - Examine Security Groups and NACLs:
   - Crucial in AWS: Security groups and NACLs are very often the cause of connectivity issues.
   - Review inbound and outbound rules for the EC2 instance's security group and the subnet's NACL.
   - Use AWS VPC Reachability Analyzer to simulate traffic paths and check rule effectiveness.
 - Trace the Path:
   - Use traceroute or mtr to see where the connection is failing along the path.
   - This can help identify if the issue is within your VPC, in the internet, or at the destination.
 - Inspect Network Traffic (If Needed):
   - Use tcpdump to capture network traffic if you need to deeply analyze packets.
   - Analyze tcpdump output directly or use Wireshark for a more visual analysis.
 - Check Logs:
   - Examine EC2 instance system logs and console output for errors.
   - If you have VPC Flow Logs enabled, analyze them to understand traffic flow and rejections.
 - Port Scanning (Use with Caution and Permission):
   - Use nmap to scan ports on the destination if you suspect port blocking issues (e.g., is a specific port open on a server?).
Remember to consider the direction of traffic (inbound vs. outbound) and the protocols involved (ICMP, TCP, UDP) when debugging. In AWS, always prioritize checking Security Groups and NACLs as the first steps in troubleshooting network connection problems.
