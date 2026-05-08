---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:45+00:00
title: Unix Timesharing System (uts namespace)
---

## Unix Timesharing System (uts namespace)

This namespace is unfortunately named by today's standards. It dates back to the early days of Unix and has to do with how information was stored for a specific system call. Today, this detail is largely lost to history and what you really need to know is that the UTS namespace allows for the segregation of hostnames. Often hostnames are simply a convenience. As mentioned earlier, with some exceptions, most communication to and from a host is done via the IP address and port number. However, it makes life a lot easier for us humans when we have some sort of name attached to a process. Searching through log files, for instance, is much easier when identifying a hostname. Not the least of which because, in a dynamic environment, IPs can change.

In our building analogy, the hostname is similar to the name of the apartment building. Telling the taxi driver I live in City Place apartments is usually more effective than providing the actual address. Having multiple hostnames on a single physical host is a great help in large containerized environments.
