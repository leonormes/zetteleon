---
aliases: []
confidence: 
created: 2025-05-26T20:29:48Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:54Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Granularity and Inherent Flaws in Mental Models
type:
uid: 
updated: 
version:
---

While essential, mental models are not perfect replicas of reality. They possess inherent characteristics and flaws:

- Varying Granularity: As mentioned, models exist at different levels of detail, from system-wide architecture down to individual lines of code. The appropriate granularity depends on the task.
- Incompleteness (All Models are Wrong): Mental models are, by necessity, simplifications of reality. They omit details to remain cognitively manageable. This simplification is what makes them useful, but it also means they are never perfectly accurate. The adage "the map is not the territory" aptly describes this; a map that included every detail of the territory would be as complex as the territory itself and therefore useless for navigation. This "necessary imperfection" is a feature, not just a bug, of mental models, as it allows for abstraction and efficient processing, provided the model is "good enough" for the task.
- Outdatedness: Software systems are constantly evolving. Mental models, however, do not automatically update with these changes. A developer might hold an outdated mental model of a module that has since been refactored, leading to incorrect assumptions and errors. One might find, for example, that a feature implementation needs to be redone because it was based on an outdated understanding of a dependent system.
- Subjectivity and Idiosyncrasy: Mental models are constructed by individuals based on their unique experiences, knowledge, and interpretations. Consequently, different developers working on the same system will inevitably form slightly different mental models.

The subjectivity of mental models presents a significant, often underestimated, challenge in collaborative software development. Because each team member carries a unique internal representation of the system, built from their personal interactions and understanding, there are bound to be divergences. These differences can be subtle or substantial, but they frequently lead to communication breakdowns, integration issues, and bugs that are "often discovered unexpectedly" when these differing assumptions collide. However, this diversity also offers an opportunity. If teams can effectively externalize, share, and reconcile their individual mental models—through practices like collaborative diagramming, robust code reviews focused on shared understanding, and clear documentation of design rationale—they can leverage these varied perspectives to build a more comprehensive and resilient collective understanding of the system.

[[Mental Models The Developer's Internal Compass]]
