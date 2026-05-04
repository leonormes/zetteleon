---
captured: "2026-05-04T11:13:16+01:00 2026-05-04T11:13:16+01:00"
created: 2026-05-04T10:13:17+00:00
modified: 2026-05-04T10:13:51+00:00
source: "https://gemini.google.com/app/64d9fd5e1e5e8122"
status: "processing"
tags: ["input"]
title: HEAD You said httpsyoutu.be7pPlhSgYMrE?si=9NO5WvORR...
type: "head"
---

That was not the video I shared. <https://youtu.be/7pPlhSgYMrE?si=xkjWJkzgL25PYEHH>

---

Gemini

that was a different video entirely. This video, "Why Your AI Forgets" by Squintist, explains the technical hurdles behind why Large Language Models (LLMs) struggle to maintain long-term memory during a conversation.

Here is a summary of the core concepts discussed:

## 1\. The Illusion of Memory

The video clarifies that LLMs do not actually "remember" anything between turns \[00:01:00\]. Every time you send a message, the entire conversation history is sent back to the model from scratch. It reads the whole history, generates a reply, and then effectively "forgets" until the next prompt.

## 2\. The Context Window and Its Limits

While context windows have grown from 4,000 tokens to millions \[00:01:24\], two major issues persist:

- Cost and Compute: The computational power required grows with the square of the context length, making it increasingly expensive \[00:01:50\].
- Context Rot: Models become less reliable as the window fills up. They get "less sharp" and start missing obvious details, a phenomenon researchers call "context rot" \[00:02:12\].

## 3\. Management Techniques

To handle these limits, developers use several strategies:

- Truncation: Silently dropping the oldest messages \[00:02:50\].
- Compaction (Summarisation): The system asks the model to summarise the conversation so far and replaces the detailed history with that summary \[00:03:12\]. However, this often results in the loss of "load-bearing" details that the model incorrectly deems unimportant \[00:03:51\].

## 4\. The Engineering Trade-off: Prefix Caching

A significant reason why memory management is so "blunt" is Prefix Caching \[00:05:09\].

- GPUs skip recomputing the parts of a conversation that haven't changed to keep responses fast.
- If a system tries to be "clever" by continuously rewriting or reorganising the context to keep only what matters, it breaks this cache, making the AI significantly slower and more expensive to run \[00:05:34\].

## 5\. The Future of Context

The video concludes that context management is one of the most active and unsolved areas in AI infrastructure \[00:06:42\]. Current experiments include "triaging" context (dropping bulky tool outputs while keeping user instructions) and moving memory into external stores that the AI can query on demand \[00:06:58\].

Ultimately, the video suggests that for an AI to be truly useful, it doesn't just need a bigger memory—it needs a better way to forget the noise while keeping the signal \[00:07:06\].
