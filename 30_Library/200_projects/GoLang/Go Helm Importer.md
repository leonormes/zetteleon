---
aliases: []
confidence: 
created: 2025-10-22T03:17:39Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:24Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Go Helm Importer
type:
uid: 
updated: 
version:
---

## 🎯 **Chart Manager CLI Overview**

This is a sophisticated Go-based CLI tool for importing Helm charts and their container images to Azure Container Registry (ACR), with automatic chart modification to use the imported images.

## 🚀 **Core Import Workflow Features**

### **1. Complete Import Command**

```bash
chart-manager import <chart-name> [flags]
```

**Key Capabilities:**

- **One-command workflow**: Pulls chart → extracts images → imports to ACR → modifies chart → validates result
- **Multi-source support**: Works with Helm repos, OCI registries, and local charts
- **Smart version handling**: Automatically detects and handles version prefixes ('v' vs no 'v')
- **Dry-run mode**: `--dry-run` flag for safe testing without making changes

### **2. Chart Acquisition & Processing**

#### **Chart Pulling ([internal/helm/chart_puller.go](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/helm/chart_puller.go:0:0-0:0))**

```go
type ChartPuller interface {
    PullChart(source ChartSource, destDir string) (*ChartInfo, error)
    ListVersions(source ChartSource) ([]string, error)
    CleanupChart(chartInfo *ChartInfo) error
}
```

**Features:**

- **Multiple source types**: Traditional Helm repos, OCI registries, HTTP URLs, local files
- **Version flexibility**: Supports specific versions, latest versions, or version ranges
- **Automatic extraction**: Downloads and extracts chart archives
- **Metadata preservation**: Maintains chart metadata and file structure

#### **Image Discovery ([internal/helmextractor/extractor.go](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/helmextractor/extractor.go:0:0-0:0))**

```go
type ImageExtractor interface {
    Extract(chartPath string, opts RenderOptions) (*ExtractionResult, error)
}
```

**Advanced Image Detection:**

- **Helm template rendering**: Uses Helm's engine to render all templates with values
- **Kubernetes resource parsing**: Analyzes Deployments, StatefulSets, DaemonSets, Jobs, CronJobs, Pods
- **Container spec extraction**: Handles main containers, init containers, and ephemeral containers
- **Template-aware parsing**: Detects Helm template expressions (`{{ .Values.image }}`)
- **Fallback extraction**: Falls back to `values.yaml` parsing if template rendering fails
- **Intelligent filtering**: Avoids false positives (file paths, URLs, config files)

### **3. Image Import to ACR**

#### **ACR Integration ([internal/acr/importer.go](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:0:0-0:0))**

```go
type ACRImporter interface {
    ImportImages(pullResult *images.PullResult, registry string) (*ImportResult, error)
    ImportSingleImage(img helmimages.ImageReference, registry string) (*ImportedImage, error)
}
```

**Import Capabilities:**

- **Batch processing**: Imports multiple images efficiently
- **Error resilience**: Continues with remaining images if individual imports fail
- **Authentication handling**: Uses Azure CLI authentication
- **Duplicate detection**: Skips images that already exist in ACR
- **Progress tracking**: Detailed success/failure reporting per image

#### **Image Processing Strategies (`internal/imageops/`)**

- **Multiple import modes**: Docker-based, Azure-enhanced, with retry logic
- **Platform awareness**: Supports multi-architecture images
- **Security scanning**: Optional Trivy integration for vulnerabilities
- **Performance optimization**: Concurrent processing for large image sets

### **4. Chart Modification & Update**

#### **Direct Chart Modification (`internal/chartmod/modifier.go`)**

```go
type ChartModifier interface {
    ModifyChart(chartPath string, images []helmimages.ImageReference, acrName string) (*ModificationResult, error)
}
```

**Smart Modification Features:**

- **Direct values.yaml editing**: Modifies the chart's `values.yaml` file directly (no override files needed!)
- **Automatic backups**: Creates `.backup` files before modifications
- **Strategy-based updates**: Different modification strategies per chart type:
  - `ArgoCDStrategy`: Handles ArgoCD-specific image references
  - `PostgreSQLStrategy`: Database-specific modifications
  - `RedisStrategy`: Redis chart optimizations
  - `GenericStrategy`: Fallback for unknown charts
- **Template preservation**: Maintains Helm template syntax and structure
- **Validation**: Ensures modified charts still render correctly

#### **Image Mapping System (`internal/helmimages/`)**

- **Registry translation**: Converts external registries to ACR format
- **Repository normalization**: Standardizes repository naming conventions
- **Tag preservation**: Maintains version tags and digests
- **Multi-format support**: Handles both simple tags and digest references

### **5. Validation & Safety**

#### **End-to-End Validation (`internal/validation/validator.go`)**

```go
type Validator interface {
    ValidateACRImports(result *acr.ImportResult) error
    ValidateHelmOverrides(modResult *chartmod.ModificationResult) error
    ValidateCompleteWorkflow(chartPath, acrName string) error
}
```

**Validation Checks:**

- **ACR import verification**: Confirms all images were imported successfully
- **Helm template validation**: Ensures modified charts still render
- **Registry access testing**: Verifies ACR accessibility
- **Image accessibility**: Tests that imported images are pullable

#### **Prerequisites Checking (`internal/prerequisites/`)**

- **Tool validation**: Ensures Azure CLI, Helm, Docker are installed
- **Authentication verification**: Checks Azure login status
- **ACR access validation**: Confirms registry permissions
- **Network connectivity**: Tests external registry access

### **6. Advanced Features**

#### **Configuration Management (`internal/config/`)**

- **YAML-based configuration**: Centralized chart definitions in `helm_chart_list.yaml`
- **Environment flexibility**: Supports multiple ACR registries and environments
- **Chart categorization**: Separates terraform-managed vs argocd-managed charts
- **Version constraints**: Configurable version ranges and update policies

#### **Concurrent Processing (`internal/comparison/`)**

- **Parallel chart checking**: Concurrent version checking across multiple charts
- **Batch import optimization**: Parallel image imports for performance
- **Resource management**: Proper concurrency control and error aggregation

#### **Error Recovery & Resilience**

- **Graceful degradation**: Continues processing when individual operations fail
- **Retry logic**: Automatic retries for transient failures
- **Partial success handling**: Reports both successes and failures clearly
- **Rollback capabilities**: Backup restoration on failures

## 📋 **CLI Usage Examples**

```bash
# Basic import
chart-manager import postgresql --version 16.7.27

# Import with verbose output and custom registry
chart-manager import mongodb --verbose --acr fitfilepublic

# Dry run to see what would be imported
chart-manager import redis --dry-run

# Import specific version from OCI registry
chart-manager import argocd --version v2.8.0 --repo oci://ghcr.io/argoproj/argo-helm
```

## 🎯 **Key Differentiators**

1. **Direct Chart Modification**: Unlike most tools that create override files, this modifies the chart's `values.yaml` directly
2. **Complete Workflow Automation**: Single command handles the entire import → modify → validate pipeline
3. **Helm-Aware Processing**: Uses proper Helm template rendering for accurate image discovery
4. **ACR-Optimized**: Built specifically for Azure Container Registry with authentication handling
5. **Production-Ready**: Comprehensive error handling, validation, and rollback capabilities

This CLI tool essentially automates the complex process of migrating Helm charts from public registries to private ACR infrastructure while maintaining all functionality and providing robust error handling throughout the process.
