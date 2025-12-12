---
aliases: []
confidence: 
created: 2025-10-22T14:38:45Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking]
title: explain this cli output_ip addr show_1_ lo_ &lt;LO
type:
uid: 
updated: 
version:
---

## Explain This Cli Output

```sh
ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host noprefixroute
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
link/ether 52:55:55:0a:13:c6 brd ff:ff:ff:ff:ff:ff
altname enx5255550a13c6
inet 192.168.5.15/24 metric 200 brd 192.168.5.255 scope global dynamic eth0
valid_lft 3388sec preferred_lft 3388sec
inet6 fe80::5055:55ff:fe0a:13c6/64 scope link proto kernel_ll
valid_lft forever preferred_lft forever
```

The command `ip addr show` displays detailed information about all network interfaces on a Linux system, including both IPv4 and IPv6 addresses, link-layer (MAC) data, and interface states. Let’s break down your specific output line by line to explain each element.

---

### First Interface – Loopback

```sh
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
```

- `1:` — Interface index.
- `lo:` — Interface name (loopback).
- `<LOOPBACK,UP,LOWER_UP>` — Flags:
  - `LOOPBACK`: special local interface.
  - `UP`: device is enabled.
  - `LOWER_UP`: link layer is active.
- `mtu 65536` — Maximum Transmission Unit (max packet size).
- `qdisc noqueue` — No queuing discipline (since traffic doesn’t go on the wire).
- `state UNKNOWN` — There’s no physical carrier to test link state.
- `group default` / `qlen 1000` — Organizational grouping and default transmit queue length.

```sh
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

- `link/loopback` — Type of link-layer interface.
- MAC address is all zeros because it’s a virtual internal interface.

```sh
inet 127.0.0.1/8 scope host lo
inet6 ::1/128 scope host noprefixroute
```

- IPv4 address `127.0.0.1/8` — Used internally for local host communication.
- IPv6 address `::1/128` — IPv6 equivalent of localhost.
- `scope host` meaning it’s only reachable from within the machine.

```sh
valid_lft forever preferred_lft forever
```

- Lease times (`lft` = lifetime). “forever” means these addresses never expire.

---

### Second Interface – Ethernet

```sh
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
```

- `eth0` — Primary ethernet NIC.
- Flags explained:
  - `BROADCAST`: can send broadcast traffic.
  - `MULTICAST`: supports multicasting.
  - `UP`: interface enabled.
  - `LOWER_UP`: physical link detected.
- `mtu 1500` — Common ethernet packet size.
- `qdisc fq_codel` — Queue discipline focusing on low latency (Fair Queue Controlled Delay).
- `state UP` — Interface active.

```sh
link/ether 52:55:55:0a:13:c6 brd ff:ff:ff:ff:ff:ff
```

- `link/ether` — Ethernet link layer.
- MAC address: `52:55:55:0a:13:c6`.
- `brd` (broadcast) address: standard ethernet broadcast FF:FF:FF:FF:FF:FF.

```sh
altname enx5255550a13c6
```

- Alternate system-generated name (predictable interface naming convention).

```sh
inet 192.168.5.15/24 metric 200 brd 192.168.5.255 scope global dynamic eth0
```

- IPv4 address: `192.168.5.15` assigned dynamically (via DHCP).
- `/24` → subnet mask 255.255.255.0.
- `scope global` → accessible on the LAN.
- `metric 200` → preference ranking for routing.
- `brd` → subnet broadcast address.

```sh
valid_lft 3388sec preferred_lft 3388sec
```

- DHCP lease lifetimes — address valid and preferred for ~56 minutes.

```sh
inet6 fe80::5055:55ff:fe0a:13c6/64 scope link proto kernel_ll
```

- IPv6 link-local address auto-generated based on the interface’s MAC.
- `scope link` → only valid within local network segment.
- `proto kernel_ll` → provided by the kernel at link-layer discovery.

---

### Summary

This `ip addr show` output reveals:

- One loopback interface used internally (`lo`).
- One active network adapter (`eth0`) with:
  - Local IPv4 address `192.168.5.15`.
  - Link-local IPv6 address `fe80::5055:55ff:fe0a:13c6`.
  - Up and connected physical link.
- DHCP manages the IPv4 lease dynamically.

The command replaces the older `ifconfig` and provides richer details for network diagnostics and configuration.[^1_6][^1_7][^1_9]

<span style="display:none">[^1_10][^1_11][^1_2][^1_3][^1_5][^1_8]</span>

<div align="center">⁂</div>

[^1_2]: <https://bbs.archlinux.org/viewtopic.php?id=226489>

[^1_3]: <https://try.direct/blog/ip-command-in-linux-with-usage-examples-guide-2022>

[^1_5]: <https://www.baeldung.com/linux/ip-command-tutorial>

[^1_6]: <https://dev.to/pikotutorial/how-to-read-ip-addr-output-on-linux-fnj>

[^1_7]: <https://greenwebpage.com/community/7-examples-of-ip-addr-command-in-linux/>

[^1_8]: <https://www.reddit.com/r/linux4noobs/comments/xzal74/what_does_ip_addr_show_exactly/>

[^1_9]: <https://www.linode.com/docs/guides/how-to-use-the-linux-ip-command/>

[^1_10]: <https://labex.io/tutorials/linux-how-to-interpret-network-interface-output-438374>

[^1_11]: <https://phoenixnap.com/kb/linux-ip-command-examples>

---

I Am on a Linux Vm. Give Me a Set of Commands to Use to Explore Dns and Dns Resolution from My Cli. I want to Understand how it Works and how I Would Go about Debugging Dns Problems

Let's walk through a structured sequence of Linux commands you can use to understand and troubleshoot **DNS (Domain Name System)** resolution from your command line. These are organized by *purpose*, so you can explore step-by-step and then apply them for debugging.

### 1. Check Network Connectivity

Before investigating DNS, ensure the network connection itself works:

```bash
ping -c 3 8.8.8.8     # Tests connectivity using Google's public IP
ping -c 3 google.com  # Tests both connectivity and name resolution
```

If the first command succeeds but the second fails, DNS resolution is the issue.

### 2. Verify DNS Configuration

Check which DNS servers your system is configured to use:

```bash
cat /etc/resolv.conf
```

You’ll typically see lines like:

```sh
nameserver 1.1.1.1
nameserver 8.8.8.8
```

If these entries look wrong or stale, DNS queries may fail.

### 3. Query DNS Directly with Common Tools

These tools bypass normal resolution steps and query DNS servers directly:

#### `dig` – Detailed DNS Query Tool

```bash
dig example.com             # Standard lookup
dig -x 93.184.216.34        # Reverse lookup (IP → domain)
dig example.com MX          # Query specific record type (Mail servers)
dig @8.8.8.8 example.com    # Query a specific DNS server
```

This shows which DNS server gave the answer, how long it took, and TTL info.

#### `nslookup` – Simpler Diagnostic Tool

```bash
nslookup example.com
nslookup -type=MX example.com
nslookup example.com 8.8.8.8   # Query Google DNS directly
```

`nslookup` is easier to read than `dig` for quick checks.

#### `host` – Lightweight name Resolver

```bash
host example.com
host -t MX example.com
host 93.184.216.34
```

Quick and succinct for basic lookups.

### 4. Check Local DNS Services (if applicable)

If your system uses `systemd-resolved` or a local caching resolver like `dnsmasq`:

```bash
resolvectl status              # Overview of DNS state
sudo systemctl status systemd-resolved
sudo systemctl status dnsmasq
```

You can also test resolution through `systemd` directly:

```bash
systemd-resolve example.com
```

### 5. Debug Firewall and Routing Issues

Firewall rules can block DNS traffic on port 53.

```bash
sudo iptables -L -n | grep 53
```

To trace packet routing:

```bash
traceroute google.com
```

### 6. Advanced Analysis

If problems persist, try these options:

- `tcpdump -i eth0 port 53` — Monitor DNS traffic live.
- `journalctl -u systemd-resolved` — Check resolver logs.
- Compare `/etc/nsswitch.conf` to ensure `dns` appears in the "hosts" line (`hosts: files dns`).

### How to Explore \& Learn

1. Run each command above and compare IPv4 vs IPv6 responses.
2. Change `/etc/resolv.conf` temporarily to use a different DNS (e.g., `8.8.8.8`) and test again.
3. Use `dig +trace example.com` to observe recursive resolution step-by-step.

Would you like me to create a *practice exercise* where you simulate diagnosing a DNS outage?

<span style="display:none">[^2_1][^2_10][^2_11][^2_12][^2_13][^2_14][^2_15][^2_2][^2_3][^2_4][^2_5][^2_6][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: <https://www.redhat.com/en/blog/DNS-name-resolution-troubleshooting-tools>

[^2_2]: <https://gcore.com/learning/troubleshooting-dns-issues-linux>

[^2_3]: <https://www.tecmint.com/troubleshoot-dns-in-linux/>

[^2_4]: <https://www.cloudns.net/blog/linux-host-command-troubleshot-dns/>

[^2_5]: <https://community.bigbeartechworld.com/t/comprehensive-guide-to-diagnosing-dns-issues-on-linux/221>

[^2_6]: <https://www.checklyhq.com/blog/dns-debugging-deep-dive/>

[^2_7]: <https://stackoverflow.com/questions/19322962/how-can-i-list-all-dns-records>

[^2_8]: <https://cleanbrowsing.org/help/docs/troubleshooting-dns-terminal-commands/>

[^2_9]: <https://eludom.github.io/blog/dns-today/>

[^2_10]: <https://www.eukhost.com/kb/how-to-check-dns-records-of-a-domain/>

[^2_11]: <https://www.youtube.com/watch?v=vntErvakmsM>

[^2_12]: <https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/>

[^2_13]: <https://www.tecmint.com/find-my-dns-server-ip-address-in-linux/>

[^2_14]: <https://www.linux.com/news/linux-troubleshooting-commands-4-tools-for-dns-name-resolution-problems/>

[^2_15]: <https://blog.dnsimple.com/2017/08/debugging-dns/>

---

## Cat /etc/resolv.conf

## This is /run/systemd/resolve/stub-resolv.conf Managed by man:systemd-resolved(8)

## Do not Edit

##

## This File Might Be Symlinked as /etc/resolv.conf. If You're Looking at

## /etc/resolv.conf And seeing This Text, You Have Followed the Symlink

##

## This is a Dynamic resolv.conf File for Connecting Local Clients to the

## Internal DNS Stub Resolver of Systemd-resolved. This File Lists All

## Configured search Domains

##

## Run "resolvectl status" to See Details about the Uplink DNS Servers

## Currently in Use

##

## Third Party Programs Should Typically not Access This File Directly, but only

## Through the Symlink at /etc/resolv.conf. To Manage man:resolv.conf(5) in a

## Different Way, Replace This Symlink by a Static File or a Different Symlink

##

## See man:systemd-resolved.service(8) for Details about the Supported Modes of

## Operation for /etc/resolv.conf

nameserver 127.0.0.53

options edns0 trust-ad

search lan fitfile.internal

Your `/etc/resolv.conf` shows that your system uses **systemd-resolved**, which runs a local stub DNS resolver listening on `127.0.0.53` (a loopback address). This means your applications don’t talk to external DNS servers directly — they query **systemd-resolved**, which forwards the request to the “uplink” DNS servers it has learned from DHCP or manual configuration.[^3_1][^3_2][^3_3]

Here’s what’s going on line by line and how to work with it.

---

### How Systemd-resolved and the Stub Resolver Work

- **Systemd-resolved** provides system-wide name resolution, caching, and DNSSEC/DoT support.
- It listens on **127.0.0.53** and handles all DNS queries that client programs send.
- The system dynamically manages `/run/systemd/resolve/stub-resolv.conf`, which lists:

```sh
nameserver 127.0.0.53
search lan fitfile.internal
```

Applications point to it via the symlink `/etc/resolv.conf`.

When you run a command like `ping example.com`, the resolver library sends the DNS query to `127.0.0.53`. The **systemd-resolved** service then decides where to send the query upstream (e.g., your router or a public DNS server such as 1.1.1.1).[^3_3][^3_4][^3_5]

---

### Viewing Real DNS Configuration and Status

To see which DNS servers *systemd-resolved* is actually using upstream, run:

```bash
resolvectl status
```

You’ll see:

- **Global settings** – fallback servers, DNSSEC status.
- **Per-link (per-interface) DNS servers** – typically ones received via DHCP.
- **Current DNS Server** – which one is being used at this moment.

To list only active upstream DNS servers:

```bash
resolvectl dns
```

To see which search domains apply:

```bash
resolvectl domain
```

---

### Managing and Debugging Systemd-resolved

**Check service status**

```bash
systemctl status systemd-resolved
```

**Flush cached DNS records**

```bash
sudo resolvectl flush-caches
```

**Inspect cached entries**

```bash
sudo resolvectl query example.com
```

**Temporarily set a DNS server for your interface**
(e.g. use Cloudflare DNS instead of DHCP-provided ones)

```bash
sudo resolvectl dns eth0 1.1.1.1
```

**Reset DNS settings**
(if something gets stuck)

```bash
sudo systemctl restart systemd-resolved
```

---

### Customizing Behavior

If you want to override or extend your current DNS configuration:

- Edit **/etc/systemd/resolved.conf** (for global settings) or drop-ins in `/etc/systemd/resolved.conf.d/*.conf`.
- Example minimal config:

```ini
[Resolve]
DNS=1.1.1.1 8.8.8.8
FallbackDNS=9.9.9.9
```

- Then run:

```bash
sudo systemctl restart systemd-resolved
```

**Note:** If you prefer not to use systemd-resolved’s stub resolver, you can unlink `/etc/resolv.conf` and point directly to a static config file with your chosen nameservers (though this disables caching and per-interface management).[^3_2][^3_6][^3_7]

---

### Summary

Your resolver setup routes all local DNS lookups to the **systemd-resolved** service via `127.0.0.53`. It manages real upstream DNS servers dynamically and can be inspected and controlled with `resolvectl`. For DNS debugging, always start with `resolvectl status` to see the "real" servers, not what’s in `/etc/resolv.conf`.

<span style="display:none">[^3_10][^3_11][^3_12][^3_13][^3_14][^3_15][^3_16][^3_17][^3_18][^3_8][^3_9]</span>

<div align="center">⁂</div>

[^3_1]: <https://wiki.archlinux.org/title/Systemd-resolved>

[^3_2]: <https://www.youtube.com/watch?v=zzFbFEOgtY0>

[^3_3]: <https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html>

[^3_4]: <https://www.linkedin.com/pulse/why-does-etcresolvconf-point-1270053-om-prakash-singh>

[^3_5]: <https://www.baeldung.com/linux/resolve-conf-systemd-avahi>

[^3_6]: <https://forum.virtualmin.com/t/127-0-0-53-do-i-need-it/127057>

[^3_7]: <https://blog.benyamin.xyz/2023/06/26/dns-in-systemd-land-using-resolvectl-temporary-set-get-status-and-clear-cache/>

[^3_8]: <https://github.com/systemd/systemd/issues/5051>

[^3_9]: <https://www.reddit.com/r/linux4noobs/comments/u618vc/systemdresolve_vs_resolvconf/>

[^3_10]: <https://github.com/systemd/systemd/issues/31674>

[^3_11]: <https://github.com/systemd/systemd/issues/10298>

[^3_12]: <https://discussion.fedoraproject.org/t/how-do-i-set-resolv-conf-contents-manually/67362>

[^3_13]: <https://hackliza.gal/en/posts/cambiar_dns_linux/>

[^3_14]: <https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdResolvedConsidering>

[^3_15]: <https://www.reddit.com/r/linux4noobs/comments/x4m8dz/cat_etcresolvconf_and_resolvectl_status_different/>

[^3_16]: <https://jpetazzo.github.io/2024/05/12/understanding-kubernetes-dns-hostnetwork-dnspolicy-dnsconfigforming/>

[^3_17]: <https://man7.org/linux/man-pages/man1/resolvectl.1.html>

[^3_18]: <https://discourse.pi-hole.net/t/linux-clients-cannot-reach-update-servers-since-activating-pi-holes-dhcp-server/72373>

---

I Am Running Lima Vm on Macos. How Would that Effect the Results from These Commands? I Am in an Ubuntu Vm but I Understand This is Different from a Full Linux Machine

When you run an Ubuntu guest inside **Lima** on macOS, DNS behavior differs slightly from a native Linux environment because Lima inserts a layer between your VM and the host’s network stack. Understanding this helps interpret what commands like `resolvectl status` or `cat /etc/resolv.conf` will show.[^4_1][^4_2][^4_3][^4_4]

---

### How Lima Handles Networking and DNS

By default, Lima uses **user-mode networking (slirp)** on the subnet `192.168.5.0/24`. MacOS doesn’t give guest VMs direct access to your physical NIC, so Lima runs an internal **gVisor TAP proxy** that provides virtual Ethernet to the guest. This proxy also runs a **DNS stub resolver** exposed to the VM, often as something like `192.168.5.2` or a similar local IP ().[^4_3]

That resolver translates guest DNS queries into requests handled by macOS itself (through `mDNSResponder`).[^4_4]

So when you see `/etc/resolv.conf` showing:

```sh
nameserver 127.0.0.53
```

and `resolvectl status` revealing a single upstream of `192.168.5.2`, that IP doesn’t lead directly to the internet—it’s handled by a small DNS service that proxies to macOS’s real system resolvers (including any VPN-split DNS configuration).[^4_2][^4_1][^4_4]

---

### Key Differences from a Full Linux Host

| Behavior                     | Native Linux                                      | Lima VM (on macOS)                                       |
| :--------------------------- | :------------------------------------------------ | :------------------------------------------------------- |
| Network interface            | Physical (eth0 or wlan0) tied to NIC              | Virtual `eth0` bridged via slirp or VZ                   |
| DNS servers                  | From DHCP on the real network                     | Usually `192.168.5.2` → host resolver                    |
| `/etc/resolv.conf`           | Often lists public resolvers or DHCP-provided IPs | Stub (127.0.0.53) handled by systemd-resolved            |
| Real upstream servers        | Directly configurable                             | Delegated through Lima's hostResolver                    |
| DNS caching \& VPN split DNS | Managed by systemd-resolved                       | Controlled primarily by macOS mDNSResponder [^4_1][^4_2] |

---

### What This means for Your Commands

- `cat /etc/resolv.conf` → Always shows the **local loopback stub** (`127.0.0.53`), same as standard Ubuntu.
- `resolvectl status` → Shows the actual **Lima DNS proxy** (often `192.168.5.2`) as the upstream.
- `dig` / `nslookup` → Return results using whatever DNS servers macOS is configured with (including VPN-specific resolvers).
- `ping` → Works normally, but success depends on both Lima NAT routing and the host DNS.

---

### Practical Debugging in Lima

1. **Inspect VM’s DNS path**

```bash
resolvectl status
```

Look for the current DNS server—usually `192.168.5.2`.

2. **Test using Lima’s resolver directly**

```bash
dig @192.168.5.2 example.com
```

3. **Check macOS host DNS configuration**

```bash
scutil --dns
```

You’ll see which macOS network interfaces and VPNs define resolvers.

4. **Debug split DNS or VPN issues**
   - If certain domains fail to resolve inside the VM but work on macOS, Lima’s proxy isn’t picking up your VPN-specific DNS configurations (a known limitation in some versions ).[^4_2]
   - Upgrading Lima or switching to `--network vzNAT` (available on Apple Silicon) can fix that behavior.

---

### Takeaway

Inside your Ubuntu Lima VM:

- `/etc/resolv.conf` and `resolvectl` describe **systemd-resolved**’s local stub layer.
- Real resolution happens via Lima’s built-in DNS proxy (`192.168.5.2`), which in turn delegates queries to macOS’s DNS stack.
- Any DNS misbehavior often stems from the macOS host’s resolver configuration, VPN split-DNS, or a disconnected host network interface rather than the VM itself.

In essence, your Ubuntu VM’s DNS experience mirrors macOS’s — just transparently bridged through Lima’s virtual resolver and `systemd-resolved`.

<span style="display:none">[^4_10][^4_11][^4_12][^4_13][^4_14][^4_15][^4_16][^4_17][^4_5][^4_6][^4_7][^4_8][^4_9]</span>

<div align="center">⁂</div>

[^4_1]: <https://github.com/lima-vm/lima/discussions/2279>

[^4_2]: <https://github.com/lima-vm/lima/issues/2939>

[^4_3]: <https://lima-vm.io/docs/config/network/user/>

[^4_4]: <https://github.com/lima-vm/lima/discussions/736>

[^4_5]: <https://lima-vm.io/docs/dev/internals/>

[^4_6]: <https://news.ycombinator.com/item?id=38989019>

[^4_7]: <https://github.com/k3s-io/k3s/issues/4087>

[^4_8]: <https://pawelweselak.com/posts/lima-vm/>

[^4_9]: <https://lima-vm.io/docs/config/network/>

[^4_10]: <https://www.reddit.com/r/linux/comments/18kh1r5/im_shocked_that_almost_no_one_is_talking_about/>

[^4_11]: <https://slack-archive.rancher.com/t/13150357/has-anyone-seen-odd-delays-when-using-rancher-desktop-1-8-x->

[^4_12]: <https://news.ycombinator.com/item?id=36668964>

[^4_13]: <https://blobfolio.com/2017/fix-linux-dns-issues-caused-by-systemd-resolved/>

[^4_14]: <https://stackoverflow.com/questions/71581201/how-to-fix-the-read-only-error-on-lima-vm>

[^4_15]: <https://wiki.archlinux.org/title/Systemd-resolved>

[^4_16]: <https://spiffyeight77.com/posts/all/2024/11/replacing-docker-desktop-on-macos-with-lima/>

[^4_17]: <https://jvns.ca/blog/2023/07/10/lima--a-nice-way-to-run-linux-vms-on-mac/>

---

## Scutil --dns

DNS configuration

resolver \#1

search domain[0] : lan

search domain[1] : fitfile.internal

nameserver[0] : 100.103.255.254

port : 53

flags : Supplemental, Request A records

reach : 0x00000002 (Reachable)

order : 103000

resolver \#2

nameserver[0] : 192.168.86.1

if_index : 14 (en0)

flags : Request A records

reach : 0x00020002 (Reachable,Directly Reachable Address)

order : 200000

resolver \#3

domain : fitfile.internal

nameserver[0] : 100.103.255.254

port : 53

flags : Supplemental, Request A records

reach : 0x00000002 (Reachable)

order : 103001

resolver \#4

domain : lan

nameserver[0] : 192.168.86.1

port : 53

flags : Supplemental, Request A records

reach : 0x00020002 (Reachable,Directly Reachable Address)

order : 102800

resolver \#5

domain : local

options : mdns

timeout : 5

flags : Request A records

reach : 0x00000000 (Not Reachable)

order : 300000

resolver \#6

domain : 103.100.in-addr.arpa

nameserver[0] : 100.103.255.254

port : 53

flags : Supplemental, Request A records

reach : 0x00000002 (Reachable)

order : 102600

resolver \#7

domain : 254.169.in-addr.arpa

options : mdns

timeout : 5

flags : Request A records

reach : 0x00000000 (Not Reachable)

order : 300200

resolver \#8

domain : 8.e.f.ip6.arpa

options : mdns

timeout : 5

flags : Request A records

reach : 0x00000000 (Not Reachable)

order : 300400

resolver \#9

domain : 9.e.f.ip6.arpa

options : mdns

timeout : 5

flags : Request A records

reach : 0x00000000 (Not Reachable)

order : 300600

resolver \#10

domain : a.e.f.ip6.arpa

options : mdns

timeout : 5

flags : Request A records

reach : 0x00000000 (Not Reachable)

order : 300800

resolver \#11

domain : b.e.f.ip6.arpa

options : mdns

timeout : 5

flags : Request A records

reach : 0x00000000 (Not Reachable)

order : 301000

DNS configuration (for scoped queries)

resolver \#1

search domain[0] : lan

nameserver[0] : 192.168.86.1

if_index : 14 (en0)

flags : Scoped, Request A records

reach : 0x00020002 (Reachable,Directly Reachable Address)

Your `scutil --dns` output reveals how **macOS’s DNS stack** manages multiple parallel resolvers, including split DNS behavior from your VPN and local network. Unlike Linux, macOS doesn’t rely on a single `/etc/resolv.conf` file; instead, it defines multiple *scoped resolvers*, each tied to interfaces, domains, or VPNs.[^5_1][^5_2][^5_3]

---

### Understanding the Structure

Each **resolver** block represents a separate DNS context. macOS prioritizes resolvers based on the **order** field and which domain a query matches.

Example from your output:

```sh
resolver #1
  search domain[^5_0] : lan
  search domain[^5_1] : fitfile.internal
  nameserver[^5_0] : 100.103.255.254
```

- **nameserver:** Where DNS queries go; `100.103.255.254` is likely from a VPN client or virtual network tunnel.
- **search domains:** Used to auto-expand short hostnames (e.g., `ping server` → `server.fitfile.internal`).
- **flags:**
  - `Supplemental` → used for specific domains (split DNS).
  - `Scoped` → bound to a network interface, e.g., a VPN.
- **order:** Lower values take priority unless a more specific domain matches.
- **reach:** Indicates availability (`Reachable`, `Directly Reachable`, etc.).[^5_4][^5_3][^5_1]

---

### How macOS Handles DNS Requests

1. **Scoped resolution:**
   If a domain matches one listed (like `fitfile.internal`), the resolver tied to that domain’s network (likely a VPN) handles it.
2. **General resolution:**
   For non-matching domains, macOS uses general resolvers (`resolver #2` here → `192.168.86.1`, your LAN router/DNS).
3. **mDNS / local resolution:**
   Resolvers like `domain : local` handle multicast DNS (Bonjour/zeroconf on your LAN), not Internet queries.

---

### Why You See These IPs

- **100.103.255.254** → Routed DNS server from a VPN, Tailscale, or ZeroTier network.
- **192.168.86.1** → Your home router’s DNS.
- **Scoped “fitfile.internal” resolver** → Used for internal/private names, typical in corporate or overlay networks.
- **Orders in the 100000–103000 range** → macOS prioritization system (smaller = higher priority).[^5_2][^5_5]

---

### Practical Interpretation for Your Setup

Your DNS graph likely looks like this:

```sh
Ubuntu VM → 192.168.5.2 (Lima DNS proxy)
              ↓
macOS resolver daemon (mDNSResponder)
              ↓
VPN DNS (100.103.255.254)
Home router DNS (192.168.86.1)
```

- **VM queries** flow through Lima to macOS’s resolver hierarchy.
- macOS decides routing based on split-DNS logic: internal domains (`fitfile.internal`, `lan`) → VPN DNS; everything else → router DNS.

---

### Commands for Exploration

Check which resolver handles a domain:

```bash
scutil --dns | grep -A5 fitfile.internal
```

Force-query a specific nameserver:

```bash
dig @100.103.255.254 host.fitfile.internal
```

Inspect what network interfaces are associated:

```bash
scutil --nwi
```

See live resolution routing:

```bash
log stream --predicate 'subsystem == "com.apple.mDNSResponder"' --info
```

---

### In Context with Your Lima VM

The Lima guest (Ubuntu) sends all DNS requests to its virtual gateway (127.0.0.53 → 192.168.5.2), which passes them to macOS. Your Mac then uses this split-DNS configuration, deciding whether to resolve through your corporate VPN or your home router. Thus, DNS differences you see in-Linux (e.g., `dig google.com`) often reflect macOS routing logic, not Ubuntu configuration issues.[^5_3][^5_6][^5_7][^5_8][^5_1]

---

In short, your `scutil --dns` output describes a **split-DNS setup managed by macOS**, where `fitfile.internal` is resolved by a VPN DNS (`100.103.255.254`), while public queries go through your local router (`192.168.86.1`). All of this cascades naturally into your Lima VM’s `systemd-resolved` layer.
