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

## 2. Complete Inventory of Confirmed Present Models (10/10)

| # | Exact Filename | Physical Size (Bytes) | Size (GiB) | SHA-256 Checksum | Base Architecture | Quantization | Parameter Count |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- | :---: |
| **1** | `Qwen3-4B-Q4_K_M.gguf` | 2,497,280,256 B | 2.33 GiB | `7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5` | `qwen3` | Q4_K_M | ~4.0B |
| **2** | `Qwen3-1.7B-Q3_K_M.gguf` | 1,073,242,208 B | 1.00 GiB | `79af9a932c6659aabc06d6560b8404063c79f616b136953370f9c67853e162e0` | `qwen3` | Q3_K_M | ~1.7B |
| **3** | `SmolLM2-1.7B-Instruct-Q4_K_M.gguf` | 1,055,609,824 B | 0.98 GiB | `77665ea4815999596525c636fbeb56ba8b080b46ae85efef4f0d986a139834d7` | `llama` | Q4_K_M (imatrix) | ~1.7B |
| **4** | `Qwen2.5-Coder-1.5B-Instruct-Q3_K_M.gguf` | 824,178,784 B | 0.77 GiB | `0c292daeec7355c9d695abf3d7da336f3766a983762bd4b82fbdad6d7dbcac7e` | `qwen2` | Q3_K_M | ~1.5B |
| **5** | `qwen2.5-1.5b-instruct-q4_k_m.gguf` | 1,117,320,736 B | 1.04 GiB | `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e` | `qwen2` | Q4_K_M | ~1.5B |
| **6** | `flux-2-klein-4b-q4_0.gguf` | 2,256,889,280 B | 2.10 GiB | `9c5939d55e3ac76e3a700029770fcc5e1b873d12c2a6d22c6c3fec217488e718` | `flux` / DiT | Q4_0 | ~4.0B |
| **7** | `qwen3-embedding-0.6b-q8_0.gguf` | 639,150,592 B | 0.60 GiB | `ee029816fb9615e361d9e444abc0059827322e665c3ed9e6bc0531efe20cddda` | `qwen3` | Q8_0 | ~0.59B |
| **8** | `ggml-base.bin` | 147,951,465 B | 0.14 GiB | `60ed5bc3dd14eea856493d334349b405782ddcaf0028d4b5df4088345fba2efe` | `whisper` | FP16 GGML | ~74M |
| **9** | `en_US-mike-medium.onnx` | 63,221,984 B | 0.06 GiB | `6876866e3dfadc7f044bc5e4fbac16c47b5a1e79eaec04e3bb0c2c6e9da8a857` | VITS (Piper) | FP32/FP16 ONNX | ~28M |
| **10** | `hi_IN-rohan-medium.onnx` | 62,950,044 B | 0.06 GiB | `b65dc80fb34d9dcd1cf684cb297966a34983bbc93bb1696fe207f32b0b33a091` | VITS (Piper) | FP32/FP16 ONNX | ~28M |

---

## 3. Deep Technical Specifications for Every Present Model

### 1. `Qwen3-4B-Q4_K_M.gguf` (KAATYA Permanent Main AI)
- **Directory:** `T:\ai creation\`
- **Size:** 2,497,280,256 bytes (2.33 GiB / 2.50 GB)
- **Architecture Details:** 36 blocks, 2,560 embedding length, 32 attention heads (8 KV heads, 4:1 GQA ratio), native context 40,960 tokens. Vocab: 151,936 tokens.
- **Estimated Runtime RAM:** **~3,100 MB** (with 4,096 working context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **PERMANENT MAIN AI.** Never unloaded.
- **Assigned Role:** **KAATYA Main AI Controller** (Agent 1) & supervisor of all logical roles.

---

### 2. `Qwen3-1.7B-Q3_K_M.gguf` (Compact Language & Writing Specialist)
- **Directory:** `T:\ai creation\`
- **Size:** 1,073,242,208 bytes (1.00 GiB / 1.07 GB)
- **Architecture Details:** `qwen3` architecture, 28 blocks, 2,048 embedding length, 16 heads (8 KV heads, 2:1 GQA ratio), native context 40,960 tokens.
- **Estimated Runtime RAM:** **~1,250 MB** (with 4,096 working context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **SAFELY COEXISTS AS LOCAL WORKER.**
  $$\text{Base System + KAATYA} (7.2\text{ GB}) + \text{Qwen3-1.7B} (1.25\text{ GB}) = \mathbf{8.45\text{ GB}} \le \mathbf{12.0\text{ GB}}$$
- **Assigned Role:** **Writer** (Agent 5), **Social Media** (Agent 19), **Presentation** (Agent 21).

---

### 3. `SmolLM2-1.7B-Instruct-Q4_K_M.gguf` (Fast English & Grammar Specialist)
- **Directory:** `T:\ai creation\`
- **Size:** 1,055,609,824 bytes (0.98 GiB / 1.06 GB)
- **Architecture Details:** `llama` architecture, 24 blocks, 2,048 embedding length, 32 heads (32 KV heads, MHA), native context 8,192 tokens. Calibrated with custom imatrix. Vocab: 49,152 tokens.
- **Estimated Runtime RAM:** **~1,350 MB** (with 4,096 working context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **SAFELY COEXISTS AS LOCAL WORKER.** ($7.2\text{ GB} + 1.35\text{ GB} = \mathbf{8.55\text{ GB}} \le 12.0\text{ GB}$).
- **Assigned Role:** **Grammar & Language** (Agent 18), **Assistant** (Agent 15), **Messenger** (Agent 6).

---

### 4. `Qwen2.5-Coder-1.5B-Instruct-Q3_K_M.gguf` (Dedicated Local Coding Helper)
- **Directory:** `T:\ai creation\`
- **Size:** 824,178,784 bytes (0.77 GiB / 0.82 GB)
- **Architecture Details:** `qwen2` architecture, 28 blocks, 1,536 embedding length, 12 heads (2 KV heads, 6:1 GQA ratio), native context 32,768 tokens.
- **Estimated Runtime RAM:** **~1,050 MB** (with 4,096 working context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **SAFELY COEXISTS AS LOCAL WORKER.** ($7.2\text{ GB} + 1.05\text{ GB} = \mathbf{8.25\text{ GB}} \le 12.0\text{ GB}$).
- **Assigned Role:** **Coder** (Agent 2), **Database Engineer** (Agent 23), **Tester** (Agent 9).

---

### 5. `qwen2.5-1.5b-instruct-q4_k_m.gguf` (General Multilingual Small Assistant)
- **Directory:** `T:\ai creation\`
- **Size:** 1,117,320,736 bytes (1.04 GiB / 1.12 GB)
- **Architecture Details:** `qwen2` architecture, 28 blocks, 1,536 embedding length, 12 heads (2 KV heads), context 32,768 tokens.
- **Estimated Runtime RAM:** **~1,280 MB** (with 4,096 context).
- **Runtime Compatibility:** Native `llama.cpp` AVX2 backend.
- **Coexistence Status:** **SAFELY COEXISTS AS LOCAL WORKER.**
- **Assigned Role:** **Document Intelligence** (Agent 22), **Data Analyst** (Agent 13).

---

### 6. `flux-2-klein-4b-q4_0.gguf` (Diffusion Transformer Backbone)
- **Directory:** `T:\ai creation\`
- **Size:** 2,256,889,280 bytes (2.10 GiB / 2.26 GB)
- **Architecture Details:** FLUX Diffusion Transformer (DiT) backbone, 149 tensors, Q4_0 quantization.
- **Crucial Technical Reality:** This file contains **ONLY the DiT transformer weights**. It does NOT contain the text encoder (CLIP-L / T5-XXL) or VAE.
- **Estimated Pipeline RAM:** Requires **~9.0 to 11.5 GB RAM** when paired with text encoders and VAE.
- **Runtime Compatibility:** ComfyUI with `ComfyUI-GGUF` or `sd.cpp`.
- **Coexistence Status:** **EXPERIMENTAL / MEMORY-GATED.** Running on CPU alongside KAATYA consumes nearly all 12 GB RAM. Cannot run simultaneously with other local workers.
- **Assigned Role:** **Image Studio** (Agent 17 - Local Offline Mode).

---

### 7. `qwen3-embedding-0.6b-q8_0.gguf` (Local Semantic Memory Embedding Engine)
- **Directory:** `T:\ai creation\`
- **Size:** 639,150,592 bytes (0.60 GiB / 0.64 GB)
- **Architecture Details:** `qwen3` architecture, 28 blocks, 1,024 embedding dimension, 16 heads (8 KV heads), mean pooling.
- **Estimated Runtime RAM:** **~750 MB**.
- **Coexistence Status:** **SAFELY COEXISTS.** Runs as an embedded feature within the SQLite vector pipeline.
- **Assigned Role:** **Memory Centre & Vector Search Engine**.

---

### 8. `ggml-base.bin` (Speech-to-Text Transcription Engine)
- **Directory:** `T:\ai creation\`
- **Size:** 147,951,465 bytes (0.14 GiB / 0.15 GB)
- **Architecture Details:** Whisper Base multilingual encoder-decoder transformer (74M parameters).
- **Estimated Runtime RAM:** **~220 MB**.
- **Assigned Role:** **Audio & Voice** (Agent 20) & Global Voice Input.

---

### 9. `en_US-mike-medium.onnx` & 10. `hi_IN-rohan-medium.onnx` (Piper Neural Voices)
- **Directory:** `T:\ai creation\english voice onnx + jons\` & `T:\ai creation\hindi voice onnx + jon\`
- **Sizes:** 63,221,984 bytes & 62,950,044 bytes (~60 MB each).
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
