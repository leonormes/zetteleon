---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:42+00:00
title: Network Exploration
---

1. Network Exploration

```bash
# Inside container
ip addr show
ip route show

# On host
ip netns list
ip netns exec container_ns ip addr show
```
