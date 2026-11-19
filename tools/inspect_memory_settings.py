import os
import re

for s in ["screen_09_memory_centre", "screen_14_settings"]:
    p = os.path.join(r"T:\ai creation\stitch_neural_command_desktop_os", s, "code.html")
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    print(f"\n{'='*60}\nSCREEN: {s}")
    headings = re.findall(r'<h[1-5][^>]*>(.*?)</h[1-5]>', html)
    for h in headings:
        print("  Heading:", re.sub(r'<[^>]+>', '', h).strip())
    
    # Check features for memory
    if "memory" in s:
        for f_name in ["library", "search", "category", "graph", "project", "related", "pin", "edit", "archive", "delete", "export", "import", "privacy", "source"]:
            print(f"    Memory {f_name}: {len(re.findall(f_name, html, re.IGNORECASE))} matches")
            
    # Check settings categories
    if "settings" in s:
        settings_cats = ["general", "ai behaviour", "models", "online providers", "plugins", "agents", "voice", "memory", "appearance", "performance", "storage", "privacy", "security", "about"]
        for c in settings_cats:
            print(f"    Settings Category '{c}': {'FOUND' if c in html.lower() else 'MISSING'}")
