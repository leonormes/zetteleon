---
created: 2026-03-14T09:49:40+00:00
modified: 2026-03-14T11:09:58+00:00
tags: [articles]
title: GitHub - mrkatebzadehcheshmak Minimal, configurable project status banner for your terminal.
---

## GitHub - mrkatebzadeh/cheshmak: Minimal, Configurable Project Status Banner for Your Terminal

![rw-book-cover](https://opengraph.githubassets.com/f548979c807cbe1ce91210185242f9ad9ef66944cf2dffa02be185c4aaec146b/mrkatebzadeh/cheshmak)

### Metadata

- Author: [[https://github.com/mrkatebzadeh/]]
- Full Title: GitHub - mrkatebzadeh/cheshmak: Minimal, configurable project status banner for your terminal.
- Category: articles
- Summary: Cheshmak is a lightweight tool that shows a project status banner when you enter a directory in the terminal. It helps you quickly see git info, project hints, and recent activity without cluttering your prompt. You can install it easily, customize plugins, and control when the summary appears.
- URL: <https://github.com/mrkatebzadeh/cheshmak>

### Full Document

#### mrkatebzadeh/cheshmak

dev

Go to file

Code

Open more actions menu

#### Cheshmak

##### Why Using This Tool

I built cheshmak because every time I `cd` into a project I end up running the same few commands to get my bearings. This tool hooks into `cd` and prints a small, readable summary so you can see the state of a project immediately.

It is intentionally lightweight and fast. The summary is meant to be useful without slowing down your shell.

I do use Starship, but I'm not fond of stuffing the prompt with too much. I want my prompt to stay clean. I also don't need this info on _every_ command, but I do want more context than a tiny prompt segment can provide. Cheshmak hits that middle ground by showing a richer snapshot only the first time I enter a project in a shell session.

[![cheshmak](https://private-user-images.githubusercontent.com/2138804/554185320-b6f37bc9-afde-4764-b870-9a4d0f53ed80.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzE5NDU0MzgsIm5iZiI6MTc3MTk0NTEzOCwicGF0aCI6Ii8yMTM4ODA0LzU1NDE4NTMyMC1iNmYzN2JjOS1hZmRlLTQ3NjQtYjg3MC05YTRkMGY1M2VkODAuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDIyNCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAyMjRUMTQ1ODU4WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODM5NGFjYTQwNjdlMWRjZWRhMTM2OThmZGY0OTNlZjY4ODMyNzM4Mzg0MzMyMzk3ZjI0YjBiY2IxMzdkYmNjZiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.wHpP9ZyHlHnZ4uOKGWtKnMC_TarUG2pnq4slAvXXXBU)](https://private-user-images.githubusercontent.com/2138804/554185320-b6f37bc9-afde-4764-b870-9a4d0f53ed80.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzE5NDU0MzgsIm5iZiI6MTc3MTk0NTEzOCwicGF0aCI6Ii8yMTM4ODA0LzU1NDE4NTMyMC1iNmYzN2JjOS1hZmRlLTQ3NjQtYjg3MC05YTRkMGY1M2VkODAuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDIyNCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAyMjRUMTQ1ODU4WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODM5NGFjYTQwNjdlMWRjZWRhMTM2OThmZGY0OTNlZjY4ODMyNzM4Mzg0MzMyMzk3ZjI0YjBiY2IxMzdkYmNjZiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.wHpP9ZyHlHnZ4uOKGWtKnMC_TarUG2pnq4slAvXXXBU)

  [![cheshmak](https://private-user-images.githubusercontent.com/2138804/554185320-b6f37bc9-afde-4764-b870-9a4d0f53ed80.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzE5NDU0MzgsIm5iZiI6MTc3MTk0NTEzOCwicGF0aCI6Ii8yMTM4ODA0LzU1NDE4NTMyMC1iNmYzN2JjOS1hZmRlLTQ3NjQtYjg3MC05YTRkMGY1M2VkODAuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDIyNCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAyMjRUMTQ1ODU4WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODM5NGFjYTQwNjdlMWRjZWRhMTM2OThmZGY0OTNlZjY4ODMyNzM4Mzg0MzMyMzk3ZjI0YjBiY2IxMzdkYmNjZiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.wHpP9ZyHlHnZ4uOKGWtKnMC_TarUG2pnq4slAvXXXBU)](https://private-user-images.githubusercontent.com/2138804/554185320-b6f37bc9-afde-4764-b870-9a4d0f53ed80.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzE5NDU0MzgsIm5iZiI6MTc3MTk0NTEzOCwicGF0aCI6Ii8yMTM4ODA0LzU1NDE4NTMyMC1iNmYzN2JjOS1hZmRlLTQ3NjQtYjg3MC05YTRkMGY1M2VkODAuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDIyNCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAyMjRUMTQ1ODU4WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODM5NGFjYTQwNjdlMWRjZWRhMTM2OThmZGY0OTNlZjY4ODMyNzM4Mzg0MzMyMzk3ZjI0YjBiY2IxMzdkYmNjZiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.wHpP9ZyHlHnZ4uOKGWtKnMC_TarUG2pnq4slAvXXXBU)

##### How to Install it

1. Visit the GitHub Releases page for Cheshmak.
2. Download the latest binary that matches your platform.
3. Make the binary executable and place it somewhere on your `PATH`.

```
chmod +x cheshmak
mv cheshmak ~/.local/bin/cheshmak
```

Ensure that `~/.local/bin` (or whichever directory you chose) is part of your `PATH`.

##### Shell Integration (hook)

To run Cheshmak automatically on directory change, add the shell hook:

```
cheshmak hook
```

This command adds a small hook to your shell rc file so `cd` prints a summary. The hook itself is intentionally minimal; the binary decides whether to render on each `cd`.

###### Uninstall the Hook

```
cheshmak unhook
```

This removes the hook from your rc file.

###### Shell Compatibility

- bash: edits `~/.bashrc`
- zsh: edits `~/.zshrc`
- fish: edits `~/.config/fish/config.fish`
- nushell: edits `~/.config/nushell/config.nu`

##### How to Use it

Once installed and hooked into your shell, Cheshmak triggers every time you `cd` into a repository. When you enter a project directory, cheshmak can show things like:

- git branch and status
- rust dependency health (if enabled)
- project identity hints
- recent activity

This gives you a quick readout of the things you typically check when opening a project. Use the plugin list in your config file to control which data points appear and how often each plugin refreshes.

##### How to Config it

Cheshmak loads configuration from `~/.config/cheshmak/config.toml`.

Only the plugins listed in `enabled_plugins` will execute. If the list is empty, none of the plugins run.

```
enabled_plugins = ["git", "todo", "project", "hints", "activity"]

# optional tuning
show_table = false
once_per_shell_session = true
hints_max_len = 48
activity_format = "relative"
```

Use this file to enable or disable plugins and to provide tuning options for individual plugins.

Setting `show_table = true` renders the summary as columnar tables with plugin names as headers, wrapping and splitting tables when they exceed the terminal width, similar to nushell's `ls` output.

Setting `once_per_shell_session = false` forces the summary to rerun every time you change directories; keep it `true` (the default) to show each project only once per shell session.

##### Plugin Guide

If you want to add or customize plugins, refer to the [Plugin Guide](https://github.com/mrkatebzadeh/cheshmak/blob/dev/docs/PLUGIN_GUIDE.md).

##### Notes

- If something feels slow, remove that plugin from `enabled_plugins`.
- Some plugins cache results and can be refreshed with flags like `--refresh-rust-upgrades`.
