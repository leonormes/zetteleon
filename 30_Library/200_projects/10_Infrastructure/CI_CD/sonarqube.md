---
aliases: []
confidence: 
created: 2024-12-05T13:13:22Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:50Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [SDLC, security]
title: sonarqube
type: 
uid: 
updated: 
version: 
---

## SonarQube

### SonarQube Quality Gate Failure in InsightFILE

#### Error Classification

- Primary Category: Configuration Error
- Subcategory: Quality Gate Failure
- Severity Level: High
- Impact Scope: Project-wide

#### Description

The SonarQube analysis for the InsightFILE project failed to pass the defined Quality Gate. This indicates that the codebase does not meet the predefined quality standards set for the project. This failure prevents the code from being merged or deployed, ensuring that quality standards are maintained.

#### Technical Details

- Error Message: `ERROR QUALITY GATE STATUS: FAILED - View details on https://sonarqube.fitfile.net/dashboard?id=fitfile_InsightFILE_51a7ae01-cee9-4f5e-866a-7dd5909103df`
- Environment Information: GitLab CI pipeline using sonarsource/sonar-scanner-cli:11 Docker image.
- Affected Components: InsightFILE project.

#### Root Cause

The specific reasons for the Quality Gate failure can be found by reviewing the SonarQube dashboard at the provided link. Common causes include:

- New code violations: New bugs, vulnerabilities, or code smells exceeding the defined thresholds.
- Decreased code coverage: Insufficient test coverage for new or modified code.
- Maintainability issues: High code complexity or code duplication exceeding the allowed limits.
- Reliability concerns: Potential performance bottlenecks or security risks identified in the code.

#### Resolution

1. Review the SonarQube dashboard: Analyze the detailed report on the SonarQube server to identify the specific issues causing the Quality Gate failure.
2. Address the identified issues: Fix bugs, vulnerabilities, and code smells. Improve test coverage and refactor code to enhance maintainability.
3. Re-run the SonarQube analysis: After addressing the issues, trigger a new pipeline run to re-analyze the codebase.
4. Monitor Quality Gate: Regularly monitor the SonarQube dashboard to track code quality and address any new issues proactively.

#### Related Information

- SonarQube Dashboard:
- SonarQube Documentation:
- Project Quality Standards:

#### Validation Checklist

### SonarQube Analysis Breakdown for Monorepo

#### Timeline of Events

1. Project Setup: The SonarScanner CLI is initiated within the GitLab CI pipeline using the `sonarsource/sonar-scanner-cli:11` Docker image.
2. Configuration Loading:

    - The scanner loads its own configuration from `/opt/sonar-scanner/conf/sonar-scanner.properties`.
    - It then locates and loads the project-specific configuration from `sonar-project.properties` in the root of the InsightFILE repository.
3. Environment Initialization:

    - The scanner logs version information for itself, Java, and the operating system.
    - It establishes a local cache directory within the project: `/builds/fitfile/InsightFILE/.sonar/cache`.
4. SonarQube Connection:

    - The scanner connects to the SonarQube server at `https://sonarqube.fitfile.net`.
    - It identifies the server with ID `92D88F0A-AZJ2H0niYQzkvmQMvAnV`.
5. Plugin Management:

    - The scanner loads the necessary plugins for the analysis. This includes downloading any missing plugins.
6. Project Identification:

    - The scanner identifies the project as `fitfile_InsightFILE_51a7ae01-cee9-4f5e-866a-7dd5909103df`.
    - It sets the base directory for analysis to `/builds/fitfile/InsightFILE` and the working directory to `/builds/fitfile/InsightFILE/.scannerwork`.
7. Project Settings and Quality Profiles:

    - The scanner retrieves project-specific settings from the SonarQube server.
    - It loads the appropriate Quality Profiles for different languages detected in the project (CSS, Docker, JavaScript, JSON, Python, TypeScript, Web, YAML).
8. Language Detection and Plugin Loading:

    - The scanner analyzes the project and detects eight different programming languages across 2157 files.
    - It loads the required plugins for each detected language.
9. Code Analysis (per language):

    - Python:
        - The Python Sensor analyzes 111 source files.
        - It executes rules to identify code quality issues.
        - Cobertura Sensor and PythonXUnitSensor gather code coverage data.
    - JavaScript/TypeScript:
        - This sensor analyzes 1685 source files, processing them in groups based on `tsconfig.json` files.
        - It performs type checking and linting to identify code issues.
    - Other Languages:
        - Sensors for HTML, web, IaC (Docker, Kubernetes, AzureResourceManager, Cloudformation), and text files are executed, analyzing the corresponding files for quality issues.
10. Global Analysis:

    - Zero Coverage Sensor: Identifies files with no test coverage.
    - CPD (Code Duplication): Detects duplicated code blocks across the project.
11. Report Generation and Upload:

    - The scanner generates a comprehensive analysis report.
    - This report is compressed and uploaded to the SonarQube server.
12. Quality Gate Evaluation:

    - The SonarQube server processes the report and evaluates it against the defined Quality Gate conditions.
    - In this case, the Quality Gate status is FAILED.

#### Monorepo Considerations

The analysis, as currently configured, treats the entire monorepo as a single project. This approach has drawbacks:

- Inefficient Analysis: Changes in one service trigger analysis of the entire codebase, wasting time and resources.
- Inaccurate Quality Gate: The Quality Gate result reflects the overall health of the monorepo, not the individual service with changes, potentially masking issues.
- Increased Noise: Issues unrelated to the modified service clutter the analysis report, making it harder to focus on relevant problems.

Recommended Solution:

Configure SonarQube to analyze each service within the monorepo as a separate project. This allows for targeted analysis, accurate Quality Gate evaluation, and reduced noise in reports. This typically involves adjusting the `sonar-project.properties` file to define project boundaries and potentially using build tools to trigger analysis only for modified services.
