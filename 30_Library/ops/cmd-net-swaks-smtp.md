---
created: 2026-02-19T13:15:17+00:00
hop_level: local
modified: 2026-07-04T10:50:43+00:00
permalink: llmeon/30-library/ops/cmd-net-swaks-smtp
requires_tunnel: false
tags: [atomic, mail, network, smtp]
target_service: mail
title: cmd-net-swaks-smtp
tool: swaks
type: atomic_command
---

## Test SMTP Delivery (Swaks)

### 🎯 Intent

Verify SMTP server connectivity and mail delivery capabilities from the command line. `swaks` (Swiss Army Knife for SMTP) handles everything from basic connectivity to complex authentication and TLS handshakes.

---

### 🌍 Execution Context

Run from:

- [x] Inside a netshoot pod or container.
- [x] Local machine (if swaks installed).

---

### ⚡ Action

```bash
export TARGET_IP=<smtp_server>

# 1. Basic Delivery Test
swaks --to <recipient_email> --server $TARGET_IP

# 2. Authenticated SMTP with TLS
swaks --to <recipient_email> \
  --from <sender_email> \
  --server $TARGET_IP \
  --port 587 \
  --auth-user <username> \
  --auth-password <password> \
  --tls

# 3. Debugging Connection Handshake
swaks --to <recipient_email> --server $TARGET_IP -tlsc
```

#### Placeholders

- `<recipient_email>`—e.g., `user@example.com`.
- `<sender_email>`—e.g., `test@fitfile.com`.
- `<smtp_server>`—Hostname or IP of the mail server.
- `<username>` / `<password>`—SMTP credentials.

---

### ✅ Verification

Expected signal:

- `=== 250 OK` indicates the server accepted the message for delivery.
- `* SMTP SHUTDOWN *` should follow a successful session.
- Error codes (like `5xx` or `4xx`) provide specific failure reasons (Auth, Relay Access Denied, etc.).

---

### 🔗 Related

- [[pb-netshoot-deployment]]
- [[cmd-k8s-run-netshoot]]
