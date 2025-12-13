---
aliases: []
confidence: 
created: 2025-02-18T09:56:42Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, ff_deploy]
title: push image to azure acr
type:
uid: 
updated: 
version:
---

how can I use az acr import to push a local image to the azure acr

The `az acr import` command is not designed to push local images directly to Azure Container Registry (ACR). Instead, it's used to import images from other registries, including public registries like Docker Hub, to your ACR. To push a local image to ACR, you should follow these steps:

1. Tag your local image with the ACR login server:

```bash
docker tag <local-image-name>:<tag> <acr-login-server>/<image-name>:<tag>
```

2. Log in to your ACR:

```bash
az acr login --name <acr-name>
```

3. Push the tagged image to ACR:

```bash
docker push <acr-login-server>/<image-name>:<tag>
```

If you want to use `az acr import`, you would first need to push your local image to a registry that's accessible via the internet, and then use the `az acr import` command to copy it to your ACR[6].

For directly pushing local images, the `docker push` method is more appropriate and commonly used[2][3][8].
