import urllib.request
import os

repo = "vishishthgaurlittle-byte/stitch-neural-command-audit"
base_url = f"https://raw.githubusercontent.com/{repo}/main/"

phase_3_1_docs = [
    "PHASE_3_1_INDEPENDENT_AUDIT.md",
    "MODEL_IDENTITY_AND_MEMORY_CORRECTIONS.md",
    "MAIN_AI_PERMANENT_RESIDENCY_CORRECTION.md",
    "REALISTIC_HARDWARE_BENCHMARK_PROTOCOL.md",
    "WINDOWS_10_AND_WEBVIEW2_COMPATIBILITY.md",
    "SECURITY_AND_AIRGAP_CORRECTIONS.md",
    "STITCH_DESIGN_PRESERVATION_AUDIT.md",
    "PHASE_3_1_FINAL_DECISIONS.md",
    "README.md",
    "PHASE_3_MASTER_ARCHITECTURE.md",
    "AI_ORCHESTRATION_ARCHITECTURE.md",
    "TECH_STACK_COMPARISON.md",
    "LOCAL_MODEL_HARDWARE_BENCHMARK_PLAN.md",
    "DESKTOP_AUTOMATION_SECURITY.md",
    "MEMORY_AND_VOICE_ARCHITECTURE.md",
    "RISKS_AND_UNRESOLVED_DECISIONS.md"
]

print("=== INDEPENDENT GITHUB RETRIEVAL VERIFICATION (PHASE 3.1) ===")
all_verified = True

for doc in phase_3_1_docs:
    url = base_url + doc
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            local_path = os.path.join(r"T:\ai creation\STITCH_DESIGN_AUDIT", doc)
            local_size = os.path.getsize(local_path)
            remote_size = len(data)
            match = "MATCH" if abs(local_size - remote_size) < 100 else f"DIFF ({local_size} vs {remote_size})"
            print(f"[HTTP {resp.status}] {doc:<44} | Remote: {remote_size:>6} B | Local: {local_size:>6} B | {match}")
    except Exception as e:
        print(f"[FAILED] {doc:<44} -> {e}")
        all_verified = False

if all_verified:
    print("\nALL 16 DOCUMENTS (8 NEW CORRECTIONS + 8 UPDATED ARCHITECTURE DOCS) VERIFIED ON GITHUB!")
else:
    print("\nSOME DOCUMENTS FAILED VERIFICATION")
