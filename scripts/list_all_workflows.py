import os

wf_dir = 'workflows'
files = [f for f in os.listdir(wf_dir) if f.endswith('.json')]
print(f"Total .json files in {wf_dir}: {len(files)}")
for i, f in enumerate(sorted(files), 1):
    fp = os.path.join(wf_dir, f)
    print(f"{i:02d}. {f} ({os.path.getsize(fp)} bytes)")
