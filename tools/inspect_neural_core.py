import os
import re

p = r"T:\ai creation\stitch_neural_command_desktop_os\screen_03_3d_neural_core\code.html"
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

svg_match = re.search(r'<svg[^>]*>(.*?)</svg>', html, re.DOTALL)
if svg_match:
    svg_content = svg_match.group(1)
    print("SVG graph found! Length:", len(svg_content))
    print("Circles (nodes):", len(re.findall(r'<circle', svg_content)))
    print("Lines (edges):", len(re.findall(r'<line', svg_content)))
    print("Paths:", len(re.findall(r'<path', svg_content)))
    print("Texts:", len(re.findall(r'<text', svg_content)))
    print("Sample nodes:")
    for t in re.findall(r'<text[^>]*>(.*?)</text>', svg_content)[:12]:
        print("  Node text:", t.strip())

# Check for 2D/3D controls
print("\nControls in screen 03:")
for c in ["2d", "3d", "zoom", "camera", "filter", "cluster", "orbit", "reset", "physics", "simulation"]:
    matches = len(re.findall(c, html, re.IGNORECASE))
    print(f"  {c}: {matches} matches")
