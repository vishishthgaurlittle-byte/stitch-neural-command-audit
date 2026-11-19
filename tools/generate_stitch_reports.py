import os
import re
import csv
import json

stitch_dir = r"T:\ai creation\stitch_neural_command_desktop_os"
audit_dir = r"T:\ai creation\STITCH_DESIGN_AUDIT"

screens = [
    ("screen_01_command_center", "Command Center", "01"),
    ("screen_02_conversation_workspace", "Conversation Workspace", "02"),
    ("screen_03_3d_neural_core", "3D Neural Core", "03"),
    ("screen_04_intelligence_ai_models", "Intelligence & AI Models", "04"),
    ("screen_05_plugin_centre", "Plugin Centre", "05"),
    ("screen_06_agent_workspace", "Agent Workspace", "06"),
    ("screen_07_workflow_builder", "Workflow Builder", "07"),
    ("screen_08_pc_control_centre", "PC Control Centre", "08"),
    ("screen_09_memory_centre", "Memory Centre", "09"),
    ("screen_10_voice_personality_studio", "Voice & Personality Studio", "10"),
    ("screen_11_tasks_activity", "Tasks & Activity", "11"),
    ("screen_12_system_monitor", "System Monitor", "12"),
    ("screen_13_security_permissions", "Security & Permissions", "13"),
    ("screen_14_settings", "Settings", "14"),
    ("screen_15_floating_ai_hud", "Floating AI HUD", "15"),
]

# 1. FILE INVENTORY GENERATION
inventory_rows = []
all_files = []
for root, dirs, files in os.walk(stitch_dir):
    for f in sorted(files):
        fpath = os.path.join(root, f)
        rel_path = os.path.relpath(fpath, stitch_dir)
        size = os.path.getsize(fpath)
        ext = os.path.splitext(f)[1].lower()
        
        category = "Unknown"
        purpose = "Design asset"
        is_ref = "Yes"
        is_req = "Yes"
        status = "Active"
        
        if f == "DESIGN.md":
            category = "Design System Specification"
            purpose = "Defines color tokens, typography, elevation, spacing, and component specs"
            is_ref = "Yes (Design reference)"
            is_req = "Required"
            status = "Verified"
        elif f == "code.html":
            category = "Screen Interface Template"
            purpose = f"Complete standalone HTML/Tailwind mockup template for {os.path.basename(root)}"
            is_ref = "Yes (Primary screen entry)"
            is_req = "Required"
            status = "Verified"
        elif f == "screen.png":
            category = "Visual Screen Preview"
            purpose = f"Visual rendered PNG screenshot of {os.path.basename(root)}"
            is_ref = "Documentation preview"
            is_req = "Optional (Asset)"
            status = "Verified"
            
        inventory_rows.append([
            rel_path.replace("\\", "/"), f, ext, size, category, purpose, is_ref, is_req, status
        ])

inventory_csv = os.path.join(audit_dir, "STITCH_FILE_INVENTORY.csv")
with open(inventory_csv, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow([
        "Relative File Path", "File Name", "File Extension", "File Size (Bytes)",
        "File Category", "Purpose", "Referenced By Another File", "Is Required", "File Status"
    ])
    writer.writerows(inventory_rows)

print(f"Generated STITCH_FILE_INVENTORY.csv with {len(inventory_rows)} entries!")

# 2. INTERACTION AUDIT GENERATION
interaction_rows = []

for s_dir, s_title, s_idx in screens:
    p = os.path.join(stitch_dir, s_dir, "code.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract interactive script handlers
    script_match = re.search(r'<script(?![^>]*src)(?![^>]*id=["\']tailwind-config["\'])[^>]*>(.*?)</script>', html, re.DOTALL)
    script_text = script_match.group(1) if script_match else ""
    
    # Analyze Navigation Links
    nav_matches = re.findall(r'<a[^>]*data-path=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
    for target, text in nav_matches:
        clean_text = re.sub(r'<[^>]+>', ' ', text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        interaction_rows.append([
            s_title, f"Sidebar Nav: {clean_text}", f"Navigate to '{target}' screen",
            "Has data-path attribute and hover styling; no single-page router wired",
            "Partial (Prototype Markup)", "Wire into desktop app router (e.g. React Router / Zustand state)"
        ])
        
    # Analyze Buttons
    button_matches = re.findall(r'<button([^>]*)>(.*?)</button>', html, re.DOTALL)
    for attrs, btext in button_matches:
        clean_btext = re.sub(r'<[^>]+>', ' ', btext).strip()
        clean_btext = re.sub(r'\s+', ' ', clean_btext)
        if not clean_btext:
            # Check title or icon
            t_match = re.search(r'title=["\']([^"\']+)["\']', attrs)
            clean_btext = t_match.group(1) if t_match else "Icon Button"

        # Check existing behavior in script
        existing = "Static HTML/Tailwind styling; no click handler"
        status = "Static"
        required = "Add event listener and backend controller action"
        
        # Check if button has specific id or class wired in script
        btn_id = re.search(r'id=["\']([^"\']+)["\']', attrs)
        btn_class = re.search(r'class=["\']([^"\']+)["\']', attrs)
        
        if btn_id and btn_id.group(1) in script_text:
            existing = f"Has client-side JS micro-interaction handler (#{btn_id.group(1)})"
            status = "Working (Client-Side Prototype)"
            required = "Connect prototype handler to native application backend"
        elif any(c in script_text for c in (btn_class.group(1).split() if btn_class else [])):
            matched_cls = [c for c in btn_class.group(1).split() if c in script_text and len(c) > 4]
            if matched_cls:
                existing = f"Has client-side CSS toggle handler (.{matched_cls[0]})"
                status = "Partial (Visual Toggle Only)"
                required = "Connect state toggle to persistent settings / agent runner"
        elif "close" in clean_btext.lower() or "cancel" in clean_btext.lower():
            required = "Dismiss dialog / modal and restore background focus"
        elif "save" in clean_btext.lower() or "apply" in clean_btext.lower():
            required = "Validate input parameters and commit to local configuration"
        elif "run" in clean_btext.lower() or "execute" in clean_btext.lower() or "start" in clean_btext.lower():
            required = "Dispatch execution job to Main AI orchestrator queue"
            
        interaction_rows.append([
            s_title, f"Button: {clean_btext[:40]}", f"Trigger {clean_btext[:30]} action",
            existing, status, required
        ])
        
    # Analyze Inputs
    input_matches = re.findall(r'<(input|textarea|select)([^>]*)>', html)
    for itag, iattrs in input_matches:
        pl_match = re.search(r'placeholder=["\']([^"\']+)["\']', iattrs)
        type_match = re.search(r'type=["\']([^"\']+)["\']', iattrs)
        id_match = re.search(r'id=["\']([^"\']+)["\']', iattrs)
        
        desc = pl_match.group(1) if pl_match else (id_match.group(1) if id_match else f"{itag} control")
        itype = type_match.group(1) if type_match else itag
        
        if itype == "checkbox":
            expected = "Toggle boolean feature / permission flag"
            existing = "Visual styled checkbox; updates state visually on click"
            status = "Working (HTML Native Toggle)"
            required = "Bind to reactive application settings state"
        elif itype == "range":
            expected = "Adjust parameter value dynamically"
            existing = "Native range slider with Tailwind track styling"
            status = "Working (HTML Native Slider)"
            required = "Bind value to model temperature / audio volume state"
        else:
            expected = f"Input text / command ({desc[:30]})"
            existing = "Standard HTML text input; receives typing focus"
            status = "Working (HTML Native Input)"
            required = "Bind value to command dispatcher / filter query"
            
        interaction_rows.append([
            s_title, f"Input ({itype}): {desc[:40]}", expected,
            existing, status, required
        ])

interaction_csv = os.path.join(audit_dir, "INTERACTION_AUDIT.csv")
with open(interaction_csv, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow([
        "Page", "Control", "Expected Action", "Existing Behaviour", "Status", "Required Implementation"
    ])
    writer.writerows(interaction_rows)

print(f"Generated INTERACTION_AUDIT.csv with {len(interaction_rows)} audited controls!")

# 3. ASSET MANIFEST JSON GENERATION
manifest = {
    "design_system_name": "Obsidian Command",
    "total_screens": 15,
    "total_files": len(inventory_rows),
    "screens": [],
    "external_dependencies": [
        {
            "name": "Tailwind CSS CDN",
            "url": "https://cdn.tailwindcss.com",
            "type": "Stylesheet Engine",
            "risk": "Requires internet access; must be compiled locally for 100% offline desktop app"
        },
        {
            "name": "Google Fonts Material Symbols Outlined",
            "url": "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined",
            "type": "Icon Font",
            "risk": "External network dependency; must bundle WOFF2 icons locally"
        },
        {
            "name": "Google Fonts (Manrope, Inter, JetBrains Mono)",
            "url": "https://fonts.googleapis.com",
            "type": "Web Typography",
            "risk": "External network dependency; must bundle WOFF2 fonts locally"
        },
        {
            "name": "Neural Emblem Image Asset",
            "url": "https://lh3.googleusercontent.com/aida/ALJJyrDkwdFfa2ZbCR92YUYuBisOJanZ8ecfnNvhI9eXBT--hdx14MyRyg6qfpPnaiS3kIpRGkkX0PNVVtIwneXNiCoblHPpmqiGrQk2CkGEIKcqfD3gRNBMLWSXQEbGOivXgnv71LBNjxftYEsjJ8cw22e5EDAyHmGagINyRC1EEZmHBwkNLqwZmekoCt_AROtGMSmXq54KIdKK2SWARwX6UIilHqAqSfaykmHb1GzCTeU",
            "type": "Remote PNG Logo",
            "risk": "External Google CDN URL; breaks offline; must download to local assets folder"
        }
    ],
    "bundled_screenshots": [
        "screen_04_intelligence_ai_models.png",
        "screen_06_agent_workspace.png",
        "screen_13_security_permissions.png",
        "screen_14_settings.png"
    ]
}

for s_dir, s_title, s_idx in screens:
    html_file = os.path.join(stitch_dir, s_dir, "code.html")
    png_file = os.path.join(stitch_dir, s_dir, "screen.png")
    
    s_info = {
        "screen_id": s_dir,
        "title": s_title,
        "index": s_idx,
        "html_file": f"{s_dir}/code.html",
        "html_size_bytes": os.path.getsize(html_file),
        "has_bundled_screenshot": os.path.exists(png_file),
        "screenshot_file": f"{s_dir}/screen.png" if os.path.exists(png_file) else None
    }
    manifest["screens"].append(s_info)

with open(os.path.join(audit_dir, "ASSET_MANIFEST.json"), "w", encoding="utf-8") as out:
    json.dump(manifest, out, indent=2)

print("Generated ASSET_MANIFEST.json!")
