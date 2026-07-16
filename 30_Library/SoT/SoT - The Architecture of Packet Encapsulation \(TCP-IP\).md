---
aliases:
- TCP/IP Encapsulation
- Packet Architecture
- SoT - Encapsulation
confidence: 5/5
created: 2025-03-26 16:26:25+00:00
epistemic: architecture
modified: 2025-12-22 12:00:00+00:00
purpose: To define the hierarchical data architecture of network encapsulation, tracing
  state from the kernel to the physical medium.
see_also:
- '[[SoT - The Data-Centric Theory of Networking]]'
- '[[SoT - The Data Architecture of DNS]]'
source_of_truth: true
tags:
- data-centric
- networking
- SoftwareEngineering/Architecture
- sot
- tcp
- encapsulation
title: SoT - The Architecture of Packet Encapsulation (TCP/IP)
permalink: llmeon/30-library/so-t/so-t-the-architecture-of-packet-encapsulation-tcp-ip
prodos:
  kind: sot
  lifecycle: stable
  review:
    last_reviewed: 2025-12-22
    interval: 6 months
  id: null
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---


## 1. Definitive Statement

> [!definition] Definition
> Encapsulation is the recursive process of wrapping a data payload within protocol-specific metadata containers (Headers/Trailers) to satisfy the requirements of different network layers.
>
> From a data-centric perspective, it is a recursive nesting of PDUs (Protocol Data Units), where each layer provides a specific "interface" for the transport, routing, or delivery of the opaque payload contained within.

---

## 2. State Definition (The Atoms)

The state of a network transmission is represented by three primary atomic units, each with a rigid bit-level schema.

### A. The TCP Segment (Layer 4)
The atom of Reliability.
- Tuple: `(SourcePort, DestPort, SeqNum, AckNum, Flags, WindowSize, Payload)`
- Key Field: `Sequence Number` (32-bit). Acts as the Byte-Index for the global stream, enabling total ordering of fragmented state.

### B. The IP Packet (Layer 3)
The atom of Global Reachability.
- Tuple: `(Version, TTL, Protocol, SourceIP, DestIP, Payload)`
- Key Field: `Protocol` (8-bit). A type-pointer (e.g., `0x06` for TCP) that defines the schema of the payload for the receiving node.

### C. The Ethernet Frame (Layer 2)
The atom of Local Delivery.
- Tuple: `(DestMAC, SourceMAC, EtherType, Payload, FCS)`
- Key Field: `FCS (Frame Check Sequence)` (32-bit CRC). The final guardian of physical state integrity.

---

## 3. Structural Mapping (The Layout)

The physical layout of the data follows the Matryoshka Model (Recursive Nesting).

### Bit-Alignment & Offsets
To maintain cache locality and processing efficiency, headers are structured in 32-bit words.
-   Data Offset (TCP): A 4-bit pointer specifying where the payload begins relative to the header apex. This allows for variable-length `Options` while preserving the boundary.
-   Header Length (IP): Similarly defines the boundary between routing metadata and transport payload.

### The Full Encapsulation Stack
```sh
[ Ethernet Header [ IP Header [ TCP Header [ Application Data ] ] ] Ethernet Trailer ]
|--- 14 Bytes ---|-- 20 Bytes --|-- 20 Bytes --|---- Variable ----|---- 4 Bytes ----|
```

---

## 4. Invariants & Constraints

1.  Integrity Invariant (End-to-End): The TCP Checksum must validate the payload AND a "pseudo-header" of the IP layer, creating a cross-layer integrity binding.
2.  Order Invariant: `Next_Expected_Seq = Current_Seq + Payload_Length`. This defines the mathematical progression of the stream state.
3.  MTU (Maximum Transmission Unit) Constraint: The total size of the Frame cannot exceed the physical limit of the medium (typically 1500 bytes). If `IP_Total_Length > MTU`, the state must be sharded (Fragmented).
4.  Flow Control Invariant: `Sent_Bytes - Acked_Bytes <= Advertised_Window_Size`. This prevents the overflow of the receiver's buffer (Memory Safety).

---

## 5. Logic Derivation (The Algorithms)

Because the data is indexed by `Sequence Numbers` and scoped by `IP/MAC` addresses, the operational logic is self-evident:

-   Reassembly: A simple Index-based Buffer Insertion. 
    -   `Target_Offset = Received_Seq - Initial_Seq`. 
    -   The logic is a "degenerate" write to a contiguous memory buffer.
-   Demultiplexing: A Nested Hash Lookup.
    -   `L2 -> MAC Table -> NIC`.
    -   `L3 -> Protocol Field -> IP Stack`.
    -   `L4 -> (SourcePort, DestPort) -> Socket_Descriptor`.
-   Error Detection: A Polynomial Division (CRC). If `Remainder != 0`, the state is corrupt and must be discarded. The logic is a direct consequence of the FCS field presence.

### Performance Optimization: Pointer Indirection
Modern OS Kernels avoid copying the payload during this process. They use structures like `sk_buff` (Linux) that manage the encapsulation via Pointer Indirection, adding headers by moving a "head" pointer through pre-allocated buffer space rather than re-allocating memory for each layer.

### Works cited

1. Services and Segment structure in TCP - GeeksforGeeks, accessed on March 26, 2025, [https://www.geeksforgeeks.org/services-and-segment-structure-in-tcp/](https://www.geeksforgeeks.org/services-and-segment-structure-in-tcp/)
2. What is TCP (Transmission Control Protocol)? - GeeksforGeeks, accessed on March 26, 2025, [https://www.geeksforgeeks.org/what-is-transmission-control-protocol-tcp/](https://www.geeksforgeeks.org/what-is-transmission-control-protocol-tcp/)
3. en.wikipedia.org, accessed on March 26, 2025, [https://en.wikipedia.org/wiki/Transmission\_Control\_Protocol\#:\~:text=A%20TCP%20segment%20consists%20of,data%20carried%20for%20the%20application.](https://en.wikipedia.org/wiki/Transmission_Control_Protocol#:~:text=A%20TCP%20segment%20consists%20of,data%20carried%20for%20the%20application.)
4. How Does TCP Work? | Kevin Sookocheff, accessed on March 26, 2025, [https://sookocheff.com/post/networking/how-does-tcp-work/](https://sookocheff.com/post/networking/how-does-tcp-work/)
5. Transmission Control Protocol - Wikipedia, accessed on March 26, 2025, [https://en.wikipedia.org/wiki/Transmission\_Control\_Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
6. TCP Header: Size, Structure, Options, Format, Checksum - Noction, accessed on March 26, 2025, [https://www.noction.com/blog/tcp-header](https://www.noction.com/blog/tcp-header)
7. TCP Message (Segment) Format - The TCP/IP Guide\!, accessed on March 26, 2025, [http://www.tcpipguide.com/free/t\_TCPMessageSegmentFormat.htm](http://www.tcpipguide.com/free/t_TCPMessageSegmentFormat.htm)
8. What is the TCP Header? - CBT Nuggets, accessed on March 26, 2025, [https://www.cbtnuggets.com/blog/technology/networking/what-is-tcp-header](https://www.cbtnuggets.com/blog/technology/networking/what-is-tcp-header)
9. TCP Header - Definition, Diagram and its Format - PyNet Labs, accessed on March 26, 2025, [https://www.pynetlabs.com/transmission-control-protocol-tcp-header/](https://www.pynetlabs.com/transmission-control-protocol-tcp-header/)
10. TCP Header - NetworkLessons.com, accessed on March 26, 2025, [https://networklessons.com/ip-routing/tcp-header](https://networklessons.com/ip-routing/tcp-header)
11. What is TCP | Header Structure to DDoS Connection | Imperva, accessed on March 26, 2025, [https://www.imperva.com/learn/ddos/tcp-transmission-control-protocol/](https://www.imperva.com/learn/ddos/tcp-transmission-control-protocol/)
12. Transmission Control Protocol (TCP) (article) - Khan Academy, accessed on March 26, 2025, [https://www.khanacademy.org/a/transmission-control-protocol--tcp](https://www.khanacademy.org/a/transmission-control-protocol--tcp)
13. Understanding TCP Header Fields: A Comprehensive Guide | NSC - NetSecCloud, accessed on March 26, 2025, [https://netseccloud.com/understanding-tcp-header-fields-a-comprehensive-guide](https://netseccloud.com/understanding-tcp-header-fields-a-comprehensive-guide)
14. Internet Protocol - Wikipedia, accessed on March 26, 2025, [https://en.wikipedia.org/wiki/Internet\_Protocol](https://en.wikipedia.org/wiki/Internet_Protocol)
15. A Deep Dive into the Anatomy of IP Packets | by Tahseen Rasheed - Medium, accessed on March 26, 2025, [https://tahseenrchowdhury.medium.com/a-deep-dive-into-the-anatomy-of-ip-packets-edd1af132aee](https://tahseenrchowdhury.medium.com/a-deep-dive-into-the-anatomy-of-ip-packets-edd1af132aee)
16. IP header - Wikipedia, accessed on March 26, 2025, [https://en.wikipedia.org/wiki/IP\_header](https://en.wikipedia.org/wiki/IP_header)
17. What are IP headers? | Hostwinds, accessed on March 26, 2025, [https://www.hostwinds.com/tutorials/what-are-ip-headers](https://www.hostwinds.com/tutorials/what-are-ip-headers)
18. IP packets (article) | The Internet - Khan Academy, accessed on March 26, 2025, [https://www.khanacademy.org/computing/ap-computer-science-principles/the-internet/x2d2f703b37b450a3:routing-with-redundancy/a/ip-packets](https://www.khanacademy.org/computing/ap-computer-science-principles/the-internet/x2d2f703b37b450a3:routing-with-redundancy/a/ip-packets)
19. IP header - Study CCNA, accessed on March 26, 2025, [https://study-ccna.com/ip-header/](https://study-ccna.com/ip-header/)
20. IPv4 Packet Header - NetworkLessons.com, accessed on March 26, 2025, [https://networklessons.com/cisco/ccna-routing-switching-icnd1-100-105/ipv4-packet-header](https://networklessons.com/cisco/ccna-routing-switching-icnd1-100-105/ipv4-packet-header)
21. TCP/IP Packet Format - GeeksforGeeks, accessed on March 26, 2025, [https://www.geeksforgeeks.org/tcp-ip-packet-format/](https://www.geeksforgeeks.org/tcp-ip-packet-format/)
22. What is IP Header? Best Explained - 2023 - Network Kings, accessed on March 26, 2025, [https://www.nwkings.com/ip-header](https://www.nwkings.com/ip-header)
23. IPv4 Header Format, Diagram, and its Significance - PyNet Labs, accessed on March 26, 2025, [https://www.pynetlabs.com/introduction-to-ipv4-header-format/](https://www.pynetlabs.com/introduction-to-ipv4-header-format/)
24. What is the Purpose of the IPv4 Header? - IP Location, accessed on March 26, 2025, [https://www.iplocation.net/what-is-the-purpose-of-the-ipv4-header](https://www.iplocation.net/what-is-the-purpose-of-the-ipv4-header)
25. en.wikipedia.org, accessed on March 26, 2025, [https://en.wikipedia.org/wiki/IP\_header\#:\~:text=An%20IP%20packet%20is%20the,%2Dto%2Dlive%2C%20etc.](https://en.wikipedia.org/wiki/IP_header#:~:text=An%20IP%20packet%20is%20the,%2Dto%2Dlive%2C%20etc.)
26. What is a packet? | Network packet definition - Cloudflare, accessed on March 26, 2025, [https://www.cloudflare.com/learning/network-layer/what-is-a-packet/](https://www.cloudflare.com/learning/network-layer/what-is-a-packet/)
27. Data Link Layer in [[OSI Model]] - GeeksforGeeks, accessed on March 26, 2025, [https://www.geeksforgeeks.org/data-link-layer/](https://www.geeksforgeeks.org/data-link-layer/)
28. Understanding Framing in Data Link Layer: A Key to Effective Communication | by Omm Ranglani | Feb, 2025 | Medium, accessed on March 26, 2025, [https://medium.com/@ommranglani/understanding-framing-in-data-link-layer-a-key-to-effective-communication-1e735b682d33](https://medium.com/@ommranglani/understanding-framing-in-data-link-layer-a-key-to-effective-communication-1e735b682d33)
29. Framing in the Data Link Layer - Dr. Balvinder Taneja, accessed on March 26, 2025, [https://drbtaneja.com/framing-in-the-data-link-layer/](https://drbtaneja.com/framing-in-the-data-link-layer/)
30. Framing in Data Link Layer - GeeksforGeeks, accessed on March 26, 2025, [https://www.geeksforgeeks.org/framing-in-data-link-layer/](https://www.geeksforgeeks.org/framing-in-data-link-layer/)
31. Framing in Data Link Layer - Piyu's CS, accessed on March 26, 2025, [https://piyuscs.com/framing-in-data-link-layer/](https://piyuscs.com/framing-in-data-link-layer/)
32. What is an Ethernet Frame? - Lightyear.ai, accessed on March 26, 2025, [https://lightyear.ai/tips/what-is-an-ethernet-frame](https://lightyear.ai/tips/what-is-an-ethernet-frame)
33. What is the Ethernet Frame Format? - CBT Nuggets, accessed on March 26, 2025, [https://www.cbtnuggets.com/blog/technology/networking/what-is-ethernet-frame-format](https://www.cbtnuggets.com/blog/technology/networking/what-is-ethernet-frame-format)
34. Ethernet frame - Wikipedia, accessed on March 26, 2025, [https://en.wikipedia.org/wiki/Ethernet\_frame](https://en.wikipedia.org/wiki/Ethernet_frame)
35. Ethernet Frame Format Explained - Computer Networking Notes, accessed on March 26, 2025, [https://www.computernetworkingnotes.com/ccna-study-guide/ethernet-frame-format-explained.html](https://www.computernetworkingnotes.com/ccna-study-guide/ethernet-frame-format-explained.html)
36. Ethernet Frame Format - GeeksforGeeks, accessed on March 26, 2025, [https://www.geeksforgeeks.org/ethernet-frame-format/](https://www.geeksforgeeks.org/ethernet-frame-format/)
37. Tutorial: Ethernet Frames and MAC Addresses - Teracom Training Institute, accessed on March 26, 2025, [https://www.teracomtraining.com/tutorials/teracom-tutorial-ethernet-frames-mac-addresses.htm](https://www.teracomtraining.com/tutorials/teracom-tutorial-ethernet-frames-mac-addresses.htm)
38. eitca.org, accessed on March 26, 2025, [https://eitca.org/cybersecurity/eitc-is-cnf-computer-networking-fundamentals/switching/how-switching-works/examination-review-how-switching-works/explain-the-significance-of-mac-addresses-in-ethernet-frames-and-how-they-contribute-to-network-uniqueness-and-efficiency/\#:\~:text=In%20Ethernet%20networking%2C%20each%20device,layer%20of%20a%20network%20segment.](https://eitca.org/cybersecurity/eitc-is-cnf-computer-networking-fundamentals/switching/how-switching-works/examination-review-how-switching-works/explain-the-significance-of-mac-addresses-in-ethernet-frames-and-how-they-contribute-to-network-uniqueness-and-efficiency/#:~:text=In%20Ethernet%20networking%2C%20each%20device,layer%20of%20a%20network%20segment.)
39. Ethernet MAC Address (7.2) - Cisco Press, accessed on March 26, 2025, [https://www.ciscopress.com/articles/article.asp?p=3089352\&seqNum=5](https://www.ciscopress.com/articles/article.asp?p=3089352&seqNum=5)
40. Ethernet frame structure and Ethernet's MAC (Medium Access Control) addresses. Each Ethernet card has a unique 48-bit address t, accessed on March 26, 2025, [https://cs.newpaltz.edu/\~easwarac/CCN/Week13/MACaddress.pdf](https://cs.newpaltz.edu/~easwarac/CCN/Week13/MACaddress.pdf)
41. MAC address - Wikipedia, accessed on March 26, 2025, [https://en.wikipedia.org/wiki/MAC\_address](https://en.wikipedia.org/wiki/MAC_address)
42. CRC Tool Computing CRC in Parallel for Ethernet - OutputLogic.com, accessed on March 26, 2025, [http://outputlogic.com/my-stuff/parallel\_crc\_byte\_enable.pdf](http://outputlogic.com/my-stuff/parallel_crc_byte_enable.pdf)
43. How CRC is Calculated in Ethernet Frame? - GeeksforGeeks, accessed on March 26, 2025, [https://www.geeksforgeeks.org/how-crc-is-calculated-in-ethernet-frame/](https://www.geeksforgeeks.org/how-crc-is-calculated-in-ethernet-frame/)