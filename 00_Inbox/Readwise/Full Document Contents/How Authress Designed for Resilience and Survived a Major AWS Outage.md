---
aliases: []
tags: []
title: How Authress Designed for Resilience and Survived a Major AWS Outage
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-04T11:35:33+00:00
modified: 2026-01-05T16:59:11+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# How Authress Designed for Resilience and Survived a Major AWS Outage

![rw-book-cover](https://res.infoq.com/news/2025/12/infrastructure-resilience-aws/en/headerimage/aws-reliability-dns-1766915460180.jpg)

## Metadata

- Author: [[Sergio De Simone]]
- Full Title: How Authress Designed for Resilience and Survived a Major AWS Outage
- Category: #articles
- Summary: Authress stayed up during a major AWS outage by using multi-region deployment and DNS dynamic routing to fail over traffic quickly. They avoid relying on AWS control-plane checks and run custom health checks across their stack to detect incidents. They also use CloudFront with Lambda@Edge and keep infrastructure simple to reduce complexity and improve resilience.
- URL: https://share.google/Ghikp1OtmsfYhcfDL

## Full Document

Identity and authentication services company Authress shared [its strategy to stay operational during major cloud infrastructure outages](https://authress.io/knowledge-base/articles/2025/11/01/how-we-prevent-aws-downtime-impacts) like the massive [October 2025 AWS outage](https://www.infoq.com/news/2025/11/aws-dynamodb-outage-postmortem/) that disrupted many major services. The company's resilience architecture relies on [strategies](https://www.infoq.com/news/2025/11/aws-disruption-cloud/) such as multi-region deployment and minimizing reliance on AWS control-plane services, Authress CTO Warren Parad explains.

Parad says the AWS October 20 incident was the worst seen in a decade. Even so, Authress maintained its SLA reliability commitments thanks to a *reliability-first* design centered on a *failover routing strategy*.

>  Simply put—our strategy is to utilize DNS dynamic routing. This means requests come into our DNS and it automatically selects between one of two target regions, the primary region that we're utilizing or the failover region in case there's an issue.

![](https://imgopt.infoq.com/fit-in/3000x4000/filters:quality(85)/filters:no_upscale()/news/2025/12/infrastructure-resilience-aws/en/resources/1route53-failover-1766915458757.png)

A critical part of this approach is rapid incident detection, enabling the DNS layer to determine when to switch traffic between regions. Parad notes that Authress intentionally avoids relying on AWS Route 53’s default health checks or any third-party service to monitor availability:

>  We wouldn't know if that's an issue of communication between AWS's infrastructure services, or an issue with the default Route 53 health check endpoint, or some entangled problem with how those specifically interact with our code that we're actually utilizing.

Authress custom solution performs several checks across the database, SQS, and the core authorizer logic, while also profiling end-to-end request latency. This allows them to reliably determine whether the primary region, out of six total, is experiencing issues and to update the DNS accordingly.

Parad notes that while this failover strategy is a solid starting point, it has limitations. Most notably, it cannot easily isolate and replace a single failing component. To address this, Authress designed an edge-optimized architecture that uses AWS CloudFront with AWS Lambda@Edge for compute.

This architecture offers two benefits: it brings Authress services closer to their users, reducing latency, and it enables a more robust failover strategy.

>  Using CloudFront gives us a highly reliable CDN, which routes requests to the locally available compute region. From there, we can interact with the local database. When our database in that region experiences a health incident, we automatically failover, and check the database in a second adjacent region. And when there's a problem there as well, we do it again to a third region.

![](https://res.infoq.com/news/2025/12/infrastructure-resilience-aws/en/resources/1edge-failover-1766915458757.gif)

An additional element in Authress's overall resilience strategy addresses application-level failures. Parad acknowledges that writing completely bug-free code is nearly impossible, and systems should be designed with this reality in mind.

Hacker News reader `rdoherty` notes:

>  This is probably one of the best summarizations of the past 10 years of my career in SRE. Once your systems get complex enough, something is always broken and you have to prepare for that. Detection & response become just as critical as pre-deploy testing.

Some commenters raised concerns that automation and IaC can introduce additional points of failure. Parad responded that Authress mitigates this risk by keeping things [simple and small](https://news.ycombinator.com/item?id=45958775):

>  We've split up our infrastructure to go with individual services, so each piece of infra is also straight forward. In practice, our infra is less DRY and more repeated, which has the benefit of avoiding complexity that often comes from attempting to reduce code duplication. The ancillary benefit is that, simple stuff changes less frequently. Less frequent changes [bring] less opportunity for issues.

This is a brief overview of the key elements of Authress’s approach to resilience, which also includes root cause analysis, validation testing, impact assessment, AI-driven filtering of non-incidents, and more. Be sure to check the original article for the full details.

[![](https://cdn.infoq.com/statics_s1_20251230094133/images/profiles/NovciOoQOAYWqYqRQBFo97SuMm0xbUiC.jpg)](https://www.infoq.com/profile/Sergio-De-Simone/)

###### Related Topics:

* [Development](https://www.infoq.com/development/)
* [Architecture & Design](https://www.infoq.com/architecture-design/)
* [DevOps](https://www.infoq.com/Devops/)
* [Cloud](https://www.infoq.com/Cloud/)
* [Infrastructure as Code](https://www.infoq.com/code-infrastructure/)
* [Incident Response](https://www.infoq.com/incident-reponse/)
* [Site Reliability Engineering](https://www.infoq.com/sre/)
* [AWS](https://www.infoq.com/AWS/)
