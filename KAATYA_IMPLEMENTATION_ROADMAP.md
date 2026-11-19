# KAATYA: Master Phased Implementation Roadmap

This roadmap defines the sequential, 10-milestone engineering schedule for constructing the **KAATYA Windows 10 Desktop AI Assistant Application**. Every milestone establishes strict dependencies, tangible deliverables, and objective acceptance criteria.

---

## 1. Phased Engineering Timeline

```mermaid
gantt
    title KAATYA Phased Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Phase 3.1 Architecture
    Master Audit & Specifications        :done,    m0, 2026-11-19, 2026-11-20
    section Phase 4 Engineering
    M1: Core Tauri v2 & Rust Foundation  :active,  m1, 2026-11-21, 2026-11-26
    M2: App Shell & Stitch HUD Overlay   :         m2, 2026-11-27, 2026-12-03
    M3: KAATYA Main AI & 23-Agent Queue  :         m3, 2026-12-04, 2026-12-10
    M4: Local Workers & Memory Gate      :         m4, 2026-12-11, 2026-12-17
    M5: Security Gate & AST Sandbox      :         m5, 2026-12-18, 2026-12-23
    M6: Video Studio & Image Studio      :         m6, 2026-12-24, 2026-12-31
    M7: Memory (sqlite-vec) & Voice      :         m7, 2027-01-01, 2027-01-08
    M8: Full Screen Wiring & Agents      :         m8, 2027-01-09, 2027-01-16
    M9: DPAPI Key Vault & MCP Plugins    :         m9, 2027-01-17, 2027-01-23
    M10: Verification & Offline MSI      :         m10, 2027-01-24, 2027-01-31
```

---

## 2. Detailed Milestone Specifications

### Milestone 1: Core Tauri v2 & Rust Foundation
- **Dependencies:** None.
- **Deliverables:**
  - Initialized Tauri v2 workspace with Rust 2024 edition and React 19 + TypeScript 5.5 frontend.
  - Bundled offline assets: Manrope, Inter, and JetBrains Mono WOFF2 fonts; Material Symbols SVG sprite sheet.
  - Precompiled Tailwind CSS via PostCSS/Vite (zero runtime CDN scripts).
  - Native Win32 memory check module (`GlobalMemoryStatusEx`) in Rust.
- **Acceptance Criteria:**
  - `cargo tauri dev` cold launches a native window in $<1.5\text{ seconds}$.
  - Zero outbound network requests detected in devtools (100% offline).
  - Base idle memory consumption is $\le 65\text{ MB RAM}$.

---

### Milestone 2: Application Shell, Obsidian Command UI & Floating AI HUD
- **Dependencies:** Milestone 1.
- **Deliverables:**
  - 14-page persistent left navigation rail matching Google Stitch styles.
  - Secondary transparent, always-on-top **Floating AI HUD** window (`screen_15`).
  - Global `F9` hotkey handler toggling the Floating HUD.
  - Responsive design tokens: `#070B14` canvas, `#43D9FF` local accent, `#367BFF` system accent.
- **Acceptance Criteria:**
  - Smooth page navigation between all 14 views with zero full-page reloads.
  - Pressing `F9` instantly reveals or conceals the Floating HUD over third-party Windows apps.

---

### Milestone 3: KAATYA Main AI Controller & 23-Agent Task Queue
- **Dependencies:** Milestone 2.
- **Deliverables:**
  - Resident model loader pinning `Qwen3-4B-Q4_K_M.gguf` in RAM via `llama.cpp` AVX2 backend.
  - Async Tokio task queue managing multi-step workflows and dependency resolution.
  - System prompt persona harnesses for all **23 logical agent roles**.
  - Strict concurrency enforcer (1 permanent Main AI, $\le 1$ local worker, $\le 1$ online worker).
- **Acceptance Criteria:**
  - KAATYA Main AI stays permanently resident in memory; never unloads.
  - State machine emits live status updates (`Ready`, `Listening`, `Planning`, `Executing`, `Completed`) to UI in $<2\text{ ms}$.

---

### Milestone 4: Local Model Runtime & Memory-Gated Worker Pool
- **Dependencies:** Milestone 3.
- **Deliverables:**
  - Ephemeral worker loader supporting `Qwen2.5-Coder-1.5B`, `SmolLM2-1.7B`, and `Qwen3-1.7B`.
  - Memory-gated pre-flight check preventing worker loading if free RAM is $<2.5\text{ GB}$.
  - Zero-copy token streaming from local models into Conversation Workspace (Screen 02).
- **Acceptance Criteria:**
  - Loading a local worker executes within remaining physical RAM without causing Windows pagefile thrashing.
  - Worker is immediately unmapped and evicted from memory upon subtask completion.

---

### Milestone 5: Security Gate, AST Shell Sandbox & Emergency Stop
- **Dependencies:** Milestone 4.
- **Deliverables:**
  - Three-tier permission gate with interactive UI approval modals.
  - Scoped workspace directory whitelisting (`T:\ai creation` / approved paths).
  - PowerShell AST semantic analyzer parsing shell commands before execution.
  - Dedicated non-swallowing emergency panic hotkey (`Ctrl + Alt + Escape`) + bare `ESC` window cancel.
  - Append-only SQLite `audit_events` logger.
- **Acceptance Criteria:**
  - Pressing `Ctrl + Alt + Escape` immediately kills running child processes and silences audio in $<50\text{ ms}$.
  - Destructive file edits or elevated commands are strictly blocked without human confirmation.

---

### Milestone 6: Video Studio & Image Studio Multimodal Engines
- **Dependencies:** Milestone 5.
- **Deliverables:**
  - FFmpeg CLI wrapper for programmatic cutting, concatenation, audio ducking, and subtitle burn-in.
  - Visible CapCut Desktop UI automation integration using Windows UIAutomation.
  - Whisper-based automatic subtitle generation and timecode alignment.
  - Experimental local `flux-2-klein-4b` pipeline loader with CPU execution warnings.
  - Online provider integration (DALL-E 3, Ideogram) with mandatory per-generation approval modal.
- **Acceptance Criteria:**
  - Video Studio successfully renders 16:9 and 9:16 MP4 videos with synchronized subtitles.
  - Online image/video generation requests display full prompt, provider, and cost before transmission.

---

### Milestone 7: Persistent Semantic Memory & Real-Time Offline Voice
- **Dependencies:** Milestone 6.
- **Deliverables:**
  - Local embedding pipeline using `qwen3-embedding-0.6b-q8_0.gguf` + `sqlite-vec`.
  - Piper TTS engine supporting `en_US-mike` and `hi_IN-rohan`.
  - Whisper Base STT engine (`ggml-base.bin`) with Push-to-Talk (PTT) and instant barge-in interruptibility.
- **Acceptance Criteria:**
  - Vector similarity search returns top-5 relevant notes in $<25\text{ ms}$.
  - Piper synthesizes natural speech in English and Hindi at RTF $\le 0.12$.
  - Speaking while audio is playing instantly halts TTS playback in $<10\text{ ms}$.

---

### Milestone 8: Full 15-Screen Wiring & 23-Agent Dispatch
- **Dependencies:** Milestone 7.
- **Deliverables:**
  - Complete backend binding for all 15 Google Stitch screens:
    - Screen 01: Central command buffer & quick actions.
    - Screen 03: 2D/2.5D Canvas neural core graph (`GL_LOWRES`).
    - Screen 06: Filterable 23-agent roster grid.
    - Screen 08: Video Studio, Image Studio, and SQL runner drawers.
    - Screen 12: Real-time telemetry (CPU, RAM, HD 530 GPU, USB 3.0 storage).
- **Acceptance Criteria:**
  - All 23 agents can be assigned tasks through the UI.
  - Zero broken buttons, missing state bindings, or console warnings.

---

### Milestone 9: Plugin Architecture & Windows DPAPI Key Vault
- **Dependencies:** Milestone 8.
- **Deliverables:**
  - Encrypted credential manager using Windows DPAPI (`CryptProtectData`).
  - Model Context Protocol (MCP) local stdio server driver.
  - Cloud provider connectors for Anthropic Claude, OpenAI, Google Gemini, and Groq.
  - Air-Gap Master Switch physically enforcing localhost-only socket policies.
- **Acceptance Criteria:**
  - API keys stored in SQLite are cryptographically unreadable outside the active Windows user session.
  - Activating the Air-Gap Shield immediately blocks all outbound remote sockets.

---

### Milestone 10: Verification, Profiling & Offline Installer Packaging
- **Dependencies:** Milestone 9.
- **Deliverables:**
  - Standalone Inno Setup / WiX installer bundling the **Microsoft Edge WebView2 Fixed Version Runtime** (~185 MB total).
  - Automated integration test suite validating memory limits, thread pinning, and security policies.
  - User administration guide and offline troubleshooting manual.
- **Acceptance Criteria:**
  - Clean installation on a fresh Windows 10 PC with zero internet connection.
  - System memory consumption remains strictly $\le 7.5\text{ GB RAM}$ with permanent Main AI resident.
