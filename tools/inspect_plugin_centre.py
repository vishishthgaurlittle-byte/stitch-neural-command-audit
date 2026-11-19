import os
import re

p = r"T:\ai creation\stitch_neural_command_desktop_os\screen_05_plugin_centre\code.html"
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

headings = re.findall(r'<h[1-5][^>]*>(.*?)</h[1-5]>', html)
print("Headings in Plugin Centre:")
for h in headings:
    print(" ", re.sub(r'<[^>]+>', '', h).strip())

# Check for plugin features requested in prompt:
features = [
    "discovery", "categories", "search", "featured", "plugin cards", 
    "detail", "connected", "oauth", "api", "permission", 
    "reconnect", "disconnect", "test connection", "activity", "error", "workflow"
]
print("\nPlugin Centre Features Check:")
for feat in features:
    matches = len(re.findall(feat, html, re.IGNORECASE))
    print(f"  {feat}: {matches} matches")
