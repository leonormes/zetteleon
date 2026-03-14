---
created: 2026-03-14T09:49:41+00:00
modified: 2026-03-14T11:09:53+00:00
tags: [articles]
title: GitHub - craigderingtonprox A modern process manager with a beautiful Terminal User Interface (TUI). Inspired by pm2, built with Go and Bubbletea.
---

## GitHub - craigderington/prox: A Modern Process Manager with a Beautiful Terminal User Interface (TUI). Inspired by Pm2, Built with Go and Bubbletea

![rw-book-cover](https://opengraph.githubassets.com/4cb94a3b89fda4cad1bcf62ee960282c76e5b00a0e9549eaa825acbae8e9b08e/craigderington/prox)

### Metadata

- Author: [[https://github.com/craigderington/]]
- Full Title: GitHub - craigderington/prox: A modern process manager with a beautiful Terminal User Interface (TUI). Inspired by pm2, built with Go and Bubbletea.
- Category: articles
- Summary: prox is a modern process manager with a beautiful terminal UI for running apps in any language. It shows real-time metrics, logs, and supports graceful control, state persistence, and YAML configs. Installable via go, it offers keyboard navigation, auto-detected interpreters, and CLI commands for start/stop/restart.
- URL: <https://github.com/craigderington/prox>

### Full Document

#### craigderington/prox

master

Go to file

Code

Open more actions menu

#### ⚡ Prox

A modern, powerful process manager with a beautiful Terminal User Interface (TUI). Inspired by pm2, built with Go and [Bubbletea](https://github.com/charmbracelet/bubbletea).

[![prox](https://camo.githubusercontent.com/7731e5532bf1eab38fdafb072f6a0f5eac961fb193a9b5865ae08e9ca4f39c85/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f676f2d312e32352b2d3030414444383f7374796c653d666c6174266c6f676f3d676f)](https://camo.githubusercontent.com/7731e5532bf1eab38fdafb072f6a0f5eac961fb193a9b5865ae08e9ca4f39c85/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f676f2d312e32352b2d3030414444383f7374796c653d666c6174266c6f676f3d676f)

[![License](https://camo.githubusercontent.com/f8df3091bbe1149f398a5369b2c39e896766f9f6efba3477c63e9b4aa940ef14/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d677265656e)](https://camo.githubusercontent.com/f8df3091bbe1149f398a5369b2c39e896766f9f6efba3477c63e9b4aa940ef14/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d677265656e)

[![prox](https://github.com/craigderington/prox/raw/master/assets/prox-monitor.png)](https://github.com/craigderington/prox/blob/master/assets/prox-monitor.png)

##### ✨ Features

- 🚀 Universal Process Management - Run applications in any language (Node.js, Python, Go, Rust, Ruby, Bash, etc.)
- 🎨 Beautiful TUI - Three interactive views: Dashboard, Monitor, and Logs
- 📊 Real-time Metrics - CPU, memory, network, and uptime monitoring
- 🔄 Smart Process Control - Graceful shutdown with SIGTERM → SIGKILL fallback
- 💾 State Persistence - Processes survive prox restarts via `~/.prox/state.json`
- 📝 Log Management - Live log tailing with continuous file writing
- ⌨️ Vim-like Navigation - Keyboard-first interface (hjkl, arrows)
- 📦 YAML Configuration - Define all your services in `prox.yml`
- 🔧 Auto-detection - Automatically detects interpreters by file extension
- 🎯 Process Monitoring - 4-panel detailed view (pm2 monit style)
- 📜 Log Viewer - Real-time log streaming with export capabilities

##### 📦 Installation

###### Option 1: Install via Go Install (Recommended)

```
go install github.com/craigderington/prox@latest
```

This installs the `prox` binary to `$GOPATH/bin` (usually `~/go/bin`). Make sure this directory is in your `PATH`.

###### Option 2: Build from Source

```
# Clone the repository
git clone https://github.com/craigderington/prox.git
cd prox

# Build the binary
go build -o prox .

# Optional: Install globally
sudo mv prox /usr/local/bin/
```

##### 🚀 Quick Start

###### Launch Interactive TUI (Default Mode)

```
prox
```

The TUI provides three main views:

1. Dashboard - Overview of all processes with quick actions
2. Monitor - Detailed 4-panel view for selected process (like pm2 monit)
3. Logs - Real-time log viewer with continuous export capability

###### CLI Commands

```
# Start a process
prox start app.py --name my-worker

# Start with custom interpreter and working directory
prox start server.js --name api --cwd /path/to/app --interpreter node

# Start all services from prox.yml
prox start-all

# List all processes
prox list

# View process logs
prox logs my-worker

# Stop a process
prox stop my-worker

# Restart a process
prox restart my-worker

# Delete a process
prox delete my-worker

# Initialize prox.yml from existing processes
prox init
```

##### 📋 Configuration File (prox.yml)

Create a `prox.yml` file to define all your services:

```
services:
  - name: web-server
    script: server.js
    interpreter: node
    cwd: /path/to/app
    args:
      - --port
      - "3000"
    env:
      NODE_ENV: production
      PORT: "3000"

  - name: worker
    script: worker.py
    interpreter: python3
    cwd: /path/to/worker
    env:
      PYTHONUNBUFFERED: "1"

  - name: api
    script: ./api
    cwd: /path/to/api
    env:
      GO_ENV: production
```

Then start all services at once:

```
prox start-all
```

##### 🎮 Keyboard Shortcuts

###### Dashboard View

| Key | Action |
| --- | --- |
| `↑/k` | Move selection up |
| `↓/j` | Move selection down |
| `n` | Start a new process (interactive input) |
| `Enter` | Open monitor view for selected process |
| `l` | Open logs view for selected process |
| `r` | Restart selected process |
| `s` | Stop selected process |
| `d` | Delete selected process |
| `R` | Refresh process list |
| `q` | Quit |

###### Monitor View (4-Panel Detailed View)

| Key | Action |
| --- | --- |
| `↑/k` | Move selection up in process list |
| `↓/j` | Move selection down in process list |
| `tab` | Switch between panels (Processes → Metrics → Metadata → Logs) |
| `f` | Toggle follow mode in logs panel |
| `w` | Write logs to file (when logs panel focused) |
| `r` | Restart selected process |
| `s` | Stop selected process |
| `d` | Delete selected process |
| `Esc/q` | Return to dashboard |

###### Logs View

| Key | Action |
| --- | --- |
| `↑/k` | Scroll up one line |
| `↓/j` | Scroll down one line |
| `u` | Scroll up half page |
| `d` | Scroll down half page |
| `g` | Go to top |
| `G` | Go to bottom |
| `f` | Toggle follow mode (auto-scroll) |
| `w` | Toggle continuous writing - Turns GOLD when actively writing logs to file |
| `r` | Refresh logs |
| `Esc/q` | Return to dashboard |

###### ✨ Continuous Log Writing

The `w` key in the logs view now works as a toggle:

- Press `w` once: Starts continuous writing mode
	- Creates a timestamped file (e.g., `myapp_logs_2025-12-25_14-30-00.txt`)
	- Writes all current logs
	- Continuously appends new logs as they arrive
	- Indicator turns GOLD showing "w WRITING"
- Press `w` again: Stops writing and closes the file
	- Indicator returns to normal "w write"

##### 🔧 Auto-detected Interpreters

prox automatically detects the interpreter based on file extension:

| Extension | Interpreter |
| --- | --- |
| `.js`, `.mjs`, `.cjs` | `node` |
| `.ts` | `ts-node` |
| `.py` | `python` |
| `.rb` | `ruby` |
| `.sh` | `bash` |
| `.pl` | `perl` |
| `.php` | `php` |

Or specify manually:

```
prox start script.py --interpreter python3
```

##### 📁 Data Storage

All process state and data is stored in `~/.prox/`:

```
~/.prox/
├── state.json          # Process configurations and status
├── logs/               # Process logs (stdout/stderr)
│   ├── myapp-out.log
│   └── myapp-err.log
├── pids/               # PID files
└── processes/          # Process definitions

```

##### 🏗️ Architecture

Built with modern Go libraries:

- [Bubbletea](https://github.com/charmbracelet/bubbletea) - TUI framework (Elm Architecture)
- [Bubbles](https://github.com/charmbracelet/bubbles) - TUI components (viewports, text inputs)
- [Lipgloss](https://github.com/charmbracelet/lipgloss) - Terminal styling and layout
- [gopsutil](https://github.com/shirou/gopsutil) - Cross-platform system and process metrics
- [Cobra](https://github.com/spf13/cobra) - CLI framework

##### 🎯 Use Cases

- Development: Manage microservices locally
- Production: Simple process orchestration on single servers
- Testing: Run and monitor test suites
- Scripts: Manage background tasks and cron alternatives

##### 🔍 Example Workflow

```
# Start your services from YAML
prox start-all

# Launch TUI to monitor everything
prox

# In the TUI:
# - Press 'Enter' on a process to see detailed metrics
# - Press 'l' to view live logs
# - Press 'w' to start continuous log writing
# - Press 'r' to restart a service
# - Press 'q' to quit

# Or use CLI commands
prox logs api --follow
prox restart worker
prox list
```

##### 🛠️ Development

###### Build & Test

```
# Build
go build -o prox .

# Run tests
go test ./...

# Run with race detection
go test -race ./...

# Install locally
go install
```

##### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

##### 📄 License

MIT License - see [LICENSE](https://github.com/craigderington/prox/blob/master/LICENSE) file for details

##### 🙏 Acknowledgments

- Inspired by [pm2](https://pm2.keymetrics.io/)
- Built with the amazing [Charm](https://charm.sh/) libraries
- Community feedback and contributions

Made with ❤️ and Go
