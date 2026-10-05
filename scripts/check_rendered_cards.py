import subprocess, re

res = subprocess.run([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--headless=new', '--dump-dom', 'http://localhost:5500/paginas/painel.html'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
html = res.stdout

start = html.find('id="gallery18Grid"')
end = html.find('id="gallery18Previous"')
grid_html = html[start:end]

cards = re.findall(r'<article class="gallery-card[^"]*"[^>]*>', grid_html)
print('Total cards rendered in gallery18Grid:', len(cards))
for i in [0, 1, 2, 10, 50, 100, 200, 500]:
    if i < len(cards):
        print(f'Card {i+1}: {cards[i][:150]}...')
