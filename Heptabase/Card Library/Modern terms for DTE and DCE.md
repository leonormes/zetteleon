---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:42+00:00
title: Modern terms for DTE and DCE
---

## Modern terms for DTE and DCE

You are correct that the core concepts behind DTE (devices that generate or consume data) and DCE (devices that transport or relay data) are still valid in networking. However, in modern networking—especially at OSI Layer 1—these specific terms are less commonly used outside of legacy serial and WAN contexts.

Are there more modern terms?

In current networking practice, especially with Ethernet and fibre, the distinction is often described using different terminology:

- Endpoint / Host / Node: These terms are used for devices that generate or consume data, such as computers, servers, printers, and IoT devices. These are the modern equivalents of DTE.
- Network Infrastructure / Network Device / Media Converter / Switch / Router / Modem: These terms refer to devices that move, relay, or convert data between endpoints. These are the modern equivalents of DCE, though the term "DCE" itself is rarely used outside of serial or WAN documentation.

At the physical layer, you may also see references to:

- Transceiver (PHY): The physical interface chip or module that handles the electrical/optical signalling.
- Media Interface: The port or connector (e.g., RJ-45, SFP) that links the device to the physical medium.

In summary, while the DTE/DCE distinction is foundational, modern documentation and standards more often use terms like "host," "endpoint," "node," "network device," "infrastructure device," or simply refer to the specific device type (e.g., switch, router, modem, transceiver) to describe the roles at Layer 1. The DTE/DCE terms are still used in some contexts, especially for serial and WAN links, but are not the primary language for Ethernet or fibre networks today.
