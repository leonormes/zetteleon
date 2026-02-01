---
aliases: ["Data Wrapping", "SDU vs PDU", "The Russian Doll Mechanism"]
created: 2025-12-23T22:39:04Z
last_reviewed: "2025-12-23"
modified: 2026-02-01T15:07:59+00:00
status: "stable"
tags: ["encapsulation", "osi", "protocol", "SoftwareEngineering/Networking", "topic/technology"]
title: SoT - Encapsulation & De-encapsulation
type: "SoT"
updated: 
---

## 1. The "Russian Doll" Mechanism

The networking stack utilizes Encapsulation to allow independent systems (apps, OS, routers) to cooperate without knowing each other's internals.

- Process: As data moves down the stack, each layer treats the unit from the layer above as an opaque payload and wraps it with its own header (and sometimes a trailer).
- Result: A nested structure where the "outer" layers provide the context needed for the "inner" data to reach its destination.

---

## 2. SDU vs. PDU

To understand the nesting, we distinguish between two types of data units:

1. SDU (Service Data Unit): The data received from the layer above.
2. PDU (Protocol Data Unit): The total package (Header + SDU + Trailer) passed to the layer below.

Formula: `Header + SDU = PDU`.

---

## 3. The Path of a Request (HTTP Example)

1. Layer 7 (Application): Starts with raw Data (e.g., `GET /index.html`).
2. Layer 4 (Transport): Wraps Data in a TCP Header -> becomes a Segment.
3. Layer 3 (Network): Wraps Segment in an IP Header -> becomes a Packet.
4. Layer 2 (Data Link): Wraps Packet in a MAC Header and FCS Trailer -> becomes a Frame.
5. Layer 1 (Physical): Converts the Frame into Bits for transmission.

De-encapsulation: At the destination, the process is reversed. Each layer verifies its own header (e.g., checks the CRC at L2 or the IP address at L3), strips it, and passes the resulting SDU up to the next layer.

---

## 4. Summary

Layered encapsulation enables Modularity. An HTTP server works identically whether the underlying packets travel over Ethernet, Wi-Fi, or Fiber, because the upper layers are abstracted from the lower-layer implementation.
