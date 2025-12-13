---
aliases: []
author: ["[[alex]]"]
confidence: 
created: 2025-03-27T09:49:25Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source: https://medium.com/@alex067/create-an-aws-api-gateway-to-your-eks-cluster-with-terraform-46cdc91d9cea
source_of_truth: []
status: 
tags: [gateway, ingress, networking]
title: Create an AWS API Gateway to your EKS Cluster (with Terraform)
type: download
uid: 
updated: 
version: 
---

This article is going to focus on how you can leverage an **AWS API Gateway** as your external facing endpoint for your Kubernetes services. We’re going to assume that you have an **EKS** cluster up and running.

But first, why would we even do this? 🤔

In the world of Kubernetes and microservices, there are so many different architectural patterns aiming to solve various pain points around how microservices can communicate with one another, and how traffic is being distributed.

[**One such pattern**](https://microservices.io/patterns/apigateway.html) is to leverage an API Gateway as your central endpoint, which connects to multiple backend services. In a sense, it’s kind of like an ingress-controller but with the functionality of an API server.

And using the managed AWS API Gateway is a great idea, for several reasons:

1. **Speed.** API Gateway is a managed solution that already comes with a host of features like rate limiting, monitoring, custom authorization, etc. You’re getting this out of the box.
2. **Rich Feature Sets**. Features like rate limiting and authorization is already there. The benefit here is that, rate limiting occurs first from AWS before the request even makes it to your Kubernetes cluster. Custom Authorizers allow you to natively integrate to AWS services, like Cognito.
3. **Security.** AWS API Gateway leverages VPC links, which are secure internal communication links between AWS and your VPC. This means, your Kubernetes services are kept strictly internal vs. exposing a public Load balancer.
4. **Lower Operational Costs**. Since API Gateway is entirely managed by AWS, you’re not managing another deployment. And because this is technically a single point of failure, having AWS deal with the burden is not a bad idea.
5. **Easy DNS**. Managing DNS records and TLS certificates can be a pain. Fortunately, with this architecture, our API Gateway is able to perform SSL termination and we’re only managing one single DNS record for multiple backend services.

## Getting Started

There are three main resources we need to make this magic work.

1. AWS API Gateway
2. A VPC link
3. An internal Load balancer created by your Kubernetes service

The API Gateway acts as a proxy into our internal Load balancer via the VPC link. If that sounds confusing, well it’s because it probably is!

[https://aws.amazon.com/blogs/containers/integrate-amazon-api-gateway-with-amazon-eks/](https://aws.amazon.com/blogs/containers/integrate-amazon-api-gateway-with-amazon-eks/)

The VPC link is a private integration endpoint, allowing AWS managed network to securely communicate with our own VPC. The traffic stays internal and never leaves AWS.

Before we get started in any Terraform work, we first need the internal Load balancer up and running.

The VPC link requires an existing, operational internal Load balancer to direct traffic to. It’s important that this Load balancer is **created by your Kubernetes Service.** This is possible by [**installing the AWS Load Balancer Controller add-on into your cluster.**](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)

Once our Cluster is bootstrapped with the necessary add-ons, let’s take a look at an example manifest, utilizing the Service object to create our Load Balancer.

```c
apiVersion: v1
kind: Service
metadata:
 name: foobar-service
 annotations:
   service.beta.kubernetes.io/aws-load-balancer-name: foobar
spec:
 type: LoadBalancer
 loadBalancerClass: service.k8s.aws/nlb
 ports:
 — name: web
 protocol: TCP
 port: 80
 targetPort: web  
 selector:
    app: foobar
```

By using the LoadBalancer type under spec.type, and specifying that we want a Network Load Balancer, the AWS Load Balancer controller takes the request and performs the necessary API calls in your AWS account.

Within a couple of minutes, you’ll have an operational internal Network Load Balancer.

We’re now ready to create our Terraform module, which will create an API Gateway, create the necessary proxy resources, and attach the API Gateway to a VPC link.

As a reminder, the VPC link acts as the middleman, forwarding requests from your API Gateway to your Load Balancer, which then directs the traffic to your Kubernetes service.

```c
resource “aws_api_gateway_vpc_link” “main” {
 name = “foobar_gateway_vpclink”
 description = “Foobar Gateway VPC Link. Managed by Terraform.”
 target_arns = [var.load_balancer_arn]
}
```

First we’ll create our VPC link. The only argument we need to supply it with, is the ARN of the Load Balancer we created earlier.

```c
resource “aws_api_gateway_rest_api” “main” {
 name = "foobar_gateway"
 description = “Foobar Gateway used for EKS. Managed by Terraform.”
 endpoint_configuration {
   types = ["REGIONAL"]
 }
}
```

Then we’ll create a regional API Gateway. Whether it’s Edge or Regional doesn’t matter in context to making this architecture work.

```hcl
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.proxy"           = true
    "method.request.header.Authorization" = true
  }
}

resource "aws_api_gateway_integration" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = "ANY"

  integration_http_method = "ANY"
  type                    = "HTTP_PROXY"
  uri                     = "http://${var.load_balancer_dns}/{proxy}"
  passthrough_behavior    = "WHEN_NO_MATCH"
  content_handling        = "CONVERT_TO_TEXT"

  request_parameters = {
    "integration.request.path.proxy"           = "method.request.path.proxy"
    "integration.request.header.Accept"        = "'application/json'"
    "integration.request.header.Authorization" = "method.request.header.Authorization"
  }

  connection_type = "VPC_LINK"
  connection_id   = aws_api_gateway_vpc_link.main.id
}
```

Here’s where the bulk of the magic happens. Let’s take a look through this block by block.

We want the Gateway to simply proxy our requests into our Kubernetes Service. We really don’t want to be managing independent endpoints.

We’ll create a single resource called **{proxy+}** at the root level, and specify that for the HTTP method, we’ll take **ANY**.

```c
"method.request.path.proxy"           = true
```

In order for the proxy to truly work, we need to tell our Method to accept path as a proxy. Without this, we won’t be able to correctly map the proxy path to our Load Balancer endpoint.

```c
resource "aws_api_gateway_integration" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = "ANY"

  integration_http_method = "ANY"
  type                    = "HTTP_PROXY"
  uri                     = "http://${var.load_balancer_dns}/{proxy}"
  passthrough_behavior    = "WHEN_NO_MATCH"
  content_handling        = "CONVERT_TO_TEXT"

  request_parameters = {
    "integration.request.path.proxy"           = "method.request.path.proxy"
    "integration.request.header.Accept"        = "'application/json'"
    "integration.request.header.Authorization" = "method.request.header.Authorization"
  }

  connection_type = "VPC_LINK"
  connection_id   = aws_api_gateway_vpc_link.main.id
}
```

For the Integration, we set the HTTP method to **ANY**. This again simplifies our entire workflow, where we’re not managing individual resource paths and their various supported HTTP methods.

We set the type to **HTTP\_PROXY**, and for the endpoint we provide an argument of our load balancer DNS.

This is why we needed our Load Balancer created beforehand; to use the ARN and the DNS values for our VPC link.

For the endpoint (the uri argument), we also concatenate the Load Balancer DNS with **/{proxy}.** This proxy template basically gets replaced with the path of the request.

If a request is sent as “user/profile”, that {proxy} template gets replaced with “user/profile”. See how easy that is?

```c
request_parameters = {
    "integration.request.path.proxy"           = "method.request.path.proxy"
    "integration.request.header.Accept"        = "'application/json'"
    "integration.request.header.Authorization" = "method.request.header.Authorization"
  }
```

We finally tell the integration that the {proxy} mapping is coming from our method.

That’s pretty much it.

I’m leaving a lot of the mundane stuff out, like setting up throttling, authentication, DNS, because they’re unrelated to actually getting the API Gateway to communicate with an internal Service in your EKS cluster.
