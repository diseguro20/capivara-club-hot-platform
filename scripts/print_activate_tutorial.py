with open('member-scripts/area_membros_esteira_interna_ferramentas-1.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

idx = js.find('function activateTutorialPlayer')
if idx != -1:
    print(js[idx:idx+1500].encode('ascii', errors='backslashreplace').decode('ascii'))
