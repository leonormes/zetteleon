---
aliases: []
confidence: 
created: 2025-03-07T08:45:14Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:44Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [sonarqube]
title: Integrating SonarQube with GitLab CICD for Nodejs and TypeScript Monorepos
type: 
uid: 
updated: 
version: 
---

## Integrating SonarQube with GitLab CI/CD for Node.js and TypeScript Monorepos

Maintaining code quality and security in a rapidly growing monorepo can be challenging. With multiple teams working on interconnected projects, ensuring consistency and catching potential issues early becomes crucial. This is where SonarQube comes in. By integrating SonarQube with your GitLab CI/CD pipeline, you can automate code analysis, identify bugs and vulnerabilities, and enforce quality standards across your Node.js and TypeScript projects. This article provides a comprehensive guide to setting up this integration, tailored to your specific environment with Yarn 3 workspaces and a self-hosted SonarQube server running on an Azure VM.

### Understanding the Core Components

Before we delve into the integration process, let's briefly discuss the key elements involved:

- **Monorepo:** A monorepo is a single repository that houses multiple distinct projects, often sharing dependencies and tooling. This approach promotes code sharing, reduces duplication, and enforces consistency across projects. However, it requires careful management of dependencies and build processes1.
- **Yarn 3 Workspaces:** Yarn 3 workspaces simplify managing dependencies and building projects within a monorepo. Each workspace has its own `package.json` file, allowing for independent dependency management while still benefiting from a single `yarn.lock` file for the entire repository.
- **GitLab CI/CD:** GitLab's built-in continuous integration and continuous delivery platform automates the building, testing, and deployment of your applications. It uses a `.gitlab-ci.yml` file to define your pipeline stages, jobs, and scripts.
- **SonarQube:** An open-source platform for continuous inspection of code quality, SonarQube performs static code analysis to identify bugs, vulnerabilities, and code smells. It provides valuable feedback for improving your codebase and helps prevent technical debt from accumulating.
- **Azure VM:** A virtual machine running on Microsoft Azure's cloud platform provides the infrastructure for hosting your self-hosted SonarQube server.

Using SonarQube for monorepo analysis offers specific benefits, such as identifying cross-project code duplications and inconsistencies, which can be easily missed in traditional, per-project analysis1. Additionally, SonarQube plays a crucial role in security scanning by detecting vulnerabilities early in the development process, preventing them from reaching production and potentially compromising your applications2.

### Setting up SonarQube Integration

To integrate SonarQube with your GitLab CI/CD pipeline, follow these steps:

#### 1. Configure SonarQube for GitLab Integration

Ensure you are using GitLab version 15.6 or higher for optimal integration3. Then, follow these steps:

- **Access SonarQube:** Log in to your SonarQube server's web interface.
- **Enable GitLab Authentication:** Navigate to **Administration > Configuration > General Settings > DevOps Platform Integrations**. Select the **GitLab** tab.
    - **Configuration Name:** Provide a descriptive name for your GitLab configuration (e.g., "My GitLab Integration").
    - **GitLab URL:** Enter the URL of your GitLab instance's API (e.g., `https://gitlab.com/api/v4`).
    - **Personal Access Token:** Generate a personal access token in GitLab with `api` scope for a dedicated GitLab user with at least *Reporter* permissions on your project. This token will be used to decorate merge requests and report the quality gate status.

#### 2. Import Your GitLab Project into SonarQube

- **Add Project:** On the SonarQube **Projects** homepage, click **Add project** and select **GitLab**.
- **Authenticate:** You'll be prompted to provide another personal access token with `read_api` scope to allow SonarQube to access and list your GitLab projects.
- **Select Project:** Choose your monorepo project from the list.
- **Enable Monorepo Support:** In your SonarQube project settings, navigate to **General Settings > DevOps Platform Integration** and set **Enable mono repository support** to `true`.

#### 3. Configure Analysis Parameters for Each Workspace

Since you have a monorepo with multiple workspaces, you need to configure analysis parameters for each workspace individually.

- **Create SonarQube Projects:** For each workspace in your monorepo, create a corresponding project in SonarQube.
- **Define Inclusion/Exclusion Patterns:** In each project's settings, go to **Analysis Scope** and define **Source File Inclusion** patterns to ensure that SonarQube analyzes only the files belonging to that specific workspace. This prevents code from other workspaces from being included in the analysis.
- **Configure Language-Specific Settings:** Adjust language-specific settings (e.g., for TypeScript or JavaScript) as needed for each workspace.
- **Configure SonarScanner using `sonar-project.properties`:** Create a `sonar-project.properties` file in the root directory of each workspace. This file allows you to specify analysis parameters for the SonarScanner4. Here's an example:

Properties

```sh
sonar.projectKey=my-workspace-a  # Replace with your workspace name
sonar.projectName=My Workspace A
sonar.sources=src  # Adjust the path if your source files are in a different directory
sonar.language=ts  # Set the language to TypeScript (or js for JavaScript)
# Add other language-specific properties as needed
```

#### 4. Set Up GitLab CI/CD Variables

In your GitLab project's settings, navigate to **CI/CD > Variables** and define the following:

- **`SONAR_HOST_URL`:** Set this variable to the URL of your SonarQube server.
- **`SONAR_TOKEN_<workspace_name>`:** For each workspace, create a separate variable with the corresponding SonarQube token. Replace `<workspace_name>` with the actual name of the workspace. You can generate these tokens in SonarQube by going to **Security** under your user profile or the project settings.

#### 5. Set Up a GitLab Runner

To execute your CI/CD pipeline, you need a GitLab runner5. Here's a brief overview of the setup process:

- **Installation:** Install a GitLab runner on a machine that has access to your code repository. You can find detailed installation instructions in the GitLab documentation.
- **Choose an Executor:** Select an executor for your runner. The Docker executor is a popular choice as it provides a clean and isolated environment for your jobs.
- **Registration:** Register the runner with your GitLab project. You'll need your project's URL and a registration token, which you can find in your project's **Settings > CI/CD > Runners** section.

#### 6. Create Your `.gitlab-ci.yml` File

Define your GitLab CI/CD pipeline in your `.gitlab-ci.yml` file. Here's an example with explanations:

YAML

```yaml
stages:
  - build
  - test
  - analyze

variables:
  GIT_DEPTH: "0"  # Fetch all branches for accurate analysis

build:
  stage: build
  script:
    - yarn install  # Install dependencies for all workspaces
  artifacts:
    paths:
      - node_modules/  # Cache dependencies [4]

test:
  stage: test
  script:
    - yarn workspaces foreach run test  # Run tests in each workspace

analyze:
  stage: analyze
  needs:  # Ensure build and test stages complete successfully
  parallel:
    matrix:
      - workspace: workspace-a  # Replace with your workspace names
      - workspace: workspace-b
      - workspace: workspace-c
  script:
    - cd packages/$workspace # Navigate to the workspace directory
    - sonar-scanner \
        -Dsonar.qualitygate.wait=true  # Wait for quality gate results
  allow_failure: false  # Fail the pipeline if SonarQube analysis fails
```

**Explanation:**

- **Stages:** Defines the stages of your pipeline: `build`, `test`, and `analyze`.
- **Variables:** Sets the `GIT_DEPTH` to `0` to disable shallow cloning, ensuring SonarQube has access to the full commit history.
- **Build Stage:** Installs dependencies for all workspaces and caches them for subsequent jobs. Caching dependencies can significantly speed up your pipeline execution4.
- **Test Stage:** Runs tests in each workspace using `yarn workspaces foreach run test`.
- **Analyze Stage:**
    - `needs`: Specifies that the `analyze` stage depends on the successful completion of the `build` and `test` stages.
    - `parallel`: Enables parallel execution of the analysis for each workspace. This is crucial for monorepos to reduce the overall analysis time6.
    - `matrix`: Defines a list of workspaces to analyze.
    - `script`: Executes the `sonar-scanner` command for each workspace. Since we've already defined the project key, project name, and other parameters in the `sonar-project.properties` file, we don't need to pass them as arguments here. We only need to specify `-Dsonar.qualitygate.wait=true` to wait for the quality gate results.
    - `allow_failure`: Set to `false` to fail the pipeline if the SonarQube analysis or quality gate fails.

#### 7. Configure Quality Gate in SonarQube

- **Define Quality Gate:** In SonarQube, navigate to **Quality Gates** and define the conditions that must be met for a project to pass the quality gate. You can set thresholds for various metrics, such as code coverage, code smells, security vulnerabilities, and code duplication.
- **Associate Quality Gate:** Associate the defined quality gate with your SonarQube projects.

Quality gates are essential for enforcing code quality standards and preventing the accumulation of technical debt. They act as a safety net, ensuring that code that doesn't meet predefined criteria is not merged into the main branch7.

#### 8. Block Merge Requests on Quality Gate Failure

- **Enable Merge Checks:** In your GitLab project settings, go to **General > Merge checks** and ensure that **Pipelines must succeed** is enabled. This will prevent merging if the pipeline fails, including SonarQube analysis failures.

### Setting up Azure Infrastructure with Terraform

To host your SonarQube server on an Azure VM, you can use Terraform to define and manage your infrastructure as code2. Here's a basic outline of the process:

- **Create a Resource Group:** Define a resource group to organize all the resources related to your SonarQube deployment.
- **Set up a Virtual Network and Subnet:** Create a virtual network and subnet to provide network connectivity for your VM.
- **Configure a Network Security Group:** Define a network security group with inbound rules to allow traffic on the necessary ports for SonarQube (e.g., SSH for administration, HTTP/HTTPS for web access, and the default SonarQube port 9000).
- **Provision an Azure VM:** Create an Azure VM with appropriate specifications (e.g., operating system, size, storage) to host your SonarQube server.

When defining your Azure infrastructure with Terraform, follow these best practices: 8

- **Use Modules:** Break down your infrastructure into reusable modules for common components like networking, VMs, and security groups. This promotes code reuse, improves maintainability, and simplifies complex deployments.
- **Consistent Naming:** Adopt a consistent naming convention for resources and variables to enhance readability and organization.
- **Manage State Files:** Store your Terraform state files securely, preferably in a remote location like Azure Storage, to enable collaboration and prevent accidental modifications.

### Troubleshooting and Best Practices

- **Certificate Issues:** A common issue when integrating SonarQube with GitLab is encountering certificate problems, especially if your SonarQube server uses a self-signed certificate. To resolve this, you may need to add your Azure VM's self-signed certificate to the Java truststore used by SonarQube9.
- **Debugging:** If you encounter any issues, enable the `DEBUG` logging level in SonarQube (**Administration > System > Log Level**) to get more detailed information for troubleshooting9.
- **Optimize Analysis Scope:** Carefully define inclusion and exclusion patterns in your SonarQube project settings to ensure that only relevant code is analyzed. This improves analysis speed and accuracy.
- **Use a Dedicated User:** Create a dedicated GitLab user with appropriate permissions for SonarQube integration. This improves security and auditability.
- **Regularly Update SonarQube:** Keep your SonarQube server and scanner updated to the latest versions to benefit from new features, bug fixes, and security improvements.

#### Alternative Integration Methods

While this article focuses on direct integration with GitLab CI/CD, there are alternative approaches you can consider:

- **SonarQube Plugin for Jenkins:** If you're using Jenkins for your CI/CD pipelines, you can use the SonarQube plugin to integrate code analysis into your Jenkins jobs7.
- **SonarScanner CLI:** You can also directly invoke the SonarScanner CLI from your CI/CD scripts. This provides more flexibility but requires manual configuration of analysis parameters10.

### Conclusion

Integrating SonarQube with your GitLab CI/CD pipeline provides continuous code quality and security analysis for your Node.js and TypeScript monorepo. By following the steps outlined in this article, you can automate code inspection, identify potential issues early in the development process, and enforce quality gates to maintain a high standard of code. This not only helps improve the overall quality and security of your codebase but also fosters a culture of code excellence within your development team. Remember to tailor the configuration to your specific needs and leverage SonarQube's features to continuously improve your codebase.
