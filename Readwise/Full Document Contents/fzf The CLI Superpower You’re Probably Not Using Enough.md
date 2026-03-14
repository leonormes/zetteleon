---
created: 2026-03-14T09:49:38+00:00
modified: 2026-03-14T11:10:04+00:00
tags: [articles]
title: fzf The CLI Superpower You’re Probably Not Using Enough
---

## Fzf: The CLI Superpower You're Probably Not Using Enough

![rw-book-cover](https://miro.medium.com/v2/resize:fit:1200/1*y5m-9cHuFtOBXip6fK_3dg.png)

### Metadata

- Author: [[Rafael Umbelino]]
- Full Title: fzf: The CLI Superpower You're Probably Not Using Enough
- Category: articles
- Summary: fzf is a fast and interactive command-line tool that helps you search and filter data easily. It makes working with logs, files, processes, and Git branches much simpler and quicker. Using fzf changes how you explore and solve problems in the terminal.
- URL: <https://medium.com/@odinumbelino/fzf-the-cli-superpower-youre-probably-not-using-enough-1df7dc76d27a>

### Full Document

![]()

If you're still chaining `grep | awk | less` like a shell caveman, this one's for you.

`fzf` is a general-purpose fuzzy finder that turns your terminal into an interactive search UI. It's fast, keyboard-driven, composable, and brutally effective.

As a DevOps/SRE, you deal with:

- Huge log files
- Endless file trees
- Git branches
- Process lists
- Kubernetes resources
- Shell history

`fzf` makes all of that interactive.

Let's install it, wire it up, and use `/var/log/syslog` to demonstrate real-world workflows.

#### What Is Fzf?

fzf is a fuzzy finder for the command line. It reads input from stdin and gives you an interactive filtering interface.

Instead of:

```
cat /var/log/syslog | grep error
```

You get:

- Live filtering
- Scrollable results
- Preview panes
- Key bindings
- Multi-select

It feels like turning your terminal into a mini TUI app builder.

### Installation

### macOS

If you use Homebrew:

```
brew install fzf
```

Then enable keybindings and completion:

```
$(brew --prefix)/opt/fzf/install
```

### Linux (Debian/Ubuntu)

```
sudo apt update  
sudo apt install fzf
```

Or install the latest version manually:

```
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf  
~/.fzf/install
```

### Windows

Use WSL (recommended) or Git Bash.

In WSL:

```
sudo apt install fzf
```

### First Contact

Run:

```
fzf
```

Now start typing.

It filters interactively.

Press:

- `Enter` → select
- `Ctrl+C` → exit
- `Ctrl+R` → fuzzy search your shell history (after install script)

You're already more powerful than yesterday.

### Classic Use Cases (With Real Log File)

Let's use your _own_ /var/log/syslog to understand how fzf works:

```
cat /var/log/syslog | fzf
```

But we'll go deeper.

### 1️⃣ Search Logs Interactively

Instead of:

```
grep ERROR /var/log/syslog
```

Do this:

```
less /var/log/syslog | fzf
```

Or better:

```
cat /var/log/syslog | fzf
```

Now type:

```
error  
systemd  
ssh  
network
```

You get fuzzy matching instantly.

### 2️⃣ Add Preview Pane (This Is Where It Gets Good)

```
fzf --preview "echo {}"
```

Not impressive.

Let's make it useful:

```
fzf --preview 'echo {} | cut -d" " -f1'
```

Better example with logs:

```
cat /var/log/syslog | fzf --preview 'echo {}'
```

Now each selected line is previewed separately.

### 3️⃣ Highlight Context in Logs

Want context around selected line?

```
cat /var/log/syslog | \  
fzf --preview 'grep -n "{}" /var/log/syslog | cut -d: -f1 | xargs -I{} sed -n "{}-3,{}+3p" /var/log/syslog'
```

Now when you select a log entry, you see 3 lines before and after.

This is production-grade troubleshooting workflow.

### 4️⃣ Combine Ripgrep + Fzf (Power Combo)

If you read my previous article about ripgrep, you know it's stupidly fast.

Now combine them:

```
rg error /var/log/syslog | fzf
```

Or fully interactive:

```
rg --line-number --no-heading '' /var/log/syslog | \  
fzf --delimiter : \  
    --preview 'sed -n {2}p /var/log/syslog'
```

Now you:

- Fuzzy filter
- Keep line numbers
- Preview exact line

Chef's kiss!

### 5️⃣ Search Only Specific Services

Want to isolate ssh?

```
grep ssh /var/log/syslog | fzf
```

Or dynamically:

```
cat /var/log/syslog | fzf --query ssh
```

Starts already filtered.

### 6️⃣ Multi-Select Mode

```
cat /var/log/syslog | fzf -m
```

Select multiple lines with `Tab`.

Press Enter → returns all selected lines.

Perfect for extracting events into another tool.

### 7️⃣ Turn It Into a Log Explorer

Here's a useful alias:

```
alias syslogf='fzf --preview "grep -n {} /var/log/syslog | cut -d: -f1 | xargs -I{} sed -n \"{}-5,{}+5p\" /var/log/syslog" < /var/log/syslog'
```

Now:

```
syslogf
```

You just built a mini log investigation tool.

### 8️⃣ Use It With Processes

Classic SRE move:

```
ps aux | fzf
```

Kill interactively:

```
kill -9 $(ps aux | fzf | awk '{print $2}')
```

Dangerous? Yes.

Efficient? Also yes.

### 9️⃣ Search Files

```
fzf
```

By default, it lists files in the current directory.

You can improve it:

```
export FZF_DEFAULT_COMMAND='find . -type f'
```

Or use it with Git:

```
git branch | fzf
```

### Performance Reality

fzf is:

- Written in Go
- Extremely fast
- Memory efficient
- Stream-based

You can pipe massive logs and it still handles them smoothly.

For SREs handling 500MB logs on a jump host, this matters.

### Workflow Mindset Shift

Instead of:

> _"Let me write the perfect grep command."_

You switch to:

> _"Let me interactively explore the data."_

It changes how you debug.

You iterate faster.

You see patterns quicker.

You stop guessing.

### Pro Setup (Recommended)

Add to `.bashrc` or `.zshrc`:

```
export FZF_DEFAULT_OPTS="--height 40% --layout=reverse --border"
```

Better UX instantly.

### Recap

`fzf` gives you:

- Interactive log search
- File filtering
- Git branch selection
- Process management
- History search
- Multi-select
- Preview panes

And it composes beautifully with:

- grep
- ripgrep
- sed
- awk
- ps
- git
- kubectl

If you're in DevOps/SRE and not using it, you're voluntarily slower.

### Final Thought

Tools like `fzf` don't just make you faster.

They change how you think about problem solving.

And that's the difference between:

- Someone who runs commands
- And someone who controls their terminal

If you found this useful, follow me on LinkedIn—I write practical, no-BS crash courses for DevOps engineers who want real leverage.
