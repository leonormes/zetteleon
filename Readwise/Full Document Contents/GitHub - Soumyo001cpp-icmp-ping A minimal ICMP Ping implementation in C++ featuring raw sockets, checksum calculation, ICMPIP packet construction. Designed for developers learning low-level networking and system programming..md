# GitHub - Soumyo001/cpp-icmp-ping: A minimal ICMP Ping implementation in C++ featuring raw sockets, checksum calculation, ICMP/IP packet construction. Designed for developers learning low-level networking and system programming.

![rw-book-cover](https://opengraph.githubassets.com/695ae9001dbe2fbd515917c8a8c80ff12037b907e3966f1df64844b2e254f59e/Soumyo001/cpp-icmp-ping)

## Metadata
- Author: [[https://github.com/Soumyo001/]]
- Full Title: GitHub - Soumyo001/cpp-icmp-ping: A minimal ICMP Ping implementation in C++ featuring raw sockets, checksum calculation, ICMP/IP packet construction. Designed for developers learning low-level networking and system programming.
- Category: #articles
- Summary: This project is a simple C++ program that sends and receives ICMP ping packets using raw sockets. It helps developers learn how network packets are built and checked for errors. The code is lightweight, easy to build, and works on Linux with root access.
- URL: https://github.com/Soumyo001/cpp-icmp-ping

## Full Document
### Soumyo001/cpp-icmp-ping

main

Go to file

Code

Open more actions menu

### Raw ICMP Ping Implementation (C++)

#### Overview

This project is a low-level implementation of an ICMP Echo Request / Echo Reply (ping) mechanism written in modern C++.  

 It manually constructs, sends, receives, parses, and validates raw IPv4 + ICMP packets using raw sockets.

The goal of this project is **deep understanding of network packet structure**.

#### **Table of Contents**

1. [Features](https://github.com/Soumyo001/cpp-icmp-ping/#features)
2. [Installation](https://github.com/Soumyo001/cpp-icmp-ping/#installation)
3. [Usage](https://github.com/Soumyo001/cpp-icmp-ping/#usage)
4. [Examples](https://github.com/Soumyo001/cpp-icmp-ping/#examples)
5. [Development](https://github.com/Soumyo001/cpp-icmp-ping/#development-notes)
6. [License](https://github.com/Soumyo001/cpp-icmp-ping/#license)

#### **Features**

* Send ICMP Echo (ping) requests to a target IP
* Receive ICMP replies
* Specify source IP
* Configurable ping count (`-c` option)
* Continuous ping until Ctrl+C if count is not specified
* Detailed packet inspection and checksum validation
* Lightweight, no external dependencies

#### **Installation**

1. Clone the repository:

```
git clone https://github.com/Soumyo001/cpp-icmp-ping.git
cd cpp-icmp-ping
```

2. Build the program:

```
make clean && make
```

3. Run with root privileges (required for raw sockets):

```
sudo ./ping <args>
```

#### **Usage**

```
sudo ./ping [--send|--recv] [-c count] <src_ip> <dest_ip>
```

##### **Options:**

| Option | Description |
| --- | --- |
| `--send` | Sends ICMP Echo requests to a target IP |
| `--recv` | Listens and receives ICMP Echo replies |
| `-c <count>` | Number of ping requests to send (optional, default: continuous) |
| `<src_ip>` | Source IP address (optional, system default used if omitted) |
| `<dest_ip>` | Destination IP address (required in send mode) |

#### **Examples**

* **Send 5 pings to a target IP:**

```
sudo ./ping --send -c 5 192.168.0.111 192.168.0.107
```

* **Continuous ping until Ctrl+C:**

```
sudo ./ping --send 192.168.0.107
```

* **Receive mode (listen for ICMP replies):**

```
sudo ./ping --recv
```

* **Specify a source IP:**

```
sudo ./ping --send -c 3 192.168.0.111 192.168.0.107
```

#### **Development Notes**

* Written in **C++17**, uses raw sockets to handle ICMP packets
* `utils.h` contains helper functions for IP conversion, checksum calculation, and packet display
* `Ping` class handles packet building and sending/receiving
* Packet structures:

	+ `RawIpPacket` and `RawIcmpPacket` for low-level byte access
	+ `IpPacket` and `IcmpPacket` for higher-level abstraction
* **Checksum validation** ensures packet integrity before processing

#### **License**

MIT License – free to use, modify, and distribute.
