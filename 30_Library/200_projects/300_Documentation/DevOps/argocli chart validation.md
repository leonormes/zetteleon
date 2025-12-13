---
aliases: []
confidence: 
created: 2025-03-05T20:32:59Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy, gitops]
title: argocli chart validation
type: 
uid: 
updated: 
version: 
---

The Argo CD CLI provides commands that allow you to render and inspect your Kubernetes manifests locally, effectively validating what Argo CD would deploy. This is primarily achieved using the argocd app manifest command.

argocd app manifest command:

This command renders the Kubernetes manifests from your application source definition (like Helm charts, Kustomize, or plain YAML) as Argo CD would. You can use this to:

 - Preview rendered manifests: See the final Kubernetes YAML that Argo CD will generate and apply to your cluster.
 - Debug configuration issues: Identify errors in your Helm charts, value overrides, or other configurations before actual deployment.
 - Validate against Kubernetes API: Although argocli doesn't directly validate against a live Kubernetes API server, reviewing the rendered manifests helps you ensure they are syntactically correct and semantically valid based on your understanding of Kubernetes.
Example Usage:
Assuming you have an Argo CD application definition in a YAML file (e.g., app.yaml) or are using a directory with application resources:
 - For a Helm chart application:
   argocd app manifest --app-name my-app --helm-chart path/to/your/helm-chart --helm-values path/to/values.yaml

   Replace my-app, path/to/your/helm-chart, and path/to/values.yaml with your actual application name, Helm chart path, and values file path.

 - For a Kustomize application:
   argocd app manifest --app-name my-kustomize-app --kustomize path/to/your/kustomize-dir

   Replace my-kustomize-app and path/to/your/kustomize-dir with your application name and Kustomize directory path.

 - For a directory of plain YAML manifests:
   argocd app manifest --app-name my-yaml-app --directory path/to/your/yaml-dir

   Replace my-yaml-app and path/to/your/yaml-dir with your application name and YAML directory path.

Output:

The command will output the rendered Kubernetes manifests to your terminal. You can then review these manifests to ensure they are as expected. You can also save the output to a file for further inspection:

ArgoCD app manifest ... > rendered-manifests.yaml

Benefits of Using argocli for Local Validation

Using argocli for local validation offers several benefits during your development process:

 - Early Error Detection: You can catch configuration errors, template issues, and value overrides problems early in the development cycle, before deploying to a live cluster. This saves time and reduces the risk of deployment failures.
 - Faster Feedback Loop: Validating locally with argocli is much faster than deploying to a cluster and waiting for Argo CD to synchronize and potentially fail. This rapid feedback loop accelerates development and debugging.
 - Reduced Cluster Load: By validating locally, you avoid unnecessary deployments to your Argo CD managed cluster, reducing load and potential instability from misconfigurations.
 - Offline Validation: You can validate your configurations even without being connected to your Argo CD server or Kubernetes cluster, making it convenient for development in various environments.
 - Confidence in Deployments: Reviewing the rendered manifests gives you confidence that Argo CD will deploy the intended resources, reducing surprises and unexpected outcomes in your live environments.
 - GitOps Best Practices: Using argocli to validate changes before committing them to your Git repository aligns with GitOps principles by ensuring that what's in Git is truly what you intend to deploy.
Limitations
While argocli app manifest is valuable for validation, it's important to note its limitations:
 - No Live Kubernetes API Validation: argocli does not fully validate against a live Kubernetes API server. It mainly renders manifests. Therefore, it won't catch issues that are only apparent when applying manifests to a specific cluster version or with specific cluster configurations (like admission controllers).
 - Limited Dry-Run: It's not a full "dry-run" deployment. It only renders the manifests. It doesn't simulate the actual application of resources or check for resource conflicts in the cluster.
 - Context Differences: There might be subtle differences between the local rendering environment and the Argo CD server environment (e.g., slight differences in Helm versions or available plugins). However, for most common use cases, argocli app manifest provides a very accurate preview.
Conclusion
In conclusion, using argocli app manifest is a highly beneficial practice for validating your Helm charts and deployments before they are managed by Argo CD. It allows for early error detection, faster feedback, and increased confidence in your deployments, making your development workflow more efficient and reliable. While it has some limitations, the benefits of local validation with argocli significantly outweigh the drawbacks for most development scenarios.
For more detailed information and options for the argocd app manifest command, you can refer to the official Argo CD documentation or use argocd app manifest --help in your terminal.
 - Argo CD CLI Documentation

---

created: 2025-03-05T08:53:35
source: <https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_manifests/>
author:
---

## Argocd App Manifests Command Reference - Argo CD

Clipped from: <https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_manifests/>

[](https://github.com/argoproj/argo-cd/edit/master/docs/user-guide/commands/argocd_app_manifests.md "Edit this page")

## `argocd app manifests` Command Reference[¶](#argocd-app-manifests-command-reference "Permanent link")

### Argocd App manifests[¶](#argocd-app-manifests "Permanent link")

Print manifests of an application

```sh
argocd app manifests APPNAME [flags]

```

#### Examples[¶](#examples "Permanent link")

```sh
  # Get manifests for an application
argocd app manifests my-app

  # Get manifests for an application at a specific revision
argocd app manifests my-app --revision 0.0.1

  # Get manifests for a multi-source application at specific revisions for specific sources
argocd app manifests my-app --revisions 0.0.1 --source-names src-base --revisions 0.0.2 --source-names src-values

  # Get manifests for a multi-source application at specific revisions for specific sources
argocd app manifests my-app --revisions 0.0.1 --source-positions 1 --revisions 0.0.2 --source-positions 2
```

#### Options[¶](#options "Permanent link")

```sh
  -h, --help                          help for manifests
      --local string                  If set, show locally-generated manifests. Value is the absolute path to app manifests within the manifest repo. Example: '/home/username/apps/env/app-1'.
      --local-repo-root string        Path to the local repository root. Used together with --local allows setting the repository root. Example: '/home/username/apps'. (default ".")
      --revision string               Show manifests at a specific revision
      --revisions stringArray         Show manifests at specific revisions for the source at position in source-positions
      --source string                 Source of manifests. One of: live|git (default "git")
      --source-names stringArray      List of source names. Default is an empty array.
      --source-positions int64Slice   List of source positions. Default is empty array. Counting start at 1. (default [])

```

#### Options Inherited from Parent commands[¶](#options-inherited-from-parent-commands "Permanent link")

```sh
      --argocd-context string           The name of the Argo-CD server context to use
      --auth-token string               Authentication token; set this or the ARGOCD_AUTH_TOKEN environment variable
      --client-crt string               Client certificate file
      --client-crt-key string           Client certificate key file
      --config string                   Path to Argo CD config (default "/home/user/.config/argocd/config")
      --controller-name string          Name of the Argo CD Application controller; set this or the ARGOCD_APPLICATION_CONTROLLER_NAME environment variable when the controller's name label differs from the default, for example when installing via the Helm chart (default "argocd-application-controller")
      --core                            If set to true then CLI talks directly to Kubernetes instead of talking to Argo CD API server
      --grpc-web                        Enables gRPC-web protocol. Useful if Argo CD server is behind proxy which does not support HTTP2.
      --grpc-web-root-path string       Enables gRPC-web protocol. Useful if Argo CD server is behind proxy which does not support HTTP2. Set web root.
  -H, --header strings                  Sets additional header to all requests made by Argo CD CLI. (Can be repeated multiple times to add multiple headers, also supports comma separated headers)
      --http-retry-max int              Maximum number of retries to establish http connection to Argo CD server
      --insecure                        Skip server certificate and domain verification
      --kube-context string             Directs the command to the given kube-context
      --logformat string                Set the logging format. One of: text|json (default "text")
      --loglevel string                 Set the logging level. One of: debug|info|warn|error (default "info")
      --plaintext                       Disable TLS
      --port-forward                    Connect to a random argocd-server port using port forwarding
      --port-forward-namespace string   Namespace name which should be used for port forwarding
      --prompts-enabled                 Force optional interactive prompts to be enabled or disabled, overriding local configuration. If not specified, the local configuration value will be used, which is false by default.
      --redis-compress string           Enable this if the application controller is configured with redis compression enabled. (possible values: gzip, none) (default "gzip")
      --redis-haproxy-name string       Name of the Redis HA Proxy; set this or the ARGOCD_REDIS_HAPROXY_NAME environment variable when the HA Proxy's name label differs from the default, for example when installing via the Helm chart (default "argocd-redis-ha-haproxy")
      --redis-name string               Name of the Redis deployment; set this or the ARGOCD_REDIS_NAME environment variable when the Redis's name label differs from the default, for example when installing via the Helm chart (default "argocd-redis")
      --repo-server-name string         Name of the Argo CD Repo server; set this or the ARGOCD_REPO_SERVER_NAME environment variable when the server's name label differs from the default, for example when installing via the Helm chart (default "argocd-repo-server")
      --server string                   Argo CD server address
      --server-crt string               Server certificate file
      --server-name string              Name of the Argo CD API server; set this or the ARGOCD_SERVER_NAME environment variable when the server's name label differs from the default, for example when installing via the Helm chart (default "argocd-server")
```

#### SEE ALSO[¶](#see-also "Permanent link")

-   [argocd app](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_manifests/../argocd_app/) \- Manage applications
