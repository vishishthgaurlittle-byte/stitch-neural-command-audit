# AI Architecture & Model Management Design Review

**Core Operating Principle:** Strict Single-Authority Hierarchy with Resource-Governed Dual Workers  
**Target Hardware Constraints:** Intel Core i3-6100T (2C/4T) | 16.0 GB RAM (16,384 MiB installed / 16,260 MiB visible) | CPU-Only Execution  

---

## 1. The Mandated Operating Philosophy

The project architecture dictates an uncompromising operational hierarchy designed specifically to prevent RAM exhaustion and eliminate chaotic agent collisions:

```mermaid
flowchart TD
    User["User Request (Text / Voice)"] --> MainAI

    subgraph Permanent_Core [Permanent Application Controller]
        MainAI["MAIN AI ORCHESTRATOR<br>(Always Resident in Memory • Sole Authority)"]
        TaskPlanner["Intent Parsing & DAG Task Planner"]
        SecurityShield["Capability Security & Permission Gate"]
        Synthesizer["Final Answer Synthesizer & Output Reviewer"]
        MainAI --> TaskPlanner
        MainAI --> SecurityShield
        MainAI --> Synthesizer
    end

    subgraph Governed_Workers [Governed Concurrency Slots (Max 1 Local + Max 1 Online)]
        LocalWorkerSlot["LOCAL WORKER SLOT<br>(Max 1 Active Model • Cold-Unload on Idle)"]
        OnlineWorkerSlot["OPTIONAL ONLINE WORKER SLOT<br>(Max 1 Stream • Strict Data Boundary)"]
    end

    subgraph Execution_Swarm [15 Managed Specialist Agents]
        Coder["Coder Agent"]
        Security["Security Auditor"]
        Desktop["PC Automation"]
        OtherAgents["Researcher, Designer, Writer, etc."]
    end

    TaskPlanner -- "Assigns Local Task" --> LocalWorkerSlot
    TaskPlanner -- "Assigns Online Task (If Permitted)" --> OnlineWorkerSlot
    TaskPlanner -- "Dispatches Managed Worker" --> Execution_Swarm

    LocalWorkerSlot -- "Raw Results" --> Synthesizer
    OnlineWorkerSlot -- "Raw Results" --> Synthesizer
    Execution_Swarm -- "Tool Observations" --> Synthesizer

    Synthesizer --> UserResponse["Verified Final Response to User"]
```

### Architectural Rules:
1. **Permanent Main AI:** One central orchestrator (powered by `Qwen3-4B-Q4_K_M` or a dedicated low-RAM planner) that never unloads while the application runs.
2. **Local Worker Concurrency Cap (Max 1):** Never load more than one local heavy model into RAM simultaneously. When a specialized local job (e.g., deep mathematical reasoning with `Nemotron-7.5B`) is required, the Main AI activates it, batches the job, waits for completion, and triggers an idle unload timeout to release RAM back to the operating system.
3. **Online Worker Concurrency Cap (Max 1):** An external cloud model (e.g., Claude 3.5 Sonnet, GPT-4o) may only be queried if explicitly authorized by the user, if the air-gap shield is disabled, and if data boundary filters pass. The online worker reports back to the Main AI; it never speaks directly to the user without Main AI review.
4. **Main AI Authority:** Specialist agents and plugins are subordinate workers. No agent or plugin may unilaterally execute destructive OS actions or bypass the Main AI.

---

## 2. Audit of Stitch Design Against This Philosophy

### A. Strengths Found in the Stitch Design
- **Command Center (Screen 01):** Strongly establishes `[FINAL AI NAME]` as the `PRIMARY CORE` and `Autonomous System Orchestrator`. The visual hierarchy places this central identity at the very top of the interface.
- **Air-Gap Shield Integration:** The design includes a prominent `AIR-GAP SHIELD ACTIVE` badge and toggle, visually indicating whether cloud workers are prohibited.
- **Central Node in Neural Core (Screen 03):** The SVG topology correctly places `CENTRAL ORCHESTRATOR (v2.4 LOCAL HUB)` at the geometrical center of all vectors, demonstrating that agents, models, and plugins radiate outward from the hub.

---

### B. Critical Architectural Deficiencies in Current Design

#### 1. Dangerous Model Concurrency Depiction (Screen 04)
- **Defect:** In `screen_04_intelligence_ai_models/code.html`, the interface depicts `Mistral-7B`, `Llama-3-8B`, and `DeepSeek-Coder-6.7B` as simultaneously `LOADED` and `WARM`.
- **Why This Fails:** On a 12 GB RAM Windows PC, loading multiple 7B models concurrently requires 16–20 GB of RAM. Attempting this would immediately crash the application or cause catastrophic Windows paging disk lockups.
- **Required Correction:** The UI must replace the open-ended model list with an explicit **Two-Slot Architecture**:
  - `Slot 1: Main AI Controller` (Fixed / Always Active)
  - `Slot 2: Local Worker Model` (Status: `Idle`, `Active [Model Name]`, `Unloaded`)

#### 2. Missing Idle-Unload Timeout Governance
- **Defect:** There is no UI setting or visual timer indicating when an idle local model will be unloaded from RAM.
- **Why This Fails:** To prevent frequent, costly reloading penalties for tiny successive tasks, the Main AI needs task batching with an idle-unload countdown (e.g. 120 seconds).
- **Required Correction:** Add an **Idle Memory Release Timer** control in both Screen 04 and Screen 14 (Settings), allowing users to configure the unload threshold (1 min, 5 min, 15 min, Never).

#### 3. Ambiguous Specialist Agent Independence (Screen 06)
- **Defect:** In `screen_06_agent_workspace/code.html`, several agent cards feature independent model selector dropdowns, which could imply to users that each agent runs its own persistent background LLM simultaneously.
- **Why This Fails:** Having 7–15 persistent LLM instances running concurrently is impossible on CPU-only hardware.
- **Required Correction:** Clarify that agents share the **single active Local Worker slot** sequentially, or utilize the Main AI's embedded function-calling parser. Add a visual `Execution Queue` indicator showing agent execution priority.

#### 4. Missing Online Data Boundary Check Indicator
- **Defect:** When triggering tools or prompts that query online providers, the interface does not show the Main AI performing a pre-flight data sanitization or boundary review.
- **Required Correction:** Add a visual badge in the Conversation Workspace (Screen 02) and Command Center (Screen 01) displaying `Main AI Review: Sanitized & Approved` prior to dispatching queries to external endpoints.

---

## 3. Recommended Design Revisions for Phase 2 Implementation

```
+-----------------------------------------------------------------------+
|  CENTRAL ORCHESTRATOR HUB (Always Resident: Qwen3-4B ~3.1 GB RAM)     |
|  [Status: Active • Monitoring System Events]                          |
+-----------------------------------------------------------------------+
|  CONCURRENCY SLOTS                                                    |
|  +----------------------------------+  +----------------------------+ |
|  | [Slot A] LOCAL WORKER            |  | [Slot B] ONLINE WORKER     | |
|  | Model: Nemotron-7.5B (On-Demand) |  | Provider: Claude 3.5 Gated | |
|  | State: UNLOADED (RAM Free: 4.7GB)|  | State: STANDBY (Shield ON) | |
|  | Idle Timeout: 120s               |  | Boundary: Strict Redaction | |
|  +----------------------------------+  +----------------------------+ |
+-----------------------------------------------------------------------+
```

1. **Implement Dedicated Slot Cards** in `screen_04_intelligence_ai_models`.
2. **Update Screen 01 Telemetry Pill:** Display `LOCAL WORKER: UNLOADED (STANDBY)` to reinforce that memory is safely preserved.
3. **Include Idle Countdown Visualizer:** Display a subtle progress ring around the local worker icon indicating time remaining before memory is reclaimed.
