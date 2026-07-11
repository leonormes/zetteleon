---
created: 2026-07-11T11:45:27+00:00
modified: 2026-07-11T11:48:30+00:00
permalink: llmeon/00-inbox/prod-os-tac-plan
title: ProdOS-TAC-Plan
type: note
---

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
    type: Literal["claim", "concept", "evidence", "question", "procedure", "map", "journal", "project", "sot"]
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
      "inferred_type": "<one of: claim | concept | evidence | question | procedure | map | journal | project | sot | unknown>",
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
