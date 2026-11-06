import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

search_roots = [
    r"c:\Users\diseg\Downloads",
    r"c:\Users\diseg\Desktop",
    r"c:\Users\diseg\Documents",
    r"C:\Users\diseg\.gemini\antigravity\brain"
]

found_keys = []

for sroot in search_roots:
    if not os.path.exists(sroot): continue
    for root, dirs, files in os.walk(sroot):
        if any(skip in root for skip in ['.git', 'node_modules']): continue
        for f in files:
            if f.endswith(('.env', '.local', '.txt', '.json', '.js', '.ts', '.mjs', '.jsonl')):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                        # look for uuid-like or hex-like keys near omega
                        if 'omega' in content.lower():
                            matches = re.findall(r'(?:OMEGA[A-Z_]*|public[-_]?key|secret[-_]?key)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{16,})["\']?', content, re.I)
                            if matches:
                                for m in matches:
                                    found_keys.append((fp, m))
                except Exception:
                    pass

print(f"Total key matches found: {len(found_keys)}")
seen = set()
for fp, k in found_keys:
    if k not in seen:
        seen.add(k)
        print(f"File: {fp} | Key: {k[:8]}...{k[-4:]}")
