---
aliases: []
confidence: 
created: 2025-02-21T05:20:44Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking]
title: Viewing Port Usage on macOS
type: info
uid: 
updated: 
version: 1
---

Code snippet

## Viewing Port Usage on macOS

Here are several commands you can use to view port usage on your Mac, along with explanations and how to interpret the results:

### 1. `lsof` (List Open Files)

`lsof` is a powerful command that can list all open files, including network sockets. It's the most common and versatile tool for this purpose.

-   List all listening ports:

```bash
lsof -i -P | grep LISTEN
````

`-i` specifies network files, `-P` disables reverse DNS lookups (making output faster), and `grep LISTEN` filters for listening sockets.

- List processes using a specific port:

Bash

```sh
lsof -i :<port_number>
```

Replace `<port_number>` with the actual port number (e.g., `lsof -i :8080`).

- List processes using a specific protocol and port:

Bash

```sh
lsof -i tcp:<port_number>  # For TCP
lsof -i udp:<port_number>  # For UDP
```

- Example Output and Interpretation:

```sh
COMMAND     PID    USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Google      123   user    4u  IPv4   0x1234567890      0t0  TCP localhost:8080 (LISTEN)
```

- `COMMAND`: The name of the process using the port.
- `PID`: The process ID.
- `USER`: The user running the process.
- `FD`: File descriptor.
- `TYPE`: Socket type (IPv4 or IPv6).
- `DEVICE`: Device information.
- `NAME`: The local address and port (e.g., `localhost:8080`). `LISTEN` indicates the port is being listened on.

### 2. `netstat` (Network Statistics)

`netstat` is another common tool, though it's being superseded by `ss` on Linux systems. macOS still includes it.

- List all listening ports (TCP and UDP):

Bash

```sh
netstat -vanp tcp | grep LISTEN  # For TCP
netstat -vanp udp | grep LISTEN  # For UDP
```

`-v` (verbose), `-a` (all), `-n` (numeric addresses), `-p` (show protocol).

- List processes using a specific port:

Bash

```sh
netstat -vanp | grep :<port_number>
```

- Example Output and Interpretation:

```sh
Proto  RecvQ SendQ  Local Address          Foreign Address        (state)     PID/Program name
tcp4       0      0  127.0.0.1.8080         *.*                    LISTEN      123/Google
```

Similar to `lsof`, the output shows the protocol, local and foreign addresses, state (LISTEN), PID, and program name.

### 3. `ss` (Socket Statistics) (May Not Be Available by Default on macOS)

`ss` is a modern replacement for `netstat`, but you may need to install it on macOS using a package manager like Homebrew. If you have it installed, the commands are similar to `netstat` but often more efficient.

- List all listening ports (TCP and UDP):

```sh
ss -tuln | grep LISTEN
```

`-t` (TCP), `-u` (UDP), `-l` (listening), `-n` (numeric).

### 4. Activity Monitor

macOS's built-in Activity Monitor provides a graphical interface to view network activity.1

1. Open Activity Monitor (Applications > Utilities > Activity Monitor).
2. Go to the "Network" tab.
3. You can see processes and their network usage. While it doesn't directly show port numbers, you can often infer which ports are being used based on the connections.

### Choosing the Right Command

- For detailed information about processes and their open ports, `lsof` is generally the most powerful and flexible.
- `netstat` is a simpler alternative if you're already familiar with it.
- `ss` is a modern and efficient option if you have it installed.
- Activity Monitor is useful for a quick overview of network activity but doesn't provide the same level of detail as the command-line tools.

Remember to use `sudo` if you need to see information about processes owned by other users. For example: `sudo lsof -i -P | grep LISTEN`.
