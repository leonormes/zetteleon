---
created: 2026-03-14T09:49:38+00:00
modified: 2026-03-14T11:10:05+00:00
tags: [articles]
title: GitHub - sinelawfresh Text editor for your terminal easy, powerful and fast
---

## GitHub - sinelaw/fresh: Text Editor for Your Terminal: Easy, Powerful and Fast

![rw-book-cover](https://repository-images.githubusercontent.com/907990001/44bf7e88-629c-4a5d-b807-85e6d05fa7a5)

### Metadata

- Author: [[GitHub]]
- Full Title: GitHub - sinelaw/fresh: Text editor for your terminal: easy, powerful and fast
- Category: articles
- Summary: Fresh is a fast and easy-to-use text editor for the terminal that feels like modern GUI editors. It handles large files smoothly and supports features like mouse control, plugins, and language servers. Fresh works on many platforms and is simple to install with various methods.
- URL: <https://share.google/S4tJ0nk6rDrIHHG24>

### Full Document

#### sinelaw/fresh

master

Go to file

Code

Open more actions menu

##### Folders and Files

##### Repository Files Navigation

- [README](https://github.com/sinelaw/fresh/#)
- [GPL-2.0 license](https://github.com/sinelaw/fresh/#)

#### Fresh

A terminal-based text editor. [Official Website →](https://sinelaw.github.io/fresh/)

[📦 Installation Instructions](https://github.com/sinelaw/fresh/#installation)

[Contributing](https://github.com/sinelaw/fresh/#contributing)

##### Why?

Why another text editor? Fresh brings the intuitive, conventional UX of editors like VS Code and Sublime Text to the terminal.

While veterans like Emacs and Vim - and newer editors like Neovim and Helix - are excellent for power users who prefer modal, highly specialized workflows, they often present a steep learning curve for those used to standard GUI interactions. Fresh is built for the developer who wants a familiar, non-modal experience out-of-the-box, without sacrificing the speed and portability of the command line. Keyboard bindings, mouse support, menus, command palette etc. are all designed to be familiar to most modern users.

Architecturally, Fresh is built to handle multi-gigabyte files or slow network streams efficiently, maintaining a negligible memory overhead regardless of file size. While traditional editors struggle with latency and RAM bloat on large files, Fresh delivers consistent, high-speed performance on any scale.

The goal for Fresh is to be an intuitive and accessible, high-performance terminal-based editor that "just works" on any hardware, for everyone.

##### Discovery & Ease of Use

Fresh is designed for discovery. It features native UIs, a full Menu system, and a powerful Command Palette. With full mouse support, transitioning from graphical editors is seamless.

##### Modern Extensibility

Extend Fresh easily using modern tools. Plugins are written in TypeScript and run securely in a sandboxed Deno environment, providing access to a modern JavaScript ecosystem without compromising stability.

##### Low-Latency Performance

Fresh is engineered for speed. It delivers a low-latency experience, with text appearing instantly. The editor is designed to be light and fast, reliably opening and editing [huge files up to multi-gigabyte sizes](https://noamlewis.com/blog/2025/12/09/how-fresh-loads-huge-files-fast) without slowdown.

##### Comprehensive Feature Set

- File Management: open/save/new/close, file explorer, tabs, auto-revert, git file finder
- Editing: undo/redo, multi-cursor, block selection, smart indent, comments, clipboard
- Search & Replace: incremental search, find in selection, query replace, git grep
- Navigation: go to line/bracket, word movement, position history, bookmarks, error navigation
- Views & Layout: split panes, line numbers, line wrap, backgrounds, markdown preview
- Language Server (LSP): go to definition, references, hover, code actions, rename, diagnostics, autocompletion
- Productivity: command palette, menu bar, keyboard macros, git log, diagnostics panel
- Plugins & Extensibility: TypeScript plugins, color highlighter, TODO highlighter, merge conflicts, path complete, keymaps
- Internationalization: Multiple language support (see [`locales/`](https://github.com/sinelaw/fresh/blob/master/locales) for available languages), plugin translation system

[![Fresh Screenshot](https://github.com/sinelaw/fresh/raw/master/docs/screenshot1.png)](https://github.com/sinelaw/fresh/blob/master/docs/screenshot1.png)

[![Fresh Screenshot](https://github.com/sinelaw/fresh/raw/master/docs/screenshot2.png)](https://github.com/sinelaw/fresh/blob/master/docs/screenshot2.png)

[![Fresh Screenshot](https://github.com/sinelaw/fresh/raw/master/docs/screenshot3.png)](https://github.com/sinelaw/fresh/blob/master/docs/screenshot3.png)

##### Installation

Quick install (autodetect best method):

`curl https://raw.githubusercontent.com/sinelaw/fresh/refs/heads/master/scripts/install.sh | sh`

Or, pick your preferred method:

| Platform | Method |
| --- | --- |
| macOS | [brew](https://github.com/sinelaw/fresh/#brew) |
| Bazzite/Bluefin/Aurora Linux | [brew](https://github.com/sinelaw/fresh/#brew) |
| Arch Linux | [AUR](https://github.com/sinelaw/fresh/#arch-linux-aur) |
| Debian/Ubuntu | [.deb](https://github.com/sinelaw/fresh/#debianubuntu-deb) |
| Fedora/RHEL | [.rpm](https://github.com/sinelaw/fresh/#fedorarhelopensuse-rpm), [Terra](https://terra.fyralabs.com/) |
| Linux (any distro) | [AppImage](https://github.com/sinelaw/fresh/#appimage), [Flatpak](https://github.com/sinelaw/fresh/#flatpak) |
| All platforms | [Pre-built binaries](https://github.com/sinelaw/fresh/#pre-built-binaries) |
| npm | [npm / npx](https://github.com/sinelaw/fresh/#npm) |
| Rust users (Fast) | [cargo-binstall](https://github.com/sinelaw/fresh/#using-cargo-binstall) |
| Rust users | [crates.io](https://github.com/sinelaw/fresh/#from-cratesio) |
| Nix | [Nix flakes](https://github.com/sinelaw/fresh/#nix-flakes) |
| Developers | [From source](https://github.com/sinelaw/fresh/#from-source) |

###### Brew

On macOS and some linux distros (Bazzite/Bluefin/Aurora):

> Note: On macOS, see [macOS Terminal Tips](https://github.com/sinelaw/fresh/blob/master/docs/USER_GUIDE.md#macos-terminal-tips) for recommended terminal configuration.

```
brew tap sinelaw/fresh
brew install fresh-editor
```

###### Arch Linux ([AUR](https://aur.archlinux.org/packages/fresh-editor-bin))

Binary package (recommended, faster install):

```
git clone https://aur.archlinux.org/fresh-editor-bin.git
cd fresh-editor-bin
makepkg --syncdeps --install
```

Build from source:

```
git clone https://aur.archlinux.org/fresh-editor.git
cd fresh-editor
makepkg --syncdeps --install
```

Using an AUR helper (such as `yay` or `paru`):

```
# Binary package (recommended, faster install)
yay -S fresh-editor-bin

# Or build from source
yay -S fresh-editor
```

###### Debian/Ubuntu (.deb)

Download and install the latest release:

```
curl -sL $(curl -s https://api.github.com/repos/sinelaw/fresh/releases/latest | grep "browser_download_url.*_$(dpkg --print-architecture)\.deb" | cut -d '"' -f 4) -o fresh-editor.deb && sudo dpkg -i fresh-editor.deb
```

Or download the `.deb` file manually from the [releases page](https://github.com/sinelaw/fresh/releases).

###### Fedora/RHEL/openSUSE (.rpm)

Download and install the latest release:

```
curl -sL $(curl -s https://api.github.com/repos/sinelaw/fresh/releases/latest | grep "browser_download_url.*\.$(uname -m)\.rpm" | cut -d '"' -f 4) -o fresh-editor.rpm && sudo rpm -U fresh-editor.rpm
```

Or download the `.rpm` file manually from the [releases page](https://github.com/sinelaw/fresh/releases).

###### AppImage

Download the `.AppImage` file from the [releases page](https://github.com/sinelaw/fresh/releases) and run:

```
chmod +x fresh-editor-VERSION-x86_64.AppImage
./fresh-editor-VERSION-x86_64.AppImage
```

For faster startup (recommended): Extract the AppImage instead of running it directly. This avoids the FUSE mount overhead on each launch (~10x faster):

```
./fresh-editor-VERSION-x86_64.AppImage --appimage-extract
mkdir -p ~/.local/share/fresh-editor ~/.local/bin
mv squashfs-root/* ~/.local/share/fresh-editor/
ln -sf ~/.local/share/fresh-editor/usr/bin/fresh ~/.local/bin/fresh
```

Ensure `~/.local/bin` is in your PATH. Available for x86\_64 and aarch64 architectures.

###### Flatpak

Download the `.flatpak` bundle from the [releases page](https://github.com/sinelaw/fresh/releases) and install:

```
flatpak install --user fresh-editor-VERSION-x86_64.flatpak
flatpak run io.github.sinelaw.fresh
```

See [flatpak/README.md](https://github.com/sinelaw/fresh/blob/master/flatpak/README.md) for building from source.

###### Pre-built Binaries

Download the latest release for your platform from the [releases page](https://github.com/sinelaw/fresh/releases).

###### Npm

```
npm install -g @fresh-editor/fresh-editor
```

Or try it without installing:

```
npx @fresh-editor/fresh-editor
```

###### Using Cargo-binstall

To install the binary directly without compiling (much faster than crates.io):

First, install cargo-binstall if you haven't already

```
cargo install cargo-binstall
```

Then install fresh

```
cargo binstall fresh-editor
```

###### Nix Flakes

Run without installing:

```
nix run github:sinelaw/fresh
```

Or install to your profile:

```
nix profile add github:sinelaw/fresh
```

###### From crates.io

```
cargo install fresh-editor
```

###### From Source

```
git clone https://github.com/sinelaw/fresh.git
cd fresh
cargo build --release
./target/release/fresh [file]
```

##### Documentation

- [User Guide](https://github.com/sinelaw/fresh/blob/master/docs/USER_GUIDE.md)
- [macOS Tips](https://github.com/sinelaw/fresh/blob/master/docs/USER_GUIDE.md#macos-terminal-tips) - Terminal configuration, keyboard shortcuts, and troubleshooting for Mac users
- [Plugin Development](https://github.com/sinelaw/fresh/blob/master/docs/PLUGIN_DEVELOPMENT.md)
- [Architecture](https://github.com/sinelaw/fresh/blob/master/docs/ARCHITECTURE.md)

##### Contributing

Thanks for contributing!

1. Reproduce Before Fixing: Always include a test case that reproduces the bug (fails) without the fix, and passes with the fix. This ensures the issue is verified and prevents future regressions.
2. E2E Tests for New Flows: Any new user flow or feature must include an end-to-end (e2e) test. E2E tests send keyboard/mouse events and examines the final rendered output, do not examine internal state.
3. No timeouts or time-sensitive tests: Use "semantic waiting" (waiting for specific state changes/events) instead of fixed timers to ensure test stability. Wait indefinitely, don't put timeouts inside tests (cargo nextest will timeout externally).
4. Test isolation: Tests should run in parallel. Use the internal clipboard mode in tests to isolate them from the host system and prevent flakiness in CI. Same for other external resources (temp files, etc. should all be isolated between tests, under a per-test temporary workdir).
5. Required Formatting: All code must be formatted with `cargo fmt` before submission. PRs that fail formatting checks will not be merged.
6. Cross-Platform Consistency: Avoid hard-coding newline or CRLF related logic, consider the buffer mode.
7. LSP: Ensure LSP interactions follow the correct lifecycle (e.g., `didOpen` must always precede other requests to avoid server-side errors). Use the appropriate existing helpers for this pattern.

Tip: You can use tmux + send-keys + render-pane to script ad-hoc tests on the UI, for example when trying to reproduce an issue.

##### Privacy

Fresh checks for new versions daily to notify you of available upgrades. Alongside this, it sends basic anonymous telemetry (version, OS/architecture, terminal type) to help understand usage patterns. No personal data or file contents are collected.

To disable both upgrade checks and telemetry, use `--no-upgrade-check` or set `check_for_updates: false` in your config.

##### License

Copyright (c) Noam Lewis

This project is licensed under the GNU General Public License v2.0 (GPL-2.0).
