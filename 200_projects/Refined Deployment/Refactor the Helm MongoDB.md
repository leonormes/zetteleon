---
aliases: []
confidence: 
created: 2025-09-06T08:10:47Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [config, database, helm, mongodb, refactoring]
title: Refactor the Helm MongoDB
type:
uid: 
updated: 
version:
---

## **Current MongoDB Configuration Scatter Analysis**

### **Configuration Locations Found:**

**1. Base Chart Definitions (3 layers):**

- [charts/ffnode/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/values.yaml:0:0-0:0) - **30 MongoDB references** (main template)
- [charts/databases/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/databases/values.yaml:0:0-0:0) - **3 MongoDB references** (database-specific)
- [charts/shared-secrets/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/shared-secrets/values.yaml:0:0-0:0) - **2 MongoDB references** (secrets)

**2. Environment-Specific Overrides (18+ locations):**

- `ffnodes/*/values.yaml` - Each deployment has MongoDB config
- `ffnodes/*/values/*/infra-config.yaml` - Infrastructure-specific settings
- `ffnodes/*/values/shared-secrets-values.yaml` - Secret configurations

**3. Application-Specific Configs:**

- `ffnodes/*/values/ffcloud/app-config.yaml` - Connection strings
- `ffnodes/*/values/fitconnect/values.yaml` - Service-specific hosts
- `ffnodes/*/values/frontend/app-config.yaml` - Frontend connections

### **Key Configuration Inconsistencies:**

**Version Management:**

- Some use `targetRevision: "16.5.*"` (production)
- Others have no version specified (development)
- Inconsistent replica counts (1 vs 2)

**Connection Patterns:**

- Multiple connection string formats
- Hardcoded hosts in some locations
- Template-based hosts in others
- Different authentication methods

**Secret Management:**

- Vault secret paths scattered
- Different secret key names
- Inconsistent transformation templates

## **Proposed MongoDB Configuration Refactor Plan**

### **1. Centralized Configuration Structure**

```yaml
# charts/components/mongodb-config/
├── Chart.yaml
├── values.yaml                    # Default MongoDB settings
├── templates/
│   ├── mongodb-secret.yaml       # Unified secret template
│   ├── connection-config.yaml    # Connection string templates
│   └── backup-config.yaml        # Backup configurations
└── environments/
    ├── production.yaml           # Prod-specific overrides
    ├── staging.yaml             # Staging overrides
    └── development.yaml         # Dev overrides
```

### **2. Consolidation Strategy**

**Phase 1: Create MongoDB Component Chart**

- Extract all MongoDB config from [ffnode/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/values.yaml:0:0-0:0)
- Create dedicated `charts/components/mongodb-config/`
- Standardize connection string templates
- Unify secret management patterns

**Phase 2: Environment-Specific Inheritance**

- Create environment-based value files
- Remove MongoDB config duplication from individual ffnodes
- Use Helm chart dependencies for MongoDB component

**Phase 3: Application Integration**

- Update ffcloud, fitconnect, frontend to use centralized config
- Standardize MongoDB host resolution functions
- Consolidate vault secret transformations

### **3. Benefits of Refactor**

**Consistency:**

- Single source of truth for MongoDB versions
- Standardized connection patterns
- Unified secret management

**Maintainability:**

- One place to update MongoDB settings
- Easier version upgrades
- Centralized backup configurations

**Scalability:**

- Environment-specific overrides without duplication
- Easier to add new deployments
- Consistent monitoring and metrics

### **4. Implementation Steps**

1. **Create `charts/components/mongodb-config/` chart**
2. **Extract common MongoDB values from ffnode**
3. **Update ffnode to depend on mongodb-config component**
4. **Migrate environment-specific overrides**
5. **Update application charts to use centralized config**
6. **Test with one environment before rolling out**

Would you like me to start implementing this refactor by creating the centralized MongoDB component chart?

Based on my comprehensive review of all the specified components, here's the complete MongoDB configuration analysis across your deployment codebase:

## **MongoDB Configuration Distribution Analysis**

### **1. charts/databases - Database Infrastructure Layer**

**Purpose**: Core database deployment and management

- **MongoDB Helm Chart Config**: Basic deployment settings (replicaCount: 2, architecture: replicaset)
- **Backup System**: Automated MongoDB backups with CronJob (daily at 9pm, 3-day retention)
- **Web Interface**: Optional MongoDB web client (mongoclient/mongoclient:4.0.1)
- **Monitoring**: ServiceMonitor and metrics configuration
- **Storage**: Persistence and volume management

### **2. charts/ffnode - Application Template Layer**

**Purpose**: Main application orchestration template

- **Dual MongoDB Support**: Both `mongodb` (current) and `mongodbNext` (future) configurations
- **Connection Templates**: Standardized connection string generation
- **Vault Integration**: Secret management with transformation templates
- **Application Integration**: Connection configs for ffcloud, fitconnect, frontend
- **ArgoCD Applications**: MongoDB application deployment definitions

### **3. ffnodes/fitfile/testing - Environment-Specific Layer**

**Purpose**: Testing environment overrides

- **Version Pinning**: `targetRevision: "16.5.*"`
- **Scaling**: `replicaCount: 1` (reduced for testing)
- **Environment-Specific**: OAuth and deployment settings

### **4. Terraform-helm-fitfile-platform - Infrastructure Module**

**Result**: ❌ **No MongoDB configuration found**

- This Terraform module focuses on platform-level Helm deployments
- MongoDB is managed at the application layer, not infrastructure

### **5. Testing-cluster Infrastructure**

**Result**: ❌ **No MongoDB configuration found**

- Terraform infrastructure focuses on AKS cluster provisioning
- Database configurations handled by Helm charts, not infrastructure

## **Configuration Architecture Pattern**

```sh
Infrastructure Layer (Terraform)
├── AKS Cluster Provisioning ❌ No MongoDB
└── Platform Helm Module ❌ No MongoDB

Application Layer (Helm)
├── charts/databases/ ✅ Core MongoDB deployment
├── charts/ffnode/ ✅ Application integration
└── ffnodes/*/values.yaml ✅ Environment overrides
```

## **Key Findings**

### **Separation Of Concerns**

- **✅ Good**: Infrastructure (Terraform) and application (Helm) layers are properly separated
- **✅ Good**: MongoDB is managed entirely within the Helm/Kubernetes layer
- **⚠️ Issue**: Configuration is scattered across multiple Helm chart layers

### **Configuration Complexity**

1. **Base Configuration**: [charts/databases/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/databases/values.yaml:0:0-0:0)
2. **Application Integration**: [charts/ffnode/values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/ffnode/values.yaml:0:0-0:0) (30+ MongoDB references)
3. **Environment Overrides**: Each `ffnodes/*/values.yaml`
4. **Service-Specific**: Individual application value files

### **Refactor Recommendations**

**Consolidation Strategy**:

1. **Keep** infrastructure separation (Terraform vs Helm)
2. **Consolidate** Helm-based MongoDB configurations
3. **Create** `charts/components/mongodb/` for centralized config
4. **Standardize** connection patterns across environments

The MongoDB configuration follows a proper infrastructure/application separation but needs consolidation within the Helm layer to reduce complexity and duplication.

## Prompt

### LLM Prompt for IDE Assistant

**Objective:** Refactor our scattered Helm MongoDB configuration into a centralised component chart.

The primary goal is to improve maintainability and establish a single source of truth for all MongoDB settings. This is a **pure refactoring task**. The final Helm-rendered Kubernetes manifests for any given environment **must remain identical** to what is currently generated. No functional changes should be introduced to our deployed environments.

You will achieve this by creating a new `mongodb-config` component chart and migrating all existing configurations into it, following the phased approach outlined in my analysis.

---

### **Phase 1: Create the Centralised MongoDB Component Chart**

1. **Create the Chart Structure:**
   - Create a new directory: `charts/components/mongodb-config/`.
   - Inside this directory, create the following files and folders:
     - `Chart.yaml`
     - `values.yaml`
     - `templates/`

2. **Define the Chart:**
   - In `charts/components/mongodb-config/Chart.yaml`, define the new component chart:

     ```sh
     apiVersion: v2
     name: mongodb-config
     description: A centralized chart for all MongoDB configurations
     type: application
     version: 0.1.0
     appVersion: "1.0.0"
     ```

3. **Consolidate Default Values:**
   - Go through the following files and identify **every** configuration key related to MongoDB (e.g., hosts, ports, replica counts, versions, secrets, connection strings, backup settings).
     - `charts/ffnode/values.yaml` (contains ~30 references)
     - `charts/databases/values.yaml`
     - `charts/shared-secrets/values.yaml`
   - Copy all these identified configurations into the new `charts/components/mongodb-config/values.yaml`. This file will now be the definitive source for all default MongoDB settings.

---

### **Phase 2: Integrate Component and Update Parent Chart**

1. **Add Chart Dependency:**
   - Modify `charts/ffnode/Chart.yaml` to include the new component as a dependency:

     ```sh
     dependencies:
     - name: mongodb-config
       version: "0.1.0"
       repository: "file://../components/mongodb-config"
     ```

2. **Refactor the Parent `values.yaml`:**
   - **Delete** all the MongoDB configuration keys from `charts/ffnode/values.yaml` that you previously moved.
   - In their place, add a single top-level key to represent the sub-chart. The values from this sub-chart will now be accessible throughout the `ffnode` templates.

     ```sh
     # In charts/ffnode/values.yaml
     mongodb-config: {} # Values will be inherited from the component chart's values.yaml
     ```

3. **Update Template References:**
   - In all templates under `charts/ffnode/templates/`, update any references to MongoDB values. For example, a reference like `{{ .Values.mongodb.host }}` must be changed to `{{ .Values.mongodb-config.host }}`.

---

### **Phase 3: Migrate Environment Overrides and Verify**

1. **Refactor Environment-Specific Values:**
   - For each environment (e.g., `ffnodes/fitfile/testing/values.yaml`), locate the MongoDB overrides.
   - Restructure them to fall under the new top-level key.
   - **Example Transformation:**
     - **Before:**

       ```sh
       # In ffnodes/fitfile/testing/values.yaml
       mongodb:
         replicaCount: 1
         auth:
           rootPasswordSecretName: "some-secret"
       ```

     - **After:**

       ```sh
       # In ffnodes/fitfile/testing/values.yaml
       mongodb-config:
         replicaCount: 1
         auth:
           rootPasswordSecretName: "some-secret"
       ```

   - Apply this change consistently across all environment override files in the `ffnodes/` directory.

2. **Verification (Crucial Step):**
   - The most important step is to confirm that this refactor has not changed the output.
   - **Before committing**, perform a `diff` to ensure zero changes:
     1. Check out the `main` branch (or your current working branch before these changes).
     2. Run helm template for a specific environment and save the output to a file:
        helm template . -f ffnodes/fitfile/testing/values.yaml > before.yaml
     3. Switch back to your refactoring branch.
     4. Run the exact same command:
        helm template . -f ffnodes/fitfile/testing/values.yaml > after.yaml
     5. Compare the files: `diff before.yaml after.yaml`.
   - **The diff must be empty.** If there are any differences, you must correct the refactored configuration until the output is identical. Repeat this verification for a representative set of environments (e.g., development, testing, production).

Start with Phase 1. Once completed, I will provide further instructions.

Excellent work on completing the first two phases. The structure is now in place. 👏

You're ready for the final and most critical phase: migrating the environment overrides and verifying that nothing will change in your deployments.

---

### ✅ **Phase 3: Migrate Environment Overrides and Verify**

Your goal here is to update all environment-specific value files to use the new `mongodb-config` structure.

#### **1. Refactor Environment-Specific `values.yaml` Files**

For each environment (e.g., in `ffnodes/fitfile/testing/values.yaml`, `ffnodes/*/values/*/infra-config.yaml`, etc.), you must find all MongoDB-related configurations and nest them under the `mongodb-config:` key.

**Example Transformation:**

If an override file currently looks like this:

YAML

```sh
# ❌ Before: In ffnodes/fitfile/testing/values.yaml
mongodb:
  replicaCount: 1
  targetRevision: "16.5.*"

mongodbNext:
  replicaCount: 1
```

You must change it to look like this:

YAML

```sh
# ✅ After: In ffnodes/fitfile/testing/values.yaml
mongodb-config:
  mongodb:
    replicaCount: 1
    targetRevision: "16.5.*"
  mongodbNext:
    replicaCount: 1
```

*Notice how the original `mongodb` and `mongodbNext` blocks are now indented under the new `mongodb-config` parent key.*

Apply this change consistently across all of your environment-specific value files.

---

#### **2. Verification: Ensure Identical Helm Output 🔍**

This step is **crucial** to guarantee the refactor is safe. You must confirm that the generated Kubernetes manifests are identical before and after your changes.

1. **Generate `before.yaml`:**
   - Go to your terminal and check out the commit **before you started this refactoring**.
   - Run `helm template` for a specific environment and save the output. For example, for the `testing` environment:

     Bash

     ```sh
     helm template . -f ffnodes/fitfile/testing/values.yaml > before.yaml
     ```

2. **Generate `after.yaml`:**
   - Switch back to your current branch containing all the refactoring work (Phases 1, 2, and 3).
   - Run the **exact same command**:

     Bash

     ```sh
     helm template . -f ffnodes/fitfile/testing/values.yaml > after.yaml
     ```

3. **Compare the Files:**
   - Run a `diff` on the two files:

     Bash

     ```sh
     diff before.yaml after.yaml
     ```

The output of the `diff` command **must be empty**. If there are any differences, you need to adjust your configuration in the component chart or the override files until the output matches perfectly.

Repeat this verification process for a few different environments to ensure all override patterns are handled correctly. Once you've confirmed the output is identical, the refactor is complete and safe to merge.
