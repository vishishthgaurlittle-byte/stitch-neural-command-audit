# Development Roadmap & Implementation Milestones

This roadmap defines the sequential, phased implementation sequence for building the Windows 10 Desktop AI Assistant Application. Each milestone establishes strict architectural dependencies, concrete deliverables, and objective acceptance criteria.

---

## Roadmap Visual Overview

```mermaid
gantt
    title Desktop AI Assistant Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Phase 3 Planning
    Master Architecture & Specs          :done,    m0, 2026-11-19, 2026-11-20
    section Phase 4 Execution
    M1: Core Shell & Rust Scaffold      :active,  m1, 2026-11-21, 2026-11-26
    M2: App Shell & Stitch Navigation   :         m2, 2026-11-27, 2026-12-03
    M3: Orchestrator & Task Queue       :         m3, 2026-12-04, 2026-12-10
    M4: Local llama.cpp Engine          :         m4, 2026-12-11, 2026-12-17
    M5: Security Gate & Emergency ESC   :         m5, 2026-12-18, 2026-12-23
    M6: Safe Desktop Automation         :         m6, 2026-12-24, 2026-12-30
    M7: 15-Screen Feature Integration   :         m7, 2026-12-31, 2027-01-08
    M8: Plugins & DPAPI Key Vault       :         m8, 2027-01-09, 2027-01-15
    M9: SQLite-Vec Memory & Piper Voice :         m9, 2027-01-16, 2027-01-23
    M10: Verification & Windows MSI     :         m10, 2027-01-24, 2027-01-31
```

---

## Detailed Milestone Breakdown

### Milestone 1: Technical Architecture & Core Rust Scaffold
- **Dependencies:** None.
- **Deliverables:**
  - Initialized Tauri v2 project repository (`src-tauri` and `src`).
  - Native Rust project configured with `tokio`, `rusqlite`, `windows-rs`, and `tracing`.
  - React 19 + TypeScript + Vite frontend configured with precompiled Tailwind CSS.
  - Bundled local offline typography (Manrope, Inter, JetBrains Mono WOFF2) and local SVG icons.
- **Acceptance Criteria:**
  - `cargo tauri dev` compiles and launches a native desktop window in <10 seconds.
  - Zero external HTTP network requests detected in browser devtools upon launch (100% offline).
  - Base memory footprint of the idle application is $\le 55\text{ MB RAM}$.

---

### Milestone 2: Application Shell, Obsidian Command Design & HUD Window
- **Dependencies:** Milestone 1.
- **Deliverables:**
  - 14-page persistent navigation rail matching Google Stitch styles.
  - Obsidian Command design system tokens (`#070B14` canvas, `#43D9FF` local accent, `#367BFF` system accent).
  - Global `F9` hotkey handler triggering the secondary transparent **Floating AI HUD** window (`screen_15`).
  - Collapsible navigation rail (`Ctrl+[`).
- **Acceptance Criteria:**
  - Seamless navigation between all 14 screens without full-page reloads.
  - Pressing `F9` instantly reveals or conceals the Floating AI HUD over active Windows applications.
  - Smooth window drag operations with zero visual tearing or frame drops.

---

### Milestone 3: Main AI Orchestrator Kernel & Async Task Queue
- **Dependencies:** Milestone 2.
- **Deliverables:**
  - Rust-based Orchestrator state machine (`Ready`, `Planning`, `Using Local Model`, `Activating Agent`, `Executing`, `Completed`).
  - Priority task queue supporting step dependency resolution and cancellation tokens.
  - Definition and prompt injection harnesses for all **15 logical agent roles**.
  - Strict concurrency enforcer (1 Main AI, $\le 1$ Local Worker, $\le 1$ Online Worker).
- **Acceptance Criteria:**
  - Task state transitions emit to the UI over Tauri events in $<2\text{ ms}$.
  - System reliably dispatches subtasks across logical agent roles sequentially without memory leakage.
  - Concurrency enforcer strictly blocks attempts to spawn concurrent worker models.

---

### Milestone 4: Local llama.cpp Engine & Streaming Token Pipeline
- **Dependencies:** Milestone 3.
- **Deliverables:**
  - Integrated `llama.cpp` AVX2 binary / FFI bindings pinned to 3 CPU threads on Intel i3-6100T.
  - Memory-mapped model loader with resident pinning for `Qwen3-4B-Q4_K_M.gguf`.
  - Sequential staging loader for `Nemotron-3.5-Bolt-E4B-Q4_K_M.gguf`.
  - Zero-copy token streaming over Tauri IPC into Conversation Workspace (Screen 02).
- **Acceptance Criteria:**
  - `Qwen3-4B` generates text at $\ge 12\text{ tokens/second}$ sustained on the i3-6100T.
  - Resident memory under active 4K context generation does not exceed $3,300\text{ MB RAM}$.
  - Sequential model eviction completely frees memory before loading the secondary worker.

---

### Milestone 5: Security Gate, Three-Tier Permissions & Emergency ESC
- **Dependencies:** Milestone 4.
- **Deliverables:**
  - Policy enforcement engine classifying actions into Tier 1, Tier 2, and Tier 3.
  - Modal confirmation dialog with side-by-side file diffs and risk summaries.
  - Low-level Win32 keyboard hook registering global `ESC` emergency interrupt.
  - Append-only SQLite audit log recording every tool invocation.
- **Acceptance Criteria:**
  - Pressing `ESC` anywhere on Windows terminates active tool subprocesses and silences audio in $<50\text{ ms}$.
  - Tier 3 actions (file deletion, external network calls) are strictly blocked without human confirmation.
  - Audit log table in Screen 13 immediately displays newly recorded events.

---

### Milestone 6: Safe Desktop Automation & Win32 Interactivity
- **Dependencies:** Milestone 5.
- **Deliverables:**
  - Scoped filesystem manager with automatic pre-edit backups (`.assistant/backups/`).
  - Sandboxed child process runner for PowerShell and CMD with output streaming and blacklist filters.
  - Win32 window enumeration and focus switching via `windows-rs`.
- **Acceptance Criteria:**
  - Attempted destructive file operations outside approved workspace paths are rejected.
  - Running a shell script streams stdout live to the terminal console (Screen 08) without UI freezes.
  - Rolling back a modified file successfully restores the original content byte-for-byte.

---

### Milestone 7: Screen-to-Feature Full Integration
- **Dependencies:** Milestone 6.
- **Deliverables:**
  - Complete backend binding for all 15 screens:
    - Screen 01: Live dashboard counters & prompt buffer.
    - Screen 03: 2D/2.5D Canvas neural core graph.
    - Screen 06: Real-time agent status inspection.
    - Screen 07: Visual workflow graph editor.
    - Screen 11: Task activity monitor with live timers.
    - Screen 12: Real-time hardware telemetry (CPU, RAM, GPU, tok/s).
- **Acceptance Criteria:**
  - Every button, slider, and toggle across all 15 screens is connected to functional Rust backend logic.
  - System Monitor meters match real Windows Task Manager performance metrics within 5%.
  - Zero unresolved UI console warnings or broken references.

---

### Milestone 8: Plugin System, DPAPI Key Vault & Air-Gap Shield
- **Dependencies:** Milestone 7.
- **Deliverables:**
  - Encrypted credential manager using Windows DPAPI (`CryptProtectData`).
  - Model Context Protocol (MCP) stdio connector.
  - Driver connectors for Anthropic Claude, OpenAI, Google Gemini, and Groq.
  - Hardware Air-Gap switch in UI header that physically blocks non-localhost network traffic.
- **Acceptance Criteria:**
  - API keys stored in SQLite are cryptographically unreadable without the active user logon session.
  - Connection Test button in Plugin Center (Screen 05) accurately reports HTTP latency and status.
  - Activating the Air-Gap Shield immediately terminates remote connections and routes exclusively to local models.

---

### Milestone 9: Persistent Vector Memory & Offline Voice Engine
- **Dependencies:** Milestone 8.
- **Deliverables:**
  - Local embedding pipeline using `qwen3-embedding-0.6b-q8_0.gguf` + `sqlite-vec`.
  - Semantic memory search and fact pinning in Memory Center (Screen 09).
  - Native Piper TTS engine supporting `en_US-mike` and `hi_IN-rohan`.
  - Whisper Base STT engine (`ggml-base.bin`) with Push-to-Talk (PTT) and barge-in audio interruption.
- **Acceptance Criteria:**
  - Vector similarity search returns top-5 relevant conversation chunks in $<25\text{ ms}$.
  - Piper TTS synthesizes spoken audio at RTF $\le 0.12$ with zero audio clicks or buffer underruns.
  - Spoken English and Hindi utterances are transcribed by Whisper in $<1.0\text{ second}$.
  - Speaking while audio is playing instantly halts TTS playback.

---

### Milestone 10: Verification, Packaging & Offline Windows Installer
- **Dependencies:** Milestone 9.
- **Deliverables:**
  - Automated integration test suite validating memory limits, thread pinning, and security policies.
  - WiX / Inno Setup standalone Windows installer (`.msi` / `.exe`).
  - Bundled Microsoft Edge WebView2 Evergreen bootstrapper for completely air-gapped PCs.
  - Complete user administration manual and offline troubleshooting guide.
- **Acceptance Criteria:**
  - Clean installation on a fresh Windows 10 PC with zero internet connection.
  - Application cold launches to a fully functional desktop interface in $<1.5\text{ seconds}$.
  - System memory consumption remains strictly within the $\le 7.5\text{ GB}$ operational ceiling during multi-agent task execution.
