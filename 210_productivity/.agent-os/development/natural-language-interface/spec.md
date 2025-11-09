# Natural Language Interface Specification

## Overview

This specification outlines the implementation of ProdOS's natural language command interface, the highest priority feature from Phase 1 of the roadmap. The goal is to replace complex command syntax with intuitive natural language interactions while leveraging the proven Obsidian-Todoist integration backend.

## Mission Alignment

**From mission-lite.md**: ProdOS provides "intelligent task orchestration, automated system integration, and context-aware decision support through natural language commands" for ADHD knowledge workers who need "seamless multi-system task coordination without cognitive overhead."

## Success Criteria

- Users can execute daily planning using simple phrases like "daily plan"
- Task selection through intuitive queries like "what's next?"
- Background system integration without manual synchronization
- ADHD-optimized response formatting with clear action steps

## Architecture Overview

### Core Components

1. **Command Parser** - Natural language to ProdOS command mapping
2. **Shell Alias System** - Quick access shortcuts (daily, next, capture)
3. **Response Formatter** - ADHD-optimized output templates
4. **Context Detection** - Current energy/focus/project awareness
5. **Error Handler** - Graceful fallbacks for unclear commands

### Integration Points

- **Proven Backend**: Obsidian-Todoist sync (495ms avg response, 61+ tasks)
- **MCP Tools**: Todoist, Obsidian, Pieces, Jira integrations
- **ProdOS Framework**: Urgency scoring, Natural Planning Model
- **Shell Environment**: Command aliases and workflow scripts

## Implementation Plan

### Phase 1.1: Command Parser Foundation

**Goal**: Parse natural language input and map to structured ProdOS commands

#### Core Parsing Patterns

```bash
# Daily workflows
"daily plan" → execute morning initialization
"what's next?" → smart task selection with context
"capture <input>" → quick task/idea capture with categorization

# Context queries
"current projects" → active project status overview
"urgent tasks" → high-priority items with deadline awareness
"low energy tasks" → energy-appropriate task suggestions

# System queries
"sync status" → integration health check
"today's progress" → completion summary and momentum
```

#### Technical Implementation

1. **Parser Function** (Python/Shell)
   - Pattern matching for common phrases
   - Confidence scoring for ambiguous input
   - Fallback to clarification prompts

2. **Command Mapping**
   - Direct mapping to existing ProdOS command structure
   - Parameter extraction from natural language
   - Context injection based on current state

#### Deliverables

- [ ] Natural language parser script
- [ ] Command mapping configuration
- [ ] Basic pattern recognition tests
- [ ] Error handling for unclear input

### Phase 1.2: Shell Alias System

**Goal**: Provide immediate usability through simple command shortcuts

#### Core Aliases

```bash
# Primary workflows
alias daily="prodos daily-plan"
alias next="prodos what-next"
alias capture="prodos quick-capture"
alias status="prodos sync-status"

# Context-aware shortcuts
alias urgent="prodos urgent-tasks"
alias lowkey="prodos low-energy-tasks"
alias projects="prodos current-projects"
alias progress="prodos today-progress"
```

#### Advanced Features

- **Smart Context Detection**: Detect current directory, time of day, recent activity
- **Parameter Passing**: Support for `capture "meeting notes"` syntax
- **Chained Commands**: `daily && next` for morning workflow

#### Deliverables

- [ ] Shell alias configuration file
- [ ] Installation script for user environment
- [ ] Parameter handling functions
- [ ] Context detection utilities

### Phase 1.3: Response Formatting

**Goal**: ADHD-optimized output that reduces cognitive overhead

#### Design Principles

1. **Clear Action Steps**: Numbered lists with specific next actions
2. **Visual Hierarchy**: Headers, bullets, and spacing for scannability
3. **Context Preservation**: Show current state and suggested transitions
4. **Progress Indicators**: Visual feedback on completion and momentum

#### Response Templates

```markdown
# Daily Plan (8:32 AM)

## 🎯 Priority Focus

- [HIGH] FFAPP-4565: Complete authentication endpoint testing
- [MED] Update project documentation

## ⚡ Energy Match

Current energy: Medium → Suggested: Code review tasks

- Review PR #234 (15min)
- Update API documentation (30min)

## 📊 Today's Capacity

Tasks: 3 scheduled | Estimated: 2.5 hours | Buffer: Available
```

#### Deliverables

- [ ] Response template library
- [ ] Context-aware formatting functions
- [ ] Progress visualization utilities
- [ ] ADHD-optimized styling guidelines

### Phase 1.4: Context Detection Engine

**Goal**: Understand current user state for intelligent recommendations

#### Context Dimensions

1. **Time Context**: Hour of day, day of week, deadline proximity
2. **Energy Context**: Historical patterns, recent completion rates
3. **Project Context**: Current directory, recent Git activity, open files
4. **System Context**: Available integrations, sync status, capacity

#### Implementation Strategy

```python
class ContextEngine:
    def detect_current_context(self):
        return {
            'time': self.get_time_context(),
            'energy': self.estimate_energy_level(),
            'project': self.detect_active_project(),
            'system': self.check_system_health()
        }

    def recommend_tasks(self, context, available_tasks):
        # Apply ProdOS urgency scoring with context weighting
        # Return ranked task list with reasoning
```

#### Deliverables

- [ ] Context detection library
- [ ] Energy level estimation algorithm
- [ ] Project context detection
- [ ] Recommendation engine integration

### Phase 1.5: Error Handling & Polish

**Goal**: Graceful handling of edge cases and system unavailability

#### Error Categories

1. **Unclear Commands**: "I didn't understand that. Try 'daily', 'next', or 'capture <task>'"
2. **System Unavailability**: "Todoist sync unavailable. Working with cached data."
3. **Empty Results**: "No urgent tasks found. Great job! Try 'next' for other options."
4. **Context Missing**: "Unable to detect current project. Use 'projects' to see all options."

#### Recovery Strategies

- **Graceful Degradation**: Work with available systems when others are offline
- **Helpful Suggestions**: Offer alternative commands when input is unclear
- **Cache Utilization**: Use local data when remote systems are unavailable
- **Progressive Disclosure**: Start simple, offer more detail on request

#### Deliverables

- [ ] Error handling framework
- [ ] Fallback response templates
- [ ] Cache management utilities
- [ ] User guidance system

## Integration Requirements

### Backend Dependencies

- **Obsidian Integration**: Leverage proven bidirectional sync
- **Todoist Integration**: Use existing MCP connection (495ms avg response)
- **ProdOS Framework**: Apply urgency scoring and Natural Planning Model
- **Shell Environment**: Bash/Zsh compatibility for aliases

### Data Flow

```
Natural Language Input
  → Parser (confidence check)
  → Command Mapping
  → Backend Integration (MCP)
  → Context Enhancement
  → Response Formatting
  → User Output
```

### Performance Requirements

- **Response Time**: <2 seconds for standard queries
- **Availability**: Graceful degradation when systems offline
- **Cache Utilization**: Minimize API calls through intelligent caching
- **Memory Footprint**: Lightweight scripts suitable for shell environment

## Testing Strategy

### Test Categories

1. **Parser Accuracy**: Verify natural language → command mapping
2. **Integration Health**: Confirm backend system connectivity
3. **Response Quality**: Validate ADHD-optimized formatting
4. **Error Handling**: Test graceful failure modes
5. **Performance**: Measure response times under load

### Test Scenarios

```bash
# Core workflow tests
test_daily_planning_workflow
test_task_selection_accuracy
test_quick_capture_functionality

# Edge case tests
test_unclear_command_handling
test_offline_system_degradation
test_empty_result_responses

# Integration tests
test_obsidian_todoist_sync_integration
test_context_detection_accuracy
test_cross_system_data_consistency
```

## Success Metrics

### Immediate (2-3 weeks)

- [ ] 5 core commands working: daily, next, capture, status, urgent
- [ ] <2s average response time
- [ ] 90% parser accuracy for common phrases
- [ ] Graceful error handling for unclear input

### Medium-term (1-2 months)

- [ ] Context-aware task recommendations
- [ ] Shell aliases integrated in user environment
- [ ] Background sync monitoring and health reporting
- [ ] ADHD user feedback incorporation

### Long-term (3+ months)

- [ ] Learning from user patterns
- [ ] Predictive task selection
- [ ] Seamless multi-system orchestration
- [ ] Zero-friction daily workflow execution

## Implementation Notes

### Development Environment Setup

1. Ensure MCP tools are configured and tested
2. Validate Obsidian-Todoist sync is operational
3. Set up Python environment for parser development
4. Configure shell environment for alias testing

### Risk Mitigation

1. **Backend Dependency**: Proven Obsidian-Todoist sync reduces integration risk
2. **Parser Complexity**: Start with simple pattern matching, enhance iteratively
3. **User Adoption**: Begin with power-user shell aliases, expand to broader interface
4. **Performance**: Cache aggressively, degrade gracefully, optimize incrementally

---

*This specification builds on the proven foundation of ProdOS's operational backend to deliver the natural language interface identified as the highest priority Phase 1 feature.*
