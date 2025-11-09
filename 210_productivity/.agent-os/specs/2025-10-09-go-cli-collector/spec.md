# Spec Requirements Document

> Spec: Go CLI Universal Collector
> Created: 2025-10-09

## Overview

This specification outlines the first phase of a new Go-based command-line interface (CLI) designed to act as a universal collector for work items from Jira and Todoist. The goal is to aggregate all tasks and issues into a local SQLite database using a unified data model, providing a single source of truth for all pending work. This foundation will later be used to power LLM-driven actions and analysis.

## User Stories

### Story: Unified Work View

As a knowledge worker with tasks spread across multiple platforms, I want to run a single command (`collector sync`) that fetches all my assigned work from Jira and Todoist and stores it in a local database, so that I have a unified, queryable view of all my responsibilities without switching contexts.

## Spec Scope

1. **Unified Data Model**: Define a universal `WorkItem` struct in Go that can represent tasks from both Jira and Todoist, including common fields (ID, Title, Project, Status) and source-specific metadata.

2. **Jira Integration**: Implement a client to connect to the Jira API, fetch all issues assigned to the current user, and transform them into the `WorkItem` structure.

3. **Todoist Integration**: Implement a client to connect to the Todoist API, fetch all of a user's tasks, and transform them into the `WorkItem` structure.

4. **Local Database**: Set up a local SQLite database with a schema that matches the `WorkItem` struct. The database will be stored in a local file (`~/.prodos/work.db`).

5. **Sync Command**: Create a `sync` command in the Go CLI that orchestrates the fetching from all sources and upserts the records into the SQLite database.

## Out of Scope

- **LLM Integration**: No LLM calls will be implemented in this phase. The focus is solely on data collection and storage.
- **Write Operations**: The CLI will be read-only from the source APIs. It will not create, update, or delete tasks in Jira or Todoist.
- **Complex UI**: This is a pure CLI tool. No graphical user interface will be developed.
- **Advanced Queries**: The initial version will not include a query engine to filter or sort the collected items via the CLI. The database can be queried directly with SQL for now.

## Expected Deliverable

1. A Go CLI application named `collector`.
2. The CLI has a `sync` command that successfully fetches all tasks from both Jira and Todoist and stores them in a local SQLite database.
3. A clearly defined `WorkItem` struct in the Go codebase that serves as the canonical data model.
