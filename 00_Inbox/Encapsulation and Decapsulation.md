---
aliases: []
confidence: 
created: 2025-04-16T07:10:31Z
epistemic: 
last_reviewed: 
modified: 2025-12-08T11:11:58Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking, pdu]
title: Encapsulation and Decapsulation
type: source
uid: 
updated: 
version: 
---

The last item we need to discuss before we move on from the OSI Model is that of Encapsulation and Decapsulation. These terms refer to how data is moved through the layers from top to bottom when sending and from bottom to top when receiving.

As the data is handed from layer to layer, each layer adds the information it requires to accomplish its goal before the complete datagram is converted to 1s and 0s and sent across the wire. For example:

- Layer 4 will add a TCP header which would include a Source and Destination port
- Layer 3 will add an IP header which would include a Source and Destination IP address
- Layer 2 would add an Ethernet header which would include a Source and Destination MAC address

On the receiving end, each layer strips the header from the data and passes it back up the stack towards the Application layers. Here is the whole process in action:

[![OSI Model - Encapsulation and De-Encapsulation](https://www.practicalnetworking.net/wp-content/uploads/2016/01/packtrav-encap-decap.gif)](https://www.practicalnetworking.net/wp-content/uploads/2016/01/packtrav-encap-decap.gif)

Note that this is only an example. The header that will be added will be dependent on the underlying communication protocol. For instance, a UDP header might be added at Layer 4 instead, or an IPv6 header might be added at Layer 3.

Either way, it is important to understand that as data is sent across the wire, it gets passed down the stack and each layer adds its own header to help it accomplish its goal. On the receiving end, the headers get stripped off one at a time, layer by layer, as the data is sent back up to the Application layer.

This article categorizes different network functions into different layers of the OSI model. While essential for understanding how packets move through a network, the OSI model itself is not a strict requirement as much as it is a *conceptual* model — not every protocol will fit perfectly within a single layer of the OSI model.

[[OSI model]]
