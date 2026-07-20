---
created: 2026-02-19T13:14:59+00:00
hop_level: local
modified: 2026-07-20T16:33:39+00:00
permalink: llmeon/30-library/ops/cmd-net-grpcurl-test
requires_tunnel: false
tags: [api, atomic, grpc, network]
target_service: api
title: cmd-net-grpcurl-test
tool: grpcurl
---

## Test gRPC Service (Grpcurl)

### 🎯 Intent

Interact with gRPC services from the command line to verify availability, list methods, and test specific RPC calls. `grpcurl` is basically `curl` for gRPC.

---

### 🌍 Execution Context

Run from:

- [x] Inside a netshoot pod or container.
- [x] Local machine (if grpcurl installed).

---

### ⚡ Action

```bash
export TARGET_IP=<server_address>

# 1. List Services (using Reflection)
grpcurl $TARGET_IP:<port> list

# 2. Describe a Service
grpcurl $TARGET_IP:<port> describe <service_name>

# 3. Call a Method
grpcurl -d '<json_payload>' $TARGET_IP:<port> <service_name>/<method_name>

# 4. Plaintext (No TLS)
grpcurl -plaintext $TARGET_IP:<port> list
```

#### Placeholders

- `<server_address>`—Hostname or IP of the gRPC server.
- `<port>`—Port (often `443` or `80`).
- `<json_payload>`—Request data in JSON format.
- `<service_name>`—Fully qualified service name.
- `<method_name>`—RPC method name.

---

### ✅ Verification

Expected signal:

- JSON response containing the RPC result.
- Error codes (like `Unimplemented`, `Unavailable`) provide specific failure signatures.

---

### 🔗 Related

- [[pb-netshoot-deployment]]
- [[cmd-k8s-run-netshoot]]
- [[cmd_curl_auth0_token_test]]
- [[sot-network-tools-patterns]]
- [[SoT - The Data-Centric Theory of Networking]]
