import os, json

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 1. Generate member_prompts_18.js
p18_json = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts_18.json')
p18_js = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts_18.js')
if os.path.exists(p18_json):
    with open(p18_json, 'r', encoding='utf-8') as f:
        data_18 = json.load(f)
    with open(p18_js, 'w', encoding='utf-8') as f:
        f.write('window.DMCN_PROMPTS_18 = ' + json.dumps(data_18, ensure_ascii=False) + ';\n')
    print(f"Generated {p18_js} ({len(data_18)} items, {os.path.getsize(p18_js)} bytes)")

# 2. Generate member_prompts.js
p_json = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts.json')
p_js = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts.js')
if os.path.exists(p_json):
    with open(p_json, 'r', encoding='utf-8') as f:
        data_p = json.load(f)
    with open(p_js, 'w', encoding='utf-8') as f:
        f.write('window.DMCN_PROMPTS = ' + json.dumps(data_p.get('prompts', []), ensure_ascii=False) + ';\n')
    print(f"Generated {p_js} ({len(data_p.get('prompts', []))} items, {os.path.getsize(p_js)} bytes)")
