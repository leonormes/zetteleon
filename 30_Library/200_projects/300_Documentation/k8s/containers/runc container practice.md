---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers]
title: runc container practice
type: curriculum
uid: 
updated: 
version: 1
---

To learn more about Linux containers using runc, here are some practical tutorials you can follow:

## Creating and Running a Container with Runc

1. Prepare a container bundle:
   - Create a directory for your bundle
   - Generate a config.json file using `runc spec`
   - Prepare a root filesystem (you can export one from a Docker image)

2. Run the container:

```bash
runc run mycontainer
```

This will create and start a container based on your bundle configuration[8].

## Exploring Container Lifecycle

1. Create a container:

```bash
runc create mycontainer
```

2. Start the container:

```bash
runc start mycontainer
```

3. List running containers:

```bash
runc list
```

4. Execute commands in the container:

```bash
runc exec mycontainer /bin/sh
```

5. Stop and delete the container:

```bash
runc kill mycontainer
runc delete mycontainer
 ```

These commands allow you to manage the container's lifecycle manually[3][8].

## Customizing Container Configuration

1. Edit the config.json file to modify:
   - Process to run
   - Environment variables
   - Namespaces
   - Resource limits

2. Apply changes by creating a new container with the modified config[1][8].

## Networking and Advanced Features

1. Set up network namespaces
2. Configure cgroups for resource management
3. Implement seccomp profiles for security

These advanced topics require additional setup but provide deeper insights into container isolation and resource control[2][5].

## Practical Exercise: Running Nginx with Runc

1. Create a bundle with Nginx root filesystem
2. Configure the config.json to start Nginx
3. Run the container and access the web server

This exercise demonstrates how to run a real-world application using runc[5][8].

By following these tutorials, you'll gain hands-on experience with runc and develop a deeper understanding of Linux container fundamentals. Remember to consult the official runc documentation for detailed information on each feature and command[8].

How do I configure networking for a container using runc

To configure networking for a container using runc, follow these steps:

## Create a Network Namespace

1. Create a new network namespace for the container:

```bash
ip netns add container_ns
```

## Set Up Virtual Ethernet Pairs

2. Create a virtual ethernet pair:

```bash
ip link add veth0 type veth peer name ceth0
```

3. Move one end of the pair into the container's namespace:

```bash
ip link set ceth0 netns container_ns
```

4. Bring up the host-side interface:

```bash
ip link set veth0 up
```

## Configure Container Network Interface

5. Enter the container's network namespace:

```bash
nsenter --net=/var/run/netns/container_ns
```

6. Configure the container-side interface:

```bash
ip link set lo up
ip link set ceth0 up
ip addr add 172.18.0.10/16 dev ceth0
```

## Bridge Configuration (Optional)

7. Create a bridge on the host:

```bash
ip link add br0 type bridge
ip link set br0 up
```

8. Connect the host-side interface to the bridge:

```bash
ip link set veth0 master br0
```

## Update Runc Configuration

9. Modify the container's config.json to use the created network namespace:

```json
"namespaces": [
  {
	 "type": "network",
	 "path": "/var/run/netns/container_ns"
  }
]
```

By following these steps, you can set up basic networking for a container using runc. This configuration allows the container to have its own network stack while being connected to the host network through a virtual ethernet pair[1][2][3].

Remember to adjust IP addresses and network configurations based on your specific requirements. For more advanced networking setups, you may need to configure routing, NAT, or use other network plugins compatible with runc[5][8].
