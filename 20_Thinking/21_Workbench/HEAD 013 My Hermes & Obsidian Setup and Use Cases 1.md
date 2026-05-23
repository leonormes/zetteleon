---
title: "#013: My Hermes & Obsidian Setup and Use Cases"
source: "https://metedata.substack.com/p/013-my-hermes-and-obsidian-set-up?utm_medium=ios"
captured: "2026-05-23T13:55:25+01:00 2026-05-23T13:55:25+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
This article started on a dog walk.

As I was walking my dog, I was dropping messy voice notes with ideas into a Telegram chat with my agent named Satori. By the time I sat down to write, Hermes had turned that pile into an Obsidian thought note: raw transcripts in the scratchpad, a cleaned-up shape of the argument in the agent section, related context linked, and an agent draft for me to react to.

I didn’t outsource my thinking - I wrote the article myself. But this system compressed the distance between messy thought and shaped material. I spent more time outside with my dog and less time hunching over my laptop. I’m happy. My dog is happy. My agent is happy because he served his purpose.

![](https://substackcdn.com/image/fetch/$s_!_uMN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F039bb832-45ce-4c2c-ae20-fc311bfa8d76_480x269.gif)

I wanted to write a proper article on the current state of my set-up as I’ve gotten lots of questions from friends and people online about this system. And the most common question I get is - **what do I actually use it for?** So here I’ll focus on the use cases and my underlying thinking for building this system. Hence, this isn’t purely a setup guide for Hermes (the open-source agent framework) or Obsidian (the note-taking app) - but I’ll link to some good guides & describe my full setup at the end of this article if you want to take the plunge.

I’m also not here to convince you that this is some incredible system that you must absolutely get into. In fact, it’s pretty messy and I think most people don’t need this, in its current shape. But I think there’s something here - I already find lots of value and it’s a harbinger of things to come in consumer tech.

### So WTF is Hermes & Obsidian?

Do these terms sound like alien swear words to you? Then this is a good place to start.

**[Hermes](https://hermes-agent.nousresearch.com/)** is a lightweight open-source agent framework - basically a way to give Claude (or any model) its own computer, its own tools, and a memory of how you like things done. You may have heard about [OpenClaw](https://openclaw.ai/) - Hermes is basically the same but more streamlined and with a few bells & whistles like self-improvement and better memory. Either would work for the setup I’m describing.

**[Obsidian](https://obsidian.md/)** is a note-taking app where every note is just a plain text file sitting on your computer instead of in someone else’s cloud. The main folder where all your Obsidian notes live is called a vault. This local-first architecture has a key advantage I will discuss more towards the end.

Think of it like your own executive assistant who has access to a computer (in my case, a Mac Mini) who you can text (through [Telegram](https://telegram.org/) - a messaging app that works well for bots) with any request and they’ll figure out how to do it for you.

### Use Cases

Below is a sample of some of the use cases that actually stuck - stuff I reach for naturally and use every day, because the workflow is that much better than the alternatives. I added a small section at the end for more experimental use cases I’ve been exploring as well.

#### Collecting Business Ideas

I have a dozen new ideas every day - fun personal projects or bigger product bets. In the past, I’d go to [Craft](https://www.craft.do/) (another note-taking app), find my “Business Ideas” note, scroll all the way to the bottom and type out a brief one-sentence idea description. It worked, but it was a messy system. The note is close to 500 bullet points and 6,700 words. It’s a mess to wade through. Most ideas went there to die.

With Hermes, I now open Telegram and send it a rambling voice note describing my idea in as much detail as I can think of. What my agent then does:

1. Transcribes my idea
2. Creates a note in my Obsidian vault under *metedata-ventures/new-business-ideas*
3. Adds proper metadata & tags.
4. Adds my voice transcript verbatim as well as a trimmed & organized version.
5. Researches & enriches the idea using a simple framework we created together (competitive research, open questions, differentiation angles, proposed MVP scope, etc.)

![](https://substackcdn.com/image/fetch/$s_!jpq9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F854887ab-c09b-4b89-b545-2377d9246ccd_2684x2456.png)

Now, instead of a single bullet point in a messy note, I have a clean one-pager that encompasses the idea in full. Does it mean I’m going to go out and build all my ideas? No. But it enables me to:

1. Quickly decide if the juice is worth the squeeze.
2. Hand off a structured spec to Claude Code and start exploring further (Hermes can talk to Claude Code / Codex as well and can kick this off for you if you want).
3. Build up a rich library of well-formatted and researched ideas for later reference, research, follow-ups, making connections between them, etc.

#### My “Content Engine”

You got a hint of this in the beginning of the article. I had the initial structure and lots of raw material in place simply by doing a bunch of brain dumps through voice notes on a dog walk.

Here’s what Hermes does for me here:

1. Transcribes any random thoughts I may have throughout the week for new newsletter ideas or social posts.
2. Cleans them up, adds metadata & tagging, and files them into the right folder in Obsidian
3. Regularly reviews old ideas, archives them if they’ve been posted (and attaches the link), and makes sure they’re properly formatted.
4. Regularly syncs all my Threads posts into a local archive. This lets me easily search for things I’ve posted before. It also references this archive when checking if my ideas have been posted.
5. After my newsletter is posted, it compares the posted newsletter to my local copy and makes sure they’re the same. It also downloads & organizes any media from my posts for later reference.

![](https://substackcdn.com/image/fetch/$s_!H0gt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28ee93ce-3668-4811-803e-8c5fe6be971f_2848x2488.png)

All this then enables a bunch of novel Hermes use cases that I’m planning to experiment more with:

- Turn my long-form writing into short-form social media content
- Find novel connections between all my social & newsletter posts to push my thinking & writing further.
- Create a [Karpathy-style wiki](https://x.com/karpathy/status/2039805659525644595) layer on top of all my writing.
- Make the system more pro-active by getting it to research & recommend & draft ideas to me based on everything it knows about me and my writing.

You may have noticed that I didn’t even start with “In the past...” because I probably wouldn’t even do this if I didn’t have all this assistance (I’m not even mentioning basic things like proof-reading, formatting, help with visuals, etc.). This has truly cut off enough friction for me to focus on what I find most enjoyable - playing with ideas and honing in my writing.

#### Personal Fitness Coach

This may be one of my favorites so far, as it goes way beyond pure capture-and-organize workflow. It also probably deserves its own post. I will try to convey the essence here briefly for now.

With Hermes, you can set up different “profiles”, which are essentially different agents with their own memory, toolset, context, and runtime. So I set one up to be my personal fitness trainer.

Like most people in their 30s, I have an ever-growing collection of injuries, abandoned programs & apps, and other life stuff that comes between me and my fitness aspirations. As someone who worked in fitness tech for more than half a decade, I’ve tried a ton of different apps and services. Most of them are too rigid and quickly fall by the wayside when I get very busy, get re-injured, or travel for an extended period. In the past half a year, I’ve been building my own programs but that also started feeling stale - I felt stuck.

So I brain dumped my entire fitness history to my new fitness coach agent - everything I’ve tried, what worked, what didn’t, what I struggle with, where I want to get to by the end of the year, where I want to be in 10 years, my injuries, etc. We went back-and-forth and created a system that works for me. There’s a lot to it, but here’s a sample:

- Every Sunday, it creates workouts for the week ahead. They’re based on templates & blueprints we built together from all my preferences & history & canonical sources it pulled from the web. The workouts are saved as notes in Obsidian.
- After every workout, I send a short voice report on how the workout went, what worked, what didn’t, what felt off, etc. It logs it, records my feedback verbatim, and makes adjustments for the future based on my notes.
- If I’m doing my own cardio / something else like a Peloton class, I just send it a screenshot of my workout stats and it logs it for context.
- Every week, it reviews my progress to make sure I’m on track for my goals & the program in its current form is still the best it can be. It puts everything through a “fitness council” I created, which is a collection of sub-agents with distinct roles like “mobility expert”, “physical therapist”, “calisthenics coach”, etc. They review, debate, and refine stuff further.

![](https://substackcdn.com/image/fetch/$s_!reFC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1727fa62-73d3-4aca-a25b-a6d752d1db70_3786x2452.png)

What I love most about this system is flexibility. Here’s what it uniquely enables me to do:

- Some days just get away from you. I just send a message like “Hey, I only have 25 minutes today”. It will adjust my workout for me while keeping it aligned with my goals and preferences.
- If I’m away from home, I can just tell it I have no equipment (or send it a picture of whatever hotel gym I’m at), and it will adjust everything to what I have available.
- When I get injured, I tell it what’s wrong and it changes my program to avoid the injured area while including PT exercises for stability & strength to start building back up.

I could keep going because there’s so much more here. This has truly become central to my daily life.

#### Recipes

I always had trouble keeping track of favorite recipes cause I hate logging / formatting / editing them. Some I find online, some I get from ChatGPT, some I get from my mom as a WhatsApp message, some I get from my grandma as a photo of a hand-written note.

Now, I just send any of it to my Hermes agent and it files it for me into Obsidian. It came up with a formatting skill so they’re all uniform and well-organized.

When I want to cook, I either ask it to pull some info for me in the chat, ask questions, or just go to Obsidian.

![](https://substackcdn.com/image/fetch/$s_!pDiM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F987f1828-b1f1-4783-a5f4-a036b18dabed_3680x2456.png)

#### Bills and “Annoying” Shopping

Stripe recently released Link for agents, effectively letting your agents safely have a wallet without having any actual access to or control over financial info. It needs approvals and gets temporary credentials for any transaction. And it works incredibly well:

[

![X avatar for @metedata](https://substackcdn.com/image/fetch/$s_!3Ar3!,w_40,h_40,c_fill,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F2032108265656422403%2F5Swp5Msj.jpg)

Mete Polat@metedata

Ok this is sick. I just sent a photo of a bill I got in the mail to my Hermes agent and it just went out, paid it, and filed the receipt for me. I hate dealing with these payment portals and always leave these bills till the last minute. Now I can just snap a pic and send it to

![](https://substackcdn.com/image/fetch/$s_!l46b!,w_1560,h_1560,c_fill,f_webp,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fpbs.substack.com%2Fmedia%2FHHKXC7UWwAE-RUg.jpg)

![](https://substackcdn.com/image/fetch/$s_!wG7i!,w_1560,h_1560,c_fill,f_webp,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fpbs.substack.com%2Fmedia%2FHHKXC7XXwAEF85g.jpg)

![](https://substackcdn.com/image/fetch/$s_!poTL!,w_20,h_20,c_fill,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F1970187852572250113%2FhhDZmj7w.jpg)

Stripe @stripe

Today, we’re launching the @link wallet for agents. It lets you securely empower agents to spend on your behalf. Your payment credentials are never exposed and you approve every purchase. https://t.co/TcvEiVNth9

4:02 PM · Apr 30, 2026 · 91.4K Views

---

17 Replies · 24 Reposts · 293 Likes

](https://x.com/metedata/status/2049866865590120525?s=20)

The other day, I also sent it a photo of a broken part on my Dyson vacuum and it went out, found the part, and bought it for me (with my oversight).

I’m not yet ready to let it go and book travel or make any large transactions for me, but for use cases like these it’s honestly perfect.

#### The Bench: Other Experiments

The above use cases have become daily / weekly for me and are reliable and increasingly dialed in. But they all came out of messy experimentation. At any given time, I’m experimenting with a host of different things to see how far I can push the system. Here are just some recent examples:

1. I’ve been experimenting with getting it to analyze all of my writing and try to create a custom skill that codifies my voice. I haven’t invested a ton of time here, which is maybe why the early results are not super encouraging. Everything I try regresses towards slop and doesn’t quite feel like something I’d say.
2. Nobody likes scrolling LinkedIn. But you gotta play the game - thoughtful comments get engagement. I asked my agent if it can scroll through 100 posts on my feed, identify 10 that are most relevant to me, and then recommend comment angles (I write them myself). I’d say it got 80% there on the first try. We’ll see if this can become value-add.
	![](https://substackcdn.com/image/fetch/$s_!kA1q!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf82b14b-e7ca-4411-b0dd-f5199818fc80_2070x1792.png)
3. I asked my personal fitness trainer agent to build a pipeline that will take a video from me of me doing a movement and analyze my form. The results ended up surprisingly good - this may actually graduate to a regular use case:
	![](https://substackcdn.com/image/fetch/$s_!9Iwu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56332f57-82fe-4a71-b88f-e75435cfbd37_1746x1652.jpeg)
4. I’m planning to start experimenting more with generative UI and [HTML artifacts](https://x.com/trq212/status/2052809885763747935). Markdown is fine for now, but it’s definitely not the final form of agentic interfaces.

### Principles

The above use cases are cool and they work for me. But I’m sharing them not as a blueprint (although you’re super welcome to replicate them) but as an embodiment of the underlying principles I follow as I build and evolve this system. If you set out to tinker and build your own, these principles are what I’d steal first:

#### #1: Build the plane as you fly it

My biggest recommendation is to just start with a blank slate - empty Obsidian vault, simple Hermes installation, etc. Don’t try to transfer all the notes & bookmarks you ever took and connect them to every service you can imagine. You’ll quickly get overwhelmed and eventually give up.

I still have a ton of notes I didn’t transfer over and many “gaps” in my system. For example, I still have no inbox processing - I drop notes there and they don’t get properly categorized. But it’ll be one voice note to my agent and it’ll come up with a cron job to do it. If it doesn’t work, I’ll change it. You get the idea.

*The system does not need to be complete before it becomes useful.* Start with one use case you’re most excited about. Try it out for a few days. If it works, layer stuff on. If it doesn’t, pivot - it’s as easy as sending a message.

#### #2: Do not overcomplicate

Maybe this is a different re-iteration of the previous principle, but it bears repeating. Do not start by trying to design your “second brain” or adopting some prescriptive methodology for managing everything. These methodologies are alluring because they promise to make everything feel organized and leave you fully in control. In reality, that’s almost never the case. Accept the mess and strive for minimalism in the beginning. *The system should emerge from your own real usage*, not someone’s abstract architecture.

#### #3: Balance the friction between you, your knowledge base, and your agent

This may be less of a principle and more of a meta framework. But it neatly explains why I chose something like Obsidian over Notion:

![](https://substackcdn.com/image/fetch/$s_!JBeO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff39478d7-ad1b-4f3d-bf79-219b693d52ce_1447x1087.png)

This graph is obviously not perfect but it communicates the core idea. As you decrease the friction between AI and your knowledge base, you increase the friction for yourself (to manipulate it directly). Craft, Apple Notes, or Notion may feel better for the human because you get infinite customization, control, and ways to access your data directly. But now updating some dynamic sub-field in some database in your Notion habit tracker takes 150 tool calls for your LLM.

Obsidian is not as polished or comfortable as the other apps, but it operates on top of local files. And those files “live” closer to the AI on the same machine - it can directly write to and manipulate them without having to go through an MCP on a remote server.

A useful way to pick your tool - decide who is the primary actor. If you are primarily writing, logging, reviewing, and living in the app yourself, optimize for your own friction. If you want the agent to live on top of your knowledge base, optimize for agent friction, where local files and simple formats win.

#### #4: Always push it

As I mentioned above - I’m always experimenting and throwing crazy use cases at my agent. Half the time, it fails miserably and I learn about the limits of the current models, my own tooling, or process. The other half of the time, I’m surprised and even stunned, like when it paid my bill on the first try from a photo or gave me a perfect analysis of my handstand form from a video.

If you ever feel frustrated with the results - [it means you’re in the opportunity zone](https://metedata.substack.com/p/012-your-ai-frustration-is-my-opportunity). That’s where you can learn, experiment, tinker, innovate, and share your knowledge with others.

### Infrequently Asked Questions

#### Can this be done with another setup?

Yes, absolutely. The point is not that Hermes is the only possible way to do this. You can cobble this together with Claude Cowork, Claude Dispatch, and tons of MCP connectors. You can go a more consumer-friendly route and just connect your ChatGPT to all your services and use it as your “agent”. But the more “mainstream” you go with your tool, the lower your ceiling will be for autonomy, customization, portability, and use case complexity.

#### Is this right for me?

If your priority is ease of use and convenience, something like [Perplexity Computer](https://www.perplexity.ai/products/computer?wpsrc=Google&wpcid=23616213562&wpscid=193266954186&wpcrid=804060162645&wpkwid=kwd-2485325191141&wpkwn=perplexity%20computer&wpkmatch=e&wpsnetn=g&wpcn=_inactivity-0d&gad_campaignid=23616213562&gbraid=0AAAAA-YN3-smh33496wDgMVf81nChu0Bx) is probably a better fit right now. And if even this seems like too much, in 6-12 months we’ll have much more polished and consumer-friendly solutions from Apple, Google, OpenAI, and Anthropic.

That said, if you truly want to understand these tools and their full potential and are ready to tinker - you need to take the plunge. Things will break. Things will occasionally not work. You’ll need to touch the terminal. You’ll need to handle API keys. If your reaction is “Eh, I can figure that out”, then you’ll have fun. If this sounds like your worst nightmare, I’m surprised you’ve gotten this far in this article.

#### Is this system scalable & sustainable?

Like any “productivity system”, the real question is whether this setup will still be useful in a year. My answer here is a resounding “maybe”. It works for me so far and I’m having fun pushing these tools to the edge. In a year, there will likely be a dozen new agent systems that are better integrated into our devices and services. Some of the trade-offs I discussed may even be solved.

So is it likely that I’ll move all of this to some other agent platform eventually? Yes. But the system and the use cases will stay portable, especially since all your knowledge and agent context live in local files.

#### Is this all secure?

For the most part, [no](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). There’s a ton of inherent risk with these agent systems today. Some of it you can and should control for (I will give a few tips below) and some you cannot. It is still in the early adopter territory - if you don’t want to think about hardening your setup or don’t want to accept higher security & privacy risks, this is probably not for you.

### Resources & Tools & Tips

Ok, enough meta jabbering about use cases and principles. Below is the overview of my full setup, plus some practical resources, tips, and tools for your own Hermes setup, should you choose to dive in.

**Setup Resources**

- If you want a full step-by-step setup guide, I’d start with the [official Quickstart guide](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart).
- [This episode of Lenny’s Podcast](https://www.youtube.com/watch?v=DIa0MYJzM5I&t=5388s) with Claire Vo helped me with some mental models for how to think about these personal agents and what they’re capable of.

**Hardware**

- My Hermes runs on a Mac Mini (M4 | 16GB RAM) I got from [Apple’s official refurbished store](https://www.apple.com/shop/refurbished). Now that they’ve gotten super popular, they’re often out of stock, but they restock a few times a week. I recommend checking often and using something like [Refurb Tracker](https://refurb-tracker.com/). I was just checking for a few weeks and it appeared in stock.
- Since the Mac Mini only has 256GB of storage (what is this, a computer for ants?), I have a high-speed external SSD always plugged into the Mac Mini for any additional heavy files / media / etc. You don’t need it if you’re only doing pure Hermes with some code and text files, but I also use it for my media server.
- If you’re fancy like me, you can [mount your Mac Mini](https://www.amazon.com/dp/B0FN3D131R) on the wall - I have it mounted next to my router so it can connect over Ethernet.
- You may want to get an [HDMI dummy plug](https://www.amazon.com/dp/B06XT1Z9TF). It makes your Mac Mini think that there’s a display connected so you can more easily use remote screen sharing (see below).

**Software**

- Everything in [this guide](https://florian-darroman.medium.com/openclaw-mac-mini-setup-the-step-by-step-guide-389337569f1a) up to the OpenClaw section is good advice on how to set up an always-on Mac Mini, which I followed.
- Assuming you have another Mac, you can use [remote screen sharing](https://support.apple.com/guide/mac-help/share-the-screen-of-another-mac-mh14066/mac) to view the “screen” of your headless Mac Mini.
- I have [Tailscale](https://tailscale.com/docs/install/mac) set up on all my devices for security & easier access to my Mac Mini. You don’t strictly need this to run Hermes. But if you need to access the display of your Mac Mini when you’re away from home (to debug something), this lets you do this. It effectively ties all your devices into a private network over the internet. I also used to use [Mullvad VPN](https://mullvad.net/en) and it turns out Tailscale has it [integrated natively](https://tailscale.com/mullvad), so I consolidated into having it all in Tailscale.
- For accessing Mac Mini’s screen from my phone, I use [RustDesk](https://rustdesk.com/) - good enough and free if you suddenly need to click on some manual approval dialog (yes, this happens a lot).
- If terminals are foreign to you, I recommend starting with [Warp](https://www.warp.dev/) - it’s a bit friendlier and has more UI controls vs pure command line.
- If you use a local machine, you can also install Codex & Claude Code on it so you have an option to use them directly through their own mobile dispatch tools.
- I pay for Obsidian’s $5/mo sync plan so my files sync across devices. Since Obsidian is often my “front-end” for Hermes, I want to be able to access it anywhere.

**Model**

- I’m using my ChatGPT subscription ($100/mo plan) to power it. I have it set to GPT 5.5, x-high effort, fast mode. I never maxed it out with Hermes and I simultaneously use Codex and ChatGPT that draw from the same subscription. It’s good value and convenient. After something like Opus 4.7, this is your next best model to drive Hermes. And Anthropic no longer allows you to use their subscription to power 3rd party agents (with a [fresh caveat](https://x.com/ClaudeDevs/status/2054610152817619388)).
- I did a lot of research into potentially using a local model but you need beefier hardware for that. Models that can run on 16GB of RAM cannot presently run these agents in a way to make them broadly practical & functional.
- I looked into using open-source Chinese models through OpenRouter and actually run one of my profiles on GLM 5.1. They’re decent and, depending on your use, can be more economical if you really optimize your setup (like routing to different models based on the task type / use case). But frankly, if you want good results, plan to use it daily, and want to experiment with ambitious use cases, you’re unlikely to spend less than $100/mo. A subscription gives you peace of mind.

**Security**

- I highly recommend [reading this](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) to get a good mental model for how these models can be hacked and exploited. This will help you understand how you can improve your own operational security.
- I recommend using 1Password or some other password manager and giving your agent their own account. I got a family plan and my agent has their own vault so I can easily share / unshare credentials (wouldn’t recommend sharing your important personal accounts, but good for their own accounts, API credentials, etc.).
- Make sure you don’t leave open ports on your machine that are exposed to the internet. It means someone can find it and access it from the open web. Ask your agent to run a full security audit on your setup and give you recommendations. Ask follow-up questions to understand it all better.
- I recommend setting up separate internet accounts for your agents - their own AppleID, Gmail, etc. This drastically reduces the blast radius if these ever get compromised. Treat it like your executive assistant - first, start with minimum trust and build it over time; second, they probably shouldn’t have access to your personal accounts.
- Be explicit with your agent on which channels are trusted. I.e., it may be prudent to take a whitelist approach - tell it that it can only take instructions from you from a specific channel like WhatsApp, and not from any other channels (email / web / etc.).
- All this assumes you have good operational security in general - 2FA everywhere, password manager, etc.

**Favorite Hermes Tools & Skills**

- [Link agent wallet](https://link.com/agents) gives your agent a secure wallet it can use to buy stuff. Works great if you already have your stuff saved in Stripe.
- [browser-harness](https://github.com/browser-use/browser-harness) is a really good tool that enables better web use for your agent. They have their own native tools but this one seems to always work where others may fail.
- [Printing Press](https://printingpress.dev/) is a tool that lets you create a CLI for anything (hence, let your agent use it). They already have a great [library](https://github.com/mvanhorn/printing-press-library/tree/main) with CLIs for [flight search](https://github.com/mvanhorn/printing-press-library/blob/main/cli-skills/pp-flight-goat/SKILL.md), [AirBnB](https://github.com/mvanhorn/printing-press-library/blob/main/cli-skills/pp-airbnb/SKILL.md), and a ton more.
- Use [Fal.ai](https://fal.ai/login?returnTo=/dashboard) and connect your agent to it if you want them to be able to generate images / videos with any model.
- Use the [obsidian-skills](https://github.com/kepano/obsidian-skills) skill from the creator of Obsidian to teach your agent how to best use Obsidian.
- If you’re having your agent code for you or create visualizations, [this skill & MCP](https://github.com/better-auth/better-icons) lets them find icons instead of hallucinating them. Also great in Claude Code / Codex.
- [Humanizer skill](https://github.com/blader/humanizer) is decent at making it sound less sloppy & AI-y if you’re having it draft things for you.
- Unofficial [Google Flights MCP](https://github.com/punitarani/fli) lets your agent search flights.
- If you really want to nerd out, check out [Hermes Atlas newsletter](https://hermesatlas.beehiiv.com/authors/kevin-simback) from Kevin Simback - he sends out a summary of updates, new tools, and community happenings.

**Other Unsolicited Advice**

- If you don’t like how your agent is doing something - tell them. They can create skills & remember your preferences for next time.
- If you want to do something but don’t know how - ask the agent. They can figure it out themselves. Even for something like installing a skill - you can just send them a GitHub link and ask them to install the skill. They can for the most part run themselves.
- Lean on voice notes - it’s just way easier and works super well. You get quickly used to it to the point that you want to use it everywhere.

### Afterword

I hope this was helpful / inspiring / fun or even horrifying. As long as you were not bored. You may not believe me, but I really tried to keep this brief. If you’re more curious about a specific use case, workflow, setup question, or something else I haven’t covered - shoot me a DM. Happy to share more. If you’re lazy like me, you could even send this entire article to your Hermes and ask it to implement the tools & best practices from here.

---

*I want to ask you for a favor - if you’ve been enjoying the newsletter, please consider sharing it with your team / colleagues / friends. It really helps, especially in these early stages as I’m posting into the social media void and looking for like-minded people. To those who already shared - thank you, it means a lot. See you next week.*
