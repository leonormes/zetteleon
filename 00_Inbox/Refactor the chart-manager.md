---
aliases: []
tags: []
title: "Refactoring Plan: Deduplication and Consolidation"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-26T20:10:11+00:00
modified: 2025-12-28T09:48:35+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# Refactoring Plan: Deduplication and Consolidation

## Goal Description

Refactor the `chart-manager` codebase to reduce complexity, eliminate redundant code, and consolidate overlapping packages. The current architecture suffers from fragmentation, particularly in chart pulling, image extraction, and container image operations.

## User Review Required

> [!IMPORTANT]
> This refactoring forces the use of the Helm Go SDK for extraction (`internal/helmextractor`) over Regex/Text-based parsing (`internal/helmimages`). This is a more robust approach but might require verification that all edge cases (like complex template logic) are handled.

## Proposed Changes

### 1. Consolidate Chart Pulling Logic

Currently split across `internal/helm`, `internal/chartpull`, and `internal/chartimport`.

- **Target Package**: `internal/helm`
- **Actions**:
    - Enhance `internal/helm/chart_puller.go` to include the robust validation logic from `chartpull` and `chartimport`.
    - Ensure `ChartInfo` (in `helm`) supercedes `PullResult` (in `chartpull`) and `ChartPullResult` (in `chartimport`).
    - **DELETE**: `internal/chartpull`
    - **DELETE**: `internal/chartimport` (move any high-level orchestration logic to `internal/appservice` or `internal/processor` if needed, but low-level pulling goes to `helm`).

### 2. Unify Image Extraction Strategy

Currently split between `internal/helmextractor` (SDK-based, accurate) and `internal/helmimages` (Regex-based, brittle).

- **Target Package**: `internal/chart/analysis` (New Package)
- **Actions**:
    - Move `internal/helmextractor/extractor.go` to `internal/chart/analysis/extractor.go`.
    - Port valuable "heuristics" from `internal/helmimages/extract_images.go` (like explicit Bitnami value keys) into the new extractor as a fallback mechanism.
    - **DELETE**: `internal/helmextractor`
    - **DELETE**: `internal/helmimages`

### 3. Consolidate Container Operations

Currently split across `internal/imageops`, `internal/imageproc`, `internal/images`, `internal/acr`, `internal/docker`.

- **Target Package**: `internal/containers` (New Package)
- **Actions**:
    - Create `internal/containers` package.
    - Move `internal/imageops/azure.go` -> `internal/containers/acr.go`.
    - Move `internal/imageops/docker.go` -> `internal/containers/docker.go`.
    - Move `internal/images/scanner.go` -> `internal/containers/scanner.go`.
    - **DELETE**: `internal/imageops`, `internal/imageproc`, `internal/images`, `internal/acr`, `internal/docker`.

### 4. Group Chart Modification

Currently in `internal/chartmod` and `internal/helmimages` (yaml updating).

- **Target Package**: `internal/chart/modifier`
- **Actions**:
    - Move `internal/chartmod/*` to `internal/chart/modifier/`.
    - Move `internal/helmimages/yaml_updater.go` to `internal/chart/modifier/values_updater.go`.
    - **DELETE**: `internal/chartmod`.

## Verification Plan

### Automated Tests

- Run existing tests for the moved packages to ensure no regressions.
- `go test./internal/helm/...`
- `go test./internal/chart/...`
- `go test./internal/containers/...`

### Manual Verification

- Run the `analyze` command (which triggers extraction) to verify it still detects images correctly.
- Run the `import` command to verify chart pulling works with the merged logic.
