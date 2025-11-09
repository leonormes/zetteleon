# Product Roadmap

## Phase 0: Already Completed

The following features have been implemented:

- [x] **Comprehensive GTD Framework** - Full productivity operating system with horizons of focus, urgency scoring, and workflow principles
- [x] **MCP Integration Foundation** - Todoist, Jira, Obsidian, and Pieces integrations via Model Context Protocol
- [x] **Command Structure Design** - 15+ structured commands for systematic workflow management
- [x] **ADHD-Optimized Principles** - Energy management, timeboxing, and workload management guidelines
- [x] **Documentation System** - Complete framework documentation with examples and templates
- [x] **🆕 Obsidian-Todoist Integration** - Bidirectional sync with metadata preservation and mobile optimization
- [x] **🆕 Project Transformation Engine** - Natural Planning Model automation (vague → structured projects)
- [x] **🆕 Task Format Standards** - Dual-layer format (clean mobile display + hidden ProdOS metadata)
- [x] **🆕 Cross-Platform Validation** - Tested with 61+ tasks across 18 projects, 495ms avg API response
- [x] **🆕 v4.0 Context Optimization** - 72-82% context reduction (4,000→735 lines) with consolidated single-source-of-truth architecture (Oct 2025)
- [x] **🆕 Clarity Framework Integration** - Complete problem-driven front-end with Chief of Staff agent, impact scoring, and constraint enforcement (Oct 2025)

## Phase 0.5: Infrastructure Optimization (COMPLETED October 2025)

**Goal:** Optimize ProdOS documentation for LLM agent consumption and maintainability  
**Success Criteria:** 75%+ context reduction while maintaining all functionality

### Completed Features

- [x] **Single Source of Truth** - Created `00_CORE.md` (250 lines) consolidating all essential ProdOS principles
- [x] **Consolidated Standards** - Merged context, energy, and priority files into `01_Standards_Consolidated.md` (150 lines)
- [x] **Streamlined Commands** - Refactored command files to executable specs (75-80 lines each, removed verbose templates)
- [x] **Horizons Quick Reference** - Created `02_Horizons_Reference.md` for strategic alignment
- [x] **Documentation Restructure** - Clear hierarchy: Core → Standards → Commands → Templates
- [x] **Redundancy Elimination** - Archived 8 superseded files (saved ~2,600 lines of duplicate content)

### Impact Achieved

**Context Reduction:**

- Before: ~4,000 lines across 40+ files
- After: ~735 lines core context (82% reduction)
- With optional details: ~1,138 lines (72% reduction)

**Benefits:**

- 75-90% faster LLM context loading
- Single source of truth eliminates version confusion
- Easier maintenance (update 1-2 files vs. 10)
- Improved LLM reasoning with clearer structure
- Scalable architecture for future development

### Technical Details

**New Architecture:**

```
00_CORE.md (250 lines)                    - Foundation
01_Standards_Consolidated.md (150 lines)  - Execution defaults
02_Horizons_Reference.md (100 lines)      - Strategic alignment
05_Commands/*.md (75-80 lines each)       - Executable specs
```

**Migration Completed:**

- All redundant files archived to `_archive_v3/`
- Full refactoring summary documented
- Automated archival script created
- README and usage guidelines updated

---

## Phase 0.75: Clarity Framework Integration (COMPLETED October 2025)

**Goal:** Transform ProdOS from reactive task management to proactive problem-driven work selection  
**Success Criteria:** Users systematically analyze problems before creating projects, with automated impact scoring and constraint enforcement

### Completed Features

- [x] **Chief of Staff Agent Role** - Upgraded LLM agent from GTD manager to strategic problem analyst
- [x] **Problem Template System** - YAML-based problem/constraint tracking with complete metadata structure
- [x] **Cause-Effect Mapping** - Problem graph analysis for identifying high-leverage interventions
- [x] **Impact Score Algorithm** - Automated calculation of force-multiplier potential by counting cause relationships
- [x] **Constraint Guardian** - ADHD and boundary constraint enforcement with automatic compliance checking
- [x] **Five Command Integration** - Complete workflow (`/capture-problem`, `/clarify-problem`, `/review-problems`, `/convert-to-project`)
- [x] **GTD Integration Bridge** - Seamless conversion from analyzed problems to Natural Planning Model projects

### Impact Achieved

**Strategic Work Selection:**

- Problems analyzed before project creation prevents symptom-focused busy work
- Impact scoring identifies highest-leverage interventions (force multipliers)
- Constraint enforcement ensures ADHD-compatible project structures

**System Evolution:**

- From: Vague idea → Direct task creation (reactive)
- To: Vague idea → Problem analysis → Impact scoring → Strategic project (proactive)

**Workflow Enhancement:**

```
Problem Capture → Socratic Analysis → Cause-Effect Mapping → Impact Scoring → Strategic Project Creation
```

---

## Phase 1: GTD Co-Pilot Foundation (NEXT PRIORITY)

**Goal:** Implement conversational GTD Co-Pilot with multi-agent orchestration for intelligent next-action suggestions  
**Success Criteria:** Users can ask "What's next?" and receive contextually intelligent recommendations with clear reasoning

**Note**: Evolution from command-based interface to conversational AI co-pilot leveraging proven backend infrastructure and optimized v4.0 documentation architecture.

### Features

- [ ] **MasterAgent Implementation** - Conversational orchestration and user intent interpretation `L` 🔥
- [ ] **Basic Conversational Flow** - Handle "What's next?", "Daily plan", "Show urgent tasks" queries `M` 🔥
- [ ] **ReasoningAgent Foundation** - GTD-aligned recommendation engine with explainable reasoning `L` 🔥
- [ ] **Response Formatting** - ADHD-optimized conversational responses with clear action steps `M`
- [x] **✅ Backend Integration** - Leverage proven Obsidian-Todoist sync and MCP integrations (operational)
- [ ] **Error Handling & Fallbacks** - Graceful handling of unclear queries and system unavailability `S`

### Dependencies

- ✅ v4.0 optimized documentation architecture (completed)
- Existing MCP integrations (Todoist, Obsidian, Jira, Pieces)
- Current ProdOS command structure and importance-driven priority scoring
- Proven Obsidian-Todoist sync infrastructure

---

## Phase 1A: Go CLI Universal Collector (COMPLETED ✅)

**Goal:** Create a high-performance Go CLI to unify tasks from Jira and Todoist into a local SQLite database, establishing a canonical data source for future LLM-powered actions.
**Success Criteria:** A `prodos sync` command successfully aggregates all work items into a local, queryable database using a unified Go struct.

### Completed Features

- [x] **Unified Data Model** - Canonical `WorkItem` struct in Go representing all tasks across sources `S` ✅
- [x] **Jira & Todoist Clients** - Context-aware API clients with timeout handling and error recovery `M` ✅
- [x] **Local DB Storage** - SQLite database with proper migrations, transactions, and CRUD operations `S` ✅
- [x] **Sync Command** - Operational `prodos sync` command orchestrating multi-source aggregation `M` ✅
- [x] **Embedding Storage** - ChromaDB vector database for semantic search capabilities `M` ✅
- [x] **Query Command** - Natural language search across unified work items `S` ✅
- [x] **Interface Architecture** - Dependency injection with `WorkItemFetcher`, `WorkItemStore`, `EmbeddingStore` `M` ✅
- [x] **Context Propagation** - Full context.Context support with appropriate timeouts `S` ✅
- [x] **Structured Logging** - slog-based JSON logging with field/component/error helpers `S` ✅
- [x] **Test Infrastructure** - Comprehensive unit tests (30 tests, 42-86% coverage) `M` ✅

### Architecture Delivered

**Core Components:**

- `internal/model/` - Unified WorkItem type with SQLite serialization
- `internal/client/` - Jira and Todoist API clients
- `internal/database/` - SQLite store with context-aware operations
- `internal/embedding/` - ChromaDB integration for vector search
- `internal/interfaces/` - Core abstractions for dependency injection
- `internal/logger/` - Structured logging foundation
- `internal/testutil/` - Mocks and fixtures for testing

**Commands:**

- `prodos sync` - Fetch from all sources → SQLite → ChromaDB embeddings
- `prodos query "search text"` - Semantic search across work items
- `prodos embed` - Regenerate embeddings (optional)

### Dependencies

- ✅ Go 1.21+
- ✅ API access to Jira and Todoist
- ✅ OpenAI API key for embeddings

---

## Phase 1B: LLM-Powered Work Clarification (NEXT PRIORITY)

**Goal:** Use LLM to analyze unified work items and clarify them according to ProdOS principles (Natural Planning Model, energy levels, urgency scoring, ADHD constraints)  
**Success Criteria:** Users can run `prodos clarify` to get AI-powered analysis of work items with actionable recommendations aligned to GTD and ProdOS frameworks

### Features

- [ ] **Principle-Based Analysis** - LLM evaluates work items against ProdOS principles (NPM, energy, urgency) `L` 🔥
- [ ] **Clarify Command** - `prodos clarify [item-id]` analyzes and suggests improvements `M` 🔥
- [ ] **Batch Clarification** - Process multiple items with `prodos clarify --all --status=open` `M` 🔥
- [ ] **Natural Planning Model Integration** - Auto-detect vague items and suggest NPM breakdown `L` 🔥
- [ ] **Energy Level Assignment** - AI recommends appropriate energy levels based on task description `M`
- [ ] **Urgency Score Calculation** - Automated urgency scoring using ProdOS algorithm `S`
- [ ] **ADHD Constraint Checking** - Validate tasks against ADHD-friendly principles (timeboxing, chunking) `M`
- [ ] **Recommendation Export** - Generate clarified task descriptions back to source systems `L`

### Clarification Workflow

```
1. User: prodos clarify JIRA-123
2. System: Fetches item from local DB
3. LLM Analysis:
   - Is the outcome clear?
   - Is it appropriately scoped for ADHD constraints?
   - What's the recommended energy level?
   - What's the urgency score?
   - Should this be broken down via NPM?
4. Output: Structured recommendations with reasoning
5. Option: Apply changes back to Jira/Todoist
```

### LLM Prompt Framework

The clarification engine will use structured prompts based on:

- **ProdOS Principles**: From `00_CORE.md` (NPM, horizons, energy management)
- **ADHD Constraints**: Timeboxing, cognitive load, context switching costs
- **Urgency Algorithm**: Importance-driven priority scoring
- **Natural Planning Model**: Purpose → Principles → Outcome → Brainstorm → Organize → Next Actions

### Output Format

```yaml
item_id: JIRA-123
original_title: "Fix the thing"
analysis:
  clarity_score: 3/10
  issues:
    - Vague outcome: "Fix what exactly?"
    - No timeboxing guidance
    - Missing energy level
  recommendations:
    title: "Debug authentication timeout in production API (2h)"
    description: |
      Purpose: Restore service reliability
      Outcome: Auth API responds within 500ms for all requests
      Next Actions:
        1. Review logs for timeout patterns (30min, low energy)
        2. Identify bottleneck in auth flow (1h, medium energy)
        3. Implement fix and test (30min, medium energy)
    energy_level: medium
    urgency_score: 8.5
    timeboxed: "2 hours total"
    adhd_compliant: true
```

### Dependencies

- ✅ Phase 1A unified collector (completed)
- OpenAI API or local LLM (Claude, Llama)
- ProdOS principles documentation (already in `.agent-os/`)

---

## Phase 2: Vector Database & Knowledge Indexing (NEW FOCUS)

**Goal:** Implement real-time knowledge synthesis through vector database and continuous indexing  
**Success Criteria:** All tasks, notes, and projects automatically indexed and semantically searchable with <2s query response times

**Status**: Building on proven sync infrastructure to add intelligent knowledge organization.

### Features

- [ ] **IngestionAgent Implementation** - Automated data collection from Todoist, Jira, Obsidian with real-time updates `L` 🔥
- [ ] **IndexingAgent Implementation** - Convert documents, tasks, notes into vector embeddings for semantic search `L` 🔥
- [ ] **Vector Database Setup** - Local vector storage (Qdrant/Weaviate) with metadata filtering capabilities `M` 🔥
- [ ] **RetrievalAgent Implementation** - Intelligent context search and information synthesis engine `L`
- [x] **✅ Data Sync Foundation** - Obsidian-Todoist sync operational (495ms avg response, 61+ tasks)
- [ ] **Continuous Indexing Pipeline** - Real-time updates when files change or tasks are modified `M`

### Dependencies

- Phase 1 GTD Co-Pilot foundation
- Vector database infrastructure
- Embedding model integration (OpenAI/local)

## Phase 3: Advanced Conversational Intelligence & Adaptive Reasoning

**Goal:** Implement sophisticated conversational AI with personalized GTD insights and learning adaptation  
**Success Criteria:** 90% user satisfaction with recommendations, continuous learning from user feedback, complex query understanding

### Features

- [ ] **Advanced Conversational Understanding** - Complex query parsing ("Show me blocked tasks for the website project") `L`
- [ ] **Personalized GTD Insights** - Learn user patterns and preferences for improved recommendations `XL`
- [ ] **Contextual Follow-up Conversations** - "Show me something else" and conversational refinement `M`
- [ ] **Energy Pattern Learning** - Adaptive recommendations based on observed productivity cycles and feedback `L`
- [ ] **Predictive Task Sequencing** - Intelligent scheduling based on completion patterns and dependencies `L`
- [ ] **Proactive Suggestions** - "You haven't worked on Project X in 3 days. Here's a good next action." `M`

### Dependencies

- Phase 2 vector database and knowledge indexing
- Historical completion data and user feedback loops
- Advanced LLM integration for complex reasoning

## Phase 4: Advanced Workflow Automation

**Goal:** Achieve fully automated productivity workflow with minimal user intervention  
**Success Criteria:** Users spend <5 minutes daily on system management while maintaining full productivity visibility

### Features

- [ ] **Smart Capture Processing** - Auto-categorization and context assignment for new inputs `L`
- [ ] **Proactive Notifications** - Intelligent timing for task switches and daily planning prompts `M`
- [ ] **Workflow Pattern Recognition** - Automatic detection and optimization of recurring work patterns `XL`
- [ ] **Cross-System Project Linking** - Automatic association of related work across Jira, Todoist, and Obsidian `L`
- [ ] **Capacity Management** - Automatic workload balancing with overcommitment prevention `M`

### Dependencies

- Phase 3 AI decision support
- Pattern recognition algorithms
- Advanced notification systems

## Phase 5: Mobile and Collaboration Features

**Goal:** Extend ProdOS capabilities to mobile devices and team coordination  
**Success Criteria:** Seamless productivity management across devices with optional team visibility

### Features

- [ ] **Mobile Companion App** - iOS/Android app for capture and basic task selection `XL`
- [ ] **Team Context Awareness** - Optional sharing of availability and current focus areas `L`
- [ ] **Cross-Device Synchronization** - Real-time sync of state across desktop and mobile `M`
- [ ] **Voice Interface** - Speech-to-text capture and voice-activated commands `L`
- [ ] **Collaborative Project Views** - Shared project visibility for team coordination `M`

### Dependencies

- Core system stability
- Mobile development framework
- Team collaboration requirements

---

## Implementation Timeline

- **Phase 0.5:** ✅ **COMPLETED** (October 2025) - Infrastructure optimization and v4.0 context refactoring
- **Phase 0.75:** ✅ **COMPLETED** (October 2025) - Clarity Framework integration with Chief of Staff agent role
- **Phase 1A:** ✅ **COMPLETED** (October 2025) - Go unified collector with vector search (2 weeks actual)
- **Phase 1B:** 2-3 weeks (LLM-powered work clarification with ProdOS principles) - **NEXT PRIORITY**
- **Phase 1:** 3-4 weeks (GTD Co-Pilot foundation with basic conversational interface)
- **Phase 2:** 4-5 weeks (Vector database, knowledge indexing, and multi-agent implementation)
- **Phase 3:** 5-6 weeks (Advanced conversational intelligence and adaptive reasoning)
- **Phase 4:** 3-4 weeks (Advanced workflow automation and proactive features)
- **Phase 5:** 6-8 weeks (Mobile collaboration and team coordination)

**Total Estimated Timeline:** 23-30 weeks for complete GTD Co-Pilot implementation

**Key Milestones:**

- ✅ **October 2025:** v4.0 infrastructure optimization complete (72-82% context reduction)
- ✅ **October 2025:** Clarity Framework integration complete (problem-driven work selection)
- ✅ **October 2025:** Phase 1A Go unified collector complete (SQLite + vector search operational)
- **Week 2:** LLM work clarification with ProdOS principles (Phase 1B)
- **Week 6:** Basic "What's next?" conversational queries working (Phase 1)
- **Week 11:** Full vector database with semantic search operational (Phase 2)
- **Week 17:** Personalized recommendations with learning adaptation (Phase 3)
- **Week 21:** Complete GTD Co-Pilot with proactive suggestions (Phase 4)
- **Week 30:** Mobile and collaboration features complete (Phase 5)
