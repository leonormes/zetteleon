---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, Processes]
title: managing and viewing processes on linux
type: documentation
uid: 
updated: 
version: 1
---

In Linux, examining active processes and managing them effectively is essential for system administration, performance monitoring, and process isolation. Below, I’ll explain some tools, the output of `ps aux`, and alternatives for better process visualization.

---

## Tools to Examine and Manage Processes

### 1. `ps aux`

The `ps` command lists information about running processes. The `aux` options:

- `a`: Shows processes for all users.
- `u`: Displays detailed information (user, CPU/memory usage, etc.).
- `x`: Includes processes without a controlling terminal (e.g., daemons).

Reading `ps aux` Output: Here's an example:

```plaintext
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 163520  1056 ?        Ss   Jan19   0:02 /sbin/init
user      1452  1.2  2.5 780320 21508 pts/0    Sl   09:10   1:15 /usr/bin/python3 script.py
```

- `USER`: The owner of the process.
- `PID`: Process ID, used to identify or manage the process.
- `%CPU`: CPU usage percentage.
- `%MEM`: Memory usage percentage.
- `VSZ`: Virtual memory size (in KB).
- `RSS`: Resident Set Size, physical memory used (in KB).
- `TTY`: Terminal associated with the process (`?` for none, like daemons).
- `STAT`: Process state:
    - `S`: Sleeping.
    - `R`: Running.
    - `Z`: Zombie (terminated but not cleaned up).
    - `T`: Stopped.
- `START`: Process start time.
- `TIME`: Total CPU time used.
- `COMMAND`: The command or program name.

---

### 2. `top`

- Interactive, real-time view of processes.
- Displays processes sorted by resource usage by default.
- Example output:

```sh
PID USER   PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
1234 root   20   0  126M   12M   10M S   0.7  0.1   0:00.11 sshd
```

- Press `h` for help, `k` to kill a process, and `q` to quit.

---

### 3. `htop`

- A more user-friendly, colorful, and interactive alternative to `top`.
- Features:
    - Easier navigation with arrow keys.
    - Sort processes by CPU, memory, or time with function keys.
    - Shows hierarchical process trees.
- Run: `htop` (install with `sudo apt install htop` or equivalent).

---

### 4. `pidstat`

- Part of the `sysstat` package, provides CPU, memory, and I/O usage per process.
- Example:

```bash
pidstat -u -p 1234
```

    This shows CPU usage for process ID 1234.

---

### 5. `lsof`

- Lists open files, including network sockets, by processes.
- Example:

```bash
lsof -p 1234
```

    Shows all files opened by process 1234.

---

### 6. `pgrep` And `pkill`

- `pgrep`: Find processes by name or pattern.

```bash
pgrep -l nginx
```

    Lists process IDs for processes with "nginx" in their name.

- `pkill`: Kills processes by name.

```bash
pkill nginx
```

---

### 7. `systemd-cgtop`

- Shows CPU, memory, and I/O usage by systemd cgroups, making it useful for analyzing containerized or isolated processes.
- Run: `systemd-cgtop`.

---

### 8. `nsenter` And `ip netns`

- For namespace-specific process isolation:
    - Use `nsenter` to enter a specific namespace and view processes (`ps` within the namespace).
    - Use `ip netns exec <namespace> ps aux` to list processes inside a network namespace.

---

### Example for Process Isolation

1. Create a namespace:

```bash
unshare --pid --fork --mount-proc bash
```

2. Run `ps aux` inside the namespace to see isolated processes.

---

## Tips for Managing and Reading Processes

1. Filtering Output:

    - Filter `ps aux` by name or user:

```bash
ps aux | grep nginx
ps aux --sort=-%mem
```

- Show processes for a specific user:

```bash
ps -u username
```

2. Killing Processes:

    - Use `kill <PID>` to terminate a process.
    - Send a specific signal:

```bash
kill -9 <PID>  # Force terminate
```

3. Monitoring System Resource Usage:

    - Use `iotop` for disk I/O analysis.
    - Use `free -h` to monitor memory usage.

---

## Summary

- `ps aux`: Provides detailed process information but is static and harder to read for beginners.
- `top` and `htop`: Interactive tools for real-time process monitoring.
- `pgrep`, `pidstat`, and `lsof`: Useful for filtering and inspecting specific processes.
- For namespaces, tools like `nsenter` or `ip netns` provide isolation-aware process management.

Start with `htop` for ease of use and move to specialized tools (`pidstat`, `lsof`, etc.) for in-depth analysis.

Let mehelp you understand Linux process management and visualization in a way that'll make process isolation much clearer to work with.

## Understanding and Visualizing Linux Processes

Let's start with the fundamentals and build up to more advanced process visualization techniques. Think of processes like a family tree - they have parents, children, and relationships that tell us how they're connected and what they're doing.

### Basic Process Viewing

#### Understanding Ps Aux

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

#### Making Ps More Readable

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

### Process Tree Visualization

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

### Real-time Process Monitoring

#### Top - The Traditional Tool

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

#### Htop - The Modern Alternative

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

### Process State Investigation

#### Process Details

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

#### Process Relationships

```bash
# Show parent-child relationships
ps -ef --forest

# Show process ancestors
pstree -s <PID>

# List child processes
ps --ppid <PID>
```

### Process Management Tools

#### Resource Usage Tracking

```bash
# Track process I/O
iotop -p <PID>

# Track process file usage
lsof -p <PID>

# Show process network connections
netstat -p <PID>
```

#### Process Control

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

### Process Isolation Investigation

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

### Common Process States (STAT Column)

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

### Practical Examples

#### Finding Resource-Heavy Processes

```bash
# CPU intensive processes
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head

# Memory intensive processes
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%mem | head

# Most active processes
ps -eo pid,ppid,cmd,stat,etimes --sort=-etimes | head
```

#### Process Troubleshooting

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

### Best Practices for Process Management

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

Let me help you get started with understanding process monitoring in a practical way. Imagine processes like a family tree of running programs. Let's explore this step by step:

First, let's look at a simplified view of your processes:

```bash
# Show your processes in a tree format
ps -u $USER f
```

This command shows only your processes in a tree structure, making it easier to see how processes relate to each other. You'll see parent processes connected to their children with lines, similar to a family tree.

Would you like to try this command and have me explain what you're seeing in the output? We can then dive deeper into specific aspects that interest you, like:

1. Understanding process states
2. Tracking resource usage
3. Viewing process relationships
4. Monitoring in real-time

What aspect would you like to explore first?

Let me break this output down and explain what each part means. Think of this like a snapshot of your running programs, organized in a family tree structure.

First, let's understand the columns:

- PID: Process ID - a unique number identifying each process
- TTY: Terminal associated with the process ("?" means no terminal)
- STAT: Process state (we'll explore these)
- TIME: CPU time used
- COMMAND: The command that started the process

Now, let's analyze the process tree you're seeing. The indentation and lines (\_) show parent-child relationships:

The first branch shows your SSH session:

```sh
1579 ?        S      0:00 sshd: lima@pts/0
   1657 pts/0    Ss     0:00  \_ /bin/bash --login
   2519 pts/0    R+     0:00      \_ ps -u lima f
```

This tells us:

- Process 1579 is your SSH daemon handling your connection
- It spawned process 1657, which is your bash shell
- Process 2519 is the ps command you just ran

The second major branch is your user session:

```sh
816 ?        Ss     0:00 /usr/lib/systemd/systemd --user
```

This is your user's systemd instance, which manages your user-specific services. Its STAT "Ss" means it's a sleeping (S) session leader (s).

Under systemd, you have several containerization-related processes:

```sh
859 ?        Ssl    0:00  \_ rootlesskit
   907 ?        Sl     0:00  |   \_ /proc/self/exe
   936 ?        Sl     0:03  |   |   \_ containerd
   927 ?        S      0:00  |   \_ slirp4netns
```

This shows your container infrastructure:

- rootlesskit: Allows running containers without root privileges
- containerd: The container runtime
- slirp4netns: Handles networking for rootless containers

The last part shows build tools:

```sh
1326 ?        Ssl    0:00  \_ buildkitd
1327 ?        Ssl    0:00  \_ containerd-stargz-grpc
```

These are services for building and managing container images.

The STAT codes tell us more about each process:

- S: Sleeping (waiting for something)
- s: Session leader
- l: Multi-threaded
- +: In the foreground process group
- R: Running (the ps command itself)

This output shows you're running a containerized environment with several supporting services, all managed under your user's systemd instance. The tree structure helps visualize how these processes relate to each other - for example, how your container runtime (containerd) is a child of rootlesskit, which helps it run without root privileges.
