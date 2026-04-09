---
created: 2026-04-08T14:38:46+00:00
modified: 2026-04-09T10:01:45+00:00
title: I want to create a mathematical model of team unde
---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## I want to Create a Mathematical Model of Team Understanding. I Have Noticed that People Have Different Ideas and Understanding about Complex Topics and Sometimes even Combined there is no Whole Picture. But because of Cognitive Biases and Certainty Groups Think They Understand a Problem. So Each Person Has a Set of Knowledge that Creates an Amount of Understanding of a Topic. Combining All the Sets via Communication line Talking or Documenting Creates a Bigger Understanding. What Would a Maths Model of This Look like

A mathematical model of team understanding can be framed using set theory and information aggregation, accounting for cognitive biases that distort perceived collective knowledge. Each team member possesses a distinct knowledge set, and communicating or documenting enables these sets to overlap and expand—though not always to a complete whole, especially in the presence of bias and miscalibration.

### Core Model Structure

- Individual knowledge can be represented as sets: \$ K_1, K_2, ···, K_n \$ for a team of \$ n \$ people.[^1][^2]
- The union \$ K_{team} = K_1 \cup K_2 \cup ··· \cup K_n \$ depicts the total pool of knowledge available if all information is perfectly shared.
- Real understanding is less than this union due to incomplete communication, documentation gaps, and biases (e.g., Dunning-Kruger effect, overconfidence).[^1][^3]

### Aggregation With Biases

- Each person's perceived certainty can be modeled by a weight \$ w_i \$ that scales their input, determined by confidence rather than their actual expertise.[^1]
- Overall team understanding: \$ U_{team} = \bigcup_{i=1}^n w_i \cdot K_i \$
- When biases are present, \$ w_i \$ may not reflect true contribution, leading to a distorted collective picture.[^3]
- Models such as confidence-weighted voting, competence-weighted aggregation, and plurality voting are used, though confidence-weighted approaches are often less accurate due to self-assessment errors.[^1][^3]

### Communication \& Documentation

- Communication acts as edges in a graph, connecting knowledge sets:
    - Member-to-member transfer expands overlap.
    - Documentation creates shared external nodes, accessible to all, increasing global coverage.[^4][^5]
- Imperfect transmission can be modeled as a subgraph or partial union, constraining effective team understanding.

### Cognitive Bias Impact

- Cognitive biases—such as overconfidence—can be captured mathematically by error terms \$ \epsilon_i \$ in individual knowledge estimates.
- Aggregate knowledge is then \$ K'_{team} = K_{team} + \sum_{i=1}^n \epsilon_i \$, often leading to misunderstanding or illusion of complete coverage.[^1][^3]

### Example Equation

$$
U_{actual} = \left( \bigcup_{i=1}^n K_i \right) - \text{loss}_{\text{comm}} + \text{bias}_{\text{overlap}}
$$

Where:

- \$ loss_{comm} \$: loss due to incomplete sharing/documenting.
- \$ bias_{overlap} \$: error introduced by overconfidence, groupthink, and false consensus.[^1]

### Relevant Models

- Shared Mental Model (SMM): focuses on the intersection of knowledge sets where team members have common understanding.[^2][^6]
- Transactive Memory System (TMS): tracks which member knows what, enhancing team recall through distributed memory.[^2]
- SECI Model: cycles of sharing, externalizing, combining, and internalizing knowledge in teams.[^4]

### Concrete Modeling Approaches

- Mathematical dynamical systems: Team understanding can be modeled as a set that evolves based on communication "events" and update rules, possibly using differential or recurrence equations.[^7][^8]
- Cognitive map aggregation: Individual knowledge graphs are merged, with mathematical procedures to minimize analyst bias in combination.[^9]
- Bias modeling: Confidence scores and self-selection can be coded as variables in collective decision simulations. Overconfidence can reduce true aggregate understanding.[^1][^3]

This foundational set-based approach, enriched with weights and bias/error terms, gives you a concrete mathematical framework for modeling team understanding and the impact of cognitive biases on collective knowledge[^1].[^3][^2][^4][^7]

<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20]</span>

<div align="center">⁂</div>

[^1]: <https://www.sciencedirect.com/science/article/abs/pii/S138904171830158X>
[^2]: <https://www.sciencedirect.com/science/article/pii/S0001691825007164>
[^3]: <https://benjamin-enke.com/pdf/Confidence_aggregate.pdf>
[^4]: <https://slite.com/en/learn/knowledge-management-frameworks>
[^5]: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9659728/>
[^6]: <https://www.tandfonline.com/doi/full/10.1080/1463922X.2022.2061080>
[^7]: <https://pubmed.ncbi.nlm.nih.gov/28744231/>
[^8]: <https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01053/full>
[^9]: <https://www.emerald.com/k/article/45/4/589/272609/Aggregation-cognitive-maps-procedure-for-group>
[^10]: <https://pressbooks.bccampus.ca/technicalwriting/chapter/understandingteamdynamics/>
[^11]: <https://ceur-ws.org/Vol-2917/paper5.pdf>
[^12]: <https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1096>\&context=studentpub_uht
[^13]: <https://www.glassfrog.com/blog-post/6-steps-to-build-a-collective-intelligence-framework-for-smarter-decision-making>
[^14]: <https://pubsonline.informs.org/doi/10.1287/mnsc.1040.0247>
[^15]: <https://www.mindtheproduct.com/how-to-tap-into-the-collective-wisdom-of-a-team/>
[^16]: <https://www.tandfonline.com/doi/full/10.1080/00031305.2018.1518265>
[^17]: <https://pmc.ncbi.nlm.nih.gov/articles/PMC11627530/>
[^18]: <https://arxiv.org/html/2511.01558v1>
[^19]: <https://www.sciencedirect.com/science/article/pii/S0148296323000863>
[^20]: <https://journals.sagepub.com/doi/10.1177/1534484310371449>
