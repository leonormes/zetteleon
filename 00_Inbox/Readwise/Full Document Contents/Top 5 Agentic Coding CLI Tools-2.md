# Top 5 Agentic Coding CLI Tools

![rw-book-cover](https://www.kdnuggets.com/wp-content/uploads/awan_top_5_agentic_coding_cli_tools_5.png)

## Metadata
- Author: [[Abid Ali Awan]]
- Full Title: Top 5 Agentic Coding CLI Tools
- Category: #articles
- Summary: The author reviews five AI coding CLI tools, highlighting Claude Code as the best overall and Droid as great for debugging. OpenCode offers deep customization, while Codex CLI works well with ChatGPT plans. Gemini CLI is free but less reliable and more difficult to use.
- URL: https://www.kdnuggets.com/top-5-agentic-coding-cli-tools

## Full Document
I have a complicated love-hate relationship with AI agentic coding. Today, I will share my experiences with top-performing AI-agentic coding CLI tools, providing a fully automated developer experience.

![Top 5 Agentic Coding CLI Tools](https://www.kdnuggets.com/wp-content/uploads/awan_top_5_agentic_coding_cli_tools_5.png)
Image by Author

#### # Introduction

I am currently trying to decide which tools to use for my MLOps and vibe coding projects. There is a new VS Code extension or command-line interface (CLI) app launching every day, claiming to lead in terminal benchmarks or topping the coding leaderboards. There is so much noise in the space that I am compelled to write this article to share my personal experiences with various Agentic Coding CLI tools and what I like about them. Please note that these are my personal experiences, so they may differ from those of others.

Additionally, all of the CLI tools mentioned below require **[Node.js](https://nodejs.org/en/download/)**, so it’s best to install that before testing them. I have also included the installation commands that you need to type into your terminal to start using these tools.

#### # 1. Claude Code

**[Claude Code](https://docs.claude.com/en/docs/claude-code/overview)** is a leading tool for vibe coding and overall professional development projects. You can connect your Anthropic API keys for token-based usage or link your Claude subscription for subscription-based usage.

I have been using Claude Code with the API, and it has worked really well so far. However, I recently discovered the **[GLM 4.6 Coding Plan](https://www.kdnuggets.com/vibe-coding-with-glm-46-coding-plan)** and started using Claude Code with GLM 4.6. This means you can modify your Claude Code to use any AI model provider, including local AI models.

All you need to do is run the following command in the terminal to get started:

```
npm install -g @anthropic-ai/claude-code
```

The best part about Claude Code is that I can just ask it to fix things or build components, and it will follow the instructions and provide a short response. This results in a low error rate, and it is quite proficient at invoking tools and terminal commands.

Claude Code is my main tool for daily tasks, as it also comes with a VS Code extension that lets me ask questions about my code and make modifications directly within the IDE. It is suitable for both professionals and hobbyists who want to build exciting projects.

#### # 2. OpenCode

Opinions on **[OpenCode](https://github.com/sst/opencode)** are divided; some people love it while others dislike it. OpenCode is a truly open-source alternative to Claude Code. It allows you to run any model and supports nearly all AI model providers, giving you the flexibility to set up without complex configurations. I use it to test new models, evaluate the MCPs, and build custom agents.

If you are a hardcore coder or a professional developer, you will appreciate the extensive customization options available to modify and improve OpenCode at a micro level. You will have control over security, design, functions, and overall project management in a controlled environment.

To get started, open your terminal and type the following command:

```
npm install -g opencode-ai@latest
```

You can even explore free models provided by OpenCode and connect to various models through openrouter.ai access.

I have been using OpenCode with the GLM Coding plan and the MiniMax-2 plan. Both have been effective for my needs, and I use OpenCode for building the UI of my website and app.

**Note:** If you are using Windows, please consider using the **[Alacritty](https://alacritty.org/)** terminal for the best experience.

#### # 3. Droid

**[Droid](https://factory.ai/)** by Factory is an amazing AI coding tool that is at the top of the terminal bench, meaning it is really good at solving local problems with your code. I have been using it for debugging and resolving my issues, as it can read the Docker logs, return Docker commands, and fix things automatically.

What I like the most is that it offers free usage when you create an account. This means you get a professional trial plan for a month, which helps you access the latest Claude and OpenAI models. I have been using it every day until my trial expired. I love it; it is simple and heavily maintained by developers.

To get started, type the following command in the terminal:

```
curl -fsSL https://app.factory.ai/cli | sh
```

If you are looking for accuracy in running commands, debugging, building, and automating your coding setup, I highly recommend you start with Droid. The only drawback is that it doesn't work well with custom models or external AI model providers. Perhaps on the backend, they have optimized the model so that it utilizes Droid to the fullest.

#### # 4. Codex CLI

I recently started using the **[openai/codex](https://github.com/openai/codex)** CLI, and I didn't realize that I could use it with my ChatGPT plan. The ChatGPT plan is much more valuable when you have access to VS Code extensions, terminal CLI tools for agentic coding, and cloud-based agentic workflows. If you prefer not to pay for the $20 ChatGPT subscription, you can still use it with the OpenAI Developer API.

What's even better is that you can modify the configuration file to use GLM or Minimax models as well. It is fully customizable, but the experience with external APIs can drop significantly, where it doesn't understand certain tags or calls the wrong tools. Therefore, it is highly recommended to use it with the ChatGPT subscription.

To get started, simply type the following command into your terminal and follow the instructions:

```
npm install -g @openai/codex
```

I have started using it because it is an almost free tool for me to access the latest OpenAI Codex and GPT-5 models. After Claude Code and Droid, I think I will continue using it for my projects. Stay tuned for my next update on the Agentic CLI tools soon.

#### # 5. Gemini CLI

Google has launched its open-source Agentic CLI, known as **[google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)**, similar to OpenAI and Microsoft Copilot. It is fully customizable, but I encountered many issues while trying to set it up and derive any value from it. If you accidentally use the Gemini 2.5 pro model, it will consume your free plan limit with just one prompt. Therefore, I primarily use the Gemini CLI for testing purposes only.

Another issue I faced was that, despite its customizability, I couldn't effectively set up MCP, agents, or other tools. I realized that it already comes with Google service tools, which encourages the use of these built-in features instead of relying on third-party tools.

To start using the Gemini CLI, type the following command in the terminal:

```
npm install -g @google/gemini-cli
```

The best part is that you get free access to Gemini CLI tools, as the free plan covers your basic needs. It automatically renews, so once you hit the limit, you can begin again the next day. While it is free, it does come with its hassles; this is why it's listed last. However, due to its popularity and being free to use, I decided to include it in the list.

#### # TL;DR

For people who scroll down to read the summary:

1. **Claude Code** is the best; use it as your primary tool
2. **OpenCode** is amazing if you like tinkering with your workflow to maximize productivity and value
3. **Droid** is really good at debugging and automating your developer experience
4. **Codex CLI** is improving and now includes features that allow you to build things both locally and in the cloud using the ChatGPT plan
5. **Gemini CLI** is popular due to its limited free plan, but I would highly discourage using it, as you may waste time and gain little value from it

There are other AI coding CLI tools out there, but they are not mature or popular enough for me to include here. All the CLI tools mentioned above work flawlessly on Windows, even without Windows Subsystem for Linux (WSL). So, go ahead and start typing the above commands to experience the new era of agentic coding.

****[Abid Ali Awan](https://abid.work)**** ([@1abidaliawan](https://www.linkedin.com/in/1abidaliawan)) is a certified data scientist professional who loves building machine learning models. Currently, he is focusing on content creation and writing technical blogs on machine learning and data science technologies. Abid holds a Master's degree in technology management and a bachelor's degree in telecommunication engineering. His vision is to build an AI product using a graph neural network for students struggling with mental illness.

##### More On This Topic
