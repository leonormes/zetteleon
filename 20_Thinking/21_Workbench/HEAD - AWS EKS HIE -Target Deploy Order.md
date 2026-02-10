---
created: 2025-12-04T12:02:41Z
last_reviewed:
modified: 2026-02-10T10:16:09+00:00
status: processing
tags:
  - state/thinking
  - customer/hie
title: HEAD - AWS EKS HIE -Target Deploy Order
type: head
updated:
---

| 1 | -target=module.vpc                            | Nothing—foundation layer                |
| ----- | --------------------------------------------- | ----------------------------------------- |
| 2 | -target=module.jumpbox          | VPC                                       |
| 3 | -target=module.eks              | VPC                                       |
| 4 | -target=module.s3_bucket        | VPC, Jumpbox                              |
| 5 | -target=module.s3_bucket_qc     | VPC, Jumpbox, EKS                         |
| 6 | -target=module.s3_bucket_export | VPC, Jumpbox, EKS                         |
| 7 | -target=module.dns_zone         | VPC, EKS (only if enable_dns_zone = true) |
