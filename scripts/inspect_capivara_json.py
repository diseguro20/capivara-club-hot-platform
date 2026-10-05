import os
import json
import glob

downloads = r"c:\Users\diseg\Downloads"
for pattern in ["*CAPIVARA*", "*capivara*", "*HOT*", "*hot*", "*SWAP*", "*CONTROLMOTION*", "*ROUPA*", "*UPSCALE*"]:
    for f in glob.glob(os.path.join(downloads, pattern)):
        if f.endswith('.json'):
            print("="*60)
            print("FILE:", os.path.basename(f), f"({os.path.getsize(f)} bytes)")
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as jf:
                    data = json.load(jf)
                if isinstance(data, dict):
                    # Check if it has nodes or workflow info
                    print("Total keys/nodes:", len(data))
                    for k, node in list(data.items())[:20]:
                        if isinstance(node, dict) and 'inputs' in node:
                            for inp_k, inp_v in node['inputs'].items():
                                if isinstance(inp_v, str) and ('prompt' in inp_k.lower() or 'text' in inp_k.lower() or len(inp_v) > 30):
                                    print(f"  [Node {k} - {node.get('class_type')}]: {inp_k} = {inp_v}")
            except Exception as e:
                print("Error reading:", e)
