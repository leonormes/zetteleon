---
aliases: []
confidence: 
created: 2025-03-17T02:57:22Z
epistemic: 
id: This error message Address is not allowed
last_reviewed: 
modified: 2025-12-13T11:39:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [k8s, networking]
title: error message Address is not allowed
type: 
uid: 
updated: 
version: 
---

This error message, "Address is not allowed," from the `validate.nginx.ingress.kubernetes.io` webhook, indicates a network connectivity issue between your `kubectl` client (running on the jumpbox) and the admission webhook service within your EKS cluster. Let's break down the problem and explore solutions:

## Understanding the Error

- Webhook Validation:
  - Kubernetes admission webhooks intercept API requests (like `kubectl apply`) to validate or mutate them before they're persisted.
  - The `validate.nginx.ingress.kubernetes.io` webhook is specifically designed to validate `Ingress` resources for the NGINX Ingress Controller.
- Network Connectivity:
  - The error "Address is not allowed" suggests that the jumpbox, where you're running `kubectl`, cannot establish a connection to the webhook service at `https://public-ingress-ingress-nginx-controller-admission.public-ingress.svc:443`.
- This could be due to several reasons, including:
  - DNS Resolution: The jumpbox might not be able to resolve `public-ingress-ingress-nginx-controller-admission.public-ingress.svc` to its internal IP address.
  - Firewall/Network Policies: Network policies within the EKS cluster or firewall rules on the jumpbox or within the VPC might be blocking the connection.
  - Service Discovery: There might be an issue with Kubernetes service discovery, preventing the jumpbox from finding the webhook service.
  - TLS Issues: Though less likely in this specific error, there could be TLS certificate validation issues.
- Admin Permissions: While your user has admin permissions on the cluster, that doesn't bypass network connectivity requirements. Admin permissions grant you authorization to perform actions, but they don't guarantee that the network will allow those actions.

## Troubleshooting Steps

1. Verify DNS Resolution:

   - From your jumpbox, try to resolve the service name:

```sh
nslookup public-ingress-ingress-nginx-controller-admission.public-ingress.svc
```

- If it doesn't resolve to an internal cluster IP, there's a DNS issue.
- You can also try to ping the service name, though this might not work if ICMP is blocked:

```sh
ping public-ingress-ingress-nginx-controller-admission.public-ingress.svc
```

- If you have the CoreDNS pods available, you can try and resolve from within the cluster.

```sh
kubectl exec -n kube-system -it $(kubectl get pods -n kube-system -l k8s-app=kube-dns -o jsonpath='{.items[0].metadata.name}') -- nslookup public-ingress-ingress-nginx-controller-admission.public-ingress.svc
```

2. Check Network Policies:

   - Inspect the network policies in the `public-ingress` namespace:

```sh
kubectl get networkpolicies -n public-ingress
```

   - Ensure that network policies aren't blocking connections from your jumpbox's IP range or the namespace where your `kubectl` client is running.
   - If you have any global network policies, verify those as well.

3. Test Connectivity from a Pod:

   - Create a temporary pod within the EKS cluster and try to connect to the webhook service from inside the pod:

```sh
kubectl run -it --rm debug --image=curlimages/curl -- sh
curl -k https://public-ingress-ingress-nginx-controller-admission.public-ingress.svc:443
     ```

- If this works, the issue is likely with the jumpbox's network configuration.
- If it fails, the problem is within the cluster's network.

4. Verify Service Status:

   - Check the status of the `public-ingress-ingress-nginx-controller-admission` service:

```sh
kubectl get svc -n public-ingress public-ingress-ingress-nginx-controller-admission
     ```

   - Ensure that the service has endpoints and that the pods backing the service are running:

```sh
kubectl get endpoints -n public-ingress public-ingress-ingress-nginx-controller-admission
kubectl get pods -n public-ingress -l app.kubernetes.io/name=ingress-nginx -l app.kubernetes.io/component=admission-webhook
```

5. Firewall Rules:

   - Examine the firewall rules on your jumpbox and within the VPC where your EKS cluster resides.
   - Ensure that outbound traffic from the jumpbox to the cluster's internal network (specifically port 443) is allowed.
   - Check security groups associated with the worker nodes.

6. Kubeconfig Context:

   - Double check that the kubeconfig file being used by kubectl, is pointing to the correct cluster.
   - Check your current context:

```sh
kubectl config current-context
```

   - Verify the server address in the kubeconfig.

7. Ingress Nginx Controller Version:

   - Sometimes very old or very new versions of the ingress controller, can have issues. Verify the deployed version, and compare it to the current stable version.

Debugging Tips

- Increase the verbosity of `kubectl` to get more detailed error messages:

```sh
kubectl apply -f echo-ingress.yaml --validate=false -v 9
```

- Check the logs of the `ingress-nginx-controller` and the webhook pods.
- `kubectl logs -n public-ingress -l app.kubernetes.io/name=ingress-nginx -l app.kubernetes.io/component=controller`
- `kubectl logs -n public-ingress -l app.kubernetes.io/name=ingress-nginx -l app.kubernetes.io/component=admission-webhook`

By systematically working through these steps, you should be able to pinpoint the cause of the network connectivity issue and resolve the error.
