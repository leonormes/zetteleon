---
created: 2026-03-14T09:50:11+00:00
modified: 2026-03-14T11:09:32+00:00
tags: [articles]
title: The creator of Claude Code just revealed his workflow, and developers are losing their minds
---

## The Creator of Claude Code just Revealed His Workflow, and Developers Are Losing Their Minds

![rw-book-cover](https://images.ctfassets.net/jdtwqhzvc2n1/6VsJWNsStTR57q9vFd5L08/a0d88b4dcbd1e9ba77fd72a9c55988d9/nuneybits_Vector_art_of_programmer_conducting_robot_orchestra_i_908157a9-d44f-4bce-b390-5913b88dad27.webp?w=800&q=75)

### Metadata

- Author: [[Michael Nuñez]]
- Full Title: The creator of Claude Code just revealed his workflow, and developers are losing their minds
- Category: articles
- Summary: Boris Cherny, creator of Claude Code, shares a simple but powerful workflow using multiple AI agents to boost coding speed like a small team. He uses a slow, smart model and a shared file to teach the AI from past mistakes, making it smarter over time. This new way turns AI from a helper into a workforce, changing how software is built forever.
- URL: <https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are>

### Full Document

![nuneybits Vector art of programmer conducting robot orchestra i 908157a9-d44f-4bce-b390-5913b88dad27](https://venturebeat.com/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fjdtwqhzvc2n1%2F6VsJWNsStTR57q9vFd5L08%2Fa0d88b4dcbd1e9ba77fd72a9c55988d9%2Fnuneybits_Vector_art_of_programmer_conducting_robot_orchestra_i_908157a9-d44f-4bce-b390-5913b88dad27.webp%3Fw%3D1000%26q%3D100&w=3840&q=85)nuneybits Vector art of programmer conducting robot orchestra i 908157a9-d44f-4bce-b390-5913b88dad27

When the creator of the world's most advanced coding agent speaks, Silicon Valley doesn't just listen—it takes notes.

For the past week, the engineering community has been dissecting a [thread on X](https://x.com/bcherny/status/2007179832300581177) from [Boris Cherny](https://x.com/bcherny), the creator and head of [Claude Code](https://code.claude.com/docs/en/overview) at [Anthropic](https://www.anthropic.com/). What began as a casual sharing of his personal terminal setup has spiraled into a viral manifesto on the future of software development, with industry insiders calling it a watershed moment for the startup.

"If you're not reading the Claude Code best practices straight from its creator, you're behind as a programmer," wrote [Jeff Tang](https://x.com/jefftangx), a prominent voice in the developer community. [Kyle McNease](https://x.com/KyleMcnease/status/2007555584724480338), another industry observer, went further, declaring that with Cherny's "game-changing updates," Anthropic is "on fire," potentially facing "their ChatGPT moment."

The excitement stems from a paradox: Cherny's workflow is surprisingly simple, yet it allows a single human to operate with the output capacity of a small engineering department. As one user noted on X after implementing Cherny's setup, the experience "[feels more like Starcraft](https://x.com/mtwichan)" than traditional coding—a shift from typing syntax to commanding autonomous units.

Here is an analysis of the workflow that is reshaping how software gets built, straight from the architect himself.

#### How Running Five AI Agents at once Turns Coding into a Real-time Strategy Game

The most striking revelation from Cherny's disclosure is that he does not code in a linear fashion. In the traditional "[inner loop](https://notes.paulswail.com/public/The+inner+and+outer+loops+of+software+development+workflow)" of development, a programmer writes a function, tests it, and moves to the next. Cherny, however, acts as a fleet commander.

"I run 5 Claudes in parallel in my terminal," Cherny wrote. "I number my tabs 1-5, and use system notifications to know when a Claude needs input."

![Screenshot 2026-01-05 at 1.53.45 PM](https://venturebeat.com/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fjdtwqhzvc2n1%2F2HdIfpu7mN6174uQ37MaSs%2Fc39fd89633bda9c1d842316ec4525abb%2FScreenshot_2026-01-05_at_1.53.45%C3%A2__PM.png%3Fw%3D1000%26q%3D100&w=3840&q=75)(credit: x.com/bcherny)

By utilizing iTerm2 system notifications, Cherny effectively manages five simultaneous work streams. While one agent runs a test suite, another refactors a legacy module, and a third drafts documentation. He also runs "5-10 Claudes on [claude.ai](https://claude.ai/)" in his browser, using a "teleport" command to hand off sessions between the web and his local machine.

This validates the "[do more with less](https://www.cnbc.com/2026/01/03/anthropic-daniela-amodei-do-more-with-less-bet.html)" strategy articulated by Anthropic President Daniela Amodei earlier this week. While competitors like OpenAI pursue trillion-dollar infrastructure build-outs, Anthropic is proving that superior orchestration of existing models can yield exponential productivity gains.

#### The Counterintuitive case for Choosing the Slowest, Smartest Model

In a surprising move for an industry obsessed with latency, Cherny revealed that he exclusively uses Anthropic's heaviest, slowest model: [Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5).

"I use Opus 4.5 with thinking for everything," Cherny [explained](https://x.com/bcherny/status/2007179838864666847). "It's the best coding model I've ever used, and even though it's bigger & slower than Sonnet, since you have to steer it less and it's better at tool use, it is almost always faster than using a smaller model in the end."

For enterprise technology leaders, this is a critical insight. The bottleneck in modern AI development isn't the generation speed of the token; it is the human time spent correcting the AI's mistakes. Cherny's workflow suggests that paying the "compute tax" for a smarter model upfront eliminates the "correction tax" later.

#### One Shared File Turns Every AI Mistake into a Permanent Lesson

Cherny also detailed how his team solves the problem of AI amnesia. Standard large language models do not "remember" a company's specific coding style or architectural decisions from one session to the next.

To address this, Cherny's team maintains a single file named [CLAUDE.md](https://x.com/bcherny/status/2007179842928947333) in their git repository. "Anytime we see Claude do something incorrectly we add it to the CLAUDE.md, so Claude knows not to do it next time," he wrote.

This practice transforms the codebase into a self-correcting organism. When a human developer reviews a pull request and spots an error, they don't just fix the code; they tag the AI to update its own instructions. "[Every mistake becomes a rule](https://x.com/aakashgupta/status/2007347705945944153)," noted [Aakash Gupta](https://x.com/aakashgupta), a product leader analyzing the thread. The longer the team works together, the smarter the agent becomes.

#### Slash Commands and Subagents Automate the Most Tedious Parts of Development

The "vanilla" workflow one observer praised is powered by rigorous automation of repetitive tasks. Cherny uses slash commands—custom shortcuts checked into the project's repository—to handle complex operations with a single keystroke.

He highlighted a command called _/commit-push-pr_, which he invokes dozens of times daily. Instead of manually typing git commands, writing a commit message, and opening a pull request, the agent handles the bureaucracy of version control autonomously.

Cherny also deploys subagents—specialized AI personas—to handle specific phases of the development lifecycle. He uses a code-simplifier to clean up architecture after the main work is done and a verify-app agent to run end-to-end tests before anything ships.

#### Why Verification Loops Are the Real Unlock for AI-generated Code

If there is a single reason Claude Code has reportedly hit [$1 billion in annual recurring revenue](https://www.anthropic.com/news/anthropic-acquires-bun-as-claude-code-reaches-usd1b-milestone) so quickly, it is likely the verification loop. The AI is not just a text generator; it is a tester.

"Claude tests every single change I land to claude.ai/code using the Claude Chrome extension," Cherny wrote. "It opens a browser, tests the UI, and iterates until the code works and the UX feels good."

He argues that giving the AI a way to verify its own work—whether through browser automation, running bash commands, or executing test suites—improves the quality of the final result by "2-3x." The agent doesn't just write code; it proves the code works.

#### What Cherny's Workflow Signals about the Future of Software Engineering

The reaction to Cherny's thread suggests a pivotal shift in how developers think about their craft. For years, "AI coding" meant an autocomplete function in a text editor—a faster way to type. Cherny has demonstrated that it can now function as an operating system for labor itself.

"Read this if you're already an engineer… and want more power," [Jeff Tang](https://x.com/jefftangx/status/2008246873275215890) summarized on X.

The tools to multiply human output by a factor of five are already here. They require only a willingness to stop thinking of AI as an assistant and start treating it as a workforce. The programmers who make that mental leap first won't just be more productive. They'll be playing an entirely different game—and everyone else will still be typing.
