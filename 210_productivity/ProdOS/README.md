---
version:
tags: []
type:
title: README
created: 2025-10-09T14:56:29Z
modified: 2025-10-13T08:14:46Z
---

## ProdOS Collector

`prodos` is a universal collector for your work items. It's a CLI tool to aggregate tasks and issues from various sources like Jira and Todoist into a unified local database.

### Features

- **Sync**: Fetch work items from multiple sources.
- **Embed**: Generate and store embeddings for semantic search.

### Setup

#### 1. Configuration

Create a configuration file at `~/.config/prodos/collector.yaml`:

```yaml
todoist:
  api_token: "YOUR_TODOIST_TOKEN"

# Jira is optional; fill to enable
jira:
  host: "https://your-domain.atlassian.net"
  username: "you@example.com"
  api_token: "YOUR_JIRA_API_TOKEN"
```

Alternatively, you can set environment variables:

```bash
export TODOIST_API_TOKEN="YOUR_TODOIST_TOKEN"
export JIRA_API_TOKEN="YOUR_JIRA_API_TOKEN"
```

#### 3. OpenAI API Key

The embedding process uses OpenAI. Ensure your API key is set as an environment variable:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

### Usage

#### Sync Work Items

The sync command fetches items from Jira and Todoist, saves them to the database, and automatically generates embeddings for semantic search:

```bash
./prodos sync
```

This command will:

1. Fetch tasks from Todoist and Jira
2. Save them to the local SQLite database
3. Generate and store embeddings using OpenAI

#### Query Work Items

Search through your work items using natural language:

```bash
./prodos query "your search query"
```

You can control the number of results with the `-n` flag:

```bash
./prodos query "bug to fix" -n 10
```

#### Generate Embeddings (Optional)

If you want to regenerate embeddings without syncing:

```bash
./prodos embed
```
