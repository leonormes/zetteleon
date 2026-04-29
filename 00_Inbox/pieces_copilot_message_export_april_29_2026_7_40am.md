*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Apr 29, 2026 - 7:40 AM*
---
### What was the Obsidian note?
From the long-term memories I can see **two Obsidian notes you had open this morning**, but **neither one is clearly the “platform poset” note**:

1) **“2026-04-28-pieces-omop-stress-testing-plan”** (seen at **7:32 AM**)  
2) **“Stress Test Execution Plan”** (seen at **7:36 AM**) — this one contains the synthesized plan text and references the Miro board + Jira anchors.

I **don’t have a captured memory snippet** showing the note that contains “platform poset” specifically, so I can’t name it with certainty from the current context.

#### Fastest way to locate it in Obsidian (30–60 seconds)
1) **Quick Switcher:** `Cmd+O` → type **“poset”**  
2) If that fails: `Cmd+Shift+F` (Search) → search for:
   - `poset`
   - `"platform poset"`
   - `partial order`
   - `roadmap`
   - `Planning Topics`
3) If you remember it was created “today”: open **File Explorer** in Obsidian → sort by **Modified time** → look for the most recent note around when you created the topic list.

If you paste me the top 10 lines (or the note title list from search results), I can tell you which one matches and help tighten the two topics.

---

### Meeting context (so we prep the right thing)
- Teams calendar shows **“Planning Topics - presentation”** (organized by **Weronika Jastrzebska**) visible at **7:34 AM**.
- Your clipboard note at **7:37 AM** says: **“Everybody has 2 topics to present for the future roadmap.”**

---

## Two solid topics you can bring (based on what you’ve been working on)
Below are two options that are strongly supported by your recent notes/threads—pick these unless your “platform poset” note suggests different priorities.

### Topic A — OMOP Stress Testing: proving capacity + federation behavior
**Why it’s roadmap-worthy:** it converts “we think it scales” into measurable platform guarantees.  
**Your supporting material:** the Obsidian notes above + Oliver’s suggestion to use [omock](https://ohdsi.github.io/omock/) for easier mock generation (Teams chat seen **7:16–7:33 AM**) + your Miro link (shared in the same chat): [NHS Synthetic Data & OMOP Pipeline](https://miro.com/app/board/uXjVGh4h0_g=/?share_linkid=49586236545)

**30-second structure to present**
- **Problem:** we don’t yet have hard numbers/curves for p50/p95/p99 latency + resource usage as data/node count grows.
- **Proposal:** run a phased stress plan: single-node → 2/3/5-node federation; record latency/CPU/mem/IO/error rate.
- **Output:** a “capacity envelope” and a repeatable benchmark harness.
- **Decision needed:** realistic synthetic data vs “good enough” mocks (omock) depending on what we’re validating.

### Topic B — Azure Backups module rollout for data providers (NNUH & MKUH)
**Why it’s roadmap-worthy:** it’s core resilience/compliance work that needs standardization across providers (not one-off fixes).  
**Your supporting material:** your Obsidian Jira note **FTFL-596: Configure the Azure backups module for NNUH & MKUH** (seen **7:37 AM**).

**30-second structure to present**
- **Problem:** backups module not enabled for some EoE data providers; need consistent backup posture for app PVCs + Hyve OMOP DB.
- **Proposal:** define backup policy (frequency, retention, cost model, PVC classes), then enable module + private endpoint dependency.
- **Dependencies/risks:** private endpoint subnet prerequisite; service principal permissions/roles per provider.
- **Outcome:** repeatable provider onboarding standard (less ad-hoc infra variance).

---

### If your “platform poset” note is important: quick way to map it into a topic
If “platform poset” was you describing **dependency ordering / what must precede what**, you can convert it into a roadmap topic like:
- **“Platform dependency ordering (‘poset’) → a formalized delivery sequence + gating criteria”**
  - outputs: dependency map, gates (security, backup, observability), “allowed parallelism,” and a canonical rollout order.

Send me the note title once you find it (or paste the section headings), and I’ll help you select the **best 2 topics** and turn them into **2 clean slides each**.