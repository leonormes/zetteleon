---
aliases: []
confidence: 
created: 2025-02-26T22:01:15Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:40Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [linux]
title: file discriptors
type: documentation
uid: 
updated: 
version: 1
---

In Linux, file descriptors are non-negative integers that serve as an abstraction to access input/output resources. These resources can be files, network connections, pipes, or devices. Think of a file descriptor as a handle or a pointer that a process uses to interact with these resources.

How File Descriptors Work:

 - Opening a File: When a process wants to access a file or resource, it makes a system call, such as open(). The kernel then checks permissions and creates an entry representing the opened file.
 - File Descriptor Allocation: The kernel maintains a file descriptor table for each process. This table is an array where each entry contains a pointer to an open file description. Upon successfully opening a file, the kernel finds the lowest available number in the process's file descriptor table and assigns it as the file descriptor for this opened file. This file descriptor is then returned to the process.
 - Using File Descriptors for I/O: The process then uses this file descriptor in subsequent system calls like read() and write() to perform operations on the file. Instead of using the file's name, the process simply refers to it by its file descriptor number.
 - Standard File Descriptors: Every Linux process, by default, has three standard file descriptors already opened:
   - 0: Standard Input (stdin): Usually connected to the keyboard, used for reading input.
   - 1: Standard Output (stdout): Usually connected to the terminal, used for normal output.
   - 2: Standard Error (stderr): Usually connected to the terminal, used for error messages.
5.  Redirection: File descriptors enable powerful I/O redirection in Linux. For example, using shell commands like command > file redirects the standard output (file descriptor 1) of command to file. Similarly, command 2> error_file redirects standard error (file descriptor 2) to error_file. command > file 2>&1 redirects both standard output and standard error to file.
 - Closing File Descriptors: When a process finishes using a file or resource, it should close the file descriptor using the close() system call. This releases the file descriptor and associated kernel resources.
Data Structures Involved:
The Linux kernel uses several data structures to manage file descriptors:
 - Per-Process File Descriptor Table:
   - Each process has its own file descriptor table.
   - It's essentially an array of pointers. The index of the array is the file descriptor number.
   - Each entry points to an entry in the system-wide open file table.
   - This table is located in the u_block area, a memory region maintained by the kernel for each process.
   - Each entry in the file descriptor table contains:
     - A pointer (*fp) to an entry in the system open file table.
     - File descriptor flags (e.g., close-on-exec).
 - System Open File Table:
   - This is a system-wide table that is shared by all processes.
   - Each entry in this table corresponds to an opened file or resource.
   - Multiple file descriptors from the same or different processes can point to the same entry in this table, especially after operations like fork() or dup().
   - Each entry in the open file table contains:
     - File offset: Keeps track of the current position for read/write operations. Shared by all file descriptors pointing to this entry.
     - File status flags: Describes how the file was opened (e.g., read-only, write-only, append).
     - File access mode: Mode specified during the open() system call.
     - Inode pointer: A pointer to the system-wide inode table.
 - Inode Table:
   - This is another system-wide table that contains information about each file in the file system.
   - An inode (index node) stores metadata about a file, such as:
     - File type (regular file, directory, device, etc.).
     - Permissions.
     - Timestamps (modification, access).
     - File size.
     - Pointers to the data blocks on disk where the file's content is stored.
     - File locks.
In summary: When a process opens a file, a file descriptor is created and associated with an entry in the per-process file descriptor table, which in turn points to an entry in the system open file table. The open file table entry then points to the inode table, which holds the file's metadata and location of data blocks. This multi-layered structure allows the kernel to efficiently manage file access, sharing, and permissions across different processes.

You're right to question the "everything is a file" statement in Linux and to think about what a "file" truly means in this context, especially when we're used to the desktop icon metaphor. It's definitely an abstraction, and it's not always intuitive if you're thinking solely in terms of GUI icons.

Let's break down what "file" means in Linux and why they say "everything is a file":

In Linux, a "file" is best understood as an abstraction for a stream of bytes.

Think of it less like a paper pad icon on your desktop and more like a generic endpoint for data. The key idea is that Linux treats many different kinds of resources as if they were ordered sequences of bytes, and it provides a unified way to interact with them using the same set of system calls (like read, write, open, close).

Here's a breakdown of what this means:

 - Not Just Disk Files: When Linux says "everything is a file," it doesn't just mean the documents, images, and programs stored on your hard drive. Those are files, of course, but the concept goes much wider.
 - Streams of Bytes: At the most fundamental level, a Linux "file" is simply a sequence of bytes. It doesn't inherently have to be stored on a disk. It's just a way to organize and access data.
 - Unified Interface: The power of "everything is a file" comes from the fact that you can use the same system calls and tools to interact with vastly different things because they are all presented as "files." This simplifies programming and system administration.
Examples of "Files" in Linux (Beyond Regular Disk Files):
To make this more concrete, let's look at examples of what Linux treats as files:
 - Regular Files: These are what you traditionally think of as files: documents, programs, images, etc., stored on your hard drive or other storage devices. They are persistent streams of bytes stored in a file system.
 - Directories: In Linux, directories are also files. They are special files that contain a list of other files and directories. When you "read" a directory file, you get back a list of its contents.
 - Devices: Hardware devices are represented as files in the /dev directory.
   - /dev/sda1: A partition on a hard drive.
   - /dev/input/mouse0: Your mouse.
   - /dev/tty: Your current terminal.
   - /dev/null: A special "null device" that discards any data written to it and provides no data when read from.
   - /dev/random and /dev/urandom: Sources of random numbers.
   When you interact with these device files, you are directly interacting with the hardware (or the kernel's representation of it). For example, you can "read" from your mouse file to get mouse input data, or "write" to a serial port device file to send data over a serial connection.
 - Pipes (Named and Anonymous): Pipes are mechanisms for inter-process communication (IPC). They allow one process to send data to another. In Linux, pipes are also treated as files. You can write data to one end of a pipe (as if writing to a file) and another process can read that data from the other end (as if reading from a file).
 - Sockets: Network sockets, used for network communication, are also represented as file descriptors. You can read and write to sockets to send and receive data over a network connection.
 - Process Information (Procfs - /proc file system): The /proc directory is a virtual file system that provides information about running processes and the kernel itself. Files within /proc (like /proc/cpuinfo, /proc/[pid]/mem, /proc/[pid]/status) are dynamically generated "files" that expose kernel data and process information. Reading these files gives you real-time system information.
Why "Everything is a File" is Powerful:
 - Simplicity and Uniformity: It provides a consistent and simple way to interact with diverse system resources. You don't need to learn different sets of commands or APIs for files, devices, and network connections. The basic file operations (open, read, write, close) work across all of them.
 - Flexibility and Redirection: This unified approach enables powerful features like I/O redirection. Because standard input, standard output, and standard error are file descriptors, you can easily redirect them to regular files, pipes, or sockets. This is fundamental to shell scripting and command-line workflows.
 - Abstraction and Modularity: It abstracts away the underlying hardware and implementation details. Programs don't need to know if they are reading from a disk file, a network socket, or a keyboard – they just read from a file descriptor. This makes programs more portable and modular.
Contrast with GUI Desktop Icons:
Your analogy to desktop icons is helpful for visualizing regular files in a GUI environment. Icons are visual representations to help users interact with files in a user-friendly way. However, the "everything is a file" concept in Linux is a more fundamental, system-level abstraction.
 - GUI Icons are a representation for users. They are designed for visual interaction and ease of use.
 - Linux "files" are a system-level abstraction for the kernel and programs. They are designed for a consistent and unified way for software to interact with resources.
The GUI desktop metaphor is built on top of the "everything is a file" foundation of Linux. The icons you see represent files (mostly regular files and directories), but the underlying system treats many more things as files behind the scenes.
In essence, when you hear "everything is a file" in Linux, think: "Everything that can be treated as a stream of bytes, and that the system needs to manage and provide access to, is represented as a file and accessed through file descriptors." It's a powerful and elegant design principle that underpins much of Linux's functionality and flexibility.

The word "file" has a fascinating history that stretches back centuries, long before computers existed. It's a great example of how language evolves and adapts to new technologies.

Here's a breakdown of its history and meaning:

Origin and Early Meanings:

 - Latin Roots: The word "file" ultimately comes from the Latin word "filum," which meant "thread" or "string." Think of a literal thread, like yarn or string.
 - Old French: "Filum" evolved into the Old French word "file." In Old French, "file" took on a few related meanings:
   - Still retained the sense of "thread" or "string."
   - Also started to mean a "row" or "line" of people or things, like soldiers marching in file. Imagine people lined up like beads on a string.
 - Middle English: The word "file" was adopted into Middle English (around the 14th century) from Old French. It carried over these core meanings:
   - Thread/String: This sense persisted, although it became less common over time.
   - Row/Line: Meaning a linear arrangement of people or things.
Evolution of Meaning - From Physical Objects to Abstractions:
Over time, the meaning of "file" broadened and became more abstract. Here's how it moved towards the modern meanings we understand:
 - "String" of Papers: Imagine keeping important papers together by threading them onto a string or piece of wire. This practice likely led to "file" being used to describe a collection of papers arranged in order, like items on a thread.
 - Organized Collection: From the idea of a "string of papers," "file" began to signify any organized collection of papers, documents, or records kept together for easy access. This is the sense of a "file of documents" in an office filing cabinet. The organization and orderliness were key, echoing the linear arrangement of items on a "string" or in a "row."
 - Tool for Smoothing: Separately, but related in sound and possibly influencing the meaning, there's another "file" that refers to a metal tool used for smoothing or shaping materials. This "file" also comes from Latin, likely from "filum" again, perhaps suggesting the action of shaving off thin "threads" of material. While this meaning is distinct, the idea of orderliness and precision might have subtly reinforced the concept of a "file" as something organized and structured.
"File" in the Computer Age:
When computers were developed, the term "file" was a natural fit for describing organized collections of digital data. The concept of a structured, ordered collection of information, like papers in a physical file, translated well to digital files.
 - Digital Files as Organized Data: Computer files became the digital equivalent of paper files – containers for organized data, whether it be text, images, programs, or anything else. The "stream of bytes" concept we discussed earlier in the Linux context is a modern technical interpretation of this ordered collection.
In Summary:
The word "file" journey is a progression from a literal "thread" to a more abstract concept of an ordered collection. It started with physical objects and evolved to describe both physical and digital collections of information. The core idea of order, arrangement in a line or sequence, and organized collection has been central to the meaning of "file" throughout its history. So, while a desktop icon might be a visual representation, the essence of a "file" is about structured, accessible information, whether on paper or in a computer.
