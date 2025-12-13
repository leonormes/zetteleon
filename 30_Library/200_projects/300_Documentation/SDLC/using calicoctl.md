---
aliases: []
confidence: 
created: 2025-02-07T12:57:52Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:44Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [calico, cni, networking, workstation]
title: using calicoctl
type:
uid: 
updated: 
version:
---

I have an azure aks and I installed Calico as the cni. how can I install and use the calicoctl tool to examine the networking in my cluster

To install and use the calicoctl tool to examine networking in your AKS cluster with Calico CNI, follow these steps:

## Install Calicoctl

There are several ways to install calicoctl:

1. As a binary:

```bash
curl -L https://github.com/projectcalico/calico/releases/download/v3.29.1/calicoctl-linux-amd64 -o calicoctl
chmod +x ./calicoctl
sudo mv ./calicoctl /usr/local/bin/calicoctl
```

2. As a kubectl plugin:

```bash
curl -L https://github.com/projectcalico/calico/releases/download/v3.29.1/calicoctl-linux-amd64 -o kubectl-calico
chmod +x kubectl-calico
sudo mv kubectl-calico /usr/local/bin/
```

3. As a container:

```bash
docker pull calico/ctl:v3.29.1
```

## Configure Calicoctl

Create a calicoctl configuration file to connect to your AKS cluster:

```bash
cat << EOF > calicoctl.cfg
apiVersion: projectcalico.org/v3
kind: CalicoAPIConfig
metadata:
spec:
  datastoreType: "kubernetes"
  kubeconfig: "/path/to/your/kubeconfig"
EOF
```

Replace "/path/to/your/kubeconfig" with the actual path to your AKS kubeconfig file.

## Use Calicoctl

Now you can use calicoctl to examine networking in your cluster. Here are some useful commands:

1. View Calico nodes:

```bash
calicoctl get nodes
```

2. Check IP pool configuration:

```bash
calicoctl get ippool -o wide
```

3. Examine network policies:

```bash
calicoctl get networkpolicy --all-namespaces
```

4. View BGP configuration:

```bash
calicoctl get bgpconfig
```

5. Check Felix configuration:

```bash
calicoctl get felixconfig
```

6. Examine Calico profiles:

```bash
calicoctl get profile
```

Remember to specify the config file when running calicoctl commands:

```bash
calicoctl --config=calicoctl.cfg <command>
```

Or set the CALICO_DATASTORE_TYPE and KUBECONFIG environment variables:

```bash
export CALICO_DATASTORE_TYPE=kubernetes
export KUBECONFIG=/path/to/your/kubeconfig
```

By using these commands, you can gain insights into your cluster's networking configuration and troubleshoot any issues that may arise[1][3][4].
