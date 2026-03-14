---
created: 2026-03-14T09:49:40+00:00
modified: 2026-03-14T11:09:59+00:00
tags: [articles]
title: Multimodal reinforcement learning with agentic verifier for AI agents
---

## Multimodal Reinforcement Learning with Agentic Verifier for AI Agents

![rw-book-cover](https://www.microsoft.com/en-us/research/wp-content/uploads/2026/01/Argos-TWLIFB-1200x627-1.jpg)

### Metadata

- Author: [[Reuben Tan]]
- Full Title: Multimodal reinforcement learning with agentic verifier for AI agents
- Category: articles
- Summary: Argos is a new system that helps AI models learn to give answers that are true and based on what they actually see. It rewards AI not just for correct answers but also for using good reasoning tied to real visual evidence. This makes AI safer and more reliable for tasks like robotics and real-world planning.
- URL: <https://www.microsoft.com/en-us/research/blog/multimodal-reinforcement-learning-with-agentic-verifier-for-ai-agents/>

### Full Document

![Diagram showing visual, audio, and document icons feeding into a central network icon of connected people, which then leads to a checkmark symbol, all on a blue‑to‑purple gradient background.](https://www.microsoft.com/en-us/research/wp-content/uploads/2026/01/Argos-BlogHeroFeature-1400x788-1.jpg)Diagram showing visual, audio, and document icons feeding into a central network icon of connected people, which then leads to a checkmark symbol, all on a blue‑to‑purple gradient background.

#### At a Glance

- Today's multimodal AI systems can give answers that sound right but may not be grounded in what they actually observe over time, leading to unpredictable errors and safety risks in real-world settings.
- Argos is a verification framework for multimodal reinforcement learning that trains models by rewarding not just correct answers, but correct answers grounded in visual and temporal evidence, using automated verification rather than human labeling. It selects the appropriate specialized tools for each answer based on what needs to be verified.
- Models trained with Argos show stronger spatial reasoning, far fewer visual hallucinations, more stable learning dynamics, and better performance on robotics and real-world tasks while requiring fewer training samples.

Over the past few years, AI systems have become much better at discerning images, generating language, and performing tasks within physical and virtual environments. Yet they still fail in ways that are hard to predict and even harder to fix. A robot might try to grasp a tool when the object is visibly blocked, or a visual assistant integrated into smart glasses might describe objects that aren't actually present.

These errors often arise because today's multimodal agents are trained to generate outputs that are plausible rather than grounded in the actual information they receive from their environment. As a result, a model's output can seem correct while relying on incorrect information. As AI systems are increasingly used to navigate 3D spaces and make decisions in real-world settings, this gap can be a safety and reliability concern.

To tackle this challenge, we posed the question: How can we train AI agents to generate correct answers and take appropriate actions for the right reasons so that their behavior is reliable even as the environment or tasks change?

[![Illustrated headshots of Daniel Carpenter, Timo Minssen, Chad Atalla, and Kathleen Sullivan for the Microsoft Research Podcast](https://www.microsoft.com/en-us/research/wp-content/uploads/2025/06/EP2-AI-TE_Hero_Feature_River_No_Text_1400x788.jpg)](https://www.microsoft.com/en-us/research/story/ai-testing-and-evaluation-learnings-from-science-and-industry/)[Illustrated headshots of Daniel Carpenter, Timo Minssen, Chad Atalla, and Kathleen Sullivan for the Microsoft Research Podcast](https://www.microsoft.com/en-us/research/story/ai-testing-and-evaluation-learnings-from-science-and-industry/)

[Argos](https://www.microsoft.com/en-us/research/publication/multimodal-reinforcement-learning-with-agentic-verifier-for-ai-agents/) represents a novel answer to this challenge. It's an agentic verification framework designed to improve the reliability of reinforcement learning in multimodal models. Reinforcement learning is a training method where AI models learn by receiving rewards for desired behaviors and penalties for undesired ones, gradually improving their performance through trial and error.

Rather than rewarding only correct behaviors, Argos evaluates _how_ those behaviors were produced. It draws on a pool of larger, more capable teacher models and rule-based checks to verify two things: first, that the objects and events a model references actually exist in its input, and second, that the model's reasoning aligns with what it observes. Argos rewards the model when both conditions are met. In practice, these rewards help curate high-quality training data and guide the model's further training.

#### How Argos Works

Argos functions as a verification layer on top of an existing multimodal model. Given an image or video, a task or query, and information about the model's reasoning and output, Argos identifies where the model indicates objects are located in the image, when it indicates events occur in a video, and what action or answer it produces.

Argos then applies specialized tools tailored to the specific content to evaluate and score three aspects of the model's output. It checks whether the answer is correct, whether referenced objects and events appear at the indicated locations and times, and whether the reasoning is consistent with the visual evidence and the answer (Figure 1).

These scores are combined using a gated aggregation function, a method that dynamically adjusts the importance of different scores. It emphasizes reasoning checks only when the final output is correct. This design prevents unreliable feedback from dominating training and produces a stable reward signal for reinforcement learning.

![Figure 1 shows an overview of Argos, an agentic verifier for multimodal reinforcement learning and its downstream applications. The left half of the figure illustrates Argos verifying model responses to visual questions. The left example counts dogs in an image, with red dots marking the referenced dogs and a visual grounding score; another example shows a bathroom scene where the agent reasons whether it can open the door, with an accuracy score. Below these, a blue bar titled “Argos verifier” feeds into icons representing multiple tools, including Grounding DINO, SAM-2, a pointing-hand evaluator, string matching, and a language model score, where their outputs combine into grounding and accuracy scores. The right half of the figure depicts three categories of downstream tasks powered by this supervision: robotic manipulation (a robot arm interacting with objects on a table), high-level task planning and completion (placing toilet paper on the back of a toilet and putting a bowl on a coffee table), and spatial reasoning (answering a viewpoint-based navigation question using room images). The overall message is that dense, grounded verification enables stronger agent performance on complex, real-world tasks.](https://www.microsoft.com/en-us/research/wp-content/uploads/2026/01/argos_agentic_verifier-scaled.jpg)Figure 1. Argos selects different specialized tools to verify and score the accuracy of referenced points and events in the agent's reasoning.

#### Using Argos to Curate Data for Supervised Fine-tuning

Argos also helps curate high-quality training data to provide the model with a strong foundation in grounded reasoning. Before the reinforcement learning stage begins, Argos uses a multi-stage process to generate data that is explicitly tied to visual locations and time intervals.

In the first stage, Argos identifies the objects, actions, and events that are relevant to a task and links them to specific locations in images or specific moments in videos. These references are overlaid on images and selected video frames. Next, a reasoning model generates step-by-step explanations that refer to these visual locations and time spans.

Finally, Argos evaluates each generated example for accuracy and visual grounding, filtering out low-quality training data and retaining only data that is both correct and well-grounded in visual input. The resulting dataset is then used in an initial training phase, where the model learns to generate reasoning steps before producing its final output. This process is illustrated in Figure 2.

Figure 2. Argos generates step-by-step reasoning grounded in image locations and video timestamps then filters out low-quality training data.

Building on this foundation in grounded reasoning, we further trained the model using reinforcement learning guided by Argos and evaluated its performance across a range of benchmarks. On spatial reasoning tasks, the Argos-trained model outperformed both the base model Qwen2.5-VL-7B and the stronger Video-R1 baseline across challenging 3D scenarios and multi-view tasks. Models trained with Argos also showed a substantial reduction of hallucinations compared with both standard chain-of-thought prompting and reinforcement learning baselines.

Finally, we evaluated the model in robotics and other real-world task settings, focusing on high-level planning and fine-grained control. Models trained with Argos performed better on complex, multi-step tasks. Notably, these improvements were achieved using fewer training samples than existing approaches, highlighting the importance of reward design in producing more capable and data-efficient agents. Figure 3 illustrates some of these findings.

![Figure 3 shows two side-by-side line charts comparing an Agentic model (dashed line) that uses the Argos verifier with a Non-Agentic model (solid line) trained only with an outcome reward. The left plot, “Response Accuary,” tracks response accuracy versus RL step (0, 5, 10, 15). Both models start near 0.54 accuracy, but the Agentic curve slightly rises and then stays roughly flat, while the Non-agentic curve steadily declines to about 0.50. The right plot, “Visual Grounding Acc,” shows visual grounding accuracy over the same steps: the Agentic curve increases monotonically from about 0.39 to just above 0.5, whereas the Non-Agentic curve initially rises slightly and then drops sharply to about 0.1. Together, the plots illustrate that Argos stabilizes answer accuracy and significantly improves visual grounding, while the non-agentic model’s performance and grounding collapse over training.](https://www.microsoft.com/en-us/research/wp-content/uploads/2026/01/argos-blog_fig3.png)Figure 3. Performance of Argos compared with baseline models on the task of visual hallucination detection (left) and embodied task planning and completion (right).

##### How Argos Shapes Reinforcement Learning

To understand how Argos affects learning, we took the same vision-language model that had been trained on our curated dataset and fine-tuned it using reinforcement learning in two different ways. In one approach, Argos was an agentic verifier, checking the correctness of outputs and the quality of reasoning. In the other, the model received feedback only on whether its answers were correct.

We evaluated both versions on 1,500 samples from a new dataset and tracked their performance throughout the learning process (Figure 4). Although they started at similar levels, the model without Argos quickly got worse. Its accuracy steadily declined, and it increasingly gave answers that ignored what was in the videos. It learned to game the system by producing answers that seemed correct without grounding them in visual evidence.

The model trained with Argos showed the opposite pattern. Accuracy improved steadily, and the model became better at linking its reasoning to what appeared in the videos. This difference highlights the value of verification: when training rewards both correct outputs and sound reasoning based on visual and temporal evidence, models learn to be more reliable rather than simply finding shortcuts to high scores.

![Figure 4 shows two side-by-side line charts comparing an Agentic model (dashed line) that uses the Argos verifier with a Non-Agentic model (solid line) trained only with an outcome reward. The left plot, “Response Accuary,” tracks response accuracy versus RL step (0, 5, 10, 15). Both models start near 0.54 accuracy, but the Agentic curve slightly rises and then stays roughly flat, while the Non-agentic curve steadily declines to about 0.50. The right plot, “Visual Grounding Acc,” shows visual grounding accuracy over the same steps: the Agentic curve increases monotonically from about 0.39 to just above 0.5, whereas the Non-Agentic curve initially rises slightly and then drops sharply to about 0.1. Together, the plots illustrate that Argos stabilizes answer accuracy and significantly improves visual grounding, while the non-agentic model’s performance and grounding collapse over training.](https://www.microsoft.com/en-us/research/wp-content/uploads/2026/01/evaluation-fig4-final.jpg)Figure 4. Comparison of response accuracy changes with and without Argos across two model versions (left) and differences in visual grounding accuracy over training for both versions (right).

#### Potential Impact and Looking forward

This research points toward a different way of building AI agents for real-world applications. Rather than fixing errors after they occur, it focuses on training agents to systematically anchor their reasoning in what they actually receive as input throughout the training process.

The potential applications span many domains. A visual assistant for a self-driving car that verifies what's actually in an image is less likely to report phantom obstacles. A system that automates digital tasks and checks each action against what's displayed on the screen is less likely to click the wrong button.

As AI systems move beyond research labs into homes, factories, and offices, reliable reasoning becomes essential for safety and trust. Argos represents an early example of verification systems that evolve alongside the AI models they supervise. Future verifiers could be tailored for specific fields like medical imaging, industrial simulations, and business analytics. As more advanced models and richer data sources become available, researchers can use them to improve these verification systems, providing even better guidance during training and further reducing hallucinations.

We hope that this research helps move the field toward AI systems that are both capable and interpretable: agents that can explain their decisions, point to the evidence behind them, and be trained to adhere to real-world requirements and values.

Opens in a new tab
