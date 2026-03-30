# The hidden pearls of TDD

![rw-book-cover](https://www.thoughtworks.com/content/dam/thoughtworks/images/photography/meta/insights/blog/blg_meta_read_blog_generic.jpg)

## Metadata
- Author: [[Carlos Cavero]]
- Full Title: The hidden pearls of TDD
- Category: #articles
- Summary: Test-Driven Development (TDD) helps engineers write only the necessary code by testing first, which leads to simpler and more reliable software. It stops overengineering and reduces bugs by making design evolve with real needs, not guesses. In the age of AI coding tools, TDD guides AI to build clear and correct code, making it a key practice for the future.
- URL: https://www.thoughtworks.com/insights/blog/testing/the-hidden-pearls-of-TDD

## Full Document
![](https://www.thoughtworks.com/content/dam/thoughtworks/images/photography/banner-image/insights/in_banner_blogs.jpg)
#### Introduction

The current noise from AI hype in software engineering is deafening. With new models and agentic tools emerging daily, it’s easy to fall into a trap of believing that the *old ways* of disciplined craftsmanship are obsolete. However, we believe that now more than ever, we need to get back to our origins. With this Cambrian period of rapid evolution, the industry is overlooking the knowledge behind the core practices of software engineering — ones that stopped being swept away by the chaos of rapid, unverified development in the past.

Our personal journey toward becoming better engineers began when we immersed ourselves in the foundational works of Kent Beck and Martin Fowler. Their books on [Extreme Programming (XP)](https://martinfowler.com/bliki/ExtremeProgramming.html), [Test-Driven Development (TDD)](https://martinfowler.com/bliki/TestDrivenDevelopment.html) and [Refactoring](https://refactoring.com/), along with the timeless principles in The Pragmatic Programmer, shifted our perspective from simply ‘writing code’ to crafting software. By adopting these disciplines, we learned that quality isn’t an adjacent work — it’s the core of it. The **hidden pearls** of [TDD](https://javi-kata.medium.com/tdd-is-not-learned-it-is-practiced-e2b9a92eeb8b?sk=a65471a96ac7f5e7da47553e6aea7843) in particular are not just legacy techniques; they’re the essential pillars we need to build the future of technology effectively. These resources taught us that being a great engineer isn't about complexity and velocity but instead about reliability and simplicity.

The discipline of proof

At its core, TDD is a disciplined process where you write a test before the actual code. This ensures your requirements are clear and your software is testable from day one. The process follows the red-green-refactor cycle. This involves:

* Writing a small test that fails, defining the desired behavior (Red).
* Writing the minimum code necessary to make the test pass (Green).
* Cleaning up and improving the code's design while ensuring the test remains successful (Refactor).

However, our understanding of this process has evolved with experience. Early in our careers, we viewed writing tests merely as a verification practice, or a way to ensure the code does what it is supposed to do. As we mature, we start obsessing over metrics like test coverage or advanced techniques like mutation testing.

But the final realization is more profound. Tests are actually a form of living documentation. They prove that the code is valid by creating structures that demonstrate the hypothesis the code holds. *Edsger Wybe Dijkstra* discovered this principle in 1960, realizing programmers could use a hierarchy of postulates similar to that of mathematicians. Starting the implementation with the tests gives all of this for free, but there’s something more precious to be discovered.

#### Lean on feedback

"**A Test Is the First User of Your Code**" is one of the key lessons of Andy Hunt and Dave Thomas’ book *The Pragmatic Programmer.* It’s simple, direct and clear: when we write a test before the implementation, it becomes the first entity verifying the functionality to implement.

This shift in perspective is invaluable. If a test is difficult to write, it’s a clear signal the code will be difficult to use. Whether we’re designing a REST API or defining public methods in a class, we’re creating an architecture that shapes how other developers interact with our code. By treating the test as the initial client of our code, we naturally design more intuitive interfaces and ensure our software is born with usability in mind. The power of this mechanism extends beyond software engineering. It’s deeply rooted in behavioral psychology, particularly in the work of Daniel Kahneman and Richard H. Thaler. As humans, we rely on feedback to improve our performance, even in coding tasks.

#### Avoiding overengineering

One of the most immediate benefits of TDD is that it forces you to implement the **minimum amount of code** necessary to make a test pass because it is easy to get carried away and write code ”'just in case”. This is a point made by Kent Beck in *Extreme Programming Explained*. Without a failing test to satisfy, developers often fall into the trap of over-engineering.

By sticking to the TDD cycle, the resulting codebase is significantly leaner. You avoid the clutter of unused methods and speculative logic. The result is cleaner code that does exactly what is required — no more, no less — reducing the surface area for potential bugs.

Reducing the surface area for potential bugs isn't just a technical luxury but a critical business strategy. The later a defect is found, the exponentially more expensive it becomes to fix. This is because work built on defective components will inevitably need to be scrapped or reworked. Fixing a bug after release can be up to 150 times more expensive than addressing it during the initial design. Thus, **avoiding overengineering is not a coding preference**, it’s a financial imperative.

#### Refactoring: Designing with purpose

The final stage of the TDD cycle — Refactoring — is where the real magic happens. Since you already have a passing test as a safety net, you can fearlessly reorganize your code to adhere to core software principles. This is the moment to apply [SOLID](https://en.wikipedia.org/wiki/SOLID) principles, remove duplication ([DRY](https://www.martinfowler.com/ieeeSoftware/repetition.pdf)), and ensure you aren't building things you don't yet need ([YAGNI](https://martinfowler.com/bliki/Yagni.html)). And fewer tokens to burn.

Refactoring with TDD isn't just about cleaning up; it’s about intentional design. It allows you to use patterns like strategy or factory only when the code truly demands them. It transforms the development process from a chaotic rush into a disciplined refinement of architecture.

#### Evolutionary design

TDD enables **evolutionary design**, which allows us to defer specific implementation details until the [last responsible moment](https://javil.substack.com/p/to-decide-or-not-to-decide-thats-the-question-f186d5858aba). Instead of relying on big upfront design (BUFD), which often results in a rigid, over-engineered system that’s difficult to change when the reality of the business inevitably shifts. TDD changes this by allowing the design to emerge organically, driven by actual requirements rather than speculative ones. This approach keeps the system flexible. By making decisions when we have the most information possible, we avoid the sunk cost fallacy of an architecture that doesn't fit the evolving needs of the project.

However, evolution isn't just for new features. It applies to existing systems too. When we need to evolve **legacy code (code without tests)** to meet new business needs, creating a safety net prior to any change is non-negotiable. It’s the only way to distinguish what’s working from what isn't. Effectively, we have two options: Edit and Pray or Cover and Modify (work safely).

In software architecture, we often face moments where the correct path isn't immediately obvious. Instead of debating these choices in lengthy meetings, we can use TDD as a laboratory for **hypothesis-driven development**. In this context, the test isn't just checking for a bug or testing a new feature; it’s an experiment designed to validate whether a specific structural approach is viable. We treat our architectural assumptions as hypotheses that must be proven through implementation.

For example, imagine the team is debating whether a complex calculation logic should be a shared **internal library** or a standalone **microservice**. Writing a test suite that mimics the service call and implementing the minimum code to pass these tests, you might discover that the data contract is so large and complex that the simple service becomes a maintenance nightmare. The test fails the viability experiment before spending weeks on infrastructure. The TDD process also allows deciding in the Last Responsible Moment.

#### Reducing accidental complexity

In his seminal essay [*No Silver Bullet*](https://en.wikipedia.org/wiki/No_Silver_Bullet), Fred Brooks makes a distinction between essential complexity — the inherent difficulty of the problem we are solving — and accidental complexity, which is the difficulty we create ourselves through poor design, bloat and mismatched tools. Brooks famously argued that no single technology or management technique could provide a tenfold improvement in productivity. Instead, he advocated for growing software organically through incremental development rather than building it all at once.

TDD is perhaps the most effective tool to cultivate organic growth. By forcing us to write only the code necessary to pass a specific test, TDD acts as a filter that strains out accidental complexity before it enters the codebase. It prevents us from building unnecessary abstractions that Brooks warned would lead to the tar pit of software engineering. When we focus on the smallest possible increment, we ensure that the software remains as simple as the problem allows it to be.

#### AI agents work better with TDD

As we enter the era of AI-assisted coding, the discipline of TDD has never been more relevant. Tools like Claude Code and advanced agentic frameworks [work best](https://www.anthropic.com/engineering/claude-code-best-practices) when they have clear exit criteria. Without a test-first approach, AI agents often fall into the trap of AI Slop and [AI Smells](https://www.thoughtworks.com/insights/blog/generative-ai/tdd-and-pair-programming-the-perfect-companions-for-copilot) — generating massive blocks of code that look correct but suffer from hallucinations or hidden bloat.

By instructing an AI agent to write the test first, or by providing the test ourselves, we provide the guardrails necessary to keep the agent focused. This forces the AI to provide the minimal, functional implementation required, effectively preventing the accidental complexity that Brooks warned us about. TDD transforms the AI from an unpredictable tool into a disciplined engineering partner that iterates until it achieves a deterministic, verified result.

#### Conclusion: ATDD and the future of orchestration

Software emerged as a commercial product approximately 75 years ago evolving into an engineering discipline around 55 years ago, triggered by the [software crisis and the 1968 NATO conference](https://en.wikipedia.org/wiki/NATO_Software_Engineering_Conferences). Since that time, proven methods and methodologies have been developed to address the challenges found along the way. **Extreme Programming (XP)** encompasses many of these solutions, **TDD** standing out as a pillar. TDD lies in the balance between discipline and flexibility, control and clarity. Whether we are using tests as an experimental lab for architectural hypotheses or as a filter for accidental complexity, the goal is to grow software organically and intentionally.

Looking ahead, in a world with AI more and more present, where code agents write thousands of lines of code in a non-deterministic way, we start to see the problems that could appear in this scenario. These are problems that we’ve actually lived through in the past, and for which we likely already know the solution. [Acceptance test-driven development (ATDD)](https://agilealliance.org/glossary/atdd/) is the natural evolution for this mindset, especially as we begin to orchestrate multiple AI agents. While unit tests handle the how, ATDD focuses on the what and engineers in the why from a business perspective. By defining high-level acceptance criteria before any agent begins its work, we can orchestrate complex, multi-agent workflows with confidence. ATDD will likely become the primary interface for software engineers through acceptance tests, and our agentic teams work to make those tests green using TDD.
