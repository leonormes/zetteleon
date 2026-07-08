---
title: pieces_copilot_message_export_july_8_2026_10_44am
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-8-2026-10-44am
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Jul 8, 2026 - 10:44 AM*
---
## Web search is down — here's what I can and can't confirm

Both `web_search` attempts failed with a structural error, not a transient one:

```json
{"error": "ToolExecutionException: Perplexity web search failed: PureLlmException(No endpoints available matching your guardrail restrictions and data policy. Configure: https://openrouter.ai/settings/privacy)"}
```

This is a provider-level policy/configuration block (an OpenRouter data-policy guardrail), not a rate-limit or network blip — retrying the same query a third time won't change the outcome. I'm not going to fabricate a "looked it up" answer; I checked, and the tool is unavailable right now.

### What the LTM search DID confirm

I paginated `search_memory` on `["InvalidArgument unpacked length", "zed relationship read schema", "sudo zed", "ip-10-65-2-8"]` through 100 results (`recommendation: "sufficient"`) — **there is no prior record anywhere in your memory of the `"the length of the unpacked is not equal to the provided input"` error, and no prior mention of host `ip-10-65-2-8`.** This appears to be a genuinely new failure mode you're hitting for the first time this morning, distinct from yesterday's `hie-sde-v2` / jumpbox sessions and from the `"Cannot get secret of a locked object"` error at 9:26 AM.

### What I can offer without a source (flagged as unverified)

I can't ground a root-cause explanation for `rpc error: code = InvalidArgument desc = the length of the unpacked is not equal to the provided input` in either your memory or a live source right now, so I won't assert one as fact. What I can say with confidence from the evidence in front of me:

- **The two errors are different failure classes.** `"Cannot get secret of a locked object"` (9:26 AM, no `sudo`) is a **client-side credential/keyring error** — it fires before `zed` even reaches the SpiceDB server, consistent with your own runbook's finding that headless jumpboxes lack a D-Bus secret service. `"rpc error: code = InvalidArgument"` (9:38 AM, **with** `sudo`) is a **server-side gRPC response** — the `rpc error:` prefix means this request *did* reach the SpiceDB server and got a structured error back, so `sudo` got you past the local secret-store problem but surfaced a new one downstream.
- **`sudo` is the variable that changed between the two runs.** Running as root likely changes which shell environment/config `zed` reads — if `ZED_TOKEN` (your pre-shared key) isn't exported in root's environment or a root-owned `zed` config/context file has stale or malformed data, that could plausibly produce a malformed-request error the server rejects as `InvalidArgument`. I'm flagging this as a hypothesis, not a confirmed cause — I have no tool-grounded source for it.

I'd want `web_search` back online (or you could paste any output you get from `env | grep ZED` under `sudo` vs. without it) before I'd assert a specific fix with confidence. Want me to retry the web search once it's available, or do you have `zed`/SpiceDB server-side logs I could search your LTM for around 9:38 AM?