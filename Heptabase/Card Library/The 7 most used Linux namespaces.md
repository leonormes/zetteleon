
I want to provide some examples to clarify the technical definitions around *namespaces*. [Wikipedia](https://en.wikipedia.org/wiki/Linux_namespaces) has the following definition:

> Namespaces are a feature of the Linux kernel that partitions kernel resources such that one set of processes sees one set of resources and another set of processes sees a different set of resources. The feature works by having the same namespace for a group of resources and processes, but those namespaces refer to distinct resources.

This definition is quite a bit to digest for some folks, so perhaps this analogy will help. Consider my apartment building. It's technically two distinct buildings with their own entrances. However, the parking garage, gym, pool, and common rooms are shared. The buildings have their own names, **City Place** and **City Place 2**. They have their own street addresses, floors, and elevators. Yet, they are attached to the same physical complex.

The physical complex is the same idea as a computer. Two namespaces (or more) can reside on the same physical computer, and much like the apartment building, namespaces can either share access to certain resources or have exclusive access.

There are seven common types of namespaces in wide use today. Using the apartment as our guide, let's walk through a summary of what each type does. Below is a brief overview of each namespace type. In subsequent articles, we will show how each namespace works by example.

[Process Isolation (PID namespace).md](Process%20Isolation%20(PID%20namespace).md)

***\[ Learn more about [PID namespaces](https://www.redhat.com/sysadmin/pid-namespace). \]***

[Network Interfaces (net namespace).md](Network%20Interfaces%20(net%20namespace).md)

***\[ Learn more about [net namespaces](https://www.redhat.com/sysadmin/net-namespaces). \]***

[Unix Timesharing System (uts namespace).md](Unix%20Timesharing%20System%20(uts%20namespace).md)

***\[ Learn more about [uts namespaces](https://www.redhat.com/sysadmin/uts-namespace). \]***

[User Namespace.md](User%20Namespace.md)

***\[ Learn more about [user namespaces](https://www.redhat.com/sysadmin/building-container-namespaces). \]***

[Mount (mnt namespace).md](Mount%20(mnt%20namespace).md)

***\[ Learn more about [mnt namespaces](https://www.redhat.com/sysadmin/mount-namespaces). \]***

[Interprocess Communication (IPC).md](Interprocess%20Communication%20(IPC).md)

[Cgroups.md](Cgroups.md)

***\[ Get this free ebook: [Managing your Kubernetes clusters for dummies](https://www.redhat.com/en/resources/managing-kubernetes-clusters-dummies-ebook?intcmp=7013a0000026EKuAAM). \]***

## Wrapping up

So there you have a brief overview of what the seven most used namespaces are. Hopefully, my analogy was useful and clear. In the next couple of articles, I explore some of these namespaces and how they are created by hand. This will give you a better understanding of the utility of namespaces. In the final article, I tie it all together, including the use of cgroups to explain how containers function "under the hood."