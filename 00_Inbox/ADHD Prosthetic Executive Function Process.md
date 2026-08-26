---
captured: 2026-08-26T06:55:38+01:00 2026-08-26T06:55:38+01:00
created: 2026-08-26T05:53:24+00:00
modified: 2026-08-26T07:16:11+00:00
permalink: llmeon/00-inbox/head-new-chat
source: https://gemini.google.com/app/c6f3586d9370853f
status: processing
tags: [input]
title: ADHD Prosthetic Executive Function Process
type: head
---

## Restructuring the Condition of Satisfaction: Cognitive Scaffolding and Executive Function Prosthetics for Neurodivergent Knowledge Workers

### Introduction to Executive Dysfunction in Agile Environments

In the contemporary landscape of digital knowledge work, particularly within software engineering, product development, and systems architecture, cognitive demands are heavily centered on sustained attention, rapid context switching, and self-directed task management. For individuals with Attention-Deficit/Hyperactivity Disorder (ADHD), these environmental demands are fundamentally misaligned with their underlying neurological profiles1. Modern frameworks such as Agile, Scrum, and Kanban rely heavily on neuro-normative assumptions about human motivation, time perception, and working memory. These frameworks assume that individuals can independently parse abstract requirements, consistently initiate tasks, accurately estimate the time required for completion, and seamlessly transition between discrete items of work2.

When knowledge workers with ADHD interact with standard Agile artifacts—most notably Jira tickets and traditional Conditions of Satisfaction (CoS) or Definitions of Done (DoD)—they frequently encounter severe systemic friction. A ubiquitous experience among neurodivergent professionals is that a ticket feels distressingly open-ended. This perceived lack of boundaries creates a psychological barrier to task completion. The individual often struggles to visualize the tangible endpoint of the work, leading to profound task paralysis5. Furthermore, even when a task is successfully initiated and executed, the individual may find themselves [[unable to effortlessly disengage]] from the completed task to begin the next, remaining trapped in a state of cognitive inertia6.

This report exhaustively investigates the neurobiological, psychological, and environmental mechanisms driving these specific challenges. It analyzes the etiology of task paralysis, the cognitive toll of task switching, and the phenomenon of attention residue. Moreover, it synthesizes empirical mitigations drawn from clinical psychology and human-computer interaction (HCI), including Episodic Future Thinking (EFT), implementation-focused Cognitive Behavioral Therapy (CBT), and Artificial Intelligence (AI) cognitive scaffolding8. Ultimately, this analysis provides a comprehensive, structural blueprint for reimagining the CoS and DoD not merely as project management checkpoints, but as customized "prosthetic executive functions." By embedding neurological mitigations directly into the task architecture, organizations can offload cognitive burden, bridge the gap between intention and action, and foster a neuro-inclusive digital workspace.

### The Neurobiology of Task Paralysis and Open-Endedness

To construct an effective cognitive prosthesis, it is essential to first decode the neurological etiology of task paralysis and the inability to visualize task completion. The perception that a work ticket is "open-ended" is not a failure of reading comprehension, nor is it a symptom of low motivation. Rather, it is a direct manifestation of specific neural network dysregulations that govern attention, working memory, and goal-directed behavior.

#### Default Mode Network and Task Positive Network Interference

Human attention and cognitive focus are largely governed by the interplay of large-scale brain networks. The Default Mode Network (DMN), which encompasses the medial prefrontal cortex, the posterior cingulate cortex, the hippocampus, the amygdala, and parts of the inferior parietal lobe, is highly active during states of wakeful rest, mind-wandering, introspection, and internal self-referential thought11. Conversely, the Task Positive Network (TPN), which includes the Central Executive Network and the dorsal attention network, activates during externally directed, goal-oriented tasks that require sustained focus11.

In neurotypical individuals, these networks are tightly anti-correlated; the activation of the TPN naturally suppresses and deactivates the DMN, allowing for seamless, undisturbed focus on the task at hand12. However, functional magnetic resonance imaging (fMRI) studies consistently reveal that in individuals with ADHD, the DMN fails to deactivate appropriately during cognitive tasks. This results in the simultaneous activation of both the DMN and the TPN11.

This hyperconnectivity and lack of reciprocal inhibition between the DMN and task-relevant networks create a state of continuous neurological "cross-talk"15. Dr. Russell Ramsay, a leading clinical psychologist specializing in adult ADHD, notes that this neural architecture leads directly to implementation failures9. When an ADHD knowledge worker views a Jira ticket that lacks rigid, concrete, and highly specified boundaries, the DMN remains highly active, generating tangential thoughts, anxieties, and associative thinking about the project's broader implications.

| Network Feature | Neurotypical Function | ADHD Dysfunction | Impact on Knowledge Work |
|:---- |:---- |:---- |:---- |
| Default Mode Network (DMN) | Deactivates during focused tasks to minimize internal distraction. | Remains active; fails to attenuate during cognitive demand14. | Intrusive thoughts, mind-wandering, and task paralysis when viewing abstract tickets6. |
| Task Positive Network (TPN) | Sustains attention on external goals. | Competes with the DMN for cognitive resources11. | High cognitive fatigue; inability to maintain linear focus on sequential task steps11. |
| Network Integration | Segregated functioning depending on task state. | Higher Participation Coefficient (PC) indicating excessive integration15. | Commission errors, response time variability, and susceptibility to distraction15. |

This neurological noise rapidly overwhelms the limited working memory capacity required to parse the ticket, resulting in what is colloquially known as task paralysis5. The brain becomes overloaded by the sheer volume of implicit requirements, potential solutions, and moving parts. Instead of initiating the task, the system shuts down, and the individual resorts to procrastination or avoidance as a protective mechanism against cognitive overload6.

#### Dopaminergic Reward Deficits and Delay Discounting

The inability to visualize completing a task and moving on is intimately tied to the brain's reward circuitry and its perception of time. ADHD is widely characterized by a hypodopaminergic state, specifically within the frontostriatal circuits and the dorsolateral prefrontal cortex (DLPFC)14. The DLPFC serves as the command center for executive functions, critically involved in the selection, manipulation, and maintenance of representations for upcoming actions—essentially, the ability to hold a future goal in working memory and direct behavior toward it21.

Because dopamine regulates the anticipation of reward and salience attribution, individuals with ADHD exhibit steep "delay discounting." Delay discounting refers to the psychological phenomenon where the subjective value of a reward decreases precipitously the further away it is in time23. An open-ended software ticket represents a delayed, highly abstract reward (the satisfaction of moving the ticket to the "Done" column or deploying a feature). Because the endpoint is not vividly represented or anchored in the DLPFC, the brain fails to generate the dopaminergic momentum necessary for task initiation20.

The clinical literature describes ADHD not as a deficit of knowledge, but as a deficit of performance at the point of performance17. The worker knows exactly what needs to be done, possesses the technical skills to execute it, and understands the negative consequences of failure. However, the executive dysfunction prevents the translation of that macro-level knowledge into localized, sequential action in the present moment17.

### The Cognitive Costs of Task Switching and Attention Residue

Even in scenarios where an ADHD professional successfully initiates and completes a complex task, transitioning to the next ticket presents a secondary, often more debilitating challenge. Task switching—the cognitive flexibility required to disengage from one mental set, clear the working memory, and engage with an entirely new set of rules and goals—is fundamentally impaired in the ADHD cognitive profile5.

#### The Phenomenon of Attention Residue

When knowledge workers switch from one task to another, their attention does not cleanly follow the physical shift in activity. Dr. Sophie Leroy's foundational research at the University of Washington identified the phenomenon of "attention residue." This occurs when a significant portion of cognitive processing remains involuntarily allocated to a previous task after a physical switch to a new one19. This residue degrades performance, increases error rates, severely diminishes decision-making capabilities, and causes immense cognitive fatigue on the subsequent task19.

Attention residue is most pronounced under specific conditions: when a task is left incomplete (creating an open loop), when the previous task involved deep cognitive engagement, and when the interruption was self-initiated31. The economic and productivity costs of this context switching are severe across the broader knowledge work industry, but they disproportionately impact those with executive function deficits.

| Context Switching Metric | Empirical Finding | Source / Researcher |
|:---- |:---- |:---- |
| Refocusing Time | It takes an average of 23 minutes and 15 seconds to fully return to an original task after an interruption. | Gloria Mark (UC Irvine)32 |
| Intervening Tasks | Before returning to the original task, workers switch to an average of 2.26 other tasks. | Gloria Mark (UC Irvine)32 |
| Average Attention Span | Time spent on a single screen before switching has collapsed from 2.5 minutes in 2004 to 47 seconds in recent years. | Gloria Mark (UC Irvine)33 |
| Daily App Switches | Knowledge workers toggle between apps and websites approximately 1,200 times a day. | Harvard Business Review33 |
| Economic Cost | Context switching costs the US economy an estimated $450 billion annually in lost productivity. | Extrapolated Workplace Data32 |
| Productive Time Loss | Up to 40% of productive time (roughly three hours daily) is lost to the mental cost of shifting between tasks. | American Psychological Association33 |

#### Amplification of Cognitive Inertia and Hyperfocus in ADHD

For individuals with ADHD, the mechanical drag of attention residue is severely amplified. The specific executive function responsible for unhooking attention from one task and locking it onto the next is known as "set-shifting" (or cognitive flexibility)5. Neurologically, set-shifting relies heavily on working memory capacity and inhibitory control to suppress the rules of the previous task and activate the rules of the new one26. Both of these faculties are biologically compromised in the ADHD profile26.

When an ADHD brain attempts to switch away from a ticket, especially if that ticket feels unresolved or lacks a definitive closure state, the task remains active in working memory as an "open loop"7. This creates profound cognitive inertia. The situation is further complicated by the phenomenon of hyperfocus. Hyperfocus is a flow-like state often utilized by ADHD brains as a compensatory mechanism to overcome baseline dopaminergic under-arousal6. When engaged in hyperfocus, the individual experiences complete absorption in a task, ignoring environmental stimuli and the passage of time38.

While hyperfocus can result in exceptional productivity, it locks the attention network so tightly that shifting away requires a massive, exhaustive mental reset6. If a developer finishes a complex coding ticket while in a state of hyperfocus and immediately opens the next ticket without a structured, neurological transition, the attention residue from the first ticket clings to their working memory. It operates much like a background application draining a computer's RAM7. Consequently, staring at the second ticket feels insurmountable, leading directly to the reported experience of being unable to "just switch to the next ticket."

### Evidence-Based Mitigations for Executive Dysfunction

To transform the Condition of Satisfaction into a functional prosthetic executive function, the project management architecture must integrate evidence-based clinical interventions. These interventions must directly counteract Default Mode Network interference, mitigate delay discounting, and actively flush attention residue. The empirical research literature points to several primary mitigation strategies: Episodic Future Thinking, Implementation-Focused Task Scoping, Transition Rituals, and AI-driven Metacognitive Scaffolding.

#### Episodic Future Thinking (EFT)

Prospective memory—the cognitive ability to remember to execute intended actions in the future—is frequently impaired in adults with ADHD, leading to chronic difficulties in planning and executing delayed intentions in everyday life8. Episodic Future Thinking (EFT) is a robust psychological intervention designed to disrupt future discounting by altering the perceived value of delayed outcomes23. EFT involves mentally projecting oneself into the future to vividly imagine, simulate, and experience a specific, personal, and detailed future-oriented event23.

Studies demonstrate that engaging in EFT during the intention-formation phase (e.g., when reading a new work ticket) significantly reduces delay discounting and improves prospective memory execution in adults with ADHD8. By mentally simulating the execution and completion of a task, EFT activates prefrontal-mediotemporal interactions, thereby enhancing goal salience and bridging the temporal gap that causes task avoidance23.

Recent clinical evaluations distinguish between process-focused EFT (imagining the steps required to complete the task) and outcome-focused EFT (imagining the state of completion and the subsequent reward)39. Interestingly, while both are beneficial, manipulating the instructional focus during intention formation yields significant improvements in daily functioning39. Narrative Episodic Future Thinking (NEFT), a variant where future events are imagined as a cohesive, thematically linked story rather than isolated snapshots, has proven even more effective at influencing decision-making and reducing task paralysis24. In the context of knowledge work, if an individual cannot visualize completing a ticket, EFT must be systematically built into the ticket's acceptance criteria to neutralize the brain's tendency to discount the delayed completion39.

#### Implementation-Focused Cognitive Behavioral Therapy (CBT)

Standard productivity advice—such as "just use a planner" or "break tasks down"—frequently fails ADHD brains because it relies on accurate time perception and reliable task initiation faculties that are neurologically compromised3. Cognitive Behavioral Therapy (CBT) adapted specifically for adult ADHD, pioneered by clinical researchers such as Dr. J. Russell Ramsay and Dr. Steven Safren, shifts the therapeutic focus entirely away from knowledge acquisition and toward implementation and environmental engineering9.

Because ADHD is characterized as an implementation deficit, the most effective cognitive intervention is granular, hyper-specific task breakdown17. A high-level project goal provides no cognitive scaffolding. Instead, the task must be deconstructed into literal, physical micro-actions41. Ramsay emphasizes the creation of "behavioral prescriptions"—written, tangible reminders of the exact steps, anticipated barriers, and predetermined solutions required to execute a task17.

This CBT framework addresses the phenomenon of "procrastivity," a specific manifestation of avoidance where an individual avoids a higher-priority task by engaging in a lower-priority, less time-urgent, but still technically productive endeavor (e.g., refactoring an old codebase instead of writing the required feature documentation)25. The CoS must serve as this behavioral prescription, externalizing the working memory required to hold the sequence of steps in mind and circumventing procrastivity by explicitly defining the path of least resistance40.

#### The "Crumb Protocol" and Transition Rituals

To mitigate attention residue and avoid the 23-minute recovery cost associated with context switching, structured transition rituals are required. These rituals act to manually close the cognitive loops that the ADHD brain fails to close automatically7.

The "Crumb Protocol," derived directly from Sophie Leroy's research on attention residue, mandates that before switching tasks, the worker must leave a "crumb" or a "bridge note"7. The protocol involves a structured sequence of actions—Capture, Close, Clear, Cue, and Commit—designed to clear residual cognitive processing from previous tasks19.

Writing down the exact, literal next physical action that will be taken when returning to the task, or formally acknowledging the exact state of the completed task, signals to the brain that the state is saved safely outside of working memory7. This fulfills the psychological requirement for closure (counteracting the Zeigarnik effect, which dictates that uncompleted tasks are remembered better than completed ones). This deliberate cognitive offloading allows the Default Mode Network to release the previous task, freeing up the impaired set-shifting mechanism to fully engage with the subsequent ticket without residual cognitive drag7.

### Artificial Intelligence and Metacognitive Scaffolding

The integration of Generative Artificial Intelligence (GenAI) and Large Language Models (LLMs) represents a paradigm shift in creating cognitive prosthetics for neurodivergent individuals. In this context, AI acts as a non-human dialogic agent that provides essential metacognitive scaffolding43. Metacognition—the ability to reflect on, monitor, and regulate one's own thinking and behavior—is heavily taxed by executive dysfunction, making self-directed task management highly fatiguing43.

Neurodivergent professionals successfully utilize AI not to generate the final work product, but to offload the executive burden of starting, structuring, and sequencing10. This dynamic creates a "scaffold that disappears," removing procedural demands from the user's working memory so that cognitive effort can be directed entirely toward content generation and problem-solving47.

#### Interaction Patterns and Executive Support

Empirical analyses of neurodivergent interactions with LLMs reveal several highly effective use cases for executive function scaffolding:

> 1. The Next Physical Step: When facing task paralysis, users prompt the AI with a frozen task and ask exclusively for the very first, five-minute concrete action. This provides a "bottom rung" to the ladder of task initiation, bypassing the overwhelming requirement to plan the entire sequence10.
> 2. Digital Body Doubling: "Body doubling" is a well-documented ADHD strategy where the presence of another individual anchors focus. Users employ voice-enabled AI or conversational agents to narrate their workflow. The AI reflects the user's actions back to them without judgment, serving as a socially safe anchor that prevents the DMN from dragging the user into distraction1.
> 3. Reframing the Wall of Overwhelm: Decision fatigue is mitigated by dumping chaotic, unorganized thoughts, emails, and loose threads into an LLM and instructing it to synthesize the data into a prioritized list of the top three critical items. This bypasses decision paralysis and immediately reduces nervous system arousal10.
> 4. Emotional Regulation and Rejection Sensitivity: Because LLMs lack ego and do not experience frustration, they serve as a safe container for users to process confusion or anxiety without the fear of straining human relationships or triggering Rejection Sensitive Dysphoria (RSD)45.

#### The Risks of Cognitive Offloading and Learned Helplessness

While the benefits of AI scaffolding are substantial, they must be implemented with rigorous safeguards. Excessive cognitive offloading carries the risk of inducing "learned dependence," which can rapidly devolve into "learned helplessness"49. If an individual relies on AI for every instance of task initiation or problem-solving, their intrinsic executive function muscles may atrophy, leading to a state where they feel entirely incapable of overcoming challenges without algorithmic intervention50.

Furthermore, researchers warn of the "Stockholm Syndrome of AI Dependency," wherein users unquestioningly accept AI-generated plans or decisions, undermining their agency, critical judgment, and metacognitive growth50. Therefore, AI must be integrated into the CoS strictly as a temporary scaffold to overcome initiation friction, not as a permanent replacement for the user's critical reasoning.

### Reengineering the Condition of Satisfaction (CoS) and Definition of Done (DoD)

Standard Agile CoS and DoD frameworks are primarily designed to ensure product quality, alignment, and releasability. They consist of checklists verifying that code is peer-reviewed, unit tests pass, documentation is updated, and the build is pushed to staging4. While these criteria are vital for organizational health, they are fundamentally neuro-normative constructs. They define the desired outcome but offer absolutely no executive function support for the cognitive navigation required to reach that outcome2.

To transform the CoS into a functional prosthetic executive function for ADHD, the ticket architecture must be fundamentally redesigned. It must integrate Episodic Future Thinking, granular implementation strategies, attention residue clearance protocols, and AI scaffolding directly into the workflow.

| Architectural Feature | Standard DoD / CoS | Prosthetic Executive Function DoD / CoS | Cognitive Rationale for ADHD |
|:---- |:---- |:---- |:---- |
| Primary Focus | Outcome-oriented (Product Quality & Releasability) | Process and Implementation-oriented (Cognitive Navigation) | Bypasses the "knowing-doing" gap by explicitly scripting the required behavior4. |
| Task Granularity | Broad requirements (e.g., "Implement login API") | Micro-physical actions (e.g., "Open auth.js, write endpoint signature") | Drastically reduces working memory load; prevents DMN intrusion and task paralysis6. |
| Endpoint Visualization | Implicit (assumes developer understands what finished looks like) | Explicit EFT narrative ("When done, you will see a green checkmark on the local host build") | Counters delay discounting by making the future reward vivid, immediate, and salient23. |
| Task Transitioning | Abrupt (Move ticket to "Done", immediately pull next ticket) | Scaffolded (Mandatory "Bridge Note" or "Crumb" entry before moving ticket) | Clears attention residue; supports impaired set-shifting; prevents cognitive drag into the next task7. |
| Blocker Management | Assumes independent problem-solving and self-regulation | Mandates AI "Brain Dump" or explicit body-doubling when stuck for \>15 minutes | Provides external metacognitive regulation; breaks hyperfocus on dead-ends and prevents emotional dysregulation10. |

#### Implementing the Prosthetic CoS in Project Management Tools

Modern project management tools like Jira possess the technical capabilities to enforce these cognitive scaffolds through automation and plugins. By utilizing tools such as "Smart Checklist for Jira" or native workflow validators, teams can embed the prosthetic CoS directly into the issue view51. A workflow validator can be configured to physically prevent a ticket from transitioning to the next status (e.g., from "In Progress" to "Done") unless specific cognitive transition criteria are checked off, enforcing the behavioral prescription4.

The implementation of the Prosthetic CoS is divided into three distinct chronological phases: Pre-Flight (Initiation), In-Flight (Execution), and Landing (Closure and Transition).

#### Phase 1: The Initiation Scaffold (Pre-Flight)

When a ticket is opened, the perception of it being "open-ended" must be immediately and systematically dismantled. The CoS begins with a required initialization checklist designed to suppress the Default Mode Network and ground the Task Positive Network.

> 1. The EFT Visualization Prompt: The ticket template must include a mandatory section where the author (or the developer during sprint refinement) explicitly states the sensory or narrative endpoint of the task. Instead of an acceptance criterion reading "Fix authentication bug," it must read: _"Visualization: Typing the test command into the terminal and watching the output return 'True' with zero latency."_ This utilizes outcome-focused Episodic Future Thinking to bridge the temporal gap to the reward, providing the dopamine necessary for initiation23.
> 2. The First Ten Minutes Rule: The ticket must explicitly define the very first physical action to be taken. If it does not, the developer's first mandated task is to use an AI prompt to generate it (e.g., _"I have to execute \[Ticket Summary\] and I am experiencing task paralysis. Provide the single first physical step that takes under 5 minutes to complete"_)10. The CoS dictates that work has not officially started until this micro-step is documented and executed.

#### Phase 2: The Execution Scaffold (In-Flight)

During the execution phase, executive dysfunction frequently manifests as getting lost in tangential details, over-engineering (driven by hyperfocus), or losing the thread of working memory.

> 1. Mandatory Micro-Batching: Because ADHD brains suffer from time blindness and cannot reliably estimate duration, the CoS should require work to be broken into 20-to-30-minute verifiable increments1. This externalizes time management. If a developer spends more than a designated amount of time without executing a micro-batch, it indicates hyperfocus or paralysis, triggering a pre-planned cognitive intervention.
> 2. Metacognitive Externalization (The Brain Dump): If the task becomes ambiguous or the developer feels overwhelmed, the CoS mandates a "Brain Dump." The developer is required to paste their current chaotic mental state, code snippets, and loose threads into an LLM, instructing it to reorganize the data into a prioritized list. This effectively offloads the impaired working memory and executive sorting functions to the machine, immediately lowering cognitive load10.

#### Phase 3: The Closure and Transition Scaffold (Landing)

This is the most critical phase for mitigating the feeling of being unable to switch to the next ticket. The traditional Agile practice of simply dragging a ticket to the "Done" column is vastly insufficient because it does not manage attention residue or support set-shifting19.

> 1. The Crumb Protocol Requirement: Jira workflow validators must be set to prevent a ticket from moving to "Done" (or moving to a blocked state) until a transition ritual is completed. The developer must write a "Bridge Note" or "Crumb" in the ticket comments7.

   - If the task is finished: The developer writes one sentence summarizing the completed state and the emotional closure (e.g., _"The API is fully integrated, tests are passing, this mental loop is permanently closed and archived."_).
   - If the task is paused (due to an interruption, blocker, or end of day): The developer writes the literal next physical keystroke required upon their return (e.g., _"Next step: paste the auth token variable into line 42 of index.js"_). This prevents the brain from keeping the loop open in the background7.

> 1. Physical Environment Reset: The CoS checklist requires the physical closure of all relevant IDE tabs, browser windows, terminal sessions, and documentation strictly related to the finished ticket6. This provides a definitive visual and physical signal to the brain that the context is closed, signaling the DMN to release its hold on the previous data structure19.
> 2. The Context-Switching Buffer: To accommodate delayed set-shifting hardware in the ADHD brain, the workflow must enforce a mandatory brief buffer (e.g., a 5-minute break involving physical movement or a brief mindfulness grounding exercise) before opening the next ticket6. This allows the neurological transition to finalize, ensuring the subsequent ticket is approached with a cleared working memory rather than a residue-depleted cognitive state28.

### Conclusion

The profound challenges faced by neurodivergent knowledge workers—task paralysis, cognitive inertia, and the overwhelming ambiguity of open-ended work—are not indicative of a lack of professional skill, technical knowledge, or motivation. Rather, they are direct manifestations of underlying neurobiological realities, specifically Default Mode Network hyperconnectivity, dopaminergic reward deficits in the prefrontal cortex, and impaired set-shifting mechanisms. Traditional Agile environments and standard Definitions of Done inadvertently exacerbate these vulnerabilities by demanding high working memory capacity, flawless time perception, and seamless context switching, all without providing the necessary structural support.

By systematically restructuring the Condition of Satisfaction into a cognitive prosthesis, organizations and individuals can successfully externalize these taxed executive functions. Integrating Episodic Future Thinking allows workers to vividly visualize task completion, effectively mitigating delay discounting and generating the momentum for task initiation. Applying implementation-focused Cognitive Behavioral Therapy principles ensures tasks are reduced to their physical primitives, bypassing the "knowing-doing" gap. Furthermore, mandating the "Crumb Protocol" and strict transition rituals actively flushes attention residue, allowing the ADHD brain to safely close cognitive loops and smoothly transition to new objectives without carrying the cognitive drag of the previous task.

When augmented by the responsible use of Artificial Intelligence for metacognitive scaffolding—providing digital body doubling and immediate step-by-step unblocking—this redesigned workflow transcends standard project management. It transforms the ticket from a static organizational requirement into an active, neuro-inclusive behavioral prescription that seamlessly bridges the gap between professional intention and executed action.

#### Works Cited

> 1. A Systems and AI-Based Human-in-the-Loop Framework for ADHD, [https://arxiv.org/html/2507.06864](https://arxiv.org/html/2507.06864)
> 2. (PDF) Neurodivergent-Inclusive Software Design: Cognitive-Aware, [https://www.researchgate.net/publication/393879998\_Neurodivergent-Inclusive\_Software\_Design\_Cognitive-Aware\_Development\_Practices\_for\_Human-Centered\_AI\_Interfaces](https://www.researchgate.net/publication/393879998_Neurodivergent-Inclusive_Software_Design_Cognitive-Aware_Development_Practices_for_Human-Centered_AI_Interfaces)
> 3. ADHD Productivity: Strategies That Actually Work \- Dr Nathalie Tasler, [https://nathalietasler.blog/2026/07/11/adhd-productivity-strategies/](https://nathalietasler.blog/2026/07/11/adhd-productivity-strategies/)
> 4. What Is the Definition of Done in Agile and Why It Matters, [https://community.atlassian.com/forums/App-Central-articles/What-Is-the-Definition-of-Done-in-Agile-and-Why-It-Matters/ba-p/3074898](https://community.atlassian.com/forums/App-Central-articles/What-Is-the-Definition-of-Done-in-Agile-and-Why-It-Matters/ba-p/3074898)
> 5. ADHD and Task Switching: 10 Tips for Improvement \- Healthline, [https://www.healthline.com/health/adhd/task-switching-adhd](https://www.healthline.com/health/adhd/task-switching-adhd)
> 6. Task Switching in ADHD: Why It Feels So Hard (and What Helps), [https://neurosparkhealth.com/executive-functioning/task-switching-and-adhd](https://neurosparkhealth.com/executive-functioning/task-switching-and-adhd)
> 7. ADHD Attention Residue: Why a 30-Second Ping Costs You 40, [https://dineshachari.com/blog/adhd-attention-residue](https://dineshachari.com/blog/adhd-attention-residue)
> 8. Episodic Future Thinking Improves Everyday Prospective Memory, [https://www.ebsco.com/articles/psychology/119299ee-60b0-57e7-a49b-8c46f353243f/episodic-future-thinking-improves-everyday-prospective-memory-performance-in-adults-with-a-previous-diagnosis-of-attention-deficit-hyperactivity-disorder-by-community-providers](https://www.ebsco.com/articles/psychology/119299ee-60b0-57e7-a49b-8c46f353243f/episodic-future-thinking-improves-everyday-prospective-memory-performance-in-adults-with-a-previous-diagnosis-of-attention-deficit-hyperactivity-disorder-by-community-providers)
> 9. CBT for adult ADHD: Helping clients turn intentions into actions, [https://www.bespokementalhealth.co.uk/on-demand/advert/cbt-for-adult-adhd%3A-helping-clients-turn-intentions-into-actions](https://www.bespokementalhealth.co.uk/on-demand/advert/cbt-for-adult-adhd%3A-helping-clients-turn-intentions-into-actions)
> 10. AI as an Executive-Function Scaffold for ADHD \- Kelly and Coffee, [https://kellyand.coffee/posts/2026-06-13-ai-as-an-adhd-executive-function-scaffold/](https://kellyand.coffee/posts/2026-06-13-ai-as-an-adhd-executive-function-scaffold/)
> 11. The Default Mode Network and ADHD \- LA Concierge Psychologist, [https://laconciergepsychologist.com/blog/default-mode-network-adhd/](https://laconciergepsychologist.com/blog/default-mode-network-adhd/)
> 12. ADHD's Secret Demon—and How to Tame It \- ADDitude, [https://www.additudemag.com/default-mode-network-adhd-brain/](https://www.additudemag.com/default-mode-network-adhd-brain/)
> 13. Intrinsic Functional Connectivity in the Default Mode Network, [https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2022.859538/full](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2022.859538/full)
> 14. Task-related Default Mode Network modulation and inhibitory … \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4754961/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4754961/)
> 15. Increased integration between default mode and task-relevant, [https://pubmed.ncbi.nlm.nih.gov/34252881/](https://pubmed.ncbi.nlm.nih.gov/34252881/)
> 16. Increased integration between default mode and task-relevant, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8278154/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8278154/)
> 17. CBT for Adult ADHD: From Intention to Action \- Psychwire, [https://psychwire.com/free-resources/q-and-a/15i4yzk/cbt-for-adult-adhd-from-intention-to-action](https://psychwire.com/free-resources/q-and-a/15i4yzk/cbt-for-adult-adhd-from-intention-to-action)
> 18. mode network abnormalities during state switching in attention, [https://pubmed.ncbi.nlm.nih.gov/26456561/](https://pubmed.ncbi.nlm.nih.gov/26456561/)
> 19. Attention Residue (Sophie Leroy): How to Clear It and Refocus, [https://goalsandprogress.com/attention-residue-management/](https://goalsandprogress.com/attention-residue-management/)
> 20. Dorsolateral prefrontal cortex dysfunction caused by a go/no-go task, [https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1145485/full](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1145485/full)
> 21. Dorsolateral Prefrontal Cortex, Working Memory, and Prospective, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6673563/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6673563/)
> 22. The Lateral Prefrontal Cortex and Selection/Inhibition in ADHD, [https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2018.00065/full](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2018.00065/full)
> 23. Digital Episodic Future Thinking Intervention (Luminaut), [https://humanfactors.jmir.org/2026/1/e74099](https://humanfactors.jmir.org/2026/1/e74099)
> 24. Narrative episodic future thinking reduces delay discounting and, [https://www.tandfonline.com/doi/full/10.1080/21642850.2025.2531948](https://www.tandfonline.com/doi/full/10.1080/21642850.2025.2531948)
> 25. CBT for Adult ADHD: Getting Patients to Do What They Know They, [https://www.ajmc.com/view/cbt-for-adult-adhd-getting-patients-to-do-what-they-know-they-need-to-do](https://www.ajmc.com/view/cbt-for-adult-adhd-getting-patients-to-do-what-they-know-they-need-to-do)
> 26. Executive Function Disorder & ADHD | ADDA, [https://add.org/executive-function-disorder/](https://add.org/executive-function-disorder/)
> 27. Cognitive Impairment in Adult Attention Deficit Hyperactivity Disorder, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12384060/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12384060/)
> 28. Context Switching: The Silent Productivity Killer (and How to Fix It), [https://mera.work/context-switching/](https://mera.work/context-switching/)
> 29. Attention Residue: The Hidden Cost of Every Interrupted Task, [https://www.calendar.com/blog/attention-residue-hidden-cost-interrupted-task/](https://www.calendar.com/blog/attention-residue-hidden-cost-interrupted-task/)
> 30. How to Reduce Attention Residue With ADHD, [https://imbusybeingawesome.com/attention-residue/](https://imbusybeingawesome.com/attention-residue/)
> 31. Attention Residue: Why Your Brain Can't Focus After AI |, [https://clearing-ai.com/attention-residue.html](https://clearing-ai.com/attention-residue.html)
> 32. Context Switching Costs $450B/Year \[2026 Research\] \- WaymakerOS, [https://www.waymakeros.com/learn/context-switching-costs-450b](https://www.waymakeros.com/learn/context-switching-costs-450b)
> 33. Context Switching Statistics 2026: The Cost of Distraction \- Carly AI, [https://www.usecarly.com/blog/context-switching-statistics/](https://www.usecarly.com/blog/context-switching-statistics/)
> 34. It Takes 23 Minutes to Refocus After One Distraction (2026 Research), [https://pomogolo.com/blog/23-minute-refocus-cost](https://pomogolo.com/blog/23-minute-refocus-cost)
> 35. Context Switching Kills Creative Productivity: The Real Cost, [https://www.mtm.video/blog/context-switching-kills-creative-productivity](https://www.mtm.video/blog/context-switching-kills-creative-productivity)
> 36. Executive function deficits in attention-deficit/hyperactivity disorder, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11485171/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11485171/)
> 37. Episodic Future Thinking Improves Everyday Prospective Memory, [https://www.researchgate.net/publication/400755431\_Episodic\_Future\_Thinking\_Improves\_Everyday\_Prospective\_Memory\_Performance\_in\_Adults\_With\_a\_Previous\_Diagnosis\_of\_Attention\_Deficit\_Hyperactivity\_Disorder\_by\_Community\_Providers](https://www.researchgate.net/publication/400755431_Episodic_Future_Thinking_Improves_Everyday_Prospective_Memory_Performance_in_Adults_With_a_Previous_Diagnosis_of_Attention_Deficit_Hyperactivity_Disorder_by_Community_Providers)
> 38. Hyperfocus: the forgotten frontier of attention \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7851038/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7851038/)
> 39. The impact of processversus outcome-focused episodic future, [https://pubmed.ncbi.nlm.nih.gov/42475007/](https://pubmed.ncbi.nlm.nih.gov/42475007/)
> 40. (PDF) CBT for Adult ADHD: Adaptations and Hypothesized, [https://www.researchgate.net/publication/233573605\_CBT\_for\_Adult\_ADHD\_Adaptations\_and\_Hypothesized\_Mechanisms\_of\_Change](https://www.researchgate.net/publication/233573605_CBT_for_Adult_ADHD_Adaptations_and_Hypothesized_Mechanisms_of_Change)
> 41. CBT Exercises for ADHD | Oxford CBT, [https://www.oxfordcbt.co.uk/cbt-exercises-for-adhd/](https://www.oxfordcbt.co.uk/cbt-exercises-for-adhd/)
> 42. Attention residue is eroding your focus \- DEV Community, [https://dev.to/stashpad/attention-residue-is-eroding-your-focus-4om5](https://dev.to/stashpad/attention-residue-is-eroding-your-focus-4om5)
> 43. Scaffolding Metacognition in Design with Generative AI, [https://dl.designresearchsociety.org/cgi/viewcontent.cgi?article=1596\&context=iasdr](https://dl.designresearchsociety.org/cgi/viewcontent.cgi?article=1596&context=iasdr)
> 44. AI META PROMPTING AS COGNITIVE SCAFFOLDING IN, [https://espeap.junis.ni.ac.rs/index.php/espeap/article/view/1777](https://espeap.junis.ni.ac.rs/index.php/espeap/article/view/1777)
> 45. Affordances and Risks of ChatGPT to Autistic Users \- arXiv, [https://arxiv.org/html/2601.17946v1](https://arxiv.org/html/2601.17946v1)
> 46. \[PDF\] Scaffolding Metacognition with GenAI: Exploring Design, [https://www.semanticscholar.org/paper/Scaffolding-Metacognition-with-GenAI%3A-Exploring-to-Zhu-Yu/1f43c9e6e4f2fab795986623794d4e82e427754e](https://www.semanticscholar.org/paper/Scaffolding-Metacognition-with-GenAI%3A-Exploring-to-Zhu-Yu/1f43c9e6e4f2fab795986623794d4e82e427754e)
> 47. The Scaffold That Disappears: AI Tools for Executive Function in, [https://ciddl.org/the-scaffold-that-disappears-ai-tools-for-executive-function-in-science-classrooms/](https://ciddl.org/the-scaffold-that-disappears-ai-tools-for-executive-function-in-science-classrooms/)
> 48. The ADHD Developer's Struggles (and How They Show Up at Work), [https://softwareascraft.com/adhd/adhd-developers-struggles/](https://softwareascraft.com/adhd/adhd-developers-struggles/)
> 49. AI's cognitive implications: the decline of our thinking skills?, [https://www.ie.edu/center-for-health-and-well-being/blog/ais-cognitive-implications-the-decline-of-our-thinking-skills/](https://www.ie.edu/center-for-health-and-well-being/blog/ais-cognitive-implications-the-decline-of-our-thinking-skills/)
> 50. Effects of Cognitive Offloading in the AI Era | by Hanning Ni, [https://watchsound.medium.com/from-learned-dependence-to-learned-helplessness-effects-of-cognitive-offloading-in-the-ai-era-e0bc63b41dbe](https://watchsound.medium.com/from-learned-dependence-to-learned-helplessness-effects-of-cognitive-offloading-in-the-ai-era-e0bc63b41dbe)
> 51. Definition of Done in Jira with Examples | TitanApps Blog, [https://titanapps.io/blog/definition-of-done-in-jira](https://titanapps.io/blog/definition-of-done-in-jira)
> 52. Definition of Done for different issue types in Jira \- Scrum.org, [https://www.scrum.org/forum/scrum-forum/54685/definition-done-different-issue-types-jira](https://www.scrum.org/forum/scrum-forum/54685/definition-done-different-issue-types-jira)
> 53. How to create a Definition of Done checklist in Jira \- HeroCoders, [https://www.herocoders.com/blog/definition-of-done](https://www.herocoders.com/blog/definition-of-done)
> 54. How to Track the Definition of Done in Jira with Checklists \- Stiltsoft, [https://stiltsoft.com/blog/how-to-track-definition-of-done-in-jira-with-checklists/](https://stiltsoft.com/blog/how-to-track-definition-of-done-in-jira-with-checklists/)
> 55. Context Switching: The Hidden Productivity Killer and How to Avoid It, [https://www.mindspacex.com/post/copy-of-context-switching-the-hidden-productivity-killer-how-to-avoid-it](https://www.mindspacex.com/post/copy-of-context-switching-the-hidden-productivity-killer-how-to-avoid-it)

## LLM Chief of Staff Protocol: ADHD Executive Function Prosthetics

Date: 26 August 2026

Scope: Task-authoring gate for Todoist, research into ADHD mechanisms and evidence-based mitigations, protocol rollout across Work project

Status: Live on FTFL-868, FTFL-619, FTFL-942; Argo task incomplete (needs Application name)

---

### I. The Problem: Why the Original System Failed

#### Surface Observation

Four tasks in the Todoist Work project (FTFL-868, FTFL-619, FTFL-942, ArgoCD) all used identical generic wrappers:

- "Check status of [ticket]—re-assess next steps."
- Empty description fields; all detail crammed into truncated titles
- One task broke mid-word ("…in the relev")
- All carried the `cos-sweep` label (automated sweep already running)

#### Root Issue: Non-Leaf-Node Tasks Disguised as Actions

<cite index="68-1">"Re-assess next steps" is not a physical action—it's asking you to redo executive-function work (deciding what to do) at the exact moment the task was supposed to have already done that for you.</cite> This creates overwhelm-by-non-leaf-node, automated.

The template violated GTD ontology: a Project wears a ticket number but gets treated as a Next Action. The brain collapses the pebble back into the implied project—shrinking the task doesn't move the resistance because the real work is still unbounded.

---

### II. ADHD Neuroscience: Three Independent Mechanisms

Research synthesised from clinical psychology, neuroscience, and organisational behaviour revealed three separate, independently-studied neural deficits, each with specific evidence-based countermeasures. These are not willpower problems.

#### Mechanism 1: Default Mode Network Failure and Task Paralysis

The neural architecture:

- In neurotypical individuals, the Task Positive Network (TPN) cleanly suppresses the Default Mode Network (DMN) during focused work.
- In ADHD, the DMN fails to deactivate appropriately during cognitive tasks, creating simultaneous activation of both networks.
- This "neurological cross-talk" leads to continuous internal noise: tangential thoughts, anxieties, associative thinking about project implications.

Why open-ended tickets cause paralysis:

When a Jira ticket lacks rigid, concrete, highly specified boundaries, the DMN remains hyperactive, generating implicit requirements and moving parts that rapidly overwhelm limited working memory. Instead of initiating, the system shuts down. Procrastination becomes a protective mechanism against cognitive overload.

The finding: This is not a comprehension failure or low motivation. It's a direct manifestation of specific neural network dysregulation.

#### Mechanism 2: Delay Discounting and Inability to Visualise Completion

The dopaminergic deficit:

ADHD is characterised by a hypodopaminergic state in the frontostriatal circuits and dorsolateral prefrontal cortex (DLPFC). The DLPFC is the command centre for holding future goals in working memory and directing behaviour toward them.

Delay discounting:

Because dopamine regulates reward anticipation and salience, individuals with ADHD exhibit steep delay discounting—the subjective value of a reward decreases precipitously the further away it is in time. An open-ended ticket represents a delayed, highly abstract reward (ticket to Done, deployment). Because the endpoint is not vividly represented in the DLPFC, the brain fails to generate dopaminergic momentum for task initiation.

The clinical reality: The worker knows exactly what needs to be done, has the technical skills, understands the consequences of failure. The executive dysfunction prevents translation of that macro-level knowledge into localized, sequential action in the present moment.

The finding: You cannot visualise completing the task—not because you haven't tried, but because the internal machinery that normally generates that image is under-resourced.

#### Mechanism 3: Attention Residue and Cognitive Inertia After Task Switching

Attention residue (Leroy, 2009):

<cite index="69-1">When switching tasks, a significant portion of cognitive processing remains involuntarily allocated to the previous task after a physical switch to a new one.</cite> This residue degrades performance, increases errors, diminishes decision-making, and causes cognitive fatigue on the subsequent task.

Residue is most pronounced when:

- A task is left incomplete (creating an open loop)
- The previous task involved deep cognitive engagement
- The interruption was self-initiated

The cost in knowledge work:

- <cite index="70-1">It takes an average of 23 minutes and 15 seconds to fully return to an original task after an interruption; workers switch to an average of 2.26 other tasks first before returning to the original.</cite>
- <cite index="71-1">Knowledge workers toggle between apps and websites approximately 1,200 times per day.</cite>
- <cite index="72-1">Up to 40% of productive time is lost to the mental cost of shifting between tasks.</cite>

ADHD amplification—cognitive inertia and hyperfocus:

For individuals with ADHD, set-shifting (the executive function responsible for unhooking attention from one task and locking it onto the next) is severely impaired due to compromised working memory and inhibitory control. Additionally, when ADHD brains enter hyperfocus as a compensatory mechanism to overcome baseline dopaminergic under-arousal, attention locks so tightly that shifting away requires massive mental reset. If you finish a complex task while hyperfocused and immediately open the next ticket without structured neurological transition, the residue from the first task clings to working memory like a background application draining RAM.

The finding: You cannot just switch to the next ticket because your brain requires an external closure signal. The brain's preference for reaching closure before disengagement is universal; your impaired set-shifting amplifies it.

---

### III. Evidence-Based Mitigations

#### Mitigation 1: Episodic Future Thinking (EFT)

What it does:

Episodic Future Thinking is a psychological intervention that reduces delay discounting by altering the perceived value of delayed outcomes. It involves mentally projecting oneself into the future to vividly imagine and experience a specific future-oriented event.

Clinical evidence:

- Engaging in EFT during the intention-formation phase (when reading a work ticket) significantly reduces delay discounting and improves prospective memory execution in adults with ADHD.
- EFT activates prefrontal-mediotemporal interactions, enhancing goal salience and bridging the temporal gap that causes task avoidance.
- Outcome-focused EFT (imagining the state of completion and reward) and process-focused EFT (imagining the steps required) are both effective; <cite index="63-1">recent clinical evaluation distinguishes that manipulating instructional focus during intention formation yields significant improvements in daily functioning.</cite>

In the protocol:

The "Done means" line in each task description provides externally-generated prospection, standing in for the self-generated version that's weaker in ADHD. Combined with the "Steps" field (process-focused variant), this is EFT built into the task architecture.

#### Mitigation 2: Implementation-Focused Cognitive Behavioral Therapy (CBT)

Why standard productivity advice fails:

<cite index="64-1">Standard productivity advice (use a planner, break tasks down) frequently fails ADHD brains because it relies on accurate time perception and reliable task initiation faculties that are neurologically compromised.</cite> The problem is not knowledge acquisition; it's implementation at the point of performance.

The CBT framework:

The therapeutic focus shifts entirely away from knowledge toward implementation and environmental engineering. The most effective intervention is granular, hyper-specific task breakdown into literal physical micro-actions, paired with written "behavioral prescriptions"—tangible reminders of the exact steps, anticipated barriers, and predetermined solutions.

In the protocol:

- The "Steps" field breaks the outcome into physical micro-actions in order.
- The "If stuck" field is a behavioral prescription: [specific likely blocker] → [specific pre-decided response]. This bypasses the decision point at the moment of maximum depletion.

#### Mitigation 3: The Ready-to-Resume Plan (Leroy & Glomb, 2018)

The mechanism:

<cite index="69-2">Writing down the exact, literal next physical action that will be taken when returning to a task, or formally acknowledging the exact state of the completed task, signals to the brain that the state is saved safely outside of working memory.</cite> This fulfils the psychological requirement for closure (the Zeigarnik effect), allowing the Default Mode Network to release the previous task and freeing up the impaired set-shifting mechanism to fully engage with the subsequent ticket.

Evidence:

<cite index="69-3">People who wrote that note were roughly 80% more likely to reach the right call afterward than people who switched cold.</cite>

In the protocol:

The "On stop, note here" field captures this: done/not done—blocker—next micro-step. This is written _before_ you start, so the exit criterion is already defined. During the session or when time runs out, you update the field to close the open loop.

---

### IV. The Task-Authoring Gate

A standalone next-action in Todoist must satisfy six fields for ADHD execution. The gate prevents non-leaf nodes from being dressed up as actions.

#### Field 1: Source Link (Jira/MR/Alert/Confluence)

Purpose: Remove the lookup step; jump straight to context.

Format: `[TICKET-NAME ↗](url)` at the start of description.

Validates that every task has a traceable source. If you can't link it, it's probably not actionable yet.

#### Field 2: Done Means (Outcome + Completion Signal)

Purpose: Combat delay discounting by making the finished state vivid and concrete.

Format: One sentence describing the tangible endpoint. Pull directly from acceptance criteria in the source ticket, never invented.

Example (FTFL-868):

> Done means: both TFC vars set, `terraform plan` runs clean against `fitapp_demo_ukw`. No apply needed for this task.

This is externally-generated prospection for the ADHD brain.

#### Field 3: Steps (Process-Focused EFT)

Purpose: Externalise the sequence so the working memory doesn't have to hold it.

Format: Numbered physical micro-actions, in order. 1–4 steps; if more than 4, the task isn't leaf-shaped.

Example (FTFL-868):

> 1. source/generate the admin password value 2) decide the firewall rule values 3) set both in the TFC workspace UI 4) trigger a plan, confirm clean.

This prevents the brain from "collapsing the pebble back into the project"—each step is named, not implied.

#### Field 4: If Stuck (Behavioral Prescription)

Purpose: Pre-decide the response to the most likely blocker, so depletion doesn't trigger re-planning.

Format: [specific likely blocker] → [specific pre-decided move]. One sentence.

Example (FTFL-868):

> If stuck: don't know the right IP range for `mysql_firewall_rules`? Default to your current IP only, note it as a follow-up—don't block the task on finding the 'correct' range.

This prevents decision fatigue at the moment of maximum cognitive depletion.

#### Field 5: Source Context (Injected Content)

Purpose: Eliminate context-switching cost; have the relevant detail already at hand.

Format: 2–3 sentences of pulled content from the source ticket: open items, dependencies, acceptance criteria, or last comment thread. Not a rewrite; direct extraction.

This trades a small increase in task description length for the removal of a context-lookup step mid-execution.

#### Field 6: On Stop (Ready-to-Resume and Attention Residue Flushing)

Purpose: Close the open loop and capture state for resumption; enable clean switching to the next ticket.

Format: A placeholder filled at session end or timeout: done/not done—what blocked you, if anything—exact next micro-step.

Example (placeholder):

> On stop, note here: done / not done—what blocked you, if anything—next micro-step.

This is written _before_ execution so the exit criterion is already clear. It's filled during or at the end of the session.

---

### V. Findings on Sources and Claims

#### Research Validated

- DMN/TPN interference: Plausible and consistent with published ADHD neuroimaging. Russell Ramsay's clinical interpretation holds.
- Delay discounting / dopaminergic reward: Corroborates Barkley's "temporal myopia" from a neuroscience angle.
- Episodic Future Thinking: Real research; processvs outcome-focused distinction is genuine upgrade to task design.
- Attention residue (Leroy, 2009): Foundational; ready-to-resume plan is the specific intervention from Leroy & Glomb (2018).
- Context switching cost (23 min recovery, 40% productivity loss): Extrapolated from Gloria Mark's UC Irvine research and Microsoft workforce studies; valid order of magnitude.

#### Claims Cut (Sources Unclear or Invented)

- "Crumb Protocol"—labelled as Leroy's work in the source document, but Leroy's own term for the intervention is simply the Ready-to-Resume Plan. The Capture/Close/Clear/Cue/Commit sequence is a productivity blog's own systematisation, not Leroy's published protocol. Do not use "Crumb Protocol" without verifying source.
- "$450 billion annually"—the figure is widely cited but has no single clean source. Appears in Loom, Atlassian, and various productivity blogs; Gallup and Microsoft studies are referenced but the exact figure is not independently verified by me. Valid as colour; not something to build a protocol claim on.

#### Gaps (Document Incomplete)

The source document cut off mid-word before the section "Risks of Cognitive Offloading and Learned Helplessness"—this is a real category worth having for a system this scaffolded (a risk of the AI offloading too much executive function and eroding capacity). The argument wasn't provided.

---

### VI. Implementation: Todoist Updates (26 August 2026)

#### Task 1: FTFL-868 (TFC Workspace Variables)

Original: "Check status of FTFL-868… re-assess next steps." (generic, non-actionable)

Updated:

| Field | Content |
|-------|---------|
| Title | FTFL-868: set the two unset TFC workspace vars (ff_demo_mysql_admin_password, mysql_firewall_rules) in fitapp_demo_ukw. |
| Done means | Both TFC vars set, `terraform plan` runs clean against `fitapp_demo_ukw`. No apply needed for this task. |
| Steps | 1) source/generate the admin password value 2) decide the firewall rule values 3) set both in the TFC workspace UI 4) trigger a plan, confirm clean. |
| If stuck | Don't know the right IP range for `mysql_firewall_rules`? Default to your current IP only, note it as a follow-up—don't block the task on finding the 'correct' range. |
| Source link | [FTFL-868 ↗](https://fitfile.atlassian.net/browse/FTFL-868) |
| Context | 6-step rebuild of ff-demo-mysql into new shared RG, restored from backup. Needs Jon Bradshaw sign-off before live apply. Still 'Selected for Development', no comments yet. |
| On stop | [Placeholder] done / not done—what blocked you, if anything—next micro-step. |

Why this works: The task is now startable. You can see the exact two variables, the acceptance signal (plan clean), the steps, and the pre-decided workaround if you hit the IP-range blocker. No re-planning at execution time.

---

#### Task 2: FTFL-619 (PostgreSQL HA Audit)

Original: "Check status of FTFL-619… re-assess next steps."

Key insight uncovered: Azure auto-migrates same-zone HA servers to zone-redundant from 1 September 2026—only 7 days out. The old wording buried this deadline entirely. Priority may need to escalate from P2.

Updated:

| Field | Content |
|-------|---------|
| Title | FTFL-619: 20 min—audit PostgreSQL Flexible Servers for same-zone HA (1 Sept deadline) |
| Done means | A list of every PostgreSQL Flexible Server in the two subscriptions that has same-zone HA set via Terraform/Bicep—even if the list is 'none found'. |
| Steps | 1) list Flexible Server instances in FITCloud Non-Production (`249df46b-f75d-4492-8e78-b33a00473548`) and Shared Services (`a085dd04-19aa-4d2b-9a35-e438097d84fc`) 2) for each, check if `zone`/`standby_availability_zone` are explicitly set in Terraform 3) note which ones, if any. |
| If stuck | Can't tell HA mode from the portal quickly? Grep the Terraform state/config for `standby_availability_zone` across both subscriptions' repos instead—faster than portal-hunting. |
| Source link | [FTFL-619 ↗](https://fitfile.atlassian.net/browse/FTFL-619) |
| Context | Azure auto-migrates same-zone-HA servers (created via Terraform/Bicep/SDK/PowerShell/Ansible) to zone-redundant HA from 1 Sept 2026—7 days out. Expect minor write-latency changes on migration. This audit decides whether anything needs self-service migration or a Terraform update before auto-migration. Full scope beyond this session: assess write-latency sensitivity per workload, decide self-service vs. auto-migrate, make the Terraform setting explicit. This task is just the audit. |
| On stop | [Placeholder] done / not done—servers found, if any—next micro-step. |

Why this works: The time-bound nature is now visible. The outcome (a list) is concrete. The pre-decided workaround (grep instead of portal-hunting) removes a potential blocker. The task is scoped to this session only—full prioritisation decisions are later.

---

#### Task 3: FTFL-942 (Trivy Metric Alerts)

Original: "Check status of FTFL-942… re-assess next steps."

Updated:

| Field | Content |
|-------|---------|
| Title | FTFL-942: 20 min—write Grafana alert for first Trivy condition (new Critical CVE) |
| Done means | One working metric-based Grafana alert rule for 'new Critical vulnerability appearing', added as a panel on the Vulnerabilities dashboard. |
| Steps | 1) find the Trivy metric reporting Critical CVE count/appearance 2) write the alert rule/query 3) add as a new panel on the Vulnerabilities dashboard 4) confirm it fires on a known/test case if possible. |
| If stuck | Unsure of the exact metric name? Check an existing (broken) log-based alert for the query pattern, or check FTFL-9002 for what's already diagnosed about the broken alerts—don't spend the session hunting metric names from scratch. |
| Source link | [FTFL-942 ↗](https://fitfile.atlassian.net/browse/FTFL-942) |
| Context | Only log-based alerts exist today and both are broken (FTFL-9002)—Trivy metrics currently drive zero notifications. Full scope is 4 conditions (new Critical, Critical count threshold, scan coverage drop, reports >24h stale)—this session is just the first, to prove the pattern before doing the other three. |
| On stop | [Placeholder] done / not done—alert working or not—next micro-step. |

Why this works: The scope is bounded to one condition, not all four. The blocked workaround (FTFL-9002) prevents a dead-end hunt. Success is binary (alert working or not), not abstract.

---

#### Task 4: ArgoCD Sync Timeout (INCOMPLETE)

Issue: The original task cut off mid-word ("…in the relev") and never named which Application or ConfigMap the timeout applies to.

Updated:

| Field | Content |
|-------|---------|
| Title | ArgoCD: reset sync timeout to 5m—confirm which Application first |
| Done means | Sync timeout set to 5m in the correct place, confirmed against a real sync. |
| If stuck (this is the blocker) | Most likely locations by ArgoCD convention: either `spec.syncPolicy` on the specific Application manifest, or the global `timeout.reconciliation` setting in `argocd-cmd-params-cm`. Check whichever GitOps repo owns the Application in question first. These are general candidates to check, not confirmed for your setup. |
| On stop | [Placeholder] which Application/config it turned out to be—done / not done—next micro-step. |

Status: This task needs you to name the Application. Once you do, the remaining fields will be filled in. Right now it's startable only if you already know which one; if you don't, it's a blocker masquerading as a task.

---

### VII. Lessons Learned: Why the Gate Works

#### The Distinction: Template vs. Diagnosis

- Wrong: "Make tasks smaller." (Doesn't work for ADHD because shrinking doesn't remove the implied project.)
- Right: "Make tasks atomic and externally-scaffolded." (Addresses the mechanism: DMN noise, delay discounting, attention residue.)

The gate doesn't try to fix ADHD. It builds a prosthetic executive function by externalising the cognitive work the brain can't reliably do internally: prospection, sequencing, blocker-planning, closure signalling.

#### The Hidden Cost of Generic Templates

A one-size-all template like "check status—re-assess" doesn't scale:

- It works for trivial status checks (a Slack ping).
- It breaks for ambiguous Jiras (what does "status" even mean?).
- It breaks catastrophically for ADHD brains, where re-assessment _is_ the hard part, not the easy part.

Each task's blocker and outcome are different. The template must be custom-fitted to the ticket, not stamped uniformly.

#### Why Sources and Injection Matter

- A task with an empty description that just points back to Jira adds a lookup step, not removing one.
- A task with injected content (pulled from the ticket) trades a bit of description length for context-switching cost—a net win.
- The source link makes the task recoverable if Todoist is down or the system resets.

---

### VIII. What's Different Now

#### Before

- Generic wrapper: "Check status—re-assess next steps."
- No Done-means; no Steps; no If-stuck; no Context; no On-stop.
- Task paralysis because the brain can't visualise the endpoint.
- Attention residue because there's no closure signal.
- Context-switching cost because there's no injected context.

#### After

- Specific action, linked to source, with concrete outcome.
- Done-means addresses delay discounting (prospection).
- Steps address DMN noise (bounded, physical sequence).
- If-stuck addresses decision fatigue (pre-decided response).
- Context addresses context-switching cost (injected detail).
- On-stop addresses attention residue (closure signal).
- All six fields are written before execution, so the exit criterion is clear from the start.

#### The Mechanism

This is not "tasks are smaller now." This is "the executive-function work is externalized now." The cognitive load shifts from your working memory (which is under-resourced) to the task architecture (which is persistent).

---

### IX. Next Steps

#### Immediate

1. Clarify the Argo task: Tell the LLM which Application/AppProject the sync timeout applies to. This will complete the fourth task.
2. Test one task this week: Execute FTFL-868 (or whichever feels most startable) using the six-field gate. Report back: Did it pull you in more than the old version? Did the "If stuck" blocker occur?

#### Consolidation

1. Establish the gate as the standard: Any future cos-sweep task that lands in Todoist must satisfy all six fields. If a field can't be filled, the ticket isn't ready yet; it goes back to Jira for clarification.
2. Monitor the On-stop field: Collect these over 2–3 weeks to identify which blockers recur. If the same "If stuck" scenario hits multiple tasks, it's a systemic blocker, not an individual task issue.

#### Expansion (After Gate Holds)

1. Bridge GitLab and Grafana: Once the Jira gate is reliable for a week, wire GitLab MR reviews and Grafana alerts into the same gate. Don't expand sources until the template is proven on a single source.
2. Obsidian-Todoist bridge: The Advanced URI plugin behind your bridge is the same deep-link mechanism as the FTFL-XXX links. Once the gate is stable, connect Obsidian project notes to Todoist via the bridge plugin using the same six-field structure.

#### Structural

1. Revisit priority weighting: FTFL-619 has a hard deadline 7 days out but is marked P2. Re-weight based on deadline visibility, not just business priority.
2. Decision on alarms: Confirm whether the LLM should set real (OS-level) alarms when bounded sessions start, or whether you're managing that yourself. This is a standing behaviour change.

---

### X. Caveats and Risks

#### Research Integrity

- The Crumb Protocol label is not Leroy's; don't cite it as such.
- The $450B figure is real in the sense that it's cited everywhere, but it has no single traceable source.
- Implementation-Focused CBT and EFT are real; ADHD-specific studies on them exist, but the application to Todoist task design is my extrapolation, not a published methodology.

#### Risk of Cognitive Offloading

The gate externalises executive function deliberately. If it works too well, there's a risk of learned helplessness—over-reliance on the external scaffolding without rebuilding internal capacity. This is why the "On-stop" field asks you to capture what you did, not just whether you did it. Reviewing those notes regularly will reveal patterns and build metacognitive awareness.

The document that was cut off in the research ("Risks of Cognitive Offloading and Learned Helplessness") likely addresses this. Worth finding the full version.

#### Incomplete Rollout

- Only four tasks updated. The gate needs to prove itself on active execution before expanding.
- GitLab, Grafana, and Obsidian integration are aspirational, not yet live.
- No standing alarm mechanism yet (question still open).

---

### XI. References and Sources

ADHD Neuroscience and Executive Function:

- Russell Ramsay (clinical psychology, adult ADHD, implementation deficits)
- Russell Barkley (ADHD as self-regulation deficit, temporality, external scaffolding)
- fMRI studies on Default Mode Network/Task Positive Network dysregulation in ADHD

Attention Residue and Task Switching:

- Sophie Leroy, "Why Is It So Hard to Do My Work?" (2009), Organizational Behavior and Human Decision Processes
- Leroy & Glomb, "Ready-to-Resume Plan" intervention (2018)
- Gloria Mark, UC Irvine (context switching recovery time: 23m 15s; task switching frequency)

Episodic Future Thinking:

- Clinical psychology literature on EFT for ADHD and delay discounting
- Process-focused vs. outcome-focused EFT distinctions

Productivity and Knowledge Work:

- Atlassian, Loom, Gallup studies on context switching costs (global economy estimate: $450B annually; knowledge workers: 40% productivity loss, 1,200 app toggles/day)

---

### XII. Vault Integration

File location: `/Volumes/DAL/Zettelkasten/LLMeon/cos-prodOS-protocol-august-2026.md`

Related notes:

- `gtd-action-system.md`—canonical GTD reference (Projects, Outcomes, Sequences, Next Actions, Starter Tasks)
- `ADHD.md`—personal ADHD profile and compensatory strategies (if it exists; consider creating)
- `todoist-config.md`—current Todoist structure (six-project runway, nine-label stack, filters)
- `obsidian-todoist-bridge.md`—Advanced URI plugin setup and bidirectional link strategy

Backlinks:

- FTFL-868, FTFL-619, FTFL-942, ArgoCD timeout (specific tasks embodying this protocol)
- cos-sweep (automated sweep label; check periodically whether new tasks satisfy the gate)

Status tags for future review:

- `#protocol/live`—Gate is live on FTFL-868, tested/live on 619, 942
- `#protocol/incomplete`—ArgoCD task needs Application name
- `#research/neuroscience`—ADHD mechanisms and evidence synthesis
- `#system/escalate`—FTFL-619 deadline (1 Sept 2026) may need priority review

---

Document prepared: 26 August 2026, 18:00 UTC

Author: Claude (Chief of Staff, LLM-based)

Confidence level: High on protocol design, medium on research synthesis, low on unpublished claims (Crumb Protocol, $450B source)

### New Chat

You

Develop a plan for an LLM chief of staff to act as a executive function prosthetic

---

Gemini

The difficulty you experience in transitioning between tasks or visualising completion is not a failure of willpower; it is a neurological bottleneck. In neuro-variable profiles, the toggle switch between the Default Mode Network (DMN)—responsible for internal noise—and the Task Positive Network (TPN)—active during focused execution—is structurally faulty. When you stare at an open-ended ticket, both networks attempt to fire simultaneously, creating severe cognitive resistance and task paralysis.

To externalise your executive function entirely, we must update the architecture of PKM ProdOS. The Chief of Staff (CoS) must transition from a passive task aggregator into an active, conversational "Constraint Guardian".

#### Upgrading the CoS Protocol in PKM ProdOS

To mitigate the knowing-doing gap and help you cleanly close out tasks, your CoS needs to enforce a rigid, step-by-step protocol:

- The "Definition of Done" Gatekeeper: Before you begin execution, the CoS must mandate absolute clarity. Much like applying a Card Forcing Function to distil complex thoughts into a constrained space, the CoS should prompt you to articulate the exact, physical end-state of the ticket. If you cannot describe what the finished product looks like, the CoS does not let you start.
	PDF
- Spatial Offloading: Broad tickets cause cognitive overload because short-term working memory is a poor storage engine. Instead of holding the steps in your head, the CoS should prompt you to map the ticket visually. Just as physically tracing a labyrinth offloads the mental burden of remembering the entire maze, mapping the ticket spatially frees up your processing bandwidth.
	PDF
- Micro-Sequencing: The CoS must automatically break the ticket down into "starter tasks" requiring less than five minutes of activation energy. This leverages the "motion creates motivation" principle to bypass initiation paralysis.
	MD+ 1
- The Somatic Switch Protocol: To break the lingering inertia of a completed task and transition to the next, the CoS must prescribe a somatic and mechanical initiation trigger. By prompting you to execute a brief, unrelated physical movement, the system forces the TPN online and cleanly severs the previous cognitive loop.

#### Executing the Hand-Off

When a task is done, the biological mind often struggles to let go of the mental residue. Your CoS should initiate an active "shut-down" routine for that specific ticket, updating your external architecture and sweeping away the open loop so your analytical mind can safely detach.

What specific conversational command would you like the CoS to use when challenging you to define the precise, visual end-state of a new ticket before you begin?

---

You

Yeh me about time blocking and the boxing and how the cos can use it to help me finish and switch

---

Gemini

Time blocking and time boxing are often treated as the same concept, but for a neuro-variable brain, the distinction is the difference between execution and chronic overwhelm.

Time _blocking_ is simply reserving space on a calendar (e.g., "I will review Kubernetes clusters from 10:00 to 11:00"). Time _boxing_, however, is an unyielding constraint: you allocate fixed, unyielding time blocks to specific activities. When the timer rings, the work stops, regardless of completion.

By enforcing a hard stop, timeboxing caps perfectionism. It replaces the anxiety-inducing, open-ended question of _"Will I finish this perfectly?"_ with the bounded constraint of _"What can I realistically execute within this 45-minute block?"_. This visualises hidden work-in-progress and exposes time theft.

Here is how you can program your Chief of Staff (CoS) to govern this process and act as your prosthetic executive function:

#### 1\. The Pre-Flight Negotiation

Before you pull a task from your Obsidian-Todoist infrastructure, the CoS must negotiate the boundaries of the box.

- The Constraint Prompt: If you need to update a Helm chart or configure a Grafana observability pipeline, the CoS should ask: "You have 30 minutes. What is the exact, visualisable output you can deliver in this box?"
- Scope Reduction: If your answer is too broad, the CoS rejects it and forces you to slice the task smaller until it fits the allocated time.
- Energy Matching: The CoS should align the box duration—typically 15-30 minute blocks—with your current energy levels.
	MD

#### 2\. Environmental Containment

During the execution phase, the CoS acts as a barrier against scope creep.

- Focus Lock: The CoS reminds you that you are not solving the whole project; you are only executing the agreed-upon slice.

#### 3\. The Hard Stop and Somatic Switch

This is where the CoS mitigates the switching cost and cleanly closes the open loop.

- The Guillotine: When time is up, the CoS mandates a hard stop.
- State Capture: The CoS asks you to log one quick sentence on what the _next_ action is, safely parking the remaining work back into your external system so your brain can let it go.
- Somatic Initiation: To break the lingering cognitive inertia, the CoS deploys a somatic and mechanical initiation trigger. It prompts you to execute a brief, unrelated physical movement—like a balancing exercise—to force the Task Positive Network (TPN) online and sever the previous thought loop.

To operationalise this within ProdOS, how strictly do you want the CoS to enforce the "Hard Stop"—should it simply require a verbal confirmation that you have stepped away, or do you need a more rigid mechanism?
