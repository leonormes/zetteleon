# Map Agent JSON Schemas

These schemas define the strict output format for the "Map" phase agents. The "Reduce" agent (The Architect) relies on these exact structures to synthesize the global plan.

## 1. The Redundancy Scout

**Role:** Detects exact duplicates and near-duplicate concepts within a single cluster.

**Output Schema:**
```json
{
  "agent": "scout",
  "cluster_id": "Cluster_X",
  "findings": [
    {
      "type": "exact_duplicate",
      "sources": ["Note_A.md", "Note_B.md"],
      "recommendation": "Merge into Note_A.md"
    },
    {
      "type": "conceptual_overlap",
      "concept": "Docker Networking",
      "sources": ["Note_C.md", "Daily_Log_2024.md"],
      "confidence": 0.85,
      "recommendation": "Extract common definition to 'Concept - Docker Networking.md'"
    }
  ]
}
```

## 2. The Ontologist

**Role:** Extracts entities, proposes naming conventions, and identifies relationships.

**Output Schema:**
```json
{
  "agent": "ontologist",
  "cluster_id": "Cluster_X",
  "proposed_title": "MOC - Container Orchestration",
  "entities": [
    {
      "name": "Kubernetes",
      "type": "Technology",
      "definition": "Container orchestration platform..."
    },
    {
      "name": "Pod",
      "type": "Concept",
      "definition": "Smallest deployable unit..."
    }
  ],
  "relationships": [
    {
      "source": "Kubernetes",
      "target": "Pod",
      "type": "manages"
    }
  ]
}
```

## 3. The Critic (Quality Assurance)

**Role:** Reviews the cluster for hallucinations, logical inconsistencies, or "context rot" risks before synthesis.

**Output Schema:**
```json
{
  "agent": "critic",
  "cluster_id": "Cluster_X",
  "status": "PASS|WARN|FAIL",
  "issues": [
    {
      "severity": "high",
      "description": "Note_D claims 'Docker uses veth pairs' but Note_E claims 'Docker uses macvlan' without context.",
      "fix_suggestion": "Clarify network driver context in final note."
    }
  ],
  "quality_score": 0.92
}
```
