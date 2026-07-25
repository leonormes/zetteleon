---
created: 2026-07-24T17:15:30+00:00
modified: 2026-07-24T17:30:56+00:00
permalink: llmeon/00-inbox/so-t-knowledge-compiler-argu
title: SoT - Knowledge Compiler (Argu
type: note
---

Research how people catalog atomic notes and zettelkasten for argumentation. I am building a knowledge compiler to read the metadata for notes and trace the links and want some ideas. I want to build my beliefs by challenging them and finding assumptions. How do logicians and philosophors organise this thinking

Good—I have enough grounding to give a substantive, actionable answer that ties the philosophical/logical traditions to concrete extensions of your compiler spec.

## What Your Spec Already Gets Right

Your Knowledge Compiler is essentially a lightweight instance of defeasible argumentation graph theory—the same territory occupied by Dung's abstract argumentation frameworks and the Argument Interchange Format (AIF). Your three primitives (claim, justification edge, axiom marker) map cleanly onto AIF's core ontology, which represents arguments as information nodes (claims/data) connected by inference, conflict, and preference relations. AIF deliberately keeps things minimal—nodes plus typed edges—and lets richer semantics (argumentation schemes, critical questions) be layered on top only when needed, which mirrors your "one marker, no ontology" discipline in §6.[^1][^2]

Your C1–C4 capabilities also line up with classic informal-logic concerns: gap detection asks "is this claim doing work with nothing beneath it," foundation audit asks "what are my real axioms," conflict detection asks "do I contradict myself or reason in a circle," and provenance asks "why do I believe this, and what falls if it's wrong." That's the whole apparatus most argument-mapping tools try to make explicit.

## The Three Traditions Worth Borrowing from

1. Toulmin's model—separates the _reason_ from the _license to use it_

Stephen Toulmin's 1958 model breaks an argument into six parts: claim, grounds (evidence), warrant (the licensing principle connecting grounds to claim), backing (support for the warrant itself), qualifier (how strongly the claim holds), and rebuttal (conditions under which it doesn't). The key insight for you: grounds and warrant are different kinds of things. Grounds are "what I have to go on"; the warrant is "why that data means the claim is true"—and warrants are often implicit, which is exactly where hidden assumptions live.[^3][^4][^5][^6]

This maps to a real gap in your v1 spec. Right now `supports` collapses grounds and warrant into one edge type. Consider distinguishing:

- `A supports B` (evidentiary grounds)
- `A warrants B` or reuse `depends_on` for the licensing principle a claim relies on to make its inferential leap valid

Toulmin's "name your assumptions" discipline is literally your C1/C2 capability, just articulated 70 years earlier—an argument is only as strong as its weakest, most-often-unstated warrant.[^7]

2. Walton's argumentation schemes + critical questions—the actual "challenge my beliefs" engine

This is the most directly useful piece for what you're describing wanting to do (build beliefs by challenging them, finding assumptions). Douglas Walton catalogued ~29 recurring patterns of everyday reasoning—argument from expert opinion, argument from analogy, practical reasoning, argument from position to know, etc.—each with a fixed premise structure and a fixed set of critical questions that probe its weak points.[^8][^9]

For example, "argument from expert opinion" has six standard critical questions: how credible is the expert, are they actually in the relevant field, did they really assert this, are they trustworthy, is it consistent with other experts, is it evidence-backed. Critically, these arguments are defeasible/presumptive—they hold provisionally until a critical question surfaces a weakness, at which point the burden of proof shifts back to whoever made the claim.[^9][^8]

This is a natural extension for your compiler:

- Add an optional `scheme` field on claim nodes (e.g. `scheme: expert_opinion`, `scheme: analogy`, `scheme: practical_reasoning`).
- The compiler doesn't validate truth—it just knows which critical questions apply to that scheme and can surface them as prompts: "You haven't addressed CQ2 (is E actually an expert in this domain?) for this claim." That's a report-only, opt-in feature exactly in the spirit of your "compiler proposes, never rewrites" guard.
- This gives you a genuine assumption-finder: unanswered critical questions ARE the smuggled assumptions.

3. IBIS—questions as first-class nodes, not just claims

The Issue-Based Information System (Kunz \& Rittel, 1970s), used for "wicked problems," structures deliberation around three node types: Issues (questions), Positions (candidate answers to an issue), and Arguments (pro/con reasons for a position). Tools like Compendium and Argdown implement this. The useful bit you're missing: your graph currently only has claims and edges between claims—there's no explicit node for "the open question this claim is trying to resolve." Adding an `issue`/`question` node type (or even just a lightweight `raises_question` edge) lets the compiler report open issues with no resolved position—a different and complementary gap signal to C1.[^10]

## A Structural Idea Worth Stealing: Rebuttal Vs Undercut Vs Undermine

Modern argumentation theory (following Pollock, and formalized further in AIF/ASPIC+ literature) distinguishes three ways an argument can be attacked, which your current single `contradicts` edge conflates:

| Attack type | What it targets | Example |
|:-- |:-- |:-- |
| Rebut | The conclusion itself | "B is false because C is true and C implies not-B" |
| Undercut | The warrant/inference link | "Even granting the grounds, they don't actually support B here" |
| Undermine | A premise/ground | "One of the grounds for B is itself false" |

Your spec already flags a distinct `rebuts` vs `undercuts` split as a candidate future edge type in §4—this is exactly that, and it's well-precedented rather than novel. Undercut edges are the sharpest tool for "finding assumptions," since they attack the warrant without needing to dispute any fact.

## Concrete Additions for Your v1–v2 Roadmap

- v1 (gap/foundation audit): keep as-is, but consider letting a claim optionally cite its `scheme` so the compiler can print unanswered critical questions alongside the gap report—this operationalizes "challenging my beliefs" mechanically rather than requiring you to remember to do it.
- v2 (conflict detection): split `contradicts` into `rebuts` (conclusion-level) and `undercuts` (warrant-level) if you find in practice that one symmetric edge isn't expressive enough—your spec already anticipates this.
- v3 (provenance): when printing the `Why(X)` justification tree, tag each edge with whether it's grounds-type or warrant-type (Toulmin), so the printed tree visually distinguishes "this is evidence" from "this is the licensing principle"—much easier to spot a shaky warrant when it's visually distinct from shaky evidence.

None of this requires abandoning your minimalism—Toulmin, Walton, and IBIS all converge on the same lesson your spec already states: keep the node/edge vocabulary small, but make sure the _few_ types you have cleanly separate evidence, inference-license, and conflict, because that's where hidden assumptions hide.

<span style="display:none">[^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30]</span>

<div align="center">⁂</div>

[^1]: <https://en.wikipedia.org/wiki/Argument_Interchange_Format>
[^2]: <https://cmna.csc.liv.ac.uk/CMNA7/papers/Rahwan.pdf>
[^3]: <https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html>
[^4]: <https://www.utsa.edu/twc/documents/Toulmin_Model_of_Argumentation.pdf>
[^5]: <https://courses.lumenlearning.com/suny-jefferson-collegecomposition/chapter/toulmins-argument-model/>
[^6]: <https://my.cgu.edu/writing-rhetoric/wp-content/uploads/sites/9/2021/11/CGU-CWR-Toulmin-Method-of-Argumentation.pdf>
[^7]: <https://www.ciris.info/learningcenter/toulmins-model/>
[^8]: <https://cgi.csc.liv.ac.uk/~katie/waltonFest10.pdf>
[^9]: <https://ecampusontario.pressbooks.pub/criticalthinking1234/chapter/__unknown__-29/>
[^10]: <https://en.wikipedia.org/wiki/Issue-based_information_system>
[^11]: <https://ics.uci.edu/~alspaugh/cls/shr/argument.html>
[^12]: <https://www.sjsu.edu/writingcenter/docs/handouts/Toulmin> Model of Argumentative Writing.pdf
[^13]: <https://www.nature.com/articles/s41599-024-03151-w>
[^14]: <https://www.youtube.com/watch?v=HALSBMQlSqU>
[^15]: <https://open.ocolearnok.org/englishcomposuokc/chapter/using-the-toulmin-system-to-build-an-argument/>
[^16]: <https://ca.indeed.com/career-advice/career-development/toulmin-model>
[^17]: <https://www.statisticssolutions.com/expanding-on-the-basic-toulmin-model-when-writing-a-literature-review/>
[^18]: <https://www.youtube.com/watch?v=8g6R9dRtAww>
[^19]: <https://eight2late.wordpress.com/wp-content/uploads/2011/07/mapping-project-dialogues-final-version.pdf>
[^20]: <http://www.arg-tech.org/wp-content/uploads/2011/09/aif-spec.pdf>
[^21]: <https://www.arg-tech.org/people/chris/publications/2008/comma2008-aif+.pdf>
[^22]: <https://webspace.science.uu.nl/~prakk101/pubs/aifsem12.pdf>
[^23]: <https://www.simonwells.org/assets/papers/reed_2010_tech.report.pdf>
[^24]: <https://jmvidal.cse.sc.edu/library/chesnevar06a.pdf>
[^25]: <http://arg.tech/people/chris/publications/2010/ker.pdf>
[^26]: <https://usiena-air.unisi.it/retrieve/e0feeaa8-a949-44d2-e053-6605fe0a8db0/A111.2_Lumer_Walton%E2%80%99sArgumentationSchemes_Print.pdf>
[^27]: <http://ndl.ethernet.edu.et/bitstream/123456789/13285/1/165.Douglas> Walton.pdf
[^28]: <https://link.springer.com/chapter/10.1007/978-3-540-78915-4_6>
[^29]: <https://www.reasoninglab.com/patterns-of-argument/argumentation-schemes/waltons-argumentation-schemes/>
[^30]: <https://www.scribd.com/document/364012515/Argumentsss-pdf>
