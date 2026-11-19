# Realistic Hardware Benchmark Protocol & Performance Audit

## 1. Audit of Phase 3 Performance Claims: Theoretical vs. Verified

In the Phase 3 architecture deliverables, several performance metrics were stated without clearly establishing that they were **theoretical estimates based on DDR4 memory bandwidth calculations**, rather than physical measurements taken on the target machine.

### Verification Status Table

| Performance Dimension | Claimed Value in Phase 3 | Status | Technical Correction & Reality |
| :--- | :--- | :---: | :--- |
| **Qwen3-4B Generation Speed** | 12 – 16 tokens/sec | **[UNVERIFIED ESTIMATE]** | Theoretical DDR4 bandwidth limit is $\sim 10.3\text{ tok/s}$. With Skylake AVX2 vector optimizations, expected range is **9.0 – 14.5 tokens/sec**. Must be measured on target PC. |
| **Qwen3-4B Prompt Ingestion** | 45 – 65 tokens/sec | **[UNVERIFIED ESTIMATE]** | Skylake AVX2 FMA compute-bound estimate. Expected real range: **35 – 55 tokens/sec**. |
| **Nemotron 7.5B Generation** | 4.2 – 6.5 tokens/sec | **[UNVERIFIED ESTIMATE]** | Theoretical bandwidth limit is $\sim 4.1\text{ tok/s}$. Realistic range: **3.5 – 5.2 tokens/sec**. (Model cannot run concurrently on 12GB RAM). |
| **Whisper Base Transcription** | 750 – 950 ms (3-sec clip) | **[UNVERIFIED ESTIMATE]** | Based on RTF $\approx 0.25 - 0.35$ using 2 threads. Realistic range: **700 – 1,150 ms**. |
| **Piper TTS Real-Time Factor** | 0.08 – 0.12 RTF | **[UNVERIFIED ESTIMATE]** | Highly realistic for VITS ONNX, but unverified on this specific i3-6100T. |
| **Qwen3 Embedding Throughput** | "120 tokens/millisecond" | **[FATAL ERROR / RETRACTED]** | **Mathematically impossible.** 120 tok/ms equates to **120,000 tokens/sec**! See Section 2 for full correction. |
| **Tauri v2 Idle Memory** | 35 – 55 MB RAM | **[UNVERIFIED ESTIMATE]** | Varies depending on WebView2 background tasks and extensions. Expected range: **45 – 85 MB RAM**. |
| **Emergency ESC Interruption** | $<50\text{ ms}$ | **[UNVERIFIED ESTIMATE]** | Process termination timing depends on Windows scheduler load. Expected: **20 – 120 ms**. |

---

## 2. Forensic Investigation of the Embedding Throughput Error

### 2.1 The Error
In `MEMORY_AND_VOICE_ARCHITECTURE.md`, Section 2.2 stated:
> *"Inference Speed on i3-6100T: ~120 tokens/millisecond (CPU vectorized). Embedding a 200-word paragraph takes ~18 ms."*

### 2.2 The Mathematical & Physical Reality
1. **The Math:** $120\text{ tokens/ms} \times 1,000\text{ ms/s} = \mathbf{120,000\text{ tokens/second}}$.
2. A 0.6B parameter transformer (`qwen3-embedding-0.6b-q8_0`) has 28 transformer layers and a 1024 embedding dimension. Processing 120,000 tokens per second would require sustained memory bandwidth exceeding **$70\text{ TB/second}$**, which is orders of magnitude beyond enterprise H100 GPU clusters, let alone a 35W Intel Core i3-6100T with 24 GB/s DDR4 memory.
3. Furthermore, the paragraph contained an internal contradiction: if throughput was 120 tokens/ms, a 200-word (~260 tokens) paragraph would take $260 / 120 = \mathbf{2.17\text{ ms}}$, not 18 ms!
4. **The Root Cause:** Typographical units confusion. The author intended to write **`~120 tokens/second`** (which corresponds to $\approx 0.12\text{ tokens/millisecond}$ or $\approx 8.3\text{ ms per token}$).
5. **The Corrected Value:**
   - **Throughput:** **~80 to 180 tokens/second** on 2 CPU threads with AVX2.
   - **Paragraph Latency:** Embedding a 200-word (~260 tokens) text segment takes **~1.4 to 2.8 seconds**, which is perfectly adequate for asynchronous background vector memory indexing.

---

## 3. Empirical Benchmark Execution Protocol (For Target PC)

When Phase 4 validation is authorized, the target machine will execute this empirical benchmark suite using official compiled binaries (`llama-bench.exe`, `whisper-bench.exe`, and a custom Rust harness).

```powershell
# ==============================================================================
# EMPIRICAL BENCHMARK PROTOCOL FOR INTEL CORE i3-6100T (16 GB RAM)
# ==============================================================================

# 1. Hardware Environment Snapshot
Write-Host "--- Recording Physical Host Baseline ---"
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
Get-WmiObject -Class Win32_VideoController | Select-Object Name, DriverVersion

# 2. Benchmark Primary Workhorse (Qwen3-4B-Q4_K_M.gguf)
# Tests prompt ingestion (p=512) and autoregressive generation (n=128) across 3 threads
.\tools\llama-bench.exe -m "T:\ai creation\Qwen3-4B-Q4_K_M.gguf" -p 512 -n 128 -t 3 -ngl 0

# 3. Benchmark Embedding Model (qwen3-embedding-0.6b-q8_0.gguf)
# Tests embedding batch latency across 2 threads
.\tools\llama-bench.exe -m "T:\ai creation\qwen3-embedding-0.6b-q8_0.gguf" -p 256,512 -n 0 -t 2 -ngl 0

# 4. Measure Working Set Memory & Swap Activity
Get-Process -Name "llama-bench" | Select-Object WorkingSet64, PeakWorkingSet64, PagedMemorySize64
```

### 3.1 Metrics Logged in Final Verification
- **CPU Clock Frequency & Throttling Status:** Verified via Windows performance counters.
- **Prompt Processing (TTFT):** Recorded in tokens/second.
- **Autoregressive Generation (Eval):** Recorded in tokens/second.
- **Peak Working Set Memory:** Recorded in Megabytes (MB).
- **Physical Free Memory Delta:** Measured before and after model allocation.
- **Audio Stutter Verification:** Simultaneous playback of a 10-second Piper TTS audio stream during maximum prompt evaluation load to verify zero audio ring-buffer drops on Thread 3.
