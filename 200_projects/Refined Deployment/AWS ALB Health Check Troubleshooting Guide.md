---
aliases: []
confidence: 
created: 2025-09-25T09:18:22Z
epistemic: 
last_reviewed: 
modified: 2025-11-12T14:24:29Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [debug, topic/technology/networking]
title: AWS ALB Health Check Troubleshooting Guide
type:
uid: 
updated: 
version:
---

## Comprehensive Troubleshooting Guide for AWS Application Load Balancer Health Check Failures

**Report Date: 2025-09-25**

### Introduction

The AWS Application Load Balancer (ALB) is a critical component for building scalable, resilient, and highly available applications on the cloud. By distributing incoming traffic across multiple targets, such as Amazon EC2 instances, containers, and IP addresses, the ALB ensures that no single target is overwhelmed. Central to this function is the health check mechanism, a process where the ALB periodically sends requests to its registered targets to verify their operational status. Only targets that respond successfully to these health checks are considered "healthy" and eligible to receive traffic. When a target fails these checks, the ALB marks it as "unhealthy" and temporarily removes it from the pool of available targets, thereby protecting end-users from potential service disruptions.

However, diagnosing the root cause of health check failures can be a complex undertaking. While initial troubleshooting often focuses on network connectivity issues like misconfigured security groups or network ACLs, many failures stem from more subtle problems within the application, its SSL/TLS configuration, or the health check settings themselves. This guide provides a comprehensive, systematic framework for troubleshooting ALB health check failures, specifically designed for AWS administrators and engineers who encounter scenarios where targets are marked as unhealthy despite seemingly correct network configurations. It offers actionable diagnostic steps, detailed explanations of common root causes, and specific remediation strategies for issues related to backend connectivity, SSL/TLS handshakes, and nuanced ALB configurations. By following this structured approach, users can efficiently isolate and resolve the underlying problems, restoring application availability and ensuring the reliability of their architecture.

### Foundational Diagnostic Steps for Unhealthy Targets

The initial phase of troubleshooting any ALB health check failure involves a systematic verification of the target's status and the health check configuration. This foundational analysis helps to quickly identify the most common misconfigurations and provides critical context through reason codes, which guide subsequent, more detailed investigation. A methodical approach at this stage prevents unnecessary exploration of more complex issues and often leads to a rapid resolution.

#### Verifying Target Health Status and Reason Codes

The first step in any diagnostic process is to confirm the current health status of the targets and identify the specific reason for any failures. The AWS Management Console and the AWS Command Line Interface (CLI) are the primary tools for this task. Within the EC2 console, navigating to the "Target Groups" section and selecting the relevant group will display a "Targets" tab. This view provides a real-time status for each registered target, indicating whether it is healthy, unhealthy, or in a transitional state such as "initial" or "draining." Crucially, for any target marked as unhealthy, the "Status details" column will display a reason code. These codes are instrumental in diagnostics, as they offer a precise explanation from the ALB's perspective about why the health check failed. For example, a code of `Target.ResponseCodeMismatch` indicates that the target responded, but with an HTTP status code that did not match the success codes defined in the health check settings. Conversely, a code like `Target.Timeout` signifies that the target failed to respond within the configured timeout period.

For users who prefer automation or command-line access, the AWS CLI offers a powerful way to retrieve this same information. By executing the `aws elbv2 describe-target-health` command with the appropriate target group ARN, an administrator can obtain a detailed JSON or table-formatted output of each target's health. This command can be filtered to show only unhealthy targets, streamlining the process of identifying problematic instances. Common reason codes that may be encountered include `Elb.InitialHealthChecking`, a transient state indicating that the target is still undergoing its initial checks after registration, and `Target.FailedHealthChecks`, a more general code that often points toward connection issues or malformed responses. Understanding these codes is paramount, as they transform the troubleshooting process from guesswork into a targeted investigation based on specific feedback from the load balancer.

#### Initial Health Check Configuration Review

Once the status and reason codes are known, the next logical step is to conduct a thorough review of the health check settings within the target group. Misconfigurations in this area are one of the most frequent causes of health check failures. These settings define the very nature of the request that the ALB sends to the targets. Key parameters include the **Protocol**, which must match what the target application is configured to listen for (e.g., HTTP or HTTPS); the **Port**, which must be the specific port the application is listening on for health check traffic; and the **Path**, which is the URI on the target that the ALB will request. A common mistake is specifying a path that does not exist or that is designed for user traffic, which may involve complex logic and slower response times. For health checks, it is a best practice to use a dedicated, lightweight endpoint, such as `/health` or `/status`, that returns a simple, static success response.

Beyond these basic settings, the timing and success criteria are equally critical. The **HealthCheckTimeoutSeconds** parameter defines how long the ALB will wait for a response before considering the check a failure. If an application's health check endpoint performs any processing that could delay the response, this timeout may need to be increased from its default value. The **HealthCheckIntervalSeconds** setting controls the frequency of the checks, while the **UnhealthyThresholdCount** and **HealthyThresholdCount** determine how many consecutive failed or successful checks are required to change a target's status. Finally, the **Matcher** setting specifies the expected HTTP success codes. By default, this is `200`, but if the application's health endpoint is designed to return other success codes (e.g., `200-299`), this setting must be adjusted accordingly to prevent `Target.ResponseCodeMismatch` failures. A meticulous review of each of these parameters against the known behavior of the backend application is essential for ruling out simple configuration errors.

#### Simulating Health Checks for Direct Verification

To definitively determine whether a health check failure originates from the ALB-to-target communication path or from the target application itself, it is highly effective to simulate the health check request directly. This involves bypassing the ALB and sending a request to the target's private IP address from a machine within the same VPC, typically another EC2 instance. The `curl` command-line utility is an excellent tool for this purpose. A successful simulation provides strong evidence that the target application is functioning correctly, pointing the investigation toward network configurations or ALB-specific settings. Conversely, a failed simulation confirms that the issue lies with the target instance or the application running on it.

When performing this simulation, it is crucial to replicate the ALB's health check request as closely as possible. The ALB includes a specific User-Agent header in its health check requests: `ELB-HealthChecker/2.0`. Therefore, the simulation command should include this header to ensure the application does not treat the request differently. A comprehensive `curl` command for this purpose would look like: `curl -vkso /dev/null -H "User-Agent: ELB-HealthChecker/2.0" HealthCheck_protocol://Target_IP:HealthCheck_port/HealthCheck_path`. The `-v` flag provides verbose output, which is invaluable for debugging connection and SSL/TLS issues, while the `-I` flag can be used to fetch only the headers and confirm the HTTP status code returned by the application. By executing this command, an administrator can directly observe the response code, measure the response time, and identify any connection errors, providing clear, actionable data to guide the next phase of troubleshooting.

### Advanced Troubleshooting for Backend Connectivity and Application Issues

After validating the fundamental health check configurations and performing direct simulations, the investigation must proceed to a deeper analysis of the backend environment. This phase focuses on the intricate layers of network security, the operational state of the target instances, and the behavior of the application itself. Issues in these areas are often more complex and require a more granular approach to diagnostics, involving the inspection of security rules, system services, and application logs.

#### Investigating Network and Security Layer Misconfigurations

Although initial checks may suggest that network configurations are correct, it is imperative to perform a meticulous re-verification of all network and security components that mediate communication between the ALB and its targets. A common point of failure is the Amazon EC2 security groups. The security group attached to the target instances must contain an inbound rule that explicitly allows traffic from the ALB on the specific port and protocol defined in the health check settings. A best practice is to source this rule from the ALB's own security group ID rather than using a broad IP address range. This creates a tightly coupled rule that automatically adapts if the ALB's nodes change. Similarly, the ALB's security group must have an outbound rule that permits traffic to the targets on that same port.

Beyond security groups, network ACLs (NACLs) operate at the subnet level and can also block health check traffic. NACLs are stateless, meaning that explicit rules must be created for both inbound and outbound traffic. The subnet's inbound NACL must allow traffic from the ALB's nodes on the health check port. Critically, the outbound NACL must allow traffic on the ephemeral port range (1024-65535), as this is required for the target to send its response back to the ALB. A misconfiguration in the outbound NACL is a frequent cause of `Target.Timeout` errors, as the target's response is blocked before it can reach the load balancer. Finally, route tables within the VPC must be correctly configured to ensure a valid path exists between the ALB's subnets and the target's subnet. Any of these network security layers, if misconfigured, can silently drop health check packets, leading to persistent and often confusing failures.

#### Diagnosing Application and Instance-Level Failures

If the network path is confirmed to be clear, the focus must shift to the health of the target instance and the application running on it. The first step is to ensure that the application service is actually running. On a Linux-based instance, this can be verified using commands like `sudo service httpd status` or `systemctl status nginx`. On Windows, the Task Manager or Services console can be used to confirm the status of the web server process. If the service is stopped, it must be started, and it should be configured to launch automatically on boot to prevent recurrence.

Once the service is confirmed to be running, the next step is to verify that it is listening on the correct network interface and port. Tools like `netstat -an | grep LISTEN` or `ss -nral | grep LISTEN` on Linux can show all listening ports. This check is crucial because an application might be configured to listen only on the localhost interface (127.0.0.1), making it inaccessible to external requests from the ALB. The application must be bound to `0.0.0.0` or the instance's private IP address to accept health check traffic. Furthermore, resource exhaustion on the target instance can lead to health check timeouts. High CPU utilization, memory pressure, or disk I/O contention can slow the application's response time to the point where it exceeds the health check timeout threshold. Monitoring tools like Amazon CloudWatch or instance-level utilities can help correlate periods of high resource usage with health check failures, suggesting that the instance may be under-provisioned or that the application has a performance bottleneck.

#### Analyzing Application Responses and Logs

When the application is running and listening correctly, the final area of investigation at the backend level is the application's logic and its response to health check requests. The application logs are an invaluable resource for this analysis. By examining the web server's access logs, an administrator can confirm whether the ALB's health check requests, identifiable by their `ELB-HealthChecker/2.0` User-Agent, are reaching the application. The logs will also show the HTTP status code that the application returned for each of these requests. If the logs show a status code of `404 Not Found` or `500 Internal Server Error`, it directly explains a `Target.ResponseCodeMismatch` failure.

The application's error logs may provide further insight into why an incorrect status code is being returned. The issue could be as simple as a misconfigured virtual host that does not correctly handle requests sent to the instance's private IP address, which is how the ALB communicates with the target. Some web server configurations require an explicit server name or alias that matches the IP address for the request to be processed by the correct virtual host. In other cases, the application logic at the health check endpoint itself may be flawed, encountering an error or containing conditional logic that results in a non-200 response under certain circumstances. A thorough review of the code and logs is necessary to uncover these application-level issues that are invisible from the network perspective.

### Resolving SSL/TLS Handshake Failures in HTTPS Health Checks

When health checks are configured to use the HTTPS protocol, a new layer of complexity is introduced: the SSL/TLS handshake. A failure at any point during this cryptographic negotiation between the ALB and the target will prevent a secure connection from being established, causing the health check to fail. These failures often manifest as `Target.FailedHealthChecks` and can be a precursor to `502 Bad Gateway` errors for user traffic, indicating a fundamental problem in secure communication with the backend.

#### Understanding SSL/TLS Failures and 502 Bad Gateway Errors

An SSL/TLS handshake is a multi-step process that involves the client (ALB) and server (target) agreeing on a protocol version, selecting a cipher suite, and authenticating the server via its digital certificate. If the ALB cannot successfully complete this handshake with a target, it cannot verify the target's health or forward client requests to it over HTTPS. This results in the target being marked as unhealthy. When a client sends an HTTPS request to the ALB, and the ALB is unable to establish a secure connection with any healthy backend target, it cannot fulfill the request and returns an HTTP `502 Bad Gateway` error. Therefore, troubleshooting SSL/TLS handshake failures is critical not only for resolving health check issues but also for ensuring the overall availability of the application. CloudWatch metrics can help differentiate the source of these errors; an increase in the `TargetConnectionErrorCount` metric often correlates with SSL/TLS handshake problems, while the `HTTPCode_ELB_502_Count` metric signals that the ALB itself is generating the 502 error, frequently due to these backend connectivity failures.

#### Common Causes of SSL/TLS Handshake Failures

Several distinct issues can cause an SSL/TLS handshake to fail between the ALB and a target. One of the most common is a **cipher suite mismatch**. The ALB uses a configurable security policy for its backend connections, which dictates the set of supported TLS protocols and cipher suites. If the target server is not configured to support any of the cipher suites offered by the ALB in its `ClientHello` message, the handshake will fail because no common encryption algorithm can be agreed upon. This is often seen with older or non-standard server configurations that do not support modern, secure ciphers.

Another frequent cause is related to the **SSL/TLS certificate** installed on the target server. The handshake will fail if the certificate is expired, is self-signed by an untrusted authority, or if its Common Name (CN) or Subject Alternative Name (SAN) does not match the domain name the ALB is attempting to connect to. Furthermore, an **incomplete certificate chain** can cause validation to fail. If the target server does not present the necessary intermediate certificates along with its server certificate, the ALB may be unable to trace a path back to a trusted root certificate authority, leading it to reject the connection. Finally, network-level events, such as a premature TCP `RST` (reset) packet sent from the target, can abruptly terminate the connection during the handshake. This can be caused by the target's keep-alive timeout being shorter than the ALB's idle timeout, or by an intervening firewall or security appliance.

#### Diagnostic and Remediation Steps for SSL/TLS Issues

Troubleshooting SSL/TLS handshake failures requires specialized tools to inspect the secure connection process. The `openssl s_client` command-line utility is indispensable for this purpose. By running a command like `openssl s_client -connect target_ip:443 -servername your_domain`, an administrator can simulate the TLS handshake from a machine within the VPC and receive detailed output. This output will reveal the certificate chain presented by the server, the negotiated protocol version and cipher suite, and any verification errors. This allows for direct validation of the certificate's validity, expiration date, and domain name matching.

If a cipher mismatch is suspected, the `openssl` command can be used to test for support of specific ciphers. The remediation involves reconfiguring the target web server (e.g., Apache, Nginx) to enable support for modern, secure cipher suites that are compatible with the ALB's security policy. If the certificate is the issue, a new, valid certificate from a trusted Certificate Authority must be installed on the target, ensuring it includes the correct domain names and that the full certificate chain is served correctly. To address premature connection closures, it is essential to review and align the keep-alive and idle timeout settings on both the target server and the ALB. The target's keep-alive timeout should always be configured to be longer than the ALB's idle timeout to prevent the target from closing connections that the ALB considers active. By systematically diagnosing and remediating these SSL/TLS configuration issues, administrators can restore secure communication and resolve related health check failures.

### Addressing Complex ALB Configuration and Protocol-Specific Issues

Beyond standard connectivity and application-level problems, health check failures can sometimes be traced back to more nuanced aspects of the ALB's configuration or incompatibilities with specific communication protocols. Fine-tuning health check timing parameters, addressing protocol-specific behaviors like those in HTTP/2, and leveraging advanced monitoring are key to resolving these complex cases and building a proactively managed, resilient system.

#### Managing Health Check Timeouts and Thresholds

The timing parameters of an ALB health check are a delicate balance. While the default settings are suitable for many applications, they may not be appropriate for applications with variable response times or those that perform complex operations as part of their health check. The `HealthCheckTimeoutSeconds` setting is particularly critical. If a target's health check endpoint occasionally takes longer to respond than this configured timeout, it will result in intermittent failures. This can cause "flapping," where a target cycles between healthy and unhealthy states. The solution is to either optimize the health check endpoint for a faster response or to carefully increase the timeout value to accommodate the application's expected performance.

Similarly, the `HealthCheckIntervalSeconds`, `HealthyThresholdCount`, and `UnhealthyThresholdCount` settings collectively determine the responsiveness and stability of the health check system. A short interval with a low unhealthy threshold will cause the ALB to react very quickly to a failing target, but it may also be overly sensitive to transient network blips or brief application stalls. Conversely, a longer interval and a higher threshold will make the system more tolerant of temporary issues but will delay the removal of a genuinely failed target from service. The optimal configuration depends on the specific application's requirements for failover speed versus stability. For critical applications, it may be necessary to tune these parameters based on performance testing and historical data to minimize both false positives and false negatives.

#### Troubleshooting Protocol-Specific Failures (HTTP/2)

The Application Load Balancer supports routing traffic to targets using the HTTP/2 protocol, which offers performance benefits such as multiplexing and header compression. However, enabling HTTP/2 for a target group can sometimes introduce new health check failures if the backend application is not fully compliant or correctly configured for the protocol. Health checks may begin to fail immediately after switching the target group protocol version to HTTP/2, even if they were succeeding with HTTP/1.1. This often indicates an incompatibility in the target's HTTP/2 implementation.

Troubleshooting these issues requires verifying that the application server (e.g., Nginx, Apache with `mod_http2`) is properly configured for HTTP/2 and that there are no known bugs or limitations in the specific version being used. The application logs on the target may contain errors related to protocol negotiation or stream processing that are specific to HTTP/2. In some cases, the application may support HTTP/2 for general traffic but have issues with the specific type of request used by the health checker. As a diagnostic step, temporarily reverting the target group's protocol version back to HTTP/1.1 can confirm if the issue is protocol-specific. If it is, the resolution may involve upgrading the web server software, adjusting its HTTP/2 configuration settings, or, if a fix is not readily available, continuing to use HTTP/1.1 for health checks while investigating the application-level incompatibility.

#### Leveraging Monitoring and Logging for Proactive Management

A reactive approach to troubleshooting, where investigation begins only after a failure occurs, is often insufficient for maintaining high availability. A proactive strategy built on comprehensive monitoring and logging is essential for identifying and addressing potential issues before they impact users. Amazon CloudWatch provides several key metrics for this purpose. Monitoring `UnHealthyHostCount` provides a direct measure of target health, and setting a CloudWatch Alarm on this metric can provide immediate notification when any target fails its health checks. The `TargetConnectionErrorCount` metric is also valuable, as it tracks failed connections between the ALB and targets, often pointing to underlying network or SSL/TLS issues.

In addition to metrics, ALB access logs are a rich source of diagnostic information. By enabling access logging, every request handled by the ALB is recorded with detailed attributes, including the target IP address, processing times, and the status codes returned by both the ALB and the target. Analyzing these logs can reveal trends, such as a specific target consistently returning 5xx errors or experiencing high latency, which may be precursors to health check failures. By ingesting these logs into a tool like Amazon Athena or a third-party log analysis platform, administrators can run complex queries to identify patterns, correlate events, and gain deep insights into the health and performance of their application architecture, enabling them to move from a reactive to a predictive and proactive operational model.

### Conclusion

Successfully diagnosing and resolving AWS Application Load Balancer health check failures requires a structured and multi-faceted approach that extends far beyond basic network troubleshooting. While verifying network paths, security groups, and ACLs is a necessary first step, the root cause of unhealthy targets frequently lies deeper within the system's architecture. This guide has outlined a systematic methodology that begins with foundational checks of health status and configuration, progresses to in-depth analysis of backend application behavior and connectivity, and addresses the complexities of SSL/TLS handshakes and protocol-specific issues.

The key to effective troubleshooting is methodical investigation. By leveraging reason codes provided by the ALB, simulating health checks directly, and meticulously examining application logs and server configurations, administrators can isolate the precise point of failure. Whether the problem is a mismatched response code, a slow application endpoint causing a timeout, an invalid SSL certificate, or a subtle protocol incompatibility, a targeted diagnostic process is the most efficient path to resolution. Furthermore, a proactive stance, supported by robust monitoring of CloudWatch metrics and detailed analysis of access logs, empowers teams to detect and mitigate issues before they escalate into service-affecting outages. By embracing this comprehensive and layered troubleshooting philosophy, organizations can ensure the resilience and high availability of their applications, fully realizing the benefits of the AWS cloud.

### References

[Health checks for your target groups - Amazon Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)

[Troubleshoot your Application Load Balancers - Amazon Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html)

[How do I troubleshoot and fix failing health checks for Application Load Balancers? - AWS re:Post](https://repost.aws/knowledge-center/elb-fix-failing-health-checks-alb)

[Check the health of your targets - Amazon Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/check-target-health.html)

[How do I troubleshoot the HTTP 502: bad gateway error in Application Load Balancer? - AWS re:Post](https://repost.aws/knowledge-center/elb-alb-troubleshoot-502-errors)

[Troubleshoot health checks - Amazon Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/ts-elb-healthcheck.html)

[Modify the health check settings of a target group - Amazon Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/modify-health-check-settings.html)

[Troubleshooting Unhealthy Hosts with Application Load Balancer - AWS TV](https://aws.amazon.com/awstv/watch/c326d7c3e9c/)

[HTTP 502: Bad Gateway - Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/http-502-bad-gateway.html)

[Health check failure with HTTP/2 in an ALB target group but succeeding with HTTP1.1 - AWS re:Post](https://repost.aws/questions/QUlKH3uu4mSI6ocMjBEMk1BA/health-check-failure-with-http-2-in-an-alb-target-group-but-succeeding-with-http1-1)

[Application Load Balancer getting 502 bad gateway error with Windows Server 2022 - AWS re:Post](https://repost.aws/questions/QUbB44ZGVKTQeRaDiH3hXdrw/application-load-balancer-getting-502-bad-gateway-error-with-windows-server-2022)

[Target groups showing instances unhealthy - AWS re:Post](https://repost.aws/questions/QU9awe2gncTTm5eEbPZqahQw/target-groups-showing-instances-unhealthy)

[EC2 instance attached to a load balancer is showing unhealthy status - Stack Overflow](https://stackoverflow.com/questions/47766584/ec2-instance-attached-to-a-load-balancer-is-showing-unhealthy-status)

[AWS Application Load Balancer time out on health check - Stack Overflow](https://stackoverflow.com/questions/77815181/aws-application-load-balancer-time-out-on-health-check)

[AWS: Our site throws a 502 when we use our certificate - Server Fault](https://serverfault.com/questions/1025387/aws-our-site-throws-a-502-when-we-use-our-certificate)

[502 Bad Gateway error of ALB + Istio when using HTTPS - Stack Overflow](https://stackoverflow.com/questions/73564712/502-bad-gateway-error-of-alb-istio-when-using-https)

[AWS Load Balancer 502 Bad Gateway - Stack Overflow](https://stackoverflow.com/questions/68729329/aws-load-balancer-502-bad-gateway)

[AWS Target Group Unhealthy Status - Reddit](https://www.reddit.com/r/aws/comments/1bd4wjg/aws_target_group_unhealthy_status/)

[How to troubleshoot an AWS ELB 5xx surge - Netdata](https://www.netdata.cloud/academy/aws-elb-surge-investigation/)

[AWS ALB Target Group Unhealthy - How to Fix 404 Error - YouTube](https://www.youtube.com/watch?v=SEp-dLGOG3E)
