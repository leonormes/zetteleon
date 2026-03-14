---
aliases: [HEAD You said Httpsyoutu.be4HMRFcg6nEY?si=0KwbDeKAT...]
captured: 2026-03-07T16:49:50+00:00 2026-03-07T16:49:50+00:00
created: 2026-03-07T16:49:53+00:00
modified: 2026-03-14T11:10:33+00:00
source: https://gemini.google.com/app/4592469568b8015c
status: processing
tags: [input]
title: HEAD You said Httpsyoutu.be4HMRFcg6nEY-si-0KwbDeKAT...
type: head
---

## Raw Output / Content

<Https://youtu.be/4HMRFcg6nEY?si=0KwbDeKATPo6076>\_

---

This video, titled "Getting to Grips with Kubernetes RBAC" by Liz Rice at GOTO 2019, explains the fundamentals of Kubernetes Role-Based Access Control (RBAC) by comparing it to the more familiar Linux file permission system.

Here is a summary of the key points covered in the talk:

### Linux vs. Kubernetes Permissions

- Linux Model: In Linux, permissions are attached directly to files. Every file has an owner and a group, with simple Read/Write/Execute bits for the owner, group, and everyone else. It is easy to see who can do what by looking at a file's attributes \[[02:03](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=123)\].
- Kubernetes Model: In Kubernetes, everything is a "resource" (e.g., pods, nodes), but resources do not have owners or permission bits attached to them. Instead, permissions are handled through a separate abstraction layer called RBAC \[[06:07](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=367)\].

### Core Components of RBAC

Rice breaks down the three main components required to grant permissions in Kubernetes:

1. Roles: A Role defines a set of rules describing _what_ actions (verbs like `get`, `create`, `delete`) can be performed on _which_ resources. Crucially, a Role does not say _who_ can perform them \[[06:46](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=406)\].
2. Subjects: These are the entities requesting access. They can be Users or Groups (often managed externally, like in LDAP) or Service Accounts (identities for processes running inside pods) \[[09:42](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=582)\].
3. RoleBindings: This is the glue that connects a Role to a Subject. A RoleBinding grants the permissions defined in a Role to a specific user, group, or service account \[[09:25](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=565)\].

### The Risk of Permission Entropy

The speaker highlights a common security issue called "permission entropy," where permissions tend to loosen over time. Administrators often grant broad permissions (like `cluster-admin`) to solve immediate access issues, violating the Principle of Least Privilege \[[15:02](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=902)\].

- Service Account Risks: By default, pods run with a service account token mounted inside them. If an application is compromised (e.g., via a vulnerability in the code), an attacker can use this token to talk to the Kubernetes API.
- Demo: Rice demonstrates this by exploiting a pod running with a "superpower" service account. After gaining shell access, she uses the mounted token to query the API and list sensitive resources, showing how easily a cluster can be compromised if permissions are too loose \[[19:15](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=1155)\].

### Tools for Auditing

- Check Permissions: You can use the native command `kubectl auth can-i <verb> <resource>` to check if a specific user can perform an action (e.g., "Can I create pods?") \[[25:23](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=1523)\].
- Reverse Lookup: To find out _who_ has permission to perform a sensitive action (like deleting nodes), Rice introduces a tool called `kubectl-who-can`. This tool scans RoleBindings and ClusterRoleBindings to list all subjects with a specific permission \[[26:38](http://www.youtube.com/watch?v=4HMRFcg6nEY&t=1598)\].

[https://youtu.be/4HMRFcg6nEY?si=0KwbDeKATPo6076](https://www.google.com/search?q=https://youtu.be/4HMRFcg6nEY%3Fsi%3D0KwbDeKATPo6076) \_
