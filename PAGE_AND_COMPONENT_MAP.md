# Page and Component Architecture Map

**Design System:** Obsidian Command  
**Source Directory:** `T:\ai creation\stitch_neural_command_desktop_os\`  
**Target Application:** Local AI Desktop Assistant (Windows 10 Desktop OS)

This document maps all 15 designed screens, detailing their layout architecture, component hierarchy, visual controls, and implementation status.

---

## 1. Global Shell & Navigation Rail (Present across Screens 01–14)

Each standard screen implements a shared, persistent desktop layout:
- **Top Application Header (`<header class="fixed top-0 ... h-14">`):**
  - **Emblem / Logo:** Remote PNG (`ALJJyrDkwdFfa2Zb...`) with fallback styling.
  - **AI Identity Pill:** Monospaced tag displaying `[FINAL AI NAME]`.
  - **Workspace Selector:** Terminal path indicator (`root / workspace`).
  - **Global Command Search Bar:** Triggered via `Ctrl + K`.
  - **Operational Telemetry Badge:** `LOCAL MODE: ACTIVE` (cyan `#43D9FF`).
  - **Utility Controls:** Mic quick-toggle, Shield status, Notifications bell, User profile menu.
- **Left Navigation Rail (`<aside class="fixed top-14 left-0 w-64 ...">`):**
  - 14 Primary Navigation Destinations:
    1. `command-center` (Screen 01)
    2. `conversation` (Screen 02)
    3. `3d-neural-core` (Screen 03)
    4. `intelligence-models` (Screen 04)
    5. `plugin-center` (Screen 05)
    6. `agent-workspace` (Screen 06)
    7. `workflow-builder` (Screen 07)
    8. `pc-control` (Screen 08)
    9. `memory-center` (Screen 09)
    10. `voice-studio` (Screen 10)
    11. `tasks-activity` (Screen 11)
    12. `system-monitor` (Screen 12)
    13. `security-permissions` (Screen 13)
    14. `settings` (Screen 14)
  - Bottom Rail Quick Actions:
    - `HUD Mode` (Shortcut `F9`) → Launches Screen 15.
    - `Collapse Rail` (Shortcut `Ctrl + [`).

---

## 2. Screen-by-Screen Component Breakdown

### Screen 01: Command Center
- **File:** `screen_01_command_center/code.html` (58,845 bytes)
- **Layout:** Two-column split grid (Col-span 7 ~60% Primary Workspace, Col-span 5 ~40% Live Operations).
- **Key Components:**
  1. *Hero Identity Card:* Central neural emblem with animated CSS pulse ring; orchestrator title `[FINAL AI NAME]` with inline edit button; `AIR-GAP SHIELD ACTIVE` badge.
  2. *Runtime Execution State Switcher:* 4-state segmented control (`STANDBY`, `REASONING`, `SYNTHESIS`, `AIR-GAPPED SHIELD`).
  3. *Primary Command Input Console:* Multi-modal prompt bar with audio visualizer waveform, attachment clip button, and dispatch action (`Ctrl+Enter`).
  4. *Pending Human Approvals Card:* Interactive security confirmation cards for sensitive actions (e.g., `File Deletion & Overwrite in /dist/artifacts`).
  5. *Live Active Task Rail:* Progress indicators for background tasks (`Local Codebase Security Audit` at 68%).
  6. *Hardware Quick-Telemetry Cards:* Real-time meters for VRAM/RAM allocation, context token utilization, and active model tag.
- **Status:** Complete structural mockup with client-side pill-switching prototype script.

---

### Screen 02: Conversation Workspace
- **File:** `screen_02_conversation_workspace/code.html` (51,995 bytes)
- **Layout:** Three-pane layout (History & Sessions Sidebar 20%, Multi-turn Chat Thread 55%, Context & Tool Inspector 25%).
- **Key Components:**
  1. *Thread History Rail:* Chronological session grouping (Today, Yesterday, Last Week) with search filter.
  2. *Message Bubbles:* Dual-bubble design distinguishing User (dark slate with blue accent) from Assistant (dark container with cyan glowing border).
  3. *Tool Call Cards:* Collapsible execution blocks displaying tool parameters, raw terminal outputs, and execution duration in milliseconds.
  4. *Multi-Model Routing Indicator:* Displays which model answered each turn (`Qwen3-4B Local` vs `Nemotron-7.5B Deep`).
  5. *Rich Text & Code Renderer:* Styled code blocks with copy-to-clipboard, language tags, and token consumption markers.
- **Status:** High visual density; message rendering and tool cards are fully designed.

---

### Screen 03: 3D Neural Core
- **File:** `screen_03_3d_neural_core/code.html` (54,440 bytes)
- **Layout:** Full-viewport interactive visualization canvas with floating HUD controls and right-hand Node Inspector drawer.
- **Key Components:**
  1. *Topology Canvas (`#topoCanvas`):* 11.7 KB inline SVG featuring 31 node circles, 17 animated connection vectors, and Gaussian blur glowing filters.
  2. *Node Clusters Represented:*
     - Central Orchestrator Hub (`v2.4 LOCAL HUB`)
     - Local Model Nodes (`Mistral-7B Q4_K_M`, `Llama-3-8B`, `DeepSeek-Coder-6.7B`, `Whisper-Base-IN`)
     - Gated Cloud Nodes (`Claude 3.5 Sonnet`, `Gemini 1.5 Pro`, `Groq LPU`)
     - Active Specialist Agents (`Coder Agent #84`, `Security Agent`, `Researcher Agent`)
     - Memory & Storage Nodes (`Obsidian Vector Store`, `Project Scratchpad`, `Local FS Reader`)
  3. *Interactive Graph Controls:* Floating camera zoom (`+` / `-`), reset view, 2D/3D projection toggle, physics simulation pause/play (`#simToggle`).
  4. *Node Inspector Drawer:* Displays node latency, active token streams, memory consumption, and runtime status upon selection.
- **Status:** Beautifully crafted SVG visualization. Operates on CPU-friendly 2D/SVG math.

---

### Screen 04: Intelligence & AI Models
- **File:** `screen_04_intelligence_ai_models/code.html` (52,978 bytes)
- **Bundled Preview:** `screen.png` (702 KB)
- **Layout:** Top dynamic routing map, followed by a grid of configured local model cards and remote provider cards.
- **Key Components:**
  1. *Routing Logic Map:* Visual flow showing intent classification, confidence gating, and local vs. cloud routing paths.
  2. *Configured Model Cards:* Dedicated cards for `Mistral-7B`, `DeepSeek-Coder-6.7B`, `Llama-3-8B`, and `Whisper-Base`.
  3. *Model Metric Badges:* Context length indicators (`32,768 tokens`), Quantization tier (`Q4_K_M`), RAM footprint (`4.8 GB`), and status pill (`LOADED`, `WARM`, `IDLE`).
  4. *Execution Actions:* Direct buttons to `Unload from RAM`, `Set as Default`, or `Run Quant Benchmark`.
- **Status:** Complete mockup; needs updating to feature the user's actual models (`Qwen3-4B`, `Nemotron-7.5B`, `qwen3-embedding`).

---

### Screen 05: Plugin Centre
- **File:** `screen_05_plugin_centre/code.html` (68,478 bytes)
- **Layout:** Filter tab bar across the top, responsive card grid of installed/available plugins, right-hand Slide-out Configuration Drawer.
- **Key Components:**
  1. *Local Plugin Cards:*
     - `FS Local Sandbox` (Filesystem sandbox v2.4.0)
     - `Obsidian Vault Sync` (Markdown knowledge base connector)
     - `Brave Local Indexer` (Privacy-first web browsing engine)
     - `Git & AST Engine` (Repository syntax parsing)
     - `Terminal Exec Enclave` (Sandboxed subshell execution)
     - `Database Inspector` (SQLite/PostgreSQL query bridge)
     - `Whisper Stream DirectML` (Audio capture driver)
     - `Telegram Bot Gateway` (External channel bridge)
  2. *Slide-out Configuration Drawer:* Shows deterministic sandbox rules, granular read/write path allowlists, and memory caps.
- **Status:** Rich local plugin mockup; lacks cloud OAuth linking flows and connection health tests.

---

### Screen 06: Agent Workspace
- **File:** `screen_06_agent_workspace/code.html` (71,082 bytes)
- **Bundled Preview:** `screen.png` (349 KB)
- **Layout:** Header with swarm metrics, search/filter bar, agent grid, and bottom inter-agent message simulation trace.
- **Key Components:**
  1. *Agent Roster Cards:*
     - `Central AI (Orchestrator Master)`
     - `Coder Agent` (Python / Rust / AST specialist)
     - `Security Auditor` (Taint & capability analysis)
     - `PC Automation Agent` (OS & PyAutoGUI worker)
     - `Voice Synthesis Agent` (Audio pipeline worker)
     - `Designer` (UI/CSS specialist)
     - `Researcher` (Web & PDF data extractor)
  2. *Agent Card Controls:* Model assignment dropdown, status toggle (`ENABLED` / `PAUSED`), permission scope badges, and task queue counters.
  3. *Live Inter-Agent Message Trace:* Terminal stream simulating structured message exchange between Orchestrator, Coder, and Security Auditor.
- **Status:** Outstanding multi-agent visualization, but only implements 7 of the intended 15 specialist agents.

---

### Screen 07: Workflow Builder
- **File:** `screen_07_workflow_builder/code.html` (62,610 bytes)
- **Layout:** Node-based visual canvas with left block library palette and bottom execution control bar.
- **Key Components:**
  1. *Visual Flow Canvas:* SVG connected step cards (Trigger → Agent Task → Evaluation Gate → Security Check → Final Output).
  2. *Node Block Types:* Triggers (Schedule, File Change, User Prompt), Workers (Coder Agent, Web Search), and Conditions (Human Approval Required, Token Budget Cap).
  3. *Execution Controls:* `Dry Run`, `Execute Pipeline`, step-by-step debugger, and zoom controls.
- **Status:** Complete UI wireframe; represents DAG workflow automation cleanly.

---

### Screen 08: PC Control Centre
- **File:** `screen_08_pc_control_centre/code.html` (60,436 bytes)
- **Layout:** Three-panel master layout: Active System Processes & Windows (Left), Real-Time Desktop Screenshot Viewport (Center), Automation Action History (Right).
- **Key Components:**
  1. *Desktop Viewport:* Displays active desktop capture with bounding boxes around detected UI controls.
  2. *Failsafe Emergency Killswitch Banner:* Prominently displays `PHYSICAL ESCAPE HOOK: ARMED` (`WH_KEYBOARD_LL`).
  3. *Permission Level Switcher:* 3-tier safety mode (`OBSERVE ONLY`, `PROMPT ON ACTION`, `FULL AUTONOMOUS`).
  4. *Action Execution Ledger:* Audit table logging exact coordinate clicks, typed keystrokes, and launched applications with timestamps.
- **Status:** Highly detailed desktop automation design; matches Stonic's Agent S3 safety model.

---

### Screen 09: Memory Centre
- **File:** `screen_09_memory_centre/code.html` (67,477 bytes)
- **Layout:** Top memory search and vector statistics bar, memory card stream (Left), and interactive Memory Vector Graph (Right).
- **Key Components:**
  1. *Memory Card Ledger:* Factual memory units with creation date, source citation (`User Chat`, `File Scan`), importance score, and pin toggle.
  2. *Memory Actions:* Direct buttons to `Edit Memory`, `Archive`, or `Confirm Irreversible Forget`.
  3. *Memory Graph Cluster:* 2D visualization showing associative clustering of memories around project topics.
  4. *Vector Injection Modal:* Interface to manually input text facts and vectorize them into the embedded store.
- **Status:** Fully realized memory interface.

---

### Screen 10: Voice & Personality Studio
- **File:** `screen_10_voice_personality_studio/code.html` (55,498 bytes)
- **Layout:** Two-column split: Voice Profile Selector & Audio Parameters (Left), Personality Matrix Sliders & Real-Time Test Console (Right).
- **Key Components:**
  1. *Voice Selector Cards:* Profiles for different synthetic voices with playback sample buttons.
  2. *Acoustic Parameter Sliders:* Sliders for Speech Rate (`length_scale`), Pitch Variability (`noise_w`), and Energy/Volume.
  3. *Personality Matrix:* Sliders for Formality (Casual ↔ Technical), Verbosity (Concise ↔ Elaborate), and Proactivity (Passive ↔ Assertive).
  4. *Live Microphone & Audio Waveform Tester:* Interactive test area to speak and hear immediate synthesized voice feedback.
- **Status:** Highly functional design; needs updating to explicitly feature Piper English (`mike`) and Hindi (`rohan`).

---

### Screen 11: Tasks & Activity
- **File:** `screen_11_tasks_activity/code.html` (59,828 bytes)
- **Layout:** Kanban-style multi-column board (Queued, In Progress, Awaiting Approval, Completed, Failed).
- **Key Components:**
  1. *Task Cards:* Task title, assigned agent badge, elapsed execution time, token consumption counter, and status indicator.
  2. *Approval Intercept Cards:* Highlighted amber cards requiring user sign-off with preview of requested command.
  3. *Historical Filter & Search:* Filter tasks by date, agent, model, or status.
- **Status:** Complete task management board.

---

### Screen 12: System Monitor
- **File:** `screen_12_system_monitor/code.html` (60,692 bytes)
- **Layout:** Multi-panel hardware telemetry dashboard with time-series charts and active process lists.
- **Key Components:**
  1. *Hardware Metric Cards:* Real-time gauges for CPU Load %, System RAM Consumption (GB), VRAM / Shared GPU Memory, and Thermal Status.
  2. *Inference Performance Telemetry:* Tokens-per-second throughput graph, Time-to-First-Token (TTFT) latency, and Context Cache hit rates.
  3. *Process Memory Table:* Breakdown of RAM used by GUI, llama.cpp engine, ONNX voice runtime, and SQLite database.
- **Status:** Matches OpenJarvis's Recharts telemetry dashboard concepts.

---

### Screen 13: Security & Permissions
- **File:** `screen_13_security_permissions/code.html` (49,590 bytes)
- **Bundled Preview:** `screen.png` (760 KB)
- **Layout:** Capability matrix grid, security shield status, and chronological security audit event ledger.
- **Key Components:**
  1. *Air-Gap Shield Mode Toggle:* Master hardware switch cutting off all external network access.
  2. *Granular Capability Grid:* Toggles for `Filesystem Read`, `Filesystem Write`, `Subprocess Execution`, `Camera / FaceLock`, `Microphone`, and `Network Access`.
  3. *Path Restriction Whitelist:* Configurable list of folders accessible to agents (e.g. `T:\ai creation\`).
  4. *Security Audit Log:* Tamper-evident ledger recording every tool execution, blocked prompt injection attempt, and permission elevation request.
- **Status:** Flawless visual design; aligns with OpenJarvis's `capabilities.py` and `data_boundary_audit.py`.

---

### Screen 14: Settings
- **File:** `screen_14_settings/code.html` (50,827 bytes)
- **Bundled Preview:** `screen.png` (512 KB)
- **Layout:** Left vertical category tabs with right scrolling settings form panels.
- **Key Components:**
  1. *Settings Categories:* General, AI Orchestrator Policy, Hardware & Performance, Storage & Paths, Appearance, Voice, Security.
  2. *Form Controls:* Model selection dropdowns, thread allocation sliders (`Pinned to 3 threads`), auto-unload idle timeouts, and theme selectors.
  3. *Action Buttons:* `Save Changes`, `Restore Defaults`, `Clear Cache`.
- **Status:** Comprehensive settings mockup; lacks an explicit dedicated "Online Providers" and "Cloud API Keys" tab.

---

### Screen 15: Floating AI HUD
- **File:** `screen_15_floating_ai_hud/code.html` (40,400 bytes)
- **Layout:** Compact, borderless floating widget designed to hover in the corner of Windows 10 desktop.
- **Key Components:**
  1. *Mini Neural Core:* Micro glowing orb displaying AI status (Listening, Thinking, Speaking).
  2. *Quick Command Input:* Pill-shaped text box with voice trigger button.
  3. *Compact Action Feedback:* Real-time micro-stream showing current agent tool (e.g., `Reading file...`).
  4. *Window Controls:* Pin on top, minimize to tray, expand to Full Command Center (`F9`).
- **Status:** Exceptional desktop companion widget design. Aligns with Stonic's Win32 layered overlay HUD concept.
