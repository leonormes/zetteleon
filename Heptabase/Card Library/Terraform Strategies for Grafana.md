# Terraform Strategies for Grafana

The demand for digital solutions to manage electric fleets has become undeniable.

At tb.lx, we build global products with Daimler Truck for their electric vehicles across different regions. These eServices are available through the different local portals, such as Fleetboard, Detroit Connect, and Truckonnect.

This global approach means that, when building the software behind these products, different regions need to be considered.

When it comes to monitoring these solutions, our team has developed strategies to make sure this global setup doesn't interfere with the value we deliver to the customer. It's time to share it with you.

If you use Grafana in your observability stack, you probably have found it difficult to replicate dashboards and alerts across multiple environments and regions. We have also faced this challenge, and to help solve it, we developed strategies using tools we rely on daily.

We use Grafana as our go-to monitoring tool for viewing our dashboards and managing our alerts. To achieve regional redundancy, we have one Grafana instance per region: East Japan, West US, and West Europe, the latter also containing two more instances for development.

However, this poses a challenge: how can we ensure every Grafana instance contains the same dashboard and alerts?

Previously, we were using an in-house solution that would sync dashboards from the development environment to each production instance. The issue with this is that maintaining the setup was cumbersome, the API of Grafana isn't too flexible for this, and it made the solution very brittle, leading to frequent failure.

We went looking for different solutions and, since we are already using Terraform to provision all our infrastructure (as code), why not use it to provision the dashboard and alerts as well? Let's find out how we've achieved it.

## How We Started

Grafana has a Terraform provider, which allows the provision of both alerts and dashboards. But it also isn't very flexible, as it is mostly an abstraction of its API — although it is better than calling it directly. We make use of it, but we add our own tweaks to add our spices to make improvements that boost the developer experience, as much as possible.

We have two different resources to provision; alerts and dashboards. Each has its own solution. Before diving into each, let's first see how we have it structured.

Our infrastructure repositories contain one Terraform source per environment, meaning that we have a separate folder for each, since not all environments have the same needs.

Then we have a repository with templates of dashboards and alerts containing one Terraform module per dashboard/alert, considering variables for any difference in environment (such as the region). This will make it easier to re-use the code of each environment in the infrastructure repository. You simply make use of these modules in the infrastructure code in the environment, where it makes sense.

To effectively provision those dashboard/alert template modules, call our own `terraform-grafana-dashboard` and `terraform-grafana-alert`modules, which in turn makes use of the Grafana provider. In this way, we can reduce any redundancy the resources require, abstracting complexity and keeping our template modules lean.

## Overview

![](https://miro.medium.com/v2/resize:fit:700/1*k_NFI5d_GtirydkOf6-L9g.png)

Overview of the infrastructure repository

To ensure that any changes to a dashboard are first tested in development before going straight to production, we use semantic release on all these modules, both the template and the provisioning ones.

This gives us both safety in applying changes, and ease in creating and replicating for each environment with no failures in the middle.

The way dashboards and alerts are written in code differs from each other. Let's see what each one looks like.

## Dashboards

For dashboards, we take a simpler approach and create the dashboard manually or modify an existing one. Then, we export it directly via the UI, and parameterize the dashboard variables that are team/project-specific to pass in the template function of Terraform. These variables are configured in the dashboard with the type "Constant" to ease this part of templating it.

![](https://miro.medium.com/v2/resize:fit:700/1*VPyqHvzsJTEs38wkfCBl2A.png)

For instance, our JVM (Java/Kotlin) dashboard, used by different teams, needs to take in the Kubernetes namespace, so we replace the "hardcoded" value that is in Grafana for `${kubernetes_namespace}`:

```
{  "schemaVersion": 38,  "style": "dark",  "tags": [    "spring",    "kotlin"  ],  "templating": {    "list": [      {        "hide": 2,        "label": "kubernetes_namespace",        "name": "kubernetes_namespace",        "query": "${namespace}", &lt;-- changed from the real value (e.g. "ns-project-a")        "skipUrlSync": false,        "type": "constant"      },}
```

*JSON cut short since it is huge*

Now, with this JSON, the template module can be written. This module is essentially a folder "spring-boot-dashboard" in the templates' repository. The JSON is stored in a "dashboard.tpl" file (as shown in the path above) and the [variables.tf](http://variables.tf) takes in the "namespace" variable as well as the folder id and title of the dashboard.

The code on [main.tf](http://main.tf) looks like the following:

```
module "spring_boot_dashboard" {  depends_on = [    module.testkube_test_dashboard  ]  source      = "git::https://git.daimlertruck.com/tblx/terraform-module-grafana-dashboard.git/?ref=v1.4.0"  title       = var.title  folder_id   = var.folder_id  config_json = templatefile(("${path.module}/dashboard.tpl"), {    "namespace" : var.namespace  })  tags = [    "Spring",    "Kotlin"  ]}
```

*Notice this is using our dashboard module via version.*

That is the template in the infrastructure code, which is referenced with the only needed variables:

```
module "sgw_spring_boot_dashboard" {  source = "git::https://git.daimlertruck.com/tblx/terraform-grafana-dashboards-alerts.git//dashboards/spring-kotlin-dashboard?ref=v4.16.1"  folder_id = data.grafana_folder.team_folder.id  dashboard = {    title     = "Project A"    namespace = "ns-team-a"  }}
```

As you can see, it is very straightforward for the teams to provision their own dashboards. But what does that terraform-module-grafana-dashboard look like? Take a look:

```
locals {  tags = concat(    ["terraform"], sort([for tag in var.tags : lower(tag)])  )  config_json = jsondecode(var.config_json)  config = merge(local.config_json, {    "title" : var.title    "uid" : random_string.dashboard_uid.result    "tags" : local.tags  })}resource "grafana_dashboard" "dashboard" {  config_json = jsonencode(local.config)  overwrite   = true  folder      = var.folder_id}resource "random_string" "dashboard_uid" {  special = false  length  = 14}
```

The *uid* is required for the dashboard to be provisioned and instead of having that *random_string* block duplicated on each template module, we have it in our own dashboard module. The same goes for the "title" for instance; we don't need to template it in the JSON because we're already overriding it here.

## Alerts

For alerts, we are doing it via code. The alert resource of Grafana's Terraform provider is very verbose and, as was the case in dashboards, it is merely a Terraform representation of the API.

However, our colleague [Nelson Silva](https://www.linkedin.com/in/nesilva/) has written an amazing module that makes writing alerts effortless (he's also the one who implemented the dashboard module). It even looks like it is provided by the Grafana provider.

When calling the module, you simply pass in what is relevant, namely the metadata of the alert (name, annotations), the conditions, and the queries, *et voilà*!

For example, an alert that is triggered when there are no pods for a deployment:

```
module "alert" {  source = "git::https://git.daimlertruck.com/tblx/terraform-module-grafana-alert.git/?ref=v1.5.1"  name             = "No healthy pods"  folder_uid       = var.folder_id  interval_seconds = 60  org_id           = var.org_id  rules = [    {      name           = "No healthy pods"      for            = "2m"            no_data_state  = "OK"      exec_err_state = "OK"      condition      = "C"      annotations = {        summary = "{{ $labels.alertname }} on deployment '{{ $labels.deployment }}'"      }      labels = {        "app" : "service-a",        "team" : "team-name",                "P" : "1"      }      data = [        {          prometheus = {            expr         = "sum(kube_deployment_status_replicas_available{namespace=${var.namespace}) by (deployment)"            legend       = "custom"            legend_value = "{{ deployment }}"            step         = "10s"          }          ref_id = "A"          relative_time_range = {            from = 3600            to   = 0          }        },        {          reduce = {            function = "last"            input    = "A"            mode     = "dropNN"          }          ref_id = "B"          relative_time_range = {            from = 3600            to   = 0          }        },        {          ref_id = "C"          relative_time_range = {            from = 3600            to   = 0          }          threshold = {            input    = "B"            is_below = 1          }        },      ]    }  ]}
```

At first sight, this may seem overwhelming, but if you look closely, the syntax is very straightforward, and these values are shown directly in Grafana. For instance, "ref_id" is what you see in "Input".

![](https://miro.medium.com/v2/resize:fit:700/1*4Vzd2MQZikt5f0ic2K_bDw.png)

We won't go over how the code of this module works but can confirm that it supports all of our needs, including Azure monitor queries.

## Wrap up

This is how we provision the dashboards and alerts, ensuring they are consistent across regions, while being able to choose whether a dashboard should be included in a certain region or not.

With the Grafana Terraform provider (and our colleague Nelson's magic powers), we achieved a lean developer experience. Now, product teams are empowered to ensure our solutions are reliable and perform well, for smoother and more effective monitorization. Being able to monitor different environments and regions efficiently allows us to lower downtime, improve responsiveness, and fix issues even before users get affected. All in all, we're able to provide dispatchers and fleet managers with reliable software to manage and operate their fleets.