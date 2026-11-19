import os
import re
import json

stitch_dir = r"T:\ai creation\stitch_neural_command_desktop_os"

def examine(screen_id):
    p = os.path.join(stitch_dir, screen_id, "code.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    return html

# 1. Examine Screen 01 (Command Center)
html_01 = examine("screen_01_command_center")
print("=== Screen 01: Command Center ===")
print("Cards / Sections:")
for h in re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html_01):
    print(" ", re.sub(r'<[^>]+>', '', h).strip())

# 2. Examine Screen 03 (Neural Core)
html_03 = examine("screen_03_3d_neural_core")
print("\n=== Screen 03: Neural Core ===")
print("Nodes found in HTML:")
nodes = re.findall(r'class="[^"]*(?:node|card|cluster)[^"]*"[^>]*>(.*?)</(?:div|g|section)>', html_03, re.DOTALL)
print("Has SVG graph elements:", len(re.findall(r'<circle|<line|<path|<rect', html_03)))
for n in re.findall(r'<text[^>]*>(.*?)</text>', html_03)[:10]:
    print("  SVG Text node:", n.strip())

# 3. Examine Screen 04 (Intelligence & AI Models)
html_04 = examine("screen_04_intelligence_ai_models")
print("\n=== Screen 04: Intelligence & AI Models ===")
for m in re.findall(r'<h[3-5][^>]*>(.*?)</h[3-5]>', html_04)[:15]:
    print("  Model/Section:", re.sub(r'<[^>]+>', '', m).strip())

# 4. Examine Screen 05 (Plugin Centre)
html_05 = examine("screen_05_plugin_centre")
print("\n=== Screen 05: Plugin Centre ===")
for p_title in re.findall(r'<h[3-5][^>]*>(.*?)</h[3-5]>', html_05)[:15]:
    print("  Plugin/Section:", re.sub(r'<[^>]+>', '', p_title).strip())

# 5. Examine Screen 06 (Agent Workspace)
html_06 = examine("screen_06_agent_workspace")
print("\n=== Screen 06: Agent Workspace ===")
for a_title in re.findall(r'<h[3-5][^>]*>(.*?)</h[3-5]>', html_06)[:25]:
    print("  Agent/Card:", re.sub(r'<[^>]+>', '', a_title).strip())
