---
aliases: []
confidence: 
created: 2025-03-03T13:28:18Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: thehyve templates deployment file
type:
uid: 
updated: 
version:
---

This `deployment.yaml` template defines a Kubernetes Deployment for the "thehyve" application, which appears to be running Airflow (a workflow management platform). Let me break it down section by section:

## Metadata and Basic Structure

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "thehyve.fullname" . }}
  labels:
    {{- include "thehyve.labels" . | nindent 4 }}
```

- This creates a Kubernetes Deployment resource
- The name is generated using the `thehyve.fullname` helper template from `_helpers.tpl`
- Labels are included using the `thehyve.labels` helper template with proper indentation (4 spaces)

## Replica Configuration and Selector

```yaml
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "thehyve.selectorLabels" . | nindent 6 }}
```

- `replicas` is set directly from `.Values.replicaCount` in your `values.yaml`
- The selector uses the `thehyve.selectorLabels` helper to ensure it matches the right pods

## Pod Template Metadata

```yaml
template:
  metadata:
    {{- with .Values.podAnnotations }}
    annotations:
      {{- toYaml . | nindent 8 }}
    {{- end }}
    labels:
      {{- include "thehyve.labels" . | nindent 8 }}
      {{- with .Values.podLabels }}
      {{- toYaml . | nindent 8 }}
      {{- end }}
```

- Pod annotations are added if defined in `values.yaml`
- Pod labels use both the standard `thehyve.labels` helper and any custom labels defined in `values.yaml`
- The `with` statement is a conditional block that only executes if the value exists

## Pod Specifications

```yaml
spec:
  {{- include "thehyve.imagePullSecrets" . | nindent 6 }}
  serviceAccountName: {{ include "thehyve.serviceAccountName" . }}
  securityContext:
    {{- toYaml .Values.podSecurityContext | nindent 8 }}
```

- Image pull secrets are included using the helper template
- Service account name is resolved using another helper
- Pod security context is directly mapped from values

## Init Container

```yaml
initContainers:
  - name: thehyve-init
    image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
    imagePullPolicy: Always
    command: ['/bin/bash', '-c']
    args:
      - |
        airflow db upgrade && \
        sleep 5 && \
        airflow db init && \
        {{- if .Values.airflow.initAdmin.enabled -}}
        airflow users create \
            --username $AIRFLOW_ADMIN_USERNAME \
            --password $AIRFLOW_ADMIN_PASSWORD \
            --firstname $AIRFLOW_ADMIN_FIRSTNAME \
            --lastname $AIRFLOW_ADMIN_LASTNAME \
            --role Admin \
            --email $AIRFLOW_ADMIN_EMAIL
        {{- else -}}
        echo "Init admin is not enabled"
        {{- end }}
    env: {{ include "thehyve.env" . | nindent 10 }}
```

- Defines an initialization container that runs before the main containers
- Uses a bash script to:
  - Upgrade the Airflow database
  - Initialize the database
  - Conditionally create an admin user if enabled in values
- Environment variables are included from the `thehyve.env` helper template

## Main Containers

The template defines two containers running in the same pod:

### Webserver Container

```yaml
containers:
  - name: webserver
    securityContext:
      {{- toYaml .Values.securityContext | nindent 12 }}
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
    imagePullPolicy: {{ .Values.image.pullPolicy }}
    resources: {{ toYaml .Values.webserver.resources | nindent 12 }}
    command: ["airflow", "webserver"]
    ports:
      - name: http
        containerPort: {{ .Values.service.port }}
        protocol: TCP
    livenessProbe:
      {{- toYaml .Values.livenessProbe | nindent 12 }}
    readinessProbe:
      {{- toYaml .Values.readinessProbe | nindent 12 }}
    {{- with .Values.volumeMounts }}
    volumeMounts:
      {{- toYaml . | nindent 12 }}
    {{- end }}
    env: {{ include "thehyve.env" . | fromYamlArray | toYaml | nindent 12 }}
```

- Runs the Airflow webserver component
- Config includes security context, probes, resources from values
- Environment variables come from the helper template with additional processing

### Scheduler Container

```yaml
- name: scheduler
  securityContext:
    {{- toYaml .Values.securityContext | nindent 12 }}
  image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
  imagePullPolicy: {{ .Values.image.pullPolicy }}
  resources: {{ toYaml .Values.scheduler.resources | nindent 12 }}
  command: ["airflow", "scheduler"]
  env: {{ include "thehyve.env" . | fromYamlArray | toYaml | nindent 12 }}
```

- Runs the Airflow scheduler component
- Shares most configuration with the webserver container
- The key difference is the command it runs

## Additional Pod Configuration

```yaml
{{- with .Values.volumes }}
volumes:
  {{- toYaml . | nindent 8 }}
{{- end }}
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 8 }}
{{- end }}
{{- with .Values.affinity }}
affinity:
  {{- toYaml . | nindent 8 }}
{{- end }}
{{- with .Values.tolerations }}
tolerations:
  {{- toYaml . | nindent 8 }}
{{- end }}
```

- These sections all conditionally include various Kubernetes pod configurations:
  - Volumes for persistent storage
  - Node selector for pod placement
  - Affinity rules for pod scheduling
  - Tolerations for node taints

## Key Template Techniques Used

1. **Template Inclusion**: `{{ include "template.name" . }}` calls helper templates
2. **Indentation Control**: `| nindent X` ensures proper YAML formatting
3. **Conditional Blocks**: `{{- with .Values.X }}` and `{{- if .Values.X }}` sections
4. **Default Values**: `{{ .Values.X | default "fallback" }}`
5. **YAML Transformation**: `toYaml`, `fromYamlArray`
6. **Multiline Handling**: Using the YAML pipe operator `|` for the init container script

This deployment template showcases how powerful Helm templating can be - it's parameterizing a complex Kubernetes deployment with multiple containers that need specific configuration, while keeping the actual manifest clean and maintainable.

Good question about why files like `deployment.yaml` have a `.yaml` extension instead of `.tpl` despite containing template directives. This reflects Helm's intended design and workflow:

## Why YAML Extensions and Not TPL

1. **Final Output Format**: The `.yaml` extension reflects the final output format - these files will ultimately become Kubernetes YAML manifests after template processing. This helps developers visualize the end product.
2. **Separation of Concerns**:
   - `.yaml` files: These are intended to be rendered into complete Kubernetes manifests
   - `.tpl` files (like `_helpers.tpl`): These are *not* rendered directly but contain shared template fragments for inclusion in other files

3. **Helm's Processing Model**: Helm processes all files in the `templates/` directory *except* those with names beginning with underscore (like `_helpers.tpl`). Files starting with underscore are considered "partial templates" or helpers.
4. **IDE and Tool Support**: Many IDEs and tools provide YAML syntax highlighting and Kubernetes schema validation, which is beneficial when working with `.yaml` files.

## How Helm Processes Files

Here's how Helm processes these files:

1. When you run `helm install` or `helm template`:
   - Helm reads all non-hidden, non-underscore prefixed files in the `templates/` directory
   - Each file is processed as a Go template, regardless of extension
   - The result is a set of Kubernetes manifests

2. During template processing:
   - Template directives (`{{ ... }}`) are evaluated
   - Helper templates defined in `_helpers.tpl` can be included
   - The output is expected to be valid YAML

## Common Patterns in Helm Charts

The pattern you're seeing in your repository follows Helm best practices:

1. **Resource Definition Files**: Individual Kubernetes resources get their own `.yaml` files (deployment.yaml, service.yaml, etc.)
2. **Helper Templates**: Reusable template fragments go in `_helpers.tpl`
3. **Note Files**: Sometimes you'll see `NOTES.txt` which is rendered and displayed to the user after installation

This structure helps maintain organization while preserving the connection to the final Kubernetes manifest output format. It makes the charts more maintainable and aligns with how most Helm charts are structured in the community.
