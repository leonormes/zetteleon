---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:42+00:00
title: Mount (mnt namespace)
---

## Mount (mnt namespace)

The mount namespace is used to isolate mount points such that processes in different namespaces cannot view each others' files. If you are familiar with the [chroot](https://www.redhat.com/en/blog/wiki.archlinux.org/index.php/chroot) command, it functions similarly.

In our analogy, I am going to deviate a little from the apartment. Let's assume two people get married. In this scenario, there are a bunch of things that usually end up being shared. You probably put their name on the address listing, you might have both names on the bills, have both names on any car ownerships, and add them to your credit cards, etc. In this sense, you are sharing the same mount point with the other person. However, their credit may be separate, they might pay their own taxes, and so on. Their Social Insurance number (Social Security number for our friends in the USA) stays distinct from yours and vice versa. Therefore, while your partner may see a similar view of the financial situation, it will not be exactly the same. They have no real ability to see any financial matters that are legally your sole possession.

The same is true for filesystem mount points. By default, different mount namespaces cannot view the other's content. As far as the namespace is concerned, it is at the root of the file system, and nothing else exists. However, you can mount portions of an underlying file system into the mount namespace, thereby allowing it to see additional information.
