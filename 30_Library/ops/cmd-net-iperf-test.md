---
type: atomic_command
tool: iperf3
hop_level: local
target_service: network
requires_tunnel: false
tags: #atomic #network #performance #iperf
---

# Network Performance Test (iperf3)

## 🎯 Intent
Measure the maximum achievable bandwidth between two points (containers, pods, or hosts) to identify network bottlenecks or performance degradation.

---

## 🌍 Execution Context
Run from:
- [x] Inside a netshoot pod or container.
- [x] Local machine (if iperf3 installed).

---

## ⚡ Action

### 1. Start Server (Destination)
```bash
iperf3 -s -p <port>
```

### 2. Start Client (Source)
```bash
export TARGET_IP=<server_ip_or_hostname>

iperf3 -c $TARGET_IP -p <port> -t <duration_seconds>
```

### Placeholders
- `<port>` — Port to listen on/connect to (default is `5201`).
- `<server_ip_or_hostname>` — Address of the iperf server.
- `<duration_seconds>` — How long to run the test (e.g., `10`).

---

## ✅ Verification
Expected signal:
- Detailed output showing intervals, transfer size, and **bandwidth** (e.g., `941 Mbits/sec`).
- Retransmissions (Retr) should be low or zero for healthy links.

---

## 🔗 Related
- [[pb-netshoot-deployment]]
- [[cmd-k8s-run-netshoot]]
