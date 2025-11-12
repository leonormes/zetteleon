# Building an MCP-Powered AI Agent with Gemini and mcp-agent Framework: A Step-by-Step Implementation Guide

![rw-book-cover](http://www.marktechpost.com/wp-content/uploads/2025/08/blog-banner-8.png)

## Metadata
- Author: [[Asif Razzaq - August 17]]
- Full Title: Building an MCP-Powered AI Agent with Gemini and mcp-agent Framework: A Step-by-Step Implementation Guide
- Category: #articles
- Summary: The tutorial shows how to build an AI agent using the mcp-agent framework and Gemini.  
It creates an MCP tool server (search, analysis, code execution, weather) and connects it to Gemini.  
The agent is modular, asynchronous, and combines tool outputs with Gemini for context-aware answers.
- URL: https://www.marktechpost.com/2025/08/17/building-an-mcp-powered-ai-agent-with-gemini-and-mcp-agent-framework-a-step-by-step-implementation-guide/

## Full Document
In this tutorial, we walk through building an advanced AI agent using the [**mcp-agent**](https://github.com/lastmile-ai/mcp-agent) and Gemini. We start by setting up a robust environment with all the necessary dependencies and then implement an MCP tool [server](https://www.marktechpost.com/2025/08/08/proxy-servers-explained-types-use-cases-trends-in-2025-technical-deep-dive/) that provides structured services such as web search, data analysis, code execution, and weather information. By wiring these tools into an MCP client powered by Gemini, we demonstrate how context-aware reasoning can be combined with external tool execution. Throughout, we emphasize asynchronous design, tool schema definition, and seamless integration between the MCP layer and Gemini’s generative capabilities, ensuring our agent remains modular, extensible, and production-ready. Check out the **[FULL CODES here](https://github.com/Marktechpost/AI-Tutorial-Codes-Included/blob/main/mcp_gemini_agent_tutorial_Marktechpost.ipynb)**.

```
import subprocess
import sys
import os
from typing import Dict, List, Any, Optional, Union
import json
import asyncio
from datetime import datetime
import logging

def install_packages():
   """Install required packages for the tutorial"""
   packages = [
       'mcp',
       'google-generativeai',
       'requests',
       'beautifulsoup4',
       'matplotlib',
       'numpy',
       'websockets',
       'pydantic'
   ]
  
   for package in packages:
       try:
           subprocess.check_call([sys.executable, "-m", "pip", "install", package])
           print(f"✅ Successfully installed {package}")
       except subprocess.CalledProcessError as e:
           print(f"❌ Failed to install {package}: {e}")

install_packages()
```

We begin by defining an install\_packages function that specifies all the dependencies required for our tutorial, including mcp-agent, Gemini, and supporting libraries. We then run this function to automatically install each package, ensuring our environment is fully prepared before proceeding further. Check out the **[FULL CODES here](https://github.com/Marktechpost/AI-Tutorial-Codes-Included/blob/main/mcp_gemini_agent_tutorial_Marktechpost.ipynb)**.

```
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent, ImageContent, EmbeddedResource
import mcp.types as types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

We import all the core libraries we need, from Gemini and web scraping utilities to visualization and numerical tools. We also bring in the mcp-agent modules for protocol communication and configure logging so that we can track our agent’s execution flow in real time. Check out the **[FULL CODES here](https://github.com/Marktechpost/AI-Tutorial-Codes-Included/blob/main/mcp_gemini_agent_tutorial_Marktechpost.ipynb)**.

We design the MCPToolServer class that defines and manages all the tools our agent can use, including web search, data analysis, code execution, and weather information. We implement async methods for each tool, enabling the agent to perform the requested operation, such as fetching Wikipedia text, generating visualizations, executing Python snippets, or simulating weather data, and return the results in a structured format. This structure makes our MCP server modular and easily extensible for adding more tools in the future. Check out the **[FULL CODES here](https://github.com/Marktechpost/AI-Tutorial-Codes-Included/blob/main/mcp_gemini_agent_tutorial_Marktechpost.ipynb)**.

We define an MCPAgent that wires Gemini to our MCP tool server and maintains conversation history, enabling us to reason, decide on a tool, execute it, and synthesize the result. We fetch the Gemini API key, configure the model, and in process\_request, we prompt Gemini to choose a tool (or answer directly), run the selected tool asynchronously, and compose a final response grounded in the tool output. Check out the **[FULL CODES here](https://github.com/Marktechpost/AI-Tutorial-Codes-Included/blob/main/mcp_gemini_agent_tutorial_Marktechpost.ipynb)**.

We run a scripted demo that initializes MCPAgent, executes a suite of representative queries, and prints Gemini-driven, tool-augmented responses with short pauses between runs. We then drop into an interactive loop where we can list tools, send arbitrary prompts, and observe end-to-end MCP orchestration, before printing a concise recap of the concepts covered.

In conclusion, we now have a comprehensive MCP agent that dynamically decides when to use external tools and how to merge their outputs into meaningful responses. We validate the agent across multiple queries, showcasing its ability to search, analyze, generate, and simulate real-world interactions with Gemini as the reasoning engine. By combining structured MCP protocols with the flexibility of Gemini, we create a template for building powerful AI systems that are both interactive and technically grounded.

Check out the **[FULL CODES here](https://github.com/Marktechpost/AI-Tutorial-Codes-Included/blob/main/mcp_gemini_agent_tutorial_Marktechpost.ipynb)**. Feel free to check out our **[GitHub Page for Tutorials, Codes and Notebooks](https://github.com/Marktechpost/AI-Tutorial-Codes-Included)**. Also, feel free to follow us on **[Twitter](https://x.com/intent/follow?screen_name=marktechpost)** and don’t forget to join our **[100k+ ML SubReddit](https://www.reddit.com/r/machinelearningnews/)** and Subscribe to **[our Newsletter](https://www.aidevsignals.com/)**.
