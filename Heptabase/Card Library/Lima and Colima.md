---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:40+00:00
title: Lima and Colima
---

## Lima and Colima

Lima (Linux Machines) is a tool that allows you to run Linux virtual machines on macOS with ease. It acts as a bridge between macOS and Linux, providing a seamless way to run Linux environments on your Mac. Here's how the various components fit together:

### Lima and macOS

Lima creates and manages Linux virtual machines on macOS using virtualization technology. It handles the complexities of setting up and running these VMs, providing an easy-to-use interface for users\[1\]. Lima automates tasks such as file sharing between the host (macOS) and guest (Linux VM), as well as port forwarding, making it simple to interact with the Linux environment from your Mac\[2\].

### Colima and Lima

Colima is a higher-level tool that uses Lima under the hood. It's specifically designed to provide a Docker-compatible environment on macOS\[7\]. Colima sets up a Lima VM preconfigured with Docker, allowing you to run Docker commands on your Mac as if you were running them directly on a Linux machine\[4\].

### What Lima Provides

Lima offers several key features:

1. Automatic file sharing: Your home directory is typically mounted read-only in the VM\[2\].
2. Port forwarding: Allows you to access services running in the VM from your Mac\[2\].
3. Containerd and nerdctl: These are pre-configured in Lima VMs, providing container functionality similar to Docker\[11\].
4. Multiple VM support: You can run different Linux distributions simultaneously\[2\].

### Using Lima for Learning

By using Lima (via Colima) to run an Ubuntu VM, you've created a sandbox environment where you can safely experiment with Linux commands and features, such as network namespaces (`ip netns`), without affecting your macOS system. This setup allows you to learn and practice Linux-specific concepts and tools that aren't natively available on macOS.

### Tooling Benefits

1. Docker compatibility: Colima provides a Docker-compatible environment, allowing you to use Docker commands on macOS\[4\].
2. Containerd and nerdctl: These offer alternative ways to work with containers, providing more flexibility than Docker alone\[11\].
3. Kubernetes support: Some Lima configurations (like those provided by Colima) can include Kubernetes, allowing you to experiment with container orchestration\[4\].

In essence, Lima (and by extension, Colima) gives you a convenient way to run Linux environments on your Mac, bridging the gap between macOS and Linux. This setup is particularly useful for developers and system administrators who need to work with Linux-specific tools and environments while using a Mac as their primary machine.
