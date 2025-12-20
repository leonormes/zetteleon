---
aliases: []
confidence: 
created: 2025-02-17T11:24:11Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:44Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Is there a more modern way than using the resource
type:
uid: 
updated: 
version:
---

Yes, there is a more modern way to replace the "null_resource" for applying Calico manifests in Terraform. As of Terraform version 1.4, introduced in 2023, you can use the built-in `terraform_data` resource instead of `null_resource`[^1][^5].

The `terraform_data` resource serves as a native replacement for `null_resource` and offers similar capabilities without requiring an additional provider[^1][^3]. Here's how you can modify the example to use `terraform_data`:

```hcl
resource "terraform_data" "apply_calico_manifest" {
  depends_on = [aws_eks_cluster.my_cluster]

  provisioner "local-exec" {
    command = <<-EOT
      kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/calico-vxlan.yaml
      kubectl -n kube-system set env daemonset/calico-node FELIX_AWSSRCDSTCHECK=Disable
    EOT
  }
}
```

This approach is more integrated with Terraform and doesn't require downloading an additional provider, making it a more efficient and modern solution[^3].
