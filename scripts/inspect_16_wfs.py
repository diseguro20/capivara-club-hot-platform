import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

wf_dir = 'workflows'
for f in sorted(os.listdir(wf_dir)):
    if not f.endswith('.json'): continue
    fp = os.path.join(wf_dir, f)
    size = os.path.getsize(fp)
    try:
        with open(fp, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
        keys = list(data.keys()) if isinstance(data, dict) else [f"array_len_{len(data)}"]
        print(f"File: {f} | Size: {size} bytes | Keys/Nodes count: {len(keys)}")
    except Exception as e:
        print(f"File: {f} | Size: {size} bytes | Error: {e}")
