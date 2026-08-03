---
title: 5 Claude, OpenClaw, and Hermes skills that deserve to be in your toolkit
source: https://www.makeuseof.com/claude-openclaw-hermes-skills-deserve-in-toolkit/
captured: 2026-07-27T17:03:48+01:00 2026-07-27T17:03:48+01:00
status: processing
tags:
- input
type: head
permalink: llmeon/20-thinking/21-workbench/head-5-claude-open-claw-and-hermes-skills-that-deserve-to-be-in-your-toolkit
---

## Raw Output / Content
If you're constantly jumping between AI tools and agents, you'll quickly realize that good prompting only gets you so far, and at some point, you're just repeating the same instructions. Fortunately, skills for AI tools exist to solve exactly that problem.

There are [skills that can do anything from making Claude turn any document into a mind map](https://www.makeuseof.com/tiny-claude-skill-that-turns-any-document-into-mind-map-visualize-anything/) to running, make OpenClaw turn data into actionable reports, or just summarize that massive documentation folder on your drive. And the best part: you can use the same one across all AI tools you want.

## Catch problems before they hit production

### Use AI-powered code reviews to spot bugs, improve readability, and provide actionable pull request feedback

![GitHub-pr skills command prompt and report.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2026/07/github-pr-skills-command-prompt-and-report.jpg?q=49&fit=crop&w=825&dpr=2)

GitHub-pr skills command prompt and report.

Instead of asking your AI whether a PR looks fine and getting inconsistent answers, you can get the [pr-reviewer-skill](https://github.com/SpillwaveSolutions/pr-reviewer-skill/blob/main/SKILL.md) to get a full, repeatable PR review pipeline. It fetches PR diffs and comments via the GitHub CLI, scores changes against security, testing, and maintainability criteria, and then drafts inline comments based on that analysis.

The flagship feature is the two-stage approval step. The skill generates review files first, lets you edit or approve them, and only then posts to GitHub — exactly the kind of guardrail you want when you're letting an agent write on your behalf.

## Turn the web into structured knowledge

### Research topics and automatically organize the results into clean, RAG-ready documents for future retrieval

![RAG chunk generation using Firecrawl skill.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2026/07/rag-chunk-generation-using-firecrawl-skill.jpg?q=49&fit=crop&w=825&dpr=2)

RAG chunk generation using Firecrawl skill.

When you want to turn a URL or topic into something your agents can actually retrieve from later, the **firecrawl-knowledge-base** skill nails the pattern. Give it a few URLs, a topic, and depth settings, and it uses Firecrawl to crawl the sites and produce LLM-ready markdown chunks in addition to a manifest.json file that describes the collection. It can also output reference documentation, RAG chunk sets, fine-tuning datasets, or even documentation mirrors depending on your goals.

Installation is also straightforward and requires only one command:

```
npx skills add https://github.com/firecrawl/firecrawl-workflows --skill firecrawl-knowledge-base
```

For Claude Code, that drops a ready-to-use skill into your.claude/skills folder, and you can start using it right away. Hermes can load the same skill folder, using the generated markdown and manifest.json as a persistent knowledge base for future conversations. OpenClaw can run it from an ops agent on a schedule, writing outputs into a shared directory or database that other skills query when they need context.

## Stop rewriting the same documents

### Generate documentation, API references, meeting notes, and technical guides with reusable AI skills

Anthropic's **document-skills** set is the boring-but-essential backbone for any agent that needs to interact with real-world documents. These are the same skills Claude.ai uses behind the scenes to open, edit, and generate DOCX, PDF, PPTX, and XLSX files, and they're shipped as open, spec-compliant skills in the anthropic/skills repository.

The skill is divided into subskills that handle a specific kind of document. They all come with a **SKILL.md** file and supporting references that define how to parse, manipulate, and write those formats. In Claude Code, installation is a single command:

```
/plugin install document-skills@anthropic-agent-skills
```

Once installed, you can call them directly from your sessions to generate documents in a specific format, annotate PDFs, and do any other document-related work. For Hermes and OpenClaw, you don't even need a port. Just copy the relevant subfolder from github.com/anthropics/skills straight into their respective skills directories, and you're good to go. Since they follow the same agent skill specification, the logic just works, and all you have to do is adjust whatever file system or storage each runtime uses.

## Make Git workflows impossible to forget

### Encode commit messages, release notes, changelogs, and repository conventions into repeatable AI-powered rituals

![Git workflow demo screnshot.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2026/07/git-workflow-demo-screnshot.jpg?q=49&fit=crop&w=825&dpr=2)

Git workflow demo screnshot.

For Git automation, **git-workflow-skill** is a great option. This agent skill covers branching strategies, conventional commits, PR workflows, CI/CD integrations, releases, and advanced operations, all organized in a layered content architecture so the agent only loads what it needs. The standout feature is the **/pr-finish** command, which rebases, fixes CI issues, resolves review threads, and merges the PR with proper cleanup.

Similar to **firecrawl-knowledge-base**, the skill plugs directly into your AI agent's skills directory, giving you slash-style commands for branch creation, PRs, and release management. OpenClaw can embed it in an ops agent so commands follow the same procedures you'd enforce manually.

## Build the skills that build more skills

### Create reusable prompts and workflows that help your AI assistants generate even better capabilities over time

![Claude Code terminal and desktop running on Windows 11 laptop.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2026/06/claude-code-terminal-and-desktop-running-on-windows-11-laptop-1.JPG?q=49&fit=crop&w=500&dpr=2)

Claude Code terminal and desktop running on Windows 11 laptop.

Anthropic has an official meta-skill for building and refining other skills. Instead of writing every skill markdown file by hand, **skill-creator** asks you about the workflow, scaffolds the folder, drafts frontmatter, and even runs trigger-phrase evaluations to make sure the skill is discoverable and behaves the way you'd expect. It can be incredibly helpful for [everyday tasks you can hand off to OpenClaw](https://www.makeuseof.com/everyday-tasks-i-handed-to-openclaw-and-instantly-stopped-doing-myself/).

It's essentially a guided assistant for designing, packaging, and iterating on your own skills. The idea here is that instead of hunting for specific skills that match your particular workflow, you teach the skill-creator your work style and conventions, and it becomes the gateway skill that bootstraps everything else in your toolkit.

### Small skills compound into powerful workflows

Skills are where your agent setup stops being a collection of useful prompts and starts looking like an actual work toolkit, whatever that might look like for you. Most, if not all, of these skills can be run across Claude, OpenClaw, and Hermes with only minor wiring differences. So all you really need to do is dial the skill in one agent, and then it's available for use across all others.

Install them once, adapt them to your work, repositories, and infrastructure, and then let them handle the port parts. From there, the only question is which one of your existing habits you want to encode next.