---
created: 2026-03-14T09:50:15+00:00
modified: 2026-03-14T11:09:15+00:00
tags: [articles]
title: Remote MCP servers
---

## Remote MCP Servers

![rw-book-cover](https://langchain-5e9cc07a.mintlify.app/mintlify-assets/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DTools%2Band%2Bintegrations%26appearance%3Dsystem%26title%3DRemote%2BMCP%2Bservers%26description%3DConnect%2BAgent%2BBuilder%2Bto%2Bpopular%2Bremote%2BMCP%2Bservers%26logoLight%3Dhttps%253A%252F%252Fmintcdn.com%252Flangchain-5e9cc07a%252FXbr8HuVd9jPi6qTU%252Fimages%252Fbrand%252Flangchain-docs-teal.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253DXbr8HuVd9jPi6qTU%2526q%253D85%2526s%253D16111530672bf976cb54ef2143478342%26logoDark%3Dhttps%253A%252F%252Fmintcdn.com%252Flangchain-5e9cc07a%252FXbr8HuVd9jPi6qTU%252Fimages%252Fbrand%252Flangchain-docs-lilac.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253DXbr8HuVd9jPi6qTU%2526q%253D85%2526s%253Db70fb1a2208670492ef94aef14b680be%26primaryColor%3D%25232F6868%26lightColor%3D%252384C4C0%26darkColor%3D%25231C3C3C%26backgroundLight%3D%2523ffffff%26backgroundDark%3D%25230b0d0f&w=1200&q=100)

### Metadata

- Author: [[Docs by LangChain]]
- Full Title: Remote MCP servers
- Category: articles
- Summary: You can connect Agent Builder to remote MCP servers to use extra tools and services. These servers run independently and need authentication like API keys or OAuth. Once set up, agents send requests to the MCP server, get data, and use it alongside built-in tools.
- URL: <https://docs.langchain.com/langsmith/agent-builder-remote-mcp-servers>

### Full Document

You can connect Agent Builder to remote MCP servers to extend your agents with additional tools and integrations. This page covers how to add custom MCP servers and provides configuration details for popular remote servers. An [*MCP (Model Context Protocol) server*](https://modelcontextprotocol.io/docs/getting-started/intro) exposes tools that an agent can call at runtime. A remote MCP server:

- Runs outside of LangSmith (usually over HTTPS).
- Owns its own authentication and authorization.
- Acts as a bridge between your agent and an external system.

LangSmith Agent Builder doesn't execute these tools itself, it forwards requests to the MCP server and returns the results to the agent.

- Agent Builder discovers tools from remote MCP servers via the standard MCP protocol.
- Headers configured in your workspace are automatically attached when fetching tools or calling them. Headers are key-value pairs sent with every HTTP request to your MCP server. They're commonly used for authentication (like API keys or bearer tokens), but can also provide configuration information, content types, or custom metadata.
- Tools from remote servers are available alongside built-in tools in Agent Builder.

Runtime: Agent Builder automatically connects to your MCP server and uses its tools. The following sections show you how to connect a remote MCP server to Agent Builder:

- [General configuration](https://docs.langchain.com/langsmith/agent-builder-remote-mcp-servers/#general-configuration): Step-by-step instructions for connecting any remote MCP server with authentication headers. Use this if you're familiar with MCP servers and want a quick reference.
- [Example: Connecting a custom MCP server](https://docs.langchain.com/langsmith/agent-builder-remote-mcp-servers/#example-connecting-a-custom-mcp-server): A detailed walkthrough using a GitHub-based MCP server as an example. Use this if you want to see a complete end-to-end example with specific authentication details.
- Headers: Add key-value pairs sent with every request. The most common pattern is using an Authorization bearer token:
	- Key: `Authorization`
	- Value: `Bearer API_KEY`
- OAuth 2.1 (Auto): Select this for servers that support OAuth via dynamic client registration. You'll be prompted to log in with your account for that service.
- OAuth 2.1 (Manual): Select this for servers that support OAuth, but require specifying the client ID/secret beforehand. OAuth providers used in this flow must have PKCE enabled.

 Agent Builder stores tool references by MCP server URL. If you update the URL of a custom MCP server, existing agents will fail when attempting to call those tools because the stored URL no longer matches. To update an MCP server URL:

1. Update your MCP server URL in the workspace settings.
2. For each agent using tools from that server:
	- Remove the affected tools from the agent configuration.
	- Re-add the tools (they will now reference the new URL).
3. Test the agent to confirm tools work correctly.

 Here's a practical example of connecting Agent Builder to a GitHub MCP server that requires authentication:

The MCP server needs permission to access GitHub on your behalf. You'll do this using a GitHub Personal Access Token (PAT).

1. Go to GitHub → Settings → Developer settings.
2. Open Personal access tokens.
3. Create a Fine-grained token (recommended).

Grant read-only permissions:

- Contents: Read
- Issues: Read
- Pull requests: Read

Once created, copy the token. You won't be able to see it again.

- Authorization proves who you are.
- The MCP server validates the token.
- Every tool call from the agent includes these headers.

1. Navigate to Settings > Workspaces > Secrets.
2. Click Add secret.
3. Name: `GITHUB_TOKEN` (or any descriptive name).
4. Value: Your authentication token.
5. Save the secret.

In Settings > MCP Servers:

1. Click Add server.
2. Add a Name for the MCP server.
3. URL: Enter your MCP server URL (e.g., `https://mcp-github.example.com`)
4. Add authentication header:
	- Key: `Authorization`
	- Value: `Bearer {{GITHUB_TOKEN}}`
5. Save the configuration.

The tools from your MCP server are now available in Agent Builder. When you create or edit an agent, you'll see these tools alongside the built-in tools. All requests to your MCP server will include the authentication header automatically.

1. The agent decides it needs GitHub data.
2. It selects a tool exposed by the MCP server.
3. LangSmith forwards the request to the remote MCP server.
4. The server authenticates using your token.
5. GitHub data is fetched and returned.
6. The agent receives structured results and continues reasoning.

 Configuration details Option 1: Headers authentication Add the following headers: Option 2: OAuth authentication

1. Select OAuth 2.1 (Auto) as the auth type when adding the server.
2. Log in with your Arcade account when prompted.

 Configuration details

| Setting | Value |
| --- | --- |
| URL | `https://search-mcp.parallel.ai/mcp` |
| Auth type | Headers |

Add the following header: Configuration details

| Setting | Value |
| --- | --- |
| URL | `https://mcp.notion.com/mcp` |
| Auth type | OAuth 2.1 (Auto) |

1. Select OAuth 2.1 (Auto) as the auth type when adding the server.
2. Log in with your Notion account when prompted.
