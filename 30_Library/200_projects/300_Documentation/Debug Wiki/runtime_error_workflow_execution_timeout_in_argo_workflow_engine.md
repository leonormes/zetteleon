---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [pipeline]
title: runtime_error_workflow_execution_timeout_in_argo_workflow_engine
type:
uid: 
updated: 
version:
---

## Runtime Error Workflow Execution Timeout in Argo Workflow Engine

```sh
[0KRunning with gitlab-runner 17.4.0~pre.110.g27400594 (27400594)[0;m
[0K  on blue-4.saas-linux-small-amd64.runners-manager.gitlab.com/default J2nyww-s, system ID: s_cf1798852952[0;m
[0K  feature flags: FF_USE_FASTZIP:true[0;m
[0K[36;1mResolving secrets[0;m[0;m
section_start:1733134319:prepare_executor
[0K[0K[36;1mPreparing the "docker+machine" executor[0;m[0;m
[0KUsing Docker executor with image fitfile/argocli:alpine …[0;m
[0KPulling docker image fitfile/argocli:alpine …[0;m
[0KUsing docker image sha256:96220a87e236cc0619ef82ef3e6bd608bead8134199a759b3b9d7282ce29a119 for fitfile/argocli:alpine with digest fitfile/argocli@sha256:0d832f213f2db74fb578f6cc1e5570ba78f24d599d1ea1c2947c37637380fa4c …[0;m
section_end:1733134328:prepare_executor
[0Ksection_start:1733134328:prepare_script
[0K[0K[36;1mPreparing environment[0;m[0;m
Running on runner-j2nyww-s-project-22023844-concurrent-0 via runner-j2nyww-s-s-l-s-amd64-1733134276-852ad40a…
section_end:1733134331:prepare_script
[0Ksection_start:1733134331:get_sources
[0K[0K[36;1mGetting source from Git repository[0;m[0;m
[32;1mFetching changes…[0;m
Initialized empty Git repository in /builds/fitfile/InsightFILE/.git/
[32;1mCreated fresh repository.[0;m
[32;1mChecking out 92f7bcdf as detached HEAD (ref is refs/merge-requests/1684/train)…[0;m

[32;1mSkipping Git submodules setup[0;m
[32;1m$ git remote set-url origin "${CI_REPOSITORY_URL}"[0;m
section_end:1733134337:get_sources
[0Ksection_start:1733134337:download_artifacts
[0K[0K[36;1mDownloading artifacts[0;m[0;m
[32;1mDownloading artifacts for prepare_kube_config (8517555352)…[0;m
Downloading artifacts from coordinator… ok      [0;m  host[0;m=storage.googleapis.com id[0;m=8517555352 responseStatus[0;m=200 OK token[0;m=glcbt-66
section_end:1733134338:download_artifacts
[0Ksection_start:1733134338:step_script
[0K[0K[36;1mExecuting "step_script" stage of the job script[0;m[0;m
[0KUsing docker image sha256:96220a87e236cc0619ef82ef3e6bd608bead8134199a759b3b9d7282ce29a119 for fitfile/argocli:alpine with digest fitfile/argocli@sha256:0d832f213f2db74fb578f6cc1e5570ba78f24d599d1ea1c2947c37637380fa4c …[0;m
[32;1m$ mkdir -p $CI_PROJECT_DIR/.kube[0;m
[32;1m$ cp $CI_PROJECT_DIR/kubeconfig $CI_PROJECT_DIR/.kube/config[0;m
[32;1m$ argo list -n testing[0;m
NAME                                           STATUS                AGE    DURATION   PRIORITY   MESSAGE
int-test-wntc2                                 Failed (Terminated)   2d     2d         0          Stopped with strategy 'Terminate'
all-integration-tests-f62rw                    Failed (Terminated)   2d     2d         0          Stopped with strategy 'Terminate'
int-test-clvph                                 Failed                37d    37d        0          
all-integration-tests-kldfg                    Failed (Terminated)   108d   108d       0          Stopped with strategy 'Stop'
all-integration-tests-rfvc5                    Failed                22m    10m        0          
all-integration-tests-dwbzc                    Failed                57m    10m        0          
k-anonymise-seventy-four-thousand-rows-2xnhn   Succeeded             2d     1m         0          
k-anonymise-preserving-data-types-fl8n8        Succeeded             5d     41s        0          
k-anonymise-preserving-data-types-b8j6r        Succeeded             5d     40s        0          
k-anonymise-preserving-data-types-bzb86        Succeeded             5d     1m         0          
k-anonymise-preserving-data-types-kx6pz        Succeeded             12d    1m         0          
optout-submit-request-integration-test-f6vtr   Succeeded             32d    15d        0          
optout-submit-request-integration-test-mc6qr   Failed                32d    15d        0          
optout-submit-request-integration-test-4rjkd   Failed (Terminated)   33d    15d        0          Stopped with strategy 'Terminate'
move-files-template-jccfl                      Succeeded             80d    11m        0          
k-anonymise-template-6qp85                     Succeeded             80d    6m         0          
k-anonymise-template-pmlth                     Failed (Terminated)   80d    2m         0          Stopped with strategy 'Terminate'
k-anonymise-template-vmz49                     Failed                82d    14h        0          retryStrategy.expression evaluated to false
k-anonymise-template-952zq                     Failed                82d    14h        0          retryStrategy.expression evaluated to false
k-anonymise-template-x4grv                     Failed (Terminated)   82d    41m        0          Stopped with strategy 'Terminate'
k-anonymise-template-kvtgv                     Failed (Terminated)   83d    1h         0          Stopped with strategy 'Terminate'
k-anonymise-template-tlptf                     Succeeded             83d    3h         0          
k-anonymise-template-xd2pc                     Failed (Terminated)   83d    4m         0          Stopped with strategy 'Terminate'
k-anonymise-template-v7ttl                     Failed                83d    2m         0          retryStrategy.expression evaluated to false
k-anonymise-template-m92ln                     Failed (Terminated)   83d    8m         0          Stopped with strategy 'Terminate'
k-anonymise-template-g5v6h                     Failed (Terminated)   83d    1m         0          Stopped with strategy 'Stop'
k-anonymise-nested-59qxv                       Failed (Terminated)   83d    21s        0          Stopped with strategy 'Terminate'
k-anonymise-template-hgz5n                     Error                 83d    1m         0          Max duration limit exceeded
k-anonymise-template-94j5m                     Failed (Terminated)   84d    8m         0          Stopped with strategy 'Terminate'
k-anonymise-template-9cjdx                     Failed                84d    2m         0          retryStrategy.expression evaluated to false
k-anonymise-template-7n242                     Failed                84d    2m         0          retryStrategy.expression evaluated to false
k-anonymise-template-nkw89                     Failed                84d    2m         0          retryStrategy.expression evaluated to false
k-anonymise-template-vm9qk                     Failed                84d    2m         0          retryStrategy.expression evaluated to false
k-anonymise-template-klgjg                     Failed                84d    2m         0          retryStrategy.expression evaluated to false
k-anonymise-template-rn4qx                     Failed                84d    3m         0          retryStrategy.expression evaluated to false
k-anonymise-template-z9rd2                     Failed                87d    3m         0          retryStrategy.expression evaluated to false
k-anonymise-template-49g2p                     Succeeded             86d    1h         0          
k-anonymise-template-bjmb5                     Error                 87d    18m        0          Max duration limit exceeded
k-anonymise-template-8qnwb                     Failed                87d    22s        0          retryStrategy.expression evaluated to false
[32;1m$ argo submit -n testing --generate-name int-test- --from workflowtemplate/all-integration-tests[0;m
Name:                int-test-n2ks5
Namespace:           testing
ServiceAccount:      unset
Status:              Pending
Created:             Mon Dec 02 10:12:35 +0000 (now)
Progress:            
[32;1m$ argo wait -n testing @latest[0;m
@latest Failed at 2024-12-02 10:16:38 +0000 UTC
section_end:1733134599:step_script
[0Ksection_start:1733134599:cleanup_file_variables
[0K[0K[36;1mCleaning up project directory and file based variables[0;m[0;m
section_end:1733134599:cleanup_file_variables
[0K[31;1mERROR: Job failed: exit code 1
[0;m
```

### Error Classification

- Primary Category: Runtime Error
- Subcategory: Resource Limit Exceeded
- Severity Level: High
- Impact Scope: System-wide

### Description

Argo workflows are failing to complete within the allocated time limit, resulting in a "Max duration limit exceeded" error. This indicates that the workflow steps are taking longer than expected to execute, potentially causing delays in downstream processes and impacting overall system performance.

### Technical Details

- Error message: `Max duration limit exceeded`
- Environment information: GitLab CI/CD pipeline, Argo Workflow Engine deployed on Kubernetes
- Affected components: Argo workflows, Kubernetes pods, underlying infrastructure
- Related system states: Resource contention, network latency, workload spikes

### Root Cause

- Primary failure point: Insufficient time allocation for workflow execution.
- Contributing factors:
    - Long-running tasks within the workflow.
    - Resource constraints on the Kubernetes cluster.
    - Network latency issues affecting communication between pods.
    - Unexpected workload spikes exceeding system capacity.
- Trigger conditions:
    - Large datasets requiring extensive processing.
    - Complex workflow logic with multiple dependencies.
    - External service calls experiencing delays.
    - Infrastructure limitations impacting performance.
- Environmental dependencies:
    - Kubernetes cluster size and configuration.
    - Network bandwidth and stability.
    - Availability of external resources.

### Resolution

- Immediate fixes:
    - Increase the `activeDeadlineSeconds` parameter in the Argo workflow spec to allow more time for execution.
    - Monitor workflow execution and identify long-running steps for optimization.
    - Scale up the Kubernetes cluster to provide additional resources.
- Long-term solutions:
    - Optimize workflow logic to reduce execution time.
    - Implement resource limits and quotas to prevent contention.
    - Improve network performance and reduce latency.
    - Monitor system health and proactively address potential bottlenecks.
- Prevention strategies:
    - Set realistic time limits based on historical data and performance testing.
    - Implement alerts and notifications for workflows exceeding thresholds.
    - Regularly review and optimize workflow definitions.
    - Conduct capacity planning to ensure sufficient resources are available.

### Related Information
- Troubleshooting Argo Workflows

### Validation Checklist

Looking at this GitLab CI job output, I can analyze what happened step by step to identify the error:

The job was attempting to run an integration test workflow using Argo, and we can trace the sequence of events:

1. First, the job successfully set up the Docker executor using a `fitfile/argocli:alpine` image
2. It then configured the Kubernetes credentials by copying a kubeconfig file
3. The job listed existing Argo workflows in the 'testing' namespace, showing various past test runs
4. It submitted a new integration test workflow named 'int-test-n2ks5' from a workflow template called 'all-integration-tests'
5. The critical error occurred during the `argo wait` command, which was waiting for the latest workflow to complete

The specific error we can see is that the workflow failed at "2024-12-02 10:16:38 +0000 UTC". This caused the job to exit with code 1, indicating failure.

Looking at the pattern of previous workflow runs shown in the `argo list` output, we can see that the most recent integration test runs have also been failing:

```sh
all-integration-tests-rfvc5    Failed                22m    10m        0          
all-integration-tests-dwbzc    Failed                57m    10m        0  
```

This suggests there might be an underlying issue with the integration tests themselves rather than the CI job configuration. The consistent 10-minute duration for recent failures could indicate a timeout or a consistent failure point in the test suite.

To help diagnose and fix this issue, I would recommend:

1. Examining the specific workflow logs for 'int-test-n2ks5' to understand the exact failure point
2. Looking for any recent changes that might have impacted the integration tests
3. Investigating why the tests are consistently taking 10 minutes before failing
4. Checking if there have been any changes to the testing environment that might be causing these failures

Would you like me to help analyze any specific aspect of this error in more detail?

### Argo Workflow Failure Analysis

#### Primary Error Category: Runtime Errors

#### Subcategory: Readiness Probe Failures

#### Severity Level: High

#### Impact Scope: System-wide

#### Description

Multiple "Unhealthy" warnings were detected in the logs, indicating that the readiness probes for several pods failed. These probes are used to check if a container is ready to serve traffic. A failure means that the container was not able to start up or is not functioning correctly, leading to the workflow's failure.

#### Technical Details

The logs show the following error messages related to the readiness probes:

- "Readiness probe errored: rpc error: code = Unknown desc = failed to exec in container: container is in CONTAINER_EXITED state"
- "Readiness probe failed:"

These messages indicate that the containers in the affected pods have exited unexpectedly. The readiness probes were unable to execute commands in the containers because they were not running. This can be caused by various issues, such as:

- Errors in the containerized application code, causing it to crash.
- Insufficient resources or limits configured for the container.
- Configuration errors in the readiness probe definition.

Further investigation is needed to pinpoint the exact cause of the container exits.

#### Root Cause

The root cause of the workflow failure is the unexpected termination of containers in several pods, leading to readiness probe failures. The specific reason for the container terminations needs to be determined through further analysis of the application code, resource configurations, and readiness probe definitions.

#### Resolution

To resolve this issue, you can try the following steps:

1. Review the application code for any errors that might be causing the containers to crash.
2. Check the resource configurations (CPU, memory, limits) for the containers and adjust them if necessary.
3. Verify the readiness probe definitions in the pod specifications to ensure they are configured correctly.
4. Monitor the logs and events for the affected pods to gather more information about the container terminations.

#### Related Information

- Kubernetes documentation on readiness probes:
- Troubleshooting guide2 for container health checks:
Let's break down the key issues and potential insights from the logs you've provided.

Primary Categories of Errors

- Runtime Errors: These seem to be the most prominent type of error in the logs. They occur during the execution of the workflows and their associated tasks.
- Configuration Errors: These are evident in the multiple instances where the `FailedToRetrieveImagePullSecret` warning appears. It suggests that there's an issue with how the necessary credentials for pulling container images are configured within the workflows or the underlying Kubernetes environment.

Specific Errors

- Readiness probe errored: This error indicates that the health check mechanism used to determine if a container is ready to serve traffic has failed. The specific cause, "container is in CONTAINER_EXITED state," implies that the container has unexpectedly terminated.
- Readiness probe failed: Similar to the previous error, this signifies a failed health check, but without a clear explanation in the provided context.
- WorkflowNodeFailed: This error points to a failure at a specific node within one of the workflows, again without a detailed cause readily available.

Potential Contributing Factors

- Image Pull Secrets: The repeated warnings about `FailedToRetrieveImagePullSecret` strongly suggest that misconfigured or missing image pull secrets are a significant contributor to the workflow failures.
- Container States: The "CONTAINER_EXITED" state in one of the readiness probe errors indicates that containers are unexpectedly terminating. Further analysis is needed to determine why these containers are exiting.
- Underlying Readiness Checks: The readiness probe failures without specific causes warrant deeper investigation into the custom health checks implemented within the containers. The checks themselves might be encountering errors or have overly strict conditions.

Additional Considerations

- Correlation: While these logs provide a snapshot of individual errors, correlating them with the specific workflows and their execution times can offer a more holistic view of the system's behavior.
- Root Cause: To pinpoint the root causes, you'll need to dive deeper into the failed workflow nodes and the configuration of the image pull secrets.
- Troubleshooting: Consider increasing the log verbosity to capture more detailed information around the time of the errors. This can help in understanding the sequence of events leading to the failures.'

Here are more logs from around the same time:

10:18:02

- The "int-test-n2ks5-start-daemon-2429250715" pod failed the readiness probe and exited.
- The "int-test-n2ks5-start-daemon-4222617225" pod failed to retrieve the image pull secrets. As a result, the pod may not be able to pull the required images successfully.

10:17:59

- The "azurepolicy-k8sazurev3allowedusersgroups-b1f7c99eebc0a61151dc" constraint has 22 violations.
- The "azurepolicy-k8sazurev2containerallowedimag-a87d09dc523488d7ca21" constraint has 49 violations.
- The "azurepolicy-k8sazurev1serviceallowedports-c4777c31b8ca13e01593" constraint has 55 violations.
- The "azurepolicy-k8sazurev3noprivilegeescalatio-09b74a6212aea1db2213" constraint has 3 violations.
- The "azurepolicy-k8sazurev3containerlimits-88f6946679e136aa4af3" constraint has 42 violations.
- The "azurepolicy-k8sazurev2blockautomounttoken-c27791ad309eb684c38a" constraint has 25 violations.
- The "azurepolicy-k8sazurev3hostnetworkingports-cfe33fd329ccbba70cb1" constraint has 2 violations.
- The "azurepolicy-k8sazurev3allowedcapabilities-e7ab9b1a183bec40d35d" constraint has 1 violation.
- The "azurepolicy-k8sazurev3hostfilesystem-5d380c1db8e57af467df" constraint has 8 violations.
- The "azurepolicy-k8sazurev3readonlyrootfilesyst-dc65a4c42d3610d9e476" constraint has 25 violations.

10:17:48

- The "argocd-applicationset-controller-69fccf9f4b-6zpqn" pod failed to retrieve the image pull secrets. As a result, the pod may not be able to pull the required images successfully.
- There were multiple TLS handshake errors from various IP addresses, all with the same error message "EOF". This indicates that the connections were closed unexpectedly.

10:16:51

- The "microsoft-defender-publisher" container reported an error: "Failed to get max memory usage with error: open /sys/fs/cgroup/memory.peak: no such file or directory".

10:16:48

- The "microsoft-defender-low-level-collector" container reported multiple errors:
    - "Failed to get max memory usage with error: open /sys/fs/cgroup/memory.peak: no such file or directory"
    - "Failed to get memory usage with error: open /sys/fs/cgroup/memory.current: no such file or directory"

10:16:45

- The "postgresql" container completed a checkpoint, writing 23 buffers (0.1%) and adding 0 new WAL files.

10:15:32

- The "int-test-n2ks5-verify-reidentify-3141498118" pod failed to retrieve the image pull secrets. The pod may not be able to pull the required images successfully.
- The "int-test-n2ks5-main-3474824669" pod failed to retrieve the image pull secrets. The pod may not be able to pull the required images successfully.

I have not included the events in the response that are similar to the ones shown in the previous response.

```yaml
Name:             int-test-n2ks5-load-data-task-1523472675.180d5483c57d4415                                                                                                                                                                 │
│ Namespace:        testing                                                                                                                                                                                                                   │
│ Labels:           <none>                                                                                                                                                                                                                    │
│ Annotations:      <none>                                                                                                                                                                                                                    │
│ API Version:      v1                                                                                                                                                                                                                        │
│ Count:            5                                                                                                                                                                                                                         │
│ Event Time:       <nil>                                                                                                                                                                                                                     │
│ First Timestamp:  2024-12-02T10:12:36Z                                                                                                                                                                                                      │
│ Involved Object:                                                                                                                                                                                                                            │
│   API Version:       v1                                                                                                                                                                                                                     │
│   Kind:              Pod                                                                                                                                                                                                                    │
│   Name:              int-test-n2ks5-load-data-task-1523472675                                                                                                                                                                               │
│   Namespace:         testing                                                                                                                                                                                                                │
│   Resource Version:  46340686                                                                                                                                                                                                               │
│   UID:               d5acbba9-0fde-4877-a316-38f4a5a6c6d4                                                                                                                                                                                   │
│ Kind:                Event                                                                                                                                                                                                                  │
│ Last Timestamp:      2024-12-02T10:13:09Z                                                                                                                                                                                                   │
│ Message:             Unable to retrieve some image pull secrets (fitfile-image-pull-secret); attempting to pull the image may not succeed.                                                                                                  │
│ Metadata:                                                                                                                                                                                                                                   │
│   Creation Timestamp:  2024-12-02T10:12:36Z                                                                                                                                                                                                 │
│   Resource Version:    46341266                                                                                                                                                                                                             │
│   UID:                 34f7aede-fd67-4fa8-b539-88be87c8206a                                                                                                                                                                                 │
│ Reason:                FailedToRetrieveImagePullSecret                                                                                                                                                                                      │
│ Reporting Component:   kubelet                                                                                                                                                                                                              │
│ Reporting Instance:    aks-workflows-32391530-vmss00001y                                                                                                                                                                                    │
│ Source:                                                                                                                                                                                                                                     │
│   Component:  kubelet                                                                                                                                                                                                                       │
│   Host:       aks-workflows-32391530-vmss00001y                                                                                                                                                                                             │
│ Type:         Warning                                                                                                                                                                                                                       │
│ Events:       <none>
```

```json
{
    "apiVersion": "v1",
    "count": 5,
    "eventTime": null,
    "firstTimestamp": "2024-12-02T10:12:36Z",
    "involvedObject": {
        "apiVersion": "v1",
        "kind": "Pod",
        "name": "int-test-n2ks5-load-data-task-1523472675",
        "namespace": "testing",
        "resourceVersion": "46340686",
        "uid": "d5acbba9-0fde-4877-a316-38f4a5a6c6d4"
    },
    "kind": "Event",
    "lastTimestamp": "2024-12-02T10:13:09Z",
    "message": "Unable to retrieve some image pull secrets (fitfile-image-pull-secret); attempting to pull the image may not succeed.",
    "metadata": {
        "creationTimestamp": "2024-12-02T10:12:36Z",
        "name": "int-test-n2ks5-load-data-task-1523472675.180d5483c57d4415",
        "namespace": "testing",
        "resourceVersion": "46341266",
        "uid": "34f7aede-fd67-4fa8-b539-88be87c8206a"
    },
    "reason": "FailedToRetrieveImagePullSecret",
    "reportingComponent": "kubelet",
    "reportingInstance": "aks-workflows-32391530-vmss00001y",
    "source": {
        "component": "kubelet",
        "host": "aks-workflows-32391530-vmss00001y"
    },
    "type": "Warning"
}
```
