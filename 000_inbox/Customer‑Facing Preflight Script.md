---
aliases: []
confidence: 
created: 2025-12-09T09:47:28Z
epistemic: 
last_reviewed: 
modified: 2025-12-09T09:51:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Customer‑Facing Preflight Script
type: 
uid: 
updated: 
---

Here’s a polished version of the script plus a one‑pager you can drop straight into your pre‑deployment pack.

---

## 1. `run_me_first.sh` (customer‑facing Preflight script)

```bash
#!/usr/bin/env bash
#
# run_me_first.sh
#
# Azure jumpbox preflight check for FITFILE deployments.
#
# PURPOSE:
#   - Verify that the jumpbox user can log in to Azure using the Azure CLI.
#   - Confirm access to the correct subscription.
#   - Perform basic role and connectivity checks against Azure Resource Manager.
#
# RUN THIS:
#   - On the jumpbox / bastion host that will be used for deployment.
#   - As the same user account that will run the deployment.
#

set -u  # treat unset variables as an error

#########################
# Configuration & Input #
#########################

# You can pre-set these via environment variables, or the script will prompt.
TENANT_ID="${ARM_TENANT_ID:-${TENANT_ID:-}}"
SUBSCRIPTION_ID="${ARM_SUBSCRIPTION_ID:-${SUBSCRIPTION_ID:-}}"

REQUIRED_ROLE_NAMES=("Owner" "Contributor")  # adjust if you use a custom deployment role

#####################
# Helper functions  #
#####################

info()  { printf '\n[INFO] %s\n'  "$*"; }
warn()  { printf '\n[WARN] %s\n'  "$*" >&2; }
error() { printf '\n[ERROR] %s\n' "$*" >&2; exit 1; }

prompt_if_empty() {
  local var_name="$1"
  local prompt_text="$2"
  local current_value
  # shellcheck disable=SC2154
  current_value="${!var_name:-}"
  if [ -z "$current_value" ]; then
    read -r -p "$prompt_text: " current_value
    if [ -z "$current_value" ]; then
      error "$var_name cannot be empty."
    fi
    eval "$var_name=\"\$current_value\""
  fi
}

########################
# 0. Collect inputs    #
########################

info "Azure jumpbox preflight check (run_me_first.sh)"

prompt_if_empty "TENANT_ID" "Enter your Azure Tenant ID (GUID)"
prompt_if_empty "SUBSCRIPTION_ID" "Enter the target Subscription ID (GUID)"

info "Using:
  Tenant ID      : $TENANT_ID
  Subscription ID: $SUBSCRIPTION_ID"

##############################
# 1. Check Azure CLI is present
##############################

info "Checking Azure CLI is installed..."
if ! command -v az >/dev/null 2>&1; then
  error "Azure CLI (az) is not installed on this host.
Please ask your administrator to install the Azure CLI and re-run this script.
See: https://learn.microsoft.com/cli/azure/install-azure-cli"
fi

AZ_CLI_VERSION="$(az version --output json 2>/dev/null | sed -n 's/.*"azure-cli": "\(.*\)".*/\1/p')"
if [ -n "$AZ_CLI_VERSION" ]; then
  info "Azure CLI version: $AZ_CLI_VERSION"
else
  warn "Unable to detect Azure CLI version (this is not usually critical)."
fi

#############################################
# 2. Check basic network connectivity to Azure
#############################################

info "Checking network connectivity to Azure endpoints..."

for host in "login.microsoftonline.com" "management.azure.com"; do
  if ! curl -fsS "https://${host}" >/dev/null 2>&1; then
    error "Cannot reach https://${host} from this host.
This usually indicates a firewall or proxy issue.
Please ensure outbound HTTPS to this endpoint is allowed from the jumpbox."
  fi
  info "Reachable: https://${host}"
done

#############################################
# 3. Azure login (device code) & CA checks  #
#############################################

info "Clearing any existing Azure CLI login session..."
az account clear >/dev/null 2>&1 || true

info "Starting Azure login using device code flow..."
info "You will see a code in this terminal and be asked to open https://microsoft.com/devicelogin in a browser."

LOGIN_STDERR="$(mktemp)"
set +e  # handle login failure manually
az login --tenant "$TENANT_ID" --use-device-code 1>/dev/null 2>"$LOGIN_STDERR"
LOGIN_EXIT_CODE=$?
set -e

if [ $LOGIN_EXIT_CODE -ne 0 ]; then
  error_msg="az login failed (exit code $LOGIN_EXIT_CODE)."
  if grep -q "53003" "$LOGIN_STDERR"; then
    warn "The error appears to be related to Conditional Access (error code 53003).

Next steps:
  1. Capture a screenshot or copy of the full error details shown in your browser,
     including Correlation ID, Request ID, and Timestamp.
  2. Send these details to your Microsoft Entra ID (Azure AD) administrator.
  3. Ask them to verify Conditional Access for:
       - User: the account you used to log in
       - App: 'Microsoft Azure CLI' (App ID: 04b07795-8ddb-461a-bbee-02f9e1bf7b46)
       - Device: this jumpbox (typically an unregistered / non-compliant device)
       - Location: this jumpbox's public egress IP/range"
  else
    warn "Raw az login error output:"
    sed 's/^/  /' "$LOGIN_STDERR" >&2
  fi
  rm -f "$LOGIN_STDERR"
  error "$error_msg Please resolve the login issue and re-run this script."
fi

rm -f "$LOGIN_STDERR"
info "Azure CLI login succeeded."

###################################
# 4. Check subscription visibility #
###################################

info "Checking access to subscription: $SUBSCRIPTION_ID ..."
set +e
ACCOUNT_JSON="$(az account show --subscription "$SUBSCRIPTION_ID" --output json 2>/dev/null)"
ACCOUNT_EXIT_CODE=$?
set -e

if [ $ACCOUNT_EXIT_CODE -ne 0 ] || [ -z "$ACCOUNT_JSON" ]; then
  error "Unable to access subscription $SUBSCRIPTION_ID with the current login.
Please check:
  - The user is assigned to this subscription; and
  - Any required PIM (Privileged Identity Management) roles are activated.

After updating permissions, re-run this script."
fi

SUB_NAME="$(printf '%s' "$ACCOUNT_JSON" | sed -n 's/.*"name": "\(.*\)".*/\1/p')"
SUB_TENANT="$(printf '%s' "$ACCOUNT_JSON" | sed -n 's/.*"tenantId": "\(.*\)".*/\1/p')"

info "Subscription details:
  Name  : ${SUB_NAME:-unknown}
  ID    : $SUBSCRIPTION_ID
  Tenant: ${SUB_TENANT:-unknown}"

info "Setting Azure CLI context to this subscription..."
az account set --subscription "$SUBSCRIPTION_ID"

################################
# 5. Check RBAC (role) on sub  #
################################

info "Checking role assignments for the signed-in user on this subscription..."

set +e
SIGNED_IN_ID="$(az ad signed-in-user show --query id -o tsv 2>/dev/null)"
SIGNED_IN_UPN="$(az ad signed-in-user show --query userPrincipalName -o tsv 2>/dev/null)"
set -e

if [ -z "$SIGNED_IN_ID" ]; then
  warn "Could not retrieve signed-in user details from Microsoft Entra ID.
This may be due to directory restrictions. Skipping detailed RBAC check.

IMPORTANT: Ensure this user has at least one of these roles on the subscription:
  - ${REQUIRED_ROLE_NAMES[*]}
"
else
  info "Signed-in user: ${SIGNED_IN_UPN:-$SIGNED_IN_ID}"

  ROLE_FILTER="$(printf "%s" "${REQUIRED_ROLE_NAMES[@]}" | tr ' ' ',')"

  set +e
  ROLE_COUNT="$(az role assignment list \
    --assignee "$SIGNED_IN_ID" \
    --scope "/subscriptions/${SUBSCRIPTION_ID}" \
    --query "[?roleDefinitionName==\`Owner\` || roleDefinitionName==\`Contributor\`].roleDefinitionName | length(@)" \
    -o tsv 2>/dev/null)"
  set -e

  if [ -z "$ROLE_COUNT" ] || [ "$ROLE_COUNT" -eq 0 ]; then
    error "The signed-in user does not appear to have a required role on subscription $SUBSCRIPTION_ID.

Required roles (any one of):
  - ${REQUIRED_ROLE_NAMES[*]}

Please ask your Azure administrator to grant one of these roles (or your agreed custom deployment role),
then re-run this script."
  else
    info "RBAC check passed: the user has a suitable role on this subscription."
  fi
fi

####################################
# 6. Basic Azure Resource Manager  #
####################################

info "Verifying Azure Resource Manager API access..."
set +e
az group list --subscription "$SUBSCRIPTION_ID" --top 1 >/dev/null 2>&1
ARM_EXIT_CODE=$?
set -e

if [ $ARM_EXIT_CODE -ne 0 ]; then
  error "Azure Resource Manager API call failed despite a successful login.

This typically indicates:
  - Outbound HTTPS to management.azure.com is being blocked by a firewall or proxy; or
  - A network inspection device is interfering with TLS.

Please ask your network/security team to verify that this jumpbox can reach:
  https://management.azure.com
over HTTPS without interception that breaks TLS."
fi

###################
# 7. Final result #
###################

info "==============================================="
info "Preflight checks PASSED."

cat <<EOF

This jumpbox and user appear to be correctly configured for Azure CLI-based deployment.

What this means:
  - Azure CLI is installed and reachable.
  - The jumpbox can contact Microsoft login and management endpoints over HTTPS.
  - The user can sign in to Azure using device-code login for the specified tenant.
  - The user can access the specified subscription and holds an appropriate role.
  - Basic calls to Azure Resource Manager succeed from this host.

If FITFILE requests evidence, please:
  - Save the full terminal output of this script (including any WARN messages); and
  - Share it with your FITFILE contact.

You can now proceed with the FITFILE deployment steps.
EOF
```

---

## 2. One‑pager For pre‑deployment Instructions

You can paste this into Confluence, a PDF, or your onboarding pack as “Azure Jumpbox Preflight Check”.

---

### Azure Jumpbox Preflight Check – `run_me_first.sh`

#### 1. Purpose

Before FITFILE deploys infrastructure into your Azure environment, we need to confirm that:

- The **jumpbox / bastion host** can reach Azure over HTTPS.
- The **deployment user** can sign in with the Azure CLI.
- The user has the **correct access** to the target subscription.
- The Azure Resource Manager (ARM) API is reachable from your network.

The `run_me_first.sh` script performs these checks in a consistent, repeatable way so that issues can be identified and resolved **before** any deployment work starts.

---

#### 2. When to Run This Script

Run `run_me_first.sh`:

- On the **same jumpbox/bastion** that FITFILE will use for deployment.
- While logged in as the **same user account** that will perform the deployment.
- After:
  - Your Azure subscription has been created.
  - The deployment user account exists.
  - Any Conditional Access or security policies have been applied.

We recommend running it **at least once** before the first deployment, and again if any access or network policies change.

---

#### 3. What the Script Checks

The script performs the following steps:

1. **Collects basic details**
   - Asks for your **Tenant ID** and **Subscription ID** (or uses `ARM_TENANT_ID` / `ARM_SUBSCRIPTION_ID` if already set).

2. **Azure CLI availability**
   - Confirms the **Azure CLI (`az`) is installed** on the jumpbox.

3. **Network connectivity**
   - Verifies the jumpbox can reach:
     - `https://login.microsoftonline.com` (for sign‑in)
     - `https://management.azure.com` (for Azure Resource Manager)

4. **User sign‑in (device-code flow)**
   - Runs `az login --use-device-code` against your tenant.
   - Detects common Conditional Access issues (e.g. error code **53003**), and prints clear instructions for your Entra ID administrator if sign‑in is blocked.

5. **Subscription access**
   - Confirms the signed‑in user can **see and select** the specified subscription.
   - Displays the subscription name, ID, and tenant for verification.

6. **Role assignment (RBAC)**
   - Checks whether the user has a suitable role (by default: **Owner** or **Contributor**) on the subscription.
   - If not, it reports exactly what needs to be granted.

7. **Azure Resource Manager (ARM) API**
   - Makes a simple test call (`az group list`) to confirm ARM is reachable and not blocked by firewalls or proxies.

At the end, the script prints a clear **“PASSED”** or a specific, actionable **“ERROR”** message.

---

#### 4. How to Run it (customer steps)

1. **Copy the script to the jumpbox**

   Save the file as `run_me_first.sh` on the jumpbox (for example in your home directory).

2. **Make it executable**

   ```bash
   chmod +x run_me_first.sh
   ```

3. **Run the script**

   ```bash
   ./run_me_first.sh
   ```

4. **Provide Tenant and Subscription IDs**

   - When prompted, enter:
     - Your **Tenant ID** (GUID)
     - Your **Subscription ID** (GUID)

5. **Complete the device‑code login**

   - The script will show a code and ask you to open `https://microsoft.com/devicelogin`.
   - In your browser:
     - Enter the code.
     - Sign in with the **same user account** you are using on the jumpbox.

6. **Review the result**

   - If the script reports **“Preflight checks PASSED”**, you are ready for FITFILE deployment.
   - If the script reports an **error**, follow the guidance printed in the output and involve the relevant team (network, security, or Entra ID admin).

---

#### 5. Common Failure Scenarios and Who Should Act

- **Azure CLI not installed**
  - Message: Azure CLI (`az`) not found.
  - Action: Your **infrastructure/IT team** should install the Azure CLI on the jumpbox.
- **Network connectivity failure**
  - Message: Cannot reach `login.microsoftonline.com` or `management.azure.com`.
  - Action: Your **network/security team** should allow outbound HTTPS from the jumpbox to these endpoints (and ensure any proxies do not break TLS).
- **Login blocked by Conditional Access (error 53003)**
  - Message: Indicates a Conditional Access‑related error and requests that details be sent to your Entra admin.
  - Action (Entra admin):
    - Use **Conditional Access “What If”** to test:
      - User: the deployment operator
      - App: “Microsoft Azure CLI” (`04b07795-8ddb-461a-bbee-02f9e1bf7b46`)
      - Location: the jumpbox’s public IP / named location
      - Device state: Unregistered / non‑compliant
    - Adjust policies so this combination is **allowed** for deployment.
- **No access to subscription**
  - Message: “Unable to access subscription … with the current login.”
  - Action: Your **Azure subscription owner/admin** should ensure:
    - The user is assigned to the correct subscription.
    - Any Privileged Identity Management (PIM) roles are activated.
- **Insufficient role (RBAC)**
  - Message: User does not have any of: Owner / Contributor (or your agreed deployment role).
  - Action: Your **Azure admin** should grant an appropriate role on the subscription scope, then re‑run the script.
- **ARM API call fails**
  - Message: Basic ARM call failed despite successful login.
  - Action: Your **network/security team** should verify that outbound HTTPS to `management.azure.com` is allowed and not being intercepted or modified.

---

#### 6. What to Share with FITFILE

If requested, please:

- Copy and save the **full terminal output** from `run_me_first.sh` (including any warnings).
- Share this output with your FITFILE contact.

This allows FITFILE to confirm readiness quickly and, if needed, help diagnose any remaining issues before the deployment window.
