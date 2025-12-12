---
aliases: []
confidence: 
created: 2025-09-26T11:13:24Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Update main app url
type:
uid: 
updated: 
version:
---

Of course, I can help with that. It's good news that Alexis can reach the server, even if it's a 404. It means the DNS change made by Telefonica is working correctly and traffic is successfully being routed from their VPN into our cluster's Nginx Ingress controller. The `404 Not Found` error indicates that while Nginx is receiving the request for the new production URL, it doesn't know where to send it.

Based on our work history, this is a classic symptom of a missing or misconfigured Ingress rule. Here's a summary of the situation and a plan to debug it.

## History of This Change

Our records show this `cuh-poc-1` to `cuh-prod-1` transition has been in progress for a little while.

- About a week ago, on **September 18th**, we were discussing the file changes needed to create the `cuh-prod-1` configuration based on the `cuh-poc-1` setup.
- The next day, on **September 19th**, we were planning the certificate issuance for the new hostname and the creation of a CNAME record.
- The email from Alexis today confirms the external DNS part of this work is now complete, and we're seeing the results of that change.

The `404 Not Found` error is the final piece of the puzzle, and it almost certainly points to a configuration gap within our Kubernetes cluster.

## Likely Cause

The Nginx Ingress controller acts as the traffic cop for our cluster. It looks at the hostname of an incoming request (e.g., `cuh-prod-1.fitfile.net`) and uses its rules to route it to the correct internal service. A `404` error from Nginx means it received the request but couldn't find a matching rule for that hostname.

Here is a step-by-step plan to investigate and resolve this.

## Debugging Plan

### 1. Inspect the Ingress Configuration

First, let's verify that an Ingress resource for the new `cuh-prod-1` hostname exists and is correctly configured to point to the right application service.

You can run these commands from the jumpbox you've been using, which I see you were logged into earlier today.

```bash
# List all Ingress resources across all namespaces to find the right one
kubectl get ingress --all-namespaces

# Once you identify the correct namespace (likely 'hie-prod-34' or 'cuh-prod-1'),
# describe the specific ingress resource to check its rules.
# Replace <ingress-name> and <namespace> with the correct values.
kubectl describe ingress <ingress-name> -n <namespace>
```

In the output of the `describe` command, look for a `Rule` where the `Host` is your new production URL (`cuh-prod-1...`). The rule should specify a `Backend` service (e.g., `hie-prod-34-frontend-frontend`) and a `Service Port`. If this rule is missing or incorrect, this is the root cause.

### 2. Check the Nginx Ingress Controller Logs

The ingress controller logs are invaluable. They will show the incoming request and may give a specific reason why it resulted in a 404.

```bash
# Find the name of your Nginx Ingress controller pod
# Based on the audit logs, it's in the 'ingress-nginx' namespace
kubectl get pods -n ingress-nginx

# Tail the logs of the controller pod while Alexis (or you) tries to access the URL
# Replace <nginx-ingress-pod-name> with the name from the previous command
kubectl logs -f <nginx-ingress-pod-name> -n ingress-nginx
```

Look for log lines that contain your new production URL. You might see an error like `no service upstream` or `host not found in ingress rule`, which will confirm our theory.

### 3. Verify the Backend Service is Healthy

The Ingress resource needs to point to a running and healthy service. Let's make sure the target application is working correctly.

```bash
# Check the status of the service the ingress should be pointing to
# (e.g., hie-prod-34-frontend-frontend)
# Replace <service-name> and <namespace>
kubectl get service <service-name> -n <namespace>

# Check that the pods associated with that service are running
kubectl get pods -n <namespace> -l app=<app-label>
```

The application pods must be in a `Running` state for the Ingress to have a healthy backend to route traffic to.

### 4. Address Alexis's Observations

- **POC Site Still Accessible**: This is very likely due to DNS caching on his machine or local network. he can try clearing her browser cache and flushing her system's DNS cache. It's also possible our old Ingress for `cuh-poc-1` is still active, which we can clean up after we get `cuh-prod-1` working.
- **PROD URL gets an Nginx 404**: This is exactly what the debugging steps above are designed to solve. My strong suspicion is that you will find the issue in Step 1.

By following these steps, you should be able to pinpoint exactly where the configuration is missing. My guess is that we need to either create a new Ingress resource for `cuh-prod-1` or update an existing one to include the new host rule.
