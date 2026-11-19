import os
import re
import json

stitch_dir = r"T:\ai creation\stitch_neural_command_desktop_os"
audit_dir = r"T:\ai creation\STITCH_DESIGN_AUDIT"

screens = [
    ("screen_01_command_center", "01. Command Center"),
    ("screen_02_conversation_workspace", "02. Conversation Workspace"),
    ("screen_03_3d_neural_core", "03. 3D Neural Core"),
    ("screen_04_intelligence_ai_models", "04. Intelligence & AI Models"),
    ("screen_05_plugin_centre", "05. Plugin Centre"),
    ("screen_06_agent_workspace", "06. Agent Workspace"),
    ("screen_07_workflow_builder", "07. Workflow Builder"),
    ("screen_08_pc_control_centre", "08. PC Control Centre"),
    ("screen_09_memory_centre", "09. Memory Centre"),
    ("screen_10_voice_personality_studio", "10. Voice & Personality Studio"),
    ("screen_11_tasks_activity", "11. Tasks & Activity"),
    ("screen_12_system_monitor", "12. System Monitor"),
    ("screen_13_security_permissions", "13. Security & Permissions"),
    ("screen_14_settings", "14. Settings"),
    ("screen_15_floating_ai_hud", "15. Floating AI HUD"),
]

deep_audit = {}

for s_dir, s_name in screens:
    p = os.path.join(stitch_dir, s_dir, "code.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract all data-path links or hrefs
    nav_links = re.findall(r'data-path=["\']([^"\']+)["\']', html)
    href_links = re.findall(r'href=["\']([^"\']+)["\']', html)
    
    # Extract buttons with their text and classes
    button_matches = re.findall(r'<button([^>]*)>(.*?)</button>', html, re.DOTALL)
    buttons = []
    for attrs, btext in button_matches:
        # clean html tags from text
        clean_text = re.sub(r'<[^>]+>', ' ', btext).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        buttons.append({"attrs": attrs.strip(), "text": clean_text})

    # Extract inputs
    input_matches = re.findall(r'<(input|textarea|select)([^>]*)>', html)
    inputs = []
    for itag, iattrs in input_matches:
        inputs.append({"tag": itag, "attrs": iattrs.strip()})

    # Extract headings
    heading_matches = re.findall(r'<(h[1-6])([^>]*)>(.*?)</\1>', html, re.DOTALL)
    headings = []
    for htag, hattrs, htext in heading_matches:
        clean_htext = re.sub(r'<[^>]+>', ' ', htext).strip()
        clean_htext = re.sub(r'\s+', ' ', clean_htext)
        headings.append({"tag": htag, "text": clean_htext})

    # Check for visual elements (canvas, svg, badges, etc.)
    has_canvas = "<canvas" in html
    has_svg = "<svg" in html
    svg_count = len(re.findall(r'<svg', html))
    
    # Check script content
    script_blocks = re.findall(r'<script(?![^>]*src)(?![^>]*id=["\']tailwind-config["\'])[^>]*>(.*?)</script>', html, re.DOTALL)
    clean_scripts = [s.strip() for s in script_blocks if s.strip()]

    # Extract all external asset links
    external_assets = re.findall(r'(?:src|href)=["\'](https?://[^"\']+)["\']', html)

    deep_audit[s_dir] = {
        "name": s_name,
        "nav_links": list(set(nav_links)),
        "buttons": buttons,
        "inputs": inputs,
        "headings": headings,
        "has_canvas": has_canvas,
        "has_svg": has_svg,
        "svg_count": svg_count,
        "script_snippets": clean_scripts,
        "external_assets": list(set(external_assets))
    }

with open(os.path.join(audit_dir, "deep_screen_analysis.json"), "w", encoding="utf-8") as out:
    json.dump(deep_audit, out, indent=2)

print("Deep screen analysis saved to deep_screen_analysis.json!")
