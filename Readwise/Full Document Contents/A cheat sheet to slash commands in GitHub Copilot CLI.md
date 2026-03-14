---
created: 2026-03-14T09:50:16+00:00
modified: 2026-03-14T11:09:06+00:00
tags: [articles]
title: A cheat sheet to slash commands in GitHub Copilot CLI
---

## A Cheat Sheet to Slash Commands in GitHub Copilot CLI

![rw-book-cover](https://github.blog/wp-content/uploads/2026/01/generic-github-copilot-logo.png)

### Metadata

- Author: [[Jacklyn Carroll]]
- Full Title: A cheat sheet to slash commands in GitHub Copilot CLI
- Category: articles
- Summary: GitHub Copilot CLI slash commands let developers quickly run tasks and manage code without leaving the terminal. These commands provide clear, repeatable actions that improve speed, security, and productivity. Starting with commands like /clear, /cwd, and /help helps users control workflow and context easily.
- URL: <https://github.blog/ai-and-ml/github-copilot/a-cheat-sheet-to-slash-commands-in-github-copilot-cli/>

### Full Document

![Copilot appears among floating cubes alongside a refresh icon, suggesting an update or automated workflow theme.](https://github.blog/wp-content/uploads/2026/01/generic-github-copilot-logo.png?w=1600)Copilot appears among floating cubes alongside a refresh icon, suggesting an update or automated workflow theme.

Do you ever feel like you're spending more time moving between different tools than you are writing code? If you thrive in the terminal and want faster, more predictable ways to run tests, fix code, and manage context, [Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli#model-usage) slash commands give you that control without breaking your flow. You can use slash commands to perform a variety of tasks like configuring [which AI model to use](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli#model-usage) or setting up an MCP server, or even sharing your session externally. Slash commands offer fast, repeatable actions without needing to craft a new prompt each time.

TL;DR: See all the slash commands and what they do at the bottom of this post.

#### What Are Slash Commands?

A slash command is a simple instruction, like `/clear` or `/session`, that tells Copilot exactly what you want to do. They are prefixed with a `/` and instantly trigger Copilot to carry out context-aware actions. To start using slash commands, open Copilot CLI and type `/` to see a list of available commands.

In addition to Copilot CLI, you can use slash commands across [Copilot Chat and with agent mode](https://github.blog/developer-skills/github/how-to-use-github-copilot-in-your-ide-tips-tricks-and-best-practices/#13-slash-commands-for-common-tasks), too.

#### Why Use Slash Commands?

As developers, we want tools that work fast in the terminal. Slash commands in Copilot CLI do just that. Instead of writing a new prompt for each task, you use quick, explicit, and repeatable commands directly in your workflow.

In practice, they help with:

- Speed and predictability: With slash commands, Copilot's actions are more transparent and predictable. Unlike natural language prompts, which can be interpreted in different ways, slash commands always trigger the same response. This removes guesswork because you always know what you're going to get, instantly.
- Productivity: Before slash commands, you might have copied and pasted code, written long prompts, or switched back and forth between tools. Now you can clean up errors, run tests, and get code explanations right from the CLI, without leaving your terminal.
- Clarity and security: Commands like `/add-dir` and `/list-dirs` give clear boundaries for file access and create an auditable trail, which is essential for teams working in sensitive environments. This eliminates uncertainty about what's happening behind the scenes, reduces the risk of accidental data exposure, and helps teams maintain control in sensitive environments.
- Better accessibility: Slash commands fit seamlessly into keyboard-driven and accessible workflows. Commands like `/help` provide an instant overview of available actions, while `/list-dirs` or `/list-files` let users browse without navigating complex interfaces. These commands enable users who rely on keyboard shortcuts or assistive technologies to quickly discover and use Copilot features.
- Trust and compliance: Slash commands enhance trust by making every Copilot action explicit and traceable. For example, teams can use `/add-dir` to grant Copilot access to a specific directory. This ensures that sensitive files stay protected. With slash commands like `/session` or `/usage`, teams can manage tool access, monitor activity, and stay compliant.
- Custom workflows and extensibility: As support for slash commands expands, you can tailor Copilot to work with your own tasks and automations. Delegate pull requests, switch agents, or connect to CI/CD pipelines, all from the CLI, with commands like `/delegate`, `/agent`, and `/mcp`.

Think of slash commands as explicit shortcuts for things you already do. There's a lot you can do with Copilot CLI, and slash commands make the process easier.

#### Useful Copilot CLI Slash Commands for Your Everyday Workflow

Below are the most commonly used slash commands, grouped by what you typically need to control in your workflows: context, scope, configuration, and collaboration.

Tip: If you only remember three commands, start with `/clear`, `/cwd`, and `/model`. These give you immediate control over context, scope, and output quality.

#### Session Management Commands

##### `/clear`: Delete the Current Session's Conversation History

Copilot accumulates context as you work. This inherited context can muddy suggestions when you have too much of it, or when you're trying to switch tasks. `/clear` lets you quickly wipe the slate when you're multitasking or working between projects.

When to use:

- Switching to a new task or repository
- Copilot responses are referencing old files or earlier conversations
- You want to avoid context bleed between projects

##### `/exit`, `/quit`: Exit the CLI

The commands `/exit` and `/quit` provide a direct way to end your session and disconnect from Copilot, ensuring resource cleanup and a clear boundary for session-based work.

When to use:

##### `/session`, `/usage`: Display Session Usage Metrics about the Current CLI Session

These commands give visibility into the actions Copilot has performed during your session, helping with audits, troubleshooting, and resource tracking.

When to use:

When you run either the `/session` or `/usage` commands, Copilot shows output similar to the following, displaying usage metrics about your session:

```
Session ID: 221b5571-3998-47e1-b57a-552cf9078947      
Started: 11/24/2025, 11:18:54 AM  
Last Modified: 11/24/2025, 11:18:54 AM      
Duration: 50s
Working Directory: /Users/jacklynlee31
      
Usage:        
Total usage est:       0 Premium requests   
Total duration (API):  0s         
Total duration (wall): 50s        
Total code changes:    0 lines added, 0 lines removed 
    
Hit Enter or Esc to continue
```

#### Directory and File Access Commands

##### `/add-dir`: Allow Copilot to Access a Directory

By limiting Copilot's access to the files you choose, you can ensure responses are relevant to your current scope and increase security.

When to use:

For example, here I am adding the Documents directory to the allowed list for file access:

```
/add-dir /Users/jacklynlee31/Documents
```

Copilot then gives me the following output:

```
Added directory to allowed list: /Users/jacklynlee31/Documents
```

##### `/list-dirs`: Show Allowed Directories

This command helps keep file access transparent. This can help with team compliance policies.

When to use:

After running the command, Copilot will show you the list of directories. For example:

```
Allowed directories for file access:

   1. /Users/jacklynlee31
   2. /Users/jacklynlee31/Documents

   Total: 2 directories
```

##### `/cwd`: Show or Change the Working Directory

This keeps Copilot focused on the part of your codebase you're actively working in.

When to use:

For example, after using the command, Copilot gave me the following output:

```
Current working directory: /Users/jacklynlee31/Downloads
```

When using `/cwd [directory]`, you are able to switch to a different directory:

```
/cwd /Users/jacklynlee31/Downloads
```

Copilot will give you a similar output to show the new working directory path:

```
Changed working directory to: /Users/jacklynlee31/Downloads
```

##### `/model`: Select an AI Model

Copilot supports multiple models, but you don't need to overthink it. Start with the default model, then experiment when you notice differences in speed, reasoning depth, or cost.

When to use:

After running the command, Copilot will display an interactive model selection menu similar to the following:

```
Choose the AI model to use for Copilot CLI. The selected model will be persisted and used for future sessions.

 ❯ 1. Claude Sonnet 4.5 (1x) (default) (current)
   2. Claude Opus 4.5 (Preview) (1x)
   3. Claude Haiku 4.5 (0.33x)
   4. Claude Sonnet 4 (1x)
   5. GPT-5.1 (1x)
   6. GPT-5.1-Codex-Mini (0.33x)
   7. GPT-5.1-Codex (1x)
   8. GPT-5 (1x)
   9. GPT-5-Mini (0x)
   10. GPT-4.1 (0x)
   11. Gemini 3 Pro (Preview) (1x)
   12. Cancel (Esc)
```

You can select a model from the list with the number or arrow keys and press Enter. You can also use `/model [model]` to directly change the AI model.

##### `/theme [show|set|list]  [auto|dark|light]`: Configure the Terminal Theme

- `Show`: shows the current theme preference.
- `Set`: used to set the terminal theme to `auto`, `dark`, or `light`.
- `List`: shows a list of available themes.

When to use:

After setting the theme, Copilot will confirm your preference and prompt you to restart the CLI to apply the new theme:

```
● Theme preference set to: dark

   The new theme will be applied on the next restart of the CLI.
```

##### `/terminal-setup`: Enable Multiline Inputs

This is especially helpful for complex instructions or multi step code changes. This command ensures your terminal is ready for advanced tasks and collaborative workflows.

When to use:

##### `/reset-allowed-tools`: Reset Tool Permissions

This command helps you quickly roll back the allowed tools set to a clean slate, removing obsolete or risky items.

When to use:

After using the command, Copilot will show a confirmation:

```
The list of allowed tools has been reset.
```

#### External Services Commands

##### `/agent`: Select a Custom Agent

Custom agents let you target specialized tasks or integrations.

When to use:

- Switching agent configurations by repository/org/project
- Testing specialized or third-party agents

##### `/delegate <prompt>`: Create an AI-generated Pull Request

This lets you automate changes and create pull requests without leaving the terminal.

When to use:

For example, here I generated a pull request in my repository to add dark mode support:

Documentation is critical—and this command lets you capture entire session histories to share or archive.

When to use:

After sharing the file, Copilot will confirm that the session was shared successfully to your chosen location:

```
● Session shared successfully to: /Users/jacklynlee31/Desktop/copilot-session-221b5571-3998-47e1-b57a-552cf9078947.md
```

##### `/login`, `/logout`: Log in or out of Copilot

When to use:

##### `/mcp [show|add|edit|delete|disable|enable]`: Manage MCP Configurations

Managing [MCP server](https://github.com/mcp) configuration directly from the terminal means you don't have to switch between tools or interfaces.

- `Show`: show the list of available MCP servers.
- `Add`: add a new MCP server.
- `Edit`: edit an existing MCP server.
- `Delete`: delete a MCP server.
- `Disable`: disable a MCP server.
- `Enable`: enable a MCP server.

##### `/user [show|list|switch]`: Manage what GitHub account You're Using

Multi-user and enterprise development often means switching between accounts. `/user` can help you with your role-based workflows and testing.

When to use:

##### `/help`: Show All Available Commands

When to use:

#### Bringing it All together

With slash commands in Copilot CLI, you can make common workflow tasks fast and repeatable. You're gaining explicit control over context, scope, and automation without leaving the terminal.

The best way to experience this is to dive in and try slash commands yourself. Start with `/clear`, `/cwd`, and `/help`. Then layer in others as your workflows grow.

As slash command capabilities grow, your feedback helps us shape what comes next. Use `/feedback` to share what's working, and what isn't.

#### Quick Reference

| Slash command | What it does | When to use |
| --- | --- | --- |
| `/clear` | Clears session history/context | Shift tasks, reset Copilot's context, resolve confusion |
| `/exit`, `/quit` | Exits the Copilot session | Finish a session, reset the CLI |
| `/session`, `/usage` | Shows current session and usage stats | Audit activity, monitor Copilot CLI usage |
| `/add-dir <directory>` | Adds allowed directory for file access | Limit scope, improve security/auditing |
| `/list-dirs` | Lists directories Copilot can access | Confirm or manage file access permissions |
| `/cwd [directory]` | Changes/outputs the working directory | Navigate projects, limit Copilot context |
| `/model [model]` | Changes Copilot AI model for the CLI | Experiment, troubleshoot, optimize model behavior |
| `/theme [show|set|list]` | Manage terminal output theme | Customize for environment or team standards |
| `/reset-allowed-tools` | Resets allowed external tools | Remove tool permissions, reset for audits |
| `/agent` | Selects a custom Copilot agent | When using specialized agents by repo/org |
| `/delegate <prompt>` | Delegates changes as a PR in a remote repository | Automate changes, multi-repo workflows |
| `/share [file|gist]` | Shares session as markdown or GitHub Gist | Document sessions, async handoff, team sharing |
| `/login`, `/logout` | Sign in/out of Copilot in the CLI | Change user, rotate credentials |
| `/mcp [show|add|edit|…]` | MCP server configuration management | Update CI/CD proxy config, enterprise setups |
| `/user [show|list|switch]` | GitHub user management | Multi-user or team CLI management |
| `/help` | Lists all CLI commands and shortcuts | Onboarding, discoverability |
| `/feedback` | Submit feedback about Copilot CLI | Share suggestions or bug reports with GitHub |

##### Additional Resources

![Decorative illustration featuring Ducky inside a translucent cube surrounded by green geometric blocks.](https://github.blog/wp-content/uploads/2026/01/00ab37fbbb9bc343b007734b0e5805a26e747c90d955750bd976cb9ce84f6a2a-1920x1080-1.png?w=1600)[Application development](https://github.blog/developer-skills/application-development/)
