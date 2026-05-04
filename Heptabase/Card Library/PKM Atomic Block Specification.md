## PKM Atomic Block Specification

### 1\. Core Metadata Structure

```json
{
  "@context": "pkm-context.json",
  "@type": "AtomicNote",
  "@id": "note:2024/02/uuid-prefix-atomic-idea-name",
  "version": 1,
  "status": "active",
  
  // Essential Properties
  "created": "2024-02-19T10:00:00Z",
  "title": "Short, distinctive name for the atomic idea",
  "summary": "One-sentence description of the core concept",
  
  // Understanding Tracking
  "maturityLevel": {
    "stage": "emerging",  // emerging, developing, stable, refined
    "confidence": "medium", // low, medium, high
    "lastAssessed": "2024-02-19T10:00:00Z"
  },
  
  // Cognitive Context
  "thoughtContext": {
    "trigger": "reading Smith's paper on knowledge graphs",
    "initialInsight": "Brief description of the original insight",
    "currentPerspective": "Current understanding of the idea"
  },
  
  // Knowledge Graph Properties
  "relationships": [{
    "@type": "Relationship",
    "relationshipType": "builds-on",
    "target": "note:2024/02/other-note-id",
    "nature": {
      "bidirectional": false,
      "strength": 4,
      "type": "theoretical", // theoretical, empirical, speculative
      "description": "How this idea builds on the target"
    },
    "history": [{
      "date": "2024-02-19T10:00:00Z",
      "change": "initial connection",
      "previousStrength": null
    }]
  }],
  
  // Composition Support
  "atomicProperties": {
    "complexity": "foundational", // foundational, intermediate, advanced
    "scope": "narrow",           // narrow, moderate, broad
    "dependencies": []           // List of required knowledge blocks
  }
}
```

### 2\. Relationship Types Taxonomy

#### 2\.1 Foundational Relationships

- `builds-on`: Extends or develops ideas from target

- `depends-on`: Requires understanding of target

- `refutes`: Contradicts or challenges target

- `supports`: Provides evidence for target

- `synthesizes`: Combines ideas from multiple targets

#### 2\.2 Cognitive Relationships

- `clarifies`: Improves understanding of target

- `exemplifies`: Provides concrete example of target

- `contextualizes`: Provides broader context for target

- `compares`: Draws parallels with target

#### 2\.3 Temporal Relationships

- `evolves-from`: Represents development of target

- `supersedes`: Replaces or updates target

- `branches-from`: Explores alternative direction from target

### 3\. Maturity Tracking

The maturity system tracks the development of ideas through stages:

1. `emerging`

   - Initial capture of idea

   - Basic relationships identified

   - Preliminary understanding

2. `developing`

   - Deeper exploration

   - More relationships established

   - Growing confidence in understanding

3. `stable`

   - Well-understood concept

   - Clear relationships

   - Tested in different contexts

4. `refined`

   - Deep understanding

   - Rich relationship network

   - Successfully applied/tested

### 4\. Implementation Guidelines

#### 4\.1 File Structure

```markdown
<!--metadata
{
  // JSON-LD metadata block as defined above
}
-->
%%content-block-start%%
# [Title of Atomic Idea]

## Core Insight
[One paragraph expressing the central idea]

## Development
[Track how understanding has evolved]

## Relationships
[Explicit discussion of relationships to other ideas]

## Open Questions
[Areas for further exploration]
%%content-block-end%%
```