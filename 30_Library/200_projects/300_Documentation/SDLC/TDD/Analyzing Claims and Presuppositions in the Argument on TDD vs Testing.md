---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:50Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [SDLC, TDD]
title: Analyzing Claims and Presuppositions in the Argument on TDD vs Testing
type: 
uid: 
updated: 
version: 
---

## Atomic Claims and Presuppositions

### Claim 1: "Many People either Reject TDD or Misunderstand It, Equating it with testing."

Presuppositions:

- TDD is a commonly misunderstood methodology.
- Some people conflate TDD with testing.
- There is a meaningful difference between TDD and testing.

### Claim 2: "TDD and Testing Serve Fundamentally Different Purposes, and Conflating Them Creates confusion."

Presuppositions:

- TDD has a distinct purpose from testing.
- Confusing TDD with testing leads to practical problems or misunderstandings in software development.

### Claim 3: "Testing is a Technique for Verifying that Software Works according to Stakeholder expectations."

Presuppositions:

- Testing focuses on validating software functionality.
- Stakeholder expectations are a central concern of testing.

### Claim 4: "Testing Challenges the System by Exploring Various Conditions and Validating Its behavior."

Presuppositions:

- Testing involves exploring different conditions to ensure system reliability.
- The purpose of testing is to validate behavior and find potential issues.

### Claim 5: "Testing Happens after the Code is Written, Aiming to Ensure Quality and Find defects."

Presuppositions:

- Testing is primarily a post-coding activity.
- The goals of testing are quality assurance and defect identification.

### Claim 6: "TDD is a Design methodology."

Presuppositions:

- TDD is more about shaping the design of software than about validating its correctness.
- There is a category of methodologies focused on design rather than verification.

### Claim 7: "In TDD, We Write Behavioural invocations—small, Executable Code Snippets that Describe the System's Expected behavior."

Presuppositions:

- TDD involves writing small, executable code snippets.
- These snippets describe the expected behavior of the system.
- Behavioural invocations are distinct from traditional test cases.

### Claim 8: "These Are not Tests in the Verification Sense; They Are Design Tools that Help Refine the System's Structure and interfaces."

Presuppositions:

- Behavioural invocations have a different purpose from verification tests.
- They serve as tools for refining system design rather than for checking correctness.

### Claim 9: "The Confusion Arises because both TDD and Testing Involve Code that Appears Similar (e.g., Assertions and checks)."

Presuppositions:

- TDD and testing can look similar on the surface.
- The similarities in syntax (e.g., assertions) contribute to the confusion.

### Claim 10: "Their Goals Are Distinct: Testing Verifies Correctness, while TDD Drives design."

Presuppositions:

- Verification and design are two distinct goals in software development.
- Testing and TDD have fundamentally different objectives.

### Claim 11: "The Behavioral Invocations Used in TDD Are Specifications of Expected Behavior, Which Help Us Explore and Shape the Code incrementally."

Presuppositions:

- Behavioral invocations act as specifications.
- TDD encourages incremental exploration and refinement of code.

### Claim 12: "The Resulting Design Checks Left behind Are Artifacts of This Process, not Its Primary purpose."

Presuppositions:

- The code produced during TDD is primarily a byproduct of the design process.
- The primary purpose of TDD is the design process itself, not the artifacts it leaves.

---

## Steelmanning the Argument

To steelman this argument, we can present the core claims as stronger and more refined:

1. TDD and testing are distinct methodologies with different goals and approaches.

    - Testing aims to verify that the software meets stakeholder expectations by challenging the system's behavior under various conditions. It focuses on correctness and defect detection after the code is written.
    - TDD is a design-oriented approach that focuses on incrementally building software by defining its expected behavior through small, executable snippets. These snippets guide the structure and design of the codebase.
2. The confusion between TDD and testing stems from surface similarities in how code is written in both practices.

    - Both TDD and testing involve assertions, checks, and executable code. However, their purposes diverge: TDD is about guiding design, while testing is about verifying correctness.
3. Behavioral invocations in TDD are better understood as design specifications than as tests.

    - These snippets help developers explore the design space and incrementally refine their implementations. The artifacts left behind may look like tests but are primarily a byproduct of the design process.

---

## Counterarguments and Critiques

1. The distinction between TDD and testing may be overstated.

    - Critics might argue that TDD inherently involves testing since it requires writing code that checks the behavior of the system. While the primary goal may be design, the practice still results in executable tests that verify behavior.
    - Additionally, the idea that TDD is purely a design methodology could be challenged. Many developers use TDD primarily to ensure that their code works correctly, blurring the line between TDD and traditional testing.
2. The claim that testing happens only after code is written may be too rigid.

    - Modern testing practices, such as behavior-driven development (BDD) and acceptance test-driven development (ATDD), involve writing tests before or alongside the code. These practices challenge the assertion that testing is always a post-coding activity.
3. The assertion that behavioral invocations are not tests might confuse practitioners.

    - For many developers, the idea of writing code to verify behavior is synonymous with testing. Introducing a new term like "behavioral invocations" could create more confusion rather than clarifying the distinction.
4. The artifacts of TDD (i.e., the resulting tests) have significant value beyond design.

    - The tests left behind after the TDD process are valuable for regression testing and continuous integration. To downplay their importance as mere artifacts risks undermining the practical benefits of TDD.
5. There may be overlap in the goals of TDD and testing.

    - While the primary goal of TDD is design, it also has secondary goals related to ensuring correctness. Similarly, testing practices like exploratory testing can influence design decisions, suggesting that the two practices are not entirely separate.
