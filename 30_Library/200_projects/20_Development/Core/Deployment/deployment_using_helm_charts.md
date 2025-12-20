---
aliases: []
confidence: 
created: 2025-02-07T12:57:55Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: deployment_using_helm_charts
type:
uid: 
updated: 
version:
---

Certainly! Below is a documentation draft for the `ff-a` demo deployment, which uses the `charts` directory and overrides specific settings. This documentation will explain the structure and how to make changes to a chart.

---

## FF-A Demo Deployment Documentation

### Overview

The `ff-a` deployment is a demo setup that utilizes the Helm charts from the `charts` directory. It overrides certain default settings to tailor the deployment for demonstration purposes. This document outlines the structure of the `ff-a` deployment and provides guidance on how to make changes to the charts.

### Structure

The `ff-a` deployment is configured using a `values.yaml` file, which overrides default values specified in the base charts. The structure of the `ff-a` values file is as follows:

#### Example Structure

```yaml
###############################
# FF A FFNode chart values    #
###############################

namespace: ff-a
deploymentKey: prod-1

host: app.fitfile.net

applicationVaultPath: ff-a-application

argocdApp:
```

#### Key Components

- namespace: Specifies the Kubernetes namespace for the deployment.
- deploymentKey: A unique identifier for the deployment.
- host: The domain name for accessing the application.
- applicationVaultPath: Path for storing application secrets in Vault.
- argocdApp: Configuration for ArgoCD, including the target revision.

### Overriding Settings

The `ff-a` deployment overrides several global and specific settings from the base charts. Here are some key overrides:

- global.fitConnectCode: Sets a specific code for the FITConnect service.
- global.sleuth: Enables Sleuth for distributed tracing in the production environment.
- argoWorkflows: Configures Argo Workflows with specific TLS and host settings.
- minio.persistence: Configures MinIO persistence settings, including existing claims for PVCs.

### Making Changes to a Chart

To make changes to a chart for the `ff-a` deployment, follow these steps:

1. Identify the Chart: Determine which chart you need to modify. The `ff-a` deployment uses several charts, such as `ffnode`, `frontend`, and `fitconnect`.
2. Edit the `values.yaml`: Modify the `values.yaml` file in the `ff-a` directory to override specific settings. For example, to change the namespace, update the `namespace` field.
3. Update Chart Templates: If necessary, update the templates in the `charts` directory. This might involve modifying Kubernetes resource templates to accommodate new configurations.
4. Test Changes: Deploy the updated chart in a test environment to ensure that all changes work as expected.
5. Document Changes: Update any relevant documentation to reflect changes made to the chart.
6. Version Control: Commit the changes to version control with a descriptive message about the updates.

### Deployment

To deploy the `ff-a` demo, use the following Helm command:

```sh
helm install <release-name> <chart-path> --values ffnodes/fitfile/ff-a/values.yaml
```

Replace `<release-name>` and `<chart-path>` with the appropriate values for your deployment.

---

This documentation provides a high-level overview of the `ff-a` demo deployment and guidelines for making changes to the charts. For more detailed information, refer to the specific files and templates within each chart directory.

Certainly! Below is a documentation draft that describes the structure of the Helm charts in the `charts` directory, what is included, and how to update them.

---

## Helm Charts Documentation

### Overview

The `charts` directory contains the Helm charts used for deploying various components of the FITFILE system. Each subdirectory within `charts` represents a distinct application or service, encapsulating its deployment configuration, templates, and values.

### Structure

The structure of each chart typically includes the following files:

- Chart.yaml: This file contains metadata about the chart, such as its name, version, and description.
- values.yaml: This file contains default configuration values for the chart. These values can be overridden during deployment.
- templates/: This directory contains Kubernetes resource templates that are processed by Helm to generate the final manifests.

#### Example Chart Structure

```sh
charts/
├── <chart-name>/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── templates/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
```

### Key Components

#### Chart.yaml

The `Chart.yaml` file provides essential information about the chart:

- apiVersion: The version of the Helm chart API.
- name: The name of the chart.
- version: The version of the chart itself.
- appVersion: The version of the application being deployed.
- description: A brief description of the chart.

Example:

```yaml
apiVersion: v2
name: storybook
appVersion: "0.1.0"
description: The FITFILE component library in Storybook
version: 0.1.1
type: application

```

#### values.yaml

The `values.yaml` file contains default values for the chart's configuration. These values can be customized by providing a custom `values.yaml` file or using the `--set` flag during deployment.

Example:

```yaml
global:
  app:
    fitfileEnv: production

image:
  repository: fitfileregistry.azurecr.io/frontend
  tag: 0.1.351
replicaCount: 1
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: true
  host: ""
tlsName: cloudflare-tls

sleuth:
  enabled: false
  environment: production
  deploymentName: frontend
  commit:
    sha: c4ac33ee9ac5b96f52f6e162c6c3bce7c99eb9dc

resources: {}

env: {}

volumes:

volumeMounts:

vault:
  enabled: false
  role: ""
  namespace: ""
  path: ""
  secretName: role-secrets

##############
# APP CONFIG #
##############
appConfig:
  mongodb:
    host: ""
  graphqlApiUrl: ""
  restApiUrl: ""
  tenantName: ""
  nextAuthSecret: 2fd583da-26ed-4a07-b984-fc9aefdcd35d
  logLevel: info
  oauthBaseURL: ""
  oauthAudience: ""

features:
  FEATURE_UPDATE_QUERY_PLAN: "false"
  FEATURE_CREATE_QUERY_PLAN: "false"
  FEATURE_DELETE_QUERY_PLAN: "false"

extraDeploy:

```

#### Templates

The `templates` directory contains Kubernetes resource templates. These templates use the Go templating language to allow dynamic configuration based on the values provided.

##### Common Templates

- deployment.yaml: Defines the Deployment resource for the application.
- service.yaml: Defines the Service resource to expose the application.
- ingress.yaml: Defines the Ingress resource for routing external traffic to the application.

Example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "frontend.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  revisionHistoryLimit: 1
  selector:
    matchLabels:
      app: {{ include "frontend.fullname" . }}
  template:
    metadata:
      {{- template "frontend.vault.annotations" . }}
      labels:
        app: {{ include "frontend.fullname" . }}
    spec:
      containers:
      - name: {{ include "frontend.fullname" . }}
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        command:
        args:
          - |
            if
              source /secrets/config;
            else
              echo "No secrets file to source";
            fi;
            node server.js;
        imagePullPolicy: IfNotPresent
        {{- if .Values.resources }}
        resources:
{{ toYaml .Values.resources | indent 10 }}
        {{- end }}
        ports:
        - name: http
          containerPort: 4000
        readinessProbe:
          tcpSocket:
            port: 4000
          initialDelaySeconds: 15
          periodSeconds: 15
        livenessProbe:
          tcpSocket:
            port: 4000
          initialDelaySeconds: 30
          periodSeconds: 15
        env: {{ ternary (toYaml .Values.env | nindent 8) "" (gt (len .Values.env) 0) }}
        - name: FITFILE_ENV
          value: "{{ .Values.global.app.fitfileEnv | default "production" }}"
        - name: GRAPHQL_API_URL
          valueFrom:
            configMapKeyRef:
              name: {{ include "frontend.appconf" . }}
              key: graphqlApiUrl
        - name: TENANT_NAME
          valueFrom:
            configMapKeyRef:
              name: {{ include "frontend.appconf" . }}
              key: tenantName
        - name: NEXTAUTH_SECRET
          valueFrom:
            configMapKeyRef:
              name: {{ include "frontend.appconf" . }}
              key: nextAuthSecret
        - name: NEXTAUTH_URL
          value: "https://{{ .Values.ingress.host }}/fitfile/api/auth"
        - name: REST_API_URL
          valueFrom:
            configMapKeyRef:
              name: {{ include "frontend.appconf" . }}
              key: restApiUrl
        - name: AUTH0_ISSUER
          valueFrom:
            configMapKeyRef:
              name: {{ include "frontend.appconf" . }}
              key: oauthBaseURL
        - name: AUTH0_AUDIENCE
          valueFrom:
            configMapKeyRef:
              name: {{ include "frontend.appconf" . }}
              key: oauthAudience
        - name: LOG_LEVEL
          value: {{ .Values.appConfig.logLevel }}
        - name: FEATURE_UPDATE_QUERY_PLAN
          value: "{{ .Values.features.FEATURE_UPDATE_QUERY_PLAN }}"
        - name: FEATURE_CREATE_QUERY_PLAN
          value: "{{ .Values.features.FEATURE_CREATE_QUERY_PLAN }}"
        - name: FEATURE_DELETE_QUERY_PLAN
          value: "{{ .Values.features.FEATURE_DELETE_QUERY_PLAN }}"
        volumeMounts: {{ toYaml .Values.volumeMounts | nindent 8 }}
      volumes: {{ toYaml .Values.volumes | nindent 8 }}
      {{- if .Values.acrBasicAuth }}
      imagePullSecrets:
        - name: acr
      {{- end }}
```

### Updating Charts

To update a chart, follow these steps:

1. Modify `Chart.yaml`: Update the version and appVersion fields if there are significant changes or updates to the application.
2. Update `values.yaml`: Modify default values as needed. Ensure any new configuration options are documented.
3. Edit Templates: Update the templates in the `templates` directory to reflect any changes in the application's deployment requirements.
4. Test Changes: Use Helm to deploy the updated chart in a test environment to ensure that all changes work as expected.
5. Document Changes: Update any relevant documentation to reflect changes made to the chart.
6. Version Control: Commit the changes to version control with a descriptive message about the updates.

### Deployment

To deploy a chart, use the following Helm command:

```sh
helm install <release-name> <chart-path> --values <custom-values.yaml>
```

Replace `<release-name>`, `<chart-path>`, and `<custom-values.yaml>` with the appropriate values for your deployment.
