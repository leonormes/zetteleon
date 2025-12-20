---
aliases: []
confidence: 
created: 2025-09-02T10:43:01Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:12Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [chart-manager, helm]
title: Helm Chart Management Tool
type:
uid: 
updated: 
version:
---

## Requirements & User Acceptance Criteria: Helm Chart Management Tool

Document Version: 1.0

Date: 2nd September 2025

### 1. Executive Summary

The goal of this project is to create a robust, modular, and automated toolset for managing the lifecycle of third-party Helm charts. This process involves checking for new versions, analysing chart contents, and securely importing both the charts and their associated container images into a private Azure Container Registry (ACR). The final system must be reliable, easy to configure, and simple for DevOps and Platform Engineers to use in both local and CI/CD environments.

### 2. User Personas

- **DevOps Engineer:** Responsible for deploying and maintaining applications. Needs to keep software up-to-date and ensure that deployment artifacts are secure and stored in the company's private registry.
- **Platform Engineer:** Responsible for the underlying infrastructure and tooling. Needs to analyse new charts for compatibility, security, and dependencies before they are approved for use.

### 3. High-Level Requirements (Epics)

The toolset will be built around four core features:

- **Epic 1: Chart Version & Update Management:** Provide a clear view of the version status of all managed Helm charts across different environments.
- **Epic 2: Chart Analysis & Inspection:** Allow deep inspection of a Helm chart to understand its composition and dependencies.
- **Epic 3: Secure Chart & Image Importing:** Automate the process of ingesting charts and images into the secure private registry.
- **Epic 4: Configuration & Usability:** Ensure the tool is easy to configure, self-validating, and provides clear user feedback.

### 4. User Stories & Acceptance Criteria

#### Epic 1: Chart Version & Update Management

> **As a DevOps Engineer, I want to check for version updates for our managed Helm charts, so that I can maintain security and access new features.**

| Story ID   | User Story                                            | Acceptance Criteria                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **UC-1.1** | **Check for updates against a central configuration** | 1. The tool **MUST** read a list of charts to manage from a central `helm_chart_list.yaml` file.<br>2. For each chart, it **MUST** identify the latest available version in the public upstream repository.<br>3. It **MUST** identify the latest version currently stored in our private ACR.<br>4. It **MUST** identify the versions currently deployed to our `production`, `staging`, and `testing` environments by querying the Terraform Cloud (TFC) API. |
| **UC-1.2** | **View update status in multiple formats**            | 1. The tool **MUST** be able to output its findings in a human-readable text format for interactive use.<br>2. The tool **MUST** also be able to output the results in structured `JSON` and `CSV` formats for use in automation pipelines.<br>3. The text output **MUST** clearly indicate with a "⚠️" or similar emoji if an update is available for ACR or any TFC environment.                                                                              |
| **UC-1.3** | **Filter results to show only actionable updates**    | 1. The tool **MUST** provide a command-line flag (`--only-updates`) that filters the output to show only those charts where an update is needed in either ACR or a TFC-managed environment.                                                                                                                                                                                                                                                                     |

#### Epic 2: Chart Analysis & Inspection

> **As a Platform Engineer, I want to analyse a Helm chart before use, so that I can understand its dependencies and security implications.**

| Story ID   | User Story                                        | Acceptance Criteria                                                                                                                                                                                                                                                                                              |
| ---------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **UC-2.1** | **Analyse a chart to discover its contents**      | 1. The tool **MUST** be able to analyse a chart specified by repository URL and name.<br>2. The analysis **MUST** list all chart dependencies declared in `Chart.yaml`.<br>3. The analysis **MUST** discover and list every container image reference found within the chart's `values.yaml` and its sub-charts. |
| **UC-2.2** | **Support different analysis sources and depths** | 1. The tool **MUST** be able to analyse a chart that has already been downloaded to a local directory.<br>2. It **MUST** provide an option (`--include-subcharts`) to perform the analysis recursively on all sub-charts.                                                                                        |
| **UC-2.3** | **View analysis in multiple formats**             | 1. The analysis output **MUST** be available in human-readable text, `JSON`, and `YAML` formats.                                                                                                                                                                                                                 |

#### Epic 3: Secure Chart & Image Importing

> **As a DevOps Engineer, I want to automate the import of a Helm chart and its images into our secure ACR, so that we have a trusted, scanned, and internally-hosted artifact.**

| Story ID   | User Story                                       | Acceptance Criteria                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **UC-3.1** | **Import chart and images into ACR**             | 1. Given a chart name and version, the tool **MUST** download it from its public repository.<br>2. It **MUST** discover all container images within the chart.<br>3. It **MUST** import each discovered image into the specified private ACR, preserving its name and tag.<br>4. The tool **MUST** rewrite the chart's `values.yaml` file to replace all public image references with their new ACR path.<br>5. The tool **MUST** package the modified chart and push it to the specified private ACR. |
| **UC-3.2** | **Perform security scanning on imported images** | 1. After an image is imported to ACR, the tool **MUST** immediately trigger a vulnerability scan using Trivy.<br>2. *(Optional)* If vulnerabilities are found and the `copa` tool is available, the tool **SHOULD** attempt to patch the image and push a new `-patched` tag to ACR. The `values.yaml` file should be updated to use this patched version.                                                                                                                                             |
| **UC-3.3** | **Provide control over the import process**      | 1. The tool **MUST** include a `--dry-run` flag that simulates the entire process and prints the actions it would take, without making any actual changes.<br>2. The tool **MUST** allow specific container images to be excluded from the import and rewrite process via an `--exclude` flag.                                                                                                                                                                                                         |
| **UC-3.4** | **Generate or execute import commands**          | 1. The tool **MUST** be able to generate the list of `import_chart_to_acr.sh` commands needed to bring all outdated charts up-to-date.<br>2. The tool **MUST** provide a flag (`--execute`) to run these import commands automatically instead of just printing them.                                                                                                                                                                                                                                  |

#### Epic 4: Configuration & Usability

> **As an administrator, I want to easily configure and run the toolset, with clear feedback on requirements and errors.**

| Story ID   | User Story                                    | Acceptance Criteria                                                                                                                                                                                                                                                                                                     |
| ---------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **UC-4.1** | **Validate prerequisites before execution**   | 1. Before running any logic, the tool **MUST** check that all required CLI dependencies (`helm`, `az`, `yq`, `jq`, `trivy`, `docker`) are installed and available in the `PATH`.<br>2. If a dependency is missing, the tool **MUST** exit with a clear error message listing the missing tools.                         |
| **UC-4.2** | **Handle authentication gracefully**          | 1. The tool **MUST** check for an active Azure CLI session. If the user is not logged in, it **MUST** inform them and exit gracefully.<br>2. The tool **MUST** use a `TF_TOKEN` environment variable for authenticating with the Terraform Cloud API. If the variable is not set, it **MUST** inform the user and exit. |
| **UC-4.3** | **Provide clear help and usage instructions** | 1. All scripts **MUST** provide a `--help` flag that prints a detailed usage message, including all available options and examples.                                                                                                                                                                                     |

---

### 5. Proposed Code Structure & Modularisation

To meet these requirements and move away from the current monolithic scripts, the code should be reorganised into a modular structure with a clear separation of concerns.

```sh
helm-chart-manager/
├── bin/
│   └── chart-manager          # Main entry point script. Parses subcommands (check, analyze, import).
│
├── lib/
│   ├── azure.sh               # Functions for Azure: check_login, get_acr_version, import_image_to_acr
│   ├── chart_parser.sh        # Functions for chart analysis: discover_images, get_dependencies
│   ├── config.sh              # Functions for loading and validating helm_chart_list.yaml
│   ├── helm.sh                # Functions for Helm commands: repo_update, search_repo, pull_chart
│   ├── output.sh              # Functions for formatting output: print_json, print_csv, print_text
│   ├── security.sh            # Functions for scanning/patching: scan_image, patch_image
│   └── tfc.sh                 # Functions for TFC API: get_workspace_outputs
│
├── config/
│   └── helm_chart_list.yaml   # Example configuration file.
│
└── README.md                  # Updated documentation for the new structure.
```

#### Rationale for Modularisation

1. **Single Entry Point (`bin/chart-manager`):** Instead of multiple scripts (`helm_chart_updater.sh`, `helm_chart_version_checker.sh`), a single script that accepts subcommands (`check`, `import`, etc.) provides a more professional and git-like user experience. This script will be a lightweight orchestrator.
2. **Shared Libraries (`lib/`):** All core logic is extracted into function libraries.
   - This **eliminates code duplication**. For example, `azure.sh` and `helm.sh` will contain functions used by the `check`, `analyze`, and `import` commands.
   - It **improves maintainability**. If the logic for getting a version from ACR changes, you only need to update the `get_acr_version` function in `azure.sh`.
   - It **simplifies testing**. Each library can be sourced and its functions tested independently.

3. **Separation of Concerns:** Each file in `lib/` has a single responsibility (e.g., `tfc.sh` only deals with Terraform Cloud; `security.sh` only deals with scanning). This makes the codebase much easier to understand and extend.
