---
aliases: []
confidence: 
created: 2025-09-03T03:27:50Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [helm, image-management, minio, patching, storage]
title: MinIO Image Import & Patching Process
type:
uid: 
updated: 
version:
---

## 🔄 **MinIO Image Import & Patching Process**

Here's the step-by-step process when you run `./import_chart_to_acr.sh --execute bitnami/minio 17.0.21`:

### **1. Chart Discovery & Image Extraction**

```bash
# Pull MinIO chart from Bitnami
helm pull bitnami/minio --version 17.0.21 --untar

# Extract all images from values.yaml
discover_images_in_chart() {
    yq eval '.. | select(has("repository") and has("tag")) | .repository + ":" + .tag' values.yaml
}
```

**Found images:**

- `bitnami/minio:2025.7.23-debian-12-r3`
- `bitnami/minio-client:2025.7.21-debian-12-r2`
- `bitnami/os-shell:12-debian-12-r50`
- `bitnami/minio-object-browser:2.0.2-debian-12-r3`

### **2. Individual Image Processing Loop**

For each image discovered:

#### **Step 2a: Import to ACR**

```bash
import_image_to_acr "$acr_name" "$image"
# Converts: bitnami/minio:2025.7.23-debian-12-r3
# To: az acr import --source docker.io/bitnami/minio:2025.7.23-debian-12-r3
```

#### **Step 2b: Vulnerability Scanning**

```bash
scan_and_patch_image "$acr_name" "fitfileregistry.azurecr.io/bitnami/minio:2025.7.23-debian-12-r3"
```

**Scanning Process:**

1. **Trivy scan**: `trivy image --ignore-unfixed -f json -o scan_file.json`
2. **Vulnerability count**: `jq '.Results | map(.Vulnerabilities | length) | add'`
3. **Decision point**: If vulnerabilities > 0, proceed to patching

#### **Step 2c: Copa Patching (When Needed)**

**Images are patched ONLY when:**

- Trivy finds HIGH or CRITICAL vulnerabilities
- Copa tool is available
- Patching succeeds

**Patching Process:**

```bash
if [ "$vuln_count" -gt 0 ]; then
    # Start BuildKit container
    docker run --detach --privileged --name buildkitd moby/buildkit:v0.12.4

    # Patch with Copa
    copa patch \
        -i "fitfileregistry.azurecr.io/bitnami/minio:2025.7.23-debian-12-r3" \
        -r "scan_file.json" \
        -t "fitfileregistry.azurecr.io/minio-patched" \
        --addr docker-container://buildkitd

    # Push patched image back to ACR
    docker push "fitfileregistry.azurecr.io/minio-patched"
fi
```

### **3. Chart Values Update**

```bash
# Update values.yaml to point to ACR images
rewrite_values_yaml() {
    yq eval -i ".repository = \"fitfileregistry.azurecr.io/bitnami/minio\"" values.yaml
}
```

### **4. Chart Packaging & Push**

```bash
helm package ./minio
helm push minio-17.0.21.tgz oci://fitfileregistry.azurecr.io/helm
```

## 🎯 **Key Points About Patching**

### **When Images Are Patched:**

- **During import process** (not at deployment time)
- **Only if vulnerabilities found** by Trivy scan
- **Automatically** without user intervention

### **In Your MinIO Case:**

- **No patching occurred** because Trivy found **0 vulnerabilities**
- All Bitnami images were already secure
- Images went straight from import → scan → values update

### **If Vulnerabilities Were Found:**

1. Original image: `bitnami/minio:2025.7.23-debian-12-r3`
2. Patched image: `minio-2025-7-23-debian-12-r3-patched`
3. Chart would reference the patched version automatically

The process ensures **zero-vulnerability images** in your ACR before any deployment occurs.
