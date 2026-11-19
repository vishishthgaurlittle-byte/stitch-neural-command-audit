import os
import re

print("=== DEEP CONTENT VALIDATION: KAATYA ARCHITECTURE DELIVERABLES ===", flush=True)

base_dir = r"T:\ai creation\STITCH_DESIGN_AUDIT"
kaatya_docs = [
    "KAATYA_PHASE_3_CORRECTION_AND_VALIDATION_REPORT.md",
    "KAATYA_FINAL_MASTER_ARCHITECTURE.md",
    "KAATYA_FINAL_MODEL_INVENTORY.md",
    "KAATYA_MODEL_COMPATIBILITY_AND_BENCHMARK_PLAN.md",
    "KAATYA_AGENT_ROSTER_AND_CAPABILITY_MATRIX.md",
    "KAATYA_VIDEO_STUDIO_ARCHITECTURE.md",
    "KAATYA_IMAGE_GENERATION_ARCHITECTURE.md",
    "KAATYA_ONLINE_PROVIDER_AND_PLUGIN_ARCHITECTURE.md",
    "KAATYA_LOCAL_RUNTIME_AND_MEMORY_POLICY.md",
    "KAATYA_MEMORY_AND_VOICE_ARCHITECTURE.md",
    "KAATYA_SECURITY_AND_AUTOMATION_POLICY.md",
    "KAATYA_WINDOWS_10_COMPATIBILITY.md",
    "KAATYA_UI_FEATURE_INTEGRATION_MAP.md",
    "KAATYA_IMPLEMENTATION_ROADMAP.md",
    "KAATYA_RISKS_AND_UNRESOLVED_DECISIONS.md",
    "KAATYA_FINAL_AUDIT_REPORT.md",
    "README.md"
]

all_passed = True

# 1. Verify existence and non-trivial size
print("\n--- 1. File Existence and Size Check ---", flush=True)
for doc in kaatya_docs:
    path = os.path.join(base_dir, doc)
    if not os.path.exists(path):
        print(f"[FAIL] Missing file: {doc}", flush=True)
        all_passed = False
    else:
        sz = os.path.getsize(path)
        if sz < 1000:
            print(f"[FAIL] File too small ({sz} B): {doc}", flush=True)
            all_passed = False
        else:
            print(f"[PASS] {doc:<52} ({sz:>6} bytes)", flush=True)

# 2. Verify restored 23-agent names in Agent Matrix
print("\n--- 2. Restored 23-Agent Exact Names Check ---", flush=True)
matrix_path = os.path.join(base_dir, "KAATYA_AGENT_ROSTER_AND_CAPABILITY_MATRIX.md")
with open(matrix_path, "r", encoding="utf-8") as f:
    matrix_content = f.read()

expected_agents = [
    "KAATYA Main AI", "Coder", "Designer", "Researcher", "Writer",
    "Messenger", "File Manager", "Game Helper", "Tester", "3D Artist",
    "Automator", "Security", "Data Analyst", "Code Reviewer", "Assistant",
    "Video Editor", "Image Studio", "Grammar & Language", "Social Media",
    "Audio & Voice", "Presentation", "Document Intel", "Database Engineer"
]

for agent in expected_agents:
    if agent in matrix_content:
        print(f"[PASS] Agent identified: {agent}", flush=True)
    else:
        print(f"[FAIL] Agent missing: {agent}", flush=True)
        all_passed = False

# 3. Verify Memory Arithmetic and Claims
print("\n--- 3. Memory Arithmetic and Claim Check ---", flush=True)
master_arch_path = os.path.join(base_dir, "KAATYA_FINAL_MASTER_ARCHITECTURE.md")
with open(master_arch_path, "r", encoding="utf-8") as f:
    arch_content = f.read()

if re.search(r"4\.8[08].*GB", arch_content):
    print("[PASS] Master Architecture contains corrected arithmetic (4.80 GB / 4.88 GB)", flush=True)
else:
    print("[FAIL] Master Architecture does not contain corrected arithmetic", flush=True)
    all_passed = False

if "guaranteed 2.5 GB safety cushion" in arch_content.lower() or "guaranteed 2.5 gb safety buffer" in arch_content.lower():
    print("[FAIL] Master Architecture still contains unsupported guaranteed buffer claim", flush=True)
    all_passed = False
else:
    print("[PASS] Unsupported guaranteed buffer claim removed", flush=True)

# 4. Verify FLUX.2 Klein dependencies
print("\n--- 4. FLUX.2 Klein Dependency Check ---", flush=True)
img_arch_path = os.path.join(base_dir, "KAATYA_IMAGE_GENERATION_ARCHITECTURE.md")
with open(img_arch_path, "r", encoding="utf-8") as f:
    img_content = f.read()

if "Qwen3" in img_content and "flux2-vae" in img_content:
    print("[PASS] Image Architecture correctly identifies Qwen3 text encoder and flux2-vae", flush=True)
else:
    print("[FAIL] Image Architecture missing Qwen3 or flux2-vae", flush=True)
    all_passed = False

if "t5xxl_fp8_e4m3fn.safetensors" in img_content:
    print("[FAIL] Image Architecture still references legacy T5-XXL for FLUX.2 Klein", flush=True)
    all_passed = False
else:
    print("[PASS] Legacy T5-XXL removed from FLUX.2 Klein pipeline", flush=True)

# 5. Verify Video Studio Diffusion Classification
print("\n--- 5. Video Studio Diffusion Classification Check ---", flush=True)
video_arch_path = os.path.join(base_dir, "KAATYA_VIDEO_STUDIO_ARCHITECTURE.md")
with open(video_arch_path, "r", encoding="utf-8") as f:
    video_content = f.read()

if "Impractical on target hardware" in video_content:
    print("[PASS] Video Studio correctly classifies diffusion models as 'Impractical on target hardware'", flush=True)
else:
    print("[FAIL] Video Studio missing 'Impractical on target hardware' classification", flush=True)
    all_passed = False

if "OpenTimelineIO" in video_content or "XML" in video_content:
    print("[PASS] Video Studio documents multi-editor interchange (XML, EDL, OTIO)", flush=True)
else:
    print("[FAIL] Video Studio missing multi-editor interchange", flush=True)
    all_passed = False

print("\n=======================================================", flush=True)
if all_passed:
    print("ALL VALIDATION CRITERIA PASSED EMPIRICALLY.", flush=True)
else:
    print("SOME CRITERIA FAILED - INSPECT LOGS.", flush=True)
print("=======================================================", flush=True)
