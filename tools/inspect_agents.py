import os
import re

p = r"T:\ai creation\stitch_neural_command_desktop_os\screen_06_agent_workspace\code.html"
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

# Look for agent cards and titles
headings = re.findall(r'<h[1-5][^>]*>(.*?)</h[1-5]>', html)
print("All Headings in screen 06:")
for h in headings:
    print(" ", re.sub(r'<[^>]+>', '', h).strip())

# Look for titles inside agent cards
agent_matches = re.findall(r'font-headline-sm[^>]*>(.*?)<', html)
print("\nAgent Names / Titles:")
for a in agent_matches:
    cleaned = a.strip()
    if cleaned and len(cleaned) < 40 and not cleaned.startswith('&'):
        print(f"  * {cleaned}")

# Check which of the 15 intended agents exist
intended_agents = [
    "Main AI / Manager", "Coder", "Designer", "Researcher", "Writer", 
    "Messenger", "File Manager", "Game Helper", "Tester", "3D Artist", 
    "Automator", "Security", "Data Analyst", "Code Reviewer", "Assistant"
]
print("\nChecking for intended 15 agents in HTML text:")
lower_html = html.lower()
for agent in intended_agents:
    found = agent.lower() in lower_html
    print(f"  {agent}: {'FOUND' if found else 'MISSING'}")
