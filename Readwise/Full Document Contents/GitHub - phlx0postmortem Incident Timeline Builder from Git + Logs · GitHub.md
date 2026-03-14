---
created: 2026-03-14T09:50:13+00:00
modified: 2026-03-14T11:09:25+00:00
tags: [articles]
title: GitHub - phlx0postmortem Incident Timeline Builder from Git + Logs · GitHub
---

## GitHub - phlx0/postmortem: Incident Timeline Builder from Git + Logs · GitHub

![rw-book-cover](https://opengraph.githubassets.com/f092d4d038a09559e730354f4b2eba7423d36c98f95f036c6c21c6b6b0286369/phlx0/postmortem)

### Metadata

- Author: [[https://github.com/phlx0/]]
- Full Title: GitHub - phlx0/postmortem: Incident Timeline Builder from Git + Logs · GitHub
- Category: articles
- Summary: Postmortem is a tool that quickly builds incident reports by combining git history, file changes, and Sentry errors. It helps teams identify what changed and when during production issues with one command. The reports show file hotspots, error details, and a timeline of commits to aid fast troubleshooting.
- URL: <https://github.com/phlx0/postmortem>

### Full Document

#### phlx0/postmortem

main

Go to file

Code

Open more actions menu

#### 🔍 Postmortem

When production breaks, stop guessing. Start knowing.

[![CI](https://camo.githubusercontent.com/3dc3f10c0ace2d8915965e6ff3440cc21a52479cd45daee9342ab588124bd597/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f70686c78302f706f73746d6f7274656d2f63692e796d6c3f7374796c653d666c61742d737175617265266c6162656c3d4349)](https://github.com/phlx0/postmortem/actions)

[![Python 3.11+](https://camo.githubusercontent.com/6e675e1a6057eb4316b7aec8552a5be989764c406c2faa94bbb19550a9efd05a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e31312b2d626c75653f7374796c653d666c61742d737175617265266c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465)](https://python.org)

[![License: MIT](https://camo.githubusercontent.com/422db9fd40f5831c765cf6530b6750c081b696bd18d904cf89554df98c676277/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d677265656e3f7374796c653d666c61742d737175617265)](https://github.com/phlx0/postmortem/blob/main/LICENSE)

*Stitches together git history, file hotspots, and Sentry errors

 into a shareable incident report—in seconds.*

```
postmortem --since 2h --output markdown --out-file incident.md
```

##### Why Postmortem?

Production is down. You need to know what changed and when—fast.

That means opening GitHub, scanning commits, cross-referencing deploy times, and asking teammates "did anyone push anything?"—all while the clock is ticking.

postmortem does it in one command.

```
────────────────────────────────────────────────────────────────────────
  🔍  postmortem  ·  my-api
  Since 2h  ·  19:58 UTC
────────────────────────────────────────────────────────────────────────

  🔥  File Hotspots

  ■■■  payments.py     changed 4x  risk 94%
       coupled: db.py  utils.py
  ■■  db.py            changed 3x  risk 71%

  ── Sat 07 Mar 2026 ──

  17:58  ⚠  [ERROR] NullPointerException in PaymentService.charge()  ← Sentry
             payments-api  ·  142 occurrences

  18:21  ●  fix: patch null pointer in payment handler  [3a7f2b1]  ← alice
             ↳ src/payments/handler.py
             ↳ tests/test_payments.py

  19:08  ⇄  Merge branch 'feature/stripe-v3' into main  [9c1e4fd]  ← bob
             ↳ src/stripe/client.py  ↳ src/stripe/webhooks.py  ↳ … +4

────────────────────────────────────────────────────────────────────────
  6 events  ·  2 authors  ·  1 Sentry error  ·  top hotspot: payments.py

```

##### Installation

postmortem installs into an isolated virtualenv at `~/.postmortem` and adds itself to your `$PATH` automatically. Open a new terminal and you're ready.

Linux / macOS

```
curl -sSL https://raw.githubusercontent.com/phlx0/postmortem/main/install.sh | bash
```

Windows (PowerShell)

```
irm https://raw.githubusercontent.com/phlx0/postmortem/main/install.ps1 | iex
```

From source (edits apply instantly—no reinstall needed)

```
git clone https://github.com/phlx0/postmortem
cd postmortem
bash install.sh       # or: .\install.ps1 on Windows
```

Requires: Python 3.11+, git

```
postmortem --version   # verify install
bash install.sh --uninstall   # remove cleanly
```

##### Commands

###### Basic Usage

```
postmortem                                    # last 2 hours, current repo
postmortem --since 30m                        # last 30 minutes
postmortem --since 1d                         # last day
postmortem --since 4h --repo /path/to/repo    # different repo
```

###### Generate a Shareable Report

```
postmortem --since 2h --output markdown --out-file incident.md
```

Paste directly into a GitHub issue or Slack. The report includes a TL;DR table, file hotspot rankings, Sentry errors, and the full commit timeline with collapsible file diffs.

###### Sentry Integration

```
export SENTRY_TOKEN=sntrys_...
export SENTRY_ORG=my-org
export SENTRY_PROJECT=api         # optional — searches all projects if omitted

postmortem --since 2h
```

Or pass inline:

```
postmortem --since 2h --sentry-org my-org --sentry-token sntrys_...
```

###### All Flags

| Flag | Default | Description |
| --- | --- | --- |
| `--since`, `-s` | `2h` | How far back to look: `30m`, `2h`, `1d`, `1w` |
| `--repo`, `-r` | `.` | Path to a git repository |
| `--output`, `-o` | `terminal` | Output format: `terminal` or `markdown` |
| `--out-file`, `-f` | stdout | Write output to a file |
| `--no-color` | false | Disable ANSI colours |
| `--sentry-token` | `$SENTRY_TOKEN` | Sentry auth token |
| `--sentry-org` | `$SENTRY_ORG` | Sentry organisation slug |
| `--sentry-project` | `$SENTRY_PROJECT` | Sentry project slug |
| `--version`, `-v` |  | Show version and exit |

##### What's in the Report

###### 🔥 File Hotspots

Pure git analysis—no config needed. Ranks every file touched during the window by:

- Change frequency—how many times it was modified
- Recency—changes in the last 25% of the window score higher
- Coupling—files that always change together are a hidden coordination risk

The coupling column is often the most useful: if `payments.py` and `db.py` consistently appear in the same commits but aren't directly imported by each other, that's a hidden dependency worth knowing about.

###### 🔴 Sentry Errors

Surfaces issues whose _last seen_ time falls inside the incident window. Requires a read-scope auth token—see [Sentry setup](https://github.com/phlx0/postmortem/#sentry-integration) above.

###### 📋 Git Timeline

Commits, merges, and tags in chronological order, each with author, SHA, and the list of files changed. Merges are labelled separately so you can spot integration points at a glance.

##### Project Structure

```
postmortem/
├── cli.py              Click entry point — stays thin
├── pipeline.py         Wires collectors → Timeline
├── models.py           Event, Timeline, HotspotFile — pure data
├── collectors/
│   ├── __init__.py     BaseCollector ABC
│   ├── git.py          Commits, merges, tags
│   ├── hotspot.py      File frequency + coupling analysis
│   └── sentry.py       Sentry Issues API
├── renderers/
│   ├── __init__.py     BaseRenderer ABC
│   ├── terminal.py     ANSI terminal output
│   └── markdown.py     GitHub-flavoured incident report
└── utils/
    └── time.py         "2h" → datetime

```

###### Adding a Collector

```
# postmortem/collectors/datadog.py
from postmortem.collectors import BaseCollector
from postmortem.models import Event, EventKind

class DatadogCollector(BaseCollector):
    def collect(self) -> list[Event]:
        # hit the Datadog API, return Events
        ...
```

Register it in `pipeline.py`. That's it.

###### Planned Collectors

- GitHub Actions—CI run pass/fail per commit
- Datadog / Grafana—annotation and alert events
- PagerDuty—on-call alerts in the window
- Heroku / Railway—deploy events

PRs welcome.

##### Development

```
git clone https://github.com/phlx0/postmortem
cd postmortem
bash install.sh          # editable install — changes apply immediately

pytest                   # run all tests
ruff check postmortem    # lint
```

See [CONTRIBUTING.md](https://github.com/phlx0/postmortem/blob/main/CONTRIBUTING.md) for the full guide.

Made with ☕ · [MIT License](https://github.com/phlx0/postmortem/blob/main/LICENSE)
