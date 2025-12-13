---
aliases: []
confidence: 
created: 2025-03-03T09:59:51Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ghcr, hyve]
title: I have this image downloaded from ghcr_Status_ Dow
type: 
uid: 
updated: 
version: 
---

update the docker tag and docker push commands to push the image

To push the image `ghcr.io/thehyve/fitfile_etl_container:0.3.0` from GitHub Container Registry (GHCR) to your Azure Container Registry (ACR) named `fitfileregistry`, follow these steps:

## 1. Tag the Image

Update the `docker tag` command to match your source image and ACR login server:

```sh
docker tag ghcr.io/thehyve/fitfile_etl_container:0.3.0 fitfileregistry.azurecr.io/thehyve/fitfile_etl_container:0.3.0
```

This command tags the image with the fully qualified name of your ACR.

## 2. Log in to ACR

Authenticate with your ACR using the Azure CLI:

```sh
az acr login --name fitfileregistry
```

This ensures you have permission to push images to the registry.

---

## 3. Push the Image

Push the tagged image to your ACR:

```sh
docker push fitfileregistry.azurecr.io/thehyve/fitfile_etl_container:0.3.0
```

This uploads the image to your ACR.

---

## 4. Verify the Push (Optional)

You can confirm that the image was successfully pushed by listing repositories in your ACR:

```sh
az acr repository list --name fitfileregistry --output table
```

This will display all repositories in `fitfileregistry`, including `thehyve/fitfile_etl_container`.
