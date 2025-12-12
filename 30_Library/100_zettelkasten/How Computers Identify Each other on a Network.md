---
aliases: []
confidence: 
created: 2025-05-12T05:13:56Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: How Computers Identify Each other on a Network
type:
uid: 
updated: 
version:
---

An important concept in DNS for us to know is that computers don't use the human friendly names to identify each other. We use something like `www.example.com` , but this is a label so we know what we are talking about. The BBC wants us to easily find their website serving computers. On the big public Internet those servers have a very non specific 'address';

```sh
bbc.co.uk.              130     IN      A       151.101.192.81
bbc.co.uk.              130     IN      A       151.101.0.81
bbc.co.uk.              130     IN      A       151.101.64.81
bbc.co.uk.              130     IN      A       151.101.128.81
```

There are a few addresses for redundancy, but for instance, one of the addresses is `151.101.192.81`.
