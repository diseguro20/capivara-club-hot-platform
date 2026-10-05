import os
import json
import glob

downloads = r"c:\Users\diseg\Downloads"

workflow_files = [
    "CAPIVARA DU HOT - GERAR VÍDEOS PROMPT.json",
    "CONTROLMOTION 2 - CAPIVARA DUHOT - VIDEO +18.json",
    "controlmotion-capivara-duhot.json",
    "faceswap-capivara-duhot.json",
    "SWAP - FLUX - CAPIVARA.json",
    "TROCA DE ROUPA - WF GRATIS.json",
    "UPSCALE IMG - CAPIVARA (GRÁTIS).json",
    "VARIOS ANGULOS.json",
    "KREA 2 - ROSTO + PROMPT.json",
    "MOTION+CONTROL+v7.json"
]

for fname in workflow_files:
    path = os.path.join(downloads, fname)
    if not os.path.exists(path):
        candidates = glob.glob(os.path.join(downloads, f"*{fname[:10]}*"))
        if candidates:
            path = candidates[0]
        else:
            continue
    print("="*60)
    print("WORKFLOW:", os.path.basename(path))
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        if 'nodes' in data:
            for node in data['nodes']:
                t = node.get('title') or node.get('type')
                # check notes or prompt text
                if 'widgets_values' in node:
                    for val in node['widgets_values']:
                        if isinstance(val, str) and len(val) > 20 and not val.endswith(('.safetensors', '.ckpt', '.pth', '.bin')):
                            print(f"  [{t}]: {val[:200]}")
    except Exception as e:
        print("Error:", e)
