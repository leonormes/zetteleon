---
aliases: [GitHub - DrDroidLabcontext-builder Infrastructure Context for your Coding Agents (Claude Code Cursor) · GitHub]
created: 2026-03-06T18:24:21+00:00
modified: 2026-03-14T11:10:52+00:00
tags: [articles]
title: GitHub - DrDroidLabcontext-builder Infrastructure Context for your Coding Agents (Claude Code Cursor) - GitHub
---

## GitHub - DrDroidLab/context-builder: Infrastructure Context for Your Coding Agents (Claude Code / Cursor) · GitHub

![rw-book-cover](https://opengraph.githubassets.com/7c73f3535a2f892cdf619fd4964a0fcbf610521f8559de5da8837fc91beabdf1/DrDroidLab/context-builder)

### Metadata

- Author: [[https://github.com/DrDroidLab/]]
- Full Title: GitHub - DrDroidLab/context-builder: Infrastructure Context for your Coding Agents (Claude Code / Cursor) · GitHub
- Category: articles
- Summary: Droidctx is an open-source tool that creates detailed infrastructure context files for coding agents like Claude Code. It connects to tools like Kubernetes, Grafana, and Datadog to gather metadata and generate easy-to-read markdown documents. This helps coding agents give faster, more accurate answers by understanding your production environment better.
- URL: <https://github.com/DrDroidLab/context-builder>

### Full Document

#### DrDroidLab/context-builder

main

Go to file

Code

Open more actions menu

#### Droidctx

Infrastructure context builder for Claude Code and coding agents.

Connect your production tools (Grafana, Datadog, Kubernetes, CloudWatch, databases, etc.), extract metadata, and generate structured `.md` files that give coding agents instant context about your infrastructure.

![](https://pbs.twimg.com/profile_images/1958859106263105536/oRwx6b2P.jpg)

[Sid Jain](https://twitter.com/TheBengaluruGuy)

[@TheBengaluruGuy](https://twitter.com/TheBengaluruGuy)

I built an Open Source CLI tool that generates infrastructure context for your coding agent.

In less than 60s, it generated documents about [@DrDroidDev](https://twitter.com/DrDroidDev)'s entire production environment for Claude Code.

In less than 5 minutes, it generated 500+ documents for a 12 years old, $5B Security Enterprise with footprint across all 3 clouds, 8000+ k8s nodes and 3 different Grafana instances.

Giving this context to your agent makes the answers more accurate, improves speed and also reduces token usage.

All of this, with just one command.

droidctx sync

And Open Source.

Check it out: <https://t.co/XSe9wbepUq> ⭐⭐⭐

![⭐](https://abs-0.twimg.com/emoji/v2/svg/2b50.svg)

![⭐](https://abs-0.twimg.com/emoji/v2/svg/2b50.svg)

![⭐](https://abs-0.twimg.com/emoji/v2/svg/2b50.svg)

[Posted Mar 5, 2026 at 2:07AM](https://twitter.com/TheBengaluruGuy/status/2029378312414347674)

![](https://pbs.twimg.com/profile_images/1958859106263105536/oRwx6b2P.jpg)

[Sid Jain](https://twitter.com/TheBengaluruGuy)

[@TheBengaluruGuy](https://twitter.com/TheBengaluruGuy)

I built an Open Source CLI tool that generates infrastructure context for your coding agent.

In less than 60s, it generated documents about [@DrDroidDev](https://twitter.com/DrDroidDev)'s entire production environment for Claude Code.

In less than 5 minutes, it generated 500+ documents for a 12 years old, $5B Security Enterprise with footprint across all 3 clouds, 8000+ k8s nodes and 3 different Grafana instances.

Giving this context to your agent makes the answers more accurate, improves speed and also reduces token usage.

All of this, with just one command.

droidctx sync

And Open Source.

Check it out: <https://t.co/XSe9wbepUq> ⭐⭐⭐

![⭐](https://abs-0.twimg.com/emoji/v2/svg/2b50.svg)

![⭐](https://abs-0.twimg.com/emoji/v2/svg/2b50.svg)

![⭐](https://abs-0.twimg.com/emoji/v2/svg/2b50.svg)

[Posted Mar 5, 2026 at 2:07AM](https://twitter.com/TheBengaluruGuy/status/2029378312414347674)

##### Quick Start

```
# Install (creates an isolated venv at ~/.droidctx automatically)
curl -fsSL https://raw.githubusercontent.com/DrDroidLab/context-builder/main/install.sh | bash

# Or via pipx
pipx install git+https://github.com/DrDroidLab/context-builder.git

# Or manually with a venv
python3 -m venv ~/.droidctx && ~/.droidctx/bin/pip install git+https://github.com/DrDroidLab/context-builder.git && mkdir -p ~/.local/bin && ln -sf ~/.droidctx/bin/droidctx ~/.local/bin/droidctx
# 1. Initialize project (creates ./droidctx-context/)
droidctx init

# 2. Auto-detect credentials from local CLI tools (kubectl, aws, gcloud, az)
droidctx detect

# 3. Add any additional credentials manually
vim ./droidctx-context/credentials.yaml

# 4. Sync infrastructure metadata
droidctx sync

# 5. Add the suggested prompt to your CLAUDE.md
```

##### Output Structure

After running `droidctx sync`, your context directory will contain:

```
my-infra/
  resources/
    overview.md                    # Summary of all connected tools
    connectors/
      grafana_prod/
        _summary.md                # Resource counts for this connector
        datasources.md             # Grafana datasources
        dashboards.md              # Dashboard index
        dashboards/
          api-gateway.md           # Individual dashboard with panels & queries
          payment-service.md
        alerts.md                  # Alert rules
      k8s_production/
        _summary.md
        namespaces.md
        deployments.md
        services.md
        ingresses.md
        ...
      datadog_prod/
        _summary.md
        monitors.md
        services.md
        dashboards.md
      postgres_main/
        _summary.md
        tables.md
    cross_references/
      services.md                  # Services seen across multiple connectors

```

##### Using with Claude Code

After syncing, add this to your `CLAUDE.md`:

```
My production infrastructure context is in ./my-infra/resources/.
Refer to this when investigating issues, writing queries, or understanding system topology.

```

##### Commands

###### `droidctx init`

Creates folder structure and a credentials template.

```
droidctx init                      # Creates ./droidctx-context/
droidctx init --path ./my-infra    # Custom path
```

###### `droidctx detect`

Auto-detects credentials from locally configured CLI tools and populates `credentials.yaml`. Scans for `kubectl`, `aws`, `gcloud`, and `az`, extracts their active configurations, and merges discovered connectors into your credentials file without overwriting existing entries.

```
droidctx detect                                # Uses ./droidctx-context/credentials.yaml
droidctx detect --keyfile ./my-infra/creds.yaml # Custom keyfile
```

What gets detected:

| CLI Tool | Connectors Created | Values Extracted |
| --- | --- | --- |
| `kubectl` | KUBERNETES (cli mode) | Cluster name from current context |
| `aws` | CLOUDWATCH, EKS | Region, EKS cluster names |
| `gcloud` | GKE, GCM | Project ID, zone, GKE cluster names |
| `az` | AZURE | Tenant ID, subscription ID (client ID/secret need manual entry) |

Kubernetes connectors created by `detect` use CLI mode (`_cli_mode: true`), which means they extract resources directly via `kubectl` using your current kubeconfig context—no API server URL or token needed.

###### `droidctx sync`

Connects to your tools, extracts metadata, and generates `.md` context files.

```
droidctx sync                                  # Uses ./droidctx-context/credentials.yaml
droidctx sync --keyfile ./my-infra/creds.yaml   # Custom keyfile
droidctx sync --connectors grafana_prod,k8s_prod  # Sync specific connectors
droidctx sync --dry-run                         # Preview what would be synced
droidctx sync --verbose                         # Verbose logging
```

###### `droidctx check`

Validates credentials format and checks for required CLI tools.

```
droidctx check                                 # Uses ./droidctx-context/credentials.yaml
droidctx check --keyfile ./my-infra/creds.yaml  # Custom keyfile
```

###### `droidctx list-connectors`

Shows all supported connector types and their required fields.

```
droidctx list-connectors
droidctx list-connectors --type GRAFANA
```

##### Credentials Format

Create a YAML file with your connector credentials. Run `droidctx init` to generate a template with all supported types, or `droidctx detect` to auto-populate from your CLI tools.

```
# Auto-detected by `droidctx detect` (uses kubectl directly, no token needed)
k8s_my-cluster:
  type: "KUBERNETES"
  _cli_mode: true
  cluster_name: my-cluster

# Auto-detected by `droidctx detect`
cloudwatch_us-east-1:
  type: "CLOUDWATCH"
  region: us-east-1

# Manual entry
grafana_prod:
  type: "GRAFANA"
  grafana_host: https://your-grafana.com
  grafana_api_key: glsa_xxxxxxxxxxxx

datadog_prod:
  type: "DATADOG"
  dd_api_key: your_api_key
  dd_app_key: your_app_key

# Standard Kubernetes (API server + token, without CLI mode)
k8s_production:
  type: "KUBERNETES"
  cluster_name: prod-cluster
  cluster_api_server: https://k8s-api.example.com
  cluster_token: eyJhbGciOiJSUzI1NiIs...

postgres_main:
  type: "POSTGRES"
  host: db.example.com
  port: 5432
  database: production
  user: readonly_user
  password: secret
```

###### CLI Mode for Kubernetes

When `_cli_mode: true` is set on a KUBERNETES connector, droidctx uses `kubectl` directly with your current kubeconfig context instead of requiring an API server URL and token. This is the default when connectors are created via `droidctx detect`. Resources extracted: Namespaces, Services, Deployments, Ingresses, StatefulSets, ReplicaSets, HPAs, and NetworkPolicies.

##### Supported Connectors (25)

| Category | Connectors |
| --- | --- |
| Monitoring | Grafana, Datadog, New Relic, CloudWatch, SigNoz, Sentry |
| Kubernetes | Kubernetes, EKS, GKE |
| Cloud | Azure, GCM (Google Cloud Monitoring) |
| Databases | PostgreSQL, MongoDB, ClickHouse, Generic SQL |
| Search | Elasticsearch, OpenSearch |
| CI/CD | GitHub, ArgoCD, Jenkins |
| Project Management | Jira Cloud |
| Logs | Grafana Loki, Victoria Logs, Coralogix, PostHog |

##### Why

When your coding agent debugs production issues, it wastes tokens fumbling across tools, picks wrong MCP servers, and hallucinates about your setup. Pre-built context files fix that—fewer steps, better hypotheses, less noise.

Your agent will know:

- Which dashboards exist and what metrics they track
- What services are running and where they're deployed
- Which alerts are configured and what they monitor
- What database tables/schemas exist
- How to write queries for your specific tools

##### Requirements

- Python >= 3.9
- Some connectors require CLI tools: `kubectl` (Kubernetes), `aws` (CloudWatch/EKS), `az` (Azure), `gcloud` (GKE/GCM)

##### License

MIT
