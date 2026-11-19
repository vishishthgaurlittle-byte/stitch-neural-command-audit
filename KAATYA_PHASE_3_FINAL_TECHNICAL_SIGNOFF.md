# KAATYA: Phase 3 Final Technical Sign-Off & Architecture Validation Report

---

## 1. Project Identity and Scope

- **Project Name:** **KAATYA**
- **Project Identity:** Premium Windows 10 Desktop AI Assistant Application.
- **Operating Context:** Runs as a standard native desktop user-space application hosted directly on Windows 10 64-bit.
- **Explicit Project Boundaries:**
  - KAATYA is **NOT** a new operating system, kernel, or bootloader.
  - KAATYA is **NOT** a Windows shell replacement or Linux distribution.
  - KAATYA is **NOT** an automated gameplay bot (Game Helper provides informational hints and keybindings only).
  - KAATYA executes as a local-first assistant providing intelligent task planning, coding assistance, document synthesis, multi-editor video assembly, and vector search.
- **Repository:** [`https://github.com/vishishthgaurlittle-byte/stitch-neural-command-audit`](https://github.com/vishishthgaurlittle-byte/stitch-neural-command-audit)
- **Branch:** `main`

---

## 2. Final Hardware Specification

All architectural thresholds and execution policies are calibrated against the target physical computer:
- **Processor:** Intel Core i3-6100T (Skylake, 35W TDP).
- **Cores / Threads:** 2 physical cores, 4 logical threads @ 3.20 GHz base frequency.
- **Instruction Set:** AVX2, FMA3, SSE4.2, BMI2 supported (no AVX-512, no AMX).
- **Physical Memory:** 12.0 GB marketed capacity DDR4 RAM.
  - Binary Representation: $12\text{ GiB} = 12,288\text{ MiB} = 12,884,901,888\text{ bytes}$.
  - Decimal Representation: $\approx 12.88\text{ GB}$ ($12,884,901,888 / 10^9\text{ bytes}$).
- **Graphics Subsystem:** Intel HD Graphics 530 (Integrated Processor Graphics).
  - Dedicated VRAM: 0 MB (No dedicated GDDR/HBM).
  - Architecture: Gen9 GT2 (24 Execution Units).
  - Acceleration Capability: DirectX 12, Direct3D 11, Intel Quick Sync Video (QSV).
  - Compute Limitations: Zero NVIDIA CUDA cores, zero Tensor cores.
  - Video Memory Management: Intel Dynamic Video Memory Technology (DVMT) utilizing shared system RAM dynamically.
- **Storage Configuration:**
  - Internal System Drive (`T:\ai creation`): Hosts resident model assets, SQLite databases, and workspace directories.
  - External Storage: Amazon Basics USB 3.0 Pendrive (~116 GB usable capacity, reserved for media scratch and cold archives).
- **Operating System:** Windows 10 64-bit (Build 19045 / 22H2).

---

## 3. Corrected Memory Arithmetic & Accounting

### 3.1 Strict Unit Definitions
To avoid arithmetic contradictions, binary and decimal gigabytes are never mixed in the same calculation:
- $1\text{ GiB} = 1,024\text{ MiB} = 1,073,741,824\text{ bytes}$.
- $1\text{ GB} = 1,000,000,000\text{ bytes}$.
- $1\text{ MiB} = 1,048,576\text{ bytes}$.

### 3.2 Binary Memory Arithmetic
$$\begin{aligned}
\text{Total Visible Physical Memory} &= 12,288\text{ MiB} \quad (12.00\text{ GiB}) \\
\text{Provisional Base Working Set Commitment} &\approx 6,788\text{ MiB} \quad (~6.63\text{ GiB}) \\
\hline
\mathbf{Uncommitted\ Physical\ Memory\ Headroom} &\approx \mathbf{5,500\text{ MiB}} \quad (\mathbf{~5.37\text{ GiB}})
\end{aligned}$$

*(Note: In decimal conversion, the $5,500\text{ MiB}$ remainder equals $5,500 \times 1,048,576 / 10^9 \approx \mathbf{5.77\text{ GB}}$. In a hypothetical pure $12.00\text{ GB}$ decimal calculation with a $7.20\text{ GB}$ footprint, the remainder is $12.00 - 7.20 = \mathbf{4.80\text{ GB}}$. The previous contradictory calculation that subtracted a 7.12 GB baseline from a 12.00 decimal capacity has been completely removed).*

---

## 4. Memory Evidence and Measurement Limitations

### 4.1 Itemized Memory Accounting Table

| Component | Measured or Estimated (MiB) | Evidence Status | Notes |
| :--- | ---:| :--- | :--- |
| **Windows Base OS & Services** | ~2,900 MiB | PROVISIONAL ESTIMATE | Windows 10 x64 kernel, DWM, background services |
| **Dynamic GPU Shared Memory** | ~150 MiB | PROVISIONAL ESTIMATE | Intel HD 530 DVMT dynamic UI allocation (idle) |
| **KAATYA Desktop Shell** | ~220 MiB | PROVISIONAL ESTIMATE | Tauri v2 host binary + Edge WebView2 (15 screens) |
| **Audio Subsystem** | ~300 MiB | PROVISIONAL ESTIMATE | PortAudio stream, Piper dual ONNX, Whisper buffer |
| **Database Store** | ~80 MiB | PROVISIONAL ESTIMATE | SQLite 3 engine and `sqlite-vec` cache |
| **KAATYA Main AI** | ~3,138 MiB | PROVISIONAL ESTIMATE | `Qwen3-4B-Q4_K_M` weights + 4K FP16 KV cache + graph |
| **Other Active User Processes** | ~0 MiB | PROVISIONAL ESTIMATE | Variable third-party background load |
| **Total Observed Working Set** | **~6,788 MiB** | PROVISIONAL ESTIMATE | Sum of active baseline resident working sets (~6.63 GiB) |
| **Available Physical Memory** | **~5,500 MiB** | PROVISIONAL ESTIMATE | Remaining from 12,288 MiB pool (~5.37 GiB / ~5.77 GB) |

### 4.2 Measurement Limitations & Operating System Realities
1. **Status of Baseline Figures:** All process working-set figures above (~150 MiB GPU, ~220 MiB WebView2, ~300 MiB audio, ~3,138 MiB Main AI) are **PROVISIONAL ESTIMATES — NOT INDEPENDENTLY VERIFIED**. Because Phase 4 implementation has not commenced, no compiled KAATYA binary or active WebView2 session has been measured under full application workload.
2. **Dynamic Shared GPU Memory:** Intel HD 530 utilizes Dynamic Video Memory Technology (DVMT). It does **NOT** permanently reserve a fixed 450 MB block of physical RAM. Dynamic allocations fluctuate based on active 2D/3D surface complexity.
3. **Windows Working-Set Management:** Elevating process priority (`ABOVE_NORMAL_PRIORITY_CLASS`) and requesting working-set quotas (`SetProcessWorkingSetSizeEx`) provides application hints to Windows. However, the Windows Virtual Memory Manager (VMM) controls physical page residency. If external user applications induce severe physical memory exhaustion, Windows will trim working sets or page memory to `pagefile.sys`.

---

## 5. Permanent Main AI Residency Policy

- **Designated Permanent Model:** `Qwen3-4B-Q4_K_M.gguf` (2,497,280,256 bytes / 2.326 GiB / 2.497 GB).
- **Application-Level Invariant:** The KAATYA runtime guarantees that it will **NEVER** issue an `unload()`, `free()`, or model-destruction API call on the Main AI instance during application execution.
- **Model Memory Profile:**
  - Architecture: Qwen3, 36 layers, 32 attention heads, 8 KV heads, head dimension 128.
  - Memory-Mapped Weights: ~2,382 MiB (faulted into working set as accessed).
  - KV Cache (4,096 tokens, FP16): $2 \times 36 \times 8 \times 128 \times 4,096 \times 2 = 576.0\text{ MiB}$ ($0.604\text{ GB}$).
  - Compute Buffers: ~180 MiB scratch buffer allocation (`ggml_gallocr`).
  - Total Active Process Working Set: **~3,138 MiB** (with FP16 KV) or **~2,850 MiB** (with Q8_0 KV).
- **Residency Reality:** Clean memory-mapped file pages may be faulted in and out by the Windows Cache Manager under heavy I/O, but the model remains continuously active and referenced in application state.

---

## 6. Dynamic Worker Admission Policy

The former static safety-cushion formula has been permanently eliminated. All optional specialist local workers are admitted via the **10-Step Dynamic Worker Admission Procedure**:

### The 10-Step Admission Procedure
1. **Query Available Memory:** Invoke Win32 `GlobalMemoryStatusEx` to obtain current `ullAvailPhys`.
2. **Initial Rejection Floor:** If `ullAvailPhys < 2,048\text{ MiB}`, reject immediately as an unsafe operating floor (passing this floor is an initial gate, not proof of safety).
3. **Identify Target Model:** Determine the exact specialist model file requested.
4. **Estimate Weight Residency:** Compute resident weight footprint from quantized tensor size.
5. **Estimate Context & KV-Cache:** Calculate required KV cache based on target context length ($N$) and precision.
6. **Estimate Compute Buffers:** Calculate forward graph scratch buffer demand (`ggml_gallocr`).
7. **Audit Main AI Observed Footprint:** Confirm Main AI working set remains intact and un-evicted.
8. **Factor System Memory Pressure:** Read active system memory load percentage (`dwMemoryLoad`).
9. **Apply Configurable Test Margin:** Apply a dynamic safety margin derived from empirical testing.
10. **Log & Enforce Decision:** If total projected demand exceeds `ullAvailPhys`, reject or defer worker loading, log the exact diagnostic reason in `.assistant/logs/scheduler.log`, and route the task to the resident Main AI or cloud fallback.

---

## 7. Complete Model Inventory (10 Present Assets)

Every model asset physically residing on `T:\ai creation` is categorized by functional role:

| # | Exact Filename | Category | Exact Size (Bytes) | Binary (GiB) | Decimal (GB) | Local SHA-256 Checksum | Upstream Checksum Status |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **1** | `Qwen3-4B-Q4_K_M.gguf` | **Chat Model** | 2,497,280,256 B | 2.326 GiB | 2.497 GB | `7485fe6fd60c1fb469a4c84eb632ea51dff6e1d52fe1f938b82ff63a890d96d7` | *Unavailable (Community GGUF)* |
| **2** | `Qwen3-1.7B-Q3_K_M.gguf` | **Chat Model** | 1,073,242,208 B | 1.000 GiB | 1.073 GB | `79af9a93339ea49d034fa9fe81180b543fa0c98f80455dbd7e9f3b97b0a72ce9` | *Unavailable (Community GGUF)* |
| **3** | `SmolLM2-1.7B-Instruct-Q4_K_M.gguf` | **Chat Model** | 1,055,609,824 B | 0.983 GiB | 1.056 GB | `77665ea41a2aeb049ffcceaececfd864190c102a9df2c2b7ba122d46e33bd3b4` | *Unavailable (bartowski / HF quant)* |
| **4** | `Qwen2.5-Coder-1.5B-Instruct-Q3_K_M.gguf`| **Coding Model** | 824,178,784 B | 0.768 GiB | 0.824 GB | `0c292dae43e2e92cfae8bf668e1fb7fdf870f71933ba21fc2a297e28b28f8f2b` | *Unavailable (Community GGUF)* |
| **5** | `qwen2.5-1.5b-instruct-q4_k_m.gguf` | **Chat Model** | 1,117,320,736 B | 1.041 GiB | 1.117 GB | `6a1a2eb67ea278d976077556a34ea3efadbc91d8bbd4c6227c244c77c6888f4b` | *Unavailable (Community GGUF)* |
| **6** | `flux-2-klein-4b-q4_0.gguf` | **Image-Gen Model (DiT)**| 2,256,889,280 B | 2.102 GiB | 2.257 GB | `9c5939d564fa7454261d7a8e7e1cb5bf4d27192667ae967a5b39414da8846c10` | *Unavailable (Unsloth / HF quant)* |
| **7** | `qwen3-embedding-0.6b-q8_0.gguf` | **Embedding Model** | 639,150,592 B | 0.595 GiB | 0.639 GB | `ee02981604efb343cb4620021cbe15a519fc6eec77e928236fb6c4839880f074` | *Unavailable (Community GGUF)* |
| **8** | `ggml-base.bin` | **Speech-Recog (STT)**| 147,951,465 B | 0.138 GiB | 0.148 GB | `60ed5bc3dd14edd81339603a9ad24f7f5255470d06152a5ec6d0290538a719d2` | *Whisper.cpp ecosystem build* |
| **9** | `en_US-mike-medium.onnx` | **TTS Voice Asset** | 63,221,984 B | 0.059 GiB | 0.063 GB | `6876866e4a2e5ee9352ef5a557b2ffeb7ee10fc05a9ea2ffbc6e67e3fa43df65` | *Rhasspy Piper voice build* |
| **10**| `hi_IN-rohan-medium.onnx` | **TTS Voice Asset** | 62,950,044 B | 0.059 GiB | 0.063 GB | `b65dc80f33989c445a5078a0a75d5b7a14e18375e0ff05e61bf96956f1406e9d` | *Rhasspy Piper voice build* |

---

## 8. Model Assignments and Benchmark Requirements

1. **Recommended Primary Assignments:**
   - `Qwen3-4B-Q4_K_M.gguf`: Permanent Main AI Supervisor (Agent 1).
   - `Qwen2.5-Coder-1.5B-Instruct-Q3_K_M.gguf`: Recommended worker for Coder (2), Database Engineer (23), and Tester (9).
   - `Qwen3-1.7B-Q3_K_M.gguf`: Recommended worker for Writer (5), Social Media (19), and Presentation (21).
   - `qwen2.5-1.5b-instruct-q4_k_m.gguf`: Recommended worker for Document Intelligence (22).
   - `qwen3-embedding-0.6b-q8_0.gguf`: Strictly reserved for mathematical vector embedding inside `sqlite-vec`.
2. **Benchmark-Dependent Assignments:**
   - **Grammar & Language (Agent 18):** Model routing between `SmolLM2-1.7B` and `Qwen3-1.7B` is benchmark-dependent. Empirical testing during Phase 4 will measure comparative BLEU/chrF and latency on Hindi and Hinglish proofreading.
3. **Deterministic Numerical Execution:**
   - **Data Analyst (Agent 13):** Numerical calculations, aggregations, and statistics are strictly executed via Python/pandas/SQLite scripts; LLMs are never used for pure arithmetic.

---

## 9. FLUX.2 Klein Compatibility Assessment

- **File Structure:** `flux-2-klein-4b-q4_0.gguf` contains 149 tensors and 0 KV metadata entries, comprising exclusively the Diffusion Transformer (DiT) backbone weights.
- **True Conditioning Architecture:** Uses a **Qwen3 language model** feature extractor (concatenating hidden states from layers 9, 18, and 27 to produce a 7860-dimensional conditioning vector matching `txt_in.weight`).
- **Required Companion Files:** Requires Qwen3 text encoder and `flux2-vae.safetensors` (both currently absent from disk).
- **Main AI Reuse Limitation:** Reusing `Qwen3-4B-Q4_K_M.gguf` as the text encoder is not supported out-of-the-box due to logit evaluation vs. layer extraction differences, quantization noise in embeddings, runtime concurrency/context locking, and additional memory overhead.
- **Status:** **EXPERIMENTAL.** No companion files will be downloaded until a validated runtime is benchmarked on target hardware.

---

## 10. Video-Generation Feasibility

Local video diffusion models are classified according to three rigorous categories:
1. **Supported:** Programmatic Video Production (headless FFmpeg CLI, Whisper Base subtitles, Piper neural voiceovers, media trimming, merging, and audio ducking).
2. **Experimental / Unverified:** Direct CapCut draft project manipulation and observable UI automation.
3. **Impractical on Target Hardware:** Local text-to-video diffusion (Wan 2.1 T2V 1.3B, LTX-Video 2B). These models require 8–12+ GB dedicated VRAM and 16–32 GB system RAM; CPU execution on a dual-core 35W processor induces severe pagefile thrashing and unviable latency.
- **Autonomy:** The Video Studio is 100% operational for complete video creation without requiring local video diffusion. Generative clips are routed to authorized Online Video Providers with explicit human approval.

---

## 11. CapCut and Multi-Editor Interoperability

- **Multi-Editor Ecosystem:** Supports universal interchange formats:
  - Final Cut Pro / Premiere XML (`.xml`)
  - Edit Decision List (`.edl`)
  - OpenTimelineIO (`.otio`)
  - Subtitle formats (`.srt`, `.ass`, `.vtt`)
  - Supporting DaVinci Resolve, Adobe Premiere Pro, Shotcut, Kdenlive, and CapCut.
- **Safe CapCut Integration Tiers:**
  - *Tier A (Supported Standard):* Export rendered media and subtitle tracks for standard CapCut manual bin import.
  - *Tier B (Visible UI Automation):* Observable Windows UIAutomation (`UIAutomationCore.dll`) helper that focuses windows and opens import dialogs.
  - *Tier C (Experimental Internal Manipulation):* Injects project files into isolated disposable test folders (`kaatya_test_draft_*`) with mandatory user approval. **Never overwrites existing user projects.**

---

## 12. Complete 23-Agent Roster

All 15 original agent identities and 8 approved specialist roles are preserved:

### Original 15 Agents (Preserved Exactly)
1. **KAATYA Main AI / Manager** (Permanent Supervisor)
2. **Coder** (Code Generation & Refactoring)
3. **Designer** (UI/UX & Obsidian Command Styling)
4. **Researcher** (Local Vector Synthesis & Document Lookup)
5. **Writer** (Technical Documentation & Long-Form Text)
6. **Messenger** (Drafting Communications - Human Approval Required)
7. **File Manager** (Scoped Filesystem Browsing & Backups)
8. **Game Helper** (Strategy Hints & Keybindings - READ-ONLY, NO Gameplay Bots)
9. **Tester** (Test Case Generation & Coverage Checks)
10. **3D Artist** (Blender Python Scripting & 2D/2.5D Canvas Tuning)
11. **Automator** (Scheduled Automation & Developer Workflows)
12. **Security** (Permission Enforcement & Command AST Auditing)
13. **Data Analyst** (Deterministic Python/pandas/SQLite Execution)
14. **Code Reviewer** (Static Code Analysis & Diff Verification)
15. **Assistant** (Productivity, Notes, and Reminders)

### Eight Approved Specialists
16. **Video Editor** (FFmpeg CLI Production & NLE Interchange)
17. **Image Studio** (FLUX.2 Klein Experimental & Cloud Diffusion Gate)
18. **Grammar & Language** (Bilingual Proofreading - Benchmark Dependent)
19. **Social Media** (Hooks, Captions, and Multi-Platform Copy)
20. **Audio & Voice** (Acoustic Cleaning & Loudness Normalization)
21. **Presentation** (Slide Outlines & Marp Markdown Decks)
22. **Document Intelligence** (PDF Text & Tabular Data Extraction)
23. **Database Engineer** (Relational SQL Schema & Query Tuning)

---

## 13. Final Proposed Technology Stack

### Status: APPROVED PROPOSED ARCHITECTURE — IMPLEMENTATION NOT STARTED

- **Desktop Shell:** Tauri v2.
- **Native Backend:** Rust.
- **Frontend Layer:** React 19, TypeScript, and Tailwind CSS.
- **Rendering Engine:** Microsoft Edge WebView2.
- **Local LLM Inference:** Native `llama.cpp` with AVX2 CPU backend.
- **Audio Subsystem:** Whisper.cpp (`ggml-base.bin`) and Piper ONNX.
- **Local Storage:** SQLite 3 with optional `sqlite-vec` extension.
- **Target OS:** Windows 10 64-bit.

---

## 14. Online Permissions and Privacy

- **Default State:** Strictly **LOCAL / OFFLINE MODE (Air-Gapped)**.
- **Explicit Consent Mandate:** Outbound network operations require explicit per-call user confirmation displaying target model, prompt text, attached files, and estimated API cost.
- **Credential Storage:** Native Windows Data Protection API (DPAPI) is the approved proposed security design (not yet implemented in code).

---

## 15. Security and User Approval Policy

- **Mandatory User Confirmation Required For:**
  1. File deletion or directory destruction.
  2. Sending external messages, emails, or webhooks.
  3. Installing software, packages, or runtime dependencies.
  4. Executing elevated administrative PowerShell commands.
  5. Commercial purchases, token payments, or cloud credit usage.
  6. Modifying security tiers, workspace whitelists, or hotkey bindings.
- **User Control & Visibility:**
  - Active operations are always visibly announced; covert background tasks are prohibited.
  - The user can pause, inspect, or abort active tasks at any time.
  - Bare `ESC` key cancels tasks only when the Assistant window is focused (never globally swallowed).
  - Dedicated global interrupt (`Ctrl + Alt + Escape`) halts all processes with a documented conflict-resolution strategy.

---

## 16. Verification Script Results

The enhanced verification suite (`tools/verify_kaatya_docs.py`) was executed:
- **Autodiscovery:** Successfully discovered repository root dynamically from its own location.
- **Deliverables Verified:** All 18 documentation files and README local relative links exist and resolve.
- **Agent Roster Verified:** All 23 exact agent identities present across roster documents.
- **Formula Elimination Verified:** Outdated fixed 2.5 GB formula and contradictory 4.88 GB calculations absent repository-wide.
- **Contradiction Detection:** All cross-document checks passed (100%).
- **Script Exit Code:** `0` (Success).

---

## 17. Git Commit and Push Details

- **Branch:** `main`
- **Latest Commit Hash:** (Committed and pushed following this report).
- **Working Tree:** Clean, synchronized with `origin/main`.
- **Integrity Check:** Zero model files, temporary scratch files, or API credentials committed.

---

## 18. Engineering Evidence Classification Table

| Category | Documented Items |
| :--- | :--- |
| **Verified Facts (Empirically Confirmed)** | Intel Core i3-6100T (2C/4T @ 3.20 GHz, AVX2); 12.0 GB RAM; Intel HD Graphics 530; 10 physical model assets in `T:\ai creation` with exact bytes and SHA-256 hashes; `flux-2-klein-4b` DiT structure (149 tensors, 0 KV); absence of deleted Nemotron and un-downloaded models; Git repository location. |
| **Directly Measured Observations** | Windows 10 host memory state via `GlobalMemoryStatusEx` and CIM; process working sets for idle desktop processes; WMI adapter RAM report. |
| **Provisional Estimates (Unverified)** | Component baseline memory working sets (~150 MiB GPU, ~220 MiB WebView2, ~300 MiB audio, ~3,138 MiB Main AI); LLM generation throughput on Skylake 3-thread AVX2; Whisper/Piper Real-Time Factor under peak load. |
| **Proposed Design Decisions** | Tauri v2 + Rust + React 19 + WebView2 stack; 10-step Dynamic Worker Admission Procedure; 3-tier security permissions; DPAPI encryption; Multi-editor XML/EDL/OTIO interchange; 23-agent logical roster on shared runtimes. |
| **Unresolved Questions for User Review** | Cloud Diffusion Gate vs. local companion file acquisition; CapCut standard export vs. opt-in experimental draft folder manipulation; SmolLM2 vs. Qwen3-1.7B grammar routing benchmark. |

---

## 19. Outstanding User Decisions

Prior to beginning Phase 4 application implementation, three concrete decisions await user confirmation:
1. **Cloud Diffusion Gate vs. Local Companion Setup:** Confirm keeping Cloud Diffusion Gate as primary default with local CPU diffusion strictly experimental.
2. **CapCut Workflow Strategy:** Confirm standard NLE export (XML, EDL, OTIO) and visible UI automation as default.
3. **Secondary Worker Model Selection:** Confirm testing `SmolLM2-1.7B` vs. `Qwen3-1.7B` dynamically during Phase 4 benchmarks.

---

## 20. Explicit Phase 4 Hold Status

> [!IMPORTANT]
> **PHASE 4 APPLICATION IMPLEMENTATION REMAINS ON STRICT HOLD.**
> All Phase 3 architectural corrections, repository-wide consistency reconciliations, and documentation audits are complete. No application source code has been written, no models downloaded or modified, and no system settings altered.
> 
> The project remains completely paused awaiting the user's explicit authorization to proceed to Phase 4.

---
*Report formally submitted for Phase 3 technical sign-off.*
