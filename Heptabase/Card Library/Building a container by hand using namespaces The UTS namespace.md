---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:37+00:00
title: Building a container by hand using namespaces The UTS namespace
---

## Building a Container by Hand Using Namespaces The UTS Namespace

This article builds upon my previous articles about namespaces, [The 7 most used Linux namespaces](https://www.redhat.com/sysadmin/7-linux-namespaces) and my series on [Building a Linux container by hand using namespaces](https://www.redhat.com/sysadmin/building-container-namespaces), using [the mount namespace](https://www.redhat.com/sysadmin/mount-namespaces), and using the [PID namespace](https://www.redhat.com/sysadmin/pid-namespace). This article covers the UTS namespace and its relationship to containers.

The casual observer often misunderstands the Unix Timesharing System (UTS) namespace, largely because its name no longer matches its purpose. Despite its name, the UTS namespace actually controls the hostname and the [NIS](https://en.wikipedia.org/wiki/Network_Information_Service) domain. Here's how the man page describes the [UTS namespace](https://man7.org/linux/man-pages/man7/uts_namespaces.7.html):

> These identifiers are set using `sethostname(2)` and `setdomainname(2)`, and can be retrieved using `uname(2)`, `gethostname(2)`, and `getdomainname(2)`. Changes made to these identifiers are visible to all other processes in the same UTS namespace, but are not visible to processes in other UTS namespaces.

This means that some modern tooling (systemd and others) may not cause the changes you expect.

As you can imagine, there might be several use cases where you might want processes to have different hostnames. Webservers, for example, tend to throw a warning if the hostname does not match the SSL certificate they are serving. On the other hand, some processes might attach the hostname to a network process. An incorrect hostname can cause failed or denied connections or myriad other problems.

With all that said, let's get into some examples.

### Explore the UTS Namespace

You can invoke the UTS namespace with:

```sh
unshare --uts /bin/bash
```

However, you might notice that once you are in the new namespace, using `hostnamectl set-hostname` does not change the hostname in the new namespace.

```sh
unshare --uts
# hostname
bastion.stratus.lab
# hostnamectl set-hostname tux
# hostname
bastion.stratus.lab
```

If you open a new shell, though, the hostname has actually changed:

```sh
[user@host ~]$ ssh root@bastion
Last login: Tue Dec 7 08:17:48 2021 from 192.168.99.198
[root@tux ~]# hostname
tux
```

Why is this? Systemd does not execute the `sethostname` system call. Instead, systemd completes the task by connecting to a socket. Since the socket is associated with the old namespace, the old namespace hostname is adjusted but not the new namespace.

#### Using Root Namespaces

In my [mount namespace](https://www.redhat.com/sysadmin/mount-namespaces) article, I write:

> Now that you're inside the new namespace, you might not expect to see any of the original mount points from the host. However, this isn't the case. The reason for this is that systemd defaults to recursively sharing the mount points with all new namespaces.

As it happens, systemd derives a lot of its information from `/run`, which is shared into the namespace I've created here.

In the mount namespace article, I mount `tmpfs` into the new namespace on a directory I don't want to share with the old namespace.

I can disable most of the systemd calls by mounting the new namespace with the following options:

```shell
unshare --mount --uts /bin/bash
```

Then remount `/run`:

```shell
mount -t tmpfs tmpfs /run
```

The whole process looks like this:

```shell
# unshare --fork --mount --uts /bin/bash
# mount -t tmpfs tmpfs /run
# hostnamectl set-hostname bastion.stratus.lab
System has not been booted with systemd as init system (PID 1). Can't operate.
Failed to connect to bus: Host is down
# hostname tux
# hostname
tux
```

I can confirm this by opening a new shell to the box:

```shell
[user@host ~]$ ssh root@bastion
Last login: Tue Dec 7 08:33:04 2021 from 192.168.99.198
[root@bastion ~]# hostname
bastion.stratus.lab
```

I can find the appropriate namespace by using the `lsns` command:

```shell
[root@bastion ~]# lsns |grep uts
4026531838 uts 133 1 root /usr/lib/systemd/systemd --switched-root --system --deserialize 31
4026532250 uts 1 645 root /usr/lib/systemd/systemd-udevd
4026532405 uts 1 743 root /usr/lib/systemd/systemd-logind
4026532479 mnt 2 11507 root unshare --fork --mount --uts /bin/bash
4026532480 uts 2 11507 root unshare --fork --mount --uts /bin/bash
```

I can then enter the namespace with the `nsenter` command:

```shell
[root@bastion ~]# nsenter -t 11507 -a
[root@tux /]#
```

#### Using a User Namespace

In my [user namespace](https://www.redhat.com/sysadmin/building-container-namespaces) article, I mention some additional considerations when creating namespaces as an unprivileged user:

> When you create a new user namespace, your current user will be mapped to the user nobody. This is because, by default, there is no user ID mapping taking place. When no mapping is defined, the namespace simply uses your system's rules to determine how to handle an undefined user.

Refer back to that article for more on user mapping. In this case, I want to have the root user mapped automatically. This way, I have "root" in the new namespace. (Again, see the user namespace article for a discussion of namespaces and permissions).

If I put my combined lessons into practice on a CentOS Stream 9 host, I observe:

```shell
ocp@bastion ~  $ unshare --map-root-user --user --mount --uts --fork /bin/bash
root@bastion ~  $ hostnamectl set-hostname tux
Could not set static hostname: Interactive authentication required.
```

This is because of how `polkit` is configured on the RHEL family of distributions. Other distributions do not necessarily throw this error. Arch Linux (with no special `polkit` configuration), for example, still allows the container to change the hostname. Therefore regardless of your distribution, it is still good security practice to remount `/run`.

It's important to note that the output of `lsns` might be easier to read by using `--fork` when creating namespaces.

Here's how it looks without the `--fork` flag:

```shell
[root@bastion ~]# lsns |grep uts
4026531838 uts 135 1 root /usr/lib/systemd/systemd --switched-root --system --deserialize 31
4026532250 uts 1 645 root /usr/lib/systemd/systemd-udevd
4026532405 uts 1 743 root /usr/lib/systemd/systemd-logind
4026532414 uts 1 11962 ocp /bin/bash
```

And with the `--fork` flag:

```shell
[root@bastion ~]# lsns |grep uts
4026531838 uts 134 1 root /usr/lib/systemd/systemd --switched-root --system --deserialize 31
4026532250 uts 1 645 root /usr/lib/systemd/systemd-udevd
4026532405 uts 1 743 root /usr/lib/systemd/systemd-logind
4026532412 user 2 11939 ocp unshare --map-root-user --user --mount --uts --fork /bin/bash
```

While `--fork` is not strictly necessary in this scenario, it may be useful or even required if a new PID namespace is required (see my [PID namespace](https://www.redhat.com/sysadmin/pid-namespace) article for more information).

### Wrapping up

The UTS namespace is not the most complicated Linux namespace. It is, however, quite useful, especially in the context of containers.

To make the most of the UTS namespace, combine it with the mount namespace, at a minimum, when using the root namespace and mount and user namespaces when spawning from an unprivileged user.

_\[Download the [intermediate Linux cheat sheet](https://developers.redhat.com/cheat-sheets/intermediate-linux-cheat-sheet?intcmp=701f20000012ngPAAQ) to keep key commands at your fingertips. \]_

In my next article, I'll discuss the net namespace and how to use it to enable namespaces to have their own IP and port space.
