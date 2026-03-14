---
created: 2026-03-14T09:49:41+00:00
modified: 2026-03-14T11:09:54+00:00
tags: [articles]
title: Easily Replicate your TLD TLS Certificate using Reflector
---

## Easily Replicate Your TLD TLS Certificate Using Reflector

![rw-book-cover](https://miro.medium.com/v2/resize:fit:1200/1*QP-WVWaIwj9VKljNO6LQ9A.png)

### Metadata

- Author: [[Lior Dux]]
- Full Title: Easily Replicate your TLD TLS Certificate using Reflector
- Category: articles
- Summary: Reflector is a Kubernetes tool that helps copy TLS certificates automatically across namespaces. This makes managing and renewing certificates easier and less error-prone. Using Reflector with cert-manager and Reloader creates a smooth, automated workflow for TLS certificate handling.
- URL: <https://medium.com/@lior.dux/easily-replicate-your-tld-tls-certificate-using-reflector-e65047dfcc77>

### Full Document

![](https://miro.medium.com/v2/resize:fit:284/1*Km7EJvtR1jL7IYS1u7yPQQ.jpeg)

#### Introduction

Lately I've came across a neat project, called [kubernetes-reflector](https://github.com/emberstack/kubernetes-reflector), and thought I'd shine some light about it, and show how great it is, with a unique use case regarding TLS certificates.

#### Reflector: Background

> Reflector is a Kubernetes addon designed to monitor changes to resources (secrets and configmaps) and reflect changes to mirror resources in the same or other namespaces.

Reflector is an FOSS (Our favourite!) project created by emberstack.

This kubernetes controller can be used to replicate secrets, configmaps and certificates.

#### WARNING

If you had read my articles so far (and if not make sure you do!), you are probably aware to the way I do things. Automation is great, and most thing should be automated, but with security in mind. That being said, I DO NOT RECOMMEND secret management using this tool / method. That is why I had created the [External Secrets Operator](https://medium.com/@lior.dux/external-secrets-operator-ddebb60a4230) article in the first place. I am also a firm believer in following GitOps principles, so although it might be nice to have the same ConfigMaps from production reflected across all other environments / staging, I would rather just use [Kustomize](https://kustomize.io/).

#### Well, Then, what is the Use Case?

I'm happy you have asked! Certificates is where I believe this controller shines brightest. Since [cert-manager](https://cert-manager.io/) versioned 1.5, reflector can easily integrate. Using reflector this way allows us to automatically mirror and distribute the secrets created by the Certificate request procedure.

#### The Scenario

You are following best practices and isolate applications and services using namespaces, while using a TLD (Top Level Domain) wildcard certificate. You have applied a CSR (Certificate Request) using the appropriate manifest, and you wish to use this certificate for different subdomains.

Let's take a look at the certificate lifecycle before going any further:

![](https://miro.medium.com/v2/resize:fit:1614/1*QP-WVWaIwj9VKljNO6LQ9A.png)

![](https://miro.medium.com/v2/resize:fit:1764/1*yCOntlwmDSMWfDkBFobQkQ.png)

#### TL; DR—The Solution

1. Deploy cert-manager (if you haven't already).
2. Deploy the kubernetes-reflector controller.
3. Create a Certificate manifest with the following annotations:

```
apiVersion: cert-manager.io/v1  
kind: Certificate  
...  
spec:  
  secretTemplate:  
    annotations:  
      # Permit for miror creation in the following namespace.  
      reflector.v1.k8s.emberstack.com/reflection-allowed: "true"  
      reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "zmynxx,develeap,develeap-demo-1"  
        
      # Automatically create a miror in the following namespace.  
      reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"  
      reflector.v1.k8s.emberstack.com/reflection-auto-namespaces: "zmynxx,develeap"  
...  
spec:  
...  
  secretName: ingress-demo-tls  
  commonName: "develeap.com"  
  dnsNames:  
  - *.develeap.com  
...
```

1. Use the generated secret in your Ingress manifest.

```
apiVersion: networking.k8s.io/v1  
kind: Ingress  
metadata:  
  name: ingress-demo  
...  
spec:  
  tls:  
    - hosts:  
        - ingress-demo.develeap.com  
      secretName: ingress-demo-tls  
...
```

1. Git add, commit and push (GitOps!).
2. Done!

#### What's the Big Deal?

If you are not using TLS for your web applications / dashboard, your clients are welcomed by multiple warning regarding the security thread of not using TLS, and if you do, you know it has more to it than just [compliance](https://tlscompliance.com/). You would have to renew your certificates yearly (I hope you remembered to set an alert set up in your IT/DevOps/System teams calendar!), and then update all of the necessary secrets across all namespaces. That's alot of manual labor, which is prone to error and bugs. Using Reflector simplify that process.

#### Love Reflector? You Would want to Hear about Reloader

Reflector is great, and you use it widely for ConfigMaps and Secrets, you might have felt that something is missing, having these resources auto-generated and reflected is great—but the resources consuming them would need to be reloaded on every change / update in order for the changes to be reflected. Meet [Reloader](https://github.com/stakater/Reloader)! Another FOSS project meant to tackle just that.

![](https://miro.medium.com/v2/resize:fit:300/1*P8nPjUR89cLqIghc3Jansg.png)Reloader logo

![](https://miro.medium.com/v2/resize:fit:600/1*J0Oyhw7nBca9DjSU_4Qm8Q.png)Reflect tls secrets across namespaces!

#### To Sum up…

We have learned about the pain of working with certificates, and how using cert-manager with reflector make our lifes easier and more automated. We have also got to know how reloader compliments reflector, making this trio the perfect stack.

> Love Reflector? Hate cert-manager? Want me to demonstrate the use of Reloader? Let me know in the comments!
> Either way, enjoy learning, see you in my next article.
