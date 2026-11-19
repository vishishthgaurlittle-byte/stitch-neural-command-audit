# KAATYA: Final Authoritative Model Inventory
## Byte-Level Verification & SHA-256 Integrity Audit

---

## 1. Executive Summary & Verification Protocol

An empirical, byte-level inspection and cryptographic hash audit was conducted across `T:\ai creation` on **November 19, 2026**. 

### Key Findings:
1. **10 Models Confirmed Present:** Exactly 10 model files exist physically on disk (6 GGUF LLMs/DiT, 1 GGUF Embedding, 1 GGML Whisper, and 2 Piper ONNX voices).
2. **Former Heavyweight Model Removed:** `Nemotron-3.5-Bolt-E4B-Q4_K_M.gguf` (6.18 GB) was deleted/removed from disk to free storage space for the newly downloaded models. It is **CONFIRMED ABSENT**.
3. **Four Historical References Confirmed Absent:** `qwen-image-2.1`, `qwen2.5-coder-3b`, `qwen2.5-coder-1.5b-q4_k_m`, and `nomic-embed-text` are **ABSENT** and exist only as historical references in earlier notes.
4. **Permanent Main AI Confirmed:** `Qwen3-4B-Q4_K_M.gguf` is physically intact, verified by SHA-256, and designated as the permanent core for **KAATYA**.

---

## 2. Complete Inventory of Confirmed Present Assets (10/10)

The 10 local files on `T:\ai creation` span multiple distinct model families and asset types (chat models, coding models, embedding models, image-generation DiT backbones, speech-recognition models, and TTS voice graphs). They must not be conflated under generic "language models".

| # | Exact Filename | Category | Size (Bytes) | Binary (GiB) | Decimal (GB) | Local SHA-256 Checksum | Upstream Checksum Status |
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

> [!IMPORTANT]
> **Integrity Verification vs. Upstream Authenticity:**
> The SHA-256 checksums documented above represent exact empirical hashes calculated directly from the disk files on `T:\ai creation`. A locally calculated checksum guarantees internal bit-level consistency and tamper detection across project builds. However, for community-quantized weights where upstream publisher manifests are not officially signed, upstream authenticity cannot be claimed without published upstream checksums. Items marked *"Unavailable"* are verified locally for reproducibility but unverified against official upstream manifests.

---

## 3. Deep Technical Specifications for Every Present Model

### 1. `Qwen3-4B-Q4_K_M.gguf` (KAATYA Permanent Main AI)
- **Directory:** `T:\ai creation\`
- **Size:** 2,497,280,256 bytes (2.326 GiB / 2.497 GB)
- **Architecture Details:** 36 blocks, 2,560 embedding length, 32 attention heads (8 KV heads, 4:1 GQA ratio), native context 40,960 tokens. Vocab: 151,936 tokens.
- **Estimated Runtime RAM:** **~3,138 MiB** (with 4,096 working context, FP16 KV cache, and compute graph buffers).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **PERMANENT MAIN AI.** Never unloaded by application policy.
- **Assigned Role:** **KAATYA Main AI Controller** (Agent 1) & supervisor of all logical roles.

---

### 2. `Qwen3-1.7B-Q3_K_M.gguf` (Compact Language & Writing Specialist)
- **Directory:** `T:\ai creation\`
- **Size:** 1,073,242,208 bytes (1.000 GiB / 1.073 GB)
- **Architecture Details:** `qwen3` architecture, 28 blocks, 2,048 embedding length, 16 heads (8 KV heads, 2:1 GQA ratio), native context 40,960 tokens.
- **Estimated Runtime RAM:** **~1,250 MB** (with 4,096 working context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **DYNAMIC LOCAL WORKER.** Admitted on demand via the 10-step admission check.
- **Assigned Role:** **Writer** (Agent 5), **Social Media** (Agent 19), **Presentation** (Agent 21).

---

### 3. `SmolLM2-1.7B-Instruct-Q4_K_M.gguf` (Fast English & Grammar Specialist)
- **Directory:** `T:\ai creation\`
- **Size:** 1,055,609,824 bytes (0.983 GiB / 1.056 GB)
- **Architecture Details:** `llama` architecture, 24 blocks, 2,048 embedding length, 32 heads (32 KV heads, MHA), native context 8,192 tokens. Calibrated with custom imatrix. Vocab: 49,152 tokens.
- **Estimated Runtime RAM:** **~1,350 MB** (with 4,096 working context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **DYNAMIC LOCAL WORKER.** Admitted on demand via the 10-step admission check.
- **Assigned Role:** **Grammar & Language** (Agent 18 - English benchmark candidate), **Assistant** (Agent 15), **Messenger** (Agent 6).

---

### 4. `Qwen2.5-Coder-1.5B-Instruct-Q3_K_M.gguf` (Dedicated Local Coding Helper)
- **Directory:** `T:\ai creation\`
- **Size:** 824,178,784 bytes (0.768 GiB / 0.824 GB)
- **Architecture Details:** `qwen2` architecture, 28 blocks, 1,536 embedding length, 12 heads (2 KV heads, 6:1 GQA ratio), native context 32,768 tokens.
- **Estimated Runtime RAM:** **~1,050 MB** (with 4,096 working context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **DYNAMIC LOCAL WORKER.** Admitted on demand via the 10-step admission check.
- **Assigned Role:** **Coder** (Agent 2), **Database Engineer** (Agent 23), **Tester** (Agent 9).

---

### 5. `qwen2.5-1.5b-instruct-q4_k_m.gguf` (General Multilingual Small Assistant)
- **Directory:** `T:\ai creation\`
- **Size:** 1,117,320,736 bytes (1.041 GiB / 1.117 GB)
- **Architecture Details:** `qwen2` architecture, 28 blocks, 1,536 embedding length, 12 heads (2 KV heads), context 32,768 tokens.
- **Estimated Runtime RAM:** **~1,280 MB** (with 4,096 context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **DYNAMIC LOCAL WORKER.** Admitted on demand via the 10-step admission check.
- **Assigned Role:** **Document Intelligence** (Agent 22), **Data Analyst** (Agent 13).

---

### 6. `flux-2-klein-4b-q4_0.gguf` (Diffusion Transformer Backbone)
- **Directory:** `T:\ai creation\`
- **Size:** 2,256,889,280 bytes (2.1019 GiB / 2,152.34 MiB / 2.2569 GB)
- **SHA-256 Checksum:** `9c5939d55e3ac76e3a700029770fcc5e1b873d12c2a6d22c6c3fec217488e718`
- **Upstream Source:** Community Hugging Face GGUF repository (unverified upstream signed manifest).
- **Architecture Details:** GGUF v3, 149 tensors, **0 KV metadata entries** (architecture reported as `unknown` due to missing `general.architecture`). Primary quantization is GGML Type 30 (`Q4_0_4_4`, 4-bit tiled blocks requiring AVX2 runtime support) with Type 0 (`F32`) for modulation and projection layers.
- **Binary Boundary Validation:** Verified via `tools/inspect_model_metadata.py` (Exit code 0). Tensor offsets are monotonically ascending and all 149 tensor payloads fall strictly within the 2,256,889,280-byte file boundary (max tensor end offset: 2,222,974,400 bytes). Passing container boundary validation proves container structural integrity on disk, but does NOT prove model authenticity, training validity, correct architecture, or runtime inference success.
- **Crucial Technical Reality:** This file contains **ONLY the DiT transformer backbone weights** (149 tensors). Unlike FLUX.1, FLUX.2 Klein departs from CLIP-L/T5-XXL and utilizes a **Qwen3 language model** text encoder (extracting layers 9, 18, and 27 to produce a 7,680-dimensional conditioning vector matching `txt_in.weight` shape `(7680, 3072)`) plus `flux2-vae.safetensors`. These companion weights are absent from disk.
- **Estimated Pipeline RAM:** Requires **~3.7 to 4.3 GB RAM** (Main AI extraction route) or **~5.2 to 6.1 GB RAM** (dedicated encoder route) when paired with companion text encoder, VAE, and latent scratch buffers.
- **Runtime Compatibility:** ComfyUI with `ComfyUI-GGUF` (or specialized `sd.cpp` FLUX.2 Klein branches).
- **Coexistence Status:** **EXPERIMENTAL — END-TO-END COMPATIBILITY AND PERFORMANCE UNPROVEN ON TARGET PC.** Under current live available RAM ($7,030.07\text{ MiB}$) and dynamic safety margin (~2,151 MiB), the provisional net admissible worker budget is $\approx 4,879.07\text{ MiB}$. The dedicated encoder route (~5,200 MiB) exceeds this budget and is strictly rejected by the dynamic admission controller. The Main AI extraction route (~3,737–4,335 MiB peak) lacks a verified CPU C++ implementation for extracting intermediate hidden states. In addition, a distinction exists between FLUX.2 Klein Distilled (4-step workflow) and FLUX.2 Klein Base (50-step workflow); while the local GGUF is titled `flux-2-klein-4b-q4_0.gguf`, step-budget compatibility is unverified on this hardware. Generation latency is an **[UNVERIFIED THEORETICAL ESTIMATE]** of 45–90s per step (~3–6 minutes for 4 steps, ~15–30 minutes for 20 steps). Feasibility will not be claimed until an end-to-end benchmark succeeds in Phase 4.
- **Assigned Role:** **Image Studio** (Agent 17 - Experimental Local Mode).

---

### 7. `qwen3-embedding-0.6b-q8_0.gguf` (Local Semantic Memory Embedding Engine)
- **Directory:** `T:\ai creation\`
- **Size:** 639,150,592 bytes (0.595 GiB / 0.639 GB)
- **Architecture Details:** `qwen3` architecture, 28 blocks, 1,024 embedding dimension, 16 heads (8 KV heads), mean pooling.
- **Estimated Runtime RAM:** **~750 MB**.
- **Coexistence Status:** **SAFELY COEXISTS.** Runs as an embedded feature within the SQLite vector pipeline.
- **Assigned Role:** **Memory Centre & Vector Search Engine**.

---

### 8. `ggml-base.bin` (Speech-to-Text Transcription Engine)
- **Directory:** `T:\ai creation\`
- **Size:** 147,951,465 bytes (0.138 GiB / 0.148 GB)
- **Architecture Details:** Whisper Base multilingual encoder-decoder transformer (74M parameters).
- **Estimated Runtime RAM:** **~220 MB**.
- **Assigned Role:** **Audio & Voice** (Agent 20) & Global Voice Input.

---

### 9. `en_US-mike-medium.onnx` & 10. `hi_IN-rohan-medium.onnx` (Piper Neural Voices)
- **Directory:** `T:\ai creation\english voice onnx + jons\` & `T:\ai creation\hindi voice onnx + jon\`
- **Sizes:** 63,221,984 bytes (0.059 GiB / 0.063 GB) & 62,950,044 bytes (0.059 GiB / 0.063 GB).
- **Architecture Details:** VITS ONNX neural speech synthesis.
- **Estimated Runtime RAM:** **~140 MB total** (both sessions loaded).
- **Assigned Role:** **Global Desktop Text-to-Speech Output (English, Hindi & Hinglish)**.

---

## 4. Audit of Absent & Historical Model References

| Model Reference | Status | Audit Findings & Verification |
| :--- | :---: | :--- |
| **`Nemotron-3.5-Bolt-E4B-Q4_K_M.gguf`** (6.18 GB) | **CONFIRMED ABSENT** | Was present during Phase 1–3 audits; removed from disk by user to free storage space for the 5 new models. |
| **`qwen-image-2.1-step90000-Q4_K_M.gguf`** | **CONFIRMED ABSENT** | Historical reference from earlier download plans. Does not exist on disk. |
| **`qwen2.5-coder-3b-instruct-q4_k_m.gguf`** | **CONFIRMED ABSENT** | Historical reference. Not present on disk. |
| **`qwen2.5-coder-1.5b-instruct-q4_k_m.gguf`** | **CONFIRMED ABSENT** | Historical reference. Replaced by `Qwen2.5-Coder-1.5B-Instruct-Q3_K_M.gguf` (Q3_K_M quantization). |
| **`nomic-embed-text-v1.5.Q4_K_M.gguf`** | **CONFIRMED ABSENT** | Historical reference. The local embedding role is fulfilled by `qwen3-embedding-0.6b-q8_0.gguf`. |

---

## 5. Duplicate & Overlapping Model Analysis

We currently possess three 1.5B–1.7B general/assistant models and one 1.5B coder:
1. `Qwen3-1.7B-Q3_K_M.gguf` (1.00 GiB) vs. `qwen2.5-1.5b-instruct-q4_k_m.gguf` (1.04 GiB):
   - `Qwen3-1.7B` features the newer Qwen 3 architecture with enhanced reasoning and longer native context.
   - `qwen2.5-1.5b` features higher quantization precision (`Q4_K_M` vs `Q3_K_M`).
2. `SmolLM2-1.7B-Instruct-Q4_K_M.gguf` (0.98 GiB):
   - Distinct Llama architecture, exceptionally fast for English grammar, summarization, and short conversational turns.
3. **Recommendation:** Keep all four compact models. Because each requires only ~0.8 to 1.1 GB of storage, keeping them gives KAATYA specialist workers tailored for coding (`Qwen2.5-Coder`), grammar/assistant duties (`SmolLM2`), writing/presentation (`Qwen3-1.7B`), and document extraction (`Qwen2.5-1.5B`).
