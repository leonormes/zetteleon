---
aliases:
- Certificate Validation
- OpenSSL Certs
- PEM Inspection
created: 2025-08-27 00:00:00+00:00
modified: 2026-03-14 11:10:09+00:00
tags:
- certificates
- cheatsheet
- openssl
- pki
title: sot-openssl-operations
type: Instruction
permalink: llmeon/30-library/ops/sot-openssl-operations
---

## Instruction SoT - OpenSSL Certificate Operations

Reference for inspecting PEM certificates and validating key pairs. All commands use `openssl x509` or `openssl rsa`. The `-noout` flag suppresses printing the raw certificate.

---

### 1. Inspect a Certificate

Full details (the default starting point):

```bash
openssl x509 -in <cert>.pem -text -noout
```

Targeted queries:

```bash
# Subject (who it's issued to)
openssl x509 -in <cert>.pem -subject -noout

# Issuer (the CA)
openssl x509 -in <cert>.pem -issuer -noout

# Validity dates
openssl x509 -in <cert>.pem -dates -noout

# Fingerprint (SHA1)
openssl x509 -in <cert>.pem -fingerprint -sha1 -noout
```

---

### 2. Check Expiry

```bash
# Has it already expired? (0 = now)
openssl x509 -in <cert>.pem -checkend 0

# Will it expire in the next 30 days? (2592000 = 30 × 86400)
openssl x509 -in <cert>.pem -checkend 2592000
```

Exit code `0` = still valid. Exit code `1` = expired (or will expire within the window).

---

### 3. Validate a Public-Private Key Pair

```bash
# Step 1: Check the private key is well-formed
openssl rsa -check -in private_key.pem

# Step 2: Extract the public key from the private key
openssl rsa -in private_key.pem -pubout -out extracted_public.pem

# Step 3: Compare — no output means they match
diff original_public.pem extracted_public.pem
```

Alternative—round-trip encryption test:

```bash
# Encrypt with the public key
echo "test" | openssl rsautl -encrypt -pubin -inkey public.pem -out test.bin

# Decrypt with the private key — should print "test"
openssl rsautl -decrypt -inkey private.pem -in test.bin
```