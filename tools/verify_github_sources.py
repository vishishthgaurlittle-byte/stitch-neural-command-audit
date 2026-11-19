import urllib.request
import json
import subprocess
import os

proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
out, _ = proc.communicate('protocol=https\nhost=github.com\n')
creds = dict(line.split('=', 1) for line in out.strip().splitlines() if '=' in line)
token = creds.get('password')

headers = {
    'Authorization': f'token {token}',
    'User-Agent': 'Python-Verification-Agent'
}

repo = 'vishishthgaurlittle-byte/stitch-neural-command-audit'
base_url = f'https://api.github.com/repos/{repo}/contents/design-source'

def get_contents(path=''):
    url = f'{base_url}/{path}' if path else base_url
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)

local_root = r'T:\ai creation\stitch_neural_command_desktop_os'
verification_results = []

items = get_contents()
for item in items:
    if item['type'] == 'dir':
        dir_items = get_contents(item['name'])
        for f in dir_items:
            rel = f"{item['name']}/{f['name']}"
            local_path = os.path.join(local_root, rel.replace('/', '\\'))
            local_size = os.path.getsize(local_path)
            gh_size = f['size']
            status = 'VERIFIED_MATCH' if local_size == gh_size else 'SIZE_MISMATCH'
            verification_results.append((rel, local_size, gh_size, f['html_url'], f['download_url'], status))
    else:
        rel = item['name']
        local_path = os.path.join(local_root, rel.replace('/', '\\'))
        local_size = os.path.getsize(local_path)
        gh_size = item['size']
        status = 'VERIFIED_MATCH' if local_size == gh_size else 'SIZE_MISMATCH'
        verification_results.append((rel, local_size, gh_size, item['html_url'], item['download_url'], status))

print(f"Total items checked on GitHub: {len(verification_results)}")
all_matched = True
for r in verification_results:
    print(f"  {r[0]}: Local={r[1]} bytes, GitHub={r[2]} bytes -> {r[5]}")
    if r[5] != 'VERIFIED_MATCH':
        all_matched = False

print("\nAll files verified match:", all_matched)

# Direct HTTP fetch of all 15 HTML files + DESIGN.md
print("\nFetching each file directly via HTTP...")
html_fetch_success = 0
for r in verification_results:
    if r[0].endswith('.html') or r[0].endswith('.md'):
        req2 = urllib.request.Request(r[4], headers=headers)
        with urllib.request.urlopen(req2) as resp:
            data = resp.read()
            if len(data) == r[1]:
                html_fetch_success += 1
            else:
                print(f"Fetch size mismatch for {r[0]}: expected {r[1]}, got {len(data)}")

print(f"Successfully fetched and verified {html_fetch_success} text/HTML files directly from GitHub!")
