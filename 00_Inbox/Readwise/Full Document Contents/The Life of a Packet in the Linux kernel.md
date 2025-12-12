# The Life of a Packet in the Linux kernel

![rw-book-cover](https://www.0xkato.xyz/assets/images/favicon/apple-touch-icon-152x152.png)

## Metadata
- Author: [[0xkato]]
- Full Title: The Life of a Packet in the Linux kernel
- Category: #articles
- Summary: Linux moves your bytes through a clear pipeline from your app to the wire and back.  
Steps include TCP/IP segmentation, routing, ARP/neighbor lookup, queuing, NIC DMA, and hop-by-hop forwarding.  
On receive the NIC hands frames to the kernel, which checks IP/TCP and delivers data to the application.
- URL: https://www.0xkato.xyz/life-of-a-packet-in-the-linux-kernel/

## Full Document
A practical tour from `write()` to `recv()`

You run `curl http://example.com` and now you have some HTML in your terminal but what actually happened? Linux walks your bytes through a small set of well‑defined steps: pick a path, learn a neighbor’s MAC address, queue the packet, ask the NIC to send it, then reverse that on the other side.

This post tries to explain that path as simply as I can. If you’ve used Linux, run `curl`, or poked at `ip addr` before, you’re qualified to read this. No deep kernel background needed.

Note: When I say “the kernel” in this post, I really mean “the Linux kernel and its networking stack” the part that runs in the kernel and moves packets around.

#### What we’ll cover

Here is the simplified path we’ll walk through:

```
your app
  ↓ write()/send()
TCP (segments your bytes)
  ↓
IP (chooses where to send them)
  ↓
Neighbor/ARP (find the next-hop MAC)
  ↓
qdisc (queueing, pacing)
  ↓
driver/NIC (DMA to hardware)
  ↓
wire / Wi‑Fi / fiber
  ↓
NIC/driver (other host)
  ↓
IP (checks, decides it's for us)
  ↓
TCP (reassembles, ACKs)
  ↓
server app

```

#### Part 1 - Transmit: from `write()` to the wire

##### Step 1: Your app hands bytes to the kernel

You call `send()` or `write()` on a TCP socket. The kernel accepts your buffer and lines it up to send.

* TCP breaks big buffers into segments sized to fit the path. Each side advertises an MSS during the TCP handshake, and the sender limits its segment size to the peer’s advertised MSS, further constrained by the current path MTU and any IP/TCP options (e.g., timestamps).
* It tags each segment with sequence numbers so the other side can reassemble in order.

>  **Tiny explainer - socket**  
>  A socket is just your program’s communication endpoint. For TCP, the kernel keeps per‑socket state: sequence numbers, congestion window, timers.
> 
>  

>  **Tiny explainer - TCP handshake** Before any `write()` reaches the peer, TCP does a quick three‑step setup: 1) Client -> Server: SYN with options (MSS, SACK‑permitted, window scale, timestamps, ECN). 2) Server -> Client: SYN‑ACK with its options. 3) Client -> Server: ACK. Both sides agree on initial sequence numbers and options; state is ESTABLISHED. TLS note: for HTTPS, the TLS handshake runs after TCP is established.
> 
>  

>  **Try it**  
>  Run `ss -tni` while a download is active. You’ll see the TCP send and receive queue sizes fluctuate as data is transmitted on the wire and consumed by the application.
> 
>  

##### Step 2: The kernel decides where to send it (routing)

The kernel looks at the destination IP and picks the best matching route. On a typical host this boils down to a simple question: Is this IP on my local network, or do I hand it to a gateway?

* If the address is on a directly‑connected network, it goes out that interface.
* Otherwise, it goes to your default gateway (often your router).

>  **Try it**
> 
>  
> ```
> ip route get 192.0.2.10
> 
> ```
>  This prints the interface, next hop (if any), and which source IP the kernel will use.
> 
>  

>  **Tiny explainer - policy routing**  
>  The kernel can consult multiple route tables using `ip rule` (e.g. pick routes by source address or mark). Most laptops and servers use the main table.
> 
>  

##### Step 3: The kernel learns the next‑hop MAC (neighbor/ARP)

IP routing picks the next hop. To actually send an Ethernet frame, the kernel needs the MAC address for that hop.

* If the kernel already knows it (in the neighbor/ARP cache), great.
* If not, it sends a broadcast ARP request: “Who has 10.0.0.1? Tell me your MAC.” The reply is cached.

>  **Try it**
> 
>  
> ```
> ip neigh show
> 
> ```
>  You’ll see entries like `10.0.0.1 lladdr 00:11:22:33:44:55 REACHABLE`.
> 
>  

>  **Tiny explainer - ARP vs NDP**  
>  IPv4 uses ARP (broadcast). IPv6 uses Neighbor Discovery (multicast). Same idea: find the link-layer address for an IP on your network.
> 
>  

##### Step 4: The packet waits its turn (qdisc)

Before the NIC sends anything, the packet enters a queueing discipline (qdisc). You can think of this as a small waiting line plus a traffic cop where the kernel can:

* Smooth out bursts so you don’t flood the link and create bufferbloat (big queues -> high latency),
* Share bandwidth fairly across different flows, and
* Enforce shaping / rate-limit rules if you’ve configured them.

>  **Try it**
> 
>  
> ```
> tc qdisc show dev eth0
> tc -s qdisc show dev eth0   # same, but with counters/stats
> 
> ```
>  Replace `eth0` with your actual interface name (e.g. `enp3s0`, `wlp2s0`).
> 
>  

>  **Tiny explainer - MTU vs MSS**  
>  MTU is the largest L2 payload your link will carry (typical Ethernet is 1500 bytes).  
>  MSS is the largest TCP payload inside a segment, after IP + TCP headers and options.  
>  During the TCP handshake, each side advertises an MSS it can receive, a sender will not send segments larger than the peer’s advertised MSS, and will also obey the path MTU (PMTU).  
>  In the common no‑options case for IPv4, MSS ≈ MTU − 40 bytes. Options reduce MSS further.
> 
>  

##### Step 5: The driver and NIC do the heavy lifting

The kernel’s network driver hands your packet to the network card (NIC) and puts it in a small transmit queue the card reads from. The NIC then:

* pulls the bytes directly from RAM (using DMA), and turns them into a stream of bits on the link, tiny voltage changes on a copper cable, light pulses on fiber, or radio waves if you’re on Wi-Fi.

That’s the actual “onto the wire” moment: data in memory becomes signals on the network.

>  **Try it**
> 
>  
> ```
> ip -s link show dev eth0
> ethtool -S eth0     # NIC stats
> ethtool -k eth0     # offloads enabled
> 
> ```
>  Replace `eth0` with your actual interface name.
> 
>  

>  **Tiny explainer - offloads**  
>  TSO/GSO: let the NIC or stack split large buffers into MTU-sized frames.  
>  Checksum offload: on transmit, the NIC fills in IP/TCP checksums after the kernel hands it the packet, just before sending, on receive, the NIC can verify checksums and tell the kernel the result. GRO (on receive): merges many small packets into bigger chunks to save CPU.
> 
>  

>  **Tiny explainer - DMA**  
>  Direct Memory Access (DMA) lets the NIC read/write your data directly in RAM over the bus (e.g., PCIe) without the CPU copying bytes around. That’s how the NIC can pull frames from the transmit ring (and place received frames) efficiently.
> 
>  

##### Step 6: On the wire

On Ethernet, the NIC sends a frame like this:

```
[ dst MAC | src MAC | EtherType (IPv4) | IP header | TCP header | payload | FCS ]

```

Switches care about the Ethernet header: they look at the destination MAC address and forward the frame out the right port.

Routers look at the IP header, decrement the TTL / Hop Limit, and (for IPv4) update the header checksum before forwarding the packet toward the next hop.

Hop by hop, each switch and router repeats this until a router finally has a route to the destination network directly and delivers the packet onto the server’s local network.

>  **Tiny explainer - frame vs packet** A packet is the IP-level unit (IP header + TCP/UDP + payload). A frame is how that packet is carried on a specific link (e.g., Ethernet) with src/dst MAC and a checksum.
> 
>  

#### Part 2 - Receive: from the wire back to your app

##### Step 7: The NIC hands data to the kernel (NAPI)

On the server, the NIC writes incoming frames into receive rings (small queues in memory). The Linux kernel then uses NAPI to pull them in efficiently: it gets a quick interrupt, then switches to polling to process a batch of packets at once.

>  **Tiny explainer - NAPI**  
>  If every single packet triggered a full interrupt, a busy NIC could overwhelm the CPU. NAPI’s trick is:
> 
>  * raise an interrupt once,
> * temporarily switch to polling to drain a bunch of packets,
> * then re-enable interrupts.
> 
>  Fewer interrupts, better throughput.
> 
>  

##### Step 8: IP checks the packet and decides what to do

The kernel validates the IP header (version, checksum, TTL, etc.) and then asks: “Is this packet for me?”

* If the destination IP matches one of the server’s addresses, it’s local and moves upward in the stack.
* If not, and IP forwarding is enabled, the kernel may route it onward instead, that’s how a Linux box behaves as a router.
* Otherwise, the packet is dropped.

If you use a firewall, this is where hooks like PREROUTING and INPUT (nftables/iptables) can filter, log, or DNAT traffic before it’s delivered to a local socket. SNAT/MASQUERADE happen in POSTROUTING. DNAT can also occur in OUTPUT for locally generated packets.

>  **Try it**
> 
>  
> ```
> sudo nft list ruleset
> # or, with iptables:
> sudo iptables -L -n -v
> sudo iptables -t nat -L -n -v
> 
> ```
>  

##### Step 9: TCP reassembles, acknowledges, and wakes the app

The TCP stack puts segments in order, checks for missing pieces, and sends ACKs. When there’s data ready, it wakes the process waiting in `recv()`.

>  **Try it**
> 
>  
> ```
> ss -tni 'sport = :80 or dport = :80'
> 
> ```
>  Watch the receive queue (Recv-Q) grow and shrink as the app reads.
> 
>  

#### Short practical notes

##### Loopback is special (and fast)

Packets to `127.0.0.1` never hit a physical NIC. Routing still happens, but everything stays in memory on the software-only `lo` interface.

##### Bridging vs routing (same box, different role)

If the box is a bridge (e.g., with `br0`), it forwards frames at Layer 2 and doesn’t change TTL. If it’s routing, it forwards at Layer 3 and TTL drops by one hop.

##### NAT hairpin (why the inside client hits the outside IP)

Accessing a service via the router’s public IP from the same LAN needs “hairpin NAT.” If connections reset in this scenario, check `PREROUTING` and `POSTROUTING` NAT rules.

##### IPv6

Swap ARP for NDP. Otherwise, the path is the same:

```
ip -6 route
ip -6 neigh

```

##### UDP is different (on purpose)

UDP doesn’t do ordering, retransmission, or congestion control. The send path uses udp\_sendmsg, and the receive path delivers whole datagrams. Your app handles loss.

##### See it for yourself (10 quick commands)

```
# 1) Where would the kernel send a packet?
ip route get 192.0.2.10

# 2) What routes and rules exist?
ip route; ip rule

# 3) Who's my next hop?
ip neigh show

# 4) What's my firewall/NAT doing?
sudo nft list ruleset
# or:
sudo iptables -L -n -v
sudo iptables -t nat -L -n -v

# 5) Which sockets are active?
ss -tni

# 6) What's on the wire (swap eth0/host as needed)?
sudo tcpdump -ni eth0 -e -vvv 'host 192.0.2.10 and tcp port 80'

# 7) Are my queues healthy?
tc -s qdisc show dev eth0

# 8) Is my NIC happy?
ip -s link show dev eth0
ethtool -S eth0

# 9) Are counters hinting at a problem?
nstat -a | grep -E 'InErrors|OutErrors|InNoRoutes|InOctets|OutOctets'
# (Use `-z` instead of `-a` if you explicitly want to zero the counters.)

# 10) Is the path MTU safe?
tracepath 192.0.2.10   # discovers PMTU via ICMP: IPv4 "Fragmentation Needed" (Type 3, Code 4) / IPv6 "Packet Too Big" (Type 2)

```

##### ARP/neighbor problems

ip neigh shows FAILED or flips states constantly -> L2 reachability, VLAN tagging, or switch filtering issues.

##### MTU / PMTU black holes

Small pings work, big transfers stall -> mismatched MTU or blocked ICMP.  

 Allow PMTU signals through your firewall (IPv4: ICMP Type 3 Code 4 “Fragmentation Needed”, IPv6: ICMPv6 Type 2 “Packet Too Big”) or fix the MTU.

##### Reverse path filter bites

Asymmetric routing + rp\_filter=1 drops return traffic. Use rp\_filter=2 (loose) or make routing symmetric.

##### NAT surprises

SNAT/MASQUERADE mis-rewrites the source, so replies go nowhere. Check NAT rules and conntrack -L.

##### Backlog/accept pressure

New connections reset under load -> increase app backlog and net.core.somaxconn, ensure the app accept()s promptly.

##### Bufferbloat from bursts

Large queues, big latency spikes -> pick fq\_codel (or fq) for qdisc and enable pacing in your app if available.

Kernel call path (in case you were interested) Transmit (typical TCP path)

```
tcp_sendmsg
  -> tcp_push_pending_frames
    -> __tcp_transmit_skb
      -> ip_queue_xmit
        -> ip_local_out / ip_output
          -> ip_finish_output
            -> neigh_output
              -> dev_queue_xmit
                -> qdisc / sch_direct_xmit
                  -> ndo_start_xmit (driver)

```
