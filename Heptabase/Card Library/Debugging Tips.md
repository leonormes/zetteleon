### Debugging Tips

#### Network Issues

- Check interface status: `ip link show`

- Verify IP addresses: `ip addr show`

- Test connectivity: `ping 172.16.0.1`

- Check routing: `ip route show`

#### Resource Limits

- Check memory usage: `cat /sys/fs/cgroup/memory/container/memory.usage_in_bytes`

- Monitor CPU: `cat /sys/fs/cgroup/cpu/container/cpu.stat`

#### Process Issues

- Check process tree: `pstree`

- Look for zombie processes: `ps aux | grep Z`

- Check mount points: `mount`