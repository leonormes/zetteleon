---
aliases: ["C10K problem", "maximum sockets", "socket limits"]
confidence: 0.8
created: 2025-10-31T13:43:00Z
epistemic: fact
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:58Z
purpose: "Explain factors limiting maximum concurrent sockets on servers."
review_interval: 90
see_also: ["Event-Driven Socket Handling with epoll and kqueue.md"]
source_of_truth: []
status: seedling
tags: [networking, performance, scalability, server, socket]
title: Server Socket Scalability Limits
type: concept
uid: 2025-10-31T13:43:00Z
updated: 2025-10-31T13:43:00Z
---

## Server Socket Scalability Limits

**Summary:** The maximum number of concurrent sockets a server can handle depends on OS limits, hardware resources, and kernel tuning, ranging from tens of thousands to millions.

**Details:**

Multiple factors constrain socket scalability:

**OS-level limits:**
- **File descriptor limits**: Each socket consumes one file descriptor
  - Per-process limit (ulimit -n): Often 1024 by default, can be increased
  - System-wide limit: Kernel parameter (e.g., /proc/sys/fs/file-max on Linux)
- **Port exhaustion**: Client-side connections limited by available ephemeral ports (~28,000-64,000)

**Hardware constraints:**
- **Memory**: Each socket requires kernel memory for buffers
  - Typical socket overhead: 4-8 KB per connection
  - 1 million sockets ≈ 4-8 GB minimum RAM requirement
- **CPU**: Context switching and event processing overhead
- **Network bandwidth**: Physical network capacity limits

**Kernel tuning parameters:**
- TCP buffer sizes (net.ipv4.tcp_rmem, tcp_wmem)
- Connection backlog (net.core.somaxconn)
- TIME_WAIT socket reuse (net.ipv4.tcp_tw_reuse)

**Typical capacity ranges:**

- **Small server** (default config): 10,000 - 50,000 concurrent sockets
- **Medium server** (tuned): 50,000 - 200,000 concurrent sockets  
- **Large production server** (heavily optimized): 500,000 - 2,000,000+ concurrent sockets

**Historical context:**

The "C10K problem" (handling 10,000 concurrent connections) was considered difficult in the 1990s. Modern servers routinely handle millions of connections using event-driven architectures like epoll/kqueue and careful kernel tuning.

**Practical considerations:**

Socket limits are rarely the bottleneck for most applications. Application logic, database connections, and business requirements usually impose lower practical limits.
