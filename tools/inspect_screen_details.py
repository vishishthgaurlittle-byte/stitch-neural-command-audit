import os
import re
import json

stitch_dir = r"T:\ai creation\stitch_neural_command_desktop_os"

def analyze_screen(s_dir):
    p = os.path.join(stitch_dir, s_dir, "code.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Strip style and script for clean text analysis
    no_script = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    no_style = re.sub(r'<style.*?</style>', '', no_script, flags=re.DOTALL)
    
    # Extract text snippets
    text_content = re.sub(r'<[^>]+>', '\n', no_style)
    lines = [l.strip() for l in text_content.splitlines() if l.strip()]
    
    # Find all data-path
    paths = re.findall(r'data-path=["\']([^"\']+)["\']', html)
    
    # Find all ids and classes of main sections
    sections = re.findall(r'<section[^>]*>(.*?)</section>', html, re.DOTALL)
    
    return {
        "lines_sample": lines[:80],
        "all_lines": lines,
        "paths": list(set(paths)),
        "section_count": len(sections)
    }

screens = [
    "screen_01_command_center",
    "screen_02_conversation_workspace",
    "screen_03_3d_neural_core",
    "screen_04_intelligence_ai_models",
    "screen_05_plugin_centre",
    "screen_06_agent_workspace",
    "screen_07_workflow_builder",
    "screen_08_pc_control_centre",
    "screen_09_memory_centre",
    "screen_10_voice_personality_studio",
    "screen_11_tasks_activity",
    "screen_12_system_monitor",
    "screen_13_security_permissions",
    "screen_14_settings",
    "screen_15_floating_ai_hud"
]

report = {}
for s in screens:
    data = analyze_screen(s)
    report[s] = {
        "paths": data["paths"],
        "section_count": data["section_count"],
        "sample": data["lines_sample"][:25]
    }
    print(f"\n{'='*60}\nSCREEN: {s}\nPaths: {data['paths']}")
    print("Sample lines:")
    for l in data["lines_sample"][:15]:
        print(f"  - {l}")

with open(r"T:\ai creation\STITCH_DESIGN_AUDIT\screen_text_analysis.json", "w", encoding="utf-8") as out:
    json.dump(report, out, indent=2)
