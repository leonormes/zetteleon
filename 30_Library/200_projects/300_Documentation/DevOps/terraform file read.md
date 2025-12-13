---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: terraform file read
type:
uid: 
updated: 
version:
---

Terraform provides multiple methods for loading and processing files in Infrastructure-as-Code workflows, with distinct approaches for structured data (like CSV) and cloud-init configurations. Below are the key techniques:

---

## 1. File Loading Fundamentals
### Basic File Reading
- `file()` function: Reads file contents as a string

```hcl
  user_data = file("${path.module}/user_data.sh")  # Loads script for EC2 instance [3][5]
```

- `local_file` data source: Accesses file content as a Terraform object

```hcl
  data "local_file" "config" {
    filename = "${path.module}/settings.cfg"
  }
  output "content" { value = data.local_file.config.content } [3]
```

---

## 2. Structured Data Handling
### CSV Processing
- `csvdecode` function: Converts CSV rows into list of maps

```hcl
  locals {
    users = csvdecode(file("users.csv"))  # Creates [{name="a",...}, {name="b",...}]
  }
  resource "aws_user" "example" {
    for_each = { for u in local.users : u.name => u }
    name     = each.value.name
  } [1][4][6]
```

  Limitations:

  - Requires manual parsing for nested structures [9]
  - Prefer JSON/YAML for complex objects using `jsondecode`/`yamldecode` [4]

### JSON/YAML Integration

```hcl
locals {
  config = jsondecode(file("config.json"))  # Direct map conversion
  vpc_settings = local.config.network.vpc [4]
}
```

---

## 3. Cloud-Init Implementation
### Direct Script Injection

```hcl
resource "aws_instance" "web" {
  user_data = file("cloud-init.yaml")  # Requires valid #! header [5][8]
}
```

### Multi-Part Configurations
- `cloudinit_config` provider: Combines scripts/cloud-init directives

  ```hcl
  data "cloudinit_config" "server" {
    part {
      content_type = "text/x-shellscript"
      content      = file("setup.sh")
    }
    part {
      content_type = "text/cloud-config"
      content      = file("security.yml")
    }
  } [8]
  ```

### Template Integration

```hcl
data "template_cloudinit_config" "app" {
  part {
    content_type = "text/cloud-config"
    content      = templatefile("app-config.tftpl", { db_ip = var.db_address })
  }
} [2]
```

---

## 4. Advanced Patterns
- Dynamic file lists:

```hcl
for_each = fileset("${path.module}/policies", ".json")
content  = file(each.value) [7]
```

- Conditional loading:

```hcl
user_data = var.use_custom_script ? file("custom.sh") : null
```

---

## Key Considerations
1. Security: Avoid sensitive data in plaintext files
2. Validation: Use `can()` for error handling with file operations
3. Performance: Large files (>1MB) may require alternative storage (S3, etc.)
4. Idempotency: Ensure file changes trigger resource updates via `timestamp()`

For CSV-based user management, a typical implementation would combine `csvdecode` with resource `for_each` iteration, while cloud-init deployments benefit from multi-part configurations using Terraform's cloud-init provider [1][5][8].
