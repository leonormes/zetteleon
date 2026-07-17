---
aliases: [Note metadata schema, ProdOS frontmatter specification, TAC Schema]
conformant: false
created: 2026-04-08T18:00:00+00:00
modified: 2026-07-17T08:28:11+00:00
non_conformance_reason: Bulk inferred type. Needs review.
permalink: llmeon/00-inbox/prod-os-tac-plan
see_also: ["[[CLAUDE.md]]", "[[Typed-Answer-Contract-RAG]]"]
tags: [8A, prodos/schema, topic/pkm]
title: Typed-Answer-Contract-RAG
type: sot
---

## Typed Answer Contract (TAC): RAG Hallucination Prevention via Structured Output

> TDS Article: _Stop Returning Text from RAG: The Typed Answer Contract That Prevents Hallucination_ (July 4, 2026)[^1]

### Executive Summary

The article argues that returning free-form text from a RAG pipeline is the _primary architectural source_ of hallucinations in production systems—not just bad retrieval. The fix is to replace the "answer in prose" step with a Typed Answer Contract (TAC): a strict Pydantic/JSON Schema that the LLM must populate. If the output doesn't conform to the schema, the pipeline rejects it. This transforms the LLM from a creative writer into a deterministic data extractor—verifiable, testable, and integrable directly into downstream systems.[^2][^3]

### The Core Problem: Unlimited Degrees of Freedom

Standard RAG pipelines end with an instruction like _"Based on the context, answer the question."_ That gives the model unlimited latitude to:

- Blend pre-training knowledge with retrieved context, overriding what the documents actually say
- Sound confident while being factually wrong—_hallucination camouflage_ in prose[^3]
- Produce output downstream systems (CRM, ERP, workflows) cannot parse without error-prone regex or another LLM call[^2]

Production debugging data cited in the article estimates ~30% of hallucinations are not due to bad retrieval but due to the LLM generating content with no grounding in the provided text—because fluency is rewarded over accuracy in training. A block of free-form text hides false dates, wrong prices, or fabricated legal clauses in plain sight.[^4][^5]

### The Solution: Schema is the Contract

A TAC reframes the generation step as a structured data extraction task. Instead of asking _"What does this document say?"_, the pipeline asks the model to populate a Pydantic model. Each field in the schema is a discrete, checkable question:[^1][^3]

```python
from pydantic import BaseModel, Field

class RAGAnswer(BaseModel):
    answer: str = Field(description="Answer derived ONLY from context.")
    is_definitive: bool = Field(description="True if context contains a clear answer.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence from 0 to 1.")
    source_ids: list[str] = Field(description="Chunk IDs used as evidence.")
    missing_info: bool = Field(description="True if context is insufficient.")
```

The `missing_info` field is the critical innovation here: it replaces the LLM's vague "I don't know" with a programmatic boolean. If `missing_info is True`, the pipeline _never surfaces the answer to the user_. If `confidence < 0.6`, a disclaimer is appended automatically. The schema enforces honesty via structure, not via prompting.[^4][^3]

#### Evidence Fields for Zero-Hallucination Extraction

The article recommends adding an `evidence` field to each extracted data point, forcing the model to cite the exact source quote. If no direct quote exists, the field stays empty:[^3]

```python
class EvidenceField(BaseModel):
    value: str
    source_quote: str = Field(description="Direct snippet from context proving this value.")
    page_number: int
```

### Implementation: The `instructor` Library

Enforcement relies on constrained decoding at the API level. Every major LLM provider as of 2026 supports structured output modes—OpenAI `response_format` with JSON Schema, Anthropic Tool Use, Gemini `response_mime_type`. The recommended library is `instructor` (v3.x), which wraps any LLM client and enforces Pydantic validation with automatic retry:[^6][^4][^2]

```python
import instructor
from openai import OpenAI

client = instructor.patch(OpenAI())

def ask_rag(question: str, context: str) -> RAGAnswer:
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=RAGAnswer,
        messages=[
            {"role": "system", "content": "Produce structured answers. Follow the contract strictly."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
```

`instructor` automatically converts the Pydantic model to a JSON schema, passes it as a tool definition, validates the response, and retries with the validation error message if it fails—achieving 95%+ correction on first retry. For self-hosted infrastructure (vLLM, llama.cpp), constrained decoding enforces JSON grammar at the token-generation level, making non-conforming outputs structurally impossible.[^7][^6]

### Text-based RAG vs. Typed Answer Contract

| Feature | Text-based RAG | Typed Answer Contract |
|---|---|---|
| Output format | Natural language prose | Validated JSON / Pydantic object |
| Validation | Manual review / LLM-eval | Schema-level, automated |
| Hallucination risk | High—hidden in text | Low—constrained by types and evidence fields |
| Downstream integration | Requires regex / secondary parsing | Native programmatic integration |
| Testability | Hard to unit test | Unit-testable like any typed object |
| Auditability | Weak—no source linkage | Strong—every field tied to a chunk ID |
| Failure handling | Silent wrong answer | Pipeline rejects or flags automatically |

### Validation and Completeness Checks

The article goes beyond schema enforcement and introduces two additional safety layers:[^2]

Self-assessment fields—Confidence scores, extraction methods, and `evidence_conflict` flags are embedded directly in the schema. This turns the LLM into an active diagnostic tool: it signals whether retrieved context was complete or whether contradictions were found, enabling the pipeline to trigger a broader retrieval search before presenting results.[^2]

Overlap page verification—Because LLMs can only evaluate what they see, a truncated document may _look_ complete. The architecture pulls an additional overlap page alongside the primary retrieved context. While the model generates its response, the pipeline checks the trailing page to confirm whether lists or clauses were cut off artificially. If continuation content is found, the partial result is rejected and retrieval is retried.[^2]

### Claimed Results and Validation

The article's companion implementation report for a legal document Q&A system cites hallucination rate dropping from 12% to 1.7%—not because the model improved, but because ~30% of outputs were rejected before reaching users. This is independently supported by peer-reviewed research (arXiv, April 2024) showing that structured output RAG significantly reduces hallucinations and improves generalization in out-of-domain settings.[^9][^4]

The approach is further corroborated by AWS Bedrock's February 2026 structured output announcement, which frames constrained decoding as the solution to JSON generation failures that "routinely break integration" in production. The `instructor` library underpinning the implementation is independently validated in production DevOps environments, consistently handling multi-provider LLM output with automatic retry.[^10][^11][^6]

What the article does _not_ claim:

- TAC is not a complete fix—broken retrieval still produces broken answers within a valid schema[^4]
- Schema complexity is a genuine trade-off; schemas with 15+ nested fields degrade model performance[^4]
- Self-assessed confidence fields can themselves be overconfident; secondary validation or a second LLM call is recommended for critical fields[^4]

### What This Offers You (Leon—DevOps / AI Pipeline Context)

Given your Go learning track, infrastructure automation focus, and LLM prompt engineering work, the TAC pattern is highly applicable:

#### Immediate Applications

- Infrastructure document Q&A—Any internal RAG over runbooks, Terraform docs, or Helm chart references can return structured, auditable objects instead of chatty prose. `kubectl` or ArgoCD context queries become programmatically parseable.
- AI-assisted triage pipelines—Alerts or incident summaries can return `{ severity: Enum, affected_services: List[str], confidence: float, source_chunk_id: str }` rather than paragraphs your on-call automation cannot parse.
- Go TDD compatibility—Typed JSON outputs map cleanly to Go structs. Schema-first design means you define the expected output as a Go type, test it, and assert against it—exactly aligning with your TDD workflow.

#### Tooling Stack

- Python: `instructor` + `pydantic v2`—lowest friction path[^6][^10]
- Self-hosted / open-source models: `vLLM` or `llama.cpp` with grammar-constrained decoding—no proprietary API required[^7]
- Multi-provider failover: n1n.ai or LangChain's `with_structured_output` for model-agnostic enforcement[^12][^3]

#### ADHD-workflow Fit

The pattern removes ambiguity from the _output_ of AI tools you use in your own workflow. A structured response with `confidence`, `missing_info`, and `source_ids` gives you immediate, scannable signal—no need to re-read a paragraph to judge if an AI answer is trustworthy.

### Key Takeaway

The Typed Answer Contract is not a novel concept, but the article synthesises it into a clear, production-validated pattern: treat LLM generation as a typed data extraction step, not a text completion step. The schema is the contract between document, model, and downstream system. Structure gives you the power to programmatically check for truth—something unstructured prose will never allow.[^4][^2]

---

### References

1. [Stop Returning Text from RAG: The Typed Answer Contract That Prevents Hallucination](https://towardsdatascience.com/stop-returning-text-from-rag-the-typed-answer-contract-that-prevents-hallucination/) - Enterprise Document Intelligence [Vol.1 8A] - The schema is the contract: every field is a question…
2. [Typed Answer Contract Prevents Hallucination in RAG Systems](https://hyper.ai/en/stories/24f099ae0e9b0af55b0edc9669b4eccf) - Build the Future of Artificial Intelligence
3. [Implementing Typed Answer Contracts to Prevent Hallucination](https://explore.n1n.ai/blog/stop-returning-text-from-rag-typed-answer-contracts-2026-07-04) - Learn why raw text responses are the weakest link in your RAG pipeline and how to implement schema-b…
4. [Prevent RAG hallucinations with typed answer contracts: complete guide](https://ai-manual.ru/article/typed-answer-contracts-the-only-way-to-stop-rag-hallucinations-with-code/) - Learn how to use typed answer contracts (Pydantic + structured generation) to prevent RAG hallucinat…
5. [Դադարեցրեք տեքստային պատասխանները RAG-ում. տիպայնացված պայմանագիր՝ հալյուցինացիաները կանխելու համար](https://www.aoodax.com/hy/blog/stop-returning-text-from-rag-prevent-ai-hallucination-via-typed-answers-mr6sgurk) - Դադարեցրեք տեքստային պատասխանները RAG-ից. մուտքագրված պատասխանի պայմանագիր, որը կանխում է հալյուցինա…
6. [LLM Output Validation with Instructor + Pydantic in Production](https://devopsboys.com/blog/llm-output-validation-instructor-pydantic-production-2026) - LLMs return unpredictable text. Instructor + Pydantic turns that into validated, typed Python object…
7. [LLM Structured Outputs: Schema Validation for Real Pipelines (2026)](https://collinwilkins.com/articles/structured-output) - If you're running models on your own infrastructure (vLLM, llama.cpp, TGI), constrained decoding eng…
8. [Stop RAG Hallucinations: Force Your Bot to Cite Sources](https://theaiinternship.com/blog/stop-rag-hallucinations-citations/) - RAG reduces hallucinations but does not eliminate them. Structured output and citation enforcement g…
9. [Reducing hallucination in structured outputs via Retrieval ... - arXiv](https://arxiv.org/abs/2404.08189) - A common and fundamental limitation of Generative AI (GenAI) is its propensity to hallucinate. While…
10. [Learning](https://python.useinstructor.com/learning/) - A lightweight library for structured outputs with LLMs.
11. [Structured outputs on Amazon Bedrock: Schema-compliant AI ... - AWS](https://aws.amazon.com/blogs/machine-learning/structured-outputs-on-amazon-bedrock-schema-compliant-ai-responses/) - Today, we're announcing structured outputs on Amazon Bedrock—a capability that fundamentally transfo…
12. [9. RAG with Structured Outputs — JSON Mode + Pydantic](https://idir-mellaz.fr/structured-outputs-pydantic/) - Force your RAG pipeline to always return valid, typed data. Combine OpenAI JSON mode, Pydantic v2 sc…

## ProdOS TAC Plan: Typed Answer Contracts for Your Obsidian Vault

> Goal: Stop LLMs from making non-conformant edits to your vault by treating every LLM operation on a note as a typed data extraction/writing contract—not a free-text generation task. The schema _is_ the rule. If an LLM can't fill the schema cleanly, it must flag `conformant: false` and do nothing.

### Why Your Vault Needs This Now

Your vault currently has a critical mismatch: your ProdOS system is highly designed (five note types, the CRPE cycle, four-tier GTD architecture, the Writing-to-Think pipeline) but the LLMs operating on it have _no machine-enforceable knowledge of that design_. Each LLM session re-invents your conventions. The result is drift: notes with missing `type` fields, inconsistent frontmatter, writing stages collapsed into each other, and free-prose outputs where structured Zettel atoms should live.[^1][^2]

The TAC pattern from the previous session resolves this: every LLM action on the vault is expressed as a Pydantic/JSON schema the model must populate. Non-conformant output is rejected before it touches a file. The vault becomes as schema-enforced as a Kubernetes manifest.

### Phase 1—Define the Schema Layer (Week 1)

#### 1.1 The Five Note Type Contracts

Each of your five canonical note types needs its own TAC. These are the ground truth schemas. Any LLM creating or editing a note must return one of these objects—never raw markdown.[^1]

`ClaimNote`

```python
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List

class EpistemicStatus(str, Enum):
    HIGH    = "high"       # I'm confident, I have evidence
    MEDIUM  = "medium"     # Plausible, needs more evidence
    LOW     = "low"        # Speculative, hunch
    UNKNOWN = "unknown"

class ClaimNote(BaseModel):
    type: Literal["claim"]
    title: str = Field(description="A single declarative sentence — the claim itself.")
    proposition: str = Field(description="The claim in one clear sentence, beginning with a verb or noun phrase. NOT a topic.")
    epistemic_status: EpistemicStatus
    evidence_links: List[str] = Field(description="Wikilinks to Evidence notes that support this claim.")
    contradicts: List[str] = Field(description="Wikilinks to Claim notes this contradicts, if any.")
    project_name: Optional[str]
    tags: List[str]
    conformant: bool = Field(description="False if this note cannot be cleanly typed. Do NOT write to vault if False.")
    non_conformance_reason: Optional[str]
```

`ConceptNote`

```python
class ConceptNote(BaseModel):
    type: Literal["concept"]
    title: str = Field(description="The term or distinction being defined.")
    definition: str = Field(description="A single-paragraph definition in your own words.")
    distinguishes_from: List[str] = Field(description="Related terms this concept is NOT, with wikilinks.")
    used_in_claims: List[str] = Field(description="Wikilinks to Claim notes that use this concept.")
    tags: List[str]
    conformant: bool
    non_conformance_reason: Optional[str]
```

`EvidenceNote`

```python
class EvidenceNote(BaseModel):
    type: Literal["evidence"]
    title: str
    source_quote: str = Field(description="The exact quote, data point, or benchmark. Direct extraction only.")
    source_reference: str = Field(description="Author, book/URL, date.")
    supports_claims: List[str] = Field(description="Wikilinks to Claim notes this evidence supports.")
    confidence: float = Field(ge=0.0, le=1.0, description="How strongly this evidence supports the claim(s).")
    conformant: bool
    non_conformance_reason: Optional[str]
```

`QuestionNote`

```python
class QuestionNote(BaseModel):
    type: Literal["question"]
    title: str = Field(description="The question itself — must end with '?'.")
    tension: str = Field(description="What belief or observation generates this question?")
    candidate_answers: List[str] = Field(description="Possible answers; can be empty.")
    related_claims: List[str]
    tags: List[str]
    conformant: bool
    non_conformance_reason: Optional[str]
```

`ProcedureNote`

```python
class ProcedureNote(BaseModel):
    type: Literal["procedure"]
    title: str = Field(description="'How to [do X]' format.")
    trigger: str = Field(description="When is this procedure invoked?")
    steps: List[str] = Field(description="Ordered, physical, verb-first steps.")
    verification: str = Field(description="How do you know it worked?")
    tags: List[str]
    conformant: bool
    non_conformance_reason: Optional[str]
```

#### 1.2 The Frontmatter Contract

Any LLM that touches frontmatter must return a `FrontmatterContract` object. This is the _shared envelope_ all five note types inherit:

```python
class FrontmatterContract(BaseModel):
    title: str
    type: Literal["claim", "concept", "evidence", "question", "procedure", "protocol", "map", "journal", "project", "sot"]
    project_name: Optional[str]
    project_category: Optional[str] = Field(description="e.g. prodos, devops, personal")
    project_status: Optional[Literal["active", "someday", "archived"]]
    status: Optional[Literal["draft", "stable", "evergreen", "stale"]]
    tags: List[str]
    permalink: Optional[str]
    conformant: bool
    non_conformance_reason: Optional[str]
```

> Rule: If `type` is `null` (as it currently is in many notes), the LLM must _infer and assign_ the correct type—or set `conformant: false` and leave the note untouched.[^3][^4]

### Phase 2—Define the Action Contracts (Week 1–2)

Every LLM _action_ on the vault also needs a typed output. This is separate from the note schema—it governs what the agent is _allowed to do_.

#### 2.1 Vault Action Enum

```python
class VaultAction(str, Enum):
    CREATE_NOTE       = "create_note"        # Writes a new file
    EDIT_FRONTMATTER  = "edit_frontmatter"   # Updates YAML only; never touches body
    EDIT_BODY         = "edit_body"          # Updates body only; never touches frontmatter
    MOVE_NOTE         = "move_note"          # Changes location in vault folder structure
    LINK_NOTES        = "link_notes"         # Adds wikilinks to a note's body
    DELETE_NOTE       = "delete_note"        # Moves to Trash — requires reason
    CLASSIFY_NOTE     = "classify_note"      # Returns type classification; no write
    AUDIT_NOTE        = "audit_note"         # Returns conformance report; no write
    PROCESS_DUMP      = "process_dump"       # Reads dump.md; routes items; no body edit
    NOOP              = "noop"               # LLM must do nothing; logs reason
```

#### 2.2 The Action Contract

```python
class VaultActionContract(BaseModel):
    action: VaultAction
    target_path: str = Field(description="Vault-relative path, e.g. '30_Library/SoT/my-note.md'")
    note_type: Optional[str] = Field(description="The TAC note type being created/modified.")
    payload: dict = Field(description="The typed note object (ClaimNote, etc.) or frontmatter dict.")
    dry_run: bool = Field(default=True, description="Always True unless user explicitly approves write.")
    conformant: bool
    non_conformance_reason: Optional[str]
    requires_human_review: bool = Field(description="True if confidence < 0.7 or note type is ambiguous.")
```

> Critical guardrail: `dry_run` defaults to `True`. No LLM writes to the vault unless the returned contract has `dry_run: False` AND `conformant: True`. You confirm the diff; Hermes executes. This is your schema-level protection against the non-conformant edits you're experiencing now.

### Phase 3—The Writing Pipeline Contracts (Week 2)

Your five-stage Writing-to-Think pipeline is already well-defined. The problem is LLMs collapse stages or skip them. Each stage gets a contract that _gates_ progression.[^5][^6][^7][^8][^9]

```python
class WritingStage(str, Enum):
    STAGE_1_GENERATE  = "generate"   # Goldberg Layer — raw dump
    STAGE_2_CLARIFY   = "clarify"    # Zinsser Layer — editorial pass
    STAGE_3_UNDERSTAND = "understand" # Writing to Learn — reflection
    STAGE_4_CONNECT   = "connect"    # Zettelkasten — deliberate linking
    STAGE_5_SYNTHESISE = "synthesise" # Outcome Layer — structure note

class WritingStageContract(BaseModel):
    current_stage: WritingStage
    next_stage: Optional[WritingStage]
    source_note_path: str
    output_note_path: Optional[str]
    stage_complete: bool = Field(description="True only when stage criteria are fully met.")
    computed_truth: Optional[str] = Field(description="Stage 3+ only: the single core insight extracted.")
    links_added: Optional[List[str]] = Field(description="Stage 4 only: wikilinks that were added.")
    conformant: bool
    non_conformance_reason: Optional[str]
    gate_passed: bool = Field(description="False blocks progression. LLM cannot advance stages unilaterally.")
```

Gate criteria per stage (LLM must verify before setting `gate_passed: True`):

| Stage | Gate Condition |
|---|---|
| Generate → Clarify | Raw body is > 100 words, `type = null` still |
| Clarify → Understand | Active verbs used, no qualifiers, body < 300 words |
| Understand → Connect | `computed_truth` field is populated |
| Connect → Synthesise | At least 2 `links_added` to existing notes |
| Synthesise | Structure note created with `type = map` or merged into existing |

### Phase 4—The Vault Audit Contract (One-time, Week 2)

Before building TAC infrastructure, you need a current-state audit. This is a _read-only_ contract—it never writes.

```python
class NoteAuditResult(BaseModel):
    path: str
    inferred_type: Optional[str]
    current_type_value: Optional[str]
    has_missing_frontmatter_fields: List[str]
    is_type_null: bool
    is_orphaned: bool = Field(description="True if no backlinks and no outbound links.")
    writing_stage: Optional[WritingStage]
    recommended_action: str
    conformant: bool

class VaultAuditContract(BaseModel):
    total_notes: int
    notes: List[NoteAuditResult]
    type_null_count: int
    orphaned_count: int
    pipeline_stalled_count: int
    recommended_priority_order: List[str] = Field(description="Paths to fix first, most impactful.")
```

### Phase 5—Hermes Integration (Week 3)

Once schemas exist, Hermes (your CoS agent) enforces them. Every Obsidian MCP call goes through a TAC wrapper:

```
User says "Process my dump"
        ↓
Hermes reads dump.md
        ↓
For each item → returns VaultActionContract (dry_run=True)
        ↓
You see a diff of proposed actions (structured, not prose)
        ↓
You approve → Hermes re-calls with dry_run=False
        ↓
Obsidian MCP writes the conformant note
```

For Hermes's system prompt, add:

```
You are operating under the ProdOS Typed Answer Contract (TAC) system.
Every output that touches the vault MUST be a VaultActionContract JSON object.
You MUST NOT return prose edits to vault notes.
If you cannot produce a conformant contract, return action=NOOP with a reason.
dry_run is ALWAYS True unless Leon explicitly says "confirm write".
```

### Implementation Roadmap

| Week | Action | Output |
|---|---|---|
| 1 | Define all 5 note TACs + FrontmatterContract | `tac/schemas/note_types.py` |
| 1 | Define VaultActionContract + VaultAction enum | `tac/schemas/actions.py` |
| 2 | Run VaultAuditContract on full vault (LLM analysis prompt below) | `tac/audit/vault_audit_YYYYMMDD.json` |
| 2 | Add WritingStageContracts to Writing Pipeline docs | Updated Stage 1–5 notes |
| 3 | Update Hermes system prompt with TAC enforcement block | `hermes/system_prompt.md` |
| 3 | Wire Obsidian MCP calls through TAC wrapper | `hermes/vault_client.py` |
| 4 | Backfill `type` field on all `type: null` notes using AuditContract | Batch write session |

### Vault Analysis Prompt

> Use this prompt verbatim with any LLM that has Obsidian MCP access to your vault. It performs a read-only audit and returns the structured data you need to build your TAC schemas. Paste it directly into Hermes, Claude, or any agent with vault access.

```
## ProdOS Vault Analysis — TAC Schema Discovery

You are performing a READ-ONLY structural audit of an Obsidian vault at:
/Volumes/DAL/Zettelkasten/LLMeon

DO NOT modify any files. DO NOT create any notes. This is an analysis-only session.

### Your Task

Produce a structured JSON report conforming to the VaultAuditContract schema below.
Return ONLY the JSON object — no prose, no markdown wrapping.

### VaultAuditContract Schema

{
  "total_notes": <int>,
  "type_null_count": <int>,  // notes where frontmatter type is null or missing
  "orphaned_count": <int>,   // notes with no inbound or outbound wikilinks
  "pipeline_stalled_count": <int>,  // notes in a writing stage with no progression
  "notes": [
    {
      "path": "<vault-relative path>",
      "title": "<note title>",
      "current_type_value": "<value of 'type' field in frontmatter, or 'MISSING'>",
      "inferred_type": "<one of: claim | concept | evidence | question | procedure | protocol | map | journal | project | sot | unknown>",
      "inferred_type_confidence": <0.0-1.0>,
      "inferred_type_reasoning": "<one sentence explaining your classification>",
      "has_missing_frontmatter_fields": ["<field1>", "<field2>"],
      "is_orphaned": <true|false>,
      "estimated_writing_stage": "<one of: generate | clarify | understand | connect | synthesise | complete | not_applicable>",
      "recommended_action": "<one of: assign_type | fix_frontmatter | link_to_notes | advance_pipeline | merge_into | delete | no_action>",
      "recommended_action_detail": "<one sentence describing exactly what should change>",
      "conformant": <true|false>
    }
  ],
  "recommended_priority_order": ["<path1>", "<path2>", "..."],  // top 10 highest-impact fixes
  "schema_gaps_detected": [
    "<description of any note pattern that does NOT fit the 5 canonical types>"
  ],
  "frontmatter_inconsistencies": [
    "<description of any frontmatter field used inconsistently across notes>"
  ],
  "audit_confidence": <0.0-1.0>,
  "audit_limitations": "<what you could not assess with the available data>"
}

### Context: The ProdOS Note Taxonomy

The vault uses exactly 5 knowledge note types:
- claim: A verifiable proposition/belief. Title is a declarative sentence.
- concept: A definition or distinction. Title is a term.
- evidence: A source quote, data point, or benchmark. Must reference a source.
- question: An unresolved tension. Title ends with '?'.
- procedure: Repeatable know-how. Title begins with 'How to'.

Administrative note types (not knowledge nodes):
- map: Index/MOC notes. Entry points only.
- journal: Daily notes, HEAD notes, raw capture.
- project: Project outcome notes in 200_projects/.
- sot: Source-of-Truth notes (e.g. SoT-Work-Open-Loops).

### Context: The Folder Structure

- 00_Inbox/: Raw capture. Notes here are temporary.
- 01_journals/: Daily notes. Not knowledge nodes.
- 20_Thinking/: HEAD notes — temporary working space. Nothing should persist here.
- 30_Library/SoT/: Source-of-Truth notes.
- 30_Library/200_projects/: Project notes.
- 30_Library/ (other): Stable knowledge notes (claim/concept/evidence/question/procedure).

### Analysis Instructions

1. List every note file in the vault.
2. For each note, read the frontmatter and first 200 words of body.
3. Classify it using the taxonomy above.
4. Identify conformance issues: missing type, wrong type, missing required fields.
5. Flag orphaned notes (no links in or out).
6. Identify notes stuck in the Writing-to-Think pipeline (Stages 1–5) that have not progressed.
7. Produce the JSON report. No other output.

### Hard Constraints

- Return ONLY valid JSON. No prose before or after.
- Do NOT suggest edits. Do NOT make changes. Observe and report.
- If you cannot classify a note, set inferred_type = "unknown" and inferred_type_confidence = 0.0.
- If vault access is unavailable, return: {"error": "vault_inaccessible", "reason": "<detail>"}
```

### What You Get From This

| Problem You Named | TAC Solution |
|---|---|
| LLMs making non-conformant edits | `conformant: false` → `action: NOOP`—nothing writes |
| Inconsistent frontmatter (`type: null`) | FrontmatterContract enforces required fields on every write |
| Different LLMs ignoring your conventions | Schema is the contract, not a prompt—structurally enforced |
| Notes drifting between writing stages | WritingStageContract gates progression |
| Hermes producing prose instead of vault actions | System prompt enforces VaultActionContract return type |
| "Mess of ideas"—unclear note classification | VaultAuditContract gives you a full classified inventory |

---

### References

1. [PKM-should-probably-be-proposition-centred-not-topic-centred.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/a5969dd7-1e33-405d-80a6-2ff79eff5525/PKM-should-probably-be-proposition-centred-not-topic-centred.md) - ---
created: 2026-04-23T15:27:21+00:00
modified: 2026-07-04T10:51:26+00:00
permalink: llmeon/30-libr…

2. [ProdOS-System-Overview-and-Development-Progress.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/7b52f64a-8c8c-4494-b801-459bf8c68f3c/ProdOS-System-Overview-and-Development-Progress.md) - ---
created: 2026-04-08T14:02:05+00:00
modified: 2026-07-04T10:51:25+00:00
permalink: llmeon/30-libr…

3. [How-to-Use-the-prodOS-Workflow.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/bb23569e-ae93-4378-8790-9026c4db6d3b/How-to-Use-the-prodOS-Workflow.md) - ---
created: 2026-05-26T13:49:47+00:00
modified: 2026-07-04T10:51:29+00:00
permalink: llmeon/30-libr…

4. [SoT-Work-Open-Loops.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/6a1b6781-fd1e-4bc9-b1cb-b65a062fe1f8/SoT-Work-Open-Loops.md) - ---
created: 2026-05-26T09:39:03+00:00
last_updated: 2026-06-08 10:01:27+01:00
modified: 2026-07-04T…

5. [Stage-2-Clarify-The-On-Writing-Well-Layer.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/4f754f93-0705-4d1a-a2da-2569e9308bc0/Stage-2-Clarify-The-On-Writing-Well-Layer.md) - ---
aliases: [Editorial Stage, Zinsser Layer]
created: 2025-12-04T12:23:40+00:00
modified: 2026-07-0…

6. [Stage-1-Generate-The-Goldberg-Layer.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/490d6ddc-0033-4273-930b-9c89fde34cec/Stage-1-Generate-The-Goldberg-Layer.md) - ---
aliases: [Goldberg Layer, Timed Writing]
created: 2025-12-04T12:23:40+00:00
modified: 2026-07-04…

7. [Stage-3-Understand-The-Writing-to-Learn-Layer.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/8eef2b72-4787-42f8-9f4f-1a86f5f66e2a/Stage-3-Understand-The-Writing-to-Learn-Layer.md) - ---
aliases: [Reflection Layer, Writing to Learn]
created: 2025-12-04T12:23:40+00:00
modified: 2026-…

8. [Stage-5-Synthesise-The-Outcome-Layer.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/35266006-6c69-471a-a944-8784aaa959c8/Stage-5-Synthesise-The-Outcome-Layer.md) - ---
aliases: [Outcome Layer, Synthesis Stage]
created: 2025-12-04T12:23:40+00:00
modified: 2026-07-0…

9. [Stage-4-Connect-The-Zettelkasten-Layer.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7869211/ef53cc81-7084-46fc-8907-cf566b5b9ee6/Stage-4-Connect-The-Zettelkasten-Layer.md) - ---
aliases: [Linking Stage, Zettelkasten Layer]
created: 2025-12-04T12:23:40+00:00
modified: 2026-0…

This is an exceptionally solid approach. The idea of using Typed Answer Contracts (TAC) is practically bulletproof for your use cases because it directly addresses the fundamental flaw of generative models: their infinite degrees of freedom. By treating LLM outputs as strict data extraction tasks rather than creative writing exercises, you eliminate the "hallucination camouflage" that text provides. Whether applied to a production RAG pipeline or your ProdOS Obsidian vault, enforcing a rigid schema ensures that if an LLM cannot definitively answer a prompt or properly format a note, it fails safely and predictably.

Here is a simplified, foundational Markdown wiki to establish the core concepts.

## Wiki: Typed Answer Contracts (TAC)

Typed Answer Contracts (TAC) structurally enforce how Large Language Models (LLMs) interact with your data. Instead of generating free-form prose, the LLM must populate a predefined, strictly typed schema (e.g., JSON or Pydantic).

### The Core Philosophy

- The Schema is the Rule: The LLM is no longer a creative writer; it is a deterministic data extractor.
- Binary Honesty: Ambiguity is eliminated by forcing the model to use programmatic booleans (like `missing_info` or `conformant`) instead of writing "I don't know"".
- Default to NOOP: If the LLM cannot perfectly fill out the required schema, the operation is flagged as false and the system does nothing.

### Why TAC is Necessary

- Standard RAG and unstructured prompts give models unlimited latitude to blend pre-trained knowledge with actual context.
- Fluent, free-form text hides false dates, fabricated clauses, and hallucinations in plain sight.
- Without machine-enforceable rules, LLMs operating on a knowledge vault will cause structural drift by ignoring naming conventions, missing metadata, and collapsing workflow stages.
- Downstream systems and automation cannot easily parse prose without relying on error-prone regex.

### Key Mechanics of a TAC System

- Evidence Enforcement: Schemas must include fields that force the model to provide exact source quotes, chunk IDs, or wikilinks to prove its output.
- Dry Runs by Default: In a read/write environment, all LLM actions default to `dry_run: True`. The LLM proposes a structural diff, which requires explicit human confirmation to execute.
- Workflow Gatekeeping: Progression through defined processes (like a Writing-to-Think pipeline) requires specific schema criteria to be met before the LLM can advance the state.
- Self-Assessment: The schema requires the model to actively self-diagnose its output via confidence scores and conflict flags.

### Implementation Contexts

|Feature|RAG Pipelines|ProdOS Vault Management|
|---|---|---|
|Primary Objective|Prevent factual hallucinations|Stop non-conformant file edits|
|Schema Output|Defined answers, confidence limits, and sources|Specific note types and frontmatter blocks|
|Failure State|`missing_info: True` blocks the user response|`conformant: false` halts the file write|
|System Benefit|Native, programmatic integration with downstream APIs|Maintains strict architecture like a Kubernetes manifest|

### Recommended Tooling Stack

- Libraries: Use `instructor` (Python) to wrap your LLM client, automatically enforcing Pydantic validation and managing retries.
- Self-Hosting: Utilize `vLLM` or `llama.cpp` for constrained decoding, which enforces JSON grammar at the token generation level.
- System Prompts: Explicitly instruct agents (like Hermes) to strictly output the requested JSON object and explicitly forbid prose modifications.

## 1. Typed Answer Contracts (TAC) Overview

Your vault has transitioned to a strictly enforced schema model governed by Typed Answer Contracts (TAC). Every LLM operation on a note is a typed data extraction/writing contract.

If an LLM or agent cannot fill the schema cleanly, it MUST flag `conformant: false` and note the `non_conformance_reason`.

- `type` is now a STRICTly required top-level field (superseding previous deprecation).
- `title`, `created`, `modified`, and `tags` remain required.
- `conformant` (boolean) and `non_conformance_reason` (string) are required top-level flags.

---

## 2. The Frontmatter Contract (All Notes)

Any agent touching frontmatter MUST return a `FrontmatterContract` object. This is the shared envelope all note types inherit:

| Field | Required | Type | Rule |
|:------|:---------|:-----|:-----|
| `title` | Yes | string | Matches filename. |
| `type` | Yes | string | `claim`, `concept`, `evidence`, `question`, `procedure`, `protocol`, `map`, `journal`, `project`, `sot`. |
| `project_name` | No | string | Parent project context if applicable. |
| `project_category` | No | string | e.g. `prodos`, `devops`, `personal`. |
| `status` | No | string | `draft`, `stable`, `evergreen`, `stale`. |
| `tags` | Yes | list | Prefer hierarchical tags. |
| `conformant` | Yes | boolean | `false` if the note cannot be cleanly typed. Do NOT write as true unless completely valid. |
| `non_conformance_reason` | Conditional | string | Required if `conformant: false`. |

---

## 3. The 5 Canonical Note Types (Knowledge Nodes)

Each of your five canonical note types has its own TAC schema. Any agent creating or editing a note must adhere to these schemas.

### 3.1 ClaimNote

- `type`: `claim`
- `title`: A single declarative sentence—the claim itself.
- `proposition`: The claim in one clear sentence, beginning with a verb or noun phrase. NOT a topic.
- `epistemic_status`: `high` (confident/evidence), `medium` (plausible), `low` (speculative), `unknown`.
- `evidence_links`: List of Wikilinks to Evidence notes that support this claim.
- `contradicts`: List of Wikilinks to Claim notes this contradicts, if any.

### 3.2 ConceptNote

- `type`: `concept`
- `title`: The term or distinction being defined.
- `definition`: A single-paragraph definition in your own words.
- `distinguishes_from`: List of related terms this concept is NOT, with wikilinks.
- `used_in_claims`: List of Wikilinks to Claim notes that use this concept.

### 3.3 EvidenceNote

- `type`: `evidence`
- `title`: Descriptive title of the evidence.
- `source_quote`: The exact quote, data point, or benchmark. Direct extraction only.
- `source_reference`: Author, book/URL, date.
- `supports_claims`: List of Wikilinks to Claim notes this evidence supports.
- `confidence`: Float 0.0 to 1.0 indicating strength of support.

### 3.4 QuestionNote

- `type`: `question`
- `title`: The question itself—must end with '?'.
- `tension`: What belief or observation generates this question?
- `candidate_answers`: List of possible answers; can be empty.
- `related_claims`: List of related Claim notes.

### 3.5 ProcedureNote

- `type`: `procedure`
- `title`: 'How to [do X]' format.
- `trigger`: When is this procedure invoked?
- `steps`: Ordered, physical, verb-first steps.
- `verification`: How do you know it worked?

---

## 4. The `prodos` Object (Legacy Extension & Routing)

The nested `prodos` YAML object handles systemic routing and lifecycle events not covered directly by the base TAC.

_(Note: As the TAC architecture rolls out, elements of `prodos` may be fully migrated into top-level typed fields.)_

### 4.1 Universal Subkeys

| Key | Required | Type | Allowed values / notes |
|:----|:---------|:-----|:----------------------|
| `prodos.kind` | Yes | string | `head`, `sot`, `protocol`, `moc`, `atomic`, `project`, `ops`, `prompt`, `journal` |
| `prodos.lifecycle` | Yes | string | `seedling`, `active`, `stable`, `evergreen`, `archived` |
| `prodos.trust` | No | string | `low`, `working`, `stable`, `authoritative`—epistemic confidence |
| `prodos.review` | No | mapping | Optional cadence (`interval`, `last_reviewed`) |
| `prodos.id` | No | string | Canonical stable id for the note. |

---

## 5. Machine-readable Schema

1. JSON Schema (many tools / IDEs): `gemini-scribe/schemas/prodos-note-frontmatter.schema.json`.
2. TAC Models are validated in Python via `pydantic`.
3. Vault Action contracts ensure `dry_run` is True unless explicitly bypassed by human execution.

---

## 6. Legacy Frontmatter Mapping (Migration Table)

> Formalised 2026-07-17. [[Goal - Frontmatter Bulk Migration (Phase 3)]] cited this section by number before it existed in this document — the table below is that migration's own mapping rules, promoted here so the spec and the prompt that depends on it actually agree. No new policy invented; this is what the 2026-07-11 migration run already used.

Legacy `type` values map to `prodos.kind` as follows (folder context disambiguates ties — see §7):

| Legacy `type` (context) | Target |
|:---|:---|
| `concept`, `atom`, `permanent`, `note`, `''`, `null`, `'null'` (in `100_zettelkasten/`) | `prodos.kind: atomic`; set `prodos.atomic.form: concept` unless tags indicate `hypothesis`/`claim`/`definition` |
| `SoT` / `sot` | `prodos.kind: sot`; if filename starts `Protocol - `, use `prodos.kind: protocol` instead and top-level `type: protocol` |
| `daily` | `prodos.kind: journal` |
| `map` | `prodos.kind: moc` (top-level `type` stays `map` — `moc` is the routing kind, not the FrontmatterContract type) |
| `command`, `atomic_command`, `playbook` | `prodos.kind: ops`; keep disambiguation (`cmd` vs `playbook`) in `tags` |
| anything else | Do NOT guess — log to an exceptions report for human decision |

Legacy key renames (apply after the type mapping above):

| Legacy key | Target |
|:---|:---|
| `status` (exact enum match only: `seedling`/`active`/`stable`/`evergreen`/`archived`; `draft` → `seedling`; anything else → exceptions report) | `prodos.lifecycle` |
| `trust-level` | `prodos.trust` |
| `last_reviewed`, `review_interval` | `prodos.review.*` |
| `last_synthesis`, `synthesis-count` | `prodos.chronos.*` |
| `id`, `ID`, `uid` | `prodos.id` |
| `updated`, `creation_date` | Delete — but only after preserving their value into `created`/`modified` if those are missing. |

Hard rules: if a note already has a `prodos` object, merge — never overwrite existing `prodos` values with legacy-derived ones. Never delete a legacy value that could not be mapped; exceptions keep their legacy keys untouched.

---

## 7. Folder-to-`prodos.kind` Normativity

> Formalised 2026-07-17, referenced as "§3.2" by [[Goal - Frontmatter Bulk Migration (Phase 3)]] before this section existed. The table is inferred from actual vault folder structure and the §6 mapping above — treat it as a strong default, not an unquestionable law; a note's content can override its folder's default `prodos.kind` when the two genuinely disagree.

The folder a note lives in is normative for its expected `prodos.kind`, absent a stronger signal from the note's own `type`/content:

| Folder | Expected `prodos.kind` |
|:---|:---|
| `30_Library/SoT/` | `sot` (or `protocol` if filename starts `Protocol - `) |
| `30_Library/MoC/` | `moc` |
| `30_Library/100_zettelkasten/` | `atomic` |
| `30_Library/200_Projects/` | `project` |
| `30_Library/ops/` | `ops` |
| `01_journals/` | `journal` |
| `10_System/prompts/` | `prompt` |
| `20_Thinking/` | `head` |

When a note's folder and its content-inferred `prodos.kind` disagree, trust the content and flag the mismatch in `non_conformance_reason` rather than silently picking one.

---

## 8. Migration Scope & Priority

> Formalised 2026-07-17, referenced as "§8 priority" by [[Goal - Frontmatter Bulk Migration (Phase 3)]] before this section existed.

TAC governs frontmatter in: `30_Library/**`, `20_Thinking/**`, `10_System/**`, `01_journals/**`, `00_Inbox/**`. It never governs: `raw/` (sealed), `wiki/` (own dossier schema), `output/`, `.trash/`, `.obsidian/`, `AGENTS.md`, `index.md`, `log.md`.

When multiple notes need bringing into conformance at once, prioritise in this order (highest-traffic, most-linked-against first): `30_Library/MoC/` and `30_Library/SoT/` and `30_Library/ops/` → `30_Library/100_zettelkasten/` → `30_Library/200_Projects/`, `20_Thinking/`, `10_System/`, `01_journals/`. A specific bulk-migration run may checkpoint this into dated batches with git commits — see [[Goal - Frontmatter Bulk Migration (Phase 3)]] for that operational detail; this section states the priority principle only.

---

## 9. Validation

> Formalised 2026-07-17, referenced as "§9" by [[Goal - Frontmatter Bulk Migration (Phase 3)]] before this section existed.

The canonical validator is `gemini-scribe/scripts/validate_note_frontmatter.py`, run over the vault after any bulk migration to confirm every in-scope note satisfies §2 (FrontmatterContract) and, where applicable, §3 (the 5 canonical note-type schemas).

**Status: this script does not currently exist in the repository** (checked 2026-07-17 — no `gemini-scribe/` directory found in the vault). Any prompt or process that assumes it can run this validation will fail until the script is written. Until then, conformance checking is manual: spot-check `conformant`/`non_conformance_reason` presence and `type` enum membership per §2.
