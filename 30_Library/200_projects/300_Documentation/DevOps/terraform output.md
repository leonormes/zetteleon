---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:39Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: terraform output
type:
uid: 
updated: 
version:
---

Terraform outputs can be directly interpolated into template strings to create dynamic SSH commands. Here's how to achieve this for both single and multiple instances:

---

## SSH Command Generation
### Single Instance

```hcl
output "ssh_command" {
  value = "ssh admin@${aws_instance.web.public_ip}"  # Direct interpolation
}
```

After apply:

`terraform output ssh_command` returns `ssh admin@203.0.113.45` [3][8]

### Multiple Instances

```hcl
output "ssh_commands" {
  value = [
    for instance in aws_instance.web : 
    "ssh admin@${instance.public_ip}"  # Generates list of commands
  ]
}
```

Output:

```sh
["ssh admin@203.0.113.45", "ssh admin@198.51.100.6"] [2][3]
```

---

## Advanced Formatting
### Named Access with Maps

```hcl
output "ssh_commands" {
  value = {
    for idx, instance in aws_instance.web :
    "server-${idx}" => "ssh admin@${instance.public_ip}"
  }
}
```

Result:

```sh
{
  "server-0" = "ssh admin@203.0.113.45"
  "server-1" = "ssh admin@198.51.100.6"
} [2][6]
```

### File Generation

```hcl
resource "local_file" "access_commands" {
  content  = join("\n", [for i in aws_instance.web : "ssh admin@${i.public_ip}"])
  filename = "ssh_access.txt"  # Creates file with one command per line
} [9]
```

---

## Template Integration

For complex command structures:

```hcl
output "bastion_ssh" {
  value = templatefile("ssh.tftpl", {
    user      = "admin"
    jump_host = aws_instance.bastion.public_ip
    targets   = aws_instance.web..public_ip
  })
}
```

Template (ssh.tftpl):

```sh
%{ for ip in targets ~}
ssh -J ${user}@${jump_host} ${user}@${ip}
%{ endfor ~} [7]
```

---

## Usage Patterns
1. Direct CLI access:
   `terraform output -raw ssh_command | pbcopy`
   Copies command to clipboard

2. Automated scripting:

```sh
eval $(terraform output -raw ssh_command)
```

3. Multi-environment handling:

```hcl
output "prod_ssh" {
 value = "ssh ${var.env_user}@${module.prod_cluster.public_ip}"
}
```

---

## Key Considerations
- Security: Avoid storing sensitive connection details in plaintext outputs
- Dynamic updates: Outputs automatically refresh after each `terraform apply`
- Platform compatibility: Use `local_file` instead of `local-exec` for file operations [9]
- State awareness: Outputs reflect current infrastructure state, not desired configuration

For environments with frequently changing IPs, combine with `terraform refresh` to update outputs without modifying infrastructure.
