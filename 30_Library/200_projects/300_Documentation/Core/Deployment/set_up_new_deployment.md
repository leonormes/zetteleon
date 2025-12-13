---
aliases: []
confidence: 
created: 2024-11-05T09:15:29Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: toProcess
tags: []
title: set_up_new_deployment
type:
uid: 
updated: 
version:
---

## Set up New Deployment

Here we have a set of secrets. It is organised

admin/deployments/\<deployment-key\>

It's 09:29

I correct the passwords for monitoring

This might need multiple nodes sharing keys and such.

Central Services

### Dependencies

- We need tf code to do the actual azure or aws deployment(IaC)
- We need a tfc workspace
- we need a gitlab repo to store the tf code for the deployment
- We need secrets in vault
- We need access to vault
- Helm deployment charts
- A helm values file for the deployment. Where is this referenced? The `/FITFILE/Terraform Infrastructure/Non-Production/fitfile-non-production-infrastructure/ff-hyve-2` which is the tf deployment code.
- Deployment Key

### What Files Do I Need to Update

Deployment repo. Has a values.yaml file.

Central services repo:

- auth0/locals.tf
- grafana/locals.t
- hcp/vault/locals.tf
- hcp/tfc/main.tf
`/FITFILE/Terraform Infrastructure/Non-Production/fitfile-non-production-infrastructure`
- \<deploymentKey\>/locals.tf
- all references to the deploymentKey

### TFC

I need to set up a workspace for the hyve2

Once the workspace is set up I need to change the terraform version it uses to be latest, rather than the version it sets at create time.

We need a TFC Project -> Workspace -> Gitlab repo.

The Gitlab repo is already there, and I have added a subfolder.

The tfc terraform needs a new workspace added

The terraform deployment code needs to add this workspace in its versions/provider block where we are telling it about the back end.

I pushed the hyve-2 dir to the `fitfile/terraform-infrastructure/non-production/fitfile-non-production-infrastructure` repo.

I pushed the changes to central services with the new node-2 workspace. This triggers a tfc plan in the `tfc-projects-iac` workspace.

It is confusing with terms.

```json
{
 cloudProvider: "azure",
 deploymentKey: "ff-hyve-2",
 tfcProject: "FITFILE Non-Production",
 tfcWorkspace: $deploymentKey,
 tfcVariables:
   "approles",
   "vault_namepace",
   "FITFILE Platform Keys",
   "FITFILE Vault Configuration",
   "FITFILE Vault Consumer"
   ],
 gitlabRepo: "fitfile/terraform-infrastructure/non-production/fitfile-non-production-infrastructure",
 repoDir: $deploymentKey,
}
```

### Variables for the Workspace

#### Approles

```sh
terraform output -json | jq --arg prefix "<replace-with-deployment-key>" '
  .deployments_approle_roles.value as $roles |
  .deployments_approle_secret_ids.value |
  to_entries |
  map(select(.key | startswith($prefix)) |
    if .key == $prefix then
      {key: "argocd", value: {secret_id: .value.secret_id, role_id: $roles[.key].role_id}}
    else
      {key: (.key | gsub("^" + $prefix + "\\.";"")), value: {secret_id: .value.secret_id, role_id: $roles[.key].role_id}}
    end
  ) |
  from_entries
'
```

### Gitlab

I Don't need a new repo as it is part of the non-prod repo.

Access

deployment key

ff-hyve-2

nhs-provider-2

[Create a FITFILE Terraform module for the whole process](Create%20a%20FITFILE%20Terraform%20module%20for%20the%20whole%20process)

It's 10:07

Ran the node 2 deployment plan.

It's 10:15

Failed at the helm part again. I think I just need to re run it

It's 10:15

It's 10:35

I have forgotten to add the values file.

Looking for the monitoring nothing seemed deployed. Looking at argo there are errors in the logs. Then it hit me.

This is a copy of the hyve-1 with the number one changed to 2.

I added the values file but nothing changed.

It's 10:47

I started the destroy

It's 10:54

Redeploy

It's 10:56

Realised I had copied the vault_namespace and not changed the 1 to a 2. It's 11:13

It seems like if we get these bits wrong it won't heal itself?

It's 11:58

Retrying from scratch.

We need to verify that all the settings are equal. If it is for deployemtKey1 all references should be checked.

We appear to have problems with backing up data in the node. Because it is inside the cluster it is difficult to set a new cluster to use the backed up data.

```sh
Warning: Value for undeclared variable

The root module does not declare a variable named "cloudflare_issuer_api_token" but a value was found in file "/home/tfc-agent/.tfc-agent/component/terraform/runs/run-z2sFjdjx3QFkhyoX/terraform.tfvars". If you meant to use this value, add a "variable" block to the configuration. To silence these warnings, use TF_VAR_… environment variables to provide certain "global" settings to all configurations in your organization. To reduce the verbosity of these warnings, use the -compact-warnings option.
```

### AWS Deployment of Fitfile

Log in to AWS! Success. Starting off well.

Look at the Documentation for deploying to AWS that is in Confluence.

What is the TFC project and Gitlab repo?

There is a workspace called Sandbox.

[terraform-aws-eks-private](https://gitlab.com/fitfile/terraform-infrastructure/sandbox/terraform-aws-eks-private)

I logged in to AWS CLI. `aws configure`. I created the keys needed to fill in this step in AWS IAM. You are only allowed 2 so I had to delete an old one.

I think there was another way to set the permissions needed. I think Ollie side stepped that though!

Started deployment It's 09:38

Not sure it is going to just work. We shall see.

I am expecting this to deploy everything we need for a private EKS. I will need to get to the box. Might be easier to do a public version of this for these kinds of demos.

It spends a long time on create eks cluster

It's 10:43 Meeting about the demo data. Confused. OMOP data should already be there.

Create new queries.

The demo is up in the air. Very unclear for such a tight deadline.

Out intention is to plan out a demo deployment for use in the presentation.

There is a DNS Name need to work with Auth0. I am unsure what this is pointing to.

<https://nhs-eoe-sde.fitfile.net>

from the previous one

<https://app.ff-sandbox.privatelink.fitfile.net>

Dependencies for deploying the AWS

Deployment directory.

`/deployment/ffnodes/eoe/ff-sde-1`

Secrets

deploymentKey

Auth0 set this up cleanly . But it needs output from the dns that the EKS terraform makes.

`FITFILE/Terraform Infrastructure/Production/central-services/auth0/non_prod/auth0/locals.tf`

```json
    ff-hyve-1 = {
      tenant_name                               = "FF Hyve 1"
      api_name                                  = "FF Hyve 1"
      api_token_lifetime                        = 300 # 5 Mins
      api_audience                              = "https://nhs-provider-1.fitfile.net"
      enabled_apis                              =
      whitelist_api_audience_for_login_redirect = true
    }
    ff-hyve-2 = {
      tenant_name                               = "FF Hyve 2"
      api_name                                  = "FF Hyve 2"
      api_token_lifetime                        = 300 # 5 Mins
      api_audience                              = "https://nhs-provider-2.fitfile.net"
      enabled_apis                              =
      whitelist_api_audience_for_login_redirect = true
    }
    ff-eoe-sde = {
      tenant_name                               = "FF EOE SDE"
      api_name                                  = "FF EOE SDE"
      api_token_lifetime                        = 300 # 5 Mins
      api_audience                              = "https://nhs-eoe-sde.fitfile.net"
      enabled_apis                              =
      whitelist_api_audience_for_login_redirect = true
    }
```

`/FITFILE/Terraform Infrastructure/Production/central-services/hcp/vault/locals.tf`

```json
"ff-hyve-1" = {
      secrets = tomap({
        "application" = {},
        "spicedb"     = {},
        "cloudflare"  = {},
        "monitoring"  = {},
      })
      auto_create = true
    }
    "ff-hyve-2" = {
      secrets = tomap({
        "application" = {},
        "spicedb"     = {},
        "cloudflare"  = {},
        "monitoring"  = {},
      })
      auto_create = true
    }
    "ff-eoe-sde" = {
      secrets = tomap({
        "application" = {},
        "spicedb"     = {},
        "monitoring"  = {},
      })
      auto_create = true
    }
```

```json
module "dns_zone" {
  count = var.enable_dns_zone ? 1 : 0

  source = "./modules/dns_zone"

  name   = local.name
  vpc_id = module.vpc.vpc_id
  tags   = local.tags

  records =
    dns_name  = data.aws_lb.eks_elb.dns_name
    zone_id   = data.aws_lb.eks_elb.zone_id
    subdomain = "argocd"
    type      = "A"
    }, {
    dns_name  = data.aws_lb.eks_elb.dns_name
    zone_id   = data.aws_lb.eks_elb.zone_id
    subdomain = "app"
    type      = "A"
  }]
}
```

dns prefix.

certs block

Let me trace through how the DNS zone name will be constructed based on the updated code:

1. In main.tf, the DNS zone module is called with:

```tf
module "dns_zone" {
  count = var.enable_dns_zone ? 1 : 0

  source = "./modules/dns_zone"

  name   = local.name
  vpc_id = module.vpc.vpc_id
  tags   = local.tags

  records =
    dns_name  = data.aws_lb.eks_elb.dns_name
    zone_id   = data.aws_lb.eks_elb.zone_id
    subdomain = "argocd"
    type      = "A"
    }, {
    dns_name  = data.aws_lb.eks_elb.dns_name
    zone_id   = data.aws_lb.eks_elb.zone_id
    subdomain = "app"
    type      = "A"
  }]
}
```

Here we see `name = local.name` being passed to the module.

2. The `local.name` value is defined in:

```tf
  zone_id = aws_route53_zone.private_dns_zone.zone_id
  name    = format("%s.%s", var.records[count.index].subdomain, local.dns_zone_name)
```

We can see `local.name = "ff-eoe-sde"`

3. The DNS zone name is constructed in the dns_zone module:

```tf
locals {
  dns_zone_name = coalesce(var.dns_zone_name, "${var.name}.privatelink.fitfile.net")
}
```

The logic works like this:

1. `var.dns_zone_name` has a default empty string value
2. Since no explicit `dns_zone_name` is provided when calling the module, it will use the empty string default
3. The `coalesce` function will then use the second option: `"${var.name}.privatelink.fitfile.net"`
4. `var.name` is set to `local.name` which is `"ff-eoe-sde"`

Therefore, the final DNS zone name will be:

`ff-eoe-sde.privatelink.fitfile.net`

This private DNS zone will be used for internal resources within the VPC, and based on the records being created, it will have two A records:

- `argocd.ff-eoe-sde.privatelink.fitfile.net`
- `app.ff-eoe-sde.privatelink.fitfile.net`

Both of these will point to the EKS load balancer's DNS name.

This matches with what's shown in your values file where you have certificates being created for:

- `ff-eoe-sde-argocd.fitfile.net`
- `ff-eoe-sde-argo-workflows.fitfile.net`
- `ff-eoe-sde.privatelink.fitfile.net
Still confused about the aws permissions to see EKS stuff.
I copied my creds for aws loging and terraform login
The terraform needs vars. To access the API it needs API creds. Usually we supply things from the kubeconfig, but aws are doing it different. To get the token we need to call a aws endpoint. But I am not sure about the certificates and such.

```json
{
  "level": "error",
  "ts": "2024-11-06T16:26:00Z",
  "logger": "cachingClientFactory",
  "msg": "Failed to get cacheKey from obj",
  "controller": "vaultstaticsecret",
  "controllerGroup": "secrets.hashicorp.com",
  "controllerKind": "VaultStaticSecret",
  "VaultStaticSecret": {
    "name": "cloudflare-issuer-api-token",
    "namespace": "cert-manager"
  },
  "namespace": "cert-manager",
  "name": "cloudflare-issuer-api-token",
  "reconcileID": "1b33fc7f-a6f5-4e5b-a192-8d3531ee6f80",
  "error": "VaultAuth.secrets.hashicorp.com \"default\" not found"
}
```

[deploymentDocs/jumpbox_eks_terraform_access](deploymentDocs/jumpbox_eks_terraform_access)

We had the problem of not having the dns set up. We needed to re run the outer terraform

## Inboxnote

I copied the stage-cluster-2 folder

I then ran terraform init in the folder to make the IDE happy

I went through the terraform and changed any ref to `ff-test-{a,b,c}` to `ff-hyve-{a,b,c}`

I filled in the confluence deployment-key table for ff-hyve-1. It is important to start with this as it is used for lots of things.

Now I should read the instructions.

I have left the values file to point at `ff-test-{a,b,c}`

> Stopped to fill in the SCAL TPP spreadsheet

### Started on the Tooling Instructions

Completed the Create Vault Resources.

I noticed that the instruction example is different from the actual code.

Example:

```sh
"<replace_with_deployment_key>" = {
  secrets = tomap({
    "application" = {},
    "spicedb" = {},
    "cloudflare" = {}, # only needed if using cloudflare
    "monitoring" = {}, # for grafana creds
  })
}
```

Code:

```sh
    "ff-hyve-1" = {
      secrets = tomap({
        "application" = {},
        "spicedb"     = {},
        "cloudflare"  = {},
        "monitoring"  = {},
      })
      auto_create = true
    }
```

I left in the auto_create from the code and aligned the keys to the example.

Commit and push the change to trigger the terraform plan and apply in

Terraform Cloud: HCP Terraform

A DevOps engineer will need to manually press the apply button on the Run page

I ran the terraform cloud apply for the creation of the empty secrets structures.

Now on to the Populate the secrets part.

Wondering about the ff-a ff-b ff-c set up. Do we need?

I straight up ran the `cargo run -- key-gen` but got an error. Then I ran the `rustup install nightly`. I had done this before so not sure why i need to do it again.

I wasn't able to generate a UDE Key at this time. I just added the other secrets and moved on for now. It will be a problem though when I deploy

I moved on to the grafana setup. This was much simpler. Only took 1 min including the apply time via TFC!

In the json block supplied it says to add the port :443. I included the : (turned out it meant add it to the end or the url) the others didn't mention it.

Next I added a gitlab repo via the central services terraform. And I didn't need to do this as I am just adding to another already existing repo! So setting up the TFC Project I copied the staging-cluster-2 block and changed the details.

Ollie came through with the rust solution.

```sh
rustup install nightly-2024-02-04;  
rustup default nightly-2024-02-04-aarch64-apple-darwin;
```

I finished off with the spicedb block. It is present in the application block but probably legacy.

I realised I had named the path to the folder in the terraform repo wrong.

So far smooth. it is a bit disjointed and having to pop all over the place. This will get boring very quickly.

I used cursor's ai to generate a bash script that fills in the 2 sets of secrets even using the cargo run -- key-gen to get the key. The script is in the ude repo

I didn't need to clone and create the files as I just copied the staging cluster code and renamed things. This should be automated!

The public infrastructure version was up to date. (1.0.8)

Stopped due to Halloween party

Day 2

Yesterday wasn't very focused on the deployment.

First real pain. The TFC workspace needs the env vars to deploy. I think I have to manually add them! This can be part of the workspace creation.

In TFC There are variable sets. I applied the same ones as in Staging-cluster-2 I am not sure if any needed changing.

Then needed to add the vault_namespace. deployments/ff-hyve-1

The approles are described in the private deployment and seem to happen after the cluster is deployed and before we deploy the application.

In this case to generate them is the same as in the docs, but I then needed to convert to HCL and add them to the env vars in tfc.

When I entered them as HCL I got a warning that they were badly formated. I tried removing the space between each line, but feel this is pretty weak!

I had made the HCL badly. it should have looked like

```sh
"argocd" = {
  "secret_id" = "some_secret"

  "role_id" = "some_id"
}

"cloudflare" = {
  "secret_id" = "some_secret"

  "role_id" = "some_id"
}

"ff-test-a-application" = {
  "secret_id" = "some_secret"

  "role_id" = "some_id"
}

"ff-test-b-application" = {
  "secret_id" = "some_secret"

  "role_id" = "some_id"
}

"ff-test-c-application" = {
  "secret_id" = "some_secret"

  "role_id" = "some_id"
}

"mesh" = {
  "secret_id" = "some_secret"

  "role_id" = "some_id"
}

"monitoring" = {
  "secret_id" = "some_secret"

  "role_id" = "some_id"
}

"spicedb" = {
  "secret_id" = "some_secret"

  "role_id" = "some_id"
}
```

Still didn't work.

I wrapped the whole thing in another set of {} and it worked

but now I have an error with keys! it is expecting them to be ff-hyve-a-application. Have I named something wrong or should I change the approles names.

All the fiddly bits. I needed to have changed the roles from ff-test... to ff-hyve...

Gordan bennet. That was still wrong. THe hcl block needed to be in

It's 09:41

nope.

Even more drama! The validation for the variable was wrong. Also seemed to be missing things. I removed it for now and should be fixed for other deployments

Went back as I didn't need to deploy a,b,c. We are doing 2 azure deployments and an aws one.

Added all the secrets in one go

We need to do auth0 and Grafana before the secrets.

I did the deployment a bit wrong. Adding the 3 application was wrong. It is simpler with the one each. I can do 2 azure deployments easily.

The data backups are difficult

It's 10:21

Spicedb pre-shared key needs to be the same in both blocks. The applications has it, the spicedb block also has it. Check these are the same value.

Auth0 can be checked via auth0 website

Monitoring comes from the monitoring output

It's 10:47

The ff-hyve-1 values file.

Removed a bunch of stuff

Need to

Remove trivy

change tags on nodepools

### Deploy the Platform

By now, we have created the

1. Set the `deployment_key` variable to the
2. `approles` - This is a sensitive HCL terraform variable. To get the values you need to read the output of the HCP vault workspace. Checkout the central services repo, and cd to the vault directory. Then run this, replacing the prefix with the deployment name:

```sh
terraform output -json | jq --arg prefix "<replace-with-deployment-key>" ' .deployments_approle_roles.value as $roles | .deployments_approle_secret_ids.value | to_entries | map(select(.key | startswith($prefix)) | if .key == $prefix then {key: "argocd", value: {secret_id: .value.secret_id, role_id: $roles[.key].role_id}} else {key: (.key | gsub("^" + $prefix + "\\.";"")), value: {secret_id: .value.secret_id, role_id: $roles[.key].role_id}} end ) | from_entries '
```

A bit confusing

Dependency tree

TFC -> approles -> secrets -> (Grafana, Auth0, SpiceDB)

The deployment failed the first time

```sh
Error: 1 error occurred:  Internal error occurred: failed calling webhook "validate.nginx.ingress.kubernetes.io": failed to call webhook: Post "https://ingress-nginx-controller-admission.ingress-nginx.svc:443/networking/v1/ingresses?timeout=10s": no endpoints available for service "ingress-nginx-controller-admission"

with module.platform.module.argocd.helm_release.argocd

on .terraform/modules/platform/argocd/main.tf line 1, in resource "helm_release" "argocd":
```

I reran the apply

> The deployment key and the domains used may not be the same variable.
