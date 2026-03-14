---
created: 2026-03-14T09:50:12+00:00
modified: 2026-03-14T11:09:29+00:00
tags: [articles]
title: GitHub - VG-dev1flux Search, monitor, and nuke processes with ease, with system resource tracking
---

## GitHub - VG-dev1/flux: Search, Monitor, and Nuke Processes with Ease, with System Resource Tracking

![rw-book-cover](https://opengraph.githubassets.com/6485e443abb9aeaf10152655be6f466497f6fc1f1103ed86b8b7f618c4b2c028/VG-dev1/flux)

### Metadata

- Author: [[https://github.com/VG-dev1/]]
- Full Title: GitHub - VG-dev1/flux: Search, monitor, and nuke processes with ease, with system resource tracking
- Category: articles
- Summary: Flux is a simple tool to find and manage processes on your computer. It shows live CPU and memory use and helps you kill processes easily. Flux is easy to use with keyboard shortcuts and clear colors.
- URL: <https://github.com/VG-dev1/flux>

### Full Document

#### VG-dev1/flux

main

Go to file

Code

Open more actions menu

#### Flux

Search, monitor, and nuke processes with ease, with system resource tracking

[![demo](https://github.com/VG-dev1/flux/raw/main/assets/demo1.png)](https://github.com/VG-dev1/flux/blob/main/assets/demo1.png)

[![demo](https://github.com/VG-dev1/flux/raw/main/assets/demo2.png)](https://github.com/VG-dev1/flux/blob/main/assets/demo2.png)

[![GitHub Actions Workflow Status](https://camo.githubusercontent.com/4bff6e63c0858d04234652c6430699029f38c1ed3ee0b461f0c7b8df71aef64a/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f56472d646576312f666c75782f727573742e796d6c3f7374796c653d666f722d7468652d6261646765)](https://camo.githubusercontent.com/4bff6e63c0858d04234652c6430699029f38c1ed3ee0b461f0c7b8df71aef64a/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f56472d646576312f666c75782f727573742e796d6c3f7374796c653d666f722d7468652d6261646765)

[![Crates.io Version](https://camo.githubusercontent.com/fc989e7952a0cc73a276af10ea53de1601ba8ac043cbb7c19adcb896d2228ef6/68747470733a2f2f696d672e736869656c64732e696f2f6372617465732f762f666c75782d636c693f7374796c653d666f722d7468652d6261646765)](https://camo.githubusercontent.com/fc989e7952a0cc73a276af10ea53de1601ba8ac043cbb7c19adcb896d2228ef6/68747470733a2f2f696d672e736869656c64732e696f2f6372617465732f762f666c75782d636c693f7374796c653d666f722d7468652d6261646765)

[![Crates.io License](https://camo.githubusercontent.com/cbfb32041699de6a8027d5d718d51e691204dc8d5fdf3fb68ce0ba84dae26777/68747470733a2f2f696d672e736869656c64732e696f2f6372617465732f6c2f666c75782d636c693f7374796c653d666f722d7468652d6261646765)](https://camo.githubusercontent.com/cbfb32041699de6a8027d5d718d51e691204dc8d5fdf3fb68ce0ba84dae26777/68747470733a2f2f696d672e736869656c64732e696f2f6372617465732f6c2f666c75782d636c693f7374796c653d666f722d7468652d6261646765)

[![Crates.io Total Downloads](https://camo.githubusercontent.com/a849935dc95a7eb403fef8919aa9d6aef5b0e564fdce2036841fb279379d1919/68747470733a2f2f696d672e736869656c64732e696f2f6372617465732f642f666c75782d636c693f7374796c653d666f722d7468652d6261646765)](https://camo.githubusercontent.com/a849935dc95a7eb403fef8919aa9d6aef5b0e564fdce2036841fb279379d1919/68747470733a2f2f696d672e736869656c64732e696f2f6372617465732f642f666c75782d636c693f7374796c653d666f722d7468652d6261646765)

##### Why Flux

Tools like `htop` and `btop` cram an overwhelming amount of information onto the screen-columns, graphs, and stats everywhere, making it hard to find the process you actually care about. `flux` strips away the clutter and focuses on what matters: quickly finding, monitoring, and acting on processes in a clean, readable interface. With live CPU and memory tracking, port-aware process discovery, and intuitive keyboard navigation, `flux` gives you all the actionable insights without the messy visual noise, letting you manage your system faster and more efficiently.

##### Features

- Real-time Resource Monitoring: Track CPU and memory usage, live
- Port Discovery: Identify which processes are listening on specific ports
- Batch Actions: Select multiple processes with `Space` or use `--nuke` to batch-kill by filter
- Easy Navigation: Move around effortlessly with `j/k` or arrow keys
- Smart UI: Context-aware coloring for high resource usage

##### Usage

```
# See all processes, live (sorted by CPU)
flux

# Pre-filter by process name
flux -f chrome

# Use a different signal (default: SIGKILL)
flux -s SIGTERM

# Sort by memory usage
flux --sort mem

# Sort by PID
flux --sort pid

# Sort by name
flux --sort name

# See system resource usage (CPU and memory)
flux --resources

# Kill all the processes with a specific name
flux -f chrome --nuke
```

##### Options

| Flag | Description |
| --- | --- |
| `-f, --filter <name>` | Pre-filter processes by name |
| `-s, --signal <signal>` | Signal to send (default: KILL) |
| `--sort <field>` | Sort by: cpu, mem, pid, name, port |
| `--ports` | Show only processes with open ports |
| `--port <PORT>` | Filter by specific port number |

##### Installation

###### From Source

```
cargo install flux-cli
```

##### License

MIT
