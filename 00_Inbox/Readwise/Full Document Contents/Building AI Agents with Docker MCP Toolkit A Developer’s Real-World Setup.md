# Building AI Agents with Docker MCP Toolkit: A Developer’s Real-World Setup

![rw-book-cover](https://www.docker.com/app/uploads/2025/03/image.png)

## Metadata
- Author: [[Rajesh Padmakumaran]]
- Full Title: Building AI Agents with Docker MCP Toolkit: A Developer’s Real-World Setup
- Category: #articles
- Summary: The post shows a real developer setup that builds an AI agent to answer questions about a GitHub repo using the Docker MCP Toolkit. MCP Gateway runs as a container to handle GitHub APIs while Docker Compose orchestrates services so the agent code stays clean and portable. This containerized approach makes setup repeatable, scalable, and faster to iterate for real-world production use.
- URL: https://share.google/EBMFpg5OxVkTvpLVw

## Full Document
Building AI agents in the real world often involves more than just making model calls — it requires integrating with external tools, handling complex workflows, and ensuring the solution can scale in production.

In this post, we’ll walk through a real-world developer setup for creating an agent using the Docker MCP Toolkit.

To make things concrete, I’ve built an agent that takes a Git repository as input and can answer questions about its contents — whether it’s explaining the purpose of a function, summarizing a module, or finding where a specific API call is made. This simple but practical use case serves as a foundation for exploring how agents can interact with real-world data sources and respond intelligently.

I built and ran it using the Docker MCP Toolkit, which made setup and integration fast, portable, and repeatable. This blog walks you through that developer setup and explains why Docker MCP is a game changer for building and running agents.

#### Use Case: GitHub Repo Question-Answering Agent

The goal: Build an AI agent that can connect to a GitHub repository, retrieve relevant code or metadata, and answer developer questions in plain language.

Example queries:

* “Summarize this repo: `https://github.com/owner/repo`”
* “Where is the authentication logic implemented?”
* “List main modules and their purpose.”
* “Explain the function `parse_config` and show where it’s used.”

**This goes beyond a simple code demo — it reflects how developers work in real-world environments**

* The agent acts like a code-aware teammate you can query anytime.
* The MCP Gateway handles tooling integration (GitHub API) without bloating the agent code.
* Docker Compose ties the environment together so it runs the same in dev, staging, or production.

Without MCP Toolkit, you’d spend hours wiring up API SDKs, managing auth tokens, and troubleshooting environment differences.

With MCP Toolkit:

1. Containerized connectors – Run the GitHub MCP Gateway as a ready-made service (`docker/mcp-gateway:latest`), no SDK setup required.
2. Consistent environments – The container image has fixed dependencies, so the setup works identically for every team member.
3. Rapid integration – The agent connects to the gateway over HTTP; adding a new tool is as simple as adding a new container.
4. Iterate faster – Restart or swap services in seconds using `docker compose`.
5. Focus on logic, not plumbing – The gateway handles the GitHub-specific heavy lifting while you focus on prompt design, reasoning, and multi-agent orchestration.

Running everything via Docker Compose means you treat the entire agent environment as a single deployable unit:

* One-command startup – `docker compose up` brings up the MCP Gateway (and your agent, if containerized) together.
* Service orchestration – Compose ensures dependencies start in the right order.
* Internal networking – Services talk to each other by name (`http://mcp-gateway-github:8080`) without manual port wrangling.
* Scaling – Run multiple agent instances for concurrent requests.
* Unified logging – View all logs in one place for easier debugging.

![Architecture overview: Docker MCP Gateway to GitHub](https://www.docker.com/app/uploads/2025/08/image1-6.png)This setup connects a developer’s local agent to GitHub through a Dockerized MCP Gateway, with Docker Compose orchestrating the environment. Here’s how it works step-by-step:
* The developer runs the agent from a CLI or terminal.
* They type a question about a GitHub repository — e.g., “Where is the authentication logic implemented?”

* The Agent (LLM + MCPTools) receives the question.
* The agent determines that it needs repository data and issues a tool call via MCPTools.

* MCPTools sends the request using `streamable-http` to the MCP Gateway running in Docker.
* This gateway is defined in `docker-compose.yml` and configured for the GitHub server (`--servers=github --port=8080`).

* The MCP Gateway handles all GitHub API interactions — listing files, retrieving content, searching code — and returns structured results to the agent.

* The agent sends the retrieved GitHub context to OpenAI GPT-4o as part of a prompt.
* The LLM reasons over the data and generates a clear, context-rich answer.

* The agent prints the final answer back to the CLI, often with file names and line references.

The detailed source code for this setup is available at this [link](https://github.com/rajeshsgr/mcp-demo-agents/tree/main).

Rather than walk through it line-by-line, here’s what each file does in the real-world developer setup:

* Defines the MCP Gateway service for GitHub.
* Runs the `docker/mcp-gateway:latest` container with GitHub as the configured server.
* Exposes the gateway on port `8080`.
* Can be extended to run the agent and additional connectors as separate services in the same network.

* Implements the GitHub Repo Summarizer Agent.
* Uses `MCPTools` to connect to the MCP Gateway over `streamable-http`.
* Sends queries to GitHub via the gateway, retrieves results, and passes them to GPT-4o for reasoning.
* Handles the interactive CLI loop so you can type questions and get real-time responses.

In short: the Compose file manages *infrastructure and orchestration*, while the Python script handles *intelligence and conversation*.

git clone https://github.com/rajeshsgr/mcp-demo-agents/tree/main

Create a .env file in the root directory and add your OpenAI API key:

To allow the MCP Gateway to access GitHub repositories, set your GitHub personal access token:

Bring up the GitHub MCP Gateway container using Docker Compose:

Enter your query: `Summarize https://github.com/owner/repo`

This setup is built with production realities in mind —

* **Docker** ensures each integration (GitHub, databases, APIs) runs in its own isolated container with all dependencies preconfigured.
* **MCP** acts as the bridge between your agent and real-world tools, abstracting away API complexity so your agent code stays clean and focused on reasoning.
* **Docker Compose** orchestrates all these moving parts, managing startup order, networking, scaling, and environment parity between development, staging, and production.

**From here, it’s easy to add:**

* More MCP connectors (Jira, Slack, internal APIs).
* Multiple agents specializing in different tasks.
* CI/CD pipelines that spin up this environment for automated testing

By combining **Docker** for isolation, **MCP** for seamless tool integration, and **Docker Compose** for orchestration, we’ve built more than just a working AI agent — we’ve created a repeatable, production-ready development pattern. This approach removes environment drift, accelerates iteration, and makes it simple to add new capabilities without disrupting existing workflows. Whether you’re experimenting locally or deploying at scale, this setup ensures your agents are reliable, maintainable, and ready to handle real-world demands from day one.

| **Aspect** | **Without Docker + MCP + Compose** | **With Docker + MCP + Compose** |
| --- | --- | --- |
| **Environment Setup** | Manual SDK installs, dependency conflicts, “works on my machine” issues. | Prebuilt container images with fixed dependencies ensure identical environments everywhere. |
| **Integration with Tools (GitHub, Jira, etc.)** | Custom API wiring in the agent code; high maintenance overhead. | MCP handles integrations in separate containers; agent code stays clean and focused. |
| **Startup Process** | Multiple scripts/terminals; manual service ordering. | `docker compose up` launches and orchestrates all services in the right order. |
| **Networking** | Manually configuring ports and URLs; prone to errors. | Internal Docker network with service name resolution (e.g., `http://mcp-gateway-github:8080`). |
| **Scalability** | Scaling services requires custom scripts and reconfigurations. | Scale any service instantly with `docker compose up --scale`. |
| **Extensibility** | Adding a new integration means changing the agent’s code and redeploying. | Add new MCP containers to `docker-compose.yml` without modifying the agent. |
| **CI/CD Integration** | Hard to replicate environments in pipelines; brittle builds. | Same Compose file works locally, in staging, and in CI/CD pipelines. |
| **Iteration Speed** | Restarting services or switching configs is slow and error-prone. | Containers can be stopped, replaced, and restarted in seconds. |
