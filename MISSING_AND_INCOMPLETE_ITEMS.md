# Missing, Incomplete, and Static Design Elements Audit

This report catalogs all missing screens, incomplete features, unlinked controls, and architectural gaps discovered during the deep inspection of `stitch_neural_command_desktop_os`.

---

## 1. Summary of Design Deficiencies by Severity

| Severity Level | Total Count | Key Areas Impacted |
| :--- | :--- | :--- |
| **CRITICAL** | **4** | Missing 9 Specialist Agents, Missing AI Concurrency Policy UI, External CDN Network Dependencies, Missing Model Configurations |
| **HIGH** | **5** | Missing OAuth & Account Flows in Plugins, Missing Online Provider Settings Tab, Static Navigation Router, Unwired Emergency Killswitch |
| **MEDIUM** | **6** | Missing Empty States, Missing Error Boundaries, Missing Transliteration Sliders in Voice Studio, Incomplete Breadcrumbs |
| **LOW** | **4** | Minor icon misalignment, placeholder lorem ipsum text, untranslated technical jargon |

---

## 2. Detailed Findings by Domain

### A. Missing Specialist Agents (Screen 06: Agent Workspace)
- **Severity:** **CRITICAL**
- **Finding:** The design specifications require an explicit **15-Agent Structure**. However, `screen_06_agent_workspace/code.html` currently only implements **6 specialist agent cards** plus the Central AI:
  1. *Central AI (Orchestrator Master)* — Implemented
  2. *Coder Agent* — Implemented
  3. *Security Auditor* — Implemented
  4. *PC Automation Agent* — Implemented
  5. *Voice Synthesis Agent* — Implemented
  6. *Designer* — Implemented
  7. *Researcher* — Implemented
- **Missing Agents (8 Agents completely absent from UI):**
  - ❌ **Writer Agent** (Creative writing, technical documentation synthesis)
  - ❌ **Messenger Agent** (Email, Telegram, WhatsApp bridge dispatch)
  - ❌ **File Manager Agent** (Filesystem organization, directory sorting, deduplication)
  - ❌ **Game Helper Agent** (Strategy hints, lore lookups, non-autonomous guidance)
  - ❌ **Tester Agent** (Unit test generation, test runner execution, validation)
  - ❌ **3D Artist Agent** (Mesh generation, Blender script assistance)
  - ❌ **Data Analyst Agent** (CSV/Excel processing, SQL generation, charting)
  - ❌ **Code Reviewer Agent** (Static analysis, security vulnerability scanning)
  - ❌ **Assistant Agent** (General personal tasks, reminders, calendar synthesis)
- **Required Remediation:** 8 additional agent cards must be added to the Agent Workspace grid with tailored role descriptions, model assignments, and capability badges.

---

### B. Missing AI Architecture & Concurrency Controls (Screen 04: Intelligence & AI Models)
- **Severity:** **CRITICAL**
- **Finding:** The operating philosophy requires strict resource governance:
  1. One permanent Main AI (Controller).
  2. Max one local worker model active at a time (with automatic idle unloading).
  3. Max one optional online worker model active at a time.
  4. Never load all models into RAM simultaneously.
- **Current UI Flaw:** `screen_04_intelligence_ai_models/code.html` depicts multiple local models simultaneously marked as `LOADED`, `WARM`, and `SELECTED`, which would exceed the user's 12 GB RAM ceiling.
- **Missing UI Controls:**
  - ❌ Dedicated **"Active Local Worker Slot"** container showing whether a local model is active, idle, or unloaded.
  - ❌ Dedicated **"Online Worker Slot"** container showing connection status, provider name, and data-sharing approval.
  - ❌ **Configurable Idle-Unload Timeout Slider** (e.g., Unload local worker after 60s / 120s / 300s of inactivity to free RAM).
  - ❌ **User Models Representation:** The screen displays generic models (`Mistral-7B`, `DeepSeek-Coder-6.7B`, `Llama-3-8B`) instead of the user's actual GGUF models (`Qwen3-4B-Q4_K_M`, `Nemotron-3.5-Bolt-7.5B`, `qwen3-embedding-0.6b`).

---

### C. Missing Plugin Center Flows (Screen 05: Plugin Centre)
- **Severity:** **HIGH**
- **Finding:** The Plugin Centre focuses exclusively on local sandbox tools (`FS Local Sandbox`, `Git Engine`, `Obsidian Sync`). All cloud and account connection workflows are missing:
  - ❌ **Zero OAuth Account Connection Cards:** No UI to link Google Workspace, GitHub, Notion, Dropbox, or Discord.
  - ❌ **No Connection Health Tests:** No `Test Connection`, `Ping API`, or `Verify Token` buttons.
  - ❌ **No Reconnect / Disconnect Toggles:** If a token expires, there is no UI state showing a warning badge or reconnect flow.
  - ❌ **No Plugin Discovery Catalog:** No marketplace shelf to browse or install new community plugins or MCP servers.

---

### D. External Network Dependencies (Threat to Air-Gap Operation)
- **Severity:** **CRITICAL**
- **Finding:** All 15 HTML files import three external cloud resources:
  1. `<script src="https://cdn.tailwindcss.com"></script>` (Tailwind CDN)
  2. `<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined..." rel="stylesheet">`
  3. `<link href="https://fonts.googleapis.com/css2?family=Manrope...&family=Inter...&family=JetBrains+Mono..." rel="stylesheet">`
  4. Top header logo points to a remote Google CDN image (`https://lh3.googleusercontent.com/aida/...`).
- **Consequence:** If the desktop PC has no internet connection, the application interface will fail to style, icon fonts will display as raw text (e.g. `settings`, `check_circle`), and the header logo will display a broken image icon.
- **Required Remediation:** 
  - Compile Tailwind CSS locally into a single static `bundle.css`.
  - Bundle fonts and Material Symbols as local `.woff2` files.
  - Save the logo image asset locally inside `assets/`.

---

### E. Missing Settings Panels (Screen 14: Settings)
- **Severity:** **HIGH**
- **Finding:** Several essential configuration tabs required by the project specifications are absent:
  - ❌ **Dedicated Online Providers Tab:** No place to manage API keys for OpenRouter, Anthropic, OpenAI, Groq, or Gemini.
  - ❌ **Dedicated Privacy & Telemetry Tab:** No UI to audit outbound network telemetry, disable analytics, or inspect local logs.
  - ❌ **Data Directory Management:** Path configuration is visually static; no folder picker buttons or disk usage gauges.

---

### F. Static Interactivity & Lack of Backend Binding
- **Severity:** **HIGH**
- **Finding:** Of the **807 audited controls** in `INTERACTION_AUDIT.csv`:
  - **712 controls (88.2%)** are purely static HTML/CSS markup with no event handlers.
  - **95 controls (11.8%)** have basic client-side JavaScript prototype toggles (e.g., toggling an active tab or pill CSS class).
  - **Zero controls** are wired to a persistent state store, local filesystem, or AI inference backend.
- **Impact:** This is expected for Phase 1 design mockups, but represents the core development work required for Phase 2.

---

### G. Incomplete Voice & Personality Studio (Screen 10)
- **Severity:** **MEDIUM**
- **Finding:**
  - ❌ **No Hindi Voice Profile:** The screen only shows generic English voice names; there is no card for `hi_IN-rohan` or Devanagari pronunciation tuning.
  - ❌ **No Transliteration Toggle:** Missing an option to switch between Devanagari script and Romanized Hindi (Hinglish) phonemization.
  - ❌ **No VAD Gate Tuning:** Missing sliders for Silero VAD gate volume threshold and speech hangover seconds.
