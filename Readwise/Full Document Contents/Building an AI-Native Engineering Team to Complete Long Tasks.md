# Building an AI-Native Engineering Team to Complete Long Tasks

![rw-book-cover](https://miro.medium.com/v2/resize:fit:1200/1*EHB79ltAiPOWdCPUgEwcHQ.png)

## Metadata
- Author: [[Fareed Khan]]
- Full Title: Building an AI-Native Engineering Team to Complete Long Tasks
- Category: #articles
- Summary: AI models can now work on long tasks like software development but need a system approach to be reliable. Google’s AlphaEvolve architecture helps manage these multi-hour or multi-day tasks effectively. The key is using step-by-step algorithms, not just better prompts, to guide AI agents.
- URL: https://share.google/ZDCYJvJueIggTZlbf

## Full Document
As of August 2025, [METR found](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) that leading AI models could complete 2 hours and 17 minutes of continuous work, with roughly a 50% chance of producing a correct answer. With improvements in maintaining much longer reasoning chains, these models can now implement a full software development lifecycle using RAG and AI agents. Achieving reliable performance, however, requires **treating long-horizon task as a systems problem** rather than relying on the capabilities of a single model.

![](https://miro.medium.com/v2/resize:fit:3100/format:webp/1*EHB79ltAiPOWdCPUgEwcHQ.png)LongHorizon Architecture (Created by [Fareed Khan](https://medium.com/u/b856005e5ecd?source=post_page---user_mention--e48b8b39cc9e---------------------------------------))
Google last year released [**AlphaEvolve**](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) for this exact class of **long-horizon tasks** problems that require **multi-hour or multi-day execution**. The architecture I created above is **inspired by** [**Google AlphaEvolve architecture**](https://arxiv.org/abs/2506.13131), and this is the same system I am going to implement throughout this blog.

> At its core, agents that **think long and execute step by step** require an **algorithmic-based approach**, not just better prompts.
> 
> 

This includes:

1. **MAP-Elites**: to explore and preserve diverse high-quality solutions instead of converging to a single…
