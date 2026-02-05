---
aliases: []
created: 2026-01-08T14:56:48+00:00
last_reviewed: ""
modified: 2026-02-01T15:08:03+00:00
status: ""
tags: []
title: Data_Flow_Plan
type: ""
---

## Data Flow Plan: Ekphos

Mapping the "Hot Path" of data through the system based on type definitions and ownership.

### 1. Input: Capturing the External World

The system accepts input from three primary sources, converted immediately into internal types:

- User Interaction (Keyboard/Mouse):
    - Source: `crossterm::event::Event`.
    - Capturing Type: `crossterm::event::KeyEvent` and `MouseEvent`.
    - Entry Point: `event::run_app` loop in `src/event/handler.rs`.
- File System (Notes & Config):
    - Source: `std::fs` and `std::env::args`.
    - Capturing Types:
        - `PathBuf` (File paths).
        - `String` (Raw markdown content).
        - `Config` (Deserialized TOML).
    - Entry Point: `App::new` and `App::load_notes_from_dir`.
- Clipboard:
    - Source: System Clipboard (via `arboard`/`clipboard-rs`).
    - Capturing Type: `String` (Text/Markdown).

### 2. Transformation: Data Shape Changes

The core logic transforms raw inputs into structured application state.

#### The Editing Loop (Hot Path)

1. Raw Input: `KeyEvent` (e.g., Char('a'), Backspace).
2. Intent Parsing:
    - Direct: `editor::input::process_key` -> `InputAction` enum (`InsertChar`, `Delete`, `Move`).
    - Vim Emulation: `VimState` accumulates keys -> `RecordedCommand` struct -> `Operator` + `Motion` enums.
3. Buffer Manipulation:
    - Target: `TextBuffer` struct.
    - Operation: `InputAction` / `EditOperation` applied to `Vec<String>` (Lines).
    - Mechanism: Gap Buffer logic (`before` / `after` vectors) shifts to cursor position.
4. History Tracking:
    - `EditOperation` (Inverse of action) -> pushed to `History` (`VecDeque<HistoryEntry>`).

#### The View Loop

1. Raw Data: `Note.content` (`String`).
2. Parsing: `App::update_content_items()`.
3. Render Model: `Vec<ContentItem>` enum.
    - Transforms raw text lines into `TextLine`, `Image`, `CodeFence`, `TaskItem`.
    - Calculates layout/wrapping.

### 3. Output: Final State & Side Effects

- Visual Output:
    - State: `App` (owning `Editor`, `VimState`, `Vec<ContentItem>`).
    - Renderer: `ratatui::Terminal::draw` consumes `App` state to produce screen buffers.
- Persistence:
    - State: `TextBuffer` -> joined into `String`.
    - Side Effect: `fs::write` updates the `.md` file on disk.

### 4. ZSTs (Zero Sized Types) & Marker Logic

- `WrapCache` (`src/editor/wrap.rs`):
    - Definition: `pub struct WrapCache;`
    - Role: Currently a ZST.
    - Implication: Represents a placeholder for a future line-wrapping optimization system. It allows the `Editor` struct to hold a "cache" slot without consuming memory until the implementation is added, or it acts as a stateless logic provider.
