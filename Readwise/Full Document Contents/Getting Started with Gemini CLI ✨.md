# Getting Started with Gemini CLI ✨

![rw-book-cover](https://miro.medium.com/v2/resize:fit:1200/1*sBKCCmRej6Cuiw_eusphtA.png)

## Metadata
- Author: [[Jack Wotherspoon]]
- Full Title: Getting Started with Gemini CLI ✨
- Category: #articles
- Summary: Gemini CLI is a free, open-source AI tool that runs in your terminal to help with coding and more. It offers powerful features like context files, built-in tools, and support for MCP servers to boost developer productivity. To start, just install it with NodeJS and sign in with your Google account.
- URL: https://medium.com/google-cloud/getting-started-with-gemini-cli-8cc4674a1371

## Full Document
Experience the power of Gemini **directly** **from your terminal** with [Gemini CLI](http://github.com/google-gemini/gemini-cli)!

> For developers, the command line interface (CLI) isn’t just a tool; it’s home. The terminal’s efficiency, ubiquity and portability make it the go-to utility for getting work done. And as developers’ reliance on the terminal endures, so does the demand for integrated AI assistance. — [Gemini CLI launch blog](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/?utm_campaign=CDR_0xc2a07d4f_awareness_b427663282&utm_medium=external&utm_source=blog)
> 
> 

**Gemini CLI** is now live! 🚀🎉

Let’s explore and answer all the important questions like “**What is it?**”, “**How do I get started**?”, and “**What can it do?**”.

![Gemini CLI start up screen.](https://miro.medium.com/v2/resize:fit:1000/1*sBKCCmRej6Cuiw_eusphtA.png)Gemini CLI start up screen.
### What is Gemini CLI?

[**Gemini CLI**](http://github.com/google-gemini/gemini-cli) is an *open-source* AI agent that brings the power of Gemini directly **into your terminal**. It provides lightweight access to Gemini, giving you the most direct path from prompt to model. While it excels at coding, Gemini CLI can do much more. It’s a versatile, local utility you can use for a wide range of tasks, from content generation and problem solving to deep research and task management.

***With the Gemini CLI you can:***

* Query and edit large codebases in and beyond **Gemini’s 1M token context window**.
* Generate new apps from PDFs or sketches, using **Gemini’s multimodal capabilities**.
* Automate operational tasks, like querying pull requests or handling complex rebases.
* Use **tools and MCP servers** to connect new capabilities, including media generation with Imagen, Veo or Lyria.
* Ground your queries with the **Google Search tool**, built in to Gemini.

### How to get started?

Install [NodeJS 18+](https://nodejs.org/en/download), then run:

```
npm install -g @google/gemini-cli  

```

You now have Gemini CLI installed, run it using the `gemini` command:

```
gemini  

```

When prompted, just sign in with your Google account! 🔑

### Why should you care?

Developers live in the command line, integrated AI assistance is a natural choice to improve your velocity and access to powerful tools. ✨

#### Unmatched Free Tier

To use Gemini CLI free-of-charge, you can simply login with a personal Google account and get a free [Gemini Code Assist](https://codeassist.google/) license. That free license gets you access to [Gemini 2.5 Pro](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-pro?utm_campaign=CDR_0xc2a07d4f_awareness_b427663282&utm_medium=external&utm_source=blog) and its massive 1 million token context window. To ensure you rarely, if ever, hit a limit during this preview, Gemini CLI offers the industry’s largest allowance: 60 model requests per minute and 1,000 requests per day at **no charge**.

### 5 Features of Gemini CLI You Need to Know

Here are a few awesome Gemini CLI features that you should be aware…

#### 1. GEMINI.md context files

Pass custom context (persona, build processes, style guide rules, etc.) to Gemini CLI using **GEMINI.md** context files.

**Example — Have Gemini CLI automatically lint/format all Python code 🐍**

```
# Example Python dev GEMINI.md file  
...  
  
## Mandatory Tooling  
To ensure all Python code adheres to these standards, the following commands **must** be run before committing any `.py` files. These commands will automatically fix many common issues and flag any that require manual intervention.  
  
When creating or modifying any `.py` Python files, you **must** run the following commands from the root of the project:  
  
1.  **Check and fix linting issues:**  
    ```bash  
    uvx ruff@latest check --fix .  
    ```  
2.  **Format the code:**  
    ```bash  
    uvx ruff@latest format .  
    ```  

```

You can view the combined context from your context files by running `/memory show` in the Gemini CLI.

![GEMINI.md context shown using /memory show command.](https://miro.medium.com/v2/resize:fit:1000/1*k0Thyl8TBTXZwpjrUgi7Qg.gif)GEMINI.md context shown using /memory show command.
To put it to the test, **ask** Gemini CLI to create a `main.py` file with the following code:

```
import sys,os  
import asyncio  
import requests  
  
def hello_world(name:str='World'):  
    print(f'Hello, {name}!')  
    unused_str = 'random string'  
  
if __name__=='__main__':  
  
  
  
  
    hello_world()  

```

There are *several* poorly formatted pieces of the code that the `ruff` commands added to the **GEMINI.md** file should be able to fix (spacing, double quotes instead of single quotes, etc. ).

![Gemini CLI creating a properly formatted code file using GEMINI.md context.](https://miro.medium.com/v2/resize:fit:1000/1*7xKXqTmZHVbCa6v4b9cK6w.gif)Gemini CLI creating a properly formatted code file using GEMINI.md context.
The code is now properly formatted. ✅

#### 2. Built-in tools (/tools)

Gemini CLI comes with many powerful pre-built tools (like **Google Search**) that can be viewed by running the `/tools` command.

![/tools — Lists built-in Gemini CLI tools.](https://miro.medium.com/v2/resize:fit:1000/1*mxJo3lFDwLq0i5eYM4CZVg.gif)/tools — Lists built-in Gemini CLI tools.
Gemini CLI is successfully able to ground it’s responses using the Google Search tool! 🏀

#### 3. MCP support (/mcp)

Gemini CLI is launching with Model Context Protocol (MCP) support already integrated! 🔌

To configure MCP servers with Gemini CLI, create a `.gemini/settings.json` file with the `mcpServers` field.

To view configured MCP servers and tools from within the Gemini CLI run `/mcp`.

**Example — GitHub MCP Server Configuration**

Below is an example of a `.gemini/settings.json` used to configure the GitHub MCP server:

```
{  
  "mcpServers": {  
    "github": {  
      "command": "npx",  
      "args": [  
        "-y",  
         "@modelcontextprotocol/server-github"  
      ],  
      "env": {  
       "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"  
      }  
    }  

```

Gemini CLI will automatically replace the `${GITHUB_PERSONAL_ACCESS_TOKEN}` placeholder from the `settings.json` file with the `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable (**which you must first set** using a command like `export GITHUB_PERSONAL_ACCESS_TOKEN=<YOUR_PAT>`).

![/mcp — List all connected MCP servers.](https://miro.medium.com/v2/resize:fit:1000/1*570jyX0hQoYa4k8wng5IyA.gif)/mcp — List all connected MCP servers.
#### 4. Shell mode (terminal passthrough)

The `!` prefix lets you interact with your system’s shell directly from within Gemini CLI.

![Shell mode activated using “!”.](https://miro.medium.com/v2/resize:fit:1000/1*zkLQlduqXb0uP0Z0aMUxRA.gif)Shell mode activated using “!”.
#### 5. Gemini CLI flags

The Gemini CLI provides flexible customization through the support of **many CLI flags**.

You can view all supported CLI flags by running the`--help` command:

```
gemini --help  

```

**Notable flags:**

* `**--yolo**` **:** YOLO mode, automatically accepts all actions withour prompting you for allowlisting.
* `**--model**`: Change the underlying Gemini model (default: gemini-2.5-pro)
* `**--prompt**:` Non-interactive mode, run a single query.

Example of using the Gemini CLI with `--prompt` flag:

```
gemini --prompt "what is a requirements.txt commonly used for in Python?"  

```

### 📣 **Gemini CLI News**

* 👨‍💻 Check out the official open source [Gemini CLI GitHub repository](https://github.com/google-gemini/gemini-cli/).
* 📑 Read the official [Gemini CLI launch blog](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/?utm_campaign=CDR_0xc2a07d4f_awareness_b427663282&utm_medium=external&utm_source=blog).
* 🧩 Complete the [Gemini CLI Getting Started Codelab](https://codelabs.developers.google.com/codelabs/codelabs/gemini-cli-getting-started?utm_campaign=CDR_0xc2a07d4f_awareness_b427663282&utm_medium=external&utm_source=blog).

### **📝 Feedback Wanted**

Have any questions? Run into any issues? We want to hear all about it!

Since Gemini CLI is fully open-source, you can [file issues](https://github.com/google-gemini/gemini-cli/issues), [start discussions](https://github.com/google-gemini/gemini-cli/discussions), or even [contribute code](https://github.com/google-gemini/gemini-cli/pulls), all on GitHub!
