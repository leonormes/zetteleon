---
aliases: []
created: 2025-10-28T11:10:21Z
last_reviewed: ""
modified: 2026-02-01T15:08:17+00:00
status: ""
tags: ["SoftwareEngineering/Networking"]
title: AWS Elastic Load Balancing (ELB)
type: ""
updated: 
---

## <https://youtube.com/watch?v=qpHLRc4Qt1E>\&si=veBzrlo2OP9emkFe

This video provides a comprehensive introduction to AWS Elastic Load Balancing (ELB), explaining key concepts and practical features relevant for cloud architects and DevOps engineers.[^1]

### Overview of AWS Load Balancing

- Elastic Load Balancer (ELB) acts as an intermediary between users and application instances (such as EC2), redirecting and distributing incoming traffic to available resources.[^1]
- Users connect to the ELB rather than directly to EC2 instances, ensuring efficient distribution and response handling.[^1]
- The ELB performs health checks on downstream instances, ensuring only healthy resources receive requests and that failures are masked from users for higher availability.[^1]

### Main Features and Benefits

- Load Distribution: Automatically balances traffic across multiple instances, providing a single point of application access and supporting horizontal scaling.[^1]
- Health Checks: Routinely checks the health of instances (via a configured route—commonly "/health") and reroutes traffic if instances become unhealthy.[^1]
- SSL Termination: Handles HTTPS connections, terminating SSL between client and the ELB, then forwarding requests in HTTP to backend resources; enhances security and simplifies certificate management.[^1]
- Stickiness: Can be configured to keep requests from the same user directed to the same backend instance (using cookies managed by the load balancer itself).[^1]
- High Availability: Operates across multiple availability zones, mitigating risks from zone failures and ensuring continued application access.[^1]
- Integration: Tightly integrated with other AWS services (monitoring, compute, management), and highly configurable via the AWS UI.[^1]
- Cost Considerations: While setting up your own load balancer might seem cheaper, managed ELB reduces total cost of ownership due to reduced maintenance and operational overhead.[^1]

### Types of AWS Load Balancers

| Type | Layer | Protocols Supported | Performance | Use Case | Status |
|:-- |:-- |:-- |:-- |:-- |:-- |
| Classic Load Balancer (CLB) | Layer 4/7 | HTTP, HTTPS, TCP, SSL | Outdated | Legacy apps, basic scenarios | Deprecated[^1] |
| Application Load Balancer (ALB) | Layer 7 | HTTP, HTTPS, WebSockets | Modern, flexible | Microservices, containers, URLs/path routing | Recommended[^1] |
| Network Load Balancer (NLB) | Layer 4 | TCP, SSL, static \& elastic IP | High-performance, low latency | TCP-based high-throughput apps, direct IP | Recommended[^1] |

- Application Load Balancers (ALB) support advanced routing (paths, hostnames), sticky sessions, and work well with ECS, Docker, and multi-app environments.[^1]
- Network Load Balancers (NLB) cater to extreme performance needs, handling millions of requests per second for TCP traffic, and preserve the original client IP.[^1]
- AWS recommends using ALB for HTTP/HTTPS/WebSockets and NLB for TCP traffic, as CLB is deprecated.[^1]

### Practical Configuration Details

- Health Check Setup: Specify port and route (e.g., `/health`). If the response code is 200, the instance is considered healthy; otherwise, traffic is rerouted.[^1]
- Target Groups: ALB allows grouping multiple applications (on same or different machines), making deployment and scaling seamless for microservices architectures.[^1]
- SSL Certificates: ALB and CLB both support SSL termination, simplifying secure access for users.[^1]
- DNS Names: All load balancers are assigned static hostnames (DNS), which should be used for connecting applications, not underlying IPs (which can change).[^1]
- Scaling: Load balancers can scale automatically, but not instantly; for traffic spikes, AWS can "warm up" the ELB on request.[^1]
- Error Codes: 4xx errors typically indicate client-side issues; 5xx errors are from the application.[^1]

### AWS Exam and Practical Tips

- Focus on knowing ALB features like stickiness, health checks, and path/host-based routing for certification and real-world deployment.[^1]
- Remember the "X-Forwarded-For" header for passing the client IP through ALB since backend instances only see the ALB's IP.[^1]
- NLB preserves client IP without header manipulation.[^1]

This summary covers all key points and practical technical details from the AWS Elastic Load Balancing introduction you linked, tailored for developers and DevOps engineers.[^1]

<div align="center">⁂</div>

[^1]: <https://www.youtube.com/watch?v=qpHLRc4Qt1E>\&si=veBzrlo2OP9emkFe
