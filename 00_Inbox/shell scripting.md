---
created: 2026-02-11T06:43:46+00:00
modified: 2026-02-11T08:10:02+00:00
title: shell scripting
---

Exactly right. This is a crucial insight that most people miss.

## Both Commands Run Simultaneously

When you write `cmd1 | cmd2`, bash launches both processes at the same time. They run concurrently. `cmd2` doesn't wait for `cmd1` to finish—it starts reading from the pipe immediately, and blocks only when there's nothing to read _yet_.

You can prove this:

```sh
# slow_producer writes one line per second
# Watch the output appear in real-time, not all at once
for i in {1.}; do echo "line $i"; sleep 1; done | while IFS= read -r line; do
    echo "Received: $line at $(date +%T)"
done
```

You'll see each "Received" message appear one second apart. If the pipe waited for the producer to finish, you'd see nothing for 5 seconds and then all five lines at once.

## The Mechanics: It's a Kernel Buffer

The pipe is implemented as a small buffer in the kernel (typically 64KB on Linux). Here's the lifecycle:

1. `cmd1` writes bytes into the buffer
2. `cmd2` reads bytes out of the buffer
3. If the buffer is empty, `cmd2` blocks (sleeps) until more data arrives
4. If the buffer is full, `cmd1` blocks until `cmd2` drains some of it
5. When `cmd1` exits and closes its end, `cmd2` gets an EOF (end of file) signal—that's how it knows the stream is done

That blocking behaviour in points 3 and 4 is called backpressure, and it's what makes the whole thing elegant. A fast producer can't overwhelm a slow consumer, and a fast consumer simply waits for a slow producer. No data is lost.

```sh
# You can see backpressure in action:
# yes produces "y\n" infinitely fast, but head only reads 3 lines then exits
yes | head -3
# y
# y
# y
# (yes gets killed by SIGPIPE when head closes the pipe)
```

That's the other important detail—when `cmd2` _stops reading_ (exits), the kernel sends `SIGPIPE` to `cmd1`, which typically kills it. The consumer can shut down the producer.

## One Nuance: Buffering Can Create an Illusion

Some programmes don't write to `stdout` byte-by-byte. They use an internal buffer (typically 4KB) and only flush it when the buffer is full or the programme exits. This can make it _look_ like the pipe is waiting for completion, but it's actually the producing programme holding onto data.

```sh
# grep buffers its output when writing to a pipe (not to a terminal)
tail -f /var/log/syslog | grep "error"
# Might seem "delayed" — grep is buffering, not the pipe
```

You can force line-by-line flushing in many tools:

```sh
# grep: --line-buffered
tail -f /var/log/syslog | grep --line-buffered "error"

# sed: -u (unbuffered)
tail -f /var/log/syslog | sed -u 's/error/ERROR/'

# python: -u (unbuffered) or PYTHONUNBUFFERED=1
some_command | python -u process.py

# Generic fix: stdbuf (coreutils) forces line-buffering on any command
some_command | stdbuf -oL grep "pattern"
```

This buffering distinction is important for real-time log processing or any long-running pipeline where you need data to flow through promptly.

## So the Full Mental Model

```
cmd1 | cmd2 | cmd3

[cmd1] --writes--> [64KB buffer] --reads--> [cmd2] --writes--> [64KB buffer] --reads--> [cmd3]

         All three processes are alive and running concurrently.
         Each buffer independently manages backpressure.
         Data flows left-to-right as it's produced, not in batch.
```

It's essentially the Unix version of a streaming data pipeline—the same concept behind Kafka or RxJS, just at the OS level, and it's been there since 1973.

This is the right instinct. These mental models are foundational and once they click, everything about shell scripting—pipes, redirection, `/dev/null`, `/proc`, all of it—stops feeling like arcane syntax and starts feeling like a coherent philosophy.

## The OOP Assumptions That Will Mislead You

Let's name them explicitly so you can catch yourself.

### Assumption 1: "A File Is a Thing on Disk"

In OOP, a `File` is a class. It has a path, a size, a modified date. It represents a document sitting on a hard drive.

In Unix, a "file" is anything you can read bytes from or write bytes to. The disk file is just one instance. All of these are "files":

|Thing|How you interact with it|But it's a "file"?|
|---|---|---|
|A document on disk|Read/write bytes|Yes|
|Your keyboard|Read bytes from it|Yes (`/dev/stdin`)|
|Your terminal screen|Write bytes to it|Yes (`/dev/stdout`)|
|A pipe between two commands|Read/write bytes|Yes|
|A network socket|Read/write bytes|Yes|
|A USB device|Read/write bytes|Yes (`/dev/sdb1`)|
|Info about a running process|Read bytes from it|Yes (`/proc/1234/status`)|
|A black hole that discards everything|Write bytes to it|Yes (`/dev/null`)|

The unifying abstraction isn't "thing on disk." It's "numbered channel you can push bytes through." That number is called a file descriptor.

### Assumption 2: "Programs Communicate Through APIs"

In OOP, object A calls a method on object B. There's a defined interface, typed parameters, a return value. The objects need to know about each other.

In Unix, programmes communicate through streams of bytes. They don't need to know each other exist. `grep` has no idea whether its input is coming from a file, a keyboard, a network socket, or the output of another programme. It doesn't care. It reads bytes from file descriptor 0, does its job, and writes bytes to file descriptor 1.

This is the deep reason pipes work. It's not a feature bolted on—it's a consequence of the design. Every programme already reads and writes generic streams, so connecting them is trivial.

### Assumption 3: "Data Has Types and Structure"

In OOP, you pass an `ArrayList<User>` or a `Dict[str, int]`. The structure is enforced by the type system.

In Unix, data between programmes is unstructured bytes. Any "structure" (lines, columns, CSV, JSON) is a social contract between tools, not an enforced schema. When `ls` outputs filenames separated by `\n`, that's a convention. Nothing in the OS enforces it. This is why the delimiter confusion from your earlier question exists—there is no metadata layer.

### Assumption 4: "Programs Are Objects with State and Methods"

In OOP you create an object, call methods on it, it maintains internal state across calls.

In Unix, a programme is a process that runs, transforms a stream, and exits. It's closer to a pure function: bytes in → bytes out → done. The "state" is whatever flows through the pipes, not stored inside the tool. `sort` doesn't "remember" what it sorted. It reads, sorts, writes, exits.

### Assumption 5: "There Are Special I/O Operations"

In OOP you might have `console.log()`, `File.open()`, `socket.send()`—different operations for different destinations.

In Unix, there is fundamentally one operation: read/write bytes to a file descriptor. Printing to screen, writing to disk, and sending data over the network are all the same system call (`write()`), just aimed at different file descriptors.

---

## First Principles: The Actual Model

### Principle 1: Three Streams, Always

Every process is born with three open file descriptors. Always. No exceptions.

```
              ┌─────────────┐
 stdin (0) ──▶│             │──▶ stdout (1)
              │   process   │
              │             │──▶ stderr (2)
              └─────────────┘
```

|FD|Name|Default connection|Purpose|
|---|---|---|---|
|0|`stdin`|Keyboard|Data flowing in|
|1|`stdout`|Terminal|Data flowing out (results)|
|2|`stderr`|Terminal|Diagnostics/errors flowing out|

That's it. A programme doesn't "decide" to accept input or produce output. The three channels are always there. The programme just reads from 0 and writes to 1 and 2. What those channels are _connected to_ is not the programme's concern—the shell decides that.

### Principle 2: Redirection Is Rewiring

When you use `>`, `<`, `|`, `2>&1`, you're not doing anything exotic. You're telling the shell: "before you launch this process, connect its file descriptors to something other than the defaults."

```sh
# Default: stdin=keyboard, stdout=terminal
cat
# Rewire stdin to a file
cat < data.txt          # FD 0 now reads from data.txt, not keyboard
# Rewire stdout to a file
cat data.txt > out.txt  # FD 1 now writes to out.txt, not terminal
# Rewire stderr to a file
cat missing.txt 2> err.log  # FD 2 now writes to err.log
# Rewire stdout of cmd1 into stdin of cmd2
cmd1 | cmd2             # cmd1's FD 1 connects to cmd2's FD 0
```

The programme's code is identical in every case. It calls `read(0)` and `write(1)`. The shell does the plumbing before the programme even starts.

### Principle 3: "Everything Is a File" Really Means "Everything Is a File Descriptor"

The file descriptor is the universal interface. The kernel translates `read(fd)` and `write(fd)` into whatever the actual device needs. This is why you can do things like:

```sh
# Write directly to the terminal device
echo "hello" > /dev/tty
# Read from the random number generator
head -c 16 /dev/urandom | xxd
# Get info about a running process by "reading a file"
cat /proc/self/status
# Discard output by writing to the void
noisy_command > /dev/null 2>&1
```

None of these are special cases. They're all just "open a file descriptor, read or write bytes."

### Principle 4: Composition Over Capability

In OOP, you build a class that does many things: parse, filter, transform, output.

In Unix, you build small tools that each do one thing, then compose them:

```sh
# Five tiny tools, each doing one job, composed into a pipeline
cat access.log | grep "POST" | cut -d' ' -f1 | sort | uniq -c | sort -rn
```

Each tool here is almost trivially simple on its own. The _pipeline_ is where the power emerges. This is the Unix philosophy, and it only works because of Principles 1–3: every tool reads from `stdin` and writes to `stdout`, so they're all naturally composable.

### Principle 5: Text Is the Universal Interface

The reason all these tools compose is that they agree on the lowest common denominator: lines of text. Not objects, not JSON (though `jq` bridges that world), not typed records. Plain text with newline separators.

This is simultaneously Unix's greatest strength (everything works together) and its greatest weakness (no type safety, delimiter confusion, the issues you asked about earlier).

---

## The Rewiring Cheat Sheet

Once you internalise "it's all file descriptors being rewired," every piece of redirection syntax becomes obvious:

```sh
cmd > file          # FD 1 → file (overwrite)
cmd >> file         # FD 1 → file (append)
cmd < file          # FD 0 ← file
cmd 2> file         # FD 2 → file
cmd 2>&1            # FD 2 → wherever FD 1 is currently pointing
cmd &> file         # FD 1 and FD 2 → file (shorthand)
cmd1 | cmd2         # cmd1's FD 1 → kernel buffer → cmd2's FD 0
cmd < /dev/null     # FD 0 ← immediate EOF (no input)
cmd > /dev/null     # FD 1 → discard all output
```

---

## A Practical Exercise to Make This Concrete

Try this in a terminal—it makes the invisible visible:

```sh
# 1. See your own process's file descriptors
ls -la /proc/self/fd
# 2. See what they're connected to during a pipe
echo "hello" | ls -la /proc/self/fd
# 3. See the difference when you redirect
ls -la /proc/self/fd > /tmp/fds.txt
cat /tmp/fds.txt
```

You'll literally see FD 0, 1, and 2 listed as symlinks to their current targets—the terminal, a pipe, or a file. It makes the whole model tangible.

Good catch—`/proc` is a Linux-ism. macOS (BSD under the hood) doesn't expose the virtual filesystem the same way. But we can still make the invisible visible.

## macOS Equivalents

### See File Descriptors with `lsof`

`lsof` (list open files) is the macOS tool for this. The `-p` flag targets a specific process.

```sh
# See the FDs of your current shell
lsof -p $$ | head -20
```

`$$` is the PID of the current shell process. You'll see rows for FD 0, 1, 2 pointing at `/dev/ttys00X` (your terminal device). That's your three streams, wired to the terminal.

### Now Rewire and Observe the Difference

```sh
# Run lsof INSIDE a pipe — its stdin is now a pipe, not the terminal
echo "hello" | lsof -p $$ 2>/dev/null | grep -E "^COMMAND|FD"
```

That won't quite work because `$$` still refers to the parent shell. Here's a cleaner approach:

```sh
# This script shows its own FDs
bash -c 'lsof -p $$ 2>/dev/null'
```

```sh
# Now the same, but with stdin redirected from a file
bash -c 'lsof -p $$ 2>/dev/null' < /etc/hosts
```

Compare the two outputs—you'll see FD 0 change from `/dev/ttys00X` to `/etc/hosts`. Same process, same code, different wiring.

### The Most Revealing Experiment

This one makes streams tangible in real-time:

```sh
# Terminal 1: find your terminal device
tty
# outputs something like: /dev/ttys001

# Terminal 2: write directly to Terminal 1's device "file"
echo "surprise" > /dev/ttys001
```

The text "surprise" appears in Terminal 1. You just proved that a terminal is a file—you opened it by path and wrote bytes to it, exactly as you would with a document on disk. There's no special "send text to another terminal" API. It's just `write bytes → file descriptor`.

### One More: `/dev/null` as a Real "File"

```sh
# /dev/null is a file. You can stat it like any other.
file /dev/null
# /dev/null: character special
ls -la /dev/null
# crw-rw-rw1 root  wheel  3, 2  … /dev/null
```

That `c` at the start means "character device"—a file-like thing that processes data one byte at a time. The kernel handles the `write()` system call by simply discarding the bytes. From your programme's perspective, it's writing to a perfectly normal file descriptor. It has no idea the bytes are going nowhere.

### macOS _Does_ Have Some Virtual Files

macOS isn't as generous as Linux here, but you still have:

```sh
# Device files
ls /dev/stdin /dev/stdout /dev/stderr
# These are real paths that point to your process's FD 0, 1, 2
# Prove it:
echo "hello from stdout" > /dev/stderr
# "hello from stdout" appears on screen via stderr — same terminal,
# but if you'd redirected stderr to a file, it would go there instead
# You can even use them in programmes that expect file paths
grep "root" /dev/stdin <<< "root:x:0:0:root:/root:/bin/bash"
```

That last example is subtle but important. `grep` expects a _filename_ argument. `/dev/stdin` is a valid filename that happens to mean "whatever is connected to FD 0." The everything-is-a-file abstraction lets you bridge tools that expect filenames with tools that produce streams.

---

The experiments to try right now: run `tty` to see your terminal's device path, then write to it from another terminal tab. Once you see text appear on a different screen by writing to a "file," the abstraction stops being theoretical.

Essentially yes—but it's worth being precise about _all_ the ways shell holds and moves data, because there are a few more than just the stream. They're just surprisingly primitive compared to what you're used to.

## The Complete Set of Shell "Data Structures"

### 1. The Byte Stream (Primary)

You already understand this one. It's the main artery. Data flows _between_ processes as untyped bytes via pipes and redirection. No structure, no schema, convention only.

### 2. Strings (The Only Variable Type)

This is the one that trips up programmers the most. Every variable in shell is a string. There are no integers, no booleans, no objects. When you write:

```sh
count=42
```

`count` holds the _string_ `"42"`, not the integer `42`. Arithmetic contexts _reinterpret_ the string as a number temporarily:

```sh
count=42
echo $((count + 8))   # 50 — bash parsed the string "42" into an integer internally
name="hello"
echo $((name + 8))    # 8 — "hello" can't be parsed as a number, so it becomes 0
flag=true
if [ "$flag" = "true" ]; then  # string comparison, not boolean evaluation
    echo "yes"
fi
```

There's no type system enforcing anything. `"true"` isn't a boolean—it's five characters that you've _chosen_ to treat as truthy. Nothing stops you assigning `flag="banana"` and the script won't complain until the logic breaks.

### 3. Exit Codes (The Only "Return Type")

Functions and programmes can't return data. They return a single integer from 0–255. That's it.

```sh
is_even() {
    return $(( $1 % 2 ))  # 0 = true (even), 1 = false (odd)
}
if is_even 4; then
    echo "even"  # this runs — 0 means success/true
fi
```

Notice the inversion from every other language: 0 is truthy, non-zero is falsy. This makes sense when you think of it as "zero problems occurred" rather than as a boolean value. But it will wrong-foot you regularly.

If a function needs to "return" actual data, it has to write to stdout and the caller captures it:

```sh
get_username() {
    echo "leon"     # "returns" by writing to stdout
}
name=$(get_username)  # captures stdout into a variable
echo "$name"          # leon
```

This is why `$()` is everywhere in shell. It's the only mechanism for getting data _out_ of a function. The subshell runs, its stdout is captured as a string, and that string is substituted in place.

### 4. Arrays (Bash-Specific, Limited)

Bash does have arrays, but they're clunky compared to any real language:

```sh
# Indexed array
fruits=("apple" "banana" "cherry")
echo "${fruits[0]}"      # apple
echo "${fruits[@]}"      # all items
echo "${#fruits[@]}"     # 3 (length)

# Append
fruits+=("durian")

# Iterate
for f in "${fruits[@]}"; do
    echo "$f"
done
```

And associative arrays (bash 4+, which macOS ships—check with `bash --version`, though you may want to use the Homebrew version as Apple ships an ancient 3.2):

```sh
declare -A scores
scores[alice]=95
scores[bob]=82
echo "${scores[alice]}"  # 95

# Iterate keys
for name in "${!scores[@]}"; do
    echo "$name: ${scores[$name]}"
done
```

These _exist_ but here's the critical limitation: you can't pass an array through a pipe. The moment data leaves a process, it collapses back to a byte stream. Arrays are process-local only. This is a fundamental boundary.

```sh
# You CANNOT do this
my_array=("one" "two" "three")
echo "${my_array[@]}" | some_command
# some_command receives "one two three" — a flat string, not an array
```

### 5. Environment Variables (Cross-Process Strings)

Exported variables are how a parent process passes configuration to its children. Still just strings, but they cross process boundaries (unlike arrays).

```sh
export DATABASE_URL="postgres://localhost:5432/mydb"

# Any child process can now read DATABASE_URL
psql "$DATABASE_URL"
```

This is the only built-in mechanism for passing _named_ data between processes without using the stream. But it's one-way (parent → child), read-only from the child's perspective, and string-only.

### 6. The Filesystem (Your Actual Data Structure)

This is the insight that completes the picture. When you need something resembling a real data structure in shell—a lookup table, a queue, persistent state—you use the filesystem.

```sh
# A file as a lookup table
cat > users.db << 'EOF'
alice:admin:active
bob:user:inactive
charlie:admin:active
EOF

# "Query" it
grep ":admin:" users.db | cut -d: -f1
# alice
# charlie

# A directory as a key-value store
mkdir -p /tmp/cache
echo "95" > /tmp/cache/alice_score
echo "82" > /tmp/cache/bob_score

# "Look up" a value
cat /tmp/cache/alice_score   # 95

# A file as a queue
echo "job1" >> /tmp/queue.txt
echo "job2" >> /tmp/queue.txt

# "Dequeue" — read and remove first line
head -1 /tmp/queue.txt       # job1
sed -i '' '1d' /tmp/queue.txt  # remove it (macOS sed syntax)
```

This isn't a hack—it's the design philosophy. The filesystem _is_ your database, your message queue, your shared state. Tools like `redis` and `sqlite` exist precisely because this approach doesn't scale, but for shell scripting, it's the intended pattern.

---

## The Complete Picture, Compared

|Concept|OOP Language|Shell|
|---|---|---|
|Variables|Typed (int, string, bool, etc.)|Always strings|
|Return values|Any type|Exit code (0–255) or stdout capture|
|Data between modules|Method calls, typed parameters|Byte stream (pipe) or env vars|
|Collections|Arrays, lists, maps, sets|Arrays (process-local only)|
|Persistent state|Objects in memory, databases|Files on disk|
|Structured data|Classes, interfaces, schemas|Convention (CSV, TSV, colon-delimited)|
|Type safety|Compiler/runtime enforced|Nonexistent—everything is bytes you choose to interpret|

## The Philosophical Shift

In OOP, data has identity and structure. You create a `User` object with fields and methods and it _knows what it is_.

In shell, data has no identity. It's bytes flowing through a system of small programmes that each impose their own transient interpretation. `cut -d: -f1` temporarily interprets the stream as colon-delimited records. Once the bytes leave `cut`, that interpretation is gone. The next tool in the pipe might treat the same bytes as newline-delimited lines, or whitespace-separated words, or raw characters.

The upside: total composability with zero coupling. The downside: nothing stops you from piping garbage into a tool that expects a specific format, and you won't find out until something silently goes wrong.

This is why defensive shell scripting (your error handling note, `set -eEuo pipefail`, validating inputs) matters so much more than in typed languages. The guardrails that a type system gives you for free simply don't exist here.
