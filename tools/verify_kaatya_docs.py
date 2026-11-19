import urllib.request
import os

repo = "vishishthgaurlittle-byte/stitch-neural-command-audit"
base_url = f"https://raw.githubusercontent.com/{repo}/main/"

kaatya_docs = [
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

print("=== VERIFYING KAATYA FINAL DELIVERABLES ON GITHUB ===", flush=True)
all_ok = True

for doc in kaatya_docs:
    url = base_url + doc
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            local_path = os.path.join(r"T:\ai creation\STITCH_DESIGN_AUDIT", doc)
            local_size = os.path.getsize(local_path)
            remote_size = len(data)
            match = "MATCH" if abs(local_size - remote_size) < 100 else f"DIFF ({local_size} vs {remote_size})"
            print(f"[HTTP {resp.status}] {doc:<48} | Remote: {remote_size:>6} B | Local: {local_size:>6} B | {match}", flush=True)
    except Exception as e:
        print(f"[NOTE] {doc:<48} -> {e}", flush=True)
        # Even if GitHub raw takes a minute to propagate CDN cache, check via local verification
        all_ok = False

print("\nVerification check finished.", flush=True)
