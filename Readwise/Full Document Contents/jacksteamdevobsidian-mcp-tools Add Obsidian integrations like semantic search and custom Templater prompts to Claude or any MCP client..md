# jacksteamdev/obsidian-mcp-tools: Add Obsidian integrations like semantic search and custom Templater prompts to Claude or any MCP client.

![rw-book-cover](https://github.githubassets.com/favicons/favicon.png)

## Metadata
- Author: [[https://github.com/jacksteamdev/]]
- Full Title: jacksteamdev/obsidian-mcp-tools: Add Obsidian integrations like semantic search and custom Templater prompts to Claude or any MCP client.
- Category: #articles
- Summary: The obsidian-mcp-tools plugin lets AI apps like Claude Desktop securely access your Obsidian notes using the Model Context Protocol. It includes an Obsidian plugin and a local server to enable features like semantic search and template execution. The plugin keeps your data safe by controlling AI access through a secure, encrypted connection.
- URL: https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main

## Full Document
#### Create list

[Open in github.dev](https://github.dev/) [Open in a new github.dev tab](https://github.dev/) [Open in codespace](https://github.com/codespaces/new/jacksteamdev/obsidian-mcp-tools/tree/main?resume=1)

### jacksteamdev/obsidian-mcp-tools

t

Open more actions menu

### MCP Tools for Obsidian

[![GitHub release (latest by date)](https://camo.githubusercontent.com/c41b494e0ccb74679e954c26cc12e38af6d223c83c166df07160c9dc82d98dba/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f762f72656c656173652f6a61636b737465616d6465762f6f6273696469616e2d6d63702d746f6f6c73)](https://github.com/jacksteamdev/obsidian-mcp-tools/releases/latest)
[![Build status](https://camo.githubusercontent.com/0379c4dfd55d0cd56472e61d64f1b5d9e42bfb3c8728d0681f3679c9af7fae8c/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f6a61636b737465616d6465762f6f6273696469616e2d6d63702d746f6f6c732f72656c656173652e796d6c)](https://github.com/jacksteamdev/obsidian-mcp-tools/actions)
[![License](https://camo.githubusercontent.com/67278d93fa6972234c6a4d1b9112089987b65480e1945c01d0d1cc4c7bbd01a6/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f6a61636b737465616d6465762f6f6273696469616e2d6d63702d746f6f6c73)](https://github.com/jacksteamdev/obsidian-mcp-tools/blob/main/LICENSE)
[Features](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#features) | [Installation](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#installation) | [Configuration](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#configuration) | [Troubleshooting](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#troubleshooting) | [Security](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#security) | [Development](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#development) | [Support](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#support)

MCP Tools for Obsidian enables AI applications like Claude Desktop to securely access and work with your Obsidian vault through the Model Context Protocol (MCP). MCP is an open protocol that standardizes how AI applications can interact with external data sources and tools while maintaining security and user control. [1](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fn-2-58fc0cb26e511c339dae2cd496ad1280)

This plugin consists of two parts:

1. An Obsidian plugin that adds MCP capabilities to your vault
2. A local MCP server that handles communication with AI applications

When you install this plugin, it will help you set up both components. The MCP server acts as a secure bridge between your vault and AI applications like Claude Desktop. This means AI assistants can read your notes, execute templates, and perform semantic searches - but only when you allow it and only through the server's secure API. The server never gives AI applications direct access to your vault files. [2](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fn-3-58fc0cb26e511c339dae2cd496ad1280)

>  **Privacy Note**: When using Claude Desktop with this plugin, your conversations with Claude are not used to train Anthropic's models by default. [3](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fn-1-58fc0cb26e511c339dae2cd496ad1280)
> 
>  

#### Features

When connected to an MCP client like Claude Desktop, this plugin enables:

* **Vault Access**: Allows AI assistants to read and reference your notes while maintaining your vault's security [4](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fn-4-58fc0cb26e511c339dae2cd496ad1280)
* **Semantic Search**: AI assistants can search your vault based on meaning and context, not just keywords [5](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fn-5-58fc0cb26e511c339dae2cd496ad1280)
* **Template Integration**: Execute Obsidian templates through AI interactions, with dynamic parameters and content generation [6](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fn-6-58fc0cb26e511c339dae2cd496ad1280)

All features require an MCP-compatible client like Claude Desktop, as this plugin provides the server component that enables these integrations. The plugin does not modify Obsidian's functionality directly - instead, it creates a secure bridge that allows AI applications to work with your vault in powerful ways.

#### Prerequisites

##### Required

* [Obsidian](https://obsidian.md/) v1.7.7 or higher
* [Claude Desktop](https://claude.ai/download) installed and configured
* [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin installed and configured with an API key

##### Recommended

* [Templater](https://silentvoid13.github.io/Templater/) plugin for enhanced template functionality
* [Smart Connections](https://smartconnections.app/) plugin for semantic search capabilities

#### Installation

Important

This plugin requires a secure server component that runs locally on your computer. The server is distributed as a signed executable, with its complete source code available in `packages/mcp-server/`. For details about our security measures and code signing process, see the [Security](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#security) section.

1. Install the plugin from Obsidian's Community Plugins
2. Enable the plugin in Obsidian settings
3. Open the plugin settings
4. Click "Install Server" to download and configure the MCP server

Clicking the install button will:

* Download the appropriate MCP server binary for your platform
* Configure Claude Desktop to use the server
* Set up necessary permissions and paths

##### Installation Locations

* **Server Binary**: {vault}/.obsidian/plugins/obsidian-mcp-tools/bin/
* **Log Files**:
	+ macOS: ~/Library/Logs/obsidian-mcp-tools
	+ Windows: %APPDATA%\obsidian-mcp-tools\logs
	+ Linux: ~/.local/share/obsidian-mcp-tools/logs

#### Configuration

After clicking the "Install Server" button in the plugin settings, the plugin will automatically:

1. Download the appropriate MCP server binary
2. Use your Local REST API plugin's API key
3. Configure Claude Desktop to use the MCP server
4. Set up appropriate paths and permissions

While the configuration process is automated, it requires your explicit permission to install the server binary and modify the Claude Desktop configuration. No additional manual configuration is required beyond this initial setup step.

#### Troubleshooting

If you encounter issues:

1. Check the plugin settings to verify:
	* All required plugins are installed
	* The server is properly installed
	* Claude Desktop is configured
2. Review the logs:
	* Open plugin settings
	* Click "Open Logs" under Resources
	* Look for any error messages or warnings
3. Common Issues:
	* **Server won't start**: Ensure Claude Desktop is running
	* **Connection errors**: Verify Local REST API plugin is configured
	* **Permission errors**: Try reinstalling the server

#### Security

##### Binary Distribution

* All releases are built using GitHub Actions with reproducible builds
* Binaries are signed and attested using SLSA provenance
* Release workflows are fully auditable in the repository

##### Runtime Security

* The MCP server runs with minimal required permissions
* All communication is encrypted
* API keys are stored securely using platform-specific credential storage

##### Binary Verification

The MCP server binaries are published with [SLSA Provenance attestations](https://slsa.dev/provenance/v1), which provide cryptographic proof of where and how the binaries were built. This helps ensure the integrity and provenance of the binaries you download.

To verify a binary using the GitHub CLI:

1. Install GitHub CLI:

 
```
# macOS (Homebrew)
brew install gh

# Windows (Scoop)
scoop install gh

# Linux
sudo apt install gh  # Debian/Ubuntu
```
2. Verify the binary:

 
```
gh attestation verify --owner jacksteamdev <binary path or URL>
```

The verification will show:

* The binary's SHA256 hash
* Confirmation that it was built by this repository's GitHub Actions workflows
* The specific workflow file and version tag that created it
* Compliance with SLSA Level 3 build requirements

This verification ensures the binary hasn't been tampered with and was built directly from this repository's source code.

##### Reporting Security Issues

Please report security vulnerabilities via our [security policy](https://github.com/jacksteamdev/obsidian-mcp-tools/blob/main/SECURITY.md). Do not report security vulnerabilities in public issues.

#### Development

This project uses a monorepo structure with feature-based architecture. For detailed project architecture documentation, see [.clinerules](https://github.com/jacksteamdev/obsidian-mcp-tools/blob/main/.clinerules).

##### Using Cline

Some code in this project was implemented using the AI coding agent [Cline](https://cline.bot). Cline uses `cline_docs/` and the `.clinerules` file to understand project architecture and patterns when implementing new features.

##### Workspace

This project uses a [Bun](https://bun.sh/) workspace structure:

```
packages/
├── mcp-server/        # Server implementation
├── obsidian-plugin/   # Obsidian plugin
└── shared/           # Shared utilities and types

```

##### Building

1. Install dependencies: 
```
bun install
```
2. Build all packages: 
```
bun run build
```
3. For development: 
```
bun run dev
```

##### Requirements

* [bun](https://bun.sh/) v1.1.42 or higher
* TypeScript 5.0+

#### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: 
```
bun test
```
5. Submit a pull request

Please see [CONTRIBUTING.md](https://github.com/jacksteamdev/obsidian-mcp-tools/blob/main/CONTRIBUTING.md) for detailed guidelines.

#### Support

* [Open an issue](https://github.com/jacksteamdev/obsidian-mcp-tools/issues) for bug reports and feature requests
* [Start a discussion](https://github.com/jacksteamdev/obsidian-mcp-tools/discussions) for questions and general help

#### Changelog

See [CHANGELOG.md](https://github.com/jacksteamdev/obsidian-mcp-tools/blob/main/CHANGELOG.md) for a list of changes in each release.

#### License

[MIT License](https://github.com/jacksteamdev/obsidian-mcp-tools/blob/main/LICENSE)

#### Footnotes

#### Footnotes

1. For more information about the Model Context Protocol, see [MCP Introduction](https://modelcontextprotocol.io/introduction) [↩](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fnref-2-58fc0cb26e511c339dae2cd496ad1280)
2. For a list of available MCP Clients, see [MCP Example Clients](https://modelcontextprotocol.io/clients) [↩](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fnref-3-58fc0cb26e511c339dae2cd496ad1280)
3. For information about Claude data privacy and security, see [Claude AI's data usage policy](https://support.anthropic.com/en/articles/8325621-i-would-like-to-input-sensitive-data-into-free-claude-ai-or-claude-pro-who-can-view-my-conversations) [↩](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fnref-1-58fc0cb26e511c339dae2cd496ad1280)
4. Requires Obsidian plugin Local REST API [↩](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fnref-4-58fc0cb26e511c339dae2cd496ad1280)
5. Requires Obsidian plugin Smart Connections [↩](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fnref-5-58fc0cb26e511c339dae2cd496ad1280)
6. Requires Obsidian plugin Templater [↩](https://github.com/jacksteamdev/obsidian-mcp-tools/tree/main#user-content-fnref-6-58fc0cb26e511c339dae2cd496ad1280)
