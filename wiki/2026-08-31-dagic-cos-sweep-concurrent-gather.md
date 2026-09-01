---
tags:
- hermes
- solution
- cos
- dagic
source: deepseek/deepseek-v4-flash
type: agent/decision
permalink: llmeon/wiki/2026-08-31-dagic-cos-sweep-concurrent-gather
---

# Dagic Integration — CoS Sweep Concurrent Gather

**Date:** 2026-08-31

**Problem:** The cos-sweep gather step ran 6 independent I/O-bound inbox checks
sequentially (Pieces → Jira → MRs → Todoist → Obsidian → Drydock), each waiting
for the previous to complete. Combined wall time ~60s.

**Solution:** Replaced the sequential `cos-gather.py` with `cos-dagic-gather.py`
using the [Dagic](https://github.com/RohitEdathil/dagic) typed DAG engine.

**How it works:**
- All 6 gather sources are registered as Dagic `Module` tools
- The Dag program expresses them as independent calls (no data dependency)
- Dagic's async execution engine runs them concurrently
- The `combine` terminal node formats the output identically to cos-gather.py

**The Dag program (simplified):**
```
p = scan("24.0");    j = jira();        m = mrs();
t = todoist();       o = obsidian();    d = drydock();
g = gk("/tmp/gk.json");

result = combine(p, j, m, t, o, d, g, "24.0");
write_line(result);
```

**Wall time:** ~60s sequential → ~20s concurrent (bounded by slowest source).

**Files:**
- `~/.hermes/scripts/cos-dagic-gather.py` — new Dagic-powered gather
- `~/.hermes/scripts/cos-sweep.py` — GATHER_SCRIPT now points to cos-dagic-gather.py
- `~/.local/share/chezmoi/.chezmoidata/packages.yaml` — dagic added as uv tool

**Key constraints:** Dagic has no float literals — all non-string values must come
from function return values. The `hours` parameter is passed as `"24.0"` and parsed
inside the registered functions.

**Critical fix — synchronous functions block asyncio:** Dagic's executor calls
`Function.execute()` which invokes `self.function(*args)` synchronously. If the
registered function is sync (using `urllib`, `subprocess`, etc.), it blocks the
event loop — `asyncio.gather()` cannot interleave it. The fix: registered functions
must be `async def` and wrap sync I/O in `asyncio.to_thread()`:

```python
@gather.register
async def todoist() -> dict:
    return await asyncio.to_thread(cos_gather.fetch_todoist_data)
```

Without this, Dagic runs all 6 gather sources sequentially despite the DAG
showing no inter-dependencies.

**Wall time:** ~22s sequential → ~16s concurrent (bounded by slowest source,
Todoist at ~15s). Speedup of ~28-40% depending on API response times.