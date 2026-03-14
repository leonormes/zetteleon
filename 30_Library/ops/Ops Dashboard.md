---
created: 2026-02-16T11:46:14+00:00
icon: layout-dashboard
modified: 2026-03-14T11:10:11+00:00
tags: [automated, dashboard, ops]
title: Ops Dashboard
type: dashboard
---

## 🛠️ Operations Control Plane

> [!INFO]
> This dashboard dynamically indexes the operational runtime in `30_Library/ops`.
> New playbooks and commands will appear here automatically if they follow the [[Atomic Command Template]].

---

### 📋 Active Playbooks

_Step-by-step guides for incident response and complex tasks._

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

### ⚡ Atomic Command Library

_Single-purpose, copy-pasteable executable units._

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

### 📜 Protocols & Source of Truth

_Stable operational standards and system-of-record knowledge._

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

### 🏗️ Maintenance

- [ ] [[Atomic Command Template|Create New Atomic Command]]
- [ ] [[playbook-template|Create New Playbook]]
