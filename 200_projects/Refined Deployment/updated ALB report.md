---
aliases: []
confidence: 
created: 2025-09-26T08:11:31Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [project/work/mkuh]
title: updated ALB report
type:
uid: 
updated: 
version:
---

Of course. Based on the logs you've provided, here is a detailed report on the system's activity and health.

## Executive Summary

The analysis of the logs from approximately 07:55 to 07:56 BST on 26th September 2025 indicates that the system is **stable and operating correctly**. The interactions between the `bunny` client in the `cuh-prod-1` cluster and the `relay` and `rabbitmq` services in the `hie-prod-34` cluster are successful and free of errors. Each request from `bunny` is received, authenticated, processed (including database and message queue interactions), and responded to without any logged failures. The behaviour observed is consistent with a healthy, functioning system.

---

## System Components and Interaction Flow

The logs reveal a three-part system with a clear client-server interaction pattern:

1. **`bunny` (Client)**: A service running in the `cuh-prod-1` cluster (`pod: hutch-bunny-78fb4f57dc-xkp4p`). Its primary role is to poll for jobs by sending periodic HTTP GET requests to the `relay` service.
2. **`relay` (API/Middleware)**: A service running in the `hie-prod-34` cluster (`pod: hutch-relay-79b7987988-jhmrb`). It acts as the central hub, performing the following actions:
   - Receives HTTP requests from `bunny`.
   - Authenticates the client using Basic Authentication.
   - Executes SQL queries against a database to validate users and check for data.
   - Connects to RabbitMQ to handle messaging tasks.
   - Responds to the `bunny` client.

3. **`rabbitmq` (Message Broker)**: A service in the `hie-prod-34` cluster (`pod: hutch-rabbitmq-0`) that manages message queues. The `relay` service communicates with it using the AMQP protocol.

The typical workflow observed in the logs is a **polling mechanism**:

`bunny` → `relay` → `database` & `rabbitmq` → `relay` → `bunny`

---

## Detailed Log Analysis

The logs show a repeating cycle of successful operations. Let's walk through a single, representative transaction to illustrate the process.

**A Single Successful Transaction (Example from 07:56:21):**

1. **Request Initiation (`bunny`)**:
   - `DEBUG - 26-Sep-25 07:56:21 - Sending get request to https://relay.codisc-eoe-sde.uk/link_connector_api/task/nextjob/[REDACTED]`
   - The `bunny` client in `cuh-prod-1` initiates a request to the `relay` service to fetch the next available job.

2. **Authentication and Processing (`relay`)**:
   - `[07:56:21 INF] Credentials validated for Client: sde-bunny-1`
   - The `relay` service receives the request and successfully authenticates the client `sde-bunny-1` using Basic Authentication.
   - It then executes two very fast (1ms) database commands to look up user and node information in the `AspNetUsers`, `SubNodes`, and related tables.

3. **Message Queue Interaction (`relay` and `rabbitmq`)**:
   - `2025-09-26 07:56:21.647... [info] ... accepting AMQP connection`
   - `2025-09-26 07:56:21.649... [info] ... user 'relay' authenticated and granted access`
   - The `relay` service establishes a connection to RabbitMQ, which is accepted and authenticated successfully. This indicates the two services within the `hie-prod-34` cluster are communicating perfectly.

4. **Response (`relay`)**:
   - `[07:56:21 INF] HTTP GET /link_connector_api/task/nextjob/... responded 204 in 132.4785 ms`
   - The `relay` service sends an **HTTP 204 No Content** response. This is **not an error**. In a polling system, this is the standard, expected response when the client asks for a job but none are available in the queue.

5. **Connection Teardown (`rabbitmq`)**:
   - `2025-09-26 07:56:21.652... [info] ... closing AMQP connection`
   - The connection to RabbitMQ is cleanly closed after the request is handled.

6. **Request Completion (`bunny`)**:
   - `DEBUG - 26-Sep-25 07:56:11 - Response Status: 204`
   - `DEBUG - 26-Sep-25 07:56:11 - No task found. Looking for task...`
   - The `bunny` client receives the `204` response, correctly interprets it as "no job available," and logs that it will continue looking.

This entire cycle repeats consistently throughout the log period for various clients (`sde-bunny-1`, `mkuh-test-user`, `nnuh-test-user`) without any deviation or error messages.

---

## Validation of System Health

Based on the logs provided, we can validate that the system is no longer experiencing the connection failures you mentioned.

- ✅ **No Connection Failures**: There are zero logs indicating timeouts, refused connections, or network-level errors between the `bunny` client and the `relay` service. All requests sent by `bunny` are successfully received and processed by `relay`.
- ✅ **Successful Authentication**: All legitimate client requests (e.g., from `sde-bunny-1`) are successfully authenticated. The only authentication "failures" noted (`Basic was not authenticated. Failure message: Missing Authorization Header`) are for the `/healthz` endpoint, which is expected for automated health probes that do not provide credentials.
- ✅ **Healthy Internal Services**: The `relay` service communicates flawlessly with both its database and the `rabbitmq` service. Database queries are fast, and AMQP connections are established and terminated cleanly.
- ✅ **Passing Health Checks**: The `relay` service consistently responds to `GET /healthz` requests with `200 OK`, indicating that the Kubernetes liveness and readiness probes are passing and the service is healthy and responsive.

## Conclusion

The provided logs paint a picture of a healthy and correctly functioning system. The cross-cluster communication from `bunny` to `relay` is working as expected, and all internal communications within the `hie-prod-34` cluster are also successful. The absence of any error codes, exceptions, or connection timeout messages during this 30-minute window strongly supports your conclusion that the previous connection problems have been resolved.
