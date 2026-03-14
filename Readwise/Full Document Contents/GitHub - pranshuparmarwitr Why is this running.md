---
created: 2026-03-14T09:49:42+00:00
modified: 2026-03-14T11:09:48+00:00
tags: [articles]
title: GitHub - pranshuparmarwitr Why is this running
---

## GitHub - pranshuparmar/witr: Why is This Running?

![rw-book-cover](https://opengraph.githubassets.com/bc19dfa7f07c63d338f285feb795e6ecd90fba794e5a8efe18ba3766135b5011/pranshuparmar/witr)

### Metadata

- Author: [[GitHub]]
- Full Title: GitHub - pranshuparmar/witr: Why is this running?
- Category: articles
- Summary: witr is a tool that explains why a process is running by tracing its causal chain from a PID, name, or port. It supports Linux, macOS, Windows, and FreeBSD, and offers various output formats like tree and short views. Installation is easy through scripts, package managers, or direct downloads for multiple platforms.
- URL: <https://share.google/182FeQ9Yh5PZtCVPN>

### Full Document

#### pranshuparmar/witr

main

Go to file

Code

Open more actions menu

##### Folders and Files

##### Repository Files Navigation

- [README](https://github.com/pranshuparmar/witr/#)
- [Code of conduct](https://github.com/pranshuparmar/witr/#)
- [Contributing](https://github.com/pranshuparmar/witr/#)
- [Apache-2.0 license](https://github.com/pranshuparmar/witr/#)
- [Security](https://github.com/pranshuparmar/witr/#)

#### Witr

##### Why is This Running?

[![Go Report Card](https://camo.githubusercontent.com/9df1cc84ec24efa7ed0dec5d847698f2402f0118e1601f7e90d749a78efb7320/68747470733a2f2f676f7265706f7274636172642e636f6d2f62616467652f6769746875622e636f6d2f7072616e7368757061726d61722f77697472)](https://goreportcard.com/report/github.com/pranshuparmar/witr)

[![Go Version](https://camo.githubusercontent.com/19c57723129c1ffa621174aed8e65eddff59112f117b9a43242210fff48f67cf/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f676f2d6d6f642f676f2d76657273696f6e2f7072616e7368757061726d61722f77697472)](https://github.com/pranshuparmar/witr/blob/main/go.mod)

[![Platforms](https://camo.githubusercontent.com/c9b4efc6a4af94d40949c61fe89291414f4450cf877eee2e22906b9494826252/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f706c6174666f726d732d6c696e75782532302537432532306d61636f7325323025374325323077696e646f7773253230253743253230667265656273642d626c7565)](https://github.com/pranshuparmar/witr)

[![Build Status](https://github.com/pranshuparmar/witr/actions/workflows/pr-check.yml/badge.svg)](https://github.com/pranshuparmar/witr/actions/workflows/pr-check.yml)

[![Latest Release](https://camo.githubusercontent.com/40a5d84c3ac994324c5343abbe42a9efe2c14a8402a53ffb86125e4d0fe20913/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f762f72656c656173652f7072616e7368757061726d61722f776974723f6c6162656c3d4c617465737425323052656c65617365)](https://github.com/pranshuparmar/witr/releases/latest)

[![Homebrew](https://camo.githubusercontent.com/8410ee93e3eafe57cbd441be67214858147668f5728efe5c8d2e3433ba645249/68747470733a2f2f696d672e736869656c64732e696f2f686f6d65627265772f762f77697472)](https://formulae.brew.sh/formula/witr)

[![AUR](https://camo.githubusercontent.com/13c37a2ed37357b542e7ded02c56c4c1f92f22406b942ef75eda0c834063a830/68747470733a2f2f696d672e736869656c64732e696f2f6175722f76657273696f6e2f776974722d62696e)](https://aur.archlinux.org/packages/witr-bin)

[![Conda](https://camo.githubusercontent.com/1dcd15fef7e260ceb55a400cb3608c311ed6f8680560534339b8f9db42859cf3/68747470733a2f2f696d672e736869656c64732e696f2f636f6e64612f766e2f636f6e64612d666f7267652f77697472)](https://anaconda.org/conda-forge/witr)

[![witr_banner](https://private-user-images.githubusercontent.com/4262592/532917908-e9c19ef0-1391-4a5f-a015-f4003d3697a9.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjgxMzIxMDIsIm5iZiI6MTc2ODEzMTgwMiwicGF0aCI6Ii80MjYyNTkyLzUzMjkxNzkwOC1lOWMxOWVmMC0xMzkxLTRhNWYtYTAxNS1mNDAwM2QzNjk3YTkucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDExMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAxMTFUMTE0MzIyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZThjOGU2ZDczZmI3NTViZTQ0MDZkYTFhMWMzZDYxNTNkNTE4YzZiYjJiNDM5ZGMxNzNmNjE3NmFjMjBhZWQxNSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.BnKeoxg_N4Rn5AqyDvXQGWXpYHMp5slApUzAO_9o9Ug)](https://private-user-images.githubusercontent.com/4262592/532917908-e9c19ef0-1391-4a5f-a015-f4003d3697a9.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjgxMzIxMDIsIm5iZiI6MTc2ODEzMTgwMiwicGF0aCI6Ii80MjYyNTkyLzUzMjkxNzkwOC1lOWMxOWVmMC0xMzkxLTRhNWYtYTAxNS1mNDAwM2QzNjk3YTkucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDExMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAxMTFUMTE0MzIyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZThjOGU2ZDczZmI3NTViZTQ0MDZkYTFhMWMzZDYxNTNkNTE4YzZiYjJiNDM5ZGMxNzNmNjE3NmFjMjBhZWQxNSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.BnKeoxg_N4Rn5AqyDvXQGWXpYHMp5slApUzAO_9o9Ug)

#### Table of Contents

- [1. Purpose](https://github.com/pranshuparmar/witr/#1-purpose)
- [2. Goals](https://github.com/pranshuparmar/witr/#2-goals)
- [3. Core Concept](https://github.com/pranshuparmar/witr/#3-core-concept)
- [4. Supported Targets](https://github.com/pranshuparmar/witr/#4-supported-targets)
- [5. Output Behavior](https://github.com/pranshuparmar/witr/#5-output-behavior)
- [6. Flags & Options](https://github.com/pranshuparmar/witr/#6-flags--options)
- [7. Example Outputs](https://github.com/pranshuparmar/witr/#7-example-outputs)
- [8. Installation](https://github.com/pranshuparmar/witr/#8-installation)
	- [8.1 Script Installation (Recommended)](https://github.com/pranshuparmar/witr/#81-script-installation-recommended)
	- [8.2 Homebrew (macOS & Linux)](https://github.com/pranshuparmar/witr/#82-homebrew-macos--linux)
	- [8.3 Conda (macOS, Linux & Windows)](https://github.com/pranshuparmar/witr/#83-conda-macos-linux--windows)
	- [8.4 Arch Linux (AUR)](https://github.com/pranshuparmar/witr/#84-arch-linux-aur)
	- [8.5 Prebuilt Packages (deb, rpm, apk)](https://github.com/pranshuparmar/witr/#85-prebuilt-packages-deb-rpm-apk)
	- [8.6 Go (cross-platform)](https://github.com/pranshuparmar/witr/#86-go-cross-platform)
	- [8.7 Manual Installation](https://github.com/pranshuparmar/witr/#87-manual-installation)
	- [8.8 Verify Installation](https://github.com/pranshuparmar/witr/#88-verify-installation)
	- [8.9 Uninstallation](https://github.com/pranshuparmar/witr/#89-uninstallation)
	- [8.10 Run Without Installation](https://github.com/pranshuparmar/witr/#810-run-without-installation)
- [9. Platform Support](https://github.com/pranshuparmar/witr/#9-platform-support)
- [10. Success Criteria](https://github.com/pranshuparmar/witr/#10-success-criteria)

#### 1. Purpose

witr exists to answer a single question:

> Why is this running?

When something is running on a system—whether it is a process, a service, or something bound to a port—there is always a cause. That cause is often indirect, non-obvious, or spread across multiple layers such as supervisors, containers, services, or shells.

Existing tools (`ps`, `top`, `lsof`, `ss`, `systemctl`, `docker ps`) expose state and metadata. They show _what_ is running, but leave the user to infer _why_ by manually correlating outputs across tools.

witr makes that causality explicit.

It explains where a running thing came from, how it was started, and what chain of systems is responsible for it existing right now, in a single, human-readable output.

#### 2. Goals

##### Primary Goals

- Explain why a process exists, not just that it exists
- Reduce time‑to‑understanding during debugging and outages
- Work with zero configuration
- Be safe, read‑only, and non‑destructive
- Prefer clarity over completeness

##### Non‑goals

- Not a monitoring tool
- Not a performance profiler
- Not a replacement for systemd/docker tooling
- Not a remediation or auto‑fix tool

#### 3. Core Concept

witr treats everything as a process question.

Ports, services, containers, and commands all eventually map to PIDs. Once a PID is identified, witr builds a causal chain explaining _why that PID exists_.

At its core, witr answers:

1. What is running?
2. How did it start?
3. What is keeping it running?
4. What context does it belong to?

#### 4. Supported Targets

witr supports multiple entry points that converge to PID analysis.

##### 4.1 Name (process or service)

```
witr node
witr nginx
```

A single positional argument (without flags) is treated as a process or service name. If multiple matches are found, witr will prompt for disambiguation by PID.

##### 4.2 PID

```
witr --pid 14233
```

Explains why a specific process exists.

##### 4.3 Port

```
witr --port 5000
```

Explains the process(es) listening on a port.

#### 5. Output Behavior

##### 5.1 Output Principles

- Single screen by default (best effort)
- Deterministic ordering
- Narrative-style explanation
- Best-effort detection with explicit uncertainty

##### 5.2 Standard Output Sections

###### Target

What the user asked about.

###### Process

Executable, PID, user, command, start time and restart count.

###### Why It Exists

A causal ancestry chain showing how the process came to exist. This is the core value of witr.

###### Source

The primary system responsible for starting or supervising the process (best effort).

Examples:

- systemd unit (Linux)
- launchd service (macOS)
- docker container
- pm2
- cron
- interactive shell

Only one primary source is selected.

###### Context (best effort)

- Working directory
- Git repository name and branch
- Container name / image (docker, podman, kubernetes, colima, containerd)
- Public vs private bind

###### Warnings

Non‑blocking observations such as:

- Process is running as root
- Process is listening on a public interface (0.0.0.0 /::)
- Restarted multiple times (warning only if above threshold)
- Process is using high memory (>1GB RSS)
- Process has been running for over 90 days

#### 6. Flags & Options

```
--pid <n>         Explain a specific PID
--port <n>        Explain port usage
--short           One-line summary
--tree            Show ancestry tree with child processes
--json            Output result as JSON
--warnings        Show only warnings
--no-color        Disable colorized output
--env             Show only environment variables for the process
--help            Show this help message
--verbose         Show extended process information

```

A single positional argument (without flags) is treated as a process or service name.

#### 7. Example Outputs

##### 7.1 Name Based Query

```
witr node
```

```
Target      : node

Process     : node (pid 14233)
User        : pm2
Command     : node index.js
Started     : 2 days ago (Mon 2025-02-02 11:42:10 +05:30)
Restarts    : 1

Why It Exists :
  systemd (pid 1) → pm2 (pid 5034) → node (pid 14233)

Source      : pm2

Working Dir : /opt/apps/expense-manager
Git Repo    : expense-manager (main)
Listening   : 127.0.0.1:5001

```

##### 7.2 Short Output

```
witr --port 5000 --short
```

```
systemd (pid 1) → PM2 v5.3.1: God (pid 1481580) → python (pid 1482060)

```

##### 7.3 Tree Output

```
witr --pid 143895 --tree
```

```
systemd (pid 1)
  └─ init-systemd(Ub (pid 2)
    └─ SessionLeader (pid 143858)
      └─ Relay(143860) (pid 143859)
        └─ bash (pid 143860)
          └─ sh (pid 143886)
            └─ node (pid 143895)
              ├─ node (pid 143930)
              ├─ node (pid 144189)
              └─ node (pid 144234)

```

_Note: Tree view now includes child processes (up to 10) and highlights the target process._

##### 7.4 Multiple Matches

###### 7.4.1 Multiple Matching Processes

```
witr node
```

```
Multiple matching processes found:

[1] PID 12091  node server.js  (docker)
[2] PID 14233  node index.js   (pm2)
[3] PID 18801  node worker.js  (manual)

Re-run with:
  witr --pid <pid>

```

###### 7.4.2 Ambiguous Name (process and service)

```
witr nginx
```

```
Ambiguous target: "nginx"

The name matches multiple entities:

[1] PID 2311   nginx: master process   (service)
[2] PID 24891  nginx: worker process   (manual)

witr cannot determine intent safely.
Please re-run with an explicit PID:
  witr --pid <pid>

```

#### 8. Installation

witr is distributed as a single static binary for Linux, macOS, FreeBSD and Windows.

##### 8.1 Script Installation (Recommended)

The easiest way to install witr is via the install script.

###### 8.1.1 Unix (Linux, macOS, FreeBSD)

Quick install:

```
curl -fsSL https://raw.githubusercontent.com/pranshuparmar/witr/main/install.sh | bash
```

Review before install:

```
curl -fsSL https://raw.githubusercontent.com/pranshuparmar/witr/main/install.sh -o install.sh
cat install.sh
chmod +x install.sh
./install.sh
```

The script will:

- Detect your operating system (`linux`, `darwin` or `freebsd`)
- Detect your CPU architecture (`amd64` or `arm64`)
- Download the latest released binary and man page
- Install it to `/usr/local/bin/witr`
- Install the man page to `/usr/local/share/man/man1/witr.1`
- Pass INSTALL\_PREFIX to override default install path

You may be prompted for your password to write to system directories.

###### 8.1.2 Windows (PowerShell)

Quick install:

```
irm https://raw.githubusercontent.com/pranshuparmar/witr/main/install.ps1 | iex
```

This will:

- Download the latest release (zip) and verify checksum.
- Extract `witr.exe` to `%LocalAppData%\witr\bin`.
- Add the bin directory to your User `PATH`.

##### 8.2 Homebrew (macOS & Linux)

You can install witr using [Homebrew](https://brew.sh/) on macOS or Linux:

```
brew install witr
```

See the [Homebrew Formula page](https://formulae.brew.sh/formula/witr#default) for more details.

##### 8.3 Conda (macOS, Linux & Windows)

You can install witr using [conda](https://docs.conda.io/en/latest/), [mamba](https://mamba.readthedocs.io/en/latest/), or [pixi](https://pixi.prefix.dev/latest/) on macOS, Linux, and Windows:

```
conda install -c conda-forge witr
# alternatively using mamba
mamba install -c conda-forge witr
# alternatively using pixi
pixi global install witr
```

##### 8.4 Arch Linux (AUR)

On Arch Linux and derivatives, install from the [AUR package](https://aur.archlinux.org/packages/witr-bin):

```
yay -S witr-bin
# alternatively using paru
paru -S witr-bin
# or use your preferred AUR helper
```

##### 8.5 Prebuilt Packages (deb, Rpm, apk)

witr provides native packages for major Linux distributions. You can download the latest `.deb`, `.rpm`, or `.apk` package from the [GitHub releases page](https://github.com/pranshuparmar/witr/releases/latest).

- Generic download command using `curl`:

```
# Replace <package name with the actual package that you need>
curl -LO https://github.com/pranshuparmar/witr/releases/latest/download/<package-name>
```

- Debian/Ubuntu (.deb):

```
sudo dpkg -i ./witr-*.deb
# Or, using apt for dependency resolution:
sudo apt install ./witr-*.deb
```

- Fedora/RHEL/CentOS (.rpm):

```
sudo rpm -i ./witr-*.rpm
```

- Alpine Linux (.apk):

```
sudo apk add --allow-untrusted ./witr-*.apk
```

##### 8.6 Go (cross-platform)

You can install the latest version directly from source:

```
go install github.com/pranshuparmar/witr/cmd/witr@latest
```

This will place the `witr` binary in your `$GOPATH/bin` or `$HOME/go/bin` directory. Make sure this directory is in your `PATH`.

##### 8.7 Manual Installation

If you prefer manual installation, follow these simple steps for your platform:

###### 8.7.1 Unix (Linux, macOS, FreeBSD)

```
# 1. Determine OS and Architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
[ "$ARCH" = "x86_64" ] && ARCH="amd64"
[ "$ARCH" = "aarch64" ] && ARCH="arm64"

# 2. Download the binary
curl -fsSL "https://github.com/pranshuparmar/witr/releases/latest/download/witr-${OS}-${ARCH}" -o witr

# 3. Verify checksum (Optional)
curl -fsSL "https://github.com/pranshuparmar/witr/releases/latest/download/SHA256SUMS" -o SHA256SUMS
grep "witr-${OS}-${ARCH}" SHA256SUMS | (sha256sum -c - 2>/dev/null || shasum -a 256 -c - 2>/dev/null)
rm SHA256SUMS

# 4. Rename and install
chmod +x witr
sudo mkdir -p /usr/local/bin
sudo mv witr /usr/local/bin/witr

# 5. Install man page (Optional)
sudo mkdir -p /usr/local/share/man/man1
sudo curl -fsSL https://github.com/pranshuparmar/witr/releases/latest/download/witr.1 -o /usr/local/share/man/man1/witr.1
```

###### 8.7.2 Windows (PowerShell)

```
# 1. Determine Architecture
if ($env:PROCESSOR_ARCHITECTURE -eq "AMD64") {
    $ZipName = "witr-windows-amd64.zip"
} elseif ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") {
    $ZipName = "witr-windows-arm64.zip"
} else {
    Write-Error "Unsupported architecture: $($env:PROCESSOR_ARCHITECTURE)"
    exit 1
}

# 2. Download the zip
Invoke-WebRequest -Uri "https://github.com/pranshuparmar/witr/releases/latest/download/$ZipName" -OutFile "witr.zip"

# 3. Extract the binary
Expand-Archive -Path "witr.zip" -DestinationPath "." -Force

# 4. Verify checksum (Optional)
Invoke-WebRequest -Uri "https://github.com/pranshuparmar/witr/releases/latest/download/SHA256SUMS" -OutFile "SHA256SUMS"
$hash = Get-FileHash -Algorithm SHA256 .\witr.zip
$expected = Select-String -Path .\SHA256SUMS -Pattern $ZipName
if ($expected -and $hash.Hash.ToLower() -eq $expected.Line.Split(' ')[0]) { Write-Host "Checksum OK" } else { Write-Host "Checksum Mismatch" }

# 5. Install to local bin directory
$InstallDir = "$env:LocalAppData\witr\bin"
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
Move-Item .\witr.exe $InstallDir\witr.exe -Force

# 6. Add to User Path (Persistent)
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$InstallDir", "User")
    $env:Path += ";$InstallDir"
    Write-Host "Added to Path. You may need to restart PowerShell."
}

# 7. Cleanup
Remove-Item witr.zip
Remove-Item SHA256SUMS
```

##### 8.8 Verify Installation

```
witr --version
man witr
```

##### 8.9 Uninstallation

To completely remove witr:

###### 8.9.1 Unix (Linux, macOS, FreeBSD)

```
sudo rm -f /usr/local/bin/witr
sudo rm -f /usr/local/share/man/man1/witr.1
```

###### 8.9.2 Windows

```
Remove-Item -Recurse -Force "$env:LocalAppData\witr"
```

##### 8.10 Run Without Installation

###### Nix Flake

If you use Nix, you can build witr from source and run without installation:

```
nix run github:pranshuparmar/witr -- --help
```

###### Pixi

If you use [pixi](https://pixi.prefix.dev/latest/), you can run without installation on macOS or Linux:

```
pixi exec witr --help
```

#### 9. Platform Support

- Linux (x86\_64, arm64) - Full feature support (`/proc`).
- macOS (x86\_64, arm64) - Uses `ps`, `lsof`, `sysctl`, `pgrep`.
- Windows (x86\_64, arm64) - Uses `wmic`, `tasklist`, `netstat`.
- FreeBSD (x86\_64, arm64) - Uses `procstat`, `ps`, `lsof`.

##### 9.1 Feature Compatibility Matrix

| Feature | Linux | macOS | Windows | FreeBSD | Notes |
| --- | --- | --- | --- | --- | --- |
| Process Inspection |  |  |  |  |  |
| Basic process info (PID, PPID, user, command) | ✅ | ✅ | ✅ | ✅ |  |
| Full command line | ✅ | ✅ | ✅ | ✅ |  |
| Process start time | ✅ | ✅ | ✅ | ✅ |  |
| Working directory | ✅ | ✅ | ❌ | ✅ | Windows: hard to get without injection |
| Environment variables | ✅ | ⚠️ | ❌ | ✅ | Windows: not supported. macOS: partial. |
| Network |  |  |  |  |  |
| Listening ports | ✅ | ✅ | ✅ | ✅ |  |
| Bind addresses | ✅ | ✅ | ✅ | ✅ |  |
| Port → PID resolution | ✅ | ✅ | ✅ | ✅ |  |
| Service Detection |  |  |  |  |  |
| systemd | ✅ | ❌ | ❌ | ❌ | Linux only |
| launchd | ❌ | ✅ | ❌ | ❌ | macOS only |
| rc.d | ❌ | ❌ | ❌ | ✅ | FreeBSD only |
| Supervisor | ✅ | ✅ | ✅ | ✅ |  |
| Containers | ✅ | ⚠️ | ❌ | ✅ | Windows/macOS: Docker detects VM context. FreeBSD: Jails. |
| Health & Diagnostics |  |  |  |  |  |
| CPU usage detection | ✅ | ✅ | ✅ | ✅ |  |
| Memory usage detection | ✅ | ✅ | ✅ | ✅ |  |
| Health status detection | ✅ | ✅ | ✅ | ✅ | Windows checks process Status (WMI). |
| Open Files / Handles | ✅ | ✅ | ✅ | ✅ | Verbose mode only. |
| Context |  |  |  |  |  |
| Git repo/branch detection | ✅ | ✅ | ❌ | ✅ | Requires working directory |

Legend: ✅ Full support | ⚠️ Partial/limited support | ❌ Not available

##### 9.2 Permissions Note

###### Linux/FreeBSD

witr inspects system directories which may require elevated permissions.

If you are not seeing the expected information, try running witr with sudo:

```
sudo witr [your arguments]
```

###### macOS

On macOS, witr uses `ps`, `lsof`, and `launchctl` to gather process information. Some operations may require elevated permissions:

```
sudo witr [your arguments]
```

Note: Due to macOS System Integrity Protection (SIP), some system process details may not be accessible even with sudo.

###### Windows

On Windows, witr uses `wmic`, `tasklist`, and `netstat`. To see details for processes owned by other users or system services, you must run the terminal as Administrator.

```
# Run in Administrator PowerShell
./witr.exe [your arguments]
```

#### 10. Success Criteria

witr is successful if:

- A user can answer "why is this running?" within seconds
- It reduces reliance on multiple tools
- Output is understandable under stress
- Users trust it during incidents
