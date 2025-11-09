# Clarity Framework Specification

*Strategic problem-driven front-end for ProdOS productivity system*

## Overview

The **Clarity Framework** transforms ProdOS from reactive task management to proactive problem-driven work selection. It provides a systematic front-end that analyzes problems *before* they become projects, using cause-effect mapping and impact scoring to identify high-leverage interventions.

## Core Principle

**Effective work solves root problems.** The framework guides users from vague problem awareness to high-impact, actionable projects by forcing systematic analysis of what problems we're actually trying to solve.

---

## System Architecture

### Chief of Staff (CoS) Agent Role

**Mission Upgrade**: From GTD system manager to strategic problem analyst

- **Primary Goal**: Guide users from vague problems to high-leverage, actionable projects
- **Method**: Systematic problem analysis using Socratic questioning and impact scoring
- **Integration**: Seamless bridge to existing GTD/Natural Planning Model workflow

### Problem/Constraint Classification

**Problems**: Situations that can be solved or improved

- Status: `1_Capture` → `2_Analysis` → `3_Project` → `5_Archived`
- Focus: Gap between current state and desired state
- Goal: Systematic improvement through targeted action

**Constraints**: Fixed realities that must be worked within

- Status: `4_Constraint` (permanent)
- Focus: Effective operation within unchangeable limitations
- Goal: Optimize performance within accepted boundaries
- Example: ADHD, work/life boundaries, resource limitations

---

## Template Structure

### YAML Frontmatter Schema

```yaml
---
# --- IDENTIFICATION ---
title: "[Problem|Constraint] - [Name]"
id: # YYYYMMDDHHMMSS (timestamp)
created: # ISO 8601
modified: # ISO 8601
tags: ["problem"]

# --- CLASSIFICATION ---
status: "1_Capture" # 1_Capture, 2_Analysis, 3_Project, 4_Constraint, 5_Archived
h2_area: "#[work|personal|family|renewal]" # H2 Area alignment
driven_by: # Constraints shaping this problem
  - "[[Constraint - ADHD]]"

# --- CORE DEFINITION ---
current_state: "What is the situation now?"
desired_state: "What would success look like?"
gap: "What's the difference?" # N/A for constraints

# --- ANALYSIS ---
control: "Direct" # Direct, Influence, None
causes: # Problems this CAUSES (downstream effects)
  - "[[Problem - Effect 1]]"
caused_by: # Problems this is CAUSED BY (upstream roots)
  - "[[Problem - Root Cause 1]]"
principles: # CONSTRAINTS ONLY: Operating rules
  - "Rule 1: All projects need 5-min @starter_task"

# --- PRIORITISATION ---
value: 5 # 1-10 scale: Importance of solving this
effort: "M" # S, M, L, XL: Rough effort estimate
impact_score: 0 # AUTO-CALCULATED: Force multiplier potential

# --- GTD INTEGRATION ---
gtd_project_link: "" # Link to created project note
---
```

---

## Command Workflow

### 1. `/capture-problem "[statement]"`

**Purpose**: Create new problem note from template
**Process**:

- Generate timestamp ID (YYYYMMDDHHMMSS)
- Set status to `"1_Capture"`
- Populate title field
- Store in appropriate location

**Example**:

```
/capture-problem "Email management feels overwhelming and chaotic"
```

### 2. `/clarify-problem`

**Purpose**: Socratic analysis of captured problems
**Process**:

- Guide through Core Definition (current/desired/gap)
- Identify control level (Direct/Influence/None)
- Trace cause-effect relationships
- Create linked problem notes as needed
- Build problem dependency graph

**Key Questions**:

- "What specifically makes this problematic?"
- "What would 'solved' look like?"
- "What might be causing this problem?"
- "What other problems does this create?"

### 3. `/review-problems`

**Purpose**: Strategic prioritization using impact scoring
**Process**:

- **Calculate impact_score**: Count problems listing this in their `caused_by` field
- Apply priority matrix: `(value × impact_score) ÷ effort_factor`
- Identify highest-leverage opportunities
- Present strategic recommendations

**Impact Score Logic**:

```
impact_score = COUNT(all_problems WHERE this_problem IN their_caused_by_field)
```

### 4. `/convert-to-project "[[Problem - Name]]"`

**Purpose**: Transform analyzed problem into GTD project
**Process**:

1. Change problem status to `"3_Project"`
2. Initiate `/define-project` using `desired_state` as vision
3. Create project note with Natural Planning Model
4. Add bidirectional link: `gtd_project_link`
5. **Constraint Guardian**: Enforce compliance with applicable constraints

### 5. Constraint Guardian (Automatic)

**Purpose**: Enforce constraint compliance during project creation
**Process**:

- Check project's `driven_by` constraints
- Validate against constraint `principles`
- Require compliance before proceeding
- Example: "This project is driven by ADHD constraint. Requires 5-minute @starter_task."

---

## Strategic Benefits

### Problem → Project Pipeline

**Traditional Workflow**:

```
Vague Idea → Direct Task Creation → Busy Work
```

**Clarity Framework Workflow**:

```
Vague Idea → Problem Analysis → Cause-Effect Mapping → Impact Scoring → Strategic Project
```

### Force Multiplier Identification

**Impact Score Algorithm** identifies problems that, when solved, eliminate multiple downstream problems simultaneously:

- **High Impact Score** (5+): Solves many other problems (force multiplier)
- **Medium Impact Score** (2-4): Moderate systemic benefit
- **Low Impact Score** (0-1): Isolated problem

### Constraint-Aware Planning

**ADHD Constraint Example**:

```yaml
principles:
  - "All projects must have 5-minute @starter_task"
  - "Energy management is non-negotiable"
  - "Work blocks minimum 30 minutes"
```

When creating ADHD-driven projects, system automatically enforces these principles.

---

## Integration with Existing Systems

### GTD Integration Bridge

**Seamless Conversion**:

- Problem `desired_state` → Project vision
- Cause analysis → Project context/background
- Impact score → Project priority weighting
- Constraint principles → Project execution requirements

### Obsidian Integration

**Template Location**: `/04_Project_Templates/problem_template.md`
**Storage Pattern**: Problems stored alongside projects in `/200_projects/`
**Linking Strategy**: Bidirectional links between problems and resulting projects

### Todoist Integration

**Project Creation**: Problems converted to projects flow through existing Obsidian-Todoist sync
**Metadata Preservation**: Impact scores and constraint flags preserved through `#tdsync`
**Mobile Access**: Clean problem-to-action traceability on mobile devices

---

## Success Metrics

### Strategic Work Selection

- **85% reduction** in low-leverage busy work
- **Force multiplier identification**: High impact_score problems get priority
- **Constraint compliance**: 100% ADHD-compatible project structures

### System Evolution Impact

- **Proactive vs. Reactive**: Strategic problem analysis vs. task reaction
- **Root Cause Focus**: Address underlying issues vs. symptom management
- **Leverage Optimization**: Work on problems that solve multiple problems

### User Experience

- **Decision Clarity**: Clear framework for "what should I work on?"
- **Strategic Confidence**: Evidence-based project selection
- **Cognitive Efficiency**: Systematic vs. ad-hoc problem analysis

---

## Implementation Status

**Phase 0.75: COMPLETED (October 2025)**

✅ **Core Framework**: Complete problem template and workflow
✅ **Command Integration**: All 5 commands functional
✅ **Impact Scoring**: Automated calculation algorithm
✅ **Constraint Guardian**: ADHD compliance enforcement  
✅ **GTD Bridge**: Seamless project conversion
✅ **Documentation**: Complete specification and user guidance

**Next Phase**: Integration with conversational GTD Co-Pilot for natural language problem analysis queries.

---

*The Clarity Framework represents ProdOS's evolution from a task management system to a strategic work selection system, ensuring users work on the right problems with maximum leverage and constraint awareness.*
