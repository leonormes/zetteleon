---
aliases: []
confidence: 
created: 2025-11-03T15:29:37Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T15:31:59Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Deploying and Accessing The Hyve Container
type: 
uid: 
updated: 
---

## **Deploying And Accessing The Hyve Container**

This guide outlines the steps to update the `thehyve/fitfile_etl_container_mkuh` image in our Azure Container Registry (ACR) and then access the Airflow dashboard for testing.

**Last Updated:** 2025-11-03

---

### **1. Pull New Image from GitHub Container Registry (GHCR) and Push to Azure Container Registry (ACR)**

This section details how to get the `ghcr.io/thehyve/fitfile_etl_container_mkuh:0.4.4-test` image into our `Fitfileregistry` ACR.

#### **1.1. Authenticate Docker to GitHub Container Registry (GHCR)**

First, ensure your Docker client can pull private images from GHCR using your GitHub CLI token. You last performed this step on **2025-10-24**.

```bash
gh auth refresh -h ghcr.io -s read:packages
gh auth token | docker login ghcr.io -u leonormes --password-stdin
```

#### **1.2. Pull the Hyve Image from GHCR**

Pull the specific image from GHCR to your local machine:

```bash
docker pull ghcr.io/thehyve/fitfile_etl_container_mkuh:0.4.4-test
```

#### **1.3. Authenticate Docker to Azure Container Registry (ACR)**

Log in to our `Fitfileregistry` ACR. You last accessed details about this registry on **2025-11-03**.

```bash
az acr login --name fitfileregistry
```

*(Alternatively, you can use `docker login fitfileregistry.azurecr.io`)*

#### **1.4. Tag the Image for Your ACR**

Retag the pulled image so it references our ACR:

```bash
docker tag ghcr.io/thehyve/fitfile_etl_container_mkuh:0.4.4-test fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_mkuh:0.4.4-test
```

#### **1.5. Push the Image to Your ACR**

Finally, push the retagged image to our `Fitfileregistry` ACR:

```bash
docker push fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_mkuh:0.4.4-test
```

---

### **2. Access the Airflow Dashboard via Port-Forwarding**

Once the new image is available in ACR and deployed to the cluster, you can access the Airflow dashboard for the `thehyve-mkuh` service using port-forwarding. You last used this method on **2025-10-24** to control the Airflow container.

#### **2.1. Confirm the `thehyve-mkuh` Service is running**

First, verify the Kubernetes services in the `thehyve-mkuh` namespace:

```bash
kubectl get services -n thehyve-mkuh
```

#### **2.2. Establish Port-Forwarding**

Create a local port-forward to access the Airflow UI:

```bash
kubectl port-forward svc/thehyve-mkuh -n thehyve-mkuh 8081:8080
```

This command maps your local port `8081` to the container's port `8080`.

#### **2.3. Access Airflow in Your Browser**

Open your web browser and navigate to:

[http://localhost:8081](http://localhost:8081)

#### **2.4. Log in to Airflow**

Use the following credentials when prompted:

-   **Username:** `ffadmin`
-   **Password:** `ffpassword`

#### **2.5. Run Airflow DAGs**

Once logged in, you can manually trigger the necessary DAGs. According to past instructions, run them in this specific order, waiting for each to complete:

1.  `run_dqd`
2.  `run_achilles`
3.  `run_cdmonboarding`
4.  `run_qc_upload`

---
