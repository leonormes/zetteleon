# MCP-powered RAG Over Complex Docs

![rw-book-cover](https://www.dailydoseofds.com/content/images/size/w1200/2025/06/21d35589-12a2-4b8c-ba86-252100470cbe_1280x1076.gif)

## Metadata
- Author: [[Daily Dose of Data Science]]
- Full Title: MCP-powered RAG Over Complex Docs
- Category: #articles
- Summary: This post shows how MCP powers a RAG app for complex documents using Cursor IDE and EyelevelAI’s GroundX. GroundX parses and searches unstructured content so the MCP server can ingest and retrieve relevant chunks. The demo includes code, setup steps, and a video walkthrough.
- URL: https://share.google/mFsp2R4aYpdx1RfxG

## Full Document
In this chapter, let us show you how we used MCP to power an RAG application over complex documents.

To give you more perspective, here’s our document:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3107bc2a-b394-4837-87e9-5dfa4be73818_2262x840.png)
Here’s our tech Stack:

* Cursor IDE as the MCP client.
* [​**EyelevelAI's GroundX**​](https://eyelevel.ai/?ref=dailydoseofds.com) to build an MCP server that can process complex docs.

Here's how it works:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21d35589-12a2-4b8c-ba86-252100470cbe_1280x1076.gif)
* User interacts with the MCP client (Cursor IDE)
* Client connects to the MCP server and selects a tool.
* Tools leverage GroundX to do an advanced search over docs.
* Search results are used by the client to generate responses.

If you prefer to watch, we have added a video below:

#### Implementation details

Now, let's dive into the code! The GitHub repo with the code is linked later in the issue.

##### **1) Setup server**

First, we set up a local MCP server using FastMCP and provide a name.

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F261f061a-fa35-4837-ba85-6ed4c341bd62_680x403.png)
##### **2) Create GroundX Client**

GroundX offers capabilities document search and retrieval capabilities for complex real-world documents. You need to [​**get an API key here**​](https://eyelevel.ai/?ref=dailydoseofds.com) and store it in a `.env` file.

Once done, here's how to set up a client:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cc06150-9192-4a7b-8f7a-60dc87458f88_679x455.png)
##### **3) Create Ingestion tool**

This tool is used to ingest new documents into the knowledge base.

The user just needs to provide a path to the document to be ingested:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2523ff19-feeb-42ce-b87a-b3755a2c6ec9_680x662.png)
##### **4) Create Search tool**

This tool leverages GroundX’s advanced capabilities to do search and retrieval from complex real-world documents.

Here's how to implement it:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab0fb021-18b8-4f7b-8abc-a42fdd600060_680x546.png)
##### **5) Start the server**

Starts an MCP server using standard input/output (stdio) as the transport mechanism:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ee2a1e6-d2a1-4c9f-95af-e2a799de1a06_680x403.png)
##### **6) Connect to Cursor**

Inside your Cursor IDE, follow this:

* Cursor → Settings → Cursor Settings → MCP

Then add and start your server like this:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4842680a-9eb2-4ef4-9a13-2dd71dac22ff_680x558.png)
Done!

Now, you can interact with these documents directly through your Cursor IDE.

The video below gives a walk-through of what it looks like:

You can test [​**EyeLevel on your complex docs here →**​](https://eyelevel.ai/?ref=dailydoseofds.com)

We use EyeLevel on all complex use cases because they have built powerful enterprise-grade parsing systems that can intuitively chunk relevant content and understand what’s inside each chunk, whether it's text, images, or diagrams, as shown below:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3ef9ab2-7734-4dfb-aeb5-9c3876eb5b31_800x543.png)
As depicted above, the system takes an unstructured (text, tables, images, flow charts) input and parses it into a JSON format that LLMs can easily process to build RAGs over.

Also, find the code for this demo in [​**this GitHub repo →**​](https://github.com/patchy631/ai-engineering-hub/tree/main/eyelevel-mcp-rag?ref=dailydoseofds.com)

Let's move to the next project now!
