---
aliases: []
confidence: 
created: 2025-04-13T09:09:34Z
epistemic: 
last_reviewed: 
modified: 2025-12-08T11:11:33Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [pdu]
title: PDU names across layers
type: source
uid: 
updated: 
version: 
---

The TCP/IP link layer and the OSI data link layer are both concerned with the transfer of data across a local network segment, but there are some notable differences in their definition and scope within their respective models.

According to the sources:

## OSI Data Link Layer (Layer 2)

- It is the second layer in the seven-layer OSI model.
- It is the protocol layer that transfers data between nodes on a network segment across the physical layer.
- It provides the functional and procedural means to transfer data between network entities and may also provide the means to detect and possibly correct errors that can occur in the physical layer.
- It is concerned with the local delivery of frames between nodes on the same network segment. Data-link frames do not cross the boundaries of a local area network.
- It responds to service requests from the network layer and issues service requests to the physical layer.
- It can provide for data transfer that is reliable or unreliable. Many data link protocols do not have acknowledgments, and some may not perform error checking.
- The PDU at this layer is called a frame.
- The frame header contains source and destination addresses that indicate the origin and intended recipient of the frame. These are flat addresses, unlike the hierarchical addresses of the network layer. Examples include MAC addresses.
- The OSI data link layer is often divided into two sublayers: the Logical Link Control (LLC) sublayer and the Media Access Control (MAC) sublayer. The LLC multiplexes protocols and can provide flow control and error notification, while the MAC controls how devices access the medium. Examples of data link protocols include Ethernet, IEEE 802.11 WiFi, ATM, and Frame Relay.

## TCP/IP Link Layer

- It is the lowest layer in the four-layer TCP/IP model (or sometimes the five-layer model).
- It contains the data link layer functionality of the OSI model.
- It has the operating scope of the link a host is connected to and concerns itself with hardware issues to the point of obtaining hardware (MAC) addresses for locating hosts on the link and transmitting data frames onto the link.
- It defines the networking methods within the scope of the local network link on which hosts communicate without intervening routers.
- It includes the protocols used to describe the local network topology and the interfaces needed to effect the transmission of internet layer datagrams to next-neighbour hosts.
- It is used to move packets between the internet layer interfaces of two different hosts on the same link**.
- The processes of transmitting and receiving packets on the link can be controlled in the device driver for the network card, firmware, or specialized chipsets. These perform functions like framing to prepare internet layer packets for transmission.
- The TCP/IP model includes specifications for translating the network addressing methods used in the Internet Protocol to link-layer addresses, such as MAC addresses using the Address Resolution Protocol (ARP).
- The PDU at this layer is also called a frame**. Examples include Ethernet and PPP. The TCP/IP link layer is considered to be hardware independent and can be implemented on top of virtually any link-layer technology, including virtual link layers like VPNs and networking tunnels.

Key Contrasts:

- Layer Numbering: The OSI model has a distinct Data Link Layer as Layer 2, whereas the TCP/IP model integrates this functionality into its lowest layer, the Link Layer.
- Scope and Detail: The OSI model provides a more detailed and strict modular separation of functionality, explicitly defining both the Data Link and Physical Layers as distinct entities. The TCP/IP model is less strict and often considered to encompass aspects of the OSI Physical Layer within its Link Layer. Some sources even refer to the TCP/IP Link Layer as the "network interface" or "network access" layer, sometimes combining the OSI Physical and Data Link layers.
- Sublayers: The OSI Data Link Layer is well-defined with LLC and MAC sublayers in IEEE 802 networks. While the TCP/IP Link Layer performs similar functions, the model itself does not explicitly define these sublayers as part of its architecture, although they are relevant in the underlying technologies it uses (like Ethernet with its MAC layer).
- Reliability: While the OSI Data Link Layer *can* provide reliable delivery, it's not always the case, and higher layers might need to handle reliability. The TCP/IP model relies on the Link Layer for basic data transfer on a local link, with reliability being more centrally managed at the Transport Layer (TCP) for end-to-end communication.
- Purpose of the Model: The OSI model was intended as a comprehensive design reference, whereas the TCP/IP model was formulated to illustrate the logical groups and scopes of functions needed for the TCP/IP protocol suite's operation. Direct comparisons should be approached with caution as layering in TCP/IP wasn't a principal design criterion.

In essence, while both layers serve the fundamental purpose of facilitating data transfer across a local network, the OSI model provides a more granular and conceptually distinct Data Link Layer, whereas the TCP/IP model's Link Layer is a broader abstraction at the bottom of its stack, often encompassing aspects of the OSI Physical Layer and focusing on the immediate link connectivity required for internetworking. The TCP/IP model assumes the existence of a hardware layer below the link layer, but doesn't explicitly define it.

A Protocol Data Unit (PDU) is a single unit of information transmitted among peer entities of a computer network. It consists of protocol-specific control information and user data. In the layered architectures of communication protocol stacks, each layer implements protocols tailored to its specific data exchange needs.

## Purpose of a PDU

The primary purpose of a PDU is to enable structured communication between corresponding layers (peer entities) on different devices in a network. It facilitates the transfer of data and control information in a way that each layer can understand and process.

- Encapsulation: A key aspect of a PDU's purpose is encapsulation. When data is passed down from a higher layer to a lower layer, the lower layer treats the data as a Service Data Unit (SDU). The protocol at the lower layer then adds its own control information, such as headers (and sometimes footers), to the SDU. This combination of the SDU and the layer's specific control information forms the PDU for that layer. This process of adding information at each layer allows each layer to perform its specific functions, such as addressing, error checking, and flow control.
- Layer-Specific Functionality: Each layer's PDU format is designed to carry the information needed for the protocols at that layer to operate effectively. For example, the network layer's packet contains addressing information for routing across networks, while the transport layer's segment includes port numbers for multiplexing and demultiplexing data to the correct applications.
- Peer-to-Peer Communication: PDUs are exchanged between peer entities at the same layer on different communicating devices. The control information added by a layer at the sending device is interpreted by the corresponding layer at the receiving device to manage the communication process.

Problems Solved by PDUs:

PDUs solve several critical problems in network communication:

- Structured Data Transfer: They provide a structured format for data exchange, ensuring that communicating entities understand the different components of the transmitted information, such as source and destination addresses, data type, and error-checking codes.
- Abstraction through Layering: By defining PDUs for each layer in a network model (like OSI or TCP/IP), they enable the principle of layering. Each layer can focus on its specific tasks without needing to understand the details of the layers above or below it. The PDU acts as the interface between layers, encapsulating the data and control information relevant to that specific layer.
- Organizing Bit Streams: The data link layer, for instance, takes the stream of bits from the physical layer and organizes them into meaningful chunks called frames (a type of PDU). This framing allows for error detection and addressing within the local network segment.
- Routing and Addressing: The network layer's packet (another PDU) includes source and destination network addresses, which are crucial for routing data across multiple networks.
- Application Identification: The transport layer's segment (again, a PDU) uses port numbers to identify the specific application processes that should send and receive the data. This multiplexing and demultiplexing of data streams from different applications is essential for modern multitasking operating systems.
- Reliable and Unreliable Delivery: Different transport layer PDUs, such as TCP segments and UDP datagrams, provide different services like reliable, connection-oriented delivery (TCP) or unreliable, connectionless delivery (UDP). The PDU structure supports the specific control information required for these different modes of transfer, such as sequence numbers for TCP reliability.

History of PDU Development:

The concept of a Protocol Data Unit is closely tied to the development of layered network models, particularly the OSI (Open Systems Interconnection) model and the TCP/IP (Internet Protocol suite) model**.

- Early Networking Concepts: The need for structured data transfer emerged with the early development of computer networks like the ARPANET. As networks became more complex, the idea of organizing network functions into layers gained traction.
- OSI Model: The OSI model, developed in the late 1970s and standardized by ISO/IEC, explicitly defined seven distinct layers, each with its own protocols and corresponding PDUs. The OSI model provided a conceptual framework for discussing and teaching networking. It defined specific names for the PDU at each layer: segment (transport), packet or datagram (network), frame (data link), and bit/symbol (physical).
- TCP/IP Model: Developed concurrently with the OSI model, the TCP/IP suite adopted a less rigorous layered structure. While it doesn't have a formal seven-layer definition in its early versions (often depicted as four or five layers), it also uses the concept of PDUs at different layers. For example, it uses segments for TCP at the transport layer, datagrams or packets for IP at the internet layer, and frames at the link layer. The TCP/IP model became the foundation for the Internet.
- Evolution and Standardization: Over time, various protocols within both models have been refined and standardized by organizations like the Internet Engineering Task Force (IETF), which publishes Requests for Comments (RFCs) that define internet standards. These RFCs specify the exact format and semantics of the PDUs for different protocols like TCP, UDP, IP, HTTP, and DNS. The IEEE 802 LAN Standards Committee also specifies standards for link-layer protocols and frame formats, such as Ethernet and Wi-Fi.
- Continuing Relevance: Even though the OSI protocols themselves didn't gain widespread implementation, the OSI model's concepts, including the idea of PDUs at different layers, remain valuable for understanding network communication and are used in the context of the TCP/IP model and modern networking technologies. The term PDU is still used generically to refer to the unit of data exchanged at a particular layer in any layered protocol architecture.

In summary, the Protocol Data Unit is a fundamental concept in computer networking that provides a structured way to exchange information between peer layers in a protocol stack, enabling the encapsulation of data with layer-specific control information necessary for the correct and efficient transfer of data across a network. The development of the PDU concept is intertwined with the history of layered network models like OSI and TCP/IP, which provide the framework for defining and using PDUs at different stages of the communication process.
