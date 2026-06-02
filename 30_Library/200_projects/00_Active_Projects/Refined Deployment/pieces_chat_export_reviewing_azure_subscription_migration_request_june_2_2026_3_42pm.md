*Shared Conversation from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Tuesday Jun 2, 2026 - 3:42 PM*
---

# Reviewing Azure Subscription Migration Request

## 👤 Leon Ormes

I am not sure what Alexis is asking me. 
 
Dear All,
 
I have some Azure maintenance to do. I have discovered a subscription which is ‘orphaned’. Although it works perfectly on our main tenant its billing ownership is attached to another tenant entirely. So, the subscription ownership needs to move to the main Trust Azure tenant.
 
Looking at the diagram below you will see that the orphaned subscription sits between your subscription and the Trust network.
 
The maintenance work planned will only change the billing ownership of the orphaned subscription, it will not touch any of the resources in it. So, no impact is anticipated. I have recently changed ownership on two other subscriptions and have a high degree of confidence you will experience no disruption.
 
Ideally I’d like to perform this subscription ownership change in the next week or so (Friday 5th June?). Please can you give some thought to the testing needed to support the activity. I will provide notification of the schedule and be in touch to ensure you are all confident that service is stable throughout.
 
If anyone has questions, please get in touch.
 
Alexis
 
 
 image008.png
 
 
 
 

                               Trust network                                                            Orphan subscription        Your subscription
Help me understand what I need to do or descide

---

## 🤖 Pieces

## What Alexis Is Asking

This is an Azure billing/tenancy maintenance notification. Here's a plain-English breakdown:

### The situation

An Azure **subscription** (a billing/resource container in Microsoft Azure) currently:
- **Works fine technically** — your services run through it as normal
- **Is billed to the wrong Microsoft tenant** — it's attached to a different organisation's billing account, not the main "Trust" tenant it should belong to

Alexis calls it **"orphaned"** because its billing parent doesn't match where it logically lives.

---

### Why it matters to you

Looking at the diagram layout:

```
Trust network  →  [Orphaned subscription]  →  Your subscription
```

The orphaned subscription is **in the network path between you and the Trust network**. Your subscription likely depends on it for connectivity or shared resources. That's why Alexis is notifying you — even though the change is billing-only, you're potentially affected if anything goes wrong.

---

### What Alexis is actually doing

- **Only changing billing ownership** — the subscription moves to the Trust tenant on paper
- **Not touching any resources** — no VMs, networks, configs, or services will be modified
- **Target date: Friday 5th June** (this Friday)

---

### What you need to do

Alexis is asking you to do **two things**:

1. **Plan your testing** — Think about what checks you would run *on the day* to confirm your services are still working after the change. For example:
   - Can you reach the Trust network from your subscription?
   - Are any shared resources in the orphaned subscription still accessible?
   - Do any applications or services that route through it still function?

2. **Be available on the day** — Alexis will notify you of the exact schedule and expects you to actively verify that your end is stable during and after the maintenance window.

---

### What you need to decide

| Question | Your call |
|---|---|
| Is Friday 5th June a good time? | Low-risk period? No other changes happening? |
| Who on your side will do the testing? | Nominate someone to be available |
| What specifically do you need to test? | List the services/connections that route through the orphaned subscription |
| Are you happy to proceed? | Reply to Alexis with confirmation or raise concerns |

**The main ask is low-effort** — Alexis isn't asking you to do any technical work, just to have a testing checklist ready and someone available to verify things look good afterwards. If Friday doesn't suit, now is the time to say so.

---

## 💬 Message

meta_complete (60664 input + 949 output + 411 reasoning tokens, $0.4299)

---

