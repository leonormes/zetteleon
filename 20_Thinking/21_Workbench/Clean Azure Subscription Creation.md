---
captured: "2026-02-09T16:06:08+00:00 2026-02-09T16:06:08+00:00"
created: 2026-02-09T16:06:11+00:00
modified: 2026-02-09T16:59:37+00:00
source: "https://gemini.google.com/share/b7338dfcf705"
status: "processing"
tags: ["input"]
title: Clean Azure Subscription Creation
type: "head"
---

## Raw Output / Content

I have an azure tenant with management groups. I want to create a new subscriptions that is as clean as possible. How do I ensure nothing is inherited from partents

Based on the management group structure provided in your file, your environment follows a nested hierarchy where everything currently sits under the FITFILE management group, which is a child of the Tenant Root Group.

In Azure, inheritance for Azure Policy and RBAC (Role-Based Access Control) is additive and cannot be "blocked" at a lower level. If a policy is assigned at the "Tenant Root Group", it will apply to every subscription in the tenant.

To create a subscription that is as clean as possible and minimises inherited settings, you should follow these steps:

### 1\. Strategic Placement in the Hierarchy

Currently, your subscriptions are nested deep within the hierarchy (e.g., `Tenant Root Group > FITFILE > Landing Zones`). To ensure the cleanest start:

- Do not place it under "FITFILE": This group likely has policies or permissions specific to your organisational standards.
- Create a new Management Group: Create a new group (e.g., "Sandbox" or "Isolated") directly under the Tenant Root Group.
- Place the subscription there: By placing it directly under the root (or in a new sibling to "FITFILE"), it will only inherit what is applied at the absolute Root level, bypassing everything configured in "FITFILE", "Landing Zones", or "Platform".

### 2\. Manage Azure Policy Inheritance

You cannot "turn off" a parent policy, but you can bypass it using two methods:

- Policy Exemptions: Once the subscription is created, you can create an "Exemption" for specific policies that are inherited from the Root.
- Excluded Scopes: If you have access to the parent management group, you can edit the policy assignment and add your new subscription to the "Excluded scopes" list. This prevents the policy from ever touching that subscription.

### 3\. Review RBAC Assignments

Permissions at the "Tenant Root Group" will flow down to your new subscription.

- Check who has roles like _Owner_, _Contributor_, or _User Access Administrator_ at the Root level.
- If you need a truly "clean" environment, ensure that administrative access at the Root is restricted to a minimal number of "Break-glass" accounts or managed via Privileged Identity Management (PIM) so that permissions are not persistent.

### 4\. Avoid Automated "Vending"

If your organisation uses an automated subscription vending process (like Terraform or Bicep modules that automatically apply "Landing Zone" defaults), ensure you create this subscription manually or via a script that does not include those standard "baseline" modules.

### Summary of Your Current Structure

| Level | Name | Recommendation |
| --- | --- | --- |
| Parent | Tenant Root Group | Inherited by ALL. Minimise assignments here. |
| Child | FITFILE | Avoid. Contains your existing organisational logic. |
| New Path | Clean-MG | Create this. Attach your new subscription here. |

By creating a new management group at the same level as FITFILE, you isolate the new subscription from any configurations applied to your existing "Landing Zones" or "Platform" environments.

can I just create a sub under Tenant Root Group or do I need MG

Yes, you can create a subscription directly under the Tenant Root Group. However, there are a few technical factors to consider regarding how "clean" that subscription will actually be:

### 1\. Mandatory Parentage

Every Azure subscription must reside within a management group. If you create a subscription and do not specify a parent, Azure will automatically place it in the Default Management Group configured for your tenant. By default, this is the Tenant Root Group unless it has been manually changed in the management group settings.

### 2\. Global Inheritance

The Tenant Root Group is the absolute top level of the hierarchy. Any Azure Policy assignments or RBAC (Role-Based Access Control) roles applied at the Root level will be inherited by the new subscription.

- You cannot block inheritance from a parent management group.
- The only way to ensure the subscription is "clean" is to ensure the Tenant Root Group itself has minimal or no assignments.

### 3\. Isolation from Other Branches

Placing a subscription directly under the Tenant Root Group is an effective way to isolate it from policies applied to other branches (like your existing "FITFILE" or "Landing Zones" groups). It will only inherit:

- Assignments made at the Tenant Root Group.
- Azure default roles and provider registrations.

### 4\. Management Group vs. Direct Root

While you can put a subscription directly under the Root, it is generally recommended to create a dedicated Management Group (e.g., "Sandbox" or "Isolated") directly under the Root and place the subscription there instead.

Why use a Management Group instead of the Root?

- Organisation: It keeps the Root level tidy and prevents a long list of individual subscriptions from cluttering the top level.
- Future-Proofing: If you decide later that you need a specific policy for "clean" subscriptions (e.g., restricted regions), you can apply it to that specific Management Group rather than having to apply it to each subscription individually or to the entire Root.
- Deployment: Many infrastructure-as-code templates expect a management group structure and can be easier to manage when subscriptions are grouped.

Recommendation: If you want the subscription to be as isolated as possible, create a new Management Group at the same level as your existing organisational groups (under the Root) and place your subscription there. This avoids inheriting your company's standard landing zone policies while still following a structured management approach.

We created a sandbox MG but it says it doesn't have permissions to create subscriptions

When creating a new Azure subscription within a specific management group, permissions are required in two separate areas: the Management Group hierarchy and the Billing hierarchy. A failure in either will prevent the subscription from being created or associated correctly.

Here are the primary reasons you might see a permission error and how to resolve them:

### 1\. Lack of Billing Permissions (Most Common)

Management groups control policy and access, but they do not provide the "right" to create a subscription that incurs costs. You must have a specific role on the billing account that will pay for the subscription.

- For Microsoft Customer Agreements (MCA): You need the Owner or Contributor role on a Billing Invoice Section. Without this, the "Create" button is often greyed out or returns a "Not Authorized" error.
- For Enterprise Agreements (EA): You must be an Account Owner on an active Enrollment Account.
- For Microsoft Online Service Program (PAYG): You must be the Account Administrator.

To check: Navigate to Cost Management + Billing > Billing scopes and verify your role at the Invoice Section or Enrollment level.

### 2\. Lack of Management Group Permissions

To place a subscription into a specific management group, you need permission to "write" to that group.

- Required Role: You must have the Owner or Contributor role on the specific Management Group where you want the subscription to reside.
- Specific Permission: The underlying action required is `Microsoft.Management/managementGroups/subscriptions/write`.

To check: Go to the Management Groups blade, select your new MG, and check Access Control (IAM) to ensure your account is listed with sufficient privileges.

### 3\. Resource Provider Registration

The subscription creation process relies on the `Microsoft.Subscription` resource provider. If this is not registered in the tenant or accessible to your account, the request may fail.

- In the Azure Portal, search for Subscriptions, select any existing subscription, and check Resource providers. Ensure `Microsoft.Subscription` is registered. (Note: This is usually a tenant-wide requirement for the creation API).

### 4\. "Default Management Group" Constraints

If you are creating a subscription without explicitly defining a parent MG during the creation process, Azure attempts to put it in the Default Management Group.

- If your account does not have permissions on the "Default Management Group," the creation will fail even if you have permissions on the "Sandbox" MG you intended to use.
- Solution: Ensure you are selecting the specific "Sandbox" MG as the Parent Management Group in the "Basics" tab during the subscription creation workflow.

### Summary Checklist

1. Billing: Do you have a role (Owner/Contributor) on a Billing Invoice Section?
2. Management Group: Do you have a role (Owner/Contributor) on the target MG?
3. Scope: Are you selecting the correct Billing Account and Parent Management Group in the creation form?

I am having problems creating the sub. it says one already exists but I can't see it in the portal. What are the az commands to find out about MG and subs and my permissions related to them

To investigate why you cannot see the subscription and why Azure claims one already exists, you can use the following Azure CLI (`az`) commands.

Since you are working within a structured hierarchy (as seen in your `generated.csv`), these commands will help you identify where the "missing" subscription might be hiding and what permissions you actually have.

### 1\. Find the "Missing" Subscription

If you get an error saying a subscription "already exists" but you cannot see it, it is often because of a "Subscription Alias" (a name reserved during the creation process) or because it is disabled/filtered out.

- List every subscription your account has any access to:
	_Check the `State` column. If it says `Disabled`, it won't show in your default portal view._
- Check for Subscription Aliases:When you create a subscription, Azure often creates an "alias". If a previous attempt failed or is stuck, the name might be taken here.

### 2\. Inspect the Management Group (MG) Hierarchy

To see exactly what is inside your new "Sandbox" MG and verify its ID:

- List all Management Groups:
- See everything inside a specific MG (including hidden subs):Replace `<Sandbox_MG_ID>` with the ID of the group you created.
	_Look at the `children` array in the JSON output. This will list every subscription currently attached to that group._

### 3\. Check Your Permissions

The "Not Authorised" status seen in your CSV for the Root Group suggests your permissions might be restricted at higher levels.

- Check your roles on the Sandbox Management Group:
- Check your permissions on the Billing Account:As mentioned before, you need billing permissions to create the sub.

### 4\. Why You Might not See it in the Portal

If the `az account list --all` command shows the subscription but the Portal does not:

1. Global Subscription Filter: In the Azure Portal, click the Directory + Subscription filter icon (top right, looks like a funnel or a folder with a gear) and click "Select All".
2. Directory Switch: Ensure you haven't accidentally created the subscription in a different Tenant (if your account belongs to multiple). Use `az account show` to see your current tenant context.

### Common "Already Exists" Cause

If you are using Terraform or Bicep to create the subscription, the "already exists" error usually refers to the Subscription Alias name. If a previous deployment was interrupted, you might need to manually delete the alias:

az account list --all --output table

Name CloudName SubscriptionId TenantId State IsDefault

\----------------------- ----------- ------------------------------------ ------------------------------------ ------- -----------

FitFileLZ AzureCloud d1043e25-5695-4d25-b658-456f3ac3e91e dbb3517b-09e6-4a76-9aa9-d7d72b1073e7 Enabled False

FITCloud Production AzureCloud a448d869-4ec5-4c81-82c5-d6e8fa0ec0df 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled False

FITCloud Non-Production AzureCloud 249df46b-f75d-4492-8e78-b33a00473548 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled False

Shared Services AzureCloud a085dd04-19aa-4d2b-9a35-e438097d84fc 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled True

Management AzureCloud a9602426-e496-44d1-ba89-8e5fc756a06b 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled False

Identity AzureCloud c1c459c8-a99f-4f7a-891b-a98d49cf12c0 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled False

NNUHFT-SDE AzureCloud 4ae8fd93-d084-481f-ba6e-370b7d4d8d0d d2a06081-6719-4548-bdc7-fff8bfd24f56 Enabled False

…/central-services/grafana on  master $! on ⛵ fitfile-cloud-testing-aks-cluster (testing) on ☁️ Shared Services on 🅰 (eu-west-2) at 14:26:28

❯ az account alias list --output table

Preview version of extension is disabled by default for extension installation, enabled for modules without stable versions.

Please run 'az config set extension.dynamic\_install\_allow\_preview=true or false' to config it specifically.

The command requires the extension account. Do you want to install it now? The command will continue to run after the extension is installed. (Y/n): y

Run 'az config set extension.use\_dynamic\_install=yes\_without\_prompt' to allow installing extensions without prompt.

An error occurred. Pip failed with status code 1. Use --debug for more information.

…/central-services/grafana on  master $! on ⛵ fitfile-cloud-testing-aks-cluster (testing) on ☁️ Shared Services on 🅰 (eu-west-2) at 14:27:07

❯ az account management-group list --output table

DisplayName Name TenantId

\------------- ------------- ------------------------------------

FITFILE FITFILE 45e73aa3-1ee9-47c0-ba25-54eda9da021a

Landing Zones LANDING-ZONES 45e73aa3-1ee9-47c0-ba25-54eda9da021a

Platform PLATFORM 45e73aa3-1ee9-47c0-ba25-54eda9da021a

…/central-services/grafana on  master $! on ⛵ fitfile-cloud-testing-aks-cluster (testing) on ☁️ Shared Services on 🅰 (eu-west-2) at 14:27:34

❯ az account management-group show --name <Sandbox\_MG\_ID> --expand --output json

zsh: no such file or directory: Sandbox\_MG\_ID

…/central-services/grafana on  master $! on ⛵ fitfile-cloud-testing-aks-cluster (testing) on ☁️ Shared Services on 🅰 (eu-west-2) at 14:27:36

❯ az account management-group show --name sandbox --expand --output json

(AuthorizationFailed) The client 'leon.ormes@fitfile.com' with object id '053a0abe-0b3e-40a3-85c8-83f2af887382' does not have authorization to perform action 'Microsoft.Management/managementGroups/read' over scope '/providers/Microsoft.Management/managementGroups/sandbox' or the scope is invalid. If access was recently granted, please refresh your credentials.

Code: AuthorizationFailed

Message: The client 'leon.ormes@fitfile.com' with object id '053a0abe-0b3e-40a3-85c8-83f2af887382' does not have authorization to perform action 'Microsoft.Management/managementGroups/read' over scope '/providers/Microsoft.Management/managementGroups/sandbox' or the scope is invalid. If access was recently granted, please refresh your credentials.

The outputs you provided reveal a few key issues: you are currently working across multiple tenants, the "Sandbox" management group does not appear to exist in your current context, and your Azure CLI is missing a required extension.

Here is how to resolve the "already exists" error and locate your missing resources.

### 1\. The "Sandbox" Management Group is Missing

Look at the output of your `az account management-group list`. It only shows FITFILE, Landing Zones, and Platform. The management group "sandbox" is not listed.

When you ran `az account management-group show --name sandbox`, the error "the scope is invalid" confirms that Azure cannot find a management group with that ID in your current tenant (`45e73aa3…`). You must create the management group before you can move a subscription into it.

To create the Management Group:

### 2\. Multi-Tenant Confusion

Your `az account list` shows you have access to three different tenants:

- `dbb3517b…` (FitFileLZ)
- `45e73aa3…` (Your primary tenant)
- `d2a06081…` (NNUHFT-SDE)

If you created a subscription in the Portal, it may have been created in the wrong tenant. Check the other tenants using these commands:

### 3\. Fixing the "Already Exists" Error (The Alias)

The "already exists" error usually refers to a Subscription Alias. When you try to create a subscription, Azure reserves that name as an alias. If the process crashed, the name is "taken" even if the subscription isn't visible.

Your previous attempt to list aliases failed because the `account` extension didn't install. Try installing it manually first:

If you see an alias in that list with the name you are trying to use, delete it to "free up" the name:

### 4\. Check for Hidden or Deleted Subscriptions

If the alias list is empty but it still says it exists, it might be a subscription that was recently deleted (and is in a "Deleted" state) or one where you lack "Read" permissions but have "Billing" permissions.

Run this command to see absolutely every subscription associated with your billing account, regardless of your RBAC permissions:

### Recommended Next Steps

1. Fix the extension: Run `az extension add --name account`.
2. Check Aliases: Run `az account alias list` to find the "ghost" subscription.
3. Verify MG: Create the `sandbox` management group if it is indeed missing from your `az account management-group list` output.
4. Check Portal Filters: In the Azure Portal, ensure your "Directory + Subscription" filter is set to include all directories and all subscriptions.

az account alias list --output table --debug

cli.knack.cli: Command arguments: \['account', 'alias', 'list', '--output', 'table', '--debug'\]

cli.knack.cli: \_\_init\_\_ debug log:

Enable color in terminal.

cli.knack.cli: Event: Cli.PreExecute \[\]

cli.knack.cli: Event: CommandParser.OnGlobalArgumentsCreate \[<function CLILogging.on\_global\_arguments at 0x1036e62a0>, <function OutputProducer.on\_global\_arguments at 0x10388e340>, <function CLIQuery.on\_global\_arguments at 0x1038cfc40>\]

cli.knack.cli: Event: CommandInvoker.OnPreCommandTableCreate \[\]

cli.azure.cli.core: Modules found from index for 'account': \['azure.cli.command\_modules.profile', 'azure.cli.command\_modules.resource'\]

cli.azure.cli.core: Loading command modules:

cli.azure.cli.core: Name Load Time Groups Commands

cli.azure.cli.core: profile 0.002 2 8

cli.azure.cli.core: resource 0.092 52 234

cli.azure.cli.core: Total (2) 0.094 54 242

cli.azure.cli.core: These extensions are not installed and will be skipped: \['azext\_ai\_examples', 'azext\_next'\]

cli.azure.cli.core: Loading extensions:

cli.azure.cli.core: Name Load Time Groups Commands Directory

cli.azure.cli.core: Total (0) 0.000 0 0

cli.azure.cli.core: Loaded 53 groups, 242 commands.

cli.azure.cli.core: Could not find a match in the command or command group table for 'account alias list'. The index may be outdated.

cli.azure.cli.core: Loading all modules and extensions

cli.azure.cli.core: Discovered command modules: \['acr', 'acs', 'advisor', 'ams', 'apim', 'appconfig', 'appservice', 'aro', 'backup', 'batch', 'batchai', 'billing', 'botservice', 'cdn', 'cloud', 'cognitiveservices', 'compute\_recommender', 'computefleet', 'config', 'configure', 'consumption', 'container', 'containerapp', 'cosmosdb', 'databoxedge', 'dls', 'dms', 'eventgrid', 'eventhubs', 'extension', 'feedback', 'find', 'hdinsight', 'identity', 'interactive', 'iot', 'keyvault', 'lab', 'managedservices', 'maps', 'marketplaceordering', 'monitor', 'mysql', 'netappfiles', 'network', 'policyinsights', 'postgresql', 'privatedns', 'profile', 'rdbms', 'redis', 'relay', 'resource', 'role', 'search', 'security', 'servicebus', 'serviceconnector', 'servicefabric', 'signalr', 'sql', 'sqlvm', 'storage', 'synapse', 'util', 'vm'\]

cli.azure.cli.core: Loading command modules:

cli.azure.cli.core: Name Load Time Groups Commands

cli.azure.cli.core: acr 0.007 36 149

cli.azure.cli.core: acs 0.057 18 96

cli.azure.cli.core: advisor 0.001 3 6

cli.azure.cli.core: ams 0.003 22 100

cli.azure.cli.core: apim 0.003 14 69

cli.azure.cli.core: appconfig 0.001 9 47

cli.azure.cli.core: appservice 0.018 88 299

cli.azure.cli.core: aro 0.006 1 10

cli.azure.cli.core: backup 0.002 17 65

cli.azure.cli.core: batch 0.017 32 96

cli.azure.cli.core: batchai 0.001 10 30

cli.azure.cli.core: billing 0.009 20 53

cli.azure.cli.core: botservice 0.002 12 42

cli.azure.cli.core: cdn 0.075 8 50

cli.azure.cli.core: cloud 0.001 1 7

cli.azure.cli.core: cognitiveservices 0.002 15 59

cli.azure.cli.core: compute\_recommender 0.002 1 1

cli.azure.cli.core: computefleet 0.005 1 1

cli.azure.cli.core: config 0.001 2 7

cli.azure.cli.core: configure 0.001 2 5

cli.azure.cli.core: consumption 0.009 8 9

cli.azure.cli.core: container 0.005 2 17

cli.azure.cli.core: containerapp 0.053 39 132

cli.azure.cli.core: cosmosdb 0.020 61 213

cli.azure.cli.core: databoxedge 0.005 2 2

cli.azure.cli.core: dls 0.001 6 36

cli.azure.cli.core: dms 0.001 3 22

cli.azure.cli.core: eventgrid 0.002 25 96

cli.azure.cli.core: eventhubs 0.007 14 21

cli.azure.cli.core: extension 0.001 1 7

cli.azure.cli.core: feedback 0.000 1 2

cli.azure.cli.core: find 0.001 1 1

cli.azure.cli.core: hdinsight 0.005 10 45

cli.azure.cli.core: identity 0.005 2 8

cli.azure.cli.core: interactive 0.000 1 1

cli.azure.cli.core: iot 0.039 18 81

cli.azure.cli.core: keyvault 0.004 20 114

cli.azure.cli.core: lab 0.015 9 30

cli.azure.cli.core: managedservices 0.005 3 8

cli.azure.cli.core: maps 0.001 4 8

cli.azure.cli.core: marketplaceordering 0.003 1 2

cli.azure.cli.core: monitor 0.278 17 64

cli.azure.cli.core: mysql 0.051 16 57

cli.azure.cli.core: netappfiles 0.025 8 15

cli.azure.cli.core: network 0.103 107 352

cli.azure.cli.core: policyinsights 0.006 9 17

cli.azure.cli.core: postgresql 0.022 20 87

cli.azure.cli.core: privatedns 0.010 14 60

cli.azure.cli.core: profile 0.000 2 8

cli.azure.cli.core: rdbms 0.023 22 90

cli.azure.cli.core: redis 0.001 7 38

cli.azure.cli.core: relay 0.012 7 8

cli.azure.cli.core: resource 0.003 52 234

cli.azure.cli.core: role 0.001 17 62

cli.azure.cli.core: search 0.007 8 20

cli.azure.cli.core: security 0.005 48 98

cli.azure.cli.core: servicebus 0.005 13 16

cli.azure.cli.core: serviceconnector 0.047 20 331

cli.azure.cli.core: servicefabric 0.010 27 80

cli.azure.cli.core: signalr 0.001 10 42

cli.azure.cli.core: sql 0.008 56 219

cli.azure.cli.core: sqlvm 0.020 4 20

cli.azure.cli.core: storage 0.026 62 279

cli.azure.cli.core: synapse 0.005 54 246

cli.azure.cli.core: util 0.001 3 7

cli.azure.cli.core: vm 0.107 60 207

cli.azure.cli.core: Total (66) 1.172 1206 4704

cli.azure.cli.core: Loading extensions:

cli.azure.cli.core: Name Load Time Groups Commands Directory

cli.azure.cli.core: bastion 0.005 2 4 /Users/leon.ormes/.azure/cliextensions/bastion

cli.azure.cli.core: costmanagement 0.003 2 6 /Users/leon.ormes/.azure/cliextensions/costmanagement

cli.azure.cli.core: dataprotection 0.024 11 40 /Users/leon.ormes/.azure/cliextensions/dataprotection

cli.azure.cli.core: k8s-extension 0.007 2 17 /Users/leon.ormes/.azure/cliextensions/k8s-extension

cli.azure.cli.core: ssh 0.009 1 4 /Users/leon.ormes/.azure/cliextensions/ssh

cli.azure.cli.core: Total (5) 0.048 18 71

cli.azure.cli.core: Loaded 1209 groups, 4775 commands.

cli.azure.cli.core: Updated command index in 0.002 seconds.

cli.knack.cli: Event: CommandInvoker.OnPreCommandTableTruncate \[<function AzCliLogging.init\_command\_file\_logging at 0x10914c2c0>\]

cli.azure.cli.core.azlogging: metadata file logging enabled - writing logs to '/Users/leon.ormes/.azure/commands/2026-02-09.14-30-44.account.15310.log'.

az\_command\_data\_logger: command args: account {} {} --output {} --debug

cli.knack.cli: Event: CommandInvoker.OnPreArgumentLoad \[<function register\_global\_subscription\_argument.<locals>.add\_subscription\_parameter at 0x109198540>\]

cli.knack.cli: Event: CommandInvoker.OnPostArgumentLoad \[\]

cli.knack.cli: Event: CommandInvoker.OnPostCommandTableCreate \[<function register\_ids\_argument.<locals>.add\_ids\_arguments at 0x10919bd80>, <function register\_cache\_arguments.<locals>.add\_cache\_arguments at 0x10919bf60>, <function register\_upcoming\_breaking\_change\_info.<locals>.update\_breaking\_change\_info at 0x1091d8040>\]

cli.knack.cli: Event: CommandInvoker.OnCommandTableLoaded \[\]

cli.knack.cli: Event: CommandInvoker.OnPreParseArgs \[<function \_documentdb\_deprecate at 0x10b135300>\]

cli.azure.cli.core.extension.dynamic\_install: Preview version of extension is disabled by default for extension installation, enabled for modules without stable versions.

cli.azure.cli.core.extension.dynamic\_install: Please run 'az config set extension.dynamic\_install\_allow\_preview=true or false' to config it specifically.

The command requires the extension account. Do you want to install it now? The command will continue to run after the extension is installed. (Y/n):

cli.azure.cli.core.extension.dynamic\_install: Run 'az config set extension.use\_dynamic\_install=yes\_without\_prompt' to allow installing extensions without prompt.

urllib3.connectionpool: Starting new HTTPS connection (1): aka.ms:443

urllib3.connectionpool: <https://aka.ms:443> "GET /azure-cli-extension-index-v1 HTTP/1.1" 301 0

urllib3.connectionpool: Starting new HTTPS connection (1): azcliextensionsync.blob.core.windows.net:443

urllib3.connectionpool: <https://azcliextensionsync.blob.core.windows.net:443> "GET /index1/index.json HTTP/1.1" 200 4511160

cli.azure.cli.core.extension.\_resolve: Candidates \['account-0.1.0-py2.py3-none-any.whl', 'account-0.2.0-py2.py3-none-any.whl', 'account-0.2.1-py3-none-any.whl', 'account-0.2.4-py3-none-any.whl', 'account-0.2.5-py3-none-any.whl'\]

cli.azure.cli.core.extension.\_resolve: Candidates \['account-0.1.0-py2.py3-none-any.whl', 'account-0.2.0-py2.py3-none-any.whl', 'account-0.2.1-py3-none-any.whl', 'account-0.2.4-py3-none-any.whl', 'account-0.2.5-py3-none-any.whl'\]

cli.azure.cli.core.extension.\_resolve: Candidates \['account-0.2.4-py3-none-any.whl', 'account-0.2.5-py3-none-any.whl'\]

cli.azure.cli.core.extension.\_resolve: Candidates \['account-0.2.4-py3-none-any.whl', 'account-0.2.5-py3-none-any.whl'\]

cli.azure.cli.core.extension.\_resolve: Candidates \['account-0.2.4-py3-none-any.whl', 'account-0.2.5-py3-none-any.whl'\]

cli.azure.cli.core.extension.\_resolve: Chosen {'downloadUrl': 'https://azcliprod.blob.core.windows.net/cli-extensions/account-0.2.5-py3-none-any.whl', 'filename': 'account-0.2.5-py3-none-any.whl', 'metadata': {'azext.minCliCoreVersion': '2.38.0', 'classifiers': \['Development Status:: 4 - Beta', 'Intended Audience:: Developers', 'Intended Audience:: System Administrators', 'Programming Language:: Python', 'Programming Language:: Python:: 3', 'Programming Language:: Python:: 3.6', 'Programming Language:: Python:: 3.7', 'Programming Language:: Python:: 3.8', 'License:: OSI Approved:: MIT License'\], 'extensions': {'python.details': {'contacts': \[{'email': 'azpycli@microsoft.com', 'name': 'Microsoft Corporation', 'role': 'author'}\], 'document\_names': {'description': 'DESCRIPTION.rst'}, 'project\_urls': {'Home': 'https://github.com/Azure/azure-cli-extensions/tree/main/src/account'}}}, 'generator': 'bdist\_wheel (0.30.0)', 'license': 'MIT', 'metadata\_version': '2.0', 'name': 'account', 'summary': 'Microsoft Azure Command-Line Tools SubscriptionClient Extension', 'version': '0.2.5'}, 'sha256Digest': '0b94df323acfc48ea3141904649106bb85695187dbf63aa3b8448ec12bc00c23'}

cli.azure.cli.core.extension.operations: Extension source is url? True

cli.azure.cli.core.extension.operations: Downloading <https://azcliprod.blob.core.windows.net/cli-extensions/account-0.2.5-py3-none-any.whl> to /var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/tmpf27hpg6\_/account-0.2.5-py3-none-any.whl

urllib3.connectionpool: Starting new HTTPS connection (1): azcliprod.blob.core.windows.net:443

urllib3.connectionpool: <https://azcliprod.blob.core.windows.net:443> "GET /cli-extensions/account-0.2.5-py3-none-any.whl HTTP/1.1" 200 87386

cli.azure.cli.core.extension.operations: Downloaded to /var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/tmpf27hpg6\_/account-0.2.5-py3-none-any.whl

cli.azure.cli.core.extension.operations: Validating the extension /var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/tmpf27hpg6\_/account-0.2.5-py3-none-any.whl

cli.azure.cli.core.extension.operations: Checksum of /var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/tmpf27hpg6\_/account-0.2.5-py3-none-any.whl is OK

cli.azure.cli.core.extension.operations: Validation successful on /var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/tmpf27hpg6\_/account-0.2.5-py3-none-any.whl

cli.azure.cli.core.extension.operations: Linux distro check: Reading from: /etc/apt/sources.list.d/azure-cli.list

cli.azure.cli.core.extension.operations: Linux distro check: An error occurred while checking linux distribution version source list consistency.

cli.azure.cli.core.extension.operations: \[Errno 2\] No such file or directory: '/etc/apt/sources.list.d/azure-cli.list'

cli.azure.cli.core.extension.operations: Executing pip with args: \['install', '--target', '/Users/leon.ormes/.azure/cliextensions/account', '/var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/tmpf27hpg6\_/account-0.2.5-py3-none-any.whl'\]

cli.azure.cli.core.extension.operations: Running: \['/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/bin/python', '-m', 'pip', 'install', '--target', '/Users/leon.ormes/.azure/cliextensions/account', '/var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/tmpf27hpg6\_/account-0.2.5-py3-none-any.whl', '--disable-pip-version-check', '--no-cache-dir'\]

cli.azure.cli.core.extension.operations: /Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/bin/python: No module named pip

cli.azure.cli.core.extension.operations: Command '\['/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/bin/python', '-m', 'pip', 'install', '--target', '/Users/leon.ormes/.azure/cliextensions/account', '/var/folders/8x/xzwf8sdd1jnf3v2gpkw8hk000000gr/T/tmpf27hpg6\_/account-0.2.5-py3-none-any.whl', '--disable-pip-version-check', '--no-cache-dir'\]' returned non-zero exit status 1.

cli.azure.cli.core.extension.operations: Pip failed so deleting anything we might have installed at /Users/leon.ormes/.azure/cliextensions/account

cli.azure.cli.core.azclierror: Traceback (most recent call last):

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/knack/cli.py", line 233, in invoke

cmd\_result = self.invocation.execute(args)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/commands/\_\_init\_\_.py", line 593, in execute

parsed\_args = self.parser.parse\_args(args)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/knack/parser.py", line 261, in parse\_args

return super().parse\_args(args)

^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 1904, in parse\_args

args, argv = self.parse\_known\_args(args, namespace)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/parser.py", line 281, in parse\_known\_args

self.\_namespace, self.\_raw\_arguments = super().parse\_known\_args(args=args, namespace=namespace)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 1914, in parse\_known\_args

return self.\_parse\_known\_args2(args, namespace, intermixed=False)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 1943, in \_parse\_known\_args2

namespace, args = self.\_parse\_known\_args(args, namespace, intermixed)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 2165, in \_parse\_known\_args

positionals\_end\_index = consume\_positionals(start\_index)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 2141, in consume\_positionals

take\_action(action, args)

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 2018, in take\_action

action(self, namespace, argument\_values, option\_string)

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 1272, in \_\_call\_\_

subnamespace, arg\_strings = parser.parse\_known\_args(arg\_strings, None)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/parser.py", line 281, in parse\_known\_args

self.\_namespace, self.\_raw\_arguments = super().parse\_known\_args(args=args, namespace=namespace)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 1914, in parse\_known\_args

return self.\_parse\_known\_args2(args, namespace, intermixed=False)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 1943, in \_parse\_known\_args2

namespace, args = self.\_parse\_known\_args(args, namespace, intermixed)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 2165, in \_parse\_known\_args

positionals\_end\_index = consume\_positionals(start\_index)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 2141, in consume\_positionals

take\_action(action, args)

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 2003, in take\_action

argument\_values = self.\_get\_values(action, argument\_strings)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/parser.py", line 272, in \_get\_values

value = super().\_get\_values(action, arg\_strings)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/argparse.py", line 2523, in \_get\_values

self.\_check\_value(action, value\[0\])

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/parser.py", line 300, in \_check\_value

use\_dynamic\_install = try\_install\_extension(self, args)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/extension/dynamic\_install.py", line 132, in try\_install\_extension

\_check\_value\_in\_extensions(cli\_ctx, parser, args, use\_dynamic\_install == 'yes\_without\_prompt')

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/extension/dynamic\_install.py", line 244, in \_check\_value\_in\_extensions

add\_extension(cli\_ctx=cli\_ctx, extension\_name=ext\_name, upgrade=True, allow\_preview=extension\_allow\_preview)

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/extension/operations.py", line 343, in add\_extension

extension\_name = \_add\_whl\_ext(cli\_ctx=cmd\_cli\_ctx, source=source, ext\_sha256=ext\_sha256,

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/core/extension/operations.py", line 172, in \_add\_whl\_ext

raise CLIError('An error occurred. Pip failed with status code {}. '

knack.util.CLIError: An error occurred. Pip failed with status code 1. Use --debug for more information.

cli.azure.cli.core.azclierror: An error occurred. Pip failed with status code 1. Use --debug for more information.

az\_command\_data\_logger: An error occurred. Pip failed with status code 1. Use --debug for more information.

cli.knack.cli: Event: Cli.PostExecute \[<function AzCliLogging.deinit\_cmd\_metadata\_logging at 0x10914c540>\]

az\_command\_data\_logger: exit code: 1

cli.\_\_main\_\_: Command ran in 6.983 seconds (init: 0.087, invoke: 6.896)

telemetry.main: Begin splitting cli events and extra events, total events: 1

telemetry.client: Accumulated 0 events. Flush the clients.

telemetry.main: Finish splitting cli events and extra events, cli events: 1

telemetry.save: Save telemetry record of length 4204 in cache

telemetry.main: Begin creating telemetry upload process.

telemetry.process: Creating upload process: "/Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/bin/python /Users/leon.ormes/.local/share/mise/installs/azure-cli/2.83.0/azure-cli/lib/python3.12/site-packages/azure/cli/telemetry/\_\_init\_\_.py /Users/leon.ormes/.azure"

telemetry.process: Return from creating process

telemetry.main: Finish creating telemetry upload process.

The debug log shows that your Azure CLI environment is broken; specifically, the Python environment managed by mise is missing `pip`, which prevents the CLI from installing the `account` extension needed for the `alias` command.

Since you cannot currently use `az account alias list`, use these alternative methods to find your "ghost" subscription and fix the "already exists" error.

### 1\. Find the Subscription via Billing (No Extension needed)

Your logs show the `billing` module is already loaded. You can query your billing account directly to see every subscription tied to it, even those not currently visible in your management group tree.

Run this to list subscriptions by billing scope:

_If the subscription appears here, note the Subscription ID. It likely exists but is not currently assigned to a Management Group._

### 2\. Search by Name (Direct Resource Query)

If you know the name you tried to give the subscription, you can check if a "Subscription Alias" exists using a generic resource graph query:

### 3\. Clear the "Already Exists" Error in the Portal

Since your CLI is having environment issues, the most reliable way to fix the "name already exists" error (which is almost always a stuck Subscription Alias) is via the Azure Portal:

1. Search for "Subscriptions" in the top search bar.
2. On the left-hand menu, look for "Subscription Aliases" (usually under the Billing section or by searching specifically for "Aliases").
3. If you see an entry with the name you've been trying to use, delete it. This releases the name so you can try the creation again.

### 4\. Fixing Your CLI Environment

The error `No module named pip` indicates your mise installation of `azure-cli` is incomplete. To fix the CLI so you can use extensions again:

### Summary of Your Management Group Status

Based on your previous `az account management-group list` output, the "sandbox" group still does not exist in your tenant. Before you try to create the subscription again:

1. Create the MG:`az account management-group create --name "sandbox" --display-name "Sandbox"`
2. Verify it exists:`az account management-group show --name "sandbox"`
3. Then attempt the subscription creation, ensuring you point to the `sandbox` ID as the parent.

how can I create a sub using terraform azuread provider

To create a subscription using Terraform, you primarily use the `azurerm` provider rather than the `azuread` provider. While the `azuread` provider manages identities (users, groups, and service principals), the `azurerm` provider is responsible for creating and managing Azure resources, including subscriptions.

However, you often use both together: the `azuread` provider to manage the service principal that runs the code, and the `azurerm` provider to create the subscription and assign it to your Sandbox management group.

### Terraform Configuration

The following example demonstrates how to create a new subscription and immediately associate it with your "sandbox" management group.

Terraform

```markdown
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.0"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "azuread" {}

# 1. Look up your billing scope (MCA example)
data "azurerm_billing_mca_account_scope" "example" {
  billing_account_name = "1234567"
  billing_profile_name = "ABC1-DEF2-GHI3"
  invoice_section_name = "XYZ4-YZA5-BCD6"
}

# 2. Create the new subscription
resource "azurerm_subscription" "sandbox_sub" {
  alias             = "isolated-sandbox-sub"
  subscription_name = "Isolated Sandbox Subscription"
  billing_scope_id  = data.azurerm_billing_mca_account_scope.example.id
}

# 3. Associate it with the Sandbox Management Group
resource "azurerm_management_group_subscription_association" "sandbox_assoc" {
  management_group_id = "/providers/Microsoft.Management/managementGroups/sandbox"
  subscription_id     = "/subscriptions/${azurerm_subscription.sandbox_sub.subscription_id}"
}
```

### Key Considerations

- The "Already Exists" Error: This typically occurs because of the `alias` property. When you run `terraform apply`, Azure creates a Subscription Alias. If a previous attempt failed or if you are trying to "re-create" a subscription that was manually deleted but the alias remains, you will get a conflict. Ensure the `alias` string is unique.
- Permissions: For this code to work, the identity (Service Principal or user) running Terraform must have the Subscription Creator role on the specific Billing Invoice Section. This is an elevated permission and is distinct from standard RBAC roles like "Owner."
- Role of AzureAD Provider: You would use the `azuread` provider if you wanted to create a new Entra ID group specifically for this subscription or assign an existing group as the "Owner" of the subscription via `azurerm_role_assignment`.
- Provider Constraints: Note that the `azurerm` provider usually requires an existing `subscription_id` to initialize. When creating a new subscription, you should configure the provider to point to a "management" or "shared services" subscription initially so it has a valid context to run the creation API.

### Management Group Association

By using the `azurerm_management_group_subscription_association` resource, you ensure the subscription is moved into the "sandbox" group immediately after creation. This prevents it from sitting in the "Tenant Root Group" where it might be exposed to broader organisational policies longer than necessary.

give me a diagram of the hierachy of the how the billing acounts and MG and sub fit together

To understand how your new subscription will sit in the environment, it is essential to distinguish between the Billing Hierarchy (where money flows) and the Management Group Hierarchy (where policies and permissions flow).

Based on your current setup, here is how these components intersect:

---

### The Combined Hierarchy

The following table and list illustrate the relationship between your billing account and the management group structure provided in your file.

| Level | Component | Description |
| --- | --- | --- |
| Top | Billing Account | The legal entity (EA or MCA) that pays for all resources. |
| Top | Tenant Root Group | The highest Management Group (`45e73aa3…`). |
| Middle | Billing Profile / MG | Where you group costs (Billing) or apply governance (MG). |
| Bottom | Subscriptions | The actual containers where resources live. |

#### 1\. The Billing Account (The "Wallet")

- Billing Account: This sits outside the Management Group (MG) hierarchy but is linked to your Azure AD Tenant.
- Billing Profile/Invoice Section: These are the sub-units of your billing. To create a subscription, your user account (`leon.ormes@fitfile.com`) needs Owner or Contributor rights here, regardless of your MG permissions.

#### 2\. The Management Group Hierarchy (The "Guardrails")

Based on your uploaded data, your hierarchy is structured as follows:

- Tenant Root Group (`45e73aa3-1ee9-47c0-ba25-54eda9da021a`)
	- FITFILE (The primary organisational group)
		- Landing Zones
			- `FITCloud Production`
			- `FITCloud Non-Production`
		- Platform
			- `Identity`
			- `Management`
			- `Shared Services`

---

### Placement for Your "Clean" Subscription

To ensure your new subscription is as isolated as possible from your existing "FITFILE" logic, you should place it directly under the Tenant Root Group, ideally within a new Sandbox MG.

This prevents it from inheriting policies or RBAC roles applied at the FITFILE, Landing Zones, or Platform levels.

Would you like me to generate the specific Terraform code to create both the new Management Group and the Subscription in one go?

give me the commands to workout all of this. my permissions, the mg and subs and so on. My az has access to different tenants by federated id. SO I need to be in the fitfile accountes

To work across different tenants with a federated identity and map out your permissions accurately, you must first ensure your Azure CLI is pointed at the correct directory.

Because you have access to multiple tenants, including the FitFile environment (`45e73aa3…`), you need to explicitly set your context to that tenant before running discovery commands.

---

### 1\. Target the FitFile Tenant

First, list all tenants your federated identity can reach and then set the active tenant to FitFile.

---

### 2\. Discover the Management Group Hierarchy

Since you want to see how MGs and subscriptions fit together, use the `--expand` flag. This will show you the children of each group.

---

### 3\. Audit Your Permissions

To understand why you might be hitting "Authorisation Failed" or "Not Authorised", you need to check your roles at the Root and Management Group levels.

---

### 4\. Verify Billing & Subscription Creation Rights

Creating a subscription requires permissions on the Billing Account, which is separate from Management Groups.

---

### 5\. Troubleshooting the "Ghost" Subscription

If you are told a subscription exists but cannot see it in the list, it is likely a Subscription Alias that was partially created or a subscription you have billing access to but no RBAC access to.

---

### Visualising the Structure

The hierarchy in your environment currently flows from the Tenant Root Group through FITFILE down to Landing Zones and Platform.

- Tenant Root Group: Contains all organisational resources.
- FITFILE: The parent MG for your specific organisational logic.
- Subscriptions: Individual containers like `Shared Services` or `FITCloud Production` nested under these groups.

Would you like me to provide a script that creates the new Sandbox Management Group and verifies your access to it in one go?

az account show --output table

EnvironmentName HomeTenantId IsDefault Name State TenantId

\----------------- ------------------------------------ ----------- ------------------- ------- ------------------------------------

AzureCloud 45e73aa3-1ee9-47c0-ba25-54eda9da021a True FITCloud Production Enabled 45e73aa3-1ee9-47c0-ba25-54eda9da021a

…/central-services/grafana on  master $!? on ⛵ fitfile-cloud-testing-aks-cluster (testing) on ☁️ FITCloud Production on 🅰 (eu-west-2) at 14:47:54

❯ # List all Management Groups you can see

az account management-group list --output table

\# Detailed view of the Root and its children (Subs and MGs)

az account management-group show --name 45e73aa3-1ee9-47c0-ba25-54eda9da021a --expand --output json

DisplayName Name TenantId

\------------- ------------- ------------------------------------

FITFILE FITFILE 45e73aa3-1ee9-47c0-ba25-54eda9da021a

Landing Zones LANDING-ZONES 45e73aa3-1ee9-47c0-ba25-54eda9da021a

Platform PLATFORM 45e73aa3-1ee9-47c0-ba25-54eda9da021a

(AuthorizationFailed) The client 'leon.ormes@fitfile.com' with object id '053a0abe-0b3e-40a3-85c8-83f2af887382' does not have authorization to perform action 'Microsoft.Management/managementGroups/read' over scope '/providers/Microsoft.Management/managementGroups/45e73aa3-1ee9-47c0-ba25-54eda9da021a' or the scope is invalid. If access was recently granted, please refresh your credentials.

Code: AuthorizationFailed

Message: The client 'leon.ormes@fitfile.com' with object id '053a0abe-0b3e-40a3-85c8-83f2af887382' does not have authorization to perform action 'Microsoft.Management/managementGroups/read' over scope '/providers/Microsoft.Management/managementGroups/45e73aa3-1ee9-47c0-ba25-54eda9da021a' or the scope is invalid. If access was recently granted, please refresh your credentials.

\# Get your Object ID for the current tenant

MY\_OID=$(az ad signed-in-user show --query id -o tsv)

\# Check your RBAC roles at the Tenant Root Group level

az role assignment list --assignee $MY\_OID --scope "/providers/Microsoft.Management/managementGroups/45e73aa3-1ee9-47c0-ba25-54eda9da021a" --output table

\# Check your roles on the 'FITFILE' Management Group specifically

az role assignment list --assignee $MY\_OID --scope "/providers/Microsoft.Management/managementGroups/FITFILE" --output table

zsh: correct '$MY\_OID' to '$MY\_ID' \[nyae\]? n

zsh: correct '$MY\_OID' to '$MY\_ID' \[nyae\]? n

(AuthorizationFailed) The client 'leon.ormes@fitfile.com' with object id '053a0abe-0b3e-40a3-85c8-83f2af887382' does not have authorization to perform action 'Microsoft.Authorization/roleAssignments/read' over scope '/providers/Microsoft.Management/managementGroups/45e73aa3-1ee9-47c0-ba25-54eda9da021a/providers/Microsoft.Authorization' or the scope is invalid. If access was recently granted, please refresh your credentials.

Code: AuthorizationFailed

Message: The client 'leon.ormes@fitfile.com' with object id '053a0abe-0b3e-40a3-85c8-83f2af887382' does not have authorization to perform action 'Microsoft.Authorization/roleAssignments/read' over scope '/providers/Microsoft.Management/managementGroups/45e73aa3-1ee9-47c0-ba25-54eda9da021a/providers/Microsoft.Authorization' or the scope is invalid. If access was recently granted, please refresh your credentials.

The error messages confirm that while you are authenticated to the FitFile tenant (`45e73aa3…`), your account lacks the necessary permissions to read or manage the Tenant Root Group level. This is why you cannot see the "ghost" subscription or create a new Management Group (MG) there.

To fix this, you need to identify where your permissions actually begin. Based on your file, you have Reader access to the FITFILE MG, but you are explicitly Not Authorised at the Root level.

### 1\. Mapping Your Current Access

Your uploaded file provides the exact hierarchy and where your permissions sit:

| Name | ID | Your Access Level |
| --- | --- | --- |
| Tenant Root Group | `45e73aa3-1ee9-47c0-ba25…` | Not Authorised |
| FITFILE | `FITFILE` | Reader |
| Landing Zones | `LANDING-ZONES` | Reader |
| Platform | `PLATFORM` | Reader |

Because you are "Not Authorised" at the Root, any command targeting that specific ID (like `az account management-group show --name 45e73aa3…`) will fail with the `AuthorizationFailed` error you saw.

---

### 2\. Why You Cannot Find the Subscription

You cannot see the new subscription or the "Sandbox" MG because your Reader permissions only start at the FITFILE level. If the subscription was created directly under the Root (or in a new MG sibling to FITFILE), it is invisible to you.

To find it, run this command which bypasses the MG hierarchy and looks at your profile's access directly:

- If it's not there: You don't have even "Reader" rights on that specific subscription yet.
- If it's there but "Disabled": It was created but likely failed a policy check or hasn't been fully provisioned.

---

### 3\. How to Get the Permissions You Need

To create a "clean" subscription outside of the `FITFILE` hierarchy, you need someone with User Access Administrator or Owner rights at the Tenant Root Group to grant you the following:

- Management Group Creator: At the Root level, so you can create your "Sandbox" MG.
- Owner/Contributor: On the new "Sandbox" MG.
- Subscription Creator: On the relevant Billing Invoice Section (as this is a billing permission, not an RBAC permission).

---

### 4\. Immediate Next Steps

Since you can't read the Root, you can't verify the "ghost" alias via CLI. You must use the Billing context instead:

1. Check Billing Access: Run `az billing account list`. If you see an account, you might have the right to see subscriptions even if you can't see the MGs.
2. Request Elevation: Show your admin the `generated.csv` and point out that you are "Not Authorised" at the Root. Ask them to:
	- Create the `Sandbox` MG directly under the Root.
	- Assign you the Owner role on that `Sandbox` MG.
	- Assign you the Subscription Creator role on the billing account.

Would you like me to draft the specific request (with the required Azure roles) that you can send to your tenant administrator?

az account list --refresh --all --output table

Authentication failed against tenant 29e004ae-2eba-4db3-aa4b-986053570a0e 'Default Directory': AADSTS50079: Due to a configuration change made by your administrator, or because you moved to a new location, you must enroll in multi-factor authentication to access '797f4846-ba00-4fd7-ba43-dac1f8f63013'. Trace ID: 6b0317cb-4f6f-4644-9d6a-60a886de7b00 Correlation ID: 8a688ed6-d412-4c12-8fbf-328c61573982 Timestamp: 2026-02-09 14:52:38Z

Authentication failed against tenant 3d7d135a-ac7f-46ad-aa55-54639dd31d14 'CUH': AADSTS50076: Due to a configuration change made by your administrator, or because you moved to a new location, you must use multi-factor authentication to access '797f4846-ba00-4fd7-ba43-dac1f8f63013'. Trace ID: 4c53d1db-a2a8-4148-a262-5ad971d63300 Correlation ID: c8bf498b-5a28-45b2-80f4-ff64514ae30d Timestamp: 2026-02-09 14:52:38Z

Authentication failed against tenant cf58d42f-717f-44c2-b55d-1a8125d48dfb 'Health Innovation East': AADSTS53003: Access has been blocked by Conditional Access policies. The access policy does not allow token issuance. Trace ID: 0129bbea-ed64-44a8-9048-ea25f62e0e00 Correlation ID: b2c2295f-23c5-4238-a772-67353ce79424 Timestamp: 2026-02-09 14:52:39Z

Authentication failed against tenant fe1c91a6-9974-4686-a257-7403bf62ae81 'Default Directory': AADSTS50076: Due to a configuration change made by your administrator, or because you moved to a new location, you must use multi-factor authentication to access '797f4846-ba00-4fd7-ba43-dac1f8f63013'. Trace ID: 1224da76-d9e3-451d-9f83-e7d9f5b16000 Correlation ID: f2283827-94b7-4383-b69a-e6f2e2b01808 Timestamp: 2026-02-09 14:52:40Z

The following tenants don't contain accessible subscriptions. Use \`az login --allow-no-subscriptions\` to have tenant level access.

82716421-7966-4385-943a-04a2cd4b7092 'East of England - Secure Data Environment'

If you need to access subscriptions in the following tenants, please use \`az login --tenant TENANT\_ID\`.

29e004ae-2eba-4db3-aa4b-986053570a0e 'Default Directory'

3d7d135a-ac7f-46ad-aa55-54639dd31d14 'CUH'

cf58d42f-717f-44c2-b55d-1a8125d48dfb 'Health Innovation East'

fe1c91a6-9974-4686-a257-7403bf62ae81 'Default Directory'

Name CloudName SubscriptionId TenantId State IsDefault

\----------------------- ----------- ------------------------------------ ------------------------------------ ------- -----------

FITCloud Production AzureCloud a448d869-4ec5-4c81-82c5-d6e8fa0ec0df 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled True

FITCloud Non-Production AzureCloud 249df46b-f75d-4492-8e78-b33a00473548 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled False

Shared Services AzureCloud a085dd04-19aa-4d2b-9a35-e438097d84fc 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled False

Management AzureCloud a9602426-e496-44d1-ba89-8e5fc756a06b 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled False

Identity AzureCloud c1c459c8-a99f-4f7a-891b-a98d49cf12c0 45e73aa3-1ee9-47c0-ba25-54eda9da021a Enabled False

NNUHFT-SDE AzureCloud 4ae8fd93-d084-481f-ba6e-370b7d4d8d0d d2a06081-6719-4548-bdc7-fff8bfd24f56 Enabled False

FitFileLZ AzureCloud d1043e25-5695-4d25-b658-456f3ac3e91e dbb3517b-09e6-4a76-9aa9-d7d72b1073e7 Enabled False

az billing account list

Command group 'billing account' is in preview and under development. Reference and support levels: <https://aka.ms/CLI>\_refstatus

\[\]

The results of your commands clarify why you are having trouble. The fact that `az billing account list` returned an empty list (`[]`) is the primary reason you cannot create a subscription. In Azure, management group permissions allow you to govern resources, but billing permissions are what allow you to create the subscription in the first place.

Here is a breakdown of the current situation and the steps to resolve it:

### 1\. The Primary Blocker: No Billing Access

Even though you are successfully logged into the FitFile tenant (`45e73aa3-1ee9-47c0-ba25-54eda9da021a`), your account does not have a "Billing" role.

- To create a subscription, you need the Owner or Contributor role on a Billing Invoice Section or Enrollment Account.
- Without this, you will continue to get "Not Authorised" or "Already exists" errors because the API cannot find a valid "wallet" to attach the new subscription to.

### 2\. Why You Can't See the "Ghost" Subscription

The "Already exists" error almost always refers to a Subscription Alias. When a creation attempt starts, Azure reserves that name. If the process fails or you lack permissions to see the resulting object, the name remains "locked."

Since your CLI extension is broken, use this `az rest` command to bypass the extension requirement and see if an alias is blocking you:

_If you see a name in that list that matches the one you tried to create, you must delete it before trying again:_

### 3\. Permission Gap at the Management Group Level

Your `generated.csv` file confirms your current limitations:

- Tenant Root Group: You are listed as "Not Authorized". This explains why your `az account management-group show` command failed with an `AuthorizationFailed` error.
- FITFILE Group: You have Reader access.

Because you only have "Reader" access to the `FITFILE` management group and no access to the Root, you cannot create the new "Sandbox" management group yourself.

### 4\. How to Ensure the Subscription is "Clean"

To achieve your goal of a "clean" subscription, you need to be outside the `FITFILE` hierarchy. Based on your structure:

1. Request a new MG: Ask your administrator to create a management group (e.g., `Sandbox`) directly under the Tenant Root Group, making it a sibling to `FITFILE`.
2. Inheritance: This ensures the subscription only inherits policies from the Root and remains completely "clean" of any configurations applied to the `FITFILE`, `Landing Zones`, or `Platform` groups.

### Recommended Request to Your Admin

Since you are working in the UK and need to resolve this with your team, you can use the following technical request:

> "I am trying to provision an isolated sandbox environment. Currently, my account (`leon.ormes@fitfile.com`) is Not Authorized at the Tenant Root Group and only has Reader access to the FITFILE MG.
>
> To proceed, please could you:
>
> 1. Billing Access: Grant me the Subscription Creator role on the relevant Billing Invoice Section.
> 2. MG Hierarchy: Create a new Management Group named `Sandbox` directly under the Tenant Root Group (not under FITFILE) and grant me Owner rights on it.
> 3. Alias Cleanup: Check for any "Subscription Aliases" that might be stuck from my previous failed attempts."

This will provide you with the "cleanest" possible start by bypassing the existing organisational hierarchy entirely.

Some else with permissions got

\[

{

"accountStatus": "Active",

"accountType": "Individual",

"agreementType": "MicrosoftCustomerAgreement",

"billingProfiles": {

"hasMoreResults": false,

"value": null

},

"departments": null,

"displayName": "jon.bradshaw@fitfile.com",

"enrollmentAccounts": null,

"enrollmentDetails": null,

"hasReadAccess": true,

"id": "/providers/Microsoft.Billing/billingAccounts/39c96ca5-73af-57eb-56d2-7eda8694becb:696294c6-7cf0-473c-8790-7189a5c2f505\_2019-05-31",

"name": "39c96ca5-73af-57eb-56d2-7eda8694becb:696294c6-7cf0-473c-8790-7189a5c2f505\_2019-05-31",

"notificationEmailAddress": null,

"soldTo": {

"addressLine1": "167-169 Great Portland Street",

"addressLine2": null,

"addressLine3": null,

"city": "London",

"companyName": "FITFILE Group Limited",

"country": "GB",

"district": null,

"email": "jon.bradshaw@fitfile.com",

"firstName": "Jon",

"lastName": "Bradshaw",

"middleName": "",

"phoneNumber": "07970268442",

"postalCode": "W1W 5PF",

"region": "Surrey"

},

"systemData": {

"createdAt": "2020-10-28T13:55:32.2135306Z",

"lastModifiedAt": "2024-04-14T08:53:23.7510124Z"

},

"type": "Microsoft.Billing/billingAccounts"

},

{

"accountStatus": "Active",

"accountType": "Individual",

"agreementType": "MicrosoftCustomerAgreement",

"billingProfiles": {

"hasMoreResults": false,

"value": null

},

"departments": null,

"displayName": "gareth hailes",

"enrollmentAccounts": null,

"enrollmentDetails": null,

"hasReadAccess": true,

"id": "/providers/Microsoft.Billing/billingAccounts/39c96ca5-73af-57eb-56d2-7eda8694becb:d337738b-06af-4b5c-9abc-bd74132a785c\_2019-05-31",

"name": "39c96ca5-73af-57eb-56d2-7eda8694becb:d337738b-06af-4b5c-9abc-bd74132a785c\_2019-05-31",

"notificationEmailAddress": null,

"soldTo": {

"addressLine1": "26 Eastcroft Mews",

"addressLine2": null,

"addressLine3": "",

"city": "Horsham",

"companyName": "gareth",

"country": "GB",

"district": null,

"email": "gareth.hailes@fitfile.com",

"firstName": "gareth",

"lastName": "hailes",

"middleName": null,

"phoneNumber": "7770785387",

"postalCode": "RH12 1UT",

"region": "west sussex"

},

"systemData": {

"createdAt": "2022-11-14T14:19:15.6941895Z",

"lastModifiedAt": "2025-11-18T20:51:56.3553947Z"

},

"type": "Microsoft.Billing/billingAccounts"

}

\]

The JSON snippets provided confirm that you are using a Microsoft Customer Agreement (MCA). This agreement type uses a specific three-tier billing hierarchy that must be navigated to find the correct `billing_scope_id` for your Terraform code.

### The MCA Billing Hierarchy

For an MCA, permissions and cost tracking are organized as follows:

1. Billing Account: The top-level agreement for FITFILE Group Limited.
2. Billing Profile: Represents a specific invoice and its payment method.
3. Invoice Section: A sub-grouping of costs where Azure subscriptions are actually attached.

---

### Step 1: Find the Missing IDs

To create a subscription via Terraform, you need the Names of the Billing Profile and the Invoice Section associated with your chosen Billing Account. Run these commands using one of the account IDs from your JSON (e.g., Jon's account):

_Note: If these commands return empty results, your account may only have permissions at the Billing Account level but not on the Profiles or Sections beneath it._

---

### Step 2: Terraform Configuration

Using the values discovered in Step 1, use the `azurerm_billing_mca_account_scope` data source to generate the correct `billing_scope_id` for your new subscription.

### Why You See Two Billing Accounts

The JSON shows two separate accounts: one registered to Jon Bradshaw (FITFILE Group Limited) and one to Gareth Hailes. In Azure, these represent two distinct "Enrollments" or agreements.

- Jon's account appears to be the official company account.
- Gareth's account is listed with the company name "gareth," which suggests a separate personal or legacy agreement.

To ensure the subscription is under the correct corporate governance, ensure you use the Billing Account ID associated with FITFILE Group Limited.

Would you like me to show you how to assign specific users as Owners of this new subscription automatically within the same Terraform plan?

how do I add the permissions to my user leon.ormes

To grant your user, leon.ormes, the necessary permissions to create subscriptions and manage them in a "clean" way, an administrator (like Jon Bradshaw, who has the required billing permissions) must assign roles in two distinct areas: the Billing Hierarchy and the Management Group (MG) Hierarchy.

Because your environment uses a Microsoft Customer Agreement (MCA), permissions are highly granular.

---

### 1\. Grant Billing Permissions

To create a subscription, you need the Azure subscription creator role on a specific Invoice Section. This is the "wallet" permission that allows you to trigger the creation API.

The Administrator should run this command:

_Note: Using the Azure Portal is often easier for this specific role. Navigate to Cost Management + Billing > Invoice Sections > Access Control (IAM)._

---

### 2\. Grant Management Group Permissions

To place that new subscription into your "clean" Sandbox MG and manage it, you need the Owner or Contributor role on that specific management group.

The Administrator should run this command:

---

### Summary of Permissions Needed

| Hierarchy | Scope | Role Required | Purpose |
| --- | --- | --- | --- |
| Billing | Invoice Section | Azure subscription creator | Permission to "buy" the subscription. |
| Governance | Sandbox MG | Owner | Permission to move the subscription here and manage resources. |

### Verifying the Assignment

Once the admin has run these commands, you can verify your new permissions by running:

Would you like me to provide a one-line summary of these requirements that you can share directly with Jon to ensure he has the right context?

yes

To grant your user, leon.ormes, the necessary permissions to create and manage "clean" subscriptions within your specific Microsoft Customer Agreement (MCA) billing account, an administrator like Jon Bradshaw must assign roles in both the billing and management group hierarchies.

### 1\. Assign Billing Permissions

To create a new subscription, you must have the Azure subscription creator role assigned at the Invoice Section level. This is a billing-specific role that is separate from standard Azure RBAC roles.

Steps for the Admin (Jon Bradshaw):

1. Search for "Cost Management + Billing" in the Azure portal.
2. Select the Billing Account (`39c96ca5-73af…`).
3. On the left menu, select "Billing profiles" and then select the specific profile (e.g., "Default").
4. Select "Invoice sections" and choose the section where you want the subscription to be billed.
5. Select "Access control (IAM)" from the left sidebar of that section.
6. Click "Add" and assign the Azure subscription creator role to leon.ormes@fitfile.com.

---

### 2\. Assign Management Group Permissions

Even with billing rights, you cannot move a subscription into a "clean" management group without Owner or Contributor rights on that specific group.

Steps for the Admin:

1. Navigate to "Management groups" in the portal.
2. Select the "Sandbox" management group (or the new group intended for clean subscriptions).
3. Select "Access control (IAM)".
4. Click "Add role assignment" and assign the Owner role to your user.

---

### Summary of Permissions Granted

| Hierarchy | Scope | Role Required | Benefit |
| --- | --- | --- | --- |
| Billing | Invoice Section | Azure subscription creator | Grants you the legal right to "purchase" new subscriptions. |
| Governance | Sandbox MG | Owner | Allows you to attach the new subscription here and manage its policies. |

### Request to Send to Your Admin

To make this easy for Jon, you can send him this specific request:

> "Hi Jon, to set up the isolated sandbox as discussed, please could you grant my user (leon.ormes@fitfile.com) the following two permissions:
>
> 1. Azure subscription creator on the company Invoice Section (under Billing Account `39c96ca5…`).
> 2. Owner on the 'Sandbox' Management Group located directly under the Tenant Root Group.
> 
> This will allow me to create subscriptions that don't inherit our standard FITFILE/Landing Zone policies."

Would you like me to help you draft a Terraform script to verify these permissions once they are assigned?

I seem to have these roles. can I add myself to the nessecary groups

No, with your current Reader and Not Authorised status, you cannot add yourself to the necessary groups or assign yourself higher roles.

In Azure, the ability to change permissions is a specific permission in itself (`Microsoft.Authorization/roleAssignments/write`). Unless you already have a role that includes this—such as Owner or User Access Administrator—the "Add" buttons in the portal will be greyed out for you.

### Why You Cannot Self-elevate

Azure follows a strict "top-down" authority model. To grant yourself access to a Management Group (MG):

- The Guardrail: You must already have a role at that MG (or its parent) that allows you to manage memberships.
- Your Current State: Your logs show you are Not Authorised at the Tenant Root Group. This means you are completely "locked out" of the administrative layer that controls the hierarchy.
- The Conflict: If a user could add themselves to a group to get more power, it would bypass all security controls.

---

### The only "Self-Service" Exceptions

There are only two scenarios where you might be able to bypass asking Jon Bradshaw:

#### 1\. Privileged Identity Management (PIM)

If your organisation uses Entra ID P2, you might have an Eligible role that isn't currently active.

- How to check: Search for "Microsoft Entra PIM" in the portal, go to "My roles", and check under "Azure resources".
- If you see "User Access Administrator" or "Owner" listed as Eligible, you can click Activate to gain those powers for a few hours.

#### 2\. Global Administrator "Elevate Access" (Highly Unlikely)

If you were a Global Administrator in Entra ID (the identity side), you could force your way into the Azure Resource side.

- The Trick: Go to Entra ID > Properties > Toggle "Access management for Azure resources" to Yes.
- The Reality: Your previous "Not Authorised" error at the Root Group strongly suggests you are not a Global Admin. If you were, you would have seen "Success" or different error codes.

---

### What to Check next

To be 100% sure of what you can and cannot do, run this command to see your _effective_ permissions at the Root:

If that returns `Allowed: false`, you have no choice but to have Jon Bradshaw (or another Admin) perform the steps we discussed.

Would you like me to write a one-sentence "Call to Action" that you can slack to Jon right now to get this moving?

az self-help check-access --scope "/providers/Microsoft.Management/managementGroups/45e73aa3-1ee9-47c0-ba25-54eda9da021a" --action "Microsoft.Authorization/roleAssignments/write"

'self-help' is misspelled or not recognized by the system.

Examples from AI knowledge base:

<https://aka.ms/cli>\_ref

Read more about the command in reference docs

The command failed because `az self-help` is an extension designed for resource diagnostics and troubleshooting, not for checking RBAC permissions.

The "AuthorizationFailed" error you encountered earlier remains the most accurate indicator of your current state. In Azure, the ability to assign roles is a specific permission (`Microsoft.Authorization/roleAssignments/write`). Unless you are already an Owner or User Access Administrator, the system will block any attempt to modify permissions—including adding yourself to a group.

To move forward, a user with the required authority at the Tenant Root Group must perform the following actions:

1. Grant Billing Access: Assign the Azure subscription creator role to you on the specific Invoice Section.
2. Grant Management Group Access: Assign the Owner or Contributor role to you on the Sandbox Management Group (after creating it directly under the Root).

Without these manual assignments from an administrator, you are technically restricted to your current "Reader" scope and cannot self-elevate.

read this screenshot. What are my persmissions from this view

Based on the data in the `generated.csv` file you provided (which represents your Management Group view), your permissions are highly restricted. Here is the breakdown of what you can see and do:

### Permissions Summary

| Scope | Name | Access Level | What this means |
| --- | --- | --- | --- |
| Root | Tenant Root Group | Not Authorised | You have no visibility or control at the highest level. |
| Management Group | FITFILE | Reader | You can see the structure but cannot make changes. |
| Management Group | Landing Zones | Reader | Read-only access inherited from FITFILE. |
| Management Group | Platform | Reader | Read-only access inherited from FITFILE. |
| Subscriptions | All listed (e.g. Production, Identity) | Reader | You can view resources but cannot create or delete them. |

---

### Detailed Analysis

#### 1\. The "Not Authorised" Gap

At the Tenant Root Group, your access is listed as Not Authorised.

- This is the primary reason you are getting errors when trying to create a "clean" subscription.
- Because you lack permissions here, you cannot create a new Management Group alongside "FITFILE" to isolate your new subscription from existing policies.

#### 2\. The "Reader" Limitation

For the rest of the hierarchy (FITFILE and everything below it), you are a Reader.

- No "Write" access: You cannot create new subscriptions, move existing ones, or change any Azure Policies.
- Inheritance: Since you are a Reader at the `FITFILE` level, that permission flows down to every child group and subscription shown (Landing Zones, Platform, etc.).

#### 3\. View of the Environment

Your view confirms that the environment is currently managing 5 subscriptions in total across the hierarchy. You can see how they are distributed:

- Landing Zones: 2 subscriptions (Production and Non-Production).
- Platform: 3 subscriptions (Identity, Management, and Shared Services).

### Why This view Confirms You Need an Admin

To achieve your goal of creating a "clean" subscription that inherits nothing from "FITFILE," you need to be able to work at the Tenant Root Group level. As "Not Authorised," you are essentially a guest in the house who can look through the windows of the `FITFILE` rooms but cannot open the front door or build a new room.

Your next step should be to ask Jon Bradshaw (or another owner) to grant you 'Owner' rights specifically on the Tenant Root Group or a newly created 'Sandbox' MG sibling to FITFILE.

Would you like me to write a specific technical summary of these findings that you can provide as evidence for why you need elevated access?

i have a role called permissions management adminsitrator in Directory

The Permissions Management Administrator role is a specific Entra ID (formerly Azure AD) directory role designed to manage the Microsoft Entra Permissions Management product (formerly known as CloudKnox).

While it sounds broad, it does not grant the permissions required to resolve your current situation. Here is the breakdown of what that role can and cannot do in this context:

### What This Role is for

- Multi-Cloud Management: It allows you to configure and manage the Entra Permissions Management service, which tracks "Permission Creep" across Azure, AWS, and GCP.
- Product Administration: You can manage settings, data collectors, and users within the Permissions Management portal.

### What This Role DOES NOT Grant

- No Azure RBAC Control: It does not grant the `Microsoft.Authorization/roleAssignments/write` permission on your Management Groups or Subscriptions. You cannot use it to assign yourself the "Owner" role on the Root Group.
- No Billing Access: It does not provide access to the Microsoft Customer Agreement billing hierarchy. You still will not be able to create a subscription or see the billing accounts.
- No Management Group Control: It does not override the "Not Authorised" status you are seeing at the Tenant Root Group.

### The Difference in "Admin" Roles

In Azure, permissions are split between the Identity (Directory) and Resources (Management Groups/Subscriptions):

| Role Type | Example Role | Can it create a Sub or fix your MG? |
| --- | --- | --- |
| Directory Role | Permissions Management Administrator | No. Manages the Permissions Management product. |
| Directory Role | Global Administrator | Yes, but only if you "Elevate Access" in Entra properties. |
| Resource Role | Owner / User Access Administrator | Yes. These are the roles you need at the Root MG level. |
| Billing Role | Azure Subscription Creator | Yes. This is the role you need at the Invoice Section level. |

### Next Steps

Having this role confirms you have some administrative standing in the directory, but it is not the "key" to the resource hierarchy. You still need an individual with Owner or User Access Administrator rights at the Tenant Root Group to:

1. Grant you RBAC permissions on a new Sandbox Management Group.
2. Grant you the Subscription Creator billing role on the company's Invoice Section.

If your organisation uses the Entra Permissions Management tool, you could use it to _view_ who has high-privilege assignments at the Root, which might help you identify exactly which colleague (besides Jon) has the power to help you.

Google Account

Leon Ormes

leonormes@gmail.com

## Processed Output

- Project Log: [[2026-02-09 - Azure Sandbox Subscription Isolation]]
- Status: Processed into [[SoT - FitFile Deployment - Strategy & Architecture]]
