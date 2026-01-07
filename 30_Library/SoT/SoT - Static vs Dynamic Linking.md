---
aliases: ["Dynamic Linking", "Shared Libraries", "Static Linking"]
confidence: "5/5"
created: 2025-12-19T00:00:00Z
epistemic: "comparison"
last_reviewed: "2025-12-19"
modified: 2026-01-03T10:18:51+00:00
purpose: "To compare the trade-offs between static and dynamic linking, focusing on binary size, performance, and security."
review_interval: "24 months"
see_also: []
source_of_truth: []
status: "stable"
tags: ["compilers", "devops", "linking", "SoftwareEngineering/Security"]
title: SoT - Static vs Dynamic Linking
type: "SoT"
uid: 
updated: 
---

> **Linking** is the process of collecting and combining various pieces of code and data into a single file that can be loaded into memory and executed. The two primary strategies for this are: ""
> 1. **Static Linking: "** All required library code is copied directly into the final executable file at compile time. The result is a large, self-contained binary."
> 2. **Dynamic Linking: "** The executable contains only references (stubs) to shared libraries. The actual linking to the library code happens at runtime when the application is loaded by the operating system."

## 2. The Core Problem: The Portability vs. Maintenance Trade-off

The choice between static and dynamic linking represents a fundamental trade-off between creating portable, isolated applications versus creating an efficient, secure, and maintainable system.

| Trade-off | Static Linking | Dynamic Linking |
|:--- |:--- |:--- |
| **Deployment** | **Simple & Portable:** The executable is a single file with no external dependencies. It "just works" when copied to a compatible system. | **Complex:** Requires the correct versions of all shared libraries (`.so`, `.dll`, `.dylib`) to be present on the target system. Can lead to "DLL Hell." |
| **Binary Size** | **Large:** Every executable contains a full copy of every library it uses. If 10 programs use the same library, the code is duplicated 10 times on disk. | **Small:** Executables are small, containing only their own code and stubs. The library code exists in one shared place. |
| **Memory Usage** | **High:** If 10 programs are running, the same library code is loaded into RAM 10 times, wasting memory and thrashing the instruction cache. | **Low:** The operating system loads the shared library into RAM once and maps it into the address space of all programs using it. |
| **Performance** | **Faster Startup:** No runtime linking is required. Potentially faster function calls due to compiler optimizations like inlining across library boundaries. | **Slower Startup:** The OS dynamic linker must resolve stubs and load libraries when the program starts. |
| **Security** | **Brittle & Insecure:** If a vulnerability is found in a library, *every single application* that was statically linked against it must be recompiled and redeployed. Old, vulnerable binaries can persist on a system for years. | **Robust & Secure:** If a vulnerability is found in a shared library, updating that single file on the operating system instantly patches *every application* that uses it. |
| **Ecosystem** | Favored by modern, single-binary focused languages like **Go** and **Rust**. | The standard for traditional operating systems (**Linux**, **Windows**, **macOS**) and languages like **C/C++**. |

---

## 3. The Architecture of the Security Risk

The primary modern critique of static linking centers on its profound negative impact on system security and maintainability.

### The "Bundled Dependency" Problem

1. **Compile Time:** A developer builds `MyCoolApp.exe` and statically links `libSSL v1.1`. The code from `libSSL` is copied into the `.exe`.
2. **Deployment:** `MyCoolApp.exe` is deployed to thousands of servers.
3. **Vulnerability Disclosure:** A critical vulnerability (like Heartbleed) is discovered in `libSSL v1.1`.
4. **The Failure:** The system administrator updates the system's shared `libSSL` to the patched `v1.2`. However, `MyCoolApp.exe` **remains vulnerable**. It has its own private, outdated copy of the library bundled inside it.
5. **The Nightmare:** To fix the vulnerability, the owners of *every single application* must now find their source code, recompile against the new library, and redeploy their binary. This is a logistical and security nightmare at scale.

Dynamic linking solves this elegantly. The administrator updates the shared `libSSL.so` file, and the next time `MyCoolApp.exe` starts, the OS automatically links it against the patched version.

---

## 5. Minimum Viable Understanding (MVU)

1. **Static Linking copies all library code into your final `.exe` file.** This makes it big and portable but creates a security nightmare.
2. **Dynamic Linking leaves the library code in a separate `.so` or `.dll` file.** The OS connects your `.exe` to it at runtime. This is efficient but can be fragile.
3. **The key trade-off is Portability vs. Security.** Static linking prioritizes making deployment easy by creating self-contained binaries. Dynamic linking prioritizes making the system efficient and easy to secure by sharing code.
4. **For system security, dynamic linking is overwhelmingly superior.** A single library update patches every application at once.

---

## 6. Open Questions & Tensions

- **Tension:** **The Rise of Containers.** Containerization technologies like Docker challenge the traditional arguments for dynamic linking. By bundling an application with its entire OS user space and dependencies, containers provide portability and isolation, making static linking more viable and attractive again. This is, in effect, system-level static linking.
- **Tension:** **Hermetic Builds.** Build systems like Bazel or Nix aim for perfectly reproducible builds. Static linking is often preferred in this context because it eliminates the variability of the target system's shared library environment. This prioritizes build-time correctness over runtime maintainability.

## 7. Related Components

- [[SoT - Pragmatism vs Rigour in Software]]
