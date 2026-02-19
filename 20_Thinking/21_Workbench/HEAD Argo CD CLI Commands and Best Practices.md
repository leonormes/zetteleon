---
title: "Argo CD CLI: Commands and Best Practices"
source: "https://codefresh.io/learn/argo-cd/argo-cd-cli-commands-and-best-practices/"
captured: "2026-02-16T14:40:28+00:00 2026-02-16T14:40:28+00:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
## What Is the Argo CD CLI?

The Argo CD CLI (Command Line Interface) is one of the primary interfaces of [Argo CD](https://codefresh.io/learn/argo-cd/), a declarative, GitOps continuous delivery tool for Kubernetes. The CLI lets you interact with the Argo CD server using a terminal window. Argo CD also offers a user-friendly graphical interface, but the CLI offers faster, more precise control, and is more suited to automation and scripting.

The Argo CD CLI lets you perform a range of operations on your Argo CD server, such as creating and managing applications, checking the status of applications, syncing applications, managing repositories, and providing cluster credentials.

## Installing Argo CD CLI

Before you can start using Argo CD CLI, you need to install it on your system. You can download the latest version of Argo CD CLI from the [official project website](https://argo-cd.readthedocs.io/en/stable/cli_installation/). The CLI is available for multiple platforms, including Windows, Linux, and macOS.

**Linux installation**

After downloading the CLI, you need to move it to your folder for the binary executables. Use the following commands:

**Windows installation**

On Windows, after downloading the CLI, you need to add it to your system’s

PATH

`PATH`. This step allows you to access the CLI from any command prompt.

You can do this by opening the **System Properties**, clicking on the **Advanced** tab, and then on **Environment Variables**. In the **System Variables** section, find the

PATH

`PATH ` variable, select it, and click on Edit. In the **Edit Environment Variable** window, click on **New** and add the path to your CLI.

## Basic Argo CD CLI Commands

Let’s see how to use CLI commands to accomplish common Argo CD tasks.

### argocd login

The ` argocd login` command is the first step in interacting with the Argo CD API. This command allows you to authenticate yourself, setting up a secure connection between your terminal and the Argo CD server. You’ll need to provide your server’s URL and your credentials.

Here are three ways to login to your Argo CD server:

Substitute

< argocd-server \>

`<argocd-server>` with the URL of your server.

### argocd context

The

argocd context

`argocd context` command is used to manage your Argo CD contexts. A context is a configuration that represents a Kubernetes cluster, user, and namespace. You can use this command to switch Argo CD between different contexts, allowing you to manage multiple Kubernetes namespaces and clusters from a single terminal.

Here’s an example of how to use the

argocd context

`argocd context` command:

This switches Argo CD to the context you specify.

### argocd cluster

The

argocd cluster

`argocd cluster` command allows you to add, list, and remove Kubernetes clusters from Argo CD. You can also use it to connect remote clusters to your Argo CD server.

Here’s an example of how to add a new cluster with the

argocd cluster

`argocd cluster` add command:

Remember to replace

< context \>

`<context>` with the name of your Kubernetes context.

You can also use

argocd cluster get

`argocd cluster get` to get cluster information,

argocd cluster list

`argocd cluster list` to list the currently configured clusters, and

argocd cluster rm

`argocd cluster rm` to remove cluster credentials from Argo CD.

### argocd proj

Projects in Argo CD are used to group related applications, allowing you to manage them as a single unit. The

argocd proj

`argocd proj` command allows you to manage these projects.

For example, to create a new project, you can use the

argocd proj

`argocd proj` create command:

You can also use the

argocd proj list

`argocd proj list` command to list all the available projects, and the

argocd proj get

`argocd proj get` command to display the details of a specific project.

### argocd app

The

argocd app

`argocd app` command allows you to manage your applications, from creating and updating applications to syncing and deleting them.

Here’s an example of how to create a new application with the

argocd app create

`argocd app create` command:

Remember to replace

< app-name \>

`<app-name>`,

< repo-url \>

`<repo-url>`,

< path-to-app \>

`<path-to-app>`,

< namespace \>

`<namespace>`, and

< kubernetes-api-server \>

`<kubernetes-api-server>` with your own values.

***Learn more in our detailed guide to*** [***Argo Kubernetes***](https://codefresh.io/learn/argo-cd/argo-kubernetes-making-gitops-work-in-your-kubernetes-clusters/)

## Advanced Argo CD CLI Operations

### argocd app sync

The

argocd app sync

`argocd app sync` command allows you to synchronize an application’s desired state with the actual state in the cluster. This could mean deploying a new version of an application, updating its configuration, or scaling its resources.

To use this command, you need to specify the name of the application you want to synchronize. The syntax is as follows:

argocd app sync \[app name\]

`argocd app sync [app name]`. If you’re synchronizing for the first time, Argo CD will create all the necessary Kubernetes resources. If you’re performing a subsequent sync, Argo CD will apply any changes you’ve made to the application’s configuration.

However, this command won’t return until the sync operation is complete, so it might take some time to execute if your application is large or complex. However, you can use the

\--async

`--async` flag if you want the command to return immediately.

### argocd app history

This command allows you to view the deployment history and details of an application within your Kubernetes cluster. It provides a historical record of changes and deployments for a specific application managed by ArgoCD.

The syntax is

argocd app history \[app name\]

`argocd app history [app name]`. This will display a list of sync operations, each with a timestamp and the commit ID of the configuration that was applied.

By default, the command only shows the last ten sync operations. However, you can use the

\--max

`--max` flag followed by a number to display more entries. For example,

argocd app history \[app name\] \--max 20

`argocd app history [app name] --max 20 ` will show the last twenty sync operations.

### argocd app rollback

Sometimes, you might need to revert your application to a previous state. The

argocd app rollback

`argocd app rollback` command allows you to do this by applying the configuration from a previous sync operation.

You need to specify the name of the application and the ID of the sync operation you want to roll back to. The syntax is

argocd app rollback \[app name\] \[ID\]

`argocd app rollback [app name] [ID]`. The ID can be obtained from the output of the

argocd app history

`argocd app history ` command.

### argocd repo

The

argocd repo

`argocd repo` command provides a range of options for managing repositories. You can add new repositories, list existing ones, and remove repositories that are no longer needed.

To add a new repository, you can use the

argocd repo add

`argocd repo add ` command followed by the URL of the repository. For example,

argocd repo add https://github.com/myorg/myrepo

`argocd repo add https://github.com/myorg/myrepo`. Argo CD will then be able to deploy applications from this repository.

To list all the repositories that Argo CD is currently using, you can use the

argocd repo list

`argocd repo list` command. This will display a list of all repositories, along with their URLs and any labels they have.

### argocd app logs

The

argocd app logs

`argocd app logs` command helps you monitor applications to detect and diagnose problems. It works by displaying the logs of an application’s pods.

You need to specify the name of the application. The syntax is

argocd app logs \[app name\]

`argocd app logs [app name]`. This will display the logs of all pods that belong to the application, which can be useful for troubleshooting issues.

By default, the command shows the logs of all containers in each pod. However, you can use the

\--container

`--container` flag followed by the name of a container to display only its logs. For example,

argocd app logs \[app name\] \--container mycontainer

`argocd app logs [app name] --container mycontainer`.

### argocd app diff

When diagnosing problems or verifying changes, it can be helpful to compare the current state of an application with its desired state. The

argocd app diff

`argocd app diff` command provides a way to do this by displaying the differences between the two states.

You only need to specify the name of the application. The syntax is

argocd app diff \[app name\]

`argocd app diff [app name]`. This will display a list of differences, each with a ‘+’ or ‘-‘ symbol to indicate whether the item is present in the desired state or the current state, respectively. It returns the following exit codes:

2

`2` on general errors,

1

`1` when a diff is found, and

0

`0` when no diff is found

This command only shows differences that Argo CD considers significant. This means it might not show all differences, especially if they’re related to automatically generated or default values.

## Argo CD CLI: Tips and Best Practices

### Secure Your CLI Access

By default, Argo CD is not exposed to the internet. It’s only accessible within your Kubernetes environment, which is a good security measure. However, if you need to access it from outside, you should secure your CLI access.

First, ensure that you’re using HTTPS for communication between the CLI and the server. HTTPS encrypts the data, making it unreadable to anyone who intercepts it. You should also use a strong, unique password for your Argo CD server. If you’re using the CLI on a public computer, make sure to clear your command history to prevent others from seeing your commands.

### Regularly Sync and Prune

Argo CD uses a GitOps approach, which means that your desired state is defined in a Git repository. The Argo CD server continuously compares the desired state with the actual state in your Kubernetes environment. If there’s a discrepancy, it can automatically sync the environment to match the desired state.

However, it’s a good practice to regularly sync and prune your applications manually using the Argo CD CLI. Syncing ensures that your environment matches the desired state, while pruning removes any resources that are not part of the desired state. You can use the argocd app sync command for syncing and the argocd app prune command for pruning.

### Leverage Auto-Sync

You can also leverage the auto-sync feature of Argo CD. Auto-sync automatically synchronizes your environment with the desired state whenever there’s a change in the Git repository. This feature can save time and effort, especially in a large environment with many applications.

To enable auto-sync, you need to use the

argocd app set

`argocd app set` command with the

\--sync-policy

`--sync-policy` flag. You can set the policy to

automated

`automated`, which means that the application will be automatically synchronized whenever there’s a change. You can also set it to ‘none’, which means that the application will not be automatically synchronized.

### Manage Multiple Contexts

Argo CD CLI allows you to manage multiple Argo CD contexts. A context represents a cluster, a user, and a namespace. If you’re managing multiple clusters, you can switch between them using different contexts.

To manage contexts, you need to use the

argocd context

`argocd context` command. You can create a new context using the

argocd context create

`argocd context create` command, switch to a different context using the

argocd context switch

`argocd context switch` command, and delete a context using the

argocd context delete

`argocd context delete` command.

Software teams that adopt GitOps deploy more often, have fewer regressions and recover from failures more quickly. GitOps works, as evidenced by many success stories we at Codefresh have seen first hand. Learn more about GitOps in an in-depth guide by Alexander Matyushentsev, one of the founders of the [Argo project](https://codefresh.io/learn/argo-cd/what-is-the-argo-project-and-why-is-it-transforming-development/). Argo is the world’s fastest growing and most popular open-source GitOps tool in the world today. Users love it, and that is the reason Codefresh has based its enterprise platform on the beloved tool.

Learn to practice GitOps with ArgoCD in the [Manning Report: GitOps with ArgoCD](https://codefresh.io/ebooks/implement-gitops-scale-today/)
