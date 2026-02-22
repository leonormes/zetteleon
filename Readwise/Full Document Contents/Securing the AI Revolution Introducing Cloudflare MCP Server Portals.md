# Securing the AI Revolution: Introducing Cloudflare MCP Server Portals

![rw-book-cover](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/40b0kS5aAIltcODm2P44OM/0f7e6145b1c8e9ba77f58cf486777141/OG_Share_2024__77_.png)

## Metadata
- Author: [[blog.cloudflare.com]]
- Full Title: Securing the AI Revolution: Introducing Cloudflare MCP Server Portals
- Category: #articles
- Summary: Cloudflare launched MCP Server Portals in open beta to centralize and secure connections between LLMs and apps. Portals route MCP traffic through Cloudflare to enforce access policies, logging, and least-privilege controls. This reduces risks like prompt injection, supply-chain exploits, and data leaks while Cloudflare adds more AI protections.
- URL: https://blog.cloudflare.com/zero-trust-mcp-server-portals/

## Full Document
##### **Securing the AI Revolution: Introducing Cloudflare MCP Server Portals**

[Large Language Models (LLMs)](https://www.cloudflare.com/learning/ai/what-is-large-language-model/) are rapidly evolving from impressive information retrieval tools into active, intelligent agents. The key to unlocking this transformation is the **Model Context Protocol (MCP)**, an open-source standard that allows LLMs to securely connect to and interact with any application — from Slack to Canva, to your own internal databases.

This is a massive leap forward. With MCP, an LLM client like Gemini, Claude, or ChatGPT can answer more than just "tell me about Slack." You can ask it: "What were the most critical engineering P0s in Jira from last week, and what is the current sentiment in the #engineering-support Slack channel regarding them? Then propose updates and bug fixes to merge."

This is the power of MCP: turning models into teammates.

But this great power comes with proportional risk. Connecting LLMs to your most critical applications creates a new, complex, and largely unprotected [attack surface](https://www.cloudflare.com/learning/security/what-is-an-attack-surface/). Today, we change that. We’re excited to announce Cloudflare **MCP Server Portals** are now available in Open Beta. MCP Server Portals are a new capability that enable you to centralize, secure, and observe every MCP connection in your organization. This feature is part of [Cloudflare One](https://www.cloudflare.com/zero-trust/), our [secure access service edge (SASE)](https://www.cloudflare.com/learning/access-management/what-is-sase/) platform that helps connect and protect your workspace.

##### **What Exactly is the Model Context Protocol?**

Think of [MCP](https://www.cloudflare.com/learning/ai/what-is-model-context-protocol-mcp/) as a universal translator or a digital switchboard for AI. It’s a standardized set of rules that lets two very different types of software—LLMs and everyday applications—talk to each other effectively. It consists of two primary components:

* **MCP Clients:** These are the LLMs you interact with, like ChatGPT, Claude, or Gemini. The client is the front end to the AI that you use to ask questions and give commands.
* **MCP Servers:** These can be developed for any application you want to connect to your LLM. SaaS providers like Slack or Atlassian may offer MCP servers for their products, or your own developers can also build custom ones for internal tools.

![](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/4Du5DBczqtDdq3qhNPbQWt/479d741dcef445f73b5da82e716fdd32/image3.png)
Credit: [Architecture Overview - Model Context Protocol](https://modelcontextprotocol.io/docs/learn/architecture)

For a useful connection, MCP relies on a few other key concepts:

* **Resources:** A mechanism for the server to give the LLM context. This could be a specific file, a database schema, or a list of users in an application.
* **Prompts:** Standardized questions the server can ask the client to get the information it needs to fulfill a request (e.g., "Which user do you want to search for?").
* **Tools:** These are the actions the client can ask the server to perform, like querying a database, calling an API, or sending a message.

Without MCP, your LLM is isolated. With MCP, it's integrated, capable of interacting with your entire software ecosystem in a structured and predictable way.

##### **The Peril of an Unsecured AI Ecosystem**

Think of an LLM as the most brilliant and enthusiastic junior hire you've ever had. They have boundless energy and can produce incredible work, but they lack the years of judgment to know what they *shouldn't* do. The current, decentralized approach to MCP is like giving that junior hire a master key to every office and server room on their first day.

It's not a matter of *if* something will go wrong, but *when*.

This "shadow AI" infrastructure is the modern equivalent of the early Internet, where every server had a public IP address, fully exposed to the world. It’s the Wild West of unmanaged connections, impossible to secure. And the risks go far beyond accidental data deletion. Attackers are actively exploiting the unique vulnerabilities of LLM-driven ecosystems:

* **Prompt and tool injection:** This is more than just telling a model to "ignore previous instructions." Attackers are now hiding malicious commands inside the descriptions of MCP tools themselves. Consider an LLM seeking to use a seemingly harmless "WebSearch" tool. A poisoned description could trick it into also running a query against a financial database and exfiltrating the results.
* **Supply chain attacks:** How can you trust the third-party MCP servers used by your teams? In mid-2025, a critical vulnerability ([**CVE-2025-6514**](https://nvd.nist.gov/vuln/detail/CVE-2025-6514)) was discovered in a popular npm package used for MCP authentication, exposing countless servers. In another incident dubbed "**NeighborJack**," security researchers found hundreds of MCP servers inadvertently exposed to the public Internet because they were bound to 0.0.0.0 without a firewall, allowing for potential OS command injection and host takeover.
* **Privilege escalation and the "confused deputy":** An attacker doesn't need to break your LLM; they just need to confuse it. In one documented case, an AI agent running with high-level privileges was tricked into executing SQL commands embedded in a support ticket. The agent, acting as a "confused deputy," couldn't distinguish the malicious SQL from the legitimate ticket data and dutifully executed the commands, compromising an entire database.
* **Data leakage:** Without centralized controls, data can bleed between systems in unexpected ways. [In June 2025](https://www.bleepingcomputer.com/news/security/asana-warns-mcp-ai-feature-exposed-customer-data-to-other-orgs/), a popular team collaboration tool’s MCP integration suffered a privacy breach where a bug caused some customer information to become visible in other customers' MCP instances, forcing them to take the integration offline for two weeks.

##### **The Solution: A Single Front Door for Your MCP Servers**

You can't protect what you can't see. **Cloudflare MCP Server Portals** solve this problem by providing a single, centralized gateway for all your MCP servers, somewhat similar to an application launcher for [single sign-on](https://www.cloudflare.com/learning/access-management/what-is-sso/). Instead of developers distributing dozens of individual server endpoints, they register their servers with Cloudflare. You provide your users with a single, unified Portal endpoint to configure in their MCP client.

![](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/5gIceb6D72AwuQSNjq0eqb/25147ec57731dd2e016887d6bab33f55/image1.png)
This changes the security posture and user experience immediately. By routing all MCP traffic through Cloudflare, you get:

* **Centralized policy enforcement:** You can integrate MCP Server Portals directly into Cloudflare One. This means you can enforce the same granular access policies for your AI connections that you do for your human users. Require [multi-factor authentication](https://www.cloudflare.com/learning/access-management/what-is-multi-factor-authentication/), check for device posture, restrict by geography, and ensure only the right users can access specific servers and tools.
* **Comprehensive visibility and logging:** Who is accessing which MCP server and which toolsets are they engaging with? What prompts are being run? What tools are being invoked? Previously, this data was scattered across every individual server. Server Portals aggregate all MCP request logs into a single place, giving you the visibility needed to audit activity and detect anomalies before they become breaches.
* **A curated AI user experience based on least privilege:** Administrators can now review and approve MCP servers before making them available to users through a Portal. When a user authenticates through their Portal, they are only presented with the curated list of servers and tools they are authorized to use, preventing the use of unvetted or malicious third-party servers. This approach adheres to the [Zero Trust security](https://www.cloudflare.com/learning/security/glossary/what-is-zero-trust/) best practice of [least privilege](https://www.cloudflare.com/learning/access-management/principle-of-least-privilege/).
* **Simplified user configuration:** Instead of having to load individual MCP server configurations into a MCP Client, users can load a single URL that pulls down all accessible MCP Servers. This drastically simplifies how many URLs need to be shared out and known by users. As new MCP Servers are added, they become dynamically available through the portal, instead of sharing each new URL on publishing of a server.

When a user connects to their MCP Server Portal, [Access](https://www.cloudflare.com/zero-trust/products/access/) prompts them to authenticate with their corporate identity provider. Once authenticated, Cloudflare enforces which MCP Servers the user has access to, regardless of the underlying server’s authorization policies. 

For MCP servers with domains hosted on Cloudflare, Access policies can be used to enforce the server’s direct authorization. This is done by creating an [OAuth server that is linked to the domain’s existing Access Application](https://developers.cloudflare.com/cloudflare-one/applications/configure-apps/mcp-servers/linked-apps/). For MCP servers with domains outside Cloudflare and/or hosted by a third party, they require [authorization controls](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) outside of Cloudflare Access, this is usually done using OAuth.

##### **The Road Ahead: What's Next for AI Security**

MCP Server Portals are a foundational step in our mission to secure the AI revolution. This is just the beginning. In the coming months, we plan to build on this foundation by:

* **Mechanisms to lock down MCP Servers:** Unless an MCP Server author enforces [Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) controls, users can still technically access MCPs outside of a Portal. We will build additional enforcement mechanisms to prevent this.
* **Integrating with Firewall for AI:** Imagine applying the power of our [WAF](https://www.cloudflare.com/application-services/products/waf/) to your MCP traffic, detecting and blocking prompt injection attacks before they ever reach your servers.
* **Cloudflare hosted MCP Servers:** We will make it easy to deploy MCP Servers using Cloudflare’s [AI Gateway](https://www.cloudflare.com/developer-platform/products/ai-gateway/). This will allow for deeper prompt filtering and controls.
* **Applying machine learning to detect abuse:** We will layer our own [machine learning models](https://www.cloudflare.com/learning/ai/what-is-machine-learning/) on top of your MCP logs to automatically identify anomalous behavior, such as unusual data exfiltration patterns or suspicious tool usage.
* **Enhancing the protocol:** We are committed to working with the open-source community to strengthen the MCP standard itself, contributing to a more secure and robust ecosystem for everyone.

This is our commitment: to provide the tools you need to innovate with confidence.

Progress doesn't have to come at the expense of security. With MCP Server Portals, you can empower your teams to build the future with AI, safely. This is a critical piece of helping to build a better Internet, and we are excited to see what you will build with it.

MCP Server Portals are now available in Open Beta for all Cloudflare One customers. To get started, navigate to the **Access > AI Controls** page in the Zero Trust Dashboard. If you don't have an account, you can [sign up today](https://dash.cloudflare.com/sign-up/zero-trust) and get started with up to 50 free seats or [contact our experts](https://www.cloudflare.com/products/zero-trust/plans/enterprise/?utm_medium=referral&utm_source=blog&utm_campaign=2025-q3-acq-gbl-connectivity-ge-ge-general-ai_week_blog) to explore larger deployments.

Cloudflare is also starting a user research program focused on AI security. If you are interested in previews of new functionality or want to help shape our roadmap, [please express your interest here](https://www.cloudflare.com/lp/ai-security-user-research-program-2025).
