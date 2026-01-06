---
aliases: []
title: Calibre Library Tags Alignment
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2026-01-05T18:04:30+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
tags: [calibre, metadata, tags, ontology]
created: 2026-01-05T14:40:23+00:00
---

# Calibre Library Tags Alignment

This table maps the raw tags from Calibre to the canonical domains defined in [[SoT - Knowledge Architecture (Associative Ontology)]].

| Existing Calibre Tag | Count | Canonical Domain (SoT) | Layer |
|:--- |:--- |:--- |:--- |
| **CLI & Tools** | 27 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **Cloud Native** | 46 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **Cognition & Focus** | 47 | [[SoT - ADHD Neurology & Core Concepts\|Cognition]] | Layer 2 (Engine) |
| **Computer Science** | 68 | [[SoT - Systems Thinking\|Systems Thinking]] / SW | Layer 1 / 3 |
| **Creativity** | 2 | [[SoT - ADHD Neurology & Core Concepts\|Cognition]] | Layer 2 (Engine) |
| **Distributed** | 18 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **Finance** | 2 | [[SoT - Financial Philosophy and Spendfulness\|Society & Economics]] | Layer 3 (Applied) |
| **Health & Performance** | 29 | [[SoT - Physical Health and Vitality\|The Human]] | Layer 3 (Applied) |
| **Music** | 2 | [[SoT - The Multifaceted Role of a Parent\|The Human]] | Layer 3 (Applied) |
| **Networking & Security** | 31 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **Productivity & PKM** | 53 | [[SoT - PRODOS Core Specification\|ProdOS]] | Layer 1 (Core) |
| **Programming** | 34 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **Software Engineering** | 44 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |

## Alignment Actions (Calibre)

To enforce consistency across tools:

1. **Merge** `CLI & Tools`, `Cloud Native`, `Distributed`, `Networking & Security`, `Programming` into -> **`Software Engineering`** (or keep as subtags if granularity is needed).
2. **Rename** `Health & Performance` -> **`The Human`** (or `Health`).
3. **Rename** `Productivity & PKM` -> **`ProdOS`**.
4. **Rename** `Finance` -> **`Economics`**.

---

# Obsidian Tags Alignment

This table maps the high-frequency tags from your Obsidian vault to the canonical domains defined in [[SoT - Knowledge Architecture (Associative Ontology)]].

| Existing Obsidian Tag | Count | Canonical Domain (SoT) | Layer |
|:--- |:--- |:--- |:--- |
| **topic/health/adhd** | 263 | [[SoT - ADHD Neurology & Core Concepts\|Cognition]] | Layer 2 (Engine) |
| **topic/productivity** | 210 | [[SoT - PRODOS Core Specification\|ProdOS]] | Layer 1 (Core) |
| **topic/technology/networking** | 180 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **topic/psychology** | 125 | [[SoT - ADHD Neurology & Core Concepts\|Cognition]] | Layer 2 (Engine) |
| **topic/cognition** | 111 | [[SoT - ADHD Neurology & Core Concepts\|Cognition]] | Layer 2 (Engine) |
| **topic/habits** | 105 | [[SoT - PRODOS Core Specification\|ProdOS]] | Layer 1 (Core) |
| **architecture** | 74 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **learning** | 68 | [[SoT - Accelerated Learning (3C Protocol)\|Cognition/ProdOS]] | Layer 1/2 |
| **neuroscience** | 64 | [[SoT - ADHD Neurology & Core Concepts\|Cognition]] | Layer 2 (Engine) |
| **security** | 62 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **topic/technology/containers** | 62 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **topic/systems** | 58 | [[SoT - Systems Thinking\|Systems Thinking]] | Layer 1 (Core) |
| **philosophy** | 56 | [[SoT - Values and Eudaimonia\|Philosophy]] | Layer 2 (Engine) |
| **project/family/bessie** | 56 | [[SoT - The Multifaceted Role of a Parent\|The Human]] | Layer 3 (Applied) |
| **topic/pkm/zettelkasten** | 54 | [[SoT - PRODOS Core Specification\|ProdOS]] | Layer 1 (Core) |
| **motivation** | 45 | [[SoT - ADHD Neurology & Core Concepts\|Cognition]] | Layer 2 (Engine) |
| **mindset** | 43 | [[SoT - Values and Eudaimonia\|Philosophy]] | Layer 2 (Engine) |
| **topic/maths** | 42 | [[SoT - Systems Thinking\|Systems Thinking]] | Layer 1 (Core) |
| **action** | 42 | [[SoT - PRODOS Core Specification\|ProdOS]] | Layer 1 (Core) |
| **identity** | 42 | [[SoT - Values and Eudaimonia\|Philosophy]] | Layer 2 (Engine) |
| **time-management** | 35 | [[SoT - PRODOS Core Specification\|ProdOS]] | Layer 1 (Core) |
| **creativity** | 35 | [[SoT - ADHD Neurology & Core Concepts\|Cognition]] | Layer 2 (Engine) |
| **topic/linux** | 35 | [[SoT - Software Configuration Management Patterns\|Software Engineering]] | Layer 3 (Applied) |
| **finance** | 19 | [[SoT - Financial Philosophy and Spendfulness\|Society & Economics]] | Layer 3 (Applied) |

## Alignment Actions (Obsidian)

1. **Refactor** `topic/health/adhd` -> **`Cognition/ADHD`** to match SoT.
2. **Refactor** `topic/productivity` & `topic/habits` -> **`ProdOS`**.
3. **Refactor** `topic/technology/*` -> **`Software Engineering/*`** (or `Technology/*` if distinct from the trade).
4. **Refactor** `topic/psychology` -> **`Cognition`** or Philosophy, depending on context (The Science vs The Compass).
5. **Merge** `architecture` (when SW related) into **`Software Engineering`**.
