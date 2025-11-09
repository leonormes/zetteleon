# Unified ProdOS Context Loader Specification

## Overview

Create a single, comprehensive context file that enables any LLM to instantly load the complete ProdOS v5.0 system, initialize integrations, and begin strategic productivity guidance. This replaces the current fragmented context loading with a unified approach that works across all LLM platforms.

## Mission Alignment

**From ProdOS mission**: Provide AI-driven productivity operating system featuring a Chief of Staff agent that helps ADHD knowledge workers achieve stress-free productivity through problem-driven work selection and intelligent next-action suggestions.

**Context Loading Problem**: Currently, new LLM sessions require multiple files, commands, and setup steps before they can effectively serve as a ProdOS Chief of Staff agent.

**Solution**: Single comprehensive context file containing all necessary information, status, and integration instructions for immediate operational capability.

## Success Criteria

- New LLM sessions can load complete ProdOS context in a single paste operation
- All system capabilities (Clarity Framework, GTD Co-Pilot, integrations) are immediately available
- Context includes current system status, operational commands, and integration health
- Zero additional setup required beyond context loading and role instruction
- Works consistently across different LLM platforms (Claude, ChatGPT, etc.)

## Architecture Overview

### Context File Structure

```markdown
# ProdOS v5.0 Universal Context Package

├── System Overview & Mission
├── Current Operational Status  
├── Core Framework (Consolidated)
├── Clarity Framework (Problem-Driven Selection)
├── GTD Implementation (Complete Workflows)
├── Command Reference (All Available Commands)
├── Integration Status (Live System State)
├── Templates & Examples
└── Quick Start Instructions
```

### File Organization Requirements

**Single Output File**: `~/prodos-universal-context.md`

- Self-contained with all necessary information
- Optimized for LLM consumption (~2,000 lines maximum)
- Includes live system status and command validation
- Compatible with copy/paste workflow

## Implementation Plan

### Phase 1: Context Consolidation Engine

**Goal**: Create intelligent context compilation from actual system files

#### Core Context Sources

```python
# Primary context sources (in loading order)
CORE_SOURCES = [
    "/Volumes/DAL/Zettelkasten/LLMeon/210_productivity/notes/00_ProdOS_Framework.md",
    "/Volumes/DAL/Zettelkasten/LLMeon/210_productivity/Productivity OS/03_TEMPLATES.md",
    "/Volumes/DAL/Zettelkasten/LLMeon/210_productivity/.agent-os/product/mission.md",
    "/Volumes/DAL/Zettelkasten/LLMeon/210_productivity/.agent-os/product/roadmap.md",
    "/Volumes/DAL/Zettelkasten/LLMeon/210_productivity/.agent-os/product/clarity-framework.md"
]

# Dynamic status checks
SYSTEM_COMMANDS = [
    "~/.local/bin/engage",
    "~/.local/bin/daily-plan",
    "~/.local/bin/what-next",
    "~/.local/bin/weekly-review",
    "~/.local/bin/prodos-mcp-bridge"
]

# MCP Integration validation
MCP_TOOLS = [
    "todoist_task_get",
    "jira_ls_issues",
    "get_active_file",
    "git_status",
    "ask_pieces_ltm"
]
```

#### Deliverables

- [ ] `prodos-universal-loader.py` - Context compilation engine
- [ ] Content optimization for LLM consumption
- [ ] Live system status integration
- [ ] File existence and command validation

### Phase 2: Integration Health Monitoring

**Goal**: Include real-time system health in context

#### Health Check Components

1. **Command Availability**: Verify all Phase 1 commands are executable
2. **MCP Integration**: Test connection to key tools (Todoist, Obsidian, Jira)
3. **File Structure**: Validate core files exist and are accessible
4. **Performance Metrics**: Include sync timing and task counts from operational system

#### Implementation

```python
def get_system_health():
    health_status = {
        'commands': check_command_availability(),
        'mcp_tools': validate_mcp_connections(),
        'file_structure': verify_core_files(),
        'performance': get_performance_metrics()
    }
    return format_health_for_context(health_status)
```

#### Deliverables

- [ ] System health monitoring functions
- [ ] Integration status formatting for LLM context
- [ ] Performance metrics collection
- [ ] Error handling for offline/unavailable services

### Phase 3: Unified Context Format Design

**Goal**: Create optimal LLM-consumable format with all necessary information

#### Context Structure Design

```markdown
# ProdOS v5.0 - Universal Productivity Operating System

## 🎯 MISSION & CAPABILITIES

[Mission, features, and current operational status]

## 🏗️ SYSTEM ARCHITECTURE

[Core framework principles and structure]

## 🧭 CLARITY FRAMEWORK

[Problem-driven work selection methodology]

## ⚙️ GTD IMPLEMENTATION

[Complete Getting Things Done workflows]

## 🤖 CONVERSATIONAL COMMANDS

[All available commands with examples and usage]

## 🔗 INTEGRATION STATUS

[Real-time status of Todoist, Obsidian, Jira, MCP tools]

## 📋 TEMPLATES & EXAMPLES

[Key templates for problems, projects, daily planning]

## 🚀 QUICK START GUIDE

[Immediate actions for new LLM sessions]
```

#### Content Optimization Principles

1. **Hierarchical Information**: Most important context first
2. **Actionable Intelligence**: Include commands and examples throughout
3. **Current State**: Live system status, not just documentation
4. **Context Preservation**: Enough detail for sophisticated reasoning
5. **ADHD Optimization**: Clear structure, scannable format

#### Deliverables

- [ ] Context format specification
- [ ] Content optimization algorithms
- [ ] Template integration system
- [ ] Quick start instruction generation

### Phase 4: Shell Integration & Aliases

**Goal**: Seamless command-line integration for context loading

#### Command Design

```bash
# Primary context loader
prodos-context --universal     # Generate unified context file
prodos-context --copy          # Copy directly to clipboard
prodos-context --status        # Show system health only
prodos-context --quick         # Minimal context for quick sessions

# Aliases for convenience
alias ctx="prodos-context --copy"
alias ctx-full="prodos-context --universal"
alias ctx-status="prodos-context --status"
```

#### Integration Features

- **Clipboard Integration**: Automatic copy to system clipboard
- **File Output**: Save to standard location for manual copying
- **Status Validation**: Pre-flight checks before context generation
- **Error Handling**: Graceful degradation when services unavailable

#### Deliverables

- [ ] Enhanced shell command with universal context option
- [ ] Clipboard integration for macOS
- [ ] Shell alias configuration
- [ ] Installation/update script

### Phase 5: LLM Session Initialization

**Goal**: Standardized instructions for optimal LLM configuration

#### Standard Initialization Pattern

```markdown
STEP 1: Load Context
[Paste the complete universal context]

STEP 2: Role Configuration  
You are my ProdOS Chief of Staff agent with full access to my operational productivity system.

Key capabilities loaded:

- Universal work consolidation (all sources → @next_action list)
- Clarity Framework for problem-driven work selection
- GTD Co-Pilot with conversational commands
- Integration with Obsidian, Todoist, Jira, and 15+ MCP tools
- ADHD-optimized constraint awareness

Current system status: [Dynamically included from live system]

STEP 3: Validation
Test the system: "What's my optimal next action right now?"
```

#### Platform-Specific Instructions

- **Claude (Anthropic)**: Specific prompting best practices
- **ChatGPT (OpenAI)**: Custom instruction recommendations
- **Local LLMs**: Context window optimization
- **Mobile Clients**: Streamlined initialization

#### Deliverables

- [ ] Standardized initialization templates
- [ ] Platform-specific optimization guides
- [ ] Context validation commands
- [ ] Mobile-friendly quick start version

## Technical Requirements

### File Processing Engine

```python
class UniversalContextLoader:
    def __init__(self):
        self.base_path = Path("/Volumes/DAL/Zettelkasten/LLMeon/210_productivity")
        self.output_path = Path.home() / "prodos-universal-context.md"

    def compile_universal_context(self):
        # Load and optimize all source files
        # Include live system status
        # Format for LLM consumption
        # Validate all references
        pass

    def validate_system_health(self):
        # Check all commands are executable
        # Verify MCP tool connections
        # Validate file structure integrity
        pass
```

### Performance Targets

- **Context Generation**: <3 seconds for full universal context
- **File Size**: <200KB for optimal copy/paste performance
- **LLM Loading**: <5 seconds in most LLM clients
- **Success Rate**: 95%+ successful context loading across platforms

### Error Handling Strategy

- **Graceful Degradation**: Include warning markers for unavailable components
- **Fallback Content**: Cached context when live system unavailable
- **Clear Messaging**: Specific error messages with resolution steps
- **Partial Loading**: Core functionality even when some integrations offline

## Integration Dependencies

### Current System Dependencies

- Existing ProdOS framework files in known locations
- Phase 1 conversational commands (`engage`, `daily-plan`, `what-next`, `weekly-review`)
- MCP tool ecosystem (Todoist, Obsidian, Jira, Pieces, Git)
- Shell environment with alias support (zsh)

### New Dependencies

- Python 3.11+ for context compilation
- System clipboard access (macOS `pbcopy`)
- File system permissions for context generation
- Network access for MCP tool validation (optional)

## Testing Strategy

### Test Categories

1. **Context Generation**: Verify complete context compiles correctly
2. **System Health**: Validate all status checks function properly
3. **LLM Compatibility**: Test across different LLM platforms
4. **Error Handling**: Verify graceful degradation scenarios
5. **Performance**: Measure generation and loading times

### Test Scenarios

```bash
# Core functionality tests
test_universal_context_generation
test_system_health_monitoring
test_clipboard_integration
test_file_output_format

# Integration tests
test_mcp_tool_validation
test_command_availability_check
test_file_structure_verification

# Error handling tests
test_missing_file_handling
test_offline_service_degradation
test_invalid_command_recovery
```

### Success Metrics

- [ ] Universal context generates in <3 seconds
- [ ] 100% of existing functionality preserved
- [ ] 95%+ LLM session success rate
- [ ] Zero manual setup steps beyond context paste
- [ ] All Phase 1 commands immediately available

## Implementation Timeline

### Week 1: Core Context Engine

- [ ] Design unified context structure
- [ ] Implement content compilation algorithm
- [ ] Create system health monitoring
- [ ] Basic file output functionality

### Week 2: Integration & Optimization

- [ ] Add MCP tool validation
- [ ] Implement clipboard integration
- [ ] Optimize content for LLM consumption
- [ ] Create shell aliases and commands

### Week 3: Testing & Polish

- [ ] Test across multiple LLM platforms
- [ ] Refine error handling and fallbacks
- [ ] Create comprehensive documentation
- [ ] Performance optimization

### Week 4: Deployment & Validation

- [ ] Deploy universal context loader
- [ ] Validate with real workflow scenarios
- [ ] Create user guide and quick reference
- [ ] Migration from current context system

## Risk Mitigation

### Technical Risks

1. **File Structure Changes**: Design flexible path resolution
2. **MCP Tool Availability**: Graceful degradation when tools offline
3. **Context Size**: Intelligent content optimization for LLM limits
4. **Performance**: Caching strategies for large file processing

### User Experience Risks

1. **Complexity**: Maintain simple single-command interface
2. **Reliability**: Comprehensive error handling and fallbacks
3. **Adoption**: Clear migration path from existing context loader
4. **Platform Compatibility**: Test extensively across LLM clients

---

*This specification creates a unified context loading system that transforms any LLM into a fully operational ProdOS Chief of Staff agent with a single paste operation, enabling immediate strategic productivity guidance.*
