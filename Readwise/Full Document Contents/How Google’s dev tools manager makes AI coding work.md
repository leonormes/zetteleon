# How Google’s dev tools manager makes AI coding work

![rw-book-cover](https://techcrunch.com/wp-content/uploads/2025/09/IMG_5424.jpg?resize=1200,900)

## Metadata
- Author: [[Russell Brandom]]
- Full Title: How Google’s dev tools manager makes AI coding work
- Category: #articles
- Summary: Ryan Salva, Google's dev tools manager, uses AI tools like Gemini CLI to help write code and create detailed project specs. Developers are starting to rely more on AI to handle coding tasks, while they focus on planning and problem solving. In the future, coding will be less about writing raw code and more about designing and managing complex software projects.
- URL: https://techcrunch.com/2025/09/23/how-googles-dev-tools-manager-makes-ai-coding-work/

## Full Document
![Ryan Salvo google AI](https://techcrunch.com/wp-content/uploads/2025/09/IMG_5424.jpg)Image Credits:Russell Brandom
As Google’s project manager for developer tools, Ryan Salva has a front-row seat to the ways AI tools are changing coding. Formerly of Github and Microsoft, he’s now responsible for tools like Gemini CLI and [Gemini Code Assist](https://codeassist.google/), nudging developers into the new world of agentic programming.

His team released [new third-party research](https://blog.google/technology/developers/dora-report-2025/) on Tuesday showing how developers actually use AI tools – and how much progress is left to make. I sat down with Salva to talk about the report and his personal experience with AI coding tools.

*This interview was edited for length and clarity.*

**Every year, Google does a survey of developer trends – but this year’s report really focuses on AI tools, and specifically how agentic developers are willing to get in their approach to programming. Was there anything in the research that surprised you?**

One of the really interesting findings was the median date when developers started using AI tools. They found it was April 2024, which corresponds fairly neatly to Claude 3 coming out and Gemini 2.5 coming out. This is really the dawn of the reasoning or thinking models, and around that same time, we got much better at tool-calling.

For coding tasks, you really need to be able to leverage external information in order to problem solve, so it may need to grep, it may need to compile the code. If the code compiles it may want to run that unit test, and that integration test. I think that tool-calling really is the important piece that gave models the ability to self-correct as they move along.

**How are you using AI coding tools personally?**

Techcrunch event

##### Join 10k+ tech and VC leaders for growth and connections at Disrupt 2025

###### Netflix, Box, a16z, ElevenLabs, Wayve, Sequoia Capital, Elad Gil — just some of the 250+ heavy hitters leading 200+ sessions designed to deliver the insights that fuel startup growth and sharpen your edge. Don’t miss the 20th anniversary of TechCrunch, and a chance to learn from the top voices in tech. **Grab your ticket before Sept 26 to save up to $668.**

##### Join 10k+ tech and VC leaders for growth and connections at Disrupt 2025

###### Netflix, Box, a16z, ElevenLabs, Wayve, Sequoia Capital, Elad Gil — just some of the 250+ heavy hitters leading 200+ sessions designed to deliver the insights that fuel startup growth and sharpen your edge. Don’t miss the 20th anniversary of TechCrunch, and a chance to learn from the top voices in tech. **Grab your ticket before Sept 26 to save up to $668.**

San Francisco | October 27-29, 2025

[**REGISTER NOW**](https://techcrunch.com/events/tc-disrupt-2025/?utm_source=tc&utm_medium=ad&utm_campaign=disrupt2025&utm_content=ticketsales&promo=tc_inline_rb&display=)

Most of my coding these days is for hobby projects, and I spend most of my time using command line-based tools. So that includes Gemini CLI. Then there’s a little bit of Claude Code, little bit of Codex in there. And you don’t ever really use a terminal-based tool by itself, so I’m really heterogeneous around the IDEs that I use. I use Zed. I use VS code. I use Cursor. I use Windsurf, all of them, because I’m interested in just seeing how the world works and how the industry is evolving.

On the professional side, product managers tend to live in documents, so the first thing is using AI to help me write the specification and requirements docs.

**I’m curious how that works. You’re using Gemini CLI to build Gemini CLI, but I would imagine it doesn’t just run itself.**

A development task will usually start as an issue, maybe it’s a GitHub issue that someone’s dropped with a bug. Often, if I’m really being honest, it’s a fairly under-specified issue. So I’ll use Gemini CLI in order to create a more robust requirement doc in Markdown. That will usually create probably about 100 lines of fairly technical, but also outcome-driven specification. Then I will use Gemini CLI to write the code based on that specification and the general preferences in the team documents.

Across the engineering team, we have a couple of different layers of rules and Markdown docs that get consumed by the model, just laying out our way of working: Here’s how we do testing, here’s how we manage dependencies, and so on. So when it produces the code, it’s also working from those documents.

And as Gemini CLI is going through and doing the troubleshooting, I’ll have it update my requirements doc saying, “I fixed this step. Now I’m on to the next step,” and so on. Each one of those creates its own commit and pull request in the repository, so I can always rewind or undo.

I would say probably 70% to 80% of my work is me working in the terminal with natural language, trying to use Gemini CLI to craft the requirements, and then allowing Gemini CLI to write most of the code for me, which I will then go review and read with whatever IDE I happen to be using. But mostly I’m using the IDE as a place to read the code, rather than to write the code.

**Do you think there’s a future for raw computer code? Or will we just move everything into terminal windows?**

For three decades, the IDE was where we went to do everything in software development. You had the IDE, you had the browser, and you had the terminal window.

I think that’s still largely the case, but I suspect that over time we’ll end up spending a lot more time working with the requirements, and the amount of time spent in the IDE will gradually shrink. And I think that change may actually happen over a pretty long time horizon.

**There’s a lot of angst about what that means for software development as a progression. If 10 years from now, we’re no longer looking at code, what does that mean for developers? Will there still be a job for them?**

I think that your job as a developer is going to look a lot more like an architect. It is going to be about taking big, complex problems and breaking them down into smaller, solvable tasks. You’ll need to be thinking about like the bigger picture about what you’re trying to produce, rather than the intermediate language in order to express that in machine code.
