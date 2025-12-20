---
aliases: []
confidence: 
created: 2025-02-07T12:57:52Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:44Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [data-centric]
title: SCM DataCentric
type:
uid: 
updated: 
version:
---

Linus Torvalds' quote, *"Bad programmers worry about the code. Good programmers worry about data structures and their relationships,"* highlights the importance of data structure design in software engineering.

It suggests that the way data is organized and how it relates within a system is more crucial to success than the specific lines of code that manipulate it. This concept can be translated into the world of SCM by thinking of the data that SCM manages as the "data structures" in question and the code that manages the data as the programs in the quote. The data in SCM includes not just the raw source code, but also its history, its various branches, and its relationships to other parts of the system, and also how different versions are stored and accessed.

Here's how this idea applies to SCM, drawing on your provided sources:

1. Data Structure of the SCM System:

- Version Control as a Data Structure: The fundamental data structure of SCM is the version control system itself. This includes how changes are tracked, how different versions are stored, and how branches are managed. A good SCM system should be designed with careful thought into how this versioning data is stored and accessed. Source control should be thought of as source *code* management, not software configuration management (SCM).
- Branching Strategy: Branching is a fundamental way that SCM systems allow for parallel development, but it also creates a complex data structure as branches are related to one another by their histories. A badly designed branching strategy, where branches are used for many purposes or are kept for too long, can lead to integration headaches. According to the sources, the need to merge branches means it’s important to think carefully before branching and to make sure you have a sensible process to support it. In general, every time you make a decision to branch in a continuous integration (CI) based development system, you are compromising to some degree.
- Commit Structure: The way commits are organised and structured is also important. Commits that are too large or too small can be hard to work with. The sources propose two basic approaches to commits: demonstrating the thinking process and presenting the final solution. Commits might represent units of work in increments as small as 15–30 minutes of effort. Alternatively, a developer might make radical changes to the working directory without tiny lifeline commits, and curate these changes into smaller, more relevant commits after the work is done.

2. Relationships between Elements in SCM:

- Dependencies: SCM should track the relationships between different parts of the software system, including dependencies between modules, libraries, and other components. This relates directly to the idea of coupling: loosely coupled components are much easier to manage and deploy than tightly coupled ones. Technical debt is a key concept that illustrates why it is necessary to manage dependencies between software components; poorer design choices lead to increased maintenance and bugs later on.
- Changes and Their Impact: Understanding the relationships between changes, features, and bug fixes is crucial for effective SCM. SCM tools track which changes are associated with which feature and also how defects were fixed. This makes it easier to understand the history of a codebase, and also to rollback specific changes if things go wrong.
- Team Collaboration: SCM also manages the relationships between team members and their code contributions. Version control is an important part of making team software development work effectively. The best teams have good cohesion and can make their own decisions without asking for permission from outside the team. Source control can be used to enhance communication and interaction between developers. However, having artificial barriers between teams will increase tension.

3. Applying This to SCM Practices:

- Focus on Modularity: Following the principles of modularity, information hiding, and separation of concerns leads to a codebase that is easier to manage. Applying modularity to the structure of your version control system makes it easier to work with too; smaller commits and branches make it easier to find issues and to integrate changes. Modularity should be used at every scale, including in code, and modules that are more testable are generally better. Modularity reduces complexity, allows for easier maintenance and reuse, and facilitates better quality software.
- Testability: The way your versioning system is configured should also enable testability. Good practices, such as test driven development (TDD) make code more testable. In TDD, you write the test first, so you are more likely to design interfaces and code that can be readily tested. If tests are difficult to write, it means that your design is poor. When you structure your commit and branching strategy, it is important to consider testability. Your testing strategy should be focused on being able to deliver that understanding feature by feature, and ensuring that testing is pervasive throughout your process.
- Iterative Development: Good SCM is crucial to the success of iterative development. SCM supports small, incremental changes, and ensures that the team can always revert to a known good state. Iterative methods place an emphasis on having production-ready code at the end of each iteration, which is the most useful measure of progress. Iteration encourages us to think in smaller batches, and to take modularity and separation of concerns more seriously.
- Feedback Loops: SCM should be part of a feedback loop that includes every aspect of the software development lifecycle. By making changes and testing them, you ensure that any problems are discovered earlier. The shortest feedback loops are created through sets of automated tests that are run upon every change to the system. It is important to optimise cycle time, which is the measure of how long it takes to go from an idea to working software, and this can be used to make our development process more efficient.

In summary, Linus's quote highlights the importance of thinking about the underlying data structures and their relationships when working with source control. Good SCM practices require attention to the organization of the code, the way changes are tracked, and the relationships between different parts of the system. By applying these principles, teams can build software more efficiently and reliably.

As a next step, I recommend we review the sections of the source materials that discuss branching strategies, commit structures, and how version control systems are integrated with other tools and practices, especially those that describe testability. Would you like to do that? I can also test your understanding of the material by offering some multiple-choice questions or creating some scenario-based exercises.
