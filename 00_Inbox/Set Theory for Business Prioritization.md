---
aliases: []
author: ["[[Gemini]]"]
confidence: 
created: 2025-12-14T00:00:00Z
description: "Created with Gemini"
epistemic: 
last_reviewed: 
modified: 2025-12-14T18:38:43Z
published:
purpose: 
review_interval: 
see_also: []
source: "https://gemini.google.com/share/5fa682de2c60"
source_of_truth: []
status: 
tags: []
title: Set Theory for Business Prioritization
type: 
uid: 
updated: 
---

Create a maths description in sets of this. We are a software company. When prioritizing work there are multiple sets involved. At the top there is the set of all possible actions we could take. This is of course a massive set. There is also a subset of that of tasks that are relevant to running a company. Then a subset for our particular company. Of those tasks/actions there are 2 sets. 1 of known tasks and one of unknown tasks. Then there are some effective tasks for the job of making the company successful. The properties of actions include value. Some tasks are short term value and others long term. If you understand what I am getting at, can you elaborate and create a mathematical description of this. Include clear notes describing each set and what it means

Of course. Here is a mathematical description of your company's work prioritisation process using the language of set theory.

This model formalises the relationships between different categories of tasks, helping to clarify the strategic challenges involved.

---

## \## Foundational Sets

Let's begin by defining the universe of discourse and the primary subsets you described.

1. **The Universal Set of Actions ()** This is the set of all theoretically possible actions that could ever be taken by anyone or anything.
	This set is vast and abstract, containing everything from "write a line of code" to "fly to Jupiter".
2. **The Set of Business-Relevant Actions ()** This is a subset of containing only those actions that are relevant to the general operation of *any* company.
	So, . For example, "hire a developer" , but "bake a cake" (unless you're a bakery).
3. **Your Company's Action Set ()** This is a further subset, containing only actions relevant to *your specific* software company.
	This gives us the relationship: . An action like "update our legacy billing system" would be in , whereas "manufacture car parts" would not. **This set is the main context for all further prioritisation.**

---

## \## Task Categorisation within Your Company

Now, we can describe the sets that categorise the tasks specifically within your company's world, .

1. **Known and Unknown Tasks ( and )** The set of all tasks for your company, , can be divided into two distinct groups:
	- : The set of **known** tasks. These are on your backlogs, in your roadmaps, or are generally recognised as things that could be done.
	- : The set of **unknown** tasks. These are the things you don't yet know you need to do—the "unknown unknowns".
	These two sets form a **partition** of . This means every task in is either known or unknown, but not both. Mathematically:
	where denotes union (everything in both sets) and denotes intersection (items in common, which is the empty set ).
2. **Effective Tasks ()** This is the crucial subset of tasks within that are **effective** for making your company successful.
	Crucially, **is independent of whether a task is known or not**. There are effective tasks you know about () and effective tasks you haven't discovered yet ().
3. **Value-Horizon Tasks ( and )** We can also partition the company's task set based on the time horizon of the value they generate:
	- : The set of tasks that provide **short-term value**.
	- : The set of tasks that provide **long-term value**.
	Assuming a task is primarily one or the other, these also form a partition of :

---

## \## The Goal of Prioritisation: A Mathematical View 🎯

Using these sets, we can define the challenge of prioritisation and strategy much more clearly. Your goal is not just to do tasks, but to do the *right* tasks.

- **The Obvious Target:** The set of tasks you should be prioritising from your backlog is the **intersection of known and effective tasks**:
	These are the tasks you know about that will genuinely drive success.
- **The Strategic Challenge:** A key business function is **discovery**. This is the process of moving valuable tasks from the unknown set to the known set. In other words, the goal of research, brainstorming, and customer feedback is to identify tasks in:
	Once an action is identified, it moves to the set and can be prioritised.
- **The Prioritisation Decision:** When deciding what to work on *next*, you are selecting an action from . The choice often depends on strategic focus:
	- To drive immediate results (e.g., hit quarterly targets), you choose from: .
	- To build a sustainable future (e.g., invest in platform health), you choose from: .

This framework shows that running the business is a two-part problem: **execution** (choosing wisely from ) and **strategy** (exploring effectively to populate from ).

Describe the function of discovery and of determining value

Of course. Within the mathematical framework we've established, discovery and determining value are the two core intellectual functions that drive effective prioritisation.

---

## \## The Function of Discovery 🧭

In simple terms, **discovery** is the business process of finding out what needs to be done.

Its primary function is to move valuable tasks from the set of **unknowns** () into the set of **knowns** (). The ultimate goal is not just to find *any* task, but to identify tasks that are both unknown and effective. Mathematically, the aim of discovery is to identify the elements of the set:

This is the wellspring of **innovation** and future growth. While your current backlog consists of tasks in , your future success depends on your ability to continuously find and define tasks from .

Activities involved in the discovery process include:

- **User Research:** Interviewing customers to uncover unmet needs.
- **Market Analysis:** Studying competitors and market trends to find opportunities.
- **Data Mining:** Analysing user behaviour data to find unexpected patterns or pain points.
- **Prototyping & Experimentation:** Building and testing novel ideas to see if they are effective.

A company that neglects discovery and only focuses on its existing known tasks () may be efficient in the short term, but it risks becoming irrelevant as the market evolves.

---

## \## The Function of Determining Value ⚖️

While discovery is about finding the *right things* to do, **determining value** is the process of figuring out their relative importance.

Its function is to analyse the tasks within your known set (), particularly those deemed effective (), and assign a magnitude to their potential impact. This process gives substance to the value function, , for each action .

Value is rarely a single number; it's often a composite of several factors:

- **Commercial Impact:** Direct revenue, cost savings, market share growth.
- **User Impact:** Increased user satisfaction, retention, or engagement.
- **Strategic Impact:** Alignment with long-term goals, opening new markets, or reducing technical debt.
- **Risk Reduction:** Mitigating security vulnerabilities or business risks.

Frameworks like **RICE** (Reach, Impact, Confidence, Effort) or **WSJF** (Weighted Shortest Job First) are practical methods for estimating this value. The output of this function is a ranked or scored list of tasks. This allows you to move beyond gut feeling and provides a rational basis for deciding which item from the set should be tackled next.

In short, **discovery fills the pool of potential work**, and **determining value tells you where to fish**.

Can we factor in the biases of humans and of organisational charts onto this formula

Yes, absolutely. We can factor in these crucial elements by evolving the model from a purely rational description to one that includes predictable irrationality. Biases act as **perception filters** that distort the discovery and valuation processes.

The pure model describes how things *should* work in a perfectly rational organisation. The biased model describes how they often *do* work in reality.

---

## \## Modelling Bias in Discovery 🧠

Human and organisational biases mean that the discovery process is not a pure, objective search for all effective tasks. Instead, biases create a "searchlight" that only illuminates certain parts of the unknown territory (), often those that are comfortable or familiar.

We can model this by introducing a **Perceived Effective Set ()**. This is the set of tasks that the organisation *believes* to be effective, based on its collective biases.

- The rational goal is to find tasks in (unknown but truly effective tasks).
- The biased reality is that the discovery process is geared towards finding tasks in (unknown tasks that *seem* effective to the organisation).

**The key issue is that .**

- **Confirmation Bias:** Teams look for problems they already believe exist, reinforcing .
- **"Not Invented Here" Syndrome:** An idea from another department might be truly effective (in ) but is ignored and thus excluded from the perceived set .
- **The Silo Effect:** The Engineering department's perceived set might barely overlap with the Sales department's , and neither fully represents the true company-wide effective set .

This misalignment means the organisation can waste resources "discovering" tasks that aren't truly effective, while genuinely game-changing ideas remain in the dark.

---

## \## Modelling Bias in Determining Value 📊

Bias fundamentally distorts the valuation of known tasks. A task's "value" is no longer an objective calculation but a subjective perception.

We can model this by replacing the true value function, , with a **Perceived Value Function,** . This function is skewed by a bias factor, which we can call .

The bias factor is not a constant; it changes depending on the task, the people involved, and the organisational context.

- **Human Factors contributing to** :
	- **HiPPO (Highest Paid Person's Opinion):** If a senior leader champions task , it receives a large, positive , artificially inflating its perceived value: .
	- **Recency Bias:** A bug reported this morning gets a temporary positive over a more critical, older issue.
- **Organisational Factors contributing to** :
	- **Short-termism:** The organisation's structure may apply a systemic bias. For any task (long-term value), is negative. For any task (short-term value), is positive.
	- **Resource Politics:** A project from a department with more political influence will have its perceived value amplified with a positive .

---

## \## The Practical Outcome: Misaligned Priorities

This leads to the final, critical conclusion. A purely rational company prioritises work from the set of known, effective tasks:

However, a real-world organisation, influenced by biases, makes its decisions based on the set of known and *perceived* effective tasks:

The core challenge of good leadership, robust processes, and healthy culture is to **minimise the discrepancy between and** . The goal is to make your perceived reality align as closely as possible with objective reality, ensuring you work on tasks that are *actually* valuable, not just the ones that feel valuable.

Write a comprehensive LLM prompt to give a deep research agent full context of this idea.

Of course. Here is a comprehensive prompt designed to give a deep research agent the full context of this idea, empowering it to validate, expand, and apply the model.

---

## LLM Research Agent Prompt

**ROLE:** You are a world-class research agent with deep expertise in behavioural economics, organisational psychology, systems thinking, and modern software business management. Your goal is to critically analyse and build upon a provided conceptual model.

**OBJECTIVE:** To research, validate, expand, and provide practical applications for the following set-theoretic model of business prioritisation. Your output will be a comprehensive report for a leadership team aiming to improve its strategic decision-making.

---

## \[CONTEXT: The Conceptual Model\]

**1\. The Core Idea:**We are modelling the task prioritisation process in a technology company. The model uses set theory to distinguish between a purely rational, ideal process and the biased reality of day-to-day operations. The central theme is the gap between what is *truly* effective and what is *perceived* as effective.

**2\. The Foundational Sets (The Rational Ideal):**

- : The set of all possible actions relevant to our company. This is our universe of discourse.
- : The subset of **Known** tasks (e.g., on backlogs).
- : The subset of **Unknown** tasks.
	- These two sets form a partition: and .
- : The subset of **Effective** tasks. These are the actions that, with objective certainty, contribute to the company's success. This is the "ground truth" set.
- **&** : Subsets for **Short-term** and **Long-term** value, which also partition .

**3\. The Core Functions (The Rational Ideal):**

- **Discovery:** The strategic function of identifying valuable tasks currently in the unknown set () and moving them into the known set (). This is the engine of innovation.
- **Determining Value:** The analytical function of assigning a true value, , to each known task. This allows for the ranking of tasks within the **Rational Priority Set:** .

**4\. The Bias Layer (The Organisational Reality):**This layer models how human and structural biases distort the rational ideal.

- **Perceived Effective Set ()**: This is the set of tasks the organisation *believes* is effective. Due to biases (confirmation bias, silo effect, etc.), .
- **Perceived Value Function ()**: This is the subjective value an organisation assigns to a task. It is modelled as , where is a dynamic bias factor influenced by:
	- **Human Factors:** The HiPPO effect, recency bias, availability heuristic.
	- **Organisational Factors:** Short-termism, departmental politics, "not invented here" syndrome.

**5\. The Consequence:**The organisation does not prioritise from the rational set. Instead, it prioritises work from its **Actual Priority Set:** . The primary goal of good leadership and process design is to minimise the difference between and .

---

## \[YOUR TASKS\]

Based on the model provided above, please conduct the following research and analysis:

**1\. Validate and Connect:**Find established theories and models from academic and industry literature that support or challenge this framework.

- Connect the model to the work of key thinkers like **Daniel Kahneman & Amos Tversky** (cognitive biases), **John Boyd** (OODA Loop, related to discovery), **Chris Argyris** (organisational learning), and **Dave Snowden** (Cynefin framework).
- Does this set-theoretic description align with established principles of organisational behaviour and decision science?

**2\. Expand and Refine:**Identify critical factors the current model overlooks and propose how to integrate them. Specifically, address:

- **Cost & Effort:** How can the cost/effort to complete a task be formally included in the prioritisation formula (e.g., as a function )?
- **Risk & Uncertainty:** How can we model the uncertainty of a task's value, especially for tasks in the discovery phase?
- **Inter-dependencies:** Tasks are not always independent. How could the model represent dependencies where the value of task 'a' is conditional on the completion of task 'b'?

**3\. Identify Practical Frameworks:**Connect the abstract concepts in the model to concrete business frameworks and tools used today.

- Which popular prioritisation methods (e.g., **RICE, WSJF, MoSCoW**) are essentially tools for estimating the perceived value function ? What are their inherent biases?
- How do strategic frameworks like **OKRs** or **Jobs-to-be-Done (JTBD)** serve as mechanisms to better align the perceived set with the true set ?

**4\. Propose Mitigation Strategies:**Research and provide a list of actionable strategies to help an organisation minimise the gap between and . Categorise them into:

- **Process-Based Interventions:** (e.g., pre-mortems, red teaming, blinded decision panels, structured debate).
- **Data-Driven Interventions:** (e.g., A/B testing as a tool for value discovery, metrics that counter vanity metrics).
- **Cultural Interventions:** (e.g., practices that foster psychological safety, intellectual humility, and a culture of experimentation).

---

## \[OUTPUT FORMAT\]

Deliver your findings as a structured Markdown report. Use clear headings for each of the four tasks. The language should be authoritative and insightful, suitable for a business leadership audience. Cite key sources where appropriate.

There is also a few more sets of work we haven't considered. The sets of incomplete and complete work. Where incomplete work has an estimated value completed work has an actual value.

Excellent point. Incorporating the state of work provides a critical dynamic element to the model, allowing us to describe the full lifecycle of a task and introduce a feedback loop for learning.

Here is how we can integrate the sets of incomplete and complete work.

---

## \## Introducing the Work Lifecycle Sets

The set of **Known** tasks () is not static. Once a task is chosen, it flows through a lifecycle. We can define two new sets to represent this:

- **(Work-in-Progress):** The set of **incomplete** tasks. These are tasks that have been selected from and are currently being worked on.
- **(Done):** The set of **completed** tasks. These are tasks that were in and are now finished.

These sets are mutually exclusive. A task can only be in one state at a time: waiting to be started (), being worked on (), or finished (). This gives us a clear flow:

---

## \## From Estimated Value to Actual Value

This distinction between work states allows us to formally differentiate between projected and realised value, which aligns perfectly with the concepts of perceived and true value we discussed.

- **For Incomplete Work ():** The value of a task that is in progress is still an **estimate**. It is based on a hypothesis of the impact it *will* have. This corresponds to the **Perceived Value,** . This is the number you use in your planning documents and roadmaps.
- **For Completed Work ():** Once a task is finished and released, you can measure its actual impact on the business and its users. This measurement reveals its **Actual Value,** .

Think of it like a financial forecast versus an earnings report. is the forecast you make when you invest in the work; is the actual return on that investment.

---

## \## The Crucial Feedback Loop 💡

This lifecycle creates the most important mechanism for improving an organisation's decision-making: **a feedback loop**.

By systematically comparing the estimated value with the actual value for all completed tasks, you can learn and adapt. For every task that enters the **Done** set , you should analyse the **Estimation Error**:

Analysing this error is the key to strategic improvement:

1. **Calibrating Your Value Model:** If you consistently find that your estimated value is much higher than the actual value (), it's a sign that your valuation process is flawed. You can identify the specific biases () at play—perhaps you're too optimistic, or you're consistently overvaluing tasks championed by certain people.
2. **Refining Your Discovery Process:** By seeing which *types* of tasks deliver high actual value (), you get better at spotting high-potential ideas in the future. This feedback trains your intuition and data models.
3. **Aligning Perception with Reality:** The ultimate purpose of this feedback loop is to make your **Perceived Effective Set ()** a more accurate reflection of the **True Effective Set ()**. The smaller your average estimation error, the more consistently you are choosing to work on things that are genuinely valuable.

In these formula are other parameters. We have constraints as well. Team capacity. Team cohesion, top down align of goals and vision, trust. Also there are factors outside of the company that are of concern but we have no control. In fact we have things we can control things we can influence and things we care about but can do nothing about.

Yes, we can definitely incorporate these critical real-world parameters. This moves our model from a simple task-selection framework to a more holistic system that accounts for operational capacity and the external environment.

We can model these as constraints on your actions and as external forces that modify the value of those actions.

---

## \## Integrating Internal Constraints

Your internal limitations don't change whether a task is *effective*, but they do constrain your ability to *execute* it.

1. **Team Capacity () & Task Effort ()** Every task has a cost. We can define an **Effort Function,** , which assigns an effort score (e.g., in story points or person-weeks) to each task .
	**Team Capacity,** , is the total effort your team can expend in a given period. This turns prioritisation into a classic optimisation problem, similar to the knapsack problem. Your goal is no longer just to pick the highest-value items but to **select the subset of tasks from your known set () that maximises total perceived value () without exceeding your capacity**.
	Mathematically, you want to choose a set of tasks (your Work-in-Progress) such that:
2. **Organisational Health ()** Factors like cohesion, trust, and goal alignment determine your team's **efficiency**. We can represent this with an **Efficiency Multiplier,** (eta), where .
	- A healthy, aligned, high-trust team has an efficiency .
	- A team with low trust, poor cohesion, or conflicting goals has a low efficiency, e.g., .
	This factor directly impacts your capacity and value realisation. A task with an estimated effort of will have an **actual cost of** . If your team's efficiency is 60%, a 1-week task will actually take almost 2 weeks to complete. This multiplier makes the "soft" concepts of team health mathematically tangible.

---

## \## Modelling the External World (Locus of Control) 🌍

Your company doesn't operate in a vacuum. We can partition the universe of events and factors based on your ability to control them. This helps clarify where to focus your strategic efforts.

- **(Control):** This is the set of internal company actions we have been discussing (what we previously called ). You decide whether to do these.
- **(Influence):** The set of external outcomes or events you can influence but not control. Examples include public relations, lobbying, or negotiations with a partner.
- **(Exogenous):** The set of external factors you care about but have no control over. Examples include interest rate changes, competitor actions, or new government regulations.

The crucial insight here is that the value of your internal actions is often **conditional on the state of the external world**. A task's value is not static. We should therefore think of the value function as:

This means the value of an action depends on the current state () of the worlds you can influence () and those you can't ().

**This creates three distinct strategic stances:**

1. **Execution (managing ):** Choosing the optimal tasks to do, given your constraints.
2. **Influence (managing ):** Expending effort to shape the external environment to your advantage (e.g., running a marketing campaign to increase the potential value of a new feature).
3. **Adaptation (monitoring ):** Watching for external threats and opportunities that change the potential value of your planned actions, forcing you to re-prioritise.

Google Account

Leon Ormes

leonormes@gmail.com
