---
aliases: []
confidence: 0.9
created: 2025-10-31T11:07:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Explain DNS message structure."
review_interval: 90
see_also: ["DNS Protocol Uses UDP and TCP for Message Transport.md"]
source_of_truth: []
status: seedling
tags: [dns, networking, protocols]
title: DNS Message Format Contains Header and Sections
type: concept
uid: 
updated: 
---

## DNS Message Format Contains Header and Sections

**Summary:** DNS messages have a standardized format with header fields and multiple data sections.

**Header (12 bytes):**
- ID: Query/response matching
- Flags: QR, OPCODE, AA, TC, RD, RA, RCODE
- Counts: QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT

**Sections:**
1. **Question:** Query parameters (QNAME, QTYPE, QCLASS)
2. **Answer:** Matching resource records
3. **Authority:** Referral nameserver records
4. **Additional:** Supporting data (e.g., glue records)

**Example:**

```sh
Header: ID=1234, QR=0, RD=1
Question: www.example.com IN A
Answer: www.example.com 3600 IN A 93.184.216.34
Authority: example.com NS ns1.example.com
Additional: ns1.example.com A 192.0.2.1
```
