---
aliases: []
confidence: 
created: 2025-07-16T19:03:13Z
epistemic: 
id: Give me the logic
last_reviewed: 
modified: 2025-11-03T13:48:23Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/maths]
title: Give me the logic
type:
uid: 
updated: 
version:
---

The relationship between logic and mathematics is foundational and symbiotic; logic serves as the language, structure, and rules of reasoning for mathematics, while mathematics provides the content and subject upon which logic operates. In essence, logic is the bedrock upon which the entire edifice of modern mathematics is built.

A Historical Perspective

The link between these two fields has evolved over millennia, with key figures and movements shaping our modern understanding.

From Antiquity to the Enlightenment

- Ancient Greece: Aristotle formalised logic through his system of syllogisms, providing the first rigorous framework for deductive reasoning. Around the same time, Euclid's Elements presented geometry as an axiomatic system, where theorems were logically deduced from a small set of initial axioms and postulates. This was the first grand application of logic to a mathematical field.
- Gottfried Wilhelm Leibniz (17th Century): Leibniz dreamt of a characteristica universalis, a universal formal language that could express all scientific and mathematical concepts, and a calculus ratiocinator (calculus of reasoning) that could solve all problems by mechanical computation. This was a direct precursor to modern mathematical logic.
  The Rise of Modern Logic and Foundational Schools
  The 19th and early 20th centuries saw a "foundational crisis" in mathematics, leading to a much deeper investigation of its logical underpinnings.
- Logicism: Spearheaded by Gottlob Frege, and later Bertrand Russell and Alfred North Whitehead, logicism is the philosophical thesis that mathematics is reducible to logic. Their magnum opus, Principia Mathematica, was an ambitious attempt to derive all mathematics from a set of purely logical axioms. They famously took hundreds of pages to formally prove that $1 + 1 = 2$, demonstrating the immense rigour required.
- Formalism: Led by David Hilbert, this school viewed mathematics as the manipulation of symbols according to specified formal rules. The meaning of the symbols was considered irrelevant; the focus was on the consistency of the game. Hilbert's Programme aimed to place all of mathematics on a firm axiomatic foundation and prove that this foundation was consistent (free from contradiction).
- Intuitionism: Championed by L.E.J. Brouwer, intuitionism posits that mathematics is a creation of the human mind. A mathematical statement is only true if a mental construction can prove it. This school notably rejects the Law of the Excluded Middle ($P \lor \neg P$, a proposition is either true or its negation is true) and proofs by contradiction as universally valid methods.
  Gödel's Bombshell
  In 1931, Kurt Gödel published his Incompleteness Theorems, which profoundly and permanently altered the landscape.
- First Incompleteness Theorem: Any consistent formal system F powerful enough to describe the arithmetic of the natural numbers contains true statements that are unprovable within F itself.
- Second Incompleteness Theorem: Such a system F cannot prove its own consistency.
  Gödel's work demonstrated that the goals of both Logicism and Hilbert's Programme were unattainable in their original forms. It showed that mathematics is inherently incomplete and that its consistency cannot be proven by its own axiomatic methods.
  Core Intersections
  Today, logic is a major branch of mathematics, and its tools are indispensable across all mathematical fields.
  Set Theory
  Set theory is often called the "lingua franca" of modern mathematics. Concepts like functions, numbers, and geometric spaces are all defined in terms of sets. The very foundation of set theory (e.g., the ZFC axioms - Zermelo-Fraenkel with the Axiom of Choice) is a list of axioms in the language of first-order logic. For example, stating that an element x is in a set A is a fundamental logical proposition, written as $x \in A$.
  Proof Theory
  Proof theory treats mathematical proofs themselves as formal objects of study. It analyses the structure of proofs, what can be proven from certain axioms, and the complexity of those proofs. It is, in essence, the mathematics of mathematical logic.
  Model Theory
  Model theory studies the relationship between formal languages (like the language of arithmetic) and the mathematical structures that "model" them. It explores how a set of axioms determines the properties of its models. For instance, it might ask what structures satisfy the axioms for a group or a field.
  Logic in Daily Mathematical Practice ✍️
  Beyond these foundational fields, logic is the everyday tool of the working mathematician.
- Logical Connectives: Statements are built using connectives like AND (\land), OR (\lor), and NOT (\neg).
- Implication: The structure of any theorem is a logical implication: "If P (hypothesis), then Q (conclusion)", written as $P \implies Q$.
- Quantifiers: Mathematical statements are saturated with quantifiers. The universal quantifier $\forall$ ("for all") and the existential quantifier $\exists$ ("there exists") are crucial for expressing general truths. For example, the definition of a limit in calculus is a complex statement involving multiple nested quantifiers.
- Proof Techniques: Standard methods of proof are direct applications of logical principles:
  - Direct Proof: Assume P is true and logically deduce a chain of implications that leads to Q.
  - Proof by Contradiction: To prove P, assume its negation $\neg P$ is true and show this leads to a logical absurdity (e.g., $Q \land \neg Q$). A classic example is the proof that $\sqrt{2}$ is irrational.
  - Proof by Contrapositive: To prove $P \implies Q$, one can instead prove the logically equivalent statement $\neg Q \implies \neg P$.
  - Proof by Induction: A powerful technique for proving statements about all natural numbers, relying on a logical chain reaction.
    In conclusion, the link between logic and mathematics is inseparable. Logic provides the rigour, language, and inferential machinery that allows mathematics to function and to build its vast, abstract, and certain structures. Mathematics, in turn, provides the rich and complex subject matter that has driven the development of logic itself.

You can learn the logic used in maths by starting with the fundamentals of propositional logic, then moving on to quantifiers, and finally applying these concepts by actively practising different proof techniques on introductory problems in number theory and set theory.

Here is a guide with practical activities to help you develop these skills.

1. Start with Propositional Logic (The Absolute Basics) 🧱
   This is the grammar of mathematical reasoning. It deals with how to combine simple statements (propositions) with logical connectives.

- Concepts: Learn the precise meaning of AND (\land), OR (\lor), NOT (\neg), IMPLIES (\implies), and IF AND ONLY IF (\iff).
- Practical Activity: Truth Tables: This is the best way to get a feel for how these connectives work. Create truth tables for simple and complex statements. Start with P ∧ Q, then move to more complex ones like (P ⇒ Q) ⇔ (¬P ∨ Q). This helps you understand logical equivalence, which is crucial for rephrasing statements in proofs.

| P     | Q     | P ⇒ Q | ¬P    | ¬P ∨ Q | (P ⇒ Q) ⇔ (¬P ∨ Q) |
| ----- | ----- | ----- | ----- | ------ | ------------------ |
| True  | True  | True  | False | True   | True               |
| True  | False | False | False | False  | True               |
| False | True  | True  | True  | True   | True               |
| False | False | True  | True  | True   | True               |

2. Master Predicates and Quantifiers 🧮
   This is how you generalise statements in mathematics.

- Concepts: A predicate is a statement involving variables, like "P(n): n is an even number". Quantifiers turn these into general statements. Learn the universal quantifier ∀ ("for all") and the existential quantifier ∃ ("there exists").
- Practical Activity: Translate Sentences: Practice translating sentences between natural English and logical notation. This is a vital skill.
  - English to Logic:
    - "Every integer has a square that is non-negative."
    - Translation: $\forall n \in \mathbb{Z}, n^2 \ge 0$.
    - "There is a prime number between 20 and 25."
    - Translation: $\exists p \in \mathbb{P}$, (20 < p < 25), where $\mathbb{P}$ is the set of prime numbers.
  - Logic to English:
    - $\forall x \in \mathbb{R}, \exists y \in \mathbb{R}, y > x$.
    - Translation: "For every real number, there is another real number that is larger than it."

3. Learn the Core Skill: Proof Techniques ✍️
   This is where logic meets mathematical creativity. Focus on understanding how and when to use each technique. Good problems to start with involve integers (even/odd properties, divisibility) and basic set theory.
   a. Direct Proof

- Idea: Assume the hypothesis (P) is true and use definitions and existing theorems to logically derive the conclusion (Q). It's a straight line from P to Q.
- Problem Type: "Prove that the sum of two even integers is even."
  b. Proof by Contrapositive
- Idea: To prove $P \implies Q$, you can instead prove the logical equivalent: $\neg Q \implies \neg P$. That is, assume the conclusion is false and show the hypothesis must also be false.
- Problem Type: "Prove that if $n^2$ is even, then n is even."
  - Direct approach is hard: Assume n^2 is even, so $n^2 = 2k$. Then $n = \sqrt{2k}$, which is not easy to work with.
  - Contrapositive is easy: Assume n is not even (i.e., odd) and show that n^2 is also not even (i.e., odd). This is much more direct (see the worked example below).
    c. Proof by Contradiction
- Idea: To prove a statement P is true, you assume it is false ($\neg P$) and show that this assumption leads to a logical contradiction (e.g., x is both rational and irrational, or 1=0).
- Problem Type: "Prove that $\sqrt{2}$ is irrational." You start by assuming it is rational and show this leads to an absurdity.
  d. Proof by Induction
- Idea: A technique for proving a statement is true for all natural numbers. First, prove a base case (show it's true for n=1). Then, in the inductive step, prove that if it's true for some number k, then it must be true for the next number, k+1.
- Problem Type: "Prove that for all n \ge 1, the sum $1+2+3+...+n = \frac{n(n+1)}{2}$."
  Worked Example: Proof by Contrapositive
  Statement: For any integer n, if n^2 is even, then n is even.
- Identify P and Q:
  - P: n^2 is even.
  - Q: n is even.
  - We need to prove P \implies Q.
- Form the Contrapositive:
  - We will prove $\neg Q \implies \neg P$.
  - $\neg Q$: n is not even (i.e., n is odd).
  - $\neg P: n^2$ is not even (i.e., n^2 is odd).
  - New statement to prove: If n is odd, then n^2 is odd.
- Prove the Contrapositive:
  - Assume n is odd. By definition of an odd integer, we can write $n = 2k + 1$ for some integer k.
  - Now, let's find n^2:
    $n^2 = (2k + 1)^2 = 4k^2 + 4k + 1$
  - We can factor out a 2:
    $n^2 = 2(2k^2 + 2k) + 1$
  - Let $m = 2k^2 + 2k$. Since k is an integer, m is also an integer. So, $n^2 = 2m + 1$.
  - By definition, this shows that n^2 is an odd number.
- Conclusion: We have successfully proven that if n is odd, then n^2 is odd. Since the contrapositive statement is true, the original statement ("if n^2 is even, then n is even") must also be true.
  Recommended Resources
- Books:
  - "How to Prove It: A Structured Approach" by Daniel J. Velleman: This is considered the gold standard for learning the logic of proofs.
  - "Book of Proof" by Richard Hammack: An excellent and often free-to-download alternative.
- Online Courses & Problems:
  - Brilliant.org: Has interactive courses on Logic and Mathematical Fundamentals.
  - Khan Academy: Their sections on pre-calculus and calculus touch on logic and proof ideas.
  - Project Euler: Provides a large number of computational problems that require rigorous logical and mathematical thinking to solve efficiently. Start with the first few problems.

Here's how you, as an adult with no formal math training, can learn mathematics and mathematical reasoning:

First and foremost, understand that anyone can learn to think like a mathematician, regardless of their past experiences or perceived ability . Many people dislike math due to traditional teaching methods that focused on memorization and "drill and kill" rather than true understanding or creativity . Mathematics, at its heart, is an art form involving creativity, visualizing, finding patterns, asking "what if?", and experimenting . It's about ideas, not just symbols or rigid rules . Your goal is not necessarily to become a university mathematician, but to adopt some of the ways mathematicians think about problems .

The key to learning mathematical reasoning as an adult is to cultivate specific "habits of mind" and practices that mathematicians use, and to apply them to problems that are engaging and relevant to you .

Here are the core components of mathematical thinking and practical ways to practice them:

1. **Become a Pattern Detective** :
   - **Understanding:** Humans are inherently wired to look for patterns, even in meaningless data (apophenia) . Mathematicians notice and study patterns to understand the world .
   - **Practice:** Consciously observe patterns in your daily life. For instance, look at tile or wallpaper patterns and try to describe the rule they follow, or imagine how they would continue beyond their visible boundaries . When listening to music, try to identify the drumbeat or bassline and predict changes, which means you're learning the pattern . Recognize how babies learn language by detecting patterns in speech . Even weather forecasting is based on pattern recognition .
   - **Applied Example:** Consider a simple growing pattern, like the one used for triangular numbers. Even if you don't delve into the algebra immediately, just noticing how it grows and trying to sketch the next figure engages mathematical thinking . This trains your brain to make sense of structured information around you .

2. **Use Probability and Experimentation** :
   - **Understanding:** Probability explains the likelihood of events, often counter-intuitively . Experimental probability approaches theoretical probability as the number of trials increases . Mathematicians are not afraid to experiment .
   - **Practice:** Analyze everyday "games of chance" like rolling dice or flipping coins. For instance, understand why "lucky sevens" in dice games are simply more probable (6 ways to roll a 7 out of 36 possible outcomes, or 1/6 probability) . Notice how probability is used in weather forecasts (e.g., 30% chance of rain) .
   - **Applied Example:** Consider lottery tickets or raffle tickets. Instead of relying on "luck," calculate the actual probability of winning (e.g., 1 in 292.2 million for Powerball jackpot) . This helps you make informed choices, even if the numbers are very small. Challenge your intuition with problems like the "Birthday Coincidences" (how many people needed for a 50% chance of two sharing a birthday – it's 23, not 182) or the Monty Hall problem, and systematically work through the probabilities to understand why your initial intuition might be wrong . These illustrate how crucial mathematical thinking is when intuition fails .

3. **Describe and Speak in Mathematical Language** :
   - **Understanding:** Mathematics is a language that helps understand the world . Algebra, for instance, generalizes arithmetic rules . Words and language are processed in different brain parts than math, yet are crucial for communication in math .
   - **Practice:** When facing a quantitative problem, try to "translate" it into a more formal, structured description. For example, think about how using different coupons (e.g., 20% off vs. $5 off at Bed Bath and Beyond) can be expressed as algebraic equations like $y = 0.8x$ and $y = x - 5$ . Solving for $x$ (the item price where savings are equal) allows you to generalize and make better decisions .
   - **Applied Example:** Engage in discussions about problems, even if your ideas are partially formed. Speaking about mathematical concepts helps solidify understanding and allows for feedback and refinement of your thinking . This is akin to how mathematicians process ideas, akin to a musician processing a composition .

4. **Tinkering: Breaking it Down and Putting it Back Together** :
   - **Understanding:** Learning often comes from experimentation and construction of knowledge, not just memorization . Tinkering involves breaking down phenomena, examining parts, and reconstructing for deeper understanding .
   - **Practice:** When faced with a large task or problem, break it into smaller, more manageable pieces . For example, when adding numbers like 13 and 8, you can decompose 13 into 10 and 3, then combine the 3 with 7 from the 8 to make another 10, resulting in 20 plus the remaining 1, which is 21 . This builds "number sense" .
   - **Applied Example:** Look at complex formulas (like the distance formula in algebra) not as something to memorize, but as something to break down into simpler, familiar concepts (like the Pythagorean Theorem) . Ask "what if?" questions and don't be afraid to try different approaches and fail, as failure leads to learning .

5. **Inventing: Understanding Algorithms and Using Them** :
   - **Understanding:** An algorithm is a reliable procedure, a set of steps to achieve a certain outcome . Mathematicians are "lazy" in the sense that they seek efficient methods and shortcuts . Algorithms are not just for computers; they're used in recipes, advertising, and daily routines .
   - **Practice:** Observe how you perform routine tasks and try to formalize the steps for efficiency. For instance, creating your own "algorithm" for making a sandwich or sorting mail (e.g., "habit stacking" – immediately sorting mail after taking off shoes) . This "if-then" planning can reduce stress and make behavioral change easier .
   - **Applied Example:** While complex algorithms might be daunting, understanding simple ones in everyday life helps. Consider the steps for multiplying multi-digit numbers – your elementary school method is an algorithm . The goal isn't necessarily to invent new universal algorithms, but to recognize and formalize efficient processes for yourself .

6. **Visualizing: Externalizing the Internal** :
   - **Understanding:** Visualizing is a powerful tool, as a large part of the brain is dedicated to visual processing . It involves internalizing, identifying, comparing, connecting, and sharing ideas .
   - **Practice:** When faced with a spatial problem, mentally picture it first. For example, before packing a car for a trip, visualize how suitcases and odd-shaped items might fit . Drawing sketches or models can help solve problems, like arranging banquet seating or planning a kitchen layout (similar to Ikea's planning tool) .
   - **Applied Example:** For non-spatial problems, visualize desired outcomes. Athletes and musicians use visualization to improve performance and reduce anxiety . When planning a difficult conversation, visualize the discussion, how you want to come across, and potential rebuttals . Sharing your plan with someone else (externalizing) can solidify it .

7. **Guessing: Making Estimations** :
   - **Understanding:** Estimation, or making educated guesses about numbers, is a daily skill tied to "number sense" . It's not about being exact, but about approximating effectively .
   - **Practice:** Practice estimating in daily scenarios: your grocery bill, the cost of gas, how much time you need to get ready, or the number of stairs in a building . Improve your "number sense" by consciously working with "friendly numbers" (multiples of ten or a hundred) for mental math, like calculating tips (e.g., estimating 15% of a $38.46 bill as between $4 and $8) .
   - **Applied Example:** Be aware of how rounding is used in pricing (e.g., $2.99 instead of $3.00) and consciously round to understand the true cost . Engage in "number talks" – looking at an image with multiple dots and finding different ways to count them without counting one by one. This encourages flexible thinking about numbers and patterns .

**Addressing "Problems I find online are way too difficult or require prior maths training":**

The sources highlight that traditional math education often focuses on facts and procedures without the underlying "why" or "how" of mathematical thinking, leading to disengagement . Your experience with difficult online problems likely stems from this gap.

- **Focus on the "Art" and "Why":** Instead of jumping to complex formulas, try to understand the *ideas* behind them. For example, the sources discuss the Pythagorean Theorem and how it can be understood visually (breaking a square into pieces) rather than just memorizing the formula $a^2 + b^2 = c^2$ .
- **Start with Engaging Questions:** Mathematics arises from natural human questions and problems, not contrived exercises . Instead of looking for generic "math problems," identify real-life situations where you naturally use quantitative reasoning, then try to formalize or deepen your understanding using the habits of mind discussed above.
- **Embrace Struggle and Iteration:** Mathematicians themselves struggle, make mistakes, and persevere . Don't expect to get the "right" answer immediately. The value is in the process of exploration, conjecture, and devising arguments .
- **Play Games and Puzzles:** For young children, playing games like Chess, Go, Hex, or Sprouts is recommended to develop deductive reasoning skills . This approach is equally valid for adults wanting to develop mathematical thinking without formal curriculum. The book "The Magical Maze" [l] itself is structured around puzzles and aims to guide you to think like a mathematician through engaging problems
- **Build Foundational Understanding:** If you find yourself needing specific arithmetic or algebraic "building blocks" that you didn't learn well, you can consult resources that explain these concepts from the ground up, focusing on understanding rather than rote memorization. For instance, the "KS3 Maths Yearly Topic Map" [j] outlines topics typically covered in middle school mathematics, such as place value, basic operations, fractions, percentages, and an introduction to algebra and geometry . This can serve as a reference for *what* areas exist in foundational math, but remember to approach them with the "how to think" mindset rather than just memorizing rules.

By consciously adopting these habits of mind and applying them to problems you encounter or find interesting in your daily life, you will train your brain to think mathematically. This approach will not only help you understand math more deeply but will also enhance your critical thinking and problem-solving skills for strategic recommendations.
