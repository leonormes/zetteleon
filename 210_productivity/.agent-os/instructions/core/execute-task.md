---
description: Rules to execute the next available task from Todoist using Agent OS
globs:
alwaysApply: false
version: 2.2
encoding: UTF-8
---

# Task Execution Rules (ProdOS v2.2)

## Overview

Execute the highest-priority actionable task from the Todoist system, following all relevant best practices and standards.

<pre_flight_check>
EXECUTE: @.agent-os/instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" subagent="todoist-reader" name="identify_next_action">

### Step 1: Identify Next Action

Query Todoist to find the single highest-priority task with the `@next_action` label.

<instructions>
  ACTION: Call `todoist_task_get`.
  PARAMETER `filter`: Use the query `"@next_action & p1"` to find the most important next action.
  IF no p1 task exists, broaden the query to `"@next_action & p2"`, and so on.
  OUTPUT: Capture the `id` and `content` of the highest-priority next action.
  CONFIRMATION: Announce to the user which task you are about to start.
</instructions>

</step>

<step number="2" subagent="context-fetcher" name="gather_context">

### Step 2: Gather Task Context

For the identified task, gather all available context. This may involve reading from an Obsidian note if a link is available in the task's description or comments.

<instructions>
  ACTION: Check the Todoist task for a link to an Obsidian note.
  IF a link exists:
    - Read the linked Obsidian note (`read_file`).
    - Analyze the project plan, especially the section the task belongs to.
  ELSE:
    - Rely on the task's description and comments for context.
  ANALYZE: Understand the task's success criteria and its role in the larger project.
</instructions>

</step>

<step number="3" name="execute_work">

### Step 3: Execute the Work

Perform the development work required to complete the task, following all relevant coding standards and best practices from the `.agent-os/standards/` directory.

<tdd_workflow>

- Write or update tests first.
- Implement the required functionality to make the tests pass.
- Refactor the code while keeping tests green.
- Verify all local tests pass before proceeding.
  </tdd_workflow>

</step>

<step number="4" subagent="todoist-writer" name="complete_task">

### Step 4: Mark Task as Complete

Once the work is done and verified, mark the task as complete in Todoist.

<instructions>
  ACTION: Call `todoist_task_complete`.
  PARAMETER `task_id`: Use the ID of the task you identified in Step 1.
  CONFIRMATION: Announce to the user that the task is complete.
</instructions>

</step>

<step number="5" subagent="todoist-writer" name="promote_next_action">

### Step 5: Promote the Next Action

After completing a task, it is critical to identify the *next* `@next_action` for that project to maintain momentum.

<instructions>
  ACTION: Call `todoist_task_get` for the project the completed task was in.
  IDENTIFY: Find the next logical task in the sequence that is not complete.
  ACTION: Call `todoist_task_update` on that identified task.
  PARAMETER `task_id`: The ID of the next task.
  PARAMETER `labels`: Add `@next_action` to its existing labels.
  CONFIRMATION: Announce to the user which task has been promoted to the next action.
</instructions>

</step>

</process_flow>

<post_flight_check>
EXECUTE: @.agent-os/instructions/meta/post-flight.md
</post_flight_check>
