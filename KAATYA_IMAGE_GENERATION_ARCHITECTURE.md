# KAATYA: Image Generation Architecture & Production Pipeline

## 1. Executive Summary: Hybrid Local & Cloud Image Generation

The **KAATYA Image Studio** (Agent 17) provides visual concept generation, graphic design assets, and video thumbnail creation through a realistic hybrid architecture:
1. **Local Offline Engine (Experimental / Resource-Gated):** Leverages `flux-2-klein-4b-q4_0.gguf` on CPU for air-gapped environments.
2. **Authorized Online Providers (Production Fast Path):** Connects to leading image generation APIs (OpenAI DALL-E 3, Stability AI, Ideogram) with mandatory per-generation approval.

```mermaid
flowchart TD
    UserConcept[User Concept / Thumbnail Request] --> ImageAgent[Agent 17: Image Studio]
    ImageAgent --> PromptEng[Prompt Expansion & Quality Optimization]
    
    PromptEng --> CheckMode{Is Air-Gap Active or Local Only?}
    
    CheckMode -->|Air-Gap Active / Local Requested| LocalCheck{Verify Available Physical RAM}
    LocalCheck -->|< 4.0 GB Free RAM| WarnRAM[Alert User: High Memory Pressure & Suggest Online Mode]
    LocalCheck -->|>= 4.0 GB Free RAM| LocalGen[Dispatch Local FLUX.2 Klein CPU Pipeline via ComfyUI / sd.cpp]
    LocalGen --> Result[Output 512x512 / 768x768 PNG]
    
    CheckMode -->|Online Allowed| CloudGate{Security Approval Modal}
    CloudGate -->|User Authorizes| CloudGen[Dispatch to DALL-E 3 / Ideogram / Stability AI]
    CloudGate -->|User Rejects| Abort[Cancel Task]
    CloudGen --> Result
    
    Result --> KAATYA_Review[KAATYA Main AI Validates Image & Delivers to User]
```

---

## 2. Technical Audit of Local Model: FLUX.2 Klein 4B

### 2.1 Binary Metadata & Architectural Inspection
- **File Name:** `flux-2-klein-4b-q4_0.gguf`
- **File Location:** `T:\ai creation\flux-2-klein-4b-q4_0.gguf`
- **File Size:** 2,256,889,280 bytes (2.102 GiB / 2.257 GB)
- **SHA-256 Checksum:** `9c5939d564fa7454261d7a8e7e1cb5bf4d27192667ae967a5b39414da8846c10`
- **GGUF Structure:** Version 3, 149 tensors, **0 KV metadata entries**.
- **Tensors Present:** Exclusively the Diffusion Transformer (DiT) weights: 5 double blocks (`double_blocks.0` through `double_blocks.4`) and 20 single blocks (`single_blocks.0` through `single_blocks.19`), plus input/output modulations and `txt_in.weight` `[7680, 3072]`.

### 2.2 True FLUX.2 Klein Pipeline Dependencies
Earlier audit references erroneously listed legacy FLUX.1 assets (`clip_l.safetensors` and `t5xxl_fp8`). FLUX.2 Klein departs fundamentally from the dual CLIP/T5 scheme:

| Pipeline Component | Actual Required Asset | Architecture Details | Status in `T:\ai creation` |
| :--- | :--- | :--- | :---: |
| **Diffusion Backbone (DiT)** | `flux-2-klein-4b-q4_0.gguf` | 4B distilled DiT, Q4_0 quant, 149 tensors | **CONFIRMED PRESENT** |
| **Text Encoder** | Qwen3 Language Model Feature Extractor | Extracts intermediate layers 9, 18, and 27 ($2560 \times 3 = 7,680$ dims) | **ABSENT AS COMPANION FILE** |
| **Variational Autoencoder** | `flux2-vae.safetensors` | FLUX.2 Latent Autoencoder (16-channel) | **ABSENT** |
| **Tokenizer & Template** | Qwen3 Tokenizer | Structured `<|im_start|>` chat template formatting | Bundled with Qwen3 runtime |

### 2.3 Evaluation: Can Resident `Qwen3-4B-Q4_K_M.gguf` Serve as the Text Encoder?
The local disk already holds `Qwen3-4B-Q4_K_M.gguf`. Could this file double as the FLUX text encoder to avoid downloading another 3–5 GB asset?
- **Architectural Overlap:** Qwen3-4B contains the necessary attention blocks and layers 9, 18, and 27.
- **Critical Technical Limitations:**
  1. **Logit Evaluation vs. Layer Extraction:** Standard `llama.cpp` inference processes tokens forward to generate logits, discarding intermediate hidden states to optimize cache memory. Harvesting concatenated hidden vectors from layers 9, 18, and 27 requires custom C-API forward hooks not present in stock runtime builds.
  2. **Quantization Noise in Conditioning Vectors:** `Qwen3-4B-Q4_K_M` uses medium 4-bit block quantization. Quantization noise in continuous text embedding spaces degrades spatial prompt adherence compared to FP8 or BF16 encodings.
  3. **Concurrency Conflict:** The Main AI is permanently resident with an active conversational KV-cache. Running feature extraction through the same instance would block the user's conversational interface or require initializing a second memory context (~500 MB RAM).

### 2.4 Compatible Runtimes: ComfyUI-GGUF vs. stable-diffusion.cpp
- **ComfyUI-GGUF:** Supports loading GGUF DiT backbones via `UnetLoaderGGUF`. However, it requires running a Python/PyTorch server (~800 MB baseline) and specialized FLUX.2 loader nodes for the Qwen text encoder and `flux2-vae`.
- **stable-diffusion.cpp (`sd.cpp`):** Lightweight C++ implementation without Python overhead. However, native support for the FLUX.2 Klein multi-layer Qwen3 extraction pipeline is currently experimental and unverified on Windows AVX2.

### 2.5 Hardware Execution Reality on Intel Core i3-6100T
- **No CUDA Cores:** Compute executes entirely across 4 CPU threads via AVX2.
- **Estimated Latency:** [UNVERIFIED THEORETICAL ESTIMATE: 8 to 25 minutes per 512x512 image on CPU].
- **Memory Footprint:** Loading DiT (2.26 GB) + Qwen text encoder (~2.0 GB) + VAE (~0.35 GB) + diffusion scratch buffers requires **~6.5 to 8.5 GB RAM**. Concurrent execution alongside Windows (~3.1 GB) and KAATYA Main AI (~3.1 GB) pushes total memory close to the 12.0 GB ceiling.
- **Architectural Directive:**
  - **Local FLUX generation is strictly EXPERIMENTAL.**
  - **Do NOT download companion files** until an end-to-end runtime implementation is empirically tested and approved.
  - The production workflow relies on the **Authorized Online Diffusion Gate** (DALL-E 3, Stability AI, Fal.ai) with explicit human confirmation.

---

## 3. Status of Historical Image Model: Qwen Image 2.1

- **File Reference:** `qwen-image-2.1-step90000-Q4_K_M.gguf`
- **Audit Finding:** **CONFIRMED ABSENT.** This model does not exist on disk in `T:\ai creation`.
- **Architectural Action:** Removed from active inventory; preserved as an optional download target if the user later acquires it.

---

## 4. Online AI Image Provider Integration (Approval Required)

Because local diffusion on CPU is slow and memory-intensive, the Image Studio provides first-class support for authorized online providers.

### 4.1 Strict Approval Gate Before Every Generation
Before transmitting any request to an external provider:
1. **The Modal Displays:**
   - Target Provider (e.g., OpenAI DALL-E 3, Stability AI SD3, Ideogram v2).
   - Expanded Prompt (e.g., *"Futuristic desktop workstation, dark obsidian theme, electric cyan accents"*).
   - Target Aspect Ratio (1:1 Square, 16:9 Landscape, 9:16 Portrait).
   - Estimated Cost (e.g., `~$0.04 USD`).
2. **User Confirmation:** Requires an explicit click on `"Authorize Generation"`.
3. **Zero Covert Transmissions:** The application never generates images online silently.

### 4.2 Security & DPAPI Vault
- API keys are encrypted locally using Windows DPAPI (`CryptProtectData`).
- In-memory keys are scrubbed with `zeroize` immediately after HTTPS transmission.
- Generated images are downloaded directly into `.assistant/exports/images/` with full local metadata logging.
