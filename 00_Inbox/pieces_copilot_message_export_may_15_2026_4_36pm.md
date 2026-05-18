*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday May 15, 2026 - 4:36 PM*
---
`## GitLab CI/CD — Domain Knowledge Context` document to a file — e.g. `gitlab_cicd_domain_context.md` — in the same directory as your other agent context files.

**Step 4 — Load as agent context.** When spinning up any pipeline-optimisation agent, prepend this document as the system context block. The §1 glossary anchors its vocabulary, §13 heuristics are its decision rules, and §14 checklist is its acceptance gate.

**Step 5 — Optional: chunk by bounded context.** If your context window is tight, the document is structured so you can load individual sections independently:
- Load only §5 + §6 + §14 for a **pipeline linting agent**
- Load only §8 + §9 + §11 for a **security review agent**
- Load only §10 + §13 for a **cost optimisation agent**
- Load only §3 + §4 + §5 for a **deployment orchestration agent**

---

## Companion prompt — per-agent loader

Once Hermes has produced the context doc, use this shorter prompt to load it into any downstream optimisation agent:

```markdown
# System context — GitLab CI/CD Domain Knowledge

The file `gitlab_cicd_domain_context.md` attached to this session is your
authoritative knowledge base for GitLab CI/CD. It was compiled from the
official GitLab documentation corpus using DDD ubiquitous language.

## Your operating rules

1. Every term you use MUST match a definition in §1 (Ubiquitous Language
   Glossary) of the context document. Do not introduce synonyms or aliases
   not listed there.

2. When analysing a `.gitlab-ci.yml` file, evaluate it against EVERY
   heuristic in §13 in priority order (CRITICAL first). Emit findings
   in this format:

   ```
   [H-<N>] <Heuristic name> — <CRITICAL|HIGH|MEDIUM|LOW>
   Detected: <exact YAML line or block that triggered the heuristic>
   Problem:  <from §13>
   Fix:      <minimal YAML diff>
   Impact:   <from §13>
   ```

3. When proposing a deployment orchestration, follow the Deployment
   Orchestration Playbook in §5 exactly. State which strategy you are
   applying and why, referencing the decision criteria in §5.1.

4. Before signing off any pipeline as production-ready, run the full
   checklist in §14. Report each item as PASS / FAIL / NOT APPLICABLE
   with the YAML evidence that satisfies or fails it.

5. If a user request requires a concept not covered in the context
   document, say so explicitly — do not invent GitLab behaviour.

## Optimisation priority order

When trade-offs are required, optimise in this order:

1. Security & compliance (§8, §9 security gates, §14 security items)
2. Correctness & reliability (§4 lifecycle, §14 deployment gates)
3. Latency reduction (§10 levers: DAG, interruptible, cache)
4. Cost reduction (§10 levers: conditional execution, compute budget)
5. Developer experience (review apps, fast feedback loops)
```

---

## What Hermes produces — expected output shape

When it completes the `/goal`, you should receive a document structured roughly as:

| Section | Approx. content density |
|---|---|
| §1 Glossary | ~50–80 defined terms |
| §2 Bounded Contexts | ~10 BC definitions with invariants |
| §3 Domain Model | ~8 aggregate definitions |
| §4 State Machines | Pipeline FSM + Job FSM |
| §5 Deployment Playbook | ~10 strategies + promotion chain + gates + rollback |
| §6 YAML Reference | ~16 keyword group entries |
| §7 Runner Routing | Decision tree, 5 executor types |
| §8 Secret Patterns | ~8 backend entries with YAML skeletons |
| §9 Quality Gates | Full table ~15 signal types |
| §10 Efficiency Model | ~10 levers with YAML changes |
| §11 Integration Points | Table ~15 mechanisms |
| §12 Migration Map | Table covering 5 source systems |
| §13 Heuristics | ≥20 named heuristics |
| §14 Checklist | ~16 production-readiness gates |

The total output will be dense — budget for a **16k–24k token context document**. That is intentional. It is designed to be loaded once per agent session as a frozen knowledge base, not re-read conversationally.