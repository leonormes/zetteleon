<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# I want to create a mathematical model of team understanding. I have noticed that people have different ideas and understanding about complex topics and sometimes even combined there is no whole picture. But because of cognitive biases and certainty groups think they understand a problem. So each person has a set of knowledge that creates an amount of understanding of a topic. Combining all the sets via communication line talking or documenting creates a bigger understanding. What would a maths model of this look like

A mathematical model of team understanding can be framed using set theory and information aggregation, accounting for cognitive biases that distort perceived collective knowledge. Each team member possesses a distinct knowledge set, and communicating or documenting enables these sets to overlap and expand—though not always to a complete whole, especially in the presence of bias and miscalibration.

### Core Model Structure

- Individual knowledge can be represented as sets: \$ K_1, K_2, ···, K_n \$ for a team of \$ n \$ people[^1_1][^1_2].
- The union \$ K_{team} = K_1 \cup K_2 \cup ··· \cup K_n \$ depicts the total pool of knowledge available if all information is perfectly shared.
- Real understanding is less than this union due to incomplete communication, documentation gaps, and biases (e.g., Dunning-Kruger effect, overconfidence)[^1_1][^1_3].


### Aggregation With Biases

- Each person's perceived certainty can be modeled by a weight \$ w_i \$ that scales their input, determined by confidence rather than their actual expertise[^1_1].
- Overall team understanding: \$ U_{team} = \bigcup_{i=1}^n w_i \cdot K_i \$
- When biases are present, \$ w_i \$ may not reflect true contribution, leading to a distorted collective picture[^1_3].
- Models such as confidence-weighted voting, competence-weighted aggregation, and plurality voting are used, though confidence-weighted approaches are often less accurate due to self-assessment errors[^1_1][^1_3].


### Communication \& Documentation

- Communication acts as edges in a graph, connecting knowledge sets:
    - Member-to-member transfer expands overlap.
    - Documentation creates shared external nodes, accessible to all, increasing global coverage[^1_4][^1_5].
- Imperfect transmission can be modeled as a subgraph or partial union, constraining effective team understanding.


### Cognitive Bias Impact

- Cognitive biases—such as overconfidence—can be captured mathematically by error terms \$ \epsilon_i \$ in individual knowledge estimates.
- Aggregate knowledge is then \$ K'_{team} = K_{team} + \sum_{i=1}^n \epsilon_i \$, often leading to misunderstanding or illusion of complete coverage[^1_1][^1_3].


### Example Equation

$$
U_{actual} = \left( \bigcup_{i=1}^n K_i \right) - \text{loss}_{\text{comm}} + \text{bias}_{\text{overlap}}
$$

Where:

- \$ loss_{comm} \$: loss due to incomplete sharing/documenting.
- \$ bias_{overlap} \$: error introduced by overconfidence, groupthink, and false consensus[^1_1].


### Relevant Models

- Shared Mental Model (SMM): focuses on the intersection of knowledge sets where team members have common understanding[^1_2][^1_6].
- Transactive Memory System (TMS): tracks which member knows what, enhancing team recall through distributed memory[^1_2].
- SECI Model: cycles of sharing, externalizing, combining, and internalizing knowledge in teams[^1_4].


### Concrete Modeling Approaches

- Mathematical dynamical systems: Team understanding can be modeled as a set that evolves based on communication "events" and update rules, possibly using differential or recurrence equations[^1_7][^1_8].
- Cognitive map aggregation: Individual knowledge graphs are merged, with mathematical procedures to minimize analyst bias in combination[^1_9].
- Bias modeling: Confidence scores and self-selection can be coded as variables in collective decision simulations. Overconfidence can reduce true aggregate understanding[^1_1][^1_3].

***

This foundational set-based approach, enriched with weights and bias/error terms, gives you a concrete mathematical framework for modeling team understanding and the impact of cognitive biases on collective knowledge[^1_1][^1_3][^1_2][^1_4][^1_7].
<span style="display:none">[^1_10][^1_11][^1_12][^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_19][^1_20]</span>

<div align="center">⁂</div>

[^1_1]: https://www.sciencedirect.com/science/article/abs/pii/S138904171830158X

[^1_2]: https://www.sciencedirect.com/science/article/pii/S0001691825007164

[^1_3]: https://benjamin-enke.com/pdf/Confidence_aggregate.pdf

[^1_4]: https://slite.com/en/learn/knowledge-management-frameworks

[^1_5]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9659728/

[^1_6]: https://www.tandfonline.com/doi/full/10.1080/1463922X.2022.2061080

[^1_7]: https://pubmed.ncbi.nlm.nih.gov/28744231/

[^1_8]: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01053/full

[^1_9]: https://www.emerald.com/k/article/45/4/589/272609/Aggregation-cognitive-maps-procedure-for-group

[^1_10]: https://pressbooks.bccampus.ca/technicalwriting/chapter/understandingteamdynamics/

[^1_11]: https://ceur-ws.org/Vol-2917/paper5.pdf

[^1_12]: https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1096\&context=studentpub_uht

[^1_13]: https://www.glassfrog.com/blog-post/6-steps-to-build-a-collective-intelligence-framework-for-smarter-decision-making

[^1_14]: https://pubsonline.informs.org/doi/10.1287/mnsc.1040.0247

[^1_15]: https://www.mindtheproduct.com/how-to-tap-into-the-collective-wisdom-of-a-team/

[^1_16]: https://www.tandfonline.com/doi/full/10.1080/00031305.2018.1518265

[^1_17]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11627530/

[^1_18]: https://arxiv.org/html/2511.01558v1

[^1_19]: https://www.sciencedirect.com/science/article/pii/S0148296323000863

[^1_20]: https://journals.sagepub.com/doi/10.1177/1534484310371449

