---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/b71df63802e9"
author:
  - "[[Gemini]]"
published:
created: 2025-12-14
description: "Created with Gemini"
tags:
  - "clippings"
---
Https://youtube.com/watch?v=7sbYMXKc0Jk&si=Qfd6hPcoZe4z4TY-

What are the conclusions from this video and how is the author setting up his computer to use these Windows managers?

This analysis outlines the core conclusions and the setup methodology for using the Aerospace tiling window manager, structured for an Abstract-Conceptual and Top-Down cognitive style.

The video focuses on establishing a functional mental model for tiling window managers on macOS, contrasting the system integration approaches of Yabai and Aerospace.

---

## System Conclusions: Yabai vs Aerospace

The primary distinction between the two managers lies in their **level of integration** with the macOS system and the resulting **security trade-off**.

| System Feature | Yabai (Deep Integration) | Aerospace (Virtualised Environment) |
| --- | --- | --- |
| **SIP Requirement** | Requires disabling System Integrity Protection (SIP) to fully remove animations and gain advanced control \[[36:29](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2189)\]. | Does **not** require disabling SIP \[[38:08](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2288)\]. |
| **Control Model** | Extends and hooks into the native macOS desktop/spaces model \[[36:19](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2179)\], offering granular control over OS elements like window shadows and application transparency \[[36:51](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2211)\]. | Operates as a self-contained, virtualised environment \[[37:47](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2267)\]. All management is self-contained and external to the native macOS desktop model. |
| **Suitability** | Ideal for personal machines where SIP disablement is an acceptable security compromise for advanced customisation \[[37:17](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2237)\]. | Recommended for work computers or environments where SIP must remain enabled \[[39:04](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2344)\]. |
| **Performance** | Works well, though requires deep system modification to eliminate all native animations \[[38:33](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2313)\]. | Modern versions are multi-threaded to prevent performance freezes previously associated with single-process design \[[33:06](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=1986)\]. |

**Conceptual Summary:** Aerospace is viewed as the superior model for security and compatibility, as it avoids the need for deep operating system modification (SIP disablement) while still providing a robust virtual workspace environment \[[39:04](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=2344)\].

---

## Author's Setup Methodology (Aerospace)

The author's setup logic is based on creating and enforcing a declarative set of rules within the configuration file (`aerospace.toml`), specifically addressing how applications are handled within the virtualised workspace environment.

### 1\. The Core Lifecycle (Efficiency)

- **Initialisation:** The setup requires explicitly disabling any competing window manager (e.g., Yabai) before launching Aerospace \[[03:08](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=188)\].
- **Rule Enforcement:** A key principle is that application rules are **not** retroactive. Any configuration change (e.g., assigning a browser to a new workspace) requires the target application to be **closed and reopened** for the rule to take effect \[[19:12](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=1152)\], \[[26:26](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=1586)\].
- **Configuration Reload:** Changes to the configuration file are applied by running a dedicated key map command (`alt shift semicolon` then `escape`) \[[06:49](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=409)\].

### 2\. Workspace and Application Assignment

- **Workspaces:** Desktops are defined in the configuration (e.g., `1, 2, 3, 4`) \[[02:45](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=165)\].
- **Assignment Rules:** Rules are set to map an application's unique identifier (`app ID` or `app name regex string`) to a specific workspace number \[[25:39](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=1539)\], ensuring applications open where they are expected (e.g., Vivaldi to Workspace 1) \[[26:17](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=1577)\].

### 3\. Handling Exceptions (Floating Windows)

For applications that should **not** be managed by the tiling system (e.g., utility windows like Skitty Notes), a rule is defined to exempt them:

- The application's ID is targeted.
- The `run` command is set to `layout floating` \[[21:20](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=1280)\].
- This removes the window from tiling management, allowing the user to manually set its size and position \[[23:50](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=1430)\].

### 4\. Implementing "Sticky" Windows (Workaround)

Since Aerospace lacks a native "sticky window" feature (where a window follows the user across workspaces), the author implements a workaround by scripting:

- A script is executed on an event that triggers every time the workspace is changed (`exit on workspace change`) \[[08:50](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=530)\], \[[13:33](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=813)\].
- The script uses a command to identify the target application (e.g., `kitty`) and **moves it to the newly focused workspace**, creating the effect of the window "travelling" with the user \[[13:59](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=839)\], \[[31:41](http://www.youtube.com/watch?v=7sbYMXKc0Jk&t=1901)\].

The video is available here: [(Part 2) Yabai vs Aerospace: Ultimate macOS Tiling WM Setup Guide](http://www.youtube.com/watch?v=7sbYMXKc0Jk).

Google Account

Leon Ormes

leonormes@gmail.com