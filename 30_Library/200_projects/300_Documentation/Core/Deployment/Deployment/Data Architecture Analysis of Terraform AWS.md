---
aliases: []
confidence: 
created: 2025-02-26T02:00:36Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, terraform]
title: Data Architecture Analysis of Terraform AWS
type: documentation
uid: 
updated: 
version: 1
---

**Data Architecture Analysis of `config.tf`**

The `config.tf` file primarily defines infrastructure configuration data for an AWS environment using Terraform. Its data architecture relies heavily on maps and lists, which is standard for Terraform configuration. While not a traditional application codebase, it exhibits several data-oriented design principles, particularly in its use of structured data and separation of concerns. The file demonstrates a clear separation between the logical model of infrastructure and the physical implementation, which is a strong point. However, it also has areas where improvements in explicitness and validation could be made.

**1. Data Entity Identification**

- **Metadata:**
    - **Purpose:** Stores basic information about the environment (name, region, tags).
    - **Scope:** Global configuration, applies to all resources.
    - **Naming:** `metadata` is a clear, self-explanatory name.
    - **Domain:** Infrastructure-as-Code
    - **Example:**

```hcp
locals {
 metadata = {
	name   = "ff-test-calico"
	region = "eu-west-2"
	tags = {
	  Owner = "Leon"
	  Env   = "Testing"
	}
 }
}
```

- **Network Base:**
    - **Purpose:** Defines the core network parameters (VPC CIDR, subnet identifiers).
    - **Scope:** Global network configuration.
    - **Naming:** `network_base` is suitable, `subnet_identifiers` is descriptive.
    - **Domain:** Networking
    - **Example:**

```hcp
locals {
 network_base = {
	vpc = {
	  cidr = "10.65.0.0/23"
	}
	subnet_identifiers = ["Jumpbox", "Eks_az_1", "Eks_az_2", "Firewall", "Endpoints", "Nat"]
 }
}
```

- **EKS:**
    - **Purpose:** Configuration for the Elastic Kubernetes Service (EKS) cluster (version, node groups, addons).
    - **Scope:** Kubernetes cluster configuration.
    - **Naming:** `eks` is standard, `node_groups`, and `addons` are descriptive.
    - **Domain:** Container Orchestration
    - **Example:**

```hcp
locals {
 eks = {
	kubernetes_version = "1.31"
	node_groups = {
	  default = {
		 instance_types = ["t3.medium"]
		 // ...
	  }
	}
	addons = {
	  vpc_cni = {
		 version = "v1.15.1-eksbuild.1"
		 enabled = true
	  }
	  // ...
	}
 }
}
```

- **Availability Zones (AZs):**
    - **Purpose:** List of available AZs in the selected region.
    - **Scope:** Region-specific.
    - **Naming:** `azs` is concise but might be better as `availability_zones` for clarity.
    - **Domain:** Cloud Computing
    - **Example:**

```hcp
locals {
 azs = slice(data.aws_availability_zones.available.names, 0, 2)
}
```

- **Subnet CIDRs:**
    - **Purpose:** Calculation of CIDR blocks for individual subnets.
    - **Scope:** Network configuration.
    - **Naming:** `subnet_cidrs` is clear.
    - **Domain:** Networking
    - **Example:**

```hcp
locals {
 subnet_cidrs = {
	Eks_az_1 = cidrsubnet(local.network_base.vpc.cidr, 3, 0)
	// ...
 }
}
```

- **Config:**
    - **Purpose:** Top-level structure organizing all other configuration entities.
    - **Scope:** Global configuration.
    - **Naming:** `config` is generic but acceptable here as it is the root.
    - **Domain:** Infrastructure-as-Code
    - **Example:**

```hcp
locals {
 config = {
	metadata = local.metadata
	network = {
	  // ...
	}
	// ...
 }
}
```

- **Convenience Accessors:**
    - **Purpose:** Provide direct access to values within the config struct.
    - **Scope:** global
    - **Naming:** self explanatory: `name`, `region`, `vpc_cidr`, `tags`
    - **Domain:** Infrastructure-as-Code

**Entity Relationships:**

- **Hierarchical Structure:** The `config` entity forms the root, containing `metadata`, `network`, `endpoints`, `compute`, and `access`.
- **Direct References:** `config.network.subnets` references `subnet_cidrs` and `azs`.
- **Implicit Relationships:** Subnet identifiers (`Jumpbox`, `Eks_az_1`, etc.) act as implicit keys relating `network_base.subnet_identifiers` with `subnet_cidrs` and `config.network.subnets`.
- `eks.node_groups.default.subnet_ids` refer to `subnet_identifiers`

**2. Data Representation Analysis**

- **Maps (Objects):**
    - **Usage:** `metadata`, `network_base`, `eks`, `subnet_cidrs`, `config` use maps extensively to represent structured data.
    - **Alignment:** Aligns well with data-oriented principles because it groups related information.
    - **Specialized vs. Generic:** Mostly specialized (e.g., `subnet_cidrs` specifically stores CIDR calculations), improving readability.
    - **Example:**

```hcp
locals {
 metadata = {
	name   = "ff-test-calico"
	region = "eu-west-2"
 }
 subnet_cidrs = {
	Eks_az_1 = cidrsubnet(local.network_base.vpc.cidr, 3, 0)
 }
}
```

- **Lists (Arrays):**
    - **Usage:** `network_base.subnet_identifiers`, `azs`, `eks.node_groups.default.instance_types`, `endpoints.interface.services`.
    - **Alignment:** Appropriate for ordered or collections of similar items.
    - **Specialized vs. Generic:** Mostly generic, but the context of use adds domain-specific meaning (e.g., `instance_types` within `node_groups`).
    - **Example:**

```hcp
locals {
 network_base = {
	 subnet_identifiers = ["Jumpbox", "Eks_az_1"]
 }
 eks = {
	node_groups = {
	  default = {
		 instance_types = ["t3.medium"]
	  }
	}
 }
}
```

- **Strings:**
    - **Usage:** `cidr` are defined as strings. `kubernetes_version` are defined as strings. `ami_type` is defined as a string.
    - **Alignment:** The correct use for data of this type
    - **Specialized vs. Generic:** Generic
    - **Example:**

```hcp
locals {
  eks = {
		kubernetes_version = "1.31"
  }
network_base = {
		vpc = {
		  cidr = "10.65.0.0/23"
		}
}
}
```

- **Computed Values:**
    - **Usage:** `azs`, `subnet_cidrs`.
    - **Alignment:** Demonstrates a data-oriented approach, deriving new data from existing inputs rather than hardcoding.
    - **Example:**

```hcp
locals {
 azs = slice(data.aws_availability_zones.available.names, 0, 2)
 subnet_cidrs = {
	Eks_az_1 = cidrsubnet(local.network_base.vpc.cidr, 3, 0)
 }
}
```

- **Optimization Structures:**
    - No explicit indexes or caches are defined, which is typical for Terraform configuration. However, the use of calculated values (`subnet_cidrs`, `azs`) can be seen as a form of pre-computation, optimizing data access.
- **Consistency:**
    - The use of maps and lists for structured data is highly consistent throughout the file.
    - The combination of maps and lists within the `config` local variable makes for a easy-to-parse structure.
- **Separation:**
    - There is excellent separation between logical models (e.g. `network_base`, `eks`) and physical implementation (the implicit mapping between subnet ids and their cidr).

**3. Relationship Mapping**

- **Direct References:**
    - `config.network.vpc` references `network_base.vpc`.
    - `config.network.subnets` references `subnet_cidrs` and `azs`.
    - `config.endpoints.gateway.s3.route_table_ids` references `subnet_identifiers` via name resolution.
    - `eks.node_groups.default.subnet_ids` refer to `subnet_identifiers` via name resolution
- **Implicit Relationships:**
    - `subnet_identifiers` in `network_base` implicitly connects to `subnet_cidrs` and `config.network.subnets` through matching names (e.g., `Jumpbox`).
    - This is based on the subnet name.
- **Hierarchical Structures:**
    - The `config` data structure forms the primary hierarchy.
    - Within `config.network`, there's a nested hierarchy of `vpc`, `availability_zones`, and `subnets`.
    - Within `config.compute`, there is `kubernetes`, and then `clusters`
- **Many-to-Many Relationships:**
    - Indirectly, the relationship between `endpoints.interface.services` and potential consumers can be seen as many-to-many. This is not explicitly modeled but implied by the services being potentially usable from many subnets.
    - Multiple node groups, as seen under `config.compute.kubernetes.clusters.main.node_groups` implicitly has a many to many relationship with `config.network.subnets` (for example through `eks.node_groups.default.subnet_ids`
- **Implementation of Relationships:**
    - **Data Structure Embedding:** `metadata`, `vpc` are embedded within `config`.
    - **Reference:** `config.network.subnets.Eks_az_1.cidr` indirectly references `subnet_cidrs["Eks_az_1"]`.
    - **Intermediate mapping:** The subnet names (`Jumpbox`, `Eks_az_1`, `Eks_az_2`) act as a mapping between subnet identifiers and their specific configurations.
- **Performance Implications:**
    - The current relationships are lightweight and efficient for configuration. There are no complex joins or lookups.
    - The use of maps allows for efficient key-based access.
    - Using name resolution is fast, but can become fragile if a name is modified or deleted.
    - The lack of complexity also implies a lack of performance issues.

**4. Schema Analysis**

- **Schema Definitions:**
    - **Implicit:** The schema is implicitly defined through the structure of the maps and lists.
    - **Documented but not enforced:** the comments help describe the structure and purpose, but no validation happens at all.
    - **No Explicit Schemas:** There are no formal schemas (e.g., JSON Schema) defined.
- **Schema Evolution:**
    - No explicit mechanisms for schema evolution are present. Changes would require manual updates to the code.
- **Validation:**
    - There is no built-in validation in the provided code. Terraform itself does some basic validation during the plan/apply phase, but no data-level validation.
- **Improvements**
    - Adding validation (such as terratest) would help ensure the config remains valid as the complexity increases.

**5. Immutability Assessment**

- **Immutability:**
    - The data structures in this file are treated as effectively immutable.
    - Terraform configurations are generally considered immutable; changes result in creating new infrastructure components.
- **Copy-on-Write:**
    - Not applicable in this context. Terraform's state management handles change tracking.
- **Modification:**
    - No methods or functions directly modify the data structures in place. Changes are made by creating new versions of the configuration file.
- **Impact:**
    - **Code Complexity:** Immutability simplifies reasoning about the configuration.
    - **Performance:** Minimal impact, as there is no need for deep copies or complex change tracking.
    - **Concurrency:** Concurrency is not a primary concern for static configuration files like this.

**6. Data Access Patterns**

- **Direct Property Access:**
    - **Usage:** `local.metadata.name`, `local.network_base.vpc.cidr`.
    - **Alignment:** Directly accessing properties of maps is efficient and common in Terraform.
    - **Example:**

```hcp
locals {
 name = local.metadata.name
}
```

- **Computed Value Access:**
    - **Usage:** Accessing derived data like `local.azs` or `local.subnet_cidrs["Eks_az_1"]`.
    - **Alignment:** Good for abstracting away the complexity of calculations.
    - **Example:**

 ```hcp
   locals {
		 azs = slice(data.aws_availability_zones.available.names, 0, 2)
		 subnet_cidrs = {
			Eks_az_1 = cidrsubnet(local.network_base.vpc.cidr, 3, 0)
		 }
	  }
 ```

- **Getter/Setter Methods:**
    - Not present. No explicit methods are used for data access.
- **Query Interfaces/ORM:**
    - Not applicable.
- **Encapsulation:**
    - Encapsulation is minimal, given that direct property access is used.
    - However, local variables do help keep the underlying complexity encapsulated from the outside world.
- **Abstraction:**
    - `config` and the `locals` are a type of abstraction, by combining and structuring disparate properties.
    - `azs` and `subnet_cidrs` offer a type of abstraction by pre-calculating commonly used values.
- **Caching/Optimization:**
    - `subnet_cidrs` and `azs` can be seen as a simple form of pre-calculation that reduces redundancy.

**Potential Improvements and Alternatives**

1. **Explicit Schemas:** Using JSON Schema or a similar mechanism to define the configuration schema could significantly improve validation and clarity.
2. **Validation:** Implement data validation using a testing framework (e.g., Terratest) to ensure configuration data meets requirements.
3. **Data integrity testing**: Adding test cases to check for invalid name usage.
4. **Naming Conventions:** Standardize naming further (e.g., consistently using `availability_zones` instead of `azs`).
5. **Abstraction:** While the abstraction is good, one could also imagine taking it one step further by creating a module to handle the kubernetes config.

**Conclusion**

The `config.tf` file demonstrates a strong data-oriented design for an infrastructure-as-code context. Its use of structured data with maps and lists, computed values, and effective separation of logical and physical models are particularly commendable. While there is room for improvement regarding explicitness and validation, the current approach provides a good basis for managing complex infrastructure configurations in a data-driven way. The data is relatively independent from the Terraform implementation, and could be fairly easily extracted and used in another system if necessary.

**Data Architecture Analysis of `main.tf`**

**Executive Summary**

The `main.tf` file demonstrates a modular approach to infrastructure-as-code by calling several modules (`vpc`, `gateway`, `vpc_endpoints`, `jumpbox`, `eks`, `dns_zone`). It primarily uses the data defined in `config.tf` to configure these modules. This file heavily relies on maps and lists, computed values, and implicit relationships to manage infrastructure data. It shows a clear understanding of data-oriented principles, especially in its separation of configuration data from implementation details. However, it also exhibits opportunities for improvement in schema enforcement and validation, similar to `config.tf`.

**1. Data Entity Identification**

- **VPC:**
    - **Purpose:** Represents the Virtual Private Cloud and its configuration.
    - **Scope:** Top-level network.
    - **Naming:** Consistent with domain terminology.
    - **Source:** Directly derived from `config.tf`
    - **Example**

```hcp
module "vpc" {
  source = "./modules/vpc"

  name       = local.name
  cidr       = local.vpc_cidr
  deploy_vpc = true

  subnets = [
  for identifier in local.network_base.subnet_identifiers : {
		cidr       = local.config.network.subnets[identifier].cidr
		az         = local.config.network.subnets[identifier].az
		identifier = identifier
		type       = local.config.network.subnets[identifier].type
		name       = identifier
		tags       = try(local.config.network.subnets[identifier].tags, {})
  }
  ]
}
```

- **Subnets:**
    - **Purpose:** Represents individual subnets within the VPC.
    - **Scope:** Contained within the VPC.
    - **Naming:** Matches the `subnet_identifiers` in `config.tf`.
    - **Source:** Mapped from `config.tf`'s `subnet_identifiers`, `subnet_cidrs`, and `network.subnets`.
    - **Example:**

    ```hcp
    module "vpc" {
       # ...
        subnets = [
        for identifier in local.network_base.subnet_identifiers : {
            cidr       = local.config.network.subnets[identifier].cidr
        }
        ]
    }
    ```

- **Network ACLs:**
    - **Purpose:** Network access control lists for the VPC.
    - **Scope:** Configured within the VPC.
    - **Naming:** Clear and consistent.
    - **Source:** Directly derived from `config.tf`
- **Gateway:**
    - **Purpose:** Represents the internet gateway and NAT gateway configuration.
    - **Scope:** Connects the VPC to the outside world.
    - **Naming:** Standard domain terminology.
    - **Source:** Derived from `config.tf` and references the `vpc` module outputs.
    - **Example:**

```hcp
module "gateway" {
	 # ...
	 vpc_id   = module.vpc.vpc_id
	 vpc_cidr = local.vpc_cidr
	 # ...
}
```

- **VPC Endpoints:**
    - **Purpose:** Represents endpoints for AWS services within the VPC.
    - **Scope:** Connects the VPC to other AWS services.
    - **Naming:** Based on the services in `config.tf`.
    - **Source:** Mapped from `config.tf`'s `endpoints` and references the `vpc` module.
    - **Example:**

```hcp
module "vpc_endpoints" {
	 # ...
  endpoints = merge(
		# Gateway endpoints (S3)
		{
		for name, config in local.config.endpoints.gateway : name => {
			 service         = config.service
			 # ...
		}
		},
		# Interface endpoints
		{
		for service in local.config.endpoints.interface.services :
		replace(service, ".", "_") => {
			 service             = service
			 # ...
		}
		}
  )
}
```

- **Jumpbox:**
    - **Purpose:** Represents the jumpbox instance.
    - **Scope:** Access to the private network.
    - **Naming:** Self-explanatory.
    - **Source:** Derived from `config.tf` and references the `vpc` module.
    - **Example**

```hcp
module "jumpbox" {
	 # ...
	 subnet_id   = module.vpc.subnets_id_map["Jumpbox"]
	 private_ips = [cidrhost(local.subnet_cidrs["Jumpbox"], 4)]
	 vpc_id      = module.vpc.vpc_id
	 # ...
}
```

- **EKS Cluster:**
    - **Purpose:** Represents the Elastic Kubernetes Service (EKS) cluster.
    - **Scope:** Container orchestration.
    - **Naming:** Consistent with AWS terminology.
    - **Source:** Derived from `config.tf`'s `eks` and references the `vpc` module.
    - **Example:**

```hcp
module "eks" {
  # ...
  cluster_version = local.eks.kubernetes_version
  # ...
}
```

- **EKS Node Groups:**
    - **Purpose:** Represents worker node groups in the EKS cluster.
    - **Scope:** Within the EKS cluster.
    - **Naming:** Follows the `default` key convention from `config.tf`.
    - **Source:** Mapped from `config.tf`'s `eks.node_groups` and refers to the VPC subnets.
- **DNS Zone:**
    - **Purpose:** Represents a DNS zone and its records.
    - **Scope:** External DNS management.
    - **Naming:** Related to the `name` of the deployment.
    - **Source:** Configured based on the `eks_elb` data.
- **IAM Roles and Policies:**
    - **Purpose:** Represents IAM roles and policies for AWS resources.
    - **Scope:** Security and permissions.
    - **Naming:** Standard AWS role names.
    - **Source:** Defined directly in `main.tf`.

**Entity Relationships:**

- **Hierarchical Structure:**
    - VPC is the root, containing subnets and network ACLs.
    - Gateway and VPC Endpoints are connected to the VPC.
    - EKS and Jumpbox are hosted within the VPC and its subnets.
    - EKS contains node groups.
- **Direct References:**
    - The `gateway` module uses `module.vpc.vpc_id` and `module.vpc.subnets_id_map`.
    - The `vpc_endpoints` module uses `module.vpc.vpc_id` and `module.vpc.subnets_id_map`.
    - The `jumpbox` module uses `module.vpc.vpc_id` and `module.vpc.subnets_id_map`.
    - The `eks` module uses `module.vpc.vpc_id` and `module.vpc.subnets_id_map`.
- **Implicit Relationships:**
    - Subnet identifiers (e.g., `Jumpbox`, `Eks_az_1`) tie together `config.tf` and the `vpc` module via the `subnets_id_map` output.
- **Many-to-Many Relationships:**
    - Subnets can have many endpoints, and an endpoint can be available in many subnets.
    - node groups can have multiple instance types, and multiple node groups can live in the same subnet.
- **Dependency Relationships:**
    - Most modules depend on the `vpc` module.
    - `gateway` depends on `vpc`
    - `vpc_endpoints` depends on `vpc`
    - `jumpbox` depends on `vpc` and `vpc_endpoints` and `gateway`
    - `eks` depends on `vpc` and `vpc_endpoints`, `gateway`, `jumpbox`
    - `dns_zone` depends on `vpc` and the output of the Load Balancer

**2. Data Representation Analysis**

- **Maps (Objects):**
    - **Usage:** `module.vpc.subnets_id_map`, `module.vpc.route_table_id_map`, `local.config.endpoints.gateway`, `local.eks.node_groups`, `endpoints` within `vpc_endpoints`, `security_group_rules`
    - **Alignment:** Excellent for organizing key-value pairs, especially where keys are meaningful identifiers.
    - **Specialized vs. Generic:** These are specialized maps tailored for managing infrastructure components.
    - **Example:**

```hcp
module "vpc" {
	# ...
	subnets = [
		 for identifier in local.network_base.subnet_identifiers : {
			  cidr       = local.config.network.subnets[identifier].cidr
		 }
	]
}
```

- **Lists (Arrays):**
    - **Usage:** `local.network_base.subnet_identifiers`, `local.config.endpoints.interface.services`, `outbound_to_nat_route_table_ids`, `subnets` in the vpc module, `eks_elb_security_group_inbound_rules`
    - **Alignment:** Appropriate for ordered lists of items.
    - **Specialized vs. Generic:** The context usually gives these generic data structures a domain-specific meaning (e.g., a list of `subnet_identifiers`).
    - **Example:**

```hcp
module "gateway" {
	# ...
	outbound_to_nat_route_table_ids = [module.vpc.route_table_id_map["Eks_az_1"], module.vpc.route_table_id_map["Eks_az_2"]]
	# ...
}
```

- **Strings:**
    - **Usage:** `local.vpc_cidr`, `local.name`, `module.vpc.vpc_id`, service names, subnet types.
    - **Alignment:** Correctly used for representing text-based data.
- **Computed Values:**
    - **Usage:** `cidrhost(local.subnet_cidrs["Jumpbox"], 4)`, `module.vpc.subnets_id_map["Jumpbox"]`, loop generated values such as `config.network.subnets[identifier].cidr`
    - **Alignment:** Data-oriented, reducing redundancy and increasing maintainability.
- **Optimization Structures:**
    - `module.vpc.subnets_id_map` and `module.vpc.route_table_id_map` are key optimization structures, allowing fast lookups of relevant subnet and route table IDs.
- **Consistency:**
    - The consistent use of maps and lists for structured data is commendable.
    - Naming is mostly consistent, following common domain terminology.
- **Separation:**
    - Excellent separation between configuration data (in `config.tf`) and the logic for creating resources (in `main.tf` and modules).
    - The use of modules enhances this separation and encourages reusability.

**3. Relationship Mapping**

- **Direct References:**
    - Modules directly reference each other's outputs (e.g., `gateway` referencing `vpc`).
    - Subnet identifiers are used to look up subnet IDs, CIDRs, and availability zones in `config.tf`.
    - `gateway.outbound_to_nat_route_table_ids` and `gateway.outbound_to_firewall_route_table_ids` directly reference `module.vpc.route_table_id_map`.
    - `jumpbox` and `eks` modules reference `module.vpc.subnets_id_map`
    - `vpc_endpoints` directly references both `config` and `module.vpc.route_table_id_map` and `module.vpc.subnets_id_map`
- **Implicit Relationships:**
    - Subnet identifiers (`Jumpbox`, `Eks_az_1`, etc.) connect `config.tf`'s network configuration with the `vpc` module's subnet management.
    - The names in `local.config.endpoints.gateway` and `local.config.endpoints.interface.services` act as keys for accessing related configurations.
- **Hierarchical Structures:**
    - The VPC module creates subnets, which are nested within the VPC.
    - The EKS module creates node groups, which are nested within the EKS cluster.
    - The top level config is implicit.
- **Many-to-Many Relationships:**
    - Multiple subnets can share the same network ACL (indirectly, through `subnet_identifiers`).
    - Multiple services can have endpoints in multiple subnets.
    - multiple node groups can exist in the same subnet.
- **Implementation of Relationships:**
    - **Data Structure Embedding:** Subnet configurations are embedded within the VPC module's `subnets` list.
    - **Reference:** Most relationships are implemented through references using module outputs and data lookups.
    - **Intermediate Mapping:** `module.vpc.subnets_id_map` and `module.vpc.route_table_id_map` are crucial intermediate structures for efficient relationship management.
- **Performance Implications:**
    - The map-based lookups (e.g., `subnets_id_map`, `route_table_id_map`) are highly efficient.
    - Direct referencing of module outputs is also fast.
    - There is potential for some overhead with loops, but in this context, it is unlikely to be a significant bottleneck.

**4. Schema Analysis**

- **Schema Definitions:**
    - **Implicit:** The schema is implicitly defined by the structure of the data in `config.tf`, the data structures used in `main.tf`, and the module input variables.
    - **No Explicit Schemas:** No explicit schema definitions are present (e.g., JSON Schema).
- **Schema Evolution:**
    - No explicit mechanisms for schema evolution. Changes require manual updates to both `config.tf` and `main.tf`.
- **Validation:**
    - Minimal validation, primarily through Terraform's built-in type checking and dependencies.
    - The `try()` function is used as a form of error handling when the `tags` are missing.
- **Improvements**
    - Adding validation (such as terratest) would help ensure the config remains valid as the complexity increases.
    - Adding a module for the config, or having the config output structured data could help with validation.

**5. Immutability Assessment**

- **Immutability:**
    - Data is treated as effectively immutable. Changes to configuration require changes to the `config.tf` file, followed by a Terraform plan/apply.
    - Terraform's state management tracks changes and triggers updates to resources as needed.
- **Copy-on-Write:**
    - Not directly applicable.
- **Modification:**
    - No functions or methods modify data in place. Changes are made by updating the configuration data and re-running Terraform.
- **Impact:**
    - **Code Complexity:** Immutability simplifies understanding resource dependencies and updates.
    - **Performance:** Minimal impact.
    - **Concurrency:** Concurrency is not a primary concern in this case.

**6. Data Access Patterns**

- **Direct Property Access:**
    - **Usage:** `local.vpc_cidr`, `local.name`, `local.eks.kubernetes_version`.
    - **Alignment:** Standard Terraform approach.
- **Map Lookups:**
    - **Usage:** `local.config.network.subnets[identifier].cidr`, `module.vpc.subnets_id_map["Jumpbox"]`.
    - **Alignment:** Very efficient.
- **Computed Value Access:**
    - **Usage:** `cidrhost(local.subnet_cidrs["Jumpbox"], 4)`.
    - **Alignment:** Promotes data derivation rather than hardcoding.
- **Module Output Access:**
    - **Usage:** `module.vpc.vpc_id`, `module.vpc.subnets_id_map`, `module.vpc.route_table_id_map`.
    - **Alignment:** Standard way to access data from modules.
- **Getter/Setter Methods:**
    - Not present.
- **Query Interfaces/ORM:**
    - Not applicable.
- **Encapsulation:**
    - Modules provide a degree of encapsulation by hiding implementation details.
    - `config.tf` acts as an abstraction layer for configuration values.
- **Abstraction:**
    - Modules provide a significant layer of abstraction.
    - `config.tf` further abstracts configuration.
- **Caching/Optimization:**
    - `subnets_id_map` and `route_table_id_map` are critical for optimization.
    - Precomputing subnet and route table IDs.

**Potential Improvements and Alternatives**

1. **Explicit Schemas:** Adding JSON Schema or a similar mechanism for `config.tf` would greatly enhance validation.
2. **Validation:** Implement more robust validation using a testing framework like Terratest, including data-level validation rules.
3. **Error Handling:** Improve error handling beyond `try()` to handle missing data more gracefully.
4. **Configuration Module:** Consider creating a configuration module that reads `config.tf` and outputs structured data to
