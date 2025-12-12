---
aliases: []
confidence: 
created: 2025-10-22T02:54:03Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:24Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [go]
title: My Go Importer
type:
uid: 
updated: 
version:
---

## ACR Import Algorithm & Go Code Explanation

Since you're new to Go, I'll break this down step by step. This file implements an algorithm to **import Docker container images from external registries into Azure Container Registry (ACR)**.

### 🎯 What the Import Algorithm Does

**Problem**: You have Docker images stored in public registries (like Docker Hub, Quay.io) that you want to copy to your private Azure Container Registry.

**Solution**: This code automatically imports images from external sources to ACR using Azure CLI commands.

**High-level Algorithm**:

1. **Input**: List of images to import + target ACR name
2. **Process**: For each image, run `az acr import` command
3. **Output**: Success/failure results + new ACR image references

### 📁 Parts of the Go File

#### 1. **Package Declaration**

```go
package acr
```

- Groups related code together
- Other files can import this with `import "example.com/project/chart-manager/internal/acr"`

#### 2. **Imports Section**

```go
import (
    "fmt"           // String formatting
    "os/exec"       // Run external commands
    "strings"       // String manipulation
    "time"          // Time handling

    // Internal project packages
    "example.com/project/chart-manager/internal/helmimages"
    "example.com/project/chart-manager/internal/images"
)
```

- Brings in external and internal code libraries

#### 3. **Interface Definition**

```go
type ACRImporter interface {
    ImportImages(pullResult *images.PullResult, registry string) (*ImportResult, error)
    ImportSingleImage(img helmimages.ImageReference, registry string) (*ImportedImage, error)
    // ... more methods
}
```

- **Interface**: Defines what methods an ACR importer must have
- **Contract**: Any type that implements these methods can be used as an ACRImporter
- **Polymorphism**: Code can work with different implementations

#### 4. **Data Structures (Types)**

##### **Result Types**

```go
type ImportResult struct {
    Registry       string          `json:"registry"`
    ImportedImages []ImportedImage `json:"imported_images"`
    FailedImports  []ImportError   `json:"failed_imports"`
    Summary        ImportSummary   `json:"summary"`
    StartTime      time.Time       `json:"start_time"`
    EndTime        time.Time       `json:"end_time"`
}
```

- **Structs**: Group related data together
- **JSON tags**: Control how structs serialize to JSON
- **Embedded types**: [ImportSummary](cci:2://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:58:0-64:1) is nested inside [ImportResult](cci:2://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:31:0-38:1)

##### **Implementation Type**

```go
type acrImporter struct {
    azCLIBinary string  // Path to Azure CLI binary
    dryRun      bool    // Whether to simulate imports
}
```

- **Private struct**: Actual implementation of the interface
- **Fields**: Configuration data

#### 5. **Constructor Functions**

```go
func NewACRImporter() ACRImporter {
    return &acrImporter{
        azCLIBinary: "az",
        dryRun:      false,
    }
}
```

- **Factory functions**: Create and return new instances
- **Return interface**: Returns [ACRImporter](cci:2://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:13:0-28:1) interface, not concrete type
- **Default values**: Sensible defaults for common usage

#### 6. **Main Algorithm Methods**

##### **ImportImages (Batch Import)**

```go
func (ai *acrImporter) ImportImages(pullResult *images.PullResult, registry string) (*ImportResult, error) {
    startTime := time.Now()

    result := &ImportResult{
        Registry:       registry,
        StartTime:      startTime,
        ImportedImages: []ImportedImage{},
        FailedImports:  []ImportError{},
    }

    // Loop through each image
    for _, pulledImg := range pullResult.PulledImages {
        importedImg, err := ai.ImportSingleImage(pulledImg.ImageRef, registry)
        if err != nil {
            // Record failure but continue with other images
            result.FailedImports = append(result.FailedImports, ImportError{...})
            continue
        }
        // Record success
        result.ImportedImages = append(result.ImportedImages, *importedImg)
    }

    // Calculate final statistics
    endTime := time.Now()
    result.EndTime = endTime
    // ... calculate summary ...

    return result, nil
}
```

- **Receiver**: `(ai *acrImporter)` - method on the struct
- **Error handling**: Continues processing even if individual images fail
- **Pointers**: `*ImportResult` returns a pointer to the struct

##### **ImportSingleImage (Single Import)**

```go
func (ai *acrImporter) ImportSingleImage(img helmimages.ImageReference, registry string) (*ImportedImage, error) {
    // Step 1: Validate input
    if img.IsTemplate {
        return nil, fmt.Errorf("cannot import template image: %s", img.TemplateRef)
    }

    // Step 2: Normalize repository name
    acrRepo := ai.normalizeRepositoryName(img)
    acrTag := img.Tag
    acrRef := fmt.Sprintf("%s.azurecr.io/%s:%s", registry, acrRepo, acrTag)

    // Step 3: Dry run check
    if ai.dryRun {
        return &ImportedImage{ /* simulated result */ }, nil
    }

    // Step 4: Execute Azure CLI command
    cmd := exec.Command(ai.azCLIBinary, "acr", "import",
        "--name", registry,
        "--source", img.FullRef,
        "--image", fmt.Sprintf("%s:%s", acrRepo, acrTag),
        "--force")

    output, err := cmd.CombinedOutput()
    if err != nil {
        return nil, fmt.Errorf("az acr import failed for %s: %s, output: %s",
            img.FullRef, err, string(output))
    }

    return &ImportedImage{
        OriginalRef: img,
        ACRRef:      acrRef,
        ACRRepo:     acrRepo,
        ACRTag:      acrTag,
        ImportTime:  time.Now(),
        Size:        0,
    }, nil
}
```

- **External commands**: Uses `os/exec` to run Azure CLI
- **Error wrapping**: Provides context when commands fail

#### 7. **Helper Methods**

##### **normalizeRepositoryName**

```go
func (ai *acrImporter) normalizeRepositoryName(img helmimages.ImageReference) string {
    repo := img.Repository

    // Remove registry prefixes like "docker.io/"
    if strings.Contains(repo, "/") {
        parts := strings.Split(repo, "/")
        if strings.Contains(parts[0], ".") || parts[0] == "docker" {
            repo = strings.Join(parts[1:], "/")
        }
    }

    // Handle official Docker images
    repo = strings.TrimPrefix(repo, "library/")

    return repo
}
```

- **String manipulation**: Cleans up image names
- **Business logic**: Converts `docker.io/library/redis` → `redis`

#### 8. **Utility Functions**

##### **Package-level Functions**

```go
// ImportBitnamiImages - convenience function
func ImportBitnamiImages(pullResult *images.PullResult, registry string) (*ImportResult, error) {
    importer := NewACRImporter()
    // Filter and import only Bitnami images
    // ...
}

// GetDefaultFitfileRegistry - configuration helper
func GetDefaultFitfileRegistry() string {
    return "fitfileregistry"
}
```

- **Not methods**: No receiver, can be called as [acr.GetDefaultFitfileRegistry()](cci:1://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:374:0-377:1)
- **Convenience functions**: Higher-level operations

### 🔄 How the Algorithm Works (Step by Step)

#### **High-Level Flow**

```sh
Input Images → Validate → Normalize Names → Run az acr import → Return Results
```

#### **Detailed Steps**

1. **Receive Input**: [ImportImages(pullResult, registry)](cci:1://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:14:1-15:84)
   - `pullResult`: Contains list of images to import
   - `registry`: Target ACR name (e.g., "myregistry")

2. **Initialize Tracking**:
   - Create [ImportResult](cci:2://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:31:0-38:1) to track successes/failures
   - Record start time

3. **Process Each Image**:

   ```go
   for each image in pullResult.PulledImages:
       result := ImportSingleImage(image, registry)
       if success: add to ImportedImages
       if failure: add to FailedImports
   ```

4. **Single Image Import**:
   - **Validate**: Skip template images
   - **Normalize**: Convert `docker.io/bitnami/postgresql` → `bitnami/postgresql`
   - **Generate ACR reference**: `myregistry.azurecr.io/bitnami/postgresql:v14`
   - **Execute**: Run `az acr import --name myregistry --source docker.io/bitnami/postgresql:v14 --image bitnami/postgresql:v14 --force`

5. **Track Results**:
   - Success: Create [ImportedImage](cci:2://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:41:0-48:1) with new ACR reference
   - Failure: Create [ImportError](cci:2://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:51:0-55:1) with details

6. **Calculate Summary**:
   - Total images requested
   - Successful imports count
   - Failed imports count
   - Total size transferred
   - Operation duration

### 🎯 Go Concepts Used

#### **Pointers** (`*` And `&`)

```go
func ImportImages(...) (*ImportResult, error)  // Returns pointer to struct
result := &ImportResult{...}                    // Create pointer to new struct
```

#### **Slices** (Dynamic Arrays)

```go
ImportedImages: []ImportedImage{}  // Empty slice
result.ImportedImages = append(result.ImportedImages, *importedImg)  // Add to slice
```

#### **Error Handling**

```go
if err != nil {
    return nil, fmt.Errorf("context: %w", err)  // Wrap errors with context
}
```

#### **Interfaces & Polymorphism**

```go
type ACRImporter interface { ... }  // Contract
func (ai *acrImporter) ImportImages(...)  // Implementation
var importer ACRImporter = NewACRImporter()  // Use interface
```

#### **Struct Embedding**

```go
type ImportResult struct {
    Summary ImportSummary  // Embedded struct
}
```

This code demonstrates real-world Go patterns: interfaces for testability, error handling, external command execution, and clean separation of concerns! 🚀

## Constructor Functions Vs Methods in Go (vs TypeScript)

You're absolutely right to notice the difference! Let me break this down with the specific example you mentioned.

### 🔍 The Key Difference: The Receiver

#### **Constructor Functions** (No Receiver)

```go
// These are just regular functions that happen to create instances
func NewACRImporter() ACRImporter {
    return &acrImporter{
        azCLIBinary: "az",
        dryRun:      false,
    }
}

func NewACRImporterWithConfig(azBinary string, dryRun bool) ACRImporter {
    return &acrImporter{
        azCLIBinary: azBinary,
        dryRun:      dryRun,
    }
}
```

#### **Methods** (Have Receiver)

```go
// This has a RECEIVER: (ai *acrImporter)
func (ai *acrImporter) ImportImages(pullResult *images.PullResult, registry string) (*ImportResult, error) {
    // 'ai' is the instance this method is called on
    startTime := time.Now()

    result := &ImportResult{
        Registry:       registry,
        StartTime:      startTime,
        ImportedImages: []ImportedImage{},
        FailedImports:  []ImportError{},
    }
    // ... rest of method
}
```

### 📋 TypeScript Comparison

| Concept             | TypeScript               | Go                                                                                                                                              |
| ------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Constructor**     | `new MyClass()`          | [NewACRImporter()](cci:1://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:72:0-78:1) (just a function) |
| **Instance Method** | `instance.method()`      | `(instance) method()`                                                                                                                           |
| **Static Method**   | `MyClass.staticMethod()` | `PackageName.Function()`                                                                                                                        |

### 🎯 How to Identify Them

#### **In Go Code:**

- **Constructor**: `func NewSomething() Something`
- **Method**: `func (receiver Type) MethodName()`

#### **When Called:**

```go
// Constructor - called as package function
importer := acr.NewACRImporter()

// Method - called on instance
result, err := importer.ImportImages(pullResult, "myregistry")
```

### 🏗️ Why This Design

**Go doesn't have classes** - it has structs and interfaces. The receiver syntax is Go's way of attaching functions to types:

```go
type acrImporter struct {  // Struct definition
    azCLIBinary string
    dryRun      bool
}

// This function is "attached" to acrImporter via the receiver
func (ai *acrImporter) ImportImages(...) (...) {
    // 'ai' refers to the specific instance
    ai.dryRun  // Access instance fields
}
```

### 💡 TypeScript Equivalent

If this were TypeScript:

```typescript
class ACRImporter {
  private azCLIBinary: string
  private dryRun: boolean

  constructor(azBinary: string = "az", dryRun: boolean = false) {
    this.azCLIBinary = azBinary
    this.dryRun = dryRun
  }

  // Instance method
  importImages(pullResult: PullResult, registry: string): ImportResult {
    // 'this' refers to the instance (like 'ai' in Go)
    this.dryRun // Access instance fields
  }
}

// Usage
const importer = new ACRImporter() // Constructor
const result = importer.importImages(pullResult, "myregistry") // Method
```

### 🔍 Your Specific Example

```go
func (ai *acrImporter) ImportImages(pullResult *images.PullResult, registry string) (*ImportResult, error)
```

**Breaking it down:**

- `func` - Function declaration
- `(ai *acrImporter)` - **Receiver**: This makes it a method on `*acrImporter` type
- `ai` - Variable name for the instance (like `this` in TypeScript)
- `*acrImporter` - Type of the receiver (pointer to acrImporter)
- [ImportImages](cci:1://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:14:1-15:84) - Method name
- `(pullResult *images.PullResult, registry string)` - Parameters
- `(*ImportResult, error)` - Return types

### 📝 Quick Test

You can tell by asking: "Can this be called without an instance?"

- **Constructor**: [acr.NewACRImporter()](cci:1://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:72:0-78:1) ✅ (no instance needed)
- **Method**: [importer.ImportImages(...)](cci:1://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:14:1-15:84) ✅ (needs instance)
- **Method**: [acr.ImportImages(...)](cci:1://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/chart-manager/internal/acr/importer.go:14:1-15:84) ❌ (wouldn't work)

The receiver is what makes it a method! 🚀
