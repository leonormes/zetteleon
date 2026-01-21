---
created: 2026-01-14T19:42:45+00:00
modified: 2026-01-20T15:33:30+00:00
tags: [articles]
title: "GitHub - tapanmeena/azp-cli: A Command-line Interface Tool for Managing Azure Privileged Identity Management (PIM) Role Activations Directly from Your Terminal"
---

# GitHub - tapanmeena/azp-cli: A Command-line Interface Tool for Managing Azure Privileged Identity Management (PIM) Role Activations Directly from Your Terminal

![rw-book-cover](https://opengraph.githubassets.com/fbd8da49c396693220ca1ff3edf85b8cc443e671b7c98175fb42dbb780edd336/tapanmeena/azp-cli)

## Metadata

- Author: [[https://github.com/tapanmeena/]]
- Full Title: GitHub - tapanmeena/azp-cli: A command-line interface tool for managing Azure Privileged Identity Management (PIM) role activations directly from your terminal.
- Category: #articles
- Summary: azp-cli is a command-line tool for managing Azure Privileged Identity Management (PIM) roles directly from your terminal. It lets you activate and deactivate roles quickly, supports multiple roles, and offers presets for common tasks. The tool also works in non-interactive mode, making it useful for automation and scripting.
- URL: <https://github.com/tapanmeena/azp-cli>

## Full Document

### tapanmeena/azp-cli

main

Go to file

Code

Open more actions menu

### Azure PIM CLI (azp-cli)

A command-line interface tool for managing Azure Privileged Identity Management (PIM) role activations directly from your terminal.

[![Terminal UI](https://camo.githubusercontent.com/521d0d926d343913f5282c0d00cf44a200a3322c0910f1148ca8ae1dab212eaf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5465726d696e616c2d55492d6379616e)](https://camo.githubusercontent.com/521d0d926d343913f5282c0d00cf44a200a3322c0910f1148ca8ae1dab212eaf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5465726d696e616c2d55492d6379616e)

[![TypeScript](https://camo.githubusercontent.com/510e5134ddb428cfda3ceac604ddce4fa60e4a4a4675ad9524a1a8ab2dc32cd8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f547970655363726970742d352e392d626c7565)](https://camo.githubusercontent.com/510e5134ddb428cfda3ceac604ddce4fa60e4a4a4675ad9524a1a8ab2dc32cd8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f547970655363726970742d352e392d626c7565)

[![License](https://camo.githubusercontent.com/420837c36e27d7cf1438e410f4a038efc30470452b2074833ee99b20b41ae6a6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4953432d677265656e)](https://camo.githubusercontent.com/420837c36e27d7cf1438e410f4a038efc30470452b2074833ee99b20b41ae6a6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4953432d677265656e)

#### Features

- 🔐 **Role Activation** - Quickly activate eligible Azure PIM roles
- 🔓 **Role Deactivation** - Deactivate active roles when no longer needed
- 📋 **Interactive Menu** - User-friendly menu-driven interface
- ✨ **Beautiful UI** - Polished terminal experience with spinners and colors
- 🔄 **Multi-role Support** - Activate or deactivate multiple roles at once
- 📊 **Status Tracking** - Real-time feedback on activation/deactivation status
- 💾 **Presets** - Save and reuse activation/deactivation configurations
- 🚀 **Non-interactive Mode** - CLI flags for scripting and automation
- 🔔 **Update Notifications** - Automatic update checks with configurable behavior
- 📤 **JSON Output** - Machine-readable output for integration with other tools

#### Prerequisites

Before using azp-cli, ensure you have:

1. **Node.js** (v18 or higher)
2. **Azure CLI** installed and configured
3. **Azure account** with PIM-eligible roles

##### Azure CLI Setup

```
# Install Azure CLI (if not installed)
# See: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login to Azure
az login

# Verify you're logged in
az account show
```

#### Installation

##### Global Installation (Recommended)

```
# Using npm
npm install -g azp-cli

# Using pnpm
pnpm add -g azp-cli

# Using yarn
yarn global add azp-cli
```

After installation, the `azp` command will be available globally.

##### From Source (Development)

```
# Clone the repository
git clone https://github.com/tapanmeena/azp-cli.git
cd azp-cli

# Install dependencies
pnpm install

# Build the project
pnpm build

# Link globally for development
npm link
```

#### Usage

##### Running the CLI

```
# After global installation
azp

# Or with specific commands
azp activate
azp deactivate
azp preset list
azp update

# Development mode (from source)
pnpm dev
```

##### Commands

| Command | Alias | Description |
| --- | --- | --- |
| `activate` | `a` | Activate a role in Azure PIM (default) |
| `deactivate` | `d` | Deactivate a role in Azure PIM |
| `preset` | - | Manage reusable presets |
| `update` | `upgrade` | Check for a newer version |
| `help` | - | Display help information |

###### Preset Subcommands

| Command | Description |
| --- | --- |
| `preset list` | List all available presets |
| `preset show` | Show details of a specific preset |
| `preset add` | Add a new preset (interactive wizard) |
| `preset edit` | Edit an existing preset (interactive wizard) |
| `preset remove` | Remove a preset |

##### Updates

You can check if a newer version is available:

```
azp update
# alias
azp upgrade
```

Notes:

- `azp update` exits with code `0` when up-to-date, `2` when an update is available, and `1` on error.
- `--output json` returns a structured response suitable for scripts.
- By default, `azp activate` and `azp deactivate` will also show a short "update available" hint (text mode only) at most once per day.
- Disable update checks via `AZP_NO_UPDATE_NOTIFIER=1` (or `AZP_DISABLE_UPDATE_CHECK=1`).

The update-check cache is stored alongside presets in your config directory:

- macOS/Linux: `~/.config/azp-cli/update-check.json` (or `$XDG_CONFIG_HOME/azp-cli/update-check.json`)
- Windows: `%APPDATA%\azp-cli\update-check.json`

##### Non-interactive Mode (Automation)

Use flags to activate or deactivate PIM roles directly without going through the interactive menu, perfect for scripting and CI/CD workflows.

###### Activation Examples

```
# Activate a single role by name (non-interactive)
azp activate --no-interactive --yes \
   --subscription-id <SUBSCRIPTION_GUID> \
   --role-name "Owner" \
   --duration-hours 2 \
   --justification "Break-glass for incident" \
   --output json

# Activate multiple roles (repeat --role-name)
azp activate --no-interactive --yes \
   --subscription-id <SUBSCRIPTION_GUID> \
   --role-name "Contributor" \
   --role-name "User Access Administrator"

# If a role name matches multiple eligible roles (different scopes),
# --no-interactive will error unless you explicitly allow activating all matches
azp activate --no-interactive --yes \
   --subscription-id <SUBSCRIPTION_GUID> \
   --role-name "Contributor" \
   --allow-multiple

# Preview what would happen without submitting requests
azp activate --no-interactive --dry-run \
   --subscription-id <SUBSCRIPTION_GUID> \
   --role-name "Contributor" \
   --output json
```

###### Deactivation Examples

```
# Deactivate specific roles
azp deactivate --no-interactive --yes \
   --subscription-id <SUBSCRIPTION_GUID> \
   --role-name "Owner" \
   --justification "Task completed"

# Deactivate across all subscriptions (omit subscription-id)
azp deactivate --no-interactive --yes \
   --role-name "Contributor" \
   --allow-multiple
```

###### Available Flags

**Common flags (activate/deactivate):**

- `--no-interactive` - Disable interactive prompts
- `-y, --yes` - Skip confirmation prompts
- `--subscription-id <id>` - Target subscription (optional for deactivate)
- `--role-name <name>` - Role name(s) to target (can be repeated)
- `--allow-multiple` - Allow multiple role matches
- `--dry-run` - Preview without submitting
- `--output <text|json>` - Output format (default: text)
- `--quiet` - Suppress non-essential output

**Activation-specific:**

- `--duration-hours <n>` - Duration (1-8 hours, default varies by role)
- `--justification <text>` - Justification for activation

**Deactivation-specific:**

- `--justification <text>` - Justification for deactivation (optional)

#### Presets

Presets let you save your daily activation/deactivation routines (subscription + role names + duration + justification) and reuse them with `--preset <name>`.

##### Presets File Location

By default, presets are stored in a per-user config file:

- macOS/Linux: `~/.config/azp-cli/presets.json` (or `$XDG_CONFIG_HOME/azp-cli/presets.json`)
- Windows: `%APPDATA%\azp-cli\presets.json`

Override the location with:

- `AZP_PRESETS_PATH=/path/to/presets.json`

##### Preset Contents

A preset can define one or both blocks:

- `activate`: `subscriptionId`, `roleNames[]`, `durationHours`, `justification`, `allowMultiple`
- `deactivate`: `subscriptionId` (optional), `roleNames[]`, `justification`, `allowMultiple`

`justification` supports simple templates:

- `${date}` → `YYYY-MM-DD`
- `${datetime}` → ISO timestamp
- `${userPrincipalName}` → resolved from Microsoft Graph `/me`

##### Common Workflows

```sh
# Create a preset (interactive wizard)
azp preset add daily-ops

# Create a preset with Azure integration (fetches subscriptions/roles)
azp preset add daily-ops --from-azure

# Edit a preset (interactive wizard)
azp preset edit daily-ops

# List all presets
azp preset list

# Show one preset details
azp preset show daily-ops

# Remove a preset
azp preset remove daily-ops

# Use a preset (flags still override preset values)
azp activate --preset daily-ops --yes

# Non-interactive run using the preset
azp activate --preset daily-ops --no-interactive --yes --output json

# Deactivate using a preset
azp deactivate --preset daily-ops --no-interactive --yes
```

##### Defaults

When you create a preset via `azp preset add`, you can optionally set it as the default for `activate` and/or `deactivate`.

- Default presets are applied automatically when you run one-shot flows and you haven't explicitly provided the required flags.
- Example: after setting a default activate preset, `azp activate --no-interactive --yes` can work without specifying `--subscription-id`/`--role-name`.

##### Example Session

```sh
╔════════════════════════════════════════════════════╗
║     Azure PIM CLI - Role Activation Manager        ║
╚════════════════════════════════════════════════════╝

✔ Authentication successful

┌─ User Information ──────────────────────────────────
│ Name: John Doe
│ Email: john@example.com
└──────────────────────────────────────────────────────

✔ Found 3 subscription(s)

? What would you like to do?
❯ ▶ Activate Role(s)
  ◼ Deactivate Role(s)
  ✕ Exit

```

##### Role Activation Flow

1. Select a subscription from your available Azure subscriptions
2. Choose one or more eligible roles to activate
3. Specify activation duration (1-8 hours)
4. Provide a justification for the activation
5. Confirm and activate

##### Role Deactivation Flow

1. View all currently active roles across subscriptions
2. Select roles to deactivate
3. Confirm deactivation

#### Development

##### Available Scripts

```sh
# Run in development mode with hot reload
pnpm dev

# Build the TypeScript project
pnpm build

# Run the built application
pnpm start

# Lint the codebase
pnpm lint
```

#### Changelog & Releases

This repo uses [Keep a Changelog](https://keepachangelog.com/) format in [CHANGELOG.md](https://github.com/tapanmeena/azp-cli/blob/main/CHANGELOG.md).

##### Recommended Commit Messages

For best results, use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: …` (new feature) → minor bump
- `fix: …` (bug fix) → patch bump
- `chore: …`, `docs: …`, `refactor: …` (no bump unless breaking)

##### Cutting a Release

1. Make sure `CHANGELOG.md` has up-to-date entries under **Unreleased**.
2. Run one of the following:

```sh
# Automatically determines next version from commits, updates CHANGELOG.md,
# bumps package.json, and creates a git tag.
pnpm release

# Preview what would change
pnpm release:dry

# Force a specific bump if needed
pnpm release -- --release-as patch
pnpm release -- --release-as minor
pnpm release -- --release-as major
```

1. Push commits + tags:

```sh
git push --follow-tags
```

1. Publish to npm (if desired):

```
npm publish
# or
pnpm publish
```

##### Project Structure

```
azp-cli/
├── src/
│   ├── index.ts          # CLI entry point and command definitions
│   ├── auth.ts           # Azure authentication handling
│   ├── azure-pim.ts      # Azure PIM API operations
│   ├── cli.ts            # Interactive menu and user flows
│   ├── presets.ts        # Preset configuration and storage
│   ├── presets-cli.ts    # Preset wizard flows
│   ├── ui.ts             # Terminal UI utilities (spinners, formatting)
│   └── update-check.ts   # Update notification system
├── package.json
├── tsconfig.json
└── README.md

```

##### Tech Stack

- **TypeScript** - Type-safe JavaScript
- **Commander.js** - CLI framework
- **Inquirer.js** - Interactive prompts
- **Ora** - Elegant terminal spinners
- **Chalk** - Terminal string styling
- **Azure SDK** - Azure service integration

#### Troubleshooting

##### "Azure CLI not found" Error

Ensure Azure CLI is installed and accessible in your PATH:

```
az --version
```

##### Authentication Errors

1. Make sure you're logged in to Azure CLI:

```
az login
```

2. Verify your account has PIM-eligible roles:

```
az account show
```

3. Check if you have the necessary permissions in Azure AD

##### No Subscriptions Found

- Verify your Azure account has access to subscriptions
- Try refreshing your Azure CLI login: `az login --refresh`

#### License

This project is licensed under the ISC License.

#### Author

**Tapan Meena** - [tapanmeena1998@gmail.com](mailto:tapanmeena1998@gmail.com)

#### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
