# Phase 1B: LLM-Powered Work Clarification

## Overview

Transform vague, unstructured work items into clear, actionable tasks aligned with ProdOS principles using LLM analysis. This phase leverages the unified work item database from Phase 1A to provide intelligent work clarification.

## Vision

**Before:**

```
JIRA-123: "Fix the authentication thing"
- Vague outcome
- No energy level
- No time estimate
- Not ADHD-friendly
```

**After (with `prodos clarify JIRA-123`):**

```yaml
item_id: JIRA-123
clarity_analysis:
  score: 3/10
  issues:
    - Vague outcome ("fix the authentication thing" - what specifically?)
    - No timeboxing (how long will this take?)
    - No energy level (when should I do this?)
    - Not chunked for ADHD (too large?)

recommendations:
  title: "Debug and fix OAuth2 token refresh timeout (2h max)"
  description: |
    **Purpose**: Restore reliable authentication for API users
    **Outcome**: OAuth2 token refresh completes within 2 seconds, no timeouts

    **Next Actions**:
    1. Review auth service logs for timeout patterns (30min, low energy)
    2. Profile token refresh endpoint (30min, medium energy)
    3. Identify bottleneck (database query, external API, etc.) (30min, medium energy)
    4. Implement fix with tests (30min, high energy)

  energy_level: medium # Requires debugging focus but not creative thinking
  urgency_score: 8.5 # User-facing, production issue, but workaround exists
  timeboxed: "2 hours maximum"
  adhd_compliant: true # Chunked into 30min blocks, clear stopping points
  horizon: Ground (next actions clearly defined)
```

---

## Core Principles

### Natural Planning Model (NPM)

Every work item should answer:

1. **Purpose**: Why are we doing this?
2. **Principles**: What standards/constraints apply?
3. **Outcome**: What does success look like?
4. **Brainstorm**: What are the options?
5. **Organize**: What's the sequence?
6. **Next Actions**: What's the immediate next physical action?

### ADHD-Friendly Constraints

1. **Timeboxing**: Every task has a maximum time estimate
2. **Chunking**: Tasks > 2 hours should be broken down
3. **Energy Levels**: Matched to cognitive load (low/medium/high)
4. **Context Clarity**: No ambiguous language
5. **Clear Outcomes**: Measurable success criteria

### Urgency Scoring Algorithm

From ProdOS MOC principles:

```
Base Score = (Importance × 5) + (Deadline Pressure × 3) + (Dependencies × 2)
Final Urgency = Base Score * Domain Multiplier

Importance:
- 2: Critical (production down, blocking others)
- 1: Important (enables significant value)
- 0: Normal (valuable but not blocking)

Deadline Pressure:
- 2: Immediate (within 24h)
- 1: Soon (within week)
- 0: Flexible

Dependencies:
- 2: Blocking multiple people/systems
- 1: Blocking one person/system
- 0: Not blocking anyone

Domain Multiplier (The Indistractable Stack):
- 1.5: SELF (tasks tagged #renewal, #personal, #health)
- 1.2: RELATIONSHIPS (tasks tagged #family)
- 1.0: WORK (tasks tagged #work, or default)
```

---

## Implementation Architecture

### Command Structure

```go
// cmd/clarify.go
var clarifyCmd = &cobra.Command{
    Use:   "clarify [item-id]",
    Short: "Analyze and clarify work items using LLM",
    Long: `Analyze work items against ProdOS principles (Natural Planning Model,
energy levels, ADHD constraints) and provide actionable recommendations.

Examples:
  prodos clarify JIRA-123              # Clarify single item
  prodos clarify --all --status=open   # Clarify all open items
  prodos clarify --apply JIRA-123      # Apply recommendations back to source
`,
    Run: func(cmd *cobra.Command, args []string) {
        // Implementation
    },
}
```

### Service Layer

```go
// internal/clarification/service.go
package clarification

type ClarificationService struct {
    db      interfaces.WorkItemStore
    llm     interfaces.LLMClient
    logger  *logger.Logger
    config  Config
}

type ClarificationRequest struct {
    ItemID string
    Context []string // Related items for context
}

type ClarificationResponse struct {
    ItemID           string
    ClarityScore     int    // 1-10
    Issues           []Issue
    Recommendations  Recommendation
    Reasoning        string
}

type Issue struct {
    Category    string // "vague_outcome", "no_timebox", "too_large", etc.
    Description string
    Severity    string // "critical", "warning", "info"
}

type Recommendation struct {
    Title            string
    Description      string
    EnergyLevel      string  // "low", "medium", "high"
    UrgencyScore     float64
    TimeboxEstimate  string
    ADHDCompliant    bool
    Horizon          string // "Ground", "Projects", "Areas", etc.
    NextActions      []NextAction
}

type NextAction struct {
    Description  string
    EnergyLevel  string
    TimeEstimate string
    Order        int
}
```

### LLM Integration

```go
// internal/llm/client.go
package llm

type Client interface {
    Clarify(ctx context.Context, req ClarificationRequest) (*ClarificationResponse, error)
}

type OpenAIClient struct {
    apiKey string
    model  string // "gpt-4" or "gpt-3.5-turbo"
}

// Structured prompt template
const clarificationPromptTemplate = `You are a productivity expert analyzing work items according to ProdOS principles.

# ProdOS Principles
{{.ProdOSPrinciples}}

# Work Item to Analyze
ID: {{.ItemID}}
Title: {{.Title}}
Description: {{.Description}}
Source: {{.Source}}
Current Status: {{.Status}}

# Your Task
Analyze this work item and provide:

1. **Clarity Score** (1-10): How clear and actionable is this task?
2. **Issues**: What problems exist? (vague outcome, no timebox, too large, etc.)
3. **Recommendations**: How to improve this task?
   - Clear title with timeboxing
   - Natural Planning Model breakdown (Purpose, Outcome, Next Actions)
   - Energy level assignment
   - Urgency score calculation
   - ADHD compliance check

Respond in YAML format following this structure:
[YAML schema here]
`
```

---

## Prompt Engineering

### System Prompt

```
You are the ProdOS Chief of Staff (CoS), an expert productivity strategist. Your mission is to help the user achieve a "Mind Like Water" by transforming vague 'stuff' into clear, actionable, and ADHD-friendly tasks.

# Core Principles You Follow

## 1. The Indistractable Stack (Value Hierarchy)
Your primary filter. You must always prioritize in this order: 1. SELF (#health, #renewal), 2. RELATIONSHIPS (#family), 3. WORK (#work).

## 2. The Unschedule Principle
Life comes first. Your recommendations should encourage scheduling renewal and connection *before* work.

## 3. Motion Creates Motivation (ADHD-Centric)
Your most important job is to overcome task initiation friction. Every project must have a ridiculously small, physical "starter task".

## 4. Natural Planning Model (Clarification Engine)
1.  **Purpose (The 'Why'):** Connect the task to a motivating outcome.
2.  **Vision (The 'What'):** Define a crystal-clear, sensory-based picture of "done".
3.  **Next Actions (The 'How'):** Define the single next *physical* action.

## 5. Urgency Scoring
Calculate using: Final Urgency = ((Importance*5)+(Deadline*3)+(Dependencies*2)) * Domain Multiplier
- Importance: 0-2 (normal, important, critical)
- Deadline: 0-2 (flexible, soon, immediate)
- Dependencies: 0-2 (none, one, multiple)
- Domain Multiplier: 1.5 for SELF, 1.2 for RELATIONSHIPS, 1.0 for WORK.

# Your Analysis Process
1.  Read the work item.
2.  Identify clarity issues (vagueness, scope creep).
3.  Apply the Natural Planning Model to structure the work.
4.  Chunk the work into tasks, ensuring every project has a **`@starter_task`** (<5 mins).
5.  Assign specific context labels (`@DeepWork`, `@QuickWins`, `@Comms`, `@Offline`).
6.  Calculate the Final Urgency score, applying the correct Domain Multiplier.
7.  Validate ADHD compliance (Is there a starter task? Is it chunked? Is the outcome clear?).
```

### Analysis Prompt Template

```yaml
work_item:
  id: { { .ID } }
  title: "{{.Title}}"
  description: "{{.Description}}"
  source: { { .Source } }
  status: { { .Status } }
  project: "{{.Project}}"

analyze:
  - clarity_check:
      - Is the outcome measurable?
      - Is there a time estimate?
      - Are prerequisites clear?
      - Is it appropriately scoped?

  - natural_planning:
      - What's the purpose?
      - What's the desired outcome?
      - What are the next physical actions?

  - adhd_compliance:
      - Is it timeboxed?
      - Is it chunked appropriately (<2h)?
      - Does it have clear stopping points?
      - Is the energy level matched?

  - urgency_scoring:
      - Importance level (0-2)?
      - Deadline pressure (0-2)?
      - Dependency blocking (0-2)?
      - Calculate final score

provide_recommendations:
  format: yaml
  required_fields:
    - clarity_score (1-10)
    - issues (list)
    - recommended_title
    - purpose
    - outcome
    - next_actions (list with timebox, energy, and a mandatory @starter_task for projects)
    - energy_level
    - urgency_score
    - adhd_compliant (boolean)
    - reasoning
```

---

## Database Schema Extensions

```go
// Add to internal/model/workitem.go

type ClarificationAnalysis struct {
    WorkItemID       string    `db:"work_item_id" json:"work_item_id"`
    AnalyzedAt       time.Time `db:"analyzed_at" json:"analyzed_at"`
    ClarityScore     int       `db:"clarity_score" json:"clarity_score"`
    Issues           StringSlice `db:"issues" json:"issues"` // JSON array
    RecommendedTitle string    `db:"recommended_title" json:"recommended_title"`
    Purpose          string    `db:"purpose" json:"purpose"`
    Outcome          string    `db:"outcome" json:"outcome"`
    NextActions      StringSlice `db:"next_actions" json:"next_actions"` // JSON array
    EnergyLevel      string    `db:"energy_level" json:"energy_level"`
    UrgencyScore     float64   `db:"urgency_score" json:"urgency_score"`
    ADHDCompliant    bool      `db:"adhd_compliant" json:"adhd_compliant"`
    Reasoning        string    `db:"reasoning" json:"reasoning"`
    Applied          bool      `db:"applied" json:"applied"` // Has recommendation been applied?
}
```

```sql
-- Migration for clarification_analyses table
CREATE TABLE IF NOT EXISTS clarification_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_item_id TEXT NOT NULL,
    work_item_source TEXT NOT NULL,
    analyzed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    clarity_score INTEGER NOT NULL,
    issues TEXT, -- JSON array
    recommended_title TEXT,
    purpose TEXT,
    outcome TEXT,
    next_actions TEXT, -- JSON array
    energy_level TEXT,
    urgency_score REAL,
    adhd_compliant BOOLEAN,
    reasoning TEXT,
    applied BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (work_item_id, work_item_source)
        REFERENCES work_items(id, source)
);
```

---

## Usage Examples

### Basic Clarification

```bash
$ prodos clarify JIRA-123

Analyzing JIRA-123...

📊 Clarity Score: 3/10

⚠️  Issues Found:
  1. Vague outcome - "Fix the authentication thing" is not specific
  2. No timeboxing - No time estimate provided
  3. Too large - Likely needs chunking for ADHD compliance
  4. Missing energy level - Cannot schedule appropriately

💡 Recommendations:

Title: "Debug and fix OAuth2 token refresh timeout (2h max)"

Purpose:
  Restore reliable authentication for API users experiencing timeouts

Outcome:
  OAuth2 token refresh completes within 2 seconds with 99% success rate

Next Actions:
  1. Review auth service logs for timeout patterns (30min, low energy)
  2. Profile token refresh endpoint with production data (30min, medium)
  3. Identify bottleneck (database, external API, etc.) (30min, medium)
  4. Implement targeted fix with unit tests (30min, high energy)

Energy Level: medium (requires focused debugging but not creative work)
Urgency Score: 8.5/10 (Important: 2, Deadline: 1, Dependencies: 1)
ADHD Compliant: ✅ Yes (chunked into 30min blocks)

🔄 Apply these recommendations?
  [Y] Yes, update Jira
  [S] Save analysis only
  [N] No, discard
```

### Batch Clarification

```bash
$ prodos clarify --all --status=open --min-clarity=5

Found 12 work items below clarity threshold...

Analyzing items... ████████████████████ 100% (12/12)

Results:
  JIRA-123: 3/10 → 9/10 ✅
  JIRA-124: 4/10 → 8/10 ✅
  TODO-456: 2/10 → 9/10 ✅
  ...

💾 All analyses saved to database
🔄 Apply recommendations? [Y/n]:
```

### Clarification with Context

```bash
$ prodos clarify JIRA-123 --include-related

# Includes related items for better context:
# - Same project
# - Mentioned in description
# - Linked issues
# - Recently completed similar tasks
```

---

## Success Metrics

### Phase 1B Goals

1. **Clarity Improvement**: Average clarity score increases from ~4/10 to ~8/10
2. **ADHD Compliance**: 90%+ of recommendations pass ADHD checklist
3. **User Adoption**: 70%+ of clarified recommendations are applied
4. **Time Savings**: Users spend 50% less time on task planning

### Measurement

```sql
-- Track clarification effectiveness
SELECT
    AVG(clarity_score) as avg_clarity_before,
    AVG(CASE WHEN applied THEN 9 ELSE NULL END) as avg_clarity_after_applied,
    COUNT(*) FILTER (WHERE applied = true) * 100.0 / COUNT(*) as application_rate,
    COUNT(*) FILTER (WHERE adhd_compliant = true) * 100.0 / COUNT(*) as adhd_compliance_rate
FROM clarification_analyses
WHERE analyzed_at > date('now', '-30 days');
```

---

## Testing Strategy

### Unit Tests

```go
func TestClarificationService_Analyze(t *testing.T) {
    tests := []struct {
        name           string
        workItem       model.WorkItem
        expectedScore  int
        expectedIssues []string
    }{
        {
            name: "vague outcome",
            workItem: model.WorkItem{
                Title: "Fix the thing",
                Description: "",
            },
            expectedScore: 3,
            expectedIssues: []string{"vague_outcome", "no_timebox"},
        },
        // More test cases...
    }
}
```

### Integration Tests

```go
func TestClarify_EndToEnd(t *testing.T) {
    // 1. Seed database with vague work item
    // 2. Run clarification
    // 3. Verify LLM was called with correct prompt
    // 4. Verify analysis was saved
    // 5. Verify recommendations are actionable
}
```

### LLM Response Validation

```go
func TestLLM_ResponseParsing(t *testing.T) {
    // Test various LLM response formats
    // Ensure YAML parsing is robust
    // Handle edge cases and errors
}
```

---

## Implementation Phases

### Week 1: Foundation

- [ ] Create `internal/clarification/` package
- [ ] Implement basic LLM client interface
- [ ] Design prompt templates
- [ ] Add database schema migrations
- [ ] Build `clarify` command structure

### Week 2: LLM Integration

- [ ] Implement OpenAI client
- [ ] Build prompt engineering pipeline
- [ ] Parse and validate LLM responses
- [ ] Store analyses in database
- [ ] Add comprehensive tests

### Week 3: Polish & Features

- [ ] Batch clarification support
- [ ] Apply recommendations back to sources
- [ ] CLI UI improvements
- [ ] Documentation and examples
- [ ] Performance optimization

---

## Future Enhancements (Post-Phase 1B)

1. **Learning Loop**: Track which recommendations users apply to improve prompts
2. **Custom Principles**: Allow users to add their own clarification rules
3. **Automated Clarification**: Auto-clarify items below threshold on sync
4. **Team Templates**: Share clarification patterns across teams
5. **Multi-LLM Support**: Claude, Llama, Mistral as alternatives to OpenAI

---

## Dependencies

- ✅ Phase 1A: Unified collector and database (completed)
- LLM API access (OpenAI preferred)
- ProdOS principles documentation (already in `.agent-os/`)
- User feedback on clarification quality

---

## Risk Mitigation

### LLM Costs

- Cache frequent prompts
- Use GPT-3.5-turbo for initial analysis, GPT-4 only when needed
- Batch process where possible

### Prompt Drift

- Version all prompts
- Track prompt performance metrics
- A/B test prompt improvements

### User Adoption

- Start with opt-in clarification
- Show before/after comparisons
- Highlight time savings metrics
