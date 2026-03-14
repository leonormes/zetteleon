---
created: 2026-03-14T09:50:11+00:00
modified: 2026-03-14T11:09:31+00:00
tags: [articles]
title: GitHub - sigridjinethk8s-hard-way Building a Kubernetes Cluster From Scratch In Your Local Macbook Pro
---

## GitHub - sigridjineth/k8s-hard-way: Building a Kubernetes Cluster From Scratch In Your Local Macbook Pro

![rw-book-cover](https://opengraph.githubassets.com/209de4376943541b0a7ebf1e65db3f437bbac58dc8bae45ce1335f4277837d54/sigridjineth/k8s-hard-way)

### Metadata

- Author: [[https://github.com/sigridjineth/]]
- Full Title: GitHub - sigridjineth/k8s-hard-way: Building a Kubernetes Cluster From Scratch In Your Local Macbook Pro
- Category: articles
- Summary: This project teaches you how to build a Kubernetes cluster from scratch on your Mac using VirtualBox and Vagrant. It helps you learn how Kubernetes components work and communicate without hiding complexity. The tutorial includes setup steps, architecture details, and troubleshooting tips for a hands-on learning experience.
- URL: <https://github.com/sigridjineth/k8s-hard-way>

### Full Document

#### sigridjineth/k8s-hard-way

main

Go to file

Code

Open more actions menu

#### Kubernetes The Hard Way (Local Edition)

A hands-on tutorial for setting up Kubernetes from scratch on your local machine using VirtualBox and Vagrant. This repository is designed for educational purposes to help you understand how all the pieces of Kubernetes fit together.

##### Why "The Hard Way"?

When you use managed Kubernetes services (EKS, GKE, AKS) or automation tools (kubeadm, kubespray), the complexity is hidden from you. While this is great for productivity, it becomes a problem when things break in production.

By building a cluster manually, you will:

- Understand how each component authenticates and communicates
- Learn the role of every certificate in the PKI infrastructure
- See exactly how the control plane manages cluster state
- Gain debugging skills that are invaluable in production

##### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Host Machine (macOS)                            │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   jumpbox   │  │   server    │  │   node-0    │  │   node-1    │   │
│  │ 192.168.10  │  │ 192.168.10  │  │ 192.168.10  │  │ 192.168.10  │   │
│  │    .10      │  │    .100     │  │    .101     │  │    .102     │   │
│  │             │  │             │  │             │  │             │   │
│  │  Admin Host │  │Control Plane│  │   Worker    │  │   Worker    │   │
│  │  - cfssl    │  │  - etcd     │  │ - kubelet   │  │ - kubelet   │   │
│  │  - kubectl  │  │  - apiserver│  │ - kube-proxy│  │ - kube-proxy│   │
│  │             │  │  - scheduler│  │ - containerd│  │ - containerd│   │
│  │             │  │  - ctrl-mgr │  │             │  │             │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                                         │
│                    Private Network: 192.168.10.0/24                     │
└─────────────────────────────────────────────────────────────────────────┘

Pod Network CIDRs:
  - node-0: 10.200.0.0/24
  - node-1: 10.200.1.0/24

Service CIDR: 10.32.0.0/24

```

##### Components

| Component | Version | Description |
| --- | --- | --- |
| Kubernetes | v1.32.0 | Container orchestration platform |
| etcd | v3.5.17 | Distributed key-value store for cluster state |
| containerd | v2.0.1 | Container runtime |
| runc | v1.2.4 | OCI container runtime |
| CNI Plugins | v1.6.2 | Container networking |
| cfssl | v1.6.5 | TLS certificate generation |

##### Prerequisites

###### Hardware Requirements

- RAM: 16GB minimum (8GB might work with reduced VM memory)
- Disk: 20GB free space
- CPU: 4+ cores recommended

###### Software Requirements

- macOS (Intel or Apple Silicon)
- [VirtualBox](https://www.virtualbox.org/) 7.0+
- [Vagrant](https://www.vagrantup.com/) 2.4+

###### Knowledge Requirements

- Basic Linux command line familiarity
- Understanding of networking (IP addresses, subnets, routing)
- Basic knowledge of TLS/SSL certificates
- Familiarity with Kubernetes concepts (pods, services, deployments)

##### Installation

###### 1. Install Prerequisites

```
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install VirtualBox
brew install --cask virtualbox

# Install Vagrant
brew install --cask vagrant

# Verify installations
VBoxManage --version
vagrant --version
```

> Note for macOS: You may need to approve VirtualBox kernel extensions in System Settings > Privacy & Security.

###### 2. Clone and Start

```
# Clone this repository
git clone <repository-url>
cd kubernetes-the-hard-way

# Start the VMs
vagrant up

# Verify VMs are running
vagrant status
```

##### Tutorial Parts

This tutorial is divided into four parts. Complete them in order.

| Part | Title | Description | Time |
| --- | --- | --- | --- |
| [Part 1](https://github.com/sigridjineth/k8s-hard-way/blob/main/docs/part-1-overview-prerequisites.md) | Overview & Prerequisites | Set up VMs, networking, SSH keys, download binaries | 30 min |
| [Part 2](https://github.com/sigridjineth/k8s-hard-way/blob/main/docs/part-2-etcd-control-plane.md) | etcd & Control Plane | Generate certificates, configure etcd, set up API server | 45 min |
| [Part 3](https://github.com/sigridjineth/k8s-hard-way/blob/main/docs/part-3-worker-nodes-networking.md) | Worker Nodes & Networking | Configure containerd, kubelet, kube-proxy, CNI | 45 min |
| [Part 4](https://github.com/sigridjineth/k8s-hard-way/blob/main/docs/part-4-smoke-test.md) | Smoke Test & Conclusion | Deploy applications, verify networking, cleanup | 20 min |

###### Blog Posts

For a narrative walkthrough with detailed explanations, check out the accompanying blog series:

- Parts 1 & 2: [Building a Kubernetes Cluster From Scratch: Overview and Prerequisites](https://sigridjin.medium.com/building-a-kubernetes-cluster-from-scratch-overview-and-prerequisites-498ed989fd45)
- Parts 3 & 4: [Building a Kubernetes Cluster From Scratch: Setting Up etcd and Control Plane](https://sigridjin.medium.com/building-a-kubernetes-cluster-from-scratch-setting-up-etcd-and-control-plane-0719698f0182?source=friends_link&sk=00c4966925330347f920f815e4ed29bc)

##### Quick Start

If you want to run everything automatically:

```
# Start VMs
vagrant up

# SSH into jumpbox
vagrant ssh jumpbox

# From jumpbox, follow the tutorial parts
```

##### File Structure

```
kubernetes-the-hard-way/
├── README.md                 # This file
├── Vagrantfile              # VM definitions
├── init.sh                  # VM provisioning script
├── machines.txt             # Machine configuration
└── docs/
    ├── part-1-overview-prerequisites.md
    ├── part-2-etcd-control-plane.md
    ├── part-3-worker-nodes-networking.md
    └── part-4-smoke-test.md

```

##### Network Configuration

| Machine | IP Address | Role |
| --- | --- | --- |
| jumpbox | 192.168.10.10 | Administration host |
| server | 192.168.10.100 | Control plane |
| node-0 | 192.168.10.101 | Worker node |
| node-1 | 192.168.10.102 | Worker node |

##### Troubleshooting

###### VirtualBox Issues on Apple Silicon

VirtualBox on Apple Silicon (M1/M2/M3) is still maturing. If you encounter issues:

1. Ensure you're using VirtualBox 7.0+
2. The Vagrantfile uses `bento/ubuntu-24.04` which supports ARM64
3. Check System Settings > Privacy & Security for any blocked extensions

###### VM Won't Start

```
# Check VirtualBox kernel modules
sudo kextload -b org.virtualbox.kext.VBoxDrv

# Restart VirtualBox services
sudo /Library/Application\ Support/VirtualBox/LaunchDaemons/VirtualBoxStartup.sh restart
```

###### SSH Connection Refused

```
# Check VM status
vagrant status

# Restart the VM
vagrant reload <vm-name>

# Check SSH config
vagrant ssh-config <vm-name>
```

###### Certificate Errors

Most certificate errors come from:

- Typos in hostnames or IP addresses
- Wrong certificate used for wrong component
- Certificate not signed by the correct CA

Use these commands to debug:

```
# View certificate details
openssl x509 -in cert.pem -text -noout

# Verify certificate chain
openssl verify -CAfile ca.pem cert.pem

# Test TLS connection
openssl s_client -connect server:6443 -CAfile ca.pem
```

##### Cleanup

To destroy all VMs and start fresh:

```
vagrant destroy -f
```

To remove downloaded box images:

```
vagrant box remove bento/ubuntu-24.04
```

##### References

- [Kubernetes The Hard Way (Original by Kelsey Hightower)](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [etcd Documentation](https://etcd.io/docs/)
- [containerd Documentation](https://containerd.io/docs/)

##### License

This project is for educational purposes. Feel free to use, modify, and distribute.

##### Contributing

Contributions are welcome! Please open an issue or pull request for any improvements.
