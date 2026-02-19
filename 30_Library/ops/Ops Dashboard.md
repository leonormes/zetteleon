---
type: dashboard
title: Ops Dashboard
icon: layout-dashboard
tags: [ops, dashboard, automated]
---

# 🛠️ Operations Control Plane

> [!INFO]
> This dashboard dynamically indexes the operational runtime in `30_Library/ops`.
> New playbooks and commands will appear here automatically if they follow the [[Atomic Command Template]].

---

## 📋 Active Playbooks
*Step-by-step guides for incident response and complex tasks.*

```dataview
TABLE 
    target_service AS "Service", 
    incident_type AS "Incident", 
    status AS "Status",
    customer AS "Customer"
FROM "30_Library/ops"
WHERE type = "playbook" OR contains(file.tags, "#playbook")
SORT target_service ASC
```

---

## ⚡ Atomic Command Library
*Single-purpose, copy-pasteable executable units.*

```dataview
TABLE 
    tool AS "Tool", 
    hop_level AS "Hop", 
    target_service AS "Target",
    requires_tunnel AS "Tunnel"
FROM "30_Library/ops"
WHERE type = "atomic_command" OR contains(file.tags, "#atomic")
SORT tool ASC, file.name ASC
```

---

## 📜 Protocols & Source of Truth
*Stable operational standards and system-of-record knowledge.*

```dataview
TABLE 
    type AS "Type",
    status AS "Status",
    modified AS "Last Modified"
FROM "30_Library/ops"
WHERE (type = "protocol" OR type = "sot" OR contains(file.name, "SoT") OR contains(file.name, "Protocol"))
  AND type != "playbook" 
  AND type != "atomic_command"
SORT file.name ASC
```

---

## 🏗️ Maintenance
- [ ] [[Atomic Command Template|Create New Atomic Command]]
- [ ] [[playbook-template|Create New Playbook]]
