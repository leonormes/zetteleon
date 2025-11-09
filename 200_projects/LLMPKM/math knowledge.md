---
aliases: []
confidence: 
created: 2025-11-05T16:45:24Z
epistemic: 
last_reviewed: 
modified: 2025-11-09T11:31:02Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: math knowledge
type: 
uid: 
updated: 
---

This is a concept that can be effectively described using set theory and probability, with added variables to account for communication and bias.

Here is a formal mathematical model built on your components.

1. The Core Elements: Knowledge Sets
First, we define the universe of information and the knowledge of individuals.
 - The "Whole Picture" (Universal Set): Let U be the complete and accurate set of all discrete concepts, facts, and relationships for a given complex topic. The "total" understanding possible is the size (cardinality) of this set, |U|.
 - Individual Knowledge (Subset): Each person i on a team has a knowledge set, K_i, which is a subset of U (i.e., K_i \subseteq U).
   - K_i represents the actual, correct knowledge that person i possesses.
   - Misinformation (ideas a person holds that are not in U) could be modelled as another set, M_i, but we'll focus on K_i for now.
 - Team's Potential Knowledge (Union): The total knowledge held by the team collectively is the union of all their individual sets:

   This K_T represents the maximum possible understanding the team could achieve if communication were perfect.

2. Measuring Understanding vs. Overlap
The "amount" of understanding is the size (cardinality) of these sets.
 - Actual Individual Understanding (A_i): This is a measure of how much of the whole picture person i has.

   (This is a value between 0 and 1, or 0% to 100%).

 - Actual Team Understanding (A_T): This is the measure of the team's collective knowledge.

This is where the problem of "combination" you mentioned becomes critical. The size of the union is not the simple sum of the individual parts. It's defined by the Principle of Inclusion-Exclusion:

 - For 2 people: |K_1 \cup K_2| = |K_1| + |K_2| - |K_1 \cap K_2|
 - The K_1 \cap K_2 term is the "overlap" or shared knowledge.
High-performing teams often have low overlap (diverse knowledge). Teams where everyone knows the same things have high overlap, and their collective knowledge |K_T| isn't much bigger than any individual's |K_i|.
3. Modelling Cognitive Bias and Certainty
This is the gap between what a team thinks it knows and what it actually knows. We must introduce new "perception" variables.
 - Perceived Individual Understanding (P_i): This is what person i thinks they know. This is often a function of their bias, B_i.
   P_i = f(A_i, B_i)
   (In Dunning-Kruger, for low A_i, B_i is high and positive, so P_i > A_i).
 - Perceived Team Understanding (P_T): This is what the group collectively assesses its understanding to be. This is not a simple union; it might be:
   - The average of individual perceptions: \text{avg}(P_i)
   - Dominated by the most confident member: \max(P_i)
   - Inflated by groupthink: \text{avg}(P_i) + B_g (where B_g is a group bias term).
This lets us define the two gaps you observed:
 - The Knowledge Gap (External): This is the part of the problem the team cannot solve, no matter how well they communicate.

   > Gap (External) = |U| - |K_T|
   > (The concepts no one on the team knows)

 - The Certainty Gap (Internal Bias): This is the "delusion" you mentioned.

   > Gap (Certainty) = P_T - A_T
   > (When P_T > A_T, the team is overconfident. They believe they understand a problem they do not).

4. Modelling the "Communication Line"
Your model correctly identifies that K_T (the potential knowledge) is not achieved instantly. Communication is a lossy process.
 - Communication Efficiency (\epsilon): We can introduce a factor \epsilon (where 0 \le \epsilon \le 1) that represents the quality of the communication line (documentation, meetings, clarity of language).
 - Realised Team Knowledge (K_R): The knowledge that is actually synthesised and available to the team for a decision is the Realised Knowledge, K_R.

If \epsilon = 1 (perfect communication), the team realises 100% of its potential. If \epsilon = 0.2 (terrible documentation, people talking over each other), they only manage to synthesise 20% of their collective knowledge.

This introduces a third, tragic gap:

 - The Synthesis Gap (Internal Process):

> Gap (Synthesis) = |K_T| - |K_R|
   > (Knowledge that exists in the team but was lost due to poor communication).

A Complete Model Example

Let's put it all together.

Topic: Understand a complex software bug.

 - Total Concepts (U): There are 100 concepts needed for a full solution. |U| = 100.
The Team:
 - Alice (K_A): Knows 30 concepts. A_A = 30\%. But she is overconfident. P_A = 60\%.
 - Bob (K_B): Knows 25 concepts. A_B = 25\%. He is under-confident. P_B = 20\%.
 - Overlap (K_A \cap K_B): They share 10 concepts.
The Model in Action:
 - Potential Team Knowledge (K_T):
   |K_T| = |K_A| + |K_B| - |K_A \cap K_B| = 30 + 25 - 10 = 45
   The team collectively holds 45 of the 100 concepts.
 - Actual Team Understanding (A_T):
   A_T = |K_T| / |U| = 45 / 100 = 45%
   (This is their objective, maximum possible understanding).
 - The Knowledge Gap:
   |U| - |K_T| = 100 - 45 = 55 concepts.
   (There is 55% of the problem that this team cannot solve, no matter what).
 - Perceived Team Understanding (P_T):
   Alice is the most confident, so the team defers to her (a \max(P_i) model).
   P_T = \max(P_A, P_B) = \max(60\%, 20\%) = 60%
 - The Certainty Gap (Bias):
   P_T - A_T = 60\% - 45\% = 15%
   (The team is 15% overconfident. They think they know 60% of the problem, but they only know 45%).
 - The Communication Line (\epsilon):
   They have a hasty 10-minute meeting. Communication is poor. \epsilon = 0.5.
 - Realised Team Knowledge (K_R):
   |K_R| = \epsilon \times |K_T| = 0.5 \times 45 = 22.5
   Their actual working knowledge after the meeting is only 22.5 concepts (or 22.5%).
The Final State: The team proceeds to make a decision, believing they have 60% understanding, when in reality they only managed to synthesise 22.5% of the problem, from a potential maximum of 45%. The remaining 55% was entirely unknown to them.
This model, based on set theory (U, K_i), set operations (\cup, \cap), and modifiers (P, \epsilon), seems to capture the dynamic you described.
Would you like to explore how to model the growth of these knowledge sets over time (e.g., through research), or how to model the "misinformation" part?

This is a rich problem! Let me sketch out a mathematical framework that captures both the actual understanding and the illusion of completeness:

## Basic Model Structure

**Problem Space**: Let Ω represent the complete "ground truth" of a problem - everything that *could* be known about it.

**Individual Knowledge**: Each person i has knowledge K_i ⊆ Ω

**Team Knowledge**: K_team = ⋃(K_i) - the union of all individual knowledge

**Coverage Metric**:
- Actual coverage: C_actual = |K_team|/|Ω|
- Perceived coverage: C_perceived = f(K_team, bias_factors)

## The Cognitive Bias Component

This is where it gets interesting. We can model perceived understanding as:

**C_perceived = C_actual + β(C_actual) · (1 - C_actual)**

Where β represents bias intensity. This creates an overconfidence effect - teams feel most certain when they have *some* knowledge but not complete knowledge (the dangerous middle zone).

## Communication Effectiveness

Let's add a communication matrix **M** where M_ij represents how effectively person i can transmit knowledge to person j:

**K_i^(t+1) = K_i^(t) ∪ (⋃_j M_ij · K_j^(t))**

Where M_ij ∈ [0,1] captures:

- Documentation quality
- Shared vocabulary
- Communication bandwidth
- Attention/understanding

## Knowledge Overlap and Redundancy

**Redundancy**: R = Σ|K_i ∩ K_j|/(|K_team|) for i≠j

High redundancy means lots of shared understanding but potential blind spots.

**Diversity bonus**: The value of adding person n+1:
**ΔC = |K_(n+1) \ K_team|/|Ω|**

## Unknown Unknowns

Perhaps most critical:

**Known unknowns**: U_known = {x ∈ Ω : ∃i such that i knows they don't know x}

**Unknown unknowns**: U_unknown = Ω \ (K_team ∪ U_known)

Teams with high C_perceived but large U_unknown are in the most danger.

---

Would you like me to develop any of these components further? I'm particularly interested in the dynamics of how *questioning* behavior (people actively probing for gaps) could be modeled to reduce the unknown-unknown space.

This is a fascinating idea! You’re essentially describing a model of **distributed cognition** and **collective understanding**, where individual knowledge sets interact to form a group-level picture—but with distortions from biases and communication limits.

Here’s one way to formalize it mathematically:

---

### **1. Represent Individual Understanding**
- Let the topic be represented as a set of concepts \( T = \{c_1, c_2, \dots, c_n\} \).
- Each person \( i \) has a knowledge subset \( K_i \subseteq T \) and an **understanding weight** \( w_i(c_j) \in [0,1] \) for each concept \( c_j \) they know (reflecting depth or certainty).

So person \( i \)'s understanding can be modeled as a vector:

\[

\mathbf{u}*i = (u*{i1}, u_{i2}, \dots, u_{in}), \quad u_{ij} = \begin{cases}

w_i(c_j) & \text{if } c_j \in K_i \\

0 & \text{otherwise}

\end{cases}

\]

---

### **2. Group Understanding Without Communication**

If we just aggregate knowledge:

\[

\mathbf{U}_{\text{union}} = \max(\mathbf{u}_1, \mathbf{u}_2, \dots, \mathbf{u}_m)

\]

This gives the **best possible coverage** if everyone shared perfectly.

---

### **3. Communication Model**

Communication is imperfect. Define a **communication matrix** \( C \in [0,1]^{m \times m} \), where \( C_{ij} \) is the probability or efficiency of person \( i \) transferring their understanding to person \( j \).

After \( t \) rounds of communication, the group understanding evolves as:

\[

\mathbf{U}(t+1) = \mathbf{U}(t) + \alpha \cdot C \cdot \mathbf{U}(t)

\]

where \( \alpha \) is a learning rate (how much new info is absorbed per interaction).

---

### **4. Cognitive Bias Factor**

Introduce a **bias function** \( b(u) \) that distorts perceived certainty. For example:

\[

b(u) = \frac{u^\gamma}{u^\gamma + (1-u)^\gamma}

\]

where \( \gamma > 1 \) exaggerates certainty (confirmation bias).

So the **perceived group understanding** is:

\[

\mathbf{U}_{\text{perceived}} = b(\mathbf{U}(t))

\]

---

### **5. Metrics**
- **Coverage**: fraction of concepts with \( U_j > \theta \) (threshold for “understood”).
- **Redundancy**: overlap between individuals’ knowledge sets.
- **Distortion**: difference between perceived and actual understanding.

---

Would you like me to:

✅ Build a **simulation in Python** for this model (with adjustable parameters for team size, communication efficiency, and bias)?  
✅ Or create a **diagram** showing how these components interact?  
✅ Or both?

I want to create a mathematical model of team understanding. I have noticed that people have different ideas and understanding about complex topics and sometimes even combined there is no whole picture. But because of cognitive biases and certainty groups think they understand a problem. So each person has a set of knowledge that creates an amount of understanding of a topic. Combining all the sets via communication line talking or documenting creates a bigger understanding. What would a maths model of this look like

A mathematical model of team understanding can be framed using set theory and information aggregation, accounting for cognitive biases that distort perceived collective knowledge. Each team member possesses a distinct knowledge set, and communicating or documenting enables these sets to overlap and expand—though not always to a complete whole, especially in the presence of bias and miscalibration.

### Core Model Structure

- Individual knowledge can be represented as sets: $$ K_1, K_2, \ldots, K_n $$

 for a team of $$ n $$

 people[1][2].

- The union $$ K_{team} = K_1 \cup K_2 \cup \ldots \cup K_n $$

 depicts the total pool of knowledge available if all information is perfectly shared.

- Real understanding is less than this union due to incomplete communication, documentation gaps, and biases (e.g., Dunning-Kruger effect, overconfidence)[1][3].

### Aggregation With Biases

- Each person's perceived certainty can be modeled by a weight $$ w_i $$

 that scales their input, determined by confidence rather than their actual expertise[1].

- Overall team understanding: $$ U_{team} = \bigcup_{i=1}^n w_i \cdot K_i $$
- When biases are present, $$ w_i $$

 may not reflect true contribution, leading to a distorted collective picture[3].

- Models such as confidence-weighted voting, competence-weighted aggregation, and plurality voting are used, though confidence-weighted approaches are often less accurate due to self-assessment errors[1][3].

### Communication & Documentation

- Communication acts as edges in a graph, connecting knowledge sets:
  - Member-to-member transfer expands overlap.
  - Documentation creates shared external nodes, accessible to all, increasing global coverage[4][5].
- Imperfect transmission can be modeled as a subgraph or partial union, constraining effective team understanding.

### Cognitive Bias Impact

- Cognitive biases—such as overconfidence—can be captured mathematically by error terms $$ \epsilon_i $$

 in individual knowledge estimates.

- Aggregate knowledge is then $$ K'_{team} = K_{team} + \sum_{i=1}^n \epsilon_i $$

, often leading to misunderstanding or illusion of complete coverage[1][3].

### Example Equation

$$
U_{actual} = \left( \bigcup_{i=1}^n K_i \right) - \text{loss}_{\text{comm}} + \text{bias}_{\text{overlap}}
$$

Where:

- $$ \text{loss}_{\text{comm}} $$

: loss due to incomplete sharing/documenting.

- $$ \text{bias}_{\text{overlap}} $$

: error introduced by overconfidence, groupthink, and false consensus[1].

### Relevant Models

- Shared Mental Model (SMM): focuses on the intersection of knowledge sets where team members have common understanding[2][6].
- Transactive Memory System (TMS): tracks which member knows what, enhancing team recall through distributed memory[2].
- SECI Model: cycles of sharing, externalizing, combining, and internalizing knowledge in teams[4].

### Concrete Modeling Approaches

- Mathematical dynamical systems: Team understanding can be modeled as a set that evolves based on communication "events" and update rules, possibly using differential or recurrence equations[7][8].
- Cognitive map aggregation: Individual knowledge graphs are merged, with mathematical procedures to minimize analyst bias in combination[9].
- Bias modeling: Confidence scores and self-selection can be coded as variables in collective decision simulations. Overconfidence can reduce true aggregate understanding[1][3].

***

This foundational set-based approach, enriched with weights and bias/error terms, gives you a concrete mathematical framework for modeling team understanding and the impact of cognitive biases on collective knowledge[1][3][2][4][7].

Citations:

[1] Modelling Cognitive Bias in Crowdsourcing Systems <https://www.sciencedirect.com/science/article/abs/pii/S138904171830158X>

[2] Collective forms of leadership and team cognition in work teams <https://www.sciencedirect.com/science/article/pii/S0001691825007164>

[3] Confidence, Self-Selection, and Bias in the Aggregate <https://benjamin-enke.com/pdf/Confidence_aggregate.pdf>

[4] Knowledge Management Frameworks: 6 Types & 5 Models - A Guide <https://slite.com/en/learn/knowledge-management-frameworks>

[5] Collective intelligence in teams - PubMed Central - NIH <https://pmc.ncbi.nlm.nih.gov/articles/PMC9659728/>

[6] Full article: The role of shared mental models in human-AI teams <https://www.tandfonline.com/doi/full/10.1080/1463922X.2022.2061080>

[7] Understanding and Modeling Teams As Dynamical Systems - PubMed <https://pubmed.ncbi.nlm.nih.gov/28744231/>

[8] Understanding and Modeling Teams As Dynamical Systems <https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01053/full>

[9] Aggregation cognitive maps procedure for group decision ... <https://www.emerald.com/k/article/45/4/589/272609/Aggregation-cognitive-maps-procedure-for-group>

[10] 4.2 Five Models for Understanding Team Dynamics <https://pressbooks.bccampus.ca/technicalwriting/chapter/understandingteamdynamics/>

[11] [PDF] Mathematical Models of Group Dynamics When Working in Teams ... <https://ceur-ws.org/Vol-2917/paper5.pdf>

[12] [PDF] Dynamic Coalescence as a Mathematical Model of Leadership and ... <https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1096&context=studentpub_uht>

[13] 6 Steps to Build a Collective Intelligence Framework for Smarter ... <https://www.glassfrog.com/blog-post/6-steps-to-build-a-collective-intelligence-framework-for-smarter-decision-making>

[14] Eliminating Public Knowledge Biases in Information ... <https://pubsonline.informs.org/doi/10.1287/mnsc.1040.0247>

[15] How to tap Into the Collective Wisdom of a Team - Mind the Product <https://www.mindtheproduct.com/how-to-tap-into-the-collective-wisdom-of-a-team/>

[16] Expert Knowledge Elicitation: Subjective but Scientific <https://www.tandfonline.com/doi/full/10.1080/00031305.2018.1518265>

[17] Going Round in Circles: A Cognitive Bias in Geometric ... <https://pmc.ncbi.nlm.nih.gov/articles/PMC11627530/>

[18] Math anxiety and associative knowledge structure are ... <https://arxiv.org/html/2511.01558v1>

[19] Stronger together: A multilevel study of collective strengths use and ... <https://www.sciencedirect.com/science/article/pii/S0148296323000863>

[20] Collective (Team) Learning Process Models: A Conceptual Review <https://journals.sagepub.com/doi/10.1177/1534484310371449>
