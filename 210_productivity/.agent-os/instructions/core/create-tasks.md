---
description: Create a Todoist project and task list from an approved feature spec
globs:
alwaysApply: false
version: 2.2
encoding: UTF-8
---

# Todoist Project Creation Rules (ProdOS v2.2)

## Overview

With the user's approval, proceed to creating a structured Todoist project based on the current feature spec, following all ProdOS v2.2 standards.

<pre_flight_check>
EXECUTE: @.agent-os/instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" subagent="todoist-creator" name="create_todoist_project">

### Step 1: Create Todoist Project

Use the `todoist_project_create` tool to create a new project for the feature.

<instructions>
  ACTION: Call `todoist_project_create`.
  PARAMETER `name`: Use the feature spec name as the project name.
  PARAMETER `is_favorite`: Set to `true` for high visibility.
  OUTPUT: Capture the `id` of the newly created project for subsequent steps.
</instructions>

</step>

<step number="2" subagent="todoist-creator" name="create_todoist_sections">

### Step 2: Create Todoist Sections

Based on the major components of the feature spec, create corresponding Sections within the new Todoist project using the `todoist_section_create` tool.

<instructions>
  ACTION: For each major component/phase of the feature, call `todoist_section_create`.
  PARAMETER `project_id`: Use the project ID from Step 1.
  PARAMETER `name`: Use the component name (e.g., "API Endpoints", "Frontend UI", "Testing").
  OUTPUT: Capture the `id` of each new section.
</instructions>

</step>

<step number="3" subagent="todoist-creator" name="create_todoist_tasks">

### Step 3: Create Todoist Tasks

Break down the feature into actionable tasks and create them in the appropriate sections using the `todoist_task_create` tool. Adhere strictly to the ProdOS v2.2 standards for prioritization and labeling.

<task_creation_rules>

- **First Task:** The first task in the first section should always be the `@next_action`.
- **Prioritization:** Apply the P1-P4 model. Use `priority: 4` for P1, `3` for P2, etc.
- **Labeling:** All tasks should receive the `@Work` label. The first task must receive the `@next_action` label.
- **Content:** Task content should be a clear, physical, visible action.
  </task_creation_rules>

<instructions>
  ACTION: For each actionable step in the feature spec, call `todoist_task_create`.
  PARAMETER `project_id`: Use the project ID from Step 1.
  PARAMETER `section_id`: Use the appropriate section ID from Step 2.
  PARAMETER `content`: The specific action to be performed.
  PARAMETER `priority`: Assign priority based on the P1-P4 model.
  PARAMETER `labels`: `["@Work"]`. For the very first task, use `["@Work", "@next_action"]`.
</instructions>

</step>

<step number="4" name="execution_readiness">

### Step 4: Execution Readiness Check

Evaluate readiness to begin implementation by presenting the first task summary and requesting user confirmation to proceed.

<readiness_summary>
<present_to_user> - The name of the new Todoist project. - The first task, identified by the `@next_action` label. - A link to the new Todoist project.
</present_to_user>
</readiness_summary>

<execution_prompt>
PROMPT: "I have created the project '[Project Name]' in Todoist and broken it down into sections and tasks according to the ProdOS v2.2 standards.

The first task is:
**Next Action:** [Content of task with @next_action label]

Would you like me to proceed with this task?"
</execution_prompt>

<execution_flow>
IF user_confirms_yes:
REFERENCE: @.agent-os/instructions/core/execute-task.md
ELSE:
WAIT: For user clarification or modifications.
</execution_flow>

</step>

</process_flow>

<post_flight_check>
EXECUTE: @.agent-os/instructions/meta/post-flight.md
</post_flight_check>
