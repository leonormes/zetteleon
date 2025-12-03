---
aliases: []
confidence: 
created: 2025-11-27T15:19:20Z
epistemic: 
last_reviewed: 
modified: 2025-11-27T15:20:06Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Azure Snapshot Retention Investigation
type: 
uid: 
updated: 
---

## Summary

Snapshots in the `PROD-1-SNAPSHOT-RG` resource group within the "FITCloud Production" subscription are being retained for longer than the configured 14-day retention policy. This is due to an issue with the Azure Backup for AKS extension, which is responsible for the lifecycle management of these snapshots.

## Findings

1.  **Problem:** Azure snapshots are being retained for much longer than the configured 14-day retention policy.
2.  **Root Cause:** The Azure Backup for AKS extension (`azbkuextension`) is in an unhealthy state, which prevents it from performing lifecycle management on the snapshots, including deletion.
3.  **Evidence:**
    -   The backup instance `prod1aksdaily` is in a `ProtectionError` state.
    -   The error message is `UserErrorKubernetesCustomResourcesNotPickedUpByExtension`.
    -   The backup extension `azbkuextension` has an empty `statuses` array, indicating it's not healthy.
    -   The Custom Resource Definition (CRD) `validateforbackup.dataprotection.microsoft.com`, which is required by the backup extension, is missing from the AKS cluster.

## Conclusion

Despite successfully reinstalling the `azbkuextension` (as reported by Azure CLI), the extension is not correctly deploying its required Custom Resource Definitions (CRDs) into your Kubernetes cluster. This prevents the extension from fully operating and performing critical tasks like deleting old snapshots, leading to the observed retention issue.

## Next Steps

Given that Azure CLI reports the extension as "Succeeded" but a critical CRD is missing, this indicates a deeper problem that requires further investigation within the AKS cluster or with Azure Support.

I recommend you take the following actions:

1.  **Inspect Extension Logs:** Access the logs of the `dataprotection-microsoft` pods in your AKS cluster for any errors or warnings related to CRD registration. You can use `kubectl logs -n dataprotection-microsoft <pod-name>` for each pod.
2.  **Check Managed Identity Permissions:** Ensure that the managed identity used by the `azbkuextension` has the necessary permissions to create and manage CRDs within your AKS cluster.
3.  **Contact Azure Support:** If the above steps do not reveal the root cause, or if you require deeper assistance, contact Azure Support. Provide them with the `protectionErrorDetails` from the backup instance and the fact that the `validateforbackup.dataprotection.microsoft.com` CRD is missing despite a successful extension provisioning state.
