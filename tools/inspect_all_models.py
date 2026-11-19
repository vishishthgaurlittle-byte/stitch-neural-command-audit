import os
import hashlib
import json
import struct

models = [
    r"T:\ai creation\Qwen3-4B-Q4_K_M.gguf",
    r"T:\ai creation\Qwen3-1.7B-Q3_K_M.gguf",
    r"T:\ai creation\SmolLM2-1.7B-Instruct-Q4_K_M.gguf",
    r"T:\ai creation\Qwen2.5-Coder-1.5B-Instruct-Q3_K_M.gguf",
    r"T:\ai creation\qwen2.5-1.5b-instruct-q4_k_m.gguf",
    r"T:\ai creation\flux-2-klein-4b-q4_0.gguf",
    r"T:\ai creation\Nemotron-3.5-Bolt-E4B-Q4_K_M.gguf",
    r"T:\ai creation\qwen3-embedding-0.6b-q8_0.gguf",
    r"T:\ai creation\ggml-base.bin",
    r"T:\ai creation\english voice onnx + jons\en_US-mike-medium.onnx",
    r"T:\ai creation\hindi voice onnx + jon\hi_IN-rohan-medium.onnx"
]

print("="*80)
print(f"{'FILENAME':<42} | {'SIZE (BYTES)':<14} | {'SIZE (GiB)':<10} | {'STATUS'}")
print("="*80)

for m in models:
    if os.path.exists(m):
        sz = os.path.getsize(m)
        gib = sz / (1024**3)
        print(f"{os.path.basename(m):<42} | {sz:<14} | {gib:<10.2f} | Confirmed Present")
    else:
        print(f"{os.path.basename(m):<42} | {'-':<14} | {'-':<10} | ABSENT")

# Check historical references
historical = [
    r"T:\ai creation\qwen-image-2.1-step90000-Q4_K_M.gguf",
    r"T:\ai creation\qwen2.5-coder-3b-instruct-q4_k_m.gguf",
    r"T:\ai creation\qwen2.5-coder-1.5b-instruct-q4_k_m.gguf",
    r"T:\ai creation\nomic-embed-text-v1.5.Q4_K_M.gguf"
]

print("\n=== HISTORICAL / ABSENT REFERENCES CHECK ===")
for h in historical:
    exists = os.path.exists(h)
    print(f"{os.path.basename(h):<42} | Present: {exists}")
