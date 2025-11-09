---
aliases: []
confidence: 
created: 2025-09-10T16:49:47Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Tip_027_External_Commands
type:
uid: 
updated: 
version:
---

## Tip 027: Integrate Shell Commands into Vim Workflow

### Problem

You need to run shell commands, view their output, or insert command results into your buffer without leaving Vim.

### Solution

Use Vim's shell integration commands to execute external programs:

```vim
:!ls -la                    " Execute command, view output
:read! date                 " Insert command output into buffer
:!!                         " Repeat last command
```

### Command Types

#### Execute and View

- `:! <cmd>` - Execute shell command and show output
- `:!!` - Repeat the last external command

#### Insert Output

- `:read! <cmd>` or `:r! <cmd>` - Execute command and insert output at cursor
- `:read!!` or `:r!!` - Repeat last command and insert output

### Practical Examples

#### System Information

```vim
:!man ascii                 " View ASCII table
:r! date                    " Insert current date
:r! uuidgen                 " Insert UUID
:r! whoami                  " Insert username
```

#### File Operations

```vim
:!ls -la                    " List directory contents
:!find . -name "*.vim"      " Find Vim files
:r! cat ~/.vimrc            " Insert vimrc contents
```

#### Development Workflow

```vim
:!git status                " Check git status
:!make                      " Build project
:r! git log --oneline -5    " Insert recent commits
```

### Filter Operations

Use ranges with `:!` to filter buffer content:

```vim
" Select lines in visual mode, then:
:'<,'>!sort                 " Sort selected lines
:'<,'>!grep pattern         " Filter lines containing pattern
:1,10!sort                  " Sort first 10 lines
```

### Key Benefits

- **Stay in context** - No need to switch to terminal
- **Insert results** - Command output goes directly into buffer
- **Filter text** - Process buffer content with external tools

### Related Tips

- See [Tip 028](Tip_028_Filter_Commands.md) for advanced filtering
- See [Tip 030](Tip_030_Redirections.md) for capturing command output

---

*Source: A Vim Guide for Adept Users*
