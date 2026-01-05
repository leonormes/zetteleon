---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/8ae0ee7125e7"
author:
  - "[[Gemini]]"
published:
created: 2026-01-05
description: "Created with Gemini"
tags:
  - "input"
---
https://youtu.be/FFgvV0sA3kU?si=Frx9eiDKrVVLPKPA

This video by **VoxelRifts** provides a high-level conceptual framework for treating code as data, structured across four hierarchical levels of abstraction. The core thesis is that while high-level programming paradigms distinguish code from data, computers treat both as binary sequences in memory, enabling powerful automation and performance optimisations.

### 1\. Level 1: String Representation (Generative)

At the most basic level, code is treated as raw text.

- **Mechanism:** Programs output strings that are saved as source files for other compilers \[[01:34](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=94)\].
- **Utility:** Useful for boilerplate automation in languages lacking robust generics or templates (e.g., C).
- **Examples:** Generating specialised data structures (like hash tables) or loading graphics API functions (e.g., **Glad** for OpenGL) \[[02:17](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=137)\], \[[04:19](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=259)\].

### 2\. Level 2: Abstract Syntax Tree (AST) (Introspective)

This level provides semantic context, allowing the meta-program to "understand" the structure of the code rather than just its text.

- **Mechanism:** Accessing the AST during compile-time using libraries like **libclang** or language-native features in Nim or Jai \[[05:11](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=311)\].
- **Utility:** Enables sophisticated checking and transformation.
- **Use Cases:**
	- **Validation:** Enforcing standards (e.g., MISRA) by detecting specific function calls or naming conventions \[[05:33](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=333)\].
	- **Automation:** Generating serialisation/deserialisation logic or transpiling C-like code into GLSL shaders \[[06:07](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=367)\], \[[06:24](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=384)\].

### 3\. Level 3: Assembly (The Middle Ground)

This level is noted as a "weird middle ground" that lacks the semantic density of an AST and the direct executability of machine code, making it less practical for most meta-programming tasks \[[06:47](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=407)\].

### 4\. Level 4: Machine Code (Runtime Execution & JIT)

This is the most direct application of "code as data," where instructions are generated and executed dynamically in RAM.

- **The OS Barrier:** Standard memory allocations (via `malloc`) lack execution permissions for security. One must interface with the OS (using `VirtualAlloc` on Windows or `mmap` on Linux) to allocate pages with **Execute** permissions \[[08:40](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=520)\], \[[09:22](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=562)\].
- **Implementation Logic:**
	- **Instruction Encoding:** Writing specific hex bytes representing ISA-specific instructions (e.g., x86-64) into the allocated buffer \[[09:51](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=591)\].
	- **Calling Convention:** To bridge C code and generated machine code, the generator must respect platform-specific calling conventions (e.g., which registers handle arguments vs. return values) \[[12:49](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=769)\].
- **The JIT (Just-In-Time) Framework:** JIT compilers occupy the space between interpreters and static compilers. They convert code to machine code at runtime to avoid the overhead of a virtual machine \[[14:10](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=850)\].
- **Example:** The **V8 engine** in browsers uses this technique to execute JavaScript at near-native speeds \[[15:03](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=903)\].

**Conclusion:** Treating code as data is a high-leverage architectural pattern, but the video cautions that excessive meta-layers can degrade code readability and maintainability \[[15:20](http://www.youtube.com/watch?v=FFgvV0sA3kU&t=920)\].

**URL:**[https://www.youtube.com/watch?v=FFgvV0sA3kU](https://www.youtube.com/watch?v=FFgvV0sA3kU)

Google Account

Leon Ormes

leonormes@gmail.com