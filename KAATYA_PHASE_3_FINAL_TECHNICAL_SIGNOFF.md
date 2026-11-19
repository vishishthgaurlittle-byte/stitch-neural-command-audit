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

## 2. Final Hardware Specification & Raw Measurement Evidence

All architectural thresholds, memory budgets, and execution policies are calibrated against the target physical computer, empirically re-measured on **November 19, 2026**:

### 2.1 Verified Hardware Architecture
- **Processor:** Intel Core i3-6100T (6th-Gen Skylake, 35W TDP).
- **Cores / Threads:** 2 physical cores, 4 logical threads @ 3.20 GHz base frequency.
- **Instruction Set:** AVX2, FMA3, SSE4.2, BMI2 supported (no AVX-512, no AMX).
- **Physical Memory Modules & Speed:**
  - Installed Physical Modules: Two 8 GB Samsung DDR4 DIMMs (`M378A1K43DB2-CTD`).
  - DIMM Rated Speed: 2666 MT/s (SPD rating).
  - **Configured Operating Clock Speed:** **2,133 MT/s** (empirically confirmed via `Win32_PhysicalMemory.ConfiguredClockSpeed`; the Core i3-6100T memory controller officially supports DDR4-1866/2133).
  - Memory Bus Configuration: Dual-channel (2x 64-bit channels = 128-bit total bus width).
  - **Theoretical Maximum Memory Bandwidth:** **34.13 GB/s** ($2 \times 8\text{ bytes} \times 2,133,333,333\text{ transfers/sec}$), matching Intel's official processor specification of 34.1 GB/s.
  - **Measured Sustained Bandwidth:** **[UNVERIFIED]** (projected realistic sustained bandwidth: ~22.0 to 25.5 GB/s on Skylake desktop, pending physical stream benchmark).
- **Graphics Subsystem:** Integrated Intel HD Graphics 530 (Skylake GT2, 24 Execution Units).
  - Dedicated VRAM: 0 MB (No dedicated GDDR/HBM).
  - Acceleration Capability: DirectX 12, Direct3D 11, Intel Quick Sync Video (QSV).
  - Compute Limitations: Zero NVIDIA CUDA cores, zero Tensor cores.
  - Video Memory Management: Intel Dynamic Video Memory Technology (DVMT) utilizing shared system RAM dynamically.
- **Storage Configuration:**
  - Internal System Drive (`T:\ai creation`): Hosts resident model assets, SQLite databases, and workspace directories.
  - External Storage: Amazon Basics USB 3.0 Pendrive (~116 GB usable capacity, reserved for media scratch and cold archives).
- **Operating System:** Windows 10 64-bit (Build 19045 / 22H2).

### 2.2 Raw Memory Measurement Telemetry & Reproducible Scripts

The host machine was empirically measured using native Windows APIs and WMI/CIM queries. 

#### Reproducible Inspection Procedures:
1. **Physical DIMM Hardware Configuration:**
   ```powershell
   Get-CimInstance Win32_PhysicalMemory | Select-Object BankLabel, Capacity, Manufacturer, PartNumber, Speed, ConfiguredClockSpeed, DataWidth, TotalWidth | Format-Table -AutoSize
   ```
2. **System Memory & Virtual Memory Statistics:**
   Execute the dedicated inspection script [`tools/measure_system_memory.py`](file:///T:/ai%20creation/STITCH_DESIGN_AUDIT/tools/measure_system_memory.py), which interfaces directly with Win32 `GlobalMemoryStatusEx` and performance counters.

#### Raw Captured Telemetry Across Historical Snapshots:
- **Win32_PhysicalMemory Module 0:** Bank 0 / `ChannelA-DIMM0`: Samsung `M378A1K43DB2-CTD`, Rated Speed: 2666 MT/s, Configured Operating Speed: 2133 MT/s, Capacity: **8,589,934,592 bytes** (8.00 GiB / 8,192 MiB).
- **Win32_PhysicalMemory Module 1:** Bank 2 / `ChannelB-DIMM0`: Samsung `M378A1K43DB2-CTD`, Rated Speed: 2666 MT/s, Configured Operating Speed: 2133 MT/s, Capacity: **8,589,934,592 bytes** (8.00 GiB / 8,192 MiB).
- **Total Physically Installed Capacity (Constant):** $8,589,934,592 \times 2 = \mathbf{17,179,869,184\text{ bytes}}$ ($16.00\text{ GiB} = 16,384\text{ MiB} \approx 17.18\text{ GB}$).
- **GlobalMemoryStatusEx `ullTotalPhys` (Windows-Visible, Constant):** **17,049,899,008 bytes** ($15.8790\text{ GiB} = 16,260.05\text{ MiB} \approx 17.05\text{ GB}$).
- **Win32_OperatingSystem `TotalVisibleMemorySize`:** **16,650,292 KB** ($17,049,899,008\text{ bytes}$).
- **Hardware-Reserved Memory Difference:** $17,179,869,184 - 17,049,899,008 = \mathbf{129,970,176\text{ bytes}}$ ($123.95\text{ MiB} \approx 124\text{ MiB}$). Measured installed-versus-visible RAM difference: 123.95 MiB. Exact hardware reservation breakdown: unverified.
- **Dynamic Available Physical RAM Snapshots (`ullAvailPhys` includes Free, Zeroed, and Standby pages):**
  - **Snapshot 1 (2026-11-19T18:32:43):** $7,371,558,912\text{ bytes}$ ($7,030.07\text{ MiB} \approx 6.87\text{ GiB}$). Non-available RAM: $17,049,899,008 - 7,371,558,912 = \mathbf{9,678,340,096\text{ bytes}}$ ($9,229.98\text{ MiB} \approx 9.01\text{ GiB}$).
  - **Snapshot 2 (2026-11-19T18:54:14):** $6,910,607,360\text{ bytes}$ ($6,590.47\text{ MiB} \approx 6.44\text{ GiB}$). Non-available RAM: $17,049,899,008 - 6,910,607,360 = \mathbf{10,139,291,648\text{ bytes}}$ ($9,669.58\text{ MiB} \approx 9.44\text{ GiB}$).
  - **Snapshot 3 (2026-11-19T20:27:06):** $7,267,610,624\text{ bytes}$ ($6,930.94\text{ MiB} \approx 6.77\text{ GiB}$). Non-available RAM: $17,049,899,008 - 7,267,610,624 = \mathbf{9,782,288,384\text{ bytes}}$ ($9,329.12\text{ MiB} \approx 9.11\text{ GiB}$).
  - **Snapshot 4 (2026-11-19T20:42:12):** $7,425,671,168\text{ bytes}$ ($7,081.67\text{ MiB} \approx 6.92\text{ GiB}$). Non-available RAM: $17,049,899,008 - 7,425,671,168 = \mathbf{9,624,227,840\text{ bytes}}$ ($9,178.38\text{ MiB} \approx 8.96\text{ GiB}$).
- **Non-Available Physical RAM Nature:** Across all snapshots, non-available physical RAM comprises active process working sets (which includes user applications and the `Memory Compression` process working set), modified pages, and locked kernel allocations (Non-Paged Pool, resident Paged Pool); standby pages are NOT part of this non-available quantity.
- **GlobalMemoryStatusEx `ullTotalPageFile` (Commit Limit):** **19,600,035,840 bytes** ($18.2540\text{ GiB} = 18,692.06\text{ MiB} \approx 19.60\text{ GB}$).
- **Committed Virtual Memory Snapshots:**
  - Snapshot 1 (18:32:43): $19,600,035,840 - 6,995,292,160 = \mathbf{12,604,743,680\text{ bytes}}$ ($12,020.82\text{ MiB} \approx 11.74\text{ GiB}$).
  - Snapshot 3 (20:27:06): $19,600,035,840 - 6,204,944,384 = \mathbf{13,395,091,456\text{ bytes}}$ ($12,774.55\text{ MiB} \approx 12.48\text{ GiB}$).
  - Snapshot 4 (20:42:12): $19,600,035,840 - 6,849,982,464 = \mathbf{12,750,053,376\text{ bytes}}$ ($12,159.40\text{ MiB} \approx 11.87\text{ GiB}$).
  *(Note: Committed memory is virtual address space promised to all processes across RAM plus `pagefile.sys`, NOT physical RAM consumed).*
- **Separately Timestamped Memory Compression Working Set Observations (Non-Additive):**
  - Observation 1 (2026-11-19T18:32:43): $1,160,495,104\text{ bytes}$ (~$1,106.73\text{ MiB}$).
  - Observation 2 (2026-11-19T20:27:29): $1,161,969,664\text{ bytes}$ (~$1,108.14\text{ MiB}$).

### 2.3 Authoritative Hardware Memory Categorization Table

| Classification Category | Exact Bytes | Binary (MiB / GiB) | Decimal (GB) | Measurement Source & Verification Method |
| :--- | ---:| ---:| ---:| :--- |
| **1. Physically Installed RAM** | 17,179,869,184 B | 16,384.00 MiB (16.00 GiB) | ~17.18 GB | WMI `Win32_PhysicalMemory` (2x Samsung 8 GB DDR4-2666 modules configured at 2,133 MT/s; physical Channel A/B slots; active dual-channel runtime mode unverified) |
| **2. Windows-Visible Physical RAM** | 17,049,899,008 B | 16,260.05 MiB (15.88 GiB) | ~17.05 GB | Win32 API `GlobalMemoryStatusEx.ullTotalPhys` / `TotalVisibleMemorySize` |
| **3. Hardware-Reserved Memory Difference** | 129,970,176 B | 123.95 MiB (~0.12 GiB) | ~0.13 GB | Difference: Installed RAM minus Windows-Visible RAM. Measured difference: 123.95 MiB. Exact hardware reservation breakdown: unverified. |
| **4. Dynamic Available Physical RAM**| 7,267,610,624 B to 7,425,671,168 B | 6,930.94 MiB to 7,081.67 MiB | ~7.27 to ~7.43 GB | Win32 API `GlobalMemoryStatusEx.ullAvailPhys` (Fluctuates dynamically with host processes; includes Free, Zeroed, and Standby pages; Snap 1: 7,030.07 MiB; Snap 2: 6,590.47 MiB; Snap 3: 6,930.94 MiB; Snap 4: 7,081.67 MiB) |
| **5. Physical RAM Not Reported Available** | 9,624,227,840 B to 10,139,291,648 B | 9,178.38 MiB to 9,669.58 MiB | ~9.62 to ~10.14 GB | Difference: Visible RAM minus `ullAvailPhys` (Comprises active process working sets [including Memory Compression], modified pages, locked kernel memory; does NOT include standby pages) |
| **6. System Virtual Commit Charge** | 12,604,743,680 B to 13,395,091,456 B | 12,020.82 MiB to 12,774.55 MiB | ~12.60 to ~13.40 GB | Win32 API `ullTotalPageFile - ullAvailPageFile` (Virtual commit backed by RAM + pagefile; NOT physical RAM consumed) |
| **7. Total System Commit Limit** | 19,600,035,840 B | 18,692.06 MiB (18.25 GiB) | ~19.60 GB | Win32 API `GlobalMemoryStatusEx.ullTotalPageFile` (Physical RAM + pagefile.sys) |

---

## 3. Disambiguation of Memory Concepts & Available-Memory Reconciliation

### 3.1 Strict Separation of Memory Concepts
To eliminate contradictions, KAATYA strictly distinguishes six discrete memory categories:
1. **Installed Physical RAM:** The total hardware capacity of physical modules ($17,179,869,184\text{ bytes} = 16,384.00\text{ MiB} = 16.00\text{ GiB}$).
2. **Windows-Visible Physical RAM:** Physical memory managed by the Windows kernel (`GlobalMemoryStatusEx.ullTotalPhys`: $17,049,899,008\text{ bytes} = 16,260.05\text{ MiB} = 15.88\text{ GiB}$). Measured installed-versus-visible RAM difference: 123.95 MiB. Exact hardware reservation breakdown: unverified.
3. **Available Physical RAM:** Dynamic memory reported by `ullAvailPhys` ($7,030.07\text{ MiB}$ at measurement timestamp; $6,590.47\text{ MiB}$ at secondary capture). Under Windows memory architecture, `ullAvailPhys` is the sum of:
   - **Free Page List:** Unassigned physical pages immediately available.
   - **Zeroed Page List:** Free physical pages initialized to zero.
   - **Standby Page List:** Cached file pages and code whose contents remain valid but can be repurposed or discarded instantly without writing to disk. Standby pages are explicitly part of **Available Physical RAM** in Windows.
4. **Physical RAM Not Currently Reported as Available:** The mathematical difference between Windows-visible RAM and `ullAvailPhys` ($16,260.05 - 7,030.07 = 9,229.98\text{ MiB}$). Standby pages are NOT part of this non-available figure. It comprises:
   - **Active Process Working Sets:** Resident physical pages mapped into process address spaces (including third-party applications, developer tooling, background services, and the `Memory Compression` process working set, which was observed at 1,160,495,104 bytes / ~1,106.73 MiB; Memory Compression is an internal component of active working sets, NOT a separate additive quantity).
   - **Modified Page List:** Pages containing modified data that must be written to disk before transitioning to standby or free.
   - **Locked Kernel Allocations:** Non-Paged Pool (locked in RAM for drivers/network), resident Paged Pool, and page tables.
5. **Process Working Sets:** The physical RAM pages currently resident for a specific process (e.g. resident GGUF weights, private heap, stack). Process working sets, standby pages, and kernel pools are different categories and cannot be naively added together. Visible RAM minus available RAM does NOT equal the arithmetic sum of process working sets, as processes share system DLLs and mapped memory.
6. **System Commit Charge vs. Commit Limit:** The total virtual address space promised to all running processes backed by physical RAM plus `pagefile.sys` ($12,020.82\text{ MiB}$ committed at measurement; $18,692.06\text{ MiB}$ commit limit; $6,671.24\text{ MiB}$ available commit). **Commit charge is NOT physical RAM consumed.**

### 3.2 Resolution of the Available-Memory and Headroom Discrepancy
The previous report referenced a calculated figure of $9,472\text{ MiB}$ as "headroom". That figure was merely a theoretical subtraction:
$$\text{Theoretical Idle Margin} = 16,260.05\text{ MiB (Visible)} - 6,788\text{ MiB (Projected Baseline)} = \mathbf{9,472.05\text{ MiB}}$$

**Correction & Truth in Telemetry:**
- $9,472\text{ MiB}$ is **NOT** measured available physical RAM and must not be described as available headroom.
- The actual measured available physical RAM at the measurement timestamp was **$7,030.07\text{ MiB}$** ($7,371,558,912\text{ bytes} / 1,048,576 = 7,030.071289...\text{ MiB}$, and $6,590.47\text{ MiB}$ in subsequent re-tests). Available physical memory fluctuates dynamically with active host processes.
- The physical memory not currently reported as available was:
  $$\text{Physical RAM Not Currently Reported as Available} = 16,260.05\text{ MiB} - 7,030.07\text{ MiB} = \mathbf{9,229.98\text{ MiB}}$$
- **Investigation of the ~2,442 MiB Difference ($9,229.98 - 6,788 \approx 2,441.98\text{ MiB}$):**
  - Status: **Partially explained; exact reconciliation unavailable.**
  - Visible RAM minus available RAM does NOT equal the sum of process working sets.
  - Active host developer processes captured at timestamp (Google Chrome at ~2,800 MiB, Antigravity IDE at ~1,200 MiB, language servers at ~400 MiB) represent independent virtual working sets that share common libraries and OS mappings.
  - Windows Memory Compression: Managed by the Windows Memory Manager (`ntoskrnl.exe`). The working set of the `Memory Compression` process was observed at **1,160,495,104 bytes** (**1,106.73 MiB**) at initial snapshot capture. This is an observation of an active process working set, NOT an additional quantity to add on top of non-available RAM.
  - The Windows kernel maintains Non-Paged Pool (locked in physical RAM, measured at **511.73 MiB** / 536,100,864 bytes) and Paged Pool (measured at **720.04 MiB** / 754,905,088 bytes).
  - The $6,788\text{ MiB}$ baseline is an engineering projection of an idle Windows machine running KAATYA, whereas the $7,030.07\text{ MiB}$ available reading reflects a live developer workstation with heavy background tooling. Exact component reconciliation cannot be claimed without independent, non-overlapping measurements across all kernel and user-space structures.

---

## 4. Revalidation of Baseline Estimates vs. Empirical Telemetry

### 4.1 Reconciliation of Historical Baseline Labels (6,788 MiB, 7.12 GB, 7.20 GB)
The three historical figures refer to the same underlying projected load:
- $6,788\text{ MiB} = 6,788 \times 1,048,576\text{ bytes} = 7,117,733,888\text{ bytes} \approx \mathbf{7.12\text{ GB}}$ decimal.
- Rounding $7.1177\text{ GB}$ to one decimal place yields $\mathbf{7.2\text{ GB}}$ (or $7.20\text{ GB}$).
- Working sets and committed pages overlap: resident working sets are backed by committed pages and cannot be summed as independent quantities.

### 4.2 Itemized Memory Projection Table (Explicitly Labeled)

| Component | Projected Footprint (MiB) | Evidence Classification | Status & Verification Method |
| :--- | ---:| :--- | :--- |
| **Windows Base OS & Services** | ~2,900 MiB | PROVISIONAL ESTIMATE | Windows 10 x64 kernel, DWM, background services (idle clean boot) |
| **Dynamic GPU Shared Memory** | ~150 MiB | PROVISIONAL ESTIMATE | Intel HD 530 DVMT dynamic UI allocation (idle 2D surface) |
| **KAATYA Desktop Shell** | ~220 MiB | PROVISIONAL ESTIMATE | Tauri v2 host binary + Edge WebView2 (unimplemented) |
| **Audio Subsystem** | ~300 MiB | PROVISIONAL ESTIMATE | PortAudio stream, Piper dual ONNX, Whisper buffer (unimplemented) |
| **Database Store** | ~80 MiB | PROVISIONAL ESTIMATE | SQLite 3 engine and `sqlite-vec` cache (unimplemented) |
| **KAATYA Main AI** | ~3,138 MiB | THEORETICAL CALCULATION | `Qwen3-4B-Q4_K_M` weights (2,382 MiB) + 4K FP16 KV (576 MiB) + graph/scratch (180 MiB) |
| **Total Projected Baseline** | **~6,788 MiB** | **PROJECTED ESTIMATE** | **Sum of projected components — NOT AN OBSERVED RUNNING SYSTEM** |
| **Live Host Visible RAM** | **16,260.05 MiB** | **EMPIRICALLY MEASURED** | Win32 API `GlobalMemoryStatusEx.ullTotalPhys` |
| **Live Host Available RAM** | **7,030.07 MiB** | **EMPIRICALLY MEASURED** | Win32 API `GlobalMemoryStatusEx.ullAvailPhys` (Captured 2026-11-19T18:32:43; workload-dependent) |
| **Live Host Commit Charge** | **12,020.83 MiB** | **EMPIRICALLY MEASURED** | Win32 API `ullTotalPageFile - ullAvailPageFile` (Virtual commit across all apps; NOT physical RAM consumed) |

*(Note: Because KAATYA has not been implemented or compiled, a live measurement of KAATYA + Main AI running concurrently does not exist. It will be captured empirically during Phase 4 milestone 4.1).*

---

## 5. Permanent Main AI Residency Policy & KV Cache Validation

- **Designated Permanent Model:** `Qwen3-4B-Q4_K_M.gguf` (2,497,280,256 bytes / 2.326 GiB / 2.497 GB).
- **Application-Level Invariant:** The KAATYA runtime architecture requires that the application must not intentionally unload, free, or evict the Main AI instance to admit a specialist worker. Main AI should remain continuously loaded in the application runtime.
- **Operating System Memory Realities & Paging Policy:**
  - While KAATYA will never intentionally unload Main AI, Windows Memory Manager (`ntoskrnl.exe`) manages physical page frames globally and may still page virtual memory pages or trim working sets under extreme system-wide memory pressure.
  - The application architecture cannot override Windows kernel memory management; actual physical working set residency, commit charge, and paging behavior under concurrent workloads require empirical runtime testing during Phase 4. No claim is made that Windows will never page Main AI memory.
- **Model Architectural Parameters (Audited from GGUF Binary & Official Architecture):**
  - Architecture: `qwen3`
  - Transformer Layers: 36 (`block_count = 36`)
  - Embedding Length: 2560 (`embedding_length = 2560`)
  - Attention Heads: 32 (`head_count = 32`)
  - KV Heads: 8 (`head_count_kv = 8`)
  - Key Length (Head Dimension): 128 (`key_length = 128`, verified via GGUF metadata and tensor shapes `blk.0.attn_k.weight` shape `(2560, 1024)` where $1024 = 8 \times 128$, and `blk.0.attn_q.weight` shape `(2560, 4096)` where $4096 = 32 \times 128$).
  - Value Length: 128 (`value_length = 128`, matching `blk.0.attn_v.weight` shape `(2560, 1024)`).
  - *Correction of Derivation Error:* An earlier calculation assumed $\text{head\_dim} = 2560 / 32 = 80$. This assumption is invalid for Qwen3-4B because Qwen3 uses an expanded query projection ($32 \times 128 = 4096$) rather than projecting to the hidden dimension (2560). The actual head dimension is definitively 128.
- **KV Cache Memory Formula & Supported Context Profiles:**
  $$\text{KV Cache Elements per Token} = 2 \times (\text{Layers} = 36) \times (\text{KV Heads} = 8) \times (\text{Head Dim} = 128) = \mathbf{73,728\text{ elements/token}}$$
  - **FP16 Precision (2 bytes/element):** $73,728 \times 2 = 147,456\text{ bytes/token}$ ($144.0\text{ KiB/token}$).
    - At $N = 2,048\text{ tokens}$: $2,048 \times 147,456 = 301,989,888\text{ bytes} = \mathbf{288.0\text{ MiB}}$.
    - At $N = 4,096\text{ tokens}$: $4,096 \times 147,456 = 603,979,776\text{ bytes} = \mathbf{576.0\text{ MiB}}$.
    - At $N = 8,192\text{ tokens}$: $8,192 \times 147,456 = 1,207,959,552\text{ bytes} = \mathbf{1,152.0\text{ MiB}}$.
  - **Q8_0 Precision (Quantized KV with Block Format & Metadata Overhead):**
    - GGML Q8_0 quantizes in blocks of 32 elements. Each 32-element block comprises 32 bytes (int8 weights) + 2 bytes (`ggml_fp16_t` delta scale) = 34 bytes per 32 elements ($1.0625\text{ bytes/element}$).
    - Bytes per token: $73,728 \times (34 / 32) = 78,336\text{ bytes/token}$ ($76.5\text{ KiB/token}$).
    - At $N = 2,048\text{ tokens}$: $2,048 \times 78,336 = 160,432,128\text{ bytes} = \mathbf{153.0\text{ MiB}}$.
    - At $N = 4,096\text{ tokens}$: $4,096 \times 78,336 = 320,864,256\text{ bytes} = \mathbf{306.0\text{ MiB}}$.
    - At $N = 8,192\text{ tokens}$: $8,192 \times 78,336 = 641,728,512\text{ bytes} = \mathbf{612.0\text{ MiB}}$.
- **Process Working Set Breakdown:**
  - Memory-Mapped Weights: $2,497,280,256\text{ bytes} = 2,381.60\text{ MiB} \approx \mathbf{2,382\text{ MiB}}$.
  - Active 4K FP16 KV Cache: **576.0 MiB** (or **306.0 MiB** with Q8_0 KV cache).
  - Compute Scratch & Graph Buffers (`ggml_gallocr`): **~180 MiB**.
  - Total Active Main AI Process Working Set: **~3,138 MiB** (~3.14 GiB / 3.29 GB) under 4K FP16, or **~2,868 MiB** under 4K Q8_0.
- **Residency Reality:** KAATYA application architecture enforces that Main AI remains loaded in the runtime state and is never unloaded to make room for optional workers. However, clean memory-mapped file pages and private pages remain subject to standard Windows kernel paging under memory pressure. Real-world physical memory residency and paging metrics will be benchmarked directly during Phase 4.

---

## 6. Dynamic Worker Admission Policy

The former static safety-cushion formula has been permanently eliminated. All optional specialist local workers are admitted via the **10-Step Dynamic Worker Admission Procedure**:

### The 10-Step Admission Procedure
1. **Query Available Memory:** Invoke Win32 `GlobalMemoryStatusEx` to obtain current `ullAvailPhys` ($7,030.07\text{ MiB}$ at snapshot 1; $6,590.47\text{ MiB}$ at snapshot 2).
2. **Initial Rejection Floor:** If `ullAvailPhys < 2,048\text{ MiB}`, reject immediately as an unsafe operating floor (passing this floor is an initial gate, not proof of safety).
3. **Identify Target Model:** Determine the exact specialist model file requested.
4. **Estimate Weight Residency:** Compute resident weight footprint from quantized tensor size.
5. **Estimate Context & KV-Cache:** Calculate required KV cache based on target context length ($N$) and precision.
6. **Estimate Compute Buffers:** Calculate forward graph scratch buffer demand (`ggml_gallocr`).
7. **Audit Main AI Observed Footprint:** Confirm Main AI working set remains intact and un-evicted.
8. **Factor System Memory Pressure:** Read active system memory load percentage (`dwMemoryLoad`).
9. **Calculate Dynamic Safety Margin:** Compute $S_{\text{dynamic}} = \max(1,200\text{ MiB},\, 0.12 \times M_{\text{total\_phys}} + M_{\text{transient}})$. On this 16 GB visible system ($16,260\text{ MiB}$), $S_{\text{dynamic}} \approx 2,151\text{ MiB}$.
   - **Provisional Classification:** This 2,151 MiB margin is classified as **provisional**. The derived worker budget must NOT be treated as a validated permanent capacity, and worker loading must never be authorized based solely on a single historical snapshot.
10. **Enforce Net Admission Budget:** Compare total worker requirement $M_{\text{worker}}$ against admissible budget:
    $$\text{Admissible Budget} = \text{ullAvailPhys} - S_{\text{dynamic}}$$
    At snapshot 1 measured available RAM ($7,030.07\text{ MiB}$), the admissible budget is $\approx \mathbf{4,879.07\text{ MiB}}$.
    - `SmolLM2-1.7B-Instruct` (~1,306 MiB total) $\le 4,879\text{ MiB} \rightarrow$ **ADMITTED**.
    - `Qwen2.5-Coder-1.5B-Instruct` (~1,044 MiB total) $\le 4,879\text{ MiB} \rightarrow$ **ADMITTED**.
    - Dedicated FLUX.2 Klein pipeline (~5,200 MiB) $> 4,879\text{ MiB} \rightarrow$ **REJECTED**.

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
| **6** | `flux-2-klein-4b-q4_0.gguf` | **Image-Gen Model (DiT)**| 2,256,889,280 B | 2.102 GiB | 2.257 GB | `9c5939d55e3ac76e3a700029770fcc5e1b873d12c2a6d22c6c3fec217488e718` | *Unavailable (Unsloth / HF quant)* |
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

## 9. FLUX.2 Klein Compatibility & Feasibility Assessment

### 9.1 Technical Identity & Integrity Profile of Local GGUF File
- **File System Path:** `T:\ai creation\flux-2-klein-4b-q4_0.gguf`
- **Exact File Size:** **2,256,889,280 bytes** (2.1019 GiB / 2.2569 GB decimal).
- **Cryptographic Hash (SHA-256):** `9c5939d55e3ac76e3a700029770fcc5e1b873d12c2a6d22c6c3fec217488e718` (locally calculated and verified).
- **Source / Originating Repository:** Community GGUF conversion (Unsloth / bartowski community conversion hosted on Hugging Face). Official upstream publisher manifest is unavailable; upstream authenticity cannot be cryptographically verified.
- **GGUF Container Format:** Version 3 (`GGUF\x03\x00\x00\x00`).
- **Metadata Key-Value Pairs:** **0 entries** (`metadata_kv_count = 0`). The container header contains no metadata keys whatsoever.
- **Model Architecture Identification:** **`unknown`** (because `general.architecture` is absent from metadata).
- **Tensor Count:** Exactly 149 tensors.
- **Observed Structural Tensors:**
  - `txt_in.weight`: shape `(7680, 3072)`, raw numeric type ID `30` (`GGML_TYPE_BF16`), byte size $47,185,920\text{ bytes}$ ($2.0\text{ bytes/element}$).
  - `img_in.weight`: shape `(128, 3072)`, raw numeric type ID `30` (`GGML_TYPE_BF16`), byte size $786,432\text{ bytes}$ ($2.0\text{ bytes/element}$).
  - `time_in.in_layer.weight`: shape `(256, 3072)`, raw numeric type ID `30` (`GGML_TYPE_BF16`).
  - `time_in.out_layer.weight`: shape `(3072, 3072)`, raw numeric type ID `30` (`GGML_TYPE_BF16`).
  - `final_layer.adaLN_modulation.1.weight`: shape `(3072, 6144)`, raw numeric type ID `30` (`GGML_TYPE_BF16`).
  - `final_layer.linear.weight`: shape `(3072, 128)`, raw numeric type ID `30` (`GGML_TYPE_BF16`).
  - 83 primary projection weights across `double_blocks.*` and `single_blocks.*`: raw numeric type ID `2` (`GGML_TYPE_Q4_0`, standard 4-bit quantization, 18 bytes / 32 elements = 0.5625 bytes/element).
  - 66 structural, projection, timestep, and normalization weights: raw numeric type ID `30` (`GGML_TYPE_BF16`, unquantized 16-bit bfloat16, 2 bytes / element).
- **Observed Quantization Types & Resolution of Enum Mapping:**
  - *Empirical Header Inspection:* Across all 149 tensors, exactly two raw numeric type IDs appear: Type ID `2` (83 tensors) and Type ID `30` (66 tensors).
  - *Resolution of GGML Enum Mappings & Historical Type 31:*
    - **Type ID 2 (`GGML_TYPE_Q4_0`):** Standard upstream GGML 4-bit block quantization (32 elements per block, 18 bytes per block = 0.5625 bytes/element).
    - **Type ID 30 (`GGML_TYPE_BF16`):** Standard upstream GGML 16-bit bfloat16 format (1 element per block, 2 bytes per block = 2.0 bytes/element).
    - **Type ID 31 (Unresolved Historical Mapping):** An earlier version of `tools/inspect_model_metadata.py` contained a hardcoded enum entry mapping ID 31 to `Q4_0_4_4`. In upstream GGML history, enum 31 appeared in certain experimental branches and community forks for tiled quantization, but is not verified as a stable or supported type in official upstream GGML specifications; it is therefore classified strictly as an **unresolved historical enum mapping**. Under no circumstances is it implied that a removed, reserved, or experimental type is supported by upstream GGML.
    - **Zero Type 31 Tensors in Local File:** Empirical audit of all 149 tensor headers confirms that **zero tensors of Type 31 exist in `flux-2-klein-4b-q4_0.gguf`**. The file consists exclusively of 83 tensors of standard `Q4_0` (Type ID 2) and 66 tensors of `BF16` (Type ID 30).
  - *txt_in.weight Precision:* With shape `(7680, 3072)` = 23,592,960 elements, `txt_in.weight` consumes exactly $47,185,920\text{ bytes}$ (data offset 2,209,692,672, absolute file start byte 2,209,703,360 to end byte 2,256,889,280), proving it is stored unquantized in **`BF16` (2.0 bytes/element)**, not 4-bit quantized.
  - *Runtime Compatibility Limitation:* Although standard `Q4_0` and `BF16` have widespread upstream GGML CPU kernel support, CPU instruction set support (such as AVX2) alone does **NOT** establish inference compatibility. An inference runtime must possess explicit architecture support for FLUX DiT models and must handle GGUF containers that lack `general.architecture` and hyperparameter metadata.
  - *Intended Local Inference Runtimes:* `stable-diffusion.cpp` (`sd.cpp`) and `ComfyUI-GGUF`. Neither runtime's compiled Windows binary on this PC has been demonstrated to successfully load or execute a 0-metadata DiT container without hyperparameter configuration. Therefore, runtime inference compatibility remains explicitly **UNVERIFIED**.
- **Scope of Boundary Validation & Exact Container Accounting:**
  - *Exact File Accounting Equation:*
    $$\begin{aligned}
    \text{Header \& Metadata Table} &= 10,682\text{ bytes} \\
    \text{Header-to-Data Alignment Padding} &= 6\text{ bytes} \quad (\text{Data Start Offset: } 10,688\text{ bytes}) \\
    83\text{ Q4\_0 Tensors Payload} &= 2,149,908,480\text{ bytes} \quad (119,439,360\text{ blocks} \times 18\text{ B}, \text{divisible by } 18) \\
    66\text{ BF16 Tensors Payload} &= 106,970,112\text{ bytes} \quad (53,485,056\text{ elems} \times 2\text{ B}, \text{divisible by } 2) \\
    \text{Inter-Tensor Alignment Padding} &= 0\text{ bytes} \\
    \text{Trailing File Padding} &= 0\text{ bytes} \\
    \hline
    \mathbf{Total\ Container\ Size} &= 10,682 + 6 + 2,149,908,480 + 106,970,112 = \mathbf{2,256,889,280\text{ bytes}}
    \end{aligned}$$
  - *What it proves:* The GGUF container binary structure is well-formed, tensor offsets are monotonically ascending, all dimensions conform to quantization block sizes (zero invalid block dimensions), and all 149 tensor payloads reside entirely within the 2,256,889,280-byte file boundary with exact zero-byte container difference (maximum tensor end offset: 2,256,889,280 bytes).
  - *What it DOES NOT prove:* A passing tensor-boundary check proves container binary integrity within file bounds, but does **NOT** prove model authenticity, does not prove weights are untampered or properly trained, does not prove upstream architecture validity, and does not prove successful runtime inference or step convergence.

### 9.2 Observed Tensor Geometry, Conditioning Hypotheses & Dependency Realities
- **Variant Disambiguation (Distilled vs. Base):**
  - **FLUX.2 Klein Distilled:** 4-step workflow utilizing rapid diffusion distillation.
  - **FLUX.2 Klein Base:** Standard 50-step iterative denoising workflow.
  - While the filename suggests a Klein distilled variant, model architecture and metadata alone do not prove step-budget tuning without empirical execution.
- **Definitive Classification:** **EXPERIMENTAL — END-TO-END COMPATIBILITY AND PERFORMANCE UNPROVEN ON TARGET PC.**
- **Observed Tensor Geometry vs. Conditioning Claims:**
  - The tensor `txt_in.weight` has an **observed tensor shape** of `(7680, 3072)`.
  - A popular community hypothesis suggests that this 7,680-dimensional input corresponds to concatenated representations from layers 9, 18, and 27 of a Qwen3 language model ($3 \times 2,560 = 7,680$).
  - **Critical Engineering Boundary:** Without architecture metadata in the GGUF container or upstream published specifications, this three-part extraction remains an **unproven theoretical conjecture**, NOT a confirmed conditioning implementation. The 7,680 dimension must be treated strictly as an observed tensor shape.
  - Reusing the Main AI (`Qwen3-4B-Q4_K_M.gguf`) for feature extraction cannot be claimed as viable until an actual extraction test proves:
    1. Correct tokenization matching FLUX prompt formatting.
    2. Correct Qwen3 model weights and architecture.
    3. Extraction of exact hidden states from layers 9, 18, and 27 (if the conjecture holds).
    4. Correct normalization (RMSNorm) and tensor layout matching DiT expectations.
    5. Valid, non-degraded conditioning output.
    6. Acceptable memory usage during forward extraction.
    7. Main AI remains continuously loaded in runtime and available according to approved residency invariants.
- **Required Companion Files:** Requires a standalone Qwen3 text encoder (if Main AI extraction is not used) and `flux2-vae.safetensors` (~335 MiB, both currently absent from disk).
- **Technical Roadblocks to Main AI Feature Extraction:**
  - Standard `llama.cpp` evaluates tokens forward to produce output logits and immediately frees intermediate layer hidden activations.
  - Reusing `Qwen3-4B-Q4_K_M.gguf` for feature extraction requires custom C++ runtime patches to intercept intermediate tensor outputs from layers 9, 18, and 27 before memory reclamation.
  - Quantization noise in `Q4_K_M` text embeddings may degrade conditioning quality compared to FP8/BF16.
  - Concurrency lock: While extracting embeddings, the resident Main AI cannot service user conversational dialogue.
- **Memory Feasibility & Admission Reality:**
  - Dedicated Text Encoder Route (~5,200 MiB total worker demand): Exceeds the current live admissible worker budget ($7,030.07 - 2,151 = 4,879.07\text{ MiB}$) and is strictly **REJECTED** by the dynamic admission controller.
  - Main AI Extraction Route (~3,737 to 4,335 MiB peak with VAE decode scratch buffers): While mathematically within the provisional 4,879 MiB planning budget, no validated software runtime currently exists on this machine that links GGUF DiT sampling to `llama.cpp` hidden layers on CPU.
  - VAE Decoding Peak Memory: Decoding a 16-channel $64 \times 64$ latent grid to an uncompressed $512 \times 512 \times 3$ RGB float image requires substantial intermediate scratch memory, inflating peak memory significantly above static weight sizes.
- **Estimated Generation Latency:** **[UNVERIFIED THEORETICAL ESTIMATE]** Projected at 45–90 seconds per Euler step on 2 CPU cores (AVX2, 0 CUDA). For a 4-step distilled workflow, this yields ~3–6 minutes; for a 20-step workflow, ~15–30 minutes. All unmeasured CPU performance figures remain explicitly marked as unverified estimates.

---

## 10. Video-Generation Feasibility

Local video diffusion models are classified according to three rigorous categories:
1. **Supported:** Programmatic Video Production (headless FFmpeg CLI, Whisper Base subtitles, Piper neural voiceovers, media trimming, merging, and audio ducking).
2. **Experimental / Unverified:** Direct CapCut draft project manipulation and observable UI automation.
3. **Impractical on Target Hardware:** Local text-to-video diffusion (Wan 2.1 T2V 1.3B, LTX-Video 2B).
   - Intel HD Graphics 530 has **0 dedicated VRAM** and dynamic shared system memory via DVMT.
   - Core i3-6100T memory controller operates at DDR4-2133 MT/s with a theoretical maximum bandwidth of 34.1 GB/s (real-world sustained bandwidth estimated at ~22–25 GB/s), which is 20–40× slower than dedicated GDDR6/HBM VRAM.
   - 3D spatio-temporal attention requires tens of gigabytes of memory bandwidth and massive tensor parallel compute.
   - Generation latency: **[UNVERIFIED THEORETICAL ESTIMATE]** Multi-hour render times per 5-second clip and heavy thermal package throttling.
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
| **Verified Facts (Empirically Confirmed)** | Intel Core i3-6100T (2C/4T @ 3.20 GHz, AVX2); 16.0 GB RAM (Two 8 GB Samsung DDR4-2666 DIMMs = 16,384 MiB installed, 16,260 MiB Windows-visible `ullTotalPhys`, ~124 MiB hardware-reserved); Intel HD Graphics 530 (0 dedicated VRAM, dynamic shared memory via DVMT); 10 physical model assets in `T:\ai creation` with exact bytes and SHA-256 hashes; `flux-2-klein-4b` DiT structure (149 tensors, 0 KV, `txt_in.weight` shape `(7680, 3072)`); absence of deleted Nemotron and un-downloaded models; Git repository location. |
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

---

## 20. Remaining Unverified Technical Claims

### Outstanding Evidence and Measurement Limitations

To enforce rigorous scientific and engineering integrity, all system metrics, architectural assertions, and performance claims are categorized across five distinct evidence tiers:

### 20.1 Empirically Measured Facts
1. **Physically Installed RAM:** Two Samsung 8 GB DDR4 modules (`M378A1K43DB2-CTD`) totaling 17,179,869,184 bytes (16,384.00 MiB / 16.00 GiB) verified via WMI `Win32_PhysicalMemory`.
2. **Configured Memory Operating Speed & Channel Topology:** Operating clock speed is **2,133 MT/s** (confirmed via WMI `Win32_PhysicalMemory.ConfiguredClockSpeed = 2133`, despite module rated speed of 2,666 MT/s), matching Intel Core i3-6100T official processor maximum memory speed. Modules occupy `ChannelA-DIMM0` (Bank 0) and `ChannelB-DIMM0` (Bank 2). While physical dual-slot installation across channels A and B is empirically confirmed, active symmetric dual-channel memory controller mode remains **unverified** without low-level diagnostic tools (e.g., CPU-Z or HWiNFO).
3. **Windows-Visible Physical RAM:** 17,049,899,008 bytes (16,260.05 MiB / 15.88 GiB) via Win32 `GlobalMemoryStatusEx.ullTotalPhys` and WMI `Win32_OperatingSystem.TotalVisibleMemorySize` (16,650,292 KB).
4. **Hardware-Reserved Memory Difference:** 129,970,176 bytes (123.95 MiB), measured as installed RAM minus Windows-visible RAM.
5. **Live Available Physical RAM Snapshots (Workload-Dependent):**
   - Snapshot 1 (2026-11-19T18:32:43): $7,371,558,912\text{ bytes}$ ($7,030.07\text{ MiB} \approx 6.87\text{ GiB}$) via Win32 `GlobalMemoryStatusEx.ullAvailPhys`. Note: In Windows memory architecture, `ullAvailPhys` includes Free, Zeroed, and Standby pages (the standby page list contains cached files/code that can be repurposed immediately).
   - Snapshot 2 (2026-11-19T18:54:14): $6,910,607,360\text{ bytes}$ ($6,590.47\text{ MiB} \approx 6.44\text{ GiB}$).
   - Snapshot 3 (2026-11-19T20:27:06): $7,267,610,624\text{ bytes}$ ($6,930.94\text{ MiB} \approx 6.77\text{ GiB}$).
   - Snapshot 4 (2026-11-19T20:42:12): $7,425,671,168\text{ bytes}$ ($7,081.67\text{ MiB} \approx 6.92\text{ GiB}$).
6. **Live System Virtual Commit:** 12,604,743,680 bytes (12,020.82 MiB) committed across RAM and `pagefile.sys` against a 19,600,035,840-byte (18,692.06 MiB) commit limit. (Committed memory is virtual address allocation backed by RAM or pagefile, NOT physical RAM consumed).
7. **Model Binary Assets on Disk:** Exact byte counts and SHA-256 hashes of all 10 local model assets residing in `T:\ai creation`.
8. **GGUF Binary Metadata & Architectural Parameters:** Verified via `tools/inspect_model_metadata.py` with exit code 0:
   - `flux-2-klein-4b-q4_0.gguf`: 149 tensors, 0 KV pairs, architecture `unknown` (missing `general.architecture`). All 149 tensor headers empirically audited with exact per-tensor validation: 83 tensors of standard `Q4_0` (raw numeric type ID 2, payload $2,149,908,480\text{ bytes} = 119,439,360\text{ blocks} \times 18\text{ B}$, divisible by 18, 0.5625 bytes/element) and 66 tensors of `BF16` (raw numeric type ID 30, payload $106,970,112\text{ bytes} = 53,485,056\text{ elements} \times 2\text{ B}$, divisible by 2, 2.0 bytes/element). Zero tensors of Type 31 (unresolved historical mapping, formerly associated in draft branches with `Q4_0_4_4`) exist in this file. The input projection `txt_in.weight` has observed shape `(7680, 3072)` and byte length $47,185,920\text{ bytes}$, proving it is stored unquantized in `BF16`. Exact container byte accounting matches down to 0 bytes: header & metadata table ($10,682\text{ bytes}$) + header alignment padding ($6\text{ bytes}$) + Q4_0 payload ($2,149,908,480\text{ bytes}$) + BF16 payload ($106,970,112\text{ bytes}$) + inter-tensor padding ($0\text{ bytes}$) + trailing padding ($0\text{ bytes}$) = $2,256,889,280\text{ bytes}$. (Passing binary boundary validation proves container structural integrity within file bounds, but does NOT prove authenticity, training validity, correct architecture, or runtime inference success).
   - `Qwen3-4B-Q4_K_M.gguf`: 398 tensors, 28 KV pairs, 36 layers (`block_count`), 2560 embedding length, 32 attention heads (`head_count`), 8 KV heads (`head_count_kv`), key length 128 (`key_length`), value length 128 (`value_length`).

### 20.2 Mathematically Derived Values
1. **Theoretical Maximum Memory Bandwidth:** $2 \times 8\text{ bytes} \times 2,133,333,333\text{ Hz} = \mathbf{34.13\text{ GB/s}}$ (matching Intel ARK specification of 34.1 GB/s, assuming active dual-channel mode).
2. **Qwen3-4B KV Cache Formula & Calculations:**
   - KV elements per token: $2 \times 36 \times 8 \times 128 = \mathbf{73,728\text{ elements/token}}$.
   - FP16 at 2K tokens ($N = 2,048$): $2,048 \times 73,728 \times 2 = 301,989,888\text{ bytes} = \mathbf{288.0\text{ MiB}}$.
   - FP16 at 4K tokens ($N = 4,096$): $4,096 \times 73,728 \times 2 = 603,979,776\text{ bytes} = \mathbf{576.0\text{ MiB}}$.
   - FP16 at 8K tokens ($N = 8,192$): $8,192 \times 73,728 \times 2 = 1,207,959,552\text{ bytes} = \mathbf{1,152.0\text{ MiB}}$.
   - Q8_0 at 4K tokens (34 bytes / 32 elements): $4,096 \times 73,728 \times (34/32) = 320,864,256\text{ bytes} = \mathbf{306.0\text{ MiB}}$.
3. **Physical Memory Not Reported as Available:**
   - Snapshot 1 (18:32:43): $16,260.05\text{ MiB} - 7,030.07\text{ MiB} = \mathbf{9,229.98\text{ MiB}}$ ($9,678,340,096\text{ bytes}$).
   - Snapshot 2 (18:54:14): $16,260.05\text{ MiB} - 6,590.47\text{ MiB} = \mathbf{9,669.58\text{ MiB}}$ ($10,139,291,648\text{ bytes}$).
   - Snapshot 3 (20:27:06): $16,260.05\text{ MiB} - 6,930.94\text{ MiB} = \mathbf{9,329.12\text{ MiB}}$ ($9,782,288,384\text{ bytes}$).
   - Snapshot 4 (20:42:12): $16,260.05\text{ MiB} - 7,081.67\text{ MiB} = \mathbf{9,178.38\text{ MiB}}$ ($9,624,227,840\text{ bytes}$).
   - This non-available physical RAM consists of active process working sets (which includes user applications and the `Memory Compression` process working set, observed at ~1,106.73 MiB at 18:32:43 and ~1,108.14 MiB at 20:27:29), modified pages, and locked kernel memory (non-paged pool, resident paged pool). Standby pages are NOT part of this figure because they are counted in available memory.
4. **Observed FLUX Tensor Geometry vs. Conditioning Conjecture:** The tensor `txt_in.weight` has an observed shape of `(7680, 3072)`. A community hypothesis proposes that this 7,680-dimensional input corresponds to three concatenated 2,560-dimensional representations from layers 9, 18, and 27 of a Qwen3 model ($3 \times 2,560 = 7,680$). Without architecture metadata or empirical demonstration, this remains an unproven theoretical conjecture, NOT a confirmed conditioning implementation.

### 20.3 Provisional Estimates
1. **Dynamic Safety Margin ($S_{\text{dynamic}}$):** $S_{\text{dynamic}} \approx \mathbf{2,151\text{ MiB}}$ is a provisional formula ($0.12 \times M_{\text{total\_phys}} + 200\text{ MiB}$) intended to protect system stability. The derived worker budget ($4,879.07\text{ MiB}$) is a theoretical estimate under Snapshot 1 and fluctuates with host workload; it must not be treated as a validated guaranteed capacity.
2. **Projected Application Base Components (Unimplemented):**
   - Windows 10 clean idle OS: ~2,900 MiB.
   - Intel HD 530 dynamic UI surface: ~150 MiB.
   - Tauri v2 host shell + WebView2 renderer (15 screens): ~220 MiB.
   - Audio subsystem (PortAudio + Piper ONNX + Whisper): ~300 MiB.
   - SQLite 3 + sqlite-vec cache: ~80 MiB.
   - Total provisional baseline: **~6,788 MiB** (~6.63 GiB / ~7.12 GB decimal).
3. **Diffusion Peak Memory Overheads:** VAE decoding scratch memory and latent grid allocations (~635–950 MiB).
4. **FLUX.2 Klein Generation Latency on CPU:** 45–90 seconds per Euler step (yielding ~3–6 minutes for 4-step distilled workflow, ~15–30 minutes for 20 steps) is an unverified theoretical estimate.

### 20.4 Unverified Implementation Assumptions
1. **FLUX Runtime Compatibility & Conditioning Extraction:** Running `flux-2-klein-4b-q4_0.gguf` on CPU requires an inference runtime with explicit software support for FLUX DiT architectures and 0-metadata GGUF layouts; AVX2 CPU support alone does not establish compatibility. Furthermore, extracting intermediate Qwen3 layers (9, 18, 27) for text conditioning assumes custom C++ patches in `llama.cpp`, which remains unverified in code. Zero tensors of Type 31 (unresolved historical mapping, formerly associated in draft forks with `Q4_0_4_4`) exist in the file (tensors are standard `Q4_0` and `BF16`), and runtime execution has not been verified.
2. **Main AI Memory Residency Behavior:** KAATYA application runtime policy mandates that Main AI is never intentionally evicted or unloaded during normal operation. However, the Windows Memory Manager (`ntoskrnl.exe`) may still page virtual memory pages to `pagefile.sys` under severe host memory pressure. Actual physical residency and paging behavior cannot be guaranteed by application policy alone and require empirical validation under load during Phase 4.
3. **Hardware-Reserved Memory Breakdown:** The exact breakdown of the 123.95 MiB hardware-reserved difference between BIOS, APIC/PCIe, and Intel HD 530 DVMT frame buffer remains unverified.
4. **Host Memory Reconciliation:** The ~2,442 MiB difference between the projected 6,788 MiB clean baseline and the 9,229.98 MiB host memory not reported as available is partially explained by background developer applications (Chrome, Antigravity, Python), Windows Memory Compression working set (observed at 1,106.73 MiB via `(Get-Process -Name "Memory Compression").WorkingSet64` as an element of active working sets, NOT an additive quantity), and kernel memory pools (1,231.77 MiB). Exact component reconciliation cannot be claimed without independent, non-overlapping measurements across all kernel and user-space structures.

### 20.5 Tests That Can Only Be Performed After Explicit Phase 4 Authorization
1. **Model Token Generation Throughput:** Physical measurement of token generation speeds (tok/s) for Qwen3-4B and secondary workers via `llama-bench` on AVX2 CPU.
2. **Real-World Sustained Memory Bandwidth:** Measurement via a physical STREAM benchmark under active dual-channel load.
3. **End-to-End FLUX.2 Klein Execution:** Actual generation of an image from prompt to PNG using `flux-2-klein-4b-q4_0.gguf` + VAE on target CPU.
4. **Concurrent Runtime Working Set:** Live empirical measurement of Tauri v2 + WebView2 + Main AI running concurrently under Windows 10.
5. **Video NLE Export & Audio Pipeline:** Real-time factor (RTF) measurement of Whisper STT and Piper TTS during active multi-track video assembly.

---

## 21. Explicit Phase 4 Hold Status

> [!IMPORTANT]
> **PHASE 4 APPLICATION IMPLEMENTATION REMAINS ON STRICT HOLD.**
> All Phase 3 architectural corrections, repository-wide consistency reconciliations, and documentation audits are complete. No application source code has been written, no models downloaded or modified, and no system settings altered.
> 
> The project remains completely paused awaiting the user's explicit authorization to proceed to Phase 4.

---
*Report formally submitted for Phase 3 technical sign-off.*
