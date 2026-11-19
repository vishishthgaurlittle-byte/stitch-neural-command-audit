# KAATYA: Final Desktop AI Assistant Master Architecture

**Project Identity:** **KAATYA** — Premium Windows 10 Desktop AI Assistant Application (Not an OS)  
**Audit & Architecture Finalization Date:** November 19, 2026  
**Design System:** Obsidian Command (Preserving all 15 Google Stitch Screens)  
**Target Hardware:** Intel Core i3-6100T (2 Cores, 4 Threads @ 3.20 GHz) | 12.0 GB DDR4 RAM | Intel HD Graphics 530 | Amazon Basics USB 3.0 (116 GB) | Windows 10 64-bit  
**Current Status:** **Final Architecture, Model Inventory & 23-Agent Expansion Complete** (Phase 4 Blocked Pending Review)  
**Primary Source Directory:** [`/design-source/`](./design-source/)  

---

## 🏛️ KAATYA Master Architecture & Engineering Deliverables

The complete, hardware-calibrated technical blueprint and multimodal architecture for KAATYA:

0. **[KAATYA_PHASE_3_CORRECTION_AND_VALIDATION_REPORT.md](./KAATYA_PHASE_3_CORRECTION_AND_VALIDATION_REPORT.md)** — **Latest Validation & Correction Report:** Arithmetic fixes ($12.0 - 7.2 = 4.8\text{ GB}$), FLUX.2 Klein Qwen3 dependencies, video diffusion feasibility, multi-editor interchange, restored 23-agent roster, and unified tech stack.
1. **[KAATYA_FINAL_MASTER_ARCHITECTURE.md](./KAATYA_FINAL_MASTER_ARCHITECTURE.md)** — **The Master Blueprint:** System topology, 12 GB RAM budget, permanent Main AI residency, boundaries.
2. **[KAATYA_FINAL_MODEL_INVENTORY.md](./KAATYA_FINAL_MODEL_INVENTORY.md)** — **Authoritative Model Inventory:** Exact byte sizes, architectures, SHA-256 hashes for all 10 present models.
3. **[KAATYA_MODEL_COMPATIBILITY_AND_BENCHMARK_PLAN.md](./KAATYA_MODEL_COMPATIBILITY_AND_BENCHMARK_PLAN.md)** — Model comparisons, KV cache formulas, CPU throughput bounds, and llama-bench suite.
4. **[KAATYA_AGENT_ROSTER_AND_CAPABILITY_MATRIX.md](./KAATYA_AGENT_ROSTER_AND_CAPABILITY_MATRIX.md)** — **The 23 Logical Agent Roles:** Complete capability matrix, schemas, and task handoff loops.
5. **[KAATYA_VIDEO_STUDIO_ARCHITECTURE.md](./KAATYA_VIDEO_STUDIO_ARCHITECTURE.md)** — **Video Studio:** 22-step production pipeline, FFmpeg CLI engine, CapCut UI automation, Whisper subtitles.
6. **[KAATYA_IMAGE_GENERATION_ARCHITECTURE.md](./KAATYA_IMAGE_GENERATION_ARCHITECTURE.md)** — **Image Studio:** FLUX.2 Klein 4B DiT audit, companion requirements, CPU limits, cloud approval gate.
7. **[KAATYA_ONLINE_PROVIDER_AND_PLUGIN_ARCHITECTURE.md](./KAATYA_ONLINE_PROVIDER_AND_PLUGIN_ARCHITECTURE.md)** — Online AI Provider Manager (Claude, OpenAI, Groq, Runway), DPAPI key vault, Air-Gap rules.
8. **[KAATYA_LOCAL_RUNTIME_AND_MEMORY_POLICY.md](./KAATYA_LOCAL_RUNTIME_AND_MEMORY_POLICY.md)** — Dynamic memory policy, pre-flight RAM checking (`GlobalMemoryStatusEx`), single-worker upper bound.
9. **[KAATYA_MEMORY_AND_VOICE_ARCHITECTURE.md](./KAATYA_MEMORY_AND_VOICE_ARCHITECTURE.md)** — `sqlite-vec` persistent memory (`qwen3-embedding`), Piper TTS (Mike/Rohan), Whisper Base STT, barge-in.
10. **[KAATYA_SECURITY_AND_AUTOMATION_POLICY.md](./KAATYA_SECURITY_AND_AUTOMATION_POLICY.md)** — Three-tier permissions, workspace scoping, PowerShell AST validation, `Ctrl + Alt + Escape` global panic hotkey.
11. **[KAATYA_WINDOWS_10_COMPATIBILITY.md](./KAATYA_WINDOWS_10_COMPATIBILITY.md)** — Windows 10 editions, offline WebView2 Fixed Version Runtime bundling, VC++ redistributable, USB 3.0 storage.
12. **[KAATYA_UI_FEATURE_INTEGRATION_MAP.md](./KAATYA_UI_FEATURE_INTEGRATION_MAP.md)** — Seamless mapping of all 23 agents, Video Studio, Image Studio, and DB runner into the 15 Google Stitch screens.
13. **[KAATYA_IMPLEMENTATION_ROADMAP.md](./KAATYA_IMPLEMENTATION_ROADMAP.md)** — 10-milestone phased development schedule with dependencies and measurable acceptance criteria.
14. **[KAATYA_RISKS_AND_UNRESOLVED_DECISIONS.md](./KAATYA_RISKS_AND_UNRESOLVED_DECISIONS.md)** — Hardware risk register, thermal mitigations, verified facts vs untested items, and 3 review decisions.
15. **[KAATYA_FINAL_AUDIT_REPORT.md](./KAATYA_FINAL_AUDIT_REPORT.md)** — Comprehensive synthesis and final architecture audit sign-off.

---

## 🚀 Original Design Source Files (100% Verified)

- **[SOURCE_RECOVERY_VERIFICATION.md](./SOURCE_RECOVERY_VERIFICATION.md)** — 100% Verification Report with direct links to all 15 HTML files & DESIGN.md
- **[design-source/](./design-source/)** — Full, uncompressed Google Stitch design package directory
  - [obsidian_command/DESIGN.md](./design-source/obsidian_command/DESIGN.md) — Obsidian Command Design System Specification
  - [Screen 01: Command Center](./design-source/screen_01_command_center/code.html)
  - [Screen 02: Conversation Workspace](./design-source/screen_02_conversation_workspace/code.html)
  - [Screen 03: 3D Neural Core](./design-source/screen_03_3d_neural_core/code.html)
  - [Screen 04: Intelligence & AI Models](./design-source/screen_04_intelligence_ai_models/code.html)
  - [Screen 05: Plugin Centre](./design-source/screen_05_plugin_centre/code.html)
  - [Screen 06: Agent Workspace](./design-source/screen_06_agent_workspace/code.html)
  - [Screen 07: Workflow Builder](./design-source/screen_07_workflow_builder/code.html)
  - [Screen 08: PC Control Centre](./design-source/screen_08_pc_control_centre/code.html)
  - [Screen 09: Memory Centre](./design-source/screen_09_memory_centre/code.html)
  - [Screen 10: Voice & Personality Studio](./design-source/screen_10_voice_personality_studio/code.html)
  - [Screen 11: Tasks & Activity](./design-source/screen_11_tasks_activity/code.html)
  - [Screen 12: System Monitor](./design-source/screen_12_system_monitor/code.html)
  - [Screen 13: Security & Permissions](./design-source/screen_13_security_permissions/code.html)
  - [Screen 14: Settings](./design-source/screen_14_settings/code.html)
  - [Screen 15: Floating AI HUD](./design-source/screen_15_floating_ai_hud/code.html)

---

## 📋 Historical Audit Documentation

- [PHASE_3_1_INDEPENDENT_AUDIT.md](./PHASE_3_1_INDEPENDENT_AUDIT.md) — Phase 3.1 independent audit and corrections.
- [MASTER_STITCH_DESIGN_AUDIT.md](./MASTER_STITCH_DESIGN_AUDIT.md) — Phase 1 UX & component audit.
- [STITCH_FILE_INVENTORY.csv](./STITCH_FILE_INVENTORY.csv) — Inventory of original templates.
- [PAGE_AND_COMPONENT_MAP.md](./PAGE_AND_COMPONENT_MAP.md) — Screen-by-screen breakdown.
- [INTERACTION_AUDIT.csv](./INTERACTION_AUDIT.csv) — Audit of all 807 interactive UI elements.
- [GITHUB_UPLOAD_LOG.md](./GITHUB_UPLOAD_LOG.md) — Remote upload logs.
