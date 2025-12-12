---
aliases: []
confidence: 
created: 2025-11-22T07:33:37Z
epistemic: 
last_reviewed: 
modified: 2025-11-22T14:22:54Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: gateway api
type: 
uid: 
updated: 
---

Gateway API for Ingress-NGINX - a Maintainer's Perspective

There have been a lot of great threads over the past couple of weeks on what Ingress-NGINX users can migrate to after it is retired in March. As a Gateway API maintainer, it's been incredibly helpful to see all the feedback and perspectives on Gateway API, thanks for all the great discussions!

I wanted to take a few minutes to clear up some common points of confusion I've seen in these threads:  

**1) Is Gateway API less stable than Ingress?**  
No. Although there are still some experimental parts of the API, they're not exposed by default (similar to how Kubernetes uses feature gates to hide alpha features). A big difference between the APIs is that Gateway API is still under active development and continues to add more features like CORS, timeouts, etc. Gateway is GA and has been for over 2 years now. It offers a "standard channel" (the default) that is just as stable as Ingress API and has never had a breaking change or even an API version deprecation.

One point worth considering is that most Gateway controllers are far more actively maintained and developed than Ingress controllers where development has largely been paused to reflect the state of the upstream API.

**2) Would it be easier to migrate to a different Ingress controller instead of Gateway API?**  
It might be if you're not using any ingress-nginx annotations. With that said, Ingress-NGINX has a lot of powerful annotations that are widely used. If you choose to move to another Ingress controller, you'll likely have to migrate to another set of implementation-specific annotations given how limited the features of the core Ingress API are.

With Gateway API we've spent a lot of time working to provide more portable features directly in the API and ensuring that implementations are providing a consistent experience, regardless of the underlying data plane. For example, if you choose one of the Gateway API implementations that is [conformant with our latest v1.4 release](https://gateway-api.sigs.k8s.io/implementations/v1.4/), you can have confidence that the behavior of these features will be consistent across each implementation.

**3) Gateway API is missing an Ingress-NGINX feature I need**
While Gateway API supports many more features than the core Ingress API, Ingress-NGINX supports an impressive list of annotations. If we're missing something that you need in Gateway API, please let us know - file an issue, join an OSS meeting, or just leave a comment on this thread.

With that said, even if Gateway API itself doesn't have a feature you need, it's likely that an implementation of the API has a similar or equivalent feature, just as an implementation-specific extension of the API. For example, [GKE Gateway](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/configure-gateway-resources), [Envoy Gateway](https://gateway.envoyproxy.io/contributions/design/backend-traffic-policy/), and many others, extend Gateway API with their own custom policies.

**4) Migrating from Ingress to Gateway API sounds like a lot of work**
While I'm not going to say that any migration like this will be easy, there's a lot of work going into [ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway) right now to make the migration experience better. We're working to add support for the most widely used Ingress-NGINX annotations, to help automate the migration for you. We could really use help and feedback as we're continuing to make progress, we really want to make sure we're doing everything we can to ease the migration.

With all of that said, I hope you'll give Gateway API a shot. If you do try it out, I'd love to hear feedback - what are we getting right? What are we getting wrong? I'll watch this thread for the next couple of days and would be happy to answer any questions.

Ingress isn't going away - it's a GA API which means it will be around until at least Kubernetes 2.0 (and there are no plans for a 2.0 as far as I know). I'd consider it conceptually similar to Endpoints vs EndpointSlices. The Endpoints API still exists, but all new features and development for the past 5+ years have been focused on EndpointSlices, with many new features being built on top of them.

I really wish there were a sustainable way to support an Ingress or Gateway controller within Kubernetes, but this feels a lot like a tragedy of the commons. In the case of Ingress-NGINX, it was incredibly widely used, but maintained entirely by a very small set of volunteers working in their personal time (x-ref [https://xkcd.com/2347/](https://xkcd.com/2347/) ).

With Gateway API, we've benefited from a wide variety of different implementations that we wouldn't have if we'd built one directly into Kubernetes. Many of these are based on different underlying data planes (Envoy, NGINX, HAProxy, Cloud LBs, etc), and this healthy competition has made the ecosystem strong. I think many of these implementations have found sustainable models that will ensure they can exist for years to come, but ultimately the best way to ensure a controller continues is to find a way to support them.
