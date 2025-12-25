---
aliases: []
AoL: Work
confidence: null
created: 2025-12-05T21:02:41Z
epistemic: null
last_reviewed: null
modified: 2025-12-23T17:53:54Z
purpose: null
review_interval: null
see_also: []
source_of_truth: []
status: processing
tags: [state/head, topic/networking, topic/sde, type/design]
title: HEAD - SDE Networking Responsibility Boundaries
type: head
uid: null
up: '[[HEAD - SDE Architecture]]'
updated: null
---

> [!abstract] The Spark
> I realized I don't know where our responsibility ends and the Data Provider's begins. Since the connection is currently *only* for our application, I assume we own the whole stack, but this implies we are effectively the "Networking Layer." Is this sustainable?

## 🧠 My Current Model (The Implicit Assumption)

- **Observation:** There is a route + resources enabling the connection between SDE and Data Provider.
- **Assumption:** Because we consume the data, we must manage the pipes.
- **Fear:** We are responsible for security, uptime, and maintenance of the *entire* transit layer.

## ⚔️ The Tension (The Boundary Problem)

- **The Conflict:** If we are the "Networking Layer," we need network engineers. We are SDE engineers.
- **The Risk:** If the network goes down, is it an *Infrastructure Incident* (Platform Team) or an *Application Incident* (Us)? Currently, it defaults to Us.
- **The Pattern:** This looks like the "Shared Responsibility Model" (like AWS vs Customer), but we haven't defined the line.

## 🧪 Next Test (The Boundary Audit)

- [ ] **Action:** Check the Terraform State. Do we *provision* the Peering/VPN Gateway, or do we just *point* to it?
- [ ] **Definition:** Draft a "Demarcation Point" diagram. Where does the handshake happen?
- [ ] **Experiment:** If the connection is severed, can *we* fix it with our permissions? If No, we are not responsible.
