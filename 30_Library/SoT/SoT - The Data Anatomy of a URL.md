---
aliases: ["Anatomy of a URL", "Uniform Resource Locator", "URL Structure"]
created: 2025-12-24T08:47:50Z
last_reviewed: "2025-12-23"
modified: 2026-02-01T15:07:50+00:00
status: "stable"
tags: ["SoftwareEngineering/Architecture", "SoftwareEngineering/Networking", "topic/technology", "url"]
title: SoT - The Data Anatomy of a URL
type: "SoT"
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> A URL (Uniform Resource Locator) is a serialized data string that provides the full set of instructions required to locate and retrieve a specific resource on a network.

---

## 2. The Data Structure

A URL follows a strict hierarchical schema:

```sh
<scheme://hostname[:port]/path?query#fragment>
```

| Component | Role | Example |
|:--- |:--- |:--- |
| Scheme | The Protocol (The "How"). | `https`, `ftp`, `ssh` |
| Hostname | The Destination (The "Where"). | `relay.fitfile.net` |
| Port | The Interface (The "Gate"). | `443`, `8080` |
| Path | The Resource (The "What"). | `/api/v1/upload` |
| Query | The Parameters (The "Context"). | `token=abc123` |
| Fragment | The Sub-Location (The "Anchor"). | `#section-2` |

---

## 3. Relationship: URL vs. Hostname

- Hostname: The label for the building (e.g., `fitfile.net`).
- URL: The complete directions to a specific room, in a specific building, via a specific method of transport (e.g., `https://fitfile.net/office/302`).

The browser extracts the Hostname from the URL to perform the initial DNS lookup and set the HTTP `Host` header.

---

## 4. Summary

The URL is the most specific address in the networking stack, combining identity (Hostname) with intent (Scheme/Path) to enable precise end-to-end communication.
