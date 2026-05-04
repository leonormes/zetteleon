# Local Dev

## Chart Structure Analysis

### 1\. List of Charts and Subcharts

- Main Chart: `seed-data`

   - Version: 1.0.0

   - Subcharts: None explicitly listed in the provided snippets.

### 2\. Chart Details

#### `seed-data` Chart

- Chart Version: 1.0.0

- apiVersion Requirements: v2

- Kubernetes Resource Types Created:

   - ConfigMap

   - Secret

   - Job

- Conditional Resources:

   - Resources related to `spicedb` are conditional based on `.Values.spicedb.enabled` (e.g., `seed-spicedb-configmap.yaml`, `seed-spicedb-job.yaml`, `seed-spicedb-secret.yaml`).

## Dependencies and Requirements

### 1\. External Dependencies

- Required Kubernetes Version: Not explicitly mentioned, but Helm v2 charts typically require Kubernetes 1.16+.

- Required Cloud Provider Resources/Services:

   - Azure Storage for downloading blobs (e.g., `azure-storage-secret.yaml`).

- Third-party Services or Systems Needed:

   - Azure CLI for downloading data.

   - PostgreSQL and MongoDB databases.

- Required Secrets and Their Format:

   - `azure-storage-secret`: Contains `account-key` and `account-name`.

   - `spicedb`: Contains `SPICEDB_GRPC_PRESHARED_KEY`.

- Required ConfigMaps:

   - `spicedb-init-scripts`: Contains initialization scripts for `spicedb`.

### 2\. Internal Dependencies

- Subchart Dependencies: None explicitly listed.

- Dependency Version Constraints: Not specified.

- Ordering Requirements in Deployment: Not specified, but jobs and secrets should be created before they are used by other resources.

## Variables and Configuration

### 1\. Required Variables

| Variable | Required | Type | Default | Description | Validation Rules | 
|---|---|---|---|---|---|
| `spicedb.enabled` | Y | boolean | true | Enables `spicedb` related resources | Must be a boolean | 
| `spicedb.tenantId` | Y | string | N/A | Tenant ID for `spicedb` | Must be a valid UUID | 
| `spicedb.projectId` | Y | string | N/A | Project ID for `spicedb` | Must be a valid UUID | 
| `spicedb.presharedKey` | Y | string | N/A | Pre-shared key for `spicedb` | Must be a valid string | 
| `postgresql.secretName` | Y | string | `dev-postgresql` | Secret name for PostgreSQL credentials | Must be a valid secret name | 
| `mongodb.secretName` | Y | string | `dev-mongodb` | Secret name for MongoDB credentials | Must be a valid secret name | 

### 2\. Optional Variables

| Variable | Impact | Recommended Values | 
|---|---|---|
| `extraDeploy` | Allows additional resources to be deployed | Depends on use case | 

## Validation Requirements

### 1\. Required Variable Validation

- `spicedb.tenantId` and `spicedb.projectId`: Must be valid UUIDs.

- `spicedb.presharedKey`: Should be a non-empty string.

- `postgresql.secretName` and `mongodb.secretName`: Must reference existing secrets.

## Security Considerations

### 1\. Security Requirements

- Required RBAC Permissions: Not explicitly mentioned, but access to secrets and configmaps is required.

- Security Context Requirements: Not specified.

- Network Policy Requirements: Not specified.

- Secret Management Needs: Secrets must be securely managed and should not be hardcoded.

## Additional Considerations

- Breaking Changes: None specified.

- Cloud-provider Specific Requirements: Azure-specific configurations for storage access.

- Performance Implications: Not specified, but resource requests and limits should be reviewed for performance tuning.

- Security-sensitive Settings: Ensure secrets are encrypted and access is restricted.

This analysis is based on the provided snippets and may need to be adjusted if additional context is available.

The `start_local_dev_environment.sh` script is designed to set up a local development environment using Kubernetes and ArgoCD. Here's how it interacts with the `local-dev` charts to create a working cluster:

1. Environment Setup:

   - The script begins by setting up environment variables and checking for necessary dependencies like Docker, k3d, and Helm. It ensures that the required tools are installed and available on the system.

2. K3d Cluster Creation:

   - The script checks if a k3d cluster named `local-dev` already exists. If not, it creates one using the `k3d cluster create` command. This involves setting up a local Kubernetes cluster with a specified registry configuration.

   - It uses the `REGISTRY_YAML_FILE_PATH` to configure the registry, which points to `charts/local-dev/registries.yaml`.

3. Namespace and Resource Setup:

   - The script ensures that necessary namespaces (`argocd`, `argo`, `spicedb`) exist in the cluster. If they don't, it creates them using `kubectl create namespace`.

4. ArgoCD Installation:

   - The script installs ArgoCD using Helm. It specifies the chart version and uses values files located in the `charts/local-dev` directory:

      - `argocd-values.yaml` for the ArgoCD installation.

      - `argocd-apps-values.yaml` for the ArgoCD applications.

   - These values files contain configurations for ArgoCD and its applications, including resource requests, RBAC settings, and repository configurations.

5. Secret Management:

   - The script checks for the existence of certain secrets (e.g., `acr`, `argocd-acr-pull-secret`) and creates them if they don't exist. These secrets are crucial for accessing container registries and other services.

6. ConfigMap and Secret Creation:

   - It creates a ConfigMap named `dev-user` with the `AUTH0_USER_ID` from the environment variables. This is used by the `spicedb` components as specified in the `charts/local-dev/seed/values.yaml`.

7. SpiceDB and Database Seeding:

   - The script indirectly triggers the seeding of databases (PostgreSQL, MongoDB) and the setup of SpiceDB through the Helm charts. The `seed` chart contains jobs and scripts for initializing these databases with necessary data.

8. Final Instructions:

   - After setting up the cluster, the script provides instructions for monitoring the cluster's progress and accessing the ArgoCD UI.

### Relevant Code Blocks

- Environment Setup and Dependency Check:

```sh
#!/usr/bin/env bash

set -e

BASEDIR=$(dirname "$0")
ARGOCD_CHART_VERSION="6.5.0"
ARGOCD_APPS_CHART_VERSION="1.6.2"
POSTGRESQL_HOST_NAME=dev-postgresql

############################################################
# Functions                                                #
############################################################

# Determine what OS the host machine is using
GetOS() {
  unameOut="$(uname -s)"
  case "${unameOut}" in
      Linux)     machine=Linux;;
      Darwin)    machine=Mac;;
      CYGWIN)    machine=Windows;;
      MINGW)     machine=Windows;;
      )          machine="UNKNOWN:${unameOut}"
  esac
  echo "${machine}"
}

OS=$(GetOS)

DoesResourceExist() {
  kubectl get $@ > /dev/null 2>&1
}

PrintDivider() {
  echo ""
  printf '%s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' \#
  echo ""
}

PingPostgresql() {
  if [[ "$OS" == "Windows" ]]; then
    ping $POSTGRESQL_HOST_NAME -n 1 2>/dev/null
  else
    ping $POSTGRESQL_HOST_NAME -c 1 2>/dev/null
  fi
}

############################################################
# Env Check                                                #
############################################################

if [[ "$ACR_SERVICE_PRINCIPLE_ACCESS_KEY" == "" ]]; then
    echo -e "ERROR:\tMissing ACR_SERVICE_PRINCIPLE_ACCESS_KEY from environment variables.\n\n\tClick the link below, sign in, and copy one of the passwords:\n\n\thttps://portal.azure.com/#@fitfile.com/resource/subscriptions/a085dd04-19aa-4d2b-9a35-e438097d84fc/resourceGroups/fitfile-shared-container-registry-rg/providers/Microsoft.ContainerRegistry/registries/Fitfileregistry/accessKey\n"
    exit 1
fi

if [[ "$AUTH0_USER_ID" == "" ]]; then
    echo -e "ERROR:\tMissing AUTH0_USER_ID from environment variables.\n\n\tClick the link below, sign in, select your user, and copy your user ID:\n\n\thttps://manage.auth0.com/dashboard/eu/fitfile-test/users\n"
    exit 1
fi

if [[ "$REGISTRY_PORT" == "" ]]; then
  REGISTRY_PORT=5001
fi

if [[ "$REGISTRY_YAML_FILE_PATH" == "" ]]; then
  REGISTRY_YAML_FILE_PATH="$BASEDIR/charts/local-dev/registries.yaml"
fi

set +e
IS_POSTGRESQL_HOST_MAPPING_ADDED=$(PingPostgresql | grep -E -i '(0.0% packet loss|0% loss)')
set -e


############################################################
# Tooling                                                  #
############################################################

echo -e "Checking dependencies are installed"

if ! command -v docker &> /dev/null
then
  echo "$ERROR_LEVEL: You must install docker desktop"
  exit 1
fi

DEPENDENCIES="k3d:k3d helm:helm"

for i in $DEPENDENCIES; do
  IFS=":"
  set -- $i
  echo $1 and $2
  if ! command -v $1 &> /dev/null
  then
    if [[ "$OS" == "Windows" ]]; then
      PrintDivider
      echo "Missing command line dependency $1. Please install using chocolatey and reload your shell"
      PrintDivider
      exit 1
    else
      echo "Missing command line dependency $1. Will install via brew"
      time brew install $2
    fi
  fi
done
```

- K3d Cluster Creation:

```sh

echo "Checking if a k3d cluster already exists"

set +e
k3d_cluster=$(k3d cluster list | grep "local-dev")
set -e

echo "(${k3d_cluster})"

if [[ "$k3d_cluster" == "" ]]; then
  echo "Creating k3d cluster"
  # https://github.com/k3d-io/k3d/issues/1063
  # export K3D_FIX_MOUNTS=1
  set +e
  existing_registry=$(k3d registry list | grep k3d-registry.localhost)
  set -e
  if [[ "$existing_registry" == "" ]]; then
    k3d registry create registry.localhost --port $REGISTRY_PORT
  fi

  echo "k3d cluster create local-dev -p "8081:80@loadbalancer" --registry-use=k3d-registry.localhost:$REGISTRY_PORT --registry-config=$REGISTRY_YAML_FILE_PATH"


  k3d cluster create local-dev -p "8081:80@loadbalancer" --registry-use=k3d-"registry.localhost:$REGISTRY_PORT" --registry-config="$REGISTRY_YAML_FILE_PATH"
else
  k3d cluster start local-dev
fi
```

- Namespace and Resource Setup:

```sh
kubectl config use-context k3d-local-dev

DoesResourceExist namespace argocd && echo "namespace argocd already exists" || kubectl create namespace argocd
DoesResourceExist namespace argo && echo "namespace argo already exists" || kubectl create namespace argo
DoesResourceExist namespace spicedb && echo "namespace spicedb already exists" || kubectl create namespace spicedb
```

- ArgoCD Installation:

```sh
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade --install -n argocd --version $ARGOCD_CHART_VERSION  argocd argo/argo-cd -f "$BASEDIR/charts/local-dev/argocd-values.yaml"

sleep 5

helm upgrade --install -n argocd --version $ARGOCD_APPS_CHART_VERSION argocd-apps argo/argocd-apps -f "$BASEDIR/charts/local-dev/argocd-apps-values.yaml"
```

- Secret Management:

```sh
DoesResourceExist secret acr && \
    echo "secret docker-registry already exists" || \
    kubectl create secret docker-registry acr --docker-server=fitfileregistry.azurecr.io --docker-username=Fitfileregistry --docker-password="$ACR_SERVICE_PRINCIPLE_ACCESS_KEY"
DoesResourceExist secret acr -n argo && \
    echo "secret docker-registry already exists" || \
    kubectl create secret docker-registry acr -n argo --docker-server=fitfileregistry.azurecr.io --docker-username=Fitfileregistry --docker-password="$ACR_SERVICE_PRINCIPLE_ACCESS_KEY"
DoesResourceExist secret acr -n spicedb && \
    echo "secret docker-registry already exists" || \
    kubectl create secret docker-registry acr -n spicedb --docker-server=fitfileregistry.azurecr.io --docker-username=Fitfileregistry --docker-password="$ACR_SERVICE_PRINCIPLE_ACCESS_KEY"

DoesResourceExist secret argocd-acr-pull-secret -n argocd && \
    echo "secret argocd-acr-pull-secret already exists" || \
    kubectl create secret generic argocd-acr-pull-secret -n argocd \
      --from-literal=name=fitfileregistry \
      --from-literal=username=Fitfileregistry \
      --from-literal=password="$ACR_SERVICE_PRINCIPLE_ACCESS_KEY" \
      --from-literal=type=helm \
      --from-literal=enableOCI=true \
      --from-literal=url=fitfileregistry.azurecr.io \
      --from-literal=ForceHttpBasicAuth=true && kubectl label secret \
        -n argocd argocd-acr-pull-secret \
        app.kubernetes.io/instance=argocd \
        argocd.argoproj.io/secret-type=repository \
        app.kubernetes.io/part-of=argocd

DoesResourceExist configmap dev-user && \
    echo "configmap dev-user already exists" || \
    kubectl create configmap dev-user --from-literal=user_id="$AUTH0_USER_ID"
```

- ConfigMap and Secret Creation:

```yaml
  userId:
    secretName: dev-user
```

- SpiceDB and Database Seeding:

```yaml
{{- if eq .Values.spicedb.enabled true }}
apiVersion: batch/v1
kind: Job
metadata:
  name: seed-spicedb-relationships
spec:
  template:
    spec:
      containers:
        - name: seed
          image: authzed/zed:v0.14.0-debug
          command: ["/bin/sh", "-c"]
          args: ["/scripts/seed.sh"]
          env:
            - name: SPICEDB_HOST
              value: {{.Values.spicedb.host}}
            - name: TENANT_ID
              value: {{.Values.spicedb.tenantId}}
            - name: PROJECT_ID
              value: {{.Values.spicedb.projectId}}
            - name: AUTH0_USER_ID
              valueFrom:
                configMapKeyRef:
                  name: {{.Values.spicedb.userId.secretName}}
                  key: user_id
            - name: SPICEDB_PRESHARED_KEY
              valueFrom:
                secretKeyRef:
                  name: spicedb
                  key: SPICEDB_GRPC_PRESHARED_KEY
          volumeMounts:
            - name: seed-data
              mountPath: /mnt/seed
            - name: scripts
              mountPath: /scripts
      restartPolicy: Never
      volumes:
        - name: seed-data
          emptyDir: {}
        - name: scripts
          configMap:
            name: spicedb-init-scripts
            defaultMode: 0777
  backoffLimit: 4
```

This setup ensures that the local development environment is configured with all necessary components and dependencies, allowing developers to work with a fully functional Kubernetes cluster locally.

To list all the images used to start the local cluster, we need to examine both the `start_local_dev_environment.sh` script and the `local-dev` Helm charts. Here's a summary of the images identified:

### From `start_local_dev_environment.sh`

The script itself does not directly specify Docker images, but it sets up the environment for deploying applications using Helm charts, which do specify images.

### From `local-dev` Helm Charts

1. Seed SpiceDB Job:

   - Image: `authzed/zed:v0.14.0-debug`

```yaml
image: authzed/zed:v0.14.0-debug
```

1. Seed PostgreSQL Job:

   - Image: `postgres:15.3-alpine`

```yaml
image: postgres:15.3-alpine
```

1. Seed PostgreSQL Demo EHR Data Job:

   - Image: `postgres:15.3-alpine`

```yaml
image: postgres:15.3-alpine
```

1. Seed MongoDB Job:

   - Image: `mongo:5.0.10`

```yaml
image: mongo:5.0.10
```

1. ArgoCD Vault Plugin:

   - Image: `registry.access.redhat.com/ubi8` (used in initContainers)

```yaml
image: registry.access.redhat.com/ubi8
```

1. ArgoCD Helm Plugin:

   - Image: `quay.io/argoproj/argocd:v2.10.1`

```yaml
image: quay.io/argoproj/argocd:v2.10.1
```

These images are used in various jobs and containers defined in the Helm charts to set up the local development environment.

# Comprehensive Analysis for Local Development Environment Setup

## 1\. Prerequisites

### Minimum Hardware Specifications

- CPU: Dual-core processor

- RAM: 8 GB

- Disk Space: 20 GB free space

### Operating System Compatibility

- Linux: Ubuntu 20.04 or later

- macOS: macOS 10.15 (Catalina) or later

- Windows: Windows 10 Pro or Enterprise (with WSL2)

### Required System Configurations

- Virtualization: Enabled in BIOS/UEFI

- Network: Stable internet connection

## 2\. Tool Dependencies

| Component | Minimum Version | Recommended Version | Notes | 
|---|---|---|---|
| Docker | 20\.10.0 | 24\.0.0 | Required for k3d | 
| k3d | 5\.0.0 | Latest | Local Kubernetes cluster | 
| Helm | 3\.5.0 | Latest | Kubernetes package manager | 
| kubectl | 1\.20.0 | Latest | Kubernetes command-line tool | 
| krew | 0\.4.0 | Latest | kubectl plugin manager | 

### OS-Specific Variations

- Windows: Requires WSL2 for Docker Desktop

- macOS: Homebrew is recommended for package management

## 3\. Installation Sequence

### Ordered List of Installation Steps

1. Install Docker

   - Linux:

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

- Windows: Install Docker Desktop with WSL2 backend

- macOS:

```sh
brew install --cask docker
```

1. Install k3d

- Linux/macOS:

```bash
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

- Windows: Use Chocolatey

```powershell
choco install k3d
```

1. Install Helm

- Linux/macOS:

```bash
brew install helm
```

- Windows:

```powershell
choco install kubernetes-helm
```

1. Install kubectl

- Linux/macOS:

```bash
brew install kubectl
```

- Windows:

```powershell
choco install kubernetes-cli
```

1. Install krew

- All OS:

```bash
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m)" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)
```

### Dependencies Between Components

- Docker must be installed before k3d.

- kubectl is required for interacting with the Kubernetes cluster.

### Critical Configuration Requirements

- Ensure Docker is running before starting k3d.

- Set up environment variables for Azure and Auth0 as required by the script.

## 4\. Configuration Requirements

- Environment Variables:

   - `ACR_SERVICE_PRINCIPLE_ACCESS_KEY`: Azure Container Registry access key

   - `AUTH0_USER_ID`: Auth0 user ID

   - `REGISTRY_PORT`: Port for local registry (default: 5001)

## 5\. Verification Steps

### Commands to Verify Successful Installation

- Docker:

```bash
docker --version
```

- Expected Output: `Docker version 20.10.0, build ...`

- k3d:

```bash
k3d --version
```

- Expected Output: `k3d version v5.0.0`

- Helm:

```bash
helm version
```

- Expected Output: `version.BuildInfo{Version:"v3.5.0", ...}`

- kubectl:

```bash
kubectl version --client
```

- Expected Output: `Client Version: v1.20.0`

### Common Error Checks

- Ensure Docker daemon is running.

- Verify network connectivity for downloading packages.

## 6\. Troubleshooting Guide

- Docker Issues: Ensure Docker Desktop is running (Windows/macOS).

- k3d Cluster Not Starting: Check Docker resources (CPU/RAM) allocation.

- Helm Chart Deployment Fails: Verify Kubernetes context is set correctly.

## 7\. Resource Requirements

- CPU: Dual-core processor

- RAM: 8 GB minimum

- Disk Space: 20 GB free space

## 8\. Network Requirements

- Ports: Ensure ports 5001 (registry) and 8081 (k3d load balancer) are open.

- Internet: Required for downloading dependencies and Docker images.