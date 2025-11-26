---
aliases: []
confidence:
created: 2025-10-24T07:13:39Z
epistemic:
last_reviewed:
modified: 2025-11-03T13:48:23Z
purpose:
review_interval:
see_also: []
source: https://gemini.google.com/share/60c321b60e08
source_of_truth: []
status:
tags: []
title: notes object
type:
uid:
updated:
version:
---

I have read how to take smart notes. I have also tried to create a digital pkm. I love computers and modelling things in code. The idea of a smart note, a note that has properties that help it combine with other notes to form ideas and new concepts is fascinating. The 2 existing ideas synthesis something new via the reason they are related. The link between the notes and it's context are the real life blood of the system. What could this note and link objects look like? What properties do they have that facilitate linking with context? Maybe a layered approach to the metadata like in a TCP packet

This is a fantastic way to model the problem. Thinking about notes and their relationships as first-class objects, rather than just text files and hyperlinks, is the key to building a truly "smart" system.

Your analogy to a TCP packet is spot on. A packet isn't just its payload (data); its value comes from its *metadata* (headers) which describes its origin, destination, sequence, and purpose. This metadata is what allows a complex, emergent system (the internet) to function.

Let's model your `Note` and `Link` objects, treating them as classes or data structures.

---

## The Note Object (The "Packet")

This object is the fundamental unit of knowledge. It contains the "payload" (your idea) but is wrapped in a "header" of metadata that gives it context and "routability" within your knowledge base.

### Key Properties Facilitating Context

- **`id`**: The unique "IP address" of your note. It allows it to be unambiguously referenced.
- **`status`**: This is like a TCP flag (e.g., `SYN`, `ACK`). It tells you the note's state of maturity. You might only want to build new ideas from `permanent` or `evergreen` notes.
- **`tags`**: These are like "ports." They group notes by topic, allowing for broad filtering (e.g., "Show me all notes on port `#pkm` ").
- **`source`**: This is the "origin IP." It tethers your thought to its source in the real world, preserving its initial context.

---

## The Link Object (The "Protocol")

This is the "lifeblood," as you said. In most systems (like standard wikis), a link is just a string: `[[target_id]]`. This is lossy; it tells you *that* a connection exists, but not *why*.

Your `Link` object must be a first-class citizen—a "thing" in its own right, just like a note. In graph database terms, notes are **Nodes** and links are **Edges**. Your Edges need properties.

### Key Properties Facilitating Synthesis

- **`type`**: This is the core of the synthesis. It defines the *reason* for the relationship. When two ideas are linked, the `type` is the *new idea* they synthesise.
  - `Note A` + `Note B` + `Link (type: 'contradicts')` = A new insight about a point of academic disagreement.
  - `Note C` + `Note D` + `Link (type: 'is_analogue_to')` = A new metaphor or a solution from a different domain.
- **`description`**: This is your "synthesis" field. When you make the link, you should be forced to write *why*. This text is pure gold. It *is* the new, combined idea.
- **`created_timestamp`**: The act of linking is a creative act. Knowing *when* you made a connection is part of the context.

---

## Your "TCP Layer" Model for Knowledge

Let's explicitly map your analogy. This layered approach is precisely how this system facilitates emergent ideas.

| Layer                     | TCP/IP Analogue                           | PKM Object & Function                                                                                                                                           |
| ------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Layer 5 (Application)** | **Application Data** (e.g., HTTP request) | **`Note.content`** (The human-readable prose and ideas you work with.)                                                                                          |
| **Layer 4 (Transport)**   | **TCP Header** (Port, Sequence, Flags)    | **`Link` Object** (The *relationship*. It defines the `type`, `description`, and `strength` of the connection. It manages the *flow* of thought between notes.) |
| **Layer 3 (Network)**     | **IP Header** (Source/Dest. IP)           | **`Note.id` & `Link.source/target`** (The unique "addresses" that route connections. This is the graph's structure.)                                            |
| **Layer 2 (Data Link)**   | **MAC Header** (Hardware address)         | **`Note.source` & `Note.tags`** (The note's "local" context—where it came from, what its topic is.)                                                             |
| **Layer 1 (Physical)**    | **Ethernet Cable / Wi-Fi**                | **The File System** (e.g., the `.md` file on your hard drive, or the database row.)                                                                             |

### How This System Answers Queries

With this model, your PKM stops being a "wiki" and becomes a "database of thought." You can run queries that are impossible in simpler systems:

- `SHOW me all notes that 'contradict' notes tagged '#productivity'.`
- `FIND the note that 'is_analogue_to' 'TCP/IP' and 'is_example_of' 'PKM'.`
- `LIST all 'description' fields from 'Link' objects created in the last month.` (This query would literally show you a journal of all your new ideas.)

This is how you get synthesis. The **`Link`** object, with its `type` and `description` properties, is the mechanism that captures the *reason* for the connection, and that *reason* is the new, synthesised idea.

### How to Build This

1. **Lo-Fi (Obsidian/Logseq):** Use YAML frontmatter for the `Note` metadata. For `Links`, you can use [Dataview inline fields](https://www.google.com/search?q=https://blacksmithgu.github.io/obsidian-dataview/queries/inline-queries/) or typed links, e.g., `[[20240112103000 |expands_on: This note provides a model...]]`. This is functional but can be clunky.
2. **Hi-Fi (Graph Database):** This is the "coder's" solution. Use a tool like **Neo4j** or **ArangoDB**.
   - Your `Note` objects are **Nodes** with properties (`id`, `title`, `status`).
   - Your `Link` objects are **Edges** (or "Relationships") with properties (`type`, `description`, `strength`). This is *exactly* what these databases are designed for, and it would allow you to run those powerful queries (using Cypher) directly.

These 3 paragraphs are each separate but related ideas that together form say something. Using the above layer system break then down and explain how it would work

Our brains construct mental models as a highly efficient evolutionary strategy to manage an overwhelming amount of sensory information. These models act as subconscious filters, allowing us to navigate the world, make predictions, and decide on actions without having to consciously process every detail.

From a survival perspective, this is critical. Having pre-built, simplified models allows for the rapid, almost instantaneous decision-making needed to avoid threats and seize opportunities. The trade-off for this speed and efficiency is that we don't experience the model itself; we experience the world \_through\_ the model.

This is analogous to wearing colored lenses from birth; one would not be aware of the lenses, but would simply believe the world is tinted that color. The neural processes that create and use these models are the fundamental architecture of our thought, not an object of our thought. This is a key reason why \[\[Naïve Realism Makes Mental Models Invisible\]\].

\---

Here's a breakdown of how those three paragraphs would be processed and synthesised using the object model we discussed.

The "something" that these three paragraphs form together is an argument: **Mental models are efficient survival tools, but this very efficiency makes them invisible, leading us to mistake them for reality.**

Our system must capture this emergent argument, not just store the three fragments.

---

## 1\. The Note Objects (The "Packets")

First, we atomise each paragraph into its own `Note` object. This is the "Data Link" and "Application" layer—capturing the payload and its local metadata.

### Note 1 (N1)

JSON

```markdown
{
"id": "20251024033001",
"title": "Mental Models as Evolutionary Filters",
"content": "Our brains construct mental models as a highly efficient evolutionary strategy...",
"status": "permanent",
"tags": ["#mental_model", "#evolution", "#cognition", "#efficiency"]
}
```

### Note 2 (N2)

JSON

```markdown
{
"id": "20251024033002",
"title": "Survival Trade-off of Mental Models",
"content": "From a survival perspective, this is critical... The trade-off... is that we don't experience the model itself; we experience the world _through_ the model.",
"status": "permanent",
"tags": ["#mental_model", "#survival", "#decision_making", "#trade_off"]
}
```

### Note 3 (N3)

JSON

```markdown
{
"id": "20251024033003",
"title": "The Invisibility of Mental Models (Coloured Lenses)",
"content": "This is analogous to wearing colored lenses from birth... This is a key reason why [[Naïve Realism Makes Mental Models Invisible]].",
"status": "permanent",
"tags": ["#mental_model", "#analogy", "#invisibility", "#naïve_realism"]
}
```

---

## 2\. The Link Objects (The "Protocol")

This is the "Transport" layer, where synthesis happens. We create `Link` objects to represent the *relationship* between the notes. The `Link.description` field *is* the new, synthesised idea.

### Link 1 (L1: Connecting N1 and N2)

- **Relationship:** N2 explains the *reason for* and *consequence of* the efficiency described in N1.
- **The Synthesised Idea:** The *reason* we have efficient filters (N1) is for *survival* (N2), and the *consequence* is that we see *through* them (N2).

JSON

```markdown
{
"id": "L-d4e5f6a1",
"source_note_id": "20251024033002",
"target_note_id": "20251024033001",
"type": "explains_consequence_of",
"description": "The survival need for rapid decisions (N2) explains _why_ the evolutionary filters (N1) are so efficient, and reveals the trade-off: this efficiency makes us experience the world _through_ the model."
}
```

### Link 2 (L2: Connecting N2 and N3)

- **Relationship:** N3 provides a powerful *analogy* for the key trade-off mentioned in N2 ("we experience the world *through* the model").
- **The Synthesised Idea:** The abstract concept of "experiencing *through* a model" can be understood concretely with the "coloured lenses" analogy.

JSON

```markdown
{
"id": "L-b8c9d0e2",
"source*note_id": "20251024033003",
"target_note_id": "20251024033002",
"type": "is_analogue_to",
"description": "The 'coloured lenses' analogy (N3) provides a concrete illustration for the abstract trade-off of 'experiencing the world \_through* the model' (N2)."
}
```

### Link 3 (L3: Connecting N3 to the Existing note)

- **Relationship:** N3 explicitly states it provides a *reason* for the idea in the note `[[Naïve Realism Makes Mental Models Invisible]]`.
- **The Synthesised Idea:** Our models are invisible because they *are* our thought architecture, not things we look *at*.

JSON

```markdown
{
"id": "L-f1a2b3c4",
"source_note_id": "20251024033003",
"target_note_id": "Naïve Realism Makes Mental Models Invisible",
"type": "is_reason_for",
"description": "The fact that mental models are our 'cognitive architecture' (N3) is a key reason _why_ naïve realism makes them invisible."
}
```

---

## 3\. How the "Layers" Facilitate Synthesis

This is how your system creates the new idea:

- **Application Layer (L5):** You read the `content` of N1, N2, and N3.
- **Network Layer (L3):** Your system identifies the "route" between them: `N1 <--L1-- N2 <--L2-- N3`. This establishes a "thought-flow."
- **Transport Layer (L4):** This is the crucial part. You don't just see that they're linked; you examine the `Link` objects themselves.
  - Reading **`L1.description`** gives you the synthesis of the first two ideas.
  - Reading **`L2.description`** gives you the synthesis of the second two.

By following this "chain" of `Link` objects, you can algorithmically build the full argument:

1. Start at N1: "Models are efficient filters."
2. Follow L1: "...this efficiency is for *survival*, and the *trade-off* is we see through them."
3. Follow L2: "...and this 'seeing through' is just like *wearing coloured lenses*."
4. Follow L3: "...which is *why* we suffer from *naïve realism*."

The emergent idea is no longer implicit. **It is explicitly captured as data** in the `Link` objects. Your system has successfully "understood" and stored the synthesis.

In your description above the link objects has a description property but the value of that key is itself another note object on the pkm. In this context it is the reason other notes link but it could be part of another set of notes with links. Review the linking system with this in mind

You are absolutely right. That is the next logical step and a much more powerful model.

My initial proposal had a "smart" edge (`Link`) with a `description` property. You are suggesting that this `description` isn't just metadata; it is **the synthesis itself**. As such, it should be a first-class `Note` object.

This is a key insight from graph theory called **reification**. We are turning a *relationship* (an edge) into an *entity* (a node). This new "Synthesis Note" can then be linked to, just like any other note, allowing for infinite recursion and meta-analysis.

This change makes the system simpler but far more powerful.

---

## The Revised Note Object

The `Note` object needs one crucial addition: a property to distinguish *what kind* of note it is.

JSON

```markdown
{
"id": "20251024050001",
"title": "Mental Models as Evolutionary Filters",
"content": "Our brains construct mental models as a highly efficient evolutionary strategy...",
"status": "permanent",

// --- New Metadata Property ---
"note_type": "atomic", // 'atomic', 'synthesis', 'literature', 'fleeting'

"tags": ["#mental_model", "#evolution", "#cognition"],
"source": "...",
"created_timestamp": "..."
}
```

- **`note_type`**: This is the new key.
  - **`atomic`**: A single idea, like our original paragraphs.
  - **`synthesis`**: This is the "Link Note." Its *content* is the reason two or more other notes are related.

---

## The Link Object (Now Simplified)

Because the "reason" now lives in its own `Note` object, the `Link` object becomes much simpler. It no longer needs a `description` field. It just needs to state the relationship. It's pure "Transport Layer."

- **`type`**: This property remains critical. It defines the *role* of the connection. For our new model, a `type` like `is_synthesis_of` or `is_component_of` becomes essential.

---

## How the System Works Now (Example Revisited)

Let's re-run your three-paragraph example with this superior model.

### 1\. We Create the Three Atomic Notes

- **`N1`** (`note_type: 'atomic'`): "Mental Models as Evolutionary Filters"
- **`N2`** (`note_type: 'atomic'`): "Survival Trade-off of Mental Models"
- **`N3`** (`note_type: 'atomic'`): "The Invisibility of Mental Models (Coloured Lenses)"

### 2\. We Create the Synthesis Note (The "Link Note")

You have the insight that connects them. You create a *new* note.

JSON

```markdown
{
"id": "20251024050010",
"title": "Synthesis: Efficiency Requires Invisibility",
"content": "The evolutionary need for _efficient_ filters (from [[N1]]) forces a _trade-off_ (from [[N2]]) where the models must be transparent. We see _through_ them. This is why they are invisible, like the 'coloured lenses' (from [[N3]])...",

// --- This is the key ---
"note_type": "synthesis",

"tags": ["#synthesis", "#mental_model", "#invisibility"],
"created_timestamp": "..."
}
```

Let's call this note **`S1`**.

### 3\. We Create the Simple Link Objects

Now we just connect the `S1` note back to the `atomic` notes it's built from.

- **`Link L1`**:
  - `source_note_id`: "S1"
  - `target_note_id`: "N1"
  - `type`: "is_synthesis_of"
- **`Link L2`**:
  - `source_note_id`: "S1"
  - `target_note_id`: "N2"
  - `type`: "is_synthesis_of"
- **`Link L3`**:
  - `source_note_id`: "S1"
  - `target_note_id`: "N3"
  - `type`: "uses_analogy_from"

## The Resulting Structure: A Hypergraph

What you've created is a **hypergraph**. The "link" is no longer a simple line between two points; it's a *node in its own right* that connects multiple other nodes.

**The Advantages of Your Model:**

1. **Infinite Recursion:** This is the most significant gain. Your synthesis note `S1` is now a first-class citizen. It can be linked to *another* synthesis note (`S2`) to create a *meta-synthesis* (`S3`). This perfectly models how arguments are built from other arguments.
2. **Richer Context:**`S1` can have its *own* tags, `source` (e.g., "Insight during a walk"), and `content`. The synthesis is no longer just a one-line description; it's a fully-fledged idea.
3. **Better Queries:** You can now run much more powerful queries:
   - `SHOW me all notes with 'note_type': 'synthesis' AND 'tag': '#invisibility'.` (This shows you all your *original arguments* about invisibility).
   - `SHOW me all 'atomic' notes that are linked *from* 'S1'.` (This shows you the building blocks of your `S1` argument).

This is precisely how the most advanced digital garden tools (like **Logseq** or **TiddlyWiki**) model knowledge. Every bullet point, every journal entry, and every "link" can be an object, creating a much richer and more realistic network of thought.

Google Account

Leon Ormes

<leonormes@gmail.com>

**Designing smart notes model**I’m conceptualizing a smart notes model with metadata layers similar to a network stack, integrating structured elements such as link types, context windows, and cognitive triggers. I’ll illustrate this with TypeScript, JSON-LD, and graph models, focusing on versioning, atomicity, offline sync, and storage models.
Love this, Leon. You’re thinking like a systems engineer: if notes are “packets of meaning,” then their *headers* (metadata) should let them route, combine, and synthesize—exactly like TCP/IP layers. Below is a concrete, developer-friendly model for **Note** and **Link** objects with a **layered header**, plus TypeScript interfaces and practical ways to implement it (TDD-friendly). The goal: make the *reason* a link exists first-class, so your graph can explain itself and generate new ideas.

---

## Design Goals

- **Atomic**: a note asserts one main concept/claim.
- **Self-describing**: notes/links carry enough metadata to explain, filter, and recombine.
- **Context-aware**: links are valid within certain scopes (project, time window, persona, question, etc.).
- **Compositional**: the same note can mean slightly different things under different contexts.
- **Queryable**: predictable fields for traversal, ranking, and synthesis.
- **Portable**: works as Markdown + frontmatter, JSON, or a graph DB; can be layered like packets.

---

## The “Note Packet” (layered header) Model

Think of each note as a **Note Packet** with layers. Each layer is optional but strongly typed. You can store it as frontmatter + body (Markdown) or JSON.

```sh
+----------------------------------------------------------------------------+
| L0 Identity       | id, kind, createdAt, updatedAt, status                 |
| L1 Integrity      | contentHash, parentId/version, immutability flags      |
| L2 Provenance     | author(s), source(s), citation(s), license             |
| L3 Context        | scope[], timeScope, location, roles/persona, audience  |
| L4 Semantics      | title, claim, entities[], facets[], tags[], ontology   |
| L5 Linking Hints  | embeddings, keywords, importance, questions, agendas   |
| L6 Presentation   | format, transclusions, media refs, excerpt selectors   |
| Payload           | body (Markdown/HTML/plain), attachments                |
+----------------------------------------------------------------------------+
```

### Links Are Packets Too

A **Link** is not just `A -> B`. It’s a packet carrying:

- the **relation type** (e.g., *supports, refutes, causes, analogizes, generalizes, contradicts, cites, exampleOf*),
- the **bridge** (why they’re related),
- the **context** (where/when this relation holds),
- the **granularity** (which span in A connects to which span in B),
- **strength/confidence**, **directionality**, **polarity**, and **freshness/decay**.

---

## TypeScript Interfaces (strongly Typed, TDD-ready)

> You can validate with `zod` or JSON Schema; start with these as core domain models.

```ts
// -------------------- Core Types --------------------

export type ID = string // UUID/ULID
export type ISODate = string // yyyy-mm-ddThh:mm:ssZ

export type NoteKind =
  | "concept"
  | "claim"
  | "definition"
  | "question"
  | "literature"
  | "example"
  | "pattern"
  | "workflow"
  | "snippet"
  | "meeting"

export interface TimeScope {
  from?: ISODate
  to?: ISODate
  // If the validity is cyclic or episodic, store schedule/cron-like patterns too.
}

export interface Selector {
  // Anchor a link to a precise span inside a note (W3C Web Annotation compatible).
  type: "TextQuote" | "TextPosition" | "Fragment" | "LineRange" | "BlockId"
  value?: string // for TextQuote
  start?: number // for TextPosition
  end?: number // for TextPosition
  fragmentId?: string // for Fragment (#heading-slug)
  startLine?: number // for LineRange
  endLine?: number // for LineRange
  blockId?: string // for Obsidian-style ^block
}

export interface ContextFacet {
  dimension:
    | "project"
    | "topic"
    | "question"
    | "persona"
    | "audience"
    | "environment"
    | "place"
  value: string // e.g., "k8s-cost-optimizer", "SRE", "prod"
  strength?: number // 0..1 relevance
}

export interface Entity {
  id?: string // e.g., Wikidata/URI
  label: string // e.g., "HPA", "KEDA", "Zettelkasten"
  type?: string // e.g., "Tool", "Concept", "Library"
}

// -------------------- Note Packet --------------------

export interface Note {
  // L0 Identity
  id: ID
  kind: NoteKind
  createdAt: ISODate
  updatedAt: ISODate
  status?: "fleeting" | "literature" | "permanent" | "draft"

  // L1 Integrity
  contentHash?: string // hash of payload/body
  parentId?: ID // for version lineage
  immutable?: boolean // lock after 'permanent'

  // L2 Provenance
  authors?: string[]
  sources?: Array<{
    title?: string
    uri?: string
    citationText?: string
    accessDate?: ISODate
    page?: string
  }>
  license?: string

  // L3 Context
  scope?: ContextFacet[] // layered contexts (project/topic/persona)
  timeScope?: TimeScope
  audience?: string[] // "self", "team", "public"
  roles?: string[] // "engineer", "researcher", "designer"

  // L4 Semantics
  title: string
  claim?: string // one clear main idea/statement
  tags?: string[]
  entities?: Entity[]
  ontology?: string[] // schema terms you use (RDF/OWL-like)
  facets?: Record<string, string | number | boolean> // custom keys

  // L5 Linking Hints
  keywords?: string[]
  importance?: number // 0..1
  questions?: string[] // open questions this note raises
  embeddingRef?: string // pointer to vector index key
  agenda?: string[] // "follow up on X", "compare with Y"

  // L6 Presentation
  format?: "markdown" | "html" | "plaintext"
  media?: Array<{ uri: string; type?: string; alt?: string }>
  excerpts?: Selector[] // notable spans

  // Payload
  body?: string // the actual content
}

// -------------------- Link Packet --------------------

export type Relation =
  | "supports"
  | "refutes"
  | "elaborates"
  | "summarizes"
  | "analogizes"
  | "contrasts"
  | "causes"
  | "enables"
  | "requires"
  | "generalizes"
  | "specializes"
  | "exampleOf"
  | "derivedFrom"
  | "cites"
  | "partOf"

export interface Link {
  // L0 Identity
  id: ID
  from: ID
  to: ID
  createdAt: ISODate
  updatedAt: ISODate

  // L3 Context on the link itself (where this relation holds)
  scope?: ContextFacet[]
  timeScope?: TimeScope

  // Semantics of the relation
  relation: Relation
  directed?: boolean // default true. If false, treat as undirected (e.g., analogizes)

  // The WHY: bridge carries the reason
  bridge: {
    rationale: string // free-text "why these relate"
    evidence?: string[] // quote IDs or source URIs
    selectors?: {
      from?: Selector // exact span(s) linked
      to?: Selector
    }
    polarity?: "positive" | "negative" | "neutral" // does it support or oppose?
    confidence?: number // 0..1 confidence
    weight?: number // influence in traversal
    freshnessHalfLifeDays?: number // time decay
    pattern?: string // optional pattern label (e.g., "A causes B")
    embeddingRef?: string // vector for the relationship itself
  }

  // Integrity & provenance
  authors?: string[]
  sources?: Array<{ uri: string; citationText?: string }>

  // Presentation / UX
  note?: string // human tip: "In prod, this holds due to X."
}
```

---

## Example (Markdown + frontmatter)

A permanent note about autoscaling strategies:

```markdown
---
id: "01J8ZJQ8H0GZ8DQH3DB7K1E3J5"
kind: "concept"
createdAt: "2025-10-24T06:55:00Z"
updatedAt: "2025-10-24T06:55:00Z"
status: "permanent"

scope:
  - { dimension: "project", value: "k8s-cost-optimizer", strength: 0.9 }
  - { dimension: "topic", value: "autoscaling" }

title: "Event-driven autoscaling reduces idle compute vs. CPU HPA in bursty workloads"
claim: "For bursty traffic, queue-length or event-rate signals scale pods more efficiently than CPU-only HPA."
tags: ["kubernetes", "scaling", "keda", "hpa", "cost"]
entities:
  - { label: "KEDA", type: "Tool" }
  - { label: "HPA", type: "Tool" }

questions:
  - "When is CPU HPA adequate vs. queue-based scaling?"
importance: 0.7
format: "markdown"
---

**Key idea**: CPU-based HPA lags for bursty, IO-heavy work; event-driven triggers (e.g., queue length) can right-size faster with lower idle time.
```

A link from this concept to a literature note:

```json
{
  "id": "01J8ZJTZ4WJZQPMJZYRZZE1V5Q",
  "from": "01J8ZJQ8H0GZ8DQH3DB7K1E3J5",
  "to": "01J8ZK2C6G4BXD3W3PV5MD6H2N",
  "createdAt": "2025-10-24T07:02:00Z",
  "updatedAt": "2025-10-24T07:02:00Z",
  "relation": "cites",
  "directed": true,
  "scope": [
    { "dimension": "project", "value": "k8s-cost-optimizer", "strength": 0.9 }
  ],
  "bridge": {
    "rationale": "The benchmark in §4 shows queue-length triggers reduce p95 latency and cost under bursty load.",
    "selectors": {
      "from": { "type": "TextQuote", "value": "bursty traffic" },
      "to": { "type": "Fragment", "fragmentId": "results-section" }
    },
    "confidence": 0.8,
    "polarity": "positive",
    "weight": 0.6
  },
  "sources": [{ "uri": "https://example.org/ed-scaling-benchmark" }]
}
```

---

## How This Facilitates Context-rich Linking

**1) Context as a first-class filter.**  
Both notes and links carry `scope`. Traversals can filter by `dimension:value` sets:

- “Show me links that hold in `project=k8s-cost-optimizer` for the `engineer` persona.”
- “What refutations exist outside that project context?”

**2) Precision via selectors.**  
`Selector` anchors let you connect exact spans (like `TextQuote` or `^block`), not just whole notes. This is gold for literature notes and granular refutations.

**3) Bridge as reason.**  
`bridge.rationale`, `evidence`, and `polarity` make “why” queryable. You can ask:

- “Give me all *supports* links with `confidence > 0.7` that rely on section X.”
- “List all *refutes* targeting this claim’s definition block.”

**4) Time-aware knowledge.**  
`timeScope` + `freshnessHalfLifeDays` model “this was true in 2022” and decay old heuristics. Your ranking can down-weight stale relations.

**5) Typed relations for synthesis.**  
Having explicit `Relation` enums enables higher-order reasoning patterns (see below).

---

## Synthesis Patterns (turn Links into New ideas)

You can compute suggestions for **new permanent notes** by scanning for patterns in the link graph:

- **Support triads**: A *supports* B, B *supports* C → propose “A indirectly supports C (via B)”.
- **Tension**: A *supports* B, A *refutes* C → propose “Under context X, B and C conflict; define boundary conditions.”
- **Analogy fusion**: A *analogizes* B and A *supports* C → propose “Does B likely support C by analogy?”
- **Generalization**: Many examples Ei *exampleOf* G → propose “Consolidate Ei into a generalized pattern G’ with enumerated constraints.”
- **Causal chain**: A *causes* B and B *enables* C → propose “A may enable C via B; test hypothesis.”

You can encode these as query templates (GraphQL/Gremlin/Cypher or in-memory TS) and auto-open a “Synthesis Draft” note with pre-filled rationales.

---

## Ranking & Traversal (context-aware)

Define an **activation function** to walk the graph:

```sh
activation(link) =
  (bridge.weight || 1.0)
* (bridge.confidence || 0.7)
* contextMatch(scope, currentContext)   // 0..1 cosine/Jaccard
* timeDecay(freshnessHalfLifeDays)      // e^-t/halfLife
* relationBoost(relation)               // e.g., supports=1.2, refutes=1.3
```

Use this score to prioritize which neighbors to show when you’re focusing on a project, question, or persona (e.g., “engineer @ prod”).

---

## Storage Options

- **Markdown + Frontmatter**: simple, git-friendly, works with Obsidian/VS Code. Links stored either inline (`[[wikilink]]`) + a `links.json` registry for rich link packets.
- **JSON(-LD)**: if you want schema evolution and typed APIs. You can expose a small local server for search/traversal.
- **Property Graph**: Neo4j or a lightweight embedded graph for fast relation queries (typed edges, scores).
- **RDF/OWL (optional)**: if you want SPARQL and ontology reasoning later.

Interoperability: keep IDs stable, selectors compatible with W3C Web Annotation concepts (TextQuote/TextPosition).

---

## Minimal In-memory SDK (TypeScript)

```ts
export class Graph {
  private notes = new Map<ID, Note>()
  private links = new Map<ID, Link>()
  private byFrom = new Map<ID, ID[]>()
  private byTo = new Map<ID, ID[]>()

  addNote(n: Note) {
    if (this.notes.has(n.id)) throw new Error("duplicate note id")
    this.notes.set(n.id, n)
  }

  addLink(l: Link) {
    if (!this.notes.has(l.from) || !this.notes.has(l.to)) {
      throw new Error("link endpoints must exist")
    }
    this.links.set(l.id, l)
    this.byFrom.set(l.from, [...(this.byFrom.get(l.from) || []), l.id])
    this.byTo.set(l.to, [...(this.byTo.get(l.to) || []), l.id])
  }

  neighbors(id: ID, ctx?: ContextFacet[]): Array<{ link: Link; note: Note }> {
    const linkIds = this.byFrom.get(id) || []
    const res: Array<{ link: Link; note: Note }> = []
    for (const lid of linkIds) {
      const link = this.links.get(lid)!
      if (ctx && !this.contextMatch(link.scope, ctx)) continue
      const note = this.notes.get(link.to)!
      res.push({ link, note })
    }
    return res.sort((a, b) => this.score(b.link, ctx) - this.score(a.link, ctx))
  }

  private contextMatch(a?: ContextFacet[], b?: ContextFacet[]): boolean {
    if (!a || !b) return true
    // simple match: any shared (dimension,value)
    const setA = new Set(a.map((x) => `${x.dimension}:${x.value}`))
    return b.some((x) => setA.has(`${x.dimension}:${x.value}`))
  }

  private score(link: Link, ctx?: ContextFacet[]): number {
    const w = link.bridge?.weight ?? 1
    const c = link.bridge?.confidence ?? 0.7
    const ctxMatch = this.contextMatch(link.scope, ctx) ? 1 : 0.6
    const pol = link.bridge?.polarity === "negative" ? 1.1 : 1.0
    const relBoost =
      (
        {
          supports: 1.1,
          refutes: 1.2,
          causes: 1.15,
          analogizes: 1.0
        } as Record<Relation, number>
      )[link.relation] ?? 1.0
    return w * c * ctxMatch * pol * relBoost
  }
}
```

---

## Workflows that Reduce Friction (ADHD-friendly)

- **Defaulting**: When you create a link, prefill `relation` from a small hotlist and auto-capture a `bridge.rationale` snippet from your selection.
- **Session scope**: Auto-attach a `scope` facet for the current project/sprint.
- **“Just-in-time” linking**: Allow quick capture with minimal fields; background job enriches (entities, tags, embedding) later.
- **Daily Inbox**: A view that suggests 3–5 synthesis candidates and 3 ambiguous links to clarify.

---

## TDD Checklist

1. **IDs & Immutability**
   - ✅ Cannot add link if endpoints missing.
   - ✅ Immutable when `immutable=true`.
2. **Selectors**
   - ✅ Round-trip serialization of selectors.
   - ✅ Validate that targeted span exists (if you want strictness).
3. **Context filtering**
   - ✅ `neighbors(id, ctx)` returns only matches.
4. **Scoring**
   - ✅ Links with higher `confidence`/`weight` outrank others.
   - ✅ Time-decay reduces rank after N days (add a test clock).
5. **Synthesis rules**
   - ✅ Pattern “supports-supports ⇒ indirect support” yields a draft with pre-filled rationale.

---

## Optional Advanced Features

- **CRDT-friendly fields**: split note into header vs. payload; merge policies per field.
- **Hash-chained versions**: `contentHash` + `parentId` for provenance.
- **Embeddings**: store `embeddingRef` to a vector store (local file + FAISS/Annoy). Use it to propose candidate links; user confirms and adds `bridge.rationale`.
- **Link TTL/decay**: `freshnessHalfLifeDays` supports forgetting heuristics gracefully.
- **Role-based semantics**: `persona`/`audience` flips which links are “true enough” for whom.

---

## Want Me to Scaffold This

If you tell me your preferred stack, I can generate a minimal TS package with:

- Zod schemas for `Note` and `Link`
- In-memory graph with traversal & scoring
- Markdown adapter (frontmatter ↔ objects)
- A few Jest tests for the behaviors above
- A VS Code snippet for quick “Note Packet” creation

**Quick questions:**

1. Where do you want to keep data—flat Markdown repo (Obsidian/VS Code), a JSON store, or a small graph DB?
2. Which editor do you live in (VS Code, Obsidian, Logseq)?
3. Do you want embeddings now or later? (We can stub the field and add a CLI to build the index.)
4. Any must-have relation types for your day-to-day (e.g., “dependsOn”, “antiPatternOf”, “tradeOffWith”)?
