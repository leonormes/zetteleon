---
aliases: []
confidence: 
created: 2025-12-09T09:40:15Z
epistemic: 
last_reviewed: 
modified: 2025-12-09T09:41:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: What NNUH could have done in Entra ID beforehand
type: 
uid: 
updated: 
---

Yes – there *is* a way they could have tested this in advance, but it lives in two places:

1. **Admin-side (Entra ID / Conditional Access “What If”)**
2. **VM-side (a small az‑based preflight script run on the actual jumpbox)**

Given your NNUH experience (error 53003, Azure CLI app blocked by Conditional Access from the jumpbox), you really want *both*.

---

## 1. What NNUH Could Have Done in Entra ID beforehand

From the Entra / Azure AD side, they can’t literally “run a command on your future jumpbox,” but they *can* test whether their Conditional Access policies will block the Azure CLI in that scenario.

The built‑in tool is:

> **Entra ID → Security → Conditional Access → What If**

They can configure it as:

- **User:** your FITFILE user (e.g. `leon.ormes@...`)
- **Cloud app:**  
  “**Microsoft Azure CLI**”  
  App ID: `04b07795-8ddb-461a-bbee-02f9e1bf7b46`
- **Client app:** “Mobile apps and desktop clients” / “Modern authentication clients”
- **Device platform:** Linux (or “Any” if unsure)
- **Location:** a named location matching the jumpbox egress IP (e.g. NAT gateway public IP)
- **Device state:** “Unregistered” (since the jumpbox isn’t a compliant corporate device)

Running the What‑If with those inputs tells them:

- Which **Conditional Access policies** would apply
- Whether those policies **block** or **require compliant device**, etc.

If they had done this with “Azure CLI + unregistered device + that IP range,” they would have seen the 53003‑style block in advance and could have:

- Allowed the Azure CLI app, or
- Excluded that IP range / your user, or
- Documented the device registration/compliance step you’d have to do.

So: yes, there *is* an Azure/Entra test, but it’s **admin-side** and not scriptable from your side.

---

## 2. What Your customer‑side Bash Preflight Script Should Do

For your FFAPP‑4670 “Create customer cloud setup verification script” task, the safest pattern is:

> **Run a script *on the jumpbox*, as the exact user who will operate AKS.  
> The script guides them through az login and then runs a series of checks.**

You can’t fully automate device‑code login, but you *can* standardise it and detect the common failures (including 53003).

### Outline of the Script

High‑level checks:

1. **Environment + tooling**
   - `az` installed and recent enough.
   - DNS + HTTPS connectivity to Azure endpoints.

2. **Login & Conditional Access**
   - Clear any stale tokens.
   - `az login --tenant "$TENANT_ID" --use-device-code`
   - If it fails, detect Conditional Access errors (53003) and print “send this to your Entra admin” instructions.

3. **Subscription & role sanity**
   - `az account show` → verify:
     - Correct tenant
     - Correct subscription ID
   - Confirm the signed‑in user has the required role (e.g. **Contributor** on the subscription or deployment scope).

4. **Basic ARM / AKS reachability (read‑only)**
   - `az resource list --top 1` or `az group list` to prove ARM is reachable.
   - Optional: `az aks list` / `az network vnet list` depending on how much you expect to exist.

### Concrete Bash Skeleton

Something like this (simplified, adjust to your conventions):

```bash
#!/usr/bin/env bash
set -euo pipefail

TENANT_ID="${ARM_TENANT_ID:-}"
SUBSCRIPTION_ID="${ARM_SUBSCRIPTION_ID:-}"

if [[ -z "$TENANT_ID" || -z "$SUBSCRIPTION_ID" ]]; then
  echo "[ERROR] ARM_TENANT_ID and ARM_SUBSCRIPTION_ID must be set in the environment."
  exit 1
fi

echo "== 1. Checking Azure CLI =="
if ! command -v az >/dev/null 2>&1; then
  echo "[ERROR] Azure CLI (az) is not installed on this jumpbox."
  exit 1
fi
echo "Azure CLI version: $(az version --output json | jq -r '.\"azure-cli\"')"

echo "== 2. Checking network connectivity to Azure endpoints =="
for host in "login.microsoftonline.com" "management.azure.com"; do
  if ! curl -fsS "https://${host}" >/dev/null 2>&1; then
    echo "[ERROR] Cannot reach ${host} over HTTPS. Check proxy/firewall."
    exit 1
  fi
done
echo "Network connectivity OK."

echo "== 3. Logging in with device code (you will need to use a browser) =="
az account clear >/dev/null 2>&1 || true

# Capture output & errors to inspect failures
LOGIN_STDERR="$(mktemp)"
if ! az login --tenant "$TENANT_ID" --use-device-code 2> "$LOGIN_STDERR" >/dev/null; then
  echo "[ERROR] az login failed."

  if grep -q "53003" "$LOGIN_STDERR"; then
    echo
    echo "It looks like a Conditional Access (53003) error."
    echo "Please send the full error page (including Correlation ID, Request ID, Timestamp)"
    echo "to your Entra ID / Azure AD administrator and ask them to allow:"
    echo "  - App: Microsoft Azure CLI (04b07795-8ddb-461a-bbee-02f9e1bf7b46)"
    echo "  - From this jumpbox's egress IP and device state."
  else
    echo "Raw az login error output:"
    cat "$LOGIN_STDERR"
  fi

  rm -f "$LOGIN_STDERR"
  exit 1
fi
rm -f "$LOGIN_STDERR"
echo "az login: OK."

echo "== 4. Verifying subscription context =="
ACCT_JSON="$(az account show --subscription "$SUBSCRIPTION_ID" --output json || true)"
if [[ -z "$ACCT_JSON" ]]; then
  echo "[ERROR] Unable to see subscription $SUBSCRIPTION_ID. Check that this user is assigned to it."
  exit 1
fi

echo "$ACCT_JSON" | jq -r '"  Subscription: \(.name) (\(.id))\n  Tenant: \(.tenantId)"'

SIGNED_IN_ID="$(az ad signed-in-user show --query id -o tsv 2>/dev/null || true)"
if [[ -z "$SIGNED_IN_ID" ]]; then
  echo "[WARN] Could not resolve signed-in user object; skipping RBAC check."
else
  echo "== 5. Checking RBAC (Contributor on subscription) =="
  HAS_CONTRIB="$(az role assignment list \
    --assignee "$SIGNED_IN_ID" \
    --scope "/subscriptions/${SUBSCRIPTION_ID}" \
    --query "[?roleDefinitionName=='Contributor'] | length(@)" -o tsv)"

  if [[ "$HAS_CONTRIB" != "1" ]]; then
    echo "[ERROR] Signed-in user does not appear to have Contributor on subscription $SUBSCRIPTION_ID."
    echo "Ask your Azure admin to grant at least Contributor on this subscription (or the documented custom role)."
    exit 1
  fi
  echo "RBAC check: Contributor found on subscription."
fi

echo "== 6. Basic ARM call test =="
if ! az group list --subscription "$SUBSCRIPTION_ID" --top 1 >/dev/null 2>&1; then
  echo "[ERROR] ARM API call failed despite successful login. Check firewall/proxy rules."
  exit 1
fi

echo
echo "✅ Preflight checks PASSED: this jumpbox + user can log in with Azure CLI and has required access."
```

You can then extend this with any deployment‑specific checks (e.g. “can create a resource group in the target RG”, “can talk to AKS once created”, etc.).

---

## 3. How to Phrase the Requirement to customers/admins

In your **Azure Deployment Readiness Checklist** and in FFAPP‑4670, I’d make the requirement explicit:

- Customer must:
  - Run the provided **jumpbox preflight script** as the intended operator user.
  - If it fails on `az login`, capture the error page and send to their Entra admin.
- Entra admin must:
  - Use **Conditional Access What‑If** to confirm that:
    - User: `<FITFILE operator>`
    - App: “Microsoft Azure CLI” (`04b07795-8ddb-461a-bbee-02f9e1bf7b46`)
    - Location: `<jumpbox egress IP range>`
    - Device state: `Unregistered`
    - is *allowed* (or at least not blocked).

That combination lets them detect exactly the sort of 53003 / CA problem you hit at NNUH *before* you ever SSH into the box.

If you’d like, I can help you turn this into a more polished, customer‑facing “run_me_first.sh” plus a short one‑pager you can attach to pre‑deployment instructions.
