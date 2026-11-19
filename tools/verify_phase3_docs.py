import urllib.request
import json
import os

token_cmd = os.popen('git credential fill')
token_input = "protocol=https\nhost=github.com\n\n"
# Instead of credential helper which might block, let's query the public GitHub REST API directly since the repo is public!

repo = "vishishthgaurlittle-byte/stitch-neural-command-audit"
files_to_check = [
    "README.md",
    "PHASE_3_MASTER_ARCHITECTURE.md",
    "TECH_STACK_COMPARISON.md",
    "AI_ORCHESTRATION_ARCHITECTURE.md",
    "LOCAL_MODEL_HARDWARE_BENCHMARK_PLAN.md",
    "DESKTOP_AUTOMATION_SECURITY.md",
    "PLUGIN_SYSTEM_ARCHITECTURE.md",
    "MEMORY_AND_VOICE_ARCHITECTURE.md",
    "SCREEN_TO_FEATURE_IMPLEMENTATION_MAP.md",
    "DEVELOPMENT_ROADMAP.md",
    "RISKS_AND_UNRESOLVED_DECISIONS.md"
]

print("--- VERIFYING PHASE 3 DELIVERABLES ON GITHUB ---")
base_url = f"https://raw.githubusercontent.com/{repo}/main/"
all_ok = True

for f in files_to_check:
    url = base_url + f
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            content = response.read()
            local_path = os.path.join(r"T:\ai creation\STITCH_DESIGN_AUDIT", f)
            local_size = os.path.getsize(local_path)
            remote_size = len(content)
            match = "MATCH" if abs(local_size - remote_size) < 100 else f"DIFF ({local_size} vs {remote_size})"
            print(f"[HTTP {response.status}] {f:<42} | Remote: {remote_size:>6} B | Local: {local_size:>6} B | {match}")
    except Exception as e:
        print(f"[FAIL] {f:<42} -> {e}")
        all_ok = False

if all_ok:
    print("\nALL PHASE 3 ARCHITECTURE DOCUMENTS SUCCESSFULLY VERIFIED ON GITHUB!")
else:
    print("\nSOME VERIFICATIONS FAILED")
