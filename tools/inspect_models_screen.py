import os
import re

p = r"T:\ai creation\stitch_neural_command_desktop_os\screen_04_intelligence_ai_models\code.html"
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

headings = re.findall(r'<h[1-5][^>]*>(.*?)</h[1-5]>', html)
print("Headings in screen 04:")
for h in headings:
    print(" ", re.sub(r'<[^>]+>', '', h).strip())

# Check for local models and online models
print("\nModel mentions:")
for m in ["qwen", "nemotron", "llama", "mistral", "deepseek", "whisper", "claude", "gemini", "gpt", "groq", "ollama", "vllm", "concurrency", "unload", "ram"]:
    matches = len(re.findall(m, html, re.IGNORECASE))
    print(f"  {m}: {matches} occurrences")

# Check for Concurrency Policy / Worker models
print("\nConcurrency policy check:")
for phrase in ["local worker", "online worker", "main ai", "concurrency", "single authority", "idle", "timeout"]:
    found = phrase in html.lower()
    print(f"  '{phrase}': {'FOUND' if found else 'NOT FOUND'}")
