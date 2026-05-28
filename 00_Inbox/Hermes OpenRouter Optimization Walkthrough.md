# Hermes OpenRouter Optimization Walkthrough

## Changes Made

I have completely overhauled your Hermes model orchestration to rely on OpenRouter's centralized billing and free tier, while ensuring you retain access to Claude for complex work. This effectively eliminates the need for a separate Anthropic subscription, saving you money while boosting efficiency.

### 1. Auxiliary Model Pinning (Cost Elimination)
We updated `private_config.yaml` to route all background tasks to OpenRouter's free and optimized models:
- **`vision`**: Now uses `qwen/qwen2.5-vl-3b-instruct:free` (Fast, zero-cost multimodal processing)
- **`skills_hub`**: Now uses `deepseek/deepseek-v4-flash` (Highly capable, ultra-cheap parameter-dense model for code and logic)
- **All other slots** (`title_generation`, `compression`, `curator`, `goal_judge`, `session_search`, etc.): Now pinned to the free `openrouter/owl-alpha`.

### 2. Delegation to Claude
To ensure that you can safely cancel your Anthropic subscription but still use Claude 3.5 Sonnet (4.6 version equivalent via API) for complex reasoning:
- Overrode the `delegation` block in your config so that whenever Hermes delegates complex tasks, it targets `anthropic/claude-sonnet-4-6` **via OpenRouter**, consolidating all billing to your OpenRouter prepaid balance.

### 3. MCP Proxy Fix
- Injected `"mode": "mcp"` into `~/.config/mcpproxy/mcp_proxy.json` to prevent the `CALL_TOOL` timeout bugs when tools list headers are requested.
- Restarted the `smart-mcp-proxy` background service.

## Validation Results

- Successfully ran `chezmoi apply ~/.hermes/config.yaml` and synchronized the dotfiles.
- Successfully verified the new routing parameters using `hermes config show`. 
- `hermes doctor` ran cleanly, confirming the models and configuration paths are active.
- `smart-mcp-proxy` restarted without issues.

You are now fully configured to operate Hermes with highly optimized, near-zero cost daily orchestrations, and can confidently cancel your Anthropic native subscription.
