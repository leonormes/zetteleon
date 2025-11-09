---
aliases: []
confidence: 
created: 2025-10-31T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:49Z
purpose: 
review_interval: 
see_also: []
source: "https://www.tigera.io/blog/calico-ebpf-source-ip-preservation-the-unexpected-story-of-high-tail-latency/?utm_campaign=Newsletter-Nurture&utm_medium=email&utm_source=marketo&mkt_tok=ODA1LUdGSC03MzIAAAGd1jCSBTI0ghnSNK6cLM5nuqJkaX13OLcIP5Xaxnti1ISFKnQF4B7mLrWMzThC35rqpsx4k5eL0N0-0ciiP8P6aRPes4SxuSEuH59izCLOlg-5"
source_of_truth: []
status: 
tags: []
title: Calico eBPF Source IP Preservation The Unexpected Story of High Tail Latency
type: 
uid: 
updated: 
---

The Calico eBPF data plane is your choice if latency is your primary concern. It was very disturbing that some benchmarking brought to our attention that [eBPF](https://www.tigera.io/learn/guides/ebpf/) had higher tail latency than iptables. The 99+% percentiles were higher by as much as a few hundred milliseconds. We did a whole bunch of experiments and we could not crack the nut until we observed that there are some occasional and unexpected TCP reset (RST) packets, but no connections were reset.

We noticed that the RST belongs to a connection that was already completed and finished a while ago. That was strange, but it pointed us in the right direction. We also knew that this happens only if the benchmark uses a LoadBalancer and we have connections going through multiple nodes to the same backend pod. That was enough to get to the root cause, but let’s start at the beginning…

## External Clients and Kubernetes Services

One of the shortcomings of iptables/nftables based networking in Kubernetes is that if an external client connects to your cluster via a NodePort or a LoadBalancer, you may lose its IP address along the way. The reason for this is that the client may connect to a node which does not host any pods backing the service that client tries to connect to.

[![Diagram showing how a client IP can be lost in Kubernetes due to NAT when connecting through a NodePort/LoadBalancer](https://www.tigera.io/app/uploads/2025/03/Calico-eBPF-Source-IP-Preservation-1.png)](https://www.tigera.io/blog/calico-ebpf-source-ip-preservation-the-unexpected-story-of-high-tail-latency/?utm_campaign=Newsletter-Nurture&utm_medium=email&utm_source=marketo&mkt_tok=ODA1LUdGSC03MzIAAAGd1jCSBTI0ghnSNK6cLM5nuqJkaX13OLcIP5Xaxnti1ISFKnQF4B7mLrWMzThC35rqpsx4k5eL0N0-0ciiP8P6aRPes4SxuSEuH59izCLOlg-5#)

The services are implemented by kube-proxy and if there is no backend on a node to handle the request, it injects rules that forward the request to a backend hosted on another node. If it merely changed the destination from service to the backend and forwarded it, the other host would not know what to do with the answer, how to translate it back to service source and how to route it via the original host (let’s leave out possible Direct Server Return – DSR – for now). To address this issue, kube-proxy also changes the source to the node which forwards the request, so the response can return through it and get properly translated back.

The obvious problem is that the backend pod does not know whether it is the node who is talking to it or someone else. This is not a problem for connectivity, but it is certainly a problem for expressing security policies in a fine-grained way. You do not want to give a free pass to any node – you want to allow the load balancer or even a specific user!

To deal with this issue and with the latency of the extra hop, Kubernetes introduced ExternalTrafficPolicy. When it is set to Local, kube-proxy does not forward any connection for that service to another node. So the source is preserved. Unfortunately, that complicates other things like rejected connections when there is no backend unless the load balancer knows where the backends are and uses only those nodes.

Since the [Calico eBPF](https://docs.tigera.io/calico/latest/about/kubernetes-training/about-ebpf) data plane replaces the upstream kube-proxy with its own version, **it can do things differently—that is the eBPF super power**! Since the inception of the eBPF data plane more than 5 years ago, it could preserve the source so that the policies can be expressed in a much more precise manner.

## The Process of Preserving the Source

To preserve the source, we need to add some extra information to the packet. There are multiple ways to do it. We opted to encapsulate the original packet into a VXLAN datagram. That datagram is addressed from node to node and our conntrack on each side remembers which node was selected as the other end. When a packet gets decapsulated from VXLAN, the node can make a local decision as if the connection landed right on this node. On the way back we reverse the process, send the encapsulated response to the original node and then to the client.

In addition, if the network permits, we may not even go back through the original node. Since we have the original packet and we have the original destination IP, we can send the response straight to the client – the so-called Direct Server Return (DSR) mode, which saves some latency on the way back.

[![Diagram showing Direct Server Return (DSR) mode, where response bypasses original node and goes straight to client](https://www.tigera.io/app/uploads/2025/03/Calico-eBPF-Source-IP-Preservation-2.png)](https://www.tigera.io/blog/calico-ebpf-source-ip-preservation-the-unexpected-story-of-high-tail-latency/?utm_campaign=Newsletter-Nurture&utm_medium=email&utm_source=marketo&mkt_tok=ODA1LUdGSC03MzIAAAGd1jCSBTI0ghnSNK6cLM5nuqJkaX13OLcIP5Xaxnti1ISFKnQF4B7mLrWMzThC35rqpsx4k5eL0N0-0ciiP8P6aRPes4SxuSEuH59izCLOlg-5#)

## The Catch

In theory all works well, however, there is a catch. If a client has many connections to a NodePort via different nodes (e.g. from a single LoadBalancer), the connections that end up on the same backend may collide. How so? After the destination is resolved, it is the same for many connections. Unfortunately the source may be the exact same as well. The reason is that with many connections, there are not that many source ports. And although the client may not use the same source port to connect to the same destination, it can use the same source port to connect to nodeports on different nodes **simultaneously** – the 4-tuple is unique as the destination is different. But preserving the source leads to the collision when the different node IPs get changed to the same backend pod IP. These collisions were easy to spot as both connections break. The resolution is trickier, but Calico tackled it a few years ago. We need to make the same sources unique enough without losing who it is.

To square the circle, we made two observations. First, the source port is usually random so it does not matter too much if we change it. The second observation is that not the entire 16bit (64k) space is usable for selecting the ephemeral ports. Each system has a setting that narrows the selection space and there is always some reserved range.The default reserved ranges across various operating systems overlap, so we can pick a port from the intersection to modify the source if there is a collision. We pick the port randomly and record it in conntrack (Calico eBPF implements its own conntrack and Linux kernel, netfilter and its conntrack are largely bypassed) so that we can fix it up in the response – the range is also configurable.

[![Diagram of load balancer routing to pods via nodes, illustrating port changes in the tunnel](https://www.tigera.io/app/uploads/2025/03/Calico-eBPF-Source-IP-Preservation-3.png)](https://www.tigera.io/blog/calico-ebpf-source-ip-preservation-the-unexpected-story-of-high-tail-latency/?utm_campaign=Newsletter-Nurture&utm_medium=email&utm_source=marketo&mkt_tok=ODA1LUdGSC03MzIAAAGd1jCSBTI0ghnSNK6cLM5nuqJkaX13OLcIP5Xaxnti1ISFKnQF4B7mLrWMzThC35rqpsx4k5eL0N0-0ciiP8P6aRPes4SxuSEuH59izCLOlg-5#)

Obviously, multiple connections through different nodes may collide and if we fix up the source port randomly on one connection, we may hit another collision if we pick the same port twice. We do not want to increase the overhead of processing with complex bookkeeping of used fix up ports, therefore we try the random pick a few times in case of repeated collisions.

Although it seemed that this might be the problem, we ruled it out quite quickly. We added counters to see whether we had any such collisions (we had), and whether we were dropping packets because we could not resolve them (we did not drop any). Also executing the resolution did not take (hundreds of) milliseconds.

## The Ultimate Catch

As we mentioned at the beginning, we observed some unexpected RST packets. Those packets looked like they belonged to the connection, the 4-tuple matched, but the sequence number (TCP uses sequence numbers to order data properly) was totally off. However, the sequence number perfectly matched another already finished connection! Our eBPF conntrack should eventually reclaim conntrack entries of finished connections. And since it was finished for some time, the time gap between the two connections suggested that it must have already happened.

[![Wireshark capture showing an unexpected RST packet (highlighted in red) with a sequence number matching another packet](https://www.tigera.io/app/uploads/2025/03/Calico-eBPF-Source-IP-Preservation-4-2.png)](https://www.tigera.io/blog/calico-ebpf-source-ip-preservation-the-unexpected-story-of-high-tail-latency/?utm_campaign=Newsletter-Nurture&utm_medium=email&utm_source=marketo&mkt_tok=ODA1LUdGSC03MzIAAAGd1jCSBTI0ghnSNK6cLM5nuqJkaX13OLcIP5Xaxnti1ISFKnQF4B7mLrWMzThC35rqpsx4k5eL0N0-0ciiP8P6aRPes4SxuSEuH59izCLOlg-5#)

The fact that the old conntrack entry must have been gone by now indicated that the eBPF data plane definitely would not resolve the source collision – after all these connections were **not simultaneous**!

How is it possible that a connection that finished some time ago is still responding to a new connection? TCP is not that simple! TCP has various states that keep the socket up even after the connection finishes — the server socket was in TIME\_WAIT state (a state used to absorb any late packets left in the network) and thus saw the two connections as somewhat simultaneous and responded with an RST to the new SYN!

After we increased the wait time before we reclaim the entries from our conntrack, the tail latency went down to the expected range. Now, because the eBPF conntrack still contained the entry of the old connection, it was able to treat the two connections as simultaneous, resolve the conflict and thus avoid hitting the socket in the TIME\_WAIT state.

## Solution

Up until now, the conntrack timeouts were hardcoded, therefore we made them configurable:

TCPSynSent, TCPEstablished, TCPFinsSeen, TCPResetSeen, UDPTimeout, GenericTimeout,  
ICMPTimeout

However, since Linux has its own conntrack with many configuration knobs for its own conntrack in `/proc/sys/net/netfilter/` with good default settings, we added an option to copy them automatically from the local Linux kernel. If the configuration value is set to `auto` instead of a duration, we read the duration from the Linux configuration.

This is coming in the next Calico 3.30 release!

Try Calico source IP preservation in your browser with this [interactive workshop](https://www.tigera.io/tutorials/?_sf_s=Calico%20Basics).

## About Calico eBPF and How to Use It

Calico’s eBPF data plane replaces traditional kube-proxy networking with a high-performance, low-latency alternative. Key features include:

- **Native Service Handling:** Efficiently manages Kubernetes services without kube-proxy.
- **Enhanced Network Policies:** Leverages eBPF to optimize policy enforcement.
- **Traffic Optimization:** Improves throughput and pod-to-pod communication speeds.

**Getting Started:**

- Ensure your nodes support eBPF (Linux kernel 5.3+ recommended)
- Follow the [Enable the eBPF data plane](https://docs.tigera.io/calico/latest/operations/ebpf/enabling-ebpf#enable-ebpf-mode) guide
