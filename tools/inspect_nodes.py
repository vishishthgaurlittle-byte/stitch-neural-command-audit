import os
import re

p = r"T:\ai creation\stitch_neural_command_desktop_os\screen_03_3d_neural_core\code.html"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'<svg[^>]*id=["\']topoCanvas["\'][^>]*>(.*?)</svg>', text, re.DOTALL)
if m:
    svg = m.group(1)
    texts = re.findall(r'<text[^>]*>(.*?)</text>', svg)
    print("All Node Labels in SVG Neural Core:")
    for t in texts:
        print("  *", t.strip())
        
    circles = re.findall(r'<circle[^>]*>', svg)
    print(f"Total circles: {len(circles)}")
    
    paths = re.findall(r'<path[^>]*>', svg)
    print(f"Total paths / connection lines: {len(paths)}")
