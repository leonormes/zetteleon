---
aliases: []
confidence: 
created: 2025-10-30T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:44Z
purpose: 
review_interval: 
see_also: []
source: "https://gemini.google.com/share/0989d399addd"
source_of_truth: []
status: 
tags: ["clipped", "llm_session"]
title: ‎Gemini - Efficient LLM Context on Laptop
type: 
uid: 
updated: 
---

I use LLM on my laptop. I want to efficiently add context so that a new LLM can have a default context to help me work. What is the most efficient format for giving LLM full context?

## Structuring for Success: The Most Efficient Formats for Providing LLM Context on Your Laptop

Providing a Large Language Model (LLM) with a default context on your local machine is crucial for streamlining your workflow. The most efficient format hinges on a trade-off between token count, human readability, and the complexity of the information you need to convey. For most users, **Markdown emerges as the superior choice for direct context**, complemented by **system prompts for persistent instructions** and **Retrieval-Augmented Generation (RAG) for extensive knowledge bases**.

### The Three Pillars of Efficient LLM Context

To effectively provide context to an LLM on your laptop, it's best to think in terms of three complementary methods:

1. **Direct Context Formatting:** How you structure the information you paste directly into your prompts.
2. **Persistent Default Context:** Setting up instructions that the LLM defaults to in every conversation.
3. **Dynamic External Context:** Enabling the LLM to pull in relevant information from a larger knowledge base on its own.

---

### 1\. Direct Context: Markdown for Clarity and Token Efficiency

When you need to provide specific information for a task, the way you format that text directly impacts both the model's comprehension and the number of tokens you use.

**Markdown** stands out as the most efficient format for several reasons:

- **Token Efficiency:** Markdown uses minimal characters for formatting (e.g., `#` for a heading, `*` for a list item). This translates to a lower token count compared to more verbose formats like JSON or XML, which require opening and closing tags for every data point. In some cases, Markdown can be **15-20% more token-efficient than JSON**.
- **Human Readability:** Markdown is easy to write and read, allowing you to quickly structure and verify the context you are providing.
- **LLM Comprehension:** LLMs are extensively trained on web content, much of which is structured with Markdown or similar conventions. They understand the hierarchical nature of headings, the separation of ideas in lists, and the emphasis of bold or italic text.

**Side-by-Side Comparison of Formats:**

| Data to Represent | Plain Text | JSON | Markdown |
| --- | --- | --- | --- |
| Project: "Website Redesign" with key contacts. | Project is Website Redesign. Lead is Jane Doe. | `{"project": "Website Redesign", "contacts": {"lead": "Jane Doe", "designer": "John Smith"}}` | `# Project: Website Redesign\n\n**Contacts:**\nLead: Jane Doe` |
| **Approximate Token Count** | ~10 tokens | ~25 tokens | ~15 tokens |

While JSON and YAML offer more rigid structure, their token overhead is generally not justified for direct context input, especially on a resource-constrained local machine.

#### Practical Examples of Structuring Information with Markdown

**For a Personal Knowledge Base:**

Markdown

```markdown
# My Personal Knowledge Base

## Topic: Machine Learning

### Key Concepts:
- **Supervised Learning:** Learning from labelled data.
- **Unsupervised Learning:** Finding patterns in unlabelled data.
- **Reinforcement Learning:** Learning through trial and error with rewards.

### Important Algorithms:
- **Linear Regression:** For predicting continuous values.
- **Logistic Regression:** For classification tasks.
```

**For Project Information:**

---

### 2\. Persistent Context: System Prompts and Custom Instructions

To avoid repeatedly providing the same background information, use the "system prompt" or "custom instructions" feature of your local LLM application. This sets a default context that influences the model's responses in every new conversation.

A well-crafted system prompt establishes the LLM's persona, your preferences, and any standing information it should always consider.

#### Examples of Effective System Prompts

**For a Writer:**

> "You are an expert editor and writing assistant. Your tone is encouraging and constructive. I am a novelist from the United Kingdom, so please use British English spelling and grammar. When I provide a piece of text, your primary role is to suggest improvements to clarity, flow, and prose. Do not rewrite entire sections unless I specifically ask you to."

**For a Programmer:**

> "You are a senior Python developer with expertise in data science libraries like Pandas and NumPy. When I ask for code, provide clean, well-commented Python 3 code. Adhere to PEP 8 standards. If a solution has multiple approaches, briefly explain the trade-offs of each. I am working on a project that uses the following libraries: \[list your project's main libraries\]."

**For a Researcher:**

> "You are a research assistant with a critical and analytical mindset. When I provide a research paper or article, help me to identify the key arguments, methodologies, and potential weaknesses. Summarise complex information concisely and highlight any unsubstantiated claims. Frame your analysis in a neutral, academic tone."

---

### 3\. Dynamic Context: Retrieval-Augmented Generation (RAG) for Large Knowledge Bases

For very large or frequently updated collections of information (e.g., your entire project documentation, a vast personal knowledge base, or a collection of research papers), providing it all as direct context is impractical due to context window limitations. This is where Retrieval-Augmented Generation (RAG) comes in.

A RAG system connects your LLM to a local database of your documents.When you ask a question, the system first searches your documents for the most relevant information and then feeds only that snippet to the LLM along with your query.

**How to Set Up a Simple Local RAG System:**

Setting up a local RAG system is becoming increasingly accessible with open-source tools. Here’s a simplified overview of the process:

1. **Choose Your Tools:**
	- **LLM Interface:** Tools like `Ollama`, `LM Studio`, or `GPT4All` allow you to run powerful open-source LLMs on your laptop.
	- **RAG Framework:** Libraries such as `LlamaIndex` or `LangChain` simplify the process of connecting your data to the LLM.
	- **Vector Database:** A lightweight local vector database like `Chroma DB` or `FAISS` (which is often integrated into the RAG frameworks) is needed to store and efficiently search your documents.
2. **The Basic Workflow:**
	- **Ingestion:** You point the RAG framework to your folder of documents (e.g., Markdown files, PDFs, text files). The framework then breaks these documents into smaller chunks and converts them into numerical representations (embeddings) which are stored in the vector database.
	- **Retrieval:** When you ask a question, your query is also converted into an embedding.The system then searches the vector database for the document chunks with the most similar embeddings.
	- **Generation:** The most relevant document chunks are then passed to the LLM as context along with your original question.The LLM then generates an answer based on this provided information.

Several open-source projects provide step-by-step guides and pre-built scripts to set up a simple local RAG pipeline, making it achievable even for those with limited programming experience.

### A Note on XML

While Markdown is generally recommended for its balance of efficiency and readability, some advanced use cases, particularly in production environments where you need to enforce a very strict structure for the LLM's output, can benefit from XML.The clear opening and closing tags of XML can help some models to better delineate different parts of a complex prompt and consistently generate structured output. However, for most individual users on a laptop, the increased token cost and reduced readability of XML make it less ideal than Markdown for providing default context.

By combining the token efficiency of Markdown for direct context, the persistence of well-crafted system prompts for your default persona and preferences, and the power of a local RAG system for your extensive knowledge base, you can create a highly efficient and context-aware LLM assistant on your own laptop.

I have this LLM framework. How can I improve it with rag so that it loads specific notes based on current tasks?

Excellent. You have a well-structured and comprehensive framework in your `ProdOS_Framework.md` document. Integrating Retrieval-Augmented Generation (RAG) is the logical next step to transform this from a static reference into a dynamic, intelligent system that actively assists you.

Here is a blueprint for how you can improve your framework with RAG to load specific notes based on your current tasks.

### Conceptual Blueprint: From Static Framework to Dynamic OS

The goal is to create a system where your ProdOS commands (e.g., `/define-project`, `/breakdown-tasks`) become RAG-powered triggers. When you issue a command, the system will not just rely on the LLM's general knowledge; it will first retrieve the relevant sections of your *own* documentation from your ProdOS folder structure, inject them as context, and then prompt the LLM to perform the task.

This turns the LLM into a true thought partner that operates according to *your* predefined standards and has access to the full context of your life and work.

---

### Step 1: Prepare Your Knowledge Corpus for Retrieval

Your current file structure is a perfect foundation for a RAG system. The key is to ensure your notes are optimised for retrieval.

1. **Atomic Notes:** Your file structure already suggests this with files like `[[workflow_principles]]` and `[[H5_Purpose_and_Principles]]`. Continue this practice. Each file should represent a single concept (a project plan, an area of focus, a standard). This makes retrieval more precise.
2. **Consistent Linking:** Use `[[wikilinks]]` consistently to connect related concepts. For example, your `[[H1_Projects]]` file for a specific project should link to its parent `[[H2_Areas_of_Focus]]` and any relevant `[[project_support_template]]` files. This graph structure can be used by more advanced RAG techniques to retrieve related notes.
3. **Structured Content:** Within each note, continue using Markdown headings. RAG frameworks like LlamaIndex can be configured to chunk your documents based on headings, which keeps related paragraphs together and improves the quality of the retrieved context.

Your knowledge corpus is the entire `Productivity OS/` directory, with a particular focus on the contents within:

- `00_ProdOS_Standards/`
- `02_Horizons_of_Focus/`
- `04_Project_Templates/` (specifically, the *filled-out* project plans)

### Step 2: Design the RAG-Powered Workflow

The magic happens when you map your ProdOS commands to specific RAG retrieval strategies. When you run a command, the system should automatically fetch the correct context layers before prompting the LLM.

Here’s how it would work for your key commands:

#### A. Command: /define-project "Organise Team offsite"

This command's purpose is to convert an idea into a clearly defined project.

- **RAG Retrieval Steps:**
	1. **Retrieve Layer 3 Templates:** The system automatically fetches `[[desired_outcome_template]]` and `[[natural_planning_template]]`.
	2. **Retrieve Layer 1 Standards:** It should also retrieve relevant standards like `[[workflow_principles]]` to ensure the plan aligns with your core rules (e.g., 100% Capture mandate).
- **Augmented Prompt to LLM:**

	```markdown
	User has initiated the /define-project command for "Organise team offsite".
	Using the provided templates and standards, guide the user through the Natural Planning Model to clarify this outcome.
	### Retrieved Context: Layer 3 Templates ###
	---
	<Content of desired_outcome_template.md>
	---
	<Content of natural_planning_template.md>
	---
	### Retrieved Context: Layer 1 Standards ###
	---
	<Content of workflow_principles.md>
	---
	Now, begin by asking the user about the project's Purpose...
	```

#### B. Command: /breakdown-tasks for "Project: Team Offsite"\`

The goal here is to generate specific Next Actions.

- **RAG Retrieval Steps:**
	1. **Retrieve the Specific Project Plan:** The system searches your `04_Project_Templates/` or `02_Horizons_of_Focus/H1_Projects/` directory for the "Team Offsite" project plan you just created.
	2. **Retrieve Layer 1 Contexts:** It must fetch `[[context_defaults]]` (e.g., @Computer, @Calls) and `[[energy_time_defaults]]` to correctly categorise the generated tasks.
	3. **Retrieve Task Template:** It fetches `[[task_breakdown_template]]` for formatting guidance.
- **Augmented Prompt to LLM:**

	```markdown
	User has initiated the /breakdown-tasks command for the "Team Offsite" project.
	Based on the project's brainstorming and organisation steps, generate a sequential checklist of single, physical, visible next actions.
	Organise these actions using the provided context defaults.
	### Retrieved Context: Project Plan ###
	---
	<Content of Project_Team_Offsite.md>
	---
	### Retrieved Context: Layer 1 Standards ###
	---
	<Content of context_defaults.md>
	---
	<Content of task_breakdown_template.md>
	---
	Now, generate the list of next actions for the "Team Offsite" project.
	```

### Step 3: Local Implementation Strategy

You can build this on your laptop using open-source tools.

1. **LLM Host:** Use **Ollama** to run open-source models (like Llama 3 or Mistral) locally. It's simple to set up and manage.
2. **RAG Framework:****LlamaIndex** is an excellent choice for this. It is a "data framework" for LLMs that excels at connecting them to your external data. You will use it to:
	- **Index your data:** Create a vector index of all the `.md` files in your `Productivity OS/` directory.
	- **Create a Query Engine:** This engine takes a user's prompt (like `/breakdown-tasks`), queries the vector index to find the most relevant notes (the retrieval step), and then automatically passes them to the LLM (the augmentation step).
3. **Vector Store:** LlamaIndex can use a simple file-based vector store by default, so you don't need a complex database. It will create a `storage` directory within your project to hold the index.

### Putting It Into Practice: A Simplified Example Workflow

1. **Setup:**
	- Install Ollama and pull a model: `ollama run llama3`
	- Install Python and LlamaIndex: `pip install llama-index-llms-ollama llama-index-embeddings-huggingface`
2. **Indexing Your ProdOS:**
	- Write a simple Python script (`ingest.py`) that uses LlamaIndex's `SimpleDirectoryReader` to load all your `.md` files from the `Productivity OS/` folder.
	- The script then creates a `VectorStoreIndex` from these documents and saves it to disk. You only need to run this script when you make significant changes to your ProdOS notes.
3. **Creating the Command Interface:**
	- Write another Python script (`query.py`) that acts as your command interface.
	- This script loads the saved index.
	- It would parse your input (e.g., `/breakdown-tasks Project: Team Offsite`).
	- Based on the command, it formulates a query to the RAG engine. For `/breakdown-tasks`, the query would be something like: `"Project plan for 'Team Offsite' AND context defaults AND task breakdown template"`.
	- The LlamaIndex query engine retrieves the relevant notes.
	- The script then combines these notes with your command into the final, augmented prompt and sends it to the Ollama LLM.
	- The LLM's response (the list of next actions) is then printed to your console.

By implementing this RAG-powered workflow, your ProdOS becomes a living system that actively uses your own documented standards and project plans to help you achieve stress-free productivity and a state of "Mind Like Water".

I have a AI agent in warp.dev terminal that has been refining this project. Give me a clear LLM prompt context to instruct it how to add the rag. What do install how to set it up and incorporate into the system

Of course. Here is a clear, copy-and-paste ready prompt context to give your AI agent in the warp.dev terminal. This prompt instructs it on the "what" and "how" of integrating the RAG system into your ProdOS framework.

---

### LLM Prompt Context: Implementing a Local RAG Pipeline for ProdOS

**SYSTEM PROMPT (Set the Agent's Role):**

> You are an expert-level AI Systems Engineer specialising in local RAG (Retrieval-Augmented Generation) pipelines. Your expertise is in Python, Ollama, and the LlamaIndex framework. You provide clear, step-by-step instructions with complete, runnable code blocks and shell commands. You will now guide me in upgrading my `ProdOS` framework.

**USER PROMPT (The Task and Implementation Plan):**

Hello Agent. I need to upgrade my static "Productivity OS" (ProdOS) framework into a dynamic, context-aware system using a local RAG pipeline. Your task is to provide a complete, step-by-step implementation plan that I can execute directly in my warp.dev terminal.

**1\. Project Objective:**

The goal is to augment my existing ProdOS commands, such as `/define-project` and `/breakdown-tasks`, with a RAG pipeline. This pipeline will search my local knowledge base (a directory of Markdown files) and inject relevant context into the LLM prompt before execution. This will ensure the LLM operates according to my predefined standards and has access to specific project data.

**2\. Existing Framework:**

- My entire knowledge base is located in a root directory named `Productivity OS/`.
- This directory contains subfolders like `00_ProdOS_Standards/`, `02_Horizons_of_Focus/`, and `04_Project_Templates/`, which hold all the context as individual `.md` files.
- The core logic is defined in `00_ProdOS_Framework.md`.

**3\. Required Technical Stack:**

- **LLM Runner:** Ollama
- **RAG Framework:** LlamaIndex
- **Language:** Python
- **Vector Store:** A simple, local file-based store created by LlamaIndex is sufficient.

**4\. Detailed Implementation Plan:**

Please provide a complete plan broken down into the following phases. For each phase, provide all necessary shell commands and full Python scripts with clear, explanatory comments.

**Phase 1: Environment Setup & Installation**

- Provide the shell commands to install Ollama and pull the `llama3` model.
- Provide the commands to create a Python virtual environment (`.venv`) and activate it.
- Provide the `pip install` command for all required libraries: `llama-index`, `llama-index-llms-ollama`, `llama-index-embeddings-huggingface`.

**Phase 2: Data Ingestion Script (`ingest.py`)**

- Write a Python script named `ingest.py`.
- This script must perform the following actions:
	1. Import necessary modules from `llama_index`.
	2. Point a `SimpleDirectoryReader` to the `./Productivity OS/` directory to load all `.md` files recursively.
	3. Create a `VectorStoreIndex` from the loaded documents.
	4. Persist the index to disk in a local directory named `./storage`.
	5. Print a confirmation message upon completion.

**Phase 3: Interactive RAG Agent Script (`prodos_agent.py`)**

- Write a Python script named `prodos_agent.py`.
- This script will be the main interactive agent. It must perform the following actions:
	1. Import necessary modules.
	2. Load the persisted index from the `./storage` directory.
	3. Initialise the Ollama LLM (`llama3`).
	4. Create a query engine from the index.
	5. Enter a main loop that prompts the user for a ProdOS command.
	6. **Implement Logic:** When a command is received (e.g., `/breakdown-tasks Project: Website Redesign`), the script must:
		- Formulate a new, more descriptive query for the RAG engine. For example, the input `/breakdown-tasks Project: Website Redesign` should be transformed into a query like `"Retrieve the project plan for 'Website Redesign', and the standards for 'context_defaults' and 'task_breakdown_template'"`.
		- Use the query engine to retrieve the relevant context from the indexed documents.
		- Construct a final, augmented prompt that includes the retrieved context and the original user command.
		- Send this augmented prompt to the LLM for a response.
		- Print the LLM's response in a clean format.
	7. Include an exit command (e.g., `quit` or `exit`).

Please ensure all code is complete, correct, and ready to be saved into files and executed. This plan should take me from a clean environment to a fully functional, RAG-powered ProdOS agent.

Review these ideas and incorporate into our plan for the agent

\### 1. \*\*Two Levels of Context You Need\*\*

\- \*\*Static / Long-term context\*\*: Things that rarely change (who you are, preferences, common workflows, domain knowledge, disabilities like ADHD that affect working style).

\- \*\*Dynamic / Session-specific context\*\*: Things relevant only to the current task (the project repo, current bug you’re debugging, meeting notes, etc.).

You don’t want to waste tokens retyping your life story every time, but you \*do\* want some baked-in personality.

\---

\### 2. \*\*Efficient Formats\*\*

\#### a. \*\*Structured JSON / YAML prompt\*\*

Most efficient + machine-readable way is to store your persistent info in structured form. LLMs handle JSON \*very well\*. Example:

\`\`\`json

{

"user": {

"name": "John Doe",

"location": "Essex, UK",

"profession": "Software Developer",

"birthday": "1973-11-03",

"traits": \["ADHD", "prefers concise technical explanations"\],

"communication\_style": "casual, focused, step-by-step"

},

"context\_rules": {

"default\_language": "python",

"code\_style": "readable, modular, with comments only when necessary",

"preferred\_format": "markdown",

"dont": \["repeat context unless relevant", "over-apologize"\],

"do": \["suggest productivity hacks for ADHD", "use clear structure"\]

}

}

\`\`\`

You can prepend this as a \*\*system prompt\*\* or inject it once at startup.

\---

\#### b. \*\*Instructional system prompt (compressed natural language)\*\*

If token cost is tight, compress context into a \*\*system persona\*\*:

\`\`\`

You are assisting John, a 51-year-old programmer from Essex with ADHD.

He prefers concise, step-by-step explanations, markdown formatting, and Python for examples.

Keep responses friendly but efficient.

Default assumptions: programming context = software development; explanations should balance clarity and efficiency.

Avoid repetition unless he asks to recap.

\`\`\`

This is less structured, but compact.

\---

\#### c. \*\*External memory + retrieval\*\*

Most efficient \*scalable\* way:

\- Save long-term memory as a JSON/YAML/markdown file on disk.

\- When starting a new session, load the chunk relevant to the conversation into the prompt.

\- Or better yet, use \*\*RAG (retrieval-augmented generation)\*\* so the LLM pulls only the needed slices of context.

\---

\### 3. \*\*Efficiency Tips\*\*

\- \*\*Prioritize\*\*: Don’t dump \*everything\*. Break context into tiers (critical, frequently used, rarely used).

\- \*\*Compress\*\*: Rewrite important facts in short, declarative form. Avoid verbose prose.

\- \*\*Modularize\*\*: Use small reusable blocks ("CodingPreferences", "CommunicationStyle").

\- \*\*Automate preload\*\*: Wrap your LLM startup script to always prepend this default context (like a \`.bashrc\` for AI).

\---

✅ \*\*Best tradeoff in practice\*\*:

\- Store core info in \*\*JSON\*\* (easy to maintain + expand).

\- Convert into a \*\*short natural language system prompt\*\* at session start.

\- Use \*\*retrieval or selective injection\*\* for less-common long-term knowledge.

\---

Do you want me to sketch out a \*\*ready-to-use \`.json\` "self-profile" template\*\* that you could plug into any LLM wrapper (like \`llama.cpp\`, \`openai\`, \`ollama\` etc.)? That way you can just maintain one file and drop it in.

Excellent. These ideas provide a crucial layer of sophistication to our plan. Incorporating the distinction between static (user profile) and dynamic (task-specific notes) context is the key to making the agent truly personalised and efficient.

Here is the revised, comprehensive LLM prompt for your agent in warp.dev. It integrates these new concepts directly into the implementation plan.

---

### LLM Prompt Context V2: Implementing a Two-Tiered RAG Pipeline for ProdOS

**SYSTEM PROMPT (Set the Agent's Role):**

> You are an expert-level AI Systems Engineer specialising in local RAG (Retrieval-Augmented Generation) pipelines. Your expertise is in Python, Ollama, and the LlamaIndex framework. You provide clear, step-by-step instructions with complete, runnable code blocks and shell commands. You will now guide me in upgrading my `ProdOS` framework with a sophisticated, two-tiered context system.

**USER PROMPT (The Task and Refined Implementation Plan):**

Hello Agent. We are refining our plan to upgrade the ProdOS framework. Your new task is to architect and provide the implementation plan for a **two-tiered context system**, incorporating a static user profile and a dynamic RAG pipeline.

**1\. Updated Project Objective:**

The goal is to create a system that intelligently manages two distinct levels of context:

- **Tier 1: Static / Long-term Context:** A persistent user profile (in JSON format) that defines my identity, preferences, and core working style. This will be loaded at startup and converted into a concise system prompt to avoid wasting tokens on every query.
- **Tier 2: Dynamic / Session-specific Context:** The RAG pipeline that we previously designed. It will retrieve relevant notes from my ProdOS knowledge base on-demand based on the current task or command.

**2\. Detailed Implementation Plan:**

Please provide a complete, updated plan broken down into the following phases. Ensure all shell commands and Python scripts are complete, commented, and reflect this new two-tiered architecture.

**Phase 1: Environment and Static Context Setup**

- Provide the shell commands to set up the Python virtual environment and install all necessary libraries (`llama-index`, `llama-index-llms-ollama`, `llama-index-embeddings-huggingface`).
- **New Requirement:** Provide the code for a template file named `user_profile.json`. This file should be structured with two main keys: `"user"` and `"context_rules"`, containing details like profession, working traits (e.g., ADHD), and communication preferences. Crucially, add a key `prodos_root_path` to this file, pointing to the location of the knowledge base (e.g., `"./Productivity OS/"`).

**Phase 2: Data Ingestion Script (`ingest.py`)**

- Write a Python script named `ingest.py`.
- **New Requirement:** This script must first read `user_profile.json` to get the `prodos_root_path`.
- It must then use LlamaIndex's `SimpleDirectoryReader` to load all `.md` files from that path.
- Finally, it should create and persist the vector index to a local `./storage` directory. This makes the ingestion process configurable.

**Phase 3: The Two-Tiered Interactive Agent (`prodos_agent.py`)**

- Write the main Python script named `prodos_agent.py`.
- This script must integrate both context tiers. At startup, it should perform the following actions:
	1. **Load Static Context:** Read and parse the `user_profile.json` file.
	2. **Generate System Prompt:** Programmatically generate a compressed, natural-language system prompt from the JSON data. For example: *"You are assisting John, a programmer from Essex with ADHD. He prefers concise, step-by-step explanations and markdown formatting..."*. This generated string will be used as the persistent persona for the LLM.
	3. **Load Dynamic Context Index:** Load the RAG index from the `./storage` directory and initialise the query engine.
- **The Main Interactive Loop:**
	1. The script should prompt the user for a ProdOS command.
	2. When a command is received (e.g., `/breakdown-tasks Project: Website Redesign`), the script must perform the RAG retrieval as planned before (formulating a query, fetching relevant notes).
	3. **Crucial Integration Step:** The script must then make a call to the Ollama LLM, providing **both** the generated system prompt (Tier 1) and the augmented user prompt containing the RAG-retrieved notes (Tier 2).
	4. Print the LLM's final, context-aware response.

Please ensure the final output is a self-contained guide. The `prodos_agent.py` script is the most critical part and must clearly demonstrate how to load the JSON, generate the system prompt, and use it in combination with the RAG query results for every interaction.

Google Account

Leon Ormes

leonormes@gmail.com
