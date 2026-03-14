---
created: 2026-03-14T09:49:42+00:00
modified: 2026-03-14T11:09:49+00:00
tags: [articles]
title: Want better AI outputs Try context engineering.
---

## Want Better AI Outputs? Try Context Engineering

![rw-book-cover](https://github.blog/wp-content/uploads/2026/01/insider.png?fit=1542%2C760)

### Metadata

- Author: [[Christina Warren]]
- Full Title: Want better AI outputs? Try context engineering.
- Category: articles
- Summary: Context engineering helps developers give AI tools like GitHub Copilot better information to improve code quality and consistency. It includes custom instructions, reusable prompts, and custom agents to guide AI in specific tasks. This approach saves time, reduces errors, and makes AI-assisted coding smoother and more reliable.
- URL: <https://github.blog/ai-and-ml/generative-ai/want-better-ai-outputs-try-context-engineering/>

### Full Document

![Decorative header image with the words 'The GitHub Insider'.](https://github.blog/wp-content/uploads/2026/01/insider.png?w=1542)Decorative header image with the words 'The GitHub Insider'.

If you've ever felt like [GitHub Copilot](https://github.com/features/copilot) could be even stronger with just a little more context, you're right. Context engineering is quickly becoming one of the most important ways developers shape, guide, and improve AI-assisted development.

#### What is Context Engineering?

Context engineering is the evolution of prompt engineering. It's focused less on clever phrasing and more, as [Braintrust CEO Ankur Goyal](https://x.com/ankrgyl/status/1913766591910842619) puts it, on _"bringing the right information (in the right format) to the LLM."_

At [GitHub Universe](https://githubuniverse.com/) this past fall, [Harald Kirschner](https://x.com/digitarald?lang=en)—principal product manager at Microsoft and longtime VS Code and GitHub Copilot expert—outlined three practical ways developers can apply context engineering today:

Each technique gives Copilot more of the information it needs to produce code matching your expectations, your architecture, and your team's standards.

Let's explore all three, so you can see how providing better context helps Copilot work the way you do.

#### 1. Custom Instructions: Give Copilot the Rules it Should Follow

[Custom instruction files](https://docs.github.com/en/copilot/tutorials/customization-library/custom-instructions/your-first-custom-instructions) help Copilot understand your:

You can use:

For example, you might define how React components should be structured, how errors should be handled in a Node service, or how you want API documentation formatted. Copilot then applies those rules automatically as Copilot works.

#### 2. Reusable Prompts: Standardize Your Common Workflows

Reusable prompt files let you turn frequent tasks—like code reviews, scaffolding components, generating tests, or initializing projects—into prompts that you can call instantly and consistently.

Use:

- Prompt files: `.github/prompts/*.prompts.md`
- Slash commands such as `/create-react-form` to trigger structured tasks

This helps teams enforce consistency, speed up onboarding, and execute repeatable workflows the same way every time.

#### 3. Custom Agents: Create Task-specific AI Personas

Custom agents allow you to build specialized AI assistants with well-defined responsibilities and scopes. For example:

Agents can include their own tools, instructions, constraints, and behavior models. And yes, you can even enable handoff between agents for more complex workflows.

#### Why Context Engineering Matters

The goal isn't just better outputs, it's better understanding by Copilot. When you provide Copilot with clearer context:

- You get more accurate and reliable code.
- You reduce back-and-forth prompting.
- You increase consistency across files and repositories.
- You stay in flow longer instead of rewriting or correcting results.

And the more you experiment with context engineering, the more you'll discover how deeply it can shape your development experience.

![Decorative background featuring floating green cubes, including one with the GitHub invertocat logo.](https://github.blog/wp-content/uploads/2026/01/4ba0cd42388a255e04c78e5143548f22e577d68e0f15f68e6a3c76c18b927981-1920x1080-1.png?w=1600)Decorative background featuring floating green cubes, including one with the GitHub invertocat logo.

![A clean header with the GitHub logo features the bold text “Top blog posts of 2025.” Below it, a grid of glowing green and translucent cubes forms a geometric landscape. GitHub’s colorful Mona mascot sits on one cube near an icon resembling a refresh or sync symbol. The design uses soft gradients and bright highlights to create a modern, tech‑themed look.](https://github.blog/wp-content/uploads/2025/12/top-blog-posts.png?w=1600)A clean header with the GitHub logo features the bold text "Top blog posts of 2025." Below it, a grid of glowing green and translucent cubes forms a geometric landscape. GitHub's colorful Mona mascot sits on one cube near an icon resembling a refresh or sync symbol. The design uses soft gradients and bright highlights to create a modern, tech‑themed look.
