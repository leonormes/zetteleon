# If MCP is the USB-C of AI agents, A2A is their Ethernet

![rw-book-cover](https://regmedia.co.uk/2023/12/02/ai_shutterstock.jpg)

## Metadata
- Author: [[Tobias Mann]]
- Full Title: If MCP is the USB-C of AI agents, A2A is their Ethernet
- Category: #articles
- Summary: MCP is a protocol that helps AI models connect to tools and data, like USB-C connects devices. A2A is another protocol that lets AI agents communicate and work together, like Ethernet connects computers. Both are supported by big tech companies and aim to improve how AI systems interact.
- URL: https://www.theregister.com/2025/07/12/ai_agent_protocols_mcp_a2a/#webview=1

## Full Document
We have protocols and standards for just about everything. It's generally helpful when we can all agree on how technologies should talk to one another. So, it was only a matter of time before the first protocols governing agentic AI started cropping up.

Anthropic's Model Context Protocol (MCP), for better or worse, is among the more recognizable of these protocols. Introduced last year, MCP makes it easier to connect models to external data stores, APIs, and other functions and tools; it also opened the door to another wave of security [threats](https://www.theregister.com/2025/06/18/asana_mcp_server_bug/).

However, MCP isn't the only AI-centric protocol gaining momentum. At Google I/O in April, the Chocolate Factory revealed its Agent-to-Agent (A2A) protocol. On the surface, MCP and A2A certainly sound a lot alike. They share a similar client-server architecture, use many of the same underlying messaging and transport protocols, and, despite their relative immaturity, have enjoyed significant industry backing.

You'd be forgiven for thinking this was the VHS and Betamax standards wars all over again, with two AI giants slugging it out over whose protocol will reign supreme. In reality, MCP and A2A address very different problems, with much of the confusion surrounding them rooted in the often vague definition of what the heck actually constitutes an AI agent. So, let's clear that up.

At a high level, agents are generally pretty simple: They usually feature some kind of model that is responsible for interpreting information and making decisions as to what to do with it. That model may have access to various functions or tools for retrieving or executing those tasks.

For example, a logging agent might use a tool to poll an API endpoint periodically for logs. If an anomaly is detected, it might use another tool to generate a support ticket for review by a human operator. If they can be made reliable enough, these agents might just be able to eliminate a number of pesky employees with their salaries, health care, and sick leave. And while early trials show agents have a [long way to go](https://www.theregister.com/2025/06/29/ai_agents_fail_a_lot/), major tech companies are already drawing up plans for who they'll [lay off first](https://www.theregister.com/2024/04/04/ai_replacement_jobs/).

Better protocols for how these agents should talk to one another may help them to get there. And this is where MCP and A2A come into play. We [explored](https://www.theregister.com/2025/04/21/mcp_guide/) MCP in depth back in April, but, in a nutshell, the protocol is "a universal, open standard for connecting AI systems with data sources."

In other words, MCP provides a standardized way for models to interact with existing resources, like a SQL database, Kubernetes cluster, or existing APIs. The protocol follows a standard client-server architecture with information exchanged using JSON-RPC, carried over Stdio, HTTP, or SSE depending on the specific use case.

[![Here's a high-level look at MCP's architecture. Credit: modelcontextprotocol.io](https://regmedia.co.uk/2025/04/11/mcp_architectural_diagram.jpg?x=442&y=306&infer_y=1)](https://regmedia.co.uk/2025/04/11/mcp_architectural_diagram.jpg)Here's a high-level look at MCP's architecture. Credit: modelcontextprotocol.io - Click to enlarge
The important bit here is that MCP is designed to facilitate communication between models and tools by exposing their capabilities in a standardized manner. This is why MCP is described by Anthropic as being like USB-C for AI. But, as we've previously [explored](https://www.theregister.com/2025/04/21/mcp_guide/), it's just one of many ways of doing so. For example, similar functionality can be achieved in LangChain.

If MCP is like USB, then you can think of A2A a bit like Ethernet. A2A also uses JSON-RPC, HTTP, and SSE, but it's instead intended to facilitate communications between agents.

[![Here's a breakdown of how Google's A2A Protocol works.](https://regmedia.co.uk/2025/07/11/a2a_flow.png?x=442&y=691&infer_y=1)](https://regmedia.co.uk/2025/07/11/a2a_flow.png)Here's a breakdown of how Google's A2A Protocol works. - Click to enlarge
These communications follow a fairly predictable path, which begins with a discovery phase where agents in a system essentially exchange business cards containing their name, what they can do, where to reach them, and how to authenticate. These agent cards also contain details on optional functionality, like streaming data over SSE, as well as the kinds of formats (i.e., text, images, audio, or video) that they can ingest or return.

Now that the agents are aware of one another, they can send each other tasks where one agent is acting as a client and the other as a server. However, it should be noted that these roles aren't necessarily fixed, and agents can act as the client or server depending on the context.

Once the task is created, the agent server sends back a message along with a task ID, which is used to track its progress, which is kind of important for longer running jobs. The client can either poll the server periodically, or, if both support SSE, the server can automatically provide updates on its progress.

This allows the task to flag missing information, like a user's email address or a support ticket's severity, which may be required to proceed. Once the task is completed, the result is sent from the server to the client in the form of an artifact, which might contain various parts including text, images, and structured JSON, among others.

Going back to our earlier example, the logging agent might send a support ticket via A2A to another agent that can perform diagnostics and assess whether it can be resolved automatically or needs human input.

A key impetus behind A2A is the idea that truly useful agentic systems will be assembled from multiple more specialized agents, some of which may have been developed internally, and others that are supplied by the software vendor.

As far as the protocol is concerned, A2A doesn't care whether an agent is using MCP to accomplish its goal; only that the agents all speak the same language and are clearly communicating their capabilities, limitations, and progress since, again, some tasks may not be completed in real time.

Since Google took the wraps off A2A at I/O this spring, the protocol has enjoyed broad support from model builders, cloud providers, and software vendors including Accenture, Arize, Atlassian, Workday, and Intuit, to name just a handful.

And with the backing of Amazon, Microsoft, Cisco, Salesforce, SAP, and ServiceNow, Google [announced](https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/) in June its intention to donate the A2A protocol to the Linux Foundation.

While both MCP and A2A have received strong support so far from tech giants, the AI ecosystem is still in its infancy, and the technology shows no signs of slowing down. Standards bodies, meanwhile, don't have a great track record for moving quickly, especially if there's a disagreement as to how something should be done or which features it should and shouldn't define. As such, it's entirely possible that new standards and protocols may emerge as the agentic systems are better understood. ®
