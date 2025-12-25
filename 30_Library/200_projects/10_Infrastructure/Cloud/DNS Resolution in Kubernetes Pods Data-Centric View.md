---
aliases: []
confidence: "null"
created: 2025-03-15T07:39:42Z
epistemic: "null"
last_reviewed: "null"
modified: 2025-12-25T11:40:44+00:00
purpose: "null"
review_interval: "null"
see_also: []
source_of_truth: []
status: "null"
tags: ["data-centric", "topic/technology/networking/dns"]
title: DNS Resolution in Kubernetes Pods Data-Centric View
type: "null"
uid: 
updated: 
version: "null"
---

To understand where DNS resolution occurs, we need to consider the different layers involved in a containerized application within Kubernetes:

The Application Process (e.g., "bunny" process):

Data Role: The "bunny" process is the consumer of the DNS resolution service. It needs to know the network address (typically an IP address) associated with the name of the "relay" service.

Action: When "bunny" needs to communicate with "relay," it will attempt to use the name of the "relay" service (e.g., relay.private.aws.internal if you've set up private DNS zones as discussed). It doesn't directly perform the DNS lookup itself. It makes a request to the underlying system to resolve this name.

The Container (e.g., Bunny Container):

Data Role: The container provides an isolated environment for the "bunny" process. It inherits network configurations from its parent Pod.

Configuration: When a container is created in Kubernetes, it's set up with a standard network configuration, including DNS settings. This configuration is typically based on the Pod's network setup.

resolv.conf: Inside the container, you'll find a file called resolv.conf. This file is a standard Linux configuration file that lists the DNS name servers that the container should use for name resolution. Kubernetes automatically manages this resolv.conf file within the container.

The Pod (Bunny Pod):

Data Role: The Pod is the fundamental unit of deployment in Kubernetes and shares networking within its containers. It's the Pod that gets the primary network configuration in Kubernetes.

[[Secure Network Plan Azure AKS (Bunny) to AWS EKS (Relay) Communication]]

[[Data-Centric Perspective Secure Cross-Cloud Communication (AWS EKS to Azure AKS)]]
