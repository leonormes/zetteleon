---
created: 2026-11-05T17:30:00+00:00
modified: 2026-11-05T17:38:17+00:00
permalink: llmeon/30-library/200-projects/home-network-test-report-2026-11-05
project_category: personal
project_name: Family
project_status: active
source: Claude Code session, 2026-11-05
status: draft
tags: [broadband, ee, network, wifi]
title: Home Network Test Report 2026-11-05
type: project
---

## Home Network Test Report: 2026-11-05

Post-fix check of the EE Full Fibre 900 line after the Openreach profile problem (stuck on a cancelled 100 Mbps order). Tests were run from the MacBook (FF-M07W9K7YN7) over Wi-Fi at about 17:05. Related: [[HEAD EE Payment error]], [[Chat_Transcript EE owed bill threat]].

### Verdict

The line is healthy and the profile fix has worked. Loaded latency (bufferbloat) is the main weakness. The hub export has gaps, so some things are unconfirmed (see below).

### Wi-Fi (En0)

- 802.11ax (Wi-Fi 6), 5 GHz, channel 149, 80 MHz, WPA2 Personal
- Signal -40 dBm, noise -91 dBm (SNR about 51 dB), transmit rate 1200 Mbps, MCS 11
- Neighbouring networks seen were on 2.4 GHz, so channel 149 is clear
- No interface errors

### Speed

| Test | Result |
|---|---|
| Apple `networkQuality` down | 391 Mbps |
| Apple `networkQuality` up | 106 Mbps |
| OVH single stream | 333 Mbps |
| ThinkBroadband single stream | 237 Mbps |
| ThinkBroadband 4 streams in parallel | about 345 Mbps |
| Cloudflare upload | 94 Mbps |

Reference from EE fault VOL055-3801106760893 (5 Nov): 925 / 110 Mbps to the hub and 629 / 110 Mbps to a device. The Wi-Fi tests above are well below the 629 Mbps device figure, so a wired test is needed to find where the gap is.

### Latency and Loss

- 0% loss to the gateway, 1.1.1.1, 8.8.8.8 and IPv6 Google
- Gateway (192.168.1.254): 11 ms average, 7 to 39 ms range
- 1.1.1.1: 16.5 ms. 8.8.8.8: 13.7 ms. IPv6 Google: 17 ms
- Traceroute to 1.1.1.1 is clean at nine hops
- `networkQuality` idle latency 86 ms, much higher than ping

### Responsiveness under Load (Bufferbloat)

- Uplink: Low, 592 ms (101 RPM)
- Downlink: Medium, 260 ms (230 RPM)
- Calls and VPN will lag when the line is saturated

### DNS and Web

- DNS 15 to 21 ms on the system resolver, 1.1.1.1, 8.8.8.8 and the router
- HTTPS total time 0.23 to 0.38 s for Google, BBC, AWS and GitLab
- IPv6 works

### Public Connection

- IPv4 81.152.61.252, BT (AS2856), Southend-on-Sea area
- IPv6 prefix 2a00:23c8:b5a2:9900::/64 on the WAN

### Hub Export (hub-status.csv, Smart Hub SH35A)

- Firmware r5.21.1-R-2045935-PROD-84001, app 5.0.50
- Uptime 8 h 14 min, so it restarted around 09:00 today (consistent with the remote profile clear)
- Usage since then: 49.89 GB down, 4.02 GB up
- Firewall on. DHCP server off
- Main Wi-Fi `EE-3JZQ37`: 2.4 GHz on channel 1 and 5 GHz on channel 149 (both Smart), WPA3-Personal-Compatibility
- Compatible Wi-Fi `EE-3JZQ37-Comp`: same channels, 5 GHz uses WPA2-Personal. My Mac joined with WPA2, so it is probably on this one
- Blank in the export: connection type, default gateway, DNS, optical levels, line sync rate, phone status

### Open Questions

- DHCP is off on the hub, so what is handing out addresses (an extender in router mode, or a second router)? Could explain the gateway jitter or double NAT
- Is the gateway jitter (7 to 39 ms) Wi-Fi or the router? Run a wired test
- Why is Wi-Fi throughput (about 345 to 391 Mbps) below the 629 Mbps device figure?
- Confirm the 900 profile and optical light levels from Technical Information
- Confirm the phone port (01702 712582 replacing the temporary number) in Phone Manager

### Suggestions

- Turn on SQM or smart queueing on the router if available
- Reboot the router once, then re-test
- Consider moving devices to the main WPA3 SSID if they all support it

### Hub Admin Access

Hub Manager is a React app using USP (TR-369) over a WebSocket at `wss://192.168.1.254/ws`, not a REST API. A command-line login would need reverse engineering of the protocol. The practical route is to log in via Chrome and export pages. The password item may be the Wi-Fi key rather than the separate Hub Manager admin password. I did not read it.

### Not Tested

`iperf3`, `mtr`, `wdutil` (needs sudo) and the `speedtest` CLI were not available. Hetzner's server was unreachable, and Cloudflare's download endpoint rejected the request, so Cloudflare was used for upload only.

### Outstanding from the EE case (Yasmin Callback Fri 6 Nov, 2 PM)

- Switch the landline from 01702 840985 to 01702 712582
- Automatic Compensation Scheme credit for 28 Oct to 3 Nov on 100 Mbps
- Motorola FW500 backup registration and the second extender
