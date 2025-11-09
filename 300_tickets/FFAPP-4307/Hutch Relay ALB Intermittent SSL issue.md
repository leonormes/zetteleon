---
aliases: []
confidence: 
created: 2025-09-25T09:28:24Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Hutch Relay ALB Intermittent SSL issue
type:
uid: 
updated: 
version:
---

Hutch Relay ALB Intermittent SSL issue

Description

We are still experiencing the intermittent ssl timeout on one of the IPs of the SDE Relay server ALB.

This is causing Cohort Discovery queries to fail from HDRUK.

We need to fix this preferably before SDE users begin to test the functionality.

Of course. Here is a detailed breakdown of the events occurring in the logs you've provided.

---

## High-Level Summary

Overall, the logs show a system where the **`bunny`** service is attempting to poll the **`relay`** service for jobs every 20-30 seconds. However, every attempt from `bunny` is failing due to a network-level **SSL/TLS error** before a successful connection can be established.

Meanwhile, the **`relay`** service is operating correctly on its own. It is successfully polling an external service (`rquest.preprod.hdruk.cloud`) for jobs every 5 seconds (finding none), handling health checks, and performing internal database maintenance.

The issue is not with the `relay` service's application logic, but with the network path or TLS configuration between `bunny` and `relay`.

---

## ## The `bunny` Service (Cluster: `cuh-prod-1`)

This service's logs indicate a single, repeating pattern: an attempt to poll the `relay` service followed immediately by a critical network error.

- **Polling Attempt**: Every 20-30 seconds, `bunny` attempts to make an HTTPS request to the `relay` service. This is visible in the debug logs:

  > `DEBUG - 25-Sep-25 08:29:32 - Sending get request to https://relay.codisc-eoe-sde.uk/link_connector_api/task/nextjob/[REDACTED] with data None and kwargs {}`

- **Critical Network Error**: Every single attempt fails with an `SSLError`.

  > `ERROR - 25-Sep-25 08:29:42 - Network error occurred: ... (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1032)')))`
  - **What this means**: This is an error during the TLS handshake, which secures the HTTPS connection. The message `UNEXPECTED_EOF_WHILE_READING` indicates that the `bunny` service was trying to read data from the `relay` service to establish a secure connection, but the `relay` side closed the connection unexpectedly. This almost always points to an issue with a network device (like an ingress controller or load balancer) or a misconfiguration in the TLS/SSL settings between the two clusters.

---

## ## The `relay` Service (Cluster: `hie-prod-34`)

The `relay` service appears to be healthy and is performing several distinct, periodic actions.

- **External Polling for Jobs**: The primary task of this service is polling an external RQuest API every 5 seconds to see if there are new jobs.
  - It sends two `GET` requests to `https://rquest.preprod.hdruk.cloud/...`
  - In every case during this log period, it receives an **`HTTP 204 No Content`** response, which is confirmed by its own debug message: `DBG] No Jobs waiting for RQ-CC...` This is normal behaviour when no jobs are available.
- **Internal Database Maintenance**: Every 5 seconds, the service runs a background task to check for tasks that might be expiring. This involves a simple SQL query to its own database.

  > `[08:30:26 INF] Finding Tasks that are expiring... <s:Hutch.Relay.Services.Hosted.TaskCompletionHostedService>`
  > `SELECT r."Id", r."Collection", ... FROM "RelayTasks" AS r WHERE r."CompletedAt" IS NULL`

- **Handling Health Checks**: The service is frequently hit by Kubernetes health probes on the `/healthz` endpoint.
  - It correctly responds with **`HTTP 200`**, indicating it is healthy.
  - These requests generate an informational message `Basic was not authenticated. Failure message: Missing Authorization Header`. This is expected, as Kubernetes health probes do not provide credentials. The key thing is that the service is up and responding.
- **Handling Authenticated API Requests**: The logs show successful authenticated requests from clients like `sde-bunny-1`, `nnuh-test-user`, and `mkuh-test-user`.

  > `[08:27:46 INF] Credentials validated for Client: sde-bunny-1`
  - This is interesting because it shows that **some** clients *can* successfully authenticate. However, the recurring `SSLError` in the `bunny` logs suggests that `bunny`'s connection attempts are failing *before* they even reach the `relay` application layer to be logged like this.

---

## ## The `rabbitmq` Service (Cluster: `hie-prod-34`)

The RabbitMQ logs are straightforward and indicate healthy operation. They show the `relay` service connecting and disconnecting periodically.

> `2025-09-25 08:30:19.811960+00:00 [info] <0.780276.0> connection ... user 'relay' authenticated and granted access to vhost '/'`
> `2025-09-25 08:30:19.817207+00:00 [info] <0.780276.0> closing AMQP connection...`

This confirms that the `relay` service has correct connectivity and credentials for the message queue within its own cluster.

---

## ## Overall Summary and Conclusion

The logs paint a clear picture of a **unidirectional communication failure**.

1. The `relay` service and its dependencies (`rabbitmq`, its database) in cluster `hie-prod-34` are all functioning as expected.
2. The `bunny` service in cluster `cuh-prod-1` is attempting to communicate with `relay` but is being stopped by an **SSL/TLS layer error**.
3. Because the `relay` service's application logs don't show any failed requests from `bunny` (only successful ones from other clients), the problem likely resides in the networking infrastructure **between** the `bunny` pod and the `relay` pod. This could be:
   - An **Ingress Controller** or **Load Balancer** in front of the `relay` service.
   - A **Network Policy** in either cluster.
   - A **Firewall** between the two clusters.
   - A **mismatch in TLS versions or cipher suites** supported by `bunny`'s client library and the `relay`'s ingress/server.
