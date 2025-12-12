---
aliases: []
confidence: 
created: 2025-10-22T16:51:15Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: I need to import images from bitnami. They recentl
type:
uid: 
updated: 
version:
---

I need to import images from bitnami. They recently changed their payments and the free versions of images only have latest tag rather than version numbers. We import images to our own acr in azure. I want to still be able to pull the latest helm chart and search for image references within that chart. But somehow I need to determine the versions of those latest images. Research this problem and suggest what to do to find the current chart and image versions for a particular chart. Use the mongoDB chart as an example for this research but I will need the same process for other charts

Bitnami’s restructuring in 2025 drastically changed how image versions are managed. As of August 28th, versioned public images have been removed from Docker Hub, breaking Helm chart workflows that depend on tagged image versions. However, you can still identify the image versions used by any given Bitnami Helm chart—including MongoDB—by combining the chart metadata and image inspection strategies below.[^1_1][^1_2][^1_3][^1_4][^1_5][^1_6]

---

## Current Situation: Bitnami Image Sources

Bitnami now maintains three distinct registries:

| Registry         | Description                                           | Status                               |
| :--------------- | :---------------------------------------------------- | :----------------------------------- |
| `bitnami/`       | Free hardened images, only `latest` tag available     | Active for small subset [^1_1][^1_2] |
| `bitnamilegacy/` | Archived images with versioned tags (frozen Aug 2025) | Read-only [^1_3][^1_4]               |
| `bitnamisecure/` | Paid registry with versioned and patched images       | Commercial tier [^1_1][^1_2]         |

Helm charts on GitHub and ArtifactHub remain up-to-date structurally but now reference non-versioned or placeholder images that you must override manually.[^1_2][^1_6]

---

## Step-by-Step: Determine Image Versions for MongoDB Chart

### 1. Fetch the chart’s Current Metadata

You can locate the latest Bitnami MongoDB chart definition from ArtifactHub or GitHub:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm pull oci://registry-1.docker.io/bitnamicharts/mongodb --untar
```

Then inspect the default values and template:

```bash
grep 'repository:' values.yaml
# repository: docker.io/bitnami/mongodb
grep 'tag:' values.yaml
# tag: latest
```

The “latest” tag is now standard.

---

### 2. Identify the Actual Image Version behind “latest”

You can determine the MongoDB version inside the container through a local Docker inspection or sandbox run:

```bash
docker pull bitnami/mongodb:latest
docker run --rm bitnami/mongodb:latest mongod --version
```

It outputs the internal MongoDB version, such as:

```sh
db version v7.0.14
```

This confirms the internal database build, even if Bitnami no longer provides granular image tags.[^1_5]

If you cannot pull interactively (e.g., automation context):

```bash
docker inspect bitnami/mongodb:latest | jq '.[^1_0].Config.Labels'
```

Some images include labels like `org.opencontainers.image.version` or `io.bitnami.app-version`.

---

### 3. Map to Legacy Tagged Version (Optional Freeze)

For reproducibility, locate this version’s corresponding frozen tag in the **bitnamilegacy** registry (snapshot taken before August 2025):

```bash
docker pull bitnamilegacy/mongodb:7.0.14-debian-12-r26
```

If this image exists, mirror it into your ACR:

```bash
az acr import --name <YOUR_ACR> \
  --source docker.io/bitnamilegacy/mongodb:7.0.14-debian-12-r26 \
  --image mongodb:7.0.14-debian-12-r26
```

This ensures reliable, version-pinned production images without `latest` risk.

---

### 4. Mirror Helm Chart and Maintain Version Indexing

Keep a record of Helm chart versions and corresponding image digests:

```bash
helm show chart oci://registry-1.docker.io/bitnamicharts/mongodb | grep version
```

To track image digests:

```bash
skopeo inspect docker://docker.io/bitnami/mongodb:latest | jq '.Digest'
```

Store both chart version and image SHA digest in your internal metadata or ACR annotations for traceability.

---

## Recommended Workflow for All Bitnami Charts

1. Pull Helm chart source (`helm pull ... --untar`).
2. Identify all image references in `values.yaml`.
3. For any `:latest` image:
   - Pull locally and check internal version.
   - Capture digest via `skopeo inspect`.
4. Use the digest (`@sha256:...`) instead of `:latest` when mirroring into ACR.
5. Maintain an internal YAML/JSON mapping between:
   - Chart version
   - Image digest
   - Application version (from runtime inspection)
6. Automate this process using a CI job (e.g., GitHub Actions or Azure DevOps) to refresh weekly.

---

Using MongoDB as an example, the approach generalizes to other Bitnami charts (PostgreSQL, Redis, RabbitMQ, etc.) since all follow the same repository structure and deprecation pattern.[^1_4][^1_6][^1_1][^1_2]

<span style="display:none">[^1_10][^1_11][^1_12][^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_19][^1_20][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: <https://northflank.com/blog/bitnami-deprecates-free-images-migration-steps-and-alternatives>

[^1_2]: <https://github.com/bitnami/charts/issues/35256>

[^1_3]: <https://github.com/bitnami/containers/issues/83267>

[^1_4]: <https://github.com/dagster-io/dagster/issues/31388>

[^1_5]: <https://www.mongodb.com/community/forums/t/what-is-the-method-to-determine-the-mongodb-version-within-a-particular-docker-image/297107>

[^1_6]: <https://github.com/bitnami/charts>

[^1_7]: <https://www.reddit.com/r/kubernetes/comments/1mc73s4/bitnami_moving_most_free_container_images_to_a/>

[^1_8]: <https://learn.microsoft.com/en-us/azure/container-registry/container-registry-import-images>

[^1_9]: <https://artifacthub.io/packages/helm/bitnami/mongodb>

[^1_10]: <https://learn.microsoft.com/en-us/azure/container-registry/container-registry-image-tag-version>

[^1_11]: <https://hub.docker.com/r/bitnami/mongodb>

[^1_12]: <https://artifacthub.io/packages/helm/bitnami/mongodb/16.0.0>

[^1_13]: <https://stackoverflow.com/questions/67749357/how-to-import-all-images-from-an-acr-repository-to-another-acr-in-different-tena>

[^1_14]: <https://artifacthub.io/packages/helm/bitnami/mongodb/13.2.0>

[^1_15]: <https://bitnami.com>

[^1_16]: <https://www.reddit.com/r/selfhosted/comments/1hlt4zr/whats_up_with_bitnamis_docker_images/>

[^1_17]: <https://www.iamraghuveer.com/posts/docker-images-version-tagging-best-practices/>

[^1_18]: <https://github.com/bitnami/charts/issues/3635>

[^1_19]: <https://www.reddit.com/r/selfhosted/comments/1n27s21/bitnami_archiving_its_registry_of_images_starting/>

[^1_20]: <https://stackoverflow.com/questions/66256564/how-to-insert-data-in-the-bitnami-mongodb-chart-on-creation>

---

## Discover how to Import Bitnami Images Properly into Azure Container Registry

To import Bitnami images properly into Azure Container Registry (ACR), you must adapt to the new post-2025 Bitnami registry structure and use Azure’s built-in import mechanisms rather than `docker pull/push` workflows. The key is to authenticate as needed, resolve the right image path, and mirror images in a reproducible form.[^2_1][^2_2][^2_3][^2_4][^2_5][^2_6]

---

### Bitnami Image Structure (as of 2025)

| Source Registry                               | Description                                         | Authentication                             |
| :-------------------------------------------- | :-------------------------------------------------- | :----------------------------------------- |
| `docker.io/bitnami`                           | Public legacy images (mostly pinned with `latest`)  | No auth, rate-limited                      |
| `docker.io/bitnamilegacy`                     | Frozen August 2025 snapshots                        | Read-only public                           |
| `registry.broadcom.com/bitnami/secure-images` | Commercial secure repository replacing old registry | Requires Broadcom credentials [^2_2][^2_3] |

When working with ACR, you can import from any of these as long as your credentials allow it.

---

### Recommended Import Approaches

#### 1. Standard Import from Docker Hub or Bitnami Legacy Registry

If the image is still public:

```bash
az acr import \
  --name myregistry \
  --source docker.io/bitnami/mongodb:latest \
  --image bitnami/mongodb:latest
```

You can specify a tag or manifest digest for determinism:

```bash
az acr import \
  --name myregistry \
  --source docker.io/bitnami/mongodb@sha256:abcd1234... \
  --image bitnami/mongodb@sha256:abcd1234...
```

If you hit Docker Hub rate limits:

```bash
az acr import \
  --name myregistry \
  --source docker.io/bitnami/mongodb:latest \
  --image bitnami/mongodb:latest \
  --username <docker_hub_user> \
  --password <docker_hub_pat>
```

This avoids downloading the image locally and copies it server-side directly into your registry.[^2_4][^2_6][^2_1]

---

#### 2. Importing from Bitnami Secure Registry (Broadcom)

If you use **Bitnami Secure Images**, first log in through Broadcom’s portal and fetch credentials for the `registry.broadcom.com` repository :[^2_2][^2_3]

```bash
az acr import \
  --name myregistry \
  --source registry.broadcom.com/bitnami/secure-images/mongodb:7.0.14-debian-12-r26 \
  --image bitnami/mongodb:7.0.14-debian-12-r26 \
  --username <broadcom_user> \
  --password <broadcom_token>
```

You can automate this import via CI/CD, refreshing images on a schedule using digest-based imports to maintain reproducibility.

---

#### 3. Import by Digest (Preferred)

Always prefer importing by digest for long-term stability:

```bash
skopeo inspect docker://docker.io/bitnami/mongodb:latest | jq .Digest
# Example output: sha256:1f0236f6252a987a7...
az acr import \
  --name myregistry \
  --source docker.io/bitnami/mongodb@sha256:1f0236f6252a987a7... \
  --image bitnami/mongodb@sha256:1f0236f6252a987a7...
```

This ensures the image in ACR stays consistent even if Bitnami updates “latest”.

---

#### 4. Validate After Import

You can verify successfully imported images via Azure CLI:

```bash
az acr repository show-tags --name myregistry --repository bitnami/mongodb
az acr repository show-manifests --name myregistry --repository bitnami/mongodb
```

Or pull and inspect locally:

```bash
docker pull myregistry.azurecr.io/bitnami/mongodb:latest
docker run --rm myregistry.azurecr.io/bitnami/mongodb:latest mongod --version
```

---

### Recommended Automation Pattern

To maintain consistent imports of Bitnami images:

1. Store image source mappings (chart name → source URI) in YAML or JSON.
2. Resolve digest with `skopeo inspect`.
3. Use a scheduled job with `az acr import` to refresh ACR copies.
4. Annotate image digests in Helm values or your manifest templates.

This creates a self-maintained, version-resilient mirror of Bitnami assets in your Azure environment.[^2_3][^2_5][^2_6][^2_1][^2_4]

<span style="display:none">[^2_10][^2_11][^2_12][^2_13][^2_14][^2_15][^2_16][^2_17][^2_18][^2_19][^2_20][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: <https://learn.microsoft.com/en-us/azure/container-registry/container-registry-import-images>

[^2_2]: <https://techdocs.broadcom.com/us/en/vmware-tanzu/bitnami-secure-images/bitnami-secure-images/services/bsi-doc/get-started-index.html>

[^2_3]: <https://techdocs.broadcom.com/us/en/vmware-tanzu/bitnami-secure-images/bitnami-secure-images/services/bsi-doc/using-adding-new-registry.html>

[^2_4]: <https://b1thunt3r.se/2024/11/acr-import>

[^2_5]: <https://github.com/bitnami/containers>

[^2_6]: <https://docs.azure.cn/en-us/container-registry/buffer-gate-public-content>

[^2_7]: <https://northflank.com/blog/bitnami-deprecates-free-images-migration-steps-and-alternatives>

[^2_8]: <https://stackoverflow.com/questions/57399853/how-to-mount-a-volume-azure-file-share-to-a-bitnami-based-docker-image-on-azur>

[^2_9]: <https://www.reddit.com/r/selfhosted/comments/1n27s21/bitnami_archiving_its_registry_of_images_starting/>

[^2_10]: <https://stackoverflow.com/questions/73226891/azure-webapp-for-containers-docker-compose-yml-referencing-bitnami-images>

[^2_11]: <https://github.com/Azure/azure-cli/issues/30840>

[^2_12]: <https://www.reddit.com/r/devops/comments/1m28mag/upcoming_changes_to_the_bitnami_catalog/>

[^2_13]: <https://capstone-s.com/urgent-bitnamis-docker-hub-and-helm-chart-changes-act-before-september-29-2025/>

[^2_14]: <https://hub.docker.com/r/bitnami/azure-cli>

[^2_15]: <https://github.com/bitnami/containers/issues/83267>

[^2_16]: <https://hub.docker.com/r/bitnamicharts/argo-workflows>

[^2_17]: <https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli>

[^2_18]: <https://learn.microsoft.com/en-us/azure/aks/quickstart-helm>

[^2_19]: <https://hub.docker.com/u/bitnami>

[^2_20]: <https://blog.bitnami.com/2018/05/Azure-Container-Marketplace.html?m=1>

---

## Do the docker.io/bitnami Get Updates Still? If We Use the Latest Charts and Images Do We Still Get the Bitnami Images with Fixes and Security? What Do We Get with that Registry? Explain with MongoDB as an Example

As of late 2025, the **docker.io/bitnami** registry no longer provides actively maintained production images — it now only contains a small, curated subset of “latest” development images that may receive occasional base-level hardening but no full, ongoing patching or version support.[^3_1][^3_2][^3_3][^3_4][^3_5][^3_6]

---

### What Happens to docker.io/bitnami

After **August 28–September 29, 2025**, Broadcom (Bitnami’s parent company) archived nearly all historical, versioned images and Helm chart releases:

| Registry                                        | Status          | Details                                                                                                                        |
| :---------------------------------------------- | :-------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **docker.io/bitnami**                           | Active, minimal | Contains only “latest” tags for selected free development images, lightly hardened but not maintained like before [^3_6][^3_4] |
| **docker.io/bitnamilegacy**                     | Archived        | Frozen August 2025 snapshot; no patches or rebuilds [^3_3][^3_2][^3_5]                                                         |
| **registry.broadcom.com/bitnami/secure-images** | Paid tier       | Full support, patches, CVE monitoring, version history [^3_6][^3_7]                                                            |

The free Docker Hub presence is now explicitly “for community development use,” not for production-grade workloads.[^3_4][^3_6]

---

### Using Bitnami MongoDB as an Example

The **MongoDB chart** at `bitnami/mongodb` and its corresponding Docker image currently follow this model:

- **Chart:** Still hosted on ArtifactHub and GitHub but references `docker.io/bitnami/mongodb:latest`.
- **Image:** The `"latest"` tag on Docker Hub is periodically rebuilt with newer Debian or app dependencies, but **does not guarantee MongoDB minor or patch-level updates**.
- **Security Fixes:** Only basic OS-level hardening (e.g., minimal CVE base image rebuilds) — no committed vulnerability response cycle.[^3_6][^3_8][^3_4]

For example:

```bash
docker pull bitnami/mongodb:latest
docker run --rm bitnami/mongodb mongod --version
# May still show MongoDB 7.0.14 in October, but not 7.0.15 or later, as patches stop flowing.
```

While this image might get a refreshed `latest` once in a while, it’s **not patched regularly** — meaning new Common Vulnerabilities and Exposures (CVEs) discovered in MongoDB or its dependencies after the 2025 transition will not be fixed in that free version.[^3_3][^3_5][^3_4]

---

### What You Actually Get Now

When you use `docker.io/bitnami/mongodb:latest` today:

1. You still receive a **functional, hardened image** suitable for testing or development.
2. You no longer have access to **specific version tags** (e.g., `7.0.14-debian-12-r26`).
3. You don’t get **ongoing security updates or long-term support**.
4. You may experience **chart version drift**, since charts reference unpinned images.

The MongoDB Helm chart itself keeps updating scaffolding and values, but references an image that’s **effectively static** in content, except for rare rebuilds related to base image refreshes.[^3_9][^3_10][^3_11]

---

### What To Use Instead

For production workloads or secure staging environments:

- **Option 1:** Subscribe to **Bitnami Secure Images** (registry.broadcom.com) for real patch coverage.
- **Option 2:** Switch to **official vendor images** (`mongo` from MongoDB Inc.).
- **Option 3:** Mirror from **bitnamilegacy** and freeze the images with explicit digests in ACR for deterministic builds.
- **Option 4:** Build your own from Bitnami’s open-source `bitnami/containers` repository on GitHub and maintain your patch schedule manually.[^3_8][^3_1][^3_6]

---

In summary:

The `docker.io/bitnami` registry after August–September 2025 continues to serve a **limited**, **non-updated**, development-grade set of images. Using it for production means accepting frozen MongoDB (and other app) versions with no guaranteed security maintenance.

<span style="display:none">[^3_12][^3_13][^3_14][^3_15][^3_16][^3_17][^3_18][^3_19]</span>

<div align="center">⁂</div>

[^3_1]: <https://github.com/bitnami/containers/issues/83267>

[^3_2]: <https://www.reddit.com/r/selfhosted/comments/1n27s21/bitnami_archiving_its_registry_of_images_starting/>

[^3_3]: <https://northflank.com/blog/bitnami-deprecates-free-images-migration-steps-and-alternatives>

[^3_4]: <https://www.kubermatic.com/blog/what-kkp-users-need-to-know-about-the-bitnami-registry-changes/>

[^3_5]: <https://www.blueshoe.io/blog/bitnami-and-alternatives/>

[^3_6]: <https://news.broadcom.com/app-dev/broadcom-introduces-bitnami-secure-images-for-production-ready-containerized-applications>

[^3_7]: <https://bitnami.com>

[^3_8]: <https://github.com/bitnami/containers>

[^3_9]: <https://www.chkk.io/blog/bitnami-deprecation>

[^3_10]: <https://artifacthub.io/packages/helm/bitnami/mongodb>

[^3_11]: <https://github.com/bitnami/charts/issues/35164>

[^3_12]: <https://www.exivity.com/blog/replacing-bitnami-dependencies-for-k8s>

[^3_13]: <https://www.mongodb.com/community/forums/t/running-mongodb-in-a-docker-container/231001>

[^3_14]: <https://hub.docker.com/r/bitnami/mongodb>

[^3_15]: <https://hub.docker.com/r/bitnami/mongodb-exporter>

[^3_16]: <https://www.reddit.com/r/kubernetes/comments/1mc73s4/bitnami_moving_most_free_container_images_to_a/>

[^3_17]: <https://artifacthub.io/packages/helm/bitnami/mongodb/13.6.4>

[^3_18]: <https://stackoverflow.com/questions/75470085/bitnami-mongodb-docker-image-fails-to-connect-when-replica-set-enabled>

[^3_19]: <https://www.reddit.com/r/selfhosted/comments/1hlt4zr/whats_up_with_bitnamis_docker_images/>
