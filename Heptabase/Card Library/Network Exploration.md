1. **Network Exploration**

```bash
# Inside container
ip addr show
ip route show

# On host
ip netns list
ip netns exec container_ns ip addr show
```