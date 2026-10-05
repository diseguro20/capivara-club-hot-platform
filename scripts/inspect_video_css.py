with open("area_membros.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['video', 'tutorial', 'workflow', 'download']):
        start = max(0, i - 5)
        end = min(len(lines), i + 15)
        print(f"--- Line {i+1} ---")
        print("".join(lines[start:end]))
        print("="*50)
