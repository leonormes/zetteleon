---
aliases: []
confidence: 
created: 2025-10-07T01:57:35Z
epistemic: 
last_reviewed: 
modified: 2025-11-05T09:44:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Bitnami Catalog Changes (2025)
type:
uid: 
updated: 
version:
---

Here’s a comprehensive, actionable deep dive on how to import and retag the latest Bitnami Helm charts for **MongoDB**, **MinIO**, and **PostgreSQL** into your own system—following the 2025 Bitnami catalog transition. This covers the full Helm chart and container strategy, including recommendations and concrete CLI/code examples.

---

## 1. **Summary: Bitnami Catalog Changes (2025)**

- **Chart Source:** Helm chart source remains OSS at [github.com/bitnami/charts](https://github.com/bitnami/charts).
- **OCI Chart Distribution:** OCI-packaged charts on Docker Hub (`bitnamicharts`) will remain but no longer be updated, and image references may break if you don’t override them.
- **Container Images:** Only a limited, “latest”-only subset stays public and free (`bitnami` or `bitnamisecure`). Archived, frozen versions are on `bitnamilegacy`. LTS, patched, and all historic versions go behind a paywall via Bitnami Secure Images.
- **Your Core Problem:** You want to continue using up-to-date open-source Bitnami Helm charts for MongoDB, MinIO, and PostgreSQL, but host/service images from your own registry, ideally using retagged images.

---

## 2. **Detailed Steps: Importing and Retagging for Your Own Registry**

## **A. Download and Mirror the Helm Charts**

**Step 1:** Clone the latest Helm chart sources

`git clone https://github.com/bitnami/charts.git cd charts/bitnami ls  # See postgresql, mongodb, minio directories (each with Chart.yaml)`

**Step 2:** Optionally fetch the latest published chart packages (if not building custom)

For OCI charts - fetch directly helm pull \<oci://registry-1.docker.io/bitnamicharts/postgresql> --version \<latest> helm pull \<oci://registry-1.docker.io/bitnamicharts/mongodb> --version \<latest> helm pull \<oci://registry-1.docker.io/bitnamicharts/minio> --version \<latest>

## **B. Identify All Bitnami Image References**

Each chart (main container and init/sidecar containers) references Bitnami images—these need to be overridden.

`# List all image fields in the chart values and docs grep -E 'repository:' values.yaml grep -E 'repository.*bitnami' README.md`

*E.g. for PostgreSQL:*

- `.Values.image.repository` (postgresql)
- `.Values.metrics.image.repository` (postgres-exporter)
- `.Values.volumePermissions.image.repository` (os-shell)

---

## **C. Pull, Retag, and Push Images to Your Registry**

## **Step 1: Pull All Bitnami Images**

**Determine tags by listing `values.yaml` and published images.**

Example: For PostgreSQL (similar for others)

`# Pull main images docker pull bitnami/postgresql:\<tag> docker pull bitnami/os-shell:\<tag> docker pull bitnami/postgres-exporter:\<tag>`

## **Step 2: Retag for Your Registry**

`# Set your private repo, e.g., myrepo.company.com/bitnami docker tag bitnami/postgresql:\<tag> myrepo.company.com/bitnami/postgresql:\<tag> docker tag bitnami/os-shell:\<tag> myrepo.company.com/bitnami/os-shell:\<tag> docker tag bitnami/postgres-exporter:\<tag> myrepo.company.com/bitnami/postgres-exporter:\<tag>`

## **Step 3: Push**

`docker push myrepo.company.com/bitnami/postgresql:\<tag> docker push myrepo.company.com/bitnami/os-shell:\<tag> docker push myrepo.company.com/bitnami/postgres-exporter:\<tag>`

*Repeat the above for MongoDB and MinIO, matching every image (main and auxiliary) used by each chart/version.*

---

## **D. Chart Customization: Point Charts to Your Images**

You can do this with `--set` overrides in Helm, or by maintaining a custom `values.yaml` in your repo.

**Example override for all images in PostgreSQL:**

`helm upgrade mypostgres \<your-local-chart-path-or-oci-uri> \   --set image.repository=myrepo.company.com/bitnami/postgresql \   --set volumePermissions.image.repository=myrepo.company.com/bitnami/os-shell \   --set metrics.image.repository=myrepo.company.com/bitnami/postgres-exporter`

**For MinIO and MongoDB:**

- Do the same: inspect all `.Values.image.repository`, sidecar repos, volume-perms, exporter, etc.

---

## **E. Automate with a Script**

Here’s an **example shell script** for retagging all images used in a chart values file:

`#!/usr/bin/env bash REPO_SRC="bitnami" REPO_DST="myrepo.company.com/bitnami" CHART_VALUES="values.yaml" IMAGES=$(grep 'repository:' $CHART_VALUES | awk '{print $2}' | grep "$REPO_SRC") TAGS="\<tag>"  # Replace with your desired version/tag(s) for img in $IMAGES; do     for tag in $TAGS; do         docker pull $img:$tag         docker tag $img:$tag $REPO_DST/$(basename $img):$tag         docker push $REPO_DST/$(basename $img):$tag     done done`

---

## **F. Best Practices for Maintenance**

- **Keep a manifest** of all versions/tags used for traceability.
- **Automate regular sync** for chart and image updates (manual if only using “latest”).
- **Test deployments** using the private registry before promoting to prod.
- **Document overrides** in Helm releases for reproducibility.

---

## 3. **Special Cases & Notes**

- **MinIO, Mongo, PostgreSQL**: These were part of the final (September) brownout, so only “latest” free tags remain unless you subscribe or use `bitnamilegacy`. Check if your desired version is present.
- **For production and ongoing stability**: Either build from Bitnami’s open GitHub source (fairly complex), or subscribe for LTS images. Avoid `bitnamilegacy` for long-term—they’re frozen.
- **Sealed Secrets, minideb, charts-syncer**: These are unaffected and operate as before.

---

## 4. **Example Helm Values (after re-homing)**

`image:   repository: myrepo.company.com/bitnami/postgresql  tag: \<your-tag> metrics:   image:    repository: myrepo.company.com/bitnami/postgres-exporter    tag: \<your-tag> volumePermissions:   image:    repository: myrepo.company.com/bitnami/os-shell    tag: \<your-tag>`

`# For MongoDB and MinIO, repeat the pattern as documented in charts/bitnami/[chart]/values.yaml`

---

## 5. **Summary Table: Chart/Registry Migration**

| Chart      | Upstream Source           | Container Registry                    | Private Registry Retag? | Helm Value Override Needed? |
| ---------- | ------------------------- | ------------------------------------- | ----------------------- | --------------------------- |
| postgresql | github.com/bitnami/charts | docker.io/bitnami (now bitnamilegacy) | Yes                     | Yes                         |
| mongodb    | github.com/bitnami/charts | docker.io/bitnami (now bitnamilegacy) | Yes                     | Yes                         |
| minio      | github.com/bitnami/charts | docker.io/bitnami (now bitnamilegacy) | Yes                     | Yes                         |

---

## 6. **Action Checklist**

- List *all* image repos/tags per chart in use.
- Pull, retag, and push each image to your private registry.
- Maintain your own up-to-date repo of Helm chart source or OCI packages.
- Update your deployment jobs (`helm upgrade/install`) to point at your images.
- Consider a CI/CD sync job to automate ongoing mirroring.
- Monitor for any changes in Bitnami repo structure.

---

**References:** All guidance is based on the Bitnami catalog migration issue, FAQ, and your stated use of the three main charts.[github](https://github.com/bitnami/containers/issues/83267)

If you need a ready-to-run bash or Python script to scan and retag images for multiple charts, or sample workflows for popular CI platforms (GitHub Actions, GitLab CI), let me know.

1. [https://github.com/bitnami/containers/issues/83267](https://github.com/bitnami/containers/issues/83267)
