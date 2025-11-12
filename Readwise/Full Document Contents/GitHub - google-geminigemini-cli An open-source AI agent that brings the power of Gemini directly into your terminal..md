# GitHub - google-gemini/gemini-cli: An open-source AI agent that brings the power of Gemini directly into your terminal.

![rw-book-cover](https://opengraph.githubassets.com/1f71c728830266034059be970e2502754004f54328e6453f44712c665332eb2d/google-gemini/gemini-cli)

## Metadata
- Author: [[GitHub]]
- Full Title: GitHub - google-gemini/gemini-cli: An open-source AI agent that brings the power of Gemini directly into your terminal.
- Category: #articles
- Summary: The Gemini CLI is a free tool that lets you use Google's Gemini AI directly in your terminal to work with code and automate tasks. It helps you manage large projects, create apps from PDFs or sketches, and connect to other tools like Google Search and media generators. You can start quickly by installing it with Node.js and signing in with your Google account for access.
- URL: https://share.google/l4OWFKToEnh2hojJv

## Full Document
### google-gemini/gemini-cli

Open more actions menu

#### Folders and files

#### Repository files navigation

* [README](https://github.com/google-gemini/gemini-cli#)
* [Apache-2.0 license](https://github.com/google-gemini/gemini-cli#)
* [Security](https://github.com/google-gemini/gemini-cli#)

### Gemini CLI

[![Gemini CLI CI](https://github.com/google-gemini/gemini-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/google-gemini/gemini-cli/actions/workflows/ci.yml)
[![Gemini CLI Screenshot](https://github.com/google-gemini/gemini-cli/raw/main/docs/assets/gemini-screenshot.png)](https://github.com/google-gemini/gemini-cli/blob/main/docs/assets/gemini-screenshot.png)
This repository contains the Gemini CLI, a command-line AI workflow tool that connects to your tools, understands your code and accelerates your workflows.

With the Gemini CLI you can:

* Query and edit large codebases in and beyond Gemini's 1M token context window.
* Generate new apps from PDFs or sketches, using Gemini's multimodal capabilities.
* Automate operational tasks, like querying pull requests or handling complex rebases.
* Use tools and MCP servers to connect new capabilities, including [media generation with Imagen, Veo or Lyria](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/tree/main/experiments/mcp-genmedia)
* Ground your queries with the [Google Search](https://ai.google.dev/gemini-api/docs/grounding) tool, built in to Gemini.

#### Quickstart

1. **Prerequisites:** Ensure you have [Node.js version 18](https://nodejs.org/en/download) or higher installed.
2. **Run the CLI:** Execute the following command in your terminal:

 
```
npx https://github.com/google-gemini/gemini-cli
```
 Or install it with:

 
```
npm install -g @google/gemini-cli
gemini
```
3. **Pick a color theme**
4. **Authenticate:** When prompted, sign in with your personal Google account. This will grant you up to 60 model requests per minute and 1,000 model requests per day using Gemini.

You are now ready to use the Gemini CLI!

##### For advanced use or increased limits:

If you need to use a specific model or require a higher request capacity, you can use an API key:

1. Generate a key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Set it as an environment variable in your terminal. Replace `YOUR_API_KEY` with your generated key.

 
```
export GEMINI_API_KEY="YOUR_API_KEY"
```

For other authentication methods, including Google Workspace accounts, see the [authentication](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/authentication.md) guide.

#### Examples

Once the CLI is running, you can start interacting with Gemini from your shell.

You can start a project from a new directory:

```
cd new-project/
gemini
> Write me a Gemini Discord bot that answers questions using a FAQ.md file I will provide
```

Or work with an existing project:

```
git clone https://github.com/google-gemini/gemini-cli
cd gemini-cli
gemini
> Give me a summary of all of the changes that went in yesterday
```

##### Next steps

* Learn how to [contribute to or build from the source](https://github.com/google-gemini/gemini-cli/blob/main/CONTRIBUTING.md).
* Explore the available **[CLI Commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md)**.
* If you encounter any issues, review the **[Troubleshooting guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/troubleshooting.md)**.
* For more comprehensive documentation, see the [full documentation](https://github.com/google-gemini/gemini-cli/blob/main/docs/index.md).
* Take a look at some [popular tasks](https://github.com/google-gemini/gemini-cli#popular-tasks) for more inspiration.

##### Troubleshooting

Head over to the [troubleshooting](https://github.com/google-gemini/gemini-cli/blob/main/docs/troubleshooting.md) guide if you're having issues.

#### Popular tasks

##### Explore a new codebase

Start by `cd`ing into an existing or newly-cloned repository and running `gemini`.

```
> Describe the main pieces of this system's architecture.

```

```
> What security mechanisms are in place?

```

##### Work with your existing code

```
> Implement a first draft for GitHub issue #123.

```

```
> Help me migrate this codebase to the latest version of Java. Start with a plan.

```

##### Automate your workflows

Use MCP servers to integrate your local system tools with your enterprise collaboration suite.

```
> Make me a slide deck showing the git history from the last 7 days, grouped by feature and team member.

```

```
> Make a full-screen web app for a wall display to show our most interacted-with GitHub issues.

```

##### Interact with your system

```
> Convert all the images in this directory to png, and rename them to use dates from the exif data.

```

```
> Organise my PDF invoices by month of expenditure.

```

##### Uninstall

Head over to the [Uninstall](https://github.com/google-gemini/gemini-cli/blob/main/docs/Uninstall.md) guide for uninstallation instructions.

#### Terms of Service and Privacy Notice

For details on the terms of service and privacy notice applicable to your use of Gemini CLI, see the [Terms of Service and Privacy Notice](https://github.com/google-gemini/gemini-cli/blob/main/docs/tos-privacy.md).
