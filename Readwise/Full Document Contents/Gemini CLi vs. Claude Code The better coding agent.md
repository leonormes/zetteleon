# Gemini CLi vs. Claude Code : The better coding agent

![rw-book-cover](https://framerusercontent.com/images/17fMEw6EPMVPxGH9ACq1oEM9fik.png)

## Metadata
- Author: [[composio.dev]]
- Full Title: Gemini CLi vs. Claude Code : The better coding agent
- Category: #articles
- Summary: Claude Code is faster, cheaper, and produces higher-quality code with a better user experience than Gemini CLI. Gemini CLI is less polished and requires more manual effort but can be useful for small projects. Overall, Claude Code is the better choice for professional and efficient coding tasks.
- URL: https://share.google/rfsMSMUNrVT54qSHc

## Full Document
The Gemini CLI is public, and Google, as usual, is the third entrant to the party. Claude code from Anthropic, Codex from OpenAI, and now, Gemini CLI, finally, the CLI coding agent trifecta is complete.

I have previously compared Claude Code and Codex, and Claude Code came on top, no surprise there. And, I have been a huge fan of them.

I was particularly interested in learning about the quality of the Gemini CLI and how it compares to the revered Claude Code.

So, I started with a decently complex task, building a Python-based CLI agent with tool integrations from [Composio](https://dub.composio.dev/aW9xei0), which would require

* Updated knowledge of the libraries (Composio)
* Internet Search
* The coding agent's capability to set up and work with the codebase.

Let's start by looking at the prompt (single-shot PRD).

#### **TL; DR**

If you've somewhere else to be, here's a summary.

* **Overview:** Compared Claude Code vs Gemini CLI using the same PRD to build an agentic CLI tool. The Claude Code is hands down better in all the departments. On the other hand, Gemini CLI needs many improvements.
* **Gemini CLI in headless mode:** To make the Gemini CLI work, I added instructions to CLAUDE.md to have Claude use the Gemini CLI in non-interactive mode (by passing the -p parameter with a prompt to receive a response from the CLI).
* **Speed:** Claude finished faster (1h17m) with full autonomy, while Gemini needed manual nudging and retries.
* **Cost:** Claude cost $4.80 with smooth execution; Gemini’s fragmented attempts pushed the cost to $7.06.
* **Token Usage:** Claude used fewer tokens efficiently with auto-compaction; Gemini consumed more without optimisation.
* **Code Quality & UX:** Claude delivered a cleaner structure and smoother UX; Gemini was decent but less polished overall.

The task here is to create a Python-based CLI agent that can connect to external tools (File tools, Search tool, and Notion) via a mix of local and managed Composio MCP servers

The prompt is the same for both Claude Code & Gemini CLI. Check it out [here](https://gist.github.com/22f2000147/b4d8b5839a614f8dddeaaf45d037840e). (basic prompt + some gemini 2.5 magic :)

The important part in a prompt is to give a clear set of instructions to the prompt, which is achieved by providing:

* Objective - Overall goal
* Core Technology - docs, resources & target audience
* Project Specifications - HLL overview of the project.
* Folder Structure (critical)
* Toolset Definition - what all tools are required, and an explanation
* Key Features - most important features
* Development Milestones - break the project into parts, build separately, and merge them while being coordinated
* Deliverables: What agents need to provide back to the user.

Here is a snapshot of the final product that has been [built](https://github.com/DevloperHS/agentic_cli_tool/tree/main).

![](https://i.ytimg.com/vi_webp/M9vmn-ukM2I/sddefault.webp)

Claude Code Built

![](https://i.ytimg.com/vi_webp/mdb8ZXw_358/sddefault.webp)

Gemini CLI Build

However, as this is a battle of wits, I would like to address a few factors so you can make a more informed choice.

#### Speed of Execution

In terms of speed, Claude Cde took the lead by completing the entire project in **1 hour 17 minutes,** compared to Gemini CLI, which took 2 hours **2** minutes. This is the total API time.

Apart from that:

* Claude Code did it in a single shot in auto mode, with no interference.
* For Gemini CLI, it took me multiple tries & multiple times I had to press `ESC` and then provide it with context to nudge it in the right direction.

![](https://framerusercontent.com/images/OS25EqakGKC0QL1DLOf5CjZU5c.png)
![](https://framerusercontent.com/images/mGnfmnilh3dQKU8YhvKKDtF8ePo.png)
Gemini CLI (with display error)

So, if you are prioritising speed, Claude Code can be your go-to.

Next, let’s look at the cost.

#### Cost of Execution

In terms of cost, Claude spent a total of $4.80, while Gemini CLI consumed $7.06 across its three tries.

In case you were wondering, the cost was approximately $2.56, with just a repository and broken code (milestones 4 and 5 remaining) for the Gemini CLI.

So, if we do math:

* Completing the remaining milestone (in addition to the two extra attempts and the context addition) will cost $4.50.
* That's the cost Claude took to complete the entire project.

However, using Claude Code involves a hefty fee; on the other hand, Gemini CLI is generally free.

> In case you want to utilize gemini-2.5-pro massive context window within Claude Code or vice versa, you can follow this [process](https://t.co/xUFMxIqDuY).
> 
> 

So, if you prioritise performance and quality at the cost, go with Calude Code. Otherwise, go with Gemini CLI + manual context additions.

Now let’s look at the token's usage!

#### Tokens Consumed

![](https://framerusercontent.com/images/Wx86tCfPqgZfx86kqkYn4iFS274.png)
Input & Output Tokens for Gemini CLI

![](https://framerusercontent.com/images/j4qPASd5fe40lLDXS0yxadG0odU.png)
Input & Output Tokens for Claude Code

In terms of tokens used:

* Claude Code took a total of 260.8K input and returned 69K tokens with 7.6M read cache ([CLAUDE.md](http://claude.md/)) - with auto compact
* Gemini CLI took a total of 432K input and returned 56.4K tokens with 8.5M read cache ([GEMINI.md](http://gemini.md/))

However, one thing I noticed while evaluating the tokens is that Gemini doesn’t use an **auto-compaction mode,** which may be the cause of this issue. Additionally, API keys can sometimes reach their maximum capacity due to this.

So, if you are concerned about efficient token usage, Claude Code is a great choice. However, if you're comfortable with small projects in teams, Gemini CLI might be a good choice.

Now let’s have a look at the generated Code Quality

#### Quality of Output

Claude Code generated directory

![](https://framerusercontent.com/images/x50FfPJSkYe6It45dllTHkBkqeI.png)
Gemini CLI generated directory

In terms of quality, both Claude Code and Gemini CLI were amazing.

* Claude Code generated a production-ready codebase, with organised folders, a readme, tests, git and workspace files.
* Gemini also generated a good codebase, but lacked the structural organisation of files for test cases. It added it to the root folder along with some extra files (probably to debug issues).

You can check out the [**repo**](https://github.com/DevloperHS/agentic_cli_tool/tree/main) to learn more!

So, if you are serious about repository organisation in production-grade settings, go for Claude Code. For small projects, prefer Gemini CLI.

Now let’s look at UX.

#### User Experience working with Claude Code and Gemini CLI

![](https://framerusercontent.com/images/PIgGSPMWvhn4nHc1EdDH5ZRKc.png)
Gemini CLI UI/UX

![](https://framerusercontent.com/images/JWiQpVO8sHyYvUSEGXa61iGzj3k.png)
Claude Code UI/UX

Personally, Claude Code can be my go-to due to this!

**Claude Code**

* Provides a premium experience while using, generating code and performing evaluations.
* I like its bash mode for quick checks and C`trl+R` to enlarge the generation data. Also, auto compact can be enabled to save tokens. Really enjoyed working with it.

> On contrary
> 
> 

**Gemini CLI**

* Tries to mimic Claude Code but lacks the premium experience Claude provides.
* I especially didn’t like its verbose generation (`ctrl+K` can be applied), no control to change settings (can keep the `/command` as setting in editor), no plan mode, and UI feels a little buggy after `/clear` command.

To conclude, if you require a premium experience, opt for Claude Code; otherwise, for simple tasks, Gemini CLI is a suitable alternative.

However, there is a caveat here!

#### Interesting Fact!

Initially, when I was working with **Gemini**, it was stuck with test cases. Even after multiple nudges, the model wasn’t able to fix it. But I wanted it to get done.

After a bit of research, I learnt that Gemini CLI have pipeline mode invoked using `gemini -p <prompt>` , which works as a headless agent, and someone on [Reddit](https://www.reddit.com/r/ChatGPTCoding/comments/1lm3fxq/gemini_cli_is_awesome_but_only_when_you_make/?share_id=kkNfDx5Xds1eigGiu3RdS&utm_content=1&utm_medium=ios_app&utm_name=ioscss&utm_source=share&utm_term=1) used it to use Gemini CLI within Claude Code. So, I updated my `CLAUDE.md` with the same.

The idea was simple → Wrap all the execution with the `gemini-p` command and tell Claude to do the same when performing task completions.

This way, I was able to utilise a massive 1m+ context window of Gemini 2.5 Pro with Claude Code and complete tasks in a single step, which had previously taken me seven failed attempts.

So, who won?

#### Final Thoughts

Ofc it’s **Claude Code.**

Let me be clear here, why?

* In all categories except Output Quality, Claude Code performed way better than Gemini CLI.
* The UX and code & generation flow was quite polished, smooth and premium
* In fact, 80% autonomous, I started the agent and then went on to study.
* Just a few permissions are required for the YOLO mode at the initial stage.
* Above all, it is less frustrating and optimised for token usage.

I have been a huge fan of Google Products, and considering how well they have turned the tables with Gemini, they are definitely going to improve this

We’re hosting first ever MCP webinar where we will discuss MCP security, Tool Authentication, Best practices for building and deploying MCP agents, and answer your questions. So, please join us on July 17, 2025. It'll be fun.
