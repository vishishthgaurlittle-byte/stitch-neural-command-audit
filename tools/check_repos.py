import urllib.request, json, subprocess

proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
out, _ = proc.communicate('protocol=https\nhost=github.com\n')
creds = dict(line.split('=', 1) for line in out.strip().splitlines() if '=' in line)
token = creds.get('password')

req = urllib.request.Request('https://api.github.com/user/repos?per_page=100&sort=updated', headers={
    'Authorization': f'token {token}',
    'User-Agent': 'Python-Git-Audit'
})
with urllib.request.urlopen(req) as resp:
    repos = json.load(resp)
    for r in repos:
        print(f"{r['name']} | URL: {r['html_url']} | Desc: {r['description']} | Updated: {r['updated_at']}")
