---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [cli, containers, linux, processes, Processes]
title: Understanding and Visualizing Linux Processes
type:
uid: 
updated: 
version:
---

Let's start with the fundamentals and build up to more advanced process visualization techniques. Think of processes like a family tree - they have parents, children, and relationships that tell us how they're connected and what they're doing.

## Basic Process Viewing

### Understanding Ps Aux

The `ps aux` command is powerful but can be overwhelming. Let's break down what each column means:

```bash
ps aux
```

The output columns represent:

- USER: Who owns the process
- PID: Process ID (unique identifier)
- %CPU: CPU usage
- %MEM: Memory usage
- VSZ: Virtual memory size
- RSS: Real memory (RAM) usage
- TTY: Terminal associated with process
- STAT: Process state (R=running, S=sleeping, etc.)
- START: When the process started
- TIME: CPU time used
- COMMAND: The command that started the process

### Making PS More Readable

Try these variations for clearer output:

```bash
# Show process hierarchy
ps axjf

# Show only your processes
ps -u $USER

# Show process tree for specific user
ps -u $USER f

# Show only important columns
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu
```

## Process Tree Visualization

The `pstree` command gives you a visual tree of processes:

```bash
# Basic process tree
pstree

# Show PIDs
pstree -p

# Show specific process tree
pstree -p <PID>
```

Example output:

```sh
systemd─┬─systemd-journal
        ├─systemd-udevd
        ├─sshd─┬─sshd───bash───pstree
        │      └─sshd───bash
        └─nginx─┬─nginx
                └─nginx
```

## Real-time Process Monitoring

### Top - The Traditional Tool

```bash
top
```

Key features in top:

- Press 'h' for help
- Press 'k' to kill a process
- Press 'r' to renice (change priority)
- Press 'c' to see full command paths
- Press 'M' to sort by memory usage
- Press 'P' to sort by CPU usage

### Htop - The Modern Alternative

```bash
# Install htop if not present
sudo apt-get install htop

# Run htop
htop
```

htop advantages:

- Mouse support
- Visual CPU/Memory bars
- Better color coding
- Easier to read tree view
- Built-in process searching

Useful htop shortcuts:

- F5: Tree view
- F6: Sort by any column
- F9: Kill process
- F10: Quit
- /: Search

## Process State Investigation

### Process Details

```bash
# Examine process status
cat /proc/<PID>/status

# View process limits
cat /proc/<PID>/limits

# Check process environment
cat /proc/<PID>/environ | tr '\0' '\n'

# View process memory maps
cat /proc/<PID>/maps
```

### Process Relationships

```bash
# Show parent-child relationships
ps -ef --forest

# Show process ancestors
pstree -s <PID>

# List child processes
ps --ppid <PID>
```

## Process Management Tools

### Resource Usage Tracking

```bash
# Track process I/O
iotop -p <PID>

# Track process file usage
lsof -p <PID>

# Show process network connections
netstat -p <PID>
```

### Process Control

```bash
# Change process priority
renice -n 10 -p <PID>

# Send signals to process
kill -l                   # List available signals
kill -SIGTERM <PID>      # Graceful termination
kill -SIGKILL <PID>      # Force termination

# Suspend/Resume processes
kill -STOP <PID>         # Suspend
kill -CONT <PID>         # Resume
```

## Process Isolation Investigation

When working with isolated processes, use these commands to understand the isolation:

```bash
# Show namespace information
ls -l /proc/<PID>/ns/

# Check cgroup membership
cat /proc/<PID>/cgroup

# View capability set
getpcaps <PID>

# Check process limits
prlimit --pid <PID>
```

## Common Process States (STAT Column)

Understanding the STAT column in ps:

- R: Running
- S: Sleeping (interruptible)
- D: Uninterruptible sleep
- Z: Zombie
- T: Stopped
- t: Tracing stop
- X: Dead
- +: Foreground process
- l: Multi-threaded
- N: Low priority
- < : High priority
- s: Session leader

## Practical Examples

### Finding Resource-Heavy Processes

```bash
# CPU intensive processes
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head

# Memory intensive processes
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%mem | head

# Most active processes
ps -eo pid,ppid,cmd,stat,etimes --sort=-etimes | head
```

### Process Troubleshooting

```bash
# Find zombie processes
ps aux | grep 'Z'

# Check process stack trace
cat /proc/<PID>/stack

# Monitor process system calls
strace -p <PID>

# Watch process file activity
strace -e trace=file -p <PID>
```

## Best Practices for Process Management

1. Regular Monitoring:
   - Check system load regularly
   - Monitor critical service processes
   - Watch for zombie processes
   - Track resource usage trends

2. Process Organization:
   - Use meaningful process names
   - Maintain proper process hierarchies
   - Set appropriate process priorities
   - Implement proper service management

3. Troubleshooting Steps:
   - Check process state
   - Examine resource usage
   - Look at open files and connections
   - Review process logs
   - Check for stuck processes
