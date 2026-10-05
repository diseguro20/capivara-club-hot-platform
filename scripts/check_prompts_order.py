import json

with open('member-assets/member_prompts_18.json', 'r', encoding='utf-8') as f:
    prompts = json.load(f)

print('Total prompts:', len(prompts))
for i in range(20):
    p = prompts[i]
    img = p.get('imagem_arquivo', '')
    txt = p.get('texto', '')
    title = p.get('titulo', '')
    ordem = p.get('ordem')
    print(f"[{i+1:03d}] img={img} | ordem={ordem} | title={title} | text={txt[:60]}...")
