---
aliases: []
confidence: 
created: 2025-10-13T14:48:12Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Refactoring Plan AWS Private Infrastructure Module
type:
uid: 
updated: 
version:
---

The primary objective is to deconstruct the single-purpose `hie-sde-v2` Terraform deployment into a generic, reusable `terraform-aws-private-infrastructure` module. This will enable consistent, version-controlled deployments of secure AWS environments for any workload.

## **Key Principles & Best Practices**

This refactoring will adhere to the following Terraform best practices:

- **Configuration over Code**: The module will be driven by input variables, not hardcoded logic. Consumers should be able to define their entire architecture through variables without modifying the module's source code.
- **Modularity & Composability**: The root module will orchestrate calls to smaller, single-purpose child modules (VPC, EKS, etc.), promoting separation of concerns.
- **Feature Toggling**: Optional components like the Jumpbox, Network Firewall, and Relay Service will be controlled by boolean feature flags, allowing the module to be tailored for different use cases.
- **Immutability**: The recommended migration path will be a blue-green deployment, creating new infrastructure from the module rather than attempting risky in-place state modification.
- **Clear Abstractions**: Complex logic, such as subnet CIDR calculations and resource naming, will be handled internally by the module, presenting a simplified interface to the user.

---

## **Phase 1: Establish the Module Structure**

This phase lays the foundation for the new module, ensuring a logical separation of concerns.

1. **Create the Module Directory**:
   - A new repository or directory will be created at the specified location: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-aws-private-infrastructure/`.

2. **Implement the Standard Module Layout**:
   - The directory structure from your plan is excellent and should be implemented exactly. Breaking resources into files like `networking.tf`, `compute.tf`, and `gateway.tf` directly maps to the components identified in your infrastructure analysis and improves maintainability.

   ```sh
   terraform-aws-private-infrastructure/
   ├── README.md
   ├── main.tf
   ├── variables.tf
   ├── outputs.tf
   ├── locals.tf
   ├── versions.tf
   ├── networking.tf    # VPC, Subnets, Endpoints
   ├── compute.tf       # EKS Cluster, Node Groups
   ├── gateway.tf       # NAT, Network Firewall
   ├── jumpbox.tf       # Conditional Jumpbox resources
   ├── relay.tf         # Conditional Relay Service resources
   └── modules/         # Existing child modules
       ├── vpc/
       ├── eks/
       └── ... (all others)
   ```

3. **Migrate Child Modules**:
   - Copy all existing child modules (vpc, eks, gateway, etc.) from `hie-sde-v2/modules/` into the new `modules/` subdirectory. As your analysis notes, these are already well-structured and require no immediate changes.

---

## **Phase 2: Standardise Naming Conventions**

Consistent naming is crucial for managing resources across multiple environments. The proposed naming convention will be implemented to ensure predictability and prevent clashes.

1. **Define Core Naming Variables**:
   - The `variables.tf` file will include the standardised variables for naming: `workload`, `environment`, `aws_region`, and the optional `region_code`. This pattern is a proven method for creating unique and descriptive resource names.

2. **Implement Naming Logic**:
   - The `locals.tf` file will contain the logic to generate a `base_name` from these variables (`${var.workload}-${local.region_code}-${var.environment}`).
   - It will also define resource-specific names (e.g., `vpc_name`, `eks_cluster_name`) using the `coalesce` function. This provides a sensible default while allowing consumers of the module to override names if necessary.

3. **Implement Standardised Tagging**:
   - A `common_tags` local variable will be created to merge default module tags with any custom tags provided by the user. This ensures all resources are tagged consistently for cost allocation and governance.

---

## **Phase 3: Abstract All Configuration into Variables**

This is the most critical phase for achieving reusability. All hardcoded values and complex structures from the original deployment's `config.tf` will be converted into flexible input variables.

1. **Network Topology Abstraction**:
   - Instead of defining static subnets, create the `subnet_configuration` map variable as planned. This powerful pattern allows the user to define any number of subnets with different sizes, types, and purposes.
   - The `locals.tf` will contain the logic to dynamically calculate the CIDR blocks and construct the list of subnets to pass to the `vpc` child module, as detailed in your plan. The default value for this variable will be the existing subnet layout from your infrastructure analysis to ensure backward compatibility.

2. **EKS Cluster Abstraction**:
   - The monolithic EKS configuration will be broken down into granular variables:
     - `eks_kubernetes_version`: With logic to pull from TFC remote state as a default.
     - `eks_node_groups`: A map of objects to allow defining multiple, differently configured node groups (`System` and `Workflows` from your analysis become the default). This is a key flexibility improvement.
     - `eks_cluster_admin_users`: A list of objects to manage user access cleanly.

3. **Implement Feature Flags**:
   - Create a boolean variable for each optional component identified in the resource inventory (e.g., `enable_jumpbox`, `enable_network_firewall`, `enable_relay_service`). This allows consumers to provision anything from a minimal VPC/EKS stack to the full, security-hardened environment.

4. **Endpoint and Service Configuration**:
   - Abstract the VPC endpoints into the `vpc_endpoints_gateway` and `vpc_endpoints_interface` variables. This makes it trivial to add or remove service endpoints in the future.
   - Group all variables for the optional relay service under a clear set of `relay_*` prefixed variables.

---

## **Phase 4: Implement Module Logic**

With the structure and variables defined, this phase involves writing the HCL code that connects them.

1. **Orchestrate Module Calls**:
   - The top-level `.tf` files (`networking.tf`, `compute.tf`, etc.) will contain the `module` blocks that call the child modules.

2. **Manage Dependencies Explicitly**:
   - Use `depends_on` to enforce the creation order identified in your resource linkage analysis. For example, the EKS module call in `compute.tf` must have `depends_on = [module.vpc, module.gateway]` because it requires network resources to exist first.

3. **Implement Conditional Logic**:
   - Use the `count` meta-argument on modules and resources to enable/disable them based on the feature flags defined in Phase 3.
   - Example from your `jumpbox.tf` plan: `count = var.enable_jumpbox ? 1 : 0`.

4. **Wire Variables and Outputs**:
   - Pass the abstracted variables from the root module down to the child modules.
   - Reference outputs from one module as inputs to another (e.g., `vpc_id = module.vpc.vpc_id`). This creates the dependency graph. The resource linkage document is the definitive guide for this mapping.

5. **Define Clear Outputs**:
   - The `outputs.tf` file should expose key information from the created resources, such as `vpc_id`, `eks_cluster_name`, `jumpbox_private_ip`, and the EKS cluster endpoint. Mark sensitive outputs appropriately.

---

## **Phase 5: Develop a Testing and Validation Strategy**

Before the module can be used, it must be thoroughly tested.

1. **Create a Test Deployment**:
   - Set up a dedicated test workspace in Terraform Cloud (`hie-sde-v2-module-test`).
   - Create a test configuration file (as outlined in your plan) that calls the new module and attempts to replicate the original `codisc` environment. This will serve as the primary validation harness.

2. **Execute Validation Steps**:
   - **Lint & Validate**: Run `terraform init` and `terraform validate` to catch syntax errors.
   - **Plan Comparison**: Run `terraform plan` and carefully compare the output against a plan from the *original* monolithic deployment. The goal is to ensure resource parity and identify any unintended changes.
   - **Apply and Verify**: Apply the plan in the test environment. Once deployed, perform functional checks:
     - Can you access the EKS cluster via the jumpbox?
     - Does the relay service route traffic correctly from the allowed IPs?
     - Are all VPC endpoints functioning?
   - **State Verification**: Use `terraform state list` to compare the resource counts between the old and new deployments to ensure nothing was missed.

---

## **Phase 6: Plan the Migration Strategy**

Migrating the live production environment must be done with minimal risk.

- **Recommendation: Blue-Green Deployment (Option B)**
  - This is the safest and most professional approach. The risk of data loss or state corruption from `terraform state mv` (Option C) on this scale is too high. An in-place refactor (Option A) is not recommended for production systems.
  - **Steps**: 1. **Deploy Parallel Infrastructure**: Using the tested module, deploy a completely new, parallel "green" infrastructure stack in a separate TFC workspace. 2. **Validate Green Environment**: Thoroughly test the new stack to ensure it is fully functional. 3. **Migrate Workloads**: Plan and execute the migration of Kubernetes workloads, data, and DNS from the old "blue" cluster to the new "green" cluster. 4. **Decommission Blue Environment**: Once traffic is fully transitioned and verified, the old infrastructure can be safely destroyed using `terraform destroy`.

---

## **Phase 7: Finalise Documentation and Examples**

Excellent documentation is what makes a module truly reusable.

1. **Create a Comprehensive `README.md`**:
   - This is the module's storefront. It must include:
     - A clear description of what the module does.
     - An architecture diagram.
     - Usage examples for different scenarios (e.g., minimal VPC, VPC with EKS, full deployment).
     - Auto-generated references for all input variables and outputs (use a tool like `terraform-docs`).

2. **Build an `examples/` Directory**:
   - Create subdirectories with working examples for `basic`, `standard`, and `full-featured` deployments, as planned. This allows users to copy, paste, and adapt working code quickly.

3. **Establish a `CHANGELOG.md`**:
   - Document all changes to the module using semantic versioning. The initial release will be `v1.0.0`.
