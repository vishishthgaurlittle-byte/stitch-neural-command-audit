import os
import re
import json
import csv
from html.parser import HTMLParser

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

class StitchHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.buttons = []
        self.inputs = []
        self.links = []
        self.images = []
        self.scripts = []
        self.headings = []
        self.current_tag = None
        self.current_attrs = {}
        self.current_text = []
        self.in_script = False
        self.script_content = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attr_dict = dict(attrs)
        self.current_attrs = attr_dict
        self.tags.append(tag)
        
        if tag == "script":
            self.in_script = True
            self.script_content = []
            if "src" in attr_dict:
                self.scripts.append({"type": "external", "src": attr_dict["src"]})
        elif tag == "button":
            self.buttons.append({"attrs": attr_dict, "text": ""})
        elif tag in ["input", "textarea", "select"]:
            self.inputs.append({"tag": tag, "attrs": attr_dict})
        elif tag == "a":
            self.links.append({"attrs": attr_dict, "text": ""})
        elif tag == "img":
            self.images.append(attr_dict)
        elif tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            self.headings.append({"tag": tag, "text": "", "attrs": attr_dict})

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
            code = "".join(self.script_content).strip()
            if code:
                self.scripts.append({"type": "inline", "code": code})
        self.current_tag = None
        self.current_attrs = {}

    def handle_data(self, data):
        text = data.strip()
        if self.in_script:
            self.script_content.append(data)
        elif text:
            if self.buttons and self.current_tag == "button":
                self.buttons[-1]["text"] += (" " + text if self.buttons[-1]["text"] else text)
            elif self.links and self.current_tag == "a":
                self.links[-1]["text"] += (" " + text if self.links[-1]["text"] else text)
            elif self.headings and self.current_tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                self.headings[-1]["text"] += (" " + text if self.headings[-1]["text"] else text)

results = {}
for s_dir, s_name in screens:
    html_path = os.path.join(stitch_dir, s_dir, "code.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
            parser = StitchHTMLParser()
            parser.feed(content)
            results[s_dir] = {
                "name": s_name,
                "file_size": len(content),
                "buttons_count": len(parser.buttons),
                "inputs_count": len(parser.inputs),
                "links_count": len(parser.links),
                "images_count": len(parser.images),
                "headings_count": len(parser.headings),
                "scripts_count": len(parser.scripts),
                "buttons_sample": parser.buttons[:10],
                "inputs_sample": parser.inputs[:10],
                "headings": parser.headings[:10],
                "external_scripts": [s["src"] for s in parser.scripts if s["type"] == "external"],
                "has_inline_js": any(s["type"] == "inline" and not s.get("attrs", {}).get("id") == "tailwind-config" for s in parser.scripts if s["type"] == "inline"),
                "images": parser.images
            }

print(f"Parsed {len(results)} screens successfully!")
for s_dir, data in results.items():
    print(f"{data['name']}: {data['file_size']} bytes | {data['buttons_count']} buttons, {data['inputs_count']} inputs, {data['headings_count']} headings, {data['images_count']} images")

with open(os.path.join(audit_dir, "parsed_screens_summary.json"), "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)
