---
aliases: []
confidence: 
created: 2025-10-26T10:23:38Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Marksman LSP Replace Obsidian with Neovim for Note-Taking
type:
uid: 
updated: 
version:
---

**Key Takeaways from "Marksman LSP Replace Obsidian with Neovim for Note-Taking"**

**Marksman LSP Overview**

- Marksman is an *LSP (Language Server Protocol)* tool for Markdown, making Neovim a powerful note-taking platform.
- Used to replace Obsidian in a Neovim workflow for linking notes, heading renames, completions, diagnostics, and more.[^1_1]

**Feature Highlights**

- **Navigation \& Document Symbols:**
  - Jump quickly between Markdown headings via LSP symbols.
  - Keymaps streamline navigation (e.g., `leader + ss` for symbols).[^1_1]
- **Hover Preview:**
  - Preview and navigate notes in popup windows using uppercase `K`—works for links and headings.
- **Completion Integration:**
  - Link notes/headers using completion, integrates with `blink.cmp`.
  - Completion also enables easy linking to headings within notes.[^1_1]
- **Jump List \& File References:**
  - Use `Ctrl+O` to jump back in the Neovim jumplist.
  - `GR` shows files referencing the currently selected heading.
- **Diagnostics:**
  - Quickly see broken links or warnings in project or file level using keymaps like `leader+xx`.
- **Rename Automation:**
  - Renaming headings auto-updates links throughout documents, mimicking Obsidian behavior for atomic note connections.
- **File Moves and Renames:**
  - Supports file moves/renames without breaking links, using H1 as canonical title reference (set via config).

**Snippets, Templates, and Daily Notes**

- Snippet/template management via plugins like `luasnip`; not reliant on Obsidian plugins.
- Daily notes and task management implemented using file explorer and Neovim-native tooling.[^1_1]

**Alternatives and Rationale**

- Explains why `obsidian.nvim` plugin was not used—Marksman proved sufficient for all needs; `obsidian.nvim` is more all-in-one but may suit users needing front matter or Zettelkasten features.
- Other editors supported: VS Code, Emacs, Helix, Zed, etc.

**Image Handling**

- Image preview/pasting is available in Neovim through dedicated plugins and documented workflows.

**Table of Contents \& Code Actions**

- Table of contents generated via code actions or custom keymaps, with Markdown plugins enabling both English and Spanish TOC insertion.

**Configuration and Setup**

- Installation and configuration demoed for Mason package manager and LazyVim distribution.
- Shares dotfiles for direct adoption/config replication.

**Backlinks**

- Marksman does not provide backlink listing; `obsidian.nvim` does, but the author found backlinks unnecessary for their workflow.

**General Workflow Points**

- Neovim can open and manage Obsidian repos directly, with no special plugins required for core Zettelkasten-style navigation.
- Documentation for Marksman could be improved, but all essential guidance is included or linked throughout the video.

**Summary**

- The transition from Obsidian to Neovim for note-taking is smooth with Marksman, covering all essential features for Markdown PKM workflows.
- The author’s full workflow (dotfiles, keymaps, snippets, task management, and daily notes) is shared for viewers to adopt or adapt.[^1_1]

***

**Action Items/References**

- [Marksman GitHub](https://github.com/artempyanykh/marksman)
- [Author’s Dotfiles and Config](https://github.com/linkarzu/dotfiles-latest)
- [Obsidian.nvim Plugin](https://github.com/obsidian-nvim/obsidian.nvim)
- [Related Neovim Markdown Playlist](https://youtube.com/playlist?list=PLZWMav2s1MZQnIfyXOQRaqwp7QAFtDPVk)

See above to dive into the referenced configs or explore more videos by the author for dedicated workflow examples, snippets, image management, and advanced navigation.[^1_1]

<div align="center">⁂</div>

[^1_1]: <https://www.youtube.com/watch?v=SXKsIyYJIrU>\&list=PLZWMav2s1MZQnIfyXOQRaqwp7QAFtDPVk

---

## Give Me a Llm Prompt with Full Context of the Use case for Marksman

**LLM Prompt: Full Context for Marksman LSP Use Case**

***

**Context:**
I'm an advanced Neovim user focused on building a distraction-free, keyboard-driven note-taking and Personal Knowledge Management (PKM) workflow. I want to completely replace Obsidian with Neovim for all tasks related to Markdown note-taking, atomic note linking, heading management, and workspace navigation. My workflow relies heavily on automation, reproducible configs, and fast note discovery, optimized for ADHD productivity.

I need an LLM agent or copilot that understands the technical and productivity requirements for using Marksman LSP with Neovim, including:

- Markdown navigation (jump to headings, search, file explorer)
- Reliable bidirectional linking (update/rename headings and files without breaking links)
- In-note and project-wide diagnostics for broken links
- Fast previewing and completion of note links/headers
- Daily notes, tasks, templates, and snippets support
- Robust note refactor (rename, move files, update links)
- Minimal reliance on external plugins (avoid Obsidian-specific workflows)
- Optional image paste/preview support within Neovim
- Prefer native Neovim features over large plugin suites whenever possible

**Goal:**
Enable advanced LLM-powered assistance for Markdown note-taking, atomic note linking, info retrieval, and workspace refactor directly in Neovim, powered by Marksman LSP. The agent should work with my keymaps, config, and ADHD-friendly workflow—providing clear, immediate feedback, code/action examples, and automation support.

***

**LLM Prompt:**

```sh
You are an LLM productivity copilot for an advanced Neovim setup optimized for ADHD-friendly, automation-driven knowledge management.
My goal is to use Neovim—with Marksman LSP—for everything I used to do in Obsidian, but faster, with more keyboard-driven power, and extensibility.

You should:
- Explain and provide actionable help for Markdown navigation, note linking, heading management, workspace navigation, and refactor operations using Marksman LSP.
- Give concise code/config examples for key workflows, including: jumping to headings, refactoring note titles, updating links, diagnostics for broken links, and completion for note/heading references.
- Prioritize workspace atomicity: renaming a heading updates all references, moving files doesn't break links, etc.
- Support fast preview for links and headings, markdown symbol navigation, and showing references.
- Cover advanced note-taking needs, like daily note creation, template/snippet expansion, and in-note task management.
- Prefer native Neovim features and minimal plugins (use Mason and LazyVim as reference setups).
- Include practical setup tips, dotfile/config links, and ADHD-oriented workflow optimizations.
- Avoid Obsidian-specific features unless strictly necessary; explain alternatives natively supported in Neovim/Marksman.
- Always give clear, immediate feedback, actionable steps, and code or command line examples.

**User Profile:**
DevOps/platform engineer; automates knowledge management; prefers fast keyboard-driven workflows; uses Mason, LazyVim, and linked dotfile configs; needs atomic, distraction-free note-taking.

**Task:**
Help me migrate/build workflows from Obsidian to Neovim using Marksman LSP. For any need I describe, compare "how it was done in Obsidian" vs "how to do it in Neovim/Marksman," with concrete config/code examples and ADHD-friendly automation advice.

Start by listing headline features available via Marksman in Neovim, code actions/keymaps for navigation and linking, and config/automation tips for atomic Markdown note management.
```

***

Use this prompt as a starting point for instructing an LLM agent focused on advanced Neovim+Marksman-based PKM workflows.
