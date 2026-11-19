import os
import re
import json

stitch_dir = r"T:\ai creation\stitch_neural_command_desktop_os"

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

screen_details = {}

for s in screens:
    p = os.path.join(stitch_dir, s, "code.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract <main> content
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    main_content = main_match.group(1) if main_match else html

    # Clean text in main
    no_tags = re.sub(r'<script.*?</script>', '', main_content, flags=re.DOTALL)
    no_tags = re.sub(r'<style.*?</style>', '', no_tags, flags=re.DOTALL)
    text_content = re.sub(r'<[^>]+>', '\n', no_tags)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in text_content.splitlines() if l.strip()]

    # Extract all section titles / h1-h4 in main
    headings = re.findall(r'<(h[1-6])[^>]*>(.*?)</\1>', main_content, re.DOTALL)
    clean_headings = [re.sub(r'<[^>]+>', '', h[1]).strip() for h in headings]

    # Extract buttons in main
    buttons = re.findall(r'<button[^>]*>(.*?)</button>', main_content, re.DOTALL)
    clean_buttons = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', b)).strip() for b in buttons]

    # Extract inputs in main
    inputs = re.findall(r'<(input|textarea|select)[^>]*placeholder=["\']([^"\']*)["\']', main_content)

    screen_details[s] = {
        "headings": clean_headings,
        "button_count": len(clean_buttons),
        "buttons_sample": clean_buttons[:15],
        "inputs": inputs,
        "text_summary": lines[:60]
    }

with open(r"T:\ai creation\STITCH_DESIGN_AUDIT\screen_main_details.json", "w", encoding="utf-8") as out:
    json.dump(screen_details, out, indent=2)

print("Screen main details extracted successfully!")
