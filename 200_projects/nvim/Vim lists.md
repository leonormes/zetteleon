---
aliases: []
confidence: 
created: 2025-07-08T12:13:03Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Vim lists
type:
uid: 
updated: 
version:
---

As your thought partner in navigating complex information, I can help you quickly analyze and understand the technical details within the provided Vim and Neovim documentation to support your strategic recommendations. My knowledge base for this conversation includes excerpts from 18 YouTube video transcripts covering various Vim commands, concepts like modal editing, registers, macros, quickfix lists, text objects, search and replace, and file management [1-156], as well as excerpts from 6 Reddit threads and a PDF guide on LazyVim and Practical Vim, offering insights into advanced features, plugin configurations, and efficient workflows [157-437].

---

To search your whole project for a keyword and save the results to a list so you can work on each result one at a time in Vim, you will primarily use a "Quickfix List" [10, 31, 68, 81, 87, 224, 362, 363, 403, 407]. This feature efficiently compiles locations (file name, row number, column number, and text) from searches, compilation errors, or test failures, allowing you to jump between them [10, 403].

Here are the primary methods to achieve this:

## 1. Using Vim's Built-in `vimgrep` Command

The `vimgrep` command allows you to search across multiple files using Vim's native regular expression engine and automatically populates the Quickfix list with the results [87, 129, 225, 381, 418].

- **Syntax**: `:vimgrep /pattern/ [flags] {file_pattern}` [129, 421].
  - `/pattern/`: The keyword or regular expression you want to search for [129, 419, 421, 423]. Vim's regex syntax can be used here [423].
  - `[flags]`:
    - `g`: Matches all occurrences of the pattern on each line, not just the first [130, 420, 424]. This is almost always desired for comprehensive search [420].
    - `j`: If supplied, Vim will not jump to the first match immediately [147].
  - `{file_pattern}`: Specifies which files to search.
    - `**/*`: Searches all files recursively in the current directory and its subdirectories [88, 131].
    - `**/*.txt`: Searches all files with a `.txt` extension recursively [381, 421]. You can replace `.txt` with any extension like `.py`, `.c`, `.java`, etc. [76].
    - `%`: Searches only in the current active buffer/file [130, 362, 421].
    - `##`: Searches all files currently in the argument list [424, 438].
- **Example**: To search for the word "function" across all `.js` files in your project recursively:

```vim
:vimgrep /function/g **/*.js
```

This command will run the search and populate the Quickfix list. If successful, you'll see a message like "(1 of X)" indicating the first match and total results [130, 362, 419].

## 2. Using Vim's External `grep` Command

Vim provides a wrapper command `:grep` to call an external `grep` (or `grep`-like) program on your system. This also populates the Quickfix list [225, 413, 439]. External `grep` tools can be faster for large projects [439].

- **Syntax**: `:grep [flags] {pattern} {file_pattern}` [416].
  - Vim automatically adds the `-n` flag to include line numbers in the output, which allows direct jumping to the match [417].
  - You can pass other flags (e.g., `-i` for case-insensitive search, `--nogroup` for `ack`) directly to the external `grep` program [417, 440].
  - By default, Vim's `:grep` might use `grep` or `ack`. You can customize the external program using `:set grepprg=` [40, 47, 225, 440]. For example, to use `ripgrep` (often aliased as `rg`), you might set `grepprg` to `rg --vimgrep` [40].
- **Example**: To search for "Waldo" (case-insensitive) in all files in the current directory using `grep`:

```vim
:grep -i Waldo *
```

This executes `grep -n -i Waldo *` behind the scenes and loads the results into Quickfix [417].

## 3. Using Fuzzy Finders (e.g., Telescope Plugin)

For Neovim users, plugins like Telescope offer a more interactive and visually appealing way to perform project-wide searches and manage results. Telescope is a fuzzy finder that can integrate with `vimgrep` or `grep` tools [58, 68, 71].

- **Workflow**:
  1. Open Telescope's grep search (often mapped to `<Space>/` or similar) [72, 203].
  2. Type your search query. Telescope provides live previews [72, 172, 210].
  3. Once satisfied with the results, send them to the Quickfix list. This is often done with `<C-q>` (Control-Q) within the Telescope picker [58, 69, 81, 84].

- **Example**:
  1. Press `<Space>/` (or your configured keybinding) to open Telescope's live grep [203].
  2. Type `food` and observe the matches.
  3. Press `<C-q>` to send these results to the Quickfix list [58].

## Working with the Quickfix List

Once the Quickfix list is populated by any of the above methods, you can interact with it using various commands:

- **Open the Quickfix Window**:
  - `:copen` (or `:cope`) [10, 40, 69, 81, 88, 130, 410]: Opens a dedicated window at the bottom of your screen displaying all search results [10, 81, 88, 410]. Each line in this window shows the file name, row number, column number, and the matching text [10, 88].
  - This window behaves like a regular Vim buffer, allowing you to scroll (`j`, `k`) and search within it [410].
- **Navigate the Quickfix List**:
  - `:cnext` (or `:cn`) [10, 40, 76, 81, 84, 88, 130, 362, 441]: Jumps to the next match in the list [10, 76, 363].
  - `:cprev` (or `:cp`) [10, 40, 76, 81, 84, 88, 130, 362, 441]: Jumps to the previous match [10, 76, 363].
  - `:cfirst` [69, 76, 88, 441]: Jumps to the very first match.
  - `:clast` [69, 76, 88, 441]: Jumps to the very last match.
  - `:c{number}`: Jumps to a specific entry by its number (e.g., `:c3` to jump to the third match) [88].
  - **Keyboard Shortcuts**: Many users map these commands for efficiency. Common mappings (often provided by plugins like `vim-unimpaired`) include `]q` for next and `[q` for previous [10, 89, 270].
  - Pressing `Enter` on an entry in the Quickfix window will jump your main editor window to that specific location [40, 81, 88, 131, 410].
- **Close the Quickfix Window**:
  - `:cclose` (or `:ccl`) [88, 411]: Closes the Quickfix window [411]. You can also quit the Quickfix window using `:q` when it is the active window [131, 411].
- **Manage Multiple Quickfix Lists**:
  - `:colder` [89, 148, 219, 411]: Recalls an older version of the Quickfix list (Vim stores up to 10 previous lists) [89, 219, 411].
  - `:cnewer` [89, 148]: Jumps to a newer Quickfix list.
- **Perform Operations on Quickfix Results**:
  - `:cdo {command}` [22, 40, 58, 81, 84, 90, 143]: This is a powerful command that runs a specified Ex command for *each entry* in the current Quickfix list [40, 58, 81, 90].
    - **Example: Search and Replace Across Multiple Files**:

            ```vim
            :cdo %s/old_text/new_text/g | update
            ```

            This command will iterate through each entry in the Quickfix list. For each entry, it will:
            1. Switch to the file of that entry.
            2. Perform a global substitution (`%s/old_text/new_text/g`) of `old_text` with `new_text` within that file [58, 90, 143].
            3. `| update`: The `|` allows chaining commands. `update` saves the file only if changes were made [90, 383]. This is crucial for saving changes made by `cdo` [90, 143].

      - You can add `c` flag to the substitute command for confirmation on each replacement (`%s/old_text/new_text/gc`) [81, 84, 90, 372].
  - `:cfdo {command}` [90, 145, 382]: Similar to `:cdo`, but runs the command for *each file* that appears in the Quickfix list, rather than each individual match. This is useful if a file has multiple matches but you only want to perform one command per file.
    - **Example**: If you want to close all files listed in the Quickfix list:

            ```vim
            :cfdo bd
            ```

            This will execute the `bd` (buffer delete) command for each file in the Quickfix list, closing them [90].

  - **Requirement for `:cdo`/`:cfdo`**: Ensure `hidden` setting is enabled (`:set hidden`) to allow navigating away from modified files without saving them first [383].
- **Saving/Loading Quickfix List**:
  - `:w {filename.txt}`: You can save the contents of the Quickfix list window to a text file for later review or processing [90].
  - You can also write custom functions to populate the Quickfix list based on your own criteria [81].

By mastering these commands, you can significantly streamline your project-wide search and editing workflows in Vim.

**Next Step**: To deepen your understanding, try performing a `vimgrep` search for a common keyword (e.g., "import" or "class") across a medium-sized project of yours. Then, open the Quickfix list (`:copen`) and practice navigating through the results using the various `cnext`, `cprev`, `cfirst`, and `clast` commands. Observe how Vim jumps between files and lines.
